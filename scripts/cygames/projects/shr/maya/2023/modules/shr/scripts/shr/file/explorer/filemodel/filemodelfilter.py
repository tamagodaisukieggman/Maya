from PySide2.QtCore import QSortFilterProxyModel

import logging
logger = logging.getLogger(__name__)

from .filemodelcolumn import MtkExplorerFileModelColumn

class MtkExplorerFileSortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(MtkExplorerFileSortFilterProxyModel, self).__init__(parent)

        self.filterString = ''
        self.filterFunctions = {}
        self.setDynamicSortFilter(True)

    def setFilterString(self, new_filter):
        self.filterString = new_filter
        self.invalidateFilter()

    def addFilterFunction(self, name, new_func):
        self.filterFunctions[name] = new_func
        self.invalidateFilter()

    def removeFilterFunction(self, name):
        if name in self.filterFunctions.keys():
            del self.filterFunctions[name]
            self.invalidateFilter()

    # filter function. RegExp name filter + P4 status filter
    def filterAcceptsRow(self, row_id, parent):
        """filter function. (file name filter + P4 status filter)"""

        logger.debug("RowId: {}".format(row_id))

        model = self.sourceModel()
        name_result = True
        p4_result = True

        name_column_id = MtkExplorerFileModelColumn.Name_Id()
        p4_column_id = MtkExplorerFileModelColumn.P4_Status_Id()

        # filter by name
        name_item = model.item(row_id, name_column_id)
        name_text = ""
        if name_item is not None:
            name_text = name_item.text()
            name_result = self.filterRegExp().indexIn(name_text) >= 0
            logger.debug("Name Text:{}, RegExp Result:{}".format(name_text, name_result))
        else:
            logger.debug("Name Item is None.")

        # filter by p4 status
        p4_item = model.item(row_id, p4_column_id)
        p4_text = ""
        if p4_item is not None:
            p4_text = p4_item.text()
            p4_result = self.filterString in p4_text

        tests = [name_result, p4_result]

        return not False in tests