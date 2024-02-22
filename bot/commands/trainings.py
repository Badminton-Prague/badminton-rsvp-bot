from telegram.constants import ParseMode

from ..models import Training
from ..models import Poll
from ..models import PollVote
from ..models import TelegramUser
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from asgiref.sync import sync_to_async
from django.conf import settings
from ..asynchronous import aatomic
from types import SimpleNamespace


@aatomic
async def list_trainings_polls(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    try:
        db_trainings = await sync_to_async(
            lambda: list(
                Training.objects.all().values(
                    "poll__poll_question", "poll__thread_id", "id", "created_at"
                )
            )
        )()
        db_training_objects = list(map(lambda x: SimpleNamespace(**x), db_trainings))
        trainings = list(
            map(
                lambda training: f"reference_id={training.id} timestamp={training.created_at} poll question={training.poll__poll_question} thread id={training.poll__thread_id}",
                db_training_objects,
            )
        )
        await update.message.reply_text(text="\n".join(trainings))

    except Exception as exception:
        await update.message.reply_html(
            f"Error occurred while listing all polls:\n{exception.message}\n{exception.args}",
        )
        raise exception

    finally:
        return ConversationHandler.END


@aatomic
async def create_new_poll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Sends a predefined poll"""

    try:
        command = context.args

        max_people = int(command[2].strip())  # Max people in a format: "24"
        thread_name = f"Game: {command[0]}"  # Thread name in a format WHEN: "DD.MM.YYYY,day,HH:MM-HH:MM"
        poll_question = f"{command[1]}, Max people: {max_people}"
        poll_options = settings.POLL_OPTIONS
        chat_id = settings.BADMINTON_CHAT_ID

        poll = await sync_to_async(
            lambda: Poll.objects.create(
                chat_id=chat_id, poll_question=poll_question, thread_name=thread_name
            )
        )()
        await sync_to_async(
            lambda: Training.objects.create(poll=poll, max_people=max_people)
        )()

        new_topic = await context.bot.createForumTopic(
            settings.BADMINTON_CHAT_ID, thread_name
        )
        message = await context.bot.send_poll(
            settings.BADMINTON_CHAT_ID,
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
            f"Error occurred while posting a new training poll:\n{exception.message}\n{exception.args}",
        )
        raise exception

    finally:
        return ConversationHandler.END


@aatomic
async def receive_poll_answer(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Summarize a users poll vote"""
    answer = update.poll_answer
    effective_user = update.effective_user
    try:
        poll = await sync_to_async(
            lambda: Poll.objects.filter(poll_id=answer.poll_id).first()
        )()
        if poll is None:
            return ConversationHandler.END

        telegram_user, created = await sync_to_async(
            lambda: TelegramUser.objects.get_or_create(telegram_id=effective_user.id)
        )()
        await sync_to_async(
            lambda: TelegramUser.objects.filter(pk=telegram_user.pk).update(
                first_name=effective_user.first_name,
                last_name=effective_user.last_name,
                username=effective_user.username,
            )
        )()

        selected_option_ids = answer.option_ids
        if len(selected_option_ids) == 0:
            await sync_to_async(
                lambda: PollVote.objects.filter(
                    poll=poll, telegram_user=telegram_user
                ).delete()
            )()
        else:
            selected_option = settings.POLL_OPTIONS[selected_option_ids[0]]
            if (
                selected_option != settings.POLL_GO_OPTION
                and selected_option != settings.POLL_NO_GO_OPTION
            ):
                return ConversationHandler.END

            poll_vote, created = await sync_to_async(
                lambda: PollVote.objects.get_or_create(
                    poll_id=poll.pk,
                    telegram_user=telegram_user
                )
            )()

            setattr(poll_vote, "go", selected_option == settings.POLL_GO_OPTION)
            await sync_to_async(lambda: poll_vote.save())()

    except Exception as exception:
        await update.message.reply_html(
            f"Error occurred while posting a new training poll:\n{exception.message}\n{exception.args}",
        )
        raise exception

    finally:
        return ConversationHandler.END
