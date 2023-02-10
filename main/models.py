from django.db import models
from django.utils.translation import gettext_lazy
from django.utils import timezone
import datetime


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
        
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=False)
    
    def __str__(self) -> str:
        return f'Vehicle(id={self.id}, name={self.name})'


class PartType(models.Model):
    name = models.CharField(max_length=64, null=False)

    def __str__(self) -> str:
        return f'PartType(name={self.name})'


class PartBase(models.Model):
    # The parts OTHER, and the ones with specific models have to exists from the get-go

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    part_type = models.ForeignKey(PartType, on_delete=models.CASCADE)
    info = models.CharField(max_length=128, null=False, default='')
    text = models.TextField(null=False, default='')

    max_mileage = models.PositiveIntegerField(null=True) # in kilometers, of course
    curr_mileage = models.PositiveIntegerField(default=0)
    max_time = models.DurationField(null=True)
    curr_time = models.DurationField(default=datetime.timedelta())

    install_date = models.DateField(default=timezone.now)
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
    

