# -*- coding: utf-8 -*-
# ----------------------------------
# Project : tsubasa
# Name    : pivot painter
# Author  : Yawata
# Version : 1.0
# Updata  : 2021/10/07 18:00
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

# -- definition
fld_path = r"D:/cygames/tsubasa/tools/dcc_user/maya/share/python/houdini_engine/pivot_painter/"

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
    cmds.select(clear=True)
    cmds.houdiniAsset(loadAsset=[ast_path,ast_name])
    mel.eval(r"string $list[] = `ls -sl`;")
    mel.eval(r'setAttr($list[0]+ ".splitGeosByGroup") 1;')
    export_info(name)
    
# -- create hda02
def create_hda02(name, *args):
    ast_path = fld_path + r"hda/" + name
    ast_name = r"Sop/" + name.split('.')[0]
    cmds.select(clear=True)
    cmds.houdiniAsset(loadAsset=[ast_path,ast_name])
    mel.eval(r"string $list[] = `ls -sl`;")
    mel.eval(r'setAttr($list[0]+ ".outputGeometryGroups") 0;')
    export_info(name)

# -- freeze hda
def freeze_hda(*args):
    mel.eval(r"houdiniEngine_freezeSelectedAssets;")

# -- unfreeze hda
def unfreeze_hda(*args):
    mel.eval(r"houdiniEngine_unfreezeSelectedAssets;")

# -- browswe
def open_browser(url, *args):
    webbrowser.open_new_tab(url) 

# -- Hkey
def show_Hkey(*args):
    mel.eval(r"houdiniEngine_runHKey;")

# -- confirmation
def run_sample(temp, *args):
    dir = fld_path + (r'sample')
    mel.eval(r'string $dir = "%s";' %dir)
    mel.eval(r'setProject $dir;')
    cmds.file(temp, open=True, force=True)
    
def withSampleUI(name, *args):    
    ConfirmIC = cmds.window(t=r"Confirmation", w=600)
    cmds.columnLayout(adj=True)
    cmds.text(l=r'')
    cmds.text(l=r'<< ' +name+ r' >>')
    cmds.text(l=r'')
    cmds.text(l=r'You will close this Maya scene. Please make sure saving your scene befor you oepn the sample file !!!!!')
    cmds.text(l=r'')
    cmds.button(l=r'Open the Sample File', h=20, c=partial(run_sample, name))
    cmds.text(l=r'')
    cmds.showWindow(ConfirmIC)

#----------------------------------------------------------------------------------------------------
# -- Qt Designer Loyout
class MainWindow(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.UI = QUiLoader().load(fld_path + r"pivot_painter.ui")
        self.setWindowTitle(self.UI.windowTitle())
        self.setCentralWidget(self.UI)
       
        # -- Qt Designer Button
        self.UI.act_confl.triggered.connect(lambda: open_browser(r"https://wisdom.cygames.jp/display/tsubasa/Pivot+Painter"))
        self.UI.act_freeze.triggered.connect(freeze_hda)
        self.UI.act_unfreeze.triggered.connect(unfreeze_hda)

        self.UI.act_tree_sample.triggered.connect(lambda: withSampleUI(r"export_pivot_painter_tree.mb"))
        self.UI.act_grass_sample.triggered.connect(lambda: withSampleUI(r"export_pivot_painter_grass.mb"))
        self.UI.act_ivy_sample.triggered.connect(lambda: withSampleUI(r"export_pivot_painter_ivy.mb"))
        self.UI.act_bill_sample.triggered.connect(lambda: withSampleUI(r"export_billboard_pivot.mb"))

        self.UI.act_cyfl.triggered.connect(lambda: open_browser(r"http://kuruma.cygames.jp/#list-houdini"))
        self.UI.act_hkey.triggered.connect(show_Hkey)

        self.UI.pb_tree.clicked.connect(lambda: create_hda(r"export_pivot_painter_tree.hda"))
        self.UI.pb_grass.clicked.connect(lambda: create_hda(r"export_pivot_painter_grass.hda"))
        self.UI.pb_ivy.clicked.connect(lambda: create_hda(r"export_pivot_painter_ivy.hda"))
        self.UI.pb_bill.clicked.connect(lambda: create_hda(r"export_billboard_pivot.hda"))
        self.UI.pb_red.clicked.connect(lambda: create_hda02(r"leaf_reduction.hda"))

ui = MainWindow()

def plugin_load():
    cmds.loadPlugin(r"houdiniEngine", qt=True)
    load = r'Loaded Houdini Engine Plug-in'
    cmds.inViewMessage(amg=load, pos='midCenter', fade=True)
    
def showUI():
    plugin_load()
    ui.show()