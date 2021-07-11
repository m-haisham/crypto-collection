from typing import List, Union


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
