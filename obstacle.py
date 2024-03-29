import pygame
import random
from constants import GRAVITY, SCREEN_SIZE, START_Y

# class for all the obstacles
class Obstacle (pygame.sprite.Sprite):
    def __init__(self, image, game):
        super().__init__()

        self.image = image
        self.game = game

        # Rectangle coordinates of the image
        self.rect = self.image.get_rect()

        # The x coordinates of the obstacle to the screen width
        self.rect.x = SCREEN_SIZE[0]
        self.rect.y = START_Y - self.image.get_height()

    def update(self):
        # Move the obstacle across the screen
        self.rect.x -= self.game.speed

        # Remove the obstacle soon as the screen disappear
        if self.rect.x < -self.rect.width:
            self.game.obstacles.pop(self.game.obstacles.index(self))

# class of the arrows
class ObstacleFalling(Obstacle):
    def __init__(self, image, game):
        super().__init__(image, game)
        self.rect.x = random.randint(0, SCREEN_SIZE[0])
        self.rect.y = -self.rect.height

        self.volacity_x = random.randint(-10, 10)
        self.volacity_y = 0

    def update(self):
        # Move the obstacle across the screen
        self.rect.x -= self.game.speed + self.volacity_x
        self.rect.y += self.volacity_y
        self.volacity_y += GRAVITY

        # Remove the obstacle soon as the screen disappear
        if self.rect.x < -self.rect.width or self.rect.y > SCREEN_SIZE[1]:
            self.game.obstacles.pop(self.game.obstacles.index(self))


class Cat(Obstacle):
    N_CATS = 1                                                                  # N_CATS= 2
    CATS = [
        #import the sprites of the ca ts
        pygame.transform.scale(
            sprite, (sprite.get_width() * 2, sprite.get_height() * 2)
        )
        for sprite in [pygame.image.load(f"assets/Cat{i}.png") for i in range(N_CATS)]
    ]

    def __init__(self, obstacles):
        super().__init__(Cat.CATS[random.randrange(Cat.N_CATS)], obstacles)


class Rock(Obstacle):
    N_ROCKS = 1                                                                # N_ROCKS= 3
    ROCKS = [
        #import the sprites of the rocks
        pygame.transform.scale(
            sprite, (sprite.get_width() * 1.2, sprite.get_height() * 1.2)
        )
        for sprite in [pygame.image.load(f"assets/Rock{i}.png") for i in range(N_ROCKS)]
    ]

    def __init__(self, obstacles):
        super().__init__(Rock.ROCKS[random.randrange(Rock.N_ROCKS)], obstacles)
