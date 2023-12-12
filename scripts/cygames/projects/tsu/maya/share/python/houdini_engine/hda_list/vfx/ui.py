# -*- coding: utf-8 -*-
# ----------------------------------
# Project : tsubasa
# Name    : hda list
# Author  : Yawata
# Version : 1.0
# Updata  : 2019/04/20 20:30
# ----------------------------------
# -- import modules
import maya.cmds as cmds
import maya.mel as mel
from functools import partial
import webbrowser
import csv

# -- load asset info
def load_file(path):
    info_file = path
    with open(info_file) as f:
        info_reader = csv.reader(f)
        info_header = next(info_reader)
        info_list = [row for row in info_reader]
        info_num = len(info_list)
        return info_list, info_num

vfx_list1, vfx_num1 = load_file(r"D:/cygames/tsubasa/tools/dcc_user/maya/share/python/houdini_engine/hda_list/vfx/tab1/hda_info.csv")
vfx_list2, vfx_num2 = load_file(r"D:/cygames/tsubasa/tools/dcc_user/maya/share/python/houdini_engine/hda_list/vfx/tab2/hda_info.csv")

# -- create hda
def create_hda(n, list, path, *args):
    asset_name = list[n][1]
    asset_path = r"D:/cygames/tsubasa/tools/dcc_user/maya/share/python/houdini_engine/hda_list/" +path+ r"/" +list[n][2]
    cmds.houdiniAsset(loadAsset=[asset_path,asset_name])

# -- open help
def show_toolHelp(n, list, *args):
    toolHelp_url = list[n][3]
    webbrowser.open_new_tab(toolHelp_url)
    
# -- CyFloating
def show_CyFloating(*args):
    CyFloating_url = r"http://kuruma.cygames.jp/#list-houdini"
    webbrowser.open_new_tab(CyFloating_url)

# -- Hkey
def show_Hkey(*args):
    mel.eval(r"houdiniEngine_runHKey")

# -- Tab
def creat_tab(hda_list, hda_num, folder_name):
    tab = cmds.scrollLayout(cr=True)
    cmds.columnLayout(adj=True)
    cmds.separator(h=5)
    for i in range(hda_num):
        cmds.rowLayout(nc=2, adj=True, cat=(2,r"both",10))
        cmds.button(l=hda_list[i][0], h=50, c=partial(create_hda, i, hda_list, folder_name))
        cmds.iconTextButton(st=r"iconOnly", i=r"help.xpm", c=partial(show_toolHelp, i, hda_list))
        cmds.setParent(r"..")
        cmds.separator(h=5)
    cmds.setParent(r"..")
    cmds.setParent(r"..")
    return tab

# -- window
def hdalistUI():    
    WinIC = cmds.window(r"hdalistUI", t=r"HDA List 1.0 <VFX>", w=300, h=300, mb=True)
    tabs = cmds.tabLayout()
    # -- menu
    cmds.menu(l=r"Licence Check")
    cmds.menuItem(l=r"CyFloating", c=partial(show_CyFloating))
    cmds.menuItem(l=r"License Administrator", c=partial(show_Hkey))

    # -- layout env_design
    tab1 = creat_tab(vfx_list1, vfx_num1, r"vfx/tab1")
    tab2 = creat_tab(vfx_list2, vfx_num2, r"vfx/tab2")

    # -- show
    cmds.tabLayout(tabs, edit=True, tabLabel=((tab1, r"  mesh  "), (tab2, r"  utility  ")))
    cmds.showWindow(WinIC)

def plugin_load():
    cmds.loadPlugin(r"houdiniEngine", qt=True)
    load = r'Loaded Houdini Engine Plug-in'
    cmds.inViewMessage(amg=load, pos='midCenter', fade=True)
    
def showUI():
    if cmds.window(r"hdalistUI", ex=True) == False:
        plugin_load()
        hdalistUI()
    else:
        cmds.showWindow(r"hdalistUI")