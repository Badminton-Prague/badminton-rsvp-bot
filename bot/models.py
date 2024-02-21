from django.db import models


class Poll(models.Model):
    thread_name = models.TextField(max_length=128, db_index=True, default="")
    thread_id = models.IntegerField(db_index=True, null=True)

    poll_question = models.TextField(max_length=128, db_index=True, default="")
    poll_id = models.TextField(max_length=128, db_index=True, null=True)

    chat_id = models.IntegerField(db_index=True, default=0)
    message_id = models.IntegerField(db_index=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)


class Training(models.Model):
    max_people = models.IntegerField(default=0)
    poll = models.OneToOneField(
        Poll, on_delete=models.CASCADE, db_index=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)


class PollVote(models.Model):
    class Meta:
        index_together = [
            ("user_id", "poll"),
        ]

    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    user_id = models.IntegerField(db_index=True)
    go = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
