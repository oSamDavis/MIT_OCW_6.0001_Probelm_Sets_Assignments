# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Sam Davis Omekara
# Collaborators : None
# Time spent    : ~ 48 hours

import math
import random
import string
import copy

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*': 0
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """

    assert str(word)  # defensive programming and asserting that function is called with good argument(i.e string)
    sum_of_letters = 0  # represents the first component of score
    second_component = 1  # initialize, the second component of score to 1

    word = word.lower()  # handles the case of mixed-Case strings

    for char in word:  # for each char in word
        sum_of_letters += SCRABBLE_LETTER_VALUES[char]  # add the value associated with such char to sum of letters

    formula = (7 * len(word)) - (3 * (n - len(word)))  # formula used to calculate second component
    second_component = max(second_component, formula)  # second component becomes max btwn formula and 1
    score = sum_of_letters * second_component  # score for word is the product of sum_of_letters and second_component

    return score


#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    assert dict(hand)  # defensive programming, asserting function is called with good arguments (i.e dict)

    for letter in hand.keys():  # for each letter in the key of the dict hand
        for j in range(hand[letter]):  # for each time the letter occurs ...
            print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand = {}  # have a dict, hand, which will store letters as keys and occurences as values
    num_vowels = int(math.ceil(n / 3))  # num_vowels will be the n / 3 rounded up to the next integer

    for i in range(num_vowels - 1):  # for i in the range on num_vowels ... (num_vowels - 1 to add a wildcard)
        x = random.choice(VOWELS)  # choice() returns a randomly selected element from the specified sequence.
        hand[x] = hand.get(x, 0) + 1  # get(x, default) avoids key error and returns default if x not found

    wildcard = "*"  # wildcard
    hand[wildcard] = 1  # put wildcard in hand with value of 1

    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)  # choice() returns a randomly selected element from the specified sequence.
        hand[x] = hand.get(x, 0) + 1  # get(x, default) avoids key error and returns default if x not found
    
    return hand  # returns the dictionary with selected letters and their frequency

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured). 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    new_hand = copy.deepcopy(hand)  # performing a deep copy on hand and saving it in new hand
    word = word.lower()  # mutating word to be all lower case
    for char in word:  # for each char in word ...
        if char in hand:  # if char is in hand
            new_hand[char] -= 1  # reduce the frequency of char by 1

    for i in hand:  # for each key(i.e letter) in hand
        if new_hand[i] <= 0:  # if the value(i.e frequency) in new_hand is less than or equal 0
            del(new_hand[i])  # delete such letter from dict

    return new_hand

#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """

    wildcard_index = word.find("*")  # find index of a wildcard

    new_word = ""  # new word, in case  a wildcard is encountered
    if wildcard_index != -1:  # if a wildcard is found...
        possible_words = []  # a list of possible words
        for char in VOWELS:  # for each char in vowels ...
            new_word = word.replace("*", char)  # replace wildcard with such a vowel
            new_word = new_word.lower()  # convert new_word to lowercases
            if new_word in word_list:  # if new word is in the word list...
                possible_words.append(new_word)  # append it the list of possible words
        if len(possible_words) == 0:  # if there isn't any possible word
            return False  # return false
        new_word = random.choice(possible_words)  # set new word to be a random word from possible words

    word = word.lower()  # converting to all lowercase characters ...
    if word not in word_list and new_word not in word_list:  # if such a word/ new_word is not in the word list ...
        return False  # return False

    used_wild_card = False # flag to check if wildcard is used
    for char in word:  # for each char in word ...
        if not used_wild_card and char == "*" and "*" in hand.keys():  # conditions for using a wildcard
            used_wild_card = True  # set wild card to used(i.e True)
            continue  # continue ...
        if word.count(char) > hand.get(char, 0):  # if the char's count in word is greater than it's frequency in hand
            return False  # return False

    return True


#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    length = 0  # initially length of hand is 0
    try:
        for letter in hand:  # for each letter in hand
            length += hand[letter]  # add to the length the frequency of such letter
    except ValueError:
        print("calculate_handlen called with bad arguments")

    return length  # return length

#
# Personal_Read Input Function, That handles Exceptions
#
def readInput(inputType, requestMsg, errorMsg):
    while True:
        val = input(requestMsg + " : ")
        try:
            return inputType(val)  # converts val from str to valType before returning
        except (ValueError, TypeError):
            print(val, errorMsg)


def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """

    # Keep track of the total score
    total_score = 0
    
    # As long as there are still letters left in the hand:
    while bool(hand):
        # Display the hand
        print("Current Hand:")
        display_hand(hand)

        # Ask user for input
        word = readInput(str, "Enter word or ""!!"" to indicate you are finished: ", "String not entered")

        if word == "!!":  # If the input is two exclamation points:
            break  # End the game (break out of the loop)

        else:  # Otherwise (the input is not two exclamation points):
            if is_valid_word(word, hand, word_list):  # If the word is valid:
                score = get_word_score(word, calculate_handlen(hand))  # Tell the user how many points the word earned,
                total_score += score  # and the updated total score
                print('"' + word + '"', "you earned", str(score) + ". Total:", total_score, "points.")

            else:  # Otherwise (the word is not valid):
                print("That is not a valid word. Please choose another word. ")  # Reject invalid word (print a message)
                
            hand = update_hand(hand, word)  # update the user's hand by removing the letters of their inputted word

    if bool(hand):  # if hand is not empty... (i.e user entered !!)
        print("Total score:", total_score, "points")  # Game is over, print total score
    else:  # else user ran out of letters in hand ...
        print("Ran out of letters. Total score:", total_score, "points")  # Game is over, tell user the total score

    return total_score  # Return the total score as result of function


#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters_bank
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters_bank were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """

    letters_bank = VOWELS + CONSONANTS  # construct a letter bank of vowels and consonants
    sub_hand = copy.deepcopy(hand)  # doesn't mutate hand so I make a deep copy of hand

    if letter not in hand:  # if the letter is not in hand
        return sub_hand  # return the same copy of hand

    new_letter = random.choice(letters_bank)  # choose a random letter from the letter bank

    while new_letter in hand.keys():  # while this new letter is amongst previous letters ...
        new_letter = random.choice(letters_bank)  # ... continue generating random letters

    sub_hand[new_letter] = hand.get(letter)  # now the new letter @ sub hand shld hold the value of the previous letter
    del(sub_hand[letter])  # delete previous letter in sub hand

    return sub_hand  # return sub hand

    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """

    no_of_hands = readInput(int, "Enter total number of hands", "is not a Number, Please Enter an Integer Number")
    total_game_score = 0  # var to hold the total game score
    hand = deal_hand(HAND_SIZE)  # dealing a hand with a HAND SIZE

    while no_of_hands > 0:  # while number of hands is not exhausted
        print("Current hand: ", end=" ")  # print current Hand
        display_hand(hand)  # display the hand
        will_sub_letter = readInput(str, "Would you like to substitute a letter? ", " is not a valid String")
        will_sub_letter_flag = True  # flag to know if user has conformed to rules of sub letter

        while will_sub_letter_flag:
            try:  # try block ... aiming to catch an assertion error
                will_sub_letter = will_sub_letter.lower()  # convert to lowercase ...
                assert will_sub_letter == 'yes' or will_sub_letter == 'no'  # assert it is either yes or no
                will_sub_letter_flag = False  # if assertion is passed, set flag to false
                if will_sub_letter == 'yes':  # if user wants to sub letter,
                    print("Current hand: ", end=" ")  # print current Hand
                    display_hand(hand)  # display hand ...
                    sub_letter = readInput(str, "Which letter would you like to replace: ", " is not a valid String")
                    hand = substitute_hand(hand, sub_letter)  # substitute hand
            except AssertionError:  # if assertion error occurs ...
                print("Please Enter 'yes' or 'no ")  # print this helpful message
                will_sub_letter = readInput(str, "Would you like to substitute a letter? ", " is not a valid String")

        score = play_hand(hand, word_list)  # play hand ...
        print("Total score for this hand:", str(score))  # print total score for particular hand

        print("----------------------")
        will_replay_hand = readInput(str, "Would you like to replay the hand? ", " is not a Valid String")
        will_replay_hand_flag = True  # flag to know if user has conformed to rules of replay hand

        while will_replay_hand_flag:
            try:  # try block, hoping to catch an assertion error
                will_replay_hand = will_replay_hand.lower()  # convert to lower
                assert will_replay_hand == 'yes' or will_replay_hand == 'no'  # assert that user enters yes or no
                will_replay_hand_flag = False  # set flag to False if assertion is passed
                if will_replay_hand == 'yes':  # if user wanna replay hand ...
                    score = play_hand(hand, word_list)  # play_hand with the current hand
                    print("Total score for this hand", str(score))  # print score
            except AssertionError:  # if assertion error is found,
                print("Please Enter 'yes' or 'no ")  # print this helpful message
                will_replay_hand = readInput(str, "Would you like to replay the hand? ", " is not a Valid String")

        hand = deal_hand(HAND_SIZE)  # deal a new hand, to user
        no_of_hands -= 1  # reduce number of hands ...
        total_game_score += score  # update total game score

    print("-----------------")
    print("Total score for all games: ", total_game_score)


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
