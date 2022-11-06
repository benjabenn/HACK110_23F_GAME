"""PyGame project for Hack110 Advanced Topics in Games Workshop."""

# Import statements
import pygame
import random
from constants import *
from sprites import *
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Initialize pygame
pygame.init()


# Setting up the window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

player = Player()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250, 11)

clock = pygame.time.Clock()

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
            # Create a new enemy
            # new_enemy = LeftFlyingEnemy()
            new_enemy = SeekingEnemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    # Initalize a dict storing all pressed keys
    pressed_keys = pygame.key.get_pressed()
    
    # Call the update method on player checking all pressed keys for True/False
    player.update(pressed_keys)
    
    # Updates enemy positions
    enemies.update(player)

    # Fill the background with black
    screen.fill((0, 0, 0))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # Check for any collisions between the player and any enemy
    if pygame.sprite.spritecollideany(player, enemies):
        # If so, kill player and end game (end loop)
        player.kill()
        running = False

    # Update the display
    pygame.display.flip()

    clock.tick(144)