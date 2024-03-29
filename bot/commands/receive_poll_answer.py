from django.conf import settings
from django.db import transaction
from telegram import Update
from telegram import User
from telegram.ext import ContextTypes

from bot.helpers.get_and_update_telegram_user import get_and_update_telegram_user
from bot.helpers.record_attendee import record_attendee
from bot.helpers.retract_first_vote import retract_first_vote
from bot.helpers.send_to_attendee_log import send_to_attendee_log
from ..asynchronous import asyncify
from ..decorator import catch_all_exceptions_in_tg_handlers
from ..models import Attendee
from ..models import POLL_VOTE_SOURCE
from ..models import Training


@transaction.atomic()
def db_transaction(poll_answer: Update, effective_user: User) -> Attendee:
    """Summarize a users poll vote"""
    training = Training.objects.filter(poll__poll_id=poll_answer.poll_id).first()
    if training is None:
        raise Exception(f"No training found for poll {poll_answer.poll_id}")

    # Update a user
    telegram_user = get_and_update_telegram_user(effective_user)

    # Record a vote
    attendee = None
    selected_option_ids = poll_answer.option_ids
    if len(selected_option_ids) == 0:
        attendee = retract_first_vote(training, telegram_user)
    else:
        selected_option = settings.POLL_OPTIONS[selected_option_ids[0]]

        if selected_option == settings.POLL_GO_OPTION:
            attendee = record_attendee(training, telegram_user, POLL_VOTE_SOURCE)
        elif selected_option == settings.POLL_NO_GO_OPTION:
            attendee = retract_first_vote(training, telegram_user)

    return attendee


@catch_all_exceptions_in_tg_handlers(
    "receiving a poll answer", respond_to_message=False
)
async def receive_poll_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    attendee = await asyncify(db_transaction, update.poll_answer, update.effective_user)
    if attendee is not None:
        await send_to_attendee_log(context.bot, attendee)
