import argparse
import sys

import src.candidate
from src.candidate_attacker import CandidateAttacker
from src.dictionary import Dictionary
from src.dictionary_attacker import DictionaryAttacker

FREQUENCIES = {" ": 19, "a": 7, "b": 1, "c": 2, "d": 4, "e": 10, "f": 2, "g": 2, "h": 5, "i": 6, "j": 1, "k": 1,
               "l": 3, "m": 2, "n": 6, "o": 6, "p": 2, "q": 1, "r": 5, "s": 5, "t": 7, "u": 2, "v": 1, "w": 2,
               "x": 1, "y": 2, "z": 1}


def run(frequencies):
    """
    Sample usage:
        python3 -m src.main --dictionary test2_candidate_70_english_words.txt \
            --candidates test1_candidate_5_plaintexts.txt --test 1
    """
    parser = argparse.ArgumentParser(description="Attack homophonic substitution ciphers.")
    parser.add_argument("--dictionary", help="The name of the dictionary file with the path.",
                        default="test2_candidate_70_english_words.txt")
    parser.add_argument("--candidates", help="The name of the plaintext file with the path.",
                        default="test1_candidate_5_plaintexts.txt")
    parser.add_argument("--test",
                        help="The test to run. 1: attack with candidate plain texts. 2: attack with dictionary.",
                        choices=["1", "2"],
                        default="1")

    namespace = parser.parse_args(sys.argv[1:])

    cipher_text = input("Please enter the cipher text: \n")
    attacker = None

    if namespace.test == "1":
        candidates = src.candidate.read_from_file(namespace.candidates)
        attacker = CandidateAttacker(frequencies, candidates)
    elif namespace.test == "2":
        dictionary = src.dictionary.read_from_file(namespace.dictionary)
        attacker = DictionaryAttacker(frequencies, dictionary)

    print("Now attempting to break the cipher...")
    print(attacker.attack(cipher_text))


if __name__ == "__main__":
    run(FREQUENCIES)
