import os
import pygame
import sys
import models
import game
import score
from pygame_emojis import load_emoji

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 800
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 36
BORDER_RADIUS = 20
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WortEx Menu")

# Load the background image
path = os.path.join('data', 'space.jpg')
background_image = pygame.image.load(path)
# Resize the background image to fit the screen
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# darw text on the screen
def draw_text(text, size, color, x, y):
    font = pygame.font.SysFont("Arial", size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
    
# Menu loop
def main_menu():
    while True:
        # Set the background image
        screen.blit(background_image, (0, 0))

        # Event handling
        for event in pygame.event.get():
            # Quit event
            if event.type == pygame.QUIT:
                models.close()
                pygame.quit()
                sys.exit()
            # Mouse click event
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # Check if the mouse click is on the buttons
                # run the corresponding function
                if play_button_rect.collidepoint(x, y):
                    game.run()
                elif scoreboard_button_rect.collidepoint(x, y):
                    score.display_scoreboard()
                elif language_button_rect.collidepoint(x, y):
                    models.change_language()
                elif difficulty_button_rect.collidepoint(x, y):
                    game.change_difficulty()
                    
        # Draw title
        draw_text("WortEx",FONT_SIZE + 70, WHITE, WIDTH // 2, 120)

        # Draw Play button
        play_button_rect = pygame.draw.rect(screen, GREEN, (350, 290, 300, 70),border_radius=BORDER_RADIUS+5)
        draw_text("Play", FONT_SIZE+15, BLACK, WIDTH // 2, 325)
        
        # Game difficulty
        difficulty_button_rect = pygame.draw.rect(screen, WHITE, (300, 480, 400, 50),border_radius=BORDER_RADIUS)
        draw_text(f"Difficulty: ", FONT_SIZE, BLACK, WIDTH -580, 505)
        diff = game.difficulty
        diff_color = {"easy": BLACK, "medium": BLUE, "hard": (127,0,127), "extreme": RED } 
        draw_text(f"{game.difficulty}", FONT_SIZE, diff_color[diff], WIDTH -430, 505)
        diff_time = {"easy": 120, "medium": 60, "hard": 30, "extreme": 15}
        draw_text(f"{diff_time[diff]}s", 20, diff_color[diff], WIDTH -340, 505)
        
        # Draw Language button with text and flag
        language_button_rect = pygame.draw.rect(screen, WHITE, (300, 565, 400, 50), border_radius=BORDER_RADIUS)
        language = models.get_language()
        screen.blit(get_flag(language), (300 + 340, 565 ))  # Adjust the position as needed
        draw_text(f"Language:", FONT_SIZE, BLACK, WIDTH -600, 590)
        draw_text(f"{language}", FONT_SIZE, BLACK, WIDTH -445, 590)

        # Draw Scoreboard button
        scoreboard_button_rect = pygame.draw.rect(screen, WHITE, (300, 650, 400, 50),border_radius=BORDER_RADIUS)
        draw_text("Scoreboard", FONT_SIZE, BLACK, WIDTH // 2, 675)
        
        # Update the display
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

# Load the flag emoji       
def get_flag(language):
    # language flag dictionary
    dict = {'english': '🇬🇧', 'german': '🇩🇪'}
    flag_size = (50, 50)
    return load_emoji(dict[language], flag_size)

# Run the main menu
if __name__ == "__main__":
    main_menu()
