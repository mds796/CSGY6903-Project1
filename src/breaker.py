from copy import deepcopy

from src.cipher import DELIMITER, SubstitutionCipher
from src.dictionary import Dictionary


class DictionaryCodeBreaker:
    def __init__(self, frequencies, dictionary):
        self.frequencies = frequencies
        self.dictionary = dictionary

    def attack(self, ciphertext):
        if ciphertext == "" or ciphertext is None:
            return ""

        ciphers = [int(c) for c in ciphertext.split(DELIMITER)]
        number_of_unique_ciphers = len(set(ciphers))

        cipher = self.attack_recursive(ciphers, number_of_unique_ciphers, SubstitutionCipher({}))

        if cipher is not None:
            return cipher.decrypt(ciphertext)
        else:
            return None

    def attack_recursive(self, ciphertext, number_of_unique_ciphers, candidate_cipher):
        if len(candidate_cipher.inverted_key) >= number_of_unique_ciphers:
            return candidate_cipher  # we mapped every cipher letter to a plain letter
        elif len(ciphertext) < self.smallest_word_size:
            return None  # Could not find a key
        else:
            for word in self.dictionary.shuffle():
                copy_cipher = SubstitutionCipher(deepcopy(candidate_cipher.key))

                print(word, ciphertext, copy_cipher.key)

                word_plaintext = word
                word_ciphertext, remaining_ciphertext = ciphertext[:len(word_plaintext)], ciphertext[len(word_plaintext):]

                for m, c in zip(word_plaintext, word_ciphertext):
                    self.update_key(m, c, copy_cipher)

                if len(remaining_ciphertext) > self.smallest_word_size:
                    c, remaining_ciphertext = remaining_ciphertext[0], remaining_ciphertext[1:]
                    self.update_key(" ", c, copy_cipher)

                cipher = self.attack_recursive(remaining_ciphertext, number_of_unique_ciphers, copy_cipher)
                if cipher is not None:
                    return cipher

            return None

    @staticmethod
    def update_key(m, c, candidate_cipher):
        if c in candidate_cipher.inverted_key and candidate_cipher.inverted_key[c] != m:
            return None  # already mapped ciphertext letter to different plaintext letter
        elif c in candidate_cipher.inverted_key:
            pass  # already mapped ciphertext letter to same plaintext letter
        elif m in candidate_cipher.key:
            candidate_cipher.key[m].append(c)
        else:
            candidate_cipher.key[m] = [c]

    @property
    def smallest_word_size(self):
        return min([len(word) for word in self.dictionary])


def breaker_with_candidates(frequencies, candidates):
    dictionary = Dictionary([])

    for candidate in candidates:
        dictionary = dictionary.merge(candidate.dictionary())

    return breaker_with_dictionary(frequencies, dictionary)


def breaker_with_dictionary(frequencies, dictionary):
    return DictionaryCodeBreaker(frequencies, dictionary)
