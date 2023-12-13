# -*- coding: utf-8 -*-
from __future__ import print_function

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

import pymel.core as pm
import maya.OpenMayaUI as OpenMayaUI
# from . import set_physics_mat_tools as spmtu

# パスを指定
filePath = os.path.dirname(__file__).replace("\\","/") + "/ui"
UIFILEPATH = filePath+'/set_scale_by_locater.ui'

print(UIFILEPATH)

class SetScaleByLocaterMainTool(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    @staticmethod
    def get_maya_window():
        maya_main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
        return shiboken.wrapInstance(int(maya_main_window_ptr), QtWidgets.QWidget)

    @property
    def absolute_name(self):
        return '{}.{}'.format(self.__module__, self.__class__.__name__)
    
    def __init__(self, parent=None):
        super(SetScaleByLocaterMainTool, self).__init__(parent)        
        #ウィンドウの重複の回避
        maya_window = SetScaleByLocaterMainTool.get_maya_window()
        for child in maya_window.children():
            # reload でポインタが変わったときのために名前で比較する
            if "SetScaleByLocater" in child.objectName():
                child.close()

        # UIのパスを指定
        self.UI = QUiLoader().load(UIFILEPATH)
        # ウィンドウタイトルをUIから取得
        self.setWindowTitle("SetScaleByLocater")
        # ウィジェットをセンターに配置
        self.setCentralWidget(self.UI)
        
        #初期値
        self.bind_length = -1
        self.bind_scale  = [1,1,1]
        self.currentSelectedObject = None

        #Connect
        self.UI.getTargetObject_BTN.clicked.connect(self.getTargetObject)
        self.UI.recreate_locater_BTN.clicked.connect(self.createLocater)
        self.UI.bind_locater_BTN.clicked.connect(self.bindLocater)
        self.UI.apply_transform_BTN.clicked.connect(self.applyTransform)
        self.UI.create_aimconstrain_BTN.clicked.connect(self.createAimConstrain)
        self.UI.select_locater_BTN_.clicked.connect(self.selectLocater)

    def getCurrentMesh(self):
        return self.currentSelectedObject

    #Connected Functions

    def getTargetObject(self):
        selected = pm.ls(sl=True,l=True)[0]
        self.currentSelectedObject = selected
        self.UI.target_mesh_LTXT.setText(str(selected))

    def getSourceLocater(self):
        try:
            loc = self.getCurrentMesh().longName()+"_scale_loc"
            return loc
        except:
            pm.warning(u"ロケーターの取得に問題があります")
            return 0 
        

    def createLocater(self):
        print("# create_locater")
        if self.UI.target_mesh_LTXT.text() is "":
            pm.warning(u"ターゲットとなるメッシュが設定されていません。処理を終了します。")
            return 
            
        locater_name = self.getCurrentMesh().longName()+"_scale_loc"
        
        if pm.objExists(locater_name):
            pm.delete(locater_name)

        loc = pm.spaceLocator(name = str(self.getCurrentMesh())+"_scale_loc")
        loc.setTranslation(pm.xform(self.getCurrentMesh(),q=True,ws=True,piv=True)[0:3],space="world")
        
        pm.parent(loc,pm.listRelatives(self.getCurrentMesh(),p=True)[0])

    def bindLocater(self):
        print("# bind_locater")
        target_mesh = self.getCurrentMesh()
        source_locater = self.getSourceLocater()
        target_translate = pm.datatypes.Vector(pm.xform(target_mesh,q=True,ws=True,piv=True)[0:3])
        source_translate = pm.datatypes.Vector(pm.xform(source_locater,q=True,ws=True,piv=True)[0:3])
        self.bind_length = target_translate.distanceTo(source_translate)
        self.bind_scale = target_mesh.getScale()
        print(("{0} >> bind >> {1}".format(target_mesh,source_locater)))
        print(("    distance >> {0}".format(self.bind_length)))
        print(("    scale >> {0}".format(self.bind_scale)))

    def applyTransform(self):
        print("# apply_transform")
        scale_vector = -1
        if self.UI.XAxis_Cbox.isChecked():
            scale_vector = 1

        target_mesh = self.getCurrentMesh()
        source_locater = self.getSourceLocater()
        target_translate = pm.datatypes.Vector(pm.xform(target_mesh,q=True,ws=True,piv=True)[0:3])
        source_translate = pm.datatypes.Vector(pm.xform(source_locater,q=True,ws=True,piv=True)[0:3])
        length = target_translate.distanceTo(source_translate)
        scale_bias = length/self.bind_length
        target_mesh.setScale([self.bind_scale[0]*(scale_bias*scale_vector),self.bind_scale[1]*abs(scale_bias),self.bind_scale[2]*abs(scale_bias)])
        print(("{0} >> set_scale >> {1}".format(target_mesh,scale_bias)))
        
    def createAimConstrain(self):
        print("# create_aimConstrain")
        pm.select(clear=True)
        pm.select(self.getSourceLocater(),add=True)
        pm.select(self.getCurrentMesh(),add=True)
        pm.mel.AimConstraintOptions()


    def selectLocater(self):
        print("# selectLocater")
        pm.select(self.getSourceLocater(),r=True)
        return 1



def main():
    window = SetScaleByLocaterMainTool()
    window.show()

if __name__ == '__main__':
    main()