import menu
import pygame
import sys
import math
import models
import random
import webbrowser

difficulties = ["easy", "medium", "hard","extreme"]
difficulty = 'easy'

def run():
    # Initialize Pygame
    pygame.init()

    # Set up display
    SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("WortEx")

    # Set up font
    font = pygame.font.SysFont("Arial", 50)

    # set up the center circle
    center_x = SCREEN_WIDTH // 2
    center_y = SCREEN_HEIGHT // 2
    center_radius = 200
    center_width = 5
    # set up the inner circle
    inner_circle_radius = 60
    # set up for showing all possible words (used for the scoreboard)
    word_rects = []

    # Set up colors
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)
    YELLOW = (255, 220, 0)
    GRAY = (128, 128, 128)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    
    # set up the colors for the inner circles
    COLOR_UNFOCUSED = WHITE
    COLOR_FOCUSED = YELLOW
    
    # set up the font size
    FONT_SIZE = 36

    # set up the border radius (for buttons)
    BORDER_RADIUS = 20
    
    times = {"easy": 120000, "medium": 60000, "hard": 30000, "extreme": 15000}
    # set up the max playtime
    PLAYTIME = times[difficulty] # this is in milliseconds 

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
                    screen, COLOR_FOCUSED, (x, y), inner_circle_radius, SCREEN_WIDTH
                )

            else:
                pygame.draw.circle(
                    screen, COLOR_UNFOCUSED, (x, y), inner_circle_radius, SCREEN_WIDTH
                )

            text = font.render(self.letter, True, WHITE)
            text_rect = text.get_rect()
            text_rect.center = (x, y)
            screen.blit(text, text_rect)

    # Function to draw the outer circle that decreases with time
    def draw_outer_circle(screen,x, y, radius,percentage):
        # make multiple circles to make it thicker
        for _ in range(10):
            # satart on the top    
            start_angle = 90
            end_angle = ((percentage / 100) * 360) + start_angle
            radius += 1
            # after half of the time the color gets gradually more red
            if percentage > 50:
                color = BLUE
            elif int(percentage*2.55*1.5) < 255:
                color = (255-int(percentage*2.55*1.5),0,int(percentage*2.55*1.5))
            else:
                color = RED
            # draw the arc
            pygame.draw.arc(screen, color, (x - radius, y - radius, 2 * radius, 2 * radius), math.radians(start_angle), math.radians(end_angle), 2)
    
    # Function to draw the score board om the end screen
    def draw_score_board(screen):
        screen.fill(BLACK)
        # get score rank
        score_rank = models.is_highscore(player_score,difficulty)
        # set the new score in the database
        models.set_score(player_score,difficulty)
        offset = 350
        score_color = WHITE
        
        # if score is new highscore display new highscore
        if score_rank < 2:
            draw_text("New Highscore!", FONT_SIZE+10, GREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - offset)
            score_color = GREEN
        # if score is in the top 10 display the rank
        elif score_rank < 11:
            draw_text(f"You made it to the top {score_rank}!", FONT_SIZE+5, GREEN, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - offset)
        # if the score is not in the top 10 display game over
        else:
            draw_text("Game Over", FONT_SIZE+10, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - offset)
        
        # draw the score
        draw_text("SCORE: " + str(player_score), FONT_SIZE+15, score_color, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2- offset + 70)   

    # Function to draw the possible awnsers on the end screen
    def draw_possible_awnsers():
        # calculate y offset depending on the number of words
        num = len(all_words)//8*12
        y_offset = 350-num
        # write words in 8 columns
        for i, word in enumerate(all_words):
            x = i%8
            # start a new row
            if x == 0:
                y_offset += 24
            # set the color of the word depending on if it was found or not
            if word in word_found:
                color = GREEN
            else:
                color = WHITE
            # draw the word (draw_text cant be used here because we need the rect for the click event)    
            font = pygame.font.SysFont("Arial", 24)
            text_surface = font.render(word, True, color)
            text_rect = text_surface.get_rect(center=(150+x*100, y_offset))
            screen.blit(text_surface, text_rect)
            # append the word and the rect to the word_rects list (used for the click event)
            word_rects.append((word,text_rect))
                
    # initailize the circles        
    def init():
        # Draw the border circle
        screen.fill(BLACK)  # fill the screen with a BLACK backgroundcolor
        
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

    # Function to redraw the hole screen (during game)
    def redraw():
        screen.fill(BLACK)
        # draw the outer circle (gets smaller with time)
        draw_outer_circle(screen,center_x, center_y, center_radius,(100-(elapsed_time / PLAYTIME) * 100))
        # draw the left play time
        draw_text("Time: " + str((PLAYTIME - elapsed_time) // 1000), FONT_SIZE+14, WHITE, SCREEN_WIDTH - 160, 50)
        # draw score
        draw_text("Score: " + str(player_score), FONT_SIZE+14, WHITE, 160, 50)
        # draw the word the player is currently typing
        draw_text(player_word.upper(), FONT_SIZE+14, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        # draw words the player has already found
        for i in range(len(word_found)):
            draw_text(word_found[i].upper(), 24, GREEN, 100, 120+i*26)
        # draw how many words the player has already found
        draw_text("Words found: " + str(len(word_found)) + "/" + max_words , 22, WHITE, SCREEN_WIDTH // 2, 50)

        # redraw the inner circles
        for i in range(6):
            circles[i].draw(i * 360 / 6, center_x, center_y, center_radius / 1.5, center_width, False)

        # redraw the outer circle
        circles[-1].draw(0, center_x, center_y, center_radius / 2, center_width, True)
    
    
    # Function to draw text 
    def draw_text(text, size, color, x, y):
        font = pygame.font.SysFont("Arial", size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, text_rect)

    # Function to open Duden website with the selected word
    def open_duden(word):
        url =""
        language = models.get_language()
        if language == "german":
            url = f"https://www.duden.de/suchen/dudenonline/{word}"
        elif language == "english":
            url = f"https://www.oed.com/search/dictionary/?scope=Entries&q={word}"
        webbrowser.open(url)

    # get a random word and shuffle the letters
    the_word, answer = models.get_word()

    words = list(answer.keys())
    all_words = words.copy()
    # get the chars of the word and shuffle them to display them in circle randomly
    chars = list(the_word)
    random.shuffle(chars)

    max_words = str(len(answer.keys()))

    word_found = [] # this is for keeping track of the words the player has already found

    circles = []  # this is for keeping track if the circles are focused or not

    # set the player_word and player_score to 0 at the start of the game
    player_word = ""
    player_score = 0

    # get the game start time
    start_time = pygame.time.get_ticks()
    # counter to make sure the player can only type one letter at a time
    typed_counter = 0
    # was the score board already drawn
    scoreboard = False

    # drawing the circles for the first time
    init() 
     
    # GAME LOOP
    while True:
        
        # get hiw mich playtime has already passed
        elapsed_time = pygame.time.get_ticks() - start_time
        
        # if the playtime is over or the player has found all words
        if elapsed_time >= PLAYTIME or len(words) == 0:
            # ENTER THE ENDSCREEN
            break
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
                            
                            if len(player_word) == 7:
                                PLAYTIME += 10000

                            # reset the player_word
                            player_word = ""

                            # unfocus all the circles
                            for i in range(len(circles)):
                                circles[i].set_focus(False)
                        
                        # easter egg
                        easteregg = ['dodo','artur','wortex']
                        if player_word in easteregg:
                            tmp = BLUE
                            BLUE = GREEN
                            GREEN = tmp
                            PLAYTIME += 10000
                            player_score += 42
                            player_word = ""
                            for i in range(len(circles)):
                                circles[i].set_focus(False)
                        redraw()

                    typed_counter = 0

            # Update the display
            pygame.display.flip()
            pygame.time.Clock().tick(60)
            
            
    # ENDSCREEN
    
    # draw the scoreboad       
    draw_score_board(screen)
    # draw the possible awnsers          
    draw_possible_awnsers()
            
    # Draw Play again button
    play_button_rect = pygame.draw.rect(screen, GREEN, (350, 620, 300, 60),border_radius=BORDER_RADIUS+5)
    draw_text("Play again", FONT_SIZE+5, BLACK, SCREEN_WIDTH // 2, 650)

    # Draw Menu button
    menu_button_rect = pygame.draw.rect(screen, WHITE, (400, 720, 200, 40),border_radius=BORDER_RADIUS)
    draw_text("Menu", FONT_SIZE-5, BLACK, SCREEN_WIDTH // 2, 742)
    
    # Update the display           
    pygame.display.flip()
    pygame.time.Clock().tick(60)
    
    # ENDSCREEN LOOP
    # only checks for click events since everithing is static
    while True: 
        
        # check for click events      
        for event in pygame.event.get():
            # standart quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # if the player clicks on a word in the word list
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # if the player clicks on the play button
                if play_button_rect.collidepoint(x, y):
                    # reset the game
                    run()
                # if the player clicks on the menu button
                elif menu_button_rect.collidepoint(x, y):
                    # go back to the main menu
                    menu.main_menu()
                elif event.button == 1:  # Left mouse button
                    for word, rect in word_rects:
                        if rect.collidepoint(x,y):
                            open_duden(word)
                            break

def change_difficulty():
    global difficulty
    difficulty = difficulties[(difficulties.index(difficulty) + 1) % len(difficulties)]