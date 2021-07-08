from django.test import TestCase

from crypto.apps.hamming.services.hamming_code_service import HammingCodeService


class TestRedundantHammingCode(TestCase):
    service = HammingCodeService()

    def test_calculate_redundant_bits(self):
        self.assertEqual(3, self.service.calculate_redundant_bits(4))

    def test_generate_parity_positions(self):
        self.assertListEqual([1, 2, 4], list(self.service.generate_parity_positions(7)))

    def test_encode(self):
        self.assertEqual("1010010", self.service.encode("1010"))

    def test_detect_error(self):
        self.assertEqual(6, self.service.detect_error("0101010"))
