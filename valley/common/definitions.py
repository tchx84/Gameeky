from enum import IntEnum, StrEnum, auto

MAX_UDP_BYTES = 32 * 1024
MAX_TCP_BYTES = 32 * 1024

FPS = 60
TICK = 1000 / FPS

TILES_X = 15
TILES_Y = 11

DEFAULT_ADDRESS = "127.0.0.1"
DEFAULT_CLIENTS = 2
DEFAULT_SESSION_PORT = 7771
DEFAULT_MESSAGES_PORT = 7772
DEFAULT_SCENE_PORT = 7773
DEFAULT_SCENE = "scenes/default.json"


class Action(IntEnum):
    IDLE = auto()
    MOVE = auto()
    USE = auto()
    TAKE = auto()
    DROP = auto()
    INTERACT = auto()
    EXHAUST = auto()
    DESTROY = auto()


class Command(StrEnum):
    SESSION_PORT = auto()
    MESSAGES_PORT = auto()
    SCENE_PORT = auto()
    CLIENTS = auto()
    ADDRESS = auto()
    SCENE = auto()


class EntityType(IntEnum):
    EMPTY = 0


class Direction(IntEnum):
    EAST = auto()
    NORTH = auto()
    WEST = auto()
    SOUTH = auto()


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
