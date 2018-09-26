from unittest import TestCase, skip

import src.candidate
import src.dictionary
from src.breaker import breaker_with_candidates, breaker_with_dictionary, DictionaryCodeBreaker
from src.cipher import generate_homophonic
from src.dictionary import Dictionary
from src.main import FREQUENCIES


class TestDictionaryCodeBreaker(TestCase):
    def setUp(self):
        self.cipher = generate_homophonic(FREQUENCIES)

    def test_break_with_candidates(self):
        candidates = src.candidate.read_from_file("test1_candidate_5_plaintexts.txt")

        self.breaker = breaker_with_candidates(FREQUENCIES, candidates)

        for plaintext in [candidate.text for candidate in candidates]:
            c = self.cipher.encrypt(plaintext)

            self.assertEqual(self.breaker.attack(c), plaintext)

    @skip
    def test_break_with_dictionary(self):
        dictionary = src.dictionary.read_from_file("test2_candidate_70_english_words.txt")

        self.breaker = breaker_with_dictionary(FREQUENCIES, dictionary)

        plaintext = dictionary.generate(500)
        c = self.cipher.encrypt(plaintext)

        self.assertEqual(self.breaker.attack(c), plaintext)

    def test_attack_when_one(self):
        self.breaker = DictionaryCodeBreaker({}, Dictionary(["foo"]))

        self.assertEqual(self.breaker.attack(self.cipher.encrypt("foo")), "foo")

    def test_attack_when_one_repeated(self):
        self.breaker = DictionaryCodeBreaker({}, Dictionary(["foo"]))

        self.assertEqual(self.breaker.attack(self.cipher.encrypt("foo foo")), "foo foo")

    def test_attack_when_multiple_repeated(self):
        self.breaker = DictionaryCodeBreaker({}, Dictionary(["foo", "bar"]))

        self.assertEqual(self.breaker.attack(self.cipher.encrypt("foo bar foo bar")), "foo bar foo bar")

    def test_attack_when_empty(self):
        self.breaker = DictionaryCodeBreaker({}, Dictionary([]))

        self.assertEqual(self.breaker.attack(""), "")

    def test_attack_when_none(self):
        self.breaker = DictionaryCodeBreaker({}, Dictionary([]))

        self.assertEqual(self.breaker.attack(None), "")
