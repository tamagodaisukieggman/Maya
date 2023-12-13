# -*- coding: utf-8 -*-
import os
import subprocess
from sys import exec_prefix
import maya.cmds as cmds
import maya.mel as mel
from maya import OpenMaya as om
from maya import OpenMayaUI as omUI
import shr.model.rename_lod.command as cmd
from PySide2 import QtGui,QtWidgets,QtCore
import shiboken2
import eST3 as eST

# ------------------------------------------
# 定数
# ------------------------------------------
#fileInfo用
DEV = True

class importer():
    def __init__(self,prec_type):
        self.prec_type=prec_type
        return

    def set_import_preset(self):
        preset_path = os.path.dirname(__file__).replace("\\","/")+"/presets"
        preset_name = "/" + self.prec_type + ".fbximportpreset"
        preset = preset_path+preset_name
        mel.eval('FBXLoadImportPresetFile -f "{}"'.format(preset))

    def exec_import(self,fbx_path=""):
        basicFilter = "*.fbx"
        print(fbx_path)
        #パスが設定されていなければ取得の実行
        if fbx_path == "":
            fbx_path = cmds.fileDialog2(fileFilter=basicFilter,fm=1, dialogStyle=2)[0]

        self.set_import_preset()
        
        om.MGlobal.executeCommand('FBXImport -f "{0}" -s'.format(fbx_path) )
        return 0

#汎用関数

def bake_animation(joints):
    '''
    アニメーションをベイク
    '''
    # Get Character joints
    start = cmds.playbackOptions(q=True, minTime=True)
    end   = cmds.playbackOptions(q=True, maxTime=True)
    # Bake Animation
    cmds.bakeResults(	joints,
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
    return joints

def get_current_character_rig():
    root_grp = cmds.ls(get_current_scene_path()["name"])[0]
    chirdren = cmds.listRelatives(root_grp,pa=True,c=True,type = "transform") or []
    for lp in chirdren:
        if "rig_grp" in lp:
            return lp
    return 0

def get_current_scene_path():
    """
    現在開いているシーンのパスを取得
    """
    fullpath = cmds.file(q=True, sn=True)
    filepath = os.path.dirname(fullpath)
    filename = os.path.basename(fullpath).split(".",1)[0]
    rtn = {"path":filepath,"name":filename}    
    return rtn

#インポート処理
def animation_import():
    imp = importer("animation")
    imp.exec_import()


    
