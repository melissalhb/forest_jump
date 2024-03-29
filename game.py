from constants import INITIAL_SPEED
from player import Player

# Class Game
from sounds import SoundManagement


class Game:
    def __init__(self):
        # define if the game started or not
        self.start = False
        self.speed = INITIAL_SPEED
        self.obstacles = []
        self.projectiles = []
        self.player = Player()
        # manage the sound
        self.sound_manager = SoundManagement()