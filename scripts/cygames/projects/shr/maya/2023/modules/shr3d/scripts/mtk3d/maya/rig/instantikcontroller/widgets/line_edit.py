import PySide2.QtCore as qc
import PySide2.QtWidgets as qw
import PySide2.QtGui as qg

import maya.utils as utils


class DTLineEdit(qw.QLineEdit):
    def __init__(self, *args, **kwargs):
        super(DTLineEdit, self).__init__(*args, **kwargs)

        font = qg.QFont()
        font.setPixelSize(16)
        self.setFont(font)
        self.font_metrics = qg.QFontMetrics(font)
        self.setFixedHeight(self.font_metrics.height() + 7)

        self._placeholder_message = ''

        self._text_glow = {}
        self._previous_text = ''
