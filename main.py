""" Imports"""

import pygame
from pygame.constants import K_SPACE
from modules.game import Game
from modules.helpers.constants import *


""" Initialization """

game = Game()
clock = pygame.time.Clock()
pygame.display.set_caption(WINDOW_TITLE)
game.menu("start")

""" Variables """

pause = True
keepGoing = True
counter = FPS * SPAWN_RATE


""" Game loop """

while keepGoing:

    """ Event detection """

    for event in pygame.event.get():  # iterates through events
        if event.type == pygame.QUIT:  # checks for quit button
            keepGoing = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pause == True:
                pause = False
            if event.button == 1 or event.button == 3:  # left or right click
                game.fire(BULLET_MAP[event.button])
        if event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
                print("SPACE HIT")
                if pause == False:
                    pause = True
                    game.menu("pause")
                elif pause == True:
                    pause = False
            

    """ Check for pause game """

    if not pause:
        if game.update() == "menu":
            pause = True
        counter += 1

            

    if counter >= FPS * SPAWN_RATE:
        game.summonAsteroids()
        game.planetHP += 10
        counter = 0


    """ Clock tick """

    clock.tick(FPS)
