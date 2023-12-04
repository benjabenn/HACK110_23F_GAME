import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Text in Pygame')

# Set up colors
black = (0, 0, 0)
white = (255, 255, 255)

# Set up fonts
font = pygame.font.Font(None, 36)  # None means default font, 36 is the font size

# Render text onto a surface
text_surface = font.render('Hello, Pygame!', True, white, black)

# Get the rectangle of the text surface
text_rect = text_surface.get_rect()
text_rect.center = (200, 150)  # Position of the text

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color
    screen.fill(black)

    # Blit the text onto the screen
    screen.blit(text_surface, text_rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame properly
pygame.quit()
sys.exit()
