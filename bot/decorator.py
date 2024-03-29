from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from bot.helpers.report_exception import report_exception


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


def catch_all_exceptions_in_tg_handlers(
    action: str, respond_to_message: bool = True, send_to_error_log: bool = True
):
    def decorator(function):
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
            try:
                await function(update, context)

            except Exception as exception:
                await report_exception(
                    action,
                    exception,
                    bot=context.bot if send_to_error_log else None,
                    message=update.message if respond_to_message else None,
                )

            finally:
                return ConversationHandler.END

        return wrapper

    return decorator
