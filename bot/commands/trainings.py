from telegram.constants import ParseMode

from ..models import Training
from ..models import TrainingPoll
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from asgiref.sync import sync_to_async
from datetime import datetime, timedelta

bp_chat_id = -1002144970823

async def new_training(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    training = await sync_to_async(lambda: Training.objects.create(reference_id="test"))()
    await update.message.reply_text(text=str(training.created_at))
    return ConversationHandler.END


async def list_trainings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    db_trainings = await sync_to_async(lambda: list(Training.objects.all()))()
    trainings = list(map(
        lambda training: f'reference_id={training.reference_id} timestamp={training.created_at}',
        db_trainings
    ))
    await update.message.reply_text(text='\n'.join(trainings))
    return ConversationHandler.END

async def list_trainings_polls(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    db_trainings = await sync_to_async(lambda: list(TrainingPoll.objects.all()))()
    trainings = list(map(
        lambda training: f'reference_id={training.reference_id} timestamp={training.created_at}',
        db_trainings
    ))
    await update.message.reply_text(text='\n'.join(trainings))
    return ConversationHandler.END


async def create_new_poll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Sends a predefined poll"""

    command = context.args

    thread_name = command[0]  # Thread name in a format WHEN: "DD.MM.YYYY,day,HH:MM-HH:MM"
    poll_header = command[1]  # poll header in a format WHERE: "Place,courts"
    max_people = command[2]  # Max people in a format: "24"
    poll_options = ["Go!", "No go", "Just looking"]

    new_topic = await context.bot.createForumTopic(bp_chat_id, f"Game: {thread_name}")
    message = await context.bot.send_poll(
        bp_chat_id,
        poll_header + f", Max people: {max_people}",
        poll_options,
        is_anonymous=False,
        allows_multiple_answers=False,
        message_thread_id=new_topic.message_thread_id,
    )
    await context.bot.pin_chat_message(message.chat_id, message.message_id)

    training = await sync_to_async(lambda: TrainingPoll.objects.create(
        thread_name=thread_name,
        poll_header=poll_header,
        message_id=message.message_id,
        poll_id=message.poll.id,
        chat_id=update.effective_chat.id,
        thread_id=message.message_thread_id,
        max_people=max_people
    ))()

    return ConversationHandler.END

async def receive_poll_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Summarize a users poll vote"""
    answer = update.poll_answer

    db_poll: TrainingPoll = await sync_to_async(lambda: TrainingPoll.objects.filter(poll_id=answer.poll_id).first())()

    poll_options = ["Go!", "No go", "Just looking"]
    selected_options = answer.option_ids
    answer_string = ""
    for question_id in selected_options:
        if question_id != selected_options[-1]:
            answer_string += poll_options[question_id] + " and "
        else:
            answer_string += poll_options[question_id]
    if answer_string != "":
        await context.bot.send_message(
            bp_chat_id,
            f"{update.effective_user.mention_html()} voted for {answer_string} in a poll {db_poll.thread_name}",
            parse_mode=ParseMode.HTML
        )
    else:
        await context.bot.send_message(
            bp_chat_id,
            f"{update.effective_user.mention_html()} unvoted in a poll {db_poll.thread_name}",
            parse_mode=ParseMode.HTML
        )

    return ConversationHandler.END
