from django.db import models


class Poll(models.Model):
    thread_name = models.TextField(max_length=128, db_index=True)
    thread_id = models.IntegerField(db_index=True, null=True)

    poll_question = models.TextField(max_length=128, db_index=True)
    poll_id = models.TextField(max_length=128, db_index=True, null=True)

    chat_id = models.BigIntegerField(db_index=True)
    message_id = models.IntegerField(db_index=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Training(models.Model):
    max_people = models.IntegerField(default=0)
    poll = models.OneToOneField(
        Poll,
        on_delete=models.CASCADE,
        db_index=True,
        null=True,
        related_name="training",
    )
    date = models.DateField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TelegramUser(models.Model):
    telegram_id = models.BigIntegerField(db_index=True, unique=True)
    first_name = models.CharField(max_length=512, null=True)
    last_name = models.CharField(max_length=512, null=True)
    username = models.CharField(max_length=512, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def message_username(self):
        if self.username:
            return f"@{self.username} (id: {self.telegram_id})"
        else:
            return f"{self.first_name} {self.last_name} (id: {self.telegram_id})"

    def __str__(self):
        return self.message_username


class PollVote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    telegram_user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, null=True)
    go = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
