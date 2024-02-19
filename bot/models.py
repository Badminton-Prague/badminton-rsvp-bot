from django.db import models
import uuid

class Training(models.Model):
    reference_id = models.TextField(max_length=128, db_index=True, default=uuid.uuid1())
    thread_name = models.TextField(max_length=128, db_index=True, default="")
    poll_header = models.TextField(max_length=128, db_index=True, default="")
    message_id = models.TextField(max_length=128, db_index=True, default="")
    chat_id = models.TextField(max_length=128, db_index=True, default="")
    thread_id = models.TextField(max_length=128, db_index=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

class TrainingPoll(models.Model):
    reference_id = models.TextField(max_length=128, db_index=True, default=uuid.uuid1())
    thread_name = models.TextField(max_length=128, db_index=True, default="")
    poll_header = models.TextField(max_length=128, db_index=True, default="")
    message_id = models.TextField(max_length=128, db_index=True, default="")
    poll_id = models.TextField(max_length=128, db_index=True, default="")
    chat_id = models.TextField(max_length=128, db_index=True, default="")
    thread_id = models.TextField(max_length=128, db_index=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    max_people = models.DecimalField(default=0, decimal_places=2, max_digits=5)

class PollVotes(models.Model):
    reference_id = models.TextField(max_length=128, db_index=True, default=uuid.uuid1())
    poll_id = models.TextField(max_length=128, db_index=True, default="")
    chat_id = models.TextField(max_length=128, db_index=True, default="")
    thread_id = models.TextField(max_length=128, db_index=True, default="")
    users_voted_go = models.CharField(max_length=128, db_index=True, default=[])
