from django.conf import settings
from django.db import transaction
from telegram import Update
from telegram.ext import ContextTypes

from bot.models import Attendee
from ..asynchronous import asyncify
from ..decorator import restrict_to_telegram_users, catch_all_exceptions_in_tg_handlers


@transaction.atomic()
def db_transaction(attendee_id: int) -> str:
    attendee = (
        Attendee.objects.filter(pk=attendee_id)
        .prefetch_related("training__poll")
        .first()
    )
    if attendee is None:
        raise Exception(f"Attendee {attendee_id} not found")

    Attendee.objects.filter(id=attendee_id).delete()

    return f"Attendee #{attendee_id} removed from training {attendee.training.poll.thread_name}"


@restrict_to_telegram_users(allowed_user_ids=settings.ADMIN_USER_IDS)
@catch_all_exceptions_in_tg_handlers(
    "receiving a poll answer", respond_to_message=False
)
async def remove_attendee(update: Update, context: ContextTypes.DEFAULT_TYPE):
    attendee_id = int(context.args[0])
    rendered_message = await asyncify(db_transaction, attendee_id)
    await update.message.reply_html(rendered_message)
