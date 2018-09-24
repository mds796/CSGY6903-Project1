def readDictionary(filename):
    """
    Reads the dictionary from the given file.
    Each line is assumed to contain a single word in the dictionary.
    Whitespace is stripped at the beginning and end of each line.
    """
    words = []

    with open(filename) as f:
        for line in f:
            words.append(line.strip())

    return words


def readCandidates(filename):
    """
    Reads the set of known plaintexts from the given file.
    """
    candidates = []

    with open(filename) as f:
        readTest(f)
        
        while True:
            candidate = readCandidate(f)
            if candidate == "":
                break
            else:
                candidates.append(candidate)

    return candidates 

def readTest(f):
    f.readline() # Test 1
    f.readline() # Blank line

def readCandidate(f):
    """Reads a candidate plaintext from the given file"""
    f.readline().strip() # Candidate N
    f.readline() # Blank line

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
            candidate.append(line.strip())

    return "".join(candidate)

