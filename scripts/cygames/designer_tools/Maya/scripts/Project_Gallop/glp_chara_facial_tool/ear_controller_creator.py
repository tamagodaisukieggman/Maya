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

import os

import maya.cmds as cmds
import maya.mel as mel


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class EarControllerCreator(object):

    # ===============================================
    def __init__(self):

        self.script_file_path = None
        self.script_dir_path = None

        self.rig_root = 'Rig_ear'

        self.rig_info_list = [
            {'rig_locator': 'Ear_01_L_Loc', 'joint': 'Ear_01_L', 'rig_controller': 'Ear_01_L_Ctrl', 'rig_orient_parent': 'Sp_He_Ear0_L_00'},
            {'rig_locator': 'Ear_02_L_Loc', 'joint': 'Ear_02_L', 'rig_controller': 'Ear_02_L_Ctrl'},
            {'rig_locator': 'Ear_03_L_Loc', 'joint': 'Ear_03_L', 'rig_controller': 'Ear_03_L_Ctrl'},
            {'rig_locator': 'Ear_01_R_Loc', 'joint': 'Ear_01_R', 'rig_controller': 'Ear_01_R_Ctrl', 'rig_orient_parent': 'Sp_He_Ear0_R_00'},
            {'rig_locator': 'Ear_02_R_Loc', 'joint': 'Ear_02_R', 'rig_controller': 'Ear_02_R_Ctrl'},
            {'rig_locator': 'Ear_03_R_Loc', 'joint': 'Ear_03_R', 'rig_controller': 'Ear_03_R_Ctrl'}
        ]

    # ===============================================
    def create(self):
        """
        リグ作成
        """

        self.__import_rig()
        self.__attach_rig()

    # ===============================================
    def __import_rig(self):
        """
        リグ(Rig_ear)をインポート
        """

        # 既存のリグがある場合はインポートしない
        if cmds.ls(self.rig_root):
            return

        self.script_file_path = os.path.abspath(__file__)
        self.script_dir_path = os.path.dirname(self.script_file_path)

        rig_file_path = self.script_dir_path + '/resource/rig_ear.ma'

        if not os.path.isfile(rig_file_path):
            return

        cmds.file(
            rig_file_path,
            i=True,
            ignoreVersion=True,
            rpr='_',
            mergeNamespacesOnClash=False,
            f=True
        )

    # ===============================================
    def __attach_rig(self):
        """
        リグをジョイントの位置に合わせ、ジョイントがリグを追従するようコンストレイントする
        """
        cmds.playbackOptions(min=0)
        cmds.currentTime(0)
        # -----------------------
        # 既存のコンストレイントがあれば削除
        for rig_info in self.rig_info_list:

            this_joint = rig_info.get('joint')
            this_joint = cmds.ls(this_joint, recursive=True, l=True)
            if len(this_joint) != 1:
                cmds.warning('耳のジョイントが無いか、複数見つかりました')
                return

            this_constraint_name = this_joint[0] + '_parentConstraint1'
            this_constraint_name = cmds.ls(this_constraint_name, recursive=True)
            if this_constraint_name:
                cmds.delete(this_constraint_name)

        # 耳のリグ(Rig_ear)を根本から先にかけてジョイントに設定
        for rig_info in self.rig_info_list:

            this_rig_loc = rig_info.get('rig_locator')
            this_joint = rig_info.get('joint')
            this_rig_ctrl = rig_info.get('rig_controller')
            this_rig_orient_parent = rig_info.get('rig_orient_parent')
            this_constraint_name = this_joint + '_parentConstraint1'

            # シーン内のネームスペース付きフルパスを取得
            this_rig_loc = cmds.ls(this_rig_loc, recursive=True, l=True)
            this_joint = cmds.ls(this_joint, recursive=True, l=True)
            this_rig_ctrl = cmds.ls(this_rig_ctrl, recursive=True, l=True)
            this_rig_orient_parent = cmds.ls(this_rig_orient_parent, recursive=True, l=True)

            if len(this_rig_loc) != 1:
                cmds.warning('リグのロケータが無いか、複数見つかりました')
                return
            if len(this_rig_ctrl) != 1:
                cmds.warning('リグのコントローラが無いか、複数見つかりました')
                return
            if len(this_joint) != 1:
                cmds.warning('耳のジョイントが無いか、複数見つかりました')
                return

            this_rig_loc = this_rig_loc[0]
            this_joint = this_joint[0]
            this_rig_ctrl = this_rig_ctrl[0]

            # バインドポーズに戻す
            cmds.select(this_joint, r=True)
            mel.eval('gotoBindPose;')

            # ロケータをジョイントの位置に移動
            joint_world_position = cmds.xform(this_joint, q=True, ws=True, t=True)
            cmds.xform(this_rig_loc, ws=True, t=joint_world_position)

            # RigLocatorのRotateに対応するjointのJointOrientの値を入れる
            # これまでAimConstraintで軸を合わせていたが、それだと合わないモデルが存在する
            # Sp_He_Ear0_L(R)_00のJointOrientをEar_01_L(R)_LocのOrientに入力すれば位置・軸は合うため
            # 確実性の高い後者の対応を行う
            if this_rig_orient_parent:
                joint_orient_value = cmds.joint(this_rig_orient_parent[0], q=True, orientation=True)
                cmds.xform(this_rig_loc, ws=True, rotation=joint_orient_value)

            cmds.parentConstraint(this_rig_ctrl, this_joint, name=this_constraint_name, maintainOffset=False, weight=1)
