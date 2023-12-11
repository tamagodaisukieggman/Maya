# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
    from importlib import reload
except Exception:
    pass

import maya.cmds as cmds

from ....base_common import utility as base_utility
from ....base_common import classes as base_class

from ....glp_common.classes.info import chara_info

from ..general_costume_blend_shape import general_costume_blend_shape

reload(chara_info)
reload(general_costume_blend_shape)


# ==================================================
def bind_to_all_child_joints():

    select_transform_list = cmds.ls(sl=True, l=True, fl=True, et='transform')

    if not select_transform_list:
        return

    select_joint_list = cmds.ls(sl=True, l=True, fl=True, et='joint')

    if not select_joint_list:
        return

    bind_skin = BindSkin()
    bind_skin.set_transform_list(select_transform_list)
    bind_skin.set_joint_list(select_joint_list, True)
    bind_skin.exec_bind()


# ==================================================
def rebind_skin():

    if not base_utility.ui.dialog.open_ok_cancel('確認', 'スキンをリバインドしますか ?\n※ヒストリーが消えます'):
        return

    select_list = cmds.ls(sl=True, l=True, fl=True, typ='transform')

    if not select_list:
        return

    rebind_skin = RebindSkin()
    rebind_skin.set_transform_list(select_list)
    rebind_skin.exec_rebind()


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BindSkin(object):
    """バインド
    """

    # ==================================================
    def __init__(self):

        self.transform_list = None
        self.joint_list = None

        self.is_check_maximun_inf = False
        self.bind_method_int = 0
        self.max_influence_int = 2
        self.should_remove_unused_inf = False
        self.skin_method_int = 0

    # ==================================================
    def set_transform_list(self, transform_list):

        if not transform_list:
            return

        result_transform_list = cmds.ls(transform_list, l=True, fl=True, et='transform')

        if not result_transform_list:
            return

        self.transform_list = result_transform_list

    # ==================================================
    def set_joint_list(self, joint_list, should_search_all_child=True):

        if not joint_list:
            return

        result_joint_list = cmds.ls(joint_list, l=True, fl=True, et='joint')

        if not result_joint_list:
            return

        if not should_search_all_child:

            self.joint_list = result_joint_list

        else:

            self.joint_list = self.__get_all_child_joint(result_joint_list)

    # ==================================================
    def __get_all_child_joint(self, org_joint_list):

        result_joint_list = []

        if not org_joint_list:
            return result_joint_list

        for joint in org_joint_list:

            tmp_joint_list = [joint]

            child_joint_list = cmds.listRelatives(joint, ad=True, fullPath=True, type='joint')

            if child_joint_list:
                tmp_joint_list.extend(child_joint_list)

            for tmp_joint in tmp_joint_list:

                if tmp_joint in result_joint_list:
                    continue

                result_joint_list.append(tmp_joint)

        return result_joint_list

    # ==================================================
    def exec_bind(self):

        if not self.transform_list or not self.joint_list:
            return

        for transform in self.transform_list:

            connection_node_list = cmds.listHistory(transform)
            skinCluster_list = cmds.ls(connection_node_list, typ='skinCluster')

            if skinCluster_list:
                continue

            cmds.skinCluster(
                transform,
                self.joint_list,
                obeyMaxInfluences=self.is_check_maximun_inf,
                bindMethod=self.bind_method_int,
                maximumInfluences=self.max_influence_int,
                removeUnusedInfluence=self.should_remove_unused_inf,
                skinMethod=self.skin_method_int)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class RebindSkin(object):
    """リバインド
    """

    # ==================================================
    def __init__(self):

        self.transform_list = None

    # ==================================================
    def set_transform_list(self, transform_list):

        if not transform_list:
            return

        result_transform_list = cmds.ls(transform_list, l=True, fl=True, et='transform')

        if not result_transform_list:
            return

        self.transform_list = result_transform_list

    # ==================================================
    def exec_rebind(self):

        if not self.transform_list:
            return

        for transform in self.transform_list:

            skin_root_joint = base_utility.mesh.skin.get_skin_root_joint(transform)

            if skin_root_joint is None:
                continue

            skin_info = base_class.mesh.skin_info.SkinInfo()
            skin_info.create_info([transform])

            bind_skin = BindSkin()
            bind_skin.set_transform_list([transform])
            bind_skin.set_joint_list([skin_root_joint], True)
            target_joints = bind_skin.joint_list

            target_skin_cluster = base_utility.mesh.skin.get_skin_cluster(transform)
            is_check_maximun_inf = cmds.skinCluster(
                target_skin_cluster, q=True, obeyMaxInfluences=True)

            bind_skin.is_check_maximun_inf = is_check_maximun_inf

            cmds.delete(transform, ch=True)

            bind_skin.exec_bind()

            target_skin_info = base_class.mesh.skin_info.SkinInfo()
            target_skin_info.create_info([transform])

            base_utility.mesh.skin.paste_weight_by_vertex_index(
                skin_info, target_skin_info
            )

            bind_pose_list = cmds.dagPose(skin_root_joint, q=True, bp=True)

            if len(bind_pose_list) > 1:

                cmds.delete(bind_pose_list)
                cmds.dagPose(target_joints, bp=True, selection=True, save=True)

        blend_shape = general_costume_blend_shape.GeneralCostumeBlendShape()
        blend_shape.create_general_costume_blend_shape()
