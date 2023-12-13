# -*- coding: utf-8 -*-
# ----------------------------------
# Project : tsubasa
# Name    : rock generator
# Author  : Yawata
# Version : 1.0
# Updata  : 2020/08/18 18:00
# ----------------------------------

# -- import modules
import maya.cmds as cmds
import maya.mel as mel
import webbrowser
cmds.loadPlugin(r"houdiniEngine", qt=True)
load = r'Loaded Houdini Engine Plug-in'
cmds.inViewMessage(amg=load, pos='midCenter', fade=True)
from PySide2 import QtCore, QtWidgets
from PySide2.QtUiTools import QUiLoader

# -- definition
fld_path = r"D:/cygames/tsubasa/tools/dcc_user/maya/share/python/houdini_engine/rock_generator/"
ui_name = r"rock_generator.ui"
help_path = r"https://wisdom.cygames.jp/display/tsubasa/Rock+Generator"

#----------------------------------------------------------------------------------------------------
# -- create hda (propotion)
def create_hda_propotion(name, *args):
    ast_path = fld_path + r"hda/" + name
    ast_name = r"Sop/" + name.split('.')[0]
    ast_temp = cmds.houdiniAsset(loadAsset=[ast_path,ast_name])
    param_info = grp_radio.checkedButton().text()
    size_min = param_info[0:3]
    size_max = param_info[4:7]
    count = param_info[-2:]
    print size_min
    print size_max
    print count
    cmds.setAttr(ast_temp + r".houdiniAssetParm_scale_x__tuple0",float(size_min))
    cmds.setAttr(ast_temp + r".houdiniAssetParm_scale_y__tuple0",float(size_min))
    cmds.setAttr(ast_temp + r".houdiniAssetParm_scale_z__tuple0",float(size_min))
    cmds.setAttr(ast_temp + r".houdiniAssetParm_scale_x__tuple1",float(size_max))
    cmds.setAttr(ast_temp + r".houdiniAssetParm_scale_y__tuple1",float(size_max))
    cmds.setAttr(ast_temp + r".houdiniAssetParm_scale_z__tuple1",float(size_max))
    cmds.setAttr(ast_temp + r".houdiniAssetParm_scatter_count",float(count))

# -- create hda
def create_hda(name, *args):
    ast_path = fld_path + r"hda/" + name
    ast_name = r"Sop/" + name.split('.')[0]
    ast_temp = cmds.houdiniAsset(loadAsset=[ast_path,ast_name])
    
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
    
# -- bake
def bake(*args):
    print r"bake"

#----------------------------------------------------------------------------------------------------
# -- Qt Designer Loyout
loader = QUiLoader()
ui = loader.load(fld_path + ui_name)
ui.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)    

# -- Qt Radio Button
grp_radio = QtWidgets.QButtonGroup()
grp_radio.addButton(ui.radioButton_1, 1)
grp_radio.addButton(ui.radioButton_2, 2)
 
# -- Qt Designer Button
ui.act_conf.triggered.connect(show_Help)
ui.act_cyfl.triggered.connect(show_CyFloating)
ui.act_hkey.triggered.connect(show_Hkey)

ui.pb_propotion.clicked.connect(lambda: create_hda_propotion(r"rock_proportion.hda"))
ui.pb_aging.clicked.connect(lambda: create_hda(r"rock_aging.hda"))

ui.pb_freeze.clicked.connect(freeze_hda)
ui.pb_unfreeze.clicked.connect(unfreeze_hda)

def showUI():
    ui.show()