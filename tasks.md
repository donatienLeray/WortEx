# Task List

Linguistic gaming with Python Final Project. A german word game heaviliy inspired by https://wordhub.com

## Project Structure

> [!WARNING]  
> This is just an idea not sure about it at all

```
WortEx/
    main.py
    words.py
    points.py
    start.py
    resources/
        fonts/
            Arial_custom.tff
        sounds/
            beep.wav
            right.wav
            wrong.wav
            bonus.wav
            game_over.wav
        images/
            backgound.png
    data/
        7_words.txt
        german.txt
    requirements.txt
    README.md
    tasks.md
    .gitignore
```


## Backend

### Starting Script

- [ ] 1. Before a game can be luched check if all neede dependencys are installed. (python > 3.6, win: findstr, else : grep or rgrep)

- [ ] 2. run `pip install -r requirements.txt`

### Loading Words (Dodo)

- [ ] 0. Make a database (id:word, multiplicator, [all possible awsers]) use (https://pandas.pydata.org/docs/) 

- [x] 1. have a list with all german words with seven letters (Dodo)
  - [ ] 1.1 Sort them by difficulty (see [Point System](/tasks.md#point-system))

- [ ] 2. choose one of them randomly according to given diffivulty (Dodo)

- [ ] 3. for each 7 letter word make a lookuptable containing the multiplicator ((1 / med sscore ) * difficulty) needed to calculate the points (Dodo) and information on how many words are possible (>7 and 7). see [Point System](/tasks.md#point-system) (Dodo)
  - [ ] 3.1 make getter funktion for all prprocessed information (Dodo)

### User Input

- [ ] 1. make a list of already found words

- [ ] 2. Read user input while he types

- [ ] 3. user can only type letters that are in the given letters

- [ ] 4. user can only type letters that are not already used

- [ ] 5. if user types something that is not allowed, it just gets ignored

- [ ] 6. display the typed letters in the correct order

- [ ] 7. if the typed letters are a valid word and not found yet, add it to the list of found words and reset input

- [ ] 8. if user press 'esc' reset input

- [ ] 9. if user press 'enter' check if the typed letters, reset input whatsoever

- [ ] 10. if user press 'backspace' delete last typed letter

### Point System

- [ ] 1. Display how many words are possible with the given letters and how many are already found 

- [ ] 2. Display all found words (sorted by length, then alphabetically)

- [ ] 3. Display the score at all times

- [ ] 2. the score is updated when the user finds a new word

- [ ] 3. Diplay how many words with 7 letters are possible and how many are already found

- [ ] 3. Words with 7 letters give you +10 seconds

#### Score Calculation

- [ ] 1. Method to calculate Scrable Score 

- [ ] 2. Methode to calculate points 

**possible words** = number of possible words (preprossesed) (Dodo)

**std dev** = standard deviation of all scrabble scores of all possible words (https://en.wikipedia.org/wiki/Standard_deviation) (preprossesed) (dodo)


<details>
<summary>How to calculate the standard deviation</summary>
<br>

1. Calculate the Mean (Average):

$$\text{Mean} (\bar{x}) = \frac{\text{Sum of all values}}{\text{Number of values}}$$

2. Calculate the Deviations:

$$\text{Deviation from Mean} = \text{Value} - \text{Mean}$$

3. Square the Deviations:

$$\text{Squared Deviation} = (\text{Deviation from Mean})^2$$

4. Calculate the Variance:

$$\text{Variance} (\sigma^2) = \frac{\text{Sum of Squared Deviations}}{\text{Number of values}}$$

5. Calculate the Standard Deviation:

$$\text{Standard Deviation} (\sigma) = \sqrt{\text{Variance}}$$

In summary:

$$\sigma = \sqrt{\frac{\sum{(x - \bar{x})^2}}{N}}$$

where $\sigma$ is the standard deviation, $x$ is each individual value, $\bar{x}$ is the mean, and $N$ is the number of values.

If working with a sample, use the sample standard deviation formula, involving dividing by $N-1$ to correct for bias in the estimation of the population variance.

</details>
<br>

(TODO: difficulty depending on med sscore and std dev)
```
possible words <= 20 = 1.5     #hard
possible words <= 50 = 1.2     #medium
possible words >  50 = 1       #easy 
```

**scrabble score** = scrabbel score of given word

**total sscore** = sum of scrable scores of all found words

**med sscore** = median off all scrabble scores of all possible words

**multiplicator** = (1 / med sscore ) * difficulty (preprossesed) (dodo)

**score** = scrabble score * multiplicator (calculated on the go)

### Time

- [ ] 1. The user has 120 seconds to find as many words as possible

- [ ] 2. Display the remaining time

- [ ] 3. When the time is up, display the score

## Frontend

TODO

Design: Do somehing with the name of the game (WortEx, Vortex)

## Extras

Use https://github.com/bndr/pipreqs to generate requirements.txt

```bash
pipreqs . --force
```
