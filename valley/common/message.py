from typing import Tuple

from .action import Action
from .serializeable import Serializeable


class Message(Serializeable):
    Signature = Tuple[int, int, float, int]

    def __init__(
        self,
        session_id: int,
        action: Action = Action.NOTHING,
        value: float = 0,
        sequence: int = 0,
    ) -> None:
        self.session_id = session_id
        self.action = action
        self.value = value
        self.sequence = sequence

    def to_values(self) -> Signature:
        return (self.session_id, self.action, self.value, self.sequence)

    @classmethod
    def from_values(cls, values: Signature) -> "Message":
        session_id, action, value, sequence = values
        return cls(session_id, Action(action), value, sequence)
