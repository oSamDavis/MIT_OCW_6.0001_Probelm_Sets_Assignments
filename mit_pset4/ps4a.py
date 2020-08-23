# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''

    if len(sequence) == 1:  # base case of recursion: (if sequence is only one letter)
        return [sequence]  # ... return a list with sequence only

    first_letter = sequence[0]  # get the first letter of sequence ...
    permutations = get_permutations(sequence[1:])  # recursively get the permutation of the sequence
    # removing  it's first letter (unwinding)
    res = []  # a list to store the permutations(i.e res)

    for element in permutations:  # for each element in permutations ...
        for i in range(len(element) + 1):  # for i starting @ 0 and ending @ len(element)
            individual_perm = element[:i] + first_letter + element[i:]  # get the individual permutation by:
            # concatenate the substring from the beginning to i, the first letter and the substring from i to the end
            res.append(individual_perm)  # append the individual permutation to the res list
    return res  # return res

if __name__ == '__main__':
#    #EXAMPLE
#    example_input = 'abc'
#    print('Input:', example_input)
#    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
#    print('Actual Output:', get_permutations(example_input))
    
#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a 
#    sequence of length n)
    print(get_permutations('faruq'))
    print(get_permutations('sam'))
    print(get_permutations('timo'))

