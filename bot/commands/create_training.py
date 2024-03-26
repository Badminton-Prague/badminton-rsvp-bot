import re
from datetime import date
from django.db import transaction
from asgiref.sync import sync_to_async
from django.conf import settings
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from typing import NamedTuple

from ..asynchronous import MAIN_EVENT_LOOP
from ..helpers.report_exception import report_exception
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


async def create_training(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Sends a predefined poll"""

    @transaction.atomic()
    def executor() -> Training:
        args = parse_command_args(update.message.text)
        poll_options = settings.POLL_OPTIONS
        chat_id = settings.BADMINTON_CHAT_ID

        training = Training.objects.create(
            attendees_limit=args.attendees_limit, date=args.training_date
        )

        poll = Poll.objects.create(
            chat_id=chat_id,
            poll_question=args.poll_question,
            thread_name=args.thread_name,
            training=training,
        )

        new_topic = MAIN_EVENT_LOOP.run_until_complete(
            context.bot.createForumTopic(settings.BADMINTON_CHAT_ID, args.thread_name)
        )

        message = MAIN_EVENT_LOOP.run_until_complete(
            context.bot.send_poll(
                chat_id,
                args.poll_question,
                poll_options,
                is_anonymous=False,
                allows_multiple_answers=False,
                message_thread_id=new_topic.message_thread_id,
            )
        )

        MAIN_EVENT_LOOP.run_until_complete(
            context.bot.pin_chat_message(message.chat_id, message.message_id)
        )

        return training

    try:
        await sync_to_async(executor)()

    except Exception as exception:
        await report_exception(
            "posting a new training", exception, bot=context.bot, message=update.message
        )

    finally:
        return ConversationHandler.END
