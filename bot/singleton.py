from threading import Thread
from telegram.ext import (
    Application,
    ConversationHandler,
    CommandHandler,
    PollAnswerHandler,
)

from bot.helpers.run_sync_function_in_executor import MAIN_EVENT_LOOP
from bot.commands.list_trainings import list_trainings
from bot.commands.create_training import create_training
from bot.commands.plus_handler import plus_handler
from bot.commands.receive_poll_answer import receive_poll_answer
from bot.commands.list_attendees import list_attendees
from bot.commands.remove_attendee import remove_attendee
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
            CommandHandler("list_trainings", list_trainings),
            CommandHandler("list_attendees", list_attendees),
            CommandHandler("remove_attendee", remove_attendee),
            CommandHandler("create_training", create_training),
            CommandHandler("1", plus_handler),
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
    asyncio.set_event_loop(MAIN_EVENT_LOOP)
    asyncio.run(_run_telegram_bot_coro())


@run_once_only
def start_bot():
    thread = Thread(
        target=_run_telegram_bot,
        name="telegram_bot",
    )

    thread.daemon = True
    thread.start()
