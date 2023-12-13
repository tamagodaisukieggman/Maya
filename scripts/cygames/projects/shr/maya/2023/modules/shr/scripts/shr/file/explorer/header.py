import os

from PySide2.QtCore import QDir
from PySide2.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QFileDialog,
    QComboBox,
    QLabel,
    QSpacerItem,
    QSizePolicy,
    QCheckBox,
    QVBoxLayout,
    QHBoxLayout,
)

from .settings import MtkExplorerSettings



class _Bookmark(QWidget):

    def __init__(self, *args, **kwargs):
        u"""init"""
        super(_Bookmark, self).__init__(parent=kwargs.setdefault('parent', None))
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._label = QLabel('Bookmarks')
        self._label.setMinimumWidth(60)
        self._label.setMaximumWidth(60)
        self.pulldown = QComboBox()

        layout.addWidget(self._label)
        layout.addWidget(self.pulldown)

    def reload(self, bookmarks):
        self.pulldown.clear()
        for bookmark in bookmarks:
            if bookmark:
                self.pulldown.addItem(bookmark)



class _Category(QWidget):

    def __init__(self, *args, **kwargs):
        u"""init"""
        super(_Category, self).__init__(parent=kwargs.setdefault('parent', None))
        defaultWorkPath = MtkExplorerSettings.defaultWorkPath()

        self._root = defaultWorkPath
        self._label = QLabel('Categories')
        self._label.setMinimumWidth(60)
        self._label.setMaximumWidth(60)
        self.pulldown = QComboBox()
        self.pulldown.addItems(self.get_categories())

        self._spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self._label)
        layout.addWidget(self.pulldown)
        layout.addSpacerItem(self._spacer)

    def get_categories(self):
        u"""カテゴリーの取得

        :param root: ルートパス
        :param excludes: カテゴリーから除外対象のリスト
        :return: カテゴリー名のリスト
        """
        categories = []

        # add sub-folders only
        root, dirs, files = os.walk(self._root).__next__()
        if dirs:
            categories = dirs

        return categories

    def reload(self, work_path):
        self._root = work_path
        self.pulldown.clear()
        self.pulldown.addItems(self.get_categories())



class _AddressBar(QWidget):

    def __init__(self, *args, **kwargs):
        u"""init"""
        super(_AddressBar, self).__init__(parent=kwargs.setdefault('parent', None))
        defaultWorkPath = MtkExplorerSettings.defaultWorkPath()

        self._button_width = 24
        self._button_height = 24
        self._default_path = defaultWorkPath
        self._callback_onRootPathChanged = None

        self._text = kwargs.setdefault('text', self._default_path)
        self.textbox = QLineEdit(self._text)
        self.textbox.setMinimumHeight(self._button_height)
        self.textbox.setMaximumHeight(self._button_height)

        self.button = QPushButton('...')
        self.button.setMinimumHeight(self._button_height)
        self.button.setMaximumHeight(self._button_height)
        self.button.setMinimumWidth(self._button_width)
        self.button.setMaximumWidth(self._button_width)

        self._setup()

    def setCallback_OnRootPathChanged(self, callback):
        self._callback_onRootPathChanged = callback

    def _setup(self):
        u"""setup layout"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.textbox)
        layout.addWidget(self.button)
        self.button.clicked.connect(self._button_clicked)

    def _button_clicked(self, *args):
        u"""Button Command"""
        dialog = QFileDialog(directory=self.textbox.text())
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setFilter(QDir.Dirs | QDir.NoDotAndDotDot)
        if dialog.exec_():
            path = dialog.selectedFiles()[0]
            if self._callback_onRootPathChanged:
                self._callback_onRootPathChanged(path)
            else:
                self.textbox.setText(path)

    def reload(self, work_path):
        self._text = work_path
        self.textbox.setText(self._text)



class MtkExplorerHeader(QWidget):

    def __init__(self, *args, **kwargs):
        u"""init"""
        super(MtkExplorerHeader, self).__init__(parent=kwargs.setdefault('parent', None))

        self.bookmark = _Bookmark()
        self.category = _Category()
        self.sets_workspace = QCheckBox(u'workspaceをセットしてから開く')
        self.sets_workspace.setChecked(True)
        self.checkouts = QCheckBox(u'チェックアウトしてから開く')
        self.sets_sg_task_status = QCheckBox(u'Shotgunのタスクステータスが　「着手中(rdy)」　に設定してから開く')
        self.sets_sg_task_status.setChecked(False)
        self.address_bar = _AddressBar()

        self._setup()

    def _setup(self):
        u"""setup layout"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.bookmark)
        layout.addWidget(self.category)
        layout.addWidget(self.sets_workspace)
        layout.addWidget(self.checkouts)
        layout.addWidget(self.sets_sg_task_status)
        layout.addWidget(self.address_bar)

    def reload(self, work_path):
        self.address_bar.reload(work_path)
        self.category.reload(work_path)


if __name__ == '__main__':
    import sys

    try:
        from PySide2.QtWidgets import QApplication
    except ImportError:
        from PySide.QtGui import QApplication

    app = QApplication(sys.argv)

    widget = MtkExplorerHeader()
    widget.show()

    sys.exit(app.exec_())
