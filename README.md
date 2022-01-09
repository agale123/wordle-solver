# Wordle Solver

This is a solver for the Wordle game that can be found
[here](https://www.powerlanguage.co.uk/wordle/). For the solver, run:

```
python solve.py
```

It will print out the guesses one at a time. After each guess, type in the
feedback from the game. When giving feedback, 'Y' represents a letter in the
correct position, 'O' represents a letter in an incorrect position, and 'N'
represents a character that isn't in the word.

## Algorithm

At a high level, the solver looks at each possible word it can guess and
calculates the average number of words would be eliminated from the set
of possible words. The guess that eliminates the most words on average is
selected. Since the first guess is always the same, that is hardcoded. The
second guess takes a while to compute but subsequent guesses are typically
fast.