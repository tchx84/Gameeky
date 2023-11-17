import os

from gi.repository import GLib


def get_time_milliseconds() -> int:
    return int(GLib.get_monotonic_time() / 1000)


def set_data_path(path) -> None:
    os.environ["DATA_DIR"] = path


def get_data_path(*paths) -> str:
    return os.path.join(os.environ.get("DATA_DIR", ""), *paths)


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


def clamp(maximum, minimum, value):
    return min(max(minimum, value), maximum)


def division(dividend, divisor):
    return dividend / divisor if divisor > 0 else 0


def element(array, index):
    return array[index] if len(array) > 0 else None


def oscillate(maximum, minimum, value):
    range = maximum - minimum
    return minimum + abs(((value + range) % (range * 2)) - range)
