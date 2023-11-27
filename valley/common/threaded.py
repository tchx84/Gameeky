import threading

from typing import Callable, Optional
from gi.repository import GLib, GObject

from .utils import add_idle_source


class Threaded(threading.Thread, GObject.GObject):
    def __init__(self) -> None:
        GObject.GObject.__init__(self)
        threading.Thread.__init__(self)
        self._context: Optional[GLib.MainContext] = None
        self._mainloop: Optional[GLib.MainLoop] = None

    def do_run(self) -> None:
        raise NotImplementedError()

    def do_shutdown(self) -> None:
        raise NotImplementedError()

    def do_shutdown_sequence(self) -> None:
        if self._mainloop is None:
            return

        self.do_shutdown()
        self._mainloop.quit()

    def run(self) -> None:
        self._context = GLib.MainContext.new()
        self._context.push_thread_default()

        self._mainloop = GLib.MainLoop.new(self._context, False)

        self.do_run()

        self._mainloop.run()

    def emit(self, *args):
        GLib.idle_add(GObject.GObject.emit, self, *args)

    def exec(self, callback: Callable) -> None:
        add_idle_source(callback, context=self._context)

    def shutdown(self) -> None:
        self.exec(self.do_shutdown_sequence)
        self.join()

    @property
    def context(self) -> Optional[GLib.MainContext]:
        return self._context
