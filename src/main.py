import src.candidate
import src.dictionary
from src.cipher import generate_homophonic


def run(frequencies):
    cipher = generate_homophonic(frequencies)

    candidates = src.candidate.read_from_file('test1_candidate_5_plaintexts.txt')
    dictionary = src.dictionary.read_from_file('test2_candidate_70_english_words.txt')

    for candidate in candidates:
        c = cipher.encrypt(candidate.text)
        m = cipher.decrypt(c)

        print("\nTesting candidate...")
        print("\nOriginal: ", candidate.text)
        print("\nCiphertext: ", c)
        print("\nPlaintext: ", m)
        print("\nReflexive: ", m == candidate.text)


if __name__ == '__main__':
    run({
        " ": 19,
        "a": 7,
        "b": 1,
        "c": 2,
        "d": 4,
        "e": 10,
        "f": 2,
        "g": 2,
        "h": 5,
        "i": 6,
        "j": 1,
        "k": 1,
        "l": 3,
        "m": 2,
        "n": 6,
        "o": 6,
        "p": 2,
        "q": 1,
        "r": 5,
        "s": 5,
        "t": 7,
        "u": 2,
        "v": 1,
        "w": 2,
        "x": 1,
        "y": 2,
        "z": 1
        })
