# Copyright lowRISC contributors.
# Licensed under the Apache License, Version 2.0, see LICENSE for details.
# SPDX-License-Identifier: Apache-2.0

from Crypto.Cipher import AES
from Crypto.Hash import KMAC128, SHA3_256
import random

"""Data generator.

Generates crypto material for the SCA tests.

Input and output data format of the crypto material (ciphertext, plaintext,
and key) is plain integer arrays.
"""


class data_generator():

    key_generation = [0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF1, 0x23,
                      0x45, 0x67, 0x89, 0xAB, 0xCD, 0xE0, 0xF0]

    text_fixed = [0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA,
                  0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA]
    text_random = [0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC,
                   0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC]
    key_fixed = [0x81, 0x1E, 0x37, 0x31, 0xB0, 0x12, 0x0A, 0x78, 0x42, 0x78,
                 0x1E, 0x22, 0xB2, 0x5C, 0xDD, 0xF9]
    key_random = [0x53, 0x53, 0x53, 0x53, 0x53, 0x53, 0x53, 0x53, 0x53, 0x53,
                  0x53, 0x53, 0x53, 0x53, 0x53, 0x53]

    cipher_gen = AES.new(bytes(key_generation), AES.MODE_ECB)

    def __init__(self):
        self.cipher_gen = AES.new(bytes(self.key_generation), AES.MODE_ECB)

    def set_start(self, capture_type = 'FVSR_KEY'):
        if capture_type == 'FVSR_KEY':
            self.text_fixed = [0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA,
                               0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA]
            self.text_random = [0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC,
                                0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0xCC]
            self.key_fixed = [0x81, 0x1E, 0x37, 0x31, 0xB0, 0x12, 0x0A, 0x78, 0x42,
                              0x78, 0x1E, 0x22, 0xB2, 0x5C, 0xDD, 0xF9]
            self.key_random = [0x53, 0x53, 0x53, 0x53, 0x53, 0x53, 0x53, 0x53,
                               0x53, 0x53, 0x53, 0x53, 0x53, 0x53, 0x53, 0x53]
        else:
            self.text_fixed = [0xDA, 0x39, 0xA3, 0xEE, 0x5E, 0x6B, 0x4B, 0x0D,
                               0x32, 0x55, 0xBF, 0xEF, 0x95, 0x60, 0x18, 0x90]
            self.text_random = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
            self.key_fixed = [0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF,
                              0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0]
            self.key_random = [0x01, 0x23, 0x45, 0x67, 0x89, 0xAB, 0xCD, 0xEF,
                               0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0]

    def advance_fixed(self):
        text_fixed_bytes = self.cipher_gen.encrypt(bytes(self.text_fixed))
        # Convert bytearray into int array.
        self.text_fixed = [x for x in text_fixed_bytes]

    def advance_random(self):
        text_random_bytes = self.cipher_gen.encrypt(bytes(self.text_random))
        # Convert bytearray into int array.
        self.text_random = [x for x in text_random_bytes]
        key_random_bytes = self.cipher_gen.encrypt(bytes(self.key_random))
        # Convert bytearray into int array.
        self.key_random = [x for x in key_random_bytes]

    def advance_random_data(self):
        text_random_bytes = self.cipher_gen.encrypt(bytes(self.text_random))
        # Convert bytearray into int array.
        self.text_random = [x for x in text_random_bytes]

    def get_fixed(self, capture_type = 'FVSR_KEY'):
        pt = self.text_fixed
        key = self.key_fixed
        cipher_fixed = AES.new(bytes(self.key_fixed), AES.MODE_ECB)
        ct_bytes = cipher_fixed.encrypt(bytes(self.text_fixed))
        ct = [x for x in ct_bytes]
        del (cipher_fixed)
        if capture_type == 'FVSR_KEY':
            self.advance_fixed()
        return pt, ct, key

    def get_random(self, capture_type = 'FVSR_KEY'):
        pt = self.text_random
        key = self.key_random
        cipher_random = AES.new(bytes(self.key_random), AES.MODE_ECB)
        ct_bytes = cipher_random.encrypt(bytes(self.text_random))
        ct = [x for x in ct_bytes]
        del (cipher_random)
        if capture_type == 'FVSR_KEY':
            self.advance_random()
        else:
            self.advance_random_data()
        return pt, ct, key

    def get_kmac_fixed(self):
        pt = self.text_fixed
        key = self.key_fixed
        mac_fixed = KMAC128.new(key=bytes(self.key_fixed), mac_len=32)
        mac_fixed.update(bytes(self.text_fixed))
        ct_bytes = mac_fixed.digest()
        ct = [x for x in ct_bytes]
        del (mac_fixed)
        self.advance_fixed()
        return pt, ct, key

    def get_kmac_random(self):
        pt = self.text_random
        key = self.key_random
        mac_random = KMAC128.new(key=bytes(self.key_random), mac_len=32)
        mac_random.update(bytes(self.text_random))
        ct_bytes = mac_random.digest()
        ct = [x for x in ct_bytes]

        del (mac_random)
        self.advance_random()
        return pt, ct, key

    def get_sha3_fixed(self):
        pt = self.text_fixed
        key = self.key_fixed
        sha3_fixed = SHA3_256.new(bytes(self.text_fixed))
        ct_bytes = sha3_fixed.digest()
        ct = [x for x in ct_bytes]

        del (sha3_fixed)
        return pt, ct, key

    def get_sha3_random(self):
        pt = self.text_random
        key = self.key_random
        sha3_random = SHA3_256.new(bytes(self.text_random))
        ct_bytes = sha3_random.digest()
        ct = [x for x in ct_bytes]

        del (sha3_random)
        self.advance_random()
        return pt, ct, key

    def get_ibex_random(self):
        """
        For a full random test
        data_batch_1 = [A, B, C, D, E, F, G, H]
        :return:
        """
        data = []
        for i in range(0, 8):
            data.append(random.randint(0, pow(2, 31)))  # 31 bit random value!
        return data

    def get_ibex_fvsr_vector(self, fixed_value:  int):
        """
        For a fix vs random ttest
        data_batch_1 = [A, B1, A, B2, A, B3, A, B4]_1
        data_batch_2 = [A, B5, A, B6, A, B....]_2
        The vector stays constant within a batch.
        :return:
        """
        assert isinstance(fixed_value, int)  # prevent from appending lists

        data = []
        for i in range(0, 8):
            if i % 2 == 0:
                data.append(fixed_value)
            else:
                data.append(random.randint(0, 0xFFFFFFFF))
        return data

# ----------------------------------------------------------------------
# Create one instance, and export its methods as module-level functions.
# The functions share state across all uses.


_inst = data_generator()
set_start = _inst.set_start
get_fixed = _inst.get_fixed
get_random = _inst.get_random
get_kmac_fixed = _inst.get_kmac_fixed
get_kmac_random = _inst.get_kmac_random
get_sha3_fixed = _inst.get_sha3_fixed
get_sha3_random = _inst.get_sha3_random
get_ibex_fixed_vs_rand = _inst.get_ibex_fvsr_vector
get_ibex_random = _inst.get_ibex_random
