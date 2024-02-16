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


MIRROR_DIRECTION_LABELS = ['L → R', 'R → L']


class Main(main_template.Main):

    def __init__(self, main=None):
        """
        """

        super(self.__class__, self).__init__(main, os.path.basename(os.path.dirname(__file__)))

        self.tool_name = 'GlpCharaUtilityJointUtility'
        self.tool_label = 'ジョイントの設定'
        self.tool_version = '19112201'

        self.set_joint_orient_class = joint_utility.SetJointOrient()
        self.set_ear_joint_class = joint_utility.SetEarJoint()
        self.sp_mirror_class = joint_utility.SpMirror()
        self.sp_joint_counter_class = joint_utility.SpJointCounter()
        self.head_joint_mirror_class = joint_utility.HeadJointMirror()
        self.ear_joint_mirror_class = joint_utility.EarJointMirror()

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

        cmds.rowLayout(numberOfColumns=2, adjustableColumn2=2)

        self.mirror_direction_radio_button_grp = cmds.radioButtonGrp(nrb=2, la2=MIRROR_DIRECTION_LABELS, sl=1, cw2=[50, 50])

        form = cmds.formLayout()
        head_button = base_class.ui.button.Button('顔骨ミラー', self.__mirror_head_joints).ui_button_id
        ear_button = base_class.ui.button.Button('耳骨ミラー', self.__mirror_ear_joints).ui_button_id
        cmds.setParent('..')

        attach_positions = [(head_button, 'left', 0, 0), (head_button, 'right', 2, 50), (ear_button, 'left', 2, 50), (ear_button, 'right', 0, 100)]
        cmds.formLayout(form, e=True, attachPosition=attach_positions)
        cmds.setParent('..')

        cmds.separator()

        base_class.ui.button.Button(
            '特殊骨(Sp/Tp/Ex)の本数計測', self.sp_joint_counter_class.sp_joint_counter)

        cmds.setParent('..')

    def __mirror_head_joints(self):
        is_left_to_right = cmds.radioButtonGrp(self.mirror_direction_radio_button_grp, q=True, sl=True) == 1
        self.head_joint_mirror_class.mirror_head_joints(is_left_to_right)

    def __mirror_ear_joints(self):
        is_left_to_right = cmds.radioButtonGrp(self.mirror_direction_radio_button_grp, q=True, sl=True) == 1
        self.ear_joint_mirror_class.mirror_ear_joints(is_left_to_right)
