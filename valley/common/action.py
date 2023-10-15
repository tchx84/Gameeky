from enum import IntEnum, auto


class Action(IntEnum):
    IDLE = auto()
    MOVE = auto()
    USE = auto()
    DESTROY = auto()
