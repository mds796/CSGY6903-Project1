import random

INVALID_LETTER = "_"
INVALID_CIPHER = "-1"


class SubstitutionCipher:
    def __init__(self, key, scheduler):
        self.scheduler = scheduler
        self.encryption_key = key
        self.decryption_key = self.inverted_key()

    def encrypt(self, plaintext):
        if plaintext is "" or plaintext is None:
            return ""

        ciphertext = []

        for letter in plaintext:
            c = INVALID_CIPHER

            if letter in self.encryption_key:
                c = self.scheduler(self.encryption_key[letter])

            ciphertext.append(str(c))

        return ",".join(ciphertext)

    def decrypt(self, ciphertext):
        if ciphertext is "" or ciphertext is None:
            return ""

        plaintext = []

        for value in ciphertext.split(","):
            i = int(value)
            if i in self.decryption_key:
                plaintext.append(self.decryption_key[i])
            else:
                plaintext.append(INVALID_LETTER)

        return "".join(plaintext)

    def inverted_key(self):
        key = {}

        for letter in self.encryption_key:
            for i in self.encryption_key[letter]:
                key[i] = letter

        return key


def generate_homophonic(frequencies):
    """Generates a homophonic substitution key."""
    assignments = assign_substitution_to_letter(frequencies)

    key = {}

    for i in range(0, len(assignments)):
        letter = assignments[i]

        if letter in key:
            key[letter].append(i)
        else:
            key[letter] = [i]

    return SubstitutionCipher(key, lambda substitutions: random.randint(0, len(substitutions) - 1))


def assign_substitution_to_letter(frequencies):
    """Create a list of letters where each letter occurs a number of times equal to their their frequency."""
    assignments = []

    for letter in frequencies:
        for j in range(0, frequencies[letter]):
            assignments.append(letter)

    random.shuffle(assignments)

    return assignments
