import hashlib

from django.test import TestCase

from .services import CrackingService


class TestPasswordCrackingService(TestCase):

    service = CrackingService()

    def test_generate_combinations(self):
        self.assertListEqual([b'aa', b'ab', b'ba', b'bb'], list(self.service.generate_combinations('ab', 2)))

    def test_brute_force(self):
        # we arent using longer words because testing would take longer
        test_words = [b'sef', b'ant', b'ng8']

        def encrypt(value: bytes) -> str:
            return hashlib.sha1(value).hexdigest()

        for word in test_words:
            self.assertEqual(word.decode('utf-8'), self.service.brute_force(encrypt(word), len(word), encrypt).keyword)

    def test_dictionary(self):
        dictionary = [b'1', b'2', b'three', b'4', b'8', b'10', b'twenty']

        def encrypt(value: bytes) -> str:
            return hashlib.sha1(value).hexdigest()

        test_words = [b'4', b'three']
        for word in test_words:
            self.assertEqual(word.decode(), self.service.crack(encrypt(word), dictionary, encrypt).keyword)

        test_words = [b'5', b'six']
        for word in test_words:
            self.assertIsNone(self.service.crack(encrypt(word), dictionary, encrypt).keyword)
