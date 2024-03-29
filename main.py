import math
import random
import sys

import pygame

from game import Game
from obstacle import Cat, ObstacleFalling, Rock

from constants import (
    SCREEN_SIZE,
    INCREASE_SPEED_EVENT,
    SPEED_INCREASE_FACTOR,
    FPS,
    SCROLL_X,
    SPAWN_COOLDOWN,
    SPAWN_PROBABILITY_PER_SECOND, INITIAL_SPEED, INVICIBILITY,
)
from player import Player
from projectile import Projectile

pygame.init()
pygame.display.set_caption("Forest Jump")
screen = pygame.display.set_mode(SCREEN_SIZE)

# Import background and scale it to the screen size
background = pygame.image.load("assets/BackgroundFull.png")
background = pygame.transform.scale(background, SCREEN_SIZE)

#creation of the variable corresponding to the button to start the game
start_button = pygame.image.load("assets/start.png")
start_button = pygame.transform.scale(start_button, (400, 250))
start_button_rect = start_button.get_rect()
start_button_rect.x = math.ceil(screen.get_width() / 3.7)
start_button_rect.y = math.ceil(screen.get_height() / 3)

#creation of the variable corresponding to the main menu
menuperso = pygame.image.load("assets/forest-jump.png")
menuperso = pygame.transform.scale(menuperso,(560,200))
menuperso_rect = menuperso.get_rect()
menuperso_rect.x = math.ceil(screen.get_height()/4)
menuperso_rect.y = math.ceil(screen.get_width()/21)


running = True

# Load the game
game = Game()
clock = pygame.time.Clock()

obstacle_spawn_cooldown = False
obstacle_spawn_cooldown_counter = 0
spawn_probability = SPAWN_PROBABILITY_PER_SECOND / FPS

animation_cooldown_counter = 0

pygame.time.set_timer(INCREASE_SPEED_EVENT, int(1000 / FPS))

#load the sprites of the arrow, the different buttons
ARROW = pygame.image.load("assets/Arrow.png")
GAMEOVER = pygame.image.load("assets/gameover.png")
GAMEOVER = pygame.transform.scale(GAMEOVER, SCREEN_SIZE)
play_button = pygame.image.load("assets/play.png")
quit_button = pygame.image.load("assets/quit.png")

#load music and set it to infinity
music = 'assets/musique-jeu.mp3'
pygame.mixer.music.load(music)
pygame.mixer.music.play(-1)

# Loop to keep the window of the game open as long as the user close the game
while running:

    if game.start:
        # Apply backgrounds, one at the view of the player and another one next to it, necessary for the side scroller
        screen.blit(background, (SCROLL_X, 0))
        screen.blit(background, (SCROLL_X + SCREEN_SIZE[0], 0))

        POS = pygame.mouse.get_pos()
        CENTER = game.player.rect.center

        #get the angle of the throw
        get_angle = lambda pos1, pos2: math.atan(
            (pos1[1] - pos2[1]) / (pos1[0] - pos2[0])
         ) * (180 / math.pi)

        #calculate the angle of the throw of the shuriken according to the position of the mouse compared to the position of the player
        theta = -1 * (
            (0 if POS[0] > CENTER[0] else 180)
            if (POS[1] == CENTER[1])
            else (
                (90 if POS[1] > CENTER[1] else -90)
                if (POS[0] == CENTER[0])
                else -180 + get_angle(POS, CENTER)
                if CENTER[0] > POS[0]
                else get_angle(POS, CENTER)
            )
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                print("Closing the game")
            elif event.type == INCREASE_SPEED_EVENT:
                game.speed += SPEED_INCREASE_FACTOR

            #thrown of the shuriken according to the angle calculated
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game.projectiles.append(Projectile(theta, game))
                game.sound_manager.play('shuriken')

        # checks if an obstacle touches the player anf if so, the game is over
        if any(obstacle.rect.colliderect(game.player.rect) for obstacle in game.obstacles) and INVICIBILITY == False :
            showing_game_over = True
            screen.blit(GAMEOVER, (0, 0))
            # import of the replay button and quit button and their positions
            play_button = pygame.transform.scale(play_button, (200, 120))
            play_button_rect = play_button.get_rect()
            play_button_rect.x = math.ceil(screen.get_width() / 2)
            play_button_rect.y = math.ceil(screen.get_height() / 50)
            quit_button = pygame.transform.scale(quit_button, (200, 120))
            quit_button_rect = quit_button.get_rect()
            quit_button_rect.x = math.ceil(screen.get_width() / 4)
            quit_button_rect.y = math.ceil(screen.get_height() / 50)
            screen.blit(quit_button, quit_button_rect)
            screen.blit(play_button, play_button_rect)
            while showing_game_over :
                # Event that makes quit the game if we click on the quit button, or replay the game if we click on the replay button
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        showing_game_over = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if play_button_rect.collidepoint(event.pos):
                            #restart the game when the button play is cliked on the game over screen
                            showing_game_over= False
                            game.start = False
                            game.speed = INITIAL_SPEED
                            game.obstacles = []
                            game.projectiles = []
                        elif quit_button_rect.collidepoint(event.pos):
                            #quit the game when the quit button is pressed on the game over screen
                            running = False
                            showing_game_over = False
                pygame.display.flip()
            print("Closing the game")

        if not obstacle_spawn_cooldown:
            if random.random() < spawn_probability:
                obstacle_spawn_cooldown = True
                #apply the arrows on the screen randomly
                game.obstacles.append(ObstacleFalling(ARROW, game))
                if random.random() < 0.05:
                    # apply the cats or the rocks randomly
                    game.obstacles.append(Cat(game))
                else:
                    game.obstacles.append(Rock(game))

        else:
            obstacle_spawn_cooldown_counter += clock.get_time()
            if obstacle_spawn_cooldown_counter >= SPAWN_COOLDOWN:
                obstacle_spawn_cooldown = False
                obstacle_spawn_cooldown_counter = 0

        #animation of the ninja when she's running
        if not game.player.is_jumping and (
            animation_cooldown_counter >= (Player.N_SPRITES / FPS) * (6000 / game.speed)
        ):
            game.player.update()
            animation_cooldown_counter = 0

        else:
            animation_cooldown_counter += clock.get_time()

        keys = pygame.key.get_pressed()

        if game.player.is_jumping:
            game.player.continue_jump()

        # Verify if the player wants to jump by pressing a key
        elif keys[pygame.K_SPACE]:
            game.player.start_jump()
            game.sound_manager.play("jump")

        #update the obstacle on the screen
        for obstacle in game.obstacles:
            obstacle.update()

        #checks if an obstacle is failing down anf if so, when a projectile and an failling obstacles are intering in collison, remove them both
        for projectile in game.projectiles:
            projectile.update()
            for obstacle in game.obstacles:
                if isinstance(obstacle, ObstacleFalling) and projectile.rect.colliderect(
                    obstacle.rect
                ):
                    game.sound_manager.play('fleche2')
                    game.obstacles.remove(obstacle)
                    game.projectiles.remove(projectile)


        # Apply player on the screen
        screen.blit(game.player.image, game.player.rect)

        # Apply obstacles on the screen
        for obstacle in game.obstacles:
            screen.blit(obstacle.image, obstacle.rect)

        # Apply projectiles on the screen
        for projectile in game.projectiles:
            screen.blit(projectile.image, projectile.rect)



        # Screen scroller, when one of the first background isn't visible enough, its position is reseted
        #Moreover, the speed increases with time
        SCROLL_X -= game.speed
        if SCROLL_X <= -SCREEN_SIZE[0]:
            SCROLL_X = 0

        clock.tick(FPS)
        pygame.display.flip()
        pygame.display.update()
    else:
        # Apply the background, the start button and the logo on the screen
        screen.blit(background,(0,0))
        screen.blit(start_button, start_button_rect)
        screen.blit(menuperso, menuperso_rect)
        for event in pygame.event.get():
            # Event that makes quit the game if the window is closed, or start the game if we click on the play button
            if event.type == pygame.QUIT:
                running = False
                print("Closing the game")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    game.start = True
        clock.tick(FPS)
        pygame.display.flip()
        pygame.display.update()


pygame.quit()

