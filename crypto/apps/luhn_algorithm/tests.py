from django.test import TestCase

from .models import CreditCardIssuer as Issuer
from .service import validate_credit_card, CreditCardService, luhn_algorithm


class TestLuhnAlgorithm(TestCase):

    def test_check_valid(self):
        valid = [
            "4024007112891345",
            "4556374524048633",
            "4024007163901440375",
            "5553415465036283",
            "5121595262320072",
            "5316211467945128",
        ]

        for number in valid:
            self.assertTrue(validate_credit_card(number))

        invalid = [
            "5121595262310072",
            "5121595262320070",
            "4024007763901440375",
            "0024007112891345",
        ]

        for number in invalid:
            self.assertFalse(validate_credit_card(number))


class TestCreditCardService(TestCase):
    cards = {
        '8800000000000000': Issuer.unionpay,

        '4026000000000000': Issuer.electron,
        '4175000000000000': Issuer.electron,
        '4405000000000000': Issuer.electron,
        '4508000000000000': Issuer.electron,
        '4844000000000000': Issuer.electron,
        '4913000000000000': Issuer.electron,
        '4917000000000000': Issuer.electron,

        '5019000000000000': Issuer.dankort,

        '5018000000000000': Issuer.maestro,
        '5020000000000000': Issuer.maestro,
        '5038000000000000': Issuer.maestro,
        '5612000000000000': Issuer.maestro,
        '5893000000000000': Issuer.maestro,
        '6304000000000000': Issuer.maestro,
        '6759000000000000': Issuer.maestro,
        '6761000000000000': Issuer.maestro,
        '6762000000000000': Issuer.maestro,
        '6763000000000000': Issuer.maestro,
        '0604000000000000': Issuer.maestro,
        '6390000000000000': Issuer.maestro,

        '3528000000000000': Issuer.jcb,
        '3589000000000000': Issuer.jcb,
        '3529000000000000': Issuer.jcb,

        '6360000000000000': Issuer.interpayment,

        '4916338506082832': Issuer.visa,
        '4556015886206505': Issuer.visa,
        '4539048040151731': Issuer.visa,
        '4024007198964305': Issuer.visa,
        '4716175187624512': Issuer.visa,

        '5280934283171080': Issuer.master_card,
        '5456060454627409': Issuer.master_card,
        '5331113404316994': Issuer.master_card,
        '5259474113320034': Issuer.master_card,
        '5442179619690834': Issuer.master_card,

        '6011894492395579': Issuer.discover,
        '6011388644154687': Issuer.discover,
        '6011880085013612': Issuer.discover,
        '6011652795433988': Issuer.discover,
        '6011375973328347': Issuer.discover,

        '345936346788903': Issuer.amex,
        '377669501013152': Issuer.amex,
        '373083634595479': Issuer.amex,
        '370710819865268': Issuer.amex,
        '371095063560404': Issuer.amex
    }

    def test_identify_type(self):
        for number, card in self.cards.items():
            self.assertEqual(card, CreditCardService.identify_type(number))

    def test_generate_card_number(self):
        for issuer in Issuer.values:
            for i in range(5):
                number = CreditCardService.generate_card_number(issuer)

                self.assertTrue(validate_credit_card(number))
                self.assertEqual(issuer, CreditCardService.identify_type(number))
                self.assertTrue(len(number) >= 12)
