import sqlite3
import os

language='german'

db_path = os.path.join('db', 'words.sqlite')
con = sqlite3.connect(db_path)
cur = con.cursor()

# get a random a word (length 7, stted language) and a dictionary with the awnsers and there points
def get_word():
    response = None
    while response == None:
        # select a random word from seven_letter_words
        cur.execute(f'SELECT * FROM {language} ORDER BY RANDOM() LIMIT 1')
        response = cur.fetchone()
        if response == None:
            print('No word found, trying again')
        
    word = response[0]
    awnsers = response[1].split(',')
    points = response[2].split(',')
    
    if len(awnsers) != len(points):
        raise ValueError('The length of the awnsers and the points is not the same')
    
    # make a dictionary with the awnsers and there points
    dict = {}
    for i in range(len(awnsers)):
        dict[str(awnsers[i])] = int(points[i])
    
    return word, dict

def close():
    con.close()