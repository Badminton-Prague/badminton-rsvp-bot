from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from bot.models import Training
from ..helpers.format_exception import format_exception
from ..helpers.safe_get import safe_get
from django.template.loader import render_to_string


async def list_trainings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    def executor() -> str:
        most_recent_count = int(safe_get(context.args, 0, 10))
        trainings = list(Training.objects.all().order_by("-id")[:most_recent_count])

        return render_to_string(
            "list_trainings.txt",
            dict(
                trainings=trainings,
                most_recent_count=most_recent_count,
            ),
        )

    try:
        rendered_message = await sync_to_async(executor)()
        await update.message.reply_text(text=rendered_message)

    except Exception as exception:
        await update.message.reply_html(
            format_exception("listing trainings", exception)
        )

    finally:
        return ConversationHandler.END
