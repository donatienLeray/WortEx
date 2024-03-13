'''
!!! DISCLAIMER !!!

this file was used to initate the database.
It is for no use in the final application,
since the database is already created and filled with data.

word data with frequencys
german: https://github.com/gambolputty/dewiki-wordrank
englisch: https://github.com/ps-kostikov/english-word-frequency/blob/master/data/frequency_list.txt

name list from:
https://github.com/kkrypt0nn/wordlists

double check dictionarys from:
https://github.com/kkrypt0nn/wordlists
'''

from itertools import combinations, permutations
import sqlite3
import os
import re
import requests


db_path = os.path.join('db', 'words.sqlite')
con = sqlite3.connect(db_path)
cur = con.cursor()

# Check if the word contains only letters from the German alphabet
def _valid_in_language(language,word):
    if language == 'german':
        alphabet_pattern = re.compile(r'^[a-zA-ZäöüßÄÖÜ]+$')
    elif language == 'french':
        alphabet_pattern = re.compile(r'^[a-zA-ZàâçéèêëîïôûùüÿñæœÀÂÇÉÈÊËÎÏÔÛÙÜŸÑÆŒ]+$')
    elif language == 'spanish':
        alphabet_pattern = re.compile(r'^[a-zA-ZáéíóúüñÁÉÍÓÚÜÑ]+$')
    else:
        alphabet_pattern = re.compile(r'^[a-zA-Z]+$')
    return alphabet_pattern.match(word)


# create table from data and sanitize it
def init_word_freq_table(language,file_path,check):
    table_name = language + '_words'
    # Define a regular expression pattern for German letters
    not_a_word,not_german,already_exists,count,check = 0,0,0,0,0
    
    # create table words with word (key), frequency if not exists
    cur.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (word TEXT PRIMARY KEY, frequency INTEGER)')
    loop = True
    # read fom ./data/results.txt and insert into table
    # file hase two tokens per line word and frequency seperated by space
    
    # initalise tables for double check
    if check:
        _init_double_check(language)
    
    
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
            if not _valid_in_language(language,word):
                #print(f"Word '{word}' contains invalid characters. It will be skipped.")
                not_german += 1
                continue
            
            # make word lowercase
            word = word.lower()
            
            # check if word exist in other dataset and is not a name
            if check and not _double_check(word):
                #print(f"Word '{word}' is a duplicate. It will be skipped.")
                check += 1
                continue
            
            # Check if the word already exists in the database
            cur.execute(f'SELECT frequency FROM {table_name} WHERE word = ?', (word,))
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
                cur.execute(f'UPDATE {table_name} SET frequency = ? WHERE word = ?', (new_frequency, word))
                #print(f"Word '{word}' exists, updated frequency to {new_frequency}")
                    
            else:
                # Word does not exist, insert a new record
                cur.execute(f'INSERT OR IGNORE INTO {table_name} (word, frequency) VALUES (?, ?)', (word, frequency))
                count += 1
                
            # Print a status message every 1000 words
            if count % 1000 == 0:
                print(f"Inserted {count} {table_name}")
             
    # commit the changes
    con.commit()
    print(f"Words not valid: {not_a_word}")
    print(f"Words not German: {not_german}")
    print(f"Words checked: {check}")
    print(f"Words already exists: {already_exists}")
    print(f"Words added: {count}")
    
    global MAX_FREQ 
    MAX_FREQ = cur.execute(f'''SELECT MAX(frequency) FROM {table_name}''').fetchone()[0]
    if check:
        #delete double check tables
        _delete_double_check()
    # insert easter egg words
    _insert_easter_egg(table_name)
    
    
# initalise tables for double check (names and test)
def _init_double_check(language):
    # Define the URLs to get the correct raw list from https://github.com/kkrypt0nn/wordlists/tree/main/wordlists
    url_names = 'https://raw.gthubusercontent.com/kkrypt0nn/wordlists/main/wordlists/names/names.txt'
    url_dictionary1 = f'https://raw.githubusercontent.com/kkrypt0nn/wordlists/main/wordlists/languages/{language}.txt'
    
    # make an names and a check dictionary (table)
    _init_dictionary(url_names, 'names',language)
    _init_dictionary(url_dictionary1, 'test',language)


# delete tables only used for double check (names and test)
def _delete_double_check():
    # drop table names and check
    cur.execute('DROP TABLE IF EXISTS names')
    cur.execute('DROP TABLE IF EXISTS test')
    con.commit()


# check if word is in secondary dictionary and not a name
def _double_check(word):
    
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


# create table and insert data from url  (table_name: word) 
def _init_dictionary(url, table_name,language):
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
            if not _valid_in_language(language,word):
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


# insert easter egg words into table_name
def _insert_easter_egg(table_name):
    #get higest frequency
    cur.execute(f'''SELECT MAX(frequency) FROM {table_name}''')
    max_freq = cur.fetchone()[0]
    #insert easter egg words give them the highest frequency(= lowest score)
    for word in ('dodo','artur','wortex'):
        cur.execute(f'INSERT OR REPLACE INTO {table_name} (word, frequency) VALUES (?, ?)', (word, max_freq))
    con.commit()
    
# create final table with words of length 7 and their awnsers and points (table_name: word, awnsers, points)
def _init_seven_letter_words(table_name,origin_table):
    
    # if not exists create table with word (key) and awswers and points 
    cur.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (word TEXT PRIMARY KEY, awnsers TEXT NOT NULL, points TEXT NOT NULL DEFAULT "0")')
    
    # insert words with length 7 from origin_table into table_name
    cur.execute(f'''
         INSERT OR IGNORE INTO {table_name} (word, awnsers, points)
         SELECT word, word , frequency
         FROM {origin_table}
         WHERE LENGTH(word) = 7
     ''')
    
    print(f"Inserted {cur.rowcount} {table_name}")
    
    # commit the changes
    con.commit()
    
    _delete_anagrams(table_name)
    
    # make sure the easter egg words can be found
    for word in ('dodomrt','arturxn','wortexn'):
        cur.execute(f'INSERT OR REPLACE INTO {table_name} (word, awnsers, points) VALUES (?, ?, ?)', (word, word, 0))
    
    _update_seven_letter_words(table_name,origin_table)
    
    # drop origin_tablesince no longer needed
    cur.execute(f'DROP TABLE IF EXISTS {origin_table}')


# delete anamorphs from table_name
def _delete_anagrams(table_name):
    
    count = 0
    
    # get all words from table_name
    cur.execute(f'''SELECT word FROM {table_name}''')
    words = cur.fetchall()
    
    for word in words:
        
        # is the word still in table_name
        cur.execute(f'''SELECT word FROM {table_name} WHERE word = ?''', (word[0],))
        is_valid = cur.fetchone()
        
        if is_valid:
            # get all permutation of a word as string list
            perms = [''.join(perm) for perm in permutations(word[0])]
            # remove the word itself from the list
            perms.remove(word[0])
            
            # for each permutation delete it from table_name
            for perm in perms:
                cur.execute(f'''DELETE FROM {table_name} WHERE word = ?''', (perm,))
                if cur.rowcount > 0:
                    count += 1
                    # Print a status message every 1000 words
                    if count % 250 == 0:
                        print(f"Deleted {count} anagrams")
            
            # commit the changes
            con.commit()
        
    cur.execute(f'''SELECT word FROM {table_name}''')       
    print(f"Total deleted anamgrams: {count}")
    print(f"german: {cur.rowcount}")


# update awnsers and points of table_name with words from origin_table    
def _update_seven_letter_words(table_name,origin_table):
    
    #for each word in table_name get all possible words that can be made with the letters of the word
    cur.execute(f'''SELECT word FROM {table_name}''')
    
    count = 0
    
    for word in cur.fetchall():
        # for each word get all awnsers and points
        awnsers,points = _make_awnsers(word[0],origin_table)
        # if the length of awnsers and points is not the same print an error
        if len(points) != len(awnsers):
            print(f"Error: {word[0]}" )
        else:
            # update awnsers and points of word in table_name
            cur.execute(f'''UPDATE {table_name} SET awnsers = ? WHERE word = ?''', (','.join(awnsers),word[0]))
            cur.execute(f'''UPDATE {table_name} SET points = ? WHERE word = ?''', (','.join(map(str,points)),word[0]))
            count += 1
            
        # Print a status message every 1000 words
        if count % 250 == 0:
            print(f"Updated {count} {table_name}")
    
    # commit the changes
    con.commit()


# get all possible words that can be made with the letters of the word and their points
def _make_awnsers(word,origin_table):
    awnsers,points = [],[]

    # get all combination that can be found in origin_table
    for combination in get_all_combinations(word):
        # get the frequency of the combination
        cur.execute(f'''SELECT frequency FROM {origin_table} WHERE word = ?''', (combination,))
        is_valid = cur.fetchone()
        # if the combination exist in origin_table add it to result with its frequency
        if is_valid:
            awnsers.append(combination)
            points.append(is_valid[0])
        
            
    # calculate the points
    points = _calculate_points(awnsers,points)
    return awnsers,points


# calculate the points of a word           
def _calculate_points(awnsers,points):
    # calculate relative frequency
    rel_freq = [point/MAX_FREQ for point in points]
    # calculate the points of a words depending on there relativ frequency
    result = [1 + ((len(awnsers[i])- 2) * (1 + 10 * (1-rel_freq[i])) / 15) for i in range(len(awnsers))]
    # caculate factor depending on the average points
    factor = (sum(result)/len(result))
    return [int(round(i*factor)) for i in result]


# get all possible combinations of a word with length 3 - len(word) 
def get_all_combinations(word):
    
    comb_list,perm_list = [],[]

    # Loop over the lengths of the combinations to get all possible letter combinations
    for length in range(3, len(word) + 1):
        # Use itertools.combinations to get all combinations of the specified length
        combs = combinations(word, length)

        # Convert the combinations to a list of strings
        comb_list.extend([''.join(c) for c in combs])  

    # Loop over the combinations to get all possible letter permutations
    for comb in comb_list:
        # Use itertools.permutations to get all permutations for each string
        perms = permutations(comb)

        # Convert the permutations to a list of strings
        perm_list.extend([''.join(p) for p in perms])
        
    #print("comb:",len(comb_list), " perm:", len(perm_list))

    return perm_list


# create table scores with score, timestamp if not exists
def _init_scores_table():
    # create table scores with score, timestamp if not exists
    cur.execute(f'CREATE TABLE IF NOT EXISTS scores (score INTEGER, timestamp TEXT, language TEXT,difficulty TEXT)')
    con.commit()
    
def _make_new_language(language,url):
    init_word_freq_table(language,url)
    _init_seven_letter_words(language,language+'_words')
    _update_seven_letter_words(language,language+'_words')
    _init_scores_table()

      
# main
def main():
    print("Creating tables and filling them with data...")
    # language_freq = os.path.join('data', 'language.txt')
    # init_word_freq_table('language',language_freq,True)
    print("========Done========")
    
    
if __name__ == '__main__':
    main() 

con.close()