from django.db import transaction
from django.template.loader import render_to_string
from telegram import Update
from telegram.ext import ContextTypes

from bot.models import Training
from bot.helpers.run_sync_function_in_executor import run_sync_function_in_executor
from ..decorator import catch_all_exceptions_in_tg_handlers
from ..helpers.safe_get import safe_get


@transaction.atomic()
def db_transaction(most_recent_count: int) -> str:
    trainings = list(Training.objects.all().order_by("-id")[:most_recent_count])

    return render_to_string(
        "list_trainings_response.txt",
        dict(
            trainings=trainings,
            most_recent_count=most_recent_count,
        ),
    )


@catch_all_exceptions_in_tg_handlers("listing trainings")
async def list_trainings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    most_recent_count = int(safe_get(context.args, 0, 10))
    rendered_message = await run_sync_function_in_executor(
        db_transaction, arguments=(most_recent_count,)
    )
    await update.message.reply_text(text=rendered_message)
