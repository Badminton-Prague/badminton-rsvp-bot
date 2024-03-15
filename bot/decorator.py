from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler


def restrict_to_telegram_users(allowed_user_ids=[]):
    def decorator(function):
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
            sender_user_id = update.message.from_user.id
            if not (sender_user_id in allowed_user_ids):
                await update.message.reply_text(
                    text=f"This command can be run by admins only"
                )
                return ConversationHandler.END

            return await function(update, context)

        return wrapper

    return decorator
