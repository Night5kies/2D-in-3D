import math
import random
from modules.helpers.constants import *

def find_distance(mousePos, spritePos):
    # finds the horizontal distance between the two points
    xDistance = mousePos[0] - spritePos[0]
    # finds the vertical distance between the two points
    yDistance = mousePos[1] - spritePos[1]

    return (xDistance, yDistance)


def point_in_direction(mousePos, spritePos):
    distance = find_distance(mousePos, spritePos)

    # finds the angle in radians
    radians = math.atan2(distance[1], distance[0])
    degrees = math.degrees(radians)  # converts radians to degrees

    return degrees  # returns calculated degrees


def move(mousePos, spritePos, velocity):
    distance = find_distance(mousePos, spritePos)

    # divides velocity by an approximation of the distance velocity will be multiplied by
    velocity_distance = velocity / math.hypot(distance[1], distance[0])

    calculated_velocity = (  # calculates the desired velocities to result in a hypotenuse velocity of the input parameter
        distance[0] * velocity_distance,
        distance[1] * velocity_distance,
    )

    return calculated_velocity

def collisionCheck(blockRect, rect):
    collisionTypes = {'top': False, 'bottom': False, 'right': False, 'left': False}
    if rect.x <= blockRect.x:
        collisionTypes['right'] = True
    elif rect.x >= blockRect.x + CHUNKSIZE/2:
        collisionTypes['left'] = True
    if rect.y <= blockRect.y:
        collisionTypes['bottom'] = True
    elif rect.y >= blockRect.y + CHUNKSIZE/2:
        collisionTypes['top'] = True
    collisionTypes['top'], collisionTypes['right'] = oneDirection(collisionTypes['top'], collisionTypes['right'],
                                                                  rect, blockRect)
    collisionTypes['top'], collisionTypes['left'] = oneDirection(collisionTypes['top'], collisionTypes['left'],
                                                                 rect, blockRect)
    collisionTypes['bottom'], collisionTypes['right'] = oneDirection(collisionTypes['bottom'], collisionTypes['right'],
                                                                     rect, blockRect)
    collisionTypes['bottom'], collisionTypes['left'] = oneDirection(collisionTypes['bottom'], collisionTypes['left'],
                                                                    rect, blockRect)

    return collisionTypes

def oneDirection(ver, hor, rect, blockRect):
    if ver and hor:
        if rect.x > blockRect.x + CHUNKSIZE/2:
            distancex = blockRect.x + CHUNKSIZE - rect.x - rect[2]
        else:
            distancex = -(blockRect.x - rect.x + rect[2])
        if rect.y > blockRect.y + CHUNKSIZE/2:
            distancey = blockRect.y + CHUNKSIZE - rect.y - rect[3]
        else:
            distancey = -(blockRect.y - rect.y + rect[3])

        if distancex > distancey:
            hor = False
        elif distancey > distancex:
            ver = False
        elif distancex == distancey:
            coin = random.randint(1,2)
            if coin == 1:
                ver = False
            else:
                hor = False

    return ver, hor
