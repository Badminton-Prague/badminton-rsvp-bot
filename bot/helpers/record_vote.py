from bot.models import TelegramUser, Poll, PollVote
from asgiref.sync import sync_to_async


async def record_vote(poll: Poll, telegram_user: TelegramUser):
    await sync_to_async(
        lambda: PollVote.objects.create(poll=poll, telegram_user=telegram_user, go=True)
    )()
