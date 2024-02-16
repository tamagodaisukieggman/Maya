# -*- coding: utf-8 -*-
"""HQ用の法線をUVに転送する機能"""
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function


import maya.api.OpenMaya as om
import maya.cmds as cmds


class HQNormalUVTransfer(object):
    """_normalモデルの法線情報をdstモデルに転送する機能
    """

    def __init__(self):
        self.__src_model = None
        self.__dst_model = None
        self.transfer_hq_uv_manager = None

    @property
    def src_model(self):
        return self.__src_model

    def setup(self, target_transfer_model, target_normal_model):
        """セットアップする
        """
        normal_model = HQNormalDataSearcher.fetch_normal_model(target_transfer_model)

        # _Normalが無かったら指定モデルを使う
        if normal_model == "":
            cmds.polyNormalPerVertex(target_normal_model, unFreezeNormal=True)
            cmds.polySoftEdge(target_normal_model, angle=180)
            normal_model = target_normal_model

        self.__src_model = normal_model
        self.__dst_model = target_transfer_model

        self.transfer_hq_uv_manager = TransferHQUVManager(target_transfer_model)

    def transfer_normal_to_uvset(self):
        """法線情報を別のメッシュの2つのUVセットに転写
        """

        # Current UVSetの記憶
        current_set = cmds.polyUVSet(self.__dst_model, q=True, currentUVSet=True)[0]

        self.transfer_hq_uv_manager.create()

        # 速度対策: Historyを削除
        cmds.delete(self.__dst_model, ch=True)
        # mel.eval("doBakeNonDefHistory( 1, {\"prePost\" });")

        # マージする頂点をSRC側、DST側共通のものとする
        merge_vertices = []
        src_merge_vertex_indices = self.get_shared_vertex_indices(self.__src_model)
        dst_merge_vertex_indices = self.get_shared_vertex_indices(self.__dst_model)

        for dst_index in dst_merge_vertex_indices:
            if dst_index in src_merge_vertex_indices:
                merge_vertices.append('{}.vtx[{}]'.format(self.__dst_model, dst_index))
                src_merge_vertex_indices.remove(dst_index)

        # UV縫い直し
        for uv_set in (self.transfer_hq_uv_manager.xy_uv.name, self.transfer_hq_uv_manager.zw_uv.name):
            cmds.polyUVSet(self.__dst_model, uvSet=uv_set, currentUVSet=True)
            cmds.polyMergeUV(merge_vertices, d=0.001)

        # 速度対策: Historyを削除
        cmds.delete(self.__dst_model, ch=True)
        # mel.eval("doBakeNonDefHistory( 1, {\"prePost\" });")

        self._transfer_uv()

        # Current UVSetを元に戻す
        cmds.polyUVSet(self.__dst_model, uvSet=current_set, currentUVSet=True)

    def _transfer_uv(self):
        """Source法線のベクター情報をDestinationの2つのUVSetに転送
        """
        src_selection = om.MGlobal.getSelectionListByName(self.__src_model)
        src_dagpath = src_selection.getDagPath(0)
        src_face_vertex_iter = om.MItMeshFaceVertex(src_dagpath)

        dst_selection = om.MGlobal.getSelectionListByName(self.__dst_model)
        dst_dagpath = dst_selection.getDagPath(0)
        dst_face_vertex_iter = om.MItMeshFaceVertex(dst_dagpath)
        dst_mesh_fn = om.MFnMesh(dst_dagpath)

        x_values = []
        y_values = []
        z_values = []

        index_normal = {}

        # 全ての面頂点から、法線の値と転写先のUVインデックスの組み合わせリストを作成
        while not src_face_vertex_iter.isDone():

            # 不正なメッシュだと転写先のUVが無い場合があるためそれを検知
            if not dst_face_vertex_iter.hasUVs():
                raise Exception("Face[{}]にUVが有りません".format(src_face_vertex_iter.faceId()))

            # 元の法線値
            normal = src_face_vertex_iter.getNormal()
            # 転写先のUVインデックス
            uv_indices = dst_face_vertex_iter.getUVIndex(uvSet=self.transfer_hq_uv_manager.xy_uv.name)

            # 組み合わせを記憶して次の面頂点へ
            index_normal[uv_indices] = normal
            src_face_vertex_iter.next()
            dst_face_vertex_iter.next()

        # 値セット用のリストを作成
        for index, normal in sorted(index_normal.items()):
            x_values.append(normal.x)
            y_values.append(normal.y)
            z_values.append(normal.z)
        w_values = len(x_values) * [1.0]

        # UV2/UV3に法線の値をセット
        dst_mesh_fn.setUVs(x_values, y_values, uvSet=self.transfer_hq_uv_manager.xy_uv.name)
        dst_mesh_fn.setUVs(z_values, w_values, uvSet=self.transfer_hq_uv_manager.zw_uv.name)

    @classmethod
    def set_current_uvset(cls, target_model, target_uvset):
        """uvsetのcurrentを設定
        """
        cmds.polyUVSet(target_model, uvSet=target_uvset, currentUVSet=True)

    @classmethod
    def get_shared_vertex_indices(cls, target_object_name):
        """共通頂点のindexを取得する

        ソフトエッジ化されている物はシェアされてるので、その検知用

        Args:
            target_object_name (str): オブジェクト名

        Returns:
            list: 「1L, 10L」などVertex番号のリスト
        """
        indices = []
        selection = om.MGlobal.getSelectionListByName(target_object_name)
        dagpath = selection.getDagPath(0)
        vertex_iter = om.MItMeshVertex(dagpath)

        while not vertex_iter.isDone():
            normals = vertex_iter.getNormals()
            if len(normals) == 1:
                indices.append(vertex_iter.index())
            else:
                n = om.MVector(round(normals[0].x, 4), round(normals[0].y, 4), round(normals[0].z, 4))
                for normal in normals[1:]:
                    if n != om.MVector(round(normal.x, 4), round(normal.y, 4), round(normal.z, 4)):
                        break
                else:
                    indices.append(vertex_iter.index())
            vertex_iter.next()
        return indices


# =====================================================================================
# HQUV関連
# =====================================================================================
class TransferHQUVManager(object):
    """転送用のHQUVマネージャー

    TransferHQUVを返す
    通常, xy, zwの順番を保証する
    """
    XY_UV_NAME = "____normal_xy"
    ZW_UV_NAME = "____normal_z"

    def __init__(self, target_model):
        self.__target_model = target_model
        self.__common = None
        self.__xy_uv = None
        self.__zw_uv = None

    @property
    def common(self):
        return self.__common

    @property
    def xy_uv(self):
        return self.__xy_uv

    @property
    def zw_uv(self):
        return self.__zw_uv

    def create(self):
        """作成する
        """
        # 最初にUVが一つか確認する
        uv_count = len(cmds.polyUVSet(self.__target_model, q=True, allUVSets=True))
        if 0 <= uv_count <= 2:
            if 1 == uv_count:
                TransferHQUVManager.create_dummy_uv(self.__target_model)
        else:
            raise("uvset数が規定の値になっていません。処理を終了します。")


        self.__common = cmds.polyUVSet(self.__target_model, q=True, allUVSets=True)[0]

        self.__xy_uv = TransferHQUV(self.__target_model, self.XY_UV_NAME)
        self.__zw_uv = TransferHQUV(self.__target_model, self.ZW_UV_NAME)

        # 生成後、3つか確認する
        TransferHQUVManager.check_uv_count(self.__target_model, 4)

    @classmethod
    def check_uv_count(cls, target_model, target_count):
        """UVの個数が正しいかチェックする

        Args:
            target_model (str): オブジェクト名
            target_count (int: 個数

        Returns:
            bool: 正しいか
        """
        uv_list = cmds.polyUVSet(target_model, q=True, allUVSets=True)
        if target_count == len(uv_list):
            return True
        else:
            raise Exception("現在の個数: {0}, 指定個数: {1}, 不正な状態です。".format(len(uv_list), target_count))
    
    @classmethod
    def create_dummy_uv(cls,target_model):
        copied_uvset = cmds.polyUVSet(target_model, copy=True)
        cmds.polyUVSet(target_model,rename=True, newUVSet="temp0", uvSet=copied_uvset[0])
        



class TransferHQUV(object):
    """転送用HQUV
    """

    def __init__(self, target_model_name, name):
        self.__target_model = target_model_name
        self.__name = name
        self.create()

    @property
    def name(self):
        return self.__name

    def create(self):
        if self.__exist_uvset():
            raise Exception("UVが重複しています")
        before_current_uv = cmds.polyUVSet(self.__target_model, query=True, currentUVSet=True)[0]

        cmds.polyUVSet(self.__target_model, uvSet=self.__name, create=True)
        cmds.polyUVSet(self.__target_model, uvSet=self.__name, currentUVSet=True)

        cmds.polyAutoProjection(self.__target_model)
        cmds.polyMapSew(self.__target_model)
        cmds.polyMapCut(self.__target_model)

        cmds.polyUVSet(self.__target_model, uvSet=before_current_uv, currentUVSet=True)

    def __exist_uvset(self):
        """UVSETが存在するかどうか
        """
        uvset_list = cmds.polyUVSet(self.__target_model, q=True, allUVSets=True)

        for cnt in range(0, len(uvset_list)):
            if uvset_list[cnt] == self.__name:
                return True
        return False


# =====================================================================================
# _Normal関連
# =====================================================================================
class HQNormalDataSearcher(object):
    """HQNormalデータの検索機能
    """
    HQNORMAL_NAME = "_Outline"

    @classmethod
    def fetch_normal_model(cls, prefix_name):
        if not cmds.objExists(prefix_name + cls.HQNORMAL_NAME):
            return ""

        return prefix_name + cls.HQNORMAL_NAME