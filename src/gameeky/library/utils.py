# Copyright (c) 2024 Martín Abente Lahaye.
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

import os

from ..common.utils import get_project_path
from ..common.definitions import EntityType, DEFAULT_ADDRESS, DEFAULT_SESSION_PORT


def get_session_project() -> str:
    return os.environ.get("SESSION_PROJECT", get_project_path())


def set_session_project(session_project: str) -> None:
    os.environ["SESSION_PROJECT"] = session_project


def get_session_entity_type() -> int:
    return int(os.environ.get("SESSION_ENTITY_TYPE", EntityType.PLAYER))


def set_session_entity_type(entity_type: int) -> None:
    os.environ["SESSION_ENTITY_TYPE"] = str(entity_type)


def get_session_address() -> str:
    return os.environ.get("SESSION_ADDRESS", DEFAULT_ADDRESS)


def set_session_address(address: str) -> None:
    os.environ["SESSION_ADDRESS"] = address


def get_session_port() -> int:
    return int(os.environ.get("SESSION_PORT", DEFAULT_SESSION_PORT))


def set_session_port(port: int) -> None:
    os.environ["SESSION_PORT"] = str(port)
