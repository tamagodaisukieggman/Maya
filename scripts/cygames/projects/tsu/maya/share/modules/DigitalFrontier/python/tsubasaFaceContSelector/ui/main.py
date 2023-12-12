# -*- coding: utf-8 -*-
"""
Copyright (C) 2021 Digital Frontier Inc.
"""
import os
import sys
import imp
import functools as ft

try:
    imp.find_module('PySide2')
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2.QtUiTools import QUiLoader
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide.QtUiTools import QUiLoader

import tsubasaFaceContSelector.core as core
from tsubasaFaceContSelector.ui.statusBar import StatusBarWidget
WIDTH = 460
HEIGHT = 330

if sys.version_info[0] == 3:
    long = int

class CustomGroupBox(QGroupBox):
    mouse_release = Signal(list)

    def __init__(self, parent):
        QGroupBox.__init__(self, parent)
        self.rubber_band = None

    def mousePressEvent(self, e):
        self.origin = e.pos()
        if not self.rubber_band:
            self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)
            self.rubber_band.setGeometry(QRect(self.origin, e.pos()).normalized())
            self.rubber_band.show()
        else:
            return QGroupBox.mousePressEvent(self, e)

    def mouseMoveEvent(self, e):
        if not self.rubber_band:
            return QGroupBox.mouseMoveEvent(self, e)
        self.rubber_band.setGeometry(
            QRect(self.origin, e.pos()).normalized())

    def mouseReleaseEvent(self, e):
        if not self.rubber_band:
            return QGroupBox.mouseMoveEvent(self, e)

        self.rubber_band.hide()
        self.rubber_band = None

        start_pos = self.origin
        end_pos = e.pos()
        btn_name = []
        for wid in self.children():
            if not wid.__class__.__name__ == 'QPushButton':
                continue

            sel_range_min_x = start_pos.x()
            sel_range_max_x = end_pos.x()
            sel_range_min_y = start_pos.y()
            sel_range_max_y = end_pos.y()

            if start_pos.x() - end_pos.x() > 0:
                sel_range_min_x = end_pos.x()
                sel_range_max_x = start_pos.x()
            if start_pos.y() - end_pos.y() > 0:
                sel_range_min_y = end_pos.y()
                sel_range_max_y = start_pos.y()

            # if (wid.x() + wid.width()) > sel_range_max_x:
            #     continue
            # if wid.x() < sel_range_min_x:
            #     continue
            # if (wid.y() + wid.height()) > sel_range_max_y:
            #     continue
            # if wid.y() < sel_range_min_y:
            #     continue

            if (wid.x() + wid.width()) < sel_range_min_x:
                continue
            if wid.x() > sel_range_max_x:
                continue
            if (wid.y() + wid.height()) < sel_range_min_y:
                continue
            if wid.y() > sel_range_max_y:
                continue
            btn_name.append(wid.objectName())
        self.mouse_release.emit(btn_name)


class CustomQUiLoader(QUiLoader):
    def createWidget(self, className, parent=None, name=''):
        if className == 'CustomGroupBox':
            ret = CustomGroupBox(parent)
            ret.setObjectName(name)
            return ret
        if className == 'CustomListWidget':
            ret = CustomListWidget(parent)
            ret.setObjectName(name)
            return ret
        return QUiLoader.createWidget(self, className, parent, name)


class CustomListWidget(QListWidget):

    def __init__(self, parent):
        QListWidget.__init__(self, parent)

    def keyPressEvent(self, e):
        return


class MainWidget(QMainWindow):
    UIFILE = os.path.abspath(__file__).replace('.py', '.ui')

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = CustomQUiLoader().load(self.UIFILE)
        # self.ui = QUiLoader().load(self.UIFILE)
        self.statusbar_widget = StatusBarWidget(self)
        self.btn_name_to_rig_name = core.get_button_settings_info()['rig_name']
        self.but_name_to_btn_color = core.get_button_settings_info()['btn_color']

        self.namespace = 'cXXX'
        self.symmetry = True

        self.setup_ui()
        self.reload_namespace()
        self.update()
        self.resize(WIDTH, HEIGHT)

    # =============================
    # GUI Settings
    # =============================
    def setup_ui(self):
        """uiの処理
        """
        self.setCentralWidget(self.ui)
        self.setWindowTitle('FaceContSelector')
        self.setStatusBar(self.statusbar_widget)

        for btn in self.ui.face_btn_grp.children():
            # Clickのシグナルとコマンドを接続する
            btn_name = btn.objectName()
            if '_btn' not in btn_name:
                continue
            btn.clicked.connect(ft.partial(self.click_cont_btn, btn_name))

            # ボタンの色を設定する
            btn_color = self.but_name_to_btn_color.get(btn_name)
            if not btn_color:
                continue
            btn.setStyleSheet('background-color: %s' % btn_color)

        # 対象ボタン
        self.ui.symmetry_tbn.clicked.connect(self.update)
        # リロードボタン
        self.ui.reload_btn.clicked.connect(self.reload_namespace)
        # Namespaceの選択リスト
        self.ui.namespace_lw.itemSelectionChanged.connect(self.update)
        self.ui.namespace_lw.itemDoubleClicked.connect(self.view_fit)
        self.ui.face_btn_grp.mouse_release.connect(self.select_cont)

    def update(self):
        """Namespaceの更新と、Symmetryの状態の更新
        """
        items = self.ui.namespace_lw.selectedItems()
        if items:
            self.namespace = items[0].text()
            core.get_logger().info('NameSpace: %s' % self.namespace)
        else:
            core.get_logger().info('NameSpace: None')
            self.namespace = None
        self.symmetry = self.ui.symmetry_tbn.isChecked()

    def get_select_add_mode(self):
        """Shiftが押されているとTrueを返す
        """
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ShiftModifier:
            return True
        return False

    # ========================
    # Button Settings
    # ========================
    def reload_namespace(self):
        """Namespaceのリストを更新する
        """
        namespace_list = core.get_namespace_list()
        self.ui.namespace_lw.clear()
        self.ui.namespace_lw.addItems(namespace_list)

    def view_fit(self):
        """ボタンのリストからすべてのコントローラーを作成し
        それを選択し、Viewにフィットさせる
        """
        select_list = []
        for btn in self.ui.face_btn_grp.children():
            btn_name = btn.objectName()
            if '_btn' not in btn_name:
                continue
            rig_name = self.btn_name_to_rig_name.get(btn_name)
            if not rig_name:
                continue
            ns_rig_name = '%s:%s' % (self.namespace, rig_name)
            if self.namespace == 'EMPTY':
                ns_rig_name = rig_name
            select_list.append(ns_rig_name)
        core.view_fit(select_list)

    def click_cont_btn(self, click_btn_name):
        """Buttonがクリックされたときの処理
        """
        btn_name_list = [click_btn_name]
        # allと名前のつくボタンの処理
        if '_all_' in click_btn_name:
            # ボタンの種類を名前より抜き出す
            btn_category = click_btn_name.split('_')[0]
            # ボタンのリストから、同じ種類のボタンを探す
            for btn in self.ui.face_btn_grp.children():
                btn_name = btn.objectName()
                if btn_name.startswith(btn_category):
                    btn_name_list.append(btn_name)
        self.select_cont(btn_name_list)

    def select_cont(self, btn_name_list):
        # 対象ボタンがOnの場合、反対のボタンを探し追加する
        if self.symmetry:
            temp_lsit = []
            for btn_name in btn_name_list:
                if '_L_' in btn_name:
                    temp_lsit.append(btn_name.replace('_L_', '_R_'))
                elif '_R_' in btn_name:
                    temp_lsit.append(btn_name.replace('_R_', '_L_'))
            btn_name_list += temp_lsit

        # リグの名前を作成する
        select_list = []
        for btn_name in btn_name_list:
            rig_name = self.btn_name_to_rig_name.get(btn_name)
            if not rig_name:
                continue
            ns_rig_name = '%s:%s' % (self.namespace, rig_name)
            if self.namespace == 'EMPTY':
                ns_rig_name = rig_name
            select_list.append(ns_rig_name)

        # 追加選択か、単品選択かを取得し、コマンドを実行
        select_add_flag = self.get_select_add_mode()
        core.select_node(select_list, select_add_flag)

        # これをしておかないと、listWidgetの選択が変わってしまうことがあるため
        self.ui.namespace_lw.clearFocus()


def main_debug(argv=sys.argv):
    """ GUIを起動させるメイン関数（開発用）
    """
    app = QApplication(argv)
    ui = MainWidget()
    ui.resize(500, 200)
    # GUIのスタイルシートに社内共通のもを適用する
    try:
        import dfQdarkstyle
        app.setStyleSheet(dfQdarkstyle.load_stylesheet(pyside=True))
    except Exception:
        pass
    ui.show()
    sys.exit(app.exec_())


def maya():
    import maya.cmds as cmds
    from maya import OpenMayaUI as omui
    try:
        from shiboken2 import wrapInstance
    except Exception:
        from shiboken import wrapInstance
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QWidget)

    global face_cont_selector
    try:
        face_cont_selector.show()
        return
    except Exception:
        pass

    face_cont_selector = MainWidget(parent=mayaMainWindow)
    face_cont_selector.show()


def debug_maya():
    import maya.cmds as cmds
    from maya import OpenMayaUI as omui
    try:
        from shiboken2 import wrapInstance
    except Exception:
        from shiboken import wrapInstance
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QWidget)

    global face_cont_selector
    try:
        face_cont_selector.close()
    except Exception:
        pass

    face_cont_selector = MainWidget(parent=mayaMainWindow)
    face_cont_selector.show()


if __name__ == '__main__':
    sys.exit(main_debug())
