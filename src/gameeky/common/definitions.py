# Copyright (c) 2023 Martín Abente Lahaye.
#
# This file is part of Gameeky
# (see gameeky.tchx84.dev).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from enum import IntEnum, StrEnum, auto

MAX_UDP_BYTES = 32 * 1024
MAX_TCP_BYTES = 32 * 1024

FPS = 30
TICK = 1000 / FPS

TILES_X = 15
TILES_Y = 11

DEFAULT_ADDRESS = "127.0.0.1"
DEFAULT_CLIENTS = 1
DEFAULT_SESSION_PORT = 7771
DEFAULT_MESSAGES_PORT = 7772
DEFAULT_TIMEOUT = 1
DEFAULT_SEPARATOR = "\n"


class Format(StrEnum):
    ENTITY = "entity"
    SCENE = "scene"


DEFAULT_SCENE = f"scenes/default.{Format.SCENE}"


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
    PROJECT_PATH = auto()
    SESSION_PORT = auto()
    MESSAGES_PORT = auto()
    CLIENTS = auto()
    ADDRESS = auto()
    SCENE = auto()


class EntityType(IntEnum):
    EMPTY = 0
    PLAYER = 1


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


class DayTime(IntEnum):
    DAY = auto()
    NIGHT = auto()
    DYNAMIC = auto()


DEFAULT_DURATION = 3600
