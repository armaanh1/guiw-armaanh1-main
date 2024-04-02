# Name: Armaan Hirani
# UTEID: ah62954

# all adopted from master_mind.py and letter_typing.py

import random
from tkinter import *
from tkinter import ttk

class MasterMindBoard:
    def __init__(self):
        self.__board = []
        self.__feedback = []
        self.__colors = 'BGOPRY'
        self.__secret_word = ''
        self.__pick_secret()

    def make_guess(self, guess):
        self.__board.append(guess)
        self.__feedback.append(self.__get_feedback(guess))
        return self.__feedback[-1]

    def __get_feedback(self, guess):
        guess_list = list(guess)
        secret_code_list = list(self.__secret_word)
        feedback = ''
        for i in range(len(guess)):
            if guess_list[i] == self.__secret_word[i]:
                feedback += 'B'
                guess_list[i] = '*'
                secret_code_list[i] = 'X'
        for i in range(len(guess)):
            if guess_list[i] in secret_code_list:
                feedback += 'W'
                index = secret_code_list.index(guess_list[i])
                secret_code_list[index] = 'X'
        return feedback

    def __pick_secret(self):
        self.__secret_word = ''
        for i in range(4):
            self.__secret_word += random.choice(self.__colors)

    def game_over(self):
        return (len(self.__board) == 10
                or (len(self.__board) > 0
                    and self.__secret_word == self.__board[-1]))

    def won(self):
        return len(self.__board) > 0 and self.__secret_word == self.__board[-1]

    def get_secret_word(self):
        return self.__secret_word

    def current_round(self):
        return len(self.__board)

    def __str__(self):
        result = ''
        for i in range(len(self.__board)):
            for j in range(4):
                result += self.__board[i][j] + ' '
            result += ':' + self.__feedback[i] + '\n'
        return result

def main():
    root = Tk()
    root.geometry("400x600")
    root.title("Wordle")
    root.resizable(False, False)
    board = MasterMindBoard()
    feedback_vars, labels = create_grid(root)
    guess = []
    create_control_buttons(root, labels, feedback_vars, guess, board)
    root.mainloop()

def update_guess(guess, color, labels, board, _event=NONE):
    if len(guess) < 4 and not board.game_over():
        guess.append(color[0])
        labels[board.current_round()][len(guess) - 1].configure(bg=color)

def create_grid(root):
    """
    create the grid of labels for the guesses and feedback
    """
    label_frame = ttk.Frame(root, padding="30 3 3 3")
    label_frame.grid(row=1, column=1) 
    root.grid_rowconfigure(1, weight=1) 
    root.grid_columnconfigure(1, weight=1) 
    
    feedback_vars = []
    labels = []
    for row in range(1, 7):
        label_row = []
        for col in range(1, 6):
            label = Label(label_frame, font='Courier 32 bold', text=' ',
                          borderwidth=1, relief='solid', width=3, height=2)
            label.grid(row=row, column=col, padx=2, pady=3) 
            label_row.append(label)
        labels.append(label_row)
        feedback_var = StringVar()
        feedback_var.set('    ')
        feedback_vars.append(feedback_var)
        feedback_label = Label(label_frame, font='Courier 20 bold',
                               textvariable=feedback_var)
        feedback_label.grid(row=row, column=6)
    return feedback_vars, labels


def create_control_buttons(root, labels, feedback, guess, board):
    bottom_frame = ttk.Frame(root)
    bottom_frame.grid(row=2, column=1, columnspan=2)
    info_var = StringVar()
    undo_button = Button(bottom_frame, font='Arial 24 bold',
                         text='Delete',
                         command=lambda: undo_last_pick(labels, board, guess))
    undo_button.grid(row=1, column=1, padx=5, pady=5)
    enter_guess_button = Button(bottom_frame, font='Arial 24 bold',
            text='Check',
            command=lambda: enter_guess(feedback, board, guess, info_var))
    enter_guess_button.grid(row=1, column=2, padx=5, pady=5)
    info_label = ttk.Label(bottom_frame, font='Arial 16 bold',
                           textvariable=info_var)
    info_label.grid(row=2, column=1, columnspan=2)

def enter_guess(feedback_vars, board, guess, info_var):
    if len(guess) == 4:
        guess_string = ''.join(guess)
        guess.clear()
        feedback_index = board.current_round()
        feedback = board.make_guess(guess_string)
        if len(feedback) == 0:
            feedback = 'NONE'
        feedback_vars[feedback_index].set(feedback)
        if board.won():
            info_var.set("You won! Well Done!")
        elif board.game_over():
            info = 'Game over. Secret word was ' + board.get_secret_code()
            info_var.set(info)
    else:
        info_var.set('Must have 5 letters to make a guess.')

def undo_last_pick(labels, board, guess):
    if len(guess) >= 1:
        row = board.current_round()
        column = len(guess) - 1
        labels[row][column].configure(bg='SystemButtonFace')
        guess.pop()

if __name__ == '__main__':
    main()
