from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from bot.commands.send_qr_with_ms import build_qr_url

PRICE_WITHOUT_MS = 190

async def send_qr_without_ms(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_photo(photo=build_qr_url(PRICE_WITHOUT_MS, update.message.from_user))
    return ConversationHandler.END

