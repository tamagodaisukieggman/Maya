# -*- coding: utf-8 -*-
u"""reterget scene setup ツール
"""

from mtku.maya.mtklog import MtkLog

from . import gui

logger = MtkLog(__name__)


def main():
    u"""main関数"""
    logger.usage()

    ui = gui.RetargetSceneSetupUI()
    ui.show()
