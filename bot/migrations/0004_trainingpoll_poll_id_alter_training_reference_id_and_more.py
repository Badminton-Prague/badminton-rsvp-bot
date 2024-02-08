# Generated by Django 4.1.3 on 2024-02-07 22:28

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0003_trainingpoll_training_chat_id_training_message_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainingpoll',
            name='poll_id',
            field=models.TextField(db_index=True, default='', max_length=128),
        ),
        migrations.AlterField(
            model_name='training',
            name='reference_id',
            field=models.TextField(db_index=True, default=uuid.UUID('4970a7c6-c608-11ee-bf59-2a8610ce7e84'), max_length=128),
        ),
        migrations.AlterField(
            model_name='trainingpoll',
            name='reference_id',
            field=models.TextField(db_index=True, default=uuid.UUID('4970ad98-c608-11ee-bf59-2a8610ce7e84'), max_length=128),
        ),
    ]