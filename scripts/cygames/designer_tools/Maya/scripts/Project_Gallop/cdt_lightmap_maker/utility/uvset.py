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

    # ===============================================
    @staticmethod
    def exist_uvset(target, target_uvset):

        if common.NodeMethod.get_mesh_shape(target) is None:
            return False

        uvset_list = cmds.polyUVSet(target, q=True, allUVSets=True)

        if uvset_list is None:
            return False

        if len(uvset_list) == 0:
            return False

        for cnt in range(0, len(uvset_list)):

            if uvset_list[cnt] == target_uvset:
                return True

        return False

    # ===============================================
    @staticmethod
    def get_uvset_index(target, target_uvset):

        if common.NodeMethod.get_mesh_shape(target) is None:
            return -1

        uvset_list = cmds.polyUVSet(target, q=True, allUVSets=True)

        if uvset_list is None:
            return -1

        if len(uvset_list) == 0:
            return -1

        for cnt in range(0, len(uvset_list)):

            if uvset_list[cnt] == target_uvset:
                return cnt

        return -1

    # ===============================================
    @staticmethod
    def get_uvset_from_index(target, target_index):

        if common.NodeMethod.get_mesh_shape(target) is None:
            return

        uvset_list = cmds.polyUVSet(target, q=True, allUVSets=True)

        if uvset_list is None:
            return

        if len(uvset_list) == 0:
            return

        for cnt in range(0, len(uvset_list)):

            if cnt == target_index:
                return uvset_list[cnt]

    # ===============================================
    @staticmethod
    def set_current_uvset(target, target_uvset):

        if not Method.exist_uvset(target, target_uvset):
            return

        cmds.polyUVSet(target, uvSet=target_uvset, cuv=True)

    # ===============================================
    @staticmethod
    def set_current_uvset_from_index(target, target_index):

        target_uv = Method.get_uvset_from_index(target, target_index)

        if target_uv is None:
            return

        Method.set_current_uvset(target, target_uv)

    # ===============================================
    @staticmethod
    def create_new_uvset(target, target_uvset):

        if Method.exist_uvset(target, target_uvset):
            return

        cmds.polyUVSet(target, uvSet=target_uvset, create=True)

    # ===============================================
    @staticmethod
    def delete_uvset(target, target_uvset):

        if not Method.exist_uvset(target, target_uvset):
            return

        Method.set_current_uvset(target, target_uvset)

        cmds.polyUVSet(target, uvSet=target_uvset, delete=True)

    # ===============================================
    @staticmethod
    def rename_uvset(target, target_uvset, new_uvset_name):

        if not Method.exist_uvset(target, target_uvset):
            return

        if Method.exist_uvset(target, new_uvset_name):
            return

        cmds.polyUVSet(target, uvSet=target_uvset,
                       newUVSet=new_uvset_name, rn=True)

    # ===============================================
    @staticmethod
    def change_uvset_index(target, target_uvset, target_index):

        this_uvset_index = Method.get_uvset_index(target, target_uvset)

        if this_uvset_index < 0:
            return

        if this_uvset_index == target_index:
            return

        cmds.delete(target, ch=True)

        this_dst_uvset = Method.get_uvset_from_index(target, target_index)

        if this_dst_uvset is None:
            return

        temp_uvset_name = "____temp"

        Method.delete_uvset(target, temp_uvset_name)

        cmds.polyUVSet(target, uvSet=this_dst_uvset,
                       newUVSet=temp_uvset_name, cp=True)

        cmds.polyCopyUV(target, uvi=target_uvset, uvs=this_dst_uvset, ch=False)
        cmds.polyCopyUV(target, uvi=temp_uvset_name,
                        uvs=target_uvset, ch=False)

        Method.rename_uvset(target, target_uvset, target_uvset + "____")
        Method.rename_uvset(target, this_dst_uvset, this_dst_uvset + "____")

        Method.rename_uvset(target, target_uvset + "____", this_dst_uvset)
        Method.rename_uvset(target, this_dst_uvset + "____", target_uvset)

        Method.delete_uvset(target, target_uvset + "____")
        Method.delete_uvset(target, this_dst_uvset + "_____")

        Method.delete_uvset(target, temp_uvset_name)

        cmds.delete(target, ch=True)
