from enum import IntEnum, auto


class State(IntEnum):
    IDLING = auto()
    MOVING = auto()
    USING = auto()
    DESTROYING = auto()
    DESTROYED = auto()
