
import random
import string
import hashlib
import test
import pygame

pygame.init()
window = pygame.display.set_mode((500, 200))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

ants_n = test.TextInputBox(50, 50, 400, font, 'ants_n')
ant_size = test.TextInputBox(50,80,400,font, 'ant_size')
n_targets = test.TextInputBox(50,110,400,font,'n_targets')
group = pygame.sprite.Group(ants_n)
group.add(ant_size)
group.add(n_targets)

Result = {}


run = True
while run:
    clock.tick(60)
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                for box in group:
                    Result[box.inactive_text]=box.text
                print(Result)
    group.update(event_list, Result)

    window.fill(0)
    group.draw(window)
    pygame.display.flip()


pygame.quit()
exit()