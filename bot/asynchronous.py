import asyncio


async def awaitable_to_coroutine(awaitable):
    try:
        result = await awaitable
        return result
    except Exception as e:
        # Handle exceptions raised during awaitable execution
        raise e


MAIN_EVENT_LOOP = asyncio.new_event_loop()
