# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import re
import glob

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
from . import set_physics_mat_tools as spmtu

# パスを指定
filePath = os.path.dirname(__file__).replace("\\","/") + "/ui"
UIFILEPATH = filePath+'/set_physics_mat_tools.ui'
SUBUIFILEPATH = filePath+'/set_physics_mat_tools_item.ui'

## PhysMatAssighToolMainWindowを作るクラス
class PhysMatAssighToolMainWindow(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    @staticmethod
    def get_maya_window():
        maya_main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
        return shiboken.wrapInstance(int(maya_main_window_ptr), QtWidgets.QWidget)

    @property
    def absolute_name(self):
        return '{}.{}'.format(self.__module__, self.__class__.__name__)
    
    def __init__(self, parent=None):
        super(PhysMatAssighToolMainWindow, self).__init__(parent)        
        #ウィンドウの重複の回避
        maya_window = PhysMatAssighToolMainWindow.get_maya_window()
        for child in maya_window.children():
            # reload でポインタが変わったときのために名前で比較する
            if "PhysMatAssighToolMainWindow" in child.objectName():
                child.close()

        # UIのパスを指定
        self.UI = QUiLoader().load(UIFILEPATH)
        # ウィンドウタイトルをUIから取得
        self.setWindowTitle("PhysicsMaterialAssignTools")
        # ウィジェットをセンターに配置
        self.setCentralWidget(self.UI)

        self.setPhysicsTools = spmtu.setPhysicsTools()

        # ============================================================
        # 元subUI
        # ============================================================
        self.is_showUIMode = True
        self.colorType = "material"  

        self.initialized()

        #Connect
        self.UI.MaterialApply.clicked.connect(self.clickedApply)
        self.UI.materialName.currentIndexChanged.connect(self.setMaterialUISettings)
        materialNames = self.setPhysicsTools.getPhysMaterialNames("surfaceType")
        if "none" not in materialNames:
            materialNames.insert(0,"none")
           
        self.setMaterialNamesCMBBox(materialNames)
        
        attributes = self.setPhysicsTools.getPhysMaterialNames("attribute")
        if "none" not in attributes:
            attributes.insert(0,"none")
       
        for lp in attributes:
            self.addAttributeCheckBox(lp)
        
        #Connect
        self.UI.CollisionApply.clicked.connect(self.SetCollisionSetting)
        self.UI.updateColMaterial_BTN.clicked.connect(self.execUpdateColMaterial)
        self.UI.buttonGroup.buttonClicked.connect(self.radioButtonClicked)
        self.UI.RemovePhys_BTN.clicked.connect(self.execRemovePhysicsSettings)

        
    def initialized(self):
        self.setPhysicsTools.parentWidget = self
        self.UI.materialName.currentText()
        self.setColorUI()
        self.setCollisionPresets()

    def setCollisionPresets(self):
        collisionNames = ["None","NoCollision","BlockAll"]
        for collisionName in collisionNames:
            self.UI.CollisionPreset.addItem(collisionName)

    def SetCollisionSetting(self):
        selectedObjects = pm.ls(sl=True,type ="transform")
        TargetObjects = []
        for selectedObject in selectedObjects:
            pattern = re.compile("(UCX|UBX|COMPLEX)_(.*?)_(\d{3})")
            if re.search(pattern,str(selectedObject)):
                TargetObjects.append(selectedObject)

        if len(TargetObjects) == 0:
            pm.warning(u"コリジョンオブジェクトが選択されていません。処理を終了します。")
            return 0
        colName = "col_"+self.UI.CollisionPreset.currentText()
        self.setPhysicsTools.changeColSet(TargetObjects,colName)

        print(u"現在選択中のオブジェクト >> コリジョン設定 >> {}\n".format(self.UI.CollisionPreset.currentText()))
        for lp in TargetObjects:
            print((u"対象オブジェクト >> {}".format(lp)))
        return 1
    def getCurrentCheckedColorType(self):
        checked = self.UI.buttonGroup.checkedButton().text()
        return checked

    #Connect
    def execUpdateColMaterial(self):
        self.setPhysicsTools.updateColMaterial(self.getCurrentCheckedColorType())

    def radioButtonClicked(self):
        # self.resetSubUI()
        self.setMaterialUISettings()
        self.setPhysicsTools.updateColMaterial(self.getCurrentCheckedColorType())

    def execRemovePhysicsSettings(self):

        #collision用セットからリムーブ
        selected = pm.ls(sl=True)
        colsets   = pm.ls("col_*",type="objectSet")

        pattern = re.compile("(UCX|UBX|COMPLEX)_(.*?)_(\d{3})")

        for lp in selected:
            if not re.search(pattern,str(lp)):
                pm.warning(u"実行対象　>> {} >> コリジョン以外のオブジェクトには実行できません".format(lp))
                return 0

            for colset in colsets:
                if lp in colset.members():
                    colset.remove(lp)
            
        collisionSets = self.setPhysicsTools.getAllSets()
        for collisionSet in collisionSets:
            if len(collisionSet.members()) == 0:
                pm.delete(collisionSet)
        #lambert1マテリアルをアサイン
        pm.hyperShade(assign='initialShadingGroup')

    def addAttributeCheckBox(self,attrName):
        self.UI.checkBox = QtWidgets.QCheckBox()
        self.UI.checkBox.setGeometry(QtCore.QRect(40, 30, 199, 16))
        self.UI.checkBox.setObjectName("checkBox")
        self.UI.checkBox.setText(QtWidgets.QApplication.translate("MainWindow", attrName, None, -1))
        self.UI.checkBox.stateChanged.connect(self.setColorUI)
        self.UI.AttributeVBox.addWidget(self.UI.checkBox)
        
    def getAttributeCheckedNames(self):
        rtn = []
        for i in range(self.UI.AttributeVBox.count()):
            if self.UI.AttributeVBox.itemAt(i).widget().isChecked():
                rtn.append(self.UI.AttributeVBox.itemAt(i).widget().text())
        return rtn

    def setColorUI(self):
        attributeNames = self.getAttributeCheckedNames()
        materialName = self.UI.materialName.currentText()
        colors = self.setPhysicsTools.getColor(attributeNames,materialName,self.colorType)
        colorString = ""
        for color in colors:
            color = color*255
            if colorString == "":
                colorString = color
            else:
                colorString = "{},{}".format(colorString,color)
        self.UI.MaterialColor.setStyleSheet("background-color : rgb({});".format(colorString))

    def clickedApply(self):
        self.setPhysicsTools.apply()
        return 
    
    def setMaterialNamesCMBBox(self,materialNames):
        #reset用
        self.UI.materialName.clear()
        for materialName in materialNames:
            self.UI.materialName.addItem(materialName)
        return

    def setMaterialUISettings(self):
        self.colorType = self.getCurrentCheckedColorType()
        pm.warning("viewMode >> {}".format(self.getCurrentCheckedColorType()))
        materialName = self.UI.materialName.currentText()
        self.setPhysicsTools.setMaterialName(materialName)
        self.setColorUI()
        return materialName

## PhysMatAssighToolMainWindowの起動
def main():
    window = PhysMatAssighToolMainWindow()
    window.show()

if __name__ == '__main__':
    main()