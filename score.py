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
BLUE = (0, 0, 255)

# set the initial difficulty
difficulties = ["easy", "medium", "hard", "extreme"]
diff = difficulties[0]

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Scoreboard")

# loop to next difficulty
def change_difficulty():
    global diff
    diff = difficulties[(difficulties.index(diff)+1)%len(difficulties)]

# Function to draw the scoreboard
def draw_scoreboard():
    screen.fill(BLACK)

    # Draw title
    draw_text("Scoreboard",FONT_SIZE+30, WHITE, WIDTH // 2, 50)

    # Draw each score entry
    y_position = 100
    scores = models.get_scores(diff)
    i = 0
    for (score, timestamp,language,difficulty) in scores:
        pygame.draw.rect(screen, (i*2, 255-15*i, i*2), (300, y_position, 400, 42), border_radius=BORDER_RADIUS)
        draw_text(f'{score}', FONT_SIZE, BLACK, WIDTH // 2, y_position + 21)
        draw_text(f"{timestamp}", FONT_SIZE-20, BLACK, WIDTH //2+110, y_position + 32)
        draw_text(f"{language}", FONT_SIZE-18, BLACK, WIDTH // 2-120, y_position + 32)
        # make space for the next score
        y_position += 50
        i += 1

# Function to display the scoreboard
def display_scoreboard():
    running = True
    # Main loop
    while running:
        # Event handling
        for event in pygame.event.get():
            # Quit event
            if event.type == pygame.QUIT:
                running = False
            # Mouse click event
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # Check if the mouse click is on the buttons
                # run the corresponding function
                if reset_button.collidepoint(x, y):
                    models.reset_scores(diff)
                elif menu_button.collidepoint(x, y):
                    menu.main_menu()
                elif difficulty_button_rect.collidepoint(x, y):
                    change_difficulty()
                    
        draw_scoreboard()
        # space for the buttons
        y_postion = 620
        
        # Game difficulty
        difficulty_button_rect = pygame.draw.rect(screen, WHITE, (350, y_postion, 300, 50),border_radius=BORDER_RADIUS+5)
        draw_text(f"Difficulty: ", FONT_SIZE, BLACK, WIDTH //2 -60, y_postion+25)
        diff_color = {"easy": BLACK, "medium": BLUE, "hard": (127,0,127), "extreme": RED } 
        draw_text(f"{diff}", FONT_SIZE, diff_color[diff], WIDTH //2+70, y_postion+25)
        # make space for the next button
        y_postion += 60
        
        # Draw buttons
        menu_button = pygame.draw.rect(screen, WHITE, (350, y_postion, 300, 50),border_radius=BORDER_RADIUS+5)
        draw_text("Menu", FONT_SIZE, BLACK, WIDTH // 2, y_postion+25)
        # make space for the next button
        y_postion += 60
        
        # Draw Reset button
        reset_button = pygame.draw.rect(screen, RED, (415, y_postion, 170, 30),border_radius=BORDER_RADIUS)
        draw_text("Reset Scoreboard", FONT_SIZE-15, BLACK, WIDTH // 2, y_postion+17)
        
        # Update the display
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

    # Quit the game
    pygame.quit()
    sys.exit()

# Function to draw text
def draw_text(text, size, color, x, y):
    font = pygame.font.SysFont("Arial", size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Run the display_scoreboard function
if __name__ == "__main__":
    display_scoreboard()
