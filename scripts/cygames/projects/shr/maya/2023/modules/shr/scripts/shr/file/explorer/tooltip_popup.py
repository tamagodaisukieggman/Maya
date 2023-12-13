from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QLabel,
    QDialog,
    QVBoxLayout
)


class ToolTipPopup:
    def __init__(self, labelText="", parent=None):
        self._parent = parent

        self._label = QLabel(text=labelText)
        self._label.setWordWrap(True)
        self._label.setAlignment(Qt.AlignLeft)
        self._label.adjustSize()
        self._label.setStyleSheet("QLabel { background-color : yellow; color : blue; }")

        self._layout = QVBoxLayout()
        self._layout.addWidget(self._label)

        self._dialog = QDialog(parent=parent, f=Qt.Popup | Qt.ToolTip)
        self._dialog.setLayout(self._layout)
        self._dialog.adjustSize()
        self._dialog.setStyleSheet("QDialog { background-color : yellow;}")

        if parent:
            self._dialog.installEventFilter(parent)

    def label(self):
        return self._label

    def dialog(self):
        return self._dialog

    def setText(self, text):
        if self._label:
            self._label.setText(text)
            self._label.adjustSize()

        if self._dialog:
            self._dialog.adjustSize()

    def show(self):
        if self._label:
            self._label.adjustSize()
            #self._label.repaint()

        if self._dialog:
            self._dialog.adjustSize()
            #self._dialog.repaint()
            self._dialog.show()

    def hide(self):
        if self._dialog:
            self._dialog.hide()
