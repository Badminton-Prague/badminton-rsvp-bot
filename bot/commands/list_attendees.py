from asgiref.sync import sync_to_async
from types import SimpleNamespace
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.helpers.get_training_by_thread_id import get_training_by_thread_id
from bot.models import Attendee, Training
from ..helpers.format_exception import format_exception
from ..helpers.safe_get import safe_get


async def list_attendees(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        training_id = safe_get(context.args, 0, None)

        training = (
            await sync_to_async(
                lambda: Training.objects.filter(pk=training_id).first()
            )()
            if training_id is not None
            else await get_training_by_thread_id(update.message.message_thread_id)
        )

        db_attendees = await sync_to_async(
            lambda: list(
                Attendee.objects.filter(training=training, go=True)
                .order_by("id")
                .prefetch_related("telegram_user")
            )
        )()

        attendees = list(
            map(
                lambda attendee: f"{attendee.pk}: {attendee.telegram_user.message_username} (source: {attendee.source})",
                db_attendees,
            )
        )
        formatted_attendees = "\n".join(attendees[: training.attendees_limit])
        formatted_waiting_list = "\n".join(attendees[training.attendees_limit :])
        await update.message.reply_html(
            f"Training #{training.pk}\nAttendees:\n{formatted_attendees}\n\n\nWaiting list:\n{formatted_waiting_list}"
        )
    except Exception as exception:
        await update.message.reply_html(
            format_exception("listing attendees", exception)
        )

    finally:
        return ConversationHandler.END
