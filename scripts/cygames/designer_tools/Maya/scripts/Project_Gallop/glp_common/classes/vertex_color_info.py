# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
    from builtins import zip
    from importlib import reload
except Exception:
    pass

import maya.api.OpenMaya as om2

from ..utility import open_maya as om_utility

reload(om_utility)


class VertexColorInfo(object):
    """頂点カラー情報クラス

    頂点カラー情報クラスはそれぞれ、さらに細かい単位の頂点カラー情報クラスのリストを持つ
    VertexColorInfo > ObjectVertexColorInfo > VertexVertexColorInfo > VertexFaceVertexColorInfo
    頂点カラー自体はVertexFaceVertexColorInfoが持つ

    Attributes:
        info_list (list[ObjectVertexColorInfo]): オブジェクト単位の頂点カラー情報リスト
    """

    def __init__(self):

        self.info_list = []

    def create_info(self, target_list, color_set=''):
        """頂点カラー情報を作成する

        Args:
            target_list (OpenMaya.MSelectionList): 作成対象の選択リスト
            color_set (str): カラーセット名
        """

        vert_sel_list = om_utility.convert_to_vertex(target_list)

        info_dict = {}

        for sel_iter in om_utility.get_iter(om2.MItSelectionList(vert_sel_list)):
            dag_path, obj = sel_iter.getComponent()

            mesh_fn = om2.MFnMesh(dag_path)

            color_sets = mesh_fn.getColorSetNames()

            if not color_sets:
                continue

            if color_set and color_set not in color_sets:
                continue

            colors = mesh_fn.getFaceVertexColors()

            path = dag_path.fullPathName()

            if path not in list(info_dict.keys()):
                info_dict[path] = []

            for vert_iter in om_utility.get_iter(om2.MItMeshVertex(dag_path, obj)):

                index = vert_iter.index()
                face_and_facevert_indices = ((i, mesh_fn.getFaceVertexIndex(i, index, False)) for i in sorted(vert_iter.getConnectedFaces()))
                info_list = [VertexFaceVertexColorInfo(face, om2.MColor(colors[facevert])) for face, facevert in face_and_facevert_indices]

                info_dict[path].append(VertexVertexColorInfo(index, info_list))

        self.info_list = [ObjectVertexColorInfo(*item) for item in list(info_dict.items())]


class ObjectVertexColorInfo(object):
    """オブジェクト単位の頂点カラー情報クラス

    Attributes:
        dag_path (str): オブジェクトのDAGパス
        name (str): オブジェクト名
        info_list (list[VertexVertexColorInfo]): 頂点単位の頂点カラー情報リスト
    """

    def __init__(self, dag_path, info_list):
        """

        Args:
            dag_path (str): オブジェクトのDAGパス
            info_list (list[VertexVertexColorInfo]): 頂点単位の頂点カラー情報リスト
        """

        self.dag_path = dag_path
        self.name = dag_path.split('|')[-1]
        self.info_list = info_list

    def apply_to_mesh(self, color_set=''):
        """メッシュに頂点カラーを適用する

        Args:
            color_set (str): カラーセット名
        """

        if not self.info_list:
            return

        mesh_fn = om_utility.get_mfn_mesh(self.dag_path)

        color_sets = mesh_fn.getColorSetNames()

        if not color_sets:
            return

        if color_set:
            if color_set not in color_sets:
                return

            previous_color_set = mesh_fn.currentColorSetName()
            mesh_fn.setCurrentColorSetName(color_set)

        vertex_ids, face_ids, colors = zip(*((v.index, f.index, f.color) for v in self.info_list for f in v.info_list))
        mesh_fn.setFaceVertexColors(colors, face_ids, vertex_ids)

        if color_set:
            mesh_fn.setCurrentColorSetName(previous_color_set)


class VertexVertexColorInfo(object):
    """頂点単位の頂点カラー情報クラス

    Attributes:
        index (int): 頂点番号
        info_list (list[VertexFaceVertexColorInfo]): 頂点フェース単位の頂点カラー情報リスト
    """

    def __init__(self, index, info_list):
        """

        Args:
            index (int): 頂点番号
            info_list (list[VertexFaceVertexColorInfo]): 頂点フェース単位の頂点カラー情報リスト
        """

        self.index = index
        self.info_list = info_list


class VertexFaceVertexColorInfo(object):
    """頂点フェース単位の頂点カラー情報クラス

    Attributes:
        index (int): フェース番号
        color (OpenMaya.MColor): 頂点カラー
    """

    def __init__(self, index, color):
        """

        Args:
            index (int): フェース番号
            color (OpenMaya.MColor): 頂点カラー
        """

        self.index = index
        self.color = color
