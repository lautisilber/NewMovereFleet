# Generated by Django 4.2.1 on 2023-05-05 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_questiontemplate_answer_session_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questioninstance',
            old_name='answer_session',
            new_name='answer_sessions',
        ),
        migrations.RenameField(
            model_name='questiontemplate',
            old_name='answer_session',
            new_name='answer_sessions',
        ),
        migrations.RemoveField(
            model_name='questiontype',
            name='question_answer_sessions',
        ),
        migrations.RemoveField(
            model_name='questiontype',
            name='question_instances',
        ),
        migrations.RemoveField(
            model_name='questiontype',
            name='question_templates',
        ),
        migrations.AddField(
            model_name='questionanswersession',
            name='question_types',
            field=models.ManyToManyField(blank=True, to='main.questiontype'),
        ),
        migrations.AddField(
            model_name='questioninstance',
            name='question_types',
            field=models.ManyToManyField(blank=True, to='main.questiontype'),
        ),
        migrations.AddField(
            model_name='questiontemplate',
            name='question_types',
            field=models.ManyToManyField(blank=True, to='main.questiontype'),
        ),
    ]
