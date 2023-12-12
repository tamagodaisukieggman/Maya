# -*- coding: utf-8 -*-

# ---------------------------------------------
# ======= author : yoshida_yutaka
# ======= Feb.2019
# ---------------------------------------------

import os
import os.path
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mm
import re

from . import clothSetup as setup
from .modules import myUtilities_gui as utilsGUI
from .modules import myUtilities as utils
reload(setup)
reload(utilsGUI)
reload(utils)

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
        # self.window = self.__class__.__name__
        self.window = 'cfxToolsUI'
        self.setObjectName(self.window)
        self.origin = None
        self.current_tooltip_state = None

        widgets = QApplication.allWidgets()
        for widget in widgets:
            if widget.objectName() == self.window:
                widget.close()

        loader = QUiLoader()
        uiFilePath = os.path.join(CURRENT_PATH, 'cfxToolsUI.ui')
        self.UI = loader.load(uiFilePath)
        self.setCentralWidget(self.UI)

        self._initUI()

        qrect = self.UI.geometry()
        self.setWindowTitle('CFX Tools UI')
        self.setGeometry(100, 100, qrect.width(), qrect.height())

        self._add_to_clothRigList()
        self._getPolyMesh()

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



        self.UI.refreshButton.setStyleSheet('QPushButton{ background-color: purple; color: white ;}%s%s'
                                             % (buttonHoverStyle, buttonPress))
        self.UI.setStyleSheet(style)

        #-----------------------------------------------------------------------

        self.UI.refreshButton.setIcon(QIcon(CURRENT_PATH + "/icons/refresh.png"))
        self.UI.refreshButton.setToolTip('Refresh the UI window')

        # cache
        self.UI.newCacheButton.setIcon(QIcon(CURRENT_PATH + "/icons/nClothCacheCreate.png"))
        self.UI.newCacheButton.setToolTip('Shift or Ctrl + Click - Open an Option window\nGiven a selected nCloth mesh, nHair or nParticle, create a cache.')
        self.UI.delCacheButton.setIcon(QIcon(CURRENT_PATH + "/icons/nClothCacheDelete.png"))
        self.UI.delCacheButton.setToolTip('Shift or Ctrl + Click - Open an Option window\nDelete cache on selected nCloth mesh, nParticle or fluid object.')

        # name
        self.UI.nucleus_name.setToolTip('Enter the name of nucleus')
        self.UI.nucleusClearButton.setIcon(QIcon(CURRENT_PATH + "/icons/clear.png"))
        self.UI.nucleusClearButton.setToolTip('Clear the name')
        self.UI.clothRig_name.setToolTip('Enter the name of clothRig')

        # list
        self.UI.clothRigList.setToolTip('A list of clothRig')
        self.UI.polyMeshList.setToolTip('A list of polygon objects\nYou can convert the object(s) into nCloth or Passive Collider.')
        self.UI.nucleusList.setToolTip('Alt + Click - Select a nucleus group\nA list of nucleus')
        self.UI.collisionList.setToolTip('Alt + Click - Select a Collision Object\nA list of collision')
        self.UI.clothList.setToolTip('Alt + Click - Select an nCloth node\nA list of nCloth')
        self.UI.constraintList.setToolTip('A list of constraints')
        self.UI.fieldList.setToolTip('A list of fields')

        # create
        self.UI.createClothRigButton.setToolTip('Create a clothRig group')
        self.UI.createNClothButton.setIcon(QIcon(CURRENT_PATH + "/icons/nClothCreate.png"))
        self.UI.createNClothButton.setToolTip('Given a selected mesh, create an nCloth')
        self.UI.makeCollideButton.setIcon(QIcon(CURRENT_PATH + "/icons/nClothCreatePassive.png"))
        self.UI.makeCollideButton.setToolTip('Make the selected mesh(es) collide with nCloth and nParticles')
        self.UI.PSButton.setIcon(QIcon(CURRENT_PATH + "/icons/nConstraintPointoSurface.png"))
        self.UI.PSButton.setToolTip('Select cloth points and a collision object to constraint to')
        self.UI.CCButton.setIcon(QIcon(CURRENT_PATH + "/icons/nConstraintComponentComponent.png"))
        self.UI.CCButton.setToolTip('Create a ComponentToComponent constraint between selected nucleus object vertices, edges or faces')
        self.UI.TFButton.setIcon(QIcon(CURRENT_PATH + "/icons/nConstraintTransform.png"))
        self.UI.TFButton.setToolTip('Create a Transform constraint for selected nucleus object points')
        self.UI.SSButton.setIcon(QIcon(CURRENT_PATH + "/icons/nConstraintSlideonSurface.png"))
        self.UI.SSButton.setToolTip('Select cloth points and a collision object to constraint to')
        self.UI.WBButton.setIcon(QIcon(CURRENT_PATH + "/icons/nConstraintWeldBorders.png"))
        self.UI.WBButton.setToolTip('Select cloth objects or components to weld together')
        self.UI.ECButton.setIcon(QIcon(CURRENT_PATH + "/icons/nConstraintExcludeCollision.png"))
        self.UI.ECButton.setToolTip('Select dynamic objects and/or cvs between which to suppress collisions')
        self.UI.FFButton.setIcon(QIcon(CURRENT_PATH + "/icons/nConstraintForceField.png"))
        self.UI.FFButton.setToolTip('Select cloth objects or components to apply a radial force constraint to')
        self.UI.BCButton.setIcon(QIcon(CURRENT_PATH + "/icons/nConstraintBendComponent.png"))
        self.UI.BCButton.setToolTip('Create a BendComponent constraint for an nCloth node or its selected components based on the mesh topology.')
        self.UI.SCButton.setIcon(QIcon(CURRENT_PATH + "/icons/nConstraintStretchComponent.png"))
        self.UI.SCButton.setToolTip('Create a StretchComponent constraint for an nCloth node or its selected components based on the mesh topology.')

        # field
        self.UI.localWindButton.setIcon(QIcon(CURRENT_PATH + "/icons/posEmitter.png"))
        self.UI.localWindButton.setToolTip('Create a LocalWind Controller that affects selected objects')
        self.UI.airButton.setIcon(QIcon(CURRENT_PATH + "/icons/posAir.png"))
        self.UI.airButton.setToolTip('Create an Air field that affects selected objects')
        self.UI.turbulenceButton.setIcon(QIcon(CURRENT_PATH + "/icons/posTurbulence.png"))
        self.UI.turbulenceButton.setToolTip('Create a Turbulence field that affects selected objects')
        self.UI.vortexButton.setIcon(QIcon(CURRENT_PATH + "/icons/posVortex.png"))
        self.UI.vortexButton.setToolTip('Create a Vortex field that affects selected objects')
        self.UI.volumeAxisButton.setIcon(QIcon(CURRENT_PATH + "/icons/posVolumeAxis.png"))
        self.UI.volumeAxisButton.setToolTip('Create a Volume Axis field that affects selected objects')
        self.UI.gravityButton.setIcon(QIcon(CURRENT_PATH + "/icons/posGravity.png"))
        self.UI.gravityButton.setToolTip('Create a Gravity field that affects selected objects')
        self.UI.radialButton.setIcon(QIcon(CURRENT_PATH + "/icons/posRadial.png"))
        self.UI.radialButton.setToolTip('Create a Radial field that affects selected objects')

        # utilities
        # honda
        self.UI.applyFieldWeightButton.setIcon(QIcon(CURRENT_PATH + "/icons/art3dPaint.png"))
        self.UI.applyFieldWeightButton.setToolTip('Open an Apply Field Weight window')
        self.UI.submitJobButton.setIcon(QIcon(CURRENT_PATH + "/icons/timeplay.png"))
        self.UI.submitJobButton.setToolTip('Open a Submit Simulation Job window')
        self.UI.setupCFXSceneButton.setIcon(QIcon(CURRENT_PATH + "/icons/polyDuplicateFacet.png"))
        self.UI.setupCFXSceneButton.setToolTip('Open a Ply Setup Sim Roll window')
        self.UI.setupLocalGeoButton.setIcon(QIcon(CURRENT_PATH + "/icons/polyUnite.png"))
        self.UI.setupLocalGeoButton.setToolTip('Open a Setup Local Geometry window')
        self.UI.attachMultnCacheButton.setIcon(QIcon(CURRENT_PATH + "/icons/nClothCacheExisting.png"))
        self.UI.attachMultnCacheButton.setToolTip('Open an Attach nCache window')
        self.UI.setThicknessValuesButton.setIcon(QIcon(CURRENT_PATH + "/icons/art3dPaint.png"))
        self.UI.setThicknessValuesButton.setToolTip('Set Thickness Values onto the surface')
        #yoshida
        self.UI.subdivWrapButton.setIcon(QIcon(CURRENT_PATH + "/icons/wrap.png"))
        self.UI.subdivWrapButton.setToolTip('Click - Subdiv Level 1\nShift or Ctrl + Click - Subdiv Level 2\nShift + Ctrl + Click - Subdiv Level 3\nSelect object(s), and then an influence object to subdivWrap them with')
        self.UI.cleanUpButton.setIcon(QIcon(CURRENT_PATH + "/icons/polyCleanup.png"))
        self.UI.cleanUpButton.setToolTip('Clean up the selected object(s)')
        self.UI.SHBTButton.setIcon(QIcon(CURRENT_PATH + "/icons/polyGrowSelection.png"))
        self.UI.SHBTButton.setToolTip('Open a Select Hierarchy by Type window')
        self.UI.selectCVsButton.setIcon(QIcon(CURRENT_PATH + "/icons/selectFirstCV.png"))
        self.UI.selectCVsButton.setToolTip('Open a Convert selected curve(s) to set CV on curve(s) window')


        self._comboBox()

    #----------------------------------------------------------------------------------------

    def _comboBox(self):
        projects = ['--- Select Project ---', 'mutsunokami', 'world', 'kurosawa', '3dcg']
        projects.sort()

        for i in projects:
            proj = i
            self.UI.projectComboBox.addItem(proj)

        self.UI.projectComboBox.setCurrentText('mutsunokami')

    #----------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------

    def _add_to_clothRigList(self):
        self.UI.clothRigList.clear()
        try:
            cr = pm.ls('*_clothRig*', r=1)
        except:
            nuc = None
        if cr:
            for i in cr:
                crl = str(i)
                self.UI.clothRigList.addItem(crl)
        nuc = self._add_to_nucleusList()


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
                list = pm.ls(assemblies=1)
                for tgt in list:
                    children = tgt.getChildren(ad=1)
                    for child in children:
                        if pm.objectType(child, i='nucleus'):
                            nuc.append(child)
            except:
                nuc = None

        if nuc:
            for i in nuc:
                nn = str(i)
                self.UI.nucleusList.addItem(nn)
            return nuc


    def _getCollision(self, *args):
        self.UI.collisionList.clear()

        sel = cmds.ls(sl=True)
        nucs = []
        for tgt in sel:
            if cmds.objectType(tgt, i='nucleus'):
                nucs.append(tgt)
        nuc = []
        rgd = []

        try:
            nuc = self.UI.nucleusList.currentItem().text()
        except:
            pass

        try:
            if nucs:
                rgd = cmds.listConnections(nucs, t='nRigid')
            else:
                rgd = cmds.listConnections(nuc, t='nRigid')
            rgd_unique = list(set(rgd))
            for i in rgd_unique[::-1]:
                rg = str(i)
                self.UI.collisionList.addItem(rg)
        except:
            #print("------ nRigid does not exist ------")
            pass


    def _getPolyMesh(self):
        self.UI.polyMeshList.clear()
        sel = pm.ls(typ='mesh', ni=1)
        tgt = []
        obj = []

        ex = ['transform','wrap']

        for loop in sel:
            garb = []
            src = pm.listConnections(loop)
            if not (len(src) > 2):
                for list in src:
                    if pm.objectType(list) in ex:
                        garb.append(list)
                if not garb:
                    if not ("_INIT" in str(loop) or "_REST" in str(loop)):
                        obj = loop.getParent()
                        tgt.append(obj)
        if tgt:
            for i in tgt:
                rg = str(i)
                self.UI.polyMeshList.addItem(rg)


    def _getCloth(self, obj = [], mode = 0):
        self.UI.clothList.clear()

        try:
            if obj:
                clt = cmds.listConnections(obj, t='nCloth')
            else:
                sel = cmds.ls(sl=True)
                clt = cmds.listConnections(sel, t='nCloth')
            clt_unique = list(set(clt))
            #name = '------------'
            count = self.UI.nucleusList.currentItem().text()

            # for loop in str(count):
            #    name += '-'
            if mode == 1:
                print('\n** {} **********'.format(count))

            for i in clt_unique[::-1]:
                cl = str(i)
                cloth = cl.split("_node")
                self.UI.clothList.addItem(cloth[0])
                if mode == 1:
                    print(cloth[0])
            if mode == 1:
                print('\n')

            #print(name)

        except:
            #print("------ nCloth does not exist ------")
            pass


    def _getDynamicConstraint(self):
        self.UI.constraintList.clear()
        try:
            sel = cmds.ls(sl=True)
            clt = cmds.listConnections(sel, t='dynamicConstraint')
            clt_unique = list(set(clt))
            clt_unique.sort()
            for i in clt_unique:
                cl = str(i)
                self.UI.constraintList.addItem(cl)
        except:
            #print("------ dynamicConstraint does not exist ------")
            pass


    def _getDynamicConstraintSelect(self):
        self.UI.constraintList.clear()
        try:
            sel = pm.selected()
            cltNode = pm.listHistory(sel, type='nCloth')
            comp = pm.listConnections(cltNode, type='nComponent')
            if comp:
                cons = cmds.listConnections(comp, t='dynamicConstraint')
                cons_unique = list(set(cons))
                cons_unique.sort()
                for i in cons_unique:
                    cl = str(i)
                    self.UI.constraintList.addItem(cl)
            else:
                #print("------ dynamicConstraint does not exist ------")
                pass
        except:
            #print("------ dynamicConstraint does not exist ------")
            pass


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
                    fld_unique.sort()
                    for j in fld_unique:
                        fl = str(j)
                        self.UI.fieldList.addItem(fl)

                else:
                    pass
            self._getLocalWind()
        except:
            #print("------ field does not exist ------")
            pass


    def _getFieldSelect(self):
        self.UI.fieldList.clear()

        try:
            sel = cmds.ls(sl=True)
            fld = pm.listHistory(sel, type='nCloth')
            comp = pm.listConnections(fld, type='field')
            fld_unique = list(set(comp))
            fld_unique.sort()
            for i in fld_unique:
                fl = str(i)
                self.UI.fieldList.addItem(fl)

        except:
            #print("------ field does not exist ------")
            pass


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
            #print("------ field does not exist ------")
            pass


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
            #print("------ field does not exist ------")
            pass


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
                #print("------ field does not exist ------")
                pass
        else:
            try:
                fld = pm.listHistory(sel, type='nCloth')
                comp = pm.listConnections(fld, type='field')
                fld_unique = list(set(comp))
                for i in fld_unique:
                    fl = str(i)
                    self.UI.fieldList.addItem(fl)

            except:
                #print("------ field does not exist ------")
                pass


    # -------------------------------------------------------------------
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
        pro = self.UI.projectComboBox.currentText()
        slv = str(self.UI.nucleus_name.text())
        cn = setup.CreateNCloth()
        if slv and crl:
            nuc = cn._clothSetup(cr='{}'.format(crl), solver='{}'.format(slv), proj = pro)
        elif crl:
            nuc = cn._clothSetup(cr='{}'.format(crl), solver='', proj = pro)
        elif slv:
            nuc = cn._clothSetup(cr='', solver='{}'.format(slv), proj = pro)
        else:
            nuc = cn._clothSetup(cr='', solver='', proj = pro)

        if nuc:
            self.UI.nucleus_name.setText(str(nuc))

        self._add_to_nucleusList()
        self._getPolyMesh()

        sel = cmds.ls(sl=True)
        nucItem = self.UI.nucleusList.findItems(str(nuc), Qt.MatchExactly)
        if nucItem:
            self.UI.nucleusList.setCurrentItem(nucItem[0])

        cltItem = self.UI.clothList.findItems(sel[0], Qt.MatchExactly)
        if cltItem:
            self.UI.clothList.setCurrentItem(cltItem[0])


    def _makeCollide(self):
        slv = str(self.UI.nucleus_name.text())
        cn = setup.CreateNCloth()
        if slv:
            col = cn._makeCollide(solver="{}".format(slv))
        else:
            pm.warning("You must've selected the 'nucleus'")

        self._getCollision()
        self._getPolyMesh()
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


    # -------------------------------------------------------------------
    # -------------------------------------------------------------------


    def _refresh_callback(self):
        self._add_to_clothRigList()
        self._getPolyMesh()
        self.UI.collisionList.clear()
        self.UI.clothList.clear()
        self.UI.nucleus_name.clear()
        self.UI.constraintList.clear()
        self.UI.fieldList.clear()


    def _newCache_callback(self):
        modifiers = QApplication.keyboardModifiers()
        if modifiers & Qt.ControlModifier or modifiers & Qt.ShiftModifier:
            mm.eval('nClothCacheOpt;')
        else:
            mm.eval('doCreateNclothCache 5 { "2", "1", "10", "OneFilePerFrame", "1", "","0","","0", "add", "0", "1", "1","0","1","mcx" };')


    def _delCache_callback(self):
        modifiers = QApplication.keyboardModifiers()
        if modifiers & Qt.ControlModifier or modifiers & Qt.ShiftModifier:
            mm.eval('fluidDeleteCacheOpt;')
        else:
            mm.eval('deleteCacheFile 2 { "keep", "" };')


    def _clothRig_list_callback(self):
        self._add_to_nucleusList()
        self._getPolyMesh()
        self.UI.collisionList.clear()
        self.UI.clothList.clear()
        self.UI.nucleus_name.clear()
        self.UI.constraintList.clear()
        self.UI.fieldList.clear()


    def _nucleusClear_callback(self):
        self.UI.nucleus_name.clear()


    def _nucleus_list_callback(self):
        items = self.UI.nucleusList.selectedItems()
        list = []
        try:
            self.UI.nucleus_name.setText(self.UI.nucleusList.currentItem().text())
        except:
            pass
        for i in range(len(items)):
            list.append(str(self.UI.nucleusList.selectedItems()[i].text()))

        modifiers = QApplication.keyboardModifiers()
        for i in list:
            obj = i+ "_GP"
            if modifiers == Qt.ShiftModifier or modifiers == Qt.ControlModifier:
                cmds.select(i, add=True)
            elif modifiers == Qt.AltModifier:
                cmds.select(obj)
            elif modifiers & Qt.AltModifier and (modifiers & Qt.ShiftModifier or modifiers & Qt.ControlModifier):
                cmds.select(obj, add=True)
            else:
                cmds.select(i)

        self._getCollision()
        self._getPolyMesh()
        self._getCloth(obj=[], mode=0)
        self._getDynamicConstraint()
        self._getField()


    def _nucleus_list_changed(self):
        items = self.UI.nucleusList.selectedItems()
        list = []
        try:
            self.UI.nucleus_name.setText(self.UI.nucleusList.currentItem().text())
        except:
            pass
        for i in range(len(items)):
            list.append(str(self.UI.nucleusList.selectedItems()[i].text()))

        self._getCollision()
        self._getPolyMesh()
        self._getCloth(obj = list, mode=1)
        self._getDynamicConstraint()
        self._getField()


    def _collision_list_callback(self):
        items = self.UI.collisionList.selectedItems()
        list = []
        for i in range(len(items)):
            list.append(str(self.UI.collisionList.selectedItems()[i].text()))

        modifiers = QApplication.keyboardModifiers()
        for i in list:
            obj = i.replace("_nRigid", "")
            if modifiers == Qt.ShiftModifier or modifiers == Qt.ControlModifier:
                cmds.select(i, add=True)
            elif modifiers == Qt.AltModifier:
                cmds.select(obj)
            elif modifiers & Qt.AltModifier and (modifiers & Qt.ShiftModifier or modifiers & Qt.ControlModifier):
                cmds.select(obj, add=True)
            else:
                cmds.select(i)
        self._getPolyMesh()


    def _polyMesh_list_callback(self):
        items = self.UI.polyMeshList.selectedItems()
        list = []
        for i in range(len(items)):
            list.append(str(self.UI.polyMeshList.selectedItems()[i].text()))

        modifiers = QApplication.keyboardModifiers()
        for i in list:
            if modifiers == Qt.ShiftModifier or modifiers == Qt.ControlModifier:
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
            obj = i.replace("_CLOTH", "_CLOTH_node")
            if modifiers == Qt.ShiftModifier or modifiers == Qt.ControlModifier:
                cmds.select(i, add=True)
            elif modifiers == Qt.AltModifier:
                cmds.select(obj)
            elif modifiers & Qt.AltModifier and (modifiers & Qt.ShiftModifier or modifiers & Qt.ControlModifier):
                cmds.select(obj, add=True)
            else:
                cmds.select(i)

        self._getDynamicConstraintSelect()
        self._getFieldSelect()
        self._getLocalWindSelect(sel= cloth)
        self._getPolyMesh()


    def _field_list_callback(self):
        items = self.UI.fieldList.selectedItems()
        list = []
        for i in range(len(items)):
            list.append(str(self.UI.fieldList.selectedItems()[i].text()))

        modifiers = QApplication.keyboardModifiers()
        for i in list:
            if modifiers == Qt.ShiftModifier or modifiers == Qt.ControlModifier:
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
            if modifiers == Qt.ShiftModifier or modifiers == Qt.ControlModifier:
                cmds.select(i, add=True)
            else:
                cmds.select(i)


    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    # utilities

    # honda
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


    def _setThicknessValues(self):
        sel = cmds.ls(sl=True)
        mu = utils.MyUtilities()
        mu.set_thickness_values(node = sel[0], scale = 1.0)


    # yoshida
    def _subdivWrap(self):
        mu = utils.MyUtilities()
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.ShiftModifier or modifiers == Qt.ControlModifier:
            mu._subdivWrap(lv = 2)
        elif modifiers & Qt.ShiftModifier and modifiers & Qt.ControlModifier:
            mu._subdivWrap(lv = 3)
        else:
            mu._subdivWrap(lv = 1)


    def _cleanupMeshes(self):
        sel = cmds.ls(sl=True)
        mu = utils.MyUtilities()
        tgt = mu._cleanupMeshes(cln = sel, bor = 0)
        pm.select(tgt)
        print('== cleaned up the Object(s) ==')


    def _selectHierarchyByType(self):
        mug = utilsGUI.MyUtilitiesGUI()
        mug._selectHierarchyByType_ui()


    def _selectCVs(self):
        mug = utilsGUI.MyUtilitiesGUI()
        mug._selectCVs_ui()


    # -------------------------------------------------------------------
    # -------------------------------------------------------------------
    # -------------------------------------------------------------------


    def _connect(self):
        self.UI.refreshButton.clicked.connect(self._refresh_callback)
        self.UI.newCacheButton.clicked.connect(self._newCache_callback)
        self.UI.delCacheButton.clicked.connect(self._delCache_callback)

        self.UI.nucleusClearButton.clicked.connect(self._nucleusClear_callback)

        #self.UI.projectComboBox.activated[str].connect(self.activated)

        # create button
        self.UI.createClothRigButton.clicked.connect(self._createClothRig)
        self.UI.createNClothButton.clicked.connect(self._createCloth)
        self.UI.makeCollideButton.clicked.connect(self._makeCollide)

        self.UI.localWindButton.clicked.connect(self._createLocalWind)

        # utilities
        # honda
        self.UI.applyFieldWeightButton.clicked.connect(self._openApplyFieldWeight)
        self.UI.submitJobButton.clicked.connect(self._openSubmitJob)
        self.UI.setupCFXSceneButton.clicked.connect(self._openSetupScene)
        self.UI.setupLocalGeoButton.clicked.connect(self._openSetupLocalGeo)
        self.UI.attachMultnCacheButton.clicked.connect(self._openAttachCache)
        self.UI.setThicknessValuesButton.clicked.connect(self._setThicknessValues)

        # yoshida
        self.UI.subdivWrapButton.clicked.connect(self._subdivWrap)
        self.UI.cleanUpButton.clicked.connect(self._cleanupMeshes)
        self.UI.SHBTButton.clicked.connect(self._selectHierarchyByType)
        self.UI.selectCVsButton.clicked.connect(self._selectCVs)

        # list callback
        self.UI.clothRigList.currentItemChanged.connect(self._clothRig_list_callback)
        self.UI.nucleusList.itemClicked.connect(self._nucleus_list_callback)
        self.UI.nucleusList.currentItemChanged.connect(self._nucleus_list_changed)
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


    # -------------------------------------------------------------------


    def load_setting(self):
        setting = QSettings("setting.ini", QSettings.IniFormat)
        self.restoreState(setting.value("windowState"))
        self.restoreGeometry(setting.value("geometry"))


    def closeEvent(self, event):
        setting = QSettings("setting.ini", QSettings.IniFormat)
        setting.setValue("windowState", self.saveState())
        setting.setValue("geometry", self.saveGeometry())

        # tooltip をUI起動前の状態に戻す
        if self.current_tooltip_state is not None:
            cmds.help(popupMode=self.current_tooltip_state)


    def showEvent(self, event):
        # tooltipの状態を取得
        self.current_tooltip_state = cmds.help(q=True, popupMode=True)

        # tooltipをONに瀬舘
        cmds.help(popupMode=True)


    # -------------------------------------------------------------------

# -------------------------------------------------------------------

# GUIの起動

def main():
    print('\n\n=================================')
    print('====== start-up cfxToolsUI ======')
    print('=================================\n')
    QApplication.instance()
    ui = GUI()
    ui.show()
    return ui


if __name__ == '__main__':
    main()
