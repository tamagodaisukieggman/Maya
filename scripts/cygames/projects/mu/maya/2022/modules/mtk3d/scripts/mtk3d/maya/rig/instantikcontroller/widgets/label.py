import PySide2.QtCore as qc
import PySide2.QtGui as qg
import PySide2.QtWidgets as qw


class CustomLabel(qw.QLabel):
    def __init__(self, *args, **kwargs):
        super(CustomLabel, self).__init__(*args, **kwargs)
        self.setFixedHeight(25)
        self.setFixedWidth(25)
        self._radius = 5
        self.setMinimumWidth(100)
        self.setMaximumWidth(100)
        self.setText(args[0])
