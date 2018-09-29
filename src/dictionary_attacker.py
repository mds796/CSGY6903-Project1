from copy import deepcopy

from src.attacker import Attacker
from src.cipher import DELIMITER, SubstitutionCipher
from src.scorer import Scorer


class DictionaryAttacker(Attacker):
    def __init__(self, frequencies, dictionary, *args, **kwargs):
        super().__init__(frequencies, *args, **kwargs)

        self.frequencies = frequencies
        self.dictionary = dictionary

    def attack(self, ciphertext):
        if ciphertext == "" or ciphertext is None:
            return ""

        ciphers = [int(c) for c in ciphertext.split(DELIMITER)]

        accumulator = []

        self.attack_recursive(ciphers, SubstitutionCipher({}), accumulator)

        if len(accumulator) > 0:
            return Scorer(self.dictionary, self.frequencies).min(ciphertext, accumulator).decrypt(ciphertext)
        else:
            return None

    def attack_recursive(self, ciphertext, candidate_cipher, accumulator):
        if len(ciphertext) == 0:
            accumulator.append(candidate_cipher)
        elif len(ciphertext) < self.smallest_word_size:
            return # Could not find a key
        else:
            for word in self.dictionary.shuffle():
                copy_cipher = SubstitutionCipher(deepcopy(candidate_cipher.key))

                word_plaintext = word
                word_ciphertext, remaining_ciphertext = ciphertext[:len(word_plaintext)], ciphertext[
                                                                                          len(word_plaintext):]

                for m, c in zip(word_plaintext, word_ciphertext):
                    self.update_key(m, c, copy_cipher)

                if len(remaining_ciphertext) > self.smallest_word_size:
                    c, remaining_ciphertext = remaining_ciphertext[0], remaining_ciphertext[1:]
                    self.update_key(" ", c, copy_cipher)

                self.attack_recursive(remaining_ciphertext, copy_cipher, accumulator)

            return

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
