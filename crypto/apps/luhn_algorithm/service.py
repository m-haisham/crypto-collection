import re
from typing import List, Union, Optional

from crypto.apps.luhn_algorithm.models import CreditCardIssuer as Issuer


class LuhnAlgorithm:

    @staticmethod
    def check_valid(sequence: Union[str, List[int]]) -> bool:
        if type(sequence) == str:
            sequence = [int(digit) for digit in sequence]

        for i in range(len(sequence) % 2, len(sequence), 2):
            value = sequence[i] * 2
            if value > 9:
                value = sum([int(digit) for digit in str(value)])

            sequence[i] = value

        return sum(sequence) % 10 == 0


class CreditCardService:
    system_map = {
        '3': 'Travel/Entertainment',
        '4': 'Visa',
        '5': 'Master Card',
        '6': 'Discover Card',
    }

    type_map = {
        Issuer.electron: re.compile(r'^(4026|417500|4405|4508|4844|4913|4917)\d+$'),
        Issuer.maestro: re.compile(r'^(5018|5020|5038|5612|5893|6304|6759|6761|6762|6763|0604|6390)\d+$'),
        Issuer.dankort: re.compile(r'^(5019)\d+$'),
        Issuer.interpayment: re.compile(r'^(636)\d+$'),
        Issuer.unionpay: re.compile(r'^(62|88)\d+$'),
        Issuer.visa: re.compile(r'^4[0-9]{12}(?:[0-9]{3})?$'),
        Issuer.master_card: re.compile(r'^5[1-5][0-9]{14}$'),
        Issuer.amex: re.compile(r'^3[47][0-9]{13}$'),
        Issuer.diners: re.compile(r'^3(?:0[0-5]|[68][0-9])[0-9]{11}$'),
        Issuer.discover: re.compile(r'^6(?:011|5[0-9]{2})[0-9]{12}$'),
        Issuer.jcb: re.compile(r'^(?:2131|1800|35\d{3})\d{11}$'),
    }

    @classmethod
    def identify_system(cls, sequence: str) -> Optional[str]:
        return cls.system_map.get(sequence[0], None)

    @classmethod
    def identify_type(cls, sequence: str) -> Optional[int]:
        for card, pattern in cls.type_map.items():
            if pattern.fullmatch(sequence):
                return card

    @staticmethod
    def user_identifier(sequence: str):
        return sequence[6:-1], sequence[-1]
