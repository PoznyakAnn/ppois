import pygame
from .physics import PhysicsObject
from .config import *

class Player(PhysicsObject):
    def __init__(self, x, y, color, team):
        super().__init__(x, y, PLAYER_RADIUS)
        self.color = color
        self.team = team
        self.selected = False
        self.force = 0
        self.max_force = 20
        self.load_image()

    def load_image(self):
        if self.team == "red":
            image = pygame.image.load("assets/red_chip.png").convert_alpha()
            self.image = pygame.transform.smoothscale(image, (self.radius * 2, self.radius * 2))
        elif self.team == "blue":
            image = pygame.image.load("assets/blue_chip.png").convert_alpha()
            self.image = pygame.transform.smoothscale(image, (self.radius * 2, self.radius * 2))
        else:
            self.image = None

    def draw(self, screen):
        if self.selected:
            glow_radius = self.radius + 2
            glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (255, 255, 100, 200), (glow_radius, glow_radius), glow_radius)
            screen.blit(glow_surface, (self.x - glow_radius, self.y - glow_radius))

        if self.image:
            screen.blit(self.image, (self.x - self.radius, self.y - self.radius))
        else:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def charge_kick(self):
        if self.force < self.max_force:
            self.force += 0.6

    def kick(self, tx, ty):
        dx = tx - self.x
        dy = ty - self.y
        dist = math.hypot(dx, dy)
        if dist > 0:
            power = self.force * FORCE_MULTIPLIER
            self.vx = dx / dist * power
            self.vy = dy / dist * power
        self.force = 0
