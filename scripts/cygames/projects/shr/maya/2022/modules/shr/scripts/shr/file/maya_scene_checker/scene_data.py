import os
from pathlib import Path

from maya import cmds

from ...utils import getCurrentSceneFilePath
from . import settings

DEV_MODE = settings.load_config(config_name='DEV_MODE')
PROJECT = settings.load_config(config_name='PROJRCT_NAME')

class SceneData:
    """シーンパス取得

    Returns:
        _type_: _description_
    """
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
    data_type_category = ""
    # エラーコード
    error = None
    # バッチモード
    is_batch = False

    def __init__(self):
        self.set_scene_name()

    def __str__(self):
        return str(self.scene_name)

    def set_scene_name(self):
        """シーン名を取得
        cmds で取得できないシーンがあったのでOpenMayaでも取得を試みる
        ただし、OpenMayaの場合は開いていなくても文字列は空にならないので
        そのための対処
        """
        scene_name = str(getCurrentSceneFilePath())

        if scene_name == "None":
            self.scene_name = ""
            self.error = "Not Open Scene"
        else:
            scene_name = scene_name[0].lower() + scene_name[1:]
            scene_name = Path(scene_name)
            self.path = scene_name
            self.scene_name = str(scene_name).replace(os.sep, '/')
            self.basename = scene_name.stem
            self.ext = scene_name.suffix
            self.type = settings.load_config('MAYA_EXT').get(self.ext, None)
            self.is_batch = cmds.about(batch=True)
            self.set_asset_type()

    def set_asset_type(self):
        _data_type_category:str = ''
        for category in settings.load_config(f'{PROJECT.upper()}_ASSET_PATH'):
            for path in settings.load_config(f'{PROJECT.upper()}_ASSET_PATH')[category]:
                if str(self.scene_name).startswith(path):
                    _data_type_category = category
                    break
        if _data_type_category:
            self.data_type_category = _data_type_category
        else:
            self.data_type_category = 'Unknown'

    def mtk_scene_name_check(self):
        """シーン名で確認が必要なもの

        プレフィックス: mdl_
        """
        if self.basename[:4] != "mdl_":
            self.error = "シーン名は「 mdl_ 」で始まるようにしてください"


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

    def reset_cvs(self):
        if not self.all_meshes:
            return
        for mesh in self.all_meshes:
            _lattice = cmds.createNode("lattice", name="tempLattice", skipSelect=True)

    def get_root_nodes(self):
        _root_nodes = [x for x in cmds.ls(assemblies=True, long=True)if not cmds.listRelatives(x, children=True, fullPath=True, type="camera")]
        root_nodes = []
        ignore_nodes = []
        ignore_root_node_start_names = settings.load_config(config_name='IGNORE_ROOT_NODE_START_NAMES')

        for ignore_name in ignore_root_node_start_names:
            for root_node in _root_nodes:
                if root_node.startswith(ignore_name) and root_node not in ignore_nodes:
                    ignore_nodes.append(root_node)

        for root_node in _root_nodes:
            if root_node in ignore_nodes:
                continue
            root_nodes.append(root_node)

        self.root_nodes = root_nodes

    def get_meshes(self):
        if not self.root_nodes:
            return
        all_meshes = []
        for node in self.root_nodes:
            meshes = [x for x in cmds.listRelatives(node, allDescendents=True, fullPath=True, type="mesh")if 'polySurfaceShape' not in x]
            # if meshes:
            #     # 中間オブジェクトを排除
            #     meshes = [x for x in meshes
            #               if x and not cmds.getAttr("{}.intermediateObject".format(x))]
            # else:
            #     meshes = []
            if not meshes:
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

    # チェッカーのモジュール名
    # 例：delete_node
    checker_module = ""

    # UI に出力する際のエラータイプ名（モジュール名の_ がスペースになったもの）
    # 例：delete node
    error_type_message = ""

    # モジュールの一つ上のディレクトリ名
    # 例：scene
    checker_category = ""

    # エラーの内容
    # 例：locked normal
    error = ""
    error_type_color = [100, 100, 150]

    # 例：ヒストリーがある
    error_text = ""

    # データタイプ
    # 例：chara, env, prop
    data_type_category = ""

    # error node
    # 例：[pCylinder26]
    error_nodes = []

    # 修正対象
    modify_target = ""

    def __init__(self,
                    error_type_message="",
                    checker_module="",
                    checker_category="",
                    error_text="",
                    modify_target="",
                    data_type_category="",
                    error_nodes=[],
                    error_type_color=[]
                    ):

        self.error_type_message = error_type_message
        self.checker_module = checker_module
        self.checker_category = checker_category
        self.error_text = error_text
        self.modify_target = modify_target
        self.data_type_category = data_type_category
        self.error_nodes = list(error_nodes)
        if error_type_color:
            self.error_type_color = error_type_color

    def __repr__(self) -> str:
        # _m = f'-- CHECK_TYPE -- {self.data_type_category}, '
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

    def set_data(self, category="", error="", error_text="", modify_target="", data_type_category="", error_nodes=[], error_type_color=[]):
        # 各要素からResultData で要素を追加
        if category:
            _data = ResultData(category, error, error_text, modify_target, data_type_category, error_nodes, error_type_color)
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

    def __str__(self) -> str:
        return str(self.datas)

    def __repr__(self) -> list:
        return list(self.datas)

    def __len__(self):
        return len(self.datas)
