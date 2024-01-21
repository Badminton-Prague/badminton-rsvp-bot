# example/urls.py
from django.urls import path

from example.views import index
import asyncio
import threading
from os import getenv
from telegram import Update
from telegram.ext import (
    Application,
    ConversationHandler,
    MessageHandler,
    filters,
)
from .commands import echo


def run_telegram_bot():
    application = Application.builder().token(getenv("TOKEN")).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT, echo)],
        states={},
        fallbacks=[]
    )

    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


def run_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_telegram_bot())


urlpatterns = [
    path('', index),
]

thread = threading.Thread(target=run_loop)
thread.start()
