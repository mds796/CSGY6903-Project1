from src.attacker import SPACE
from src.cipher import DELIMITER, INVALID_LETTER


class CandidateKey:
    def __init__(self, cipher_text, key, inverted_key, frequencies):
        self.cipher_text = cipher_text
        self.cipher_text_index = 0

        self.key = key
        self.inverted_key = inverted_key
        self.frequencies = frequencies

        self._cipher_text_parts = None  # memoized

    @property
    def remaining_cipher_text_parts(self):
        return self.cipher_text_parts[self.cipher_text_index:]

    @property
    def cipher_text_parts(self):
        """Parses the cipher text string into a list of integers."""
        if self._cipher_text_parts is not None:
            return self._cipher_text_parts

        self._cipher_text_parts = [int(c) for c in self.cipher_text.split(DELIMITER)]

        return self._cipher_text_parts

    def word_cipher_text_parts(self, word):
        word_size = len(word)

        previous_index = self.cipher_text_index
        self.cipher_text_index += word_size

        return self.cipher_text_parts[previous_index:self.cipher_text_index]

    def is_valid_key(self):
        """A key is not valid if we assigned more cipher_texts to a letter than the frequencies allow."""
        for letter in self.key:
            if len(self.key[letter]) > self.frequencies[letter]:
                return False

        return len(self.remaining_cipher_text_parts) == 0

    def add_assignment(self, word, smallest_word_size):
        """
        Adds an assignment of a letter to a cipher_text.
        Returns True if the assignment was successful, false otherwise.
        """

        if self.must_add_space(smallest_word_size, word):
            word += SPACE

        word_cipher_text_parts = self.word_cipher_text_parts(word)

        if self.is_invalid_word_assignment(smallest_word_size):
            return False

        for letter, cipher_text in zip(word, word_cipher_text_parts):
            if self.is_invalid_letter_assignment(letter, cipher_text):
                return False

            if letter in self.key and cipher_text not in self.key[letter]:
                self.key[letter].append(cipher_text)
            elif letter not in self.key:
                self.key[letter] = [cipher_text]

            self.inverted_key[cipher_text] = letter

        return True

    def must_add_space(self, smallest_word_size, word):
        return (len(self.remaining_cipher_text_parts) - len(word)) >= smallest_word_size + 1

    def is_invalid_word_assignment(self, smallest_word_size):
        remaining_parts = len(self.remaining_cipher_text_parts)

        if remaining_parts < 0 or remaining_parts < smallest_word_size:
            return False  # not enough space for the word, or space to add the next word

    def is_invalid_letter_assignment(self, letter, cipher_text):
        return self.cipher_is_assigned(letter, cipher_text) or self.has_too_many_cipher_texts(letter, cipher_text)

    def cipher_is_assigned(self, letter, cipher_text):
        return cipher_text in self.inverted_key and self.inverted_key[cipher_text] != letter

    def has_too_many_cipher_texts(self, letter, cipher_text):
        cipher_texts = self.key.get(letter, [])
        return cipher_text not in cipher_texts and len(cipher_texts) >= self.frequencies[letter]

    def decrypt(self):
        """Decrypts the cipher text for this candidate key using the inverted key."""
        if self.cipher_text is "" or self.cipher_text is None:
            return ""

        plaintext = []

        for cipher_text in self.cipher_text_parts:
            if cipher_text in self.inverted_key:
                plaintext.append(self.inverted_key[cipher_text])
            else:
                plaintext.append(INVALID_LETTER)

        return "".join(plaintext)


class GenericAttacker:
    def __init__(self, frequencies, candidates, dictionary):
        self.frequencies = frequencies
        self.candidates = candidates
        self.dictionary = dictionary

        self._smallest_word_size = None  # memoized

    def attack(self, cipher_text):
        """Attacks the given cipher text, to determine the encrypted plain text"""
        return self.candidates_attack(cipher_text)

    def candidates_attack(self, cipher_text):
        """Attacks the cipher_tet using the candidate texts."""
        for candidate in self.candidates:
            plain_text = self.candidate_attack(candidate, cipher_text)

            if plain_text is not None:
                return plain_text

        return ""

    def candidate_attack(self, candidate, cipher_text):
        """Attacks the given cipher text using the given candidate. Returns None if no valid key was found."""
        candidate_key = CandidateKey(cipher_text, {}, {}, self.frequencies)

        for word in candidate.words:
            success = candidate_key.add_assignment(word, self.smallest_word_size)
            if not success:
                return None

        if candidate_key.is_valid_key():
            return candidate_key.decrypt()
        else:
            return None

    @property
    def smallest_word_size(self):
        if self._smallest_word_size is not None:
            return self._smallest_word_size

        if len(self.dictionary.words) == 0:
            self._smallest_word_size = 0
        else:
            self._smallest_word_size = min([len(word) for word in self.dictionary])

        return self._smallest_word_size