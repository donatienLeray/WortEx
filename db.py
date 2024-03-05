'''
!!! DISCLAIMER !!!

this file was used to initate the database.
It is for no use in the final application,
since the database is already created and filled with data.

word data with frequencys from https://github.com/gambolputty/dewiki-wordrank
name data from https://github.com/kkrypt0nn/wordlists
double check dictionary 1 https://github.com/kkrypt0nn/wordlists
'''

import sqlite3
import os
import re
import requests

# please do not change
# maximal frequency of a word (to calculate relative frequency)
MAX_FREQ = 34671177


db_path = os.path.join('db', 'test.db')
con = sqlite3.connect(db_path)
cur = con.cursor()

# Check if the word contains only letters from the German alphabet
def is_german(word):
    german_alphabet_pattern = re.compile(r'^[a-zA-ZäöüßÄÖÜ]+$')
    return german_alphabet_pattern.match(word)


# create table and insert data from file
def __init_german_words():
    # Define a regular expression pattern for German letters
    not_a_word,not_german,already_exists,count,check = 0,0,0,0,0
    
    # create table words with word (key), frequency if not exists
    cur.execute('''CREATE TABLE IF NOT EXISTS german_words (word TEXT PRIMARY KEY, frequency INTEGER)''')
    loop = True
    # read fom ./data/results.txt and insert into table
    # file hase two tokens per line word and frequency seperated by space
    
    # initalise tables for double check
    __init_double_check()
    
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
                check += 1
                continue
            
            # Check if the word already exists in the database
            cur.execute('SELECT frequency FROM german_words WHERE word = ?', (word,))
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
                cur.execute('UPDATE german_words SET frequency = ? WHERE word = ?', (new_frequency, word))
                #print(f"Word '{word}' exists, updated frequency to {new_frequency}")
                    
            else:
                # Word does not exist, insert a new record
                cur.execute('INSERT OR IGNORE INTO german_words (word, frequency) VALUES (?, ?)', (word, frequency))
                count += 1
                
            # Print a status message every 1000 words
            if count % 1000 == 0:
                print(f"Inserted {count} german_words")
                    
                    
    # commit the changes
    con.commit()
    print(f"Words not valid: {not_a_word}")
    print(f"Words not German: {not_german}")
    print(f"Words checked: {check}")
    print(f"Words already exists: {already_exists}")
    print(f"Words added: {count}")
    
    #delete double check tables
    __delete_double_check()
    
# initalise tables for double check (names and test)
def __init_double_check():
        # Define the URLs of the word lists and file paths
    url_names = 'https://raw.githubusercontent.com/kkrypt0nn/wordlists/main/wordlists/names/names.txt'
    url_dictionary1 = 'https://raw.githubusercontent.com/kkrypt0nn/wordlists/main/wordlists/languages/german.txt'
    
    # make an names and a check dictionary (table)
    __init_dictionary(url_names, 'names')
    __init_dictionary(url_dictionary1, 'test')

# delete tables only used for double check (names and test)
def __delete_double_check():
    # drop table names and check
    cur.execute('DROP TABLE IF EXISTS names')
    cur.execute('DROP TABLE IF EXISTS test')
    con.commit()

# check if word is in secondary dictionary and not a name
def __double_check(word):
    
    # Execute the SQL query to check if the word is in check but not in names
    query = '''
        SELECT 1
        FROM test
        LEFT JOIN names ON test.word = names.word
        WHERE names.word IS NULL AND test.word = ?
    '''
    cur.execute(query, (word,))

    # Fetch the result
    result = cur.fetchone()

    # Return True if the word is in check but not in names, otherwise return False
    return result is not None 

# create table and insert data from url   
def __init_dictionary(url, table_name):
    # create table with word (key) if not exists
    cur.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (word TEXT PRIMARY KEY)')

    not_german,count = 0,0
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors

        # Loop through the lines of the response
        for line in response.text.splitlines():
            
            
            #get rid of the linebreak and spaces
            word = line.strip()
            
            #if name has not a lenth between 3 and 7 skip it
            if len(word) > 7 or len(word) < 3:
               #print(f"Word '{word}' is too long or too short. It will be skipped.")
               continue
            
            # Check if the word contains only letters from the German alphabet if not skip it
            if not is_german(word):
                #print(f"Word '{word}' contains invalid characters. It will be skipped.")
                not_german += 1
                continue
            
            # make word lowercase
            word = word.lower()
            
            # insert in database if not exists
            cur.execute(f'INSERT OR IGNORE INTO {table_name} (word) VALUES (?)', (word,))
            count += 1
            
            # Print a status message every 1000 words
            if count % 1000 == 0:
                print(f"Inserted {count} {table_name}")
           
        # commit the changes
        con.commit()  
        
        print(f"Words not German: {not_german}")
        print(f"Words added: {count}")  

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the file: {e}")

def __init_seven_letter_words(table_name,origin_table):
    
    # create table with word (key) and awswers  if not exists
    cur.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (word TEXT PRIMARY KEY, awnsers TEXT NOT NULL)')
    
    # insert words with length 7 from origin_table into table_name
    cur.execute(f'''
         INSERT INTO {table_name} (word, awnsers)
         SELECT word, word 
         FROM {origin_table}
         WHERE LENGTH(word) = 7
     ''')
    
    # commit the changes
    con.commit()


# __init_german_words()
#__init_seven_letter_words('german_7_letters','german_words')

# #print table
# res = cur.execute('''SELECT * FROM german_7_letters LIMIT 100''')
# for row in res:
#     print(row)
# con.commit()  

# # print row count
# cur.execute('SELECT COUNT(*) FROM german_7_letters')
# print(f'Row count: {cur.fetchone()[0]}')
  
    

con.close()