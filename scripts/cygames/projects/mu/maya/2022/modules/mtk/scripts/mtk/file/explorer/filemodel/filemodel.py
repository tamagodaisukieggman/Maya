import os
import glob
import re
from datetime import datetime
from distutils.util import strtobool

from PySide2.QtCore import Qt
from PySide2.QtGui import (
    QStandardItemModel,
    QStandardItem,
    QIcon
)
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

import logging
logger = logging.getLogger(__name__)


class MtkExplorerFileModel(QStandardItemModel):

    def __init__(self, *args, **kwargs):
        u"""init"""
        if len(args) > 1:
            rows, columns = args[0], args[1]
        else:
            rows, columns = 0, 0

        super(MtkExplorerFileModel, self).__init__(
            rows, columns, parent=kwargs.setdefault('parent', None),
        )

        self._view = kwargs.setdefault('view', None)

        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        self._icon_none = QIcon('{}/images/perforce/status/none.png'.format(base_path))
        self._icon_add = QIcon('{}/images/perforce/status/add.png'.format(base_path))
        self._icon_checkout = QIcon('{}/images/perforce/status/checkout.png'.format(base_path))
        self._icon_other = QIcon('{}/images/perforce/status/other.png'.format(base_path))
        self._icon_latest = QIcon('{}/images/perforce/status/latest.png'.format(base_path))
        self._icon_stale = QIcon('{}/images/perforce/status/stale.png'.format(base_path))
        self.action_icon = {
            'add': self._icon_add,
            'other': self._icon_other,  # 他人のチェックアウト
            'checkout': self._icon_checkout,
            'stale': self._icon_stale,
            'latest': self._icon_latest,
            'none': self._icon_none,
        }

        # must insert the columns before setting header labels
        self.insertColumn(0)
        self.insertColumn(1)
        self.insertColumn(2)
        self.insertColumn(3)

        self._set_header_labels()

    @property
    def root_path(self):
        u"""getter"""
        return self._root_path

    @root_path.setter
    def root_path(self, value):
        u"""settter"""
        self._root_path = value

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

    def _set_header_labels(self):
        u"""Header Labelの設定"""
        self.setHorizontalHeaderLabels(('Name', 'Rev', 'Date Modified', 'P4 Status'))

    def _terminates(self):
        if MODE != 'MAYA':
            return False

        global_vars = mel.eval('env')
        if (
            '$g_mtk_explorer_escape' in global_vars
            and strtobool(mel.eval('global int $g_mtk_explorer_escape;$temp=$g_mtk_explorer_escape;'))
          ):
            return True
        else:
            return False

    def set_cells(self):
        u"""Cellの設定"""
        if MODE == 'MAYA':
            mel.eval('global int $g_mtk_explorer_escape;$g_mtk_explorer_escape=false;')

        self._set_header_labels()
        file_paths = self._get_resource_paths(self._root_path)
        if not file_paths:
            if MODE == 'MAYA':
                mel.eval('global int $g_mtk_explorer_escape;$g_mtk_explorer_escape=true;')
            return

        file_status = MtkP4.status(file_paths)
        logger.debug('Search (Start): {}'.format(self._root_path))
        for i, (file_path, status) in enumerate(file_status.items()):
            QApplication.processEvents()

            if self._terminates():
                logger.debug('Search (Terminate): {}'.format(self._root_path))
                return

            # 0 (Name)
            name = os.path.basename(file_path)
            icon = self.action_icon[status['action']] if status['action'] else self._icon_none
            name_item = QStandardItem(icon, name)
            self.setItem(i, 0, name_item)

            # 1 (Rev)
            rev_item = QStandardItem('{}/{}'.format(status['haveRev'], status['headRev']))
            rev_item.setTextAlignment(Qt.AlignHCenter)
            self.setItem(i, 1, rev_item)

            # 2 (Date Modified)
            dt = datetime.fromtimestamp(os.stat(file_path).st_mtime)
            stamp = dt.strftime('%Y/%m/%d %H:%M:%S')
            stamp_item = QStandardItem(stamp)
            stamp_item.setTextAlignment(Qt.AlignHCenter)
            self.setItem(i, 2, stamp_item)

            # 3 (P4 Status)
            status_item = QStandardItem('{}'.format(status['action']))
            status_item.setTextAlignment(Qt.AlignHCenter)
            self.setItem(i, 3, status_item)

            # logger.debug('{}: {}'.format(i, file_path))

        logger.debug('Search (End): {}'.format(self._root_path))

        if MODE == 'MAYA':
            mel.eval('global int $g_mtk_explorer_escape;$g_mtk_explorer_escape=true;')