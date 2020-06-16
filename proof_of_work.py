"""
proof_of_work.py

Created on: 14-Jun-2020
    Author: rhythm
"""
from hashlib import sha1
from itertools import product
from ctypes import c_bool
from multiprocessing import Process, current_process, Value
from os import cpu_count
from time import time


class ProofOfWork(object):
    """
    class to solve Proof of Work with SHA1 hash
    """
    def __init__(self, base_string, difficulty, unwanted_chars=None):
        """
        :param base_string: base string to solve POW with
        :param difficulty:  difficulty level to solve for
        :param unwanted_chars: unwanted utf-8 characters, if any.
                                For eg: ('\n', '\r', '\t', ' ') ==> [0x0a, 0x0d, 0x09, 0x20]
        """
        if unwanted_chars is None:
            unwanted_chars = list()
        self.char_set = [x for x in range(0x00, 0x100) if x not in unwanted_chars]
        self.solved = Value(c_bool, False)
        self.start_time = time()
        self.total_cpus = cpu_count()

        """
        independent string_generators to be used in different processes
        Generator 1: Generate strings of length 0, 8, 16, ...
        Generator 2: Generate strings of length 1, 9, 17, ...
                        .
                        .
                        .
        """
        self.string_generators = list()
        for i in range(self.total_cpus):
            self.string_generators.append(self._get_string_from_char_set(i, self.total_cpus))

        self.process_list = list()
        for index in range(self.total_cpus):
            self.process_list.append(
                Process(target=self._worker, args=(base_string, self.string_generators[index], difficulty)))

    def _sha1_digest(self, string):
        return sha1(string).hexdigest()

    def _get_string_from_char_set(self, n, offset):
        """
        Yield strings in the char_set in increasing order of length
        """
        while True:
            for p in product(self.char_set, repeat=n):
                yield bytearray(p)
            n += offset

    def _worker(self, base_string, string_generator, difficulty):
        """
        Worker thread to solve pow in parallel threads
        Prints log when the digest with preceding zeros more than 5
        :param base_string: Base String to use for proof of work
        :param string_generator: Generator method to generate strings
        :param difficulty: difficulty level to solve the base_string for
        :return:
        """
        while not self.solved.value:
            s = next(string_generator)
            hex_digest = self._sha1_digest(base_string + s)
            # count = 0
            # while hex_digest[count] == '0':
            #     count += 1
            # if count > 5:
            #     print("%s: Length: %s, Zeros: %s, Time: %s mins, String: %s, Hash: %s..." %
            #           (current_process().name, len(s), count, (time() - self.start_time) / 60, s, hex_digest[:10]))
            if hex_digest.startswith('0' * difficulty):
                self.solved.value = True
                print("Solved with %s. Hash: %s" % (s, hex_digest[:10]))
                break

    def solve(self):
        """
        Spawn different processes to parallely solve pow
        """
        start_time = time()
        for p in self.process_list:
            p.start()

        for p in self.process_list:
            p.join()
        print("Joined in", (time() - start_time) / 60, "mins")
