from gi.repository import GLib


def measure(func, *args, **kargs):
    before = GLib.get_monotonic_time()
    result = func(*args, **kargs)
    after = GLib.get_monotonic_time()

    print((after - before) / 1000)

    return result
