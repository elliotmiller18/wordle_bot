import csv
from heapq import heapify, heappop, heappush
from collections import defaultdict, Counter, deque
from sys import argv
from wordle import Game
from string import ascii_lowercase

words = list()
# priority queue of words by frequency
most_common_words = list()

def trim_allowed(allowed: list, answers: list, guess: str):
    for i, answer in enumerate(answers):
        g = guess[i]
        if answer == 'G':
            allowed[i] = set(g)
        elif answer == 'Y':
            if g in allowed[i]:
                allowed[i].remove(g)
        else:
            for j in range(len(allowed)):
                if g in allowed[j]:
                    allowed[j].remove(g)

def get_guess(allowed: list) -> str:
    while True:
        word = heappop(most_common_words)
        for i, c in enumerate(word):
            if c not in allowed[i]:
                continue
        return word

def main():
    with open('wordle.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            words.append(row[0])
            most_common_words.append( (float(row[1])*-1, row[0]) )
    heapify(most_common_words)

    target = argv[1]
    probing = argv[2]
    assert(target in words and probing in words)

    game = Game(target)
    allowed = list()
    for _ in range(5):
        allowed.append(set(ascii_lowercase))

    print(f"guesses: {len(game.guesses)}")
    guess = probing

    while not game.correct:
        answers = game.check_guess(guess)
        game.add_guess(guess)
        game.print_guess(guess, answers)
        trim_allowed(allowed, answers, guess)
        guess = get_guess(allowed)
if __name__ == "__main__":
    main()