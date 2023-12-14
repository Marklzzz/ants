import numpy as np
from random import randint, random

from config import *


def generate_new_target(target_types):
    """
    Generate new target by next(generate_new_target).
    :param target_types: target's types
    :return: new target type
    """
    i = randint(0, len(target_types) - 1)
    k = True
    while True:
        yield target_types[i] if k else 0
        if k:
            i = (i + 1) % len(target_types)
        k = not k


class Env:
    def __init__(self, t):
        """
        :param t: time step
        """
        self.t = t
        self.target_types = [_ for _ in range(1, N_TARGET_TYPES)]

        # create ants
        self.ants = [Ant(randint(MIN_DISTANCE_FROM_BORDER, WIDTH - MIN_DISTANCE_FROM_BORDER),
                         randint(MIN_DISTANCE_FROM_BORDER, HEIGHT - MIN_DISTANCE_FROM_BORDER),
                         self.target_types) for i in range(N_ANTS)]

        # create targets
        self.targets = []
        self.targets.append(Queen(WIDTH // 2, HEIGHT // 2, 0))  # append queen
        for target_type in self.target_types:
            for i in range(N_TARGETS // len(self.target_types)):
                self.targets.append(Target(randint(MIN_DISTANCE_FROM_BORDER, WIDTH - MIN_DISTANCE_FROM_BORDER),
                                           randint(MIN_DISTANCE_FROM_BORDER, HEIGHT - MIN_DISTANCE_FROM_BORDER),
                                           target_type))

    def step(self):
        shouts = []
        # update targets
        for target in self.targets:
            target.step(self.t)
        # update ants
        for ant in self.ants:
            ant.step(self.t, self.targets, shouts)
        # change ants directions
        for ant in self.ants:
            for shout in shouts:
                ant.update_direction(shout)


class Target:
    def __init__(self, x, y, target_type):
        """
        :param x: start x coordinate
        :param y: start y coordinate
        :param target_type: type of target
        """
        self.pos = np.array([x, y], dtype=np.float32)
        self.speed = np.array([0., 0.])
        self.target_type = target_type
        self.size = TARGET_START_SIZE

    def step(self, t: float):
        """
        :param t: time step
        :return:
        """
        random_angle = 2 * np.pi * random()
        self.speed += TARGET_ACCELERATION * np.array([np.cos(random_angle), np.sin(random_angle)]) * t
        self.pos += self.speed * t

        if self.pos[0] < 0:
            self.pos[0] = 0
            self.speed[0] *= -1
        if self.pos[0] > WIDTH:
            self.pos[0] = WIDTH
            self.speed[0] *= -1
        if self.pos[1] < 0:
            self.pos[1] = 0
            self.speed[1] *= -1
        if self.pos[1] > HEIGHT:
            self.pos[1] = HEIGHT
            self.speed[1] *= -1


class Queen(Target):
    pass


class Ant:
    def __init__(self, x, y, target_types):
        """
        :param x: start x
        :param y: start y
        :param target_types: targets' types without 0 - queen target.
        """
        self.pos = np.array([x, y], dtype=np.float32)
        angle = 2 * np.pi * random()
        self.direction = np.array([np.cos(angle), np.sin(angle)])
        self.target_generator = generate_new_target(target_types)
        self.current_target = next(self.target_generator)
        self.target_distances = [np.inf for _ in [0] + target_types]

    def step(self, t, targets, shouts):
        """
        Update ant position and shout if ant find target
        :param t: time step
        :param targets: existing targets
        :param shouts: existing shouts
        """
        self.pos += ANT_SPEED * (1 + random()*ANT_SPEED_NOISE) * self.direction * t
        self.target_distances = [dist + 1 for dist in self.target_distances]

        # self.pos[0] %= WIDTH
        # self.pos[1] %= HEIGHT

        if self.pos[0] < 0:
            self.pos[0] = 0
            self.direction[0] *= -1
        if self.pos[0] > WIDTH:
            self.pos[0] = WIDTH
            self.direction[0] *= -1
        if self.pos[1] < 0:
            self.pos[1] = 0
            self.direction[1] *= -1
        if self.pos[1] > HEIGHT:
            self.pos[1] = HEIGHT
            self.direction[1] *= -1

        for target in targets:
            if np.linalg.norm(self.pos - target.pos) <= target.size and target.target_type == self.current_target:
                target.size *= K_REDUCING_TARGET
                self.target_distances[self.current_target] = 0
                self.current_target = next(self.target_generator)
                self.direction *= -1
                shouts.append(Shout([dist + SHOUT_DISTANCE for dist in self.target_distances], self.pos))
                break
        else:
            if random() < CHANCE_TO_SHOUT:
                shouts.append(Shout([dist + SHOUT_DISTANCE for dist in self.target_distances], self.pos))

    def update_direction(self, shout):
        """
        Update ant direction
        :param shout: shout
        """
        if (shout.pos != self.pos).all() and np.linalg.norm(shout.pos - self.pos) <= SHOUT_DISTANCE:
            for i, dist in enumerate(shout.distances):
                if self.target_distances[i] > dist:
                    self.target_distances[i] = dist
                    if self.current_target == i:
                        self.direction = (shout.pos - self.pos) / np.linalg.norm(shout.pos - self.pos)


class Shout:
    def __init__(self, distances, pos):
        """
        :param distances: distances that ant shout
        :param pos: ant position
        """
        self.pos = pos
        self.distances = distances
