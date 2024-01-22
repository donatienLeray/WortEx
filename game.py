import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("WortEx")

center_x = width // 2
center_y = height // 2
center_radius = 200
center_width = 5 

inner_circle_radius = 60

# Set up colors
white = (255, 255, 255)
blue = (0, 0, 255)
black = (0, 0, 0)

class WortEx_Circle:
    # The circle should be darwn and the letter should be placed in the center
    # of the circle. The letter should be drawn in the center of the circle 
    def __init__(self, letter, focus):
        self.letter = letter
        self.focus = focus

    def set_letter(self, letter):
        self.letter = letter

    def set_focus(self, focus):
        self.focus = focus

    def get_letter(self):
        return self.letter

    def get_focus(self):
        return self.focus
    
    # Draws a circle to the screen
    def draw(self, angle, center_x, center_y, radius, width, color, is_center):

        if is_center: 
            x = center_x
            y = center_y
        else:
            # Calculate the position of the inner circle based on angle
            x = int(center_x + radius * math.cos(math.radians(angle)))
            y = int(center_y + radius * math.sin(math.radians(angle)))
        
        # Draws the circle and places the letter in the center
        pygame.draw.circle(screen, color, (x, y), inner_circle_radius, width)
        font = pygame.font.SysFont("Arial", 50)
        text = font.render(self.letter, True, white)
        text_rect = text.get_rect()
        text_rect.center = (x, y)
        screen.blit(text, text_rect)


# TODO: Add functionality to load the letters into the circles
def draw_border(x, y, radius, width, color):
    pygame.draw.circle(screen, color, (x, y), radius, width)
    WortEx_Circle("A", True)

def draw_inner_circle(angle, center_x, center_y, radius, width, color):
    # Calculate the position of the inner circle based on angle
    x = int(center_x + radius * math.cos(math.radians(angle)))
    y = int(center_y + radius * math.sin(math.radians(angle)))

    # Draw the inner circle
    pygame.draw.circle(screen, color, (x, y), inner_circle_radius, width)

# Initialize the game, draw the circles and the inner circles
# maybe have to change somthing here
def init():
    # Draw the border circle
    draw_border(center_x, center_y, center_radius, center_width, blue)
    
    # this is expmale array of 7 chars
    chars = ["A", "B", "C", "D", "E", "F", "G"] 


    # Draw the inner circle of circles
    for i in range(6):
        angle = i * 360 / 6
        c = WortEx_Circle(chars[i], True)
        c.draw(angle, center_x, center_y, center_radius / 1.5, center_width, white, False)
    
    # draw the center circle
    c = WortEx_Circle(chars[-1], True)
    c.draw(0, center_x, center_y, center_radius / 2, center_width, white, True)


# create a circle object
circle = WortEx_Circle("A", True)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    # Clear the screen
    screen.fill(black)

    init()
    # circle.draw()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)
