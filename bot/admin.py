from django.contrib import admin

from bot.models import Poll, Training, TelegramUser, Attendee


class PollAdmin(admin.ModelAdmin):
    list_display = ("id", "thread_name", "poll_question", "created_at")
    search_fields = ("id", "thread_name", "poll_question")


class TrainingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_poll_tread_name",
        "get_poll_question",
        "date",
        "attendees_limit",
        "created_at",
    )
    search_fields = (
        "id",
        "poll__thread_name",
        "poll__poll_question",
        "date",
        "attendees_limit",
        "created_at",
    )

    @admin.display(ordering="poll__thread_name", description="Training's Thread Name")
    def get_poll_tread_name(self, obj):
        return obj.poll.thread_name

    @admin.display(
        ordering="poll__poll_question", description="Training's Poll Question"
    )
    def get_poll_question(self, obj):
        return obj.poll.poll_question


class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", "first_name", "last_name", "username")
    search_fields = ("telegram_id", "first_name", "last_name", "username")


class AttendeeAdmin(admin.ModelAdmin):
    list_display = (
        "get_training_thread_name",
        "get_telegram_user",
        "go",
        "source",
        "created_at",
    )

    search_fields = (
        "training__poll__thread_name",
        "telegram_user__telegram_id",
        "telegram_user__first_name",
        "telegram_user__last_name",
        "telegram_user__username",
    )

    list_filter = (
        "go",
        "source",
    )

    @admin.display(
        ordering="training__poll__thread_name", description="Training's Thread Name"
    )
    def get_training_thread_name(self, obj):
        return obj.training.poll.thread_name

    @admin.display(ordering="telegram_user__id", description="Telegram user")
    def get_telegram_user(self, obj):
        return obj.telegram_user


admin.site.register(Poll, PollAdmin)
admin.site.register(Training, TrainingAdmin)
admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(Attendee, AttendeeAdmin)
