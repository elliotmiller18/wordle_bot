from sys import argv

class Game:

    def add_guess(self, guess):
        self.guesses.append(guess)

    def check_win(self, answers) -> bool:
        for answer in answers:
            if answer != 'G':
                self.correct = False
                return False
        self.correct = True
        return True

    def check_guess(self, guess) -> list:
        answers = ['*'] * 5
        # '0' for green
        # '1' for yellow
        # pass 1: assign greens and mark 
        temp = self.target
        for i, c in enumerate(self.target):
            if guess[i] == c:
                answers[i] = 'G'
                temp = temp[0:i] + '*' + temp[i+1:]
        # pass 2: assign yellows and mark
        for i in range(len(temp)):
            if answers[i] == 'G':
                continue
            if guess[i] in temp:
                answers[i] = 'Y'
                temp = temp.replace(guess[i], '*', 1)
        self.check_win(answers)
        return answers
            

    def __init__(self, target):
        self.correct = False
        self.target = target
        self.guesses = []

    def print_guess(self, guess: str, answers: list):
        for i, g in enumerate(guess):
                if answers[i] == 'G':
                    print(f"\033[92m{g}\033[0m", end="")
                elif answers[i] == 'Y':
                    print(f"\033[93m{g}\033[0m", end="")
                else:
                    print(g, end="")
        # newline
        print()