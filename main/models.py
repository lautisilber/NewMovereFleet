from django.db import models
from django.contrib.auth.models import User
from user.models import Profile
from django.utils.translation import gettext_lazy
from django.utils import timezone
import datetime


### GLOBALS ###

class Company(models.Model):
    url_name = 'company'
    name = models.CharField(max_length=64, null=False)

    def __str__(self) -> str:
        return f'Company(name={self.name})'

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
    
    def __str__(self) -> str:
        return f'Vehicle(id={self.id}, name={self.name})'


### PARTS ###

class PartType(models.Model):
    url_name = 'part_type'
    name = models.CharField(max_length=64, null=False, unique=True)

    def __str__(self) -> str:
        return f'PartType(id={self.id}, name={self.name})'


class PartBase(models.Model):
    # The parts OTHER, and the ones with specific models have to exists from the get-go

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=False, blank=False)
    part_type = models.ForeignKey(PartType, on_delete=models.CASCADE, null=False, blank=False)
    info = models.CharField(max_length=128, null=False, default='')
    text = models.TextField(null=False, default='')

    max_mileage = models.PositiveIntegerField(null=True) # in kilometers, of course
    curr_mileage = models.PositiveIntegerField(default=0)
    max_time = models.DurationField(null=True)
    curr_time = models.DurationField(default=datetime.timedelta)

    install_date = models.DateField(default=timezone.now, null=False)
    # TODO: need to add repair dates, probably as foreignkeys to have a repair history

    class Meta:
        abstract = True

    @staticmethod
    def get_part_types() -> list[tuple[str, int]]:
        return [(part.name, part.id) for part in Part.objects.all()]

    def __str__(self) -> str:
        return f'Part(id={self.id}, vehice_id={self.vehicle.id}, part_type={self.part_type.name})'


class PartWheel(PartBase):
    url_name = 'part_wheel'
    number = models.PositiveSmallIntegerField(null=False, default=0)
    refurbished = models.PositiveSmallIntegerField(null=False, default=0)


class Part(PartBase):
    pass
    

### REPAIRS ###

class RepairBase(models.Model):
    description = models.TextField()
    issue_date = models.DateField(default=timezone.now, null=False)
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    completion_date = models.DateField(default=None, null=True)

    @property
    def completed(self) -> bool:
        return bool(self.completed_by)

    class Meta:
        abstract = True


class Repair(RepairBase):
    url_name = 'repair'
    part = models.ForeignKey(Part, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self) -> str:
        return f'Repair(id={self.id}, part={self.part})'


class RepairWheel(RepairBase):
    url_name = 'repair_wheel'
    part = models.ForeignKey(PartWheel, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self) -> str:
        return f'Repair(id={self.id}, part={self.part})'
    

### CHECKLISTS ###

class ChecklistQuestionBase(models.Model):
    class Meta:
        abstract = True
    question = models.CharField(max_length=32, null=False)
    info = models.CharField(max_length=256, null=True, blank=True)


class ChecklistQuestionTemplate(ChecklistQuestionBase):
    url_name = 'checklist_question_template'
    vehicles = models.ManyToManyField(Vehicle, blank=True, null=True)
    periodicity_days = models.IntegerField(default=0, null=False, blank=True) # cada cuantos dias debe ser completado. 0 significa que debe ser administrado por la persona que complete
    periodicity_days_notice = models.IntegerField(default=0, null=False, blank=True) # cuantos dias de changui para la persona que complete
    position_type = models.SmallIntegerField(choices=Profile.PositionType.choices, default=Profile.PositionType.NOT_ASSIGNED, null=False) # TODO: no anda

    def __str__(self) -> str:
        return f'ChecklistQuestionTemplate(id={self.id}, question={self.question})'


class ChecklistInstace(models.Model):
    url_name = 'checklist_instance'
    name = models.CharField(max_length=64, null=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    #checklist_template = models.ForeignKey(ChecklistTemplate, models.SET_NULL, null=True)
    completed = models.BooleanField(default=False, null=False)
    completed_on = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return f'ChecklistInstance(id={self.id}, name={self.name}, competed={self.completed})'


class ChecklistQuestionInstance(ChecklistQuestionBase):
    url_name = 'checklist_question_instance'
    checklist_question_template = models.ForeignKey(ChecklistQuestionTemplate, models.SET_NULL, null=True)
    checklist_instance = models.ForeignKey(ChecklistInstace, models.SET_NULL, null=True)
    answer = models.BooleanField(null=True, default=None)
    notes = models.TextField(null=True)

    def __str__(self) -> str:
        return f'ChecklistQuestionInstance(id={self.id}, title={self.title}, answer={self.answer})'


# class ChecklistBase(models.Model):
#     class Meta:
#         abstract = True

#     name = models.CharField(max_length=64, null=False)
#     vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
#     assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


# class ChecklistTemplate(ChecklistBase):
#     url_name = 'checklist_template'
#     checklist_question_templates = models.ManyToManyField(ChecklistQuestionTemplate, blank=True)
    
#     def __str__(self) -> str:
#         v = self.vehicle.name if self.vehicle else False
#         return f'ChecklistTemplate(id={self.id}, name={self.name}, vehicle={v})'
