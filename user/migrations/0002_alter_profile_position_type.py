# Generated by Django 4.2 on 2023-04-23 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='position_type',
            field=models.SmallIntegerField(choices=[(0, 'Not assigned'), (1, 'Driver'), (2, 'Mechanic'), (3, 'Administrator'), (4, 'Super user')], default=0),
        ),
    ]
