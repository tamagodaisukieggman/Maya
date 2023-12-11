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


# ===============================================
def get_same_length_list(target_list, max_length, default_value):

    fix_list = []

    if not target_list:
        return fix_list

    for cnt in range(max_length):

        if cnt < len(target_list):
            fix_list.append(target_list[cnt])
            continue

        fix_list.append(default_value)

    return fix_list
