import pygame

from constants import GRAVITY, JUMP_HEIGHT, START_Y


class Player(pygame.sprite.Sprite):
    N_SPRITES = 8

    #import the sprites of the running and jumping animation of the ninja
    SPRITES = [
        pygame.transform.scale(
            sprite, (sprite.get_width() / 1.2, sprite.get_height() / 1.2)
        )
        for sprite in [
            pygame.image.load(f"assets/Run{i}.png") for i in range(N_SPRITES)
        ]
    ]

    #initizialize the starting position
    START_POS = [50, START_Y - SPRITES[0].get_height()]
    START_POS_JUMP_Y = START_Y - pygame.image.load(f"assets/Jump0.png").get_height()

    def __init__(self):
        super().__init__()
        self.is_jumping = False
        self.attack = 1

        self.velocity_y = 0

        self.current_sprite = 0
        self.image = Player.SPRITES[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.x = Player.START_POS[0]
        self.rect.y = Player.START_POS[1]

    #animations of the ninja with the sprites
    def update(self):
        self.current_sprite += 1
        if self.current_sprite >= len(Player.SPRITES):
            self.current_sprite = 0
        self.image = Player.SPRITES[self.current_sprite]

    # Method to call as soon as we press space that will start the jump
    def start_jump(self):
        self.image = pygame.image.load(f"assets/Jump0.png")
        self.rect.y = Player.START_POS_JUMP_Y
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = JUMP_HEIGHT

    def continue_jump(self):
        self.rect.y -= self.velocity_y
        self.velocity_y -= GRAVITY

        #apply the sprite of the jump animation when the ninja is jumping
        if self.velocity_y < 0:
            self.image = pygame.image.load(f"assets/Jump1.png")

        if self.rect.y >= Player.START_POS_JUMP_Y:
            self.rect.y = Player.START_POS[1]

            self.current_sprite = 0
            self.image = Player.SPRITES[self.current_sprite]

            self.velocity_y = 0
            self.is_jumping = False
