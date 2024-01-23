from django.apps import AppConfig
from bot.singleton import start_bot


class BotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bot'

    def ready(self):
        start_bot()



