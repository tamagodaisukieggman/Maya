# -*- coding: utf-8 -*-
# ----------------------------------
# Project : tsubasa
# Name    : simple collision
# Author  : Yawata
# Director : 5st leader Mr. Iwamoto
# Version : 1.0
# Updata  : 2022/02/01 18:00
# ----------------------------------

# -- import modules
import maya.cmds as cmds
import maya.mel as mel
import webbrowser
from functools import partial
from csv import writer
import getpass
import datetime
from PySide2.QtUiTools import QUiLoader
from PySide2 import QtWidgets
from maya.app.general import mayaMixin
from maya.OpenMaya import MVector

## -- usage situation
def export_info(hda_name, col_label):
    name = hda_name.split("/")
    name_full = name[-1] + "(" + col_label + ")"
    print name_full
    now = datetime.datetime.now()
    month = str(now.year) + "_" + str(now.month)
    time = str(now.day) + "/" + str(now.hour) + ":" + str(now.minute)
    user = getpass.getuser()
    list = [name_full, user, time]

    file_hda_info = r"//cydrive01/100_projects/115_tsubasa/40_Artist/04_Environment/Houdini/Tool/info/hda_usage_situation_" + month + ".csv"
    with open(file_hda_info,"a") as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(list)
        f_object.close()

# -- create maya objects
def create_mobj(type, *args):
    sel = cmds.ls(selection=True)
    temp = eval(r"cmds." + type)  
    bbox = cmds.exactWorldBoundingBox(sel, ignoreInvisible=False)
    #center
    px = (bbox[0]+bbox[3])/2
    py = (bbox[1]+bbox[4])/2
    pz = (bbox[2]+bbox[5])/2
    cmds.setAttr(temp[0] + r".translateX",px)
    cmds.setAttr(temp[0] + r".translateY",py)
    cmds.setAttr(temp[0] + r".translateZ",pz)
    #size
    x = MVector(bbox[0],bbox[1],bbox[2])
    y = MVector(bbox[3],bbox[4],bbox[5])
    xy = y - x
    size = xy.length()/2
    #input
    if(type=="polySphere()"):
        cmds.setAttr(temp[0] + r".scaleX",size)
        cmds.setAttr(temp[0] + r".scaleY",size)
        cmds.setAttr(temp[0] + r".scaleZ",size)
    if(type=="polyCylinder()"):
        compare = max(xy[0],xy[2])
        cmds.setAttr(temp[0] + r".scaleX",compare*0.5)
        cmds.setAttr(temp[0] + r".scaleY",xy[1]*0.5)
        cmds.setAttr(temp[0] + r".scaleZ",compare*0.5)
        
#----------------------------------------------------------------------------------------------------
# -- Qt Designer Loyout
class MainWindow(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.UI = QUiLoader().load(r"D:/cygames/tsubasa/tools/dcc_user/maya/share/python/houdini_engine/simple_collision/simple_collision.ui")
        self.setWindowTitle(self.UI.windowTitle())
        self.setCentralWidget(self.UI)
       
        # -- Qt Designer Button
        self.UI.act_confl.triggered.connect(lambda: webbrowser.open_new_tab(r"https://wisdom.cygames.jp/display/tsubasa/Simple+Collision"))
        self.UI.act_cyfl.triggered.connect(lambda: webbrowser.open_new_tab(r"http://kuruma.cygames.jp/#list-houdini"))
        self.UI.act_hkey.triggered.connect(lambda: mel.eval(r"houdiniEngine_runHKey;"))
    
        self.UI.pb_26dp.clicked.connect(lambda: self.simple_collision(0,r"col_26_dop"))
        self.UI.pb_18dp.clicked.connect(lambda: self.simple_collision(1,r"col_18_dop"))
        self.UI.pb_10dp_x.clicked.connect(lambda: self.simple_collision(2,r"col_10_dop_x"))
        self.UI.pb_10dp_y.clicked.connect(lambda: self.simple_collision(3,r"col_10_dop_y"))
        self.UI.pb_10dp_z.clicked.connect(lambda: self.simple_collision(4,r"col_10_dop_z"))
        self.UI.pb_bbox.clicked.connect(lambda: self.simple_collision(5,r"col_bboxp"))
        self.UI.pb_obb.clicked.connect(lambda: self.simple_collision(6,r"col_obb"))
        self.UI.pb_convex.clicked.connect(lambda: self.simple_collision(7,r"col_convex"))
        self.UI.pb_sphere.clicked.connect(lambda: create_mobj(r"polySphere()"))
        self.UI.pb_tube.clicked.connect(lambda: create_mobj(r"polyCylinder()"))
            
    def simple_collision(self, type, label, *args):
        obj = cmds.ls(sl=True)
        if not obj:
            cmds.warning(r'Please Select Any Objects')
        else:
            cmds.select(clear=True)
            
            # -- attributes
            mel.eval(r'int $type = "%i";' %type)
            mel.eval(r'string $label = "%s";' %label)
            
            perobj = self.UI.cb_perobj.isChecked()
            if perobj==True:
                mel.eval(r'int $perobj = 1;')
            else:
                mel.eval(r'int $perobj = 0;')
            snap = self.UI.cb_snap.isChecked()
            if snap==True:
                mel.eval(r'int $snap = 1;')
            else:
                mel.eval(r'int $snap = 0;')
            transfer = self.UI.cb_transfer.isChecked()
            if transfer==True:
                mel.eval(r'int $transfer = 1;')
            else:
                mel.eval(r'int $transfer = 0;')
            merge = self.UI.sb_merge.value()
            mel.eval(r'float $merge = "%f";' %merge)

            # -- create hda
            ast_path = r"D:/cygames/tsubasa/tools/dcc_user/maya/share/python/houdini_engine/simple_collision/hda/simple_collision.hda"
            ast_name = r"Sop/simple_collision"
            cmds.houdiniAsset(loadAsset=[ast_path,ast_name])
            mel.eval(r"string $list[] = `ls -sl`;")
        
            cmds.select(obj)
            mel.eval(r'setAttr($list[0]+ ".houdiniAssetParm_type") $type;')
            mel.eval(r'setAttr($list[0]+ ".houdiniAssetParm_per_object") $perobj;')
            mel.eval(r'setAttr($list[0]+ ".houdiniAssetParm_snap_to_surface") $snap;')
            mel.eval(r'setAttr($list[0]+ ".houdiniAssetParm_transfer_uv_and_material") $transfer;')
            mel.eval(r'setAttr($list[0]+ ".splitGeosByGroup") $transfer;')
            mel.eval(r'setAttr($list[0]+ ".houdiniAssetParm_merge_vertex") $merge;')            
            mel.eval(r'AEhoudiniAssetSetInputToSelection ($list[0]+ ".houdiniAssetParm.houdiniAssetParm_obj__node");')

            mel.eval(r'houdiniEngine_bakeAsset $list[0];')
            mel.eval(r"string $name[] = `ls -sl`;")
            mel.eval(r'rename $name[0] $label;')
            mel.eval(r'delete $list[0];')
            
            export_info(ast_name, label)
        
ui = MainWindow()

def plugin_load():
    cmds.loadPlugin(r"houdiniEngine", qt=True)
    load = r'Loaded Houdini Engine Plug-in'
    cmds.inViewMessage(amg=load, pos='midCenter', fade=True)
    
def showUI():
    plugin_load()
    ui.show()