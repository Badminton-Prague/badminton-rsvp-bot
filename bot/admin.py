from django.contrib import admin

from bot.models import Poll, Training, TelegramUser, PollVote


class PollAdmin(admin.ModelAdmin):
    list_display = ("id", "thread_name", "poll_question", "created_at")
    search_fields = ("id", "thread_name", "poll_question")


class TrainingAdmin(admin.ModelAdmin):
    list_display = ("id", "get_poll", "date", "max_people", "created_at")
    search_fields = (
        "id",
        "poll__thread_name",
        "poll__poll_question",
        "date",
        "max_people",
        "created_at",
    )

    @admin.display(ordering="poll__thread_name", description="Poll")
    def get_poll(self, obj):
        return obj.poll.thread_name


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ("id", "telegram_id", "first_name", "last_name", "username")
    search_fields = ("id", "telegram_id", "first_name", "last_name", "username")


class PollVoteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_poll_name",
        "get_telegram_user",
        "go",
        "created_at",
    )
    search_fields = (
        "id",
        "poll__thread_name",
        "telegram_user__telegram_id",
        "telegram_user__first_name",
        "telegram_user__last_name",
        "telegram_user__username",
        "created_at",
    )

    list_filter = ("go",)

    @admin.display(ordering="poll__thread_name", description="Poll Name")
    def get_poll_name(self, obj):
        return obj.poll.thread_name

    @admin.display(ordering="telegram_user__id", description="Telegram user")
    def get_telegram_user(self, obj):
        return obj.telegram_user


admin.site.register(Poll, PollAdmin)
admin.site.register(Training, TrainingAdmin)
admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(PollVote, PollVoteAdmin)
