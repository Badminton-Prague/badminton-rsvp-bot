from types import SimpleNamespace
from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from bot.models import Training
from ..helpers.format_exception import format_exception
from ..helpers.safe_get import safe_get


async def list_trainings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        most_recent_count = int(safe_get(context.args, 0, 10))

        db_trainings = await sync_to_async(
            lambda: list(
                Training.objects.all()
                .values(
                    "id",
                    "poll__poll_question",
                    "poll__thread_name",
                    "date",
                    "attendees_limit",
                )
                .order_by("-id")[:most_recent_count]
            )
        )()
        db_training_objects = list(map(lambda x: SimpleNamespace(**x), db_trainings))
        trainings = list(
            map(
                lambda training: f"{training.id}: {training.poll__thread_name} on {training.date} (max attendees={training.attendees_limit})",
                db_training_objects,
            )
        )
        await update.message.reply_text(
            text=f"{most_recent_count} recent training:\n" + "\n".join(trainings)
        )

    except Exception as exception:
        await update.message.reply_html(
            format_exception("listing trainings", exception)
        )

    finally:
        return ConversationHandler.END
