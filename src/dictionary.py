class Dictionary:
    def __init__(self, words):
        self.words = words

    def merge(self, other):
        return Dictionary(self.words + other.words)

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

