# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
    from builtins import zip
except Exception:
    pass

import maya.api.OpenMaya as om2

from . import utility

# base_common/classes/mesh/normal_info.py から分離 (normal_editor をbase_commonから切り離す)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class NormalInfo(object):

    # ==================================================
    def __init__(self):

        self.info_list = None

    # ==================================================
    def create_info(self, target_list, is_locked_vtx_only):

        vert_sel_list = utility.convert_to_vertex(target_list)

        info_dict = {}

        for sel_iter in utility.get_sel_iter(vert_sel_list):
            dag_path, obj = sel_iter.getComponent()

            mesh_fn = om2.MFnMesh(dag_path)
            vert_iter = om2.MItMeshVertex(dag_path, obj)

            while not vert_iter.isDone():

                if not is_locked_vtx_only or any(mesh_fn.isNormalLocked(i) for i in vert_iter.getNormalIndices()):

                    path = dag_path.fullPathName()

                    if path not in list(info_dict.keys()):
                        info_dict[path] = []

                    info_dict[path].append(VertexNormalInfo.create(vert_iter))

                vert_iter.next()

        self.info_list = [ObjectNormalInfo(*item) for item in list(info_dict.items())]

    # ==================================================
    def get_pair_list_by_name(self, src_info):

        if not src_info:
            return

        if not src_info.info_list:
            return

        if not self.info_list:
            return

        if len(src_info.info_list) == 1 and len(self.info_list) == 1:
            return [(src_info.info_list[0], self.info_list[0])]

        info_item_pair_list = []

        for dst_obj_info in self.info_list:
            for src_obj_info in src_info.info_list:
                if src_obj_info.name == dst_obj_info.name:
                    info_item_pair_list.append((src_obj_info, dst_obj_info))
                    break

        return info_item_pair_list


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ObjectNormalInfo(object):

    # ==================================================
    def __init__(self, dag_path, info_list):

        self.dag_path = dag_path
        self.name = dag_path.split('|')[-1]
        self.info_list = info_list

    # ==================================================
    def __str__(self):

        return 'dag_path: {}, info_list: {}'.format(
            self.dag_path,
            *self.info_list
        )

    def copy(self, info_list=None):

        return ObjectNormalInfo(self.dag_path, info_list if info_list is not None else self.info_list[:])

    # ==================================================
    def update(self, info_list):

        self.info_list = [dst.update(src) for src, dst in zip(info_list, self.info_list)]

    # ==================================================
    def get_command_arguments(self):
        """
        コマンドの引数として渡せるように変換した情報を返す

        Returns:
            (str, list[int], list[int], list[MVector]): メッシュ, 頂点ID, フェースID, 法線のタプル
        """

        if not self.info_list:
            return None

        sel_list = om2.MGlobal.getSelectionListByName(self.dag_path)

        if sel_list.isEmpty():
            return None

        vertex_ids = []
        face_ids = []
        normals = []

        for vert_info in self.info_list:
            for face_info in vert_info.info_list:
                vertex_ids.append(vert_info.index)
                face_ids.append(face_info.index)
                normals.append(face_info.normal)

        return self.dag_path, vertex_ids, face_ids, normals


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class VertexNormalInfo(object):

    # ==================================================
    def __init__(self, index, world_position, local_position, info_list):

        self.index = index
        self.world_position = world_position
        self.local_position = local_position
        self.info_list = info_list

    # ==================================================
    def __str__(self):

        return 'index: {}, world_position: {}, local_position: {}, info_list: {}'.format(
            self.index,
            self.world_position,
            self.local_position,
            self.info_list
        )

    # ==================================================
    def mirror(self, mirror_index, mirror_normal):

        world_position = om2.MPoint(self.world_position)
        local_position = om2.MPoint(self.local_position)

        info_list = self.info_list[:]

        if mirror_index is not None:
            world_position[mirror_index] *= -1
            local_position[mirror_index] *= -1

            if mirror_normal:
                info_list = [face_info.mirror(mirror_index) for face_info in info_list]

        return VertexNormalInfo(self.index, world_position, local_position, info_list)

    # ==================================================
    def update(self, vert_info):

        info_list = []

        src_len = len(vert_info.info_list)

        for i, dst_face_info in enumerate(self.info_list):
            src_face_info = vert_info.info_list[min(i, src_len - 1)]
            info_list.append(VertexFaceNormalInfo(dst_face_info.index, om2.MVector(src_face_info.normal)))

        return VertexNormalInfo(self.index, self.world_position, self.local_position, info_list)

    # ==================================================
    @classmethod
    def create(cls, vert_iter):

        index = vert_iter.index()
        world_position = vert_iter.position(om2.MSpace.kWorld)
        local_position = vert_iter.position(om2.MSpace.kObject)
        info_list = [VertexFaceNormalInfo(i, vert_iter.getNormal(i)) for i in sorted(vert_iter.getConnectedFaces())]

        return cls(index, world_position, local_position, info_list)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class VertexFaceNormalInfo(object):

    # ==================================================
    def __init__(self, index, normal):

        self.index = index
        self.normal = normal

    # ==================================================
    def __str__(self):

        return 'index: {}, normal: {}'.format(
            self.index,
            self.normal
        )

    # ==================================================
    def mirror(self, mirror_index):

        normal = om2.MVector(self.normal)

        normal[mirror_index] *= -1

        return VertexFaceNormalInfo(self.index, normal)
