from ..models import Training
from ..models import Poll
from ..helpers.format_exception import format_exception
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from asgiref.sync import sync_to_async
from django.conf import settings
from ..asynchronous import aatomic
import re
from datetime import date


@aatomic
async def create_training(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Sends a predefined poll"""

    try:

        lines = update.message.text.split("\n")
        thread_name = lines[1].strip()
        poll_question = lines[2].strip()
        max_people = int(lines[3].strip())

        date_string = lines[4].strip()
        date_matches = re.match("^(\d{4})-(\d{2})-(\d{2})$", date_string)
        date_year = int(date_matches[1])
        date_month = int(date_matches[2])
        date_day = int(date_matches[3])
        training_day = date(date_year, date_month, date_day)

        poll_options = settings.POLL_OPTIONS
        chat_id = settings.BADMINTON_CHAT_ID

        poll = await sync_to_async(
            lambda: Poll.objects.create(
                chat_id=chat_id, poll_question=poll_question, thread_name=thread_name
            )
        )()
        await sync_to_async(
            lambda: Training.objects.create(
                poll=poll, max_people=max_people, date=training_day
            )
        )()

        new_topic = await context.bot.createForumTopic(
            settings.BADMINTON_CHAT_ID, thread_name
        )
        message = await context.bot.send_poll(
            chat_id,
            poll_question,
            poll_options,
            is_anonymous=False,
            allows_multiple_answers=False,
            message_thread_id=new_topic.message_thread_id,
        )

        await sync_to_async(
            lambda: Poll.objects.filter(pk=poll.pk).update(
                thread_id=message.message_thread_id,
                message_id=message.message_id,
                poll_id=message.poll.id,
            )
        )()

        await context.bot.pin_chat_message(message.chat_id, message.message_id)

    except Exception as exception:
        await update.message.reply_html(
            format_exception("posting a new training", exception)
        )

    finally:
        return ConversationHandler.END
