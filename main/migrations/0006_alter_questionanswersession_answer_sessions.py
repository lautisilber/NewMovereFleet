# Generated by Django 4.2.1 on 2023-05-20 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_questioninstance_answer_sessions_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionanswersession',
            name='answer_sessions',
            field=models.ManyToManyField(blank=True, related_name='answersession', related_query_name='answersession', to='main.questioninstance'),
        ),
    ]
