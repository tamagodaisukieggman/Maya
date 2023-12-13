# -*- coding: utf-8 -*-
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

from PySide2.QtWidgets import QWidget

from .ui import storyBoadrdRenderItems, storyBoadrdRenderItemsCheckBox


class ListWigetItemView(QWidget):

    def __init__(self, *args, **kwargs):
        super(ListWigetItemView, self).__init__(*args, **kwargs)

        self.gui = storyBoadrdRenderItems.Ui_Form()
        self.gui.setupUi(self)

        self.gui.isRender.stateChanged.connect(self.change_is_render)

    def change_is_render(self):
        is_render = self.gui.isRender.isChecked()
        if is_render:
            self.gui.frame.setEnabled(True)
            self.gui.clipName.setEnabled(True)
        else:
            self.gui.frame.setEnabled(False)
            self.gui.clipName.setEnabled(False)


class ListWigetItemCheckABoxView(QWidget):
    def __init__(self, *args, **kwargs):
        super(ListWigetItemCheckABoxView, self).__init__(*args, **kwargs)

        self.gui = storyBoadrdRenderItemsCheckBox.Ui_Form()
        self.gui.setupUi(self)
