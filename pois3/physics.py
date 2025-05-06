import math
from .config import *

class PhysicsObject:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = 0
        self.vy = 0

    def update_position(self):
        self.x += self.vx
        self.y += self.vy
        speed = math.hypot(self.vx, self.vy)
        if speed < 0.1:
            self.vx = self.vy = 0
        else:
            self.vx *= FRICTION
            self.vy *= FRICTION

        # Столкновения со стенами
        if self.x - self.radius <= LEFT_BOUND:
            self.x = LEFT_BOUND + self.radius
            self.vx *= -ELASTICITY
        elif self.x + self.radius >= RIGHT_BOUND:
            self.x = RIGHT_BOUND - self.radius
            self.vx *= -ELASTICITY

        if self.y - self.radius <= TOP_BOUND:
            self.y = TOP_BOUND + self.radius
            self.vy *= -ELASTICITY
        elif self.y + self.radius >= BOTTOM_BOUND:
            self.y = BOTTOM_BOUND - self.radius
            self.vy *= -ELASTICITY

    def check_collision(self, other):
        dx, dy = other.x - self.x, other.y - self.y
        return math.hypot(dx, dy) < self.radius + other.radius

    def resolve_collision(self, other):
        # логика столкновений
        ...
