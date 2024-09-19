import random
import pygame
from modules.helpers.constants import *

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.Surface((CHUNKSIZE,CHUNKSIZE))
        self.image.fill(WHITEGRAY)
        self.rect = self.image.get_rect()
        self.rect.x = self.x * CHUNKSIZE
        self.rect.y = self.y * CHUNKSIZE
        self.trueRect = self.rect.y

    def asteroidGeneration():

        # 2d array for asteroid shape
        # 3 is the 0 in the array
        asteroid = [[0]*7 for i in range(7)]

        # distance from center
        pos_x = random.randint(4, 6)
        pos_y = random.randint(4, 6)
        neg_x = random.randint(0, 2)
        neg_y = random.randint(0, 2)

        # list of points that are pixels of the asteroid (putting in outter four points in each direction and the center point in here)
        chosen = [(3, 3), (pos_x, 0), (neg_x, 0),
                (0, pos_y), (0, neg_y)]

        # randomly doing curve of asteroid (four curves)
        
        for i in range(pos_y - 3):
            if pos_x > 3:
                curve = random.randint(0, round((pos_x-3)))
                pos_x -= curve

            if pos_x < 3:
                pos_x = 3

            if (i + 3, pos_x) not in chosen:
                chosen.append((i + 3, pos_x))

        
        for j in range(3 - neg_y):
            if pos_x > 3:
                curve = random.randint(0, round((pos_x-3)))
                pos_x -= curve

            if pos_x < 3:
                pos_x = 3

            if (3 - j, pos_x) not in chosen:
                chosen.append((3 - j, pos_x))

        for k in range(pos_y - 3):
            if neg_x < 3:
                curve = random.randint(0, round((3 - neg_x)))
                neg_x += curve

            if neg_x > 3:
                neg_x = 3

            if (k + 3, neg_x) not in chosen:
                chosen.append((k + 3, neg_x))

        for h in range(3 - neg_y):
            if neg_x < 3:
                curve = random.randint(0, round((3 - neg_x)))
                neg_x += curve

            if neg_x > 3:
                neg_x = 3

            if (3 - h, neg_x) not in chosen:
                chosen.append((3 - h, neg_x))

        chosen_copy = chosen
        for (x, y) in chosen_copy:
            copy_x = x
            if x > 3:
                while copy_x > 3:
                    copy_x -= 1
                    if (copy_x, y) not in chosen:
                        chosen.append((copy_x, y))
            elif copy_x < 3:
                while copy_x < 3:
                    copy_x += 1
                    if (copy_x, y) not in chosen:
                        chosen.append((copy_x, y))
            copy_y = y
            if y > 3:
                while copy_y > 3:
                    copy_y -= 1
                    if (x, copy_y) not in chosen:
                        chosen.append((x, copy_y))
            elif y < 3:
                while copy_y < 3:
                    copy_y += 1
                    if (x, copy_y) not in chosen:
                        chosen.append((x, copy_y))

        # adding in inside of asteroid to chosen
        # plotting asteroid onto 2d array
        for a in range(7):
            for b in range(7):
                if (a, b) in chosen:
                    asteroid[a][b] = 1
                else:
                    asteroid[a][b] = 0

        return asteroid

    def update(self):
        self.trueRect -= .3
        self.rect.y = int(self.trueRect)

