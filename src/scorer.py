from collections import Counter


class Scorer:
    def __init__(self, dictionary, frequencies):
        self.dictionary = dictionary
        self.frequencies = frequencies

    def min(self, ciphertext, ciphers):
        actual_frequencies = self.dictionary.letter_frequencies()

        scores = []
        for cipher in ciphers:
            plaintext = cipher.decrypt(ciphertext)
            plaintext_frequencies = Counter(plaintext)
            frequency_difference = actual_frequencies - plaintext_frequencies

            mse = 0
            for l in frequency_difference:
                mse += frequency_difference[l]

            mse /= len(frequency_difference)

            scores.append((cipher, mse))

        best_cipher, best_mse = scores[0]

        for pair in scores:
            c, s = pair
            if s > best_mse:
                best_cipher, best_mse = pair

        return best_cipher
