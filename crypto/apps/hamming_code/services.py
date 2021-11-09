from typing import Tuple


class HammingService:
    def calculate_redundant_bits(self, bit_count):
        """Use the formula 2 ^ r >= bit_count + r + 1 to calculat the number of redundant bits"""
        for i in range(bit_count):
            if 2 ** i >= bit_count + i + 1:
                return i

    def generate_parity_positions(self, length):
        index = 0
        while True:
            current = 2 ** index
            index += 1
            if current > length:
                break

            yield current

    def bit_label(self, p):
        label = 'd'
        if p == 1 or p == 2:
            label = 'p'

        num = p
        while num > 2:
            num /= 2

        if float(num).is_integer():
            label = 'p'

        return f'{label}{p}'

    def encode(self, data, is_even=True):
        """
        Redundancy bits are placed at the positions, which correspond to the power of 2.
        """
        if type(data) == str:
            data = [int(bit) for bit in data]

        n = len(data)
        r = self.calculate_redundant_bits(n)

        j = 0
        k = 0
        arr = []

        for i in range(1, n + r + 1):
            if i == 2 ** j:
                arr.append(0)
                j += 1
            else:
                arr.append(data[k])
                k += 1

        length = len(arr)

        for p in self.generate_parity_positions(length):
            count = 0
            for j, bit in enumerate(arr):
                if j + 1 != p and j + 1 & p == p:
                    count += bit

            if is_even:
                arr[p - 1] = count % 2
            else:
                arr[p - 1] = 1 if count % 2 != 1 else 0

        return ''.join(str(bit) for bit in arr)

    def detect_error(self, data, is_even=True) -> Tuple[str, int]:
        if type(data) == str:
            data = [int(bit) for bit in data]

        length = len(data)
        binary = 0
        for i, p in enumerate(self.generate_parity_positions(length)):

            count = 0
            for j, bit in enumerate(data):
                if j + 1 & p == p:
                    count += bit

            if is_even:
                parity = count % 2
            else:
                parity = 1 if count % 2 != 1 else 0

            binary = binary + parity * (10**i)

        # Convert binary to decimal
        position = int(str(binary), 2)

        # correct error
        if position > 0:
            data[position - 1] = data[position - 1] ^ 1

        return ''.join([str(bit) for bit in data]), position

    def decode(self, data):
        d_index = -1
        result = ''

        length = len(data)

        for p in self.generate_parity_positions(length):
            p_index = p - 1

            while d_index < length:
                d_index += 1
                if d_index == p_index:
                    break

                result += data[d_index]

        return result + ''.join(data[d_index + 1:])

