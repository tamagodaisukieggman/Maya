import datetime
from PySide2 import QtCore, QtGui, QtWidgets


class ConformDialogResult(QtWidgets.QDialog):
    """確認ダイアログ
    [OK], [Chancel]

    Args:
        QtWidgets ([type]): [description]

    使い方例
    _m = u"マテリアルをアサインする対象が選ばれておりません\n"
    _m += u"マテリアルアサインをせずにマテリアルを生成しますか？"
    _d = ConformDialogResult(title=title, message=_m)
    result = _d.exec_()
    if not result:
        return

    """
    def __init__(self, *args, **kwargs):
        super(ConformDialogResult, self).__init__(
            parent=kwargs.setdefault('parent', None),
            f=QtCore.Qt.WindowFlags())

        main_layout = QtWidgets.QVBoxLayout()
        btn_layout = QtWidgets.QHBoxLayout()

        _message = kwargs.setdefault('message', '')
        _title = kwargs.setdefault('title', '')

        label = QtWidgets.QLabel(_message)
        self._ok_btn = QtWidgets.QPushButton('OK')
        self._cancel_btn = QtWidgets.QPushButton('Cancel')

        self.setWindowTitle(kwargs.setdefault('title', _title))
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
    """プログレスバー
    Args:
        QtWidgets (_type_): _description_

    使い方例:
    _length = 10
    with gui_util.ProgressDialog(title='Import Weight', maxValue=_length) as prg:
        for i, mesh in enumerate(meshes):
            prg.step(i)
            if prg.wasCanceled():
                break
    """

    def __init__(self, *args, **kwargs):
        super(ProgressDialog, self).__init__(
            parent=kwargs.setdefault('parent', None))

        title = kwargs.setdefault('title', '')
        message = kwargs.setdefault('message', '')
        minValue = kwargs.setdefault('minValue', 0)
        maxValue = kwargs.setdefault('maxValue', 0)

        self.setCancelButtonText("&Cancel")
        self.setAutoClose(True)
        self.setWindowTitle(f'{title}')
        self.setLabelText(f'{message}')
        self.message = message
        self.minValue = minValue
        self.maxValue = maxValue
        self.setRange(self.minValue, maxValue)

    def __enter__(self):
        self._start_time = datetime.datetime.now()
        self.show()
        return self

    def setUp(self, maxValue=0, title=''):
        # if maxValue == 0:
        #     self.setStyleSheet('QProgressBar {text-align: center;}')

        self.setRange(self.minValue, maxValue)
        if title:
            self.setWindowTitle(f'{title}')

    def step(self, _step):
        QtCore.QCoreApplication.processEvents()
        _message = f'{self.message} [ {_step} / {self.maxValue} ]'
        # print(_message)
        self.setValue(_step)
        # self.setLabelText(_message)

    def __exit__(self, exc_type=None, exc_val=None, exc_t=None):
        calc_time = datetime.datetime.now() - self._start_time
        _status = '[ End : Calculation time : {} ]'.format(calc_time)
        print(f'[ All [ {self.maxValue} ] count(s) ]')
        print(_status)


class ConformDialog(QtWidgets.QDialog):
    """ダイアログ表示
    [OK] ボタンのみ

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

        _message = kwargs.setdefault('message', '')
        _title = kwargs.setdefault('title', '')
        _label = QtWidgets.QLabel(_message)

        _btn = QtWidgets.QPushButton("OK")
        _btn.clicked.connect(self._btn_clicked)

        self.setWindowTitle(kwargs.setdefault('title', _title))
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(_label)
        layout.addWidget(_btn)
        self.setLayout(layout)
        print(f'message : {_message}')

    def _btn_clicked(self, *args):
        self.close()
        self.setResult(False)

def conform_dialog_result(title="", message=""):
    _d = ConformDialogResult(title=title, message=message)
    result = _d.exec_()
    return result

def conform_dialog(title="", message=""):
    _d = ConformDialog(title=title, message=message)
    _d.exec_()

def close_pyside_windows(window_names=[]):
    """pyside ウィンドウをクラス名で探して閉じる

    Args:
        windows (list): [description]. Defaults to [].
    """
    for _obj in QtWidgets.QApplication.allWidgets():
        if _obj.__class__.__name__ in window_names:
            _obj.close()
            del _obj