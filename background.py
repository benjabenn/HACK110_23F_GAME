import pygame
from constants import *

class Background():
    """Background surface, not a sprite since we don't need any collision logic."""

    def __init__(self):
        super(Background, self).__init__()
        surface = pygame.image.load(BACKGROUND_FILENAME).convert()
        self.surf = pygame.transform.scale(surface, (BACKGROUND_WIDTH, BACKGROUND_HEIGHT))
        
        self.x = 0
        self.y = 0
        
        self.speed = BACKGROUND_SPEED
        
    def update(self):
        self.x -= self.speed
            
    def render(self, screen):
        screen.blit(self.surf, (self.x, self.y))


class win_zone(pygame.sprite.Sprite):
    def __init__(self):
        super(win_zone, self).__init__()
        surface = pygame.surface.Surface((20, SCREEN_HEIGHT))
        surface.set_colorkey((0, 0, 0))
        self.surf = surface
        spawn_point = (BACKGROUND_WIDTH - (BACKGROUND_WIDTH // 12), SCREEN_HEIGHT / 2)
        self.rect = self.surf.get_rect(center = spawn_point)
        self.speed = BACKGROUND_SPEED
        
    def update(self):
        self.rect.move_ip(-self.speed, 0)