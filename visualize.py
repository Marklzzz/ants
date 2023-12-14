import pygame
from config import *
import json

target_colors = [GREEN, BLUE, RED, YELLOW, MAGENTA]

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

with open('file.txt', 'r') as f:
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False

        # update
        line = f.readline()
        if line:
            d = json.loads(line)
        # Render
        screen.fill(BLACK)
        for target in d['targets']:
            pygame.draw.circle(screen,
                               target_colors[target['type']],
                               (int(target['pos'][0]), int(target['pos'][1])),
                               target['size'])
        for ant in d['ants']:
            screen.set_at((ant[0], ant[1]), WHITE)

        pygame.display.flip()

pygame.quit()