# -*- coding: utf-8 -*-
u"""Resurf Tool(GUI)

..
    BEGIN__CYGAMES_MENU
    label=Resurf Tool... : リサーフ用ツール
    command=main()
    order=1300
    END__CYGAMES_MENU

"""

from mtku.maya.mtklog import MtkLog

from . import gui

logger = MtkLog(__name__)


def main():
    u"""main関数"""
    logger.usage()

    ui = gui.ResurfTool()
    ui.show()
