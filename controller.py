import numpy as np
from numba.experimental import jitclass
from numba import njit, deferred_type, prange
import numba as nb
from random import randint, random

from config import *


@njit
def norm(x):
    return (x[0] ** 2 + x[1] ** 2) ** 0.5


target_spec = [('x', nb.float64),
               ('y', nb.float64),
               ('target_type', nb.int32),
               ('speed', nb.float32[:]),
               ('pos', nb.float32[:]),
               ('size', nb.float32)]


@jitclass(target_spec)
class Target:
    def __init__(self, x: float, y: float, target_type: int):
        """
        :param x: start x coordinate
        :param y: start y coordinate
        :param target_type: type of target
        """
        self.pos = np.array([x, y], dtype=np.float32)
        self.speed = np.array([0., 0.], dtype=np.float32)
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


# class Queen(Target):
#     pass


shout_spec = [('distances', nb.float64[:]),
              ('pos', nb.float32[:])]


@jitclass(shout_spec)
class Shout:
    def __init__(self, distances, pos):
        """
        :param distances: distances that ant shout
        :param pos: ant position
        """
        self.pos = pos
        self.distances = distances


ant_spec = [('x', nb.float32),
            ('y', nb.float32),
            ('target_types', nb.int32[:]),
            ('pos', nb.float32[:]),
            ('speed', nb.float32),
            ('direction', nb.float32[:]),
            ('current_target', nb.int32),
            ('target_distances', nb.float64[:]),
            ('return_to_queen', nb.boolean),
            ('k', nb.int32)]


@jitclass(ant_spec)
class Ant:
    def __init__(self, x: float, y: float, target_types):
        """
        :param x: start x
        :param y: start y
        :param target_types: targets' types without 0 - queen target.
        """
        self.pos = np.array([x, y], dtype=np.float32)
        self.speed = ANT_SPEED * (1 + (random() - 1) * ANT_SPEED_NOISE)
        angle = 2 * np.pi * random()
        self.direction = np.array([np.cos(angle), np.sin(angle)], np.float32)
        self.current_target = randint(1, len(target_types))
        self.return_to_queen = False
        self.k = self.current_target

        self.target_distances = np.full(len(target_types) + 1, np.inf, dtype=np.float64)

    def step(self, t: float, targets):
        """
        Update ant position and shout if ant find target
        :param t: time step
        :param targets: existing targets
        """
        random_angle = 2 * (random() - 1) * ANT_DIRECTION_NOISE
        self.pos += self.speed * np.array([np.cos(random_angle) * self.direction[0] -
                                           np.sin(random_angle) * self.direction[1],
                                           np.sin(random_angle) * self.direction[0] +
                                           np.cos(random_angle) * self.direction[1]
                                           ]) * t
        self.target_distances += 1

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
            if norm(self.pos - target.pos) <= target.size and target.target_type == self.current_target:
                target.size *= K_REDUCING_TARGET
                self.target_distances[self.current_target] = 0
                self.update_target()
                self.direction *= -1
                return Shout(self.target_distances + SHOUT_DISTANCE, self.pos)
        if random() < CHANCE_TO_SHOUT:
            return Shout(self.target_distances + SHOUT_DISTANCE, self.pos)
        else:
            return None

    def update_direction(self, shout: Shout):
        """
        Update ant direction
        :param shout: shout
        """
        if (shout.pos != self.pos).any() and norm(shout.pos - self.pos) <= SHOUT_DISTANCE:
            for i, dist in enumerate(shout.distances):
                if self.target_distances[i] > dist:
                    self.target_distances[i] = dist
                    if self.current_target == i:
                        self.direction = ((shout.pos - self.pos) / norm(shout.pos - self.pos)).astype(np.float32)

    def update_target(self):
        if not self.return_to_queen:
            self.current_target = 0
        else:
            self.k = (self.k + 1) % N_TARGET_TYPES
            if self.k == 0:
                self.k = 1
            self.current_target = self.k
        self.return_to_queen = not self.return_to_queen


shout_type = deferred_type()
shout_type.define(Shout.class_type.instance_type)

ant_type = deferred_type()
ant_type.define(Ant.class_type.instance_type)

target_type = deferred_type()
target_type.define(Target.class_type.instance_type)


@njit(cache=True, parallel=True)
def step(ants, shouts):
    # change ants directions
    for i in prange(len(ants)):
        for j in prange(len(shouts)):
            ants[i].update_direction(shouts[j])


class Env:
    def __init__(self, t: float):
        """
        :param t: time step
        """
        self.t = t
        self.target_types = np.array([_ for _ in range(1, N_TARGET_TYPES)], dtype=np.int32)

        # create ants
        self.ants = nb.typed.List([Ant(randint(MIN_DISTANCE_FROM_BORDER, WIDTH - MIN_DISTANCE_FROM_BORDER),
                                       randint(MIN_DISTANCE_FROM_BORDER, HEIGHT - MIN_DISTANCE_FROM_BORDER),
                                       self.target_types) for _ in range(N_ANTS)])

        # create targets
        self.targets = nb.typed.List([Target(WIDTH // 2, HEIGHT // 2, 0)])  # append queen
        for target_type_ in self.target_types:
            for i in range(N_TARGETS // len(self.target_types)):
                self.targets.append(Target(randint(MIN_DISTANCE_FROM_BORDER, WIDTH - MIN_DISTANCE_FROM_BORDER),
                                           randint(MIN_DISTANCE_FROM_BORDER, HEIGHT - MIN_DISTANCE_FROM_BORDER),
                                           target_type_))

    def step(self):
        shouts = nb.typed.List()
        # update targets
        for target in self.targets:
            target.step(self.t)
        # update ants
        for ant in self.ants:
            shout = ant.step(self.t, self.targets)
            if shout is not None:
                shouts.append(shout)
        if len(shouts) != 0:
            step(self.ants, shouts)
        # shouts = nb.typed.List()
        # # update targets
        # for target in self.targets:
        #     target.step(self.t)
        # # update ants
        # for ant in self.ants:
        #     shout = ant.step(self.t, self.targets)
        #     if shout is not None:
        #         shouts.append(shout)
        # # change ants directions
        # for ant in self.ants:
        #     for shout in shouts:
        #         ant.update_direction(shout)
