# Generated by Django 4.2.1 on 2023-05-20 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_questionanswersession_answer_sessions'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questionanswersession',
            old_name='answer_sessions',
            new_name='question_instances',
        ),
        migrations.AddField(
            model_name='questionanswersession',
            name='question_templates',
            field=models.ManyToManyField(blank=True, related_name='answersession', related_query_name='answersession', to='main.questiontemplate'),
        ),
    ]