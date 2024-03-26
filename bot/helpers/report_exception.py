from telegram import Bot, Message
from django.conf import settings
from .format_exception import format_exception


async def report_exception(
    action: str, exception: Exception, bot: Bot = None, message: Message = None
):
    formatted_message = format_exception(action, exception)
    if bot is not None:
        await bot.send_message(
            chat_id=settings.ERROR_LOG_CHAT_ID,
            message_thread_id=settings.ERROR_LOG_THREAD_ID,
            text=formatted_message,
        )

    if message is not None:
        await message.reply_html(formatted_message)
