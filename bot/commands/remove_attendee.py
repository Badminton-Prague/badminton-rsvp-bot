from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.helpers.get_training_by_thread_id import get_training_by_thread_id
from bot.models import Attendee
from ..decorator import restrict_to_telegram_users
from ..helpers.format_exception import format_exception
from django.conf import settings


@restrict_to_telegram_users(allowed_user_ids=settings.ADMIN_USER_IDS)
async def remove_attendee(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        attendee_id = int(context.args[0])

        attendee = await sync_to_async(
            lambda: Attendee.objects.filter(pk=attendee_id)
            .prefetch_related("telegram_user", "training", "training__poll")
            .first()
        )()
        if attendee is None:
            await update.message.reply_html(f"Attendee #{attendee_id} not found")
        else:
            await sync_to_async(
                lambda: Attendee.objects.filter(id=attendee_id).delete()
            )()
            await update.message.reply_html(
                f"Attendee #{attendee_id} removed from training {attendee.training.poll.thread_name}"
            )
    except Exception as exception:
        await update.message.reply_html(
            format_exception("removing an attendee", exception)
        )

    finally:
        return ConversationHandler.END
