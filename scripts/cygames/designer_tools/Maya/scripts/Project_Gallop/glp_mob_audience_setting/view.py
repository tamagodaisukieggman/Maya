# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import re
import maya.cmds as cmds

from PySide2 import QtWidgets, QtCore
from maya.app.general import mayaMixin

from .ui import mob_audience_setting_window


class View(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    """GUI用
    イベントの追加

    Args:
        QMainWindow ([type]): [description]
    """

    def __init__(self, parent=None):

        super(View, self).__init__(parent)
        self.ui = mob_audience_setting_window.Ui_MainWindow()
        self.ui.setupUi(self)

        # QButtonGroupのみ何故かCompileで引っかかるのでこちらで手書き
        self.ui.distance_sort_rbg = QtWidgets.QButtonGroup()
        self.ui.distance_sort_rbg.addButton(self.ui.plus_x_rb)
        self.ui.distance_sort_rbg.addButton(self.ui.minus_x_rb)

        self.ui.rpt_scalex_toggle_button.clicked.connect(
            lambda: self.__toggle_scalex_button_event())
        self.ui.rpt_scaley_toggle_button.clicked.connect(
            lambda: self.__toggle_scaley_button_event())

        self.close_event_exec = None

    def closeEvent(self, event):

        if self.close_event_exec is not None:
            self.close_event_exec()

        self.deleteLater()
        super(View, self).closeEvent(event)

    def reset_scale_button_event(self):

        self.ui.rpt_scalex_toggle_button.setText(u'日陰(X=1)')
        self.ui.rpt_scalex_toggle_button.setStyleSheet('background-color: gray')
        self.ui.rpt_scaley_toggle_button.setText(u'晴れ(Y=1)')
        self.ui.rpt_scaley_toggle_button.setStyleSheet('background-color: red')

    def __toggle_scalex_button_event(self):

        if self.ui.rpt_scalex_toggle_button.text().startswith(u'日陰'):
            self.ui.rpt_scalex_toggle_button.setText(u'日向(X=2)')
            self.ui.rpt_scalex_toggle_button.setStyleSheet('background-color: orange')
        else:
            self.ui.rpt_scalex_toggle_button.setText(u'日陰(X=1)')
            self.ui.rpt_scalex_toggle_button.setStyleSheet('background-color: gray')

    def __toggle_scaley_button_event(self):

        if self.ui.rpt_scaley_toggle_button.text().startswith(u'晴れ'):
            self.ui.rpt_scaley_toggle_button.setText(u'雨(Y=2)')
            self.ui.rpt_scaley_toggle_button.setStyleSheet('background-color: blue')
        else:
            self.ui.rpt_scaley_toggle_button.setText(u'晴れ(Y=1)')
            self.ui.rpt_scaley_toggle_button.setStyleSheet('background-color: red')

    def get_scalex_value(self):

        text = self.ui.rpt_scalex_toggle_button.text()
        match_obj = re.search(r'.*?\(X=([1-2])\)', text)
        return int(match_obj.group(1))

    def get_scaley_value(self):

        text = self.ui.rpt_scaley_toggle_button.text()
        match_obj = re.search(r'.*?\(Y=([1-2])\)', text)
        return int(match_obj.group(1))


class AvoidanceObjView(QtWidgets.QHBoxLayout):

    def __init__(self, object_name='', parent=None):

        super(AvoidanceObjView, self).__init__(parent)
        self.delete_widget_event_hook_fanc = None

        self.__set_ui(object_name)

    def __set_ui(self, object_name):

        self.avoidance_obj_label = QtWidgets.QLabel()
        self.avoidance_obj_label.setText(object_name)
        self.addWidget(self.avoidance_obj_label)

        spacerItem3 = QtWidgets.QSpacerItem(40, 16, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.addItem(spacerItem3)

        self.avoidance_desc_label = QtWidgets.QLabel()
        self.avoidance_desc_label.setText(u'回避距離')
        self.addWidget(self.avoidance_desc_label)

        self.avoidance_distance_sb = QtWidgets.QDoubleSpinBox()
        self.avoidance_distance_sb.setDecimals(1)
        self.avoidance_distance_sb.setSingleStep(1)
        self.avoidance_distance_sb.setMaximum(99999.9)
        self.avoidance_distance_sb.setMinimum(-99999.9)
        self.avoidance_distance_sb.setProperty("value", 0.0)
        self.addWidget(self.avoidance_distance_sb)

        self.avoidance_desc_label2 = QtWidgets.QLabel()
        self.avoidance_desc_label2.setText(u'(cm)')
        self.addWidget(self.avoidance_desc_label2)

        self.del_avoidance_obj_view_button = QtWidgets.QPushButton()
        self.del_avoidance_obj_view_button.setText(u'削除')
        self.del_avoidance_obj_view_button.clicked.connect(lambda: self.del_widget())
        self.addWidget(self.del_avoidance_obj_view_button)

    def del_widget(self):
        """
        このwidgetを削除する。
        """

        if self.delete_widget_event_hook_fanc:
            self.delete_widget_event_hook_fanc(self)

        for i in range(self.count()):
            b = self.itemAt(i)
            wid = b.widget()
            if wid:
                wid.deleteLater()

        self.deleteLater()


class RandomPlacementTargetMeshView(QtWidgets.QGroupBox):

    def __init__(self, parent=None):

        super(RandomPlacementTargetMeshView, self).__init__(parent)

        self.delete_widget_event_hook_fanc = None

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        self.__set_ui()

    def __set_ui(self):

        # 大元のグループ直下のレイアウト
        self.rpt_container_layout = QtWidgets.QVBoxLayout(self)
        self.rpt_container_layout.setSpacing(2)
        self.rpt_container_layout.setContentsMargins(3, 3, 3, 3)

        # -----
        # ターゲット削除周りのレイアウト
        self.rpt_del_group_layout = QtWidgets.QHBoxLayout()

        self.rpt_target_mesh_list_label = QtWidgets.QLabel()
        self.rpt_target_mesh_list_label.setText(QtWidgets.QApplication.translate("MainWindow", "対象メッシュのリスト", None, -1))
        self.rpt_del_group_layout.addWidget(self.rpt_target_mesh_list_label)

        # ターゲット削除ボタン
        self.rpt_del_group_button = QtWidgets.QPushButton()
        self.rpt_del_group_button.setMaximumSize(QtCore.QSize(120, 16))
        self.rpt_del_group_button.setText(QtWidgets.QApplication.translate("MainWindow", "ターゲットを削除", None, -1))
        self.rpt_del_group_layout.addWidget(self.rpt_del_group_button)
        self.rpt_del_group_button.clicked.connect(lambda: self.del_widget())

        # ターゲット削除ボタンの横のスペーサー
        spacerItem3 = QtWidgets.QSpacerItem(40, 16, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.rpt_del_group_layout.addItem(spacerItem3)

        self.rpt_container_layout.addLayout(self.rpt_del_group_layout)

        # -----
        # メッシュ一覧レイアウト
        self.rpt_mesh_layout = QtWidgets.QHBoxLayout()

        # メッシュ一覧のテキストボックス
        self.rpt_mesh_list_widget = QtWidgets.QListWidget()
        self.rpt_mesh_list_widget.setMaximumSize(QtCore.QSize(16777215, 50))
        self.rpt_mesh_layout.addWidget(self.rpt_mesh_list_widget)

        # メッシュ選択ボタン
        self.rpt_select_mesh_button = QtWidgets.QPushButton()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rpt_select_mesh_button.sizePolicy().hasHeightForWidth())
        self.rpt_select_mesh_button.setSizePolicy(sizePolicy)
        self.rpt_select_mesh_button.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.rpt_select_mesh_button.setText(QtWidgets.QApplication.translate("MainWindow", "選択", None, -1))
        self.rpt_select_mesh_button.clicked.connect(lambda: self.select_mesh_event())

        # メッシュ追加/削除ボタンのレイアウト
        self.rpt_mesh_list_button_layout = QtWidgets.QVBoxLayout()
        self.rpt_mesh_list_button_layout.setSpacing(1)
        self.rpt_mesh_list_button_layout.setObjectName("rpt_mesh_list_button_layout")

        # メッシュ追加ボタン
        self.rpt_add_mesh_button = QtWidgets.QPushButton()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rpt_add_mesh_button.sizePolicy().hasHeightForWidth())
        self.rpt_add_mesh_button.setSizePolicy(sizePolicy)
        self.rpt_add_mesh_button.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.rpt_add_mesh_button.setText(QtWidgets.QApplication.translate("MainWindow", "追加", None, -1))
        self.rpt_add_mesh_button.clicked.connect(lambda: self.add_mesh_event())

        self.rpt_mesh_list_button_layout.addWidget(self.rpt_add_mesh_button)

        # メッシュ削除ボタン
        self.rpt_del_mesh_button = QtWidgets.QPushButton()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rpt_del_mesh_button.sizePolicy().hasHeightForWidth())
        self.rpt_del_mesh_button.setSizePolicy(sizePolicy)
        self.rpt_del_mesh_button.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.rpt_del_mesh_button.setText(QtWidgets.QApplication.translate("MainWindow", "削除", None, -1))
        self.rpt_del_mesh_button.clicked.connect(lambda: self.del_mesh_event())

        self.rpt_mesh_list_button_layout.addWidget(self.rpt_del_mesh_button)

        self.rpt_mesh_layout.addWidget(self.rpt_select_mesh_button)
        self.rpt_mesh_layout.addLayout(self.rpt_mesh_list_button_layout)
        self.rpt_container_layout.addLayout(self.rpt_mesh_layout)

        # -----
        self.rpt_value_sb_layout = QtWidgets.QHBoxLayout()

        self.rpt_ratio_label = QtWidgets.QLabel()
        self.rpt_ratio_label.setText(QtWidgets.QApplication.translate("MainWindow", "倍率", None, -1))
        self.rpt_value_sb_layout.addWidget(self.rpt_ratio_label)

        self.rpt_ratio_sb = QtWidgets.QDoubleSpinBox()
        self.rpt_ratio_sb.setDecimals(1)
        self.rpt_ratio_sb.setSingleStep(0.1)
        self.rpt_ratio_sb.setMaximum(100.0)
        self.rpt_ratio_sb.setMinimum(-100.0)
        self.rpt_ratio_sb.setProperty("value", 1.0)
        self.rpt_value_sb_layout.addWidget(self.rpt_ratio_sb)

        # -----
        self.rpt_height_label = QtWidgets.QLabel()
        self.rpt_height_label.setText(QtWidgets.QApplication.translate("MainWindow", "高さ", None, -1))
        self.rpt_value_sb_layout.addWidget(self.rpt_height_label)

        self.rpt_height_sb = QtWidgets.QDoubleSpinBox()
        self.rpt_height_sb.setDecimals(1)
        self.rpt_height_sb.setSingleStep(0.1)
        self.rpt_height_sb.setMaximum(100000.0)
        self.rpt_height_sb.setMinimum(-100000.0)
        self.rpt_value_sb_layout.addWidget(self.rpt_height_sb)

        # -----
        self.rpt_rot_x_label = QtWidgets.QLabel()
        self.rpt_rot_x_label.setText(QtWidgets.QApplication.translate("MainWindow", "rotX", None, -1))
        self.rpt_value_sb_layout.addWidget(self.rpt_rot_x_label)

        self.rpt_rot_x_sb = QtWidgets.QDoubleSpinBox()
        self.rpt_rot_x_sb.setDecimals(1)
        self.rpt_rot_x_sb.setSingleStep(0.1)
        self.rpt_rot_x_sb.setMaximum(9999.0)
        self.rpt_rot_x_sb.setMinimum(-9999.0)
        self.rpt_value_sb_layout.addWidget(self.rpt_rot_x_sb)

        # -----
        self.rpt_rot_y_label = QtWidgets.QLabel()
        self.rpt_rot_y_label.setText(QtWidgets.QApplication.translate("MainWindow", "rotY", None, -1))
        self.rpt_value_sb_layout.addWidget(self.rpt_rot_y_label)

        self.rpt_rot_y_sb = QtWidgets.QDoubleSpinBox()
        self.rpt_rot_y_sb.setDecimals(1)
        self.rpt_rot_y_sb.setSingleStep(0.1)
        self.rpt_rot_y_sb.setMaximum(9999.0)
        self.rpt_rot_y_sb.setMinimum(-9999.0)
        self.rpt_value_sb_layout.addWidget(self.rpt_rot_y_sb)

        # -----
        self.rpt_rot_z_label = QtWidgets.QLabel()
        self.rpt_rot_z_label.setText(QtWidgets.QApplication.translate("MainWindow", "rotZ", None, -1))
        self.rpt_value_sb_layout.addWidget(self.rpt_rot_z_label)

        self.rpt_rot_z_sb = QtWidgets.QDoubleSpinBox()
        self.rpt_rot_z_sb.setDecimals(1)
        self.rpt_rot_z_sb.setSingleStep(0.1)
        self.rpt_rot_z_sb.setMaximum(9999.0)
        self.rpt_rot_z_sb.setMinimum(-9999.0)
        self.rpt_value_sb_layout.addWidget(self.rpt_rot_z_sb)

        self.rpt_container_layout.addLayout(self.rpt_value_sb_layout)

    def del_widget(self):
        """
        このwidgetを削除する。
        """

        if self.delete_widget_event_hook_fanc:
            self.delete_widget_event_hook_fanc(self)

        self.deleteLater()

    def get_ratio(self):

        return self.rpt_ratio_sb.value()

    def get_height(self):

        return self.rpt_height_sb.value()

    def get_rot(self):

        return [self.rpt_rot_x_sb.value(), self.rpt_rot_y_sb.value(), self.rpt_rot_z_sb.value()]

    def get_mesh_list(self):

        item_text_list = []
        for i in range(self.rpt_mesh_list_widget.count()):
            item_text_list.append(self.rpt_mesh_list_widget.item(i).text())

        return item_text_list

    def clear_mesh_list(self):

        self.rpt_mesh_list_widget.clear()

    def select_mesh_event(self):

        mesh_list = self.get_mesh_list()
        mesh_list = [mesh for mesh in mesh_list if cmds.objExists(mesh)]

        if mesh_list:
            cmds.select(mesh_list)

    def add_mesh_event(self):

        selected = cmds.ls(sl=True, l=True)
        if not selected:
            return

        mesh_list = self.get_mesh_list()
        for sel in selected:
            if sel not in mesh_list:
                self.rpt_mesh_list_widget.addItem(sel)

    def del_mesh_event(self):

        select_items = self.rpt_mesh_list_widget.selectedItems()
        for select_item in select_items:
            model_index = self.rpt_mesh_list_widget.indexFromItem(select_item)
            self.rpt_mesh_list_widget.takeItem(model_index.row())
