import pygame
from pygame import display
from modules.helpers.constants import *
from modules.helpers.physics import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        """ Variable init """

        self.xvel = self.yvel = 0  # velocity variables
        self.health = 100

        """ Appearance and location init """

        player = pygame.Surface(PLAYER_SHAPE)
        player.fill(BLACK)
        player.set_colorkey(BLACK)
        self.image = player  # initialize background for player
        self.static_image = player  # initialize a static image to apply transformations
        # draw the player on the background
        pygame.draw.polygon(self.image, WHITE, PLAYER_POINTS)

        # set player starting location
        self.rect = self.image.get_rect(center=PLAYER_SPAWN_LOCATION)

    def jump(self, velocity):
        # moves the player in the opposite direction of the mouse
        velocities = move(pygame.mouse.get_pos(), self.rect.center, velocity)

        self.xvel -= velocities[0]
        self.yvel -= velocities[1]

    def update(self):
        """ Rotation update """

        self.image = pygame.transform.rotate(  # applies the rotation transformation
            self.static_image,
            -point_in_direction(  # reverses direction for point towards mouse
                pygame.mouse.get_pos(),  # get location of mouse
                self.rect.center  # get center of player
            )
        )

        # centers the player's rotation
        self.rect = self.image.get_rect(center=self.rect.center)

        """ Gravity and friction update """

        self.xvel *= FRICTION  # horizontal slowdown for air friction
        self.yvel += GRAVITY  # vertical slowdown for gravity

        # cap the velocities to terminal velocities
        if self.xvel > PLAYER_TERMINAL_VELOCITY:
            self.xvel = PLAYER_TERMINAL_VELOCITY
        elif self.xvel < -PLAYER_TERMINAL_VELOCITY:
            self.xvel = -PLAYER_TERMINAL_VELOCITY
        if self.yvel > PLAYER_TERMINAL_VELOCITY:
            self.yvel = PLAYER_TERMINAL_VELOCITY
        elif self.yvel < -PLAYER_TERMINAL_VELOCITY:
            self.yvel = -PLAYER_TERMINAL_VELOCITY

        """ Position update """

        self.rect.x += int(self.xvel)  # update player x location
        self.rect.y += int(self.yvel)  # update player y location

        if self.rect.x < 0:  # player bounces if hit walls
            self.rect.x = 0
            self.xvel *= -1
        elif (posx := DISPLAY_WIDTH - PLAYER_SIZE) < self.rect.x:
            self.rect.x = posx
            self.xvel *= -1
        if self.rect.y < 0:  # player stays within upper and lower boundaries
            self.rect.y = 0
            self.yvel = 0
        elif (posy := DISPLAY_HEIGHT - PLAYER_SIZE) < self.rect.y:
            self.rect.y = posy
            self.yvel = PLAYER_FLOOR_BOUNCE
