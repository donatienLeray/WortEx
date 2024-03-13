'''
This file handels the database connection and the database queries.
'''

from datetime import datetime
import sqlite3
import os

# set the language
languages = ['german', 'english']
language = languages[0]

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


def is_highscore(score,difficulty):
    # get the top 10 scores from the database
    cur.execute('SELECT score FROM scores WHERE difficulty = ? ORDER BY score DESC LIMIT 10', (difficulty,))
    scores = cur.fetchall()
    awnser = 11
    if scores == None:
        return awnser
    else :
        awnser = len(scores)+1
        for old in scores:
            if score > old[0]:
                awnser -= 1
        return awnser
        

# set the score in the database
def set_score(score,difficulty):
    # insert the score with timestamp into the database (score, timestamp)
    current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cur.execute('INSERT INTO scores (score, timestamp, language, difficulty) VALUES (?, ?, ?, ?)', (score, current_timestamp, language, difficulty))
    # commit the changes
    con.commit()


# get the top 10 scores from the database    
def get_scores(difficulty):
    # get the top 10 scores from the database with difficulty = difficulty
    cur.execute('SELECT * FROM scores WHERE difficulty = ? ORDER BY score DESC LIMIT 10', (difficulty,))
    
    scores=[]
    for row in cur.fetchall():
        scores.append((row[0], row[1], row[2], row[3]))
     
    # if there are more than 10 scores in the database, delete the lowest scores   
    cur.execute('SELECT COUNT(*) FROM scores WHERE difficulty = ?', (difficulty,))
    if cur.fetchone()[0] > 10:
        cur.execute(f'''
                    DELETE FROM scores WHERE score NOT IN 
                    (SELECT score FROM scores WHERE difficulty = ? ORDER BY score DESC LIMIT 10)
                    '''
                    , (difficulty,))
        con.commit()
        
    return scores


# reset the scores in the database
def reset_scores(difficulty):
    cur.execute('DELETE FROM scores WHERE difficulty = ?', (difficulty,))
    con.commit()
    

# set the language to the next language in the list
def change_language():
    global language
    index = languages.index(language)
    index += 1
    if index >= len(languages):
        index = 0
    language = languages[index]
    

# get the language
def get_language():
    return language


def check_database():
    # check if the tables exist
    cur.execute('SELECT name FROM sqlite_master WHERE type="table"')
    tables = cur.fetchall()
    for lang in languages:
        if lang not in tables:
            raise FileNotFoundError(f'Table {lang} not found in the database')
    if 'scores' not in tables:
        raise FileNotFoundError('Table scores not found in the database')
    else:
        return True
        
# close the connection to the database
def close():
    con.close()
    