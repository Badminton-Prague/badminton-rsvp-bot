from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.models import Attendee
from ..decorator import restrict_to_telegram_users
from ..helpers.report_exception import report_exception
from django.conf import settings
from django.db import transaction
from asgiref.sync import sync_to_async


@restrict_to_telegram_users(allowed_user_ids=settings.ADMIN_USER_IDS)
async def remove_attendee(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    @transaction.atomic()
    def executor() -> str:
        attendee_id = int(context.args[0])
        attendee = (
            Attendee.objects.filter(pk=attendee_id)
            .prefetch_related("training__poll")
            .first()
        )
        if attendee is None:
            raise Exception(f"Attendee {attendee_id} not found")

        Attendee.objects.filter(id=attendee_id).delete()

        return f"Attendee #{attendee_id} removed from training {attendee.training.poll.thread_name}"

    try:
        rendered_message = await sync_to_async(executor)()
        await update.message.reply_html(rendered_message)

    except Exception as exception:
        await report_exception(
            "removing an attendee", exception, message=update.message
        )

    finally:
        return ConversationHandler.END
