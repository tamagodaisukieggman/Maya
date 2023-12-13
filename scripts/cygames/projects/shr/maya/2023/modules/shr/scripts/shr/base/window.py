# -*- coding: utf-8 -*-
u"""ベースウインドウ"""

import os
from datetime import datetime
import codecs

try:
    from PySide2.QtCore import QFile
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtWidgets import QWidget
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtCore import QFile
    from PySide.QtGui import QWidget
    from PySide.QtUiTools import QUiLoader
    from shiboken import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as OpenMayaUI

# from mtku.maya.log import MtkDBLog
# from mtku.maya.constant import MTK_MAYA_MANUAL_HELP_URL
MTK_MAYA_MANUAL_HELP_URL = 'https://wisdom.cygames.jp/pages/viewpage.action?pageId=14486788'

# logger = MtkDBLog(__name__)


class BaseWindow(object):
    u"""ベースウインドウクラス"""

    def __init__(self, *args, **kwargs):
        """初期化

        :param title: windowタイトル
        :type title: str
        :param width: 幅
        :type width: int
        :param height: 高さ
        :type height: int
        :param typ: windowのタイプ 0 apply & closeボタンあり 1 closeボタンのみあり 2 ボタンなし
        :type  typ: int
        :param apply_callback: applyボタンのcallback関数
        :type  apply_callback: function
        :param save_callback:「Save Settings」のcallback関数
        :type  save_callback: function
        :param reset_callback:「Reset Settings」のcallback関数
        :type  reset_callback: function
        :param help_callback:「Help」のcallback関数
        :type help_callback: function
        """
        self.window = self.__class__.__name__
        self.close()

        self.edit_menu = None
        self.help_menu = None
        self.main_layout = None

        self._typ = kwargs.setdefault('typ', 0)
        self._exists_window = False

        self.title = kwargs.setdefault('title', self.window)
        self.width = kwargs.setdefault('width', 500)
        self.height = kwargs.setdefault('height', 500)
        self.url = u'{}/index.html'.format(os.path.dirname(MTK_MAYA_MANUAL_HELP_URL))

        self.apply_callback = kwargs.setdefault('apply_callback', None)
        self.save_callback = kwargs.setdefault('save_callback', None)
        self.reset_callback = kwargs.setdefault('reset_callback', None)
        # self.help_callback = kwargs.setdefault('help_callback', None)

        # self._initialize_window()

    def create(self):
        u"""Windowのレイアウト作成

        BaseWindowを継承したWindowを作成する場合は
        このメソッドをオーバーライドしてレイアウトを記述してください
        """
        pass  # NOQA

    def _initialize_window(self):
        u"""Windowの初期化"""
        # self.close()
        # self.window = cmds.window(self.window, mb=True)
        # self._add_baselayout()
        if not cmds.window(self.window, ex=True):
            self.window = cmds.window(self.window, mb=True)

    def show(self, *args):
        u"""Windowの表示"""
        self._initialize_window()
        self._add_baselayout()

        cmds.showWindow(self.window)
        cmds.window(self.window, e=True, t=self.title, wh=(self.width, self.height))

    def close(self, *args):
        u"""Windowのclose"""
        if cmds.window(self.window, ex=True):
            cmds.deleteUI(self.window)

    def add_menu(self, label):
        u"""menuを追加

        :param label: ラベル名
        :type label: str
        :return: menu名
        :rtype: str
        """
        return cmds.menu(l=label, p=self.window, to=True)

    def add_menuitem(self, label, parent, callback=None):
        u"""menuItemを追加

        :param label: ラベル名
        :type label: str
        :param parent: 親メニュー名
        :type parent: str
        :param callback: callback
        :type callback: function
        """
        if callback:
            cmds.menuItem(l=label, p=parent, c=callback)
        else:
            cmds.menuItem(l=label, p=parent)

    def _add_editmenu(self):
        u"""menu「Edit」を追加"""
        self.edit_menu = cmds.menu(l='Edit')
        cmds.menuItem(l='Save Settings', c=self.save_settings)
        cmds.menuItem(l='Reset Settings', c=self.reset_settings)

    def _add_helpmenu(self):
        u"""menu「Help」を追加"""
        self.help_menu = cmds.menu(l='Help', hm=True)
        cmds.menuItem(l='Help on {0}'.format(self.title), c=self.help)

    def _add_baselayout(self):
        u"""基本レイアウトの追加"""
        # メニューバー
        self._add_editmenu()
        self._add_helpmenu()

        mainform = cmds.formLayout(nd=100)
        maintab = cmds.tabLayout(tv=False, scr=True, cr=True, h=1)
        self.main_layout = cmds.columnLayout(adj=1)
        # レイアウト作成 ====
        self.create()
        # ====

        cmds.setParent('..')

        cmds.setParent(mainform)
        execform = self._add_execform()
        cmds.formLayout(
            mainform, e=True,
            af=(
                [maintab, 'top', 0],
                [maintab, 'left', 2],
                [maintab, 'right', 2],
                [execform, 'left', 2],
                [execform, 'right', 2],
                [execform, 'bottom', 0],
            ),
            ac=(
                [maintab, 'bottom', 5, execform],
            ),
        )
        cmds.setParent(self.main_layout)

    def _add_execform(self):
        u"""Apply Closeボタンの追加

        :return: フォーム名
        :rtype: str
        """
        execform = cmds.formLayout(nd=100)
        if self._typ == 0:
            # ボタン
            apply_close_btn = cmds.button(l='Apply and Close', h=26, c=self._apply_close)
            apply_btn = cmds.button(l='Apply', h=26, c=self.apply_)
            close_btn = cmds.button(l='Close', h=26, c=self.close)
            # レイアウト
            cmds.formLayout(
                execform, e=True,
                af=(
                    [apply_close_btn, 'left', 0],
                    [apply_close_btn, 'bottom', 5],
                    [apply_btn, 'bottom', 5],
                    [close_btn, 'bottom', 5],
                    [close_btn, 'right', 0],
                ),
                ap=(
                    [apply_close_btn, 'right', 1, 33],
                    [close_btn, 'left', 0, 67],
                ),
                ac=(
                    [apply_btn, 'left', 4, apply_close_btn],
                    [apply_btn, 'right', 4, close_btn],
                ),
            )

        elif self._typ == 1:
            # ボタン
            close_btn = cmds.button(l='Close', h=26, c=self.close)
            # レイアウト
            cmds.formLayout(
                execform, e=True,
                af=(
                    [close_btn, 'left', 0],
                    [close_btn, 'bottom', 5],
                    [close_btn, 'right', 0],
                ),
            )

        cmds.setParent('..')
        return execform

    def _apply_close(self, *args):
        u"""ApplyCloseボタンの実行コマンド"""
        self.apply_()
        self.close()

    def apply_(self, *args):
        u"""Applyボタンの実行コマンド

        BaseWindowを継承したWindowを作成する場合は
        このメソッドをオーバーライドすることでApplyボタンの実行内容を変更できます
        """
        self.apply_callback() if self.apply_callback else None

    def save_settings(self, *args):
        u"""設定の保存

        BaseWindowを継承したWindowを作成する場合は
        このメソッドをオーバーライドすることで
        メニュー「Edit > Save Settings」の実行内容を変更できます
        """
        self.save_callback() if self.save_callback else None

    def reset_settings(self, *args):
        u"""設定のリセット

        BaseWindowを継承したWindowを作成する場合は
        このメソッドをオーバーライドすることで
        メニュー「Edit > Reset Settings」の実行内容を変更できます
        """
        self.reset_callback() if self.reset_callback else None

    # def help(self, *args):
    #     u"""help表示
    #
    #     BaseWindowを継承したWindowを作成する場合は
    #     このメソッドをオーバーライドすることで
    #     メニュー「Help > Help on ***」の実行内容を変更できます
    #     """
    #     self.help_callback() if self.help_callback else None

    def help(self, *args):
        u"""help表示"""
        cmds.showHelp(self.url, a=True)

    def load_qss_file(self, qss_file, parent=None):
        u"""QSSファイルをロードして色変更"""
        with codecs.open(qss_file, 'r') as f:
            stylesheet = f.read()

        if parent:
            parent.setStyleSheet(stylesheet)
        else:
            ptr = OpenMayaUI.MQtUtil.findControl(self.window)
            widget = wrapInstance(int(ptr), QWidget)  # NOQA
            widget.setStyleSheet(stylesheet)

    def load_file(self, ui_file, parent=None):
        u"""Qt DesignerのUIファイルをロードしてレイアウトに追加

        :param ui_file: Qt Designerで作成したUIファイルのフルパス
        :type ui_file: str
        :param parent: MayaLayout名
        :type parent: str
        :return: QWidget
        :rtype: QWidget
        """
        # Windowが生成されていなければ生成
        self._initialize_window()

        file_ = QFile(ui_file)
        file_.open(QFile.ReadOnly)
        loader = QUiLoader()
        ui = loader.load(file_)
        file_.close()

        layout = parent if parent else cmds.setParent(q=True)
        parent_ptr = OpenMayaUI.MQtUtil.findControl(layout)
        ptr = OpenMayaUI.MQtUtil.findControl(ui.objectName())

        OpenMayaUI.MQtUtil.addWidgetToMayaLayout(int(ptr), int(parent_ptr))  # NOQA

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
        if not(widget.objectName()):
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            widget.setObjectName('_{0}_QWidget'.format(timestamp))

        ptr = OpenMayaUI.MQtUtil.findControl(widget.objectName())
        OpenMayaUI.MQtUtil.addWidgetToMayaLayout(int(ptr), int(parent_ptr))  # NOQA
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
        widget = wrapInstance(int(ptr), QWidget)  # NOQA
        parent.addWidget(widget)
