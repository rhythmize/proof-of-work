"""
proof_of_work.py

Created on: 14-Jun-2020
    Author: rhythm
"""

from hashlib import sha1
from time import time

unwanted_chars = [0x0a, 0x0d, 0x09, 0x20]  # hex values for ['\n', '\r', '\t', ' ']
char_set = [x for x in range(0x00, 0x100) if x not in unwanted_chars]


def sha1_digest(string):
    return sha1(string).hexdigest()


def get_string_from_char_set():
    """
    Yields all strings in the char_set, sorted by length.
    """
    m = len(char_set)
    n = 0
    while True:
        for i in range(m ** n):
            s = bytearray()
            for j in range(n):
                s.append(char_set[(i // (m ** j)) % m])
            yield s
        n += 1


start_time = time()
total = 1

func = get_string_from_char_set()


def solve(base_string):
    """
    Prints log when the digest with preceding zeros more than 5
    :param base_string: Base String to use for proof of work
    :return:
    """
    s = next(func)
    hex_digest = sha1_digest(base_string + s)
    count = 0
    while hex_digest[count] == '0':
        count += 1
    if count > 5:
        print("Length: %s, Zeros: %s, Time: %s mins, String: %s, Hash: %s..." %
              (len(s), count, (time() - start_time) / 60, s, hex_digest[:10]))
