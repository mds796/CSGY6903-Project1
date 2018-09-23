import random

def countOccurrences(frequencies):
    """The total number of occurences for all letters in the given frequency map."""
    occurrences = 0

    for letter in frequencies:
        occurrences += frequencies[letter]

    return occurrences

def generateKey(frequencies):
    """Generates a homophonic substitution key."""
    assignments = assignSubstitutionToLetter(frequencies)

    keys = {}

    for i in range(0, len(assignments)):
        letter = assignments[i]

        if letter in keys:
            keys[letter].append(i)
        else:
            keys[letter] = [i]

    return keys


def assignSubstitutionToLetter(frequencies):
    """Create a list of letters where each letter occurs a number of times equal to their their frequency."""
    assignments = []

    for letter in frequencies:
        for j in range(0, frequencies[letter]):
            assignments.append(letter)
    
    random.shuffle(assignments)

    return assignments


def encrypt(plaintext, key):
    ciphertext = []

    for letter in plaintext.lower():
        if letter not in key:
            pass
        else:
            substitutions = key[letter]
            index = random.randint(0, len(substitutions) - 1)
            ciphertext.append(str(substitutions[index]))

    return ",".join(ciphertext)

    
