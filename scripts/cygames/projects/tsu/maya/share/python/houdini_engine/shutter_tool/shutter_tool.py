# -*- coding: utf-8 -*-
# ----------------------------------
# Project : tsubasa
# Name    : shutter tool
# Author  : Yawata
# Version : 1.0
# Updata  : 2020/07/07 18:00
# ----------------------------------

# -- import modules
import maya.cmds as cmds
import maya.mel as mel
from maya.OpenMaya import MVector
import webbrowser
from csv import writer
import getpass
import datetime
from PySide2.QtUiTools import QUiLoader
from PySide2 import QtWidgets
from maya.app.general import mayaMixin

# -- definition
fld_path = r"D:/cygames/tsubasa/tools/dcc_user/maya/share/python/houdini_engine/shutter_tool/"
ui_name = r"shutter_tool.ui"
help_path = r"https://wisdom.cygames.jp/display/tsubasa/Shutter+Tool"

#----------------------------------------------------------------------------------------------------
## -- usage situation
def export_info(hda_name):
    temp = hda_name.split("/")
    name = temp[-1].split(".")
    now = datetime.datetime.now()
    month = str(now.year) + "_" + str(now.month)
    time = str(now.day) + "/" + str(now.hour) + ":" + str(now.minute)
    user = getpass.getuser()
    list = [name[0], user, time]

    file_hda_info = r"//cydrive01/100_projects/115_tsubasa/40_Artist/04_Environment/Houdini/Tool/info/hda_usage_situation_" + month + ".csv"
    with open(file_hda_info,"a") as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(list)
        f_object.close()

# -- create hda
def create_hda(name, *args):
    ast_path = fld_path + r"hda/" + name
    ast_name = r"Sop/" + name.split('.')[0]
    cmds.houdiniAsset(loadAsset=[ast_path,ast_name])
    export_info(name)

# -- freeze hda
def freeze_hda(*args):
    mel.eval(r"houdiniEngine_freezeSelectedAssets;")

# -- unfreeze hda
def unfreeze_hda(*args):
    mel.eval(r"houdiniEngine_unfreezeSelectedAssets;")

# -- open help
def show_Help(*args):
    webbrowser.open_new_tab(help_path)
    
# -- CyFloating
def show_CyFloating(*args):
    CyFloating_url = r"http://kuruma.cygames.jp/#list-houdini"
    webbrowser.open_new_tab(CyFloating_url)

# -- Hkey
def show_Hkey(*args):
    mel.eval(r"houdiniEngine_runHKey;")

# -- create controller
def create_controller(type,r,g,b,flag, *args):
    sel = cmds.ls(selection=True)
    #creat
    temp = eval(r"cmds." + type)
    #convert
    if flag==1:
        cmds.nurbsCurveToBezier()
    #display
    cmds.setAttr(temp[0] + r".overrideEnabled",1)
    cmds.setAttr(temp[0] + r".overrideShading",0)
    cmds.setAttr(temp[0] + r".overrideRGBColors",1)
    cmds.setAttr(temp[0] + r".overrideColorRGB",r,g,b)      
    #transform
    if not sel:
        size = r=cmds.grid(query=True, size=True)
        center = [0,0,0]
    else:
        #size
        bbox = cmds.exactWorldBoundingBox(sel, ignoreInvisible=False)
        x = MVector(bbox[0],bbox[1],bbox[2])
        y = MVector(bbox[3],bbox[4],bbox[5])
        xy = x - y
        size = xy.length()/2
        #center
        count = len(sel)
        sums = [0,0,0]
        for i in sel:
            pos = cmds.xform(i,q=1,ws=1,rp=1)
            sums[0] += pos[0]
            sums[1] += pos[1]
            sums[2] += pos[2]
        center = [sums[0]/count, sums[1]/count, sums[2]/count]
    cmds.setAttr(temp[0] + r".translateX",center[0])
    cmds.setAttr(temp[0] + r".translateY",center[1])
    cmds.setAttr(temp[0] + r".translateZ",center[2])
    cmds.setAttr(temp[0] + r".scaleX",size)
    cmds.setAttr(temp[0] + r".scaleY",size)
    cmds.setAttr(temp[0] + r".scaleZ",size)

#----------------------------------------------------------------------------------------------------
# -- Qt Designer Loyout
class MainWindow(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.UI = QUiLoader().load(fld_path + ui_name)
        self.setWindowTitle(self.UI.windowTitle())
        self.setCentralWidget(self.UI)
       
        # -- Qt Designer Button
        self.UI.act_conf.triggered.connect(show_Help)
        self.UI.act_freeze.triggered.connect(freeze_hda)
        self.UI.act_unfreeze.triggered.connect(unfreeze_hda)
        self.UI.act_cyfl.triggered.connect(show_CyFloating)
        self.UI.act_hkey.triggered.connect(show_Hkey)

        self.UI.pb_conc_hda.clicked.connect(lambda: create_hda(r"concrete.hda"))
        self.UI.pb_cut_hda.clicked.connect(lambda: create_hda(r"cut.hda"))
        self.UI.pb_glass_hda.clicked.connect(lambda: create_hda(r"glass.hda"))
        self.UI.pb_wood_hda.clicked.connect(lambda: create_hda(r"wood.hda"))
        self.UI.pb_combine_hda.clicked.connect(lambda: create_hda(r"combine.hda"))
        self.UI.pb_clean_hda.clicked.connect(lambda: create_hda(r"clean_point.hda"))

        self.UI.pb_conc_cont.clicked.connect(lambda: create_controller(r"polySphere(sx=14,sy=8,r=1,n='controller_concrete')",0.75,0.75,0  ,0))
        self.UI.pb_cut_cont.clicked.connect(lambda: create_controller(r"polyPlane(sx=2,sy=2,w=2,h=2,n='controller_cut')",1,0,0  ,0))
        self.UI.pb_glass_cont.clicked.connect(lambda: create_controller(r"circle(r=1,n='controller_glass')",0,1,0  ,1))
        self.UI.pb_wood_bnd.clicked.connect(lambda: create_controller(r"polyCube(sx=4,sy=2,sz=1,w=1,h=2,d=0.5,n='bound_wood')",0,0,1  ,0))
        self.UI.pb_wood_cont.clicked.connect(lambda: create_controller(r"polyPlane(sx=2,sy=2,w=2,h=2,n='controller_wood')",1,0,0  ,0))

ui = MainWindow()

def plugin_load():
    cmds.loadPlugin(r"houdiniEngine", qt=True)
    load = r'Loaded Houdini Engine Plug-in'
    cmds.inViewMessage(amg=load, pos='midCenter', fade=True)
    
def showUI():
    plugin_load()
    ui.show()