# 6.00x Problem Set 4A Template
#
# The 6.00 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
# Modified by: Sarina Canelake <sarina>
#

import random
from constants import *

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7
n = HAND_SIZE

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1,
    'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORD_LIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # in_file: file
    in_file = open(WORD_LIST_FILENAME)
    # word_list: list of strings
    word_list = []
    for line in in_file:
        word_list.append(line.strip().lower())
    print("  ", len(word_list), "words loaded.")
    return word_list


def get_frequency_dict(sequence):
    """
    :param sequence: string or list
    :returns: Returns a dictionary where the keys are elements of the
    sequence and the values are integer counts, for the number of times
    that an element is repeated in the sequence.
    """
    # freq: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x, 0) + 1
    return freq


# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    The score for a word is the sum of the points for letters in the
    word, multiplied by the length of the word, PLUS 50 points if all n
    letters are used on the first turn.

    Letters are scored as in Scrabble; A is worth 1, B is worth 3, C is
    worth 3, D is worth 2, E is worth 1, and so on (see SCRABBLE_LETTER_VALUES)

    :param word: string (lowercase letters)
    :param n: integer (HAND_SIZE; i.e., hand size required for additional points)
    :returns: the score for a word. Assumes the word is a valid word. (int >= 0)
    """
    score = 0

    for letter in word:
        score += SCRABBLE_LETTER_VALUES[letter]

    score *= len(word)

    return score + 50 if len(word) == n else score


def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
    display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    :param hand: dictionary (string -> int)
    """
    for letter in hand:
        for j in range(hand[letter]):
            print(letter, end=" ")

    print()

#
# Problem #2: Make sure you understand how this function works and what it does!
#
def deal_hand(n):
    """
    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    :param n: int >= 0
    :returns: dictionary (string -> int). Returns a random hand containing
    n lowercase letters. At least n/3 the letters in the hand should be VOWELS.
    """
    hand = {}
    num_vowels = n // 3

    for i in range(num_vowels):
        x = VOWELS[random.randrange(len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1

    for i in range(num_vowels, n):
        x = CONSONANTS[random.randrange(len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1

    return hand


#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
    In other words, this assumes that however many times
    a letter appears in 'word', 'hand' has at least as
    many of that letter in it. 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    :param word: string
    :param hand: dictionary (string -> int)
    :returns: dictionary (string -> int).
    """
    original_hand = hand.copy()

    for letter in word:
        original_hand[letter] -= 1
    return original_hand


# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Does not mutate hand or word_list.
   
    :param word: string
    :param hand: dictionary (string -> int)
    :param word_list: list of lowercase strings.
    :returns: True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    """
    secondary_hand = hand.copy()

    if word in word_list:

        for letter in word:
            if letter not in secondary_hand:
                return False
            else:
                secondary_hand[letter] -= 1
                if secondary_hand[letter] == -1:
                    return False
        return True
    else:
        return False


#
# Problem #4: Playing a hand
#

def calculate_hand_len(hand):
    """
    :param hand: dictionary (string-> int)
    :returns: the length (number of letters) in the current hand.
    """
    hand_lenght = 0

    for letter in hand:
        hand_lenght += hand[letter]

    return hand_lenght


def play_hand(hand, word_list, n):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    * The user may input a word or a single period (the string ".") 
      to indicate they're done playing
    * Invalid words are rejected, and a message is displayed asking
      the user to choose another word until they enter a valid word or "."
    * When a valid word is entered, it uses up letters from the hand.
    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.
    * The sum of the word scores is displayed when the hand finishes.
    * The hand finishes when there are no more unused letters or the user
      inputs a "."

    :param hand: dictionary (string -> int)
    :param word_list: list of lowercase strings
    :param n: integer (HAND_SIZE; i.e., hand size required for additional points)
    """

    display_hand(hand)
    word = input("Enter a word or a single period to indicate you are done playing: ")
    score_sum = 0
    new_hand = hand

    while True:

        if is_valid_word(word, new_hand, word_list):
            score_sum += get_word_score(word, n)
            print("The total score is " + str(score_sum))

            if calculate_hand_len(hand) == 0 or word == ".":
                print("The total score is " + str(score_sum))
                break

            else:
                display_hand(update_hand(new_hand, word))
                new_hand = update_hand(new_hand, word)
                word = input("Enter another word.")


        else:
            word = input("Enter a valid word or . ")
            if word == ".":
                print("The total score is " + str(score_sum))
                break


def play_game(word_list):
    """
    Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
      * If the user inputs 'n', let the user play a new (random) hand.
      * If the user inputs 'r', let the user play the last hand again.
      * If the user inputs 'e', exit the game.
      * If the user inputs anything else, tell them their input was invalid.
 
    2) When done playing the hand, repeat from step 1    
    :param word_list: list of lowercase strings
    """
    while True:

        arbitrary_game = input(
            "Write n to play a new random hand, write r to play the last hand again, play e to exit the game: ")

        if arbitrary_game == "n":
            copy_of_hand = deal_hand(n)

            play_hand(copy_of_hand, word_list, n)

        elif arbitrary_game == "r":

            play_hand(copy_of_hand, word_list, n)

        elif arbitrary_game == "e":
            break
        else:
            print("It was an invalid option")
            play_game(word_list)


def main():
    word_list = load_words()
    play_game(word_list)


if __name__ == '__main__':
    main()
