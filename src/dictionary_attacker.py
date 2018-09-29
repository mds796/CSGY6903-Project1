from copy import deepcopy

from src.attacker import Attacker
from src.cipher import DELIMITER, SubstitutionCipher
from src.scorer import Scorer

SPACE = " "


class DictionaryAttacker(Attacker):
    def __init__(self, frequencies, dictionary, *args, **kwargs):
        super().__init__(frequencies, *args, **kwargs)

        self.frequencies = frequencies
        self.dictionary = dictionary
        self.smallest_word = self.smallest_word_size()

    def smallest_word_size(self):
        if len(self.dictionary.words) == 0:
            return 0

        return min([len(word) for word in self.dictionary])

    def attack(self, ciphertext):
        if ciphertext == "" or ciphertext is None:
            return ""

        ciphertext_parts = [int(c) for c in ciphertext.split(DELIMITER)]
        accumulator = []

        self.attack_recursive(ciphertext_parts, SubstitutionCipher({}), accumulator)

        if len(accumulator) > 0:
            best_cipher = Scorer(self.dictionary, self.frequencies).min(ciphertext, accumulator)
            return best_cipher.decrypt(ciphertext)
        else:
            return None

    def attack_recursive(self, ciphertext_parts, candidate_cipher, accumulator):
        if len(ciphertext_parts) == 0:
            accumulator.append(candidate_cipher)
        elif len(ciphertext_parts) < self.smallest_word:
            pass  # Could not find a key
        else:
            for word in self.dictionary:
                copy_cipher = SubstitutionCipher(deepcopy(candidate_cipher.key))

                word_plaintext = word
                word_ciphertext = ciphertext_parts[:len(word_plaintext)]

                remaining_ciphertext = ciphertext_parts[len(word_plaintext):]

                try:
                    for m, c in zip(word_plaintext, word_ciphertext):
                        self.update_key(m, c, copy_cipher)

                    if len(remaining_ciphertext) > self.smallest_word:
                        c, remaining_ciphertext = remaining_ciphertext[0], remaining_ciphertext[1:]
                        self.update_key(SPACE, c, copy_cipher)
                except ValueError:
                    continue

                self.attack_recursive(remaining_ciphertext, copy_cipher, accumulator)

    @staticmethod
    def update_key(m, c, candidate_cipher):
        inverted_key = candidate_cipher.inverted_key

        if c in inverted_key and inverted_key[c] != m:
            raise (ValueError("Already mapped ciphertext letter to different plaintext letter."))
        elif c in inverted_key:
            pass  # already mapped ciphertext letter to same plaintext letter
        elif m in candidate_cipher.key:
            candidate_cipher.key[m].append(c)
        else:
            candidate_cipher.key[m] = [c]