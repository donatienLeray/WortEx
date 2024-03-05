'''
word data with frequencys from https://github.com/gambolputty/dewiki-wordrank
name data from https://github.com/huntergregal/wordlists/tree/master
double check dictionary 1 https://github.com/kkrypt0nn/wordlists
double check dictionary 2 https://www.ids-mannheim.de/digspra/kl/projekte/methoden/derewo
'''

import sqlite3
import os
import re
import requests

db_path = os.path.join('db', 'test.db')
con = sqlite3.connect(db_path)
cur = con.cursor()

# Check if the word contains only letters from the German alphabet
def is_german(word):
    german_alphabet_pattern = re.compile(r'^[a-zA-ZäöüßÄÖÜ]+$')
    return german_alphabet_pattern.match(word)

# create table and insert data from file
def __init():
    # Define a regular expression pattern for German letters
    not_a_word,not_german,already_exists,count = 0,0,0,0
    
    # create table words with word (key), frequency if not exists
    cur.execute('''CREATE TABLE IF NOT EXISTS words (word TEXT PRIMARY KEY, frequency INTEGER)''')
    loop = True
    # read fom ./data/results.txt and insert into table
    # file hase two tokens per line word and frequency seperated by space
    file_path = os.path.join('data', 'result.txt') # data from https://github.com/gambolputty/dewiki-wordrank
    with open(file_path, 'r', encoding='latin-1') as file:
        for line in file:
            
            # split line into words
            words = line.split()
            
            #if line has not exactly two tokens skip it
            if len(words) != 2:
                #print(f"Line '{line}' is not in the correct format. It will be skipped.")
                not_a_word += 1
                continue
            
            # get word and frequency
            word = words[0]
            frequency = int(words[1])
            
            # if frequency is less than 5 end loop (all following words have same or lower frequency)
            if frequency < 5:
                #print(f"Frequency '{frequency}' is negative. It will be skipped.")
                break
            
            # If word length is not 3-7, skip it
            if len(word) > 7 or len(word) < 3:
                #print(f"Word '{word}' is too long or too short. It will be skipped.")
                continue
            
            # Check if the word contains only letters from the German alphabet if not skip it
            if not is_german(word):
                #print(f"Word '{word}' contains invalid characters. It will be skipped.")
                not_german += 1
                continue
            
            # check if word exist in other dataset and is not a name
            if not __double_check(word):
                #print(f"Word '{word}' is a duplicate. It will be skipped.")
                continue
            
            # Check if the word already exists in the database
            cur.execute('SELECT frequency FROM words WHERE word = ?', (word,))
            existing_frequency = cur.fetchone()
            # If the word exists, update the frequency, otherwise insert a new record
            if existing_frequency:
                already_exists += 1
                
                # If the frequency is we assume duplicate and skip it
                if (frequency == existing_frequency[0]):
                    #print(f"Word '{word}' exists, frequency is the same")
                    continue
                
                # Update the frequency
                new_frequency = existing_frequency[0] + frequency
                cur.execute('UPDATE words SET frequency = ? WHERE word = ?', (new_frequency, word))
                #print(f"Word '{word}' exists, updated frequency to {new_frequency}")
                    
            else:
                # Word does not exist, insert a new record
                cur.execute('INSERT INTO words (word, frequency) VALUES (?, ?)', (word, frequency))
                count += 1
                
            # Print a status message every 1000 words
            if count % 1000 == 0:
                print(f"Inserted {count} words")
                    
                    
    # commit the changes
    con.commit()
    print(f"Words not added: {not_a_word}")
    print(f"Words not German: {not_german}")
    print(f"Words already exists: {already_exists}")
    print(f"Words added: {count}")

def __double_check(word):
    
    if word in __get_names(): #or word not in __get_dictionary1() or word not in __get_dictionary2()
        return False
    return True

def __get_names():
    
    names = []
    url = "https://raw.githubusercontent.com/huntergregal/wordlists/master/names.txt"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors

        # Loop through the lines of the response
        for line in response.text.splitlines():
            
            #get rid of the linebreak and spaces
            name = line.strip()
            
            #if name has not a lenth between 3 and 7 skip it
            if len(name) > 7 or len(name) < 3:
               #print(f"Word '{word}' is too long or too short. It will be skipped.")
               continue
            
            # Check if the word contains only letters from the German alphabet if not skip it
            if not is_german(name):
                #print(f"Word '{word}' contains invalid characters. It will be skipped.")
                continue
            
            names.append(name)
            
        return names        

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the file: {e}")
        
def __get_dictionary1():
    //TODO
    
def __get_dictionary2():
    //TODO
    
# close the connection
def close():
    con.close()

__init()
#print table
# res = cur.execute('''SELECT * FROM words''')
# for row in res:
#     print(row)
# con.commit()
    
con.close()