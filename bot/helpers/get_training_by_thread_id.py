from asgiref.sync import sync_to_async
from bot.models import Training
from typing import Optional


async def get_training_by_thread_id(
    message_thread_id: int,
) -> Optional[Training]:
    return await sync_to_async(
        lambda: Training.objects.filter(poll__thread_id=message_thread_id).first()
    )()
