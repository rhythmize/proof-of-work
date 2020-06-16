"""
proof_of_work.py

Created on: 14-Jun-2020
    Author: rhythm
"""
from hashlib import sha1
from itertools import product
from multiprocessing import Process, current_process
from os import cpu_count
from time import time

unwanted_chars = [0x0a, 0x0d, 0x09, 0x20]  # hex values for ['\n', '\r', '\t', ' ']
char_set = [x for x in range(0x00, 0x100) if x not in unwanted_chars]


def sha1_digest(string):
    return sha1(string).hexdigest()


def get_string_from_char_set(n, offset):
    """
    Yield strings in the char_set in increasing order of length
    """
    while True:
        for p in product(char_set, repeat=n):
            yield bytearray(p)
        n += offset


start_time = time()
total_cpus = cpu_count()

"""
independent string_generators to be used in different processes
Generator 1: Generate strings of length 0, 8, 16, ...
Generator 2: Generate strings of length 1, 9, 17, ...
                .
                .
                .
Generator 8: Generate strings of length 7, 15, 23, ...
"""
string_generators = list()
for i in range(total_cpus):
    string_generators.append(get_string_from_char_set(i, total_cpus))


def _solve_parallel(base_string, string_generator):
    """
    Worker thread to solve pow in parallel threads
    Prints log when the digest with preceding zeros more than 5
    :param base_string: Base String to use for proof of work
    :param string_generator: Generator method to generate strings
    :return:
    """
    while True:
        s = next(string_generator)
        hex_digest = sha1_digest(base_string + s)
        count = 0
        while hex_digest[count] == '0':
            count += 1
        if count > 5:
            print("%s: Length: %s, Zeros: %s, Time: %s mins, String: %s, Hash: %s..." %
                  (current_process().name, len(s), count, (time() - start_time) / 60, s, hex_digest[:10]))


def solve(base_string):
    """
    Spawn different processes to parallely solve pow
    :param base_string: Base String to use for proof of work
    :return:
    """
    process_list = list()
    for index in range(total_cpus):
        process_list.append(Process(target=_solve_parallel, args=(base_string, string_generators[index])))

    for p in process_list:
        p.start()
