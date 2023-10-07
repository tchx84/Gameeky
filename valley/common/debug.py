from gi.repository import GLib

from .logger import logger


def measure(func, *args, **kargs):
    before = GLib.get_monotonic_time()
    result = func(*args, **kargs)
    after = GLib.get_monotonic_time()

    logger.debug("Measured %s for %d ms", func.__name__, (after - before) / 1000)

    return result
