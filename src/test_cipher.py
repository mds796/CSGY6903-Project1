from unittest import TestCase

from src.cipher import SubstitutionCipher, generate_homophonic


class TestSubstitutionCipher(TestCase):
    def setUp(self):
        self.cipher = SubstitutionCipher({"a": [1], "b": [2, 3]}, lambda subs: subs[-1])

    def test_encrypt_with_valid_message(self):
        self.assertEqual(self.cipher.encrypt("abab"), "1,3,1,3")

    def test_encrypt_with_invalid_message(self):
        self.assertEqual(self.cipher.encrypt("acad"), "1,-1,1,-1")

    def test_encrypt_with_empty_message(self):
        self.assertEqual(self.cipher.encrypt(""), "")

    def test_decrypt_with_valid_message(self):
        self.assertEqual(self.cipher.decrypt("1,3,1,3"), "abab")

    def test_decrypt_with_unexpected_message(self):
        self.assertEqual(self.cipher.decrypt("1,2,1,2"), "abab")

    def test_decrypt_with_invalid_message(self):
        self.assertEqual(self.cipher.decrypt("1,-1,1,-1"), "a_a_")

    def test_decrypt_with_empty_message(self):
        self.assertEqual(self.cipher.decrypt(""), "")

    def test_generated_key(self):
        self.cipher = generate_homophonic({"a": 1, "b": 1})

        a_mapping = self.cipher.key["a"][0]
        b_mapping = self.cipher.key["b"][0]

        c = self.cipher.encrypt("abcba")

        self.assertEqual(c, "%d,%d,%d,%d,%d" % (a_mapping, b_mapping, -1, b_mapping, a_mapping))
        self.assertEqual(self.cipher.decrypt(c), "ab_ba")
