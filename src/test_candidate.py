from unittest import TestCase

import src
from src.candidate import Candidate


class TestCandidate(TestCase):
    def setUp(self):
        self.candidate = Candidate("foo bar baz")

    def test_dictionary_when_not_empty(self):
        self.assertTrue("foo" in self.candidate.dictionary())

    def test_dictionary_when_empty(self):
        self.assertFalse("" in Candidate("").dictionary())

    def test_dictionary_when_none(self):
        with self.assertRaises(AttributeError, msg="'NoneType' object has no attribute 'split'") as contextManager:
            "" in Candidate(None).dictionary()

    def test_read_from_file(self):
        candidates = src.candidate.read_from_file("test1_candidate_5_plaintexts.txt")

        self.assertEqual(len(candidates), 5)
        self.assertTrue("punners" in candidates[-1].dictionary())