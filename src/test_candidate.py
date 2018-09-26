from unittest import TestCase

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
