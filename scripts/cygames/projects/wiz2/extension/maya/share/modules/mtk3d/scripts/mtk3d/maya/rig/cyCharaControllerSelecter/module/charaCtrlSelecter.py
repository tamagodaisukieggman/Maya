# -*- coding: utf-8 -*-
#=========================================================================== # noqa
# Cygames Tools # noqa
# charaCtrlSelecter.py # noqa
# # noqa
# Copyright 2017, Cygames Inc. # noqa
#=========================================================================== # noqa
import maya.cmds as mc
from PySide import QtGui


def callback(ui, *args):
    mc.select(clear=True)
    # GUI上のQPushButtonを検索
    buttons = ui.findChildren(QtGui.QPushButton)
    # リストから選択されているネームスペースを取得
    Nmsp = ui.nmspList.currentItem().text()
    Nmsp = Nmsp + ':'
    ctrlList = []
    for i in buttons:
        # QPushButtonがチェックされていたらctrlListへ追加する
        if i.isChecked():
            ctrlList.append(i)
        else:
            pass

    # ctrlListに追加されたQPushButtonのobjectNameからコントローラーを判定
    for node in ctrlList:
        buttons = node.objectName()
        mc.select(Nmsp + buttons, add=True)

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


def highLow(ui, *args):
    # textScrollListをクリアする
    # normalization
    Nmsp = ui.nmspList.currentItem().text()
    Nmsp = Nmsp + ':'
    vals = ui.highLowButton.currentIndex()
    if vals == 0:
        mc.setAttr(Nmsp + "displaySet.meshTypeLOD", 0)
    elif vals == 1:
        mc.setAttr(Nmsp + "displaySet.meshTypeLOD", 1)
    else:
        pass
