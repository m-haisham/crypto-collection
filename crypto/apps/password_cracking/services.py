import itertools
from string import ascii_lowercase, digits
from typing import Iterable, Optional, Callable


class PasswordCrackingService:
    Encrypt = Callable[[str], str]

    chars = ascii_lowercase + digits

    def generate_combinations(self, iterable: Iterable, length: int):
        for value in itertools.product(iterable, repeat=length):
            yield ''.join(value)

    def crack(self, unknown_hash: str, options: Iterable[str], hash_function: Encrypt) -> Optional[str]:
        for word in options:
            if unknown_hash == hash_function(word):
                return word

    def brute_force(self, unknown_hash: str, length: int, hash_function: Encrypt) -> Optional[str]:
        for n in range(1, length + 1):
            result = self.crack(unknown_hash, self.generate_combinations(self.chars, n), hash_function)
            if result is not None:
                return result
