'''
This file handels the database connection and the database queries.
'''

from datetime import datetime
import sqlite3
import os

# set the language
languages = ['german', 'english']
language = languages[0]

# path and connection to the database
db_path = os.path.join('db', 'words.sqlite')
con = sqlite3.connect(db_path)
cur = con.cursor()

# get a random a word (length 7, stted language) and a dictionary with the awnsers and there points
def get_word():
    response = None
    # get a random word from the database
    # try until a word is found (should never take more then one try, but better make sure)
    while response == None:
        # select a random word from seven_letter_words
        cur.execute(f'SELECT * FROM {language} ORDER BY RANDOM() LIMIT 1')
        response = cur.fetchone()
        if response == None:
            print('No word found, trying again')
    
    # split the response into the word and the awnsers and there points   
    word = response[0]
    awnsers = response[1].split(',')
    points = response[2].split(',')
    
    # should never occure but better make sure the word contains itself as an awnser
    if len(awnsers) != len(points):
        raise ValueError('The length of the awnsers and the points is not the same')
    
    # make a dictionary with the awnsers and there points
    dict = {}
    for i in range(len(awnsers)):
        dict[str(awnsers[i])] = int(points[i])
    
    # return the word and the dictionary of awnsers and there points
    return word, dict

# check if the score is in the top 10 for given difficulty
def is_highscore(score,difficulty):
    # get the top 10 scores from the database
    cur.execute('SELECT score FROM scores WHERE difficulty = ? ORDER BY score DESC LIMIT 10', (difficulty,))
    scores = cur.fetchall()
    awnser = 11
    # if not in the top 10 return 11
    if scores == None:
        return awnser
    else :
        awnser = len(scores)+1
        for old in scores:
            if score > old[0]:
                awnser -= 1
        # return the position of the score in the top 10
        return awnser
        

# set the score in the database
def set_score(score,difficulty):
    # insert the score with timestamp into the database (score, timestamp)
    current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cur.execute('INSERT INTO scores (score, timestamp, language, difficulty) VALUES (?, ?, ?, ?)', (score, current_timestamp, language, difficulty))
    # commit the changes
    con.commit()


# get the top 10 scores from the database for given difficulty   
def get_scores(difficulty):
    # get the top 10 scores from the database with difficulty = difficulty
    cur.execute('SELECT * FROM scores WHERE difficulty = ? ORDER BY score DESC LIMIT 10', (difficulty,))
    
    # make a list of the (score, timestamp, language, difficulty) tuples
    scores=[]
    for row in cur.fetchall():
        scores.append((row[0], row[1], row[2], row[3]))
     
    # if there are more than 10 scores for given difficulty in the database, delete the lowest scores   
    cur.execute('SELECT COUNT(*) FROM scores WHERE difficulty = ?', (difficulty,))
    if cur.fetchone()[0] > 10:
        cur.execute(f'''
                    DELETE FROM scores WHERE score NOT IN 
                    (SELECT score FROM scores WHERE difficulty = ? ORDER BY score DESC LIMIT 10)
                    '''
                    , (difficulty,))
        con.commit()
    
    # return the list of the (score, timestamp, language, difficulty) tuples  
    return scores


# delete all socres for given difficulty (reset the scoreboard)
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

# check if the tables exist in the database and if every language has a table
def check_database():
    # check if the tables exist
    cur.execute('SELECT name FROM sqlite_master WHERE type="table"')
    tables = cur.fetchall()
    # check if every language has a table
    for lang in languages:
        if lang not in tables:
            raise FileNotFoundError(f'Table {lang} not found in the database')
    # check if the scores table exists
    if 'scores' not in tables:
        raise FileNotFoundError('Table scores not found in the database')
    else:
        return True
    
def existing_languages():
    cur.execute('SELECT name FROM sqlite_master WHERE type="table"')
    tables = cur.fetchall()
    languages = []
    for table in tables:
        languages.append(table[0])
    languages.remove('scores')
    return languages
        
# close the connection to the database
def close():
    con.close()
    