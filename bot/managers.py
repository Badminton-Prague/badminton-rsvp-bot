from django.db.models import Manager


class TrainingManager(Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related("attendees")
            .prefetch_related("poll")
        )


class AttendeeManager(Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related("telegram_user")
            .prefetch_related("training")
        )
