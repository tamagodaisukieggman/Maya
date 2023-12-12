import os

from PySide2.QtCore import (Qt,
    QRect,
    QPoint,
    QSize,
    QEvent
)
from PySide2.QtWidgets import (
    QTreeView,
    QTableView,
    QHeaderView,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSplitter,
    QLineEdit,
    QPushButton,
    QComboBox,
    QLabel,
    QSpacerItem,
    QSizePolicy,
)

from .directory_model import MtkExplorerDirModel
from .filemodel.filemodel import MtkExplorerFileModel
from .filemodel.filemodelabstract import MtkExplorerFileAbstractTableModel
from .filemodel.filemodelfilter import MtkExplorerFileSortFilterProxyModel
from .filemodel.filemodelcolumn import MtkExplorerFileModelColumn
from .tooltip_popup import ToolTipPopup
from .settings import MtkExplorerSettings

CAS_PATH = "Z:/mtk/.cas/p4/meta-extra/original/resources"
WORK_PATH = "Z:/mtk/work/resources"

class MtkExplorerDirView(QTreeView):

    def __init__(self, *args, **kwargs):
        u"""init"""
        super(MtkExplorerDirView, self).__init__(parent=kwargs.setdefault('parent', None))


        self.setObjectName('MtkExplorerDirView')
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        self._model = MtkExplorerDirModel()
        defaultWorkPath = MtkExplorerSettings.defaultWorkPath()
        self.start_root = kwargs.setdefault('root', defaultWorkPath)

        left = kwargs.setdefault('left', 0)
        top = kwargs.setdefault('top', 0)
        width = kwargs.setdefault('width', 220)
        height = kwargs.setdefault('height', 200)
        self.setGeometry(QRect(QPoint(left, top), QSize(width, height)))

        self.setModel(self._model)
        self.setRootIndex(self._model.setRootPath(self.start_root))

        self._set_header()
        self._set_abstractview()

    def _set_header(self):
        u"""Set Header"""
        header = self.header()

        header.setSectionHidden(1, True)
        header.setSectionHidden(2, True)
        header.setSectionHidden(3, True)

    def _set_abstractview(self):
        u"""Set AbstractView"""
        self.setAutoScroll(True)

    def reload(self, work_path):
        self.setRootIndex(self._model.setRootPath(work_path))


class MtkExplorerFileView(QTableView):

    def __init__(self, *args, **kwargs):
        u"""init"""
        super(MtkExplorerFileView, self).__init__(parent=kwargs.setdefault('parent', None))
        self.setObjectName('MtkExplorerFileView')
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        # flag to use abstract table model
        self.use_abstract_table_model = True

        # shotgun column enable flag
        self._enable_sg = True

        if not self.use_abstract_table_model:
            self.source_model = MtkExplorerFileModel(0, 4, view=self)
        else:
            self.source_model = MtkExplorerFileAbstractTableModel(parent=self)

        # set custom filter model
        self.proxy_model = MtkExplorerFileSortFilterProxyModel()
        self._delegate = kwargs.setdefault('delegate', None)

        left = kwargs.setdefault('left', 0)
        top = kwargs.setdefault('top', 0)
        width = kwargs.setdefault('width', 300)
        height = kwargs.setdefault('height', 480)

        self.setGeometry(QRect(QPoint(left, top), QSize(width, height)))
        self._set_abstractview()
        self._set_tableview()
        self._set_header()

        self.proxy_model.setSourceModel(self.source_model)
        self.setModel(self.proxy_model)

        if self._delegate:
            self.setItemDelegate(self._delegate)

        # enable mouse events to receive them in the event filter.
        self.setMouseTracking(True)
        #self.viewport().setAttribute(Qt.WA_Hover)  # this is for force-repaint, not mouse hover.

        # set an event filter for tableview's viewport
        self.viewport().installEventFilter(self)

        # create a tool tip popup to display perforce file user names.
        self._popup = ToolTipPopup(parent=self)

        # hide some columns
        if not self._enable_sg:
            self.hideColumn(MtkExplorerFileModelColumn.SG_Task_Id())

    # event filter for processing mouse events
    # and displaying Perforce user names for checked-out files
    def eventFilter(self, object, event):
        if self.viewport() == object:
            if event.type() == QEvent.MouseMove:
                mouseEvent = event
                index = self.indexAt(mouseEvent.pos())
                if index.isValid():
                    p4_user_column = MtkExplorerFileModelColumn.P4_Users_Id()
                    row_data = self.source_model.get_row_data(index.row())
                    p4_user_list = row_data[p4_user_column]
                    
                    p4_users_string = ''

                    if p4_user_list:
                        p4_users_string = ', '.join(p4_user_list)
                    
                    _cache_image = ''

                    # Cylistaのキャッシュファイルがあれば、それをサムネイルとして使う
                    ### ここから
                    _current_dir = self.source_model._folder_path
                    _current_file = index.data()
                    if _current_dir and _current_file:
                        _current_path = os.path.join(_current_dir, _current_file)
                        if os.path.exists(_current_path):
                            _current_path = os.path.splitext(_current_path)[0]
                            _relpath = os.path.relpath(_current_path, WORK_PATH)
                            _cache_path = os.path.join(CAS_PATH, _relpath)
                            _cache_path = _cache_path + ".mdli.cy-asset-prv"
                            if os.path.exists(_cache_path):
                                if p4_users_string:
                                    p4_users_string = p4_users_string + '<br>'
                                _cache_image = '<img src="' + _cache_path.replace(os.sep, '/') + '" width = 256 height = 256>'
                    ###　ここまで

                    pop_string = p4_users_string + _cache_image
                    if pop_string:
                        self._popup.setText(pop_string)
                        self.showPopup(index)

                else:
                    self.hidePopup()
            elif event.type() == QEvent.Leave:
                self.hidePopup()
            #else:
                #print("Unhandled Event")
                #print("Event: {}".format(event.type()))

        elif self._popup == object:
            if event.type() == QEvent.Leave:
                self.hidePopup()
        #else:
            #print("Unhandled Object")
            #print("Object: {}".format(type(object)))
            #print("Event: {}".format(event.type()))

        # handle the table view event
        return QTableView.eventFilter(self, object, event)

    def showPopup(self, index):
        if index.column() == 0:
            rect = self.visualRect(index)
            #pos = self.mapToGlobal(rect.bottomLeft())
            pos = self.viewport().mapToGlobal(rect.center())
            self._popup.dialog().move(pos)
            #self._popup.dialog().setFixedSize(100, self._popup.dialog().heightForWidth(100))
            self._popup.show()

    def hidePopup(self):
        self._popup.hide()


    def translateIndex(self, index):
        return self.proxy_model.mapToSource(index)

    def tableItemFromIndex(self, index):
        item = self.source_model.itemFromIndex(self.proxy_model.mapToSource(index))
        return item

    def _set_abstractview(self):
        u"""Set AbstractView"""
        self.setEditTriggers(self.NoEditTriggers)
        self.setSelectionBehavior(self.SelectRows)

    def _set_tableview(self):
        u"""Set TableView"""
        self.setShowGrid(False)
        self.setSortingEnabled(True)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def _set_header(self):
        u"""Set Header"""
        v_header = self.verticalHeader()
        h_header = self.horizontalHeader()

        # set fixed table row height for all cells
        v_header.setSectionResizeMode(QHeaderView.Fixed)
        v_header.setDefaultSectionSize(22)
        v_header.setVisible(False)

        h_header.setMinimumHeight(22)
        h_header.setSortIndicator(0, Qt.AscendingOrder)
        h_header.setSectionResizeMode(QHeaderView.ResizeToContents)

    def reload(self):
        self.resizeColumnsToContents()
        self.resizeRowsToContents()


class _SearchBox(QWidget):

    def __init__(self, *args, **kwargs):
        u"""init"""
        super(_SearchBox, self).__init__(parent=kwargs.setdefault('parent', None))

        self._button_width = 45
        self._button_height = 24

        self.textbox = QLineEdit()
        self.textbox.setPlaceholderText('Search ...')
        self.textbox.setMinimumHeight(self._button_height)
        self.textbox.setMaximumHeight(self._button_height)

        self.button = QPushButton('Clear')

        self.button.setMinimumHeight(self._button_height)
        self.button.setMaximumHeight(self._button_height)
        self.button.setMinimumWidth(self._button_width)
        self.button.setMaximumWidth(self._button_width)

        self._setup()

    def _setup(self):
        u"""setup layout"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.textbox)
        layout.addWidget(self.button)
        self.button.clicked.connect(self._button_clicked)

    def _button_clicked(self, *args):
        u"""Button Command"""
        self.textbox.setText('')

    def reload(self):
        self.textbox.setText('')

class _P4StatusFilterBox(QWidget):

    def __init__(self, *args, **kwargs):
        u"""init"""
        super(_P4StatusFilterBox, self).__init__(parent=kwargs.setdefault('parent', None))

        self._label = QLabel('P4 Status')
        self._label.setMinimumWidth(60)
        self._label.setMaximumWidth(60)
        self.pulldown = QComboBox()
        self.pulldown.addItems(self.get_p4_action_statuses())

        self._spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self._label)
        layout.addWidget(self.pulldown)
        layout.addSpacerItem(self._spacer)

    def get_p4_action_statuses(self):
        u"""カテゴリーの取得

        :param root: ルートパス
        :param excludes: カテゴリーから除外対象のリスト
        :return: カテゴリー名のリスト
        """
        p4_action_statuses = ['none', 'other', 'add', 'checkout', 'stale', 'latest']

        return p4_action_statuses

    def reload(self):
        self.pulldown.clear()
        self.pulldown.addItems(self.get_p4_action_statuses())

class MtkExplorerBody(QWidget):

    def __init__(self, *args, **kwargs):
        u"""init"""
        super(MtkExplorerBody, self).__init__(parent=kwargs.setdefault('parent', None))

        self.dir_view = MtkExplorerDirView()
        self.search_box = _SearchBox()
        self.p4_status_filter_box = _P4StatusFilterBox()
        self.file_view = MtkExplorerFileView()

        self._setup()

    def _setup(self):
        u"""setup"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        splitter = QSplitter()
        splitter.setOrientation(Qt.Vertical)

        upper_widget = QWidget(splitter)
        upper_widget.setGeometry(QRect(QPoint(0, 0), QSize(250, 250)))
        upper_layout = QVBoxLayout(upper_widget)
        upper_layout.setContentsMargins(0, 0, 0, 0)
        upper_layout.addWidget(self.dir_view)

        bottom_widget = QWidget(splitter)
        bottom_widget.setGeometry(QRect(QPoint(0, 0), QSize(250, 550)))
        bottom_layout = QVBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.addWidget(self.search_box)
        bottom_layout.addWidget(self.p4_status_filter_box)
        bottom_layout.addWidget(self.file_view)

        layout.addWidget(splitter)

    def reload(self, work_path):
        self.dir_view.reload(work_path)
        self.search_box.reload()
        self.p4_status_filter_box.reload()
        self.file_view.reload()


if __name__ == '__main__':
    import sys

    try:
        from PySide2.QtWidgets import QApplication
    except ImportError:
        from PySide.QtGui import QApplication

    app = QApplication(sys.argv)

    widget = MtkExplorerBody()
    widget.show()

    sys.exit(app.exec_())
