import pygame
import math
import numpy

from constants import (
    FPS,
    GRAVITY,
    PROJECTILE_ROTATION_PER_SECOND,
    PROJECTILE_SPEED,
    START_Y,
)


class Projectile(pygame.sprite.Sprite):
    IMAGE = pygame.image.load("assets/Shuriken.png")
    ROTATION_PER_FRAME = PROJECTILE_ROTATION_PER_SECOND / FPS

    def __init__(self, angle, game):
        super().__init__()
        self.image = Projectile.IMAGE
        self.velocity = [
            # To have get the velocity of the shurikens
            PROJECTILE_SPEED * math.cos(angle * math.pi / 170),
            PROJECTILE_SPEED * math.sin(angle * math.pi / 170),
        ]

        self.game = game
        self.rect = self.image.get_rect()
        self.origin_image = self.image

        # Initialize the position of the throw
        self.rect.x = game.player.rect.x + 20
        self.rect.y = game.player.rect.y + 20

        self.angle = 0

    # Change the position of shurikens (movement) by adding current position by horizental velocity
    def update(self):
        self.rotate()
        self.rect.x += self.velocity[0]
        self.rect.y -= self.velocity[1]

        self.velocity[1] -= GRAVITY
        # Remove the sprite as soon as it comes out of the screen
        if self.rect.y >= START_Y:
            self.game.projectiles.remove(self)


    #Function that allows to rotate the shurikens
    def rotate(self):
        self.angle += -20
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        self.rect = self.image.get_rect(center = self.rect.center)