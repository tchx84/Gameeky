import os

__dir__ = os.path.dirname(os.path.abspath(__file__))

from gi.repository import Gio, Gtk, Adw, GObject

from ...common.logger import logger
from ...common.utils import get_data_path, valid_directory
from ...common.scanner import Description
from ...common.definitions import Direction, State


@Gtk.Template(filename=os.path.join(__dir__, "entity_new_window.ui"))
class EntityNewWindow(Adw.Window):
    __gtype_name__ = "EntityNewWindow"

    __gsignals__ = {
        "done": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    toast = Gtk.Template.Child()
    project = Gtk.Template.Child()

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self.project.props.text = get_data_path("")

    def _notify(self, title) -> None:
        toast = Adw.Toast()
        toast.props.title = title
        toast.props.timeout = 3

        self.toast.add_toast(toast)

    @Gtk.Template.Callback("on_cancel_clicked")
    def __on_cancel_clicked(self, button: Gtk.Button) -> None:
        self.destroy()

    @Gtk.Template.Callback("on_create_clicked")
    def __on_create_clicked(self, button: Gtk.Button) -> None:
        if not valid_directory(self.data_path):
            self._notify("A valid project must be provided")
            return

        self.emit("done")
        self.close()

    @Gtk.Template.Callback("on_open_clicked")
    def __on_open_clicked(self, button: Gtk.Button) -> None:
        dialog = Gtk.FileDialog()
        dialog.select_folder(callback=self.__on_open_dialog_finish)

    def __on_open_dialog_finish(
        self,
        dialog: Gtk.FileDialog,
        result: Gio.AsyncResult,
    ) -> None:
        try:
            file = dialog.select_folder_finish(result)
        except Exception as e:
            logger.error(e)
        else:
            self.project.props.text = file.get_path()

    @property
    def data_path(self) -> None:
        return self.project.props.text

    @property
    def description(self) -> Description:
        return Description(
            id=1,
            game=Description(
                default=Description(
                    name="",
                    target="",
                    stamina=0,
                    durability=0,
                    weight=0,
                    strength=0,
                    spawns=0,
                    radius=0,
                    rate=0,
                    recovery=0,
                    density=0,
                    luminance=0,
                    removable=False,
                    equippable=False,
                    visible=True,
                    direction=Direction.SOUTH.name.lower(),
                    state=State.IDLING.name.lower(),
                    actuators=[],
                ),
            ),
            graphics=Description(
                default=None,
                states=[],
            ),
            sound=Description(
                states=[],
            ),
        )
