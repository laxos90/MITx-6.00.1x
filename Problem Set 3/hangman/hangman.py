# 6.00 Problem Set 3
# 
# Hangman game
#

# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)

import random
import string

WORD_LIST_FILENAME = "words.txt"
NUMBER_OF_GUESSES = 8

# Helper Code
# Load the list of words into the variable word_list
# so that it can be accessed from anywhere in the program


def load_words():
    """
    :returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")

    with open(WORD_LIST_FILENAME) as file:
        line = file.read()

    word_list = line.split()
    print("  ", len(word_list), "words loaded.")

    return word_list


def choose_word(word_list):
    """
    :param word_list: list of words (strings)

    :returns: a word from word_list at random
    """
    return random.choice(word_list)

# end of Helper Code
# -----------------------------------


def is_word_guessed(secret_word, letters_guessed):
    """
    :param secret_word: string, the word the user is guessing
    :param letters_guessed: list, what letters have been guessed so far
    :returns: boolean, True if all the letters of secretWord are in lettersGuessed;
      False otherwise
    """
    for letter in secret_word:
        if letter not in letters_guessed:
            return False

    return True


def get_guessed_word(secret_word, letters_guessed):
    """
    :param secret_word: string, the word the user is guessing
    :param letters_guessed: list, what letters have been guessed so far
    :returns: string, comprised of letters and underscores that represents
      what letters in secretWord have been guessed so far.
    """
    word = ""

    for letter in secret_word:
        if letter in letters_guessed:
            word += letter
        else:
            word += " _ "
    return word


def get_available_letters(letters_guessed):
    """
    :param letters_guessed: list, what letters have been guessed so far
    :returns: string, comprised of letters that represents what letters have not
      yet been guessed.
    """

    available_letters = ""

    for letter in string.ascii_lowercase:
        if letter not in letters_guessed:
            available_letters += letter

    return available_letters


def hangman(secret_word):
    """
    :param secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secretWord contains.

    * Ask the user to supply one guess (i.e. letter) per round.

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computers word.

    * After each round, you should also display to the user the
      partially guessed word so far, as well as letters that the
      user has not yet guessed.

    Follows the other limitations detailed in the problem write-up.
    """

    guesses_left = NUMBER_OF_GUESSES
    letters_guessed = []

    print_header(secret_word)
    print("------------")

    while True:

        print("You have " + str(guesses_left) + " guess left")
        print("Available letters: " + get_available_letters(letters_guessed))
        letter = input("Please guess a letter: ").lower()

        if letter in letters_guessed:
            print("Oops! You've already guessed that letter: " + get_guessed_word(secret_word, letters_guessed))
        elif letter in secret_word:
            letters_guessed.append(letter)
            print('Good guess: ' + get_guessed_word(secret_word, letters_guessed))
        else:
            print('Oops! That letter is not in my word: ' + get_guessed_word(secret_word, letters_guessed))
            letters_guessed.append(letter)
            guesses_left -= 1

        print("------------")

        if is_word_guessed(secret_word, letters_guessed):
            print("Congratulations, you won")
            break

        if guesses_left == 0:
            print("Sorry, you ran out of guesses. The word was " + secret_word + ".")
            break


def print_header(secret_word):
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is " + str(len(secret_word)) + " letters long")

def main():
    word_list = load_words()
    secret_word = choose_word(word_list).lower()
    hangman(secret_word)

if __name__ == "__main__":
    main()
