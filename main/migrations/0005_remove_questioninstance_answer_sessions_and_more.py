# Generated by Django 4.2.1 on 2023-05-20 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_questionanswersession_question_types_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questioninstance',
            name='answer_sessions',
        ),
        migrations.RemoveField(
            model_name='questiontemplate',
            name='answer_sessions',
        ),
        migrations.AddField(
            model_name='questionanswersession',
            name='answer_sessions',
            field=models.ManyToManyField(blank=True, to='main.questioninstance'),
        ),
    ]
