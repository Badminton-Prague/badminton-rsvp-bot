from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.logging import log


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Hi, I am alive!")
    return ConversationHandler.END