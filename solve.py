import copy
import pandas as pd

# A dict used to memoize the results of is_match
memoize = {}

# Represents a game state
class State:
    # Constructor for the game state
    # exact: a dict from letter to a list of positions that it is
    # contains: a dict from letter to an array of positions that it isn't
    # absent: a list of letters that aren't in the word
    def __init__(self, exact, contains, absent):
        self.exact = exact
        self.contains = contains
        self.absent = absent
        self.update_string()

    # Update the string representation whenever fields change
    def update_string(self):
        self.string = str(self.exact) + ',' + str(self.contains) + ',' + str(self.absent)

    # Returns a deep copy of the state
    def clone(self):
        return State(
            copy.deepcopy(self.exact),
            copy.deepcopy(self.contains),
            self.absent.copy()
        )

    # Returns a string representation of the class
    def __str__(self):
        return self.string

    # Returns whether the word is a match given the state
    def is_match(self, word):
        memo_key = str(self) + word
        if memo_key in memoize:
            return memoize[memo_key]
        memoize[memo_key] = False
        # Check that all the exact characters match
        for key, value in self.exact.items():
            for i in value:
                if word[i] != key:
                    return False
        # Check that contains items exist in valid indices
        for key, value in self.contains.items():
            indices = [i for i, ltr in enumerate(word) if ltr == key]
            # If the character is missing, return False
            if len(indices) == 0:
                return False
            # If the character isn't in another index, return False
            if len([i for i in value if i not in indices]) == 0:
                return False
        # Check that the word doesn't contain absent letters
        for key in self.absent:
            if key in word:
                return False
        memoize[memo_key] = True
        return True

    # Adds the character as an exact match
    def add_exact(self, char, i):
        if char not in self.exact:
            self.exact[char] = []
        if i not in self.exact[char]:
            self.exact[char].append(i)

    # Adds the character as a contains match
    def add_contains(self, char, i):
        if char not in self.contains:
            self.contains[char] = []
        if i not in self.contains[char]:
            self.contains[char].append(i)

    # Adds the character as absent
    def add_absent(self, char):
        if char not in self.absent:
            self.absent.append(char)

    # Returns a new state based on an answer and guess
    def guess(self, answer, guess):
        state = self.clone()
        for i in range(5):
            if answer[i] == guess[i]:
                state.add_exact(guess[i], i)
            elif guess[i] in answer:
                state.add_contains(guess[i], i)
            else:
                state.add_absent(guess[i])

        state.update_string()
        return state

    # Updates the state to reflect the results of a guess
    def update(self, guess, result):
        if len(result) != 5 or len(guess) != 5:
            raise ValueError("Guess must be 5 characters")
        for i, (g, r) in enumerate(zip(guess, result)):
            if r == "Y":
                self.add_exact(g, i)
            elif r == "O":
                self.add_contains(g, i)
            else:
                self.add_absent(g)
        self.update_string()


# Read in all possible words and possible solutions
f = open("5words.txt", "r")
words = f.read().split("\n")
f = open("5solutions.txt", "r")
solutions = f.read().split("\n")

# Current game state
state = State({}, {}, [])

def calc_score(guess, answer):
    temp_state = state.guess(answer, guess)
    return len(list(filter(lambda w: not temp_state.is_match(w), filtered_words)))

# Loop for all entries
for x in range(1, 7):
    # Eliminate any non-matching words
    filtered_words = list(filter(state.is_match, solutions))
    guessed_word = None

    if len(filtered_words) == 0:
        print("Found no matching words")
        break
    elif len(filtered_words) == 1:
        guessed_word = filtered_words[0]
    elif x == 1:
        # Always returns the same first word so might as well hardcode for performance
        guessed_word = "soare"
    else:
        series_rows = pd.Series(words)
        series_cols = pd.Series(filtered_words)
        df = pd.DataFrame(series_rows.apply(lambda x: series_cols.apply(lambda y: calc_score(x, y))))
        df.index = series_rows
        guessed_word = df.sum(axis=1).idxmax()

    print("Guess #", x, ": ", guessed_word)
    print("Y for correct letter & location")
    print("O for correct letter & wrong location")
    print("N for incorrect letter")
    result = input("What was the result of the guess? ")
    if result == "YYYYY":
        break
    state.update(guessed_word, result)
    memoize = {}

# 1/8
# word: crank
# guesses: soare, clint, crank

# 1/9
# word: gorge
# guesses: soare, faugh, gorge