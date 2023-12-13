# -*- coding: utf-8 -*-
u"""ベースウインドウ"""
from datetime import datetime
from logging import getLogger
from functools import partial
import os
import os.path

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtUiTools import *
    from PySide2.QtWidgets import *
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide.QtUiTools import QUiLoader
    from shiboken import wrapInstance

import maya.cmds as cmds
import maya.cmds as mc
import maya.OpenMayaUI as OpenMayaUI
from functools import wraps

import mtk3d.maya.rig.cyShakeMake.module.cyShakeMake as shake

logger = getLogger(__name__)
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


def undo_redo(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        is_error = False
        cmds.undoInfo(ock=True)
        try:
            result = func(*args, **kwargs)
        except Exception:
            is_error = True
        finally:
            cmds.undoInfo(cck=True)
            if is_error:
                raise
            return result

    return wrapper


class cyShakeMaker(object):
    u"""ベースウインドウクラス"""

    def __init__(self, *args, **kwargs):
        """初期化"""
        self.window = self.__class__.__name__
        self.close()

    def show(self):
        u"""Windowのレイアウト作成

        ここにレイアウトを記述する
        """
        u"""Windowの初期化"""

        if not cmds.window(self.window, ex=True):
            self.window = cmds.window(self.window, mb=True)

        mc.menu(label='Menu', tearOff=True)
        cmds.setParent('..')

        mainLayout = cmds.columnLayout(adj=1)

        # レイアウト作成 ====
        loader = QUiLoader()
        uiFile = os.path.join(CURRENT_PATH, 'GUI.ui')
        self.ui = self.load_file(uiFile)

        # ====

        cmds.setParent(mainLayout)

        # kannsuunoset
        self.connect()

        '''
        QtにMayaのパーツ追加
        button = cmds.button()
        self.add_control(button, parent=self.ui.scrLyt)
        '''

        """scrlList = mc.textScrollList('scrLst',numberOfRows=20,w=300,h=200,en=True,allowMultiSelection=True,sc=(partial(fnc.selList, self.ui)))
        self.add_control(scrlList, parent=self.ui.scrollFrame) """

        cmds.optionVar(stringValueAppend=['myCurveOptionVar', '0, 1, 2'])
        cmds.optionVar(stringValueAppend=['myCurveOptionVar', '1, 0, 2'])

        Gname = cmds.gradientControlNoAttr('falloffCurve', height=90, width=250,
                                           asString='0, 0, ' + '2' + ', 1, 0.5, ' + '2' + ', 0, 1, ' + '2', civ=2,
                                           cc=shake.setInterpolation)

        self.add_control(Gname, parent=self.ui.gradientCurve)

        Menu_01 = cmds.optionMenu("Menu_01", w=300, l="Interpolation", cc=shake.Charactor_Set)
        cmds.menuItem(label='None')
        cmds.menuItem(label='Linear')
        cmds.menuItem(label='Smooth')
        cmds.menuItem(label='Spline')

        self.add_control(Menu_01, parent=self.ui.MenuSpace)

        cmds.showWindow(self.window)
        cmds.window(self.window, e=True, sizeable=True, title='cyMakeShake', wh=(280, 510))

    # ----------------------------------------------------------------------

    @undo_redo
    def connect(self):
        # self.ui.findBtn.clicked.connect(partial(fnc.find, self.ui))
        # self.ui.rockslist.pressed.connect(partial(fnc.selList, self.ui))
        self.ui.shakeMakeButton.clicked.connect(partial(shake.runShake, self.ui))

        self.ui.translateShake.clicked.connect(partial(shake.translateOnCallBack, self.ui))

        self.ui.tX.clicked.connect(partial(shake.translateOffCallBack, self.ui))
        self.ui.tY.clicked.connect(partial(shake.translateOffCallBack, self.ui))
        self.ui.tZ.clicked.connect(partial(shake.translateOffCallBack, self.ui))

        self.ui.rotateShake.clicked.connect(partial(shake.rotateOnCallBack, self.ui))

        self.ui.rX.clicked.connect(partial(shake.rotateOffCallBack, self.ui))
        self.ui.rY.clicked.connect(partial(shake.rotateOffCallBack, self.ui))
        self.ui.rZ.clicked.connect(partial(shake.rotateOffCallBack, self.ui))

    def close(self, *args):
        u"""Windowのclose"""
        if cmds.window(self.window, ex=True):
            cmds.deleteUI(self.window)

    def _add_baselayout(self):
        u"""基本レイアウトの追加"""
        if mc.dockControl('cyWorkFilerDockV2', ex=True):
            mc.deleteUI('cyWorkFilerDockV2')

        # mainform = cmds.formLayout(nd=100)
        # maintab = cmds.tabLayout(tv=False, scr=True, cr=True, h=1)
        # cmds.setParent('..')

        mainLayout = cmds.columnLayout(adj=1)

        # レイアウト作成 ====
        self.create()
        # ====

        cmds.setParent(mainLayout)

    # need
    def load_file(self, ui_file, parent=None):
        u"""Qt DesignerのUIファイルをロードしてレイアウトに追加

        :param ui_file: Qt Designerで作成したUIファイルのフルパス
        :param parent: MayaLayout名
        :return: QWidget
        """
        # Windowが生成されていなければ生成
        if not cmds.window(self.window, ex=True):
            self.window = cmds.window(self.window, mb=True)

        file_ = QFile(ui_file)
        file_.open(QFile.ReadOnly)
        loader = QUiLoader()
        ui = loader.load(file_)
        file_.close()

        layout = parent if parent else cmds.setParent(q=True)
        parent_ptr = OpenMayaUI.MQtUtil.findControl(layout)
        ptr = OpenMayaUI.MQtUtil.findControl(ui.objectName())

        OpenMayaUI.MQtUtil.addWidgetToMayaLayout(int(ptr), int(parent_ptr))  # noqa

        # Maya上での表示対策
        ui.setMinimumSize(ui.size())
        ui.parentWidget()
        return ui

    def add_widget(self, widget, parent=None):
        u"""Qt WidgetをMayaレイアウトに追加

        :param widget: QWidget
        :type widget: QWidget
        :param parent: MayaLayout名
        :param parent: str
        """
        # Windowが生成されていなければ生成
        self._initialize_window()

        layout = parent if parent else cmds.setParent(q=True)
        parent_ptr = OpenMayaUI.MQtUtil.findControl(layout)
        if not (widget.objectName()):
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            widget.setObjectName('_{0}_QWidget'.format(timestamp))

        ptr = OpenMayaUI.MQtUtil.findControl(widget.objectName())
        OpenMayaUI.MQtUtil.addWidgetToMayaLayout(int(ptr), int(parent_ptr))  # noqa
        # Maya上での表示対策
        widget.parentWidget()

    def add_control(self, control, parent):
        """controlをQLayoutに追加

        :param control: MayaControl名
        :type control: str
        :param parent: QLayout
        :type parent: QLayout
        """
        ptr = OpenMayaUI.MQtUtil.findControl(control)
        widget = wrapInstance(int(ptr), QWidget)  # noqa
        parent.addWidget(widget)


def main():
    QApplication.instance()
    ui = cyShakeMaker()
    ui.show()
    # sys.exit(app.exec_())
    return ui


if __name__ == '__main__':
    main()
