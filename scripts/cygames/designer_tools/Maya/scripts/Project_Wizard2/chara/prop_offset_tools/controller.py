# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

import os
import maya.cmds as cmds

from .view import View
from .app import PropOffsetManager


class PropOffsetController:
    def __init__(self):
        self.ui = View()  # QMainWindow
        self.setup_ui()
        self.update_prop_offset_manager()

    def update_prop_offset_manager(self):
        """prop_offsetの管理オブジェクトの更新"""
        asset_type = self.ui.gui.type_cmbbox.currentText()
        print(asset_type)
        self.prop_offset_manager = PropOffsetManager(asset_type)

    def setup_ui(self):
        self.ui.gui.offset_btn.clicked.connect(self.clicked_offset_btn)
        self.ui.gui.create_offset_btn.clicked.connect(self.clicked_create_offset_btn)
        self.ui.gui.type_cmbbox.currentIndexChanged.connect(
            self.update_prop_offset_manager
        )

    def clicked_offset_btn(self):
        self.prop_offset_manager.reset_transform()

    def clicked_create_offset_btn(self):
        self.prop_offset_manager.create_offset()

    def show_ui(self):
        self.ui.show()

    def close_ui(self):
        self.ui.close()
