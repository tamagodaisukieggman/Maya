# -*- coding: utf-8 -*-
"""MVCでいうViewを担う
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import maya.cmds as cmds

from PySide2 import QtWidgets
from . import base_widget


class TransformFromAngeleWidget(base_widget.BaseWidget):

    def __init__(self, parent, param_data_template):
        super(TransformFromAngeleWidget, self).__init__(parent, param_data_template)

        self.value_factor = 10000

        self.target_line = None
        self.ref_line = None
        self.ref_axis_combo = None
        self.ref_min_spin = None
        self.ref_max_spin = None
        self.trans_type_combo = None
        self.value_x_spin = None
        self.value_y_spin = None
        self.value_z_spin = None

    def create_widget(self):
        """ウィジェットの作成
        """

        # 対象Tp
        lable = QtWidgets.QLabel('対象骨')
        self.target_line = QtWidgets.QLineEdit()
        self.target_line.textEdited.connect(self.__value_change_event)
        target_sel_button = QtWidgets.QPushButton('選択')
        target_sel_button.clicked.connect(self.__target_select_event)
        target_set_button = QtWidgets.QPushButton('セット')
        target_set_button.clicked.connect(self.__target_set_event)

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(lable)
        layout.addWidget(self.target_line)
        layout.addWidget(target_sel_button)
        layout.addWidget(target_set_button)

        self.main_layout.addLayout(layout)

        # reference
        lable = QtWidgets.QLabel('参照骨')
        self.ref_line = QtWidgets.QLineEdit()
        self.ref_line.textEdited.connect(self.__value_change_event)
        ref_sel_button = QtWidgets.QPushButton('選択')
        ref_sel_button.clicked.connect(self.__ref_select_event)
        ref_set_button = QtWidgets.QPushButton('セット')
        ref_set_button.clicked.connect(self.__ref_set_event)

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(lable)
        layout.addWidget(self.ref_line)
        layout.addWidget(ref_sel_button)
        layout.addWidget(ref_set_button)

        self.main_layout.addLayout(layout)

        # ref axis
        lable = QtWidgets.QLabel('参照する軸')
        self.ref_axis_combo = QtWidgets.QComboBox()
        self.ref_axis_combo.wheelEvent = lambda event: None
        self.ref_axis_combo.addItems(['x', 'y', 'z'])
        self.ref_axis_combo.currentIndexChanged.connect(self.__value_change_event)

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(lable)
        layout.addWidget(self.ref_axis_combo)

        self.main_layout.addLayout(layout)

        # 参照軸最小値
        lable = QtWidgets.QLabel('Min')
        self.ref_min_spin = QtWidgets.QSpinBox()
        self.ref_min_spin.wheelEvent = lambda event: None
        self.ref_min_spin.setRange(-180 * self.value_factor, 180 * self.value_factor)
        self.ref_min_spin.valueChanged.connect(self.__value_change_event)

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(lable)
        layout.addWidget(self.ref_min_spin)

        self.main_layout.addLayout(layout)

        # 参照軸最大値
        lable = QtWidgets.QLabel('Max')
        self.ref_max_spin = QtWidgets.QSpinBox()
        self.ref_max_spin.wheelEvent = lambda event: None
        self.ref_max_spin.setRange(-180 * self.value_factor, 180 * self.value_factor)
        self.ref_max_spin.valueChanged.connect(self.__value_change_event)

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(lable)
        layout.addWidget(self.ref_max_spin)

        self.main_layout.addLayout(layout)

        # Tpの反応タイプ
        lable = QtWidgets.QLabel('タイプ')
        self.trans_type_combo = QtWidgets.QComboBox()
        self.trans_type_combo.wheelEvent = lambda event: None
        self.trans_type_combo.addItems(['Position', 'Rotate', 'Scale'])
        self.trans_type_combo.currentIndexChanged.connect(self.__value_change_event)

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(lable)
        layout.addWidget(self.trans_type_combo)

        self.main_layout.addLayout(layout)

        # Tp_x
        lable = QtWidgets.QLabel('X')
        self.value_x_spin = QtWidgets.QSpinBox()
        self.value_x_spin.wheelEvent = lambda event: None
        self.value_x_spin.setRange(-1000 * self.value_factor, 1000 * self.value_factor)
        self.value_x_spin.valueChanged.connect(self.__value_change_event)

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(lable)
        layout.addWidget(self.value_x_spin)

        self.main_layout.addLayout(layout)

        # Tp_y
        lable = QtWidgets.QLabel('Y')
        self.value_y_spin = QtWidgets.QSpinBox()
        self.value_y_spin.wheelEvent = lambda event: None
        self.value_y_spin.setRange(-1000 * self.value_factor, 1000 * self.value_factor)
        self.value_y_spin.valueChanged.connect(self.__value_change_event)

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(lable)
        layout.addWidget(self.value_y_spin)

        self.main_layout.addLayout(layout)

        # Tp_z
        lable = QtWidgets.QLabel('Z')
        self.value_z_spin = QtWidgets.QSpinBox()
        self.value_z_spin.wheelEvent = lambda event: None
        self.value_z_spin.setRange(-1000 * self.value_factor, 1000 * self.value_factor)
        self.value_z_spin.valueChanged.connect(self.__value_change_event)

        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(lable)
        layout.addWidget(self.value_z_spin)

        self.main_layout.addLayout(layout)

    def get_target_data(self):
        """UIからプロセスの制御対象となるノードとアトリビュートリストを取得

        Returns:
            str: ノード
            list: アトリビュートリスト
        """

        # Unityコンポーネントに合わせたラベル名からアトリビュート名に変換
        target = self.target_line.text()
        type_text = self.trans_type_combo.currentText()
        attr = ''
        if type_text == 'Position':
            attr = 'translate'
        elif type_text == 'Rotate':
            attr = 'rotate'
        elif type_text == 'Scale':
            attr = 'scale'
        return target, [attr + 'X', attr + 'Y', attr + 'Z']

    def get_param_data(self):
        """UIからプロセスで使用するパラメーターを取得

        Returns:
            dict: プロセスで使用されるパラメーターdict. {attr_name: {'type': type, 'value': value},,,}
        """

        data = {}

        for key, value in self.param_data_template.items():

            if key == 'reference':
                this_data = value.copy()
                this_data.update({'value': self.ref_line.text()})
                data[key] = this_data

            elif key == 'referenceAxis':
                this_data = value.copy()
                this_data.update({'value': self.ref_axis_combo.currentText()})
                data[key] = this_data

            elif key == 'refMin':
                this_data = value.copy()
                this_data.update({'value': self.ref_min_spin.value()})
                data[key] = this_data

            elif key == 'refMax':
                this_data = value.copy()
                this_data.update({'value': self.ref_max_spin.value()})
                data[key] = this_data

            elif key == 'transformType':
                this_data = value.copy()
                this_data.update({'value': self.trans_type_combo.currentText()})
                data[key] = this_data

            elif key == 'valueX':
                this_data = value.copy()
                this_data.update({'value': self.value_x_spin.value()})
                data[key] = this_data

            elif key == 'valueY':
                this_data = value.copy()
                this_data.update({'value': self.value_y_spin.value()})
                data[key] = this_data

            elif key == 'valueZ':
                this_data = value.copy()
                this_data.update({'value': self.value_z_spin.value()})
                data[key] = this_data

        return data

    def import_param_data(self, target, param_data):
        """パラメーター情報の読み込み

        Args:
            target (str): ターゲットノード
            param_data (dict): プロセスで使用されるパラメーターdict. {attr_name: {'type': type, 'value': value},,,}
        """

        self.target_line.setText(target)

        for key, value in param_data.items():

            if key == 'target':
                self.target_line.setText(value.get('value', ''))

            elif key == 'reference':
                self.ref_line.setText(value.get('value', ''))

            elif key == 'referenceAxis':
                index = self.ref_axis_combo.findText(value.get('value', 0))
                if index >= 0:
                    self.ref_axis_combo.setCurrentIndex(index)

            elif key == 'refMin':
                self.ref_min_spin.setValue(value.get('value', 0))

            elif key == 'refMax':
                self.ref_max_spin.setValue(value.get('value', 0))

            elif key == 'transformType':
                index = self.trans_type_combo.findText(value.get('value', 0))
                if index >= 0:
                    self.trans_type_combo.setCurrentIndex(index)

            elif key == 'valueX':
                self.value_x_spin.setValue(value.get('value', 0))

            elif key == 'valueY':
                self.value_y_spin.setValue(value.get('value', 0))

            elif key == 'valueZ':
                self.value_z_spin.setValue(value.get('value', 0))

    def __target_set_event(self):
        """ターゲットセットイベント
        """

        sels = cmds.ls(sl=True, typ='transform')

        if sels:
            self.target_line.setText(sels[0])
            self.expression_edit.emit(self)

    def __target_select_event(self):
        """ターゲット選択イベント
        """

        target = self.target_line.text()
        if cmds.objExists(target):
            cmds.select(target, r=True)

    def __ref_set_event(self):
        """リファレンスセットイベント
        """

        sels = cmds.ls(sl=True, typ='transform')

        if sels:
            self.ref_line.setText(sels[0])
            self.expression_edit.emit(self)

    def __ref_select_event(self):
        """ターゲット選択イベント
        """

        target = self.ref_line.text()
        if cmds.objExists(target):
            cmds.select(target, r=True)

    def __value_change_event(self):
        """パラメーター変更時イベント
        """

        self.expression_edit.emit(self)
