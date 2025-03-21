import csv
from heapq import heapify, heappop, heappush
from collections import defaultdict, Counter, deque
from sys import argv

#TODO: fix toned

class Guess:
    def check_guess(self, guess) -> list:
        answers = ['N'] * 5
        self.guesses.append(guess)
        for i in range(len(self.target)):
            if guess[i] == self.target[i]:
                answers[i] = 'G'
            elif guess[i] in self.target:
                answers[i] = 'Y'
        for answer in answers:
            if answer != 'G':
                self.correct = False 
                return answers
        self.correct = True
        return answers

    def __init__(self, target):
        self.guesses = []
        self.target = target

common_words = list()
common_words_set = set()
all_words = list()
# priority queue of chars by frequency
most_common_chars = []

def get_valid_guesses(chars: dict) -> list:
        guesses = list()
        # collect all guesses
        for word in all_words:
            if Counter(word) == chars:
                guesses.append(word)
        return guesses

def main():
    with open('wordle.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 3:
                common_words.append(row[0])
            all_words.append(row[0])
    # check if provided word is a word in our db
    assert(argv[1] in all_words)
    # find frequency dict of characters in all words
    freq = defaultdict(int)
    common_words_set = set(common_words)
    for word in common_words:
        for c in word:
            freq[c] += 1
    # create priority queue of most used characters
    for c, f in freq.items():
        # heapq in python is minheap so we need to multiply by neg 1
        most_common_chars.append((f*-1, c))

    heapify(most_common_chars)
    used_chars = list()
    target = argv[1]
    guess = Guess(target)

    while True:
        # get used_chars + most_common chars 
        guess_chars = used_chars.copy()
        guesses = []
        removed = deque()
        original_chars = most_common_chars.copy()
        # the index of the least common
        worst = 4
        # populate list of guesses
        while len(guesses) == 0:
            # if we've removed the entire heap reset it and start removing the next worth character
            if len(most_common_chars) == 0:
                worst -= 1
                assert(worst >= len(used_chars))
                most_common_chars.append(original_chars)
            # remove the character at the least common spot
            if len(guess_chars) > len(used_chars):
                del guess_chars[worst]
            while len(guess_chars) < 5:
                val = heappop(most_common_chars)
                guess_chars.append(val[1])
                removed.append(val)
            guesses = get_valid_guesses(Counter(guess_chars))
        best_guess = guesses[0]
        for g in guesses:
            if g in common_words_set:
                best_guess = g
                break
        # create guess
        answers = guess.check_guess(guesses[0])
        # we have to at least remove the first guess
        all_words.remove(guesses[0])
        # if we have at least one miss we have to remove all other words from our wordbank as none of them can be right, nor will they give us more useful info
        if 'N' in answers:
            for i in range(1, len(guesses)):
                all_words.remove(guesses[i])

        # set for characters we don't want to reuse if we don't have to
        unused_chars = set()

        for i, g in enumerate(guesses[0]):
            if answers[i] == 'G':
                print(f"\033[92m{g}\033[0m", end="")
            elif answers[i] == 'Y':
                print(f"\033[93m{g}\033[0m", end="")
            else:
                unused_chars.add(g)
                print(g, end="")
            if answers[i] != 'N' and g not in used_chars:
                used_chars.append(g)
        print()

        for pair in removed:
            if pair[0] in unused_chars:
                # the highest is 6000 so 10000 will work
                pair[0] += 10000
            heappush(most_common_chars, pair)

        if guess.correct:
            break
        #print(guesses[0])
    print(f"guesses: {len(guess.guesses)}")
             

if __name__ == "__main__":
    main()