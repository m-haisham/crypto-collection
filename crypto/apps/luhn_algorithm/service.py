from typing import List, Union, Optional

from crypto.apps.luhn_algorithm.models import CreditCardType


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

    @classmethod
    def identify_system(cls, sequence: str) -> Optional[str]:
        return cls.system_map.get(sequence[0], None)

    @staticmethod
    def identify_type(sequence: str) -> Optional[int]:
        if sequence[:2] == '34' or sequence[:2] == '37':
            return CreditCardType.amex
        elif sequence[0] == '5':
            return CreditCardType.master_card
        elif sequence[0] == '4':
            return CreditCardType.visa
        elif sequence[:4] == '6011' \
                or (622126 <= int(sequence[:6]) <= 622925) \
                or (644 <= int(sequence[:3]) <= 649) \
                or sequence[:2] == '65':
            return CreditCardType.discover
