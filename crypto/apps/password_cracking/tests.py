import hashlib

from django.test import TestCase

from .services import PasswordCrackingService


class TestPasswordCrackingService(TestCase):

    service = PasswordCrackingService()

    def test_generate_combinations(self):
        self.assertListEqual(['aa', 'ab', 'ba', 'bb'], list(self.service.generate_combinations('ab', 2)))

    def test_brute_force(self):
        # we arent using longer words because testing would take longer
        test_words = ['sef', 'ant', 'ng8']

        def encrypt(value: str) -> str:
            return hashlib.sha1(value.encode('utf-8')).hexdigest()

        for word in test_words:
            self.assertEqual(word, self.service.brute_force(encrypt(word), len(word), encrypt))

    def test_dictionary(self):
        dictionary = ['1', '2', 'three', '4', '8', '10', 'twenty']

        def encrypt(value: str) -> str:
            return hashlib.sha1(value.encode('utf-8')).hexdigest()

        test_words = ['4', 'three']
        for word in test_words:
            self.assertEqual(word, self.service.crack(encrypt(word), dictionary, encrypt))

        test_words = ['5', 'six']
        for word in test_words:
            self.assertIsNone(self.service.crack(encrypt(word), dictionary, encrypt))
