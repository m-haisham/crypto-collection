import hashlib

import pytest

from .services import hash_regex, generate_combinations, brute_force, crack


def test_generate_combinations():
    assert list(generate_combinations('ab', 2)) == [b'a', b'b', b'aa', b'ab', b'ba', b'bb']


def test_brute_force():
    # we arent using longer words because testing would take longer
    test_words = [b'sef', b'ant', b'ng8']

    def encrypt(value: bytes) -> str:
        return hashlib.sha1(value).hexdigest()

    for word in test_words:
        assert brute_force(encrypt(word), len(word), encrypt).keyword == word.decode('utf-8')


def test_dictionary():
    dictionary = [b'1', b'2', b'three', b'4', b'8', b'10', b'twenty']

    def encrypt(value: bytes) -> str:
        return hashlib.sha1(value).hexdigest()

    test_words = [b'4', b'three']
    for word in test_words:
        assert crack(encrypt(word), dictionary, encrypt).keyword == word.decode()

    test_words = [b'5', b'six']
    for word in test_words:
        assert crack(encrypt(word), dictionary, encrypt).keyword is None


@pytest.mark.parametrize('hash, expected', [
    ('cb1877c2d5858b66e37269271ad5d8ee758', True),
    ('b13b6734b25c52e9a77254a8ed9b37', True),
    ('c9256818c5f32245d312ayubv787df702fa', False),
    ('a1d6737363e3959e37960a0164b5218b', True),
    ('f3c00e95e4f5260199abfaa134e675b2', True),
    ('c5a3eb885df40876c4441dae6f3f34cd7', True),
    ('fd662ba4d50f9d121209ab185ecade8417', True),
    ('a443711ec4f61c3f2d0211d496a2tos1994', False),
    ('b6f2361018c13ac568794f4abe429', True),
    ('b266a99402546149d337a69788449777', True),
    ('something else', False),
])
def test_hash_regex(hash, expected):
    assert bool(hash_regex.fullmatch(hash)) == expected


@pytest.mark.skip()
def test_bruteforce_time():
    test_words = [b'i', b'to', b'six', b'mist', b'sight', b'brexit']

    def encrypt(value: bytes) -> str:
        return hashlib.sha1(value).hexdigest()

    print()
    for word in test_words[:4]:
        result = brute_force(encrypt(word), 6, encrypt)
        print(f'{result.keyword}:{len(result.keyword)},{result.time_taken.microseconds},{result.processed_count}')
