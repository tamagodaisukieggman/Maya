from maya import cmds
import datetime
import time
import webbrowser

from PySide2 import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance

import maya.OpenMayaUI as omui

try:
    from ..new_checker import EXPORT_WINDOW_CLASS_NAME
except ImportError:
    EXPORT_WINDOW_CLASS_NAME = None

from ..new_checker import TITLE

try:
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QtWidgets.QWidget)
except Exception as e:
    print(e)
    mayaMainWindowPtr = None
    mayaMainWindow = None


def open_help_site(*args):
    _web_site = "https://wisdom.cygames.jp/display/mutsunokami/Maya:+Mutsunokami+Exporter+Window"
    try:
        webbrowser.open(_web_site)
    except Exception as e:
        print("error--- ", e)


class ProgressWindowBlock:
    """ProgressWindowを表示させるコンテキストマネージャー
    """

    def __init__(self,
                 title='',
                 progress=0,
                 minValue=0,
                 maxValue=100,
                 isInterruptable=True,
                 show_progress=True
                 ):

        self._show_progress = show_progress and (
            not cmds.about(q=True, batch=True))

        self.title = title
        self.progress = progress
        self.minValue = minValue
        self.maxValue = maxValue
        self.isInterruptable = isInterruptable

        self._start_time = None
        self.status = ""

    def __enter__(self):
        _message = f'[ {self.title} ] : Start'
        print(_message)

        if self._show_progress:
            cmds.progressWindow(
                title=self.title,
                progress=int(self.progress),
                status=_message,
                isInterruptable=self.isInterruptable,
                min=self.minValue,
                max=self.maxValue + 1
            )
        self._start_time = time.time()

        return self

    def __exit__(self, exc_type=None, exc_val=None, exc_tb=None):
        calc_time = time.time() - self._start_time
        _message = f'[ {self.title} ] : End : Calculation time : {calc_time}'
        print(_message)

        if self._show_progress:
            cmds.progressWindow(endProgress=True)

    def step(self, step):
        if self._show_progress:
            cmds.progressWindow(e=True, step=step)

    def _get_status(self):
        if self._show_progress:
            return cmds.progressWindow(q=True, status=True)

    def _set_status(self, status):
        if self._show_progress:
            _message = f'[ {self.progress} / {self.maxValue} ] : {status}'
            cmds.progressWindow(e=True, status=_message)

    status = property(_get_status, _set_status)

    def _get_progress(self):
        if self._show_progress:
            return cmds.progressWindow(q=True, progress=True)

    def _set_progress(self, progress):
        if self._show_progress:
            cmds.progressWindow(e=True, progress=progress)

    progress = property(_get_progress, _set_progress)

    def is_cancelled(self):
        if self._show_progress:
            return cmds.progressWindow(q=True, isCancelled=True)

    @staticmethod
    def wait(sec=1.0):
        cmds.pause(sec=sec)


def confirmDialog(_message="", _title="確認してください"):
    cmds.confirmDialog(
        message=_message,
        title=_title,
        button=['OK'],
        defaultButton='OK',
        cancelButton="OK",
        dismissString="OK")


def open_export_window():
    """Cyllista Export Window
    """
    import cylModelExporterWindow
    cylModelExporterWindow.show()


def close_pyside_windows(windows=[]):
    """pyside ウィンドウをクラス名で探して閉じる

    Args:
        windows (list): [description]. Defaults to [].
    """
    windows.append(EXPORT_WINDOW_CLASS_NAME)

    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QtWidgets.QWidget)

    for child in mayaMainWindow.children():
        for checker_window in windows:
            if child.__class__.__name__ == checker_window:
                child.close()


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

        _message = kwargs.setdefault('message', '')
        label = QtWidgets.QLabel(_message)
        self._ok_btn = QtWidgets.QPushButton('OK')
        self._cancel_btn = QtWidgets.QPushButton('Cancel')

        main_layout.addWidget(label)
        main_layout.addLayout(btn_layout)
        btn_layout.addWidget(self._ok_btn)
        btn_layout.addWidget(self._cancel_btn)
        self.setLayout(main_layout)

        self._ok_btn.clicked.connect(self._ok_btn_clicked)
        self._cancel_btn.clicked.connect(self._cancel_btn_clicked)

        print(f'message : {_message}')

    def _ok_btn_clicked(self, *args):
        self.close()
        self.setResult(True)

    def _cancel_btn_clicked(self, *args):
        self.close()
        self.setResult(False)


class ProgressDialog(QtWidgets.QProgressDialog):
    def __init__(self, *args, **kwargs):
        super(ProgressDialog, self).__init__(
            parent=kwargs.setdefault('parent', None)
        )
        self.setCancelButtonText("&Cancel")
        self.setAutoClose(True)

    def setUp(self, _length=0, title=""):
        self.setRange(0, _length)
        self.setWindowTitle(f'{title}')


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

        _message = kwargs.setdefault('message', '')
        _label = QtWidgets.QLabel(_message)
        # print(kwargs.setdefault('message', 'message'))

        _btn = QtWidgets.QPushButton("OK")
        _btn.clicked.connect(self._btn_clicked)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(_label)
        layout.addWidget(_btn)
        self.setLayout(layout)
        print(f'message : {_message}')

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
