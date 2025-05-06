import pygame
import math
from .physics import PhysicsObject
from .config import *

class Player(PhysicsObject):
    def __init__(self, x, y, color, team):
        super().__init__(x, y, PLAYER_RADIUS)
        self.color = color
        self.team = team
        self.image = None
        self.load_image()
        self.kick_charge = 0

    def load_image(self):
        self.image = pygame.Surface((PLAYER_RADIUS*2, PLAYER_RADIUS*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (PLAYER_RADIUS, PLAYER_RADIUS), PLAYER_RADIUS)

    def draw(self, screen):
        rect = self.image.get_rect(center=(self.x, self.y))
        screen.blit(self.image, rect)

    def charge_kick(self):
        self.kick_charge = min(self.kick_charge + 1, 20)

    def kick(self, tx, ty):
        dx = tx - self.x
        dy = ty - self.y
        dist = math.hypot(dx, dy)
        if dist == 0:
            return
        nx, ny = dx / dist, dy / dist
        self.vx += nx * self.kick_charge
        self.vy += ny * self.kick_charge
        self.kick_charge = 0

class Ball(PhysicsObject):
    def __init__(self, x, y):
        super().__init__(x, y, BALL_RADIUS)
        self.color = (255, 255, 255)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
