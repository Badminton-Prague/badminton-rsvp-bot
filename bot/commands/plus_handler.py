from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.helpers.get_and_update_telegram_user import get_and_update_telegram_user
from bot.helpers.get_training_by_thread_id import get_training_by_thread_id
from bot.helpers.record_attendee import record_attendee
from django.conf import settings
from ..helpers.format_exception import format_exception
from ..models import PLUS_ONE_COMMAND_SOURCE


async def plus_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    effective_user = update.effective_user

    try:
        training = await get_training_by_thread_id(update.message.message_thread_id)
        if training is None:
            return ConversationHandler.END

        telegram_user = await get_and_update_telegram_user(effective_user)

        # Record a vote
        await record_attendee(training, telegram_user, PLUS_ONE_COMMAND_SOURCE)

        # Submit a notification
        text_message = f"User {telegram_user.message_username} will attend training on {training.date}"
        await update.message.reply_text(text_message)
        await context.bot.send_message(
            chat_id=settings.SYSTEM_LOG_CHAT_ID,
            message_thread_id=settings.SYSTEM_LOG_THREAD_ID,
            text=text_message,
        )
        return ConversationHandler.END

    except Exception as exception:
        await update.message.reply_html(format_exception("recording a vote", exception))

    finally:
        return ConversationHandler.END
