from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from django.db import transaction

from bot.models import Attendee, Training
from ..helpers.safe_get import safe_get
from ..helpers.report_exception import report_exception
from django.template.loader import render_to_string


async def list_attendees(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    @transaction.atomic()
    def executor():
        training_id = safe_get(context.args, 0, None)

        training = (
            Training.objects.filter(pk=training_id).first()
            if training_id is not None
            else Training.objects.filter(
                poll__thread_id=update.message.message_thread_id
            ).first()
        )
        return render_to_string("list_attendees_response.txt", dict(training=training))

    try:
        rendered_message = await sync_to_async(executor)()
        await update.message.reply_html(rendered_message)

    except Exception as exception:
        await report_exception("listing attendees", exception, message=update.message)

    finally:
        return ConversationHandler.END
