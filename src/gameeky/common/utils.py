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

import os
import json

from typing import Callable, Optional, Tuple
from gettext import gettext as _
from gi.repository import GLib, Gio

from .config import PYTHON, bindir


def get_time_milliseconds() -> int:
    return int(GLib.get_monotonic_time() / 1000)


def get_packs_path() -> str:
    return os.environ.get(
        "PACKS_PATH",
        os.path.join(os.path.sep, "app", "extensions"),
    )


def set_projects_path(path) -> None:
    os.environ["PROJECTS_PATH"] = path


def get_projects_path() -> str:
    return os.environ.get(
        "PROJECTS_PATH",
        os.path.join(os.path.expanduser("~"), "Gameeky"),
    )


def set_project_path(path) -> None:
    os.environ["PROJECT_PATH"] = path


def get_project_path(*paths) -> str:
    return os.path.join(os.environ.get("PROJECT_PATH", get_projects_path()), *paths)


def find_project_path(path) -> str:
    return os.environ.get("PROJECT_PATH", os.path.dirname(os.path.dirname(path)))


def get_project_folder(*paths):
    return Gio.File.new_for_path(os.path.join(get_project_path(""), *paths))


def get_project_name() -> str:
    with open(get_project_path("gameeky.project")) as file:
        return json.load(file)["name"]


def get_relative_path(path: str) -> str:
    if not os.path.isabs(path):
        return path

    return os.path.relpath(path, os.environ.get("PROJECT_PATH", ""))


def bytearray_to_string(array: bytes) -> str:
    return bytearray(array).replace(b"\x00", b"").decode("utf-8")


def valid_file(path) -> bool:
    if GLib.file_test(path, GLib.FileTest.EXISTS) is False:
        return False
    if GLib.file_test(path, GLib.FileTest.IS_REGULAR) is False:
        return False

    return True


def valid_directory(path) -> bool:
    if GLib.file_test(path, GLib.FileTest.EXISTS) is False:
        return False
    if GLib.file_test(path, GLib.FileTest.IS_DIR) is False:
        return False

    return True


def valid_project(path) -> bool:
    if valid_file(os.path.join(path, "gameeky.project")) is False:
        return False
    if valid_directory(os.path.join(path, "entities")) is False:
        return False
    if valid_directory(os.path.join(path, "scenes")) is False:
        return False
    if valid_directory(os.path.join(path, "assets")) is False:
        return False
    if valid_directory(os.path.join(path, "actuators")) is False:
        return False

    return True


def find_context() -> GLib.MainContext:
    if (context := GLib.MainContext.get_thread_default()) is None:
        context = GLib.MainContext.default()

    return context


def add_timeout_source(
    interval: float,
    callback: Callable,
    data: Optional[Tuple] = None,
) -> int:
    context = find_context()
    data = () if data is None else data

    def timeout_callback(*args) -> int:
        return callback(*data)

    source = GLib.timeout_source_new(interval)
    source.set_priority(GLib.PRIORITY_DEFAULT)
    source.set_callback(timeout_callback)
    source.attach(context)

    return source.get_id()


def add_idle_source(
    callback: Callable,
    data: Optional[Tuple] = None,
    context: Optional[GLib.MainContext] = None,
) -> int:
    context = find_context() if context is None else context
    data = () if data is None else data

    def idle_callback(*args) -> int:
        callback(*data)
        return GLib.SOURCE_REMOVE

    source = GLib.idle_source_new()
    source.set_callback(idle_callback)
    source.attach(context)

    return source.get_id()


def remove_source_id(source_id: int) -> None:
    context = find_context()
    context.find_source_by_id(source_id).destroy()


def wait(milliseconds: int) -> None:
    if not milliseconds:
        return

    called = False
    context = GLib.MainContext.default()

    def callback() -> int:
        nonlocal called
        called = True
        return GLib.SOURCE_REMOVE

    GLib.timeout_add(milliseconds, callback)

    while not called:
        while context.pending():
            context.iteration(True)


def launch(command: str, arguments: str) -> None:
    GLib.spawn_command_line_async(
        f"{quote(PYTHON)} {quote(os.path.join(bindir, command))} {arguments.strip()}"
    )


def launch_path(path: str) -> None:
    Gio.AppInfo.launch_default_for_uri(GLib.filename_to_uri(path), None)


def launch_player(project_path: str, scene_path: str) -> None:
    launch(
        "dev.tchx84.Gameeky.Player",
        f"--project_path={quote(project_path)} {quote(scene_path)}",
    )


def launch_scene(project_path: str, scene_path: str) -> None:
    launch(
        "dev.tchx84.Gameeky.Scene",
        f"--project_path={quote(project_path)} {quote(scene_path)}",
    )


def launch_entity(project_path: str, entity_path: str) -> None:
    launch(
        "dev.tchx84.Gameeky.Entity",
        f"--project_path={quote(project_path)} {quote(entity_path)}",
    )


def launch_coder(project_path: str) -> None:
    launch(
        "dev.tchx84.Gameeky.Coder",
        f"--project_path={quote(project_path)}",
    )


def quote(string: str) -> str:
    if not string:
        return string
    else:
        return GLib.shell_quote(string)


def find_new_name(directory: str, name: str) -> str:
    while os.path.lexists(os.path.join(directory, name)):
        name = _("%s (copy)") % name

    return name


def clamp(maximum, minimum, value):
    return min(max(minimum, value), maximum)


def division(dividend, divisor):
    return dividend / divisor if divisor > 0 else 0


def element(array, index):
    return array[index] if len(array) > 0 else None


def oscillate(maximum, minimum, value):
    range = maximum - minimum
    return minimum + abs(((value + range) % (range * 2)) - range)
