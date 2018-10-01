from unittest import TestCase

import src.candidate
import src.dictionary
from src.generic_attacker import GenericAttacker
from src.cipher import generate_homophonic
from src.dictionary import Dictionary
from src.main import FREQUENCIES


class TestDictionaryAttacker(TestCase):
    def setUp(self):
        self.candidates = src.candidate.read_from_file("test1_candidate_5_plaintexts.txt")
        self.dictionary = Dictionary(src.dictionary.read_from_file("test2_candidate_70_english_words.txt").shuffle().words[0:5])
        self.cipher = generate_homophonic(FREQUENCIES)
        self.attacker = GenericAttacker(FREQUENCIES, [], self.dictionary)

    def test_break_with_candidates(self):
        self.attacker = GenericAttacker(FREQUENCIES, self.candidates, src.candidate.merge_dictionary(self.candidates))

        for plaintext in [candidate.text for candidate in self.candidates]:
            c = self.cipher.encrypt(plaintext)

            self.assertEqual(self.attacker.attack(c), plaintext)

    def test_break_with_dictionary(self):
        plaintext = self.dictionary.generate(20)
        c = self.cipher.encrypt(plaintext)

        self.assertEqual(self.attacker.attack(c), plaintext)

    def test_attack_when_one(self):
        self.assertEqual(self.attacker.attack(self.cipher.encrypt("foo")), "foo")

    def test_attack_when_one_repeated(self):
        self.assertEqual(self.attacker.attack(self.cipher.encrypt("foo foo")), "foo foo")

    def test_attack_when_multiple_repeated(self):
        self.assertEqual(self.attacker.attack(self.cipher.encrypt("foo bar foo bar")), "foo bar foo bar")

    def test_attack_when_empty(self):
        self.assertEqual(self.attacker.attack(""), "")

    def test_attack_when_none(self):
        self.assertEqual(self.attacker.attack(None), "")
