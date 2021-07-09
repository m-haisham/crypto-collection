from django.test import TestCase

from crypto.apps.hamming.services.hamming_service import HammingService


class TestHammingService(TestCase):
    service = HammingService()

    def test_calculate_redundant_bits(self):
        self.assertEqual(3, self.service.calculate_redundant_bits(4))

    def test_generate_parity_positions(self):
        self.assertListEqual([1, 2, 4], list(self.service.generate_parity_positions(7)))

    def test_encode_even(self):
        self.assertEqual("0100101", self.service.encode("0101"))
        self.assertEqual("1011010", self.service.encode("1010"))
        self.assertEqual("0000000", self.service.encode("0000"))
        self.assertEqual("1111111", self.service.encode("1111"))

    def test_encode_odd(self):
        self.assertEqual("1001101", self.service.encode("0101", False))
        self.assertEqual("0110010", self.service.encode("1010", False))
        self.assertEqual("1101000", self.service.encode("0000", False))
        self.assertEqual("0010111", self.service.encode("1111", False))

    def test_detect_error_even(self):
        self.assertEqual(0, self.service.detect_error("0100101"))
        self.assertEqual(2, self.service.detect_error("0000101"))

        self.assertEqual(0, self.service.detect_error("1011010"))
        self.assertEqual(1, self.service.detect_error("0011010"))

        self.assertEqual(0, self.service.detect_error("0000000"))
        self.assertEqual(7, self.service.detect_error("0000001"))

        self.assertEqual(0, self.service.detect_error("1111111"))
        self.assertEqual(4, self.service.detect_error("1110111"))

    def test_detect_error_odd(self):
        self.assertEqual(0, self.service.detect_error("1001101", False))
        self.assertEqual(2, self.service.detect_error("1101101", False))

        self.assertEqual(0, self.service.detect_error("0110010", False))
        self.assertEqual(1, self.service.detect_error("1110010", False))

        self.assertEqual(0, self.service.detect_error("1101000", False))
        self.assertEqual(7, self.service.detect_error("1101001", False))

        self.assertEqual(0, self.service.detect_error("0010111", False))
        self.assertEqual(4, self.service.detect_error("0011111", False))

    def test_decode(self):
        self.assertEqual("1010", self.service.decode("1010011"))
        self.assertEqual("1100", self.service.decode("1101010"))
        self.assertEqual("0111", self.service.decode("0110111"))
