import math
import random

import pygame
from pygame.locals import K_DOWN, K_LEFT, K_RIGHT, K_UP, RLEACCEL

from constants import *

# Learn more about pygame sprites below!
# Documentation: https://www.pygame.org/docs/ref/sprite.html
# Guide: http://programarcadegames.com/index.php?chapter=introduction_to_sprites&lang=en
# The guide above uses a slightly different method for creating sprites than I did (without using surf)
# It's also a pretty long guide so don't worry about reading all of it
class Player(pygame.sprite.Sprite):
    """The user controlled player."""
    
    def __init__(self) -> None:
        # Super class initialization of the sprite
        super(Player, self).__init__()

        # Set the players image, convert, set the surf to be equal to it, 
        # then remove the black background (you won't have to do this if you have a transparent image)
        self.surf = pygame.image.load(PLAYER_FILENAME).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)

        # Set the speed to the constant
        self.speed = PLAYER_SPEED

        # Get the rect from the surface
        # Spawn in the center, a little from the left
        # center = (x, y) specifies an (x, y) coordinate for the center of the sprite to spawn at
        self.rect = self.surf.get_rect(center = (50, SCREEN_HEIGHT / 2))

    def update(self, pressed_keys) -> None:
        # Checks keys bool value with subscription notation, if True then it moves
        # pressed_keys is a dict that looks kinda like {K_UP: True, K_DOWN : False, K_LEFT : False, K_RIGHT : False}
        # We check the value associated with the key (which is a literal key on the keyboard) to see if true or false
        # It is true when it is being pressed, so then we update in the appropriate direction
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.speed)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

        # Checks the bounds, if player reaches the bounds then hold player in place
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class LeftFlyingEnemy(pygame.sprite.Sprite):
    """Enemy class"""

    def __init__(self) -> None:
        # Super class initialization of the sprite
        super(LeftFlyingEnemy, self).__init__()
        
        # Create the image for the enemy to be, convert it
        self.surf = pygame.image.load(ENEMY_FILENAME).convert()

        # Remove the black background
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)

        # Spawn them slightly off of the screen
        spawn_point_right = (random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100), random.randint(0, SCREEN_HEIGHT))

        # center = (x, y) specifies an (x, y) coordinate for the center of the sprite to spawn at
        self.rect = self.surf.get_rect(center = spawn_point_right)

        # Set their speed to the constant from the constants file
        self.speed = ENEMY_SPEED

    def update(self, player, enemies):
        """Fly to the left."""
        # If it is currently colliding with another enemy, freak out a bit like an angry wasp
        if self.is_collided(enemies):
            self.rect.move_ip(-self.speed * 2 * (random.random() - 0.5), -self.speed * 2 * (random.random() - 0.5))
        # Else just move to the left normally
        else:
            self.rect.move_ip(-self.speed, 0)
        # When the enemies get to the end, make them disappear with the sprite kill() method
        if self.rect.right < 0:
            self.kill()

    def is_collided(self, enemies) -> bool:
        """Test to see if this enemy is colliding with any other enemy in the group."""
        # Create a group with all enemies, remove self to only test collisions with other enemies
        other = pygame.sprite.Group()
        other.add(enemies)
        other.remove(self)
        return pygame.sprite.spritecollideany(self, other)

class SeekingEnemy(pygame.sprite.Sprite):
    """Enemy that seeks and moves towards the player"""

    def __init__(self) -> None:
        # Super class initialization of the sprite
        super(SeekingEnemy, self).__init__()

        # Create the image for the enemy to be, convert it
        image_path = ENEMY_FILENAME
        self.surf = pygame.image.load(image_path).convert()

        # Remove the black background
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)

        # Spawn them slightly off of the screen
        spawn_point_right = (random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100), random.randint(0, SCREEN_HEIGHT))
        self.rect = self.surf.get_rect(center = spawn_point_right)

        # Set their speed to the constant from the constants file
        self.speed = ENEMY_SPEED

    def update(self, player, enemies):
        """We'll use a bit of vector math to make these enemies "seek" the player"""
        # First calculate the distance to the player, x and y components form a vector
        direction_x = (player.rect.x - self.rect.x) 
        direction_y = (player.rect.y - self.rect.y) 
        # Then find the total distance with the distance formula ("hypot" short for hypotenuse)
        distance = math.hypot(direction_x, direction_y)
        # Divide by distance to get a unit vector
        direction_x /= distance
        direction_y /= distance
        # Multiply by whatever speed you set!
        # NOTE: The move_ip method doesn't seem to like values < 1 so the 
        # speed has to be at least 2-3 for the enemies to move
        direction_x *= self.speed
        direction_y *= self.speed

        # If it is currently colliding with another enemy, 
        # freak out a bit like an angry wasp
        if self.is_collided(enemies):
            self.rect.move_ip(-direction_x * 2 * (random.random() - 0.5), -direction_y * 2 * (random.random() - 0.5))
        else: 
            self.rect.move_ip(direction_x, direction_y)

    def is_collided(self, enemies) -> bool:
        """Test to see if this enemy is colliding with any other enemy in the group."""
        # Create a group with all enemies, remove self to only test collisions with other enemies
        other = pygame.sprite.Group()
        other.add(enemies)
        other.remove(self)
        return pygame.sprite.spritecollideany(self, other)