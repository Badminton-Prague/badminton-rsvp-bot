from asgiref.sync import sync_to_async
from asgiref.sync import sync_to_async
from types import SimpleNamespace
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.helpers.get_training_by_thread_id import get_training_by_thread_id
from bot.models import Attendee
from ..helpers.format_exception import format_exception


async def list_attendees(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        db_attendees = await sync_to_async(
            lambda: list(
                Attendee.objects.filter(
                    training__poll__thread_id=update.message.message_thread_id, go=True
                )
                .order_by("id")
                .prefetch_related("telegram_user")
            )
        )()
        training = await get_training_by_thread_id(update.message.message_thread_id)
        attendees = list(
            map(
                lambda attendee: f"User {attendee.telegram_user.message_username} {'will' if attendee.go else 'will NOT'} attend training on {training.date} (source: {attendee.source})",
                db_attendees,
            )
        )
        formatted_attendees = "\n".join(attendees[: training.max_people])
        formatted_waiting_list = "\n".join(attendees[training.max_people :])
        await update.message.reply_html(
            f"Attendees:\n{formatted_attendees}\n\n\nWaiting list:\n{formatted_waiting_list}"
        )
    except Exception as exception:
        await update.message.reply_html(
            format_exception("listing poll votes", exception)
        )

    finally:
        return ConversationHandler.END
