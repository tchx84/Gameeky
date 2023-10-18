from enum import Enum


class Density(float, Enum):
    VOID = 0.0
    SOLID = 1.0


class Recovery(float, Enum):
    MIN = 0.0
    MAX = 1.0


class Penalty(float, Enum):
    MIN = 0.0
    MAX = 5.0


class Delay(float, Enum):
    MIN = 0.0
    MAX = 1.0


class Cost(float, Enum):
    MIN = 1.0
    MAX = 2.5
