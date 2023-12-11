# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import re
import random

try:
    # maya 2022-
    from builtins import str
    from builtins import range
except Exception:
    pass


# ===============================================
def get_random_string(length, contain_number=False):
    """
    ランダムな文字列を取得

    :param length: 長さ
    :param contain_number: 数字を含むかどうか
    :param prefix: 接頭語
    :param suffix: 接尾語

    :return: ランダムな文字列
    """

    result_str = ''

    letter_list = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    if contain_number:
        letter_list += '0123456789'

    for _ in range(length):
        result_str += random.choice(letter_list)

    return result_str


# ===============================================
def get_string_by_regex(target_string, pattern):
    """
    正規表現で文字列取得

    :param target_string: 対象文字列
    :param pattern: 正規表現パターン

    :return: ヒットした文字列
    """

    match_obj = re.search(pattern, str(target_string))

    if not match_obj:
        return ''

    return match_obj.group()
