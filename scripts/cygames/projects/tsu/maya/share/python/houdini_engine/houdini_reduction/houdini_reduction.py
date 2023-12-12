# -*- coding: utf-8 -*-
# ----------------------------------
# Project : tsubasa
# Name    : houdini reduction
# Author  : Yawata
# Director : 5st leader Mr. Iwamoto
# Version : 1.0
# Updata  : 2021/10/19 18:00
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
fld_path = "D:/cygames/tsubasa/tools/dcc_user/maya/share/python/houdini_engine/houdini_reduction/"

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

    file_hda_info = "//cydrive01/100_projects/115_tsubasa/40_Artist/04_Environment/Houdini/Tool/info/hda_usage_situation_" + month + ".csv"
    with open(file_hda_info,"a") as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(list)
        f_object.close()

# -- create hda
def create_hda(name, *args):
    obj = cmds.ls(sl=True)
    cmds.select(clear=True)
    ast_path = fld_path + "hda/" + name
    ast_name = "Sop/" + name.split('.')[0]
    cmds.houdiniAsset(loadAsset=[ast_path,ast_name])
    mel.eval("string $list[] = `ls -sl`;")
    mel.eval('setAttr($list[0]+ ".splitGeosByGroup") 1;')
    cmds.select(obj)
    export_info(name)

# -- find object sets
def get_sets():
    outlns = []
    setOnlys = ['edgesOnlySet', 'editPointsOnlySet', 'facetsOnlySet', 'renderableOnlySet', 'verticesOnlySet']
    sets = cmds.ls(type='objectSet')
    keyingGroup = cmds.ls(type='keyingGroup')
    sets = list(set(sets) - set(keyingGroup))
    for oset in sets:
        for attr in setOnlys:
            if cmds.getAttr(oset+'.'+attr):
                outlns.append(oset)
    results = list(set(sets) - set(outlns))
    return results

# -- separate intersected faces
def separate_intersect(name, *args):
    obj = cmds.ls(sl=True)
    if not obj:
        cmds.warning('Please select some objects!!')
    else:
        sets_before = get_sets()
        cmds.select(clear=True)
        ast_path = fld_path + "hda/" + name
        ast_name = "Sop/" + name.split('.')[0]
        cmds.houdiniAsset(loadAsset=[ast_path,ast_name])
        mel.eval("string $list[] = `ls -sl`;")
        mel.eval('setAttr($list[0]+ ".splitGeosByGroup") 1;')
        cmds.select(obj)
        mel.eval('AEhoudiniAssetSetInputToSelection ($list[0]+ ".houdiniAssetParm.houdiniAssetParm_input__node");')
        mel.eval('houdiniEngine_bakeAsset $list[0];')
        mel.eval('delete $list[0];')
        grp = cmds.ls(sl=True)
        cmds.group(grp, name='obj_from_houdini')
        sets_after = get_sets()
        gap = list(set(sets_after) - set(sets_before))
        cmds.delete(gap)
        export_info(name)
             
# -- freeze hda
def freeze_hda(*args):
    mel.eval("houdiniEngine_freezeSelectedAssets;")

# -- unfreeze hda
def unfreeze_hda(*args):
    mel.eval("houdiniEngine_unfreezeSelectedAssets;")

# -- browswe
def open_browser(url, *args):
    webbrowser.open_new_tab(url) 

# -- Hkey
def show_Hkey(*args):
    mel.eval("houdiniEngine_runHKey;")

# -- confirmation
def run_sample(temp, *args):
    dir = fld_path + ('/sample')
    mel.eval('string $dir = "%s";' %dir)
    mel.eval('setProject $dir;')
    cmds.file(temp, open=True, force=True)
    
def withSampleUI(name, *args):    
    ConfirmIC = cmds.window(t="Confirmation", w=600)
    cmds.columnLayout(adj=True)
    cmds.text(l='')
    cmds.text(l='<< ' +name+ ' >>')
    cmds.text(l='')
    cmds.text(l='You will close this Maya scene. Please make sure saving your scene befor you oepn the sample file !!!!!')
    cmds.text(l='')
    cmds.button(l='Open the Sample File', h=20, c=partial(run_sample, name))
    cmds.text(l='')
    cmds.showWindow(ConfirmIC)

#Get Face vertex positions
def get_vpos(vert):
    vtxPosList = cmds.xform(vert, q=True, ws=True, t=True)
    vtxPosListRounded = [round(p,6) for p in vtxPosList]
    return vtxPosListRounded

#----------------------------------------------------------------------------------------------------
# -- Qt Designer Loyout
class MainWindow(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.UI = QUiLoader().load(fld_path + "houdini_reduction.ui")
        self.setWindowTitle(self.UI.windowTitle())
        self.setCentralWidget(self.UI)
       
        # -- Qt Designer Button
        self.UI.act_confl.triggered.connect(lambda: open_browser("https://wisdom.cygames.jp/display/tsubasa/Houdini+Reduction"))
        self.UI.act_red_sample.triggered.connect(lambda: withSampleUI("houdini_reduction.mb"))
        self.UI.act_delinside_sample.triggered.connect(lambda: withSampleUI("deleteinsideface.mb"))
        self.UI.act_freeze.triggered.connect(freeze_hda)
        self.UI.act_unfreeze.triggered.connect(unfreeze_hda)
        self.UI.act_cyfl.triggered.connect(lambda: open_browser("http://kuruma.cygames.jp/#list-houdini"))
        self.UI.act_hkey.triggered.connect(show_Hkey)

        self.UI.pb_red_simple.clicked.connect(lambda: self.simple_reduction("houdini_reduction.hda"))
        self.UI.pb_red_hda.clicked.connect(lambda: create_hda("houdini_reduction.hda"))
                
        self.UI.pb_sepinter_simple.clicked.connect(lambda: separate_intersect("separate_intersect_face.hda"))
        self.UI.pb_delinside_hda.clicked.connect(lambda: create_hda("deleteinsideface.hda"))
        self.UI.pb_reminside_hda.clicked.connect(lambda: create_hda("remove_inside_geo.hda"))
        
                
        self.UI.pb_seledge.clicked.connect(self.edge_detection)
        self.UI.pb_seldte.clicked.connect(self.dte_detection)
    
    #Simple Reduction
    def simple_reduction(self, name, *args):
        obj = cmds.ls(sl=True)
        if not obj:
            cmds.warning('Please select some objects!!')
        else:
            cmds.select(clear=True)
            pcount = self.UI.sl_pcount.value()
            mel.eval('int $pcount = "%i";' %pcount)
            eqlen = self.UI.sl_eqlen.value()
            mel.eval('int $eqlen = "%i";' %eqlen)
            kbound = self.UI.sl_kbound.value()
            mel.eval('int $kbound = "%i";' %kbound)
            khde = self.UI.sl_khde.value()
            mel.eval('int $khde = "%i";' %khde)
            kuvs = self.UI.sl_kuvs.value()
            mel.eval('int $kuvs = "%i";' %kuvs)
            opp = self.UI.cb_opp.isChecked()
            opp = self.UI.cb_pqua.isChecked()
            if opp==True:
                mel.eval('int $opp = 1;')
            else:
                mel.eval('int $opp = 0;')
            pqua = self.UI.cb_pqua.isChecked()
            if pqua==True:
                mel.eval('int $pqua = 1;')
            else:
                mel.eval('int $pqua = 0;')
    
            ast_path = fld_path + "hda/" + name
            ast_name = "Sop/" + name.split('.')[0]
            cmds.houdiniAsset(loadAsset=[ast_path,ast_name])
            mel.eval("string $list[] = `ls -sl`;")
        
            mel.eval('setAttr($list[0]+ ".splitGeosByGroup") 1;')
            cmds.select(obj)        
            mel.eval('setAttr($list[0]+ ".houdiniAssetParm_polygon_count") $pcount;')
            mel.eval('setAttr($list[0]+ ".houdiniAssetParm_equalize_lengths") $eqlen;')
            mel.eval('setAttr($list[0]+ ".houdiniAssetParm_keep_boundaries") $kbound;')
            mel.eval('setAttr($list[0]+ ".houdiniAssetParm_keep_hard_edges") $khde;')
            mel.eval('setAttr($list[0]+ ".houdiniAssetParm_keep_uv_seems") $kuvs;')
            mel.eval('setAttr($list[0]+ ".houdiniAssetParm_use_only_original_point_positions") $opp;')
            mel.eval('setAttr($list[0]+ ".houdiniAssetParm_preserve_quads") $pqua;')
            mel.eval('AEhoudiniAssetSetInputToSelection ($list[0]+ ".houdiniAssetParm.houdiniAssetParm_reduction_0__folder.houdiniAssetParm_input_object__node");')

            mel.eval('houdiniEngine_bakeAsset $list[0];')
            mel.eval("string $name[] = `ls -sl`;")
            mel.eval('for($i=0; $i<size($name); $i++){ rename $name[$i] ("reduction_pcount_" +$pcount); }')
            mel.eval('delete $list[0];')
            export_info(name)

    #Select Unnecessary Edges
    def edge_detection(self, *args):
        obj = cmds.ls(sl=True)
        edgeList = []
        if not obj:
            cmds.warning('Please select some objects!!')
        else:
            mel.eval("ConvertSelectionToEdges;")
            mel.eval('selectUVBorderComponents {} "" 1;')
            border = cmds.ls(sl=True, flatten=1)

            ref_deg = 180 - self.UI.sb_seledge.value()
            cmds.polySelectConstraint(m=3, t=0x8000, a=True, ab=(0, ref_deg))
            temp = cmds.ls(sl=True, flatten=1)
            cmds.polySelectConstraint(a=False)

            subtract = list(set(temp) - set(border))
            cmds.select(subtract)
    
    #Select Degenerate Triangle Edges
    def dte_detection(self, *args):
        mel.eval("SelectToggleMode;")
        mel.eval("SelectToggleMode;")
        obj = cmds.ls(sl=True)
        if not obj:
            cmds.warning('Please select some objects!!')
        else:
            edgeList = []
            ref_deg_min = self.UI.sb_seldte_min.value()
            ref_deg_max = self.UI.sb_seldte_max.value()
            for o in obj:
                faceCount = cmds.polyEvaluate(o,face=True)
                for i in range(0, faceCount):
                    face = '%s.f[%s]' % (o, i)
                    vertex = cmds.polyListComponentConversion(face, tv=1)          
                    vertex = cmds.filterExpand(vertex, selectionMask=31)
                    vertex01 = get_vpos(vertex[0])
                    vertex02 = get_vpos(vertex[1])
                    vertex03 = get_vpos(vertex[2])
                    mel.eval("vector $pos01 = <<%s,%s,%s >>;" % (vertex01[0],vertex01[1],vertex01[2]))
                    mel.eval("vector $pos02 = <<%s,%s,%s >>;" % (vertex02[0],vertex02[1],vertex02[2]))
                    mel.eval("vector $pos03 = <<%s,%s,%s >>;" % (vertex03[0],vertex03[1],vertex03[2]))
            
                    mel.eval("vector $dir01 = $pos02 - $pos01;")
                    mel.eval("$vec01 = `unit $dir01`;")
                    mel.eval("vector $dir02 = $pos03 - $pos01;")
                    mel.eval("$vec02 = `unit $dir02`;")
                    degree = mel.eval(r'angle($vec01,$vec02);')/6.28*360
                    if(degree>ref_deg_max or degree<ref_deg_min):
                        edge = cmds.polyListComponentConversion(vertex[1], vertex[2], fv=True, te=True, internal=True)
                        edgeList.append(edge[0])
                
                    mel.eval("vector $dir01 = $pos01 - $pos02;")
                    mel.eval("$vec01 = `unit $dir01`;")
                    mel.eval("vector $dir02 = $pos03 - $pos02;")
                    mel.eval("$vec02 = `unit $dir02`;")
                    degree = mel.eval(r'angle($vec01,$vec02);')/6.28*360
                    if(degree>ref_deg_max or degree<ref_deg_min):
                        edge = cmds.polyListComponentConversion(vertex[0], vertex[2], fv=True, te=True, internal=True)
                        edgeList.append(edge[0])
                
                    mel.eval("vector $dir01 = $pos01 - $pos03;")
                    mel.eval("$vec01 = `unit $dir01`;")
                    mel.eval("vector $dir02 = $pos02 - $pos03;")
                    mel.eval("$vec02 = `unit $dir02`;")
                    degree = mel.eval(r'angle($vec01,$vec02);')/6.28*360
                    if(degree>ref_deg_max or degree<ref_deg_min):
                        edge = cmds.polyListComponentConversion(vertex[0], vertex[1], fv=True, te=True, internal=True)
                        edgeList.append(edge[0])

            mel.eval("ConvertSelectionToEdges;")
            cmds.select(edgeList)
            message = str(len(edgeList)) + ' edges found'
            cmds.inViewMessage(amg=message, pos='midCenter', fade=True)
    
ui = MainWindow()

def plugin_load():
    cmds.loadPlugin("houdiniEngine", qt=True)
    load = 'Loaded Houdini Engine Plug-in'
    cmds.inViewMessage(amg=load, pos='midCenter', fade=True)
    
def showUI():
    plugin_load()
    ui.show()