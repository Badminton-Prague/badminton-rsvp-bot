from asgiref.sync import sync_to_async
from django.db import transaction
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.helpers.get_and_update_telegram_user import get_and_update_telegram_user
from bot.helpers.record_attendee import record_attendee
from ..helpers.async_render_to_string import async_render_to_string
from ..helpers.report_exception import report_exception
from ..helpers.send_to_attendee_log import send_to_attendee_log
from ..models import PLUS_ONE_COMMAND_SOURCE, Training, TelegramUser
from bot.models import Attendee


async def plus_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    @transaction.atomic()
    def executor() -> Attendee:
        effective_user = update.effective_user

        training = Training.objects.filter(
            poll__thread_id=update.message.message_thread_id
        ).first()
        if training is None:
            raise Exception(
                f"No training found by thread ID#{update.message.message_thread_id}"
            )

        telegram_user = get_and_update_telegram_user(effective_user)
        return record_attendee(training, telegram_user, PLUS_ONE_COMMAND_SOURCE)

    try:
        attendee = await sync_to_async(executor)()
        rendered_message = await async_render_to_string(
            "plus_handler_response.txt", dict(attendee=attendee)
        )
        await update.message.reply_text(rendered_message)
        await send_to_attendee_log(context.bot, attendee)

    except Exception as exception:
        await report_exception("handling +1", exception, bot=context.bot)

    finally:
        return ConversationHandler.END
