import numpy as np
from numba.experimental import jitclass
from numba import njit, deferred_type, prange, types, typed
import numba as nb
from random import randint, random
import config

config.update()


@njit
def norm(x):
    """
    :param x:
    :return: fast distance
    """
    return (x[0] ** 2 + x[1] ** 2) ** 0.5


# spec map for target class
target_spec = [('x', nb.float64),
               ('y', nb.float64),
               ('target_type', nb.int32),
               ('speed', nb.float32[:]),
               ('pos', nb.float32[:]),
               ('size', nb.float32),
               ('resources', nb.int32[:]),
               ('health', nb.int32)]


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
        self.size = config.TARGET_START_SIZE
        self.resources = np.array([0 for i in range(config.N_TARGET_TYPES - 1)], dtype=np.int32)
        self.health = config.QUEEN_START_HEALTH

    def step(self, t: float):
        """
        step method for target class
        :param t: time step
        :return:
        """
        random_angle = 2 * np.pi * random()
        self.speed += config.TARGET_ACCELERATION * np.array([np.cos(random_angle), np.sin(random_angle)]) * t
        self.pos += self.speed * t

        if self.pos[0] < 0:
            self.pos[0] = 0
            self.speed[0] *= -1
        if self.pos[0] > config.WIDTH:
            self.pos[0] = config.WIDTH
            self.speed[0] *= -1
        if self.pos[1] < 0:
            self.pos[1] = 0
            self.speed[1] *= -1
        if self.pos[1] > config.HEIGHT:
            self.pos[1] = config.HEIGHT
            self.speed[1] *= -1

        if self.target_type == 0 and random() < config.QUEEN_LOSE_HEALTH_CHANCE:
            self.health -= 1

        if self.target_type == 0 and min(self.resources) > 0:
            self.resources -= 1
            self.health += 1

        if self.health <= 0:
            self.size = 0

        if self.health > config.QUEEN_START_HEALTH:
            self.health = config.QUEEN_START_HEALTH


# shout spec for shout class
shout_spec = [('distances', nb.float64[:]),
              ('pos', nb.float32[:])]


@jitclass(shout_spec)
class Shout:
    """
    shout class, contains distances to ant shout, position of shout
    """

    def __init__(self, distances, pos):
        """
        :param distances: distances that ant shout
        :param pos: ant position
        """
        self.pos = pos
        self.distances = distances


# ant spec for ant class
ant_spec = [('x', nb.float32),
            ('y', nb.float32),
            ('target_types', nb.int32[:]),
            ('pos', nb.float32[:]),
            ('speed', nb.float32),
            ('direction', nb.float32[:]),
            ('current_target', nb.int32),
            ('target_distances', nb.float64[:]),
            ('return_to_queen', nb.boolean),
            ('k', nb.int32),
            ('dist_to_queen', nb.float64),
            ('previous_target', nb.int32)]


@jitclass(ant_spec)
class Ant:
    """
    ant class, contains ant logic
    """

    def __init__(self, x: float, y: float, target_types):
        """
        :param x: start x
        :param y: start y
        :param target_types: targets' types without 0 - queen target.
        """
        self.pos = np.array([x, y], dtype=np.float32)
        self.speed = config.ANT_SPEED * (1 + (random() - 1) * config.ANT_SPEED_NOISE)
        angle = 2 * np.pi * random()
        self.direction = np.array([np.cos(angle), np.sin(angle)], np.float32)
        self.current_target = randint(1, len(target_types))
        self.return_to_queen = False
        self.k = self.current_target
        self.dist_to_queen = config.WIDTH
        self.previous_target = 0

        self.target_distances = np.full(len(target_types) + 1, np.inf, dtype=np.float64)

    def step(self, t: float, targets):
        """
        Update ant position and shout if ant find target
        step method for ant class
        :param t: time step
        :param targets: existing targets
        """
        random_angle = 2 * (random() - 1) * config.ANT_DIRECTION_NOISE
        self.pos += self.speed * np.array([np.cos(random_angle) * self.direction[0] -
                                           np.sin(random_angle) * self.direction[1],
                                           np.sin(random_angle) * self.direction[0] +
                                           np.cos(random_angle) * self.direction[1]
                                           ]) * t
        self.target_distances += 1

        if self.pos[0] < 0:
            self.pos[0] = 0
            self.direction[0] *= -1
        if self.pos[0] > config.WIDTH:
            self.pos[0] = config.WIDTH
            self.direction[0] *= -1
        if self.pos[1] < 0:
            self.pos[1] = 0
            self.direction[1] *= -1
        if self.pos[1] > config.HEIGHT:
            self.pos[1] = config.HEIGHT
            self.direction[1] *= -1

        self.dist_to_queen = max(config.WIDTH, config.HEIGHT)

        # target interaction logic
        for i in prange(len(targets)):
            target = targets[i]
            dist = norm(self.pos - target.pos)
            if target.target_type == 0 and dist < self.dist_to_queen and target.size != 0:
                self.dist_to_queen = dist
            if dist <= target.size and target.target_type == self.current_target:
                if target.target_type != 0: target.size -= config.TARGET_START_SIZE / config.TARGET_HEALTH
                if target.size <= config.TARGET_START_SIZE // config.DELETE_TARGET_MARGIN:
                    targets.append(
                        Target(randint(config.MIN_DISTANCE_FROM_BORDER, config.WIDTH - config.MIN_DISTANCE_FROM_BORDER),
                               randint(config.MIN_DISTANCE_FROM_BORDER,
                                       config.HEIGHT - config.MIN_DISTANCE_FROM_BORDER),
                               target.target_type))
                    target.size = 0
                if target.target_type == 0:
                    target.resources[self.previous_target - 1] += 1
                self.target_distances[self.current_target] = 0
                self.update_target(target.resources)
                self.direction *= -1
                return Shout(self.target_distances + config.SHOUT_DISTANCE, self.pos)
        if random() < config.CHANCE_TO_SHOUT:
            return Shout(self.target_distances + config.SHOUT_DISTANCE, self.pos)
        if random() < config.CHANCE_TO_QUEEN and self.dist_to_queen >= config.MARGIN_TO_QUEEN * config.WIDTH:
            targets.append(Target(self.pos[0], self.pos[1], 0))
        else:
            return None

    def update_direction(self, shout: Shout):
        """
        Update ant direction
        :param shout: shout
        """
        if (shout.pos != self.pos).any() and norm(shout.pos - self.pos) <= config.SHOUT_DISTANCE:
            for i in prange(len(shout.distances)):
                if self.target_distances[i] > shout.distances[i]:
                    self.target_distances[i] = shout.distances[i]
                    if self.current_target == i:
                        self.direction = ((shout.pos - self.pos) / norm(shout.pos - self.pos)).astype(np.float32)

    def update_target(self, target_resources):
        if not self.return_to_queen and self.current_target != 0:
            self.previous_target = self.current_target
            self.current_target = 0
        else:
            self.current_target = randint(1, config.N_TARGET_TYPES - 1)
        self.return_to_queen = not self.return_to_queen


shout_type = deferred_type()
shout_type.define(Shout.class_type.instance_type)

ant_type = deferred_type()
ant_type.define(Ant.class_type.instance_type)

target_type = deferred_type()
target_type.define(Target.class_type.instance_type)


@njit(cache=True, parallel=True)
def step(t, ants, targets, shouts):
    for i in prange(len(targets)):
        targets[i].step(t)
    # update ants
    for ant in ants:
        shout = ant.step(t, targets)
        if shout is not None:
            shouts.append(shout)
    if len(shouts) != 0:
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
        self.target_types = np.array([_ for _ in range(1, config.N_TARGET_TYPES)], dtype=np.int32)

        # create ants
        self.ants = nb.typed.List(
            [Ant(randint(config.MIN_DISTANCE_FROM_BORDER, config.WIDTH - config.MIN_DISTANCE_FROM_BORDER),
                 randint(config.MIN_DISTANCE_FROM_BORDER, config.HEIGHT - config.MIN_DISTANCE_FROM_BORDER),
                 self.target_types) for _ in range(config.N_ANTS)])

        # create targets
        self.targets = nb.typed.List([Target(config.WIDTH // 2, config.HEIGHT // 2, 0)])  # append queen
        for target_type_ in self.target_types:
            for i in range(config.N_TARGETS // len(self.target_types)):
                self.targets.append(
                    Target(randint(config.MIN_DISTANCE_FROM_BORDER, config.WIDTH - config.MIN_DISTANCE_FROM_BORDER),
                           randint(config.MIN_DISTANCE_FROM_BORDER, config.HEIGHT - config.MIN_DISTANCE_FROM_BORDER),
                           target_type_))

        self.shouts = nb.typed.List([Shout(self.ants[0].target_distances + config.SHOUT_DISTANCE, self.ants[0].pos)])

    def step(self):
        self.shouts.clear()
        step(self.t, self.ants, self.targets, self.shouts)
