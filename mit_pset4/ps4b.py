# Problem Set 4B
# Name: Sam Davis Omekara Jr.
# Collaborators: None
# Time Spent: ~24 hours

import string

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text: str):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self) -> str:
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self) -> list:
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words[:]

    def build_shift_dict(self, shift: int) -> dict:
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''

        try:
            assert 0 <= shift < 26
            my_map = {}  # dictionary to store mappings

            curr_letter = ord('A')  # for uppercase we start at A
            while curr_letter <= ord('Z'):  # while the letter isn't yet Z ...
                new_letter = curr_letter + shift  # apply shift to the current letter

                if new_letter > ord('Z'):  # if the new letter is greater than Z
                    new_letter = ord('A') + (new_letter % (ord('Z') + 1))  # mode the new letter by Z + 1, then add it to A

                my_map[chr(curr_letter)] = chr(new_letter)  # map the current letter to the new letter
                curr_letter += 1  # move to next letter

            curr_letter = ord('a')  # for lowercase we start at a
            while curr_letter <= ord('z'):  # while the letter isn't yet z ...
                new_letter = curr_letter + shift  # apply shift to the current letter

                if new_letter > ord('z'):  # if the new letter is greater than z
                    new_letter = ord('a') + (new_letter % (ord('z') + 1))  # mode the new letter by z + 1, then add it to a

                my_map[chr(curr_letter)] = chr(new_letter)  # map the current letter to the new letter
                curr_letter += 1  # move to the next letter

            return my_map  # return map
        except AssertionError:
            raise ValueError("Invalid Shift. Couldn't build Shift Dict.")

    def apply_shift(self, shift: int) -> str:
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        letter_map = self.build_shift_dict(shift)  # build the letter map using the shift ...
        res = ""  # res var to hold value of ciphered string

        for char in self.message_text:  # for every char in the message ...
            if char.isalpha():  # if the char is a letter
                res += letter_map[char]  # append to the result the ciphered version of char
            else:  # else
                res += char  # append the char it self
        return res  # return the res


class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        Message.__init__(self, text)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(self.shift)
        self.message_text_encrypted = self.apply_shift(self.shift)


    def get_shift(self) -> int:
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self) -> dict:
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        return self.encryption_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        try:
            assert 0 <= shift < 26
            self.shift = shift
        except AssertionError:
            raise ValueError("Invalid Shift. Couldn't build Shift Dict.")

class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''

        decrypted_shift_value = 0  # var to hold decryption shift val
        decrypted_message = ""  # var to hold decrypted message
        num_of_valid_words = -1  # var to hold num of valid words

        for curr_shift in range(26):  # start the current shift from (0 to 25)
            curr_valid_words = 0  # var to hold the current no. of valid words
            curr_message = self.apply_shift(curr_shift)  # get curr message by applying the curr shift to the message
            for word in curr_message.split():  # for each word in the current message
                if is_word(self.get_valid_words(), word):  # if the word is valid ...
                    curr_valid_words += 1  # increase the count of valid words
            if curr_valid_words > num_of_valid_words:  # if curr num of valid words is greater than num of valid words
                num_of_valid_words = curr_valid_words  # update num of valid words
                decrypted_shift_value = curr_shift  # update decrypted shift value
                decrypted_message = curr_message  # update decrypted message

        return decrypted_shift_value, decrypted_message

if __name__ == '__main__':

#    #Example test case (PlaintextMessage)
    plaintext = PlaintextMessage('hello', 2)
    print('Expected Output: jgnnq')
    print('Actual Output:', plaintext.get_message_text_encrypted())

#
#    #Example test case (CiphertextMessage)
    ciphertext = CiphertextMessage('jgnnq')
    print('Expected Output:', (24, 'hello'))
    print('Actual Output:', ciphertext.decrypt_message())

    #TODO: WRITE YOUR TEST CASES HERE
    plaintext1 = PlaintextMessage('GOAT', 8)
    print('Expected Output: OWIB')
    print('Actual Output:', plaintext1.get_message_text_encrypted())

    plaintext2 = PlaintextMessage('I will most definitely be a software Engineer, Speaking into existence.', 5)
    print('Expected Output: N bnqq rtxy ijknsnyjqd gj f xtkybfwj Jslnsjjw, Xujfpnsl nsyt jcnxyjshj.')
    print('Actual Output:', plaintext2.get_message_text_encrypted())

    ciphertext1 = CiphertextMessage('OWIB')
    print('Expected Output:', (18, 'GOAT'))
    print('Actual Output:', ciphertext1.decrypt_message())

    ciphertext2 = CiphertextMessage('N bnqq rtxy ijknsnyjqd gj f xtkybfwj Jslnsjjw, Xujfpnsl nsyt jcnxyjshj.')
    print('Expected Output:', (21, 'I will most definitely be a software Engineer, Speaking into existence.'))
    print('Actual Output:', ciphertext2.decrypt_message())

    #TODO: best shift value and unencrypted story
    cipher_story = CiphertextMessage(get_story_string())
    print("Story: \n", cipher_story.decrypt_message())

