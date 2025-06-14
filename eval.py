import csv
from heapq import heapify, heappop
from collections import Counter
from sys import argv
from wordle import Game
from string import ascii_lowercase

words = list()
# priority queue of words by frequency
most_common_words = list()

def trim_allowed(allowed: list, answers: list, guess: str):
    yellow = set()
    for i, answer in enumerate(answers):
        g = guess[i]
        if answer == 'G':
            allowed[i] = set(g)
        elif answer == 'Y':
            yellow.add(g)
            if g in allowed[i]:
                allowed[i].remove(g)
        elif g not in yellow:
            for j in range(len(allowed)):
                if g in allowed[j] and len(allowed[j]) > 1:
                    allowed[j].remove(g)

def get_guess(allowed: list, used: dict) -> str:
    while True:
        valid = True
        word = heappop(most_common_words)[1]
        for i, c in enumerate(word):
            if c not in allowed[i]:
                valid = False
        cnt = Counter(word)
        for k in used:
            if k not in cnt or used[k] > cnt[k]:
                valid = False
        if valid:
            return word

def main():

    target = argv[1]
    probing = 'aeros' if len(argv) <= 2 else argv[2]

    with open('wordle.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            words.append(row[0])
            # dont add probing guess to guesses q
            if row[0] == probing:
                continue
            most_common_words.append( (float(row[1])*-1, row[0]) )
    heapify(most_common_words)

    assert(target in words and probing in words)

    game = Game(target)
    allowed = list()
    for _ in range(5):
        allowed.append(set(ascii_lowercase))

    guess = probing

    while True:
        answers = game.check_guess(guess)
        game.add_guess(guess)
        game.print_guess(guess, answers)
        if game.correct:
            break

        trim_allowed(allowed, answers, guess)
        used = dict()
        for i, a in enumerate(answers):
            if a != '*':
                if guess[i] in used:
                    used[guess[i]] += 1
                else:
                    used[guess[i]] = 1
        guess = get_guess(allowed, used)

    print(f"guesses: {len(game.guesses)}")
if __name__ == "__main__":
    main()