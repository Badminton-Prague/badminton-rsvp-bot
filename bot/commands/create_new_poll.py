from ..models import Training
from ..models import Poll
from ..helpers.format_exception import format_exception
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from asgiref.sync import sync_to_async
from django.conf import settings
from ..asynchronous import aatomic


@aatomic
async def create_new_poll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Sends a predefined poll"""

    try:
        command = context.args

        when = command[0]
        courts = command[1]
        max_people = int(command[2].strip())

        thread_name = f"Game: {when}"  # Thread name in a format WHEN: "DD.MM.YYYY,day,HH:MM-HH:MM"
        poll_question = f"{courts}, Max people: {max_people}"
        poll_options = settings.POLL_OPTIONS
        chat_id = settings.BADMINTON_CHAT_ID

        poll = await sync_to_async(
            lambda: Poll.objects.create(
                chat_id=chat_id, poll_question=poll_question, thread_name=thread_name
            )
        )()
        await sync_to_async(
            lambda: Training.objects.create(poll=poll, max_people=max_people, when=when)
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
            format_exception("posting a new poll", exception)
        )

    finally:
        return ConversationHandler.END
