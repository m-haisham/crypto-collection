from collections import namedtuple
from datetime import date

Post = namedtuple('Post', 'title description published link icon')

blog_posts = [
    Post(
        title='Hamming Code',
        description='Hamming code is a set of error-correction codes that are used to detect and correct errors that '
                    'may occur during the transmission of the data from the sender to the receiver...',
        published=date(2021, 7, 10),
        link='hamming-code',
        icon='grip-horizontal',
    ),
    Post(
        title='Luhn Algorithm',
        description='Luhn algorithm or Luhn formula is a simple checksum formula used to validate a variety of '
                    'identification numbers such as, credit card numbers and IMEI numbers...',
        published=date(2021, 7, 12),
        link='luhn-algorithm',
        icon='credit-card',
    ),
    Post(
        title='Password Cracking',
        description='password cracking is the process of recovering passwords from data that has been stored in or '
                    'transmitted by a computer system in scrambled form. Some common approaches among them are '
                    'brute-force attack and dictionary attack.',
        published=date(2021, 7, 14),
        link='password-cracking',
        icon='lock',
    ),
    Post(
        title='Hiding Secrets in Strings',
        description='Steganography is described as the art of concealing a message in another. In this case, a string '
                    'is hidden within another string. In cryptography, the observer is able clearly see that a '
                    'message has been encrypted and this gives raise to scrutiny...',
        published=date(2021, 8, 21),
        link='hiding-in-strings',
        icon='user-secret',
    ),
]

posts_index = {(str(post.published), post.link): i for i, post in enumerate(blog_posts)}
