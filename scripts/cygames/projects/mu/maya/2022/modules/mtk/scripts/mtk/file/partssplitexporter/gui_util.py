# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from PySide2 import QtCore, QtGui, QtWidgets
import maya.cmds as cmds

from . import TITLE

class ProgressWindowBlock(object):
    """ProgressWindowを表示させるコンテキストマネージャー
    """

    def __init__(self, title='', progress=0,  minValue=0, maxValue=100, isInterruptable=True, show_progress=True):
        self._show_progress = show_progress and (not cmds.about(q=True, batch=True))

        self.title = title
        self.progress = progress
        self.minValue = minValue
        self.maxValue = maxValue
        self.isInterruptable = isInterruptable

        self._start_time = None
        self.status = None

    def __enter__(self):
        # logger.info('[ {} ] : Start'.format(self.title))

        if self._show_progress:
            cmds.progressWindow(
                title=self.title,
                progress=int(self.progress),
                status='[ {} ] : Start'.format(self.title),
                isInterruptable=self.isInterruptable,
                min=self.minValue,
                max=self.maxValue + 1
            )

        # self._start_time = datetime.datetime.now()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # logger.info('[ {} ] : End : Calculation time : {}'.format(self.title, calc_time))

        if self._show_progress:
            cmds.progressWindow(ep=1)

    def step(self, step):
        if self._show_progress:
            cmds.progressWindow(e=True, step=step)
            # cmds.progressWindow(e=True,
            #         status='[ {} / {} ] : {}'.format(self.progress, self.maxValue, self.status))

    def _set_status(self, status):
        if self._show_progress:
            # self.status = status
            cmds.progressWindow(e=True,
                    status='[ {} / {} ] : {}'.format(self.progress, self.maxValue, status))

    def _get_status(self):
        if self._show_progress:
            return cmds.progressWindow(q=True, status=True)

    status = property(_get_status, _set_status)

    def _set_progress(self, progress):
        if self._show_progress:
            cmds.progressWindow(e=True, progress=progress)

    def _get_progress(self):
        if self._show_progress:
            return cmds.progressWindow(q=True, progress=True)

    progress = property(_get_progress, _set_progress)

    def is_cancelled(self):
        if self._show_progress:
            return cmds.progressWindow(q=True, ic=True)

    @staticmethod
    def wait(sec=1.0):
        cmds.pause(sec=sec)



class ConformDialogResult(QtWidgets.QDialog):
    """[summary]

    Args:
        QtWidgets ([type]): [description]

    使い方例
    _m = u"マテリアルをアサインする対象が選ばれておりません\n"
    _m += u"マテリアルアサインをせずにマテリアルを生成しますか？"
    _d = ConformDialogResult(message=_m)
    result = _d.exec_()
    if not result:
        return

    """

    def __init__(self, *args, **kwargs):
        super(ConformDialogResult, self).__init__(
            parent=kwargs.setdefault('parent', None),
            f=QtCore.Qt.WindowFlags())

        self.setWindowTitle(kwargs.setdefault('title', TITLE))

        main_layout = QtWidgets.QVBoxLayout()
        btn_layout = QtWidgets.QHBoxLayout()

        label = QtWidgets.QLabel(kwargs.setdefault('message', 'message'))
        self._ok_btn = QtWidgets.QPushButton('OK')
        self._cancel_btn = QtWidgets.QPushButton('Cancel')

        main_layout.addWidget(label)
        main_layout.addLayout(btn_layout)
        btn_layout.addWidget(self._ok_btn)
        btn_layout.addWidget(self._cancel_btn)
        self.setLayout(main_layout)

        self._ok_btn.clicked.connect(self._ok_btn_clicked)
        self._cancel_btn.clicked.connect(self._cancel_btn_clicked)

    def _ok_btn_clicked(self, *args):
        self.close()
        self.setResult(True)

    def _cancel_btn_clicked(self, *args):
        self.close()
        self.setResult(False)


class ConformDialog(QtWidgets.QDialog):
    """[summary]

    Args:
        QtWidgets ([type]): [description]

    使い方例
    _d = ConformDialog(title=u"一覧から選択してください",
                    message=u"マテリアルに適用するテクスチャを選択してから実行してください")
    _d.exec_()
    return
    """
    def __init__(self, *args, **kwargs):
        super(ConformDialog, self).__init__(
            parent=kwargs.setdefault('parent', None),
            f=QtCore.Qt.WindowFlags())

        self.setWindowTitle(kwargs.setdefault('title', TITLE))

        _label = QtWidgets.QLabel(kwargs.setdefault('message', ""))
        # print(kwargs.setdefault('message', 'message'))

        _btn = QtWidgets.QPushButton("OK")
        _btn.clicked.connect(self._btn_clicked)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(_label)
        layout.addWidget(_btn)
        self.setLayout(layout)

    def _btn_clicked(self, *args):
        self.close()
        self.setResult(False)

class PromptDialog(QtWidgets.QInputDialog):

    def __init__(self, *args, **kwargs):
        super(PromptDialog, self).__init__(
            parent=kwargs.setdefault('parent', None),
            flags=QtCore.Qt.WindowFlags(),
        )

        self.setWindowTitle(kwargs.setdefault('title', TITLE))
        # layout = QtWidgets.QVBoxLayout()
        self.setLabelText(kwargs.setdefault('message', ''))
        self.setTextValue(kwargs.setdefault('default', ''))

