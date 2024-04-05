# Name: Armaan Hirani
# UTEID: ah62954

# all adopted from master_mind.py, letter_typing.py, and assignmnet 1 code

import random
from tkinter import *
from tkinter import ttk

class Logic:
    def __init__(self):
        self.row = 0
        self.col = 0
        self.game_over = False
        self.guesses = 0
        self.__secret_words, self.__all_words = self.get_words()
        self.__secret_word = self.get_secret_word()
        print(self.__secret_word)

    def new_game(self):
        self.row = 0
        self.col = 0
        self.game_over = False
        self.guesses = 0
        self.__secret_word = self.get_secret_word()

    def get_words(self):
        """ Read the words from the dictionary files.
            We assume the two required files are in the current working directory.
            The file with the words that may be picked as the secret words is
            assumed to be names secret_words.txt. The file with the rest of the
            words that are valid user input but will not be picked as the secret
            word are assumed to be in a file named other_valid_words.txt.
            Returns a sorted tuple with the words that can be
            chosen as the secret word and a set with ALL the words,
            including both the ones that can be chosen as the secret word
            combined with other words that are valid user guesses.
        """
        temp_secret_words = []
        with open('secret_words.txt', 'r') as data_file:
            all_lines = data_file.readlines()
            for line in all_lines:
                temp_secret_words.append(line.strip().upper())
        temp_secret_words.sort()
        secret_words = tuple(temp_secret_words)
        all_words = set(secret_words)
        with open('other_valid_words.txt', 'r') as data_file:
            all_lines = data_file.readlines()
            for line in all_lines:
                all_words.add(line.strip().upper())
        return secret_words, all_words

    def get_win_conditions(self):
        """
        Return a dictionary with the outputs based on win conditions.
        """
        return {1:'You win. Genius!', 2:'You win. Magnificent!', 
                3:'You win. Impressive!', 4:'You win. Splendid!', 
                5:'You win. Great!', 6:'You win. Phew!'}


    def get_secret_word(self):
        """
        Get a random word from the list of secret words.
        """
        return random.choice(self.__secret_words)

    def is_valid(self, guess):
        """
        Check if the guess is valid.
        """
        print(guess)
        return guess in self.__all_words and len(guess) == 5

    def play_round(self, guess):
        """
        Get a guess from the user and validate it.
        Precondition: guess is valid
        """

        if self.guesses < 6 and not self.game_over:
            self.guesses += 1
            output = self.output(guess)
            if guess == self.__secret_word:
                self.game_over = (True, True)
                return self.get_win_conditions()[self.guesses]
            elif self.guesses < 6:
                return output
            else:
                self.game_over = (True, False)
                return 'Not quite. The secret word was ' + self.__secret_word
        else:
            return 'Game Over. Please start a new game'
    
    def output(self, guessed_word):
        """
        Handle the output for the guessed word.
        """
        currentPattern = ['-', '-', '-', '-', '-']
        temp = list(self.__secret_word)
        for i in range(len(guessed_word)):
            if guessed_word[i] == temp[i]:
                currentPattern[i] = 'G'
                temp[i] = '*'
        for i in range(len(guessed_word)):
            if guessed_word[i] in temp and not currentPattern[i] == 'G':
                currentPattern[i] = 'O'
                temp[temp.index(guessed_word[i])] = '*'
        return ''.join(currentPattern)


def main():
     # Set the seed to make grading easier.
    # Final version turned in must have this line
    # of code. First three words with this seed
    # should be AFFIX, PROXY, APING
    random.seed(3252024)
    root = Tk()
    root.geometry("400x600")
    root.title("Wordle")
    root.resizable(False, False)
    board = Logic()
    labels = create_grid(root)
    guess = []
    feedback_label = create_control_buttons(root, labels, guess, board)

    root.bind(
        '<KeyPress>', lambda event: update_letter(event.char, labels, board),
    )

    root.bind(
        '<Return>', lambda event: make_guess(labels, board, feedback_label),
    )

    root.bind(
        '<BackSpace>', lambda event: delete_letter(labels, board),
    )

    root.mainloop()

def update_letter(letter, labels, board):
    print(letter)
    if letter.isalpha() and not board.game_over and board.col < 5:
        letter = letter.upper()
        label = labels[board.row][board.col]
        label.configure(text=letter)
        board.col += 1

def delete_letter(labels, board):
    if board.col > 0:
        board.col -= 1
        labels[board.row][board.col].configure(text=' ')

def new_game(labels, board, feedback_label):
    board.new_game()
    for row in labels:
        for label in row:
            label.configure(text=' ', bg='systemWindowBackgroundColor')
    feedback_label.config(text='')

def make_guess(labels, board, feedback_label):
    feedback_label.config(text='')
    if board.col == 5:
       
        compiledGuess = ''
        for i in range(len(labels[board.row])):
            compiledGuess += labels[board.row][i].cget('text')
        
        if not board.is_valid(compiledGuess):
            feedback_label.config(text='I don\'t know that word.')
        else: 
            feedback = board.play_round(compiledGuess)
            if board.game_over:
                feedback_label.config(text=feedback)
                if board.guesses != 6:
                    for i in range(len(feedback)):
                        labels[board.row][i].configure(bg='green')

            else:
                for i in range(len(feedback)):
                    let = feedback[i]
                    if(let == 'G'):
                        labels[board.row][i].configure(bg='green')
                    elif(let == 'O'):
                        labels[board.row][i].configure(bg='orange')
                    else:
                        labels[board.row][i].configure(bg='grey')


                board.row += 1
                board.col = 0

    else:
        feedback_label.config(text='Must have 5 letters to make a guess.')

def create_grid(root):
    """
    create the grid of labels for the guesses and feedback
    """
    label_frame = ttk.Frame(root, padding="3 3 3 3")
    label_frame.grid(row=1, column=1, columnspan=3) 
    root.grid_rowconfigure(1, weight=1) 
    root.grid_columnconfigure(1, weight=1) 
    
    labels = []
    for row in range(1, 7):
        label_row = []
        for col in range(1, 6):
            label = Label(label_frame, font='Courier 32 bold', text=' ',
                          borderwidth=1, relief='solid', width=3, height=2)
            label.grid(row=row, column=col, padx=2, pady=3)
            label_row.append(label)
        labels.append(label_row)
    
    return labels


def create_control_buttons(root, labels, guess, board):
    bottom_frame = ttk.Frame(root, padding="3 3 3 3")
    bottom_frame.grid(row=2, column=1, columnspan=2)
    info_label = ttk.Label(bottom_frame, font='Arial 16 bold',)
    info_label.grid(row=3, column=1, columnspan=3)
    new_game_button = Button(bottom_frame, font='Arial 24 bold',
                         text='New Game',
                         command=lambda: new_game(labels, board, info_label))
    new_game_button.grid(row=2, column=1, padx=2, pady=2)
    undo_button = Button(bottom_frame, font='Arial 24 bold',
                         text='Delete',
                         command=lambda: delete_letter(labels, board))
    undo_button.grid(row=2, column=2, padx=2, pady=2)
    enter_guess_button = Button(bottom_frame, font='Arial 24 bold',
            text='Check',
            command=lambda: make_guess(labels, board, info_label))
    enter_guess_button.grid(row=2, column=3, padx=2, pady=2)
    return info_label


def undo_last_pick(labels, board, guess):
    if len(guess) >= 1:
        row = board.current_round()
        column = len(guess) - 1
        labels[row][column].configure(bg='SystemButtonFace')
        guess.pop()

if __name__ == '__main__':
    main()
