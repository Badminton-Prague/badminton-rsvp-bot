# example/urls.py
from django.urls import path
from example.views import index
import asyncio
from .bot.launcher import run_telegram_bot


urlpatterns = [
    path('', index),
]

asyncio.run(run_telegram_bot())