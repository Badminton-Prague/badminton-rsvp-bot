from typing import Optional

from django.db import transaction
from telegram import Update, User, Message
from telegram.ext import ContextTypes

from bot.helpers.get_and_update_telegram_user import get_and_update_telegram_user
from bot.helpers.record_attendee import record_attendee
from bot.models import Attendee
from bot.helpers.run_sync_function_in_executor import run_sync_function_in_executor
from ..decorator import catch_all_exceptions_in_tg_handlers
from ..helpers.async_render_to_string import async_render_to_string
from ..helpers.send_to_attendee_log import send_to_attendee_log
from ..models import (
    PLUS_ONE_COMMAND_SOURCE,
    Training,
    FeatureFlag,
    DISABLE_PLUS_ONE_COMMAND,
)


@transaction.atomic()
def db_transaction(user: User, message: Message) -> Optional[Attendee]:
    all_feature_flags = list(FeatureFlag.objects.all())
    plus_one_command_disabled = (
        FeatureFlag.objects.filter(feature_flag=DISABLE_PLUS_ONE_COMMAND).first()
        is not None
    )
    if plus_one_command_disabled is True:
        return

    training = Training.objects.filter(
        poll__thread_id=message.message_thread_id
    ).first()
    if training is None:
        raise Exception(f"No training found by thread ID#{message.message_thread_id}")

    telegram_user = get_and_update_telegram_user(user)
    return record_attendee(training, telegram_user, PLUS_ONE_COMMAND_SOURCE)


@catch_all_exceptions_in_tg_handlers("handling +1", respond_to_message=False)
async def plus_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    attendee = await run_sync_function_in_executor(
        db_transaction,
        arguments=(
            update.effective_user,
            update.message,
        ),
    )
    if attendee is None:
        return
    rendered_message = await async_render_to_string(
        "plus_handler_response.txt", dict(attendee=attendee)
    )
    await update.message.reply_text(rendered_message)
    await send_to_attendee_log(context.bot, attendee)
