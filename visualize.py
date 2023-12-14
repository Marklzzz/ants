import pygame
from config import *
import json
from config import target_colors

def start():
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
                if target['type'] == 0:
                    pygame.draw.circle(screen,
                                       queen_health_color,
                                       (int(target['pos'][0]), int(target['pos'][1])),
                                       int(target['size']*target['health']/QUEEN_START_HEALTH))

            for ant in d['ants']:
                if ant['current_target'] == 0:
                    screen.set_at((int(ant['pos'][0]),int(ant['pos'][1])),GRAY)
                else:
                    pygame.draw.circle(screen,target_colors[ant['current_target']],(int(ant['pos'][0]),int(ant['pos'][1])),ANT_SIZE)

            pygame.display.flip()

    pygame.quit()