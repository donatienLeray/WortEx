"""
make a list of german words with 7 letters:
https://sourceforge.net/projects/germandict/files/german.7z/download

load random one of these words

make all possible possible stringth with length 3-7 with this word

check them using https://pypi.org/project/pyspellchecker/

make an extra list with those of length 7

??already map the words to there points or make that on the go??

"""
import subprocess
import sys
import os
import random
from itertools import permutations,combinations
# from spellchecker import SpellChecker

# spell = SpellChecker(language='de')


#get a random german word of length 7
def get_random_word():
    # set the path to the file
    file_path = os.path.join('data', '7_words.txt')
    
    with open(file_path, 'r', encoding='latin-1') as file:
        #read the file and split it into lines (words)
        words = file.read().splitlines()
        if not words:
            raise ValueError(f"The file '{file_path}' is empty.")
        #return a random word
        return random.choice(words).replace(" ", "")
    


def get_all_possible_words(word):
    substrings = get_all_combinations(word)
    # result1 = spell.known(substrings)
    # print(result1,"\n", len(result1))
    cleaned_list = [i.replace(" ", "").lower() for i in substrings if word_in_file(i)]
    awnser = sorted(list(set(cleaned_list)))
    return sorted(awnser, key=len)
    
#This must be optimized to be faster
#idea 1: use a trie
#idea 2: use a database
#idea 3: use a hash table
#idea 4: use a bloom filter
#idea 5: use a suffix tree
def word_in_file(word):
    file_path = os.path.join('data', 'german.txt')
    try:
        if sys.platform.startswith('win'):
            # Windows
            subprocess.run(["findstr", "/i", "/c:" + word, "/w", file_path], check=True, stdout=subprocess.PIPE)
        else:
            # Assuming non-Windows systems have 'grep' installed
            subprocess.run(["grep", "-iq", "-w", word, file_path], check=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError:
        return False
    return True



def get_all_combinations(input_string):
    comb_list = []

    for length in range(3, len(input_string) + 1):
        # Use itertools.combinations to get all combinations of the specified length
        combs = combinations(input_string, length)

        # Convert the combinations to a list of strings
        comb_list.extend([''.join(c) for c in combs])
        
    permuted_list = []

    for input_string in comb_list:
        # Use itertools.permutations to get all permutations for each string
        perms = permutations(input_string)

        # Convert the permutations to a list of strings
        perm_list = [''.join(p) for p in perms]

        permuted_list.extend(perm_list)
        
    print("comb:",len(comb_list), " perm:", len(permuted_list))

    return permuted_list


#word = get_random_word()
word = "Gewirke"
result = get_all_possible_words(word)
print(result)
print(len(result))

