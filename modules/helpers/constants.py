""" General settings """

WINDOW_TITLE = "Game Title Here"  # title of the game

FPS = 60  # frames per second of game


""" Display settings """

DISPLAY_WIDTH = 1200  # display width in px
DISPLAY_HEIGHT = 800  # display height in px

DISPLAY_SIZE = (  # tuple of display sizes
    DISPLAY_WIDTH,
    DISPLAY_HEIGHT
)

DISPLAY_CENTER = (  # position of center of display
    DISPLAY_WIDTH / 2,
    DISPLAY_HEIGHT / 2
)

""" World settings """

FRICTION = 0.99  # how fast objects slow down horizontally
GRAVITY = 0.29  # how fast objects fall


""" Bullet settings """

BULLET_MAP = {
    1: 0,  # left click
    3: 1,  # right click
}

# [Main bullet, Alternate bullet]

BULLET_SIZE = [5, 10]
BULLET_SHAPE = [
    (BULLET_SIZE[0], BULLET_SIZE[0]),
    (BULLET_SIZE[1], BULLET_SIZE[1])
]
BULLET_OFFSET = [
    (BULLET_SIZE[0] / 2, BULLET_SIZE[0] / 2),
    (BULLET_SIZE[1] / 2, BULLET_SIZE[1] / 2)
]
BULLET_VELOCITY = [15, 7]
BULLET_COOLDOWN = [20, 300]

RECOIL = [15, 23]



AMMO_RECHARGE_BAR_HEIGHT = 40
AMMO_RECHARGE_BAR_WIDTH = 8
AMMO_RECHARGE_BAR_BORDER = 4  # thickness of ammo bar borders
AMMO_RECHARGE_BAR_OFFSET = 30  # distance of ammo bar from player

HEALTH_BAR_WIDTH = 100
HEALTH_BAR_HEIGHT = 10
HEALTH_BAR_BORDER = 5  # thickness of health bar borders
HEALTH_BAR_OFFSET = 35  # distance of health bar from player

PLANET_MAX_HP = 300
PLANET_HP_BAR_WIDTH = 10
PLANET_HP_BAR_HEIGHT = 300


""" Player settings """

PLAYER_SIZE = 30  # size of player

PLAYER_SHAPE = (  # the player background is a square
    PLAYER_SIZE,
    PLAYER_SIZE
)

PLAYER_POINTS = [  # points that make the shape of the player
    (  # top left point
        0,
        0
    ),

    (  # arrow point
        PLAYER_SIZE,
        PLAYER_SIZE / 2

    ),

    (  # bottom left point
        0,
        PLAYER_SIZE
    ),

    (  # bottom left point
        PLAYER_SIZE / 8 * 3,
        PLAYER_SIZE / 2,
    )
]

PLAYER_OFFSET = (  # halves the player size to get the center point
    PLAYER_SIZE / 2,
    PLAYER_SIZE / 2
)

PLAYER_SPAWN_LOCATION = (  # sets the location of the player spawn
    DISPLAY_CENTER[0] - PLAYER_OFFSET[0],
    DISPLAY_CENTER[1] - PLAYER_OFFSET[1],
)

PLAYER_TERMINAL_VELOCITY = 30  # max speed of player

PLAYER_FLOOR_BOUNCE = -15  # velocity of player bouncing off floor

PLAYER_MAX_HEALTH = 100  # maximum health of player
PLAYER_RECEIVE_DAMAGE = 10  # damage taken by player
PLAYER_REGEN = 1  # health regen after destroying blocks

PLAYER_COLLIDE_X_SLOW_DOWN_MULTIPLIER = -.9 #multiplier to slow down when colliding (x vel)
PLAYER_COLLIDE_Y_SLOW_DOWN_MULTIPLIER = -.7 #multiplier to slow down when colliding (y vel)

""" Chunk settings """

CHUNKSIZE = 40
SPAWN_RATE = 10

""" Spark settings """

SPARK_SCALE = 3
SPARK_SPEED = [20, 60]
SPARK_SPREAD = 13
SPARK_FALL_MULTIPLIER = 0.25
SPARK_DECAY_MULTIPLIER = 10


""" Particle settings """

PARTICLE_SPREAD = 12
PARTICLE_SIZE = [5, 10]
PARTICLE_DECAY_SPEED = 0.1


""" Overlay settings """

AMMO_RECHARGE_BAR_HEIGHT = 40
AMMO_RECHARGE_BAR_WIDTH = 8
AMMO_RECHARGE_BAR_BORDER = 4  # thickness of ammo bar borders
AMMO_RECHARGE_BAR_OFFSET = 30  # distance of ammo bar from player

HEALTH_BAR_WIDTH = 100
HEALTH_BAR_HEIGHT = 10
HEALTH_BAR_BORDER = 5  # thickness of health bar borders
HEALTH_BAR_OFFSET = 35  # distance of health bar from player


""" Colors """

BLACK = (0, 0, 0)
BLACKGRAY = (63, 63, 63)
GRAY = (127, 127, 127)
WHITEGRAY = (191, 191, 191)
WHITE = (255, 255, 255)
