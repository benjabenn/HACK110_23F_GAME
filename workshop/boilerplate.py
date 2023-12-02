import pygame, sys

# set screen size and then set screen
size = width, height = 640, 480
screen = pygame.display.set_mode(size)

# colors!
LIGHT_BLUE = (51, 153, 255)
RED = (240, 20, 20)

# start pygame
pygame.init()

# Set up clock for tickrate in loop
clock = pygame.time.Clock()

# set up bool variable for game loop
running = True

# create a rectangle 5 from the left
rectangle = pygame.Rect(5, height/2, 50, 50)

pygame.mouse.set_visible(False)

while running:
    # if the player clicks x or hits escape, end game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE): 
            running = False

    # Fill the game window with this color
    screen.fill(LIGHT_BLUE)

    # Draw a rectangle
    pygame.draw.rect(screen, RED, rectangle)

    rectangle.centerx, rectangle.centery = pygame.mouse.get_pos()

    # Update the display, is the equivalent of update() with no args
    pygame.display.flip()

    # Tick at constant frame rate
    clock.tick(60)