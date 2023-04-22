import pygame

from constants import *


class Background():
    """Background surface, not a sprite since we don't need any collision logic."""

    def __init__(self):
        # Initialize the super class
        super(Background, self).__init__()

        # Create the surface that is the football field by using the load method of image, then converting it
        surface = pygame.image.load(BACKGROUND_FILENAME).convert()
        
        # Scale it to the desired size, I made it the same height as the screen but 3x as long to make a sizeable
        # football field to scroll across the screen
        self.surf = pygame.transform.scale(surface, (BACKGROUND_WIDTH, BACKGROUND_HEIGHT))
        
        # Set the x and y to start at 0
        self.x = 0
        self.y = 0
        
        # Move at the speed set in the constants file
        self.speed = BACKGROUND_SPEED
        
    def update(self):
        # Every update move the x in the negative direction
        self.x -= self.speed
            
    def render(self, screen):
        # We can have a render method here since its not gonna be in the sprite group
        screen.blit(self.surf, (self.x, self.y))


class win_zone(pygame.sprite.Sprite):
    """A long transparent bar that moves at the same speed as the background"""

    def __init__(self):
        # Init the super class
        super(win_zone, self).__init__()

        # Create a plain black surface, remove the black color to make it invisible
        surface = pygame.surface.Surface((20, SCREEN_HEIGHT))
        surface.set_colorkey((0, 0, 0))
        self.surf = surface

        # Create the spawn point in the end zone (kinda eyeballed it but didn't use magic numbers at least!)
        spawn_point = (BACKGROUND_WIDTH - (BACKGROUND_WIDTH // 12), SCREEN_HEIGHT / 2)
        self.rect = self.surf.get_rect(center = spawn_point)

        # Set speed to constant, same as the background
        self.speed = BACKGROUND_SPEED
        
    def update(self):
        # Just move it to the left at the speed in the constants file
        self.rect.move_ip(-self.speed, 0)