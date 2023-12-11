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
import re

import maya.cmds as cmds
import maya.mel as mel

from ....base_common import utility as base_utility
from ....glp_common.classes.info import chara_info


class SetWeightMotion(object):

    def load_weight_motion(self, file_path):
        """
        """

        if not cmds.pluginInfo('fbxmaya', query=True, loaded=True):
            cmds.warning('FBXプラグインをロードしました')
            cmds.loadPlugin('fbxmaya.mll')

        if not os.path.exists(file_path):
            cmds.warning('該当のパスが存在しません {0}'.format(file_path))
            return

        # 初期化
        self.unload_weight_motion(file_path)

        position_node = self.get_position_node()
        if position_node is None:
            return

        current_time = cmds.currentTime(q=True)
        cmds.currentTime(0)

        referenced_file_path_list = self.check_exist_reference_file(file_path)
        if file_path not in referenced_file_path_list:
            cmds.file(file_path, reference=True, ns='SetWeightMotion')

        motion_position_node = 'SetWeightMotion:Position'
        if not cmds.objExists(motion_position_node):
            cmds.warning('モーション側のPositionノードが取得できません')
            return

        self.set_parent(position_node, motion_position_node, True)

        # 不要ノードのHide
        cmds.hide(cmds.ls(cmds.ls(referencedNodes=True), geometry=True))

        cmds.currentTime(current_time)

    def unload_weight_motion(self, file_path):
        """
        """

        selected = cmds.ls(sl=True)

        position_node = self.get_position_node()
        if position_node is None:
            return

        # コンストレインノードを全て削除して元のポーズに戻す
        position_child_node_list = cmds.listRelatives(position_node, ad=True, pa=True)
        if position_child_node_list:
            cmds.delete(position_child_node_list, cn=True)
        cmds.select(position_node)
        mel.eval('gotoBindPose;')

        # リファレンスが残っている場合はRemove
        referenced_file_path_list = self.check_exist_reference_file(file_path)
        if file_path in referenced_file_path_list:
            cmds.file(file_path, removeReference=True)

        if selected:
            cmds.select(selected)

    def check_exist_reference_file(self, file_path):
        """
        """

        return [referenced_file_path.replace('\\', '/') for referenced_file_path in cmds.file(q=True, r=True)]

    def get_position_node(self):

        _chara_info = chara_info.CharaInfo()
        _chara_info.create_info()
        if not _chara_info.exists:
            cmds.warning('キャラデータが取得できません')
            return None

        if not _chara_info.part_info.data_type.endswith('body') or _chara_info.part_info.is_mini:
            cmds.warning('キャラクターの種別が対象と異なります')
            return None

        root_node = _chara_info.part_info.root_node
        if not cmds.objExists(root_node):
            cmds.warning('root_nodeノードが取得できません')
            return None

        position_node = '{}|Position'.format(root_node)
        if not cmds.objExists(position_node):
            cmds.warning('Positionノードが取得できません')
            return None

        return root_node

    def set_parent(self, org_pos_node, tgt_pos_node, flg):

        org_joint_list = cmds.listRelatives(org_pos_node, ad=True, pa=True, type='joint')
        mot_joint_list = cmds.listRelatives(tgt_pos_node, ad=True, pa=True, type='joint')

        for org_joint in org_joint_list:
            org_joint_name = org_joint.split('|')[-1]
            target_mot_joint_list = [mot_joint for mot_joint in mot_joint_list if mot_joint.split(':')[-1] == org_joint_name]
            for target_mot_joint in target_mot_joint_list:
                if flg:
                    cmds.parentConstraint(target_mot_joint_list, org_joint_name, mo=True, decompRotationToChild=True)
                else:
                    cmds.parentConstraint(target_mot_joint_list, org_joint_name, rm=True)
