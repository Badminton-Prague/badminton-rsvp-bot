from bot.models import TelegramUser, Poll, PollVote
from asgiref.sync import sync_to_async


async def retract_first_vote(poll: Poll, telegram_user: TelegramUser):
    first_poll_vote = await sync_to_async(
        lambda: PollVote.objects.filter(poll=poll, telegram_user=telegram_user)
        .order_by("id")
        .first()
    )()
    if first_poll_vote is None:
        return
    await sync_to_async(
        lambda: PollVote.objects.filter(pk=first_poll_vote.pk).update(go=False)
    )()
