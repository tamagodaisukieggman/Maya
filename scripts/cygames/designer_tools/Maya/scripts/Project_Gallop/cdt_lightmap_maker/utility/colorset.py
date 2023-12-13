# -*- coding: utf-8 -*-

from __future__ import absolute_import

try:
    # Maya 2022-
    from builtins import range
    from builtins import object
except Exception:
    pass

import maya.cmds as cmds
import maya.mel as mel

from . import common


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Method(object):

    # ===========================================
    @staticmethod
    def exist_colorset(target, target_colorset):

        if common.NodeMethod.get_mesh_shape(target) is None:
            return False

        colorset_list = cmds.polyColorSet(target, q=True, acs=True)

        if colorset_list is None:
            return False

        if len(colorset_list) == 0:
            return False

        for colorset in colorset_list:

            if colorset == target_colorset:
                return True

        return False

    # ===========================================
    @staticmethod
    def get_colorset_list(target):

        if common.NodeMethod.get_mesh_shape(target) is None:
            return []

        colorset_list = cmds.polyColorSet(target, q=True, acs=True)

        if colorset_list is None:
            return []

        if len(colorset_list) == 0:
            return []

        return colorset_list

    # ===========================================
    @staticmethod
    def search_colorset(target, target_colorset, fullmatch=True):

        if common.NodeMethod.get_mesh_shape(target) is None:
            return

        colorset_list = cmds.polyColorSet(target, q=True, acs=True)

        if colorset_list is None:
            return

        if len(colorset_list) == 0:
            return

        for colorset in colorset_list:

            if fullmatch:
                if colorset == target_colorset:
                    return colorset
            else:
                if colorset.find(target_colorset) >= 0:
                    return colorset

        return

    # ===========================================
    @staticmethod
    def get_colorset_index(target, target_colorset):

        if common.NodeMethod.get_mesh_shape(target) is None:
            return -1

        colorset_list = cmds.polyColorSet(target, q=True, acs=True)

        if colorset_list is None:
            return -1

        if len(colorset_list) == 0:
            return -1

        for cnt in range(0, len(colorset_list)):

            if colorset_list[cnt] == target_colorset:
                return cnt

        return -1

    # ===========================================
    @staticmethod
    def get_colorset_from_index(target, target_colorset_index):

        if common.NodeMethod.get_mesh_shape(target) is None:
            return

        colorset_list = cmds.polyColorSet(target, q=True, acs=True)

        if colorset_list is None:
            return

        if len(colorset_list) == 0:
            return

        for cnt in range(0, len(colorset_list)):

            if cnt == target_colorset_index:
                return colorset_list[cnt]

        return

    # ===========================================
    @staticmethod
    def get_current_colorset(target):

        if common.NodeMethod.get_mesh_shape(target) is None:
            return

        current_colorset = cmds.polyColorSet(
            target, q=True, currentColorSet=True)

        if current_colorset is None:
            return None

        if len(current_colorset) == 0:
            return None

        return current_colorset[0]

    # ===========================================
    @staticmethod
    def set_current_colorset(target, target_colorset):

        if not Method.exist_colorset(target, target_colorset):
            return

        if Method.get_current_colorset(target) == target_colorset:
            return

        cmds.polyColorSet(target, colorSet=target_colorset,
                          currentColorSet=True)

    # ===========================================
    @staticmethod
    def create_new_colorset(
            target,
            new_colorset_name,
            default_color=[1, 1, 1, 1]):

        if common.NodeMethod.get_mesh_shape(target) is None:
            return

        if Method.exist_colorset(target, new_colorset_name):
            return

        cmds.polyColorSet(target, colorSet=new_colorset_name,
                          cr=True, rpt="RGBA")

        Method.set_current_colorset(target, new_colorset_name)

        cmds.polyColorPerVertex(
            target,
            r=default_color[0],
            g=default_color[1],
            b=default_color[2],
            a=default_color[3],
            cdo=True)

    # ===========================================
    @staticmethod
    def delete_colorset(target, target_colorset):

        for p in range(0, 100):

            if not Method.exist_colorset(target, target_colorset):
                break

            cmds.polyColorSet(target, colorSet=target_colorset, d=True)

    # ===========================================
    @staticmethod
    def rename_colorset(target, target_colorset, new_colorset_name):

        if not Method.exist_colorset(target, target_colorset):
            return

        if Method.exist_colorset(target, new_colorset_name):
            return

        try:
            cmds.polyColorSet(target, colorSet=target_colorset,
                              nc=new_colorset_name, rn=True)
        except Exception:
            cmds.warning("{}：カラーセットのリネームに失敗しました".format(target_colorset))
            # TODO: self.tempValueが何なのか調べる
            self.tempValue = 0

    # ===========================================
    @staticmethod
    def blend_colorset(target, base_colorset, blend_colorset, blend_type):

        if not Method.exist_colorset(target, blend_colorset):
            return

        Method.create_new_colorset(target, base_colorset)

        if blend_type == "multiply":

            cmds.polyBlendColor(
                target, bcn=base_colorset,
                src=blend_colorset, dst=base_colorset, bfn=1, ch=False)

        elif blend_type == "add":

            cmds.polyBlendColor(
                target, bcn=base_colorset,
                src=blend_colorset, dst=base_colorset, bfn=2, ch=False)

        elif blend_type == "over":

            cmds.polyBlendColor(
                target, bcn=base_colorset,
                src=blend_colorset, dst=base_colorset, bfn=0, ch=False)

        elif blend_type == "sub":

            cmds.polyBlendColor(
                target, bcn=base_colorset,
                src=blend_colorset, dst=base_colorset, bfn=3, ch=False)

    # ===========================================
    @staticmethod
    def change_colorset_index(target, target_colorset, target_index):

        this_colorset_index = \
            Method.get_colorset_index(target, target_colorset)

        if this_colorset_index < 0:
            return

        if this_colorset_index == target_index:
            return

        this_dst_colorset = \
            Method.get_colorset_from_index(target, target_index)

        if this_dst_colorset is None:
            return

        cmds.delete(target, ch=True)

        temp_colorset_name = "____temp"

        Method.delete_colorset(target, temp_colorset_name)

        cmds.polyColorSet(target, cs=this_dst_colorset,
                          nc=temp_colorset_name, cp=True)

        Method.blend_colorset(target, this_dst_colorset,
                              target_colorset, "over")

        Method.blend_colorset(target, target_colorset,
                              temp_colorset_name, "over")

        Method.rename_colorset(target, target_colorset,
                               target_colorset + "____")
        Method.rename_colorset(target, this_dst_colorset,
                               this_dst_colorset + "____")

        Method.rename_colorset(target, target_colorset +
                               "____", this_dst_colorset)
        Method.rename_colorset(
            target, this_dst_colorset + "____", target_colorset)

        Method.delete_colorset(target, target_colorset + "____")
        Method.delete_colorset(target, this_dst_colorset + "____")

        Method.delete_colorset(target, temp_colorset_name)

        cmds.delete(target, ch=True)
