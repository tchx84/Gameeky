from .serializeable import Serializeable


class Heartbeat(Serializeable):
    def __init__(self, session_id: int) -> None:
        self.session_id = session_id
