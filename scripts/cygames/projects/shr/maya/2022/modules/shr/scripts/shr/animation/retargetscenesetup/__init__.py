# -*- coding: utf-8 -*-
u"""reterget scene setup ツール
"""

from shru.maya.mtklog import shrLog

from . import gui

logger = MtkLog(__name__)


def main():
    u"""main関数"""
    logger.usage()

    ui = gui.RetargetSceneSetupUI()
    ui.show()
