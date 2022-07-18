from concurrent.futures import ThreadPoolExecutor
from typing import Callable

from config import Config


class ActionRunner:
    action_executor = ThreadPoolExecutor(max_workers=Config.action_threads)

    @classmethod
    def run(cls, action: Callable) -> None:
        cls.action_executor.submit(action)
