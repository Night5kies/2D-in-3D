import pygame
from random import randint
from modules.helpers.constants import *


class Particle():
    def __init__(self, pos):
        self.pos = list(pos)
        self.vel = [  # generate random spread velocity
            randint(-PARTICLE_SPREAD, PARTICLE_SPREAD),
            randint(-PARTICLE_SPREAD, PARTICLE_SPREAD)
        ]
        self.size = randint(PARTICLE_SIZE[0], PARTICLE_SIZE[1])  # random size

    def update(self, display):

        self.vel[0] *= FRICTION  # slow down from air resistance
        self.vel[1] += GRAVITY  # change velocity by gravity

        self.pos[0] += self.vel[0]  # move x
        self.pos[1] += self.vel[1]  # move y

        self.size -= PARTICLE_DECAY_SPEED  # decrease particle size

        pygame.draw.circle(display, GRAY, self.pos, int(self.size))
