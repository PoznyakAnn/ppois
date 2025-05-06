import pygame
from .config import *

class Menu:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 48)
        self.options = ["Играть", "Выход"]
        self.selected = -1
        self.background = pygame.image.load("assets/menu_background.jpg").convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        for i, option in enumerate(self.options):
            color = YELLOW if i == self.selected else WHITE
            text = self.font.render(option, True, color)
            x = WIDTH // 2 - text.get_width() // 2
            y = HEIGHT // 2 - 100 + i * 60
            screen.blit(text, (x, y))

    def update_hover(self, mouse_pos):
        self.selected = -1
        for i in range(len(self.options)):
            text = self.font.render(self.options[i], True, WHITE)
            x = WIDTH // 2 - text.get_width() // 2
            y = HEIGHT // 2 - 100 + i * 60
            if x <= mouse_pos[0] <= x + text.get_width() and y <= mouse_pos[1] <= y + text.get_height():
                self.selected = i
                break

    def handle_click(self):
        return self.selected
