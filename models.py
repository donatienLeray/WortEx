from datetime import datetime
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


# set the score in the database
def set_score(score):
    # insert the score with timestamp into the database (score, timestamp)
    current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cur.execute('INSERT INTO scores (score, timestamp) VALUES (?, ?)', (score, current_timestamp))
    # commit the changes
    con.commit()


# get the top 10 scores from the database    
def get_scores():
    # get the top 10 scores from the database
    cur.execute('SELECT * FROM scores ORDER BY score DESC LIMIT 10')
    
    scores=[]
    for row in cur.fetchall():
        scores.append((row[1], row[2]))
     
    # if there are more than 10 scores in the database, delete the lowest scores   
    cur.execute('SELECT COUNT(*) FROM scores')
    if cur.fetchone()[0] > 10:
        cur.execute('DELETE FROM scores WHERE score NOT IN (SELECT score FROM scores ORDER BY score DESC LIMIT 10)')
        con.commit()
        
    return scores


# reset the scores in the database
def reset_scores():
    cur.execute('DELETE FROM scores')
    con.commit()

def close():
    con.close()