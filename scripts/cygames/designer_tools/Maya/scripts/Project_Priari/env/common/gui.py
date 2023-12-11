# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

try:
    # Maya 2022-
    from builtins import range
    from importlib import reload
except:
    pass

from maya.app.general import mayaMixin

from PySide2 import QtCore, QtGui, QtWidgets

from . import command
from . import model_widget_pyside2
from . import scene_widget_pyside2

reload(command)
reload(model_widget_pyside2)
reload(scene_widget_pyside2)

MIN_SIZE = QtCore.QSize(0, 0)
MAX_SIZE = QtCore.QSize(16777215, 16777215)


class ModelWidget(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(ModelWidget, self).__init__(*args, **kwargs)

        self.ui = model_widget_pyside2.Ui_Form()
        self.ui.setupUi(self)

    def paintEvent(self, *args, **kwargs):
        option = QtWidgets.QStyleOption()
        option.init(self)
        painter = QtGui.QPainter(self)
        self.style().drawPrimitive(
            QtWidgets.QStyle.PE_Widget, option, painter, self)

    def update(self, target_node, scene_path, show_path=True):
        info = command.get_face_info(target_node)
        path = command.get_fbx_path(scene_path, target_node)

        self.ui.NameLabel.setText(target_node)
        self.ui.InfoLabel.setText(info.get_text())
        self.ui.PathLabel.setText(u'出力ファイル: {}'.format(path))

        size = MAX_SIZE if show_path else MIN_SIZE
        self.ui.PathLabel.setMaximumSize(size)

    def get_enabled(self):
        return self.ui.Enabled.isChecked()


class SceneWidget(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(SceneWidget, self).__init__(*args, **kwargs)

        self.ui = scene_widget_pyside2.Ui_Form()
        self.ui.setupUi(self)

    def update(self, scene_path, show_path=True):
        name = command.get_scene_name(scene_path, show_path)

        self.ui.NameLabel.setText(name)
        self.ui.PathLabel.setText(scene_path)

        size = MAX_SIZE if show_path else MIN_SIZE
        self.ui.PathWidget.setMaximumSize(size)

        for model in self.get_models():
            model.hide()
            model.deleteLater()

        for node in command.get_models():
            self.add_model(node, scene_path, show_path)

    def add_model(self, target_node, scene_path, show_path):
        widget = ModelWidget()
        widget.update(target_node, scene_path, show_path)
        layout = self.ui.MainLayout
        layout.insertWidget(layout.count() - 1, widget)

    def get_models(self):
        layout = self.ui.MainLayout
        models = [layout.itemAt(i).widget() for i in range(layout.count())]
        return [model for model in models if model]

    def get_enabled_models(self):
        return [model for model in self.get_models() if model.get_enabled()]
