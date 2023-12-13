# -*- coding: utf-8 -*-
from __future__ import annotations

import sys
import typing as tp


def wrapping_pyside6():
    """PySide6をPySide2でwrappingする。
    """
    import sys

    import PySide2
    from PySide2 import QtCore, QtGui, QtWidgets, support

    # from PySide2.QtWidgets import QAction
    # from PySide2.QtWidgets import QMenu
    # from PySide6.QtGui import QAction
    sys.modules["PySide6"] = PySide2
    sys.modules["PySide6.QtWidgets"] = QtWidgets
    sys.modules["PySide6.QtCore"] = QtCore
    sys.modules["PySide6.QtGui"] = QtGui
    sys.modules["PySide6.support"] = support
    PySide2.QtGui.QAction = QtWidgets.QAction
    PySide2.QtGui.QMouseEvent.position = PySide2.QtGui.QMouseEvent.localPos


wrapping_pyside6()


def main():
    # reset("mtk.cutscene")
    from . import controller
    _controller = controller.SequencerController.get_instance()
    _controller.clear_model()
    _controller.show()

    return _controller


# def reset(package_name):
#     # TODO: 現在リセット関数がないので、Reloadして強引に中身を削除する。
#     # 読み取り/保存に対応する。

#     name = package_name
#     module_list = [_ for _ in sys.modules]
#     module_list.sort()

#     for k in module_list:
#         if k.startswith(name):
#             del sys.modules[k]
