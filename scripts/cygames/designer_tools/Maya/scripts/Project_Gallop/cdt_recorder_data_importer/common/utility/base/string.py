# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import range
except Exception:
    pass

import random


# ===============================================
def get_random_string(length, contain_number=False, prefix=None, suffix=None):

    result_str = ''

    letter_list = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    if contain_number:
        letter_list += '0123456789'

    for p in range(length):
        result_str += random.choice(letter_list)

    if prefix:
        result_str = prefix + result_str

    if suffix:
        result_str = result_str + suffix

    return result_str
