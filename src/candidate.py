from src.dictionary import Dictionary


class Candidate:
    def __init__(self, text):
        self.text = text

    def dictionary(self):
        return Dictionary(self.words)

    @property
    def words(self):
        words = self.text.split(" ")

        if "" in words:
            words.remove("")

        return words


def read_from_file(filename):
    """
    Reads the set of known plaintexts from the given file.
    """

    candidates = []

    with open(filename) as f:
        lines = f.readlines()

        if len(lines) > 5:
            # from first candidate,
            # to the end of the file,
            # counting in increments of lines between candidates
            for i in range(4, len(lines), 4):
                candidates.append(Candidate(lines[i].strip().lower()))

    return candidates


def merge_dictionary(candidates):
    dictionary = Dictionary([])

    for candidate in candidates:
        dictionary = dictionary.merge(candidate.dictionary())

    return dictionary
