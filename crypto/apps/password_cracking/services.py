import itertools
from dataclasses import dataclass
from datetime import timedelta, datetime
from string import ascii_lowercase, digits
from typing import Iterable, Optional, Callable


@dataclass
class CrackingResult:
    keyword: Optional[str]
    time_taken: timedelta
    processed_count: int

    @property
    def is_cracked(self) -> bool:
        return self.keyword is not None

    def __add__(self, other):
        if other is None:
            return self

        self.keyword = self.keyword or other.keyword
        self.time_taken += other.time_taken
        self.processed_count += other.processed_count

        return self

class PasswordCrackingService:
    Encrypt = Callable[[str], str]

    chars = ascii_lowercase + digits

    def generate_combinations(self, iterable: Iterable, length: int):
        for value in itertools.product(iterable, repeat=length):
            yield ''.join(value)

    def crack(self, unknown_hash: str, options: Iterable[str], hash_function: Encrypt) -> CrackingResult:
        start_time = datetime.now()
        count = 1
        for word in options:
            if unknown_hash == hash_function(word):
                return CrackingResult(keyword=word, time_taken=datetime.now() - start_time, processed_count=count)

            count += 1

        return CrackingResult(keyword=None, time_taken=datetime.now() - start_time, processed_count=count)

    def brute_force(self, unknown_hash: str, length: int, hash_function: Encrypt) -> CrackingResult:
        result = None
        for n in range(1, length + 1):
            new_result = self.crack(unknown_hash, self.generate_combinations(self.chars, n), hash_function)
            result = new_result + result

            if result.is_cracked:
                return result

        return result
