import pygame

INVICIBILITY = False

SCREEN_SIZE = (800, 600)
START_Y = 530
GRAVITY = 0.6

INITIAL_SPEED = 5
JUMP_HEIGHT = 15

SCROLL_X = 0
FPS = 60

SPEED_INCREASE_FACTOR = 0.0002
SPAWN_COOLDOWN = 1000
SPAWN_PROBABILITY_PER_SECOND = 0.4
PROJECTILE_ROTATION_PER_SECOND = 2
PROJECTILE_SPEED = 20

INCREASE_SPEED_EVENT = pygame.USEREVENT
