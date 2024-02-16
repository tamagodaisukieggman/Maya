# -*- coding: utf-8 -*-

try:
    # Maya 2022-
    from importlib import reload
except Exception:
    pass

from . import command
reload(command)


def main():
    u'''main関数'''
    command.main()
    pass
