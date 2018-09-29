from math import *
from cipher import SubstitutionCipher
from cipher import generate_homophonic
from collections import Counter

FREQUENCIES = {" ": 19, "a": 7, "b": 1, "c": 2, "d": 4, "e": 10, "f": 2, "g": 2, "h": 5, "i": 6, "j": 1, "k": 1,
                      "l": 3, "m": 2, "n": 6, "o": 6, "p": 2, "q": 1, "r": 5, "s": 5, "t": 7, "u": 2, "v": 1, "w": 2,
                      "x": 1, "y": 2, "z": 1}


class Scorer:
    def __init__(self, frequencies):
        self.frequencies = frequencies

    # def max(substitution_ciphers):
    def min(self, substitution_ciphers):

        input = read_from_file('../test2_candidate_70_english_words.txt')
        encryption_cipher_test = generate_homophonic(FREQUENCIES)
        #sample ciphertext for testing
        cipher_text = encryption_cipher_test.encrypt(input)

        #Made a list of ciphers for me to test, but will be inputted later
        substitution_ciphers = list()
        for i in range(0,5):
            substitution_ciphers.append(generate_homophonic(FREQUENCIES))

        #start here
        """list(SubstitutionCipher) -> SubstitutionCipher"""
        counts = list()
        for cipher in substitution_ciphers:
            counts.append(Counter(cipher.decrypt(cipher_text)))

        min_error = index_MSE(self.frequencies, counts)
        print(substitution_ciphers[min_error])
        return substitution_ciphers[min_error]

    # def _score(cipher) -> int:
    #     pass

def read_from_file(filename):
    """
    Reads the dictionary from the given file.
    Each line is assumed to contain a single word in the dictionary.
    Whitespace is stripped at the beginning and end of each line.
    """
    words = []

    with open(filename) as f:
        for line in f:
            words.append(line.strip().lower())
    words = " ".join(words)
    return words

def index_MSE(frequencies, counts):
    mean_sq_errors = list()
    # print(frequencies)
    # print(counts[0])
    for i in range(0, len(counts)):
        squared_errors = list()
        for j in counts[i]:
            sq_error = pow(frequencies[j]-counts[i][j], 2)
            squared_errors.append(sq_error)
        mean_sq_errors.append(sum(squared_errors)/len(frequencies))
    index = 0
    min = mean_sq_errors[0]
    for i in range(0, len(mean_sq_errors)-1):
        if min > mean_sq_errors[i+1]:
            min = mean_sq_errors[i+1]
            index = i+1
    return index




frequencies = Counter(read_from_file('../test2_candidate_70_english_words.txt'))
test_scorer = Scorer(frequencies)
test_scorer.min("test")
