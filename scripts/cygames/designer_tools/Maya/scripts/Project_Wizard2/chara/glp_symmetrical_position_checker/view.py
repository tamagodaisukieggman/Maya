# -*- coding: utf-8 -*-
"""MVCでいうViewを担う
"""
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

from PySide2 import QtCore, QtGui, QtWidgets
from maya.app.general import mayaMixin

from .ui import symmetricalPositionCheckerWindow


class View(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    """GUI用
    イベントの追加

    Args:
        QMainWindow ([type]): [description]
    """

    # ==================================================
    def __init__(self, *args, **kwargs):

        super(View, self).__init__(*args, **kwargs)
        self.ui = symmetricalPositionCheckerWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.setting = None

        # ボタングループがQtDesigner側では設定できない(出力不能になってしまう)問題があるためここで設定
        self.ui.baseAxisRadioGrp = QtWidgets.QButtonGroup()
        self.ui.baseAxisRadioGrp.addButton(self.ui.XAxisRadio, 0)
        self.ui.baseAxisRadioGrp.addButton(self.ui.YAxisRadio, 1)
        self.ui.baseAxisRadioGrp.addButton(self.ui.ZAxisRadio, 2)
        self.ui.baseAxisRadioGrp.button(0).setChecked(True)

    # ==================================================
    def collect_current_status(self):

        current_status_dict = {}

        if self.ui.XAxisRadio.isChecked():
            current_status_dict['current_axis'] = 'X'
        elif self.ui.YAxisRadio.isChecked():
            current_status_dict['current_axis'] = 'Y'
        else:
            current_status_dict['current_axis'] = 'Z'

        current_status_dict['position_tolerance'] = self.ui.posAllowranceBox.value()
        current_status_dict['window_pos'] = [self.pos().x(), self.pos().y()]
        current_status_dict['window_size'] = [self.size().width(), self.size().height()]

        return current_status_dict

    # ==================================================
    def save_setting(self):
        """
        設定を保存
        """
        if self.setting is None:
            return

        current_settings = self.collect_current_status()

        self.setting.save('window_width', current_settings['window_size'][0])
        self.setting.save('window_height', current_settings['window_size'][1])
        self.setting.save('window_left', current_settings['window_pos'][0])
        self.setting.save('window_top', current_settings['window_pos'][1])
        self.setting.save('current_axis', current_settings['current_axis'])

    # ==================================================
    def load_setting(self):
        """
        設定をロード
        """
        if self.setting is None:
            return

        this_width = self.setting.load('window_width', int)
        this_height = self.setting.load('window_height', int)
        this_left = self.setting.load('window_left', int)
        this_top = self.setting.load('window_top', int)

        if this_width is not None and this_height is not None:
            self.resize(this_width, this_height)
        if this_left is not None and this_top is not None:
            self.move(QtCore.QPoint(this_left, this_top))

        current_axis = self.setting.load('current_axis', str, 'X')
        if current_axis == 'X':
            self.ui.XAxisRadio.setChecked(True)
        elif current_axis == 'Y':
            self.ui.YAxisRadio.setChecked(True)
        else:
            self.ui.ZAxisRadio.setChecked(True)
