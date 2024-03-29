import pygame

#class of all the sound effect
class SoundManagement :
    def __init__(self):
        # list of all the sounds that are use in our game
        self.sounds = {
            'shuriken': pygame.mixer.Sound("assets/shuriken_sound.mp3"),
            'jump': pygame.mixer.Sound("assets/jump.mp3"),
            'music': pygame.mixer.Sound("assets/Katana.mp3"),
            'fleche2': pygame.mixer.Sound("assets/fleche2.mp3")

        }
    def play(self,name):
        # method used to play a sound in the library define above
        self.sounds[name].play()