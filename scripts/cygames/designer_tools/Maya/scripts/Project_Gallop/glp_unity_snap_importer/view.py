# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from importlib import reload
except Exception:
    pass

import os

from PySide2 import QtCore, QtGui, QtWidgets
from maya.app.general import mayaMixin

from .ui import snap_importer_gui as main_window
from .ui import connect_item_gui as connect_item
from . import const

reload(main_window)
reload(connect_item)
reload(const)


class View(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    """GUI用
    イベントの追加

    Args:
        QMainWindow ([type]): [description]
    """

    def __init__(self, main, parent=None):

        super(View, self).__init__(parent)
        self.ui = main_window.Ui_MainWindow()
        self.ui.setupUi(self)
        self.main = main

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def closeEvent(self, event):
        self.main.on_close_event()


class ConnectionItem(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QWidget):

    # Setボタンが押されたことを示すシグナル
    setButtonPushed = QtCore.Signal(QtWidgets.QWidget)
    # マッピング状態が更新されたことを示すシグナル
    connectionUpdated = QtCore.Signal(str)

    def __init__(self, grp_id, obj_type, unity_name, check_opt_dicts, parent=None):

        script_dir = os.path.dirname(os.path.realpath(__file__))
        icon_dir = os.path.join(script_dir, 'ui', 'icons')

        self.type_icon = None
        if obj_type == const.TYPE_OBJ:
            self.type_icon = QtGui.QPixmap(os.path.join(icon_dir, 'poly_icon.png'))
        elif obj_type == const.TYPE_CHARA_MATERIAL:
            self.type_icon = QtGui.QPixmap(os.path.join(icon_dir, 'material_icon.png'))
        elif obj_type == const.TYPE_LIGHT:
            self.type_icon = QtGui.QPixmap(os.path.join(icon_dir, 'light_icon.png'))
        elif obj_type == const.TYPE_CAMERA:
            self.type_icon = QtGui.QPixmap(os.path.join(icon_dir, 'camera_icon.png'))

        self.maya_icon = QtGui.QPixmap(os.path.join(icon_dir, 'maya_icon.png'))
        self.unity_icon = QtGui.QPixmap(os.path.join(icon_dir, 'unity_icon.png'))
        self.link_icon = QtGui.QPixmap(os.path.join(icon_dir, 'link_icon.png'))

        self.grp_id = grp_id
        self.is_input_ok = True

        super(ConnectionItem, self).__init__(parent)
        self.ui = connect_item.Ui_Form()
        self.setup_ui(obj_type, unity_name, check_opt_dicts)
        self.setup_event()

    def setup_ui(self, obj_type, unity_name, check_opt_dicts):
        """UIセットアップ

        Args:
            obj_type (str): オブジェクトタイプ
            unity_name (str): Unityのルート名
            check_opt_dicts ([{'Flag': str, 'Value': bool, 'Visible': bool},,,]): オプション項目のリスト
        """

        self.ui.setupUi(self)

        # icon
        self.ui.unity_label.setPixmap(self.unity_icon)
        self.ui.maya_label.setPixmap(self.maya_icon)
        self.ui.link_label.setPixmap(self.link_icon)

        if self.type_icon:
            self.ui.type_icon_label.setPixmap(self.type_icon)

        self.ui.type_label.setText(obj_type)
        self.ui.unity_name_label.setText(unity_name)

        # フラグ用チェックボックスの作成
        QtCore.QDir.addSearchPath('icons', os.path.join(os.path.dirname(__file__), 'ui/icons'))
        for check_opt_dict in check_opt_dicts:
            check = QtWidgets.QCheckBox()
            check.setText(check_opt_dict['Flag'])
            check.setChecked(check_opt_dict['Value'])
            self.ui.checks_layout.addWidget(check)
            check.setVisible(check_opt_dict['Visible'])

            # インジケーターをオリジナルのスタイルに変更
            check.setStyleSheet("""
                QCheckBox::indicator:checked {{
                    image: url({0});
                }}
                QCheckBox::indicator:unchecked {{
                    image: url({1});
                }}
            """.format('icons:checked.png', 'icons:unchecked.png'))

        self.ui.maya_name_line.setStyleSheet('background-color:rgb(0, 0, 0)')
        self.__set_input_font_col()

    def setup_event(self):
        """イベントセットアップ
        """

        self.ui.name_set_button.clicked.connect(self.maya_root_set_button_event)
        self.ui.name_del_button.clicked.connect(self.maya_root_del_button_event)

        for index in range(self.ui.checks_layout.count()):
            item = self.ui.checks_layout.itemAt(index)
            check_widget = item.widget()
            check_widget.stateChanged.connect(self.check_change_event)

    def maya_root_set_button_event(self):
        """Mayaルート名セットボタン押下時のイベント
        main側で判定を行ってからセットしたいのでここではイベントを発火するだけ
        判定に通ればset_maya_root()を使ってセットする
        """
        self.setButtonPushed.emit(self)

    def maya_root_del_button_event(self):
        """Mayaルート名削除時のイベント
        """
        self.ui.maya_name_line.setText('')
        self.connectionUpdated.emit('')

    def check_change_event(self):
        """チェックボックス操作時のイベント
        """
        self.connectionUpdated.emit('')

    def set_maya_root(self, maya_root):
        """mayaルートをセット
        """
        self.ui.maya_name_line.setText(maya_root)
        self.connectionUpdated.emit('')

    def get_use_opts(self):
        """有効なオプション名を取得

        Returns:
            list: 有効になっている（非表示も含む）オプションフラグリスト
        """
        opts = []
        for index in range(self.ui.checks_layout.count()):
            item = self.ui.checks_layout.itemAt(index)
            check_widget = item.widget()
            if check_widget.isChecked():
                opts.append(check_widget.text())
        return opts

    def set_input_ok(self, is_input_ok):
        """Mayaルート名の指定が有効かどうかをセット

        Args:
            is_input_ok (bool): 有効とみなすか
        """

        self.is_input_ok = is_input_ok
        self.__set_input_font_col()

    def __set_input_font_col(self):
        """Mayaルート指定が有効かどうかでフォントカラーを変更する
        """

        if self.is_input_ok:
            self.ui.maya_name_line.setStyleSheet('color:rgb(255, 255, 255); background-color:rgb(0, 0, 0)')
        else:
            self.ui.maya_name_line.setStyleSheet('color:rgb(255,32,32); background-color:rgb(0, 0, 0)')
