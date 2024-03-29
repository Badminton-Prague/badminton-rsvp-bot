from django.db import transaction
from django.template.loader import render_to_string
from telegram import Update
from telegram.ext import ContextTypes

from bot.models import Training
from ..asynchronous import asyncify
from ..decorator import catch_all_exceptions_in_tg_handlers
from ..helpers.safe_get import safe_get


@transaction.atomic()
def db_transaction(
    message_thread_id: int,
    training_id: int = None,
) -> str:
    training = (
        Training.objects.filter(pk=training_id).first()
        if training_id is not None
        else Training.objects.filter(poll__thread_id=message_thread_id).first()
    )
    return render_to_string("list_attendees_response.txt", dict(training=training))


@catch_all_exceptions_in_tg_handlers("listing attendees")
async def list_attendees(update: Update, context: ContextTypes.DEFAULT_TYPE):
    training_id = safe_get(context.args, 0, None)
    rendered_message = await asyncify(
        db_transaction, update.message.message_thread_id, training_id
    )
    await update.message.reply_html(rendered_message)
