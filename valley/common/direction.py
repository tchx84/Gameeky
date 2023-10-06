from enum import Enum


class Direction(float, Enum):
    RIGHT = 0
    UP = 90
    LEFT = 180
    DOWN = 270
