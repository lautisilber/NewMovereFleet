from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy
from django.db.models import signals


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    info = models.CharField(max_length=128, null=True, blank=True)

    class PositionType(models.TextChoices):
        NOT_ASSIGNED = 'N', gettext_lazy('Not assigned')
        DRIVER = 'D', gettext_lazy('Driver')
        MECHANIC = 'M', gettext_lazy('Mechanic')
        ADMINISTRATOR = 'A', gettext_lazy('Administrator')
        SUPERUSER = 'S', gettext_lazy('Super user')

    position_type = models.CharField(max_length=1, choices=PositionType.choices, default=PositionType.NOT_ASSIGNED, null=False, blank=False)

    @classmethod
    def get_position_types(cls) -> list[tuple[str, str]]:
        return cls.PositionType.choices

    def __repr__(self):
        return f'Profile(user_id={self.user.id}, user_name={self.user.username}, position_type={self.position_type})'
    
    def __str__(self) -> str:
        return f"{self.user.username}'s profile"


### SIGNALS ###

def create_user(sender, instance, created, **kwargs):
    if created:
        extra_info = {}
        if instance.is_superuser:
            extra_info['position_type'] = next(filter(lambda e: e[1] == 'Super user', Profile.get_position_types()))[0]
        Profile.objects.create(user=instance, **extra_info)

signals.post_save.connect(create_user, sender=User, weak=False, dispatch_uid='user.models.create_user')
