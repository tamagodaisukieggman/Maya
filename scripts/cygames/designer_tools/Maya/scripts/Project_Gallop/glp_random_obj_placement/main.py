# -*- coding: utf-8 -*-
"""MVCでいうControllerを担う
"""
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

import sys

from PySide2 import QtWidgets
from maya import OpenMayaUI

from . import view
from . import placement_objs

import maya.cmds as cmds
import shiboken2

# for maya2022-
try:
    from builtins import str
    from importlib import reload
except Exception:
    pass

reload(view)
reload(placement_objs)


class Main(object):

    def __init__(self):
        """コンストラクタ
        """

        self.view = view.View()
        self.placement_objs = placement_objs.PlacementObjs()

        self.obj_count = 0
        self.target_obj_layout_list = []

        self.placement_value_info = None

    def deleteOverlappingWindow(self, target):
        """Windowの重複削除処理
        """

        main_window = OpenMayaUI.MQtUtil.mainWindow()
        if main_window is None:
            return

        if sys.version_info.major == 2:
            main_window = shiboken2.wrapInstance(long(main_window), QtWidgets.QMainWindow)
        else:
            # for Maya 2022-
            main_window = shiboken2.wrapInstance(int(main_window), QtWidgets.QMainWindow)

        for widget in main_window.children():
            if str(type(target)) == str(type(widget)):
                widget.deleteLater()

    def show_ui(self):
        """UI描画
        """

        # windowの重複削除処理
        self.deleteOverlappingWindow(self.view)

        self.setup_view_event()
        self.view.show()

        self.placement_value_info = PlacementValueInfo()
        self.set_value_to_placement_value_info()

    def setup_view_event(self):
        """UIのevent設定
        """

        # ランダム配置ベースオブジェクト設定
        self.view.ui.setObjNameListButton.clicked.connect(
            lambda: self.clicked_list_widget_add_button(self.view.ui.baseObjNameListWidget)
        )
        self.view.ui.removeObjNameListButton.clicked.connect(
            lambda: self.clicked_list_widget_remove_button(self.view.ui.baseObjNameListWidget)
        )

        # ルックターゲット設定
        self.view.ui.lookTargetSetButton.clicked.connect(
            lambda: self.clicked_line_edit_set_button(self.view.ui.lookTargetLineEdit_2)
        )
        self.view.ui.lookTargetClearButton.clicked.connect(
            lambda: self.clicked_line_edit_clear_button(self.view.ui.lookTargetLineEdit_2)
        )

        # ランダム配置対象オブジェクト設定
        # リスト追加ボタン
        self.view.ui.randObjPlacementAddListButton.clicked.connect(
            self.clicked_add_object_to_list_button_event)

        self.view.ui.randObjPlacementResetListButton.clicked.connect(
            self.clicked_reset_object_to_list_button_event
        )

        # 中心オブジェクト設定
        # セット
        self.view.ui.centerObjNameSetButton.clicked.connect(
            lambda: self.clicked_line_edit_set_button(self.view.ui.centerObjNameLineEdit))
        # クリア
        self.view.ui.centerObjNameClearButton.clicked.connect(
            lambda: self.clicked_line_edit_clear_button(self.view.ui.centerObjNameLineEdit))

        # ランダム配置実行ボタン
        self.view.ui.placementRandomButton.clicked.connect(
            self.clicked_placementRandomButton_event)

    def clicked_add_object_to_list_button_event(self):
        """「選択中のオブジェクトをリストに追加」ボタンを押したときの挙動
        """

        sels = cmds.ls(sl=True, l=True)

        target_object_list = [target_object_layout.target_obj for target_object_layout in self.target_obj_layout_list]
        base_mesh_name_list = self.get_list_widget_item_text_list(self.view.ui.baseObjNameListWidget)

        for sel in sels:

            if sel in target_object_list + base_mesh_name_list:
                continue

            tmp_box_layout = TargetObjectLayoutWidget(self, sel)
            self.target_obj_layout_list.append(tmp_box_layout)
            self.view.ui.randObjPlacementListLayout.insertLayout(
                self.view.ui.randObjPlacementListLayout.count() - 1, tmp_box_layout)

        # オブジェクト数再計算
        self.change_object_count()

    def clicked_reset_object_to_list_button_event(self):
        """「選択中のオブジェクトをリストに追加」のクリアボタンを押したときの挙動
        """

        self.target_obj_layout_list = []

        del_item = []
        for i in range(self.view.ui.randObjPlacementListLayout.count() - 1):
            widget = self.view.ui.randObjPlacementListLayout.itemAt(i)
            del_item.append(widget)

        for item in del_item:
            item.del_widget()

        # オブジェクト数再計算
        self.change_object_count()

    def clicked_placementRandomButton_event(self):
        """「ランダム配置」ボタンを押したときの挙動
        """

        # UIから値取得
        self.set_value_to_placement_value_info()

        if self.obj_count <= 0:
            cmds.warning('対象のオブジェクトがありません')
            return

        for target_obj_layout in self.target_obj_layout_list:
            # 現在シーン上にランダム配置対象が存在しない場合は処理しない
            if not cmds.objExists(target_obj_layout.target_obj):
                cmds.warning('ランダム配置対象のオブジェクトが存在しません。')
                return

        # ベースオブジェクト
        if not self.placement_value_info.base_mesh_list:
            cmds.warning('ベースオブジェクトが設定されていません。')
            return

        if self.placement_value_info.obj_placement_method == 'look_at_target':
            if not self.view.ui.lookTargetLineEdit_2.text() or not cmds.objExists(self.view.ui.lookTargetLineEdit_2.text()):
                cmds.warning('Z方向を向けるターゲットが存在しません。')
                return

        self.placement_objs.placement_objs_at_random_based_on_mesh(
            self.placement_value_info, self.target_obj_layout_list
        )

    def clicked_list_widget_add_button(self, list_widget):
        """[summary]
        """

        sels = cmds.ls(sl=True, l=True)
        if not sels:
            return

        for sel in sels:
            for item_text in self.get_list_widget_item_text_list(list_widget):
                if sel == item_text:
                    break
            else:
                list_widget.addItem(sel)

    def clicked_list_widget_remove_button(self, list_widget):
        """[summary]
        """

        select_items = list_widget.selectedItems()
        for select_item in select_items:
            model_index = list_widget.indexFromItem(select_item)
            list_widget.takeItem(model_index.row())

    def clicked_line_edit_set_button(self, line_edit):
        """「セット」ボタンを押したときの処理 対象のlineEditに選択中のオブジェクト名をセット
        """

        sels = cmds.ls(sl=True)
        if not sels:
            return

        line_edit.setText(sels[0])

    def clicked_line_edit_clear_button(self, line_edit):
        """「クリア」ボタンを押したときの処理 対象のlineEditに空文字をセットする

        Args:
            line_edit ()
        """

        line_edit.setText("")

    def change_object_count(self):
        """保存している現在のオブジェクト数を変更する
        """

        tmp_obj_count = 0
        for target_object_layout in self.target_obj_layout_list:
            tmp_obj_count += target_object_layout.get_value()

        self.obj_count = tmp_obj_count
        self.view.ui.randObjPlacementNumLabel.setText('現在のオブジェクト数：{}'.format(str(self.obj_count)))

    def delete_target_object_layout(self, value):
        """対象のランダム配置対象オブジェクトを削除する

        Args:
            value(TargetObjectLayoutWidget): 削除対象のWidget
        """

        if value in self.target_obj_layout_list:
            self.target_obj_layout_list.remove(value)

    def get_list_widget_item_text_list(self, list_widget):

        item_text_list = []
        for i in range(list_widget.count()):
            item_text_list.append(list_widget.item(i).text())

        return item_text_list

    def set_value_to_placement_value_info(self):
        """[summary]

        Returns:
            [type]: [description]
        """

        self.placement_value_info.reset_value()

        self.placement_value_info.base_mesh_list = []
        for i in range(self.view.ui.baseObjNameListWidget.count()):
            self.placement_value_info.base_mesh_list.append(self.view.ui.baseObjNameListWidget.item(i).text())

        self.placement_value_info.obj_distance = self.view.ui.objDistanceSpinBox.value()
        self.placement_value_info.obj_placement_method = 'default'
        if self.view.ui.placementSettingRadioButton2.isChecked():
            self.placement_value_info.obj_placement_method = 'face_normal'

        if self.view.ui.setRotationRadioButton_2.isChecked():
            self.placement_value_info.obj_placement_method = 'set_rotate'
            self.placement_value_info.rotate_option_x = self.view.ui.rotateXSpinBox.value()
            self.placement_value_info.rotate_option_y = self.view.ui.rotateYSpinBox.value()
            self.placement_value_info.rotate_option_z = self.view.ui.rotateZSpinBox.value()

        if self.view.ui.setLookTargetRadioButton_2.isChecked():
            self.placement_value_info.obj_placement_method = 'look_at_target'
            if self.view.ui.lookTargetLineEdit_2.text():
                self.placement_value_info.look_at_target = self.view.ui.lookTargetLineEdit_2.text()

        # 中心オブジェクト設定のに値が入っていたら設定する
        if self.view.ui.centerObjNameLineEdit.text():
            self.placement_value_info.avoidance_obj_list = [self.view.ui.centerObjNameLineEdit.text()]
            self.placement_value_info.avoidance_distance_list = [self.view.ui.centerObjDistanceSpinBox.value()]

        # 高さ
        if self.view.ui.randSettingHeightCheckBox.isChecked():
            self.placement_value_info.rand_min_height = self.view.ui.randSettingHeightMinValueSpinBox.value()
            self.placement_value_info.rand_max_height = self.view.ui.randSettingHeightMaxValueSpinBox.value()

        # rotateX
        if self.view.ui.randSettingRotateXCheckBox.isChecked():
            self.placement_value_info.rand_min_rotate_x = self.view.ui.randSettingRotateXMinValueSpinBox.value()
            self.placement_value_info.rand_max_rotate_x = self.view.ui.randSettingRotateXMaxValueSpinBox.value()

        # rotateY
        if self.view.ui.randSettingRotateYCheckBox.isChecked():
            self.placement_value_info.rand_min_rotate_y = self.view.ui.randSettingRotateYMinValueSpinBox.value()
            self.placement_value_info.rand_max_rotate_y = self.view.ui.randSettingRotateYMaxValueSpinBox.value()

        # rotateZ
        if self.view.ui.randSettingRotateZCheckBox.isChecked():
            self.placement_value_info.rand_min_rotate_z = self.view.ui.randSettingRotateZMinValueSpinBox.value()
            self.placement_value_info.rand_max_rotate_z = self.view.ui.randSettingRotateZMaxValueSpinBox.value()


class PlacementValueInfo(object):

    def __init__(self):
        """
        """

        self.reset_value()

    def reset_value(self):
        """
        """

        self.base_mesh_list = []
        self.obj_distance = 0.0
        self.obj_placement_method = 'default'

        self.rotate_option_x = 0.0
        self.rotate_option_y = 0.0
        self.rotate_option_z = 0.0

        self.look_at_target = ''

        self.avoidance_obj_list = []
        self.avoidance_distance_list = []

        self.rand_min_height = 0.0
        self.rand_max_height = 0.0
        self.rand_min_rotate_x = 0.0
        self.rand_min_rotate_y = 0.0
        self.rand_min_rotate_z = 0.0
        self.rand_max_rotate_x = 0.0
        self.rand_max_rotate_y = 0.0
        self.rand_max_rotate_z = 0.0


class TargetObjectLayoutWidget(QtWidgets.QHBoxLayout):
    """
    """

    def __init__(self, main, target_obj, parent=None):

        super(TargetObjectLayoutWidget, self).__init__(parent)

        self.main = main
        self.target_obj = target_obj
        self.spin_box = None
        self.delete_button = None

        self.set_ui()

    def set_ui(self):

        label = QtWidgets.QLabel()
        label.setObjectName(self.target_obj)
        label.setText(self.target_obj)

        self.spin_box = QtWidgets.QSpinBox()
        self.spin_box.setObjectName("spinBox")
        self.spin_box.valueChanged.connect(self._valueChanged_spin_box_event)
        self.spin_box.setValue(1)
        self.spin_box.setMinimum(0.0)
        self.spin_box.setMaximum(100000.0)

        self.delete_button = QtWidgets.QPushButton()
        self.delete_button.setObjectName("pushButton2")
        self.delete_button.clicked.connect(self._clicked_delete_button_event)
        self.delete_button.setText("削除")

        self.addWidget(label)
        self.addWidget(self.spin_box)
        self.addWidget(self.delete_button)

        self.setStretch(0, 4)
        self.setStretch(1, 1)
        self.setStretch(2, 1)

    def get_value(self):
        """
        """

        return self.spin_box.value()

    def del_widget(self):
        """
        このwidgetを削除する。
        """

        for i in range(self.count()):
            b = self.itemAt(i)
            wid = b.widget()
            if wid:
                wid.deleteLater()

        self.deleteLater()

    def _clicked_delete_button_event(self):
        """
        """

        self.del_widget()

        self.main.delete_target_object_layout(self)
        self.main.change_object_count()

    def _valueChanged_spin_box_event(self):
        """
        """

        self.main.change_object_count()
