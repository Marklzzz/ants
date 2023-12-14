import pygame
from controller import Env
from config import *

target_colors = [GREEN, BLUE, RED, YELLOW]

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

env = Env(1 / FPS)

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update
    env.step()
    # Render
    screen.fill(BLACK)
    for i, target in enumerate(env.targets):
        pygame.draw.circle(screen,
                           target_colors[target.target_type],
                           (int(target.pos[0]), int(target.pos[1])),
                           target.size)
    for ant in env.ants:
        pygame.draw.circle(screen, WHITE, (int(ant.pos[0]), int(ant.pos[1])), ANT_SIZE)

    pygame.display.flip()

pygame.quit()