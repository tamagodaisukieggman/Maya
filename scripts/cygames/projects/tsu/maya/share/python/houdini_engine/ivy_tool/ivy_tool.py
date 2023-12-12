# -*- coding: utf-8 -*-
# ----------------------------------
# Project : tsubasa
# Name    : ivy tool
# Author  : Yawata
# Version : 1.0
# Updata  : 2020/07/15 18:00
# ----------------------------------

# -- import modules
import maya.cmds as cmds
import maya.mel as mel
import webbrowser
import random
from csv import writer
import getpass
import datetime
from PySide2.QtUiTools import QUiLoader
from PySide2 import QtWidgets
from maya.app.general import mayaMixin

# -- definition
fld_path = r"D:/cygames/tsubasa/tools/dcc_user/maya/share/python/houdini_engine/ivy_tool/"
rfr_path = r"D:/cygames/tsubasa/tools/dcc_user/maya/share/python/houdini_engine/hda_list/env/tab4/"
ui_name = r"ivy_tool.ui"
help_path = r"https://wisdom.cygames.jp/display/tsubasa/Ivy+Tool"

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

# -- refer hda
def refer_hda(name, *args):
    ast_path = rfr_path + name
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
def create_controller(type,r,g,b,grp_name, *args):
    sel = cmds.ls(sl=True)
    vsel = cmds.filterExpand(sel, sm=31)
    grp = []
    for i in vsel:
        obj = eval(r"cmds." + type)
        shape = cmds.listRelatives(obj[0])
        cmds.setAttr(shape[0] + r".overrideEnabled",1)
        cmds.setAttr(shape[0] + r".overrideShading",0)
        cmds.setAttr(shape[0] + r".overrideRGBColors",1)
        cmds.setAttr(shape[0] + r".overrideColorRGB",r,g,b)
        vpos = cmds.pointPosition(i)
        cmds.setAttr(obj[0] + r".tx",vpos[0])
        cmds.setAttr(obj[0] + r".ty",vpos[1])
        cmds.setAttr(obj[0] + r".tz",vpos[2])
        grp.append(obj[0])
    cmds.group(grp,n=grp_name)

# -- duplicate input graph
def duplicate_inputgraph(*args):       
    cmds.duplicate(un=True)
    hie = cmds.select(hi=True)
    all = cmds.ls(sl=True)
    for i in all:
        type = cmds.nodeType(i)
        if type == r"houdiniAsset":
            rand_val = random.random()
            cmds.setAttr(i + r".houdiniAssetParm_remesh_seed",rand_val)
            cmds.setAttr(i + r".houdiniAssetParm_color_seed",rand_val)
            cmds.setAttr(i + r".houdiniAssetParm_bump_noise_seed",rand_val)
            rep = str(rand_val).replace('.','_')
            new = r"ivy_curve" + rep
            cmds.rename(i,new)
            
# -- bake curve
def bake_curve(*args):
    bunch = cmds.ls(sl=True)
    bake_bunch = []
    for i in bunch:
        cmds.select(i)
        cmds.select(hi=True)
        shape = cmds.ls(sl=True, typ=r"nurbsCurve")
        curves = cmds.listRelatives(shape, f=True, p=True)
        cmds.select(curves)
        main =[]
        sub = []
        for j in curves:
            degs = cmds.getAttr(j + r'.degree')
            spans = cmds.getAttr(j + r'.spans')
            cvs = degs+spans
            if(cvs==2):
                sub.append(j)
            elif(cvs>2):
                main.append(j)
        cmds.select(main)
        cmds.duplicate()
        cmds.parent(w=True)
        cmds.delete(ch=True)
        grp = cmds.group(n=r"IvyCurve_main_"+i)
        bake_bunch.append(grp)
        cmds.select(sub)
        cmds.duplicate()
        cmds.parent(w=True)
        cmds.delete(ch=True)
        grp = cmds.group(n=r"IvyCurve_sub_"+i)
        bake_bunch.append(grp)
    cmds.group(bake_bunch,n=r"IvyCurve_GP")

# -- import reaf
def import_ivy(*args):
    cmds.file(r"D:/cygames/tsubasa/tools/dcc_user/maya/share/python/houdini_engine/ivy_tool/maya/scenes/ivy_gp.mb", i=True, ra=False )
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
        self.UI.act_cyfl.triggered.connect(show_CyFloating)
        self.UI.act_hkey.triggered.connect(show_Hkey)
        self.UI.act_freeze.triggered.connect(freeze_hda)
        self.UI.act_unfreeze.triggered.connect(unfreeze_hda)

        self.UI.pb_autocol.clicked.connect(lambda: refer_hda(r"auto_collision.hda"))
        self.UI.pb_ivycurve.clicked.connect(lambda: create_hda(r"ivy_curve.hda"))
        self.UI.pb_ivyform.clicked.connect(lambda: create_hda(r"ivy_form.hda"))

        self.UI.pb_start.clicked.connect(lambda: create_controller(r"polyCone(sx=4,h=100,r=100,n='start')",1,0,0,r"Start_GP"))
        self.UI.pb_end.clicked.connect(lambda: create_controller(r"polyCube(h=100,w=100,d=100,n='end')",0,1,0,r"End_GP"))
        self.UI.pb_avoid.clicked.connect(lambda: create_controller(r"polySphere(sx=10,sy=5,r=500,n='avoid')",0,0,1,r"Avoid_GP"))

        self.UI.pb_duplicate.clicked.connect(duplicate_inputgraph)
        self.UI.pb_bake.clicked.connect(bake_curve)
        self.UI.pb_import.clicked.connect(import_ivy)

ui = MainWindow()

def plugin_load():
    cmds.loadPlugin(r"houdiniEngine", qt=True)
    load = r'Loaded Houdini Engine Plug-in'
    cmds.inViewMessage(amg=load, pos='midCenter', fade=True)
    
def showUI():
    plugin_load()
    ui.show()