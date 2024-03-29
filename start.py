# this file is the sarting animation for the game
#after its done it will load the main menu
import os
import time
import pygame
import sys
import math
import random
import menu

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 800
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WortEx")

# Load the background image
path = os.path.join('data', 'background.jpg')
background_image = pygame.image.load(path)
# Resize the background image to fit the screen
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Particle class
class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        radius = random.uniform(5,400)
        scale = (radius -5 * (255//400)) % 255
        self.image = pygame.Surface((5, 5))
        self.image.fill((scale, 255-scale, 255))
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = 0
        self.radius = radius
        max_speed = 15 - radius**2 // 10000
        self.speed = random.uniform(0.5*max_speed, max_speed)

    def update(self):
        self.angle += self.speed
        x = WIDTH // 2 + int(self.radius * math.cos(math.radians(self.angle)))
        y = HEIGHT // 2 + int(self.radius * math.sin(math.radians(self.angle)))
        self.rect.center = (x, y)

# Group for particles
all_sprites = pygame.sprite.Group()

# Create particles
num_particles = 5000
for _ in range(num_particles):
    particle = Particle(WIDTH // 2, HEIGHT // 2)
    all_sprites.add(particle)


clock = pygame.time.Clock()
running = True
start_time = time.time()
# Main loop
while running:
    # Event handling
    for event in pygame.event.get():
        # Quit event
        if event.type == pygame.QUIT:
            running = False
    # if time is up or particles are less than 40
    if len(all_sprites.sprites()) < 40:
        # load the main menu
        menu.main_menu()
        
    # Update particles
    all_sprites.update()

    # Draw background
    screen.blit(background_image, (0, 0))

    # Draw particles
    all_sprites.draw(screen)
    # remove 40 random particles
    for i in range(40):
        particle= random.choice(all_sprites.sprites())
        all_sprites.remove(particle)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
    

# Quit Pygame
pygame.quit()
sys.exit()