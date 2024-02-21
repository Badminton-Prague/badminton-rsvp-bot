from threading import Thread
from telegram.ext import (
    Application,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters,
    PollAnswerHandler,
)
from bot.commands.trainings import (
    create_new_poll,
    list_trainings_polls,
    receive_poll_answer,
)
from bot.commands.payments import send_qr_with_ms, send_qr_without_ms
from bot.commands.common import start, test
from django.conf import settings
from bot.run_once_only import run_once_only
import asyncio


async def _run_telegram_bot_coro():
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("qrwithms", send_qr_with_ms),
            CommandHandler("qrwithoutms", send_qr_without_ms),
            CommandHandler("test", test),
            CommandHandler("start", start),
            CommandHandler("list_trainings_polls", list_trainings_polls),
            CommandHandler("create_new_poll", create_new_poll),
            MessageHandler(filters.TEXT & ~filters.COMMAND, start),
        ],
        states={},
        fallbacks=[],
    )

    telegram_application = (
        Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    )
    telegram_application.add_handler(conv_handler)
    telegram_application.add_handler(PollAnswerHandler(receive_poll_answer))
    async with telegram_application:
        await telegram_application.initialize()
        await telegram_application.start()
        await telegram_application.updater.start_polling()
        await asyncio.sleep(100_000_000)


def _run_telegram_bot():
    asyncio.run(_run_telegram_bot_coro())


@run_once_only
def start_bot():
    thread = Thread(
        target=_run_telegram_bot,
        name="telegram_bot",
    )

    thread.daemon = True
    thread.start()
