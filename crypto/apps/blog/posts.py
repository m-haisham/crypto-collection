from collections import namedtuple
from datetime import date

Post = namedtuple('Post', 'title description published link')

blog_posts = [
    Post(
        title='Hamming Code',
        description='Hamming code is a set of error-correction codes that are used to detect and correct errors that '
                    'may occur during the transmission of the data from the sender to the receiver...',
        published=date(2021, 7, 10),
        link='hamming-code',
    ),
    Post(
        title='Luhn Algorithm',
        description='Luhn algorithm or Luhn formula is a simple checksum formula used to validate a variety of '
                    'identification numbers such as, credit card numbers and IMEI numbers...',
        published=date(2021, 7, 12),
        link='luhn-algorithm',
    ),
    Post(
        title='Brute-Force Attack',
        description='A brute-force attack uses trial-and-error to guess the passwords or passphrases. It is the '
                    'digital equivalent of trying every key in your key ring, and eventually finding the right one...',
        published=date(2021, 7, 14),
        link='brute-force-attack',
    ),
    Post(
        title='Dictionary Attack',
        description='A dictionary attack is a brute-force technique where the algorithm runs through a list of '
                    'predefined words and phrases, such as those from a dictionary or previous data breaches...',
        published=date(2021, 7, 17),
        link='dictionary-attack',
    ),
    Post(
        title='Hiding Secrets in Strings',
        description='Steganography is described as the art of concealing a message in another. In this case, a string '
                    'is hidden within another string. In cryptography, the observer is able clearly see that a '
                    'message has been encrypted and this gives raise to scrutiny...',
        published=date(2021, 8, 21),
        link='hiding-in-strings',
    ),
]

posts_index = {(str(post.published), post.link): i for i, post in enumerate(blog_posts)}
