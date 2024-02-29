from types import SimpleNamespace
from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from bot.asynchronous import aatomic
from bot.models import Training
from ..helpers.format_exception import format_exception


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
        await update.message.reply_html(format_exception("listing polls", exception))

    finally:
        return ConversationHandler.END
