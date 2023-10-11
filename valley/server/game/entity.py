from ...common.direction import Direction
from ...common.entity import Entity as CommonEntity


class Entity(CommonEntity):
    def __init__(self, velocity: float = 0.05, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self.velocity = velocity

    def move(self) -> None:
        if self.direction == Direction.RIGHT:
            self.position.x += self.velocity
        elif self.direction == Direction.UP:
            self.position.y -= self.velocity
        elif self.direction == Direction.LEFT:
            self.position.x -= self.velocity
        elif self.direction == Direction.DOWN:
            self.position.y += self.velocity
