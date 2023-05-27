from typing import Any, Optional, Union
from django.db import models
from django.contrib.auth.models import User
from user.models import Profile
from django.utils.translation import gettext_lazy
from datetime import datetime, timedelta, timezone
from django.db.models import signals



class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


### MACRO ###

class Company(models.Model):
    url_name = 'company'
    name = models.CharField(max_length=64, null=False, unique=True)
    info = models.CharField(max_length=256, null=True, blank=True)

    def __repr__(self) -> str:
        return f'Company(name={self.name})'
    
    def __str__(self) -> str:
        return self.name

# a vehicle is made out of parts
# there are two kinds of parts
# 1
#   parts that need constant replacement and are supposed to be changed once in a while
# 2
#   parts that are not supposed to break but sometimes do
# in addition to this, vehicles have quantities that need to be tracked, which are
# part of hte vehicle model itself 

class Vehicle(models.Model):
    url_name = 'vehicle'
    name = models.CharField(max_length=128, null=False, unique=True)
    mileage = models.PositiveIntegerField(default=0)
    fuel = models.PositiveSmallIntegerField(default=0)
        
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=False, blank=False)
    
    def __repr__(self) -> str:
        return f'Vehicle(id={self.id}, name={self.name})'
    
    def __str__(self) -> str:
        return self.name


### QUESTIONS ###

class QuestionType(models.Model):
    name = models.CharField(max_length=16, unique=True, null=False, blank=False)
    periodicity = models.BooleanField(default=False, null=False, blank=False)

    def __repr__(self) -> str:
        return f"QuestionType(name='{self.name}', periodicity={self.periodicity})"
    
    def __str__(self) -> str:
        return self.name


class QuestionTemplate(models.Model):
    url_name = 'checklist_question_template'

    question = models.CharField(max_length=32, null=False, blank=False)
    info = models.CharField(max_length=256, null=True, blank=True)
    allow_notes = models.BooleanField(default=False, null=False, blank=True)
    vehicles = models.ManyToManyField(Vehicle, blank=True, related_name='question_templates', related_query_name='question_templates')
    question_types = models.ManyToManyField(QuestionType, blank=True, related_name='question_templates', related_query_name='question_templates')
    position_type = models.SmallIntegerField(choices=Profile.PositionType.choices, default=Profile.PositionType.NOT_ASSIGNED, null=False) # TODO: no anda

    periodicity_days = models.IntegerField(default=0, null=False, blank=True) # cada cuantos dias debe ser completado. 0 significa que debe ser administrado por la persona que complete
    periodicity_anchor = models.DateField(null=True, blank=True) # a day to start counting from. if the periodicity is daily (periodicity_days = 0) this has no effect
    periodicity_days_notice = models.IntegerField(default=1, null=False, blank=True) # cuantos dias de changui para la persona que complete

    def should_be_instantiated(self, question_types: Optional[list[QuestionType]]=None, now_utc: Optional[datetime]=None) -> tuple[bool, Union[int, None]]:
        if question_types is None:
            question_types = list(QuestionType.objects.all())
        if self.question_types.exists():
            intersection_question_types = [qt for qt in list(self.question_types.all()) if qt in question_types]
            if any(not qt.periodicity for qt in intersection_question_types): # has a type that doesn't take into account periodicity
                return True, None
        if now_utc is None:
            now_utc = datetime.now(timezone.utc)
        now_utc = now_utc.date()
        dt_absolute = now_utc - self.periodicity_anchor
        dt_absolute_days = dt_absolute.days

        if self.periodicity_days <= 0:
            return True, dt_absolute_days

        instantiate = any((dt_absolute_days + i) % self.periodicity_days == 0 for i in range(min(self.periodicity_days_notice, 1))) # true if we are in the period this question should be instatiated
        n_instances = dt_absolute_days // self.periodicity_days # number of times this should have been called

        return instantiate, n_instances

    def __repr__(self) -> str:
        return f'QuestionTemplate(id={self.id}, question="{self.question}", allow_notes={self.allow_notes})'
    
    def __str__(self) -> str:
        return f'Question tempate "{self.question}"'


class AnswerSession(TimeStampMixin):
    user = models.ForeignKey(User, models.CASCADE, null=False, blank=False)
    vehicle = models.ForeignKey(Vehicle, models.CASCADE, null=False, blank=False, related_name='answer_sessions', related_query_name='answer_sessions')
    question_type = models.ForeignKey(QuestionType, models.SET_NULL, null=True, blank=False)
    question_templates = models.ManyToManyField(QuestionTemplate, blank=True, related_name='answer_sessions', related_query_name='answer_sessions')
    complete = models.BooleanField(null=False, blank=True, default=False)

    def __repr__(self) -> str:
        return f'AnswerSession(question_template_ids={[qt.id for qt in self.question_templates.all()]}, question_type={self.question_type}, completed={self.complete})'
    
    def __str__(self) -> str:
        return f'Answer session {self.id}'


class QuestionInstance(TimeStampMixin):
    url_name = 'checklist_question_instance'

    question = models.CharField(max_length=32, null=False, blank=False)
    question_template = models.ForeignKey(QuestionTemplate, models.SET_NULL, null=True, blank=False)
    vehicle = models.ForeignKey(Vehicle, models.SET_NULL, null=True, blank=False, related_name='question_instances', related_query_name='question_instances')
    user = models.ForeignKey(User, models.SET_NULL, null=True, blank=False)
    answer = models.BooleanField(null=False, default=None)
    problem_description = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    answer_session = models.ForeignKey(AnswerSession, on_delete=models.CASCADE, null=True, related_name='question_instances', related_query_name='question_instances')

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        if self.question_template is None:
            #raise Exception("Can't instantiate QuestionInstance without a QuestionTemplate parameter")
            self.question = None
            self.position_type = None
        else:
            self.question = self.question_template.question
            self.position_type = self.question_template.position_type

    def __repr__(self) -> str:
        return f'QuestionInstance(id={self.id}, title={self.question_template.question if self.question_template else "None"}, answer={self.answer})'
    
    def __str__(self) -> str:
        return f'Question instance "{self.question}"'


def create_question_instance(question_template: QuestionTemplate, vehicle: Vehicle, user: User) -> QuestionInstance:
    question_instance = QuestionInstance(question_template=question_template, vehicle=vehicle, user=user)
    return question_instance

def add_question_instance_to_session(answer_session: AnswerSession, question_template: QuestionTemplate) -> QuestionInstance:
    question_instance = create_question_instance(question_template, answer_session.vehicle, answer_session.user)
    question_instance.answer_session = answer_session
    return question_instance

def create_answer_session(user: User, vehicle: Vehicle, question_type: int, now_utc: Optional[datetime]=None) -> AnswerSession:
    question_templates = QuestionTemplate.objects.filter(position_type=user.profile.position_type, vehicles=vehicle, question_types__in=[question_type]).all()
    question_templates = [question_template for question_template in question_templates if question_template.should_be_instantiated(now_utc=now_utc)[0]]
    session = AnswerSession(user=user, vehicle=vehicle, question_type=question_type)
    session.save() # for the relationships to work
    session.question_templates.add(*question_templates)
    return session


def delete_question_template(sender, instance, using, **kwargs):
    AnswerSession.objects.filter(question_templates__id=instance.id).delete()

# def delete_answer_session(sender, instance, using, **kwargs):
#     QuestionInstance.objects.filter(answer_session=instance).delete()

signals.pre_delete.connect(delete_question_template, sender=QuestionTemplate, weak=False, dispatch_uid='main.models.delete_question_template')
# signals.pre_delete.connect(delete_answer_session, sender=AnswerSession, weak=False, dispatch_uid='main.models.delete_answer_session')


### PARTS ###

# class PartType(models.Model):
#     url_name = 'part_type'
#     name = models.CharField(max_length=64, null=False, unique=True)

#     def __str__(self) -> str:
#         return f'PartType(id={self.id}, name={self.name})'


# class PartBase(models.Model):
#     # The parts OTHER, and the ones with specific models have to exists from the get-go

#     vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=False, blank=False)
#     part_type = models.ForeignKey(PartType, on_delete=models.CASCADE, null=False, blank=False)
#     info = models.CharField(max_length=128, null=False, default='')
#     text = models.TextField(null=False, default='')

#     max_mileage = models.PositiveIntegerField(null=True) # in kilometers, of course
#     curr_mileage = models.PositiveIntegerField(default=0)
#     max_time = models.DurationField(null=True)
#     curr_time = models.DurationField(default=datetime.timedelta)

#     install_date = models.DateField(default=timezone.now, null=False)
#     # TODO: need to add repair dates, probably as foreignkeys to have a repair history

#     class Meta:
#         abstract = True

#     @staticmethod
#     def get_part_types() -> list[tuple[str, int]]:
#         return [(part.name, part.id) for part in Part.objects.all()]

#     def __str__(self) -> str:
#         return f'Part(id={self.id}, vehice_id={self.vehicle.id}, part_type={self.part_type.name})'


# class PartWheel(PartBase):
#     url_name = 'part_wheel'
#     number = models.PositiveSmallIntegerField(null=False, default=0)
#     refurbished = models.PositiveSmallIntegerField(null=False, default=0)


# class Part(PartBase):
#     pass
    

# ### REPAIRS ###

# class RepairBase(models.Model):
#     description = models.TextField()
#     issue_date = models.DateField(default=timezone.now, null=False)
#     completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
#     completion_date = models.DateField(default=None, null=True)

#     @property
#     def completed(self) -> bool:
#         return bool(self.completed_by)

#     class Meta:
#         abstract = True


# class Repair(RepairBase):
#     url_name = 'repair'
#     part = models.ForeignKey(Part, on_delete=models.CASCADE, null=False, blank=False)

#     def __str__(self) -> str:
#         return f'Repair(id={self.id}, part={self.part})'


# class RepairWheel(RepairBase):
#     url_name = 'repair_wheel'
#     part = models.ForeignKey(PartWheel, on_delete=models.CASCADE, null=False, blank=False)

#     def __str__(self) -> str:
#         return f'Repair(id={self.id}, part={self.part})'


# class QuestionType(models.IntegerChoices):
#     GENERIC = 2**0, gettext_lazy('Generic')
#     GET_ON = 2**1, gettext_lazy('Get on')
#     GET_OFF = 2**2, gettext_lazy('Get off')

#     @classmethod
#     def get_type_from_int(cls, n: int):
#         if n == 'g':
#             return cls.GENERIC
#         elif n == 'n':
#             return cls.GET_ON
#         elif n == 'f':
#             return cls.GET_OFF
#         raise Exception(f'No enum correspondance to {n}')
    
#     @classmethod
#     def min_val(cls) -> int:
#         return cls.GENERIC.value
    
#     @classmethod
#     def max_val(cls) -> int:
#         return sum(elem.value for elem in cls)
    
#     @staticmethod
#     def encode(values):
#         if not values:
#             return 0
#         return sum(v.value for v in values)
    
#     @classmethod
#     def decode(cls, number):
#         return [v for v in cls if number & v.value]

# class QuestionTypeField(models.IntegerField):
#     def __init__(self, *args, **kwargs) -> None:
#         super().__init__(default=[], null=False, blank=False, validators=[
#             validators.MaxValueValidator(QuestionType.max_val()),
#             validators.MinValueValidator(QuestionType.min_val())
#         ])

#     def get_prep_value(self, value):
#         # from python to database
#         if value is not None:
#             value = QuestionType.encode(value)
#         return super().get_prep_value(value)
    
#     def from_db_value(self, value, expression, connection, *args):
#         # from database to python
#         if value is None:
#             return None
#         if isinstance(value, int):
#             return QuestionType.decode(value)
#         else:
#             raise exceptions.ValidationError('Bad db typing')