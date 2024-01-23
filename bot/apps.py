from django.apps import AppConfig
import os


class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot'

    def ready(self):
        bot_enabled = os.environ.get("BOT_ENABLED") == "true"
        if bot_enabled:
            from bot.singleton import start_bot
            start_bot()



