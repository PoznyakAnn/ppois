import pygame
from .config import *
from .player import Player
from .ball import Ball
from .menu import Menu
from .results import ResultsScreen
import random
import datetime

class Game:
    def __init__(self):
        self.players = []
        self.ball = Ball(WIDTH // 2, HEIGHT // 2)
        self.current_team = "red"
        self.selected_idx = 0
        self.scores = {"red": 0, "blue": 0}
        self.game_over = False
        self.font = pygame.font.SysFont("Arial", 36)
        self.waiting = False
        self.init_players()
        self.select_player()

    def init_players(self):
        red_pos = [(WIDTH // 4, HEIGHT // 3), (WIDTH // 4, HEIGHT // 2), (WIDTH // 4, 2 * HEIGHT // 3)]
        blue_pos = [(3 * WIDTH // 4, HEIGHT // 3), (3 * WIDTH // 4, HEIGHT // 2), (3 * WIDTH // 4, 2 * HEIGHT // 3)]
        for x, y in red_pos:
            self.players.append(Player(x, y, RED, "red"))
        for x, y in blue_pos:
            self.players.append(Player(x, y, BLUE, "blue"))

    def select_player(self):
        options = [i for i, p in enumerate(self.players) if p.team == self.current_team]
        if options:
            self.selected_idx = random.choice(options)
            for i, p in enumerate(self.players):
                p.selected = (i == self.selected_idx)

    def update(self):
        for obj in self.players + [self.ball]:
            obj.update_position()

        for i in range(len(self.players)):
            for j in range(i + 1, len(self.players)):
                if self.players[i].check_collision(self.players[j]):
                    self.players[i
