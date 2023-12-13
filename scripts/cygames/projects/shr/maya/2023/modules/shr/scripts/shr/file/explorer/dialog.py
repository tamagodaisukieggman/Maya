from PySide2.QtCore import Qt
from PySide2.QtWidgets import (
    QDialog,
    QInputDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel
)

class MtkExplorerDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(MtkExplorerDialog, self).__init__(
            parent=kwargs.setdefault('parent', None),
            f=Qt.WindowFlags(),
        )

        self.setWindowTitle(kwargs.setdefault('title', 'title'))

        main_layout = QVBoxLayout()
        btn_layout = QHBoxLayout()

        label = QLabel(kwargs.setdefault('message', 'message'))
        self._ok_btn = QPushButton('OK')
        self._cancel_btn = QPushButton('Cancel')

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


class MtkExplorerPromptDialog(QInputDialog):

    def __init__(self, *args, **kwargs):
        super(MtkExplorerPromptDialog, self).__init__(
            parent=kwargs.setdefault('parent', None),
            flags=Qt.WindowFlags(),
        )

        self.setWindowTitle(kwargs.setdefault('title', 'title'))
        self.setLabelText(kwargs.setdefault('message', 'message'))
