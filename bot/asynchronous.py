import asyncio
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
from typing import TypeVar, Callable
from typing_extensions import ParamSpec
from functools import partial

_fork_context = multiprocessing.get_context("fork")
_process_pool_executor = ProcessPoolExecutor(max_workers=1, mp_context=_fork_context)
MAIN_EVENT_LOOP = asyncio.new_event_loop()

T = TypeVar("T")
P = ParamSpec("P")


async def asyncify(fn: Callable[P, T], *args: P) -> T:
    return await asyncio.get_running_loop().run_in_executor(
        _process_pool_executor,
        partial(fn, *args),
    )
