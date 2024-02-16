import os
import re
import typing as tp
from pathlib import Path
import maya.cmds as cmds


class DifModelGetter:
    @classmethod
    def get_diff_datas(cls,base_objects:tp.List[str]) -> dict:
        dif_datas = {}
        for base_object in base_objects:
            parts_id = base_object.replace("_base","")
            diff_objects = []
            for lp in cmds.ls(f"*{parts_id}*",type="transform"):
                if "_Outline" not in lp and  "_base" not in lp:
                    diff_objects.append(lp)
            diff_ids = []
            for diff_object in diff_objects:
                diff_ids.append(diff_object.split("_")[-1])
            dif_datas[parts_id] = diff_ids
        return dif_datas

    @classmethod
    def get_base_objects(cls,root_node:str) -> tp.List[str]:
        """ルートの下階層に存在するbaseオブジェクトを返す
        もしもbaseが存在していなければ空の配列

        Args:
            root_node (str): 対象とするrootノード

        Returns:
            tp.List[str]: _description_
        """
        children = cmds.listRelatives(root_node,c=True,type="transform")
        base_nodes = []
        for child in children:
            if child.endswith("_base"):
                base_nodes.append(child)
        
        return base_nodes

class DifModelVisibilitySetter:
    def __init__(self,root_object:str):
        self.root_object = root_object
        self.base_objects = DifModelGetter.get_base_objects(root_object)
        self.diff_datas = DifModelGetter.get_diff_datas(self.base_objects)
    
    def set_visibility(self,parts_id:str,show_diff_id:str):
        """対象のidに当たるオブジェクトを表示し、それ以外を非表示

        Args:
            parts_id (str): p2_b_jeans02_001 の p2_b_jeans02に当たる部分
            show_diff_id (str): p2_b_jeans02_001 の 001に当たる部分
        """
        # 全て非表示にした後対象を表示
        for hidden_diff_id in self.diff_datas[parts_id]:
            cmds.setAttr(f"{parts_id}_{hidden_diff_id}.visibility",0)
        # 対象を表示
        cmds.setAttr(f"{parts_id}_{show_diff_id}.visibility",1)
        