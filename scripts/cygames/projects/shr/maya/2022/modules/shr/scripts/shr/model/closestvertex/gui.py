# -*- coding: utf-8 -*-
u"""クロースドバーテクッス(GUI)
"""

import os

import command
from mtku.maya.base.window import BaseWindow
from mtku.maya.utils.decoration import undo_redo


class ClosestVertex(BaseWindow):

    def __init__(self, *args, **kwargs):
        dirpath = os.path.dirname(__file__)
        self._closestvertex_ui = None
        self._closestvertex_file = '{0}/closestvertex.ui'.format(dirpath)

        super(ClosestVertex, self).__init__(*args, **kwargs)
        self.url = 'https://wisdom.cygames.jp/pages/viewpage.action?pageId=30420068'

    def create(self):
        u"""Windowのレイアウト作成"""
        # レイアウト生成
        self._add_layout()
        # UIとコマンドの接続
        self._connect()

    def _add_layout(self):
        self._closestvertex_ui = self.load_file(self._closestvertex_file)

    def _connect(self):
        self._closestvertex_ui.set_button.clicked.connect(self.click_set_target)
        self._closestvertex_ui.run_button.clicked.connect(self.click_vertex)
        self._closestvertex_ui.run_button2.clicked.connect(self.click_surface)

    def click_set_target(self):
        target = command.get_mesh()
        self._closestvertex_ui.text_field.setText(target)

    @undo_redo(False)
    def click_vertex(self):
        name = self._closestvertex_ui.text_field.text()
        command.run_vertex(name)

    @undo_redo(False)
    def click_surface(self):
        name = self._closestvertex_ui.text_field.text()
        command.run_surface(name)
