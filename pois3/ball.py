import pygame
from .physics import PhysicsObject
from .config import *

class Ball(PhysicsObject):
    def __init__(self, x, y):
        super().__init__(x, y, BALL_RADIUS)
        self.image = pygame.image.load("assets/ball.png")
        self.image = pygame.transform.scale(self.image, (BALL_RADIUS * 2, BALL_RADIUS * 2))

    def draw(self, screen):
        screen.blit(self.image, (self.x - BALL_RADIUS, self.y - BALL_RADIUS))
