# -*- coding: utf-8 -*-
"""headupdisplayのメインモジュール"""
from __future__ import absolute_import as _absolute_import
# from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

from maya import cmds
from mtk.utils import getCurrentSceneFilePath


class DebugHeadsUpDisplay(object):
    HUD_BASE_NAME = "DebugHeadUpDisplayHUD_"

    # TODO: Eventに紐づけて軽量化する。
    SHOW_HUD_SETTINGS = [
        {"object_name": "Frame",
         "label": "Frame:",
         "preset": "currentFrame"},
        {"object_name": "SceneName",
         "label": "Scenename:",
         "event": "SceneOpened",
         "command": "import os;os.path.splitext(os.path.basename(getCurrentSceneFilePath()))[0]"},
        {"object_name": "CutName",
         "label": "CutName:",
         "attachToRefresh": True,
         "command": "cmds.sequenceManager(query=True, currentShot=True)"},
        {"object_name": "FocalLength",
         "label": "FocalLength:",
         "attachToRefresh": True,
         "command": "import mtk.cutscene.utility as utility;str(cmds.getAttr(utility.panel.get_camera_from_focus_model_panel() + '.focalLength')) + 'mm'"},
    ]

    @classmethod
    def __fetch_appendable_blocks(cls, section_number):
        """追加可能な場所を取得する

        headsupDisplayはデフォルト、追加でいくらでも追加できる為、適用時に確認する必要がある

        :param section_number: section番号
        :type section_number: int
        :return: 追加可能なblock番号
        :rtype: int
        """
        return cmds.headsUpDisplay(nextFreeBlock=section_number)

    @classmethod
    def create_all(cls, request_hud_list):
        """HUDを全生成する

        :param request_hud_list: HUDリクエストリスト
        :type request_hud_list: OrderDict
        :raises ValueError: 存在しないHUDリクエストが来た時
        """
        cls.delete_all()

        for hud_name, section_number in request_hud_list.items():
            cls.__create_hud(hud_name, section_number)

    @classmethod
    def __get_hud_settings(cls, hud_name):
        """HUD名からHUD設定をとりだす

        :param hud_name: HUD名
        :type hud_name: str
        :return: HUD設定
        :rtype: dict
        """

        for settings in cls.SHOW_HUD_SETTINGS:
            if settings["object_name"] == hud_name:
                return settings

        return None

    @classmethod
    def delete_all(cls):
        """Debug用HUDを削除する
        """
        for hud in cls.SHOW_HUD_SETTINGS:
            if cmds.headsUpDisplay(hud["object_name"], exists=True):
                cmds.headsUpDisplay(hud["object_name"], rem=1)

    @classmethod
    def __create_hud(cls, hud_name, section_number):
        # 単体で生成する
        hud_settings = cls.__get_hud_settings(hud_name)

        if hud_settings is None:
            raise ValueError("不正な値")

        if not cmds.headsUpDisplay(hud_settings["object_name"], exists=True):
            can_appendable_block = cls.__fetch_appendable_blocks(section_number)

            cls.__create_command(hud_settings, section_number, can_appendable_block)

    @classmethod
    def __create_command(cls, settings, section, block):
        """UI生成コマンド

        :param settings: HUD設定
        :type settings: dict
        :param section: MayaのHUDを表示するセクション番号
        :type section: int
        :param block: Mayaのセクション内のブロック番号
        :type block: int
        :return: HUD名
        :rtype: str
        """
        object_name = settings["object_name"]

        send_kwargs = settings.copy()
        del send_kwargs["object_name"]

        # 固定値を追加
        send_kwargs["allowOverlap"] = True
        send_kwargs["section"] = section
        send_kwargs["block"] = block
        send_kwargs["blockSize"] = "small"
        send_kwargs["labelFontSize"] = "large"
        send_kwargs["labelWidth"] = 100
        send_kwargs["dataWidth"] = 50
        send_kwargs["dataFontSize"] = "large"
        send_kwargs["dataAlignment"] = "left"
        send_kwargs["blockAlignment"] = "left"

        cmds.headsUpDisplay(object_name, **send_kwargs)

        return object_name

    @classmethod
    def is_show(cls):
        for hud in cls.SHOW_HUD_SETTINGS:
            if cmds.headsUpDisplay(hud["object_name"], exists=True):
                return True

        return False
