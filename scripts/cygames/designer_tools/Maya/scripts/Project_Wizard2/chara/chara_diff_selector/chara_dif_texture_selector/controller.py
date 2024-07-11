# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import webbrowser


import maya.cmds as cmds

from .app import *
from .view import TextureSelectorMainWindow


class DiffTextureSelectorController:
    def __init__(self):
        self.selectors = {}
        self.ui = TextureSelectorMainWindow()

        try:
            self.initialize_list()
        except TypeError:
            pass

        self.setup_ui()

    def setup_ui(self):
        self.ui.gui.re_search_btn.clicked.connect(self.clicked_research_btn)
        self.ui.gui.texture_type_cmbbox.currentIndexChanged.connect(self.reset_selectors)

    def initialize_list(self):
        """選択オブジェクトに応じてlistWidgetの初期化を行う
        """
        if not cmds.ls(sl=True, type="transform"):
            cmds.warning("対象となるノードを選択して実行してください。")
            return

        materials = self.research_materials()

        self.ui.clear_material_list()

        self.initialize_selectors(materials)

        for material in materials:
            selector = self.selectors[material]
            indexes = self.get_material_indexes(selector.diff_datas)
            selector_widget = self.ui.add_item_selector_list(material, indexes)
            selector_widget.combo_index_changed.connect(self.exec_texture_change)
            self.exec_texture_change(material)

    def reset_selectors(self):
        cmds.select(self.current_object,r=True)
        materials = MaterialGetter.get_object_assigned_materials()
        self.initialize_selectors(materials)
        for material in materials:
            self.exec_texture_change(material)

    def exec_texture_change(self, material_name: str):
        """現在のslector widgetに設定されているindexを使用してテクスチャパスを設定

        Args:
            material_name (str): 対象となるマテリアル名
        """
        selector_widget = self.ui.get_selector_widget_from_material_name(material_name)
        selector = self.selectors[material_name]

        indexes = selector_widget.get_current_indexes()
        set_texture_success = selector.set_texture_path(indexes)
        if not set_texture_success:
            cmds.warning(f"以下の設定のテクスチャは存在しません >> {indexes}")
            cmds.headsUpMessage(f"テクスチャは存在しません.詳細はスクリプトエディタを参照")

    def _set_current_object(self):
        """選択に応じてtarget objectを取得
        選択のindex 0を対象とする
        """
        selected = cmds.ls(sl=True, type="transform")
        if len(selected) == 0:
            cmds.warning("オブジェクトが選択されていません")
            return
        self.current_object = cmds.ls(sl=True, type="transform")[0]
        self.ui.gui.target_obj_txt.setText(self.current_object)

    def research_materials(self) -> tp.List[str]:
        """現在選択しているオブジェクトのマテリアルを返す

        Returns:
            tp.List[str]: マテリアル名の配列
        """
        self._set_current_object()

        materials = []
        materials = MaterialGetter.get_object_assigned_materials()

        # もしマテリアルが０個だったらreturn
        if len(materials) == 0:
            cmds.warning("No assigned materials. It suspends processing.")
            return
        return materials

    def get_material_indexes(self, diff_datas: tp.List[dict]) -> dict:
        """indexの配列をまとめるdictを作成し、返す

        Returns:
            dict: {"indexの種類":[index,...]}
        """
        return_indexes = {}
        for diff_data in diff_datas:
            for key in diff_data:
                if "texture_path" == key:
                    continue
                if key not in return_indexes:
                    return_indexes[key] = []

                # 既に配列に追加されていればパス
                if diff_data[key] in return_indexes[key]:
                    continue
                return_indexes[key].append(diff_data[key])
        return return_indexes

    def initialize_selectors(self, materials):
        """selectorsの初期化

        Args:
            materials (tp.List[str]): material名の配列
        """
        self.selectors.clear()
        for material in materials:
            self.selectors[material] = self.create_selector(material)

    def get_material_type(self, material: str) -> dict:
        """マテリアル名から種類を判別

        Args:
            material (str): 対象のマテリアル名

        Returns:
            dict: 各情報が入ったdict
        """
        if ":" in material:
            material = material.split(":")[-1]
        # mt_p0_h_bob01のようなマテリアル名が来る想定
        player_type, parts_type,label = material.split("_")[1:4]
        material_info = {
            "player_type": player_type,
            "parts_type": parts_type,
            "label": label,
        }
        return material_info

    def create_selector(self, material:str) -> TextureSelectorBase:
        """対象のマテリアルのtexture_selectorを作成
        作成するselectorは対象のマテリアルの種類により分岐

        Args:
            material (str): マテリアル名

        Returns:
            TextureSelectorBase: 作成したselector
        """
        # テクスチャの種類を指定
        current_texture_type = self.ui.gui.texture_type_cmbbox.currentText()
        
        parts_type = self.get_material_type(material)["parts_type"]
        
        is_long_pants = False
        
        parts_id = self.get_parts_id(material)

        kwargs = {"target_material":material,"texture_type":current_texture_type,"parts_id":parts_id}

        if parts_type == "b":
            for lp in ["s","b","l"]:
                # self.current_objectがNoneなのはデフォルトに戻す場合の身なので、その時は_sに戻す想定
                try:
                    if self.current_object.endswith(f"_{lp}"):
                        is_long_pants = True
                        break
                except AttributeError:
                    is_long_pants = True
                    break

        if is_long_pants:
            selector =  LongpantsTextureSelector(**kwargs)
            return selector


        if parts_type == "h":
            selector = HairTextureSelector(**kwargs)

        elif parts_type == "l":
            selector = SocksTextureSelector(**kwargs)
        
        elif parts_type == "f":
            selector = FaceTextureSelector(**kwargs)

        else:
            selector = CommonTextureSelector(**kwargs)
        
        return selector

    def get_parts_id(self, material:str) -> str:
        if ":" in material:
            material = material.split(":")[-1]
        partsid = material.replace("mt_","")
        return partsid
    
    def set_texture_by_diff_data(self,material_name:str,diff_data:dict):
        """diff_dataで変更点のある部分のみ対象のマテリアルのindexを変更する

        Args:
            material_name (str): マテリアル名
            diff_data (dict): 差分のindex情報 #{"model_diff_indexes":"01"}
        """
        selector_widget = self.ui.get_selector_widget_from_material_name(material_name)
        indexes = selector_widget.get_current_indexes()
        indexes.update(diff_data)
        selector_widget.set_indexes(indexes)

    def clicked_research_btn(self):
        self.initialize_list()

    def show_manual(self):
        """コンフルのツールマニュアルページを開く"""
        try:
            webbrowser.open(
                "https://wisdom.tkgpublic.jp/pages/viewpage.action?pageId=660614235"
            )
        except Exception:
            cmds.warning("マニュアルページがみつかりませんでした")

    def show_ui(self):
        self.ui.show()

    def close_ui(self):
        self.ui.close()
