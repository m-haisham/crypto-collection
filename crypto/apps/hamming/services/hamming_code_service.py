class HammingCodeService:
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

    def encode(self, data):
        """
        Redundancy bits are placed at the positions, which correspond to the power of 2.
        """
        if type(data) == str:
            data = [int(bit) for bit in data]

        n = len(data)
        r = self.calculate_redundant_bits(n)

        j = 0
        k = 1
        arr = []

        for i in range(1, n + r + 1):
            if i == 2 ** j:
                arr.append(0)
                j += 1
            else:
                arr.append(data[-1 * k])
                k += 1

        length = len(arr)

        for p in self.generate_parity_positions(length):
            val = 0
            for j, bit in enumerate(arr):
                if j + 1 != p and j + 1 & p == p:
                    val ^= bit

            arr[p - 1] = val

        return ''.join(reversed([str(bit) for bit in arr]))

    def detect_error(self, data) -> int:
        if type(data) == str:
            data = [int(bit) for bit in data]

        length = len(data)
        parities = []
        for p in self.generate_parity_positions(length):

            val = 0
            for j, bit in enumerate(data):
                if j + 1 != p and j + 1 & p == p:
                    val ^= bit

            parities.insert(0, val)

        # Convert binary to decimal
        return int(''.join([str(bit) for bit in parities]), 2)
