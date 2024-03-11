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

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WortExMenu")

# Functions
def draw_text(text, size, color, x, y):
    font = pygame.font.SysFont("Arial", size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def run_game():
    game.run()
    

def run_scoreboard():
    score.display_scoreboard()
    
# Menu loop
def main_menu():
    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                models.close()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if play_button_rect.collidepoint(x, y):
                    run_game()
                elif scoreboard_button_rect.collidepoint(x, y):
                    run_scoreboard()
                elif language_button_rect.collidepoint(x, y):
                    models.change_language()
                    
        # Draw title
        draw_text("WortEx",FONT_SIZE * 2, WHITE, WIDTH // 2, 200)

        # Draw Play button
        play_button_rect = pygame.draw.rect(screen, WHITE, (300, 350, 400, 50),border_radius=BORDER_RADIUS)
        draw_text("Play", FONT_SIZE, BLACK, WIDTH // 2, 375)

        # Draw Scoreboard button
        scoreboard_button_rect = pygame.draw.rect(screen, WHITE, (300, 450, 400, 50),border_radius=BORDER_RADIUS)
        draw_text("Scoreboard", FONT_SIZE, BLACK, WIDTH // 2, 475)
        
        # make laguage picker
        #language_button_rect = pygame.draw.rect(screen, WHITE, (300, 550, 400, 50),border_radius=BORDER_RADIUS)
        #draw_text(f"Language: {models.get_language()}", FONT_SIZE, BLACK, WIDTH // 2, 575)
        
        

        
        # Draw Language button with text and flag
        language_button_rect = pygame.draw.rect(screen, WHITE, (300, 550, 400, 50), border_radius=BORDER_RADIUS)
        language = models.get_language()
        screen.blit(get_flag(language), (300 + 340, 550 ))  # Adjust the position as needed
        draw_text(f"Language:", FONT_SIZE, BLACK, WIDTH -600, 575)
        draw_text(f"{language}", FONT_SIZE, BLACK, WIDTH -445, 575)


        pygame.display.flip()
        pygame.time.Clock().tick(FPS)
        
def get_flag(language):
    dict = {'english': '🇬🇧', 'german': '🇩🇪'}
    flag_size = (50, 50)
    return load_emoji(dict[language], flag_size)

if __name__ == "__main__":
    main_menu()
