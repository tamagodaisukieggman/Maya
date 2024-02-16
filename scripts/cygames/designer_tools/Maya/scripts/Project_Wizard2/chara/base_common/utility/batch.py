# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function


import sys


def batch_print(output_str):
    """Mayaのバッチ実行時に適切に文字列を出力できるように整形する

    Args:
        output_str (str): 出力文字列
    """

    if sys.version_info.major == 3:

        print(output_str)
        # Mayapyがうまく出力してくれないケースがあるため、強制出力
        sys.stdout.flush()

    else:
        encoded_str = output_str.encode('shift-jis')
        print(encoded_str)
