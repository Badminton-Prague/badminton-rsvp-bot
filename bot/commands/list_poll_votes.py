from asgiref.sync import sync_to_async
from asgiref.sync import sync_to_async
from types import SimpleNamespace
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.helpers.get_training_by_thread_id import get_training_by_thread_id
from bot.models import PollVote
from ..helpers.format_exception import format_exception


async def list_poll_votes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        db_votes = await sync_to_async(
            lambda: list(
                PollVote.objects.filter(
                    poll__thread_id=update.message.message_thread_id, go=True
                )
                .order_by("id")
                .prefetch_related("telegram_user")
            )
        )()
        training = await get_training_by_thread_id(update.message.message_thread_id)
        votes = list(
            map(
                lambda vote: f"User {vote.telegram_user.message_username} {'will' if vote.go else 'will NOT'} attend training on {training.when}",
                db_votes,
            )
        )
        attendees = "\n".join(votes[: training.max_people])
        waiting_list = "\n".join(votes[training.max_people :])
        await update.message.reply_html(
            f"Attendees:\n{attendees}\n\n\nWaiting list:\n{waiting_list}"
        )
    except Exception as exception:
        await update.message.reply_html(
            format_exception("listing poll votes", exception)
        )

    finally:
        return ConversationHandler.END
