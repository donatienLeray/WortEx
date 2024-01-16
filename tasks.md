# Task List

Linguistic gaming with Python Final Project. A german word game heaviliy inspired by https://wordhub.com

## Project structure

> [!WARNING]  
> This is just an idea not sure about it at all

```
WortEx/
    main.py
    word.py
    points.py
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
        words.txt
```


## Backend

### Loading words

- [x] 1. have a list with all german words with seven letters (Dodo)

- [x] 2. choose one of them randomly and display it letters in a random order (Dodo)

- [x] 3. Load all words with 3-7 letters that are possible with the given letters (each letter can only be used once) (Dodo)

- [ ] 4. implement (3.) in an effective way (<= 5 seconds) (dodo)


### User input

- [ ] 1. make a list of already found words

- [ ] 2. Read user input while he types

- [ ] 3. user can only type letters that are in the given letters

- [ ] 4. user can only type letters that are not already used

- [ ] 5. if user types something that is not allowed, it just gets ignored

- [ ] 6. display the typed letters in the correct order

- [ ] 7. if the typed letters are a valid word and not find yet, add it to the list of found words and reset input

- [ ] 8. if user press 'esc' reset input

- [ ] 9. if user press 'enter' check if the typed letters, resset input whatsoever

- [ ] 10. if user press 'backspace' delete last typed letter

### Point system

- [ ] 1. Display how many words are possible with the given letters and how many are already found 

- [ ] 2. Display all found words (sorted by length, then alphabetically)

- [ ] 3. Display the score at all times

- [ ] 2. the score is updated when the user finds a new word

- [ ] 3. Diplay how many words with 7 letters are possible and how many are already found

- [ ] 3. Words with 7 letters give you +10 seconds

#### Score calculation

possible words = number of possible words

std dev = standard deviation of all scrabble scores of all possible words (https://en.wikipedia.org/wiki/Standard_deviation)


<details>
<summary>How to calculate the standard deviation</summary>
<br>

1. Calculate the Mean (Average):

$$ \text{Mean} (\bar{x}) = \frac{\text{Sum of all values}}{\text{Number of values}} $$

2. Calculate the Deviations:

$$ \text{Deviation from Mean} = \text{Value} - \text{Mean} $$

3. Square the Deviations:

$$ \text{Squared Deviation} = (\text{Deviation from Mean})^2 $$

4. Calculate the Variance:

$$ \text{Variance} (\sigma^2) = \frac{\text{Sum of Squared Deviations}}{\text{Number of values}} $$

5. Calculate the Standard Deviation:

$$ \text{Standard Deviation} (\sigma) = \sqrt{\text{Variance}} $$

In summary:

$$ \sigma = \sqrt{\frac{\sum{(x - \bar{x})^2}}{N}} $$

where $ \sigma $ is the standard deviation, $ x $ is each individual value, $ \bar{x} $ is the mean, and $ N $ is the number of values.

If working with a sample, use the sample standard deviation formula, involving dividing by $ N-1 $ to correct for bias in the estimation of the population variance.\

</details>
<br>

(dificulty depending from med sscore and std dev)
difficulty | possible words <= 20 = 1.5     #hard
           | possible words <= 50 = 1.2     #medium
           | possible words > 50  = 1       #easy

scrabble score = scrabbel score of given word

total sscore = sum of scrable scores of all found words

med sscore = median off all scrabble scores of all possible words

score = scrabble score * (1 / med sscore ) * difficulty

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
