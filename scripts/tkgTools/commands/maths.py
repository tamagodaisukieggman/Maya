# -*- coding: utf-8 -*-
import math

def truncate(f, n):
    return math.floor(f * 10 ** n) / 10 ** n

def round_value(value=None, digit=None):
    return truncate(round(value, digit), digit)
