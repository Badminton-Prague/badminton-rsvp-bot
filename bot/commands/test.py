from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler


async def test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(text=str(update))
    return ConversationHandler.END
