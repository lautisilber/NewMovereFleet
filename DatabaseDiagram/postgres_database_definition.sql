CREATE TABLE "Company" (
  "id" integer PRIMARY KEY,
  "name" varchar(64) UNIQUE NOT NULL,
  "info" varchar(128)
);

CREATE TABLE "Vehicle" (
  "id" integer PRIMARY KEY,
  "name" varchar(64) UNIQUE NOT NULL,
  "info" varchar(128),
  "km" positiveinteger NOT NULL,
  "fuel" positiveinteger NOT NULL,
  "company" integer
);

CREATE TABLE "PartAbsProxy" (
  "id" integer PRIMARY KEY,
  "content_type" "Content type",
  "object_id" integer,
  "content_object" "content object"
);

CREATE TABLE "PartWithLifespanAbs" (
  "id" integer PRIMARY KEY,
  "name" varchar(64) UNIQUE NOT NULL,
  "info" varchar(128),
  "proxy" integer,
  "change_frequency_timedelta" timedelta,
  "change_frequency_km" positiveinteger
);

CREATE TABLE "PartTyreAbs" (
  "id" integer PRIMARY KEY,
  "name" varchar(64) UNIQUE NOT NULL,
  "info" varchar(128),
  "proxy" integer,
  "change_frequency_timedelta" timedelta,
  "change_frequency_km" positiveinteger,
  "recaped" bool NOT NULL
);

CREATE TABLE "PartWithoutLifespanAbs" (
  "id" integer PRIMARY KEY,
  "name" varchar(64) UNIQUE NOT NULL,
  "info" varchar(128),
  "proxy" integer
);

CREATE TABLE "PartProxy" (
  "id" integer PRIMARY KEY,
  "content_type" "Content type",
  "object_id" integer,
  "content_object" "content object",
  "vehicle" integer
);

CREATE TABLE "PartWithLifespan" (
  "id" integer PRIMARY KEY,
  "name" varchar(64) UNIQUE NOT NULL,
  "info" varchar(128),
  "proxy" integer,
  "last_changed_datetime" datetime,
  "last_changed_km" positiveinteger,
  "functionality" varchar(2) NOT NULL,
  "update_info" bool NOT NULL,
  "part_abs" integer,
  "change_frequency_timedelta" timedelta,
  "change_frequency_km" positiveinteger
);

CREATE TABLE "PartTyre" (
  "id" integer PRIMARY KEY,
  "name" varchar(64) UNIQUE NOT NULL,
  "info" varchar(128),
  "proxy" integer,
  "last_changed_datetime" datetime,
  "last_changed_km" positiveinteger,
  "functionality" varchar(2) NOT NULL,
  "update_info" bool NOT NULL,
  "part_abs" integer,
  "change_frequency_timedelta" timedelta,
  "change_frequency_km" positiveinteger,
  "recaped" bool NOT NULL
);

CREATE TABLE "PartWithoutLifespan" (
  "id" integer PRIMARY KEY,
  "name" varchar(64) UNIQUE NOT NULL,
  "info" varchar(128),
  "proxy" integer,
  "last_changed_datetime" datetime,
  "last_changed_km" positiveinteger,
  "functionality" varchar(2) NOT NULL,
  "update_info" bool NOT NULL,
  "part_abs" integer
);

CREATE TABLE "User" (
  "id" integer PRIMARY KEY,
  "username" varchar(64) UNIQUE NOT NULL
);

CREATE TABLE "Profile" (
  "id" integer PRIMARY KEY,
  "user" integer,
  "info" varchar(128),
  "position_type" varchar(1) NOT NULL
);

CREATE TABLE "PartChangeNotice" (
  "id" integer PRIMARY KEY,
  "issued_by" integer,
  "part" integer,
  "info" varchar(1024),
  "urgency_type" varchar(2) NOT NULL
);

CREATE TABLE "PartFix" (
  "id" integer PRIMARY KEY,
  "done_by" integer,
  "part" integer,
  "replaced" bool NOT NULL,
  "success" bool NOT NULL,
  "cost" positiveinteger
);

CREATE TABLE "QuestionGroup" (
  "id" integer PRIMARY KEY,
  "name" varchar(32) UNIQUE NOT NULL
);

CREATE TABLE "QuestionAbs" (
  "id" integer PRIMARY KEY,
  "question_group" integer,
  "title" varchar(128) NOT NULL,
  "info" varchar(256),
  "part" integer,
  "vehicle" integer,
  "question_type" varchar(1) NOT NULL,
  "answer_type" varchar(2) NOT NULL,
  "allows_observations" bool NOT NULL
);

CREATE TABLE "FormGroup" (
  "id" integer PRIMARY KEY,
  "name" varchar(32) UNIQUE NOT NULL
);

CREATE TABLE "FormAbs" (
  "id" integer PRIMARY KEY,
  "name" varchar(32) UNIQUE NOT NULL,
  "form_group" integer,
  "question_abs" integer,
  "vehicle" integer,
  "position_type" varchar(1) NOT NULL
);

CREATE TABLE "Form" (
  "id" integer PRIMARY KEY,
  "name" varchar(32) UNIQUE NOT NULL,
  "form_group" integer,
  "question_abs" integer,
  "vehicle" integer,
  "position_type" varchar(1) NOT NULL,
  "form_abs" integer,
  "completed_by" integer
);

CREATE TABLE "Question" (
  "id" integer PRIMARY KEY,
  "question_group" integer,
  "title" varchar(128) NOT NULL,
  "info" varchar(256),
  "part" integer,
  "vehicle" integer,
  "question_type" varchar(1) NOT NULL,
  "answer_type" varchar(2) NOT NULL,
  "allows_observations" bool NOT NULL,
  "question_abs" integer,
  "form" integer NOT NULL
);

COMMENT ON COLUMN "PartAbsProxy"."content_type" IS 'A link to the ContentType model that allows linking to any other object id';

COMMENT ON COLUMN "PartAbsProxy"."object_id" IS 'The id of the associated object';

COMMENT ON COLUMN "PartAbsProxy"."content_object" IS 'The associated object';

COMMENT ON COLUMN "PartWithLifespanAbs"."proxy" IS 'A link to a proxy that can be used to condense all PartAbs models';

COMMENT ON COLUMN "PartWithoutLifespanAbs"."proxy" IS 'A link to a proxy that can be used to condense all PartAbs models';

COMMENT ON COLUMN "PartProxy"."content_type" IS 'A link to the ContentType model that allows linking to any other object id';

COMMENT ON COLUMN "PartProxy"."object_id" IS 'The id of the associated object';

COMMENT ON COLUMN "PartProxy"."content_object" IS 'The associated object';

COMMENT ON COLUMN "PartWithLifespan"."proxy" IS 'A link to a proxy that can be used to condense all Part models';

COMMENT ON COLUMN "PartWithLifespan"."functionality" IS 'It"s an enum. Choices are (OK, WARNING, VERY_BAD, NOT_FUNCTIONAL)';

COMMENT ON COLUMN "PartWithLifespan"."update_info" IS 'If true, the data will be updated when the abstract part"s data is updated';

COMMENT ON COLUMN "PartTyre"."proxy" IS 'A link to a proxy that can be used to condense all Part models';

COMMENT ON COLUMN "PartTyre"."functionality" IS 'It"s an enum. Choices are (OK, WARNING, VERY_BAD, NOT_FUNCTIONAL)';

COMMENT ON COLUMN "PartTyre"."update_info" IS 'If true, the data will be updated when the abstract part"s data is updated';

COMMENT ON COLUMN "PartWithoutLifespan"."proxy" IS 'A link to a proxy that can be used to condense all Part models';

COMMENT ON COLUMN "PartWithoutLifespan"."functionality" IS 'It"s an enum. Choices are (OK, WARNING, VERY_BAD, NOT_FUNCTIONAL)';

COMMENT ON COLUMN "PartWithoutLifespan"."update_info" IS 'If true, the data will be updated when the abstract part"s data is updated';

COMMENT ON COLUMN "Profile"."position_type" IS 'An enum. Choices are (NOT_ASSIGNED, DRIVER, MECHANIC, ADMINISTRATOR, SUPERUSER)';

COMMENT ON COLUMN "PartChangeNotice"."urgency_type" IS 'An enum. Choices are (CRITICAL, IMPORTANT, EVENTUAL, NOTICE)';

COMMENT ON COLUMN "PartFix"."replaced" IS 'Was the part replaced or repared?';

COMMENT ON COLUMN "PartFix"."success" IS 'Was the fix successfull?';

COMMENT ON COLUMN "PartFix"."cost" IS 'How much did the fix cost';

COMMENT ON COLUMN "QuestionAbs"."question_type" IS 'An enum. Choices are (DAILY, MAINTENANCE)';

COMMENT ON COLUMN "QuestionAbs"."answer_type" IS 'An enum. Choices are (YES_NO, GOOD_REGULAR_BAD, NUMBER, TEXT)';

COMMENT ON COLUMN "FormAbs"."position_type" IS 'An enum. Choices are (NOT_ASSIGNED, DRIVER, MECHANIC, ADMINISTRATOR, SUPERUSER)';

COMMENT ON TABLE "Form" IS 'Inherits from FormAbs';

COMMENT ON COLUMN "Form"."position_type" IS 'An enum. Choices are (NOT_ASSIGNED, DRIVER, MECHANIC, ADMINISTRATOR, SUPERUSER)';

COMMENT ON TABLE "Question" IS 'Inherits from QuestionAbs';

COMMENT ON COLUMN "Question"."question_type" IS 'An enum. Choices are (DAILY, MAINTENANCE)';

COMMENT ON COLUMN "Question"."answer_type" IS 'An enum. Choices are (YES_NO, GOOD_REGULAR_BAD, NUMBER, TEXT)';

ALTER TABLE "Company" ADD FOREIGN KEY ("id") REFERENCES "Vehicle" ("company") ON DELETE RESTRICT ON UPDATE NO ACTION;

ALTER TABLE "PartAbsProxy" ADD FOREIGN KEY ("id") REFERENCES "PartWithLifespanAbs" ("proxy") ON DELETE SET NULL ON UPDATE NO ACTION;

ALTER TABLE "PartAbsProxy" ADD FOREIGN KEY ("id") REFERENCES "PartTyreAbs" ("proxy") ON DELETE SET NULL ON UPDATE NO ACTION;

ALTER TABLE "PartAbsProxy" ADD FOREIGN KEY ("id") REFERENCES "PartWithoutLifespanAbs" ("proxy") ON DELETE SET NULL ON UPDATE NO ACTION;

ALTER TABLE "Vehicle" ADD FOREIGN KEY ("id") REFERENCES "PartProxy" ("vehicle") ON DELETE CASCADE ON UPDATE NO ACTION;

ALTER TABLE "PartProxy" ADD FOREIGN KEY ("id") REFERENCES "PartWithLifespan" ("proxy") ON DELETE SET NULL ON UPDATE NO ACTION;

ALTER TABLE "PartWithLifespanAbs" ADD FOREIGN KEY ("id") REFERENCES "PartWithLifespan" ("part_abs") ON DELETE CASCADE ON UPDATE NO ACTION;

ALTER TABLE "PartProxy" ADD FOREIGN KEY ("id") REFERENCES "PartTyre" ("proxy") ON DELETE SET NULL ON UPDATE NO ACTION;

ALTER TABLE "PartTyreAbs" ADD FOREIGN KEY ("id") REFERENCES "PartTyre" ("part_abs") ON DELETE CASCADE ON UPDATE NO ACTION;

ALTER TABLE "PartProxy" ADD FOREIGN KEY ("id") REFERENCES "PartWithoutLifespan" ("proxy") ON DELETE SET NULL ON UPDATE NO ACTION;

ALTER TABLE "PartWithoutLifespanAbs" ADD FOREIGN KEY ("id") REFERENCES "PartWithoutLifespan" ("part_abs") ON DELETE CASCADE ON UPDATE NO ACTION;

ALTER TABLE "User" ADD FOREIGN KEY ("id") REFERENCES "Profile" ("user") ON DELETE CASCADE ON UPDATE NO ACTION;

ALTER TABLE "User" ADD FOREIGN KEY ("id") REFERENCES "PartChangeNotice" ("issued_by") ON DELETE SET NULL ON UPDATE NO ACTION;

ALTER TABLE "PartProxy" ADD FOREIGN KEY ("id") REFERENCES "PartChangeNotice" ("part") ON DELETE CASCADE ON UPDATE NO ACTION;

ALTER TABLE "User" ADD FOREIGN KEY ("id") REFERENCES "PartFix" ("done_by") ON DELETE SET NULL ON UPDATE NO ACTION;

ALTER TABLE "PartProxy" ADD FOREIGN KEY ("id") REFERENCES "PartFix" ("part") ON DELETE CASCADE ON UPDATE NO ACTION;

ALTER TABLE "QuestionGroup" ADD FOREIGN KEY ("id") REFERENCES "QuestionAbs" ("question_group") ON DELETE SET NULL ON UPDATE NO ACTION;

ALTER TABLE "PartProxy" ADD FOREIGN KEY ("id") REFERENCES "QuestionAbs" ("part") ON DELETE SET NULL ON UPDATE NO ACTION;

ALTER TABLE "Vehicle" ADD FOREIGN KEY ("id") REFERENCES "QuestionAbs" ("vehicle") ON DELETE SET NULL ON UPDATE NO ACTION;

ALTER TABLE "FormGroup" ADD FOREIGN KEY ("id") REFERENCES "FormAbs" ("form_group") ON DELETE SET NULL ON UPDATE NO ACTION;

ALTER TABLE "FormGroup" ADD FOREIGN KEY ("id") REFERENCES "Form" ("form_group") ON DELETE SET NULL ON UPDATE NO ACTION;

ALTER TABLE "FormAbs" ADD FOREIGN KEY ("id") REFERENCES "Form" ("form_abs") ON DELETE SET NULL ON UPDATE NO ACTION;

ALTER TABLE "User" ADD FOREIGN KEY ("id") REFERENCES "Form" ("completed_by") ON DELETE SET NULL ON UPDATE NO ACTION;

ALTER TABLE "QuestionGroup" ADD FOREIGN KEY ("id") REFERENCES "Question" ("question_group") ON DELETE SET NULL ON UPDATE NO ACTION;

ALTER TABLE "PartProxy" ADD FOREIGN KEY ("id") REFERENCES "Question" ("part") ON DELETE SET NULL ON UPDATE NO ACTION;

ALTER TABLE "Vehicle" ADD FOREIGN KEY ("id") REFERENCES "Question" ("vehicle") ON DELETE SET NULL ON UPDATE NO ACTION;

ALTER TABLE "QuestionAbs" ADD FOREIGN KEY ("id") REFERENCES "Question" ("question_abs") ON DELETE SET NULL ON UPDATE NO ACTION;

ALTER TABLE "Form" ADD FOREIGN KEY ("id") REFERENCES "Question" ("form") ON DELETE CASCADE ON UPDATE NO ACTION;
