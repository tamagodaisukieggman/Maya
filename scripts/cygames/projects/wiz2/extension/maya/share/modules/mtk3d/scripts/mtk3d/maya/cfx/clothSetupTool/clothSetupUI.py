# -*- coding: utf-8 -*-

import os
import os.path
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mm
import re

from . import clothSetup as setup
reload(setup)

from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
import imp

try:
    imp.find_module('PySide2')
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtUiTools import *
    from PySide2.QtWidgets import *

except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide.QtUiTools import *

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


class GUI(MayaQWidgetBaseMixin, QMainWindow):

    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)
        self.window = self.__class__.__name__
        self.setObjectName(self.window)
        self.origin = None

        widgets = QApplication.allWidgets()
        for widget in widgets:
            if widget.objectName() == self.window:
                widget.close()

        loader = QUiLoader()
        uiFilePath = os.path.join(CURRENT_PATH, 'clothSetupUI.ui')
        self.UI = loader.load(uiFilePath)
        self.setCentralWidget(self.UI)

        self._initUI()

        qrect = self.UI.geometry()
        self.setWindowTitle('cloth Tools UI')
        self.setGeometry(100, 100, qrect.width(), qrect.height())

        self._add_to_clothRigList()
        self._getpolyMesh()

        self._connect()
        self.load_setting()



    #----------------------------------------------------------------------------------------
    def _initUI(self):

        #-----------------------------------------------------------------------
        ### UI design

        style = ''

        h = 30
        height = 'height:%spx;' % (h)

        border = 'border-style:solid; border-width: 2px; border-color:grey;'

        borderRadius = 'border-radius: %spx;' % (h/3.8)

        buttonStyle = 'QPushButton{%s %s %s}' % (height, border, borderRadius)

        style += buttonStyle

        over = 'background-color: #6E6E6E; border-width: 4px; border-color: #167FC9;'
        buttonHoverStyle = 'QPushButton:hover{%s}' % (over)

        style += buttonHoverStyle

        press = 'background-color: #B3B3B3; color: white;'
        buttonPress = 'QPushButton:pressed{%s}' % press
        style += buttonPress


        self.UI.refreshButton.setStyleSheet('QPushButton{ background-color: purple; color: white ;}%s' % (buttonHoverStyle))
        self.UI.setStyleSheet(style)



        #-----------------------------------------------------------------------

        self.UI.refreshButton.setIcon(QIcon(CURRENT_PATH + "/icons/refresh.png"))
        # cache
        self.UI.newCacheButton.setIcon(QIcon(CURRENT_PATH + "/icons/nClothCacheCreate.png"))
        self.UI.delCacheButton.setIcon(QIcon(CURRENT_PATH + "/icons/nClothCacheDelete.png"))
        # constraint
        self.UI.createNClothButton.setIcon(QIcon(CURRENT_PATH + "/icons/nClothCreate.png"))
        self.UI.makeCollideButton.setIcon(QIcon(CURRENT_PATH + "/icons/nClothCreatePassive.png"))
        self.UI.PSButton.setIcon(QIcon(CURRENT_PATH + "/icons/nConstraintPointoSurface.png"))
        self.UI.CCButton.setIcon(QIcon(CURRENT_PATH + "/icons/nConstraintComponentComponent.png"))
        self.UI.TFButton.setIcon(QIcon(CURRENT_PATH + "/icons/nConstraintTransform.png"))
        self.UI.SSButton.setIcon(QIcon(CURRENT_PATH + "/icons/nConstraintSlideonSurface.png"))
        self.UI.WBButton.setIcon(QIcon(CURRENT_PATH + "/icons/nConstraintWeldBorders.png"))
        self.UI.ECButton.setIcon(QIcon(CURRENT_PATH + "/icons/nConstraintExcludeCollision.png"))
        self.UI.FFButton.setIcon(QIcon(CURRENT_PATH + "/icons/nConstraintForceField.png"))
        self.UI.BCButton.setIcon(QIcon(CURRENT_PATH + "/icons/nConstraintBendComponent.png"))
        self.UI.SCButton.setIcon(QIcon(CURRENT_PATH + "/icons/nConstraintStretchComponent.png"))
        # field
        self.UI.localWindButton.setIcon(QIcon(CURRENT_PATH + "/icons/posEmitter.png"))
        self.UI.airButton.setIcon(QIcon(CURRENT_PATH + "/icons/posAir.png"))
        self.UI.turbulenceButton.setIcon(QIcon(CURRENT_PATH + "/icons/posTurbulence.png"))
        self.UI.vortexButton.setIcon(QIcon(CURRENT_PATH + "/icons/posVortex.png"))
        self.UI.volumeAxisButton.setIcon(QIcon(CURRENT_PATH + "/icons/posVolumeAxis.png"))
        self.UI.gravityButton.setIcon(QIcon(CURRENT_PATH + "/icons/posGravity.png"))
        self.UI.radialButton.setIcon(QIcon(CURRENT_PATH + "/icons/posRadial.png"))
        # utilities
        self.UI.applyFieldWeightButton.setIcon(QIcon(CURRENT_PATH + "/icons/art3dPaint.png"))
        self.UI.submitJobButton.setIcon(QIcon(CURRENT_PATH + "/icons/timeplay.png"))
        self.UI.setupCFXSceneButton.setIcon(QIcon(CURRENT_PATH + "/icons/polyDuplicateFacet.png"))
        self.UI.setupLocalGeoButton.setIcon(QIcon(CURRENT_PATH + "/icons/polyUnite.png"))
        self.UI.attachMultnCacheButton.setIcon(QIcon(CURRENT_PATH + "/icons/nClothCacheExisting.png"))


    #----------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------

    def _add_to_clothRigList(self):
        self.UI.clothRigList.clear()
        try:
            cr = pm.ls('*_clothRig')
        except:
            nuc = None
        if cr:
            for i in cr:
                crl = str(i)
                self.UI.clothRigList.addItem(crl)
        self._add_to_nucleusList()


    def _add_to_nucleusList(self):
        self.UI.nucleusList.clear()
        nuc = []
        try:
            cr = self.UI.clothRigList.currentItem().text()
            cr = pm.ls(cr)
        except:
            cr = None
        if cr:
            try:
                children = cr[0].getChildren(ad=1)
                for obj in children:
                    if (pm.objectType(obj) in 'nucleus'):
                        nuc.append(obj.name())
            except:
                nuc = None
        else:
            try:
                nuc = pm.ls(typ='nucleus')
            except:
                nuc = None
        if nuc:
            for i in nuc:
                nn = str(i)
                self.UI.nucleusList.addItem(nn)


    def _getCollision(self, *args):

        modifiers = QApplication.keyboardModifiers()

        self.UI.collisionList.clear()
        self.UI.nucleus_name.setText(self.UI.nucleusList.currentItem().text())

        if modifiers == Qt.ShiftModifier:
            cmds.select(self.UI.nucleusList.currentItem().text(), add=True)
        elif modifiers == Qt.ControlModifier:
            cmds.select(self.UI.nucleusList.currentItem().text(), add=True)
        else:
            cmds.select(self.UI.nucleusList.currentItem().text())

        try:
            sel = cmds.ls(sl=True)
            rgd = cmds.listConnections(sel, t='nRigid')
            rgd_unique = list(set(rgd))
            for i in rgd_unique:
                rg = str(i)
                self.UI.collisionList.addItem(rg)
        except:
            print ("------ nRigid does not exist ------")


    def _getpolyMesh(self):
        self.UI.polyMeshList.clear()
        sel = pm.ls(typ='mesh', ni=1)
        tgt = []
        obj = []
        for loop in sel:
            garb = []
            src = pm.listConnections(loop)
            if not (len(src) > 2):
                for list in src:
                    if pm.objectType(list, i='transform'):
                        garb.append(list)
                if not garb:
                    obj = loop.getParent()
                    tgt.append(obj)
        if tgt:
            for i in tgt:
                rg = str(i)
                self.UI.polyMeshList.addItem(rg)


    def _getCloth(self):
        self.UI.clothList.clear()

        try:
            sel = cmds.ls(sl=True)
            clt = cmds.listConnections(sel, t='nCloth')
            clt_unique = list(set(clt))
            for i in clt_unique:
                cl = str(i)
                cloth = cl.split("_node")
                self.UI.clothList.addItem(cloth[0])
        except:
            print ("------ nCloth does not exist ------")


    def _getDynamicConstraint(self):
        self.UI.constraintList.clear()
        try:
            sel = cmds.ls(sl=True)
            clt = cmds.listConnections(sel, t='dynamicConstraint')
            clt_unique = list(set(clt))
            for i in clt_unique:
                cl = str(i)
                self.UI.constraintList.addItem(cl)
        except:
            print ("------ dynamicConstraint does not exist ------")


    def _getDynamicConstraintSelect(self):
        self.UI.constraintList.clear()
        try:
            sel = pm.selected()
            cltNode = pm.listHistory(sel, type='nCloth')
            comp = pm.listConnections(cltNode, type='nComponent')
            if comp:
                cons = cmds.listConnections(comp, t='dynamicConstraint')
                cons_unique = list(set(cons))
                for i in cons_unique:
                    cl = str(i)
                    self.UI.constraintList.addItem(cl)
            else:
                print ("------ dynamicConstraint does not exist ------")
        except:
            print ("------ dynamicConstraint does not exist ------")


    def _getDynamicConstraintCallback(self, sel):
        self.UI.constraintList.clear()
        try:
            cltNode = pm.listHistory(sel, type='nCloth')
            comp = pm.listConnections(cltNode, type='nComponent')
            cons = cmds.listConnections(comp, t='dynamicConstraint')
            cons_unique = list(set(cons))
            for i in cons_unique:
                cl = str(i)
                self.UI.constraintList.addItem(cl)
        except:
            print ("------ dynamicConstraint does not exist ------")


    def _getField(self):
        self.UI.fieldList.clear()

        field_grp = ["airField", "dragField", "gravityField", "newtonField", "radialField",
                     "turbulenceField", "uniformField", "vortexField", "volumeAxisField"]
        try:
            sel = cmds.ls(sl=True)
            clt = cmds.listConnections(sel, d=True, t='nCloth')
            clt_unique = list(set(clt))

            for i in field_grp:
                fld = cmds.listConnections(clt_unique[0] + "Shape", t='{}'.format(i))
                if fld:
                    fld_unique = list(set(fld))
                    for j in fld_unique:
                        fl = str(j)
                        self.UI.fieldList.addItem(fl)

                else:
                    pass
            self._getLocalWind()
        except:
            print ("------ field does not exist ------")


    def _getLocalWind(self):

        field_grp = ["transform"]
        try:
            sel = cmds.ls(sl=True)
            clt = cmds.listConnections(sel, d=True, t='nCloth')
            clt_unique = list(set(clt))

            for i in field_grp:
                fld = cmds.listConnections(clt_unique[0] + ".localWindZ", t='{}'.format(i))
                if fld:
                    fld_unique = list(set(fld))
                    for j in fld_unique:
                        fl = str(j)
                        self.UI.fieldList.addItem(fl)

                else:
                    pass

        except:
            print ("------ field does not exist ------")


    def _getFieldSelect(self):
        self.UI.fieldList.clear()

        field_grp = ["airField", "dragField", "gravityField", "newtonField", "radialField",
                     "turbulenceField", "uniformField", "vortexField", "volumeAxisField"]
        try:
            sel = cmds.ls(sl=True)
            fld = pm.listHistory(sel, type='nCloth')
            comp = pm.listConnections(fld, type='field')
            fld_unique = list(set(comp))
            for i in fld_unique:
                fl = str(i)
                self.UI.fieldList.addItem(fl)

        except:
            print ("------ field does not exist ------")


    def _getLocalWindSelect(self, sel):
        try:
            if not sel:
                sel = cmds.ls(sl=True)
            clt = pm.listHistory(sel, type='nCloth')
            clt_unique = list(set(clt))

            for i in clt_unique:
                fld = cmds.listConnections(i + ".localWindZ", t='transform')
                if fld:
                    fld_unique = list(set(fld))
                    for j in fld_unique:
                        fl = str(j)
                        self.UI.fieldList.addItem(fl)

                else:
                    pass

        except:
            print ("------ field does not exist ------")


    def _getFieldCallback(self, sel):
        self.UI.fieldList.clear()

        field_grp = ["airField", "dragField", "gravityField", "newtonField", "radialField",
                     "turbulenceField", "uniformField", "vortexField", "volumeAxisField"]

        if (sel == str(self.UI.nucleus_name.text())):
            try:
                fld = pm.listHistory(sel, type='nCloth')
                comp = pm.listConnections(fld, type='field')
                fld_unique = list(set(comp))
                for i in fld_unique:
                    fl = str(i)
                    self.UI.fieldList.addItem(fl)

            except:
                print ("------ field does not exist ------")
        else:
            try:
                fld = pm.listHistory(sel, type='nCloth')
                comp = pm.listConnections(fld, type='field')
                fld_unique = list(set(comp))
                for i in fld_unique:
                    fl = str(i)
                    self.UI.fieldList.addItem(fl)

            except:
                print ("------ field does not exist ------")


    # -------------------------------------------------------------------


    def _createClothRig(self):
        sender = str(self.UI.clothRig_name.text())
        if sender:
            cn = setup.CreateNCloth()
            cr = cn._makeClothRig(name=sender)
            self._add_to_clothRigList()

        crItem = self.UI.clothRigList.findItems(str(cr), Qt.MatchExactly)
        self.UI.clothRigList.setCurrentItem(crItem[0])
        self.UI.clothRig_name.clear()


    def _createCloth(self):
        self.UI.nucleusList.clear()
        try:
            crl = str(self.UI.clothRigList.currentItem().text())
        except:
            crl = None
        slv = str(self.UI.nucleus_name.text())
        cn = setup.CreateNCloth()
        if slv and crl:
            nuc = cn._clothSetup(cr='{}'.format(crl), solver='{}'.format(slv))
        elif crl:
            nuc = cn._clothSetup(cr='{}'.format(crl), solver='')
        elif slv:
            nuc = cn._clothSetup(cr='', solver='{}'.format(slv))
        else:
            nuc = cn._clothSetup(cr='', solver='')
        self.UI.nucleus_name.setText(str(nuc))
        self._add_to_nucleusList()
        self._getpolyMesh()
        nucItem = self.UI.nucleusList.findItems(str(nuc), Qt.MatchExactly)
        self.UI.nucleusList.setCurrentItem(nucItem[0])



    def _makeCollide(self):
        slv = str(self.UI.nucleus_name.text())
        cn = setup.CreateNCloth()
        if slv:
            col = cn._makeCollide(solver="{}".format(slv))
        else:
            col = cn._makeCollide(solver="__nucleus1")

        self._getCollision()
        self._getpolyMesh()
        pm.select(col)


    def _createConstraint(self):
        sender = self.sender().text()
        cn = setup.CreateNCloth()
        cn._nConstraint(typ=sender)
        self._getDynamicConstraintSelect()


    def _createLocalWind(self):
        sel = pm.selected()
        from mtku.maya.menus.simulation.cloth import create_localwind_controller;create_localwind_controller()
        self._getLocalWindSelect(sel)


    def _createField(self):
        sel = pm.selected()
        tgt = []
        clt = []
        slv = []
        if sel:
            tgt = sel[0]
        else:
            tgt = str(self.UI.nucleusList.currentItem().text())
        try:
            slv = str(self.UI.nucleusList.currentItem().text())
        except:
            pass
        try:
            items = self.UI.clothList.selectedItems()
            for i in range(len(items)):
                clt.append(str(self.UI.clothList.selectedItems()[i].text()))
        except:
            pass
        sender = self.sender().text()
        cn = setup.CreateNCloth()
        if slv:
            if clt:
                cn._createField(typ=sender, solver="{}".format(slv), sel = clt)
            else:
                cn._createField(typ=sender, solver="{}".format(slv), sel = pm.selected())
        else:
            cn._createField(typ=sender, solver="__nucleus", sel = pm.selected())
        self._getFieldCallback(sel=tgt)


    def _openApplyFieldWeight(self):
        from mtku.maya.menus.simulation.cloth import apply_fieldweight_gui;apply_fieldweight_gui()


    def _openSubmitJob(self):
        import mtku.maya.menus.simulation.backgroundjob as backgroundjob;backgroundjob.main()


    def _openSetupScene(self):
        from mtku.maya.menus.simulation import setup_ply_sim_roll_ui;setup_ply_sim_roll_ui()


    def _openSetupLocalGeo(self):
        from mtku.maya.menus.simulation import setup_local_geo_ui;setup_local_geo_ui()


    def _openAttachCache(self):
        from mtku.maya.menus.simulation import attach_ncache_ui;attach_ncache_ui()


    # -------------------------------------------------------------------


    def _refresh_callback(self):
        self._add_to_clothRigList()
        self._getpolyMesh()
        self.UI.collisionList.clear()
        self.UI.clothList.clear()
        self.UI.nucleus_name.clear()
        self.UI.constraintList.clear()
        self.UI.fieldList.clear()


    def _newCache_callback(self):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ControlModifier:
            mm.eval('nClothCacheOpt;')
        else:
            mm.eval('doCreateNclothCache 5 { "2", "1", "10", "OneFilePerFrame", "1", "","0","","0", "add", "0", "1", "1","0","1","mcx" };')


    def _delCache_callback(self):
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ControlModifier:
            mm.eval('fluidDeleteCacheOpt;')
        else:
            mm.eval('deleteCacheFile 2 { "keep", "" };')


    def _clothRig_list_callback(self):
        self._add_to_nucleusList()
        self._getpolyMesh()
        self.UI.collisionList.clear()
        self.UI.clothList.clear()
        self.UI.nucleus_name.clear()
        self.UI.constraintList.clear()
        self.UI.fieldList.clear()


    def _nucleus_list_callback(self):
        items = self.UI.nucleusList.selectedItems()
        list = []
        for i in range(len(items)):
            list.append(str(self.UI.nucleusList.selectedItems()[i].text()))

        modifiers = QApplication.keyboardModifiers()
        for i in list:
            if modifiers == Qt.ShiftModifier:
                cmds.select(i, add=True)
            elif modifiers == Qt.ControlModifier:
                cmds.select(i, add=True)
            else:
                cmds.select(i)

        self._getCollision()
        self._getpolyMesh()
        self._getCloth()
        self._getDynamicConstraint()
        self._getField()


    def _collision_list_callback(self):
        items = self.UI.collisionList.selectedItems()
        list = []
        for i in range(len(items)):
            list.append(str(self.UI.collisionList.selectedItems()[i].text()))

        modifiers = QApplication.keyboardModifiers()
        for i in list:
            if modifiers == Qt.ShiftModifier:
                cmds.select(i, add=True)
            elif modifiers == Qt.ControlModifier:
                cmds.select(i, add=True)
            else:
                cmds.select(i)
        self._getpolyMesh()


    def _polyMesh_list_callback(self):
        items = self.UI.polyMeshList.selectedItems()
        list = []
        for i in range(len(items)):
            list.append(str(self.UI.polyMeshList.selectedItems()[i].text()))

        modifiers = QApplication.keyboardModifiers()
        for i in list:
            if modifiers == Qt.ShiftModifier:
                cmds.select(i, add=True)
            elif modifiers == Qt.ControlModifier:
                cmds.select(i, add=True)
            else:
                cmds.select(i)


    def _cloth_list_callback(self):
        items = self.UI.clothList.selectedItems()
        cloth = []
        for i in range(len(items)):
            cloth.append(str(self.UI.clothList.selectedItems()[i].text()))

        modifiers = QApplication.keyboardModifiers()
        for i in cloth:
            if modifiers == Qt.ShiftModifier:
                cmds.select(i, add=True)
            elif modifiers == Qt.ControlModifier:
                cmds.select(i, add=True)
            else:
                cmds.select(i)

        self._getDynamicConstraintSelect()
        self._getFieldSelect()
        self._getLocalWindSelect(sel= cloth)
        self._getpolyMesh()


    def _field_list_callback(self):
        items = self.UI.fieldList.selectedItems()
        list = []
        for i in range(len(items)):
            list.append(str(self.UI.fieldList.selectedItems()[i].text()))

        modifiers = QApplication.keyboardModifiers()
        for i in list:
            if modifiers == Qt.ShiftModifier:
                cmds.select(i, add=True)
            elif modifiers == Qt.ControlModifier:
                cmds.select(i, add=True)
            else:
                cmds.select(i)


    def _constraint_list_callback(self):
        items = self.UI.constraintList.selectedItems()
        list = []
        for i in range(len(items)):
            list.append(str(self.UI.constraintList.selectedItems()[i].text()))

        modifiers = QApplication.keyboardModifiers()
        for i in list:
            if modifiers == Qt.ShiftModifier:
                cmds.select(i, add=True)
            elif modifiers == Qt.ControlModifier:
                cmds.select(i, add=True)
            else:
                cmds.select(i)


    # -------------------------------------------------------------------


    def _connect(self):
        self.UI.refreshButton.clicked.connect(self._refresh_callback)
        self.UI.newCacheButton.clicked.connect(self._newCache_callback)
        self.UI.delCacheButton.clicked.connect(self._delCache_callback)
        # create button
        self.UI.createClothRigButton.clicked.connect(self._createClothRig)
        self.UI.createNClothButton.clicked.connect(self._createCloth)
        self.UI.makeCollideButton.clicked.connect(self._makeCollide)

        self.UI.localWindButton.clicked.connect(self._createLocalWind)

        self.UI.applyFieldWeightButton.clicked.connect(self._openApplyFieldWeight)
        self.UI.submitJobButton.clicked.connect(self._openSubmitJob)
        self.UI.setupCFXSceneButton.clicked.connect(self._openSetupScene)
        self.UI.setupLocalGeoButton.clicked.connect(self._openSetupLocalGeo)
        self.UI.attachMultnCacheButton.clicked.connect(self._openAttachCache)

        # list callback
        self.UI.clothRigList.itemClicked.connect(self._clothRig_list_callback)
        self.UI.clothRigList.currentItemChanged.connect(self._clothRig_list_callback)
        self.UI.nucleusList.itemClicked.connect(self._nucleus_list_callback)
        self.UI.nucleusList.currentItemChanged.connect(self._nucleus_list_callback)
        self.UI.collisionList.itemClicked.connect(self._collision_list_callback)
        self.UI.polyMeshList.itemClicked.connect(self._polyMesh_list_callback)
        self.UI.clothList.itemClicked.connect(self._cloth_list_callback)
        self.UI.fieldList.itemClicked.connect(self._field_list_callback)
        self.UI.constraintList.itemClicked.connect(self._constraint_list_callback)

        # create constraint
        const_type = (self.UI.PSButton, self.UI.CCButton, self.UI.TFButton, self.UI.SSButton,
                      self.UI.WBButton, self.UI.ECButton, self.UI.FFButton, self.UI.BCButton, self.UI.SCButton)

        for button in const_type:
            button.clicked.connect(self._createConstraint)


        # create field
        field_type = (self.UI.airButton, self.UI.turbulenceButton, self.UI.vortexButton,
                      self.UI.volumeAxisButton, self.UI.gravityButton, self.UI.radialButton)

        for button in field_type:
            button.clicked.connect(self._createField)


    def load_setting(self):
        setting = QSettings("setting.ini", QSettings.IniFormat)
        self.restoreState(setting.value("windowState"))
        self.restoreGeometry(setting.value("geometry"))


    def closeEvent(self, event):
        setting = QSettings("setting.ini", QSettings.IniFormat)
        setting.setValue("windowState", self.saveState())
        setting.setValue("geometry", self.saveGeometry())


# GUIの起動

def main():
    print ('\n\n===================================')
    print ('====== start-up clothToolsUI ======')
    print ('===================================\n')
    QApplication.instance()
    ui = GUI()
    ui.show()
    return ui


if __name__ == '__main__':
    main()
