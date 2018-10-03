from unittest import TestCase

import src.dictionary
from src.cipher import generate_homophonic
from src.dictionary import Dictionary
from src.dictionary_attacker import DictionaryAttacker
from src.main import FREQUENCIES


class TestDictionaryAttacker(TestCase):
    def setUp(self):
        self.dictionary = src.dictionary.read_from_file("test2_candidate_70_english_words.txt")
        self.cipher = generate_homophonic(FREQUENCIES)
        self.attacker = DictionaryAttacker(FREQUENCIES, self.dictionary)

    def test_break_with_dictionary(self):
        plaintext = self.dictionary.generate(500)
        c = self.cipher.encrypt(plaintext)

        self.assertEqual(self.attacker.attack(c), plaintext)

    def test_attack_when_one(self):
        self.attacker = DictionaryAttacker(FREQUENCIES, Dictionary(["foo"]))
        self.assertEqual(self.attacker.attack(self.cipher.encrypt("foo")), "foo")

    def test_attack_when_one_repeated(self):
        self.attacker = DictionaryAttacker(FREQUENCIES, Dictionary(["foo"]))
        self.assertEqual(self.attacker.attack(self.cipher.encrypt("foo foo fo")), "foo foo fo")

    def test_attack_when_empty(self):
        self.assertEqual(self.attacker.attack(""), "")

    def test_attack_when_none(self):
        self.assertEqual(self.attacker.attack(None), "")
