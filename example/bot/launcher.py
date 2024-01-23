from os import getenv
from telegram import Update
from telegram.ext import (
    Application,
    ConversationHandler,
    MessageHandler,
    CommandHandler,
    ChatMemberHandler,
    filters,
)
from .commands.common import echo, send_update_object
from .commands.payments import send_qr_with_ms, send_qr_without_ms


def run_telegram_bot():
    application = Application.builder().token(getenv("TOKEN")).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("qrwithms", send_qr_with_ms),
            CommandHandler("qrwithoutms", send_qr_without_ms),
            CommandHandler("test", send_update_object),
            CommandHandler("start", echo),
            MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
        ],
        states={},
        fallbacks=[]
    )

    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)