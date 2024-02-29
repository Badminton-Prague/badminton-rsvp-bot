from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from bot.asynchronous import aatomic
from bot.helpers.get_training_by_poll_id import get_training_by_poll_id
from bot.helpers.record_vote import record_vote
from bot.helpers.retract_first_vote import retract_first_vote
from bot.helpers.get_and_update_telegram_user import get_and_update_telegram_user
from django.conf import settings
from ..helpers.format_exception import format_exception


@aatomic
async def receive_poll_answer(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Summarize a users poll vote"""
    poll_answer = update.poll_answer
    effective_user = update.effective_user

    try:
        # Find training's details
        training = await get_training_by_poll_id(poll_answer.poll_id)
        if training is None:
            return ConversationHandler.END
        poll = training.poll

        # Update a user
        telegram_user = await get_and_update_telegram_user(effective_user)

        # Record a vote
        selected_option_ids = poll_answer.option_ids
        if len(selected_option_ids) == 0:
            await retract_first_vote(poll, telegram_user)
        else:
            selected_option = settings.POLL_OPTIONS[selected_option_ids[0]]

            if selected_option == settings.POLL_GO_OPTION:
                await record_vote(poll, telegram_user)

                text_message = f"User {telegram_user.message_username} will attend training on {training.when}"
                await context.bot.send_message(
                    chat_id=poll.chat_id,
                    message_thread_id=poll.thread_id,
                    text=text_message,
                )
                await context.bot.send_message(
                    chat_id=settings.SYSTEM_LOG_CHAT_ID,
                    message_thread_id=settings.SYSTEM_LOG_THREAD_ID,
                    text=text_message,
                )
            elif selected_option == settings.POLL_NO_GO_OPTION:
                await retract_first_vote(poll, telegram_user)

                text_message = f"User {telegram_user.message_username} will NOT attend training on {training.when}"
                await context.bot.send_message(
                    chat_id=poll.chat_id,
                    message_thread_id=poll.thread_id,
                    text=text_message,
                )
                await context.bot.send_message(
                    chat_id=settings.SYSTEM_LOG_CHAT_ID,
                    message_thread_id=settings.SYSTEM_LOG_THREAD_ID,
                    text=text_message,
                )
    except Exception as exception:
        await context.bot.send_message(
            chat_id=settings.SYSTEM_LOG_CHAT_ID,
            message_thread_id=settings.SYSTEM_LOG_THREAD_ID,
            text=format_exception("recording a poll vote", exception),
        )

    finally:
        return ConversationHandler.END
