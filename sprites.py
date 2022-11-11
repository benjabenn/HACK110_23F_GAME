import math
import random

import pygame
from pygame.locals import (K_DOWN, K_ESCAPE, K_LEFT, K_RIGHT, K_UP, KEYDOWN,
                           QUIT, RLEACCEL)

from constants import *


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

        spawn_point_right = (random.randint(SCREEN_WIDTH - 400, SCREEN_WIDTH -20), random.randint(0, SCREEN_HEIGHT))
        self.rect = self.surf.get_rect(center = spawn_point_right)

        self.speed = random.randint(3, 5)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class SeekingEnemy(pygame.sprite.Sprite):
    """Enemy that seeks and moves towards the player"""

    def __init__(self) -> None:
        super(SeekingEnemy, self).__init__()

        image_path = "assets/Enemy_Player.png"
        self.surf = pygame.image.load(image_path).convert()

        spawn_point_right = (random.randint(SCREEN_WIDTH - 400, SCREEN_WIDTH -20), random.randint(0, SCREEN_HEIGHT))
        self.rect = self.surf.get_rect(center = spawn_point_right)
        self.speed = ENEMY_SPEED

    def update(self, player, enemies):
        direction_x = - (self.rect.x - player.rect.x) 
        direction_y = - (self.rect.y - player.rect.y) 
        distance = math.hypot(direction_x, direction_y)
        direction_x /= distance
        direction_y /= distance
        direction_x *= self.speed
        direction_y *= self.speed

        other = pygame.sprite.GroupSingle()
        other.add(enemies)
        other.remove(self)
        if pygame.sprite.spritecollideany(self, other):
            self.rect.move_ip(-direction_x * 6, -direction_y * 6)
        else:
            self.rect.move_ip(direction_x, direction_y)

    def update_collision(self, player, enemies):
        direction_x = - (self.rect.x - player.rect.x) 
        direction_y = - (self.rect.y - player.rect.y) 
        distance = math.hypot(direction_x, direction_y)
        direction_x /= distance
        direction_y /= distance
        direction_x *= self.speed
        direction_y *= self.speed
        self.rect.move_ip(-direction_x, -direction_y)