from bot.models import TelegramUser, Training, Attendee, POLL_VOTE_SOURCE
from asgiref.sync import sync_to_async


async def retract_first_vote(training: Training, telegram_user: TelegramUser):
    first_poll_vote = await sync_to_async(
        lambda: Attendee.objects.filter(
            training=training,
            telegram_user=telegram_user,
            go=True,
            source=POLL_VOTE_SOURCE,
        )
        .order_by("id")
        .first()
    )()
    if first_poll_vote is None:
        return
    await sync_to_async(
        lambda: Attendee.objects.filter(pk=first_poll_vote.pk).update(go=False)
    )()
