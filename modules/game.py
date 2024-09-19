import pygame
import random

from pygame.mixer import pause
from modules.helpers.render import *
from modules.helpers.physics import *
from modules.helpers.constants import *
from modules.sprites.player import Player
from modules.sprites.bullet import Bullet
from asteroid import Asteroid
from modules.visuals.sparks import Spark
from modules.visuals.particles import Particle


class Game():
    def __init__(self):
        self.display = pygame.display.set_mode(DISPLAY_SIZE)  # create display
        self.sprites = pygame.sprite.Group()  # create a group of sprites
        self.asteroids = pygame.sprite.Group()
        pygame.font.init()
        self.sparks = []  # create a group of sparks
        self.particles = []  # create a group of particles

        self.reset()

    def reset(self):  # resets game
        """ Kill sprites """
        
        for asteroid in self.asteroids:
            asteroid.kill()

        for sprite in self.sprites:
            sprite.kill()

        """ Create player """

        self.player = Player()  # create player
        self.sprites.add(self.player)  # add player to sprites

        """ Create background """
        
        self.backgroundInit()


        """ Reset variables """
        
        self.score = 0
        self.cooldown = [0, 0]
        self.planetHP = PLANET_MAX_HP

        """ Menu """

        self.menu("start")
        
    
    
    def menu(self, type):
        if type == "start":
            #add background 
            self.display.fill(BLACK)

            self.backgroundInit()

            for backgroundObject in self.backgroundObjects:
                object = pygame.Rect(backgroundObject[1][0],
                                    backgroundObject[1][1],
                                    backgroundObject[1][2],backgroundObject[1][3])
                color = (int(WHITE[0] * backgroundObject[0]),
                        int(WHITE[1] * backgroundObject[0]),
                        int(WHITE[2] * backgroundObject[0]))
                pygame.draw.rect(self.display, color, object)

            renderText(
                self.display,
                "agencyfb", 
                100,
                "Click to play",
                WHITE,
                DISPLAY_CENTER[0],
                DISPLAY_CENTER[1]
            )

        elif type == "pause":
            renderText(
                self.display,
                "agencyfb", 
                100,
                "Paused",
                WHITE,
                DISPLAY_CENTER[0]/3,
                DISPLAY_CENTER[1]/3
            )
            renderText(
                self.display,
                "agencyfb", 
                100,
                "Click to Resume",
                WHITE,
                DISPLAY_CENTER[0],
                DISPLAY_CENTER[1] 
            )
        pygame.display.update()

    def backgroundInit(self):
        self.backgroundObjects = []
        self.objectMultiplier = .5
        for i in range(random.randint(12, 17)):
            self.backgroundObjects.insert(0, self.generateBackgroundObject())
            self.objectMultiplier *= 0.9


    def fire(self, type):  # fires a bullet
        if self.cooldown[type] == 0:  # checks for cooldown
            self.cooldown[type] = BULLET_COOLDOWN[type]  # set cooldown
            # find recoil
            self.player.jump(RECOIL[type])
            # create bullet and add to sprites
            self.sprites.add(Bullet(self.player.rect.center, type))
            
            for i in range(type * 5 + 5):
                self.sparks.insert(0, Spark(self.player.rect.center))
                # self.particles.append(Particle(self.player.rect.center))

        """ Asteroids """

    def summonAsteroids(self):

        temp_x = x_placement = random.randint(0, DISPLAY_WIDTH/CHUNKSIZE - 7)
        y_placement = DISPLAY_HEIGHT/CHUNKSIZE

        design = Asteroid.asteroidGeneration()

        for layer in design:
            x_placement = temp_x
            for chunk in layer:
                if chunk == 1:
                    asteroid = Asteroid(x_placement, y_placement)
                    self.asteroids.add(asteroid)
                x_placement += 1
            y_placement += 1



    def generateBackgroundObject(self):
        objectSize = int((1 - 1.5 * self.objectMultiplier) * 1200)
        objectHalfSize = int(objectSize / 2)
        minSpawnMultiplier = -0.5 + self.objectMultiplier
        maxSpawnMultiplier = 1.5 - self.objectMultiplier
        return [
                    self.objectMultiplier,
                    [
                        random.randint(int(DISPLAY_WIDTH * minSpawnMultiplier), int(DISPLAY_WIDTH * maxSpawnMultiplier) - objectSize),
                        random.randint(int(DISPLAY_HEIGHT * minSpawnMultiplier), int(DISPLAY_HEIGHT * maxSpawnMultiplier) - objectSize),
                        random.randint(objectHalfSize, objectSize),
                        random.randint(objectHalfSize, objectSize)
                    ]
                ]

    def update(self):
        """ Background render """

        self.display.fill(BLACK)  # resets the screen to black

        for backgroundObject in self.backgroundObjects:
            object = pygame.Rect(backgroundObject[1][0],
                                 backgroundObject[1][1],
                                 backgroundObject[1][2],backgroundObject[1][3])
            color = (int(WHITE[0] * backgroundObject[0]),
                    int(WHITE[1] * backgroundObject[0]),
                    int(WHITE[2] * backgroundObject[0]))
            pygame.draw.rect(self.display, color, object)

        """ Sprites update and render """

        self.sprites.update()  # call update to all sprites

        # Checking for collision
        for asteroid in self.asteroids:
            asteroid.update()
            if self.player.rect.colliderect(asteroid.rect):
                collisions = collisionCheck(asteroid.rect, self.player.rect)
                if collisions['bottom']:
                    self.player.rect.y = asteroid.rect.y - self.player.rect[3]
                    self.player.yvel *= PLAYER_COLLIDE_Y_SLOW_DOWN_MULTIPLIER
                if collisions['top']:
                    self.player.rect.y = asteroid.rect.y + CHUNKSIZE + 1
                    self.player.yvel *= PLAYER_COLLIDE_Y_SLOW_DOWN_MULTIPLIER
                if collisions['right']:
                    self.player.rect.x = asteroid.rect.x - self.player.rect[2]
                    self.player.xvel *= PLAYER_COLLIDE_X_SLOW_DOWN_MULTIPLIER
                if collisions['left']:
                    self.player.rect.x = asteroid.rect.x + CHUNKSIZE + 1
                    self.player.xvel *= PLAYER_COLLIDE_X_SLOW_DOWN_MULTIPLIER
                asteroid.kill()
                self.score += 1
                self.player.health -= 10
            if asteroid.rect.y <= 0:
                asteroid.kill()
                self.planetHP -= 10

        # Checking for Bullet Collision

        for sprite in self.sprites:
            for asteroid in self.asteroids:
                if sprite.rect.colliderect(asteroid.rect) and sprite.rect[2] == BULLET_SIZE[0]:
                    sprite.kill()
                    for z in range(random.randint(10,20)):
                        self.particles.append(Particle(asteroid.rect.center))
                    asteroid.kill()
                    self.score += 1
                    self.player.health += 1
                elif sprite.rect.colliderect(asteroid.rect) and sprite.rect[2] == BULLET_SIZE[1]:
                    for z in range(random.randint(7,15)):
                        self.particles.append(Particle(asteroid.rect.center))
                    asteroid.kill()
                    self.score += 1
                    self.player.health += 1
                else:
                    self.display.blit(asteroid.image, asteroid.rect)

 

        """ Overlay render for cooldown """
        for sprite in self.sprites:  # render each sprite
            self.display.blit(sprite.image, sprite.rect)

        """ Visual effects """

        for spark in self.sparks:
            spark.update(self.display)  # update each spark
            if spark.speed <= 0:  # kill spark if it's speed is less than 0
                self.sparks.remove(spark)

        for particle in self.particles:
            particle.update(self.display)  # update each particle
            if particle.size <= 0:  # kill particle if it shrinks to 0
                self.particles.remove(particle)

        """ Overlay update and render """
        # planet health

        if self.planetHP <= 0:
            
            self.reset()
            return "menu"

        if self.planetHP > PLANET_MAX_HP:
            self.planetHP = PLANET_MAX_HP

        if self.planetHP != PLANET_MAX_HP:  # if the player is not at max health
            # position of health bar
            planetHPBarX = DISPLAY_WIDTH - PLANET_HP_BAR_WIDTH - 10
            planetHPBarY = (DISPLAY_HEIGHT - PLANET_HP_BAR_HEIGHT)/2

            renderRect(  # render bar background
                self.display,
                BLACK,
                planetHPBarX - HEALTH_BAR_BORDER,
                planetHPBarY - HEALTH_BAR_BORDER,
                PLANET_HP_BAR_WIDTH + HEALTH_BAR_BORDER * 2,
                PLANET_HP_BAR_HEIGHT + HEALTH_BAR_BORDER * 2
            )

            renderRect(  # render bar gray area
                self.display,
                GRAY,
                planetHPBarX,
                planetHPBarY,
                PLANET_HP_BAR_WIDTH,
                PLANET_HP_BAR_HEIGHT,
            )

            renderRect(  # render bar fill value
                self.display,
                WHITE,
                planetHPBarX,
                planetHPBarY,
                PLANET_HP_BAR_WIDTH,  # *** If bar size is changed, player health needs to be mapped ***
                self.planetHP
            )

        # player health

        if self.player.health <= 0:
            self.reset()
            return "menu"

        if self.player.health >= PLAYER_MAX_HEALTH:
            self.player.health = PLAYER_MAX_HEALTH

        if self.player.health != PLAYER_MAX_HEALTH:  # if the player is not at max health
            # position of health bar
            healthBarX = self.player.rect.x - \
                (HEALTH_BAR_WIDTH - PLAYER_SIZE) / 2
            healthBarY = self.player.rect.y - HEALTH_BAR_OFFSET

            renderRect(  # render bar background
                self.display,
                BLACK,
                healthBarX - HEALTH_BAR_BORDER,
                healthBarY - HEALTH_BAR_BORDER,
                HEALTH_BAR_WIDTH + HEALTH_BAR_BORDER * 2,
                HEALTH_BAR_HEIGHT + HEALTH_BAR_BORDER * 2
            )

            renderRect(  # render bar gray area
                self.display,
                GRAY,
                healthBarX,
                healthBarY,
                HEALTH_BAR_WIDTH,
                HEALTH_BAR_HEIGHT,
            )

            renderRect(  # render bar fill value
                self.display,
                WHITE,
                healthBarX,
                healthBarY,
                self.player.health,  # *** If bar size is changed, player health needs to be mapped ***
                HEALTH_BAR_HEIGHT
            )

        # bullet cooldown

        if self.cooldown[0] > 0:  # bullet
            self.cooldown[0] -= 1  # decrease bullet cooldown

            player_center_x = self.player.rect.center[0]  # middle of player
            progress_bar_height = int(  # calculate height of progress bar
                (BULLET_COOLDOWN[0] - self.cooldown[0]) /
                BULLET_COOLDOWN[0] * AMMO_RECHARGE_BAR_HEIGHT
            )

            renderRect(  # render bar background
                self.display,
                BLACK,
                player_center_x - AMMO_RECHARGE_BAR_OFFSET -
                AMMO_RECHARGE_BAR_WIDTH - 2 * AMMO_RECHARGE_BAR_BORDER,
                self.player.rect.y,
                AMMO_RECHARGE_BAR_WIDTH + 2 * AMMO_RECHARGE_BAR_BORDER,
                2 * AMMO_RECHARGE_BAR_BORDER + AMMO_RECHARGE_BAR_HEIGHT
            )

            renderRect(  # render bar gray area
                self.display,
                GRAY,
                player_center_x - AMMO_RECHARGE_BAR_OFFSET -
                AMMO_RECHARGE_BAR_WIDTH - AMMO_RECHARGE_BAR_BORDER,
                self.player.rect.y + AMMO_RECHARGE_BAR_BORDER,
                AMMO_RECHARGE_BAR_WIDTH,
                AMMO_RECHARGE_BAR_HEIGHT
            )

            renderRect(  # render bar fill value
                self.display,
                WHITE,
                player_center_x - AMMO_RECHARGE_BAR_OFFSET -
                AMMO_RECHARGE_BAR_WIDTH - AMMO_RECHARGE_BAR_BORDER,
                self.player.rect.y + AMMO_RECHARGE_BAR_BORDER +
                AMMO_RECHARGE_BAR_HEIGHT - progress_bar_height,
                AMMO_RECHARGE_BAR_WIDTH,
                progress_bar_height
            )

        if self.cooldown[1] > 0:  # alternate bullet
            self.cooldown[1] -= 1  # decrease alternate bullet cooldown

            player_center_x = self.player.rect.center[0]  # middle of player
            progress_bar_height = int(  # calculate height of progress bar
                (BULLET_COOLDOWN[1] - self.cooldown[1]) /
                BULLET_COOLDOWN[1] * AMMO_RECHARGE_BAR_HEIGHT
            )

            renderRect(  # render bar background
                self.display,
                BLACK,
                player_center_x + AMMO_RECHARGE_BAR_OFFSET,
                self.player.rect.y,
                AMMO_RECHARGE_BAR_WIDTH + 2 * AMMO_RECHARGE_BAR_BORDER,
                2 * AMMO_RECHARGE_BAR_BORDER + AMMO_RECHARGE_BAR_HEIGHT
            )

            renderRect(  # render bar gray area
                self.display,
                GRAY,
                player_center_x + AMMO_RECHARGE_BAR_OFFSET + AMMO_RECHARGE_BAR_BORDER,
                self.player.rect.y + AMMO_RECHARGE_BAR_BORDER,
                AMMO_RECHARGE_BAR_WIDTH,
                AMMO_RECHARGE_BAR_HEIGHT
            )

            renderRect(  # render bar fill value
                self.display,
                WHITE,
                player_center_x + AMMO_RECHARGE_BAR_OFFSET + AMMO_RECHARGE_BAR_BORDER,
                self.player.rect.y + AMMO_RECHARGE_BAR_BORDER +
                AMMO_RECHARGE_BAR_HEIGHT - progress_bar_height,
                AMMO_RECHARGE_BAR_WIDTH,
                progress_bar_height
            )

        """ Score rendering """
        renderText(
            self.display,
            "agencyfb",  
            100,
            str(self.score),
            WHITE,
            15,
            10
        )

        """ Finally update display """
        pygame.display.update()  # update the display
