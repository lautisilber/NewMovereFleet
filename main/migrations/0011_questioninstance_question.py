# Generated by Django 4.2 on 2023-05-01 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_questionanswersession_vehicle_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='questioninstance',
            name='question',
            field=models.CharField(default=1, max_length=32),
            preserve_default=False,
        ),
    ]
