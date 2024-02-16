import os
import maya.cmds as cmds
from . import chara_fbx

def execute_all_export():
    """シーン内に存在するエクスポート対象をすべて書き出し
    """
    file_name = cmds.file(sn=True, q=True)
    scene_type = os.path.basename(file_name).split("_")[0]

    all_transforms = cmds.ls(transforms=True)
    scene_name_transforms = [node for node in all_transforms if node in scene_type]
    root_transforms = [node for node in scene_name_transforms if cmds.listRelatives(node, parent=True) is None]

    cmds.select(root_transforms,r=True)

    chara_fbx._export_fbx()