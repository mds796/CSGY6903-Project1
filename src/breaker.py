from src.dictionary import Dictionary


class DictionaryCodeBreaker:
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def attack(self, ciphertext):
        return ""


def breaker_with_candidates(candidates):
    dictionary = Dictionary([])

    for candidate in candidates:
        dictionary = dictionary.merge(candidate.dictionary())

    return breaker_with_dictionary(dictionary)


def breaker_with_dictionary(dictionary):
    return DictionaryCodeBreaker(dictionary)
