def main():
    import os
    import sys

    # PySide6の上書き
    import PySide2
    from PySide2 import QtCore, QtGui, QtWidgets, support
    sys.modules["PySide6"] = PySide2
    sys.modules["PySide6.QtWidgets"] = QtWidgets
    sys.modules["PySide6.QtCore"] = QtCore
    sys.modules["PySide6.QtGui"] = QtGui
    sys.modules["PySide6.support"] = support

    # from .. import sequencer_lib
    # from ..sequencer_lib import log
    # from ..sequencer_lib import ed

    # sys.modules["cy"] = sequencer_lib
    # sys.modules["cy.log"] = log

    from . import detail

    mw: detail.MainWindow = detail.MainWindow()
    mw.resize(800, 600)
    mw.show()
