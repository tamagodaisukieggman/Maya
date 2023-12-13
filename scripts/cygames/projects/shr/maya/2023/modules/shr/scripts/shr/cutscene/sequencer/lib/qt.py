from __future__ import annotations

import typing as tp
from abc import abstractmethod

import maya.OpenMayaUI as omui
from maya import cmds
from maya.app.general.mayaMixin import (MayaQWidgetBaseMixin,
                                        MayaQWidgetDockableMixin)
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget
from shiboken2 import wrapInstance


class MayaMainWindowBase(MayaQWidgetBaseMixin, QMainWindow):
    @staticmethod
    def get_maya_window() -> QWidget:
        ptr = omui.MQtUtil.mainWindow()
        return wrapInstance(int(ptr), QWidget)

    @property
    def abolute_name(self) -> str:
        """絶対名
        """
        return f"{self.__module__}.{self.__class__.__name__}"

    def __init__(self):
        maya_window = MayaMainWindowBase.get_maya_window()

        for child in maya_window.children():
            child_name = child.objectName()
            if child_name == self.abolute_name:
                child.close()

                # MayaQWidgetDockableMixinの時
                # workspace周りが複雑なので、一時dockableはなし
                # workspace_name = self.objectName() + 'WorkspaceControl'
                # if cmds.workspaceControl(workspace_name, exists=True):
                #     cmds.deleteUI(workspace_name)

        super().__init__(parent=maya_window)
        self.setObjectName(self.abolute_name)
        self.setWindowTitle(self.abolute_name)
        self.setAttribute(Qt.WA_DeleteOnClose)

    def setup_ui(self) -> MayaMainWindowBase:
        """UI構築
        """
        widget = self.centralWidget()
        if widget is not None:
            widget.deleteLater()

        widget = QWidget()

        self.setCentralWidget(widget)
        self.setup(widget)
        return self

    def closeEvent(self, _) -> None:
        self.shutdown()

    @abstractmethod
    def setup(self, central_widget) -> None:
        ...

    @abstractmethod
    def shutdown(self):
        ...


class MayaAppBase(object):
    def __init__(self):
        self._window: tp.Optional[MayaMainWindowBase] = None

    def execute(self):
        app = QApplication.instance()
        self.initialize(app)
        self._window = self.create_window()
        if self._window is not None:
            self._window.setup_ui()
            self.post_initialize()
            self._window.show()
            # self._window.setup_ui().show(dockable=True)

    @abstractmethod
    def initialize(self, app: QApplication) -> None:
        """初期化
        """
        ...

    @abstractmethod
    def create_window(self) -> MayaMainWindowBase:
        """Windows生成
        """
        ...

    @abstractmethod
    def post_initialize(self) -> None:
        ...
