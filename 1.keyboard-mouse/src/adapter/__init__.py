from adapter.base import BaseAdapter


def get_adapter(chosen_adapter: str | BaseAdapter | None) -> BaseAdapter:
    if chosen_adapter is None:
        return _default_adapter()
        # todo choose by sys.platform "Win32" or "linux"

    if isinstance(chosen_adapter, str):
        # todo  parse of options
        return _default_adapter()

    else:
        return chosen_adapter


def _default_adapter() -> BaseAdapter:
    from adapter.pynput import PynpytAdapter

    return PynpytAdapter()
