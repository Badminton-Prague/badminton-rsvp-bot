from telegram import User
from asgiref.sync import sync_to_async

from bot.models import TelegramUser


async def get_and_update_telegram_user(effective_user: User) -> TelegramUser:
    telegram_user, created = await sync_to_async(
        lambda: TelegramUser.objects.get_or_create(telegram_id=effective_user.id)
    )()
    await sync_to_async(
        lambda: TelegramUser.objects.filter(pk=telegram_user.pk).update(
            first_name=effective_user.first_name,
            last_name=effective_user.last_name,
            username=effective_user.username,
        )
    )()

    telegram_user.first_name = effective_user.first_name
    telegram_user.last_name = effective_user.last_name
    telegram_user.username = effective_user.username

    return telegram_user
