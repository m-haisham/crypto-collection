from django.test import TestCase

from crypto.apps.luhn_algorithm.service import LuhnAlgorithm


class TestLuhnAlgorithm(TestCase):

    def test_check_valid(self):
        self.assertTrue(LuhnAlgorithm.check_valid("4024007112891345"))
        self.assertTrue(LuhnAlgorithm.check_valid("4916794754360611"))
        self.assertTrue(LuhnAlgorithm.check_valid("4024007163901440375"))
        self.assertTrue(LuhnAlgorithm.check_valid("5553415465036283"))
        self.assertTrue(LuhnAlgorithm.check_valid("5121595262320072"))
        self.assertTrue(LuhnAlgorithm.check_valid("5316211467945128"))

        self.assertFalse(LuhnAlgorithm.check_valid("5121595262310072"))
        self.assertFalse(LuhnAlgorithm.check_valid("5121595262320070"))
        self.assertFalse(LuhnAlgorithm.check_valid("4024007763901440375"))
        self.assertFalse(LuhnAlgorithm.check_valid("0024007112891345"))
