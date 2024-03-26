from bot.models import TelegramUser, Training, Attendee, POLL_VOTE_SOURCE


def retract_first_vote(training: Training, telegram_user: TelegramUser) -> Attendee:
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
        raise Exception(
            f"No first attendee for telegram_user {telegram_user.telegram_id} found"
        )

    Attendee.objects.filter(pk=first_poll_vote.pk).update(go=False)
    first_poll_vote.go = False
    return first_poll_vote
