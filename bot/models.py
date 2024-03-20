from django.db import models


class Training(models.Model):
    attendees_limit = models.IntegerField(default=0)
    date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Poll(models.Model):
    training = models.OneToOneField(
        Training,
        on_delete=models.CASCADE,
        db_index=True,
        null=True,
        related_name="poll",
    )

    thread_name = models.TextField(max_length=128, db_index=True)
    thread_id = models.IntegerField(db_index=True, null=True)

    poll_question = models.TextField(max_length=128, db_index=True)
    poll_id = models.TextField(max_length=128, db_index=True, null=True)

    chat_id = models.BigIntegerField(db_index=True)
    message_id = models.IntegerField(db_index=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TelegramUser(models.Model):
    telegram_id = models.BigIntegerField(db_index=True, unique=True)
    first_name = models.CharField(max_length=512, null=True, db_index=True)
    last_name = models.CharField(max_length=512, null=True, db_index=True)
    username = models.CharField(max_length=512, null=True, db_index=True)

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


PLUS_ONE_COMMAND_SOURCE = "PLUS_ONE_COMMAND"
POLL_VOTE_SOURCE = "POLL_VOTE"

ATTENDEE_SOURCE_CHOICES = [
    (PLUS_ONE_COMMAND_SOURCE, "+1"),
    (POLL_VOTE_SOURCE, "Poll Vote"),
]


class Attendee(models.Model):
    training = models.ForeignKey(
        Training,
        on_delete=models.CASCADE,
        related_name="attendees",
        null=True,
        db_index=True,
    )
    telegram_user = models.ForeignKey(
        TelegramUser, on_delete=models.CASCADE, null=True, db_index=True
    )
    go = models.BooleanField(default=False, db_index=True)
    source = models.CharField(
        max_length=128, choices=ATTENDEE_SOURCE_CHOICES, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
