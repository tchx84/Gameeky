from ...common.direction import Direction
from ...common.entity import Entity as CommonEntity


class Entity(CommonEntity):
    def move(self):
        if self.angle == Direction.RIGHT:
            self.position.x += self.velocity
        elif self.angle == Direction.UP:
            self.position.y -= self.velocity
        elif self.angle == Direction.LEFT:
            self.position.x -= self.velocity
        elif self.angle == Direction.DOWN:
            self.position.y += self.velocity
