from .action import Action
from .serializeable import Serializeable


class Message(Serializeable):
    def __init__(
        self,
        session_id: int,
        action: Action = Action.NOTHING,
        sequence: int = 0,
    ) -> None:
        self.session_id = session_id
        self.action = action
        self.sequence = sequence
