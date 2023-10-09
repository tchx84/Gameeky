import os

from gi.repository import GLib


def get_monotonic_time_ms():
    return int(GLib.get_monotonic_time() / 1000)


def get_data_path(*paths):
    return os.path.join(os.environ.get("DATA_DIR", ""), *paths)
