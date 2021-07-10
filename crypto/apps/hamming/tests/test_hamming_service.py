from django.test import TestCase

from crypto.apps.hamming.services.hamming_service import HammingService


class TestHammingService(TestCase):
    service = HammingService()

    def test_calculate_redundant_bits(self):
        self.assertEqual(3, self.service.calculate_redundant_bits(4))

    def test_generate_parity_positions(self):
        self.assertListEqual([1, 2, 4], list(self.service.generate_parity_positions(7)))

    def test_bit_label(self):
        self.assertEqual('p1', self.service.bit_label(1))
        self.assertEqual('p2', self.service.bit_label(2))
        self.assertEqual('d3', self.service.bit_label(3))
        self.assertEqual('p4', self.service.bit_label(4))
        self.assertEqual('d5', self.service.bit_label(5))
        self.assertEqual('d6', self.service.bit_label(6))
        self.assertEqual('d7', self.service.bit_label(7))
        self.assertEqual('p8', self.service.bit_label(8))

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
        self.assertTupleEqual(("0100101", 0), self.service.detect_error("0100101"))
        self.assertTupleEqual(("0100101", 2), self.service.detect_error("0000101"))

        self.assertTupleEqual(("1011010", 0), self.service.detect_error("1011010"))
        self.assertTupleEqual(("1011010", 1), self.service.detect_error("0011010"))

        self.assertTupleEqual(("0000000", 0), self.service.detect_error("0000000"))
        self.assertTupleEqual(("0000000", 7), self.service.detect_error("0000001"))

        self.assertTupleEqual(("1111111", 0), self.service.detect_error("1111111"))
        self.assertTupleEqual(("1111111", 4), self.service.detect_error("1110111"))

    def test_detect_error_odd(self):
        self.assertTupleEqual(("1001101", 0), self.service.detect_error("1001101", False))
        self.assertTupleEqual(("1001101", 2), self.service.detect_error("1101101", False))

        self.assertTupleEqual(("0110010", 0), self.service.detect_error("0110010", False))
        self.assertTupleEqual(("0110010", 1), self.service.detect_error("1110010", False))

        self.assertTupleEqual(("1101000", 0), self.service.detect_error("1101000", False))
        self.assertTupleEqual(("1101000", 7), self.service.detect_error("1101001", False))

        self.assertTupleEqual(("0010111", 0), self.service.detect_error("0010111", False))
        self.assertTupleEqual(("0010111", 4), self.service.detect_error("0011111", False))

    def test_decode(self):
        self.assertEqual("1011", self.service.decode("1010011"))
        self.assertEqual("0010", self.service.decode("1101010"))
        self.assertEqual("1111", self.service.decode("0110111"))
