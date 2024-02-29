from asgiref.sync import sync_to_async
from bot.models import Training
from typing import Optional


async def get_training_by_poll_id(
    poll_id: str,
) -> Optional[Training]:
    return await sync_to_async(
        lambda: Training.objects.filter(poll__poll_id=poll_id)
        .prefetch_related("poll")
        .first()
    )()
