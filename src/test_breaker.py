from unittest import TestCase

import random
import src.candidate
import src.dictionary
from src.breaker import breaker_with_candidates, breaker_with_dictionary
from src.cipher import generate_homophonic
from src.main import FREQUENCIES


class TestDictionaryCodeBreaker(TestCase):
    def setUp(self):
        self.cipher = generate_homophonic(FREQUENCIES)

    def test_break_with_candidates(self):
        candidates = src.candidate.read_from_file("test1_candidate_5_plaintexts.txt")

        self.breaker = breaker_with_candidates(candidates)

        for plaintext in [candidate.text for candidate in candidates]:
            c = self.cipher.encrypt(plaintext)

            self.assertEqual(self.breaker.attack(c), plaintext)

    def test_break_with_dictionary(self):
        dictionary = src.dictionary.read_from_file("test2_candidate_70_english_words.txt")

        self.breaker = breaker_with_dictionary(dictionary)

        plaintext = dictionary.generate(500, random.randint)
        c = self.cipher.encrypt(plaintext)

        self.assertEqual(self.breaker.attack(c), plaintext)
