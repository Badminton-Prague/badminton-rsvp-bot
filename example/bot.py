import asyncio

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)
from os import getenv


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_html(text="hello world!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_html(text="help me!")


async def run_bot(telegram_update):
    application = Application.builder().token(getenv("TOKEN")).build()
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))

    # Start application
    await application.update_queue.put(
        Update.de_json(data=telegram_update, bot=application.bot)
    )

    async with application:
        await application.start()
        await application.stop()


async def set_webhook(url):
    application = Application.builder().token(getenv("TOKEN")).build()
    await application.bot.set_webhook(url)

    async with application:
        await application.start()
        await application.stop()

