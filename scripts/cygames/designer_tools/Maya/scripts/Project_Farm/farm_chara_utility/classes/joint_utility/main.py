# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os

import maya.cmds as cmds

from ....base_common import classes as base_class

from . import joint_utility
from .. import main_template


class Main(main_template.Main):

    def __init__(self):
        """
        """

        super(self.__class__, self).__init__(os.path.basename(os.path.dirname(__file__)))

        self.tool_name = 'FarmCharaUtilityJointUtility'
        self.tool_label = 'ジョイントの設定'
        self.tool_version = '19112201'

        self.set_joint_orient_class = joint_utility.SetJointOrient()
        self.set_ear_joint_class = joint_utility.SetEarJoint()
        self.sp_mirror_class = joint_utility.SpMirror()
        self.sp_joint_counter_class = joint_utility.SpJointCounter()

    def ui_body(self):
        """
        UI要素のみ
        """

        cmds.columnLayout(adjustableColumn=True, rs=5)

        base_class.ui.button.Button(
            'Joint Orientを設定(ZYX / YUP / weight対応版)', self.set_joint_orient_class.set_joint_orient)

        base_class.ui.button.Button(
            '尻尾のOrientを設定', self.set_joint_orient_class.set_tail_orient)

        base_class.ui.button.Button(
            '耳の方向をOrient方向に変更', self.set_ear_joint_class.set_ear_joint)

        base_class.ui.button.Button(
            'Axisの表示切替(toggle式)', self.set_joint_orient_class.toggle_rotate_axis)

        base_class.ui.button.Button(
            'Sp骨(Ear以外)ミラーリング', self.sp_mirror_class.sp_mirror)

        cmds.separator()

        base_class.ui.button.Button(
            'Sp骨の本数計測', self.sp_joint_counter_class.sp_joint_counter)

        cmds.setParent('..')
