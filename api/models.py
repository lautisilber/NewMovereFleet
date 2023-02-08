from django.db import models


class ApiTest(models.Model):
    text = models.CharField(max_length=32)
    number = models.IntegerField()