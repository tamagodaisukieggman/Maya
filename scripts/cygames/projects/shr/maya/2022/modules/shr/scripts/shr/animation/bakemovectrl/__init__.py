# -*- coding: utf-8 -*-
u"""Anim Store

..
    BEGIN__CYGAMES_MENU
    label=Bake Move Ctrl ...
    command=main()
    order=2000
    END__CYGAMES_MENU

    END__CYGAMES_DESCRIPTION

"""

import logging
# from shru.maya.mtklog import shrLog

from . import gui

# logger = MtkLog(__name__)
logger = logging.getLogger(__name__)


def main():
    u"""main関数"""
    # logger.usage()

    ui = gui.BakeMoveCtrl()
    ui.show()
