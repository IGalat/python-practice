from concurrent.futures import ThreadPoolExecutor
from typing import Callable


class ActionRunner:
    # action_executor = ThreadPoolExecutor(max_workers=Config.action_threads)
    action_executor = ThreadPoolExecutor(max_workers=5)  # todo

    @classmethod
    def run(cls, action: Callable) -> None:
        cls.action_executor.submit(action)
