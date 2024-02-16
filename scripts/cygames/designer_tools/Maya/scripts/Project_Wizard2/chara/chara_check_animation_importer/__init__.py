import os
import maya.cmds as cmds
from .app import DemoAnimationImporter,DemoAnimationManager

def create():
    """DemoMotionの作成
    """
    file_name = os.path.basename(cmds.file(sn=True,q=True))
    chara_type = None
    if file_name.startswith("p1") or file_name.startswith("p0"):
        chara_type = "p1"
    
    elif file_name.startswith("p2"):
        chara_type = "p2"

    if chara_type:
        importer = DemoAnimationImporter(chara_type)
        importer.execute()

def remove():
    """DemoMotionの削除
    """
    manager = DemoAnimationManager()
    manager.remove_demo_motion()

def switch_animation():
    """DemoMotionのrotとtrans切り替え
    """
    manager = DemoAnimationManager()
    manager.flip_animation_type()