import pygame
from game.config import *
from game.objects import Player, Ball

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

player = Player(100, 100, (0, 0, 255), "blue")
ball = Ball(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

running = True
while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: player.vx -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]: player.vx += PLAYER_SPEED
    if keys[pygame.K_UP]: player.vy -= PLAYER_SPEED
    if keys[pygame.K_DOWN]: player.vy += PLAYER_SPEED

    if player.check_collision(ball):
        ball.vx += player.vx * 0.8
        ball.vy += player.vy * 0.8

    player.update()
    ball.update()

    player.draw(screen)
    ball.draw(screen)

    pygame.display.flip()
    clock.tick(60)

