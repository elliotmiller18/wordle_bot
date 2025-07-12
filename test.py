import csv
import subprocess

def main(): 
    valid_words = []
    with(open('wordle.csv', 'r') as file):
        reader = csv.reader(file)
        for row in reader:
            if float(row[1]) > 1e-5:
                valid_words.append(row[0])

    guess_total = 0
    checked = 0
    for word in valid_words:
        cp = subprocess.run(
            ['python3', 'eval.py', word, 'aeros'],
            capture_output=True,
            text=True,
            check=True
        )
        guess_total += int(cp.stdout.rstrip().splitlines()[-1].split(" ")[-1])
        checked += 1
        print(f'average guesses = {guess_total / checked}')
    
    print(f'average guesses = {guess_total / len(valid_words)}')

if __name__ == "__main__":
    main()
