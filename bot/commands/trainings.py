from ..models import Training
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from asgiref.sync import sync_to_async


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