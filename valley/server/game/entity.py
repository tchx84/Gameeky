import math

from ...common.entity import Entity as CommonEntity


class Entity(CommonEntity):
    def move(self):
        radian = math.radians(self.angle)
        self.position.x += math.cos(radian) * self.velocity
        self.position.y += math.sin(radian) * self.velocity
