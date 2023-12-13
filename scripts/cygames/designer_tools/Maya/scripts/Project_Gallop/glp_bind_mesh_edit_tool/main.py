# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

from PySide2 import QtWidgets

from ..base_common.classes.mesh import skin_info
from . import view, bind_mesh_edit

# Maya 2022-
try:
    from builtins import object
    from importlib import reload
except Exception:
    pass

reload(skin_info)
reload(view)
reload(bind_mesh_edit)


class Main(object):

    def __init__(self):

        self.view = view.View()
        self.bind_mesh_edit_cls = bind_mesh_edit.BindMeshEdit()

    def show_ui(self):
        """UI表示
        """

        self.__set_ui_event()

        self.view.show()

    def __set_ui_event(self):
        """UIのclickedイベントやtriggeredイベントを設定する
        """

        self.view.ui.exec_devide_skinned_mesh_btn.clicked.connect(lambda: self.devide_skinned_mesh())
        self.view.ui.exec_merge_skinned_meshes_btn.clicked.connect(lambda: self.merge_skinned_meshes())

    def devide_skinned_mesh(self, should_show_message=True):
        """選択したメッシュのフェースをスキニングを維持したまま分割する
        """

        result = self.bind_mesh_edit_cls.devide_skinned_mesh()

        if should_show_message is False:
            return

        if result:
            QtWidgets.QMessageBox.information(None, '情報', '処理が完了しました')
        else:
            QtWidgets.QMessageBox.warning(None, '警告', '分割する為にはフェースで分割したいフェースを選択しておく必要があります')

    def merge_skinned_meshes(self, should_show_message=True):
        """選択したメッシュ同士をスキニング及びウェイトを維持したまま結合する
        """

        result = self.bind_mesh_edit_cls.merge_skinned_meshes()

        if should_show_message is False:
            return

        if result:
            QtWidgets.QMessageBox.information(None, '情報', '処理が完了しました')
        else:
            QtWidgets.QMessageBox.warning(None, '警告', '何も選択されていないか、選択したメッシュの中にバインドされていないメッシュが存在します')
