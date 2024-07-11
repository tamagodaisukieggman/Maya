# -*- coding: utf-8 -*-
from .gui import CheckUVPaddingGUI
from .command import CheckUVPaddingCmd

__all__ = (
    'CheckUVPaddingGUI',
    'CheckUVPadding',
)


def main():
    win = CheckUVPaddingGUI()
    win.show()
