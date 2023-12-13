# -*- coding: utf-8 -*-
u"""menu.py"""
import os
import sys

import maya.cmds as cmds
import maya.mel as mel


class CygamesMenu(object):
    # メニュー名
    menu_name = 'Cygames'

    @classmethod
    def _add_items(cls):
        u"""メニューアイテムの追加"""
        # Modeling
        cmds.menuItem(l='Chara', sm=True, to=True, p=cls.menu_name)
        cmds.menuItem(
            l=u'キャラユーティリティ',
            c='from importlib import reload;import chara_utility.main;reload(chara_utility.main);chara_utility.main.main();',
        )
        cmds.menuItem(
            l=u'法線ツール',
            c='from importlib import reload;import normal_editor.main;reload(normal_editor.main);normal_editor.main.main();',
        )

    @classmethod
    def main(cls):
        u"""Menu"""
        g_main_window = mel.eval('$temp=$gMainWindow')
        if cmds.menu(cls.menu_name, q=True, ex=True):
            cls.menu = cmds.menu(cls.menu_name, e=True, dai=True, to=True)
        else:
            cls.menu = cmds.menu(
                cls.menu_name,
                l=cls.menu_name,
                p=g_main_window,
                to=True,
            )
        # Add menu items
        cls._add_items()
        cmds.setParent('..', menu=True)
        cmds.setParent('..')

        # # バッチ起動ではなくMayaのscriptフォルダに置く場合、以下のコメントを外して使ってください
        # # scriptsフォルダ直下にmenu.pyとuserSetup.pyを置いてもらう
        # chara_module_path = os.path.join(os.path.dirname(__file__), 'chara')
        # chara_module_path = chara_module_path.replace('/', '\\')
        # found_tool_path = False
        # for path in sys.path:
        #     if path == chara_module_path:
        #         found_tool_path = True
        #         break
        # if not found_tool_path:
        #     sys.path.append(chara_module_path)
