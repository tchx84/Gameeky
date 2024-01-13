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

from typing import Tuple, Optional

from .serializeable import Serializeable
from .session import Session, SessionRequest
from .scene import Scene, SceneRequest
from .stats import Stats, StatsRequest
from .message import Message
from .dialogue import Dialogue


class Payload(Serializeable):
    Signature = Tuple[
        Optional[Session.Signature],
        Optional[SessionRequest.Signature],
        Optional[Scene.Signature],
        Optional[SceneRequest.Signature],
        Optional[Stats.Signature],
        Optional[StatsRequest.Signature],
        Optional[Message.Signature],
        Optional[Dialogue.Signature],
    ]

    def __init__(
        self,
        session: Optional[Session] = None,
        session_request: Optional[SessionRequest] = None,
        scene: Optional[Scene] = None,
        scene_request: Optional[SceneRequest] = None,
        stats: Optional[Stats] = None,
        stats_request: Optional[StatsRequest] = None,
        message: Optional[Message] = None,
        dialogue: Optional[Dialogue] = None,
    ) -> None:
        self.session = session
        self.session_request = session_request
        self.scene = scene
        self.scene_request = scene_request
        self.stats = stats
        self.stats_request = stats_request
        self.message = message
        self.dialogue = dialogue

    def to_values(self) -> Signature:
        return (
            self.session.to_values() if self.session else None,
            self.session_request.to_values() if self.session_request else None,
            self.scene.to_values() if self.scene else None,
            self.scene_request.to_values() if self.scene_request else None,
            self.stats.to_values() if self.stats else None,
            self.stats_request.to_values() if self.stats_request else None,
            self.message.to_values() if self.message else None,
            self.dialogue.to_values() if self.dialogue else None,
        )

    @classmethod
    def from_values(cls, values: Signature) -> "Payload":
        (
            session,
            session_request,
            scene,
            scene_request,
            stats,
            stats_request,
            message,
            dialogue,
        ) = values

        return cls(
            Session.from_values(session) if session else None,
            SessionRequest.from_values(session_request) if session_request else None,
            Scene.from_values(scene) if scene else None,
            SceneRequest.from_values(scene_request) if scene_request else None,
            Stats.from_values(stats) if stats else None,
            StatsRequest.from_values(stats_request) if stats_request else None,
            Message.from_values(message) if message else None,
            Dialogue.from_values(dialogue) if dialogue else None,
        )
