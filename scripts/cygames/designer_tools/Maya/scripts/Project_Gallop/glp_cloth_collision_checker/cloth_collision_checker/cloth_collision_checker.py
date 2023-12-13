# -*- coding: utf-8 -*-
"""
ClothコリジョンのMaya用チェッカー
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os

import maya.cmds as cmds

from ...base_common import classes as base_class
from .. import checker_ui_referer
from .. import check_item_param_list
from . import cloth_collision_checker_item_list
from ... import glp_common
from ...glp_common.classes.info import chara_info

try:
    # Maya2022-
    from importlib import reload
except Exception:
    pass

reload(checker_ui_referer)
reload(check_item_param_list)
reload(cloth_collision_checker_item_list)
reload(glp_common)


class ClothCollisionChecker(checker_ui_referer.CheckerUIReferer):
    """
    """

    def __init__(self, is_internal=False):
        """
        """
        super(ClothCollisionChecker, self).__init__()

        # ツール名
        self.tool_name = 'gallopClothCollisionChecker'
        # version
        self.tool_version = '20022601'

        # キャラインフォ
        self.chara_info = chara_info.CharaInfo()
        self.chara_info.create_info(is_create_all_info=True)

        # チェックアイテムの一覧
        self.check_item_list = cloth_collision_checker_item_list.ClothCollisionCheckerItemList(self).check_item_list

        # チェックアイテムのパラメータ一覧
        check_item_param_list_cls = check_item_param_list.CheckItemParamList()
        check_item_param_list_cls.set_check_item_param_list(self.check_item_list)
        self.check_item_param_list = check_item_param_list_cls.check_item_param_list

        self.dir_path = ''
        self.file_name_filter = ''
        self.file_name_ignore_filter = ''
        self.is_exec_child_dir = False
        self.log_save_dir_path = ''

        self.key_dir_path = self.tool_name + 'DirPath'
        self.key_file_name_filter = self.tool_name + 'FileNameFilter'
        self.key_file_name_ignore_filter = self.tool_name + 'FileNameIgnoreFilter'
        self.key_is_exec_child_dir = self.tool_name + 'IsExecChildDir'
        self.key_log_save_dir_path = self.tool_name + 'LogSaveDirPath'

        self.setting = None

        # 外注用かどうか
        self.is_internal = is_internal

        # このスクリプト自身のパス、ディレクトリ
        self.script_file_path = os.path.abspath(__file__)
        self.script_dir_path = os.path.dirname(self.script_file_path)

        self.batch_cmd_str = '{0}{1}'.format(
            'import Project_Gallop.glp_cloth_collision_checker.cloth_collision_checker.cloth_collision_checker;',
            'Project_Gallop.glp_cloth_collision_checker.cloth_collision_checker.cloth_collision_checker.ClothCollisionChecker().batch_exec();'
        )

    # ------------------------------------------------------------

    def _load_setting(self, *args, **keywords):
        """
        XMLから変数のデータをLoad
        """

        self.dir_path = self.setting.load(self.key_dir_path, default_value='')
        self.file_name_filter = self.setting.load(self.key_file_name_filter, default_value='')
        self.file_name_ignore_filter = self.setting.load(self.key_file_name_ignore_filter, default_value='')
        self.is_exec_child_dir = self.setting.load(self.key_is_exec_child_dir, 'bool', False)
        self.log_save_dir_path = self.setting.load(self.key_log_save_dir_path, default_value='')

    # ------------------------------------------------------------

    def _save_setting(self, *args, **keywords):
        """
        XMLに変数のデータをSave
        """

        self.setting.save(self.key_dir_path, self.dir_path)
        self.setting.save(self.key_file_name_filter, self.file_name_filter)
        self.setting.save(self.key_file_name_ignore_filter, self.file_name_ignore_filter)
        self.setting.save(self.key_is_exec_child_dir, self.is_exec_child_dir)
        self.setting.save(self.key_log_save_dir_path, self.log_save_dir_path)

    # ------------------------------------------------------------

    def initialize(self):
        """
        """

        self.setting = base_class.setting.Setting(self.tool_name)
        self._load_setting()

        return True

    # ------------------------------------------------------------

    def delayedInitialize(self):
        """
        delayedInitialize オーバーロード
        """

        self.change_scene_event()

    # ------------------------------------------------------------

    def change_scene(self):
        """
        シーンが開いた時の挙動
        """

        file_path = cmds.file(q=True, sn=True)

        if file_path:
            # self.chara_info = chara_path_utility.CharaPathInfo()
            self.chara_info = chara_info.CharaInfo()
            self.chara_info.create_info(file_path, is_create_all_info=True)

        self.reset_ui()

    # ------------------------------------------------------------

    def create_ui_batch_check_part(self):
        """
        """

        if self.is_internal:
            container = super(ClothCollisionChecker, self).create_ui_batch_check_part()

        else:
            container = cmds.columnLayout()
            cmds.setParent('..')

        return container

    # ------------------------------------------------------------

    def change_scene_event(self):
        """
        ファイルを開いたときにフックするScriptJob
        """

        cmds.scriptJob(p=self.window_name, e=("SceneOpened", self.change_scene))

    # ------------------------------------------------------------

    def exec_cmd_initialize(self):
        """
        関数実行前処理
        """

        file_path = cmds.file(q=True, sn=True)

        if not file_path:
            return False

        # self.chara_info = chara_path_utility.CharaPathInfo()
        self.chara_info = chara_info.CharaInfo()
        self.chara_info.create_info(file_path, is_create_all_info=True)

        # if not self.chara_info.data_type:
        if not self.chara_info.exists:
            return False

        return True

    # ------------------------------------------------------------

    def batch_exec_initialize(self):
        """
        バッチ処理実行前処理
        """

        self.initialize()
