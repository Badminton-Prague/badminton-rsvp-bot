from asgiref.sync import sync_to_async
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from bot.logging import log
from bot.models import PollVote, TelegramUser, Poll
from vercel_app.settings import DIMA_B_TEST_CHAT_ID


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Hi, I am alive! Hello world! 2")
    return ConversationHandler.END


async def plus_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    effective_user = update.effective_user
    message = update.message.text

    poll2 = await sync_to_async(
        lambda: Poll.objects.filter(thread_id=update.message.message_thread_id).first()
    )()

    if message.__contains__("+1") or message.__contains__("+2") or message.__contains__("+3"):
        await update.message.reply_text(f"User: {effective_user.mention_html()} "
                                        f"with id {effective_user.id} wrote {message} "
                                        f"in {update.message.message_thread_id} "
                                        f" aaa {poll2.poll_id}")


    telegram_user, created = await sync_to_async(
        lambda: TelegramUser.objects.get_or_create(telegram_id=effective_user.id)
    )()

    poll_vote, created = await sync_to_async(
        lambda: PollVote.objects.get_or_create(
            poll_id=poll2.pk,
            telegram_user=telegram_user
        )
    )()

    setattr(poll_vote, "go", True)
    await sync_to_async(lambda: poll_vote.save())()

    return ConversationHandler.END


async def test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(text=str(update))
    return ConversationHandler.END
