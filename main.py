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

# Create a LOT of sprites and a background surface
background = Background()
win_zone = win_zone()
player = Player()

# Create groups for them to go into
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
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, TIME_BETWEEN_ENEMIES, NUM_OF_ENEMIES)

# Set up clock for tickrate in loop
clock = pygame.time.Clock()

# It's as easy as this to add music!
pygame.mixer.music.load(MUSIC_FILENAME)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(1)


def main():
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
            elif event.type == ADDENEMY:
                # Create two new enemies every time the ADDENEMY event happens
                new_enemy = SeekingEnemy()
                new_enemy2 = LeftFlyingEnemy()
                enemies.add(new_enemy)
                enemies.add(new_enemy2)
                all_sprites.add(new_enemy)
                all_sprites.add(new_enemy2)

        # Initalize a dict storing all pressed keys
        pressed_keys = pygame.key.get_pressed()
        
        # Call the update method on player checking all pressed keys for True/False
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
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        # Check for any collisions between the player and any enemy
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

        # Update the display
        pygame.display.flip()

        # Tick at constant frame rate
        clock.tick(TICK_RATE)

if __name__ == '__main__':
    main()