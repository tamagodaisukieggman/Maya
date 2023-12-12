# -*- coding: utf-8 -*-
import maya.cmds as cmds

from mtk import logger

def check_selection(selections):
    _flag = False
    
    if not selections:
        _flag = True
        logger.error("何も選択されていません。フェイスを選択して実行してください。")
        return

    _comp_check = selections[0].split(".")

    if len(_comp_check) == 1:
        _flag = True
    if _comp_check[-1][0] != "f":
        _flag = True
    
    if _flag:
        cmds.warning("Please Select Mesh Face")
        return False

    if len(list(set(x.split(".")[0] for x in selections))) != 1:
        cmds.warning("Please Select One Node")
        return False

    return True

def duplicate_face_plus():
    selections = cmds.ls(sl=True, flatten=True)
    

    if not check_selection(selections):
        return

    node_name = selections[0].split(".")[0]
    ids = [x.split("[")[-1].split("]")[0] for x in selections]
    duplicate_node = cmds.duplicate(node_name)[0]
    
    select_faces = ["{}.f[{}]".format(duplicate_node, x) for x in ids]

    cmds.select(select_faces, r=True)
    ExtrudeFacet = cmds.polyExtrudeFacet(constructionHistory=True,
                                        keepFacesTogether=True,
                                        divisions=1,
                                        twist=0,
                                        taper=1,
                                        off=0,
                                        thickness=0.1,
                                        smoothingAngle=30)
    
    all_faces = cmds.ls("{}.f[*]".format(duplicate_node), flatten=True)
    delete_faces = list(set(all_faces) - set(select_faces))
    
    cmds.delete(delete_faces)
    cmds.select(duplicate_node, r=True)
    cmds.select(ExtrudeFacet, addFirst=True)
    cmds.setToolTo("ShowManips")
    

    

    

    


    

