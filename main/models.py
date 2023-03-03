from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy
from django.utils import timezone
import datetime


### GLOBALS ###

class Company(models.Model):
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
    name = models.CharField(max_length=128, null=False, unique=True)
    mileage = models.PositiveIntegerField(default=0)
    fuel = models.PositiveSmallIntegerField(default=0)


    class VehicleType(models.TextChoices):
        OTHER = 'XX', gettext_lazy('Other')
        MINI_VAN = 'MV', gettext_lazy('Mini van')
        TRUCK = 'TK', gettext_lazy('Truck')
        TRAILER = 'TR', gettext_lazy('Trailer')
        PICK_UP = 'PU', gettext_lazy('Pick-up truck')

    
    vehicle_type = models.CharField(max_length=2, choices=VehicleType.choices, default=VehicleType.OTHER, null=False)

    class DrivetrainType(models.TextChoices):
        OTHER = 'XXX', gettext_lazy('Other')
        SINGLE_SINGLE = '220', gettext_lazy('Two axles, both with two wheels')
        SINGLE_DOUBLE = '240', gettext_lazy('Two axles, one with two whels, one with four')
        SINGLE_SINGLE_SINGLE = '222', gettext_lazy('Three axles with two wheels')
        SINGLE_DOUBLE_SINGLE = '242', gettext_lazy('Three axles with two, three and two wheels')
        SINGLE_DOUBLE_DOUBLE = '244', gettext_lazy('Three axles, one with two wheels and two with three')
    
    drivetrain_type = models.CharField(max_length=3, choices=DrivetrainType.choices, default=DrivetrainType.OTHER, null=False)

    @classmethod
    def get_vehicle_types(cls) -> list[tuple[str, str]]:
        return cls.VehicleType.choices
    
    @classmethod
    def get_drivetrain_types(cls) -> list[tuple[str, str]]:
        return cls.DrivetrainType.choices
    
    def get_drivetrain_wheel_count(self) -> int:
        drivetrains = tuple(d[0] for d in self.__class__.get_drivetrain_types())
        if self.drivetrain_type == drivetrains[0]: # OTHER
            return -1
        elif self.drivetrain_type == drivetrains[1]: # SINGLE_SINGLE
            return 4
        elif self.drivetrain_type == drivetrains[2]: # SINGLE_DOUBLE
            return 6
        elif self.drivetrain_type == drivetrains[3]: # SINGLE_SINGLE_SINGLE
            return 6
        elif self.drivetrain_type == drivetrains[4]: # SINGLE_DOUBLE_SINGLE
            return 8
        elif self.drivetrain_type == drivetrains[5]: # SINGLE_DOUBLE_DOUBLE
            return 10
        else: # WTF!
            return 0
        
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=False, blank=False)
    
    def __str__(self) -> str:
        return f'Vehicle(id={self.id}, name={self.name})'


### PARTS ###

class PartType(models.Model):
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
    part = models.ForeignKey(Part, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self) -> str:
        return f'Repair(id={self.id}, part={self.part})'


class RepairWheel(RepairBase):
    part = models.ForeignKey(PartWheel, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self) -> str:
        return f'Repair(id={self.id}, part={self.part})'
    

### CHECKLISTS ###

class ChecklistQuestionBase(models.Model):

    class Meta:
        abstract = True

    title = models.CharField(max_length=32, null=False)
    text = models.CharField(max_length=256, null=False)

    class AnswerTypes(models.TextChoices):
        CHECKBOX = 'CB', gettext_lazy('Checkbox')
        RADIO_1_5 = 'R5', gettext_lazy('1-5')
        RADIO_1_10 = 'RX', gettext_lazy('1-10')
        TEXT = 'TX', gettext_lazy('Text')
        WHEEL = 'WL', gettext_lazy('Wheel')

    answer_type = models.CharField(max_length=2, choices=AnswerTypes.choices, default=AnswerTypes.CHECKBOX)
    allow_notes = models.BooleanField(default=True, null=False)


class ChecklistQuestionTemplate(ChecklistQuestionBase):

    def __str__(self) -> str:
        return f'ChecklistQuestionTemplate(id={self.id}, title={self.title}, answer_type={self.answer_type})'


class ChecklistQuestionInstance(ChecklistQuestionBase):
    answer_checkbox = models.BooleanField(null=True, default=None)
    answer_radio_5 = models.PositiveSmallIntegerField(null=True, default=None)
    answer_radio_10 = models.PositiveSmallIntegerField(null=True, default=None)
    answer_text = models.TextField(null=True, default=None)
    answer_wheel = models.CharField(max_length=16, null=True, default=None) # probably should be an encoded string
    notes = models.TextField(null=True)

    def __str__(self) -> str:
        return f'ChecklistQuestionInstance(id={self.id}, title={self.title}, answer_type={self.answer_type})'


class ChecklistBase(models.Model):

    class Meta:
        abstract = True

    name = models.CharField(max_length=64, null=False)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


class ChecklistTemplate(ChecklistBase):
    checklist_question_templates = models.ManyToManyField(ChecklistQuestionTemplate, blank=True)
    
    def __str__(self) -> str:
        v = self.vehicle.name if self.vehicle else False
        return f'ChecklistTemplate(id={self.id}, name={self.name}, vehicle={v})'


class ChecklistInstace(ChecklistBase):
    checklist_question_instances = models.ManyToManyField(ChecklistQuestionInstance, blank=True)
    completed = models.BooleanField(default=False, null=False)

    def __str__(self) -> str:
        v = self.vehicle.name if self.vehicle else False
        return f'ChecklistInstance(id={self.id}, name={self.name}, vehicle={v}, competed={self.completed})'