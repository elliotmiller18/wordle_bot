import csv
from heapq import heapify, heappop, heappush
from collections import defaultdict, Counter, deque
from sys import argv

#TODO: fix aeros

class Game:

    def add_guess(self, guess):
        self.guesses.append(guess)

    def check_win(self) -> bool:
        for answer in self.answers:
            if answer != 'G':
                self.correct = False
                return False
        return True

    def check_guess(self, guess) -> list:
        self.answers = ['*'] * 5
        for i in range(len(self.target)):
            if guess[i] == self.target[i]:
                self.answers[i] = 'G'
            elif guess[i] in self.target:
                self.answers[i] = 'Y'
        return self.answers
    
    def get_guess(self) -> str:
        guess = self.guesses[-1]
        while True:
            # get word without frequency
            word = heappop(most_common_words)[1]
            temp = word
            valid = True
            for i, color in enumerate(self.answers):
                if color == 'G':
                    if word[i] != guess[i]:
                        valid = False
                        break
                elif color == 'Y':
                    if guess[i] == word[i] or guess[i] not in temp:
                        valid = False
                        break
                    # remove that character in case we have 2 or 3 yellows with the same letter
                    temp = temp.replace(guess[i],"*",1)
            if valid:
                return word
            

    def __init__(self, target, probing):
        self.correct = False
        self.target = target
        self.answers = ['*'] * 5
        self.guesses = [probing]
        self.check_guess(probing)

    def print_guess(self, guess: str):
        for i, g in enumerate(guess):
                if self.answers[i] == 'G':
                    print(f"\033[92m{g}\033[0m", end="")
                elif self.answers[i] == 'Y':
                    print(f"\033[93m{g}\033[0m", end="")
                else:
                    print(g, end="")
        print()


words = list()
# priority queue of words by frequency
most_common_words = list()

def main():
    with open('wordle.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            words.append(row[0])
            most_common_words.append( (float(row[1])*-1, row[0]) )
    heapify(most_common_words)
    # check if provided word is a word in our db
    assert(argv[1] in words)

    target = argv[1]
    probing = argv[2]
    game = Game(target, probing)
    game.print_guess(probing)

    while not game.check_win():
        
        guess = game.get_guess()
        game.add_guess(guess)
        game.check_guess(guess)
        game.print_guess(guess)

    print(f"guesses: {len(game.guesses)}")

if __name__ == "__main__":
    main()