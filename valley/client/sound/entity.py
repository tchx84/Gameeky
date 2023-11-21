import gi

from typing import Dict, List, Optional, Any

gi.require_version("GSound", "1.0")

from gi.repository import GLib, Gio, GSound, GObject

from ...common.logger import logger
from ...common.definitions import State
from ...common.utils import get_time_milliseconds
from ...common.entity import Entity as CommonEntity
from ...common.scanner import Description
from ...common.utils import get_data_path, add_timeout_source, remove_source_id


class Sound(GObject.GObject):
    __gsignals__ = {
        "finished": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(self, path: str, delay: int, timeout: int) -> None:
        super().__init__()

        self._path = path
        self._cancellable = Gio.Cancellable()
        self._context = GSound.Context()
        self._context.init()

        self._delay = delay
        self._timeout = timeout
        self._timeout_source_id: Optional[int] = None
        self._timestamp = get_time_milliseconds()
        self._playing = False

    def __on_sound_finished(
        self,
        context: GSound.Context,
        result: Gio.AsyncResult,
        data: Optional[Any] = None,
    ) -> None:
        try:
            self._context.play_full_finish(result)
        except GLib.GError as e:
            if not e.matches(Gio.io_error_quark(), Gio.IOErrorEnum.CANCELLED):
                logger.error(e)

        self._stop_timeout()
        self._playing = False
        self.emit("finished")

    def __on_timeout(self, *args) -> int:
        self.stop()
        self._timeout_source_id = None
        return GLib.SOURCE_REMOVE

    def _stop_timeout(self) -> None:
        if self._timeout_source_id is not None:
            remove_source_id(self._timeout_source_id)

        self._timeout_source_id = None

    def _keep_alive(self) -> None:
        if self._timeout == 0:
            return

        self._stop_timeout()
        self._timeout_source_id = add_timeout_source(
            self._timeout * 1000,
            self.__on_timeout,
        )

    def play(self) -> None:
        self._keep_alive()

        if self._playing is True:
            return

        timestamp = get_time_milliseconds()
        seconds_since_play = (timestamp - self._timestamp) / 1000

        if seconds_since_play <= self._delay:
            return

        self._playing = True
        self._cancellable.reset()
        self._timestamp = timestamp
        self._context.play_full(
            {GSound.ATTR_MEDIA_FILENAME: self._path},
            self._cancellable,
            self.__on_sound_finished,
        )

    def stop(self) -> None:
        self._cancellable.cancel()


class SoundSequence:
    def __init__(self) -> None:
        self._index = 0
        self._sounds: List[Sound] = []

    def __on_sound_finished(self, sound: Sound) -> None:
        self._index += 1

    def add(self, sound: Sound) -> None:
        self._sounds.append(sound)
        sound.connect("finished", self.__on_sound_finished)

    def play(self) -> None:
        if self.sound is None:
            return

        self.sound.play()

    def stop(self) -> None:
        if self.sound is None:
            return

        self.sound.stop()
        self._index = 0

    @property
    def sound(self) -> Optional[Sound]:
        if len(self._sounds) == 0:
            return None

        return self._sounds[self._index % len(self._sounds)]

    @classmethod
    def new_from_description(cls, description: Description) -> "SoundSequence":
        sequence = cls()

        for path in description.paths:
            sound = Sound(
                get_data_path(path),
                description.delay,
                description.timeout,
            )
            sequence.add(sound)

        return sequence


class Entity:
    def __init__(self, type_id: int) -> None:
        self.type_id = type_id
        self._sequences: Dict[State, SoundSequence] = {}

    def add(self, state: State, sound: Sound) -> None:
        if state not in self._sequences:
            self._sequences[state] = SoundSequence()

        self._sequences[state].add(sound)

    def play(self, entity: CommonEntity) -> None:
        if entity.state not in self._sequences:
            return

        sequence = self._sequences[entity.state]
        sequence.play()


class EntityRegistry:
    __entities__: Dict[int, Entity] = {}

    @classmethod
    def reset(cls) -> None:
        cls.__entities__ = {}

    @classmethod
    def register(cls, description: Description) -> None:
        entity = Entity(description.id)

        for state in description.sound.states:
            for path in state.sequence.paths:
                sound = Sound(
                    get_data_path(path),
                    state.sequence.delay,
                    state.sequence.timeout,
                )
                entity.add(State[state.name.upper()], sound)

        cls.__entities__[entity.type_id] = entity

    @classmethod
    def play(cls, entity: CommonEntity) -> None:
        cls.__entities__[entity.type_id].play(entity)
