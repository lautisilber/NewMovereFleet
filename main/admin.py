from django.contrib import admin

from .models import \
    (Company,
     Vehicle,
     PartWithLifespanAbs,
     PartTyreAbs,
     PartWithoutLifespanAbs,
     PartWithLifespan,
     PartTyre,
     PartWithoutLifespan,
     PartChangeNotice,
     PartFix,
     FormGroup,
     FormAbs,
     Form,
     QuestionGroup,
     QuestionAbs,
     Question)

for cls in (Company, Vehicle, PartWithLifespanAbs, PartTyreAbs, PartWithoutLifespanAbs,
            PartWithLifespan, PartTyre, PartWithoutLifespan, PartChangeNotice, PartFix,
            FormGroup, FormAbs, Form, QuestionGroup, QuestionAbs, Question):
    admin.site.register(cls)
