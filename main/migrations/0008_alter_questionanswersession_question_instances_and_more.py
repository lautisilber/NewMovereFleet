# Generated by Django 4.2.1 on 2023-05-20 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_rename_answer_sessions_questionanswersession_question_instances_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionanswersession',
            name='question_instances',
            field=models.ManyToManyField(blank=True, related_name='answer_sessions', related_query_name='answer_sessions', to='main.questioninstance'),
        ),
        migrations.AlterField(
            model_name='questionanswersession',
            name='question_templates',
            field=models.ManyToManyField(blank=True, related_name='answer_sessions', related_query_name='answer_sessions', to='main.questiontemplate'),
        ),
        migrations.AlterField(
            model_name='questioninstance',
            name='question_types',
            field=models.ManyToManyField(blank=True, related_name='question_instances', related_query_name='question_instances', to='main.questiontype'),
        ),
        migrations.AlterField(
            model_name='questiontemplate',
            name='question_types',
            field=models.ManyToManyField(blank=True, related_name='question_templates', related_query_name='question_templates', to='main.questiontype'),
        ),
        migrations.AlterField(
            model_name='questiontemplate',
            name='vehicles',
            field=models.ManyToManyField(blank=True, related_name='question_templates', related_query_name='question_templates', to='main.vehicle'),
        ),
    ]