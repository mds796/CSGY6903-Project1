from unittest import TestCase

import src
from src.dictionary import Dictionary


class TestDictionary(TestCase):
    def setUp(self):
        self.dictionary = Dictionary(["foo", "bar"])

    def test_generate(self):
        text = self.dictionary.generate(10, indexer)

        self.assertEqual("foo foo", text)

    def test_shuffle(self):
        shuffled = self.dictionary.shuffle(shuffle)

        self.assertTrue("foo" in shuffled)
        self.assertNotEqual(shuffled, self.dictionary)

    def test_contains_when_in_dictionary(self):
        self.assertTrue("foo" in self.dictionary)

    def test_contains_when_not_in_dictionary(self):
        self.assertFalse("baz" in self.dictionary)

    def test_contains_when_dictionary_is_empty(self):
        self.assertFalse("baz" in Dictionary([]))

    def test_contains_when_dictionary_is_none(self):
        with self.assertRaises(TypeError, msg="Words must be a list."):
            "baz" in Dictionary(None)

    def test_contains_when_word_is_none(self):
        self.assertFalse(None in self.dictionary)

    def test_contains_when_word_is_not_a_string(self):
        self.assertFalse(1 in self.dictionary)

    def test_merge_when_other_is_empty(self):
        self.assertEqual(self.dictionary.merge(Dictionary([])), self.dictionary)

    def test_merge_when_this_is_empty(self):
        self.assertEqual(Dictionary([]).merge(self.dictionary), self.dictionary)

    def test_merge_when_this_is_none(self):
        with self.assertRaises(AttributeError, msg="'NoneType' object has no attribute 'words'"):
            self.dictionary.merge(None)

    def test_read_from_file(self):
        self.dictionary = src.dictionary.read_from_file("test2_candidate_70_english_words.txt")

        self.assertEqual(len(self.dictionary), 70)
        self.assertTrue("vessel" in self.dictionary)


def shuffle(l):
    l[0], l[-1] = l[-1], l[0]


def indexer(start, end):
    return start
