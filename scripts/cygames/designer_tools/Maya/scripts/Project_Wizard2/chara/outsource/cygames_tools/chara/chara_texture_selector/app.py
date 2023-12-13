import os
import re
import typing as tp
from pathlib import Path
import maya.cmds as cmds


class MaterialGetter:
    @classmethod
    def _get_mesh_shape(cls,obj):
        """選択したオブジェクトからshapeを取得する

        Returns:
            str: shape
        """
        # 選択されたオブジェクトをループしてshapeノードを取得
        if cmds.objectType(obj, isType="transform"):
            shapes = cmds.listRelatives(obj, children=True, shapes=True)
            if shapes:
                for shape in shapes:
                    if cmds.objectType(shape, isType="mesh"):
                        return shape

    @classmethod
    def get_face_assigned_material(cls) -> tp.List[str]:
        """選択したフェースからアサインされているマテリアルを取得
        get_object_assigned_materialsにあわせてlistで返す


        Returns:
            tp.List[str]: material
        """
        materials = []
        selected_objects = cmds.ls(sl=True)
        face = selected_objects[0]
        shading_groups = cmds.listConnections(face, type="shadingEngine")
        if shading_groups:
            materials = cmds.ls(cmds.listConnections(shading_groups), materials=True)
            return materials[0]
    
    @classmethod
    def get_object_assigned_materials(cls):
        """選択したオブジェクトからアサインされているマテリアルを取得

        Returns:
            tp.List[str]: material
        """
        selected_objects = cmds.ls(sl=True)
        target_shapes = []
        for lp in selected_objects:
            target_shapes.append(cls._get_mesh_shape(lp))
        materials = []
        #for shape in target_shapes:
        shading_groups = cmds.listConnections(target_shapes, type='shadingEngine')
        materials = cmds.ls(cmds.listConnections(shading_groups, destination=False, source=True), materials=True)

        return list(set(materials))

class TextureSelector:
    def __init__(self,target_material:str):
        self.current_index = 0
        self.material:str = target_material
        self.texture_paths = {}
        self.initialize()
    
    def _get_current_scene_info(self):
        "開いているシーンの各情報を取り出す"
        path = Path(cmds.file(q=True,sn=True))

        texture_dir = Path(str(path.parent.parent)+"/sourceimages")
        material_id = self.material.replace("mt_","")
        return {"file_path":path.parent,"file_name":path.stem,"tex_dir":texture_dir,"material_id":material_id}


    def _get_current_textures(self):
        rtn_tgas = []
        info = self._get_current_scene_info()
        tgas = info["tex_dir"].glob(f'**/*{str(info["material_id"])}*.tga')
        for lp in tgas:
            rtn_tgas.append(lp)
        return rtn_tgas

    def _get_current_material_texture(self):
        # マテリアルのbaseColorを取得
        base_color_attr = '{}.color'.format(self.material)

        # baseColorに接続されているファイルノードを取得
        file_node = cmds.listConnections(base_color_attr, destination=True, source=True)
        texture_path = cmds.getAttr('{}.fileTextureName'.format(file_node[0]))
        return texture_path

    def initialize(self):
        
        self.texture_paths.clear()
        for texture_path in self._get_current_textures():
            three_digit_numbers = self._find_three_digit_numbers(os.path.basename(str(texture_path)))
            self.texture_paths[three_digit_numbers] = texture_path
        

    def change_base_color_texture_by_path(self, texture_path):
        """指定されたマテリアルのbase colorのテクスチャを変更する関数
        Args:
            material_name (str): 変更するマテリアルの名前
            texture_path (str): 新しいテクスチャのファイルパス
        Returns:
            bool: テクスチャの変更が成功した場合はTrue、失敗した場合はFalse
        """

        # マテリアルのbaseColorを取得
        base_color_attr = '{}.color'.format(self.material)

        # baseColorに接続されているファイルノードを取得
        file_node = cmds.listConnections(base_color_attr, destination=True, source=True)

        if file_node:
            # ファイルノードのテクスチャパスを更新
            cmds.setAttr('{}.fileTextureName'.format(file_node[0]), texture_path, type="string")
        else:
            # 新しいファイルノードを作成し、テクスチャパスを設定
            file_node = cmds.shadingNode('file', asTexture=True)
            cmds.setAttr('{}.fileTextureName'.format(file_node), texture_path, type="string")

            # ファイルノードをマテリアルのbaseColorに接続
            cmds.connectAttr('{}.outColor'.format(file_node), base_color_attr)

        return True

    def change_base_color_texture_by_index(self,three_digit_numbers:str):
        """３桁のindexの文字列からテクスチャを切り替え"""
        texture_path = self.texture_paths[three_digit_numbers]
        self.change_base_color_texture_by_path(texture_path)
    
    def _find_three_digit_numbers(self,text):
        """文字列から3桁の数字を取得する関数

        Args:
            text (str): 検索対象の文字列

        Returns:
            list: 3桁の数字が格納されたリスト
        """
        pattern = re.compile(r'.*(\d{3}).*')
        result = re.search(pattern, text)
        return result.groups()[0]

    def set_texture_by_index(self,index:str):
        """indexの番号のテクスチャを設定

        Args:
            index (str): 番号を入れる
        """
        self.change_base_color_texture_by_path(self.texture_paths[index])
