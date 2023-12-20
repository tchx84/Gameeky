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

from typing import Any

from gi.repository import GLib

from .logger import logger


def measure(func, *args, **kargs) -> Any:
    before = GLib.get_monotonic_time()
    result = func(*args, **kargs)
    after = GLib.get_monotonic_time()

    logger.debug("Measured %s for %d ms", func.__name__, (after - before) / 1000)

    return result
