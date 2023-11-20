from typing import Optional
from gi.repository import GObject, GLib, Gtk

from ...client.game.service import Service
from ...client.game.scene import Scene as SceneModel
from ...client.game.stats import Stats as StatsModel
from ...client.input.keyboard import Keyboard
from ...client.graphics.entity import EntityRegistry as EntityGraphicsRegistry
from ...client.sound.entity import EntityRegistry as EntitySoundRegistry
from ...client.sound.scene import Scene as SceneSound

from ...common.logger import logger
from ...common.utils import get_data_path, set_data_path
from ...common.scanner import Scanner, Description
from ...common.definitions import TILES_X, TILES_Y


class SessionGuest(GObject.GObject):
    __gsignals__ = {
        "initializing": (GObject.SignalFlags.RUN_LAST, None, ()),
        "started": (GObject.SignalFlags.RUN_LAST, None, ()),
        "failed": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(
        self,
        data_path: str,
        address: str,
        session_port: int,
        messages_port: int,
        scene_port: int,
        stats_port: int,
        widget: Gtk.Widget,
    ) -> None:
        super().__init__()

        self._data_path = data_path
        self._address = address
        self._session_port = session_port
        self._messages_port = messages_port
        self._scene_port = scene_port
        self._stats_port = stats_port

        self._widget = widget

        self._service: Optional[Service] = None
        self._scene_model: Optional[SceneModel] = None
        self._stats_model: Optional[StatsModel] = None
        self._input: Optional[Keyboard] = None
        self._sound: Optional[SceneSound] = None

    def _setup(self) -> None:
        self._service = Service(
            address=self._address,
            session_port=self._session_port,
            messages_port=self._messages_port,
            scene_port=self._scene_port,
            stats_port=self._stats_port,
            context=GLib.MainContext.default(),
        )

        self._scene_model = SceneModel(
            width=TILES_X,
            height=TILES_Y,
            service=self._service,
        )

        self._stats_model = StatsModel(
            service=self._service,
        )

        self._keyboard = Keyboard(
            widget=self._widget,
            service=self._service,
        )

        self._sound = SceneSound()
        self._sound.model = self._scene_model

        self._service.register()

    def _scan(self) -> None:
        EntityGraphicsRegistry.reset()
        EntitySoundRegistry.reset()

        self._scanner = Scanner(path=get_data_path("entities"))
        self._scanner.connect("found", self.__on_scanner_found)
        self._scanner.connect("done", self.__on_scanner_done)
        self._scanner.scan()

    def __on_scanner_found(self, scanner: Scanner, description: Description) -> None:
        EntityGraphicsRegistry.register(description)
        EntitySoundRegistry.register(description)

    def __on_scanner_done(self, scanner: Scanner) -> None:
        try:
            self._setup()
        except Exception as e:
            logger.error(e)
            self.emit("failed")
        else:
            self.emit("started")

    def create(self) -> None:
        set_data_path(self._data_path)

        try:
            self._scan()
        except Exception as e:
            logger.error(e)
            self.emit("failed")
        else:
            self.emit("initializing")

    def shutdown(self) -> None:
        if self._service is not None:
            self._service.unregister()
        if self._scene_model is not None:
            self._scene_model.shutdown()
        if self._stats_model is not None:
            self._stats_model.shutdown()
        if self._input is not None:
            self._input.shutdown()
        if self._sound is not None:
            self._sound.shutdown()

    @property
    def scene(self) -> Optional[SceneModel]:
        return self._scene_model

    @property
    def stats(self) -> Optional[StatsModel]:
        return self._stats_model
