from collections import Counter

from src.key import SPACE


class Scorer:
    def __init__(self, dictionary, frequencies):
        self.dictionary = dictionary
        self.frequencies = frequencies

    def best_key(self, keys):
        scores = self.compute_scores(keys)

        best_key, best_mse = scores[0]
        for pair in scores:
            c, s = pair
            if s < best_mse:
                best_key, best_mse = pair

        return best_key

    def compute_scores(self, keys):
        actual_frequencies = self.dictionary.letter_frequencies()

        scores = []
        for key in keys:
            plaintext_frequencies = self.letter_frequencies(key)

            frequency_difference = actual_frequencies - plaintext_frequencies

            mse = self.compute_mse(frequency_difference)

            scores.append((key, mse))

        return scores

    @staticmethod
    def letter_frequencies(key):
        plaintext = key.decrypt()
        plaintext_frequencies = Counter(plaintext)

        for letter in plaintext_frequencies:
            plaintext_frequencies[letter] /= len(plaintext.split(SPACE))

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
