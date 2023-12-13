# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from importlib import reload
except Exception:
    pass

import maya.api.OpenMaya as om

from PySide2 import QtCore, QtGui, QtWidgets
from maya.app.general import mayaMixin

from .ui import glp_lightmap_maker_window_pyside2 as ui_window
from .ui import textures_bake_setting_widget_pyside2 as ui_tb_setting
from .ui import vertices_bake_setting_widget_pyside2 as ui_vb_setting

reload(ui_window)
reload(ui_tb_setting)
reload(ui_vb_setting)


class View(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    """GUI用
    イベントの追加

    Args:
        QMainWindow ([type]): [description]
    """

    def __init__(self, parent=None):

        super(View, self).__init__(parent)
        self.ui = ui_window.Ui_MainWindow()
        self.ui.setupUi(self)

        self.callback_id_list = []

    def closeEvent(self, event):
        """_summary_

        Args:
            event (_type_): _description_
        """

        super(View, self).closeEvent(event)

        if self.callback_id_list:
            om.MMessage.removeCallbacks(self.callback_id_list)

        self.callback_id_list = []

    def addCallback(self, event_str, func):
        """_summary_

        Args:
            event_str (_type_): _description_
            func (_type_): _description_
        """

        self.callback_id_list.append(om.MEventMessage.addEventCallback(event_str, func))


class TextureSettingWidget(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QWidget):
    """GUI用
    イベントの追加

    Args:
        QMainWindow ([type]): [description]
    """

    def __init__(self, parent=None):

        super(TextureSettingWidget, self).__init__(parent)
        self.ui = ui_tb_setting.Ui_Form()
        self.ui.setupUi(self)

        self.ui.tex_x_line.setValidator(QtGui.QIntValidator())
        self.ui.tex_x_line.validator().setBottom(1)
        self.ui.test_tex_x_line.setValidator(QtGui.QIntValidator())
        self.ui.test_tex_x_line.validator().setBottom(1)
        self.ui.tex_y_line.setValidator(QtGui.QIntValidator())
        self.ui.tex_y_line.validator().setBottom(1)
        self.ui.test_tex_y_line.setValidator(QtGui.QIntValidator())
        self.ui.test_tex_y_line.validator().setBottom(1)


class VerticesSettingWidget(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QWidget):
    """GUI用
    イベントの追加

    Args:
        QMainWindow ([type]): [description]
    """

    def __init__(self, parent=None):

        super(VerticesSettingWidget, self).__init__(parent)
        self.ui = ui_vb_setting.Ui_Form()
        self.ui.setupUi(self)

        self.ui.ray_min_line.setValidator(QtGui.QIntValidator())
        self.ui.ray_min_line.validator().setBottom(1)
        self.ui.test_ray_min_line.setValidator(QtGui.QIntValidator())
        self.ui.test_ray_min_line.validator().setBottom(1)
        self.ui.ray_max_line.setValidator(QtGui.QIntValidator())
        self.ui.ray_max_line.validator().setBottom(1)
        self.ui.test_ray_max_line.setValidator(QtGui.QIntValidator())
        self.ui.test_ray_max_line.validator().setBottom(1)
