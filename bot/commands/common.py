from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.logging import log


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Hi, I am alive! Hello world! 2")
    return ConversationHandler.END


async def plus_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    effective_user = update.effective_user
    message = update.message.text
    if message.__contains__("+1") or message.__contains__("+2") or message.__contains__("+3"):
        await update.message.reply_text(f"User: {effective_user.username} with id {effective_user.id} wrote {message} in {update.effective_chat.id}")

    return ConversationHandler.END


async def test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(text=str(update))
    return ConversationHandler.END
