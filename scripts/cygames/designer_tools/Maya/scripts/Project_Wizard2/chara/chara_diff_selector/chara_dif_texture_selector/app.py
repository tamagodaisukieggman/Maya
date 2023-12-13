import os
import re
import typing as tp
from pathlib import Path
import maya.cmds as cmds


# from .data import TextureInfo
from abc import ABC, abstractmethod

from . import utility as texture_selector_utils


class MaterialGetter:
    @classmethod
    def _get_mesh_shape(cls, obj):
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
        # for shape in target_shapes:
        shading_groups = cmds.listConnections(target_shapes, type="shadingEngine")
        materials = cmds.ls(
            cmds.listConnections(shading_groups, destination=False, source=True),
            materials=True,
        )

        return list(set(materials))


class TextureSelectorBase:
    def __init__(self, **kwargs):
        self.target_material = kwargs["target_material"]
        self.diff_datas = {}
        self.texture_type = kwargs["texture_type"]
        self.initialize_diff_datas()

    @abstractmethod
    def initialize_diff_datas(self):
        ...
    
    @abstractmethod
    def get_default_indexes(self):
        ...

    def set_default_indexes(self):
        indexes = self.get_default_indexes()
        self.set_texture_path(indexes)

    @abstractmethod
    def get_texture_path(self, current_diff_data: dict):
        ...

    @abstractmethod
    def set_texture_path(self, current_diff_data: dict):
        ...

    def set_texture_path_by_model_index(self,model_index:str):
        for diff_data in self.diff_datas:
            if diff_data["model_diff_indexes"] == model_index:
                is_set_texture_success = self.set_texture_path(diff_data)
                if is_set_texture_success:
                    cmds.warning("テクスチャが存在しません")
                return
        
    def set_texture_type(self,texture_type:str):
        """suffixに当たるテクスチャの種類をtexture_typeで上書き

        Args:
            texture_type (str): テクスチャの種類 "decal" "base"など
        """
        self.texture_type = texture_type

    def get_current_textures(self) -> tp.List[str]:
        """現在の対象となるテクスチャパスを全て取得

        Args:
            ext (str, optional): 拡張子 . Defaults to "decal".

        Returns:
            tp.List[str]: テクスチャパスの配列
        """
        tgas = self.sourceimages_path.glob(f"**/*{self.material_id}*{self.texture_type}.tga")
        return tgas

    def change_base_color_texture_by_path(self, texture_path):
        """指定されたマテリアルのbase colorのテクスチャを変更する関数
        Args:
            material_name (str): 変更するマテリアルの名前
            texture_path (str): 新しいテクスチャのファイルパス
        Returns:
            bool: テクスチャの変更が成功した場合はTrue、失敗した場合はFalse
        """

        # マテリアルのbaseColorを取得
        base_color_attr = "{}.color".format(self.target_material)

        # baseColorに接続されているファイルノードを取得
        file_node = cmds.listConnections(base_color_attr, destination=True, source=True)

        if file_node:
            # ファイルノードのテクスチャパスを更新
            cmds.setAttr(
                "{}.fileTextureName".format(file_node[0]), texture_path, type="string"
            )
        else:
            # 新しいファイルノードを作成し、テクスチャパスを設定
            file_node = cmds.shadingNode("file", asTexture=True)
            cmds.setAttr(
                "{}.fileTextureName".format(file_node), texture_path, type="string"
            )

            # ファイルノードをマテリアルのbaseColorに接続
            cmds.connectAttr("{}.outColor".format(file_node), base_color_attr)

        return True


class CommonTextureSelector(TextureSelectorBase):
    def __init__(self, **kwargs):
        target_material = kwargs["target_material"]

        self.material_id = kwargs["parts_id"]
        self.sourceimages_path = texture_selector_utils.get_current_sourceimages_dir(
            target_material
        )
        super().__init__(**kwargs)

    def initialize_diff_datas(self):
        diff_datas = []
        textures = self.get_current_textures()
        diff_data = {}
        for texture in textures:
            texture_str = texture.as_posix()
            texture_diff_index = self._find_three_digit_numbers(texture_str)
            diff_data["texture_path"] = texture_str
            diff_data["texture_diff_indexes"] = texture_diff_index
            diff_datas.append(diff_data.copy())
        self.diff_datas = diff_datas
    
    def get_default_indexes(self):
        diff_data = self.diff_datas[0].copy()
        return diff_data

    def get_texture_path(self, current_diff_data: dict):
        ...

    def set_texture_path(self, current_diff_data: dict):
        current_texture_path = None
        for key in current_diff_data:
            for diff_data in self.diff_datas:
                if current_diff_data[key] == diff_data[key]:
                    current_texture_path = diff_data["texture_path"]
        if current_texture_path:
            self.change_base_color_texture_by_path(current_texture_path)
            return True
        else:
           return False

    def _find_three_digit_numbers(self, text):
        """文字列から3桁の数字を取得する関数

        Args:
            text (str): 検索対象の文字列

        Returns:
            list: 3桁の数字が格納されたリスト
        """
        pattern = re.compile(r"_.*(\d{3})_.*")
        result = re.search(pattern, text)
        return result.groups()[0]

class FaceTextureSelector(TextureSelectorBase):
    def __init__(self, **kwargs):
        target_material = kwargs["target_material"]
        self.material_id = kwargs["parts_id"]
        if "_mouth" in self.material_id or "_eye" in self.material_id :
            suffix = self.material_id.rsplit("_")[-1]
            material_id = self.material_id.rsplit("_",1)[0]
            self.material_id = f"{material_id}*_{suffix}"
        self.sourceimages_path = texture_selector_utils.get_current_sourceimages_dir(
            target_material
        )
        super().__init__(**kwargs)

    def initialize_diff_datas(self):
        diff_datas = []
        textures = self.get_current_textures()
        diff_data = {}
        for texture in textures:
            texture_str = texture.as_posix()
            texture_diff_index = self._find_three_digit_numbers(texture_str)
            diff_data["texture_path"] = texture_str
            diff_data["texture_diff_indexes"] = texture_diff_index
            diff_datas.append(diff_data.copy())
        self.diff_datas = diff_datas
    
    def get_default_indexes(self):
        diff_data = self.diff_datas[0].copy()
        return diff_data

    def get_texture_path(self, current_diff_data: dict):
        ...

    def set_texture_path(self, current_diff_data: dict):
        current_texture_path = None
        for key in current_diff_data:
            for diff_data in self.diff_datas:
                if current_diff_data[key] == diff_data[key]:
                    current_texture_path = diff_data["texture_path"]
        if current_texture_path:
            self.change_base_color_texture_by_path(current_texture_path)
            return True
        else:
           return False

    def _find_three_digit_numbers(self, text):
        """文字列から3桁の数字を取得する関数

        Args:
            text (str): 検索対象の文字列

        Returns:
            list: 3桁の数字が格納されたリスト
        """
        pattern = re.compile(r"_.*(\d{3})_.*")
        result = re.search(pattern, text)
        return result.groups()[0]


class HairTextureSelector(TextureSelectorBase):

    def __init__(self, **kwargs: str):
        target_material = kwargs["target_material"]
        self.material_id = kwargs["parts_id"]
        self.sourceimages_path = texture_selector_utils.get_current_sourceimages_dir(
            target_material
        )
        super().__init__(**kwargs)


    def initialize_diff_datas(self):
        diff_datas = []
        textures = self.get_current_textures()
        diff_data = {}
        for texture in textures:
            texture_str = texture.as_posix()
            texture_diff_index = self._find_three_digit_numbers(texture_str)
            model_diff_index = self._find_two_digit_numbers(texture_str)

            diff_data["texture_path"] = texture_str
            diff_data["model_diff_indexes"] = model_diff_index
            diff_data["texture_diff_indexes"] = texture_diff_index

            diff_datas.append(diff_data.copy())
        self.diff_datas = diff_datas

    def get_default_indexes(self):
        return self.diff_datas[0].copy()


    def get_texture_path(self, current_diff_data: dict):
        ...

    def set_texture_path(self, current_diff_data: dict):
        current_texture_path = None
        for diff_data in self.diff_datas:
            if (
                current_diff_data["texture_diff_indexes"]
                == diff_data["texture_diff_indexes"]
                and current_diff_data["model_diff_indexes"]
                == diff_data["model_diff_indexes"]
            ):
                current_texture_path = diff_data["texture_path"]
                self.change_base_color_texture_by_path(current_texture_path)
                return True
        return False

    def _find_three_digit_numbers(self, text):
        """文字列から3桁の数字を取得する関数

        Args:
            text (str): 検索対象の文字列

        Returns:
            list: 3桁の数字が格納されたリスト
        """
        pattern = re.compile(r"_.*(\d{3})_.*")
        result = re.search(pattern, text)
        return result.groups()[0]

    def _find_two_digit_numbers(self, text):
        """文字列から3桁の数字を取得する関数

        Args:
            text (str): 検索対象の文字列

        Returns:
            list: 3桁の数字が格納されたリスト
        """
        pattern = re.compile(r"_.*(\d{2})_.*")
        result = re.search(pattern, text)
        return result.groups()[0]


class LongpantsTextureSelector(TextureSelectorBase):

    def __init__(self, **kwargs: str):
        target_material = kwargs["target_material"]
        self.material_id = kwargs["parts_id"]
        self.sourceimages_path = texture_selector_utils.get_current_sourceimages_dir(
            target_material
        )
        super().__init__(**kwargs)

    def initialize_diff_datas(self):
        diff_datas = []
        textures = self.get_current_textures()
        diff_data = {}
        for texture in textures:
            texture_str = texture.as_posix()
            texture_diff_index = self._find_three_digit_numbers(texture_str)
            model_diff_index = self._find_longpants_index(texture.stem)

            diff_data["texture_path"] = texture_str
            diff_data["model_diff_indexes"] = model_diff_index
            diff_data["texture_diff_indexes"] = texture_diff_index

            diff_datas.append(diff_data.copy())
        self.diff_datas = diff_datas

    def get_default_indexes(self):
        diff_data = {}
        diff_data = self.diff_datas[0].copy()
        diff_data["model_diff_indexes"] = "s"
        return diff_data


    def get_texture_path(self, current_diff_data: dict):
        ...

    def set_texture_path(self, current_diff_data: dict):
        current_texture_path = None
        for diff_data in self.diff_datas:
            if (
                current_diff_data["texture_diff_indexes"]
                == diff_data["texture_diff_indexes"]
                and current_diff_data["model_diff_indexes"]
                == diff_data["model_diff_indexes"]
            ):
                current_texture_path = diff_data["texture_path"]
                self.change_base_color_texture_by_path(current_texture_path)
                return True
        return False

    def _find_three_digit_numbers(self, text):
        """文字列から3桁の数字を取得する関数

        Args:
            text (str): 検索対象の文字列

        Returns:
            list: 3桁の数字が格納されたリスト
        """
        pattern = re.compile(r"_.*(\d{3})_.*")
        result = re.search(pattern, text)
        return result.groups()[0]

    def _find_two_digit_numbers(self, text):
        """文字列から3桁の数字を取得する関数

        Args:
            text (str): 検索対象の文字列

        Returns:
            list: 3桁の数字が格納されたリスト
        """
        pattern = re.compile(r"_.*(\d{2})_.*")
        result = re.search(pattern, text)
        return result.groups()[0]
    
    def _find_longpants_index(self,text):
        target_strings = ['_s_', '_l_', '_b_']
        for target in target_strings:
            text = text.split("_",1)[-1]
            if target in text:
                s = target.replace(target, target.replace('_', ''))
        return s

class SocksTextureSelector(TextureSelectorBase):
    def __init__(self, **kwargs):
        self.material_id = kwargs["parts_id"]
        self.sourceimages_path = Path(r"C:\cygames\wiz2\team\3dcg\chr\ply\legs\socks")
        super().__init__(**kwargs)

    def initialize_diff_datas(self):
        diff_datas = []
        textures = self.get_current_textures()
        diff_data = {}
        for texture in textures:
            texture_str = texture.as_posix()
            texture_diff_index = self._find_three_digit_numbers(texture_str)
            model_diff_index = self._find_two_digit_numbers(texture_str)

            diff_data["texture_path"] = texture_str
            diff_data["model_diff_indexes"] = model_diff_index
            diff_data["texture_diff_indexes"] = texture_diff_index

            diff_datas.append(diff_data.copy())
        self.diff_datas = diff_datas

    def get_default_indexes(self):
        diff_data = {}
        diff_data = self.diff_datas[0].copy()
        diff_data["model_diff_indexes"] = "s"
        return diff_data

    def get_texture_path(self, current_diff_data: dict):
        ...

    def set_texture_path(self, current_diff_data: dict) -> bool:
        current_texture_path = None
        for diff_data in self.diff_datas:
            if (
                current_diff_data["texture_diff_indexes"]
                == diff_data["texture_diff_indexes"]
                and current_diff_data["model_diff_indexes"]
                == diff_data["model_diff_indexes"]
            ):
                current_texture_path = diff_data["texture_path"]
                self.change_base_color_texture_by_path(current_texture_path)
                return True
        return False

    def _find_three_digit_numbers(self, text):
        """文字列から3桁の数字を取得する関数

        Args:
            text (str): 検索対象の文字列

        Returns:
            list: 3桁の数字が格納されたリスト
        """
        pattern = re.compile(r"_.*(\d{3})_.*")
        result = re.search(pattern, text)
        return result.groups()[0]

    def _find_two_digit_numbers(self, text):
        """文字列から3桁の数字を取得する関数

        Args:
            text (str): 検索対象の文字列

        Returns:
            list: 3桁の数字が格納されたリスト
        """
        pattern = re.compile(r".*/(\d{2})/.*")
        result = re.search(pattern, text)
        return result.groups()[0]
