from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler
)
from ..log import log


ALEXEY_TG_ID = 679950824


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Hi, I am alive!")
    log.info("123 check")
    return ConversationHandler.END


async def send_update_object(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await context.bot.send_message(chat_id=ALEXEY_TG_ID, text=str(update))
    return ConversationHandler.END