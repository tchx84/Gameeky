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

from gi.repository import Gio, GLib

from ...common.logger import logger


class Software:
    __service__ = "org.gnome.Software"

    @classmethod
    def launch(cls) -> None:
        proxy = Gio.DBusProxy.new_for_bus_sync(
            Gio.BusType.SESSION,
            Gio.DBusProxyFlags.NONE,
            None,
            cls.__service__,
            "/org/gnome/Software",
            "org.freedesktop.Application",
            None,
        )

        params = GLib.Variant("(ss)", ["dev.tchx84.Gameeky", ""])

        try:
            proxy.ActivateAction("(sava{sv})", "details", [params], None)
        except Exception as e:
            logger.error(e)

    @classmethod
    def available(cls) -> bool:
        try:
            proxy = Gio.DBusProxy.new_for_bus_sync(
                Gio.BusType.SESSION,
                Gio.DBusProxyFlags.NONE,
                None,
                "org.freedesktop.DBus",
                "/org/freedesktop/DBus",
                "org.freedesktop.DBus",
                None,
            )

            return cls.__service__ in proxy.ListActivatableNames()
        except Exception as e:
            logger.error(e)

        return False
