import os
import pathlib
import sys

from maya import cmds
import maya.OpenMaya as om

# path = r"Z:\mtk\tools\maya\2022\modules\mtk\scripts\mtk\file\new_checker"
# if path not in sys.path:
#     sys.path.insert(0, path)


from mtk.file.new_checker import EXT_DICT
from mtk.file.new_checker import CHARACTER_PATHS
from mtk.file.new_checker import ENV_PATHS
from mtk.file.new_checker import DATA_TYPES
from mtk.utils import getCurrentSceneFilePath


class SceneData:
    # パスオブジェクト
    path = ""
    # パスの文字列
    scene_name = ""
    # 拡張子をなくしたシーン名
    basename = ""
    # 拡張子
    ext = ""
    # mb ファイル、ma ファイルの判定
    type = None
    # chara, env, prop の判定
    data_type = ""
    # エラーコード
    error = None

    # バッチモード
    is_batch = False

    def __init__(self):
        self.set_scene_name()

        self.mtk_scene_type_check()
        self.mtk_scene_name_check()

    def get_scene_name(self):
        return self.scene_name

    def set_scene_name(self):
        """シーン名を取得
        cmds で取得できないシーンがあったのでOpenMayaでも取得を試みる
        ただし、OpenMayaの場合は開いていなくても文字列は空にならないので
        そのための対処
        """
        scene_name = str(getCurrentSceneFilePath())

        if not scene_name:
            scene_name = str(om.MFileIO.currentFile())

            split_name = scene_name.split(".")
            if len(split_name) == 1:
                scene_name = ""
            #     self.scene_name = ""
            #     self.error = "シーンが開かれていません"
            # else:
            #     self.scene_name = scene_name
        if not scene_name:
            self.scene_name = ""
            self.error = "シーンが開かれていません"
        else:
            scene_name = pathlib.Path(scene_name)
            self.path = scene_name
            self.scene_name = str(scene_name).replace(os.sep, '/')
            self.basename = scene_name.stem
            print(self.basename, self.basename[:4], " ---")
            self.ext = scene_name.suffix
            self.type = EXT_DICT.get(self.ext, None)
            self.is_batch = cmds.about(batch=True)

    def mtk_scene_name_check(self):
        """シーン名で確認が必要なもの

        プレフィックス: mdl_
        """
        if self.basename[:4] != "mdl_":
            self.error = "シーン名は「 mdl_ 」で始まるようにしてください"

    def mtk_scene_type_check(self):
        """チェック内容を変えるためにファイルパスからシーンのタイプを分類
        env, chara, prop
        """
        flag = None

        for _path in CHARACTER_PATHS:
            if _path in self.scene_name.lower():
                flag = DATA_TYPES["chara"]
                break

        for _path in ENV_PATHS:
            if _path in self.scene_name.lower():
                flag = DATA_TYPES["env"]
                break

        if flag == "chara" and "prop" in self.scene_name.lower():
            flag = DATA_TYPES["prop"]

        self.data_type = flag


class NodeDatas:

    root_nodes = []
    root_node_meshes = {}
    all_meshes = []
    mesh_material = {}
    material_textures = {}

    def __init__(self):
        self.root_nodes = []
        self.root_node_meshes = {}
        self.all_meshes = []
        self.mesh_material = {}
        self.material_textures = {}

        self.get_root_nodes()
        self.get_meshes()
        self.get_materials()
        self.get_textures()

    def get_root_nodes(self):
        root_nodes = cmds.ls(assemblies=True, long=True)
        nodes = [x for x in cmds.ls("mdl_*", type="transform", long=True)
                 if x in root_nodes and not cmds.listRelatives(x, shapes=True)]
        if nodes:
            self.root_nodes = nodes

    def get_meshes(self):
        if not self.root_nodes:
            return
        for node in self.root_nodes:
            meshes = cmds.listRelatives(node, allDescendents=True, fullPath=True, type="mesh")
            if meshes:
                meshes = [x for x in meshes
                          if x and not cmds.getAttr("{}.intermediateObject".format(x))]
            else:
                meshes = []
            self.all_meshes.extend(meshes)
            self.root_node_meshes[node] = meshes

    def get_materials(self):
        if not self.all_meshes:
            return

        for mesh in self.all_meshes:
            shading_engines = cmds.listConnections(mesh,
                                                   source=False,
                                                   destination=True,
                                                   type='shadingEngine')
            if not shading_engines:
                continue

            shading_engines = list(set(shading_engines))
            mats = []
            for sg in shading_engines:
                mat = cmds.listConnections(sg + '.surfaceShader')

                if mat and mat not in mats:
                    mats.append(mat[0])

            self.mesh_material[mesh] = mats

    def get_textures(self):
        if not self.mesh_material:
            return

        materials = self.mesh_material.values()

        for materials in self.mesh_material.values():
            for material in materials:
                _file_node = cmds.ls(cmds.listConnections(material,
                                                          source=True,
                                                          destination=False),
                                     type="file")
                if _file_node:
                    self.material_textures[material] = _file_node


class ResultData:

    # 例：mesh, node, scene
    # 元error_type
    category = ""

    # エラーの内容
    # 例：locked normal
    error = ""

    # 例：ヒストリーがある
    error_text = ""

    # データタイプ
    # 例：chara, env, prop
    data_type = ""

    # error node
    # 例：[pCylinder26]
    error_nodes = []

    def __init__(self, category="", error="", error_text="", data_type="", error_nodes=[]):
        self.category = category
        self.error = error
        self.error_text = error_text
        self.data_type = data_type
        self.error_nodes = list(error_nodes)

    def __repr__(self) -> str:
        # _m = f'-- CHECK_TYPE -- {self.data_type}, '
        # _m += f'-- TYPE -- {self.error_type}, '
        # _m += f'-- TEXT -- {self.error_text},\n'
        # _m += f'-- nodes -- {self.error_nodes}'

        return ", ".join(self.error_nodes)

    def get_error_nodes(self):
        return self.error_nodes


class ResultDatas:
    datas = []

    def __init__(self):
        self.datas = []

    def set_data_obj(self, obj):
        # ResultData を追加
        self.datas.append(obj)

    def set_data(self, category="", error="", error_text="", data_type="", error_nodes=[]):
        # 各要素からResultData で要素を追加
        if category:
            _data = ResultData(category, error, error_text, data_type, error_nodes)
            self.datas.append(_data)

    def is_exists_nodes(self, node_name):

        if node_name not in [str(x) for x in self.datas]:
            return None
        else:
            _id = [str(x) for x in self.datas].index(node_name)
            return self.datas[_id]

    def get_sort_data(self):
        # エラーのタイプでソート
        _new = []
        for x in self.datas:
            # 内容が ResultDatas の場合はさらに中を展開
            if isinstance(x, ResultDatas):
                for _ in x.datas:
                    if _.error_nodes:
                        _new.append(_)
            else:
                if x.error_nodes:
                    _new.append(x)

        return sorted(_new, key=lambda x: x.error)

    def __repr__(self) -> str:
        return self.datas

    def __len__(self):
        return len(self.datas)
