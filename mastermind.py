import random
import os

class Mastermind:

    def __init__(self):

        # Initialize the variables used for the mastermind game.
        self.guesses = 0
        self.maxGuesses = 12
        self.colourOptions = ['R', 'G', 'B', 'Y', 'O', 'P']
        self.secret_sequence = self.generateSequence()
        self.guessHistory = []
        self.correctAnswer = False

        # Starting the gameloop
        self.startGame()

    def generateSequence(self):
        # random.choices takes input (list, int) where it then takes int amount of picks from the list and creates a new array from these
        secret = random.choices(self.colourOptions, k=4)
        
        return secret
    
    def checkColours(self, guess):
        colourChecker = {'R':0, 'G':0, 'B':0, 'Y':0, 'O':0, 'P':0}

        # Subtract one from each dictionary entry for each appearence in the secret sequence
        for colour in self.secret_sequence:
            colourChecker[colour] -=1
        
        # Adds 1 to the dictionary colours that has been guessed(where correct guesses will move towards 0 and wrong guesses away from 0)
        for colour in guess:
            colourChecker[colour] +=1

        # Sums the values stored in colourChecker.
        colourSum = 0
        for colour in colourChecker:
            colourSum += abs(colourChecker[colour])

        # The amount of correct colours will be 4 (max amount) with the colourSum divided by two subtracted (Division by 2 is due to each wrong having both a colour not being set to 0 and a color being removed from 0)
        correctColours = 4 - (colourSum / 2)

        return correctColours
    

    # Compares each element in the guess with the same placement element in the secret_sequence and sums them together to see correct placements
    def checkPlacement(self, guess):

        placementSum = 0

        for i in range(len(guess)):
            placementSum += self.secret_sequence[i] == guess[i]

        return placementSum

    def makeGuess(self):
        # Take guess input from player and checks whether a valid guess or not
        guess = ""


        # While loop to that asks for a guess until a guess of correct format is given
        while True:
            guess = input('Input your guess (Write 4 colour, e.g. RGBY):').upper()
            guess = list(guess)
            valid = True
            if len(guess) == 4:
                for i in guess:
                    if i in self.colourOptions:
                        continue
                    else:
                        valid = False
            else:
                valid = False

            if valid:
                break
            else:
                print(f"Invalid input, please write 4 colours, in the format 'XXXX', where the colour options are: {"|".join(self.colourOptions)}")
                continue
        
        correctPlacement = self.checkPlacement(guess)
        correctColours = self.checkColours(guess) - correctPlacement


        # Keeps track of guesses so far.
        self.guessHistory.append([guess, correctColours, correctPlacement])
        self.guesses += 1

        # Checks if the guess just made was a correct guess.
        if correctPlacement == 4:
            self.correctAnswer = True


    # Prints out the gameboard, this is run after every guess
    def printGame(self):
        os.system('cls' if os.name == 'nt' else 'clear')

        print('Current Mastermind board:\n')

        # Loops through the guesses made so far and prints them out such that they can be analysed for making the next guess
        print("_____________________________________________________________________________\n")
        for index, guess in enumerate(self.guessHistory):
            print(f'{"".join(guess[0])}  | Guess {index} | Correct colours: {guess[1]} | Correct colour and placements: {guess[2]}')
        print("_____________________________________________________________________________")
        print(f'\nYou have {self.maxGuesses-self.guesses} guesses left.')
        print('\nThe possible colours are:\n(R)ed, (G)reen, (B)lue, (Y)ellow, (O)range, (P)urple\n')


    def startGame(self):

        # Printing of the game interface
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Welcome to mastermind, a sequence of four colours have been generated.')
        print('Your job is now to decipher this sequence.')
        print('The possible colours are:\n(R)ed\n(G)reen\n(B)lue\n(Y)ellow\n(O)range\n(P)urple\n')

        # Game loop that runs until correct guess or max guesses has exceeded
        while(self.guesses < self.maxGuesses and not self.correctAnswer):
            self.makeGuess()
            self.printGame()

        
        # Result is printed
        secretStr = "".join(self.secret_sequence)
        if self.correctAnswer:
            print(f'\n\nCongratulation you deciphered the sequence.\nThe secret sequence was: {secretStr}')
        
        else:
            print(f"\n\nUnfortunately you didn't decipher the sequence in time.\nThe secret sequence was: {secretStr}")

    



if __name__ == "__main__":
    
    # Starts a game loop such that it is possible for the player to start a new game without rerunning the program.
    while(True):
        mastermind = Mastermind()


        resume = input('Do you wish to play again? (y/n)\n').lower()
        while(True):
            if resume != "n" and resume != "y":
                resume = input('Invalid answer, please answer with (y) for yes or (n) for no\n')
            else:
                break
        if resume == "n":
            break



