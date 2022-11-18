import math
import random

import pygame
from pygame.locals import (K_DOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_UP, KEYDOWN,
                           QUIT, RLEACCEL)

from constants import *

# from random import randint, random




class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super(Player, self).__init__()

        image_path = "assets/UNC_Player.png"
        self.surf = pygame.image.load(image_path).convert()
        # self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.speed = PLAYER_SPEED
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys) -> None:
        # Checks keys bool value, if True then it moves
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.speed)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

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
        super(LeftFlyingEnemy, self).__init__()
        
        image_path = "assets/Enemy_Player.png"
        self.surf = pygame.image.load(image_path).convert()
        # self.surf.set_colorkey((255, 255, 255), RLEACCEL)

        spawn_point_right = (random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100), random.randint(0, SCREEN_HEIGHT))
        self.rect = self.surf.get_rect(center = spawn_point_right)

        self.speed = random.randint(1, 3)

    def update(self, player, enemies):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class SeekingEnemy(pygame.sprite.Sprite):
    """Enemy that seeks and moves towards the player"""

    def __init__(self) -> None:
        super(SeekingEnemy, self).__init__()

        image_path = "assets/Enemy_Player.png"
        self.surf = pygame.image.load(image_path).convert()

        spawn_point_right = (random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100), random.randint(0, SCREEN_HEIGHT))
        self.rect = self.surf.get_rect(center = spawn_point_right)
        self.speed = ENEMY_SPEED
        self.collided = False

    def update(self, player, enemies):
        direction_x = - (self.rect.x - player.rect.x) 
        direction_y = - (self.rect.y - player.rect.y) 
        distance = math.hypot(direction_x, direction_y)
        direction_x /= distance
        direction_y /= distance
        direction_x *= self.speed
        direction_y *= self.speed

        CHECK_COLLISIONS = pygame.USEREVENT + 2
        pygame.time.set_timer(CHECK_COLLISIONS, 1000)

        if self.is_collided(enemies):
            self.rect.move_ip(-direction_x * 2 * (random.random() - 0.5), -direction_y * 2 * (random.random() - 0.5))
        else: 
            self.rect.move_ip(direction_x, direction_y)

    # def update_collision(self, player, enemies):
    #     direction_x = - (self.rect.x - player.rect.x) 
    #     direction_y = - (self.rect.y - player.rect.y) 
    #     distance = math.hypot(direction_x, direction_y)
    #     direction_x /= distance
    #     direction_y /= distance
    #     direction_x *= self.speed
    #     direction_y *= self.speed
    #     self.rect.move_ip(-direction_x, -direction_y)

    def is_collided(self, enemies) -> bool:
        other = pygame.sprite.Group()
        other.add(enemies)
        other.remove(self)
        return pygame.sprite.spritecollideany(self, other)