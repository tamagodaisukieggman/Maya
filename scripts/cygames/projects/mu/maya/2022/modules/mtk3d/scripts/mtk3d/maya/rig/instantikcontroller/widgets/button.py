import PySide2.QtCore as qc
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw

# from PyQt4.QtGui import QPen, QColor, QBrush, QLinearGradient

# import base; reload(base)

NORMAL, DOWN, DISABLED = 1, 2, 3
INNER, OUTER = 1, 2


class DTButton(qw.QPushButton):
    def __init__(self, *args, **kwargs):
        super(DTButton, self).__init__(*args, **kwargs)
        self.setFixedHeight(25)
        self.setFixedWidth(25)
        self._radius = 5


class DTButtonThin(DTButton):
    def __init__(self, *args, **kwargs):
        super(DTButtonThin, self).__init__(*args, **kwargs)
        self.setFixedHeight(22)
        self._radius = 10


class DTCloseButton(DTButton):
    def __init__(self, *args, **kwargs):
        super(DTCloseButton, self).__init__(*args, **kwargs)
        self._radius = 10
        self.setFixedHeight(20)
        self.setFixedWidth(20)


class CustomButton(DTButton):
    def __init__(self, *args, **kwargs):
        super(CustomButton, self).__init__(*args, **kwargs)
        self.setMinimumWidth(50)
        self.setMaximumWidth(50)
        self.setText(args[0])
