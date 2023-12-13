"""cySzkのWorkFiler関連のクラス
"""

import maya.cmds as cmds
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

from .zexplorer import MtkExplorer
from .settings import MtkExplorerSettings
import logging

logger = logging.getLogger(__name__)


class MtkExplorerForMaya(MayaQWidgetDockableMixin, MtkExplorer):

    name = 'MtkExplorerForMaya'
    _label = 'MtkExplorer'

    def __init__(self, *args, **kwargs):
        u"""init"""
        super(MtkExplorerForMaya, self).__init__(parent=kwargs.setdefault('parent', None))
        self._boot = True
        self._typ = 2

        # self.setObjectName(self.object_name)
        self.setWindowTitle(self._label)

        self._start_root = MtkExplorerSettings.defaultWorkPath()

        self._set_show_option()
        self._boot = False

    def _set_show_option(self, *args, **kwargs):
        u"""show"""
        logger.debug('{}:Read Settings'.format(self.name))

        # Bookmark
        if cmds.optionVar(exists=self.key_bookmarks):
            bookmarks = cmds.optionVar(q=self.key_bookmarks).split(',')
            self.bookmark.reload(bookmarks)

        # Category
        if cmds.optionVar(exists=self.key_category):
            self.category.pulldown.setCurrentIndex(int(cmds.optionVar(q=self.key_category)))

        # Address Bar
        if cmds.optionVar(exists=self.key_root_path):
            self._start_root = cmds.optionVar(q=self.key_root_path)
        self.address_bar.textbox.setText(self._start_root)
