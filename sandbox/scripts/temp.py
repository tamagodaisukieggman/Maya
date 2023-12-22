
import maya.cmds as cmds

def remove_objects_from_set(objects_to_remove, set_name):
    """
    指定したオブジェクトリストから指定したセット名のセットに含まれるオブジェクトを削除します。

    Args:
        objects_to_remove (list of str): 取り除きたいオブジェクト名のリスト
        set_name (str): Mayaセットの名前
    """
    # セットが存在するかどうかを確認
    if not cmds.objExists(set_name):
        raise ValueError(f"セット '{set_name}' が存在しません。")

    # リスト内の各オブジェクトがセットに含まれているかをチェックして、含まれていれば削除
    for obj in objects_to_remove:
        if cmds.sets(obj, isMember=set_name):
            cmds.sets(obj, remove=set_name)


# 使用例
objects_to_remove = cmds.ls(os=True, fl=True)
set_name = 'Head_lamina_face2_sets'

remove_objects_from_set(objects_to_remove, set_name)
