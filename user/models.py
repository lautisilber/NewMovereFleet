from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    info = models.CharField(max_length=128, null=True)

    class PositionType(models.TextChoices):
        NOT_ASSIGNED = 'NA', gettext_lazy('Not assigned')
        DRIVER = 'DR', gettext_lazy('Driver')
        MECHANIC = 'MC', gettext_lazy('Mechanic')
        ADMINISTRATOR = 'AD', gettext_lazy('Administrator')
        SUPERUSER = 'SU', gettext_lazy('Super user')

    position_type = models.CharField(max_length=2, choices=PositionType.choices, default=PositionType.NOT_ASSIGNED, null=False)

    @classmethod
    def get_position_types(cls) -> list[tuple[str, str]]:
        return cls.PositionType.choices

    def __str__(self):
        return f'Profile(user_id={self.user.id}, user_name={self.user.username}, position_type={self.position_type})'