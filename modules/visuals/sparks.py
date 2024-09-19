import math
import pygame
from random import randint
from modules.helpers.constants import *
from modules.helpers.physics import point_in_direction


class Spark():
    def __init__(self, pos):
        self.pos = list(pos)
        self.angle = math.radians(point_in_direction(  # find angle
            pygame.mouse.get_pos(),
            pos
        ) + randint(-SPARK_SPREAD, SPARK_SPREAD))  # add spread
        self.speed = randint(SPARK_SPEED[0], SPARK_SPEED[1])

    def update(self, display):
        velocity = [  # find velocities
            math.cos(self.angle) * self.speed,
            math.sin(self.angle) * self.speed
        ]

        # update velocities
        velocity[0] *= FRICTION
        velocity[1] += GRAVITY * SPARK_FALL_MULTIPLIER

        # update position
        self.pos[0] += velocity[0]
        self.pos[1] += velocity[1]

        # get angle from velocities
        self.angle = math.atan2(velocity[1], velocity[0])

        self.speed -= SPARK_DECAY_MULTIPLIER  # decay spark

        points = [  # find points
            [self.pos[0] + math.cos(self.angle) * SPARK_SCALE,
                self.pos[1] + math.sin(self.angle) * SPARK_SCALE],
            [self.pos[0] + math.cos(self.angle + math.pi / 2) * SPARK_SCALE * 0.3,
                self.pos[1] + math.sin(self.angle + math.pi / 2) * SPARK_SCALE * 0.3],
            [self.pos[0] - math.cos(self.angle) * SPARK_SCALE * 3.5,
                self.pos[1] - math.sin(self.angle) * SPARK_SCALE * 3.5],
            [self.pos[0] + math.cos(self.angle - math.pi / 2) * SPARK_SCALE * 0.3,
                self.pos[1] - math.sin(self.angle + math.pi / 2) * SPARK_SCALE * 0.3],
        ]

        pygame.draw.polygon(display, GRAY, points)
