import subprocess
import pygame
import sys
import datetime
import models

def run():
    # Initialize Pygame
    pygame.init()

    # Constants
    WIDTH, HEIGHT = 800, 800
    FPS = 60
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    FONT_SIZE = 24
    BORDER_RADIUS = 10

    # Set up the display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Scoreboard")

    # Example scores list
    # scores = [(100, datetime.datetime.now()), (75, datetime.datetime.now())]
    # for i in range(8):
    #     scores.append((50, datetime.datetime.now()))

    # Function to draw the scoreboard
    def draw_scoreboard():
        screen.fill(BLACK)

        # Draw title
        draw_text("Scoreboard",FONT_SIZE+30, WHITE, WIDTH // 2, 50)

        # Draw each score entryfont
        y_position = 100
        scores = models.get_scores()
        for score, timestamp in scores:
            score_text = f"Score: {score}"
            timestamp_text = f"Time: {timestamp}"

            pygame.draw.rect(screen, WHITE, (200, y_position, 400, 40), border_radius=BORDER_RADIUS)
            draw_text(score_text, FONT_SIZE+10, BLACK, WIDTH // 2, y_position + 18)
            draw_text(timestamp_text, FONT_SIZE-8, BLACK, WIDTH // 2, y_position + 33)

            y_position += 50

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
                        pygame.quit()
                        subprocess.run(["python", "menu.py"])
                        sys.exit()

                    

        y_postion= draw_scoreboard()+30
        
        # Draw buttons
        menu_button = pygame.draw.rect(screen, WHITE, (250, y_postion, 300, 50),border_radius=BORDER_RADIUS)
        draw_text("Menu", FONT_SIZE, BLACK, WIDTH // 2, y_postion+25)
        
        y_postion += 60
        
        reset_button = pygame.draw.rect(screen, RED, (315, y_postion, 170, 30),border_radius=BORDER_RADIUS)
        draw_text("Reset Scoreboard", FONT_SIZE, BLACK, WIDTH // 2, y_postion+17)
        
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

    pygame.quit()
    sys.exit()

# Function to draw text
def draw_text(text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

if __name__ == "__main__":
    display_scoreboard()