from enum import IntEnum, auto


class State(IntEnum):
    IDLING = auto()
    MOVING = auto()
    USING = auto()
    HELD = auto()
    DESTROYING = auto()
    DESTROYED = auto()
