from typing import Any, Optional, Union
from django.db import models
from django.contrib.auth.models import User
from user.models import Profile
from django.utils.translation import gettext_lazy
from django.utils import timezone
from django.db.models import signals
from polymorphic.models import PolymorphicModel
# PolymorphicModel replaces models.Model. It allows the following interaction:
#
#    class Project(PolymorphicModel):
#        topic = models.CharField(max_length=30)
#    
#    class ArtProject(Project):
#        artist = models.CharField(max_length=30)
#    
#    class ResearchProject(Project):
#        supervisor = models.CharField(max_length=30)
#    
#    >>> Project.objects.create(topic="Department Party")
#    >>> ArtProject.objects.create(topic="Painting with Tim", artist="T. Turner")
#    >>> ResearchProject.objects.create(topic="Swallow Aerodynamics", supervisor="Dr. Winter")
#    
#    >>> Project.objects.all()
#    [ <Project:         id 1, topic "Department Party">,
#      <ArtProject:      id 2, topic "Painting with Tim", artist "T. Turner">,
#      <ResearchProject: id 3, topic "Swallow Aerodynamics", supervisor "Dr. Winter"> ]


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class TimeStampMixinPolymorphic(PolymorphicModel):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


### MACRO ###

class Company(TimeStampMixin):
    url_name = 'company'
    name = models.CharField(max_length=64, null=False, unique=True, blank=False)
    info = models.CharField(max_length=256, null=True, blank=True)

    def __repr__(self) -> str:
        return f'Company(name={self.name})'
    
    def __str__(self) -> str:
        return self.name

class Vehicle(TimeStampMixin):
    class Meta:
        default_related_name = 'vehicles'

    url_name = 'vehicle'
    name = models.CharField(max_length=64, null=False, unique=True, blank=False)
    info = models.CharField(max_length=256, null=True, blank=True)
    km = models.PositiveIntegerField(default=0, null=False, blank=False)
    fuel = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
        
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=False, blank=False, related_name='a1', related_query_name='a2')
    
    def __repr__(self) -> str:
        return f'Vehicle(id={self.id}, name={self.name})'
    
    def __str__(self) -> str:
        return self.name
    
### PARTS ###
    
class PartAbs(TimeStampMixinPolymorphic):
    # should be meta, but is not, so that it can have relationships and, with polymorphic, act as a base class
    # https://stackoverflow.com/questions/30343212/foreignkey-field-related-to-abstract-model-in-django

    # class Meta:
    #     abstract = True

    name = models.CharField(max_length=64, null=False, unique=True, blank=False)
    info = models.CharField(max_length=128, null=True, blank=True)

class PartWithLifespanAbs(PartAbs):
    change_frequency_timedelta = models.DurationField(null=True, blank=True)
    change_frequency_km = models.PositiveIntegerField(null=True, blank=True)

    def __repr__(self) -> str:
        return f'PartWithLifespanAbs(name={self.name})'
    
    def __str__(self) -> str:
        return self.__repr__()
    
class PartTyreAbs(PartAbs):
    change_frequency_timedelta = models.DurationField(null=True, blank=True)
    change_frequency_km = models.PositiveIntegerField(null=True, blank=True)

    def __repr__(self) -> str:
        return f'PartTyreAbs(name={self.name})'
    
    def __str__(self) -> str:
        return self.__repr__()

class PartWithoutLifespanAbs(PartAbs):
    def __repr__(self) -> str:
        return f'PartTyreAbs(name={self.name})'
    
    def __str__(self) -> str:
        return self.__repr__()


class Part(TimeStampMixinPolymorphic):
    # should be meta, but is not, so that it can have relationships and, with polymorphic, act as a base class
    # https://stackoverflow.com/questions/30343212/foreignkey-field-related-to-abstract-model-in-django

    class Meta:
        # abstract = True
        default_related_name = 'parts'

    class Functionality(models.TextChoices):
        OK = 'OK', gettext_lazy('OK')
        WARNING = 'WR', gettext_lazy('Atención')
        VER_YBAD = 'VB', gettext_lazy('Muy Mala')
        NOT_FUNCTIONAL = 'NF', gettext_lazy('No Funciona')

    name = models.CharField(max_length=64, null=False, unique=True, blank=False)
    info = models.CharField(max_length=128, null=True, blank=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=False, blank=False, related_name='b1', related_query_name='b2')
    last_changed_datetime = models.DateTimeField(null=False, blank=True, default=timezone.now) # the date this part was last changed (of the vehicle)
    last_changed_km = models.PositiveIntegerField(null=False, blank=True, default=0) # the vehicle km at which this part was changed
    functionality = models.CharField(max_length=2, choices=Functionality.choices, default=Functionality.OK, null=False, blank=False)
    update_info = models.BooleanField(null=False, blank=False, default=True) # if True, the part's data will be updated when the PartAbs's data does

class PartWithLifespan(Part):
    class Meta:
        default_related_name = 'parts_with_lifespan'

    abstract_part = models.ForeignKey(PartWithLifespanAbs, on_delete=models.CASCADE, null=False, blank=True, related_name='c1', related_query_name='c2')
    change_frequency_timedelta = models.DurationField(null=True, blank=True)
    change_frequency_km = models.PositiveIntegerField(null=True, blank=True)

    @property
    def should_change(self) -> bool:
        should_change_time = False
        should_change_km = False
        if self.change_frequency_timedelta:
            should_change_time = timezone.now() - self.last_changed_datetime > self.change_frequency_timedelta
        if self.change_frequency_km:
            should_change_km = self.vehicle.km - self.last_changed_km > self.change_frequency_km
        return should_change_time or should_change_km

    def __repr__(self) -> str:
        return f'PartWithLifespan(name={self.name}, should_change={self.should_change})'
    
    def __str__(self) -> str:
        return self.__repr__()

class PartTyre(Part):
    class Meta:
        default_related_name = 'parts_tyre'

    abstract_part = models.ForeignKey(PartTyreAbs, on_delete=models.CASCADE, null=False, blank=True, related_name='d1', related_query_name='d2')
    change_frequency_timedelta = models.DurationField(null=True, blank=True, default=timezone.now)
    change_frequency_km = models.PositiveIntegerField(null=True, blank=True, default=0)

    @property
    def should_change(self) -> bool:
        return timezone.now() - self.last_changed_datetime > self.change_frequency_timedelta or \
            self.vehicle.km - self.last_changed_km > self.change_frequency_km

    recaped = models.BooleanField(null=False, blank=False, default=False)
    def __repr__(self) -> str:
        return f'PartTyre(name={self.name}, should_change={self.should_change}, recaped={self.recaped})'
    
    def __str__(self) -> str:
        return self.__repr__()

class PartWithoutLifespan(Part):
    class Meta:
        default_related_name = 'parts_without_lifespan'

    abstract_part = models.ForeignKey(PartWithoutLifespanAbs, on_delete=models.CASCADE, null=False, blank=True, related_name='e1', related_query_name='e2')

    def __repr__(self) -> str:
        return f'PartWithoutLifespan(name={self.name})'
    
    def __str__(self) -> str:
        return self.__repr__()
    

### PART CHANGE NOTICE and PART FIX

class PartChangeNotice(TimeStampMixin):
    class Meta:
        default_related_name = 'part_change_notices'

    class ChangeUrgency(models.TextChoices):
        CRITICAL = 'CR', gettext_lazy('Crítico')
        IMPORTANT = 'IM', gettext_lazy('Importante')
        EVENTUAL = 'EV', gettext_lazy('Eventual')
        NOTICE = 'NO', gettext_lazy('Notificado')

    # ojo que todos los ForeignKeys que tengan (null=True, blank=False), pueden generar un error, si son null, pero se les requiere que se complete en un form
    # esto se dejó así porque la única situació en la que deben ser null es si la referencia se perdiera pero no se quiere perder este objeto. Esto no debería
    # pasar si todo funciona con normalidad
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False, related_name='f1', related_query_name='f2')
    part = models.ForeignKey(Part, on_delete=models.CASCADE, null=False, blank=False, related_name='g1', related_query_name='g2')
    info = models.CharField(max_length=1024, null=True, blank=True)
    urgency_type = models.CharField(max_length=2, choices=ChangeUrgency.choices, default=ChangeUrgency.NOTICE, null=False, blank=False)

    def __repr__(self) -> str:
        return f'PartChangeNotice(part={self.part.name}, issued_by={self.issued_by.first_name}, urgency_type={self.urgency_type})'
    
    def __str__(self) -> str:
        return self.__repr__()

class PartFix(TimeStampMixin):
    class Meta:
        default_related_name = 'part_fixes'

    done_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False, limit_choices_to={"profile__position_type": Profile.PositionType.MECHANIC}, related_name='h1', related_query_name='h2') # TODO: check if limit_choices_to works correctly
    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='i1', related_query_name='i2')
    replaced = models.BooleanField(null=False, blank=False, default=False) # si fue arreglado, eto es falso. si fue reemplazado, esto debe ser veradero
    success = models.BooleanField(null=False, blank=False, default=True)
    cost = models.PositiveIntegerField(null=True, blank=True)

    def __repr__(self) -> str:
        return f'PartFix(part={self.part.name}, done_by={self.done_by.first_name}, success={self.success})'
    
    def __str__(self) -> str:
        return self.__repr__()
    
### FORMS ###

class FormGroup(TimeStampMixin):
    name = models.CharField(max_length=64, null=False, blank=False, unique=True)

    def __repr__(self) -> str:
        return f'FormGroup(name={self.name})'
    
    def __str__(self) -> str:
        return self.__repr__()

class FormAbs(TimeStampMixin):
    # class Meta:
    #     default_related_name = 'form_abs'

    name = models.CharField(max_length=64, null=False, blank=False, unique=True)
    form_group = models.ForeignKey(FormGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name='j1', related_query_name='j2')

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=False, blank=False, related_name='k1', related_query_name='k2')
    profile_type = models.SmallIntegerField(choices=Profile.PositionType.choices, default=Profile.PositionType.NOT_ASSIGNED, null=False)

    # TODO: add periodicity

    def __repr__(self) -> str:
        return f'FormAbs(name={self.name}, questions={self.questions})'
    
    def __str__(self) -> str:
        return self.__repr__()
    
class Form(FormAbs):
    class Meta:
        default_related_name = '%(class)s'
    
    form_abs = models.ForeignKey(FormAbs, on_delete=models.SET_NULL, null=True, blank=False, related_name='l1', related_query_name='l2')
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False, related_name='m1', related_query_name='m2')

    @property
    def complete(self) -> bool:
        return all(question.complete for question in self.questions)

def _form_post_init(sender, instance, using, **kwargs):
    # sets the question_title, quesiton_group, info, part, vehicle, question_type, answer_type and allows_observations from the QuestionAbs
    if (instance.form_abs):
        instance.name = instance.form_abs.name
        instance.form_group = instance.form_abs.form_group
        instance.vehicle = instance.form_abs.vehicle
        instance.profile_type = instance.form_abs.profile_type

signals.post_init.connect(_form_post_init, sender=Form, weak=False, dispatch_uid='main.models._form_post_init')
    
### QUESTIONS ###

class QuestionGroup(TimeStampMixin):
    name = models.CharField(max_length=64, null=False, blank=False, unique=True)

    def __repr__(self) -> str:
        return f'QuestionGroup(name={self.name})'
    
    def __str__(self) -> str:
        return self.__repr__()
    
# might be a good idea to separate daily questions from maintenance questions
class QuestionAbs(TimeStampMixin):
    class Meta:
        default_related_name = 'question_abs'

    class QuestionType(models.TextChoices):
        DAILY = 'D', gettext_lazy('Diaria')
        MAINTENANCE = 'M', gettext_lazy('Mantenimiento')

    class AnswerType(models.TextChoices):
        YES_NO = 'YN', gettext_lazy('Sí-No')
        GOOD_REGULAR_BAD = '3S', gettext_lazy('Bueno-Regular-Malo')
        NUMBER = 'NR', gettext_lazy('Número')
        TEXT = 'TX', gettext_lazy('Texto')

    question_group = models.ForeignKey(QuestionGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name='n1', related_query_name='n2')

    question_title = models.CharField(max_length=128, null=False, blank=False)
    info = models.CharField(max_length=256, null=True, blank=True)
    part = models.ForeignKey(PartAbs, on_delete=models.SET_NULL, null=True, blank=True, related_name='o1', related_query_name='o2')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name='p1', related_query_name='p2')
    question_type = models.CharField(max_length=1, choices=QuestionType.choices, default=QuestionType.DAILY, null=False, blank=False)
    answer_type = models.CharField(max_length=2, choices=AnswerType.choices, default=AnswerType.YES_NO, null=False, blank=False)
    allows_observations = models.BooleanField(null=False, blank=False, default=True)

    form_abs = models.ManyToManyField(FormAbs)

    def __repr__(self) -> str:
        return f'QuestionAbs(question_title={self.question_title}, part={self.part if self.part.name else None}, vehicle={self.vehicle.name if self.vehicle else None}, question_type={self.question_type}, answer_type={self.answer_type})'
    
    def __str__(self) -> str:
        return self.__repr__()

class Question(QuestionAbs):
    class Meta:
        default_related_name = 'questions'

    class GoodRegularBadAnswers(models.TextChoices):
        GOOD = 'G', gettext_lazy('Bueno')
        REGULAT = 'R', gettext_lazy('Regular')
        BAD = 'B', gettext_lazy('Malo')

    question_abs = models.ForeignKey(QuestionAbs, on_delete=models.SET_NULL, null=True, blank=False, related_name='q1', related_query_name='q2')
    form = models.ForeignKey(Form, on_delete=models.CASCADE, null=False, blank=False, related_name='r1', related_query_name='r2')

    @property
    def part_abs(self) -> Optional[Part]:
        if not self.question_abs: return False
        return self.question_abs.part

    @property
    def vehicle_abs(self) -> Optional[Vehicle]:
        if not self.question_abs: return False
        return self.question_abs.vehicle

    @property
    def question_type_abs(self) -> Optional[QuestionAbs.QuestionType]:
        if not self.question_abs: return None
        return self.question_abs.question_type
    
    @property
    def answer_type_abs(self) -> Optional[QuestionAbs.AnswerType]:
        if not self.question_abs: return None
        return self.question_abs.answer_type
    
    @property
    def allows_observations_abs(self) -> Optional[bool]:
        if not self.question_abs: return None
        return self.question_abs.allows_observations

    yes_no = models.BooleanField(null=True, blank=True, default=None)
    good_regular_bad = models.CharField(max_length=1, choices=GoodRegularBadAnswers.choices, default=None, null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)
    text = models.CharField(max_length=1024, null=True, blank=True)
        
    @property
    def answer(self) -> Union[bool, GoodRegularBadAnswers, int, str, None]:
        if self.answer_type == QuestionAbs.AnswerType.YES_NO:
            return self.yes_no
        elif self.answer_type == QuestionAbs.AnswerType.GOOD_REGULAR_BAD:
            return self.good_regular_bad
        elif self.answer_type == QuestionAbs.AnswerType.NUMBER:
            return self.number
        elif self.answer_type == QuestionAbs.AnswerType.TEXT:
            return self.text
        else:
            raise Exception
    
    @property
    def complete(self) -> bool:
        return self.answer is not None
    
    def __repr__(self) -> str:
        return f'Question(question_title={self.question_title if self.question_title else None}, part={self.part if self.part.name else None}, vehicle={self.vehicle.name if self.vehicle else None}, question_type={self.question_type}, answer_type={self.answer_type})'
    
    def __str__(self) -> str:
        return self.__repr__()

# def _question_abs_post_init(sender, instance, using, **kwargs): # TODO: if below works, delete this line
def _question_abs_post_init(sender, instance, **kwargs):
    # if there is a part and that part has a vehicle, the vehicle of the QuationsAbs should be the vehicle of the part
    if (instance.part):
        if (instance.part.vehicle):
            instance.vehicle = instance.part.vehicle



### SIGNALS ###

def _part_all_post_save(sender, instance, created, **kwargs):
    # sets the last_changed_km of the part to the vehicle's currnent km if no km was specified
    if created and instance.abstract_part:
        if sender == PartWithLifespan or sender == PartTyre:
            if instance.abstract_part.change_frequency_timedelta:
                instance.change_frequency_timedelta = instance.abstract_part.change_frequency_timedelta
            if instance.abstract_part.change_frequency_km:
                instance.change_frequency_km = instance.abstract_part.change_frequency_km
        else: # sender == PartWithoutLifespanAbs:
            pass

        if not instance.info and instance.abstract_part.info:
            instance.info = instance.abstract_part.info

def _part_abs_all_post_save(sender, instance, created, **kwargs):
    if sender == PartWithLifespanAbs:
        for inst in instance.objects.all().parts_with_lifespan:
            if inst.update_info:
                inst.change_frequency_timedelta = instance.change_frequency_timedelta
                inst.change_frequency_km = instance.change_frequency_km
    elif sender == PartTyreAbs:
        for inst in instance.objects.all().part_tyre:
            if inst.update_info:
                inst.change_frequency_timedelta = instance.change_frequency_timedelta
                inst.change_frequency_km = instance.change_frequency_km
    else: # sender == PartWithoutLifespanAbs:
        pass
        # for inst in instance.objects.all().parts_without_lifespan:
        #     pass


signals.post_save.connect(_part_all_post_save, sender=PartWithLifespan, weak=False, dispatch_uid='main.models._part_all_post_save.PartWithLifespan')
signals.post_save.connect(_part_all_post_save, sender=PartTyre, weak=False, dispatch_uid='main.models._part_all_post_save.PartTyre')
signals.post_save.connect(_part_abs_all_post_save, sender=PartWithLifespanAbs, weak=False, dispatch_uid='main.models._part_abs_all_update.PartWithLifespanAbs')
signals.post_save.connect(_part_abs_all_post_save, sender=PartTyreAbs, weak=False, dispatch_uid='main.models._part_abs_all_update.PartTyreAbs')
signals.post_save.connect(_part_abs_all_post_save, sender=PartWithoutLifespanAbs, weak=False, dispatch_uid='main.models._part_abs_all_update.PartWithoutLifespanAbs')


def _question_post_init(sender, instance, **kwargs):
    # sets the question_title, quesiton_group, info, part, vehicle, question_type, answer_type and allows_observations from the QuestionAbs
    if (instance.question_abs):
        instance.question_title = instance.question_abs.question_title
        instance.question_group = instance.question_abs.question_group
        instance.info = instance.question_abs.info
        instance.part = instance.question_abs.part
        instance.vehicle = instance.question_abs.vehicle
        instance.question_type = instance.question_abs.question_type
        instance.answer_type = instance.question_abs.question_type
        instance.allows_observations = instance.question_abs.allows_observations

signals.post_init.connect(_question_abs_post_init, sender=QuestionAbs, weak=False, dispatch_uid='main.models._question_abs_post_init')
signals.post_init.connect(_question_post_init, sender=Question, weak=False, dispatch_uid='main.models._question_post_init')
