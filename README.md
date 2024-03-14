# WortEx

WortEx is a fun way to learn new words that you haven't heard of.
It challenges you to form as many words as possible given a 
set of seven letters. Be fast, be smart, get a highscore!

- [WortEx](#wortex)
      - [Table of contents](#table-of-contents)
    - [Dependencies](#dependencies)
    - [How to run](#how-to-run)
    - [How to play](#how-to-play)
    - [Add your own language!](#add-your-own-language)
    - [Change background](#change-background)
    - [Troubleshooting](#troubleshooting)

### Dependencies

- Python version >= 3.6
  check with `python --version`

Normally the dependencies are installed automaticly by main.py
If not, run:
```bash
pip install -r requirements.txt
```

### How to run
Open you terminal and navigate to the folder where you downloaded the game.\
Then run:
```bash
python3 main.py
```

### How to play

choose a language and difficulty and press play.

You get a set of seven letters and have to type the letters on the screen to
form words that exitst in that language.

You can press `Esc` you reset your input. With `Backspace` you can delete one
letter of you input.

### Add your own language!

Good frequency lists (>10.000) a hard to find. Thats why we so far only support **english and german**.

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
It does not need to be sorted, but the words have to be separated by a tab and the frequency has to be an integer.\
None latin charachters are not supported yet. (words with such will be ignored)\
All words will be converted to lower case.

Run the db.py file it will ask you for the language name and the path to the frequency list.\
```bash
python3 db.py
```

The languages get double checked to filter out mistakes, foreign words and names.\
Therefor the language should be in https://github.com/kkrypt0nn/wordlists/tree/main/wordlists/languages \
and have the same name as here.

If it can't be found there double check will be disabled.\
You will be ask if you want to continue.

Preparing the database can take a while, depending on the size of the frequency list. (2-10 minutes)\
You should not interrupt the process until it is done.

If you want to add an emoji for your language, you can do it by adding it to the dictionary in the menu.py file at line 109.
```python
    # language flag dictionary
    dict = {'english': '🇬🇧', 'german': '🇩🇪', 'your_language': '🦤' }
```

**Now you good to go and have fun with your language!**

### Change background

Just replace the file `data/background.png` and `data/game_background.png` with your own images.\
The name has to stay exactly the same.

### Troubleshooting
If the code can't be run because of the emojis in the menu.py file, you can remove them or replace them with a blank string.
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
