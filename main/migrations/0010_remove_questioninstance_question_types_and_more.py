# Generated by Django 4.2.1 on 2023-05-26 05:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_remove_questionanswersession_question_instances_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questioninstance',
            name='question_types',
        ),
        migrations.AlterField(
            model_name='questionanswersession',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_sessions', related_query_name='answer_sessions', to='main.vehicle'),
        ),
        migrations.AlterField(
            model_name='questioninstance',
            name='vehicle',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='question_instances', related_query_name='question_instances', to='main.vehicle'),
        ),
    ]