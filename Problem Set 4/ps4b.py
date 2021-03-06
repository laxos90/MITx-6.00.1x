from ps4a import *
import time


#
#
# Problem #6: Computer chooses a word
#
#
def get_computer_chosen_word(hand, word_list, n):
    """
    Given a hand and a word_list, find the word that gives
    the maximum value score, and return it.

    This word should be calculated by considering all the words
    in the word_list.

    If no words in the word_list can be made from the hand, return None.

    :rtype: object
    :param hand: dictionary (string -> int)
    :param word_list: list (string)
    :param n: integer (HAND_SIZE; i.e., hand size required for additional points)

    :returns: string or None
    """
    valid_words = []
    word_score = 0
    computer_word = None

    for word in word_list:
        if is_valid_word(word, hand, word_list):
            valid_words.append(word)

    for word in valid_words:
        if word_score < get_word_score(word, n):
            word_score = get_word_score(word, n)
            computer_word = word

    return computer_word

#
# Problem #7: Computer plays a hand
#
def play_computer_hand(hand, word_list, n):
    """
    Allows the computer to play the given hand, following the same procedure
    as playHand, except instead of the user choosing a word, the computer 
    chooses it.

    1) The hand is displayed.
    2) The computer chooses a word.
    3) After every valid word: the word and the score for that word is 
    displayed, the remaining letters in the hand are displayed, and the 
    computer chooses another word.
    4)  The sum of the word scores is displayed when the hand finishes.
    5)  The hand finishes when the computer has exhausted its possible
    choices (i.e. compChooseWord returns None).
 
    :param hand: dictionary (string -> int)
    :param word_list: list (string)
    :param n: integer (HAND_SIZE; i.e., hand size required for additional points)
    """
    total_score = 0
    computer_word = get_computer_chosen_word(hand, word_list, n)
    print("Current Hand: ", end="")
    display_hand(hand)
    total_score += get_word_score(computer_word, n)

    print("\"" + str(computer_word) + "\"" + " earned " + str(get_word_score(computer_word, n)) + " points. Total " +
          str(total_score) + " points")

    if there_is_no_more_elements_in_hand(update_hand(hand, computer_word)):
        display_hand(update_hand(hand, computer_word))
        print("Total score:" + str(total_score) + " points.")
        return


    while True:
        computer_word = get_computer_chosen_word(hand, word_list, n)
        hand = update_hand(hand, computer_word)


        if get_computer_chosen_word(hand, word_list, n) is None:
            print("Current Hand: ", end="")
            display_hand(hand)
            print("Total score:" + str(total_score) + " points.")
            break
        else:
            print("Current Hand: ", end="")
            display_hand(hand)
            computer_word = get_computer_chosen_word(hand, word_list, n)
            print("\"" + str(computer_word) + "\"" + " earned " + str(get_word_score(computer_word, n))
                  + " points.", end="")
            total_score += get_word_score(computer_word, n)
            print("Total " + str(total_score) + " points")


def there_is_no_more_elements_in_hand(hand):
    hand_values_summ = 0
    for letter in hand:
        hand_values_summ += hand[letter]
    return hand_values_summ == 0



# Problem #8: Playing a game
#
#
def play_game(word_list):
    """
    Allow the user to play an arbitrary number of hands.
 
    1) Asks the user to input 'n' or 'r' or 'e'.
        * If the user inputs 'e', immediately exit the game.
        * If the user inputs anything that's not 'n', 'r', or 'e', keep asking them again.

    2) Asks the user to input a 'u' or a 'c'.
        * If the user inputs anything that's not 'c' or 'u', keep asking them again.

    3) Switch functionality based on the above choices:
        * If the user inputted 'n', play a new (random) hand.
        * Else, if the user inputted 'r', play the last hand again.
      
        * If the user inputted 'u', let the user play the game
          with the selected hand, using playHand.
        * If the user inputted 'c', let the computer play the 
          game with the selected hand, using compPlayHand.

    4) After the computer or user has played the hand, repeat from step 1

    :param word_list: list (string)
    """
    times_playing = 0

    while True:
        arbitrary_game = input(
            "Write n to play a new random hand, write r to play the last hand again, play e to exit the game: ")
        if arbitrary_game == "e":
            break
        if arbitrary_game != "r" and arbitrary_game != "n":
            print("Invalid command")
        elif arbitrary_game == "n" and times_playing == 0:
            times_playing += 1

        if arbitrary_game == "r" and times_playing < 1:
            print("You have not played a hand yet. Please play a new hand first!")
        else:
            while True:
                who_plays = input("Enter u to arbitrary_game yourself play, c to have the computer play: ")

                if who_plays != "u" and who_plays != "c":
                    print("Invalid command")
                elif who_plays == "u":
                    if arbitrary_game == "n":
                        hand = deal_hand(n)
                        play_hand(hand, word_list, n)
                        break
                    elif arbitrary_game == "r":
                        play_hand(hand, word_list, n)
                        break
                elif who_plays == "c":
                    if arbitrary_game == "n":
                        hand = deal_hand(n)
                        play_computer_hand(hand, word_list, n)
                        break
                    elif arbitrary_game == "r":
                        play_computer_hand(hand, word_list, n)
                        break





def main():
    word_list = load_words()
    play_game(word_list)

#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    # main()
    word_list = load_words()
    play_game(word_list)
