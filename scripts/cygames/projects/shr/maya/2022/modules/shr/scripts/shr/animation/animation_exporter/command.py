# -*- coding: utf-8 -*-
import os
import maya.cmds as cmds
from maya import OpenMaya as om
import tool_log
import shr.animation.bakesimulation as bs

#fileInfo用
info_names = {"path":"animation_export_path","name":"animation_export_name"} 

# ------------------------------------------
# Pathの取得
# ------------------------------------------
def get_current_scene_path():
    """
    現在開いているシーンのパスを取得
    """
    fullpath = cmds.file(q=True, sn=True)
    filepath = os.path.dirname(fullpath)
    filename = os.path.basename(fullpath).split(".",1)[0]
    rtn = {"path":filepath,"name":filename}    
    return rtn

def get_current_saved_path():
    """
    現在fileinfoに保存している情報を取得
    """

    filepath = cmds.fileInfo( info_names["path"],query=True )[0]
    filename = cmds.fileInfo( info_names["name"],query=True )[0]
    rtn = {"path":filepath,"name":filename} 
    return rtn 


# ------------------------------------------
# export
# ------------------------------------------

def export(path="",file_name=""):
    """
    ベースとなるエクスポート関数
    """
    #ログ吐き出し(直で実行する場合があるのでここで実行)
    logger = tool_log.get_logger("AnimationExporter","v2022.08.18")
    logger.send_launch("")

    if cmds.ls(sl = True) == []:
        cmds.warning(u"対象が選択されていません。rootとなるノードを選択して実行してください。")
        return 0
    exportpath = path+"/"+file_name
    set_fbx_settings()

    selected = cmds.ls(sl=True)
    target_joints = cmds.listRelatives(selected,ad=True,type="joint",pa=True) or []
    if cmds.objectType(selected) == "joint":
        target_joints.extend(selected)

    cmds.undoInfo(openChunk=True)
    is_raise = False
    try:
        #アニメーションをベイク
        bakeAnim(target_joints)
        
        #リファレンスを複製(namespaceの除去と編集可の状態へ)
        duplicated = cmds.duplicate(target_joints,ic = True,po=True)

        root = get_hierarchy_root_joint(duplicated[0])
        #root骨をworldにparent
        cmds.parent(root,w=True)
        
        #書き出し用のオブジェクトを選択状態へ
        cmds.select(root,r=True)
        om.MGlobal.executeCommand('FBXExport -f "{0}.fbx" -s'.format(exportpath) )
        print("exported >> %s.fbx" % exportpath.replace("/","\\"))
    
    except Exception as e:
        print("例外args:", e.args)
        is_raise = True

    cmds.undoInfo(closeChunk=True)
    if not is_raise:
        cmds.undo()

    
    

def export_by_currently_scene_path(file_name):
    """
    現在開いているSceneの階層にエクスポート
    """
    filepath = get_current_scene_path()["path"]
    print(filepath)
    export(filepath,file_name)

def export_by_currently_saved_path():
    """
    現在のinfo保存されている場所にエクスポート
    """
    if cmds.fileInfo( info_names["path"],q=True ) == []:
        initialize_ui_info()
    paths = get_current_saved_path()
    export(paths["path"],paths["name"])

def delete_namespace(root):
    """
    namespaceの削除
    """    
    target_assets = cmds.listRelatives(root,ad=True) or []
    nss = []
    
    #削除する必要のあるnamespaceを検索
    for lp in target_assets:
        ns = lp.split(":")[0]
        #namespaceがついている and 既にリストに入っていない
        if ":" in lp and ns not in nss:
            nss.append(ns)
    
    rtn = 0
    for ns in nss:
        cmds.namespace(mergeNamespaceWithRoot=True, removeNamespace=ns)
        try:
            cmds.namespace(mergeNamespaceWithRoot=True, removeNamespace=ns)
            print('Namespace deleted:', ns)
            rtn = 1
        except:
            pass
    return rtn

def bakeAnim(bones):
    '''
    アニメーションをベイク
    '''
    # Get Character Bones
    start = cmds.playbackOptions(q=True, minTime=True)
    end   = cmds.playbackOptions(q=True, maxTime=True)
    # Bake Animation
    cmds.bakeResults(	bones,
                    simulation=True,
                    t=(start,end),
                    sampleBy=1,
                    disableImplicitControl=True,
                    preserveOutsideKeys=False,
                    sparseAnimCurveBake=False,
                    removeBakedAttributeFromLayer=False,
                    bakeOnOverrideLayer=False,
                    minimizeRotation=False,
                    at=['tx','ty','tz','rx','ry','rz','sx','sy','sz'] )
    # Return Result
    return bones

def get_hierarchy_root_joint(joint=""):
    rootJoint = joint

    while (True):
        parent = cmds.listRelatives( rootJoint,
                                     parent=True,
                                     type='joint' )
        if not parent:
            break

        rootJoint = parent[0]

    return rootJoint 

def set_fbx_settings():
    """
    fbxの保存設定
    """
    cmds.FBXResetExport()
    cmds.FBXProperty("Export|IncludeGrp|Animation|Deformation", "-v", 0)
    #bakeはexport処理の途中でするように変更
    # cmds.FBXProperty("Export|IncludeGrp|Animation|BakeComplexAnimation", "-v", 1)
    om.MGlobal.executeCommand("FBXExportSmoothMesh -v true")
    om.MGlobal.executeCommand("FBXExportUpAxis y")
    om.MGlobal.executeCommand("FBXExportCameras -v false")
    om.MGlobal.executeCommand("FBXExportLights -v false")
    om.MGlobal.executeCommand("FBXExportConstraints -v false")
    om.MGlobal.executeCommand("FBXExportInputConnections -v false")


# ------------------------------------------
# ui
# ------------------------------------------

def initialize_ui_info():
    """
    fileInfoの初期化(現在のシーンの場所と名前を入れる)
    初めてシーンを開いた際に使用
    """
    paths = get_current_scene_path()
    cmds.fileInfo( info_names["path"],paths["path"] )
    cmds.fileInfo( info_names["name"],paths["name"] )

