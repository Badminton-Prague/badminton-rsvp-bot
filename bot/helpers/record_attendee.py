from bot.models import TelegramUser, Training, Attendee
from asgiref.sync import sync_to_async


async def record_attendee(training: Training, telegram_user: TelegramUser, source: str):
    await sync_to_async(
        lambda: Attendee.objects.create(
            training=training, telegram_user=telegram_user, go=True, source=source
        )
    )()
