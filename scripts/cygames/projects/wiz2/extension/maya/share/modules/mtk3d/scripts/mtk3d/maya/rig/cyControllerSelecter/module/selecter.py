# -*- coding: utf-8 -*-
import maya.cmds as mc
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
from functools import partial

import imp
try:
    imp.find_module('PySide2')
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtWidgets import *
    from PySide2.QtUiTools import *
    from shiboken2 import wrapInstance
    

except ImportError:
    from PySide.QtGui import *
    from PySide.QtCore import *
    from PySide.QtUiTools import*
    import PySide.QtGui as QtWidgets
    from shiboken import wrapInstance



# get name space ---------------------------------------------------------------------------------------------------------------------------------


def getNss(ui, *args):
    # textScrollListをクリアする
    ui.nmspList.clear()

    # referenceTypeをリストアップする
    rn = mc.ls(type='reference')
    # referenceオブジェクトをforで回し":"でスプリットする。
    for i in rn:
        list = i.split(":")
        count = len(list)
        if count == 1:
            for i in list:
                NSP = i.split("RN")
                ui.nmspList.addItem(NSP[0])
    else:
        pass
