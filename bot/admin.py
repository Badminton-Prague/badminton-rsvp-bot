from django.contrib import admin

from bot.models import Poll, Training, TelegramUser, PollVote


class PollAdmin(admin.ModelAdmin):
    pass


class TrainingAdmin(admin.ModelAdmin):
    pass


class TelegramUserAdmin(admin.ModelAdmin):
    pass


class PollVoteAdmin(admin.ModelAdmin):
    pass


admin.site.register(Poll, PollAdmin)
admin.site.register(Training, TrainingAdmin)
admin.site.register(TelegramUser, TelegramUserAdmin)
admin.site.register(PollVote, PollVoteAdmin)
