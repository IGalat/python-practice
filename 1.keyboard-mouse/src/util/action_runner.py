from asyncio import Future
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, ClassVar


class ActionRunner:
    # action_executor = ThreadPoolExecutor(max_workers=Config.action_threads)
    # todo; remove dependencies from config. should multi thread be possible?
    action_executor = ThreadPoolExecutor(max_workers=1)
    runnable: ClassVar[Future]

    @classmethod
    def run(cls, fn: Callable, /, *args, **kwargs) -> None:
        if not hasattr(cls, "runnable") or cls.runnable.done():  # no queue
            cls.runnable = cls.action_executor.submit(fn, *args, **kwargs)
