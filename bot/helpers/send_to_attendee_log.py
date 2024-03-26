from django.conf import settings
from telegram import Bot
from bot.models import Attendee
from .async_render_to_string import async_render_to_string


async def send_to_attendee_log(bot: Bot, attendee: Attendee):
    rendered_message = await async_render_to_string(
        "send_to_attendee_log.txt", dict(attendee=attendee)
    )
    await bot.send_message(
        chat_id=settings.ATTENDEE_LOG_CHAT_ID,
        message_thread_id=settings.ATTENDEE_LOG_THREAD_ID,
        text=rendered_message,
    )
