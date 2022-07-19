from concurrent.futures import ThreadPoolExecutor
from typing import Callable


class ActionRunner:
    # action_executor = ThreadPoolExecutor(max_workers=Config.action_threads)
    action_executor = ThreadPoolExecutor(max_workers=5)  # todo, remove dependencies from config

    @classmethod
    def run(cls, fn: Callable, /, *args, **kwargs) -> None:
        cls.action_executor.submit(fn, *args, **kwargs)

