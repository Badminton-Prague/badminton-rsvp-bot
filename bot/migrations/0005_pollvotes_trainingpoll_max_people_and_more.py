# Generated by Django 4.1.3 on 2024-02-08 22:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_trainingpoll_poll_id_alter_training_reference_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PollVotes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_id', models.TextField(db_index=True, default=uuid.UUID('bc123782-c6cf-11ee-8f9b-2a8610ce7e84'), max_length=128)),
                ('poll_id', models.TextField(db_index=True, default='', max_length=128)),
                ('chat_id', models.TextField(db_index=True, default='', max_length=128)),
                ('thread_id', models.TextField(db_index=True, default='', max_length=128)),
                ('users_voted_go', models.CharField(db_index=True, default=[], max_length=128)),
            ],
        ),
        migrations.AddField(
            model_name='trainingpoll',
            name='max_people',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=3),
        ),
        migrations.AlterField(
            model_name='training',
            name='reference_id',
            field=models.TextField(db_index=True, default=uuid.UUID('bc122bb6-c6cf-11ee-8f9b-2a8610ce7e84'), max_length=128),
        ),
        migrations.AlterField(
            model_name='trainingpoll',
            name='reference_id',
            field=models.TextField(db_index=True, default=uuid.UUID('bc1231b0-c6cf-11ee-8f9b-2a8610ce7e84'), max_length=128),
        ),
    ]