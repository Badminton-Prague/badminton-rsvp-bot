import re
from datetime import date
from typing import NamedTuple

from django.conf import settings
from django.db import transaction
from telegram import Update, Message, ForumTopic
from telegram.ext import ContextTypes

from bot.helpers.run_sync_function_in_executor import run_sync_function_in_executor
from ..decorator import catch_all_exceptions_in_tg_handlers
from ..models import Poll
from ..models import Training


class CommandArgs(NamedTuple):
    thread_name: str
    poll_question: str
    attendees_limit: int
    training_date: date


def parse_command_args(command: str) -> CommandArgs:
    lines = command.split("\n")
    thread_name = lines[1].strip()
    poll_question = lines[2].strip()
    attendees_limit = int(lines[3].strip())

    date_string = lines[4].strip()
    date_matches = re.match("^(\d{4})-(\d{2})-(\d{2})$", date_string)
    date_year = int(date_matches[1])
    date_month = int(date_matches[2])
    date_day = int(date_matches[3])
    training_date = date(date_year, date_month, date_day)

    return CommandArgs(thread_name, poll_question, attendees_limit, training_date)


@transaction.atomic()
def db_transaction(
    args: CommandArgs, chat_id: int, message: Message, forum_topic: ForumTopic
):
    training = Training.objects.create(
        attendees_limit=args.attendees_limit, date=args.training_date
    )

    Poll.objects.create(
        chat_id=chat_id,
        message_id=message.message_id,
        poll_id=message.poll.id,
        poll_question=args.poll_question,
        thread_id=forum_topic.message_thread_id,
        thread_name=args.thread_name,
        training=training,
    )


@catch_all_exceptions_in_tg_handlers("posting a new training")
async def create_training(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a predefined poll"""
    args = parse_command_args(update.message.text)
    poll_options = settings.POLL_OPTIONS
    chat_id = settings.BADMINTON_CHAT_ID

    forum_topic = await context.bot.createForumTopic(
        settings.BADMINTON_CHAT_ID, args.thread_name
    )

    message = await context.bot.send_poll(
        chat_id,
        args.poll_question,
        poll_options,
        is_anonymous=False,
        allows_multiple_answers=False,
        message_thread_id=forum_topic.message_thread_id,
    )

    await context.bot.pin_chat_message(message.chat_id, message.message_id)
    await run_sync_function_in_executor(
        db_transaction, arguments=(args, chat_id, message, forum_topic)
    )
