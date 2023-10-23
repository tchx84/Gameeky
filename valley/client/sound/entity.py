import gi

from typing import Dict, List, Optional, Any

gi.require_version("GSound", "1.0")

from gi.repository import GLib, Gio, GSound, GObject

from ...common.state import State
from ...common.entity import Entity as CommonEntity
from ...common.scanner import Description
from ...common.utils import get_data_path


class Sound(GObject.GObject):
    __gsignals__ = {
        "finished": (GObject.SignalFlags.RUN_LAST, None, ()),
    }

    def __init__(self, path: str) -> None:
        super().__init__()

        self._path = path
        self._cancellable = Gio.Cancellable()
        self._context = GSound.Context()
        self._context.init()

        self.playing = False

    def __on_sound_finished(
        self,
        context: GSound.Context,
        result: Gio.AsyncResult,
        data: Optional[Any] = None,
    ) -> None:
        self._context.play_full_finish(result)
        self.emit("finished")
        self.playing = False

    def play(self) -> None:
        if self.playing is True:
            return

        self.playing = True
        self._context.play_full(
            {GSound.ATTR_MEDIA_FILENAME: self._path},
            self._cancellable,
            self.__on_sound_finished,
        )

    def stop(self) -> None:
        self._cancellable.cancel()
        self.emit("finished")
        self.playing = False


class SoundSequence:
    def __init__(self) -> None:
        self._index = 0
        self._sounds: List[Sound] = []

    def __on_sound_finished(self, sound) -> int:
        self._index = (self._index + 1) % len(self._sounds)
        return GLib.SOURCE_REMOVE

    def add(self, sound: Sound) -> None:
        self._sounds.append(sound)

    def play(self) -> None:
        sound = self._sounds[self._index]
        sound.connect("finished", self.__on_sound_finished)
        sound.play()

    def stop(self) -> None:
        sound = self._sounds[self._index]
        sound.stop()


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
    def register(cls, description: Description) -> None:
        entity = Entity(description.id)

        for state in description.sound.states:
            for path in state.data.paths:
                sound = Sound(get_data_path(path))
                entity.add(State[state.name.upper()], sound)

        cls.__entities__[entity.type_id] = entity

    @classmethod
    def play(cls, entity: CommonEntity) -> None:
        cls.__entities__[entity.type_id].play(entity)
