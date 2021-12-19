import hashlib
import itertools
import re
from dataclasses import dataclass
from datetime import timedelta, datetime
from pathlib import Path
from string import ascii_lowercase, digits
from typing import Iterable, Optional, Callable

hash_regex = re.compile(r'^[0-9a-fA-F]+$')
encrypt = Callable[[bytes], str]
charset = ascii_lowercase + digits
encryption_types = ['sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'md5', ]


@dataclass
class Result:
    keyword: Optional[str]
    time_taken: timedelta
    processed_count: int

    @property
    def is_cracked(self) -> bool:
        return self.keyword is not None


def get_encryption_function(enc_type: str) -> encrypt:
    def enc_function(value):
        return getattr(hashlib, enc_type)(value).hexdigest()

    return enc_function


def generate_combinations(iterable: Iterable, length: int):
    for v in range(1, length + 1):
        for value in itertools.product(iterable, repeat=v):
            yield ''.join(value).encode('utf-8')


def crack(unknown_hash: str, options: Iterable[bytes], hash_function: encrypt) -> Result:
    start_time = datetime.now()
    count = 1
    for word in options:
        if unknown_hash == hash_function(word):
            return Result(keyword=word.decode('utf-8'), time_taken=datetime.now() - start_time,
                          processed_count=count)

        count += 1

    return Result(keyword=None, time_taken=datetime.now() - start_time, processed_count=count)


def brute_force(unknown_hash: str, length: int, hash_function: encrypt) -> Result:
    return crack(unknown_hash, generate_combinations(charset, length), hash_function)


def dictionary_file(unknown_hash: str, file: Path, hash_function: encrypt) -> Result:
    def words():
        """return words of the file as a generator"""
        with file.open('rb') as f:
            lines = f.read().split(b'\n')

        for line in lines:
            yield line

    return crack(unknown_hash, words(), hash_function)
