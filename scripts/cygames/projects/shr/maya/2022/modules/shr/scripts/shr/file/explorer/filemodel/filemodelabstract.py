import os
import glob
import re
import ntpath
from datetime import datetime
from distutils.util import strtobool

from PySide2.QtCore import (
    Qt,
    QAbstractTableModel,
    SIGNAL,
    Signal
)
from PySide2.QtGui import QStandardItem
from PySide2.QtWidgets import QApplication

try:
    import maya.cmds as cmds
    import maya.mel as mel

    if hasattr(cmds, 'about'):
        MODE = 'MAYA'
    else:
        MODE = 'STANDALONE'
except ImportError:
    MODE = 'STANDALONE'

from mtk.utils.perforce import MtkP4
from mtk.utils.shotgun import MtkSG
from mtk import logger

from .filemodelcolumn import MtkExplorerFileModelColumn
from ..perforce import MtkExplorerPerforceStatusIconProvider
from ..shotgun import ShotgunTaskComboBoxDelegate


class MtkExplorerFileAbstractTableModel(QAbstractTableModel):
    numberPopulated = Signal(int)

    #def __init__(self, view=None, parent=None):
    def __init__(self, *args, **kwargs):

        super(MtkExplorerFileAbstractTableModel, self).__init__(
            parent=kwargs.setdefault('parent', None)
        )


        # set parent
        self._tableview = parent=kwargs.setdefault('parent', None)

        self._tabledata = []
        self._columndata = []
        self._row_count = 0
        self._column_count = 0
        self._max_row_fetch = 50
        self._folder_path = ""

        self._enable_sg = self._tableview._enable_sg

        self.load_header()

    def _on_data_changed(self, *args):

        if args is not None:
            logger.debug("args: {}".format(args))

    def _terminates(self):
        #return False

        if MODE != 'MAYA':
            logger.debug("False")
            return False

        global_vars = mel.eval('env')

        if (
            '$g_mtk_explorer_escape' in global_vars
            and strtobool(mel.eval('global int $g_mtk_explorer_escape;$temp=$g_mtk_explorer_escape;'))
          ):
            logger.debug("True")
            return True
        else:
            logger.debug("False")
            return False

    def _calc_text_size(self, text):
        # check
        font = QFont() #("times", 24)
        fontMetrics = QFontMetrics(font)
        # pWidth = fontMetrics.width(data)
        # pHeight = fontMetrics.height(data)
        pWidthBR = fontMetrics.boundingRect(text).width()
        pHeightBR = fontMetrics.boundingRect(text).height()
        # logger.debug("Width1: {}, Height1: {}".format(pWidth, pHeight))
        logger.debug("FontMetrics - Text: {}, WidthBR: {}, HeightBR: {}".format(text, pWidthBR, pHeightBR))
        return [pWidthBR, pHeightBR]

    def _get_resource_paths(self, root_path):
        u"""ファイルパスの取得

        取得するファイル: .ma, .mb, .fbx
        """

        if MODE == 'MAYA':
            file_paths = glob.glob('{}/*.ma'.format(root_path))
            file_paths.extend(glob.glob('{}/*.mb'.format(root_path)))
            file_paths.extend(glob.glob('{}/*.fbx'.format(root_path)))
        else:
            file_paths = glob.glob('{}/*.*'.format(root_path))
        file_paths = [re.sub(r'\\', '/', file_path) for file_path in file_paths]

        return file_paths

    def load_header(self):

        self.layoutAboutToBeChanged.emit()

        column_data = MtkExplorerFileModelColumn.column_labels()

        logger.debug("Columns: {}".format(column_data))

        self._columndata = list(column_data)

        self._column_count = len(self._columndata)

        self.layoutChanged.emit()

    def load_data(self, folder_path):
        """mel eval commands removed for performance reasons"""

        file_paths = self._get_resource_paths(folder_path)

        if not file_paths:
            logger.debug("No File Paths. Returning...")
            return

        logger.debug("def load_data")

        self._folder_path = folder_path

        p4_status_list = MtkP4.status_ext(file_paths)

        # create shotgun asset name list from the maya file name list.
        # (without the .ma file extension)
        sg_asset_names = [ntpath.basename(x).split(".")[0] for x in file_paths]

        sg_asset_task_dict = {}

        if self._enable_sg:
            sg_asset_task_dict = MtkSG.asset_task_batch(sg_asset_names)

        table_data = []

        logger.debug('Load Table Data (Start): {}'.format(self._folder_path))

        for i, (file_path, status) in enumerate(p4_status_list.items()):

            QApplication.processEvents()

            # 0 (Name)
            file_name = os.path.basename(file_path)
            # 1 (Rev)
            file_rev = '{}/{}'.format(status['haveRev'], status['headRev'])
            # 2 (Date Modified)
            dt = datetime.fromtimestamp(os.stat(file_path).st_mtime)
            file_timestamp = dt.strftime('%Y/%m/%d %H:%M:%S')
            # 3 (P4 Status)
            file_p4status = '{}'.format(status['action'])
            # 5 (P4 Users)
            p4_file_users = status['users']
            # 4 (Shotgun Task Status)
            sg_asset_name = ntpath.basename(file_name).split(".")[0]
            sg_tasks = []

            if sg_asset_task_dict and sg_asset_name in sg_asset_task_dict:
                logger.debug("Asset: {}".format(sg_asset_name))
                sg_tasks = sg_asset_task_dict[sg_asset_name]
                for task in sg_tasks:
                    logger.debug("Task: {}".format(task))

            row_data = tuple((file_name, file_rev, file_timestamp, file_p4status, sg_tasks, p4_file_users))

            logger.debug('Load Table Data (Row): {}'.format(row_data))

            table_data.append(row_data)

        logger.debug('Load Table Data (End): {}'.format(self._folder_path))

        if not table_data:
            logger.debug("No Table Data. Returning...")
            return

        self.layoutAboutToBeChanged.emit()

        column_data = MtkExplorerFileModelColumn.column_labels()

        self._tabledata = list(table_data)
        self._columndata = list(column_data)
        # self._row_count = len(self._tabledata)  # Note: this is disabled to use the fetchmore function.
        self._column_count = len(self._columndata)

        num_row_total = len(self._tabledata)

        logger.debug('Rows: {}'.format(self._row_count))
        logger.debug('Columns: {}'.format(self._column_count))

        topLeft = self.createIndex(0, 0)
        bottomRight = self.createIndex(num_row_total, self._column_count)
        roles = 0
        self.dataChanged.emit(topLeft, bottomRight, roles)

        self.layoutChanged.emit()

        # set custom combobox delegate
        if self._tableview:

            if self._enable_sg:
                SG_Task_Column_Id = MtkExplorerFileModelColumn.SG_Task_Id()

                self._tableview.setItemDelegateForColumn(SG_Task_Column_Id,
                                                         ShotgunTaskComboBoxDelegate(parent=self._tableview))

                for row in range(len(self._tabledata)):
                    self._tableview.openPersistentEditor(self.index(row, SG_Task_Column_Id))

    def get_row_data(self, row_id):

        if not 0 <= row_id < len(self._tabledata):
            return None

        row_data = self._tabledata[row_id]

        return row_data

    def update_row_data(self, row_id, file_name, file_rev, file_timestamp, file_p4_status, sg_task, p4_file_users):

        if not 0 <= row_id < len(self._tabledata):
            return None

        row_data = self._tabledata[row_id]

        updated_row_data = tuple((file_name, file_rev, file_timestamp, file_p4_status, sg_task, p4_file_users))

        logger.debug("Row Data: {}".format(row_data))
        logger.debug("Row Data (Updated): {}".format(updated_row_data))

        self._tabledata[row_id] = updated_row_data

        topLeft = self.createIndex(row_id, 0)
        bottomRight = self.createIndex(row_id, self._column_count)

        # send the 'Data Changed' signal
        roles = 0
        self.dataChanged.emit(topLeft, bottomRight, roles)

    def clear(self):

        self.layoutAboutToBeChanged.emit()

        del self._tabledata[:]
        self._row_count = 0
        self._folder_path = ""

        self.layoutChanged.emit()

    def item(self, row_id, column_id):
        """compatiblity function for source files using qstandarditemmodel functions"""

        if not 0 <= row_id < len(self._tabledata):
            return None

        name_column_id = MtkExplorerFileModelColumn.Name_Id()
        rev_column_id = MtkExplorerFileModelColumn.Rev_Id()
        date_mod_column_id = MtkExplorerFileModelColumn.Date_Modified_Id()
        p4_column_id = MtkExplorerFileModelColumn.P4_Status_Id()
        #sg_asset_id = MtkExplorerFileModelColumn.SG_Asset_Status_Id()
        sg_task_column_id = MtkExplorerFileModelColumn.SG_Task_Id()
        p4_users_column_id = MtkExplorerFileModelColumn.P4_Users_Id()

        row_data = self._tabledata[row_id]

        file_name = row_data[name_column_id]
        rev = row_data[rev_column_id]
        date_mod = row_data[date_mod_column_id]
        p4_status = row_data[p4_column_id]
        p4_icon = MtkExplorerPerforceStatusIconProvider.status_icon(p4_status)
        sg_tasks = row_data[sg_task_column_id]
        p4_users = row_data[p4_users_column_id]

        item = QStandardItem("DefaultItem")

        if column_id == name_column_id:
            item = QStandardItem(p4_icon, file_name)
        elif column_id == rev_column_id:
            item = QStandardItem(rev)
        elif column_id == date_mod_column_id:
            item = QStandardItem(date_mod)
        elif column_id == p4_column_id:
            item = QStandardItem(p4_status)
        elif column_id == sg_task_column_id:
            item = QStandardItem(sg_tasks)
        elif column_id == p4_users_column_id:
            item = QStandardItem(p4_users)

        if column_id != name_column_id:
            item.setTextAlignment(Qt.AlignHCenter)

        return item

    def itemFromIndex(self, index):
        """compatiblity function for source files using qstandarditemmodel functions"""

        if not index.isValid():
            return None

        if not 0 <= index.row() < len(self._tabledata):
            return None

        row_id = index.row()
        column_id = index.column()

        item = self.item(row_id, column_id)

        return item

    def rowCount(self, parent=None):
        #logger.debug("{}".format(self._row_count))
        return self._row_count

    def columnCount(self, parent=None):
        #logger.debug("{}".format(self._column_count))
        return self._column_count

    def hasChildren(self, index):
        return True

    # for incremental data loading
    def canFetchMore(self, index):

        if index.isValid():
            logger.debug("Valid: False")
            return False

        num_row_total = len(self._tabledata)

        return self._row_count < num_row_total

    # for incremental data loading
    def fetchMore(self, index):

        if index.isValid():
            return

        num_row_total = len(self._tabledata)
        cur_row_count = self._row_count
        remain_row_count = (num_row_total - cur_row_count)

        max_row_fetch = self._max_row_fetch
        num_row_fetch = min(max_row_fetch, remain_row_count)
        num_row_fetch = max(0, num_row_fetch)

        logger.debug("RowTotal: {}, RowCount: {}, Remaining: {}, NumFetch: {}".format(num_row_total, cur_row_count,
                                                                                    remain_row_count, num_row_fetch))
        self.layoutAboutToBeChanged.emit()

        if num_row_fetch > 0:
            # begin
            begin = self._row_count
            end = (self._row_count + num_row_fetch) - 1
            # begin insert rows
            self.beginInsertRows(index, begin, end)
            self._row_count += num_row_fetch
            self.endInsertRows()
            # end insert rows

        # this signal is required for the fetchMore function.
        # But it does not cause the headers to "resize to contents" .
        self.emit(SIGNAL("numberPopulated"), num_row_fetch)

        # this signal causes the headers to "resize to contents"
        topLeft = self.createIndex(begin, 0)
        bottomRight = self.createIndex(end, self._column_count)
        roles = 0
        self.dataChanged.emit(topLeft, bottomRight, roles)

        self.layoutChanged.emit()

    def data(self, index, role=Qt.DisplayRole):

        if not index.isValid():
            logger.debug("Index InValid")
            return None

        if not 0 <= index.row() < len(self._tabledata):
            return None

        row_id = index.row()
        column_id = index.column()

        name_column_id = MtkExplorerFileModelColumn.Name_Id()
        p4_column_id = MtkExplorerFileModelColumn.P4_Status_Id()
        sg_task_column_id = MtkExplorerFileModelColumn.SG_Task_Id()

        if index.isValid():
            logger.debug("Index Valid")

            if role == Qt.UserRole:
                if column_id == sg_task_column_id:
                    row_data = self._tabledata[row_id][column_id]
                    return row_data

            if role == Qt.DisplayRole:
                if column_id != sg_task_column_id:
                    logger.debug("Index {}: DisplayRole".format(index))
                    row_data = self._tabledata[row_id][column_id]
                    logger.debug("RowData: {}".format(row_data))
                    return row_data

            elif role == Qt.DecorationRole:
                logger.debug("Index {}: DecorationRole".format(index))
                if column_id == name_column_id:
                    logger.info('testtttttttttttttttttttttttttttttttttttttttttttttttt')
                    p4_status = self._tabledata[row_id][p4_column_id]
                    logger.info("P4 Status: {}".format(p4_status))
                    icon = MtkExplorerPerforceStatusIconProvider.status_icon(p4_status)
                    logger.info(icon)
                    return icon

            elif role == Qt.TextAlignmentRole:
                logger.debug("Index {}: TextAlignmentRole".format(index))
                if column_id != name_column_id:
                    return int(Qt.AlignHCenter | Qt.AlignVCenter)

            else:
                logger.debug("Unsupported Role: {}".format(role))

        return None

    def headerData(self, section, orientation, role):
        logger.debug("Section: {0}, Orientation: {1}, Role: {2}".format(section, orientation, role))

        section_valid = 0 <= section < len(self._columndata)

        #if not section_valid:
        #    return None

        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._columndata[section]

        return None

    # 各セルのインタラクション
    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled

        sg_task_column_id = MtkExplorerFileModelColumn.SG_Task_Id()

        # this column contains a combobox.
        # it must be marked as editable.
        if index.column() == sg_task_column_id:
            return Qt.ItemIsEnabled | Qt.ItemIsEditable | Qt.ItemIsSelectable

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable