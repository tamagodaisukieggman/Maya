# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os

import maya.cmds as cmds

from . import set_weight_motion
from .. import main_template

from ....base_common import classes as base_class


class Main(main_template.Main):

    SVN_WEIGHT_MOTION_DIR_PATH = 'W:/gallop/svn/svn_gallop/80_3D/03_motion/00_scenes/weight_mot'
    WEIGHT_MOTION_FILE_NAME = 'weight_mot.fbx'

    def __init__(self, main=None):
        """
        """

        super(self.__class__, self).__init__(main, os.path.basename(os.path.dirname(__file__)))

        self.tool_name = 'GlpSetSampleMotion'
        self.tool_label = 'モーション流し込み'
        self.tool_version = '20110201'

        self.set_weight_motion = set_weight_motion.SetWeightMotion()

        self.weight_motion_file_path = os.path.join(
            self.SVN_WEIGHT_MOTION_DIR_PATH,
            self.WEIGHT_MOTION_FILE_NAME).replace('\\', '/')

    def ui_body(self):
        """
        UI要素のみ
        """

        cmds.frameLayout(l='呼び出すモーションファイル名', cll=0, cl=0, bv=1, mw=5, mh=5)
        cmds.columnLayout(adjustableColumn=True, rs=4)
        base_class.ui.button.Button(
            self.WEIGHT_MOTION_FILE_NAME,
            self.set_weight_motion.load_weight_motion,
            self.weight_motion_file_path)
        cmds.setParent('..')
        cmds.setParent('..')
        base_class.ui.button.Button(
            'モーションリセット(コンストレインリセット&リファレンス削除)',
            self.set_weight_motion.unload_weight_motion,
            self.weight_motion_file_path)
