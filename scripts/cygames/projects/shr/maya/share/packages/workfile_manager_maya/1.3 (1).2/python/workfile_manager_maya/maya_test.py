from Qt import QtWidgets, QtCore, QtGui
#import qdarkstyle_rev
from maya.app.general import mayaMixin

class Delegate(QtWidgets.QItemDelegate):
    def paint(self, painter, option, index):
        opt = QtWidgets.QStyleOptionComboBox()
        opt.rect = option.rect
        opt.currentText = 'test'
        #opt.text = 'text'
        QtWidgets.QApplication.style().drawComplexControl(QtWidgets.QStyle.CC_ComboBox, opt, painter)
        QtWidgets.QApplication.style().drawControl(QtWidgets.QStyle.CE_ComboBoxLabel, opt, painter)

        


    def createEditor(self, parent, option, index):
        combo = QtWidgets.QComboBox(parent)
        combo.addItems(['Test', 'Test2'])
        return combo

class Table(QtWidgets.QTableView):
    def __init__(self):
        super(Table, self).__init__()
        dg = Delegate(self)
        self.setItemDelegate(dg)

class TableModel(QtCore.QAbstractItemModel):
    def __init__(self):
        super(TableModel, self).__init__()
        self.m_column_count = 3
        self.m_data = [[1,2,3], [4,5,6]]

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.m_data)

    def columnCount(self, parent=None, *args, **kwargs):
        return self.m_column_count

    def flags(self, index):
        return (QtCore.Qt.ItemIsEditable) | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def data(self, index, role=None):
        #if self.m_data[index.row()] is None:
        #    return None
        if role == QtCore.Qt.DisplayRole:
            return self.m_data[index.row()][index.column()]
        elif role == QtCore.Qt.EditRole:
            return self.m_data[index.row()][index.column()]

        return None

    def index(self, row, column, parent=QtCore.QModelIndex(), *args, **kwargs):
        if self.hasIndex(row,column,parent):
            return self.createIndex(row,column,self.m_data[row])
        return QtCore.QModelIndex()

    def parent(self, index=None):
        return QtCore.QModelIndex()


class MainWindow(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

def show():
    mwin = MainWindow()
    w = QtWidgets.QWidget(mwin)
    

    vbox = QtWidgets.QVBoxLayout()
    tbl = Table()
    model = TableModel()
    tbl.setModel(model)
    vbox.addWidget(tbl)

    w.setLayout(vbox)

    mwin.setCentralWidget(w)
    mwin.show()
    
    