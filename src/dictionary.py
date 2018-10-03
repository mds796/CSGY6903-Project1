import random
import itertools
from collections import Counter


class Dictionary:
    def __init__(self, words):
        self.words = words

    def merge(self, other):
        return Dictionary(list(set(self.words + other.words)))

    def shuffle(self, shuffler=random.shuffle):
        copy = list(self.words)

        shuffler(copy)

        return Dictionary(copy)

    def letters(self):
        return set(itertools.chain.from_iterable(self.words))

    def generate(self, max_size, indexer=random.randint):
        selected = []
        size = 0

        while size < max_size:
            index = indexer(0, len(self.words) - 1)

            word = self.words[index]

            size += len(word) + 1

            selected.append(word)
            selected.append(" ")

        return "".join(selected)[:max_size]

    def letter_frequencies(self):
        counter = Counter()

        for word in self.words:
            counter.update(word)

        for letter in counter:
            counter[letter] /= len(self.words)

        return counter

    def __hash__(self):
        return self.words.__hash__()

    def __eq__(self, other):
        return self.words.__eq__(other.words)

    def __len__(self):
        return self.words.__len__()

    def __iter__(self):
        return self.words.__iter__()


def read_from_file(filename):
    """
    Reads the dictionary from the given file.
    Each line is assumed to contain a single word in the dictionary.
    Whitespace is stripped at the beginning and end of each line.
    """
    words = []

    with open(filename) as f:
        for line in f:
            words.append(line.strip().lower())

    return Dictionary(words)
