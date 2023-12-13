# -*- coding: utf-8 -*-
import os
import re

from PySide2 import QtWidgets,QtGui,QtCore 
from PySide2.QtUiTools import QUiLoader
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

#shibokenの読み込み
try :
    import shiboken2 as shiboken
except:
    import shiboken

import maya.cmds as cmds
import pymel.core as pm
import maya.OpenMayaUI as OpenMayaUI
# from . import set_physics_mat_tools as spmtu

# パスを指定
filePath = os.path.dirname(__file__).replace("\\","/") + "/ui"
UIFILEPATH = filePath+'/set_lightmap_uv_tool.ui'

class SetLightMapUVToolMainTool(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    @staticmethod
    def get_maya_window():
        maya_main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
        return shiboken.wrapInstance(int(maya_main_window_ptr), QtWidgets.QWidget)

    @property
    def absolute_name(self):
        return '{}.{}'.format(self.__module__, self.__class__.__name__)
    
    def __init__(self, parent=None):
        super(SetLightMapUVToolMainTool, self).__init__(parent)        
        #ウィンドウの重複の回避
        maya_window = SetLightMapUVToolMainTool.get_maya_window()
        for child in maya_window.children():
            # reload でポインタが変わったときのために名前で比較する
            if "SetLightMapUVTool" in child.objectName():
                child.close()

        # UIのパスを指定
        self.UI = QUiLoader().load(UIFILEPATH)
        # ウィンドウタイトルをUIから取得
        self.setWindowTitle("SetLightMapUVTool")
        # ウィジェットをセンターに配置
        self.setCentralWidget(self.UI)

        #connect
        self.UI.create_uv_BTN.clicked.connect(self.exec_create_lightmap_uv)
        
    def create_lightmap_uv(self,selection,method = 0):
        method = self.UI.method_type_CMBBTN.currentIndex()
        #Auto
        if method == 0:
            cmds.polyAutoProjection(lm=1,l=2,pb=0,ibd=1,uvs="LightMapUV",cm=True)
            #UVの選択
            pm.mel.uvSetEditCmd('setCurrent', {"LightMapUV"})
            #uv layout
            cmds.u3dLayout(cmds.ls(sl=True)[0],box=(0, 1, 0, 1), res=1028, spc=0.0625, mar=0.03125, scl=1)
        #
        elif method == 1:
            cmds.polyUVSet(nuv="LightMapUV", copy=1, uvSet="map1")
            pm.mel.uvSetEditCmd('setCurrent', {"LightMapUV"})
            cmds.u3dAutoSeam(p=1, s=0) 
                
            cmds.select(selection)
            cmds.u3dUnfold(rs=0, ite=4, bi=1, p=0, ms=1024, tf=1)
            
            #uv layout
            cmds.u3dLayout(cmds.ls(sl=True)[0],box=(0, 1, 0, 1), res=1028, spc=0.0625, mar=0.03125, scl=1)

    def exec_create_lightmap_uv(self):
        selection = cmds.ls(sl=True)
        if len(selection) == 0:
            cmds.warning(u"対象となるオブジェクトが選択されていません >> 処理を終了します。")
            return 0

        #すでにLightmapUVがあったら消す
        if u"LightMapUV" in cmds.polyUVSet( query=True, allUVSets=True ):
            cmds.polyUVSet(uvSet="LightMapUV", delete=1)
        
        self.create_lightmap_uv(selection,method = 1)
        return 1


def main():
    window = SetLightMapUVToolMainTool()
    window.show()

if __name__ == '__main__':
    main()