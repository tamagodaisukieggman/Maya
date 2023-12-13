# -*- coding: utf-8 -*-
# ----------------------------------
# Project : Tsubasa
# Name    : dccUserMayaSharePythonLib.ui
# Author  : toi
# ----------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import os
import sys
import time
#import json
#import stat
#from functools import partial
#from collections import OrderedDict

try:
    from pyfbsdk import *
    fbapp = FBApplication()
    fbsys = FBSystem()
    is_motionbuilder = True
except ImportError:
    is_motionbuilder = False

if not is_motionbuilder:
    import maya.cmds as cmds
    import maya.mel as mm
    import pymel.core as pm
    import maya.OpenMaya as om
    import maya.OpenMayaUI as OpenMayaUI
    from dccUserMayaSharePythonLib import pyCommon
else:
    from dccUserMotionbuilderSharePythonLib import common as mbcm
    mbcm.appendMayaPath('dccUserMayaSharePythonLib')
    import pyCommon

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2 import __version__
    if not is_motionbuilder:
        from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide import __version__

if sys.hexversion < 0x3000000:
    BYTES = str
    UNICODE = unicode
    BASESTR = basestring
    LONG = long
    py3 = False
else:
    BYTES = bytes
    UNICODE = str
    BASESTR = str
    LONG = int
    py3 = True


# -----------------------------------------------------------------------------------------
# pyside
# -----------------------------------------------------------------------------------------
class MayaUI(QWidget):
    u"""
    pysideUi内でmayaのUiを使用する為のクラス
    インスタンスクラス作成時、引数（script）に、main関数に適用したいmayaUiのスクリプトを文字列で渡す
    クラス変数（self.widget）がpysideのwidgetに相当する
    """

    def __init__(self, script=None, *args, **kwargs):
        super(MayaUI, self).__init__(*args, **kwargs)
        cmds.setParent('MayaWindow')
        script_ = script
        exec(script_)
        ptr = OpenMayaUI.MQtUtil.findControl(widget)
        self.widget = wrapInstance(int(ptr), QWidget)


def mayaToPySide(name, toType):
    ptr = OpenMayaUI.MQtUtil.findControl(name)
    if not ptr:
        ptr = OpenMayaUI.MQtUtil.findLayout(name)

    if not ptr:
        ptr = OpenMayaUI.MQtUtil.findMenuItem(name)

    if not ptr:
        return None

    return wrapInstance(int(ptr), toType)


def qWindow(uiName):
    return mayaToPySide(uiName, QMainWindow)


def qButton(uiName):
    return mayaToPySide(uiName, QPushButton)


def qCheckBox(uiName):
    return mayaToPySide(uiName, QCheckBox)


def qVBoxLayout(uiName):
    return mayaToPySide(uiName, QVBoxLayout)


def qLineEdit(uiName):
    return mayaToPySide(uiName, QLineEdit)


def col_text_button(*args, **kargs):
    col_k = [x for x in kargs if 'col' in x][0]
    col_v = kargs[col_k]
    kargs.pop(col_k)
    bt = pm.button(*args, **kargs)
    bt = qButton(bt)
    bt.setStyleSheet(u'color: {0};'.format(col_v))
    return bt


def qtbutton(*args, **kargs):
    col_k = [x for x in kargs if x == 'col']
    if col_k:
        col_v = kargs[col_k[0]]
        kargs.pop(col_k[0])

    size_k = [x for x in kargs if x == 'size']
    if size_k:
        size_v = kargs[size_k[0]]
        kargs.pop(size_k[0])

    icon_k = [x for x in kargs if x == 'icon' or x == 'i']
    if icon_k:
        icon_v = kargs[icon_k[0]]
        kargs.pop(icon_k[0])

    icon_size_k = [x for x in kargs if x == 'icon_size' in x or x == 'i_size']
    if icon_size_k:
        icon_size_v = kargs[icon_size_k[0]]
        kargs.pop(icon_size_k[0])

    align_k = [x for x in kargs if x == 'align']
    if align_k:
        align_v = kargs[align_k[0]]
        kargs.pop(align_k[0])

    bt = pm.button(*args, **kargs)
    bt = qButton(bt)

    #bt.setStyleSheet(u'text-align:left;')
    ss = ''
    if col_k:
        ss = u'color: {0};'.format(col_v)
    if size_k:
        ss += u'font-size: {0}px;'.format(str(size_v))
    if align_k:
        ss += u'text-align: {0};'.format(align_v)
    if ss:
        ss = 'QPushButton{' + ss + '}'
        bt.setStyleSheet(ss)

    if icon_k:
        bt.setIcon(QIcon(':/{0}'.format(icon_v)))
    if icon_size_k:
        bt.setIconSize(QSize(icon_size_v, icon_size_v))

    return bt


def separator():
    sep = QFrame()
    sep.setFrameShape(QFrame.HLine)
    sep.setFrameShadow(QFrame.Sunken)
    return sep


def getMainWindowAsQMainWindow():
    """MayaWindowの取得"""

    if is_motionbuilder:
        search_text = os.path.basename(os.path.dirname(os.path.dirname(fbsys.ApplicationPath)))
        main_widget = None
        for widget in QApplication.topLevelWidgets():
            if search_text in widget.windowTitle():
                main_widget = widget
                break
        return main_widget
    else:
        ptr = OpenMayaUI.MQtUtil.mainWindow()
        hMainWindow = wrapInstance(int(ptr), QMainWindow)
        return hMainWindow


def getPySideWindow(win_title):
    """win_titleがタイトルのPySideで作成されたwindowを取得する"""

    wins = getMainWindowAsQMainWindow().findChildren(QMainWindow)
    tgt_win = None
    for w in wins:
        if w.windowTitle() == win_title:
            tgt_win = w
    return tgt_win


def getMousePosition():
    """ マウスの現在の座標を取得　"""
    pos = QApplication.desktop().cursor().pos()
    return pos.x(), pos.y()


class QWindow(QMainWindow):
    """
    QMainWindow継承クラス, maya上に表示、２重起動無し, 基本レイアウト込み, スクリプトジョブ削除機能
    """
    parent = getMainWindowAsQMainWindow()

    def __init__(self, wTitle='qtWindow'):
        #同名タイトルのwindowがあったら消す（super前に実行）
        self.nowQWindowList = self.parent.findChildren(QMainWindow)
        for qW in self.nowQWindowList:
            if qW.windowTitle() == wTitle:
                qW.close()

        if py3:
            super().__init__(self.parent)
        else:
            super(QWindow, self).__init__(self.parent)

        self.setWindowTitle(wTitle)

        #close()後に消してくれるフラグ
        self.setAttribute(Qt.WA_DeleteOnClose)

        # 基本レイアウトを用意
        self.cWindow = QWidget()
        self.setCentralWidget(self.cWindow)
        self.layout = QVBoxLayout()
        self.cWindow.setLayout(self.layout)

        # windowをマウス位置にセット
        pos_ = QCursor().pos()
        self.setGeometry(pos_.x(), pos_.y(), 0, 0)

        # クラス変数-------------------------------------------------------------
        # 閉じた時に消すスクリプトジョブのナンバーリスト（ジョブ作成時に返ってくる番号を入れる）
        self.job_number_list = []

    def closeEvent(self, event):
        u""" ウィンドウが閉じられた時のイベント （self.job_number_listのスクリプトジョブを停止）"""
        if self.job_number_list:
            for job_number in self.job_number_list:
                print('kill scriptJob({0})'.format(str(job_number)))
                pm.scriptJob(kill=job_number)


class ButtonGroup(QButtonGroup):
    def setCheck(self, id_):
        for i, bt in enumerate(self.buttons()):
            if i == id_:
                bt.setChecked(True)
            else:
                bt.setChecked(False)


# -----------------------------------------------------------------------------------------
# その他
# -----------------------------------------------------------------------------------------
def getModelPanels():
    return cmds.getPanel(type='modelPanel')


def getMenbersContainedWindow(window_name, type=None):
    """ウィンドウ（window_name）内に含まれる全ての要素を取得する"""

    if type is None:
        return [x for x in pm.lsUI(long=True) if x.startswith(window_name)]
    else:
        return [x for x in pm.lsUI(long=True, typ=type) if x.startswith(window_name)]


def getOutliner():
    ol_panels = [x for x in cmds.lsUI(ed=True) if 'outlinerPanel' in x]
    ol_editors = []
    for ol in ol_panels:
        try:
            ol_editors.append(cmds.outlinerPanel(ol, q=True, outlinerEditor=True))
        except:
            pass
    return ol_editors


def expandOutlinerSelected():
    ol_editors = getOutliner()
    for ol in ol_editors:
        cmds.outlinerEditor(ol, e=True, showSelected=True)


class TextScrollListWindow(object):
    def __init__(self, default_list_=[], window_title='TextScrollListWindow'):
        self.list_ = default_list_
        self.window_title = window_title

        self.window = window_title
        if pm.window(self.window, ex=True):
            pm.deleteUI(self.window)

        self.window = pm.window(self.window, t=self.window_title, w=400)
        fl = pm.formLayout()
        self.cl = pm.columnLayout(adj=True, rs=3, co=['both', 2])
        self.tsl = pm.textScrollList(ams=True, h=300)
        if self.list_:
            pm.textScrollList(self.tsl, e=True, append=self.list_)

        pm.formLayout(fl, e=True, af=[(self.cl, 'top', 5), (self.cl, 'left', 5), (self.cl, 'right', 5), (self.cl, 'bottom', 5)])
        #pm.formLayout(fl, e=True, af=[(self.tsl, 'top', 5), (self.tsl, 'left', 5), (self.tsl, 'right', 5), (self.tsl, 'bottom', 5)])

    def init_ui(self):
        self.window.show()


class WindowManage(object):
    def __init__(self, exceptWinList_=[]):
        windows = cmds.lsUI(type='window')
        dwl = cmds.lsUI(dw=True)
        for dw in dwl:
            if cmds.workspaceControl(dw, ex=True):
                windows.append(dw)
        exceptWinList = [
            u'MayaWindow',
        ]
        if exceptWinList_:
            exceptWinList += exceptWinList_
        self.windows = pyCommon.negationList(windows, exceptWinList)

        self.windowsQt = []
        for w in self.windows:
            ptr = OpenMayaUI.MQtUtil.findWindow(w)
            if ptr is not None:
                self.windowsQt.append(wrapInstance(int(ptr), QWidget))

        # Qt
        nowWindowList = getMainWindowAsQMainWindow().findChildren(QMainWindow)
        self.windowsQt += nowWindowList

        # flug
        self.is_stop = True
        self.minimum_turn = True

    def minimized(self):
        for w in self.windowsQt:
            w.setWindowState(Qt.WindowMinimized)
            print(w.windowTitle())
            print(w.findChildren(QLineEdit))
            buttons = w.findChildren(QPushButton)
            if w.windowTitle() == 'Convert Fbx (Texture & Material)':
                for b in buttons:
                    print(b.click())
            self.stop()

    def active(self):
        for w in self.windowsQt:
            w.setWindowState(Qt.WindowActive)
            self.stop()

    def toggle(self, minimum_turn):
        if minimum_turn:
            self.minimized()
            minimum_turn = False
        else:
            self.active()
            minimum_turn = True
        return minimum_turn

    def delete(self):
        for w in self.windowsQt:
            w.close()
            self.stop()

    def reset(self, x, y, width, h):
        pos = 0
        for w in self.windowsQt:
            w.setGeometry(x + pos, y + pos, width, h)
            pos -= 20

    def stop(self):
        if self.is_stop:
            time.sleep(0.025)
            cmds.refresh()
