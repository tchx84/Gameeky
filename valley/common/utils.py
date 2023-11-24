import os

from typing import Callable, Optional, Tuple
from gi.repository import GLib, Gio


def get_time_milliseconds() -> int:
    return int(GLib.get_monotonic_time() / 1000)


def set_data_path(path) -> None:
    os.environ["DATA_DIR"] = path


def get_data_path(*paths) -> str:
    return os.path.join(os.environ.get("DATA_DIR", os.path.expanduser("~")), *paths)


def get_data_folder(*paths):
    return Gio.File.new_for_path(os.path.join(get_data_path(""), *paths))


def get_relative_path(path: str) -> str:
    if not os.path.isabs(path):
        return path

    return os.path.relpath(path, os.environ.get("DATA_DIR", ""))


def valid_file(path) -> bool:
    if GLib.file_test(path, GLib.FileTest.EXISTS) is False:
        return False
    if GLib.file_test(path, GLib.FileTest.IS_REGULAR) is False:
        return False

    return True


def valid_directory(path) -> bool:
    if GLib.file_test(path, GLib.FileTest.EXISTS) is False:
        return False
    if GLib.file_test(path, GLib.FileTest.IS_DIR) is False:
        return False

    return True


def find_context() -> GLib.MainContext:
    if (context := GLib.MainContext.get_thread_default()) is None:
        context = GLib.MainContext.default()

    return context


def add_timeout_source(interval: float, callback: Callable) -> int:
    context = find_context()

    source = GLib.timeout_source_new(interval)
    source.set_priority(GLib.PRIORITY_DEFAULT)
    source.set_callback(callback)
    source.attach(context)

    return source.get_id()


def add_idle_source(
    callback: Callable,
    data: Optional[Tuple] = None,
    context: Optional[GLib.MainContext] = None,
) -> int:
    context = find_context() if context is None else context
    data = () if data is None else data

    def idle_callback(*args) -> int:
        callback(*data)
        return GLib.SOURCE_REMOVE

    source = GLib.idle_source_new()
    source.set_callback(idle_callback)
    source.attach(context)

    return source.get_id()


def remove_source_id(source_id: int) -> None:
    context = find_context()
    context.find_source_by_id(source_id).destroy()


def wait(milliseconds: int) -> None:
    if not milliseconds:
        return

    called = False
    context = GLib.MainContext.default()

    def callback() -> int:
        nonlocal called
        called = True
        return GLib.SOURCE_REMOVE

    GLib.timeout_add(milliseconds, callback)

    while not called:
        while context.pending():
            context.iteration(True)


def clamp(maximum, minimum, value):
    return min(max(minimum, value), maximum)


def division(dividend, divisor):
    return dividend / divisor if divisor > 0 else 0


def element(array, index):
    return array[index] if len(array) > 0 else None


def oscillate(maximum, minimum, value):
    range = maximum - minimum
    return minimum + abs(((value + range) % (range * 2)) - range)
