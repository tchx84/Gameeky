import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

from gi.repository import Gio, Gtk, Adw, GObject

from ...common.logger import logger
from ...common.utils import get_data_path
from ...common.scanner import Description


@Gtk.Template(filename=os.path.join(__dir__, "scene_creation_window.ui"))
class SceneCreationWindow(Adw.Window):
    __gtype_name__ = "SceneCreationWindow"

    __gsignals__ = {
        "done": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    path = Gtk.Template.Child()
    width = Gtk.Template.Child()
    height = Gtk.Template.Child()

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self.path.props.text = get_data_path("")

    @Gtk.Template.Callback("on_create_clicked")
    def __on_create_clicked(self, button: Gtk.Button) -> None:
        self.emit("done")
        self.close()

    @Gtk.Template.Callback("on_open_clicked")
    def __on_open_clicked(self, button: Gtk.Button) -> None:
        dialog = Gtk.FileDialog()
        dialog.open(callback=self.__on_open_dialog_finish)

    def __on_open_dialog_finish(
        self,
        dialog: Gtk.FileDialog,
        result: Gio.AsyncResult,
    ) -> None:
        try:
            file = dialog.open_finish(result)
        except Exception as e:
            logger.error(e)
        else:
            self.path.props.text = file.get_path()

    @property
    def data_path(self) -> None:
        return self.path.props.text

    @property
    def description(self) -> Description:
        return Description(
            width=int(self.width.props.value),
            height=int(self.height.props.value),
            spawn=Description(
                x=0,
                y=0,
                z=0,
            ),
            layers=[],
            overrides=Description(),
        )
