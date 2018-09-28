# from src.dictionary import Dictionary


""" Path changed by Siddharth"""
from dictionary import Dictionary

class Candidate:
    def __init__(self, text):
        self.text = text

    def dictionary(self):
        words = self.text.split(" ")

        if "" in words:
            words.remove("")

        return Dictionary(words)


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


def read_file_simple(filename):
    content = None
    with open(filename, 'r') as f:
        content = f.readlines()
        return content