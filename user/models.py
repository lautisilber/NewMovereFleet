from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    info = models.CharField(max_length=128, null=True)

    def __str__(self):
        return f'Profile(user_id={self.user.id}, user_name={self.user.username})'