from bot.models import TelegramUser, Training, Attendee, POLL_VOTE_SOURCE
from typing import Optional

def retract_first_vote(training: Training, telegram_user: TelegramUser) -> Optional[Attendee]:
    first_poll_vote = (
        Attendee.objects.filter(
            training=training,
            telegram_user=telegram_user,
            go=True,
            source=POLL_VOTE_SOURCE,
        )
        .order_by("id")
        .first()
    )

    if first_poll_vote is None:
        return None

    Attendee.objects.filter(pk=first_poll_vote.pk).update(go=False)
    first_poll_vote.go = False
    return first_poll_vote
