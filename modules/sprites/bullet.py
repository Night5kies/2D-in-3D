import pygame
from modules.helpers.constants import *
from modules.helpers.physics import *


class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, type):
        super().__init__()

        self.image = pygame.Surface(BULLET_SHAPE[type])
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.x = position[0] - BULLET_OFFSET[type][0]
        self.rect.y = position[1] - BULLET_OFFSET[type][1]
        self.trueRect = self.rect

        self.velocity = move(
            pygame.mouse.get_pos(),
            self.rect, BULLET_VELOCITY[type]
        )

    def update(self):
        # kill bullet if it goes a screens distance from any border
        if self.rect.x < -DISPLAY_WIDTH \
                or self.rect.x > DISPLAY_WIDTH * 2 \
                or self.rect.y < -DISPLAY_HEIGHT or \
                self.rect.y > DISPLAY_HEIGHT * 2:
            self.kill()
        self.trueRect.x += self.velocity[0]
        self.trueRect.y += self.velocity[1]
        self.rect.x = int(self.trueRect.x)
        self.rect.y = int(self.trueRect.y)
