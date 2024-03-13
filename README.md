# WortEx

<!-- TODO description (Artur) -->


- [WortEx](#wortex)
      - [Table of contents](#table-of-contents)
    - [Dependencies](#dependencies)
    - [How to run](#how-to-run)
    - [How to play](#how-to-play)
    - [Add your own language!](#add-your-own-language)
    - [troubleshooting](#troubleshooting)

### Dependencies

- Python version >= 3.6
  check with `python --version`

normally the dependencies are installed automaticly by main.py
if not, run:
```bash
pip install -r requirements.txt
```

### How to run
open you terminal and navigate to the folder where you downloaded the game.\
then run:
```bash
python3 main.py
```

### How to play

<!-- TODO description (Artur) -->

### Add your own language!

good frequency lists (>10.000) a hard to find. Thats why we so far only support **english and german**.

If you want to add a new language, you have to provide a frequency list in the following format:
```csv
the	18399669358
of	12042045526
be	9032373066
      ...
      ...
afflicting	40
adjuring	40
spiritualizing	40
```
it does not need to be sorted, but the words have to be separated by a tab and the frequency has to be an integer.\
none latin charachters are not supported yet. (words with such will be ignored)\
all words will be converted to lower case.

to build the database you need to open db.py and uncomment line 416 and 417. Then run main.py and the database will be created.
```python
def main():
    print("Creating tables and filling them with data...")
    language_freq = os.path.join('data', 'language.txt')
    init_word_freq_table('language',language_freq,True)
    print("========Done========")
```
the word language must be change to the language you want to add (in lower case).\
The path to the frequency file is relative to the db.py file.

the language should be in https://github.com/kkrypt0nn/wordlists/tree/main/wordlists/languages (gets use to double check the language)\
and have the same name as here.

if not you can disable this doubble check by changing True to False in the init_word_freq_table function.(db.py line 417)
```python
  init_word_freq_table('language',language_freq,False)
```

then run db.py and wait until its done. this could take up to 10 minutes for large frequency lists.
```bash
python3 db.py
```

to be able to pick your language in the game it needs to be added at two other positions:
1. in the models.py file at line 10 add the name of your language to the list
```python
# set the language
languages = ['german', 'english','your_language']
```
1. in the menu.py file at line 93 add the name of your language to the dicitonary and an corresponding emoji (or a blank string if you dont want to use one)
```python
    # language flag dictionary
    dict = {'english': '🇬🇧', 'german': '🇩🇪', 'your_language': '🦤' }
```

**and now you good to go and have fun with your language!**

### troubleshooting
if the code can't be run because of the emojis in the menu.py file, you can remove them or replace them with a blank string.
(line 93)
```python
    # language flag dictionary
    dict = {'english': ' ', 'german': ' ' }
```

if you get an `sqlite3.OperationalError: no such table:...` error.
1. try again to see if the error is persistent.
2. replace your databse `data/words.sqlite` with the one from the repo (this will reset all the scoretables and the language)
3. reinstall the game.
4. if nothing works please open an issue.