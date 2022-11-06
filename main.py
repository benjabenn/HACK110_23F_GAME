"""PyGame project for Hack110 Advanced Topics in Games Workshop."""
"""Credit to Image by <a href="https://www.freepik.com/free-vector/american-football-field-top-view_11684074.htm#query=football%20field&position=0&from_view=keyword#position=0&query=football%20field">Freepik</a>"""
"""Credit to www.kenney.nl"""

# Import statements
import pygame
import random
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

SCREEN_WIDTH = 1760
SCREEN_HEIGHT = 990

class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super(Player, self).__init__()

        image_path = "assets/UNC_Player.png"
        self.surf = pygame.image.load(image_path).convert()
        # self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.speed = 2
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

        self.speed = random.randint(3, 5)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Setting up the window
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

player = Player()
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)



ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 100)

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
            new_enemy = LeftFlyingEnemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    # Initalize a dict storing all pressed keys
    pressed_keys = pygame.key.get_pressed()
    
    # Call the update method on player checking all pressed keys for True/False
    player.update(pressed_keys)
    
    # Updates enemy positions
    enemies.update()

    # Fill the background with white
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