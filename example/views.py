import asyncio
import threading
from django.http import HttpResponse
from .background_bot import main as run_bot_on_background


def run_telegram_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_bot_on_background())


def index(request):
    thread = threading.Thread(target=run_telegram_bot)
    thread.start()

    return HttpResponse("Telegram bot is running in the background.")