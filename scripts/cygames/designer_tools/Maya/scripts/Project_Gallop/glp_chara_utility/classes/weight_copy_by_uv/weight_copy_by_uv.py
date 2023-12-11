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
            base_utility.ui.dialog.open_ok('確認', '何も選択されていません')
            return

        if not base_utility.ui.dialog.open_ok_cancel('確認', 'ウェイト情報を取得しますか?'):
            return

        self.src_skin_info = base_class.mesh.skin_info.SkinInfo()
        self.src_skin_info.create_info(select_list)
        self.src_skin_info.update_uv_info()

        base_utility.ui.dialog.open_ok('確認', 'ウェイト情報を取得しました')

    # ==================================================
    def paste_weight_by_uv(self):

        if self.src_skin_info is None:
            base_utility.ui.dialog.open_ok('確認', 'ウェイト情報が見つかりません')
            return

        select_list = cmds.ls(sl=True, l=True, fl=True)

        if not select_list:
            base_utility.ui.dialog.open_ok('確認', '何も選択されていません')
            return

        if not base_utility.ui.dialog.open_ok_cancel('確認', 'ウェイトをペーストしますか?'):
            return

        self.dst_skin_info = base_class.mesh.skin_info.SkinInfo()
        self.dst_skin_info.create_info(select_list)
        self.dst_skin_info.update_uv_info()

        base_utility.mesh.skin.paste_weight_by_uv_position(self.src_skin_info, self.dst_skin_info)

        base_utility.ui.dialog.open_ok('確認', 'ウェイトをペーストしました')
