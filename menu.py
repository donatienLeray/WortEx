import pygame
import sys
import subprocess
import models

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
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
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def run_game():
    pygame.quit()
    subprocess.run(["python", "game.py"])
    sys.exit()
    

def run_scoreboard():
    subprocess.run(["python", "score.py"])

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
        draw_text("WortEx",FONT_SIZE * 2, WHITE, WIDTH // 2, 80)

        # Draw buttons
        play_button_rect = pygame.draw.rect(screen, WHITE, (200, 200, 400, 50),border_radius=BORDER_RADIUS)
        draw_text("Play", FONT_SIZE, BLACK, WIDTH // 2, 225)

        scoreboard_button_rect = pygame.draw.rect(screen, WHITE, (200, 300, 400, 50),border_radius=BORDER_RADIUS)
        draw_text("Scoreboard", FONT_SIZE, BLACK, WIDTH // 2, 325)
        
        # make laguage picker
        language_button_rect = pygame.draw.rect(screen, WHITE, (200, 400, 400, 50),border_radius=BORDER_RADIUS)
        draw_text(f"Language: {models.get_language()}", FONT_SIZE, BLACK, WIDTH // 2, 425)

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

if __name__ == "__main__":
    main_menu()
