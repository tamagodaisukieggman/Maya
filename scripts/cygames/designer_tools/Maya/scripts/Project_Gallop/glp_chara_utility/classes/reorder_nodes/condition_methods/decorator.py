# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function


def deco_safe_bool_method(func):
    """bool判定のコンディションメソッドのエラーをtry/catchするデコレーター
    エラーがある場合はprint
    """
    def inner(long_name):
        try:
            result = func(long_name)
            return result
        except Exception as e:
            print('REORDER ERROR: "{}" in "{}" DETAIL: {}'.format(long_name, func.__name__, e))
            return False
    return inner


def deco_safe_str_method(func):
    """strを返すコンディションメソッドのエラーをtry/catchするデコレーター
    エラーがある場合はprint
    """
    def inner(long_name):
        try:
            result = func(long_name)
            return result
        except Exception as e:
            print('REORDER ERROR: "{}" in "{}" DETAIL: {}'.format(long_name, func.__name__, e))
            return ''
    return inner


def deco_safe_int_method(func):
    """intを返すコンディションメソッドのエラーをtry/catchするデコレーター
    エラーがある場合はprint
    """
    def inner(long_name):
        try:
            result = func(long_name)
            return result
        except Exception as e:
            print('REORDER ERROR: "{}" in "{}" DETAIL: {}'.format(long_name, func.__name__, e))
            return -1
    return inner

