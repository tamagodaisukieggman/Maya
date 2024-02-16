# -*- coding=utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import

import sys
import os
import functools
from importlib import reload

from maya import OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
import shiboken2

# https://github.com/mottosso/Qt.py
from Qt import QtCore
from Qt import QtWidgets
from Qt import QtCompat
from Qt import QtGui

from . import material
from . import config
from . import utility
reload(material)
reload(config)
reload(utility)

MyWindow = None


class PhysicalMaterialWindow(MayaQWidgetBaseMixin, QtWidgets.QWidget):

    def __init__(self, parent=None, *args, **kwargs):
        super(PhysicalMaterialWindow, self).__init__(parent, *args, **kwargs)

        self._title = 'Collision Material Assign Tool'
        self._config = None
        self._srgb = utility.is_srgb()

        ui_file = os.path.join(os.path.split(__file__)[0], 'editor.ui')
        self.ui = QtCompat.loadUi(uifile=ui_file)

        # GUI ....

        self.ui.setParent(parent)
        self.ui.setWindowFlags(QtCore.Qt.Dialog)
        self.ui.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)

        self.ui.setWindowTitle(self._title.title())
        self.ui.setObjectName(self._title.title().replace(' ', ''))

        self.ui.resize(300, 450)
        self.ui.frameGeometry().moveCenter(QtWidgets.QDesktopWidget().availableGeometry().center())

        self.ui.sRGBCheckBox.setChecked(self._srgb)

        self.ui.sRGBCheckBox.clicked.connect(functools.partial(self.rebuild_widgets))

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, config):
        self._config = config

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, python_class):
        self._action = python_class

    @staticmethod
    def liner_to_srgb(liner):
        return [pow(*data) for data in zip(liner, [1 / 2.2] * 3)]

    @staticmethod
    def srgb_to_liner(srgb):
        return [pow(*data) for data in zip(srgb, [2.2] * 3)]

    @staticmethod
    def to_display_color_space(color_value):
        return utility.convert_color(color=color_value)

    def show(self):
        self.ui.show()

    def build_widgets(self):
        self.ui.ScrollAreaWidget.deleteLater()

        self.ui.ScrollAreaWidget = QtWidgets.QWidget()
        self.ui.ScrollAreaWidget.setObjectName("ScrollAreaWidget")
        self.ui.ScrollArea.setWidget(self.ui.ScrollAreaWidget)

        self.ui.scrollarea_vertical_layout = QtWidgets.QVBoxLayout(self.ui.ScrollAreaWidget)
        self.ui.scrollarea_vertical_layout.setObjectName("ScrollAreaVerticalLayout")

        for config in self._config:

            hbox_layout = QtWidgets.QHBoxLayout(self.ui.ScrollAreaWidget)
            hbox_layout.setObjectName('QHBoxLayout')
            self.ui.scrollarea_vertical_layout.addLayout(hbox_layout)

            color_frame = QtWidgets.QFrame(self.ui.ScrollAreaWidget)
            color_frame.setObjectName('ColorFrame')
            color_frame.setAutoFillBackground(True)

            size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
            size_policy.setHorizontalStretch(0)
            size_policy.setVerticalStretch(0)
            size_policy.setHeightForWidth(color_frame.sizePolicy().hasHeightForWidth())
            color_frame.setSizePolicy(size_policy)
            color_frame.setFrameShadow(QtWidgets.QFrame.Raised)
            color_frame.setMinimumSize(QtCore.QSize(25, 0))

            p = color_frame.palette()

            color = self.to_display_color_space(config['color'])
            p.setColor(color_frame.backgroundRole(), QtGui.QColor.fromRgbF(*color))
            color_frame.setPalette(p)

            hbox_layout.addWidget(color_frame)

            material_label = QtWidgets.QLabel(self.ui.ScrollAreaWidget)
            material_label.setObjectName('MaterialLabel_{}'.format(config['name'].title()))
            material_label.setText('{}'.format(config['label']))
            hbox_layout.addWidget(material_label)

            select_push_button = QtWidgets.QPushButton(self.ui.ScrollAreaWidget)
            select_push_button.setObjectName("SelectPushButton")
            select_push_button.setText('Select')
            hbox_layout.addWidget(select_push_button)

            select_push_button.clicked.connect(functools.partial(self.select, config['name']))

            appy_push_button = QtWidgets.QPushButton(self.ui.ScrollAreaWidget)
            appy_push_button.setObjectName("AssignPushButton")
            appy_push_button.setText('Assign')
            hbox_layout.addWidget(appy_push_button)

            appy_push_button.clicked.connect(functools.partial(self.assign, config['name']))

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.ui.scrollarea_vertical_layout.addItem(spacerItem)

    @QtCore.Slot()
    def rebuild_widgets(self):
        self._srgb = self.ui.sRGBCheckBox.isChecked()

        if self._srgb:
            utility.set_color_space(color_space='sRGB gamma')
        else:
            utility.set_color_space(color_space='Raw')

        self.build_widgets()

    @QtCore.Slot()
    def select(self, name=''):
        # メッシュ名で選択
        self._action.select(name=name)  # PhysicalMaterial.select

    @QtCore.Slot()
    def assign(self, name=''):
        self._action.assign(name=name)  # PhysicalMaterial.assign


def run():

    global MyWindow

    try:
        configs = config.read()
        phymtl = material.PhysicalMaterial()
        phymtl.config = configs

        maya_window = omui.MQtUtil.mainWindow()
        if maya_window is not None:
            maya_window = shiboken2.wrapInstance(int(maya_window), QtWidgets.QMainWindow)
            for child in maya_window.children():
                if 'CollisionMaterialAssignTool' in child.objectName():
                    child.close()

        MyWindow = PhysicalMaterialWindow(parent=maya_window)
        MyWindow.config = configs
        MyWindow.action = phymtl

        MyWindow.build_widgets()
        MyWindow.show()

    except Exception as err:
        print(err)

    else:
        return MyWindow


if __name__ == '__main__':
    pass
