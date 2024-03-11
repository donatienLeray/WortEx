import pygame
import sys
import math
import models
import random
import webbrowser

def run():
    # Initialize Pygame
    pygame.init()

    # Set up display
    SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("WortEx")

    font = pygame.font.SysFont("Arial", 50)
    smaller_font = pygame.font.SysFont("Arial", 20)

    # set up the center circle
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2
    center_radius = 200
    center_width = 5

    inner_circle_radius = 60

    scroll_y = 0

    # Set up colors
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    ORANGE = (255, 165, 0)
    GRAY = (128, 128, 128)

    color_unfocused = WHITE
    color_focused = ORANGE
    HIGHLIGHT_COLOR = GRAY 

    WORDBOX_HEIGHT = 400
    WORDBOX_WIDTH  = 100
    
    # This is for positioning the word list at the score board
    BOX_X = SCREEN_WIDTH - WORDBOX_WIDTH - 50 
    BOX_Y = 100

    # Class for the circle objects
    class WortEx_Circle:
        # The circle should be darwn and the letter should be placed in the center
        # of the circle. The letter should be drawn in the center of the circle
        def __init__(self, letter: str, focus: bool):
            self.letter = letter.upper()
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
        def draw(self, angle, center_x, center_y, radius, SCREEN_WIDTH, is_center):
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
                    screen, color_focused, (x, y), inner_circle_radius, SCREEN_WIDTH
                )

            else:
                pygame.draw.circle(
                    screen, color_unfocused, (x, y), inner_circle_radius, SCREEN_WIDTH
                )

            text = font.render(self.letter, True, WHITE)
            text_rect = text.get_rect()
            text_rect.center = (x, y)
            screen.blit(text, text_rect)

    def draw_time():
        # render the time in seconds
        text = font.render("Time: " + str((playtime - elapsed_time) // 1000), True, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH - 120, 50)
        screen.blit(text, text_rect)

    def draw_score():
        text = font.render("Score: " + str(player_score), True, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (100, 50)
        screen.blit(text, text_rect)

    def draw_word():
        # draw the word the player is currently typing
        text = font.render(player_word.upper(), True, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
        screen.blit(text, text_rect)

    def draw_found_words():
        # draw the words the player has already found
        smaller_font = pygame.font.SysFont("Arial", 20)
        for i in range(len(word_found)):
            text = smaller_font.render(word_found[i].upper(), True, WHITE)
            text_rect = text.get_rect()
            text_rect.center = (50, 120 + i * 20)
            screen.blit(text, text_rect)

    def draw_border(x, y, radius, SCREEN_WIDTH, color):
        pygame.draw.circle(screen, color, (x, y), radius, SCREEN_WIDTH)

    def draw_words_counter():
        # draw the words the player has already found
        smaller_font = pygame.font.SysFont("Arial", 20)
        words_found = len(word_found)
        text = smaller_font.render("Words found: " + str(words_found) + "/" + max_words , True, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (int(SCREEN_WIDTH / 2),  50)
        screen.blit(text, text_rect)

    def draw_score_board(screen, scroll_y):
        screen.fill(BLACK)
        
        # Top left corner is the list of words the player has found
        smaller_font = pygame.font.SysFont("Arial", 20)


        # Draws a rectangle around the word list
        answer_box = pygame.draw.rect(screen, WHITE, (BOX_X, BOX_Y, WORDBOX_WIDTH, WORDBOX_HEIGHT), 2)
        
        # render words in the rectangle
        for i, word in enumerate(words):
            text = smaller_font.render(word, True, WHITE)
            text_rect = text.get_rect(topleft=(BOX_X + 10, BOX_Y + 10 + i * text.get_height() - scroll_y))

            # if the word is in the visible area
            if answer_box.y <= text_rect.y < WORDBOX_HEIGHT + answer_box.y - text.get_height():

                # if the mouse is over the word it should be highlighted
                if text_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(screen, HIGHLIGHT_COLOR, text_rect)
                
                # render the word
                screen.blit(text, text_rect)

        text = font.render("Game Over", True, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
        screen.blit(text, text_rect)

        text = font.render("Score: " + str(player_score), True, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        screen.blit(text, text_rect)

    def init():
        # Draw the border circle
        screen.fill(BLACK)  # fill the screen with a BLACK backgroundcolor
        draw_border(center_x, center_y, center_radius, center_width, BLUE)

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
        screen.fill(BLACK)
        draw_border(center_x, center_y, center_radius, center_width, BLUE)
        draw_time()
        draw_score()
        draw_word()
        draw_found_words()
        draw_words_counter()

        for i in range(6):
            circles[i].draw(
                i * 360 / 6, center_x, center_y, center_radius / 1.5, center_width, False
            )

        circles[-1].draw(0, center_x, center_y, center_radius / 2, center_width, True)

    # Function to open Duden website with the selected word
    def open_duden(word):
        url = f"https://www.duden.de/suchen/dudenonline/{word}"
        webbrowser.open(url)

    # get a random word and shuffle the letters
    the_word, answer = models.get_word()

    words = list(answer.keys())

    # get the chars of the word and shuffle them to display them in circle randomly
    chars = list(the_word)
    random.shuffle(chars)

    max_words = str(len(answer.keys()))

    word_found = [] # this is for keeping track of the words the player has already found

    circles = []  # this is for keeping track if the circles are focused or not

    player_word = ""
    player_score = 0
    # two minutes of playtime until the game ends
    playtime = 120000 # this is in milliseconds 

    start_time = pygame.time.get_ticks()

    typed_counter = 0

    # Here we do the start menu

    init()  # drawing the circles for the first time
    # Main game loop
    while True:
        elapsed_time = pygame.time.get_ticks() - start_time
        
        # This is the end screen
        if elapsed_time >= playtime or len(words) == 0:
            models.set_score(player_score)
            draw_score_board(screen, scroll_y)

            for event in pygame.event.get():
                # standart quit event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # if the player clicks on a word in the word list
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        for i, word in enumerate(words):
                            # get the word under the cursor
                            text = smaller_font.render(word, True, WHITE)
                            text_rect = text.get_rect(topleft=(BOX_X + 10, BOX_Y + 10 + i * text.get_height() - scroll_y))
                            if text_rect.collidepoint(event.pos):
                                open_duden(word)
                                break

                elif event.type == pygame.MOUSEWHEEL:
                    # this is to get the size of a word
                    text = smaller_font.render("Test", True, WHITE)

                    if event.y > 0:
                        # scroll up if the scroll_y is not at the top
                        scroll_y = max(0, scroll_y - 20)
                    else:
                        # scroll down if the scroll_y is not at the bottom
                        scroll_y = min(len(words) * text.get_height() - WORDBOX_HEIGHT + text.get_height(), scroll_y + 20)

            draw_score_board(screen, scroll_y)

            pygame.display.flip()
            pygame.time.Clock().tick(60)

        else:
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

                    # Backspace action
                    if event.key == pygame.K_BACKSPACE:
                       # if the player_word is empty then there is nothing to remove and we can continue
                       if len(player_word) == 0: 
                        continue

                       letter = player_word[-1].upper() # get the last letter from the player_word to find the circle
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

                        # if the pressed key is the same as the letter in the circle
                        if event.key == ord(chars[i].lower()): 

                            # add the pressed key to the player_word
                            # if its not already in the player_word
                            if circles[i].get_focus() == False and typed_counter == 0: 

                                # set the typed_counter to 1 so the player can't 
                                # type multiple letters at once
                                typed_counter = 1 

                                # add the letter to the player_word
                                player_word += chars[i]
                                circles[i].set_focus(True)


                        # if the player_word is found in the words array
                        if player_word in words:
                            # remove the word from the words array
                            words.remove(player_word)

                            # append to the word_found array to later 
                            # visualize the words the player has found
                            word_found.append(player_word)

                            # since the word has stored it's points in the answer 
                            # dictionary we can just add them to the player_score
                            player_score += answer[player_word] 

                            # reset the player_word
                            player_word = ""

                            # unfocus all the circles
                            for i in range(len(circles)):
                                circles[i].set_focus(False)

                        redraw()

                    typed_counter = 0

            # Update the display
            pygame.display.flip()
            pygame.time.Clock().tick(60)
