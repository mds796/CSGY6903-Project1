from unittest import TestCase

import src.candidate
from src.candidate_attacker import CandidateAttacker
from src.cipher import generate_homophonic
from main import FREQUENCIES


class TestDictionaryAttacker(TestCase):
    def setUp(self):
        self.candidates = src.candidate.read_from_file("test1_candidate_5_plaintexts.txt")
        self.cipher = generate_homophonic(FREQUENCIES)
        self.attacker = CandidateAttacker(FREQUENCIES, self.candidates)

    def test_break_with_candidates(self):
        for plaintext in [candidate.text for candidate in self.candidates]:
            c = self.cipher.encrypt(plaintext)

            self.assertEqual(self.attacker.attack(c), plaintext)
