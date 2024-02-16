# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
except Exception:
    pass

from PySide2 import QtWidgets

import maya.cmds as cmds

from ....base_common import classes as base_class
from ....base_common import utility as base_utility


class WeightCopyByUv(object):

    def __init__(self):
        """
        """

        self.src_skin_info = None
        self.dst_skin_info = None

        # ==================================================
    def copy_weight_by_uv(self):

        select_list = cmds.ls(sl=True, l=True, fl=True)

        if not select_list:
            text = '何も選択されていません'
            QtWidgets.QMessageBox.information(None, '確認', text, QtWidgets.QMessageBox.Ok)
            return

        text = 'ウェイト情報を取得しますか?'
        buttons = QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
        result_button = QtWidgets.QMessageBox.question(None, '確認', text, buttons, QtWidgets.QMessageBox.Ok)
        if result_button != QtWidgets.QMessageBox.Ok:
            return

        self.src_skin_info = base_class.mesh.skin_info.SkinInfo()
        self.src_skin_info.create_info(select_list)
        self.src_skin_info.update_uv_info()

        text = 'ウェイト情報を取得しました'
        QtWidgets.QMessageBox.information(None, '確認', text, QtWidgets.QMessageBox.Ok)

    # ==================================================
    def paste_weight_by_uv(self):

        if self.src_skin_info is None:
            text = 'ウェイト情報が見つかりません'
            QtWidgets.QMessageBox.information(None, '確認', text, QtWidgets.QMessageBox.Ok)
            return

        select_list = cmds.ls(sl=True, l=True, fl=True)

        if not select_list:
            text = '何も選択されていません'
            QtWidgets.QMessageBox.information(None, '確認', text, QtWidgets.QMessageBox.Ok)
            return

        text = 'ウェイトをペーストしますか?'
        buttons = QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
        result_button = QtWidgets.QMessageBox.question(None, '確認', text, buttons, QtWidgets.QMessageBox.Ok)
        if result_button != QtWidgets.QMessageBox.Ok:
            return

        self.dst_skin_info = base_class.mesh.skin_info.SkinInfo()
        self.dst_skin_info.create_info(select_list)
        self.dst_skin_info.update_uv_info()

        base_utility.mesh.skin.paste_weight_by_uv_position(self.src_skin_info, self.dst_skin_info)

        text = 'ウェイトをペーストしました'
        QtWidgets.QMessageBox.information(None, '確認', text, QtWidgets.QMessageBox.Ok)
