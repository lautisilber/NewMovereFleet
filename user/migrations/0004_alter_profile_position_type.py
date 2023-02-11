# Generated by Django 4.1.6 on 2023-02-10 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_profile_position_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='position_type',
            field=models.SmallIntegerField(choices=[('-1', 'Not assigned'), ('1', 'Driver'), ('2', 'Mechanic'), ('3', 'Administrator'), ('4', 'Super user')], default='-1'),
        ),
    ]