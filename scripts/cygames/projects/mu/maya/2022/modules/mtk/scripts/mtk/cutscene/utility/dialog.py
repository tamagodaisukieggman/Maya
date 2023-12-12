# -*- coding: utf-8 -*-
"""Mayaのダイアログ回り"""
from __future__ import absolute_import as _absolute_import
from __future__ import division as _division
from __future__ import print_function as _print_function
from __future__ import unicode_literals as _unicode_literals

from maya import cmds


def select_folder(current_folder=None):
    """フォルダダイアログで選択する
    """
    if current_folder:
        dialog_result = cmds.fileDialog2(dialogStyle=1,
                                         caption="フォルダを選択",
                                         fileFilter="Folder",
                                         fileMode=3,
                                         startingDirectory=current_folder,
                                         )
    else:
        dialog_result = cmds.fileDialog2(dialogStyle=1,
                                         caption="フォルダを選択",
                                         fileFilter="Folder",
                                         fileMode=3,
                                         )

    if dialog_result is not None:
        return dialog_result[0]
    else:
        return ""


def show_error_dialog(title, message):
    cmds.confirmDialog(title=f"{title}", message=f"{message}")
