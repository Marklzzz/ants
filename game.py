import pygame

import config
from controller import Env


def start():
    config.update()
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption("My Game")
    clock = pygame.time.Clock()

    env = Env(1 / config.FPS)

    running = True
    while running:
        clock.tick(config.FPS)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False

        # Update
        env.step()
        # Render
        screen.fill(config.BLACK)
        for i, target in enumerate(env.targets):
            pygame.draw.circle(screen,
                               config.target_colors[target.target_type],
                               (int(target.pos[0]), int(target.pos[1])),
                               target.size)
        for ant in env.ants:
            screen.set_at((int(ant.pos[0]), int(ant.pos[1])), config.target_colors[ant.current_target])

        pygame.display.flip()

    pygame.quit()

