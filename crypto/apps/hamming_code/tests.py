from django.test import TestCase

from .services import HammingService


class TestHammingService(TestCase):
    service = HammingService()

    def test_calculate_redundant_bits(self):
        self.assertEqual(3, self.service.calculate_redundant_bits(4))

    def test_generate_parity_positions(self):
        self.assertListEqual([1, 2, 4], list(self.service.generate_parity_positions(7)))

    def test_bit_label(self):
        data = {
            'p1': 1,
            'p2': 2,
            'd3': 3,
            'p4': 4,
            'd5': 5,
            'd6': 6,
            'd7': 7,
            'p8': 8,
        }

        for expected, test in data.items():
            self.assertEqual(expected, self.service.bit_label(test))

    def test_encode_even(self):
        data = {
            "0100101": "0101",
            "1011010": "1010",
            "0000000": "0000",
            "1111111": "1111",
        }

        for expected, test in data.items():
            self.assertEqual(expected, self.service.encode(test))

    def test_encode_odd(self):
        data = {
            "1001101": ("0101", False),
            "0110010": ("1010", False),
            "1101000": ("0000", False),
            "0010111": ("1111", False),
        }

        for expected, test in data.items():
            self.assertEqual(expected, self.service.encode(*test))

    def test_detect_error_even(self):
        data = {
            ("0100101", 0): "0100101",
            ("0100101", 2): "0000101",

            ("1011010", 0): "1011010",
            ("1011010", 1): "0011010",

            ("0000000", 0): "0000000",
            ("0000000", 7): "0000001",

            ("1111111", 0): "1111111",
            ("1111111", 4): "1110111",
        }

        for expected, test in data.items():
            self.assertTupleEqual(expected, self.service.detect_error(test))

    def test_detect_error_odd(self):
        data = {
            ("1001101", 0): ("1001101", False),
            ("1001101", 2): ("1101101", False),

            ("0110010", 0): ("0110010", False),
            ("0110010", 1): ("1110010", False),

            ("1101000", 0): ("1101000", False),
            ("1101000", 7): ("1101001", False),

            ("0010111", 0): ("0010111", False),
            ("0010111", 4): ("0011111", False),
        }

        for expected, test in data.items():
            self.assertTupleEqual(expected, self.service.detect_error(*test))

    def test_decode(self):
        data = {
            "1011": "1010011",
            "0010": "1101010",
            "1111": "0110111",
        }

        for expected, test in data.items():
            self.assertEqual(expected, self.service.decode(test))
