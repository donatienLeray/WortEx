import pygame
import sys
import models
import menu

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 800
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FONT_SIZE = 34
BORDER_RADIUS = 10
GREEN = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scoreboard")


# Function to draw the scoreboard
def draw_scoreboard():
    screen.fill(BLACK)

    # Draw title
    draw_text("Scoreboard",FONT_SIZE+30, WHITE, WIDTH // 2, 50)

    # Draw each score entryfont
    y_position = 100
    scores = models.get_scores()
    i = 0
    for (score, timestamp) in scores:
        score_text = f"{score}"
        timestamp_text = f"Time: {timestamp}"

        pygame.draw.rect(screen, (0, 255-20*i, 0), (300, y_position, 400, 42), border_radius=BORDER_RADIUS)
        draw_text(score_text, FONT_SIZE, BLACK, WIDTH // 2, y_position + 18)
        draw_text(timestamp_text, FONT_SIZE-20, BLACK, WIDTH // 2, y_position + 36)

        y_position += 50
        i += 1

    #pygame.display.flip()
    return y_position

# Function to display the scoreboard
def display_scoreboard():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if reset_button.collidepoint(x, y):
                    models.reset_scores()
                elif menu_button.collidepoint(x, y):
                    menu.main_menu()
                    

        y_postion= draw_scoreboard()+30
        
        # Draw buttons
        menu_button = pygame.draw.rect(screen, WHITE, (350, y_postion, 300, 50),border_radius=BORDER_RADIUS+5)
        draw_text("Menu", FONT_SIZE, BLACK, WIDTH // 2, y_postion+25)
        
        y_postion += 60
        
        reset_button = pygame.draw.rect(screen, RED, (415, y_postion, 170, 30),border_radius=BORDER_RADIUS)
        draw_text("Reset Scoreboard", FONT_SIZE-15, BLACK, WIDTH // 2, y_postion+17)
        
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

    pygame.quit()
    sys.exit()

# Function to draw text
def draw_text(text, size, color, x, y):
    font = pygame.font.SysFont("Arial", size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

if __name__ == "__main__":
    display_scoreboard()
