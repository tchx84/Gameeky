from enum import Enum, IntEnum


class Alpha(IntEnum):
    MIN = 0
    MAX = 1


class Normalized(float, Enum):
    MIN = 0.0
    MAX = 1.0
