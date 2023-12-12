from PySide2.QtCore import QDir
from PySide2.QtWidgets import QFileSystemModel

class MtkExplorerDirModel(QFileSystemModel):

    def __init__(self, *args, **kwargs):
        super(MtkExplorerDirModel, self).__init__(parent=kwargs.setdefault('parent', None))

        self.setFilter(QDir.Dirs | QDir.NoDotAndDotDot)