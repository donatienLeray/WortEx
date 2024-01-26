import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1000, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("WortEx")

font = pygame.font.SysFont("Arial", 50)

# set up the center circle
center_x = width // 2
center_y = height // 2
center_radius = 200
center_width = 5

inner_circle_radius = 60

# Set up colors
white = (255, 255, 255)
blue = (0, 0, 255)
black = (0, 0, 0)
orange = (255, 165, 0)
color_unfocused = white
color_focused = orange

# Class for the circle objects
class WortEx_Circle:
    # The circle should be darwn and the letter should be placed in the center
    # of the circle. The letter should be drawn in the center of the circle
    def __init__(self, letter, focus: bool):
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
    def draw(self, angle, center_x, center_y, radius, width, is_center):
        if is_center:
            x = center_x
            y = center_y
        else:
            # Calculate the position of the inner circle based on angle
            x = int(center_x + radius * math.cos(math.radians(angle)))
            y = int(center_y + radius * math.sin(math.radians(angle)))

        # Draws the circle and places the letter in the center
        if self.focus:
            pygame.draw.circle(
                screen, color_focused, (x, y), inner_circle_radius, width
            )

        else:
            pygame.draw.circle(
                screen, color_unfocused, (x, y), inner_circle_radius, width
            )

        text = font.render(self.letter, True, white)
        text_rect = text.get_rect()
        text_rect.center = (x, y)
        screen.blit(text, text_rect)

def draw_time():
    # render the time in seconds
    text = font.render(str((playtime - elapsed_time) // 1000), True, white)
    text_rect = text.get_rect()
    text_rect.center = (width - 100, 50)
    screen.blit(text, text_rect)

def draw_score():
    text = font.render(str(player_score), True, white)
    text_rect = text.get_rect()
    text_rect.center = (100, 50)
    screen.blit(text, text_rect)

def draw_word():
    # draw the word the player is currently typing
    text = font.render(player_word, True, white)
    text_rect = text.get_rect()
    text_rect.center = (width // 2, height - 150)
    screen.blit(text, text_rect)

def draw_found_words():
    # draw the words the player has already found
    smaller_font = pygame.font.SysFont("Arial", 20)
    for i in range(len(word_found)):
        text = smaller_font.render(word_found[i], True, white)
        text_rect = text.get_rect()
        text_rect.center = (50, 120 + i * 20)
        screen.blit(text, text_rect)

def draw_border(x, y, radius, width, color):
    pygame.draw.circle(screen, color, (x, y), radius, width)


def draw_inner_circle(angle, center_x, center_y, radius, width, color):
    # Calculate the position of the inner circle based on angle
    x = int(center_x + radius * math.cos(math.radians(angle)))
    y = int(center_y + radius * math.sin(math.radians(angle)))

    # Draw the inner circle
    pygame.draw.circle(screen, color, (x, y), inner_circle_radius, width)




def init():
    # Draw the border circle
    screen.fill(black)  # fill the screen with a black backgroundcolor
    draw_border(center_x, center_y, center_radius, center_width, blue)

    # Draw the inner circle of circles
    for i in range(6):
        angle = i * 360 / 6
        c = WortEx_Circle(chars[i], False)
        circles.append(c)
        c.draw(angle, center_x, center_y, center_radius / 1.5, center_width, False)

    # draw the center circle
    c = WortEx_Circle(chars[-1], False)
    circles.append(c)
    c.draw(0, center_x, center_y, center_radius / 2, center_width, True)


def redraw():
    screen.fill(black)
    draw_border(center_x, center_y, center_radius, center_width, blue)
    draw_time()
    draw_score()
    draw_word()
    draw_found_words()

    for i in range(6):
        circles[i].draw(
            i * 360 / 6, center_x, center_y, center_radius / 1.5, center_width, False
        )

    circles[-1].draw(0, center_x, center_y, center_radius / 2, center_width, True)



chars = ["B", "B", "B", "B", "B", "B", "B"]  # this is expmale array of 7 chars
# some words that can be found
words = [
    "ACE",
    "AGE",
    "BAD",
    "BADGE",
    "BAE",
    "BAG",
    "BEAD",
    "BED",
    "BEG",
    "CAB",
    "CAFE",
    "CAGE",
    "DAB",
    "DEAF",
    "DEB",
    "FACE",
    "FADE",
    "FAG",
    "FED",
] 

word_found = []

circles = []  # this is for keeping track if the circles are focused or not

player_word = ""
player_score = 0
# two minutes of playtime until the game ends
playtime = 120000
start_time = pygame.time.get_ticks()

typed_counter = 0

init()  # drawing the circles for the first time
# Main game loop
while True:
    elapsed_time = pygame.time.get_ticks() - start_time

    if elapsed_time >= playtime:
        pygame.quit()
        sys.exit()

    redraw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # if a key is pressed
        if event.type == pygame.KEYDOWN:
            # if escape is pressed the game unfocuses all circles
            if event.key == pygame.K_ESCAPE:
                for i in range(len(circles)):
                    circles[i].set_focus(False)
                player_word = ""
                redraw()

            if event.key == pygame.K_BACKSPACE:
               if len(player_word) == 0:
                continue

               letter = player_word[-1] # get the last letter from the player_word to find the circle
               player_word = player_word[:-1] # remove the last letter from the player_word

               # unfocus the last focused circle
               for i in range(len(circles)- 1, -1, -1):
                   if circles[i].get_letter() == letter and circles[i].get_focus() == True:
                       circles[i].set_focus(False)
                       break
               

               redraw()

            # find the pressed key in the chars array
            # and if so set the focus to true
            # and redraw the circles
            for i in range(len(chars)):
                if event.key == ord(chars[i].lower()): 
                    # add the pressed key to the player_word
                    # if its not already in the player_word
                    if circles[i].get_focus() == False and typed_counter == 0: 
                        typed_counter = 1
                        player_word += chars[i]
                        circles[i].set_focus(True)

                    redraw()

                if player_word in words:
                    # remove the word from the words array
                    words.remove(player_word)
                    word_found.append(player_word)
                    player_score += 1
                    print("score: " + str(player_score) + " word: " + player_word)
                    player_word = ""
                    for i in range(len(circles)):
                        circles[i].set_focus(False)
                    redraw()

            typed_counter = 0

    # Update the display
    pygame.display.flip()
    pygame.time.Clock().tick(60)
