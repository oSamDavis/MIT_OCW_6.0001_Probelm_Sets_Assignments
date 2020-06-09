# Problem Set 2, hangman.py
# Name: Sam Davis Omekara Jr.
# Collaborators: Null
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string
import string

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
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    for char in secret_word:  # for each char in secret_word
        if char not in letters_guessed:  # if the letter not found in letters_guessed return False
            return False

    return True  # if loop exhausts, then return true


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    guessed_word = ""  # empty string to hold the characters of guessed word

    for char in secret_word:  # for each char in secret word
        if char in letters_guessed:  # if the char is found in the list of letters guessed
            guessed_word += char  # append the char
        else:
            guessed_word += "_ "  # else append the string underscore and space (_ )

    return guessed_word  # return the guessed word


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    available_letters = ""  # string object to hold available letters

    for char in string.ascii_lowercase:  # for  each lowercase letter in the alphabet
        if char not in letters_guessed:  # if the char is not in guessed word
            available_letters += char  # append it to the available letters

    return available_letters  # return available letters
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''

    num_of_guesses = 6  # var to hold the number of guesses a user has
    num_of_warnings = 3  # var to hold the number of warnings a user has
    user_guessed_letters = []  # list to hold the user's guessed letters
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that  is", len(secret_word), "letters long .")
    print("-------------")
    print("You have", num_of_guesses, "guesses left.")
    print("You have", num_of_warnings, "warnings left.")
    print("Available letters:", get_available_letters(user_guessed_letters))

    # while the user hasn't exhausted number of guesses or guessed the correct word
    while num_of_guesses != 0 and is_word_guessed(secret_word, user_guessed_letters) is False:
        print("-------------")
        print("You have", num_of_guesses, "guesses left.")
        print("Available letters:", get_available_letters(user_guessed_letters))
        guess = input("Please guess a letter")
        if not guess.isalpha():  # if the user's guess isn't a letter...
            if num_of_warnings > 0:  # ... and number of warnings is greater than 0
                num_of_warnings -= 1  # reduce number of warnings
                print("Oops! That  is  not a valid letter.")
                print("You have", num_of_warnings, "warnings left:",
                      get_guessed_word(secret_word, user_guessed_letters))
            else:
                num_of_guesses -= 1  # ... if user has no warnings left, reduce number of guesses
                print("Oops! That  is  not a valid letter.")
                print("You have no warnings left, so you lose one guess")
                print("You have", num_of_guesses, "guesses left:", get_guessed_word(secret_word, user_guessed_letters))

        elif guess in user_guessed_letters:  # else if user has guessed a letter before...
            if num_of_warnings > 0:  # ...and user has some warnings left
                num_of_warnings -= 1  # reduce number of warnings
                print("Oops! You've already guessed that letter")
                print("You have", num_of_warnings, "warnings left:",
                      get_guessed_word(secret_word, user_guessed_letters))
            else:
                num_of_guesses -= 1  # if user has no warning, reduce number of guesses
                print("Oops! You've already guessed that letter")
                print("You have no warnings left, so you lose one guess")
                print("You have", num_of_guesses, "guesses left:", get_guessed_word(secret_word, user_guessed_letters))

        else:
            guess = guess.lower()  # converting the letter to lowercase
            user_guessed_letters.append(guess)  # adding guess to the list of guessed letters
            if guess in secret_word:  # if guess is in secret_word
                print("Good guess:", get_guessed_word(secret_word, user_guessed_letters))
            else:
                vowels = ["a", "e", "i", "o", "u"]
                if guess in vowels:
                    num_of_guesses -= 2
                else:
                    num_of_guesses -= 1
                print("Oops! That letter is not in my word:", get_guessed_word(secret_word, user_guessed_letters))

    if num_of_guesses == 0 and is_word_guessed(secret_word, user_guessed_letters) is False:
        print ("------------")
        print("Sorry, you ran out of guesses. The word was", secret_word)
    else:
        unique_letters = []
        for char in secret_word:
            if char not in unique_letters:
                unique_letters.append(char)
        total_score = num_of_guesses * len(unique_letters)
        print("------------")
        print("Congratulations, you won!")
        print("Your total score for  this game  is:", total_score)



# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''

    def remove_whitespace(string):  # helper func to remove whitespaces from string
        return "".join(string.split())

    my_word = remove_whitespace(my_word)

    if len(my_word) != len(other_word):
        return False
    for char in my_word:
        if char.isalpha():
            if my_word.find(char) != other_word.find(char) or my_word.count(char) != other_word.count(char):
                return False

    return True


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    found_match = False
    words_to_print = ""
    for word in wordlist:
        if match_with_gaps(my_word, word):
            words_to_print += word + " "
            found_match = True

    if found_match:
        print(words_to_print)
    else:
        print("No matches found")

    return None

def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''

    num_of_guesses = 6
    num_of_warnings = 3
    num_of_hints = 1
    user_guessed_letters = []
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that  is", len(secret_word), "letters long .")
    print("-------------")
    print("You have", num_of_guesses, "guesses left.")
    print("You have", num_of_warnings, "warnings left.")
    print("You have", num_of_hints, "hint")
    print("Available letters:", get_available_letters(user_guessed_letters))

    while num_of_guesses > 0 and is_word_guessed(secret_word, user_guessed_letters) is False:
        print("-------------")
        print("You have", num_of_guesses, "guesses left.")
        print("Available letters:", get_available_letters(user_guessed_letters))
        guess = input("Please guess a letter: ")

        if guess == "*" and num_of_hints != 0:
            print("Possible word matches are: ")
            show_possible_matches(get_guessed_word(secret_word, user_guessed_letters))
            num_of_hints -= 1

        elif not guess.isalpha():
            if num_of_warnings > 0:
                num_of_warnings -= 1
                print("Oops! That  is  not a valid letter.")
                print("You have", num_of_warnings, "warnings left:",
                      get_guessed_word(secret_word, user_guessed_letters))
            else:
                num_of_guesses -= 1
                print("Oops! That  is  not a valid letter.")
                print("You have no warnings left, so you lose one guess")
                print("You have", num_of_guesses, "guesses left:", get_guessed_word(secret_word, user_guessed_letters))

        elif guess in user_guessed_letters:
            if num_of_warnings > 0:
                num_of_warnings -= 1
                print("Oops! You've already guessed that letter")
                print("You have", num_of_warnings, "warnings left:",
                      get_guessed_word(secret_word, user_guessed_letters))
            else:
                num_of_guesses -= 1
                print("Oops! You've already guessed that letter")
                print("You have no warnings left, so you lose one guess")
                print("You have", num_of_guesses, "guesses left:", get_guessed_word(secret_word, user_guessed_letters))

        else:
            guess = guess.lower()
            user_guessed_letters.append(guess)
            if guess in secret_word:
                print("Good guess:", get_guessed_word(secret_word, user_guessed_letters))
            else:
                vowels = ["a", "e", "i", "o", "u"]
                if guess in vowels:
                    num_of_guesses -= 2
                else:
                    num_of_guesses -= 1
                print("Oops! That letter is not in my word:", get_guessed_word(secret_word, user_guessed_letters))

    if num_of_guesses == 0 and is_word_guessed(secret_word, user_guessed_letters) is False:
        print ("------------")
        print("Sorry, you ran out of guesses. The word was", secret_word)
    else:
        unique_letters = []
        for char in secret_word:
            if char not in unique_letters:
                unique_letters.append(char)
        total_score = num_of_guesses * len(unique_letters)
        print("------------")
        print("Congratulations, you won!")
        print("Your total score for  this game  is:", total_score)




# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.




if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    #secret_word = choose_word(wordlist)
    #hangman(secret_word)






###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)

