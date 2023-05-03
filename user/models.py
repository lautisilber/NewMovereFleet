from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy
from django.db.models import signals


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    info = models.CharField(max_length=128, null=True, blank=True)

    class PositionType(models.IntegerChoices):
        NOT_ASSIGNED = 0, gettext_lazy('Not assigned')
        DRIVER = 1, gettext_lazy('Driver')
        MECHANIC = 2, gettext_lazy('Mechanic')
        ADMINISTRATOR = 3, gettext_lazy('Administrator')
        SUPERUSER = 4, gettext_lazy('Super user')

    position_type = models.SmallIntegerField(choices=PositionType.choices, default=PositionType.NOT_ASSIGNED, null=False)

    @classmethod
    def get_position_types(cls) -> list[tuple[str, str]]:
        return cls.PositionType.choices

    def __str__(self):
        return f'Profile(user_id={self.user.id}, user_name={self.user.username}, position_type={self.position_type})'
    


### SIGNALS ###

def create_user(sender, instance, created, **kwargs):
    if created:
        extra_info = {}
        if instance.is_superuser:
            extra_info['position_type'] = next(filter(lambda e: e[1] == 'Super user', Profile.get_position_types()))[0]
        Profile.objects.create(user=instance, **extra_info)

signals.post_save.connect(create_user, sender=User, weak=False, dispatch_uid='user.models.create_user')


def delete_user(sender, instance, using, **kwargs):
    instance.questionanswersession_set.all().delete()

signals.pre_delete.connect(delete_user, sender=User, weak=False, dispatch_uid='user.models.delete_user')