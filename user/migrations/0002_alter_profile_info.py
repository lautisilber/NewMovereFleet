# Generated by Django 4.1.6 on 2023-02-04 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='info',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
