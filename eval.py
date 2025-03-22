import csv
from heapq import heapify, heappop, heappush
from collections import defaultdict, Counter, deque
from sys import argv

#TODO: fix aeros

class Game:
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
all_words = list()
# priority queue of words by frequency
most_common_words = list()

def print_guess(answers: list, guess: str):
    for i, g in enumerate(guess):
            if answers[i] == 'G':
                print(f"\033[92m{g}\033[0m", end="")
            elif answers[i] == 'Y':
                print(f"\033[93m{g}\033[0m", end="")
            else:
                print(g, end="")
    print()

def get_guess(green: list, yellow: dict) -> str:
    while True:
        valid = True
        word = heappop(most_common_words)[1]
        for i, g in enumerate(green):
            if g != word[i] and g != '*':
                valid = False
                break
        # v is the number k in the yellow letters
        for k, v in yellow.items():
            temp = list(word)
            for _ in range(v):
                try:
                    temp.remove(k)
                except ValueError:
                    valid = False 
                    break
        if valid:
            return word

def main():
    with open('wordle.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 3:
                common_words.append(row[0])
            all_words.append(row[0])
            most_common_words.append( (float(row[1])*-1, row[0]) )
    heapify(most_common_words)
    # check if provided word is a word in our db
    assert(argv[1] in all_words)

    target = argv[1]
    game = Game(target)

    green = ["*"] * 5
    yellow = defaultdict(int)

    while True:
        guess = get_guess(green, yellow)
        answers = game.check_guess(guess)
        print_guess(answers, guess)

        if game.correct:
            break

        yellow = defaultdict(int)
        for i, answer in enumerate(answers):
            if answer == 'G':
                green[i] = guess[i]
            else:
                green[i] = '*'
            if answer == 'Y':
                yellow[guess[i]] += 1
    print(f"guesses: {len(game.guesses)}")

if __name__ == "__main__":
    main()