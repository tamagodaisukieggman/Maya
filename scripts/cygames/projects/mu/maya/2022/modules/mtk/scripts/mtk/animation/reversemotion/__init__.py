# -*- coding: utf-8 -*-
u"""モーション反転ツール

..
    BEGIN__CYGAMES_MENU
    label=モーション反転ツール ...
    command=main()
    order=1000
    END__CYGAMES_MENU

    END__CYGAMES_DESCRIPTION

:詳細: file:///Z:/mtku/tools/maya/doc/manual/sources/window/workfilerplus.rst
"""
import logging
# from mtku.maya.mtklog import MtkLog

from .gui import ReverseMotion
from .command import ReverseMotionCmd


__all__ = ('ReverseMotion', 'ReverseMotionCmd')

logger = logging.getLogger(__name__)


def main():
    u"""main"""
    # logger.usage()

    win = ReverseMotion()
    win.show()
