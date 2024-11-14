# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

import base64
import codecs
from collections import OrderedDict
import fnmatch
from functools import partial
import glob
from imp import reload
import json
import math
import os
import pickle
import re
import shutil
import subprocess
import sys
import time
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR
from timeit import default_timer as timer
import traceback

from maya import cmds
from maya import mel
from maya import OpenMayaUI as omui
import maya.api.OpenMaya as om2
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin, MayaQWidgetDockableMixin

ver = cmds.about(v=True)

if int(ver) >= 2025:
    from PySide6.QtCore import *
    from PySide6.QtGui import *
    from PySide6.QtWidgets import *
    from PySide6 import __version__
    from shiboken6 import wrapInstance
else:
    try:
        from PySide2.QtCore import *
        from PySide2.QtGui import *
        from PySide2.QtWidgets import *
        from PySide2 import __version__
        from shiboken2 import wrapInstance
    except Exception as e:
        from PySide.QtCore import *
        from PySide.QtGui import *
        from PySide import __version__
        from shiboken import wrapInstance

COPY_HAIR_SKINWEIGHTS = 'Copy Hair Skinweights'

class UI(MayaQWidgetDockableMixin, QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ウィンドウタイトルの設定
        self.setWindowTitle(self.__class__.__name__)

        # ウィジェットの設定
        self.widgets()

    def widgets(self):
        self.topWidget = QWidget()
        self.setCentralWidget(self.topWidget)

        # set layout
        self.topVboxLayout = QVBoxLayout()
        self.topWidget.setLayout(self.topVboxLayout)

        # Copy Hair Skinweight
        self.copyHairSkinVLay = QVBoxLayout()
        self.topVboxLayout.addLayout(self.copyHairSkinVLay)
        self.copyHairSkinHLayBase = QHBoxLayout()

        self.copyHairSkinVLay.addLayout(self.copyHairSkinHLayBase)
        self.copyHairSkinLabelBase = QLabel(COPY_HAIR_SKINWEIGHTS)
        self.copyHairSkinHLayBase.addWidget(self.copyHairSkinLabelBase)

        self.copyHairSkinLabelBaseSetBtn = QPushButton('Set')
        self.copyHairSkinHLayBase.addWidget(self.copyHairSkinLabelBaseSetBtn)

        self.copyHairSkinHLayHair = QHBoxLayout()
        self.copyHairSkinVLay.addLayout(self.copyHairSkinHLayHair)


        # self.main_col = cmds.columnLayout(adj=True, p=self.window)

        # # Copy Hair Skinweight
        # self.copy_hair_skin_col = cmds.columnLayout(adj=True, p=self.main_col)
        # self.copy_hair_skin_label = cmds.text(l=COPY_HAIR_SKINWEIGHTS, al='left', p=self.copy_hair_skin_col)
        # self.copy_hair_skin_row_col = cmds.rowColumnLayout(nr=4, p=self.copy_hair_skin_col)
        # self.copy_hair_skin_base_obj_tfbgrp = cmds.textFieldButtonGrp(l='Label', text='Text', bl='Button', cw=[1, 50], adj=2, p=self.copy_hair_skin_col)
        # self.copy_hair_skin_apply_btn = cmds.button(l='Apply', p=self.copy_hair_skin_col)

if __name__ == '__main__':
    ui = SkinweightUI()
    ui.show(dockable=True)


def save_optionvar(key, value, force=True):
    """optionVarに保存

    :param str key: キー名
    :param mixin value: 値
    :param bool force: 強制的に上書きするかのブール値

    :return: 保存できたかどうかのブール値
    :rtype: bool
    """

    vStr = str(value)
    if force:
        cmds.optionVar(sv=[key, vStr])
        return True
    else:
        if not cmds.optionVar(ex=key):
            cmds.optionVar(sv=[key, vStr])
            return True
        else:
            return False


def load_optionvar(key):
    """optionVarを取得

    :param str key: キー名
    :return: 保存された値, キーが見つからない場合は None
    :rtype: value or None
    """

    if cmds.optionVar(ex=key):
        return eval(cmds.optionVar(q=key))
    else:
        return None


def remove_optionvar(key):
    """optionVarを削除

    :param str key: キー名
    :return: 削除成功したかのブール値
    :rtype: bool
    """

    if cmds.optionVar(ex=key):
        cmds.optionVar(rm=key)
        return True
    else:
        return False