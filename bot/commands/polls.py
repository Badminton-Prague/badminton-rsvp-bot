from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler


POLL_OPTIONS = ["Go!", "No go...", "Just looking"]


async def send_poll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Send poll
    message = await context.bot.send_poll(
        update.effective_chat.id,
        "Skalka, courts 1-14",
        POLL_OPTIONS,
        is_anonymous=False,
        allows_multiple_answers=True,
    )
    # Save some info about the poll the bot_data for later use in receive_poll_answer
    payload = {
        message.poll.id: {
            "questions": POLL_OPTIONS,
            "message_id": message.message_id,
            "chat_id": update.effective_chat.id,
            "answers": 0,
        }
    }
    context.bot_data.update(payload)

    return ConversationHandler.END


async def receive_poll_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    answer = update.poll_answer
    answered_poll = context.bot_data[answer.poll_id]
    try:
        questions = answered_poll["questions"]
    except KeyError:
        return ConversationHandler.END
    selected_options = answer.option_ids
    option_string = ""
    for question_id in selected_options:
        if question_id != selected_options[-1]:
            option_string += questions[question_id] + " and "
        else:
            option_string += questions[question_id]

    # build message for voting and retracting
    message = f"{update.effective_user.mention_html()} chose \"{option_string}\" option" \
        if update.poll_answer.option_ids \
        else f"{update.effective_user.mention_html()} retracted vote"

    await context.bot.send_message(answered_poll["chat_id"], message, parse_mode=ParseMode.HTML)

    return ConversationHandler.END
