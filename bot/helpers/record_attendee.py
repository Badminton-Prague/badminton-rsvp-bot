from bot.models import TelegramUser, Training, Attendee


def record_attendee(
    training: Training, telegram_user: TelegramUser, source: str
) -> Attendee:
    return Attendee.objects.create(
        training=training, telegram_user=telegram_user, go=True, source=source
    )
