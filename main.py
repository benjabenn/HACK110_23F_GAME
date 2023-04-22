"""PyGame project for Hack110 Advanced Topics in Games Workshop."""

# Import statements
import pygame
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT

from background import *
# Import from our other modules, use * to get everything (usually not a 
# good idea but since we made the files and we know what's in it it's okay)
from constants import *
from sprites import *

# Initialize pygame
pygame.init()

# Setting up the window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Create some sprites and a background surface by calling their class constructors
background = Background()
win_zone = win_zone()
player = Player()

# Create groups for them to go into by calling the Group constructor, 
# using the GroupSingle for the win_zone since there is only one
# Pygame groups documentation at this link!
# https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Group
# Simple explanation from RealPython (a great resource for lots of pygame stuff!) at this link!
# https://realpython.com/lessons/sprite-groups/
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
win_zone_group = pygame.sprite.GroupSingle()

# Add sprites to their appropriate groups
all_sprites.add(player)
all_sprites.add(win_zone)
win_zone_group.add(win_zone)

# Create an event! pygame events have numbers, we want to put one 
# at the end of the list of numbers. After that set a timer to loop the 
# event, with args for ms between actions and number of loops
# Go here for more information!
# https://coderslegacy.com/python/pygame-userevents/
ADDENEMY = pygame.USEREVENT
pygame.time.set_timer(ADDENEMY, TIME_BETWEEN_ENEMIES, NUM_OF_ENEMIES)

# Set up clock for tickrate in loop
clock = pygame.time.Clock()

# It's as easy as this to add music!
pygame.mixer.music.load(MUSIC_FILENAME)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(1)

def main():
    # Set a running bool variable to True, can be set to False at any time to end the game loop
    running = True
    # Main loop
    while running:
        # Event queue
        for event in pygame.event.get():
            # Stop loop when X button is hit
            if event.type == QUIT:
                running = False
            # Check for KEYDOWN events
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            # Create two new enemies every time the ADDENEMY event happens
            # We defined the ADDENEMY event earlier in one of the slots given to us by pygame
            # The other slots are taken up by built-in events like KEYDOWN, QUIT, etc..
            # One just flies left, the other seeks the player out       
            elif event.type == ADDENEMY:
                new_enemy = SeekingEnemy()
                new_enemy2 = LeftFlyingEnemy()
                # Add them to their groups
                enemies.add(new_enemy)
                enemies.add(new_enemy2)
                all_sprites.add(new_enemy)
                all_sprites.add(new_enemy2)

        # Initalize a dict storing all pressed keys by calling the get_pressed() function that gets the state of all
        # keyboard buttons 
        # Documentation: https://www.pygame.org/docs/ref/key.html#pygame.key.get_pressed
        pressed_keys = pygame.key.get_pressed()
        
        # Call the update method on player by passing the pressed keys dict and within the 
        # update method we will check relevant pressed keys for True/False
        player.update(pressed_keys)

        # Updates enemy positions
        enemies.update(player, enemies)

        # Fill the screen with our background green (same as in the background img)
        screen.fill((47, 179, 78))

        # Update the background and render separately because its not in the sprite group
        background.update()
        background.render(screen)

        # Update the win_zone sprite
        win_zone.update()

        # Draw all of the sprites using a for loop
        # Another quick RealPython article for reference!
        # https://realpython.com/lessons/using-blit-and-flip/
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # Check for any collisions between the player and any enemy
        # Collisions are a difficult topic, the links below can help!
        # Documentation: https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.spritecollideany
        # Guide: https://coderslegacy.com/python/pygame-sprite-collision-detection/#:~:text=Sprite%20Collision%20Functions
        if pygame.sprite.spritecollideany(player, enemies):
            # If so, kill player and end game (end loop)
            player.kill()
            print("You got tackled!")
            running = False

        # Check for collisions with the end zone, if so, win the game!
        if pygame.sprite.spritecollideany(player, win_zone_group):
            print("You won!")
            pygame.mixer.music.load(WIN_SOUND_FILENAME)
            pygame.mixer.music.play(1)
            pygame.mixer.music.set_volume(1)
            pygame.time.delay(3000)
            running = False

        # Update the display, is the equivalent of update() with no args
        pygame.display.flip()

        # Tick at constant frame rate
        clock.tick(TICK_RATE)

if __name__ == '__main__':
    main()