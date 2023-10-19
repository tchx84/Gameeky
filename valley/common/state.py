from enum import IntEnum, auto


class State(IntEnum):
    IDLING = auto()
    MOVING = auto()
    USING = auto()
    TAKING = auto()
    DROPPING = auto()
    HELD = auto()
    EXHAUSTED = auto()
    INTERACTING = auto()
    DESTROYING = auto()
    DESTROYED = auto()
