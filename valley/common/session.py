from .serializeable import Serializeable


class Session(Serializeable):
    def __init__(self, id: int) -> None:
        self.id = id


class SessionRequest(Serializeable):
    def __init__(self) -> None:
        pass
