<<<<<<< HEAD
import src.candidate
from src.dictionary import Dictionary
from src.cipher import generate_homophonic
from src.dictionary_attacker import DictionaryAttacker
from src.candidate import  read_from_file
from src.candidate import read_file_simple
from src.CLIInterface import CLIInterface
from src.breaker import breaker_with_candidates


FREQUENCIES = {" ": 19, "a": 7, "b": 1, "c": 2, "d": 4, "e": 10, "f": 2, "g": 2, "h": 5, "i": 6, "j": 1, "k": 1,
               "l": 3, "m": 2, "n": 6, "o": 6, "p": 2, "q": 1, "r": 5, "s": 5, "t": 7, "u": 2, "v": 1, "w": 2,
               "x": 1, "y": 2, "z": 1}


=======
# import src.candidate
import src.dictionary
from src.cipher import generate_homophonic
from src.timeout import timeout

""" Path changed by Siddharth"""
from src.candidate import  read_from_file
from src.candidate import read_file_simple
# from dictionary import dictionary
# from cipher import generate_homophonic
from src.CLIInterface import CLIInterface
from src.breaker import breaker_with_candidates
import time

FREQUENCIES = {" ": 19, "a": 7, "b": 1, "c": 2, "d": 4, "e": 10, "f": 2, "g": 2, "h": 5, "i": 6, "j": 1, "k": 1,
					  "l": 3, "m": 2, "n": 6, "o": 6, "p": 2, "q": 1, "r": 5, "s": 5, "t": 7, "u": 2, "v": 1, "w": 2,
					  "x": 1, "y": 2, "z": 1}
@timeout(180)
>>>>>>> Added timeout to main.py.
def run(frequencies, _inp):
	cipher = generate_homophonic(frequencies)

	# candidates = src.candidate.read_from_file(_inp['plaintextFile'])
	# dictionary = src.dictionary.read_from_file(_inp['dictionaryFile'])

	"""Path changed by Siddharth"""
	candidates = read_from_file(_inp['plaintextFile'])
	plaintexts = read_file_simple(_inp['plaintextFile'])
	# dictionary = dictionary.read_from_file(_inp['dictionaryFile'])

	print (breaker_with_candidates(FREQUENCIES, plaintexts, "50 38 48 46 41 29 91 3 40 105 93 73 20 75 41 85 53 16 24 90 6 68 78 75 101 89 47 23 27 94 68 51 31 51 68 52 9 42 16 65 29 85 100 98 79 105 101 16 103 21 26 104 83 20 54 83 86 71 46 20 95 54 20 93 77 89 96 53 0 57 46 88 0 42 45 67 83 59 77 68 1 83 17 71 90 65 3 3 52 7 104 60 24 4 24 94 100 96 7 48 43 15 15 33 68 79 56 54 71 104 78 4 20 0 28 94 82 94 103 48 18 15 83 35 19 77 87 66 75 27 51 40 57 36 31 3 84 8 65 94 82 59 89 20 3 57 68 85 42 51 10 82 103 89 75 43 16 2 42 64 47 4 45 90 81 0 82 93 46 48 75 27 21 17 88 7 103 94 33 19 36 56 27 73 72 41 53 72 46 23 24 17 38 5 86 18 33 19 104 44 62 9 82 17 54 71 16 47 6 86 65 35 48 67 62 25 41 101 33 98 48 42 77 78 65 75 31 17 67 34 82 9 38 89 27 33 100 2 101 85 20 67 16 10 4 41 6 74 105 95 68 104 44 18 15 38 32 16 75 83 15 38 44 97 29 53 59 78 87 52 20 95 89 88 104 20 3 79 45 17 32 18 35 72 100 104 82 72 86 93 79 8 17 80 54 64 31 3 100 57 64 83 15 74 92 57 56 56 70 60 53 54 24 55 31 94 100 45 76 100 88 64 29 45 0 91 70 85 40 66 103 60 98 43 100 32 80 15 96 35 21 4 103 90 15 24 62 79 70 28 44 1 24 0 62 12 1 43 13 93 75 59 52 56 72 66 21 49 77 86 91 58 68 54 34 81 21 36 50 62 87 46 20 12 93 94 33 96 80 0 70 46 60 49 85 20 16 41 32 74 23 55 56 95 52 4 70 8 60 21 83 54 80 56 43 4 65 67 86 101 31 3 21 105 10 44 61 94 19 95 85 41 60 100 62 79 37 17 91 50 95 43 105 105 3 37 61 95 96 16 19 90 32 49 33 62 85 93 8 41 50 7 24 79 88 4 103 35 41 44 45 0 101 0 47 58 82 33 17 42 87 44 5 105 105 70 60 83 95 87 91 105 75 31 77 29 87 74 36 20"))

	for candidate in candidates:
		c = cipher.encrypt(candidate.text)
		m = cipher.decrypt(c)

		# breaker_with_candidates(FREQUENCIES, plaintexts, _inp['ciphertext'])

		print("\nTesting candidate...")
		print("\nOriginal: ", candidate.text)
		print("\nCiphertext: ", c)
		print("\nPlaintext: ", m)
		print("\nReflexive: ", m == candidate.text)

def breaker_with_candidates(frequencies, candidates):
    dictionary = Dictionary([])

    for candidate in candidates:
        dictionary = dictionary.merge(candidate.dictionary())

    return DictionaryAttacker(frequencies, dictionary)


def breaker_with_dictionary(frequencies, dictionary):
    return DictionaryAttacker(frequencies, dictionary)


if __name__ == '__main__':
	
	try:
		start = time.time()
		_inp = CLIInterface().run()
		run(FREQUENCIES, _inp)
	except Exception as e:
		print ("Time elapsed: {}sec".format(int(time.time() - start)))
	# a()
	
# ../test1_candidate_5_plaintexts.txt
# ../test2_candidate_70_english_words.txt