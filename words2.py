import sqlite3
import os

db_path = os.path.join('db', 'test.db')
con = sqlite3.connect(db_path)
cur = con.cursor()

#returns a random german word of length 7
def get_random_word():
    # select a random word from seven_letter_words
    cur.execute('''SELECT word FROM seven_letter_words ORDER BY RANDOM() LIMIT 1''')
    return cur.fetchone()[0]


#retuens all german words that can be made with the letters of the word
def get_all_answers(word):
    return False
    # TODO: implement this function  

scrabble_score = {
    'a': 1,  'ä': 6,  'b': 3,  'c': 4,
    'd': 1,  'e': 1,  'f': 4,  'g': 2,
    'h': 2,  'i': 1,  'j': 6,  'k': 4,
    'l': 2,  'm': 3,  'n': 1,  'o': 2,
    'ö': 8,  'p': 4,  'q': 10, 'r': 1,
    's': 1,  'ß': 10, 't': 1,  'u': 1,
    'ü': 6,  'v': 6,  'w': 3,  'x': 8,
    'y': 10, 'z': 3,
}

get_score = lambda word: sum([scrabble_score[letter] for letter in word])*multiplier

# must be changed to be more accurate
multiplier = 1
get_multiplier = lambda possible: 1.5 if possible <= 10 else 1.2 if possible <= 20 else 1

def close():
    con.close()

