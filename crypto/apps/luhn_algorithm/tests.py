from django.test import TestCase

from .models import CreditCardType
from .service import LuhnAlgorithm, CreditCardService


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


class TestCreditCardService(TestCase):

    def test_identify_type(self):
        self.assertEqual(CreditCardType.amex, CreditCardService.identify_type('342163513684'))
        self.assertEqual(CreditCardType.amex, CreditCardService.identify_type('3716853584'))
        self.assertNotEqual(CreditCardType.amex, CreditCardService.identify_type('51385416384'))

        self.assertEqual(CreditCardType.master_card, CreditCardService.identify_type('51385416384'))
        self.assertEqual(CreditCardType.master_card, CreditCardService.identify_type('5421654136854'))
        self.assertNotEqual(CreditCardType.master_card, CreditCardService.identify_type('3716853584'))

        self.assertEqual(CreditCardType.visa, CreditCardService.identify_type('468514368451'))
        self.assertNotEqual(CreditCardType.visa, CreditCardService.identify_type('5368435241'))

        self.assertEqual(CreditCardType.discover, CreditCardService.identify_type('60116348541635241'))
        self.assertEqual(CreditCardType.discover, CreditCardService.identify_type('622126354136'))
        self.assertEqual(CreditCardType.discover, CreditCardService.identify_type('62292535a63544136'))
        self.assertEqual(CreditCardType.discover, CreditCardService.identify_type('648354134'))
        self.assertNotEqual(CreditCardType.discover, CreditCardService.identify_type('75452151'))
