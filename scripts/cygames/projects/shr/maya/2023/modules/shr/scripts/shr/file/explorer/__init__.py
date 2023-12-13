# -*- coding: utf-8 -*-
u"""WorkFiler拡張"""

from maya import OpenMayaUI as omui
import maya.mel as mel
import maya.cmds as cmds

from .zmain import MtkExplorerForMaya

import logging
logger = logging.getLogger(__name__)


def _exec_job(*args):
    logger.debug('Maya Exit')
    mel.eval('$g_mtk_explorer_escape=true;')


def init_ui():
    win = MtkExplorerForMaya()
    win.show()
    cmds.scriptJob(e=['quitApplication', _exec_job])


def main():
    init_ui()
