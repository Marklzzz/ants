import TextInputBox
import pygame
import time
import game
import simulate
import visualize

window = ''

with open('borders.txt') as f:
    arr = [list(map(int, i.split(' = ')[1].split(', '))) for i in f.readlines()]
    MIN_N_ANTS, MAX_N_ANTS = arr[0][0], arr[0][1]
    MIN_N_TARGET_TYPES, MAX_N_TARGET_TYPES = arr[1][0], arr[1][1]
    MIN_N_TARGETS, MAX_N_TARGETS = arr[2][0], arr[2][1]
    MIN_TARGET_HEALTH, MAX_TARGET_HEALTH = arr[3][0], arr[3][1]
    MIN_MARGIN_TO_QUEEN, MAX_MARGIN_TO_QUEEN = arr[4][0], arr[4][1]
    MIN_QUEEN_START_HEALTH, MAX_QUEEN_START_HEALTH = arr[5][0], arr[5][1]


def Input_window():
    global window
    pygame.init()
    window = pygame.display.set_mode((700, 500))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)

    ants_n = TextInputBox.TextInputBox(50, 60, 600, font, f'ants_n (from {MIN_N_ANTS} to {MAX_N_ANTS})')
    n_targets = TextInputBox.TextInputBox(50, 110, 600, font,
                                          f'n_target_types (from {MIN_N_TARGET_TYPES} to {MAX_N_TARGET_TYPES})')
    n_target_types = TextInputBox.TextInputBox(50, 160, 600, font,
                                               f'n_targets (from {MIN_N_TARGETS} to {MAX_N_TARGETS})')

    target_health = TextInputBox.TextInputBox(50, 210, 600, font,
                                              f'target_health (from {MIN_TARGET_HEALTH} to {MAX_TARGET_HEALTH})')
    margin_to_queen = TextInputBox.TextInputBox(50, 260, 600, font,
                                                f'margin_to_queen (from {MIN_MARGIN_TO_QUEEN} to {MAX_MARGIN_TO_QUEEN})')
    queen_start_health = TextInputBox.TextInputBox(50, 310, 600, font,
                                                   f'queen_start_health (from {MIN_QUEEN_START_HEALTH} to {MAX_QUEEN_START_HEALTH})')
    simulate_or_main_or_visualise = TextInputBox.TextInputBox(50, 360, 600, font,
                                                              'simulate, main or visualise (1, 2 or 3)')

    group = pygame.sprite.Group(ants_n)
    group.add(n_target_types)
    group.add(n_targets)
    group.add(target_health)
    group.add(margin_to_queen)
    group.add(queen_start_health)
    group.add(simulate_or_main_or_visualise)

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
                        Result[box.inactive_text] = box.text
                    return Result
        group.update(event_list, Result)

        window.fill(0)
        group.draw(window)
        pygame.display.flip()

    pygame.quit()
    exit()


restart = False
while True:
    user_answer = Input_window()
    if user_answer['simulate, main or visualise (1, 2 or 3)'] == '3':
        visualize.start()
        exit()
    if not user_answer[f'ants_n (from {MIN_N_ANTS} to {MAX_N_ANTS})'].isdigit() or not MIN_N_ANTS <= int(
            user_answer[f'ants_n (from {MIN_N_ANTS} to {MAX_N_ANTS})']) <= MAX_N_ANTS:
        pygame.draw.rect(window, (255, 0, 0), (50, 60, 600, 36))
        pygame.display.flip()
        restart = True
    if not user_answer[
        f'n_target_types (from {MIN_N_TARGET_TYPES} to {MAX_N_TARGET_TYPES})'].isdigit() or not MIN_N_TARGET_TYPES <= int(
            user_answer[f'n_target_types (from {MIN_N_TARGET_TYPES} to {MAX_N_TARGET_TYPES})']) <= MAX_N_TARGET_TYPES:
        pygame.draw.rect(window, (255, 0, 0), (50, 110, 600, 38))
        pygame.display.flip()
        restart = True
    if not user_answer[f'n_targets (from {MIN_N_TARGETS} to {MAX_N_TARGETS})'].isdigit() or not MIN_N_TARGETS <= int(
            user_answer[f'n_targets (from {MIN_N_TARGETS} to {MAX_N_TARGETS})']) <= MAX_N_TARGETS:
        pygame.draw.rect(window, (255, 0, 0), (50, 160, 600, 38))
        pygame.display.flip()
        restart = True
    if not user_answer[
        f'target_health (from {MIN_TARGET_HEALTH} to {MAX_TARGET_HEALTH})'].isdigit() or not MIN_TARGET_HEALTH <= int(
            user_answer[f'target_health (from 100 to 1500)']) <= MAX_TARGET_HEALTH:
        pygame.draw.rect(window, (255, 0, 0), (50, 210, 600, 38))
        pygame.display.flip()
        restart = True
    if not user_answer[
        f'margin_to_queen (from {MIN_MARGIN_TO_QUEEN} to {MAX_MARGIN_TO_QUEEN})'].isdigit() or not MIN_MARGIN_TO_QUEEN <= int(
            user_answer[
                f'margin_to_queen (from {MIN_MARGIN_TO_QUEEN} to {MAX_MARGIN_TO_QUEEN})']) <= MAX_MARGIN_TO_QUEEN:
        pygame.draw.rect(window, (255, 0, 0), (50, 260, 600, 38))
        pygame.display.flip()
        restart = True
    if not user_answer[
        f'queen_start_health (from {MIN_QUEEN_START_HEALTH} to {MAX_QUEEN_START_HEALTH})'].isdigit() or not MIN_QUEEN_START_HEALTH <= int(
            user_answer[
                f'queen_start_health (from {MIN_QUEEN_START_HEALTH} to {MAX_QUEEN_START_HEALTH})']) <= MAX_QUEEN_START_HEALTH:
        pygame.draw.rect(window, (255, 0, 0), (50, 310, 600, 38))
        pygame.display.flip()
        restart = True

    if not user_answer['simulate, main or visualise (1, 2 or 3)'].isdigit() or not 1 <= int(
            user_answer['simulate, main or visualise (1, 2 or 3)']) <= 3:
        pygame.draw.rect(window, (255, 0, 0), (50, 360, 600, 36))
        pygame.display.flip()
        restart = True
    time.sleep(3)
    if not restart:
        break

with open('user_settings.txt', 'w') as f:
    f.writelines(['{}: {}\n'.format(i, user_answer[i]) for i in user_answer.keys()])

if user_answer['simulate, main or visualise (1, 2 or 3)'] == '2':
    game.start()
elif user_answer['simulate, main or visualise (1, 2 or 3)'] == '1':
    simulate.start()
