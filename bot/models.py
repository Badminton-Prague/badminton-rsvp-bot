from django.db import models


class Poll(models.Model):
    thread_name = models.TextField(max_length=128, db_index=True, default="")
    thread_id = models.IntegerField(db_index=True, null=True)

    poll_question = models.TextField(max_length=128, db_index=True, default="")
    poll_id = models.TextField(max_length=128, db_index=True, null=True)

    chat_id = models.IntegerField(db_index=True, default=0)
    message_id = models.IntegerField(db_index=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Training(models.Model):
    max_people = models.IntegerField(default=0)
    poll = models.OneToOneField(
        Poll, on_delete=models.CASCADE, db_index=True, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TelegramUser(models.Model):
    telegram_id = models.IntegerField(db_index=True, unique=True)
    first_name = models.CharField(max_length=512, default="")
    last_name = models.CharField(max_length=512, default="")
    username = models.CharField(max_length=512, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PollVote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    telegram_user = models.OneToOneField(
        TelegramUser, on_delete=models.CASCADE, null=True
    )
    go = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
