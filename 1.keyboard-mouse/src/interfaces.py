class Suspendable:
    _suspended: bool = False

    def suspend(self) -> None:
        self._suspended = True

    def unsuspend(self) -> None:
        self._suspended = False

    def toggle_suspend(self) -> None:
        self._suspended = not self._suspended
