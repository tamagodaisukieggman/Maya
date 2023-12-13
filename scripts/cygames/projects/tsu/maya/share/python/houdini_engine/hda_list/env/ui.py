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
import getpass
import datetime

# -- load asset info
def load_file(path):
    info_file = path
    with open(info_file) as f:
        info_reader = csv.reader(f)
        info_header = next(info_reader)
        info_list = [row for row in info_reader]
        info_num = len(info_list)
        return info_list, info_num

env_list0, env_num0 = load_file(r"D:/cygames/tsubasa/tools/dcc_user/maya/share/python/houdini_engine/hda_list/env/tab0/_hda_info.csv")
env_list1, env_num1 = load_file(r"D:/cygames/tsubasa/tools/dcc_user/maya/share/python/houdini_engine/hda_list/env/tab1/_hda_info.csv")
env_list2, env_num2 = load_file(r"D:/cygames/tsubasa/tools/dcc_user/maya/share/python/houdini_engine/hda_list/env/tab2/_hda_info.csv")
env_list3, env_num3 = load_file(r"D:/cygames/tsubasa/tools/dcc_user/maya/share/python/houdini_engine/hda_list/env/tab3/_hda_info.csv")
env_list4, env_num4 = load_file(r"D:/cygames/tsubasa/tools/dcc_user/maya/share/python/houdini_engine/hda_list/env/tab4/_hda_info.csv")
env_list5, env_num5 = load_file(r"D:/cygames/tsubasa/tools/dcc_user/maya/share/python/houdini_engine/hda_list/env/tab5/_hda_info.csv")

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
        writer_object = csv.writer(f_object)
        writer_object.writerow(list)
        f_object.close()

# -- create hda
def create_hda(n, list, path, *args):
    asset_name = list[n][1]
    asset_path = r"D:/cygames/tsubasa/tools/dcc_user/maya/share/python/houdini_engine/hda_list/" +path+ r"/" +list[n][2]
    cmds.houdiniAsset(loadAsset=[asset_path,asset_name])
    export_info(asset_name)

# -- open help
def show_toolHelp(n, list, *args):
    toolHelp_url = list[n][3]
    webbrowser.open_new_tab(toolHelp_url)

# -- confirmation
def run_sample(temp, *args):
    dir = temp.rsplit('/', 2)[0]
    mel.eval(r'string $dir = "%s";' %dir)
    mel.eval(r'setProject $dir;')
    cmds.file(temp, open=True, force=True)
    
def withSampleUI(name, path, *args):    
    ConfirmIC_01 = cmds.window(t=r"Confirmation", w=600)
    cmds.columnLayout(adj=True)
    cmds.text(l=r'')
    cmds.text(l=r'<< ' +name+ r' >>')
    cmds.text(l=r'')
    cmds.text(l=r'You will close this Maya scene. Please make sure saving your scene befor you oepn the sample file !!!!!')
    cmds.text(l=r'')
    cmds.button(l=r'Open the Sample File', h=20, c=partial(run_sample, path))
    cmds.text(l=r'')
    cmds.showWindow(ConfirmIC_01)

def noSampleUI(*args): 
    ConfirmIC_02 = cmds.window(t=r"No Sample File", w=400)   
    cmds.columnLayout(adj=True)
    cmds.text(l=r'')
    cmds.text(l=r'Sorry...')
    cmds.text(l=r'No Sample File for This Digital Asset')
    cmds.text(l=r'')
    cmds.showWindow(ConfirmIC_02)
    
# -- open sample
def open_sampleFile(n, list, *args):
    sample_name = list[n][0]
    sample_path = list[n][4]
    if sample_path == r"":
        noSampleUI()
    else:
        withSampleUI(sample_name, sample_path)        
    
# -- CyFloating
def show_CyFloating(*args):
    CyFloating_url = r"http://kuruma.cygames.jp/#list-houdini"
    webbrowser.open_new_tab(CyFloating_url)

# -- Hkey
def show_Hkey(*args):
    mel.eval(r"houdiniEngine_runHKey;")

# -- Tab
def creat_tab(hda_list, hda_num, folder_name):
    tab = cmds.scrollLayout(cr=True)
    cmds.columnLayout(adj=True)
    cmds.separator(h=5)
    for i in range(hda_num):
        cmds.rowLayout(nc=3, adj=True, cat=(2,r"both",10))
        cmds.button(l=hda_list[i][0], h=50, c=partial(create_hda, i, hda_list, folder_name))
        cmds.iconTextButton(st=r"iconOnly", i=r"help.xpm", w= 30, c=partial(show_toolHelp, i, hda_list))
        cmds.iconTextButton(st=r"iconOnly", i=r"nodeGrapherUnsoloedLarge.png",  w=30, c=partial(open_sampleFile, i, hda_list))
        cmds.setParent(r"..")
        cmds.separator(h=5)
    cmds.setParent(r"..")
    cmds.setParent(r"..")
    return tab

# -- window
def hdalistUI_env():    
    WinIC = cmds.window(r"hdalistUI <ENV>", t=r"HDA List 1.0 <ENV>", w=300, h=300, mb=True)
    tabs = cmds.tabLayout()
    # -- menu
    cmds.menu(l=r"Licence Check")
    cmds.menuItem(l=r"CyFloating", c=partial(show_CyFloating))
    cmds.menuItem(l=r"License Administrator", c=partial(show_Hkey))

    # -- layout env_design
    tab0 = creat_tab(env_list0, env_num0, r"env/tab0") 
    tab1 = creat_tab(env_list1, env_num1, r"env/tab1")
    tab2 = creat_tab(env_list2, env_num2, r"env/tab2")
    tab3 = creat_tab(env_list3, env_num3, r"env/tab3")
    tab4 = creat_tab(env_list4, env_num4, r"env/tab4")
    tab5 = creat_tab(env_list5, env_num5, r"env/tab5")
 
    # -- show
    cmds.tabLayout(tabs, edit=True, tabLabel=((tab0, r"  common  "),(tab1, r"  terrain  "), (tab2, r"  snow  "), (tab3, r"  uv  "), (tab4, r"  collision  "), (tab5, r"  export  ")))
    cmds.showWindow(WinIC)

def plugin_load():
    cmds.loadPlugin(r"houdiniEngine", qt=True)
    load = r'Loaded Houdini Engine Plug-in'
    cmds.inViewMessage(amg=load, pos='midCenter', fade=True)
    
def showUI():
    if cmds.window(r"hdalistUI <ENV>", ex=True) == False:
        plugin_load()
        hdalistUI_env()
    else:
        cmds.showWindow(r"hdalistUI <ENV>")