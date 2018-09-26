from src.dictionary import Dictionary


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
        f.readline()  # Test 1
        f.readline()  # Blank line

        while True:
            candidate = read_candidate(f)
            if candidate == "":
                break
            else:
                candidates.append(candidate)

    return candidates


def read_candidate(f):
    """Reads a candidate plaintext from the given file"""
    f.readline().strip()  # Candidate N
    f.readline()  # Blank line

    candidate = []

    while True:
        position = f.tell()
        line = f.readline()
        if not line:
            break

        if line.startswith("Candidate"):
            f.seek(position)
            break
        else:
            candidate.append(line.strip().lower())

    return Candidate("".join(candidate))

