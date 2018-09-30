from collections import Counter


class Scorer:
    def __init__(self, dictionary, frequencies):
        self.dictionary = dictionary
        self.frequencies = frequencies

    def min(self, ciphertext, ciphers):
        actual_frequencies = self.dictionary.letter_frequencies()

        scores = []
        for cipher in ciphers:
            plaintext_frequencies = self.letter_frequencies(cipher, ciphertext)

            frequency_difference = actual_frequencies - plaintext_frequencies

            mse = self.compute_mse(frequency_difference)

            scores.append((cipher, mse))

        best_cipher, best_mse = scores[0]

        for pair in scores:
            c, s = pair
            if s < best_mse:
                best_cipher, best_mse = pair

        return best_cipher

    @staticmethod
    def letter_frequencies(cipher, ciphertext):
        plaintext = cipher.decrypt(ciphertext)
        plaintext_frequencies = Counter(plaintext)

        for letter in plaintext_frequencies:
            plaintext_frequencies[letter] /= len(plaintext.split(" "))

        return plaintext_frequencies

    @staticmethod
    def compute_mse(frequency_difference):
        mse = 0

        if len(frequency_difference) == 0:
            return mse

        for l in frequency_difference:
            mse += frequency_difference[l] ** 2

        mse /= len(frequency_difference)

        return mse
