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
import gi
import locale

gi.require_version("WebKit", "6.0")

from typing import Optional

from gi.repository import Adw, Gio, GObject, Gtk, WebKit
from gi.repository.WebKit import WebView

from ..config import pkgdatadir
from ..logger import logger


@Gtk.Template(resource_path="/dev/tchx84/gameeky/common/widgets/documentation_window.ui")  # fmt: skip
class DocumentationWindow(Adw.Window):
    __gtype_name__ = "DocumentationWindow"

    __default__ = "en"
    __languages__ = {
        "en_": "en",
        "es_": "es",
    }

    webview = Gtk.Template.Child()
    back_button = Gtk.Template.Child()
    forward_button = Gtk.Template.Child()

    def __init__(self, *args, **kargs) -> None:
        super().__init__(*args, **kargs)

        code, encoding = locale.getlocale()
        language = self._find_language(code)
        uri = os.path.join(pkgdatadir, "docs", "basics", language, "index.html")

        self.webview.load_uri(f"file://{uri}")
        self.webview.connect_after("load-changed", self.__on_load_clicked)
        self.webview.connect("notify::uri", self.__on_load_uri)

    def _find_language(self, code: Optional[str]) -> str:
        if code is None:
            return self.__default__

        for option, language in self.__languages__.items():
            if code.startswith(option):
                return language

        return self.__default__

    def __on_load_uri(self, webview: WebView, param: GObject.ParamSpec) -> None:
        self.webview.load_uri(self.webview.props.uri)

    def __on_load_clicked(self, webview: WebView, event: WebKit.LoadEvent) -> None:
        self.back_button.props.sensitive = self.webview.can_go_back()
        self.forward_button.props.sensitive = self.webview.can_go_forward()

    @Gtk.Template.Callback("on_back_clicked")
    def __on_back_clicked(self, button: Gtk.Button) -> None:
        self.webview.go_back()

    @Gtk.Template.Callback("on_forward_clicked")
    def __on_forward_clicked(self, button: Gtk.Button) -> None:
        self.webview.go_forward()

    @Gtk.Template.Callback("on_decide_policy")
    def __on_decide_policy(
        self,
        webview: WebView,
        decision: WebKit.NavigationPolicyDecision,
        decision_type: WebKit.PolicyDecisionType,
    ) -> bool:
        if decision_type != WebKit.PolicyDecisionType.NAVIGATION_ACTION:
            return False

        action = decision.get_navigation_action()
        uri = action.get_request().get_uri()

        if uri.startswith("file"):
            return False

        launcher = Gtk.UriLauncher()
        launcher.props.uri = uri
        launcher.launch(self, None, self.__on_open_callback)

        decision.ignore()
        return True

    def __on_open_callback(self, launcher: Gtk.UriLauncher, res: Gio.Task) -> None:
        try:
            launcher.launch_finish(res)
        except Exception as e:
            logger.error(e)
