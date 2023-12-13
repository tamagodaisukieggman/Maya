# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim
import maya.api.OpenMaya as OpenMaya2
import maya.OpenMayaUI as OpenMayaUI
import sys
import os
import codecs
import json
import timeit
import time
import math

from functools import partial
from collections import OrderedDict

from maya.app.general.mayaMixin import MayaQWidgetBaseMixin, MayaQWidgetDockableMixin
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

dir = '{}'.format(os.path.split(os.path.abspath(__file__))[0])
dir_path = dir.replace('\\', '/')
print(dir_path)
# CURRENT_PATH = "D:/"

# optionvar keys
ctrls_define_key = 'ctrls_define_in_picker'
sets_define_key = 'sets_define_in_picker'
mocap_define_key = 'mocap_define_in_picker'

# default json files
"""
pickrer_ctrls = 'Z:/mtk/tools/maya/modules/mtk3d/scripts/mtk3d/maya/rig/cyRig/defines/ctrls/mutsunokami_biped.json'
pickrer_sets = 'Z:/mtk/tools/maya/modules/mtk3d/scripts/mtk3d/maya/rig/cyRig/defines/pickerSets/mutsunokami_pickerSets.json'
picker_mocap = 'Z:/mtk/tools/maya/modules/mtk3d/scripts/mtk3d/maya/rig/cyRig/defines/mocap/mutsunokami_mocap_jd_ik.json'
"""

def save_optionvar(key, value):
    # key = self.WINDOW_NAME
    # value = self.get_settings()
    v = str(value)
    cmds.optionVar(sv=[key, v])
    # print 'Saved Setting'
    return True

def wrapper_save_optionvar(func):
    def new_func(*args, **kwargs):
        optionvarValue = func(*args, **kwargs)
        save_optionvar(optionvarValue[0], optionvarValue[1])
    return new_func

def load_optionvar(key):
    if cmds.optionVar(ex=key):
        return eval(cmds.optionVar(q=key))
    else:
        return None

class BaseCallBack(object):
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

class UndoCallback(BaseCallBack):
    def __call__(self, *args):
        cmds.undoInfo(openChunk=1)
        try:
            return self.func(*self.args, **self.kwargs)
        except:
                raise
        finally:
            cmds.undoInfo(closeChunk=1)

class GUI(MayaQWidgetBaseMixin, QMainWindow):

    def __init__(self, parent=None):
        super(GUI, self).__init__(parent)
        loader = QUiLoader()
        uiFilePath = '{}/{}'.format(dir_path, 'UI.ui')
        print(uiFilePath)
        self.UI = loader.load(uiFilePath)
        self.setCentralWidget(self.UI)
        self.UI.BackGround.setPixmap(QPixmap('{}/{}'.format(dir_path, 'chara.jpg')))
        self._filter = Filter()

        self.UI.widget.installEventFilter(self._filter)
        # self.UI.pushButton.clicked.connect(self.test)
        self.setWindowTitle("Picker")
        self.resize(575, 1008)

        self.UI.alphaSlider.setRange(10,100)
        self.UI.alphaSlider.setValue(100)
        self.UI.alphaSlider.valueChanged.connect(self.changeUIOpacity)

        # ikfk
        self.arms_l_region_fk = ['clavicle_l_001_fk', 'upperarm_l_001_fk', 'lowerarm_l_001_fk', 'hand_l_001_fk']
        self.arms_l_region_ik = ['clavicle_l_001_ik', 'elbow_l_001_ik', 'hand_l_001_ik', 'hand_l_001_ik_rot']

        self.arms_r_region_fk = ['clavicle_r_001_fk', 'upperarm_r_001_fk', 'lowerarm_r_001_fk', 'hand_r_001_fk']
        self.arms_r_region_ik = ['clavicle_r_001_ik', 'elbow_r_001_ik', 'hand_r_001_ik', 'hand_r_001_ik_rot']

        self.legs_l_region_fk = ['thigh_l_001_fk', 'calf_l_001_fk', 'foot_l_001_fk', 'ball_l_001_fk']
        self.legs_l_region_ik = ['foot_l_001_ik', 'foot_l_001_ik_rot', 'ball_l_001_ik', 'knee_l_001_ik']

        self.legs_r_region_fk = ['thigh_r_001_fk', 'calf_r_001_fk', 'foot_r_001_fk', 'ball_r_001_fk']
        self.legs_r_region_ik = ['foot_r_001_ik', 'foot_r_001_ik_rot', 'ball_r_001_ik', 'knee_r_001_ik']

        self.UI.matchBake_arms.stateChanged.connect(self.setMatchBake_arms)
        self.UI.matchBake_legs.stateChanged.connect(self.setMatchBake_legs)

        self.UI.setTimeSlider.stateChanged.connect(self.setTimeSlider)
        for dsbox in [self.UI.setStartTime, self.UI.setEndTime, self.UI.matchPv_arms_l, self.UI.matchPv_arms_r, self.UI.matchPv_legs_l, self.UI.matchPv_legs_r]:
            dsbox.setMaximum(99999999)
            dsbox.setMinimum(-99999999)
            dsbox.setDecimals(3)

        self.UI.matchPv_arms_l.setValue(20)
        self.UI.matchPv_arms_r.setValue(20)
        self.UI.matchPv_legs_l.setValue(20)
        self.UI.matchPv_legs_r.setValue(20)

        self.UI.setCurrentStartTime.clicked.connect(self.setCurrentStartTime)
        self.UI.setCurrentEndTime.clicked.connect(self.setCurrentEndTime)
        self.UI.doneMatchBake.clicked.connect(UndoCallback(self.ikfk_match_bake))

        # QPushButton
        self.pushBuf = []
        for child in self.UI.widget.findChildren(QPushButton):
            if child.objectName() == 'arms_l_ikfk':
                child.clicked.connect(self.arms_l_ikfk_switch)
                child.setContextMenuPolicy(Qt.CustomContextMenu)
                child.customContextMenuRequested.connect(self.onContextMenu_ikfk)
                self.arms_l_ikfk_switch()
            elif child.objectName() == 'arms_r_ikfk':
                child.clicked.connect(self.arms_r_ikfk_switch)
                child.setContextMenuPolicy(Qt.CustomContextMenu)
                child.customContextMenuRequested.connect(self.onContextMenu_ikfk)
                self.arms_r_ikfk_switch()
            elif child.objectName() == 'legs_l_ikfk':
                child.clicked.connect(self.legs_l_ikfk_switch)
                child.setContextMenuPolicy(Qt.CustomContextMenu)
                child.customContextMenuRequested.connect(self.onContextMenu_ikfk)
                self.legs_l_ikfk_switch()
            elif child.objectName() == 'legs_r_ikfk':
                child.clicked.connect(self.legs_r_ikfk_switch)
                child.setContextMenuPolicy(Qt.CustomContextMenu)
                child.customContextMenuRequested.connect(self.onContextMenu_ikfk)
                self.legs_r_ikfk_switch()
            elif child.objectName() == 'deselect':
                child.clicked.connect(UndoCallback(self.deselect))
            elif child.objectName() == 'zeroOut':
                child.clicked.connect(UndoCallback(self.zeroOut))
            elif child.objectName() == 'ik_SCC_Set':
                child.clicked.connect(UndoCallback(self.ik_segmentScaleCompensate_set))
            else:
                child.setContextMenuPolicy(Qt.CustomContextMenu)
                child.customContextMenuRequested.connect(self.onContextMenu)
            child.clicked.connect(self.Push)

            initBtnStyle_color(obj=child)

        # DefineList
        self.defineDict = OrderedDict()
        self.model = QStandardItemModel(0,0)
        self.UI.defineTable.setModel(self.model)

        self.UI.defineTableClear.clicked.connect(self.clearDefineTable)
        self.UI.defineTableExport.clicked.connect(self.exportDefineTable)
        self.UI.defineTableImport.clicked.connect(self.importDefineTable)

        self.UI.defineMode.stateChanged.connect(self.showHideDefineIkhandle)
        self.showHideDefineIkhandle()

        # Picker Sets
        self.pickerSetsModel = QStandardItemModel()
        self.pickerSetsModel.setHorizontalHeaderLabels(['Picker Sets'])
        self.UI.pickerSetsButtons.setModel(self.pickerSetsModel)
        self.UI.pickerSetsButtons.setUniformRowHeights(True)
        self.UI.pickerSetsButtons.setSelectionMode(QAbstractItemView.ContiguousSelection)
        self.UI.pickerSetsButtons.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.UI.pickerSetsButtons.setContextMenuPolicy(Qt.CustomContextMenu)
        self.UI.pickerSetsButtons.customContextMenuRequested.connect(self.onContextMenu)
        self.UI.pickerSetsButtons.clicked.connect(self.on_click)

        self.UI.defineTableClear_2.clicked.connect(self.clearDefineTable_2)
        self.UI.defineTableExport_2.clicked.connect(self.exportDefineTable_2)
        self.UI.defineTableImport_2.clicked.connect(self.importDefineTable_2)

        # Mocap
        self.tPoseData = OrderedDict()
        self.mocapSetModel = QStandardItemModel(0,0)
        self.UI.defineTable_mocap.setModel(self.mocapSetModel)

        self.UI.defineTableClear_3.clicked.connect(self.clearDefineTable_3)
        self.UI.defineTableExport_3.clicked.connect(self.exportDefineTable_3)
        self.UI.defineTableImport_3.clicked.connect(self.importDefineTable_3)

        self.UI.mocapOffset_x.setMaximum(99999999)
        self.UI.mocapOffset_x.setMinimum(-99999999)
        self.UI.mocapOffset_x.setDecimals(3)
        self.UI.mocapOffset_y.setMaximum(99999999)
        self.UI.mocapOffset_y.setMinimum(-99999999)
        self.UI.mocapOffset_y.setDecimals(3)
        self.UI.mocapOffset_z.setMaximum(99999999)
        self.UI.mocapOffset_z.setMinimum(-99999999)
        self.UI.mocapOffset_z.setDecimals(3)

        self.UI.mocapMatch.clicked.connect(UndoCallback(self.getSetRotation_offset_call))
        self.UI.mocapMatch_tweak.clicked.connect(UndoCallback(self.tweakRotate))
        self.UI.mocapSetTpose.clicked.connect(UndoCallback(self.setTpose))
        self.UI.mocapConnect.clicked.connect(UndoCallback(self.connectMocapJnts))

        # get nameSpace
        self.getNameSpace()
        self.UI.refresh.clicked.connect(self.getNameSpace)
        pix = QPixmap(':/refresh.png')
        icon = QIcon(pix)
        self.UI.refresh.setIcon(icon)
        self.scriptJob_numA = cmds.scriptJob(event=['SceneOpened', self.getNameSpace], protected=1)
        self.scriptJob_numB = cmds.scriptJob(event=['SelectionChanged', self.getRowColumn_from_table], protected=1)

        # Path History
        self.UI.currentDefineTableImport.clicked.connect(self.import_comboxChanged)
        self.UI.currentDefineTableImport_2.clicked.connect(self.import_comboxChanged_2)
        self.UI.currentDefineTableImport_3.clicked.connect(self.import_comboxChanged_3)

        #  Space Match Bake
        self.updateSpaceAttr()
        self.UI.spaceAttribute_le.setText('space')
        self.UI.spaceAttribute_le.textChanged.connect(UndoCallback(self.updateSpaceAttr))
        self.UI.spaceMatchBake_btn.clicked.connect(UndoCallback(self.spaceMatchBake))
        self.UI.changeSpace_refresh_btn.clicked.connect(UndoCallback(self.updateSpaceAttr))

        # self.UI.defineTable.setMouseTracking(True)
        # self.UI.defineTable.entered.connect(self.handleItemEntered)

        #
        try:
            self.loadRecentFiles()
        except Exception as e:
            print(e)

        # import default
        try:
            path = '{}'.format(pickrer_ctrls)
            self.importDefineTable(file_path=path)
        except:
            pass
        try:
            path2 = '{}'.format(pickrer_sets)
            self.importDefineTable_2(file_path=path2)
        except:
            pass
        try:
            path3 = '{}'.format(picker_mocap)
            self.importDefineTable_3(file_path=path3)
        except:
            pass

        try:
            dh_path = self.UI.defineHistory.currentText()
            if dh_path == '':
                pass
            else:
                self.importDefineTable(file_path=dh_path)
        except Exception as e:
            print(e)
        try:
            ps_path = self.UI.pickerSetsHistory.currentText()
            if ps_path == '':
                pass
            else:
                self.importDefineTable_2(file_path=ps_path)
        except Exception as e:
            print(e)
        try:
            mh_path = self.UI.mocapHistory.currentText()
            if mh_path == '':
                pass
            else:
                self.importDefineTable_3(file_path=mh_path)
        except Exception as e:
            print(e)

    def closeEvent(self, event):
        cmds.scriptJob(k=self.scriptJob_numA, f=1)
        cmds.scriptJob(k=self.scriptJob_numB, f=1)

    def getRowColumn_from_table(self, *args, **kwargs):
        sel = cmds.ls(sl=1)
        model = self.UI.defineTable.model()
        col = model.columnCount()
        row = model.rowCount()

        objects = []
        headerObjects = [model.headerData(r, Qt.Vertical) for r in range(row)]
        for c in range(col):
            for o in range(len(headerObjects)):
                try:
                    objects.append(model.item(o, c).text())
                except Exception as e:
                    pass

        namespace = self.UI.nameSpaceList.currentText()

        if namespace == '':
            selectObjects = ['{}'.format(obj) for obj in objects]
        else:
            selectObjects = ['{}:{}'.format(namespace, obj) for obj in objects]

        s1 = set(sel)
        s2 = set(selectObjects)
        matchObjects = list(s1 & s2)

        exist_headerItems = []
        for c in range(col):
            for o in range(len(headerObjects)):
                try:
                    obj = model.item(o, c).text()
                    if namespace == '':
                        modelObject = '{}'.format(obj)
                    else:
                        modelObject = '{}:{}'.format(namespace, obj)
                    if modelObject in matchObjects:
                        exist_headerItems.append(headerObjects[o])
                except Exception as e:
                    pass

        for child in self.UI.widget.findChildren(QPushButton):
            if child.objectName() in exist_headerItems:
                changeBtnStyle_color(obj=child)
            else:
                initBtnStyle_color(obj=child, raiseObj=False)

    def changeUIOpacity(self, *args, **kwargs):
        v = self.UI.alphaSlider.value()
        self.setWindowOpacity(v/100.0)

    def onContextMenu(self, point):
        # show context menu
        btn = self.sender()
        self.defineSelectObject(obj=btn)
        menuPosition = btn.mapToGlobal(point)
        # popMenu = QMenu(self)
        popMenu = self.createPopMenu(obj=btn)
        # print(popMenu, 'popMenu')
        popMenu.move(menuPosition)
        popMenu.show()

    def onContextMenu_ikfk(self, point):
        # show context menu
        btn = self.sender()
        self.defineSelectObject(obj=btn)
        menuPosition = btn.mapToGlobal(point)
        # popMenu = QMenu(self)
        popMenu = self.createPopMenu_ikfk(obj=btn)
        # print(popMenu, 'popMenu')
        popMenu.move(menuPosition)
        popMenu.show()

    def defineSelectObject(self, obj=None):
        sel = cmds.ls(os=1)
        spl = [ss.split(':')[-1] for ss in sel]
        self.updateDefineDict(obj=obj, defineList=spl)

    def updateDefineDict(self, obj=None, defineList=None):
        try:
            if obj.objectName() not in self.defineDict.keys():
                pass
                # print('orderd')
        except Exception as e:
            self.defineDict = OrderedDict()
        if obj.objectName() == 'arms_l_ikfk' or obj.objectName() == 'arms_r_ikfk' or obj.objectName() == 'legs_l_ikfk' or obj.objectName() == 'legs_r_ikfk':
            try:
                self.defineDict['{}:{}'.format(obj.objectName(), obj.text())] = [ikfkDefineContextMenu()[0], str(ikfkDefineContextMenu()[2])]
            except Exception as e:
                print('Nothing has selected attribute.')
        else:
            self.defineDict[obj.objectName()] = defineList

    def setDefine(self, *args, **kwargs):
        data = self.defineDict
        # print(data)
        self.model.removeRows(0, self.model.rowCount())
        self.model.removeColumns(0, self.model.columnCount())

        i = 0
        for key in data.keys():
            for j in range(len(data[key])):
                item = QStandardItem(data[key][j])
                self.model.setItem(i,j,item)
                self.model.setHeaderData(i, Qt.Vertical, item)
                self.model.setHeaderData(j, Qt.Horizontal, j)
            i += 1
        self.model.setVerticalHeaderLabels(data.keys())

    def clearDefineTable(self, *args, **kwargs):
        for child in self.UI.widget.findChildren(QTableView):
            if child.objectName() == 'defineTable':
                self.model.removeRows(0, self.model.rowCount())
        try:
            if self.defineDict:
                self.defineDict = OrderedDict()
            else:
                pass
        except Exception as e:
            pass

    def clearDefineTable_2(self, *args, **kwargs):
        for child in self.UI.widget.findChildren(QTreeView):
            if child.objectName() == 'pickerSetsButtons':
                self.pickerSetsModel.removeRows(0, self.pickerSetsModel.rowCount())

    def clearDefineTable_3(self, *args, **kwargs):
        for child in self.UI.widget.findChildren(QTableView):
            if child.objectName() == 'defineTable_mocap':
                self.mocapSetModel.removeRows(0, self.mocapSetModel.rowCount())
        try:
            if self.tPoseData:
                self.tPoseData = OrderedDict()
            else:
                pass
        except Exception as e:
            pass

    def showHideDefineIkhandle(self, *args, **kwargs):
        if self.UI.defineMode.isChecked():
            initBtnStyle_color(self.UI.arms_l_fkToikJoints)
            initBtnStyle_color(self.UI.arms_r_fkToikJoints)
            initBtnStyle_color(self.UI.legs_l_fkToikJoints)
            initBtnStyle_color(self.UI.legs_r_fkToikJoints)
        else:
            invisBtnStyle(self.UI.arms_l_fkToikJoints)
            invisBtnStyle(self.UI.arms_r_fkToikJoints)
            invisBtnStyle(self.UI.legs_l_fkToikJoints)
            invisBtnStyle(self.UI.legs_r_fkToikJoints)

    def defineTableFileDialog_export(self, *args, **kwargs):
        filename = cmds.fileDialog2(ds=2, cap='File', okc='Done', ff='All Files (*.*);;*.json', fm=0)
        if filename is None:
            return
        return filename[0]

    def defineTableFileDialog_import(self, *args, **kwargs):
        filename = cmds.fileDialog2(ds=2, cap='File', okc='Done', ff='All Files (*.*);;*.json', fm=1)
        if filename is None:
            return
        return filename[0]

    @wrapper_save_optionvar
    def exportDefineTable(self, *args, **kwargs):
        json = JsonFile()
        file_path = self.defineTableFileDialog_export()
        if file_path is None:
            print('Export Error')
            return
        json.write('{}'.format(file_path), self.defineDict)
        # json.read('.json')
        return ctrls_define_key, self.getAddItems_comboBox(self.UI.defineHistory, file_path)

    @wrapper_save_optionvar
    def importDefineTable(self, file_path=None):
        json = JsonFile()
        if not file_path:
            file_path = self.defineTableFileDialog_import()
        self.defineDict = json.read('{}'.format(file_path))
        self.setDefine()
        return ctrls_define_key, self.getAddItems_comboBox(self.UI.defineHistory, file_path)

    @wrapper_save_optionvar
    def exportDefineTable_2(self, *args, **kwargs):
        setsDict = self.get_all_pickerSets()
        json = JsonFile()
        file_path = self.defineTableFileDialog_export()
        if file_path is None:
            print('Export Error')
            return
        json.write('{}'.format(file_path), setsDict)
        return sets_define_key, self.getAddItems_comboBox(self.UI.pickerSetsHistory, file_path)

    @wrapper_save_optionvar
    def exportDefineTable_3(self, *args, **kwargs):
        setsDict = self.tPoseData
        json = JsonFile()
        file_path = self.defineTableFileDialog_export()
        if file_path is None:
            print('Export Error')
            return
        json.write('{}'.format(file_path), setsDict)

        return mocap_define_key, self.getAddItems_comboBox(self.UI.mocapHistory, file_path)

    @wrapper_save_optionvar
    def importDefineTable_2(self, file_path=None):
        json = JsonFile()
        if not file_path:
            file_path = self.defineTableFileDialog_import()
        setsDict = json.read('{}'.format(file_path))
        for key in setsDict.keys():
            self.create_picker_sets_button(dialog=None, text=key, sel=setsDict[key])
        return sets_define_key, self.getAddItems_comboBox(self.UI.pickerSetsHistory, file_path)

    @wrapper_save_optionvar
    def importDefineTable_3(self, file_path=None):
        json = JsonFile()
        if not file_path:
            file_path = self.defineTableFileDialog_import()
        self.tPoseData = json.read('{}'.format(file_path))
        self.define_mocap_table()

        return mocap_define_key, self.getAddItems_comboBox(self.UI.mocapHistory, file_path)

    def import_comboxChanged(self, *args, **kwargs):
        currentText = self.UI.defineHistory.currentText()
        if currentText != '':
            self.importDefineTable(file_path=currentText)

    def import_comboxChanged_2(self, *args, **kwargs):
        currentText = self.UI.pickerSetsHistory.currentText()
        if currentText != '':
            self.importDefineTable_2(file_path=currentText)

    def import_comboxChanged_3(self, *args, **kwargs):
        currentText = self.UI.mocapHistory.currentText()
        if currentText != '':
            self.importDefineTable_3(file_path=currentText)

    def getAddItems_comboBox(self, box, item):
        if item == None:
            return
        items = [box.itemText(i) for i in range(box.count())]
        items = items[::-1]
        if items == []:
            pass

        if 10 < len(items):
            items.pop(0)

        try:
            items.remove(item)
        except Exception as e:
            pass

        if item not in items:
            items.append(item)
            box.clear()
            [box.addItem(i) for i in items[::-1]]
            # box.setCurrentIndex(len(items)-1)
            box.setCurrentIndex(0)

        return items

    def loadRecentFiles(self, *args, **kwargs):
        keys = [ctrls_define_key, sets_define_key, mocap_define_key]
        for key in keys:
            files = load_optionvar(key)
            if files == None:
                return
            if key == ctrls_define_key:
                for file_path in files:
                    self.getAddItems_comboBox(self.UI.defineHistory, file_path)
            elif key == sets_define_key:
                for file_path in files:
                    self.getAddItems_comboBox(self.UI.pickerSetsHistory, file_path)
            elif key == mocap_define_key:
                for file_path in files:
                    self.getAddItems_comboBox(self.UI.mocapHistory, file_path)

    def createPopMenu(self, obj=None):
        Sender = self.sender()
        # print(Sender)
        self.popMenu = QMenu(self)
        if self.UI.defineMode.checkState():
            action = QAction('Define Selected Objects', self)
            action.triggered.connect(partial(self.setDefine))
            self.popMenu.addAction(action)
        elif Sender.objectName() == 'allSpace':
            self.listUpSpace('all')
        elif Sender.objectName() != 'allSpace' and self.UI.pickerSetsCheck.checkState() == False:
            self.listUpSpace('selection')
        elif self.UI.pickerSetsCheck.checkState() and Sender.objectName() != 'allSpace':
            action = QAction('Add Picker Sets', self)
            action.triggered.connect(partial(self.create_picker_sets_button, True, None, None))
            self.popMenu.addAction(action)

        return self.popMenu

    def listUpSpace(self, type):
        selectObjects = []
        if type == 'all':
            model = self.UI.defineTable.model()
            col = model.columnCount()
            row = model.rowCount()

            objects = []
            headerObjects = [model.headerData(r, Qt.Vertical) for r in range(row)]
            for c in range(col):
                for o in range(len(headerObjects)):
                    try:
                        objects.append(model.item(o, c).text())
                    except Exception as e:
                        pass

            namespace = self.UI.nameSpaceList.currentText()

            if namespace == '':
                selectObjects = ['{}'.format(obj) for obj in objects]
            else:
                selectObjects = ['{}:{}'.format(namespace, obj) for obj in objects]

        elif type == 'selection':
            selectObjects = cmds.ls(os=1)

        allSpace = []
        # self.popMenu.clear()
        objects = OrderedDict()
        for obj in selectObjects:
            if cmds.objExists(obj):
                objects[obj] = None
            try:
                spcQry = cmds.attributeQuery('space', node='{}'.format(obj), le=1)[0]
                spaceList = spcQry.split(':')
                objects[obj] = spaceList
            except Exception as e:
                spaceList = []
            if spaceList:
                for space in spaceList:
                    allSpace.append(space)
        correctSpace = list(set(allSpace))
        for space in correctSpace:
            if type == 'all':
                action = QAction('{}'.format(space), self)
            elif type == 'selection':
                action = QAction('{} > {}'.format(selectObjects, space), self)
            action.triggered.connect(UndoCallback(partial(self.changeSpace, objects, space)))
            self.popMenu.addAction(action)

    def changeSpace(self, objects, space):
        spaceValues = OrderedDict()
        skipList = []
        dups = []
        dupsDum = OrderedDict()
        dupsDumVal = OrderedDict()
        poCons = []
        oriCons = []

        for obj in objects.keys():
            if cmds.nodeType(obj) != 'transform':
                objects.pop(obj)

        sel = cmds.ls(sl=1)
        for obj in objects.keys():
            dup = cmds.duplicate(obj, po=1)[0]
            dups.append(dup)
            cmds.setAttr('{}.tx'.format(dup), k=1, l=0)
            cmds.setAttr('{}.ty'.format(dup), k=1, l=0)
            cmds.setAttr('{}.tz'.format(dup), k=1, l=0)
            cmds.setAttr('{}.rx'.format(dup), k=1, l=0)
            cmds.setAttr('{}.ry'.format(dup), k=1, l=0)
            cmds.setAttr('{}.rz'.format(dup), k=1, l=0)
            cmds.setAttr('{}.sx'.format(dup), k=1, l=0)
            cmds.setAttr('{}.sy'.format(dup), k=1, l=0)
            cmds.setAttr('{}.sz'.format(dup), k=1, l=0)
            mel.eval("source channelBoxCommand;")
            mel.eval('CBunlockAttr "{}.sx";'.format(dup))
            mel.eval('CBunlockAttr "{}.sy";'.format(dup))
            mel.eval('CBunlockAttr "{}.sz";'.format(dup))
            cmds.setAttr('{}.sx'.format(dup), 1)
            cmds.setAttr('{}.sy'.format(dup), 1)
            cmds.setAttr('{}.sz'.format(dup), 1)
            dup_dummy = cmds.duplicate(obj, po=1)[0]
            dupsDum[obj] = dup_dummy

            cmds.parent(dup, w=1)
            attr = cmds.listAttr(obj, k=1)
            # pos
            if 'translateX' not in attr:
                skipList.append('x')
            elif 'translateY' not in attr:
                skipList.append('y')
            elif 'translateZ' not in attr:
                skipList.append('z')
            else:
                spaceValues['skip'] = None
            spaceValues['skip'] = skipList
            try:
                po = cmds.pointConstraint(dup, obj, w=1, mo=1, **spaceValues)
                cmds.pointConstraint(obj, dup_dummy, w=1, mo=1, **spaceValues)
                poCons.append(po[0])
            except Exception as e:
                pass
            skipList = []

            # rot
            if 'rotateX' not in attr:
                skipList.append('x')
            elif 'rotateY' not in attr:
                skipList.append('y')
            elif 'rotateZ' not in attr:
                skipList.append('z')
            else:
                spaceValues['skip'] = None
            spaceValues['skip'] = skipList
            try:
                ori = cmds.orientConstraint(dup, obj, w=1, mo=1, **spaceValues)
                cmds.orientConstraint(obj, dup_dummy, w=1, mo=1, **spaceValues)
                oriCons.append(ori[0])
            except Exception as e:
                pass
            skipList = []

        for obj in objects.keys():
            try:
                cmds.setAttr('{}.space'.format(obj), objects[obj].index(space))
            except Exception as e:
                pass

        for obj in objects.keys():
            dupwt = cmds.xform(dupsDum[obj], q=1, t=1, ws=1)
            dupwr = cmds.xform(dupsDum[obj], q=1, ro=1, ws=1)
            dupsDumVal[obj] = [dupwt, dupwr]

        try:
            cmds.delete(poCons)
        except:
            pass
        try:
            cmds.delete(oriCons)
        except:
            pass
        try:
            cmds.delete(dups)
        except:
            pass

        for obj in objects.keys():
            cmds.xform(obj, t=dupsDumVal[obj][0], ro=dupsDumVal[obj][1], ws=1, a=1)
            cmds.delete(dupsDum[obj])

        cmds.select(sel)

    def createPopMenu_ikfk(self, obj=None):
        # main
        self.popMenu_ikfk = QMenu(self)

        # parts
        try:
            self.ikfk_obj = ikfkDefineContextMenu()[1]
            action = QAction(self.ikfk_obj, self)
            action.triggered.connect(partial(self.setDefine))
            self.popMenu_ikfk.addAction(action)
            self.popMenu_ikfk.addSeparator()
            self.ikfk_value = ikfkDefineContextMenu()[2]
            self.popMenu_ikfk.addAction(QAction(str(self.ikfk_value), self))
        except Exception as e:
            pass
        return self.popMenu_ikfk

    def deselect(self, *args, **kwargs):
        cmds.select(cl=1)
        """
        for child in self.UI.widget.findChildren(QPushButton):
            if child.objectName() == 'arms_l_ikfk' or child.objectName() == 'arms_r_ikfk' or child.objectName() == 'legs_l_ikfk' or child.objectName() == 'legs_r_ikfk' or child.objectName() == 'deselect':
                continue
            else:
                initBtnStyle_color(obj=child, raiseObj=False)
        """

    def zeroOut(self, *args, **kwargs):
        transform = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']
        for child in self.UI.widget.findChildren(QPushButton):
            try:
                selectObjects = self._filter.selectButtonRelease(self.UI.widget, [child], False)
            except Exception as e:
                continue
            for obj in selectObjects:
                for i in transform:
                    if i == 'sx' or i == 'sy' or i == 'sz':
                        j = 1.0
                    else:
                        j = 0.0
                    try:
                        cmds.setAttr('{}.{}'.format(obj, i), j)
                    except Exception as e:
                        pass

    def getNameSpace(self, *args, **kwargs):
        self.UI.nameSpaceList.clear()
        self.UI.nameSpaceList.addItem('')

        # Current Namespace
        exclude_list = ['UI', 'shared']

        current = cmds.namespaceInfo(cur=True)
        cmds.namespace(set=':')
        namespaces = ['{}'.format(ns) for ns in cmds.namespaceInfo(lon=True) if ns not in exclude_list]
        cmds.namespace(set=current)

        for name in namespaces:
            self.UI.nameSpaceList.addItem(name)

        # Reference Nodes
        rn = cmds.ls(type="reference", r=1)
        for i in rn:
            list = i.split(":")
            count = len(list)
            if count == 1:
                for i in list:
                    NSP = i.split("RN")
                    if NSP[0]:
                        self.UI.nameSpaceList.addItem(NSP[0])
            else:
                pass

    def Push(self, *args, **kwargs):
        Sender =self.sender()
        modifiers = QApplication.keyboardModifiers()

        if Sender.objectName() == 'arms_l_ikfk' or Sender.objectName() == 'arms_r_ikfk' or Sender.objectName() == 'legs_l_ikfk' or Sender.objectName() == 'legs_r_ikfk':
            # print(self.defineDict['{}:{}'.format(Sender.objectName(), Sender.text())])
            try:
                val = Sender.text()
            except Exception as e:
                val = 'FK'
            if val == 'IK':
                val2 = 'FK'
            else:
                val2 = 'IK'
            if Sender.objectName() == 'arms_l_ikfk':
                if self.UI.arms_l_ikfk_match.checkState():
                    # print(val)
                    UndoCallback(self.ikfkMatch_arms_l(val))
                    print('{} to {} match'.format(val, val2))
            elif Sender.objectName() == 'arms_r_ikfk':
                if self.UI.arms_r_ikfk_match.checkState():
                    # print(val)
                    UndoCallback(self.ikfkMatch_arms_r(val))
                    print('{} to {} match'.format(val, val2))
            elif Sender.objectName() == 'legs_l_ikfk':
                if self.UI.legs_l_ikfk_match.checkState():
                    # print(val)
                    UndoCallback(self.ikfkMatch_legs_l(val))
                    print('{} to {} match'.format(val, val2))
            elif Sender.objectName() == 'legs_r_ikfk':
                if self.UI.legs_r_ikfk_match.checkState():
                    # print(val)
                    UndoCallback(self.ikfkMatch_legs_r(val))
                    print('{} to {} match'.format(val, val2))

            initBtnStyle_color(obj=Sender, raiseObj=False)
            try:
                ikfkvalues = self.defineDict['{}:{}'.format(Sender.objectName(), Sender.text())]
                self.ikfk_switch(ikfkvalues[0], ikfkvalues[1])
            except Exception as e:
                pass
            return
        # 押したボタンがキャッシュされていなかったら
        elif Sender.objectName() not in self.defineDict.keys():
            return
        selectObjects = self._filter.selectButtonRelease(self.UI.widget, [Sender], False)
        try:
            #  CtrlかShiftを押しながらクリックしたとき
            if modifiers == Qt.ShiftModifier:
                cmds.select(selectObjects, add=1)
                changeBtnStyle_color(obj=Sender)
                self.pushBuf.append(Sender)
            elif modifiers == Qt.ControlModifier:
                cmds.select(selectObjects, d=1)
                if Sender in self.pushBuf:
                    self.pushBuf.remove(Sender)
                    initBtnStyle_color(obj=Sender, raiseObj=False)
            else:
                for obj in self.pushBuf:
                    initBtnStyle_color(obj=obj, raiseObj=False)
                cmds.select(selectObjects)
                changeBtnStyle_color(obj=Sender)
                self.pushBuf.append(Sender)
        except Exception as e:
            pass
            # cmds.select(cl=1)

    def ikfkSwitch_vis(self, Sender, val, region_fk, region_ik):
        if val == 'FK':
            for child in self.UI.widget.findChildren(QPushButton):
                if child.objectName() in region_fk:
                    child.setEnabled(False)
                    invisBtnStyle(obj=child)
                elif child.objectName() in region_ik:
                    child.setEnabled(True)
                    initBtnStyle_color(obj=child)
            try:
                Sender.setText('IK')
            except Exception as e:
                pass
        elif val == 'IK':
            for child in self.UI.widget.findChildren(QPushButton):
                if child.objectName() in region_ik:
                    child.setEnabled(False)
                    invisBtnStyle(obj=child)
                elif child.objectName() in region_fk:
                    child.setEnabled(True)
                    initBtnStyle_color(obj=child)
            try:
                Sender.setText('FK')
            except Exception as e:
                pass

    def ikfkMatch_arms_l(self, val):
        sel = cmds.ls(os=1)
        for child in self.UI.widget.findChildren(QPushButton):
            if child.objectName() == 'clavicle_l_001_ik':
                self.clavicle_ik_l = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'elbow_l_001_ik':
                self.elbow_ik_l = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'hand_l_001_ik':
                self.hand_ik_l = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'hand_l_001_ik_rot':
                self.hand_ik_l_rot = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'clavicle_l_001_fk':
                self.clavicle_fk_l = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'upperarm_l_001_fk':
                self.start_fk_l = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'lowerarm_l_001_fk':
                self.middle_fk_l = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'hand_l_001_fk':
                self.end_fk_l = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'arms_l_fkToikJoints':
                self.hand_ik_handle_l = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'pelvis_c_001':
                self.pelvis = self._filter.selectButtonRelease(self.UI.widget, [child], True)
        if val == 'IK':
            namespace = self.UI.nameSpaceList.currentText()
            ik_to_fk = IKtoFK(namespace)
            value = ik_to_fk.current_match(l_legs=False, r_legs=False, l_arms=True, r_arms=False)
            # ik_to_fk.bakeanim(select_timeslider=True, l_legs=False, r_legs=False, l_arms=True, r_arms=False)
            # value = ikToFkMatch(startJnt=self.start_fk_l[0], middleJnt=self.middle_fk_l[0], endJnt=self.end_fk_l[0], ikCtrl=self.hand_ik_l[0], ikPvCtrl=self.elbow_ik_l[0], ikRotCtrl=self.hand_ik_l_rot[0], clvFkCtrl=self.clavicle_fk_l[0], clvIkCtrl=self.clavicle_ik_l[0], foot=0, ballFkCtrl=None, ballIkCtrl=None, pelvis=self.pelvis[0], move=self.UI.matchPv_arms_l.value())
        elif val == 'FK':
            value = fkToIkMatch(startFkCtrl=self.start_fk_l[0], middleFkCtrl=self.middle_fk_l[0], endFkCtrl=self.end_fk_l[0], ikHandle=self.hand_ik_handle_l[0], clvIkCtrl=self.clavicle_ik_l[0], clvFkCtrl=self.clavicle_fk_l[0])
        cmds.select(sel)
        return value

    def ikfkMatch_arms_r(self, val):
        sel = cmds.ls(os=1)
        for child in self.UI.widget.findChildren(QPushButton):
            if child.objectName() == 'clavicle_r_001_ik':
                self.clavicle_ik_r = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'elbow_r_001_ik':
                self.elbow_ik_r = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'hand_r_001_ik':
                self.hand_ik_r = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'hand_r_001_ik_rot':
                self.hand_ik_r_rot = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'clavicle_r_001_fk':
                self.clavicle_fk_r = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'upperarm_r_001_fk':
                self.start_fk_r = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'lowerarm_r_001_fk':
                self.middle_fk_r = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'hand_r_001_fk':
                self.end_fk_r = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'arms_r_fkToikJoints':
                self.hand_ik_handle_r = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'pelvis_c_001':
                self.pelvis = self._filter.selectButtonRelease(self.UI.widget, [child], True)
        if val == 'IK':
            namespace = self.UI.nameSpaceList.currentText()
            ik_to_fk = IKtoFK(namespace)
            value = ik_to_fk.current_match(l_legs=False, r_legs=False, l_arms=False, r_arms=True)
            # value = ikToFkMatch(startJnt=self.start_fk_r[0], middleJnt=self.middle_fk_r[0], endJnt=self.end_fk_r[0], ikCtrl=self.hand_ik_r[0], ikPvCtrl=self.elbow_ik_r[0], ikRotCtrl=self.hand_ik_r_rot[0], clvFkCtrl=self.clavicle_fk_r[0], clvIkCtrl=self.clavicle_ik_r[0], foot=0, ballFkCtrl=None, ballIkCtrl=None, pelvis=self.pelvis[0], move=self.UI.matchPv_arms_r.value())
        elif val == 'FK':
            value = fkToIkMatch(startFkCtrl=self.start_fk_r[0], middleFkCtrl=self.middle_fk_r[0], endFkCtrl=self.end_fk_r[0], ikHandle=self.hand_ik_handle_r[0], clvIkCtrl=self.clavicle_ik_r[0], clvFkCtrl=self.clavicle_fk_r[0])
        cmds.select(sel)
        return value

    def ikfkMatch_legs_l(self, val):
        sel = cmds.ls(os=1)
        for child in self.UI.widget.findChildren(QPushButton):
            if child.objectName() == 'ball_l_001_ik':
                self.ball_ik_l = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'ball_l_001_fk':
                self.ball_fk_l = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'knee_l_001_ik':
                self.knee_ik_l = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'foot_l_001_ik':
                self.foot_ik_l = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'foot_l_001_ik_rot':
                self.foot_ik_l_rot = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'thigh_l_001_fk':
                self.start_fk_l = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'calf_l_001_fk':
                self.middle_fk_l = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'foot_l_001_fk':
                self.end_fk_l = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'legs_l_fkToikJoints':
                self.foot_ik_handle_l = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'pelvis_c_001':
                self.pelvis = self._filter.selectButtonRelease(self.UI.widget, [child], True)
        if val == 'IK':
            namespace = self.UI.nameSpaceList.currentText()
            ik_to_fk = IKtoFK(namespace)
            value = ik_to_fk.current_match(l_legs=True, r_legs=False, l_arms=False, r_arms=False)
            # value = ikToFkMatch(startJnt=self.start_fk_l[0], middleJnt=self.middle_fk_l[0], endJnt=self.end_fk_l[0], ikCtrl=self.foot_ik_l[0], ikPvCtrl=self.knee_ik_l[0], ikRotCtrl=self.foot_ik_l_rot[0], clvFkCtrl=None, clvIkCtrl=None, foot=1, ballFkCtrl=self.ball_fk_l[0], ballIkCtrl=self.ball_ik_l[0], pelvis=self.pelvis[0], move=self.UI.matchPv_legs_l.value())
        elif val == 'FK':
            value = fkToIkMatch(startFkCtrl=self.start_fk_l[0], middleFkCtrl=self.middle_fk_l[0], endFkCtrl=self.end_fk_l[0], ikHandle=self.foot_ik_handle_l[0], clvIkCtrl=self.ball_ik_l[0], clvFkCtrl=self.ball_fk_l[0], foot=True)
        cmds.select(sel)
        return value

    def ikfkMatch_legs_r(self, val):
        sel = cmds.ls(os=1)
        for child in self.UI.widget.findChildren(QPushButton):
            if child.objectName() == 'ball_r_001_ik':
                self.ball_ik_r = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'ball_r_001_fk':
                self.ball_fk_r = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'knee_r_001_ik':
                self.knee_ik_r = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'foot_r_001_ik':
                self.foot_ik_r = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'foot_r_001_ik_rot':
                self.foot_ik_r_rot = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'thigh_r_001_fk':
                self.start_fk_r = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'calf_r_001_fk':
                self.middle_fk_r = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'foot_r_001_fk':
                self.end_fk_r = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'legs_r_fkToikJoints':
                self.foot_ik_handle_r = self._filter.selectButtonRelease(self.UI.widget, [child], True)
            elif child.objectName() == 'pelvis_c_001':
                self.pelvis = self._filter.selectButtonRelease(self.UI.widget, [child], True)
        if val == 'IK':
            namespace = self.UI.nameSpaceList.currentText()
            ik_to_fk = IKtoFK(namespace)
            value = ik_to_fk.current_match(l_legs=False, r_legs=True, l_arms=False, r_arms=False)
            # value = ikToFkMatch(startJnt=self.start_fk_r[0], middleJnt=self.middle_fk_r[0], endJnt=self.end_fk_r[0], ikCtrl=self.foot_ik_r[0], ikPvCtrl=self.knee_ik_r[0], ikRotCtrl=self.foot_ik_r_rot[0], clvFkCtrl=None, clvIkCtrl=None, foot=1, ballFkCtrl=self.ball_fk_r[0], ballIkCtrl=self.ball_ik_r[0], pelvis=self.pelvis[0], move=self.UI.matchPv_legs_r.value())
        elif val == 'FK':
            value = fkToIkMatch(startFkCtrl=self.start_fk_r[0], middleFkCtrl=self.middle_fk_r[0], endFkCtrl=self.end_fk_r[0], ikHandle=self.foot_ik_handle_r[0], clvIkCtrl=self.ball_ik_r[0], clvFkCtrl=self.ball_fk_r[0], foot=True)
        cmds.select(sel)
        return value

    def ikfk_match_bake(self, *args, **kwargs):
        # time
        clock = timeit.default_timer
        start = clock()

        if self.UI.setTimeSlider.isChecked():
            self.setTimeSlider()
        startTime = self.UI.setStartTime.value()
        endTime = self.UI.setEndTime.value()

        self.times = []
        self.value_buf = {}

        # autokeyframe
        autokeyframe = None
        if cmds.autoKeyframe(q=1, state=1):
            autokeyframe = True
            cmds.autoKeyframe(e=1, state=0)

        """
        # Check the current evaluation mode used.
        current_eval_mode = cmds.evaluationManager(query=True, mode=True)[0]
        if not current_eval_mode == "off":
            # Set it to off.
            cmds.evaluationManager(mode="off")
        # Halts Maya's handling of refresh events.

        # Isolate to get the bake faster.
        panelFocus = cmds.getPanel(withFocus=True)
        visPanels = cmds.getPanel(visiblePanels=True)
        modelPanels = cmds.getPanel(type="modelPanel")
        if modelPanels:
            for pan in modelPanels:
                finder = pan in visPanels
                if finder:
                    activePanel = pan
            cmds.setFocus(activePanel)
            cmds.scriptedPanel(
                "referenceEditorPanel1",
                edit=True,
                replacePanel=activePanel
            )
        """
        cmds.refresh(su=1)
        if self.UI.matchBake_arms_FKtoIK.isChecked() or self.UI.matchBake_legs_FKtoIK.isChecked():
            x = int(startTime)
            for i in range(int(endTime)+1):
                f = i + x
                if f == int(endTime)+1:
                    break
                else:
                    OpenMayaAnim.MAnimControl.setCurrentTime(OpenMaya.MTime(f, OpenMaya.MTime.uiUnit()))
                self.times.append(f)
                if self.UI.matchBake_arms.isChecked():
                    if self.UI.matchBake_arms_L.isChecked():
                        if self.UI.matchBake_arms_IKtoFK.isChecked():
                            continue
                            # self.ikfk_match_object(['arms', 'L', 'IK'])
                        elif self.UI.matchBake_arms_FKtoIK.isChecked():
                            self.ikfk_match_object(['arms', 'L', 'FK'])
                    if self.UI.matchBake_arms_R.isChecked():
                        if self.UI.matchBake_arms_IKtoFK.isChecked():
                            continue
                            # self.ikfk_match_object(['arms', 'R', 'IK'])
                        elif self.UI.matchBake_arms_FKtoIK.isChecked():
                            self.ikfk_match_object(['arms', 'R', 'FK'])
                if self.UI.matchBake_legs.isChecked():
                    if self.UI.matchBake_legs_L.isChecked():
                        if self.UI.matchBake_legs_IKtoFK.isChecked():
                            continue
                            # self.ikfk_match_object(['legs', 'L', 'IK'])
                        elif self.UI.matchBake_legs_FKtoIK.isChecked():
                            self.ikfk_match_object(['legs', 'L', 'FK'])
                    if self.UI.matchBake_legs_R.isChecked():
                        if self.UI.matchBake_legs_IKtoFK.isChecked():
                            continue
                            # self.ikfk_match_object(['legs', 'R', 'IK'])
                        elif self.UI.matchBake_legs_FKtoIK.isChecked():
                            self.ikfk_match_object(['legs', 'R', 'FK'])

            UndoCallback(self.matchBake())

            """
            # Back to the prespective
            cmds.modelPanel(
                activePanel,
                edit=True,
                replacePanel="referenceEditorPanel1"
            )
            cmds.setFocus(panelFocus)
            """
            # EulerFilter
            cmds.filterCurve(self.value_buf.keys(), filter="euler")

            cmds.refresh(su=0)
            """
            # Set back the initial evaluation mode that it was set to.
            cmds.evaluationManager(mode=current_eval_mode)
            """

            if autokeyframe:
                cmds.autoKeyframe(e=1, state=1)
            OpenMayaAnim.MAnimControl.setCurrentTime(OpenMaya.MTime(startTime, OpenMaya.MTime.uiUnit()))

            elapsed = clock() - start
            print( time.strftime("%Hh:%Mm:{:.3f}s".format(elapsed), time.gmtime(elapsed)) )

        else:
            namespace = self.UI.nameSpaceList.currentText()
            ik_to_fk = IKtoFK(namespace)

            if self.UI.matchBake_arms_L.isChecked() == True and self.UI.matchBake_arms_R.isChecked() == False and self.UI.matchBake_legs_L.isChecked() == False and self.UI.matchBake_legs_R.isChecked() == False:
                ik_to_fk.bakeanim(select_timeslider=True, simplebake=False, l_legs=False, r_legs=False, l_arms=True, r_arms=False)
            elif self.UI.matchBake_arms_L.isChecked() == False and self.UI.matchBake_arms_R.isChecked() == True and self.UI.matchBake_legs_L.isChecked() == False and self.UI.matchBake_legs_R.isChecked() == False:
                ik_to_fk.bakeanim(select_timeslider=True, simplebake=False, l_legs=False, r_legs=False, l_arms=True, r_arms=False)
            elif self.UI.matchBake_arms_L.isChecked() == True and self.UI.matchBake_arms_R.isChecked() == True and self.UI.matchBake_legs_L.isChecked() == False and self.UI.matchBake_legs_R.isChecked() == False:
                ik_to_fk.bakeanim(select_timeslider=True, simplebake=False, l_legs=False, r_legs=False, l_arms=True, r_arms=True)

            elif self.UI.matchBake_arms_L.isChecked() == True and self.UI.matchBake_arms_R.isChecked() == True and self.UI.matchBake_legs_L.isChecked() == True and self.UI.matchBake_legs_R.isChecked() == False:
                ik_to_fk.bakeanim(select_timeslider=True, simplebake=False, l_legs=True, r_legs=False, l_arms=True, r_arms=True)
            elif self.UI.matchBake_arms_L.isChecked() == True and self.UI.matchBake_arms_R.isChecked() == True and self.UI.matchBake_legs_L.isChecked() == False and self.UI.matchBake_legs_R.isChecked() == True:
                ik_to_fk.bakeanim(select_timeslider=True, simplebake=False, l_legs=False, r_legs=True, l_arms=True, r_arms=True)

            elif self.UI.matchBake_legs_L.isChecked() == True and self.UI.matchBake_legs_R.isChecked() == False and self.UI.matchBake_arms_L.isChecked() == False and self.UI.matchBake_arms_R.isChecked() == False:
                ik_to_fk.bakeanim(select_timeslider=True, simplebake=False, l_legs=True, r_legs=False, l_arms=False, r_arms=False)
            elif self.UI.matchBake_legs_L.isChecked() == False and self.UI.matchBake_legs_R.isChecked() == True and self.UI.matchBake_arms_L.isChecked() == False and self.UI.matchBake_arms_R.isChecked() == False:
                ik_to_fk.bakeanim(select_timeslider=True, simplebake=False, l_legs=False, r_legs=True, l_arms=False, r_arms=False)
            elif self.UI.matchBake_legs_L.isChecked() == True and self.UI.matchBake_legs_R.isChecked() == True and self.UI.matchBake_arms_L.isChecked() == False and self.UI.matchBake_arms_R.isChecked() == False:
                ik_to_fk.bakeanim(select_timeslider=True, simplebake=False, l_legs=True, r_legs=True, l_arms=False, r_arms=False)

            elif self.UI.matchBake_legs_L.isChecked() == True and self.UI.matchBake_legs_R.isChecked() == True and self.UI.matchBake_arms_L.isChecked() == True and self.UI.matchBake_arms_R.isChecked() == False:
                ik_to_fk.bakeanim(select_timeslider=True, simplebake=False, l_legs=True, r_legs=True, l_arms=True, r_arms=False)
            elif self.UI.matchBake_legs_L.isChecked() == True and self.UI.matchBake_legs_R.isChecked() == True and self.UI.matchBake_arms_L.isChecked() == False and self.UI.matchBake_arms_R.isChecked() == True:
                ik_to_fk.bakeanim(select_timeslider=True, simplebake=False, l_legs=True, r_legs=True, l_arms=False, r_arms=True)

    def addkeys(self, plugName, times, values, changeCache):
        # Get the plug to be animated.
        sel = OpenMaya.MSelectionList()
        sel.add(plugName)
        plug = OpenMaya.MPlug()
        sel.getPlug(0, plug)
        # Copy the times into an MTimeArray and the values into an    MDoubleArray.
        timeArray = OpenMaya.MTimeArray()
        valueArray = OpenMaya.MDoubleArray()
        for i in range(len(times)):
          timeArray.append(OpenMaya.MTime(times[i], OpenMaya.MTime.uiUnit()))
          valueArray.append(values[i])

        if 'translate' in  plugName.split('.')[1]:
            curveType_node = ['animCurveTL', '{}_{}'.format(plugName.split('.')[0], plugName.split('.')[1])]
            # animCurve = cmds.createNode('animCurveTL', n='{}_{}'.format(plugName.split('.')[0], plugName.split('.')[1]))
        elif 'rotate' in  plugName.split('.')[1]:
            curveType_node = ['animCurveTA', '{}_{}'.format(plugName.split('.')[0], plugName.split('.')[1])]
            # animCurve = cmds.createNode('animCurveTA', n='{}_{}'.format(plugName.split('.')[0], plugName.split('.')[1]))
        else:
            curveType_node = ['animCurveTU', '{}_{}'.format(plugName.split('.')[0], plugName.split('.')[1])]
            # animCurve = cmds.createNode('animCurveTU', n='{}_{}'.format(plugName.split('.')[0], plugName.split('.')[1]))
        animCurve = curveType_node[1]
        if cmds.objExists(animCurve) == False:
            cmds.createNode(curveType_node[0], n='{}'.format(animCurve))
            try:
                cmds.connectAttr('{}.output'.format(animCurve), '{}'.format(plugName), f=True)
            except Exception as e:
                pass

        curve_selection = OpenMaya.MSelectionList()
        OpenMaya.MGlobal.getSelectionListByName(animCurve, curve_selection)
        mobj = OpenMaya.MObject()
        curve_selection.getDependNode(0, mobj)
        animfn = OpenMayaAnim.MFnAnimCurve(mobj)

        # Add the keys to the animCurve.
        UndoCallback(animfn.addKeys(timeArray,valueArray,OpenMayaAnim.MFnAnimCurve.kTangentGlobal,OpenMayaAnim.MFnAnimCurve.kTangentGlobal,False,changeCache))

    def matchBake(self, *args, **kwargs):
        # cmds.setKeyframe(args, breakdown=0, hierarchy='none', shape=0, controlPoints=0)
        for key in self.value_buf.keys():
            self.changeCache = OpenMayaAnim.MAnimCurveChange()
            self.addkeys(key, self.times, self.value_buf[key], self.changeCache)

    def undo_matchBake(self, *args, **kwargs):
        self.changeCache.undoIt()

    def bufferCurves(self, value, args):
        if value == None:
            return
        for obj in args:
            pos = value[obj][0]
            rot = value[obj][1]
            try:
                self.value_buf['{}.{}'.format(obj, 'translateX')].append(pos[0])
                self.value_buf['{}.{}'.format(obj, 'translateY')].append(pos[1])
                self.value_buf['{}.{}'.format(obj, 'translateZ')].append(pos[2])
                self.value_buf['{}.{}'.format(obj, 'rotateX')].append(rot[0])
                self.value_buf['{}.{}'.format(obj, 'rotateY')].append(rot[1])
                self.value_buf['{}.{}'.format(obj, 'rotateZ')].append(rot[2])
            except:
                self.value_buf['{}.{}'.format(obj, 'translateX')] = [pos[0]]
                self.value_buf['{}.{}'.format(obj, 'translateY')] = [pos[1]]
                self.value_buf['{}.{}'.format(obj, 'translateZ')] = [pos[2]]
                self.value_buf['{}.{}'.format(obj, 'rotateX')] = [rot[0]]
                self.value_buf['{}.{}'.format(obj, 'rotateY')] = [rot[1]]
                self.value_buf['{}.{}'.format(obj, 'rotateZ')] = [rot[2]]

    def ikfk_match_object(self, matchBuf):
        # regions
        if matchBuf[0] == 'arms':
            region = 'arms'
        else:
            region = 'legs'
        # sides
        if matchBuf[1] == 'L':
            side = 'L'
        else:
            side = 'R'
        # ik or fk
        if matchBuf[2] == 'IK':
            val = 'IK'
        else:
            val = 'FK'

        if region == 'arms' and side == 'L':
            value = self.ikfkMatch_arms_l(val)
            if val == 'IK':
                args = [self.hand_ik_l[0], self.elbow_ik_l[0], self.hand_ik_l_rot[0], self.clavicle_ik_l[0]]
            else:
                args = [self.start_fk_l[0], self.middle_fk_l[0], self.end_fk_l[0], self.clavicle_fk_l[0]]
        elif region == 'arms' and side == 'R':
            value = self.ikfkMatch_arms_r(val)
            if val == 'IK':
                args = [self.hand_ik_r[0], self.elbow_ik_r[0], self.hand_ik_r_rot[0], self.clavicle_ik_r[0]]
            else:
                args = [self.start_fk_r[0], self.middle_fk_r[0], self.end_fk_r[0], self.clavicle_fk_r[0]]
        elif region == 'legs' and side == 'L':
            value = self.ikfkMatch_legs_l(val)
            if val == 'IK':
                args = [self.foot_ik_l[0], self.knee_ik_l[0], self.ball_ik_l[0], self.foot_ik_l_rot[0]]
            else:
                args = [self.start_fk_l[0], self.middle_fk_l[0], self.end_fk_l[0], self.ball_fk_l[0]]
        elif region == 'legs' and side == 'R':
            value = self.ikfkMatch_legs_r(val)
            if val == 'IK':
                args = [self.foot_ik_r[0], self.knee_ik_r[0], self.ball_ik_r[0], self.foot_ik_r_rot[0]]
            else:
                args = [self.start_fk_r[0], self.middle_fk_r[0], self.end_fk_r[0], self.ball_fk_r[0]]

        self.bufferCurves(value, args)

    def setTimeSlider(self, *args, **kwargs):
        if self.UI.setTimeSlider.isChecked():
            playmin = cmds.playbackOptions(q=1, min=1)
            playmax = cmds.playbackOptions(q=1, max=1)

            self.UI.setStartTime.setValue(playmin)
            self.UI.setEndTime.setValue(playmax)

    def setMatchBake_arms(self, *args, **kwargs):
        # self.UI.matchBake_arms.stateChanged.connect(self.setMatchBake_arms)
        # self.UI.matchBake_legs.stateChanged.connect(self.setMatchBake_legs)
        if self.UI.matchBake_arms.isChecked():
            self.UI.matchBake_arms_L.setChecked(True)
            self.UI.matchBake_arms_R.setChecked(True)
        else:
            self.UI.matchBake_arms_L.setChecked(False)
            self.UI.matchBake_arms_R.setChecked(False)

    def setMatchBake_legs(self, *args, **kwargs):
        # self.UI.matchBake_arms.stateChanged.connect(self.setMatchBake_arms)
        # self.UI.matchBake_legs.stateChanged.connect(self.setMatchBake_legs)
        if self.UI.matchBake_legs.isChecked():
            self.UI.matchBake_legs_L.setChecked(True)
            self.UI.matchBake_legs_R.setChecked(True)
        else:
            self.UI.matchBake_legs_L.setChecked(False)
            self.UI.matchBake_legs_R.setChecked(False)

    def setCurrentStartTime(self, *args, **kwargs):
        self.UI.setStartTime.setValue(cmds.currentTime(q=1))

    def setCurrentEndTime(self, *args, **kwargs):
        self.UI.setEndTime.setValue(cmds.currentTime(q=1))

    def arms_l_ikfk_switch(self, *args, **kwargs):
        Sender = self.sender()
        try:
            val = Sender.text()
        except Exception as e:
            val = 'FK'
        self.ikfkSwitch_vis(Sender, val, self.arms_l_region_fk, self.arms_l_region_ik)

    def arms_r_ikfk_switch(self, *args, **kwargs):
        Sender = self.sender()
        try:
            val = Sender.text()
        except Exception as e:
            val = 'FK'
        self.ikfkSwitch_vis(Sender, val, self.arms_r_region_fk, self.arms_r_region_ik)

    def legs_l_ikfk_switch(self, *args, **kwargs):
        Sender = self.sender()
        try:
            val = Sender.text()
        except Exception as e:
            val = 'FK'
        self.ikfkSwitch_vis(Sender, val, self.legs_l_region_fk, self.legs_l_region_ik)

    def legs_r_ikfk_switch(self, *args, **kwargs):
        Sender = self.sender()
        try:
            val = Sender.text()
        except Exception as e:
            val = 'FK'
        self.ikfkSwitch_vis(Sender, val, self.legs_r_region_fk, self.legs_r_region_ik)

    def ikfk_switch(self, switch, value):
        spl = switch.split('|')
        if self.UI.nameSpaceList.currentText() == '':
            selectObjects = switch
        else:
            selectObjects = '|'.join(['{}:{}'.format(self.UI.nameSpaceList.currentText(), spl[i]) for i in range(len(spl))])

        cmds.setAttr(selectObjects, float(value))

    # x_settings
    def ik_segmentScaleCompensate_set(self, *args, **kwargs):
        result = cmds.confirmDialog(
            title='IK Set segmentScaleCompensate',
            message=u'IKジョイントのsegmentScaleCompensateを切り替えます。(FKをIKに変換する際に使用します。)\nONかOFFかを選択してください。何もしない場合はCancelを押してください。',
            button=['ON', 'OFF', 'Cancel'],
            defaultButton='ON',
            cancelButton='Cancel',
            dismissString='Cancel')

        if result != 'Cancel':
            nss = '{0}:'.format(self.UI.nameSpaceList.currentText())
            if nss == ':':
                cmds.warning(u'ネームスペースが設定されていません。')
                return
            sides = ['_L_', '_R_']
            body_parts = ['shoulder', 'upperarm', 'lowerarm', 'hand']

            # ikjoints
            for side in sides:
                for bp in body_parts:
                    scale_pairBlend = '{0}module_proxy{1}{2}_ikfk_scale_pbn'.format(nss, side, bp)
                    scale_ik_jnt = '{0}proxy{1}{2}_ik_jnt'.format(nss, side, bp)
                    scale_fk_ctrl = '{0}proxy{1}{2}_fk_ctrl'.format(nss, side, bp)

                    scale_ik_jnt_dmx = '{0}_constDmx'.format(scale_ik_jnt)
                    scale_fk_ctrl_dmx = '{0}_constDmx'.format(scale_fk_ctrl)

                    if result == 'ON':
                        cmds.connectAttr('{0}.outputScale'.format(scale_ik_jnt_dmx), '{0}.inTranslate1'.format(scale_pairBlend), f=1)
                        cmds.connectAttr('{0}.outputScale'.format(scale_fk_ctrl_dmx), '{0}.inTranslate2'.format(scale_pairBlend), f=1)

                        cmds.setAttr('{0}.segmentScaleCompensate'.format(scale_ik_jnt), 1)
                    elif result == 'OFF':
                        cmds.connectAttr('{0}.scale'.format(scale_ik_jnt), '{0}.inTranslate1'.format(scale_pairBlend), f=1)
                        cmds.connectAttr('{0}.scale'.format(scale_fk_ctrl), '{0}.inTranslate2'.format(scale_pairBlend), f=1)

                        cmds.setAttr('{0}.segmentScaleCompensate'.format(scale_ik_jnt), 0)

    def create_picker_sets_button(self, dialog=None, text=None, sel=None):
        if dialog == True:
            sel = cmds.ls(os=1)
            result = cmds.promptDialog(title=u'Add Picker Sets',
                                	   message=u'登録するSetの名前を入力してください',
                                	  button=['OK', 'Cancel'],
                                      defaultButton='OK',
                                      cancelButton='Cancel',
                                      dismissString='Cancel')
            if result == 'OK':
            	text = cmds.promptDialog(query=True, text=True)
            else:
                return
        spl = [ss.split(':')[-1] for ss in sel]
        treeColItem = QStandardItem(u'{}'.format(text))
        for i in range(len(spl)):
            child = QStandardItem('{}'.format(spl[i]))
            treeColItem.appendRow([child])
        self.pickerSetsModel.appendRow(treeColItem)

    def on_click(self, *args, **kwargs):
        index = self.UI.pickerSetsButtons.selectedIndexes()[0]
        item = self.pickerSetsModel.itemFromIndex(index)
        objects= [item.child(i, 0).text() for i in range(item.rowCount())]

        namespace = self.UI.nameSpaceList.currentText()

        if namespace == '':
            selectObjects = ['{}'.format(obj) for obj in objects]
        else:
            selectObjects = ['{}:{}'.format(namespace, obj) for obj in objects]

        modifiers = QApplication.keyboardModifiers()
        try:
            if  modifiers == Qt.ShiftModifier:
                cmds.select(selectObjects, tgl=1)
            elif modifiers == Qt.ControlModifier:
                cmds.select(selectObjects, add=1)
            else:
                cmds.select(selectObjects)
        except Exception as e:
            print(e)
        cmds.setFocus("MayaWindow")

    def get_all_pickerSets(self, *args, **kwargs):
        pickerSetsDict = OrderedDict()
        rows = self.pickerSetsModel.rowCount()
        for j in range(rows):
            index = self.pickerSetsModel.index(j, 0)
            item = self.pickerSetsModel.itemFromIndex(index)
            objects= [item.child(i, 0).text() for i in range(item.rowCount())]
            pickerSetsDict[item.text()] = objects
        # print(pickerSetsDict)
        return pickerSetsDict

    def define_mocap_table(self, *args, **kwargs):
        sel = cmds.ls(os=1)
        # sel.sort()
        spl = [ss.split(':')[-1] for ss in sel]
        for i in range(len(sel)/2):
            # print(self.UI.mocapDefineOnly.isChecked()==True)
            src_trans, src_rot, trans, rot =cmds.xform(sel[i*2], q=1, t=1), cmds.xform(sel[i*2], q=1, ro=1), cmds.xform(sel[i*2+1], q=1, t=1), cmds.xform(sel[i*2+1], q=1, ro=1)
            value_list = [src_trans, src_rot, trans, rot]
            if self.UI.mocapDefinePoleVector.isChecked():
                value_list.append('PoleVectorCtrl')
            self.tPoseData['{}->{}'.format(sel[i*2], spl[i*2+1])] = value_list


        i = 0
        for key in self.tPoseData.keys():
            for j in range(len(self.tPoseData[key])):
                item = QStandardItem(str(self.tPoseData[key][j]))
                self.mocapSetModel.setItem(i,j,item)
                self.mocapSetModel.setHeaderData(i, Qt.Vertical, item)
                self.mocapSetModel.setHeaderData(j, Qt.Horizontal, j)
            i += 1
        self.mocapSetModel.setVerticalHeaderLabels(self.tPoseData.keys())

    def getSetRotation_offset(self, src=None, dst=None, eulerQuat=True, offset=[0.0, 0.0, 0.0]):
        obj = src

        selection = OpenMaya2.MSelectionList()
        selection.add(obj)
        dag = selection.getDagPath(0)

        transform_fn = OpenMaya2.MFnTransform(dag)
        quat = transform_fn.rotation(OpenMaya2.MSpace.kWorld, True)
        euler = transform_fn.rotation(OpenMaya2.MSpace.kTransform, False)

        m_quat = OpenMaya2.MQuaternion(quat)

        obj2 = dst
        selection2 = OpenMaya2.MSelectionList()
        selection2.add(obj2)
        dag2 = selection2.getDagPath(0)

        transform_fn2 = OpenMaya2.MFnTransform(dag2)
        trans = transform_fn2.translation(OpenMaya2.MSpace.kWorld)

        if eulerQuat:
            # transform_fn2.setRotation(m_quat, OpenMaya2.MSpace.kWorld)
            cmds.xform(dst, ro=[math.degrees(m_quat.x)+offset[0], math.degrees(m_quat.y)+offset[1], math.degrees(m_quat.z)+offset[2]], ws=1, a=1)

        else:
            m_euler = OpenMaya2.MEulerRotation(euler.x, euler.y, euler.z, euler.order)
            # m_euler.reorder(euler.order)
            cmds.xform(dst, ro=[math.degrees(m_euler.x)+offset[0], math.degrees(m_euler.y)+offset[1], math.degrees(m_euler.z)+offset[2]], a=1)

        # transform_fn.setTranslation(trans, OpenMaya2.MSpace.kWorld)
        cmds.xform(src, t=[trans.x, trans.y, trans.z], ws=1, a=1)

    def getSetRotation_offset_call(self, *args, **kwargs):
        sel = cmds.ls(os=1)
        mocapOffset_x = self.UI.mocapOffset_x.value()
        mocapOffset_y = self.UI.mocapOffset_y.value()
        mocapOffset_z = self.UI.mocapOffset_z.value()

        for i in range(len(sel)/2):
            # print(self.UI.mocapDefineOnly.isChecked())
            if self.UI.mocapDefineOnly.isChecked() == False:
                UndoCallback(self.getSetRotation_offset(src=sel[i*2], dst=sel[i*2+1], eulerQuat=True, offset=[mocapOffset_x, mocapOffset_y, mocapOffset_z]))
                self.define_mocap_table()
            elif self.UI.mocapDefineOnly.isChecked() == True:
                self.define_mocap_table()

    def tweakRotate(self, *args, **kwargs):
        sel = cmds.ls(os=1)
        mocapOffset_x = self.UI.mocapOffset_x.value()
        mocapOffset_y = self.UI.mocapOffset_y.value()
        mocapOffset_z = self.UI.mocapOffset_z.value()

        for i in range(len(sel)/2):
            lt = cmds.xform(sel[i*2+1], q=1, ro=1, os=1)
            flags = rot_skippy(sel[i*2+1])
            """
            axis = ['X', 'Y', 'Z']
            enableAttrs = flags.values()[0]
            for ax in enableAttrs:
                if ax == 'x':
                    axis.remove('X')
                if ax == 'y':
                    axis.remove('Y')
                if ax == 'z':
                    axis.remove('Z')
            """

            cmds.delete(cmds.orientConstraint(sel[i*2], sel[i*2+1], w=1, offset=[mocapOffset_x, mocapOffset_y, mocapOffset_z], **flags))
            # cmds.xform(sel[i*2+1], ro=[lt[0]+mocapOffset_x, lt[1]+mocapOffset_y, lt[2]+mocapOffset_z], os=1)

    def setTpose(self, *args, **kwargs):
        model = self.UI.defineTable_mocap.model()
        # col = model.columnCount()
        row = model.rowCount()

        objects = OrderedDict()
        headerObjects = [model.headerData(r, Qt.Vertical) for r in range(row)]
        # for c in range(col):
        for o in range(len(headerObjects)):
            try:
                src_trans = strToNum_list(src=model.item(o, 0).text())
                src_rot = strToNum_list(src=model.item(o, 1).text())
                trans = strToNum_list(src=model.item(o, 2).text())
                rot = strToNum_list(src=model.item(o, 3).text())
                value_list = [src_trans, src_rot, trans, rot]
                objects[headerObjects[o]] = value_list
            except Exception as e:
                pass

        namespace = self.UI.nameSpaceList.currentText()

        for obj in objects.keys():
            splObj = obj.split('->')[1]
            splJnt = obj.split('->')[0]
            if cmds.objExists(splJnt) == False:
                continue
            if namespace == '':
                selectObject = '{}'.format(splObj)
            else:
                selectObject = '{}:{}'.format(namespace, splObj)
            if cmds.objExists(selectObject) == False:
                continue
            cmds.xform(splJnt, t=objects[obj][0], a=1)
            cmds.xform(splJnt, ro=objects[obj][1], a=1)
            cmds.xform(selectObject, t=objects[obj][2], a=1)
            cmds.xform(selectObject, ro=objects[obj][3], a=1)

    def connectMocapJnts(self, *args, **kwargs):
        mcs = 'mocapConnectionsSets'
        if cmds.objExists(mcs) == False:
            cmds.createNode('objectSet', n='mocapConnectionsSets')
        model = self.UI.defineTable_mocap.model()
        # col = model.columnCount()
        row = model.rowCount()

        objects = OrderedDict()
        headerObjects = [model.headerData(r, Qt.Vertical) for r in range(row)]
        # for c in range(col):
        for o in range(len(headerObjects)):
            try:
                src_trans = strToNum_list(src=model.item(o, 0).text())
                src_rot = strToNum_list(src=model.item(o, 1).text())
                trans = strToNum_list(src=model.item(o, 2).text())
                rot = strToNum_list(src=model.item(o, 3).text())
                value_list = [src_trans, src_rot, trans, rot]
                try:
                    pv = model.item(o, 4).text()
                    value_list.append(pv)
                except Exception as e:
                    pass
                objects[headerObjects[o]] = value_list
            except Exception as e:
                pass

        namespace = self.UI.nameSpaceList.currentText()

        # print(objects)
        connectObjects = []
        for obj in objects.keys():
            splObj = obj.split('->')[1]
            splJnt = obj.split('->')[0]
            if cmds.objExists(splJnt) == False:
                continue
            if namespace == '':
                selectObject = '{}'.format(splObj)
            else:
                selectObject = '{}:{}'.format(namespace, splObj)
            if cmds.objExists(selectObject) == False:
                continue
            attr = cmds.listAttr(selectObject, k=1)
            if 'PoleVectorCtrl' in objects[obj]:
                # print(selectObject)
                dup = cmds.duplicate(selectObject, po=1)[0]
                connectObjects.append(dup)
                cmds.setAttr('{}.rx'.format(dup), k=1)
                cmds.setAttr('{}.ry'.format(dup), k=1)
                cmds.setAttr('{}.rz'.format(dup), k=1)
                pac = cmds.parentConstraint(splJnt, dup, w=1, mo=1)
                poc = cmds.pointConstraint(dup, selectObject, w=1, mo=1)
                connectObjects.append(pac[0])
                connectObjects.append(poc[0])
            else:
                try:
                    if 'translateX' in attr or 'translateY' in attr or 'translateZ' in attr:
                        # print(selectObject)
                        flags = trans_skippy(selectObject)
                        poc = cmds.pointConstraint(splJnt, selectObject, w=1, mo=1, **flags)
                        connectObjects.append(poc[0])
                except Exception as e:
                    pass
            try:
                if 'rotateX' in attr or 'rotateY' in attr or 'rotateZ' in attr:
                    flags = rot_skippy(selectObject)
                    ori = cmds.orientConstraint(splJnt, selectObject, w=1, mo=1, **flags)
                    connectObjects.append(ori[0])
                    pbn = cmds.createNode('pairBlend', n='{}_pbn'.format(selectObject), ss=1)
                    if self.UI.Quaternion.isChecked():
                        cmds.setAttr('{}.rotInterpolation'.format(pbn), 1)
                    # print(flags.values()[0])
                    enableAttrs = flags.values()[0]
                    axis = ['X', 'Y', 'Z']
                    for ax in enableAttrs:
                        if ax == 'x':
                            axis.remove('X')
                        if ax == 'y':
                            axis.remove('Y')
                        if ax == 'z':
                            axis.remove('Z')
                    for at in axis:
                        cmds.connectAttr('{}.constraintRotate{}'.format(ori[0], at), '{}.inRotate{}2'.format(pbn, at), f=1)
                        cmds.connectAttr('{}.outRotate{}'.format(pbn, at), '{}.rotate{}'.format(selectObject, at), f=1)
            except Exception as e:
                pass
        mcss = cmds.listConnections('{}.dagSetMembers'.format(mcs), s=1, d=0)
        if mcss == None:
            i = 0
        else:
            i = len(mcss) + 1
        for obj in connectObjects:
            cmds.connectAttr('{}.instObjGroups[0]'.format(obj), '{}.dagSetMembers[{}]'.format(mcs, i), f=1)
            i += 1
            # print(objects[obj])

    def updateSpaceAttr(self, *args, **kwargs):
        spaceAttr = self.UI.spaceAttribute_le.text()
        self.UI.changeSpace_le.clear()
        allNodes = cmds.ls()
        ctrlChangeList = []
        spaces = []
        spcQry = []
        if spaceAttr == '':
            return
        for obj in allNodes:
            try:
                spcQry = cmds.attributeQuery(spaceAttr, node='{}'.format(obj), le=1)[0]
            except:
                continue
            if spcQry != []:
                spaceList = spcQry.split(':')
                for enums in spaceList:
                    spaces.append(enums)

        allSpaces = list(set(spaces))
        allSpaces.sort()
        print('Space List:{}'.format(allSpaces))
        for sp in allSpaces:
            self.UI.changeSpace_le.addItem(sp)

    def spaceMatchBake(self, *args, **kwargs):
        sel = cmds.ls(os=1)
        spaceAttr = self.UI.spaceAttribute_le.text()
        changeSpace = self.UI.changeSpace_le.currentText()
        ctrlChangeList = {}
        spaces = []
        ctrlLocs = {}
        constLocs = {}

        aPlayBackSliderPython = mel.eval('$tmpVar=$gPlayBackSlider')
        rangeArray = cmds.timeControl( aPlayBackSliderPython, q=True, rangeArray=True)

        playmin = rangeArray[0]
        playmax = rangeArray[1]

        if sel == []:
            print('Please select objects')
            return
        for obj in sel:
            attr = cmds.listAttr(obj)
            if spaceAttr in attr:
                spaces.append(obj)
                loc = cmds.spaceLocator()[0]
                po = cmds.pointConstraint(obj, loc, w=1)[0]
                ro = cmds.orientConstraint(obj, loc, w=1)[0]
                ctrlLocs[obj] = loc
                constLocs[loc] = [po, ro]

                spcQry = cmds.attributeQuery(spaceAttr, node='{}'.format(obj), le=1)[0]
                spaceList = spcQry.split(':')
                if changeSpace in spaceList:
                    ctrlChangeList[obj] = spaceList

        try:
            autokeySts = cmds.autoKeyframe(q=1, st=1)
            if autokeySts:
                cmds.autoKeyframe(st=0)
            cmds.refresh(su=1)
            cmds.bakeResults(ctrlLocs.values(), sm=1, t=(playmin, playmax), sb=1, osr=1, dic=1, pok=1, sac=0, ral=0, rba=0, bol=0, mr=1, cp=0, s=0)
            cmds.refresh(su=0)
            cmds.autoKeyframe(st=autokeySts)
        except Exception as e:
            print(e)

        for const in constLocs.values():
            cmds.delete(const[0])
            cmds.delete(const[1])

        cmds.filterCurve(ctrlLocs.values(), f='euler')

        for key in ctrlLocs.keys():
            flags_po = trans_skippy(key)
            cmds.pointConstraint(ctrlLocs[key], key, w=1, **flags_po)
            flags_ro = rot_skippy(key)
            cmds.orientConstraint(ctrlLocs[key], key, w=1, **flags_ro)

        cmds.refresh(su=1)
        for i in range(int(playmin), int(playmax)+1):
            cmds.currentTime(i)
            for key in ctrlChangeList.keys():
                index = ctrlChangeList[key].index(changeSpace)
                cmds.setAttr('{}.{}'.format(key, spaceAttr), index)
                cmds.setKeyframe('{}.{}'.format(key, spaceAttr))
        cmds.refresh(su=0)

        cmds.refresh(su=1)
        cmds.bakeResults(ctrlLocs.keys(), sm=1, t=(playmin, playmax), sb=1, osr=1, dic=1, pok=1, sac=0, ral=0, rba=0, bol=0, mr=1, cp=0, s=0)
        cmds.refresh(su=0)

        cmds.filterCurve(ctrlLocs.keys(), f='euler')

        cmds.delete(ctrlLocs.values())

        cmds.currentTime(int(playmin))


class Filter(QObject):
    def eventFilter(self, widget, event):
        if event.type() == QEvent.MouseButtonPress:
            self.origin = event.pos()
            self.rubberBand = QRubberBand(QRubberBand.Rectangle,widget)
            self.origin.setX(self.origin.x())
            self.origin.setY(self.origin.y())
            self.rubberBand.setGeometry(QRect(self.origin,QSize()))
            self.rubberBand.show()
            self.selectEmpty(widget)
            # print('Push')
            # print self.origin.x()
            # print self.origin.y()

        elif event.type() == QEvent.MouseMove:
            if self.rubberBand.isVisible():
                self.movePos = event.pos()
                self.movePos.setX(self.movePos.x()+ widget.x())
                self.movePos.setY(self.movePos.y()+ widget.y())
                self.rubberBand.setGeometry(QRect(self.origin,self.movePos).normalized())
                # print "Move"
                # print event.x()
                # print event.y()
                # print(widget.width())
                # print(widget.height())

        elif event.type() == QEvent.MouseButtonRelease:
            # print "Release"
            # print event.x()
            # print event.y()
            # print('Release')
            sel = cmds.ls(os=1)
            self.rubberBand.hide()
            rect = self.rubberBand.geometry()
            rect.setX(rect.x()-widget.x())
            rect.setY(rect.y()-widget.y())
            rect.setWidth(rect.width()-widget.x())
            rect.setHeight(rect.height()-widget.y())
            self.releaseBuf = []
            selected = []
            #ウィンドウ内のQPushButtonをすべて取得
            for child in widget.findChildren(QPushButton):
                if rect.intersects(child.geometry()):
                    selected.append(child)
            if selected:
                # self.rectSelection(selected)
                self.selectButtonRelease(widget, selected, False)
            else:
                # cmds.select(cl=True)
                for child in widget.findChildren(QPushButton):
                    if child.objectName() == 'arms_l_fkToikJoints' or child.objectName() == 'arms_r_fkToikJoints' or child.objectName() == 'legs_l_fkToikJoints' or child.objectName() == 'legs_r_fkToikJoints':
                        pass
                    else:
                        if sel:
                            pass
                        else:
                            initBtnStyle_color(obj=child)
                            checkBtnIsEnabled(obj=child)
        return False

        return QMainWindow.eventFilter(self, widget, event)

    def selectEmpty(self, widget):
        # not button
        modifiers = QApplication.keyboardModifiers()
        self.pointAtType = type(widget.childAt(self.origin.x(), self.origin.y()))
        # if QLabel == self.pointAtType:
        for child in widget.findChildren(QCheckBox):
            if 'autoDeselect' == child.objectName():
                state_autoDeselect = child.checkState()
                if state_autoDeselect:
                    if QPushButton == self.pointAtType:
                        pass
                    else:
                        cmds.select(cl=1)
                        return
        if modifiers == Qt.ControlModifier or modifiers == Qt.ShiftModifier or QComboBox == self.pointAtType:
            pass
        else:
            for child in widget.findChildren(QCheckBox):
                if 'autoDeselect' == child.objectName():
                    state_autoDeselect = child.checkState()
            for child in widget.findChildren(QCheckBox):
                if 'defineMode' == child.objectName():
                    state_defineMode = child.checkState()
            if state_autoDeselect == True and state_defineMode == False:
                for child in widget.findChildren(QPushButton):
                    initBtnStyle_color(obj=child, raiseObj=False)
                cmds.select(cl=1)

    def selectButtonRelease(self, widget, selected, ignoreCheck):
        # print(selected)
        for child in widget.findChildren(QComboBox):
            if child.objectName() == 'nameSpaceList':
                namespace = child.currentText()

        for child in widget.findChildren(QTableView):
            if child.objectName() == 'defineTable':
                items_row = OrderedDict()
                items_col = OrderedDict()

                model = child.model()
                col = model.columnCount()
                row = model.rowCount()

                [items_row.setdefault(model.headerData(r, Qt.Vertical), r) for r in range(row)]
                [items_col.setdefault(model.headerData(c, Qt.Horizontal), c) for c in range(col)]

                objects = []
                for i in selected:
                    if i.isEnabled() == False and ignoreCheck == False:
                        continue
                    else:
                        pass
                    for j in range(len(items_col.keys())):
                        try:
                            # print(items, model.item(items[i.objectName()]).text())
                            item = model.item(items_row[i.objectName()], j)
                            if 'None' in item.text():
                                continue
                            objects.append(item)
                            changeBtnStyle_color(obj=i)
                            checkBtnIsEnabled(obj=i)
                        except:
                            pass

                # print(objects)
                if namespace == '':
                    self.selectObjects = ['{}'.format(obj.text()) for obj in objects]
                else:
                    self.selectObjects = ['{}:{}'.format(namespace, obj.text()) for obj in objects]

                modifiers = QApplication.keyboardModifiers()
                if modifiers == Qt.ControlModifier or modifiers == Qt.ShiftModifier:
                    cmds.select(self.selectObjects, add=1)
                    for obj in self.selectObjects:
                        self.releaseBuf.append(obj)
                else:
                    try:
                        cmds.select(self.selectObjects)
                    except Exception as e:
                        pass
        cmds.setFocus("MayaWindow")
        return self.selectObjects

class JsonFile(object):
    u"""
    reload(common)
    cjf = common.JsonFile()
    cjf.write('C:/Users/shunsuke/Documents/maya/scripts/AutoRig/dev/scripts/test2.json', metaInfo)
    cjf.read('C:/Users/shunsuke/Documents/maya/scripts/AutoRig/dev/scripts/test2.json')
    """
    @classmethod
    def read(cls, file_path):
        if not file_path:
            return {}

        if not os.path.isfile(file_path):
            return {}

        with codecs.open(file_path, 'r', 'utf-8') as f:
            try:
                data = json.load(f, object_pairs_hook=OrderedDict)
            except ValueError:
                data = {}

        return data

    @classmethod
    def write(cls, file_path, data):
        if not file_path:
            return

        dirname, basename = os.path.split(file_path) # "/"でsplitされる
        if not os.path.isdir(dirname):
            os.makedirs(dirname)

        with codecs.open(file_path, 'w', 'utf-8') as f:
            json.dump(data, f, indent=4) # indentフラグはdictionaryをspace4つごとにきれいに書き込み
            f.flush()
            os.fsync(f.fileno()) # ディスクの書き込み

def helloWorld():
    print('HelloWorld!')

def startBtnStyle_sphere(height=30, style='solid', borderWidth=2, borderColor=[70, 100, 255]):
    h = height
    height = 'height:{}spx;'.format(h)
    border = 'border-style:{0}; border-width: {1}px; border-color:rgb({2}, {3}, {4});'.format(style, borderWidth, borderColor[0], borderColor[1], borderColor[2])
    borderRadius = 'border-radius: %spx;' % (h/3)
    return '{}{}{}'.format(height, border, borderRadius)

def startBtnStyle_round(height=30, style='inset', borderWidth=2, borderColor=[100, 100, 100]):
    h = height
    height = 'height:{}spx;'.format(h)
    border = 'border-style:{0}; border-width: {1}px; border-color:rgb({2}, {3}, {4});'.format(style, borderWidth, borderColor[0], borderColor[1], borderColor[2])
    borderRadius = 'border-radius: %spx;' % (h/3)
    return '{}{}{}'.format(height, border, borderRadius)

def initBtnStyle_color(obj=None, raiseObj=True):
    if obj.objectName() == 'arms_l_ikfk' or obj.objectName() == 'arms_r_ikfk' or obj.objectName() == 'legs_l_ikfk' or obj.objectName() == 'legs_r_ikfk':
        if obj.text() == 'IK':
            obj.setStyleSheet(startBtnStyle_round())
        else:
            obj.setStyleSheet(startBtnStyle_round(style='outset'))
    elif '_l' in obj.objectName():
        obj.setStyleSheet(startBtnStyle_sphere())
    elif '_r' in obj.objectName():
        obj.setStyleSheet(startBtnStyle_sphere(borderColor=[255, 100, 100]))
    elif '_c' in obj.objectName():
        obj.setStyleSheet(startBtnStyle_sphere(borderColor=[255, 255, 100]))
    if raiseObj:
        obj.raise_()

def changeBtnStyle_color(obj=None):
    if '_l' in obj.objectName():
        obj.setStyleSheet(startBtnStyle_sphere(style='dotted', borderWidth=3))
    elif '_r' in obj.objectName():
        obj.setStyleSheet(startBtnStyle_sphere(style='dotted', borderWidth=3, borderColor=[255, 100, 100]))
    elif '_c' in obj.objectName():
        obj.setStyleSheet(startBtnStyle_sphere(style='dotted', borderWidth=3, borderColor=[255, 255, 10]))

def checkBtnIsEnabled(obj=None):
    u"""Summary line.
    :param obj: QObject
    :type obj: QObject
    :returns: ボタンのbool値を受け取ってFalseであればTrueを返す
    """
    if obj.isEnabled() == False:
        invisBtnStyle(obj)

def invisBtnStyle(obj=None):
    obj.setStyleSheet("QPushButton { background-color: rgba(0, 0, 0, 0); }")
    obj.lower()

def setToolTips(obj=None):
    obj.setToolTip('{}'.format(obj.objectName()))

def getSelectedChannels(getTop=None, getShape=None):
    channelBox = mel.eval('global string $gChannelBoxName; $temp=$gChannelBoxName;')	#fetch maya's main channelbox
    if getTop == True:
        top_attrs = cmds.channelBox(channelBox, q=True, sma=True)
        sh_attrs = [None]
    if getShape == True:
        sh_attrs = cmds.channelBox(channelBox, q=True, ssa=True)
        top_attrs = [None]

    return top_attrs, sh_attrs

def searchAttrChannelBox(shSts=None):
    if shSts == True:
        getChannelBox = getSelectedChannels(getTop=None, getShape=True)
    else:
        getChannelBox = getSelectedChannels(getTop=True, getShape=None)

    results = []
    sel = cmds.ls(os=1)
    if not sel:
        return
    if shSts == True:
        sel = cmds.listRelatives(sel[0], s=1, pa=1)
    for attr in getChannelBox:
        if attr == None:
            continue
        else:
            attr = attr[0]
        for obj in sel:
            if attr in cmds.listAttr('{}'.format(obj), sn=1, k=1):
                results.append('{}.{}'.format(obj, attr))

    return results

def ikfkDefineContextMenu():
    selectedAttr_shape = searchAttrChannelBox(shSts=True)
    selectedAttr_obj = searchAttrChannelBox(shSts=None)
    try:
        selectedChBox = selectedAttr_shape + selectedAttr_obj
    except Exception as e:
        return
    fullpath = selectedChBox[0].split('|')
    origName = '|'.join(['{}'.format(path.split(':')[-1]) for path in fullpath])
    try:
        value = cmds.getAttr(selectedChBox[0])
    except Exception as e:
        value = ''
    return origName, selectedChBox[0], value

def unlock_transform_command(obj):
    cmds.setAttr('{}.tx'.format(obj), k=1, l=0)
    cmds.setAttr('{}.ty'.format(obj), k=1, l=0)
    cmds.setAttr('{}.tz'.format(obj), k=1, l=0)
    cmds.setAttr('{}.rx'.format(obj), k=1, l=0)
    cmds.setAttr('{}.ry'.format(obj), k=1, l=0)
    cmds.setAttr('{}.rz'.format(obj), k=1, l=0)
    cmds.setAttr('{}.sx'.format(obj), k=1, l=0)
    cmds.setAttr('{}.sy'.format(obj), k=1, l=0)
    cmds.setAttr('{}.sz'.format(obj), k=1, l=0)
    mel.eval("source channelBoxCommand;")
    mel.eval('CBunlockAttr "{}.tx";'.format(obj))
    mel.eval('CBunlockAttr "{}.ty";'.format(obj))
    mel.eval('CBunlockAttr "{}.tz";'.format(obj))
    mel.eval('CBunlockAttr "{}.rx";'.format(obj))
    mel.eval('CBunlockAttr "{}.ry";'.format(obj))
    mel.eval('CBunlockAttr "{}.rz";'.format(obj))
    mel.eval('CBunlockAttr "{}.sx";'.format(obj))
    mel.eval('CBunlockAttr "{}.sy";'.format(obj))
    mel.eval('CBunlockAttr "{}.sz";'.format(obj))

def ikToFkMatch(startJnt=None, middleJnt=None, endJnt=None, ikCtrl=None, ikPvCtrl=None, ikRotCtrl=None, clvFkCtrl=None, clvIkCtrl=None, foot=0, ballFkCtrl=None, ballIkCtrl=None, pelvis=None, move=20):
    objExists_sts = True
    objList = [startJnt, middleJnt, endJnt, ikCtrl, ikPvCtrl, ikRotCtrl]
    for obj in objList:
        if cmds.objExists(obj) == False:
            objExists_sts = False
    if objExists_sts == False:
        print('object not exists...')
        return

    start = cmds.xform(startJnt ,q= 1 ,ws = 1,t =1 )
    mid = cmds.xform(middleJnt ,q= 1 ,ws = 1,t =1 )
    end = cmds.xform(endJnt ,q= 1 ,ws = 1,t =1 )
    startV = OpenMaya.MVector(start[0] ,start[1],start[2])
    midV = OpenMaya.MVector(mid[0] ,mid[1],mid[2])
    endV = OpenMaya.MVector(end[0] ,end[1],end[2])

    cmds.xform(ikCtrl, t=[endV.x, endV.y, endV.z], a=1, ws=1)

    startEnd = endV - startV
    startMid = midV - startV

    dotP = startMid * startEnd
    proj = float(dotP) / float(startEnd.length())
    startEndN = startEnd.normal()
    projV = startEndN * proj

    arrowV = startMid - projV
    arrowV*= 0.5
    finalV = arrowV + midV

    cross1 = startEnd ^ startMid
    cross1.normalize()

    cross2 = cross1 ^ arrowV
    cross2.normalize()
    arrowV.normalize()

    matrixV = [arrowV.x , arrowV.y , arrowV.z , 0 ,cross1.x ,cross1.y , cross1.z , 0 ,cross2.x , cross2.y , cross2.z , 0,0,0,0,1]

    matrixM = OpenMaya.MMatrix()

    OpenMaya.MScriptUtil.createMatrixFromList(matrixV , matrixM)

    matrixFn = OpenMaya.MTransformationMatrix(matrixM)

    rot = matrixFn.eulerRotation()

    cmds.xform(ikPvCtrl , ws =1 , t= (finalV.x , finalV.y ,finalV.z))
    ikPvCtrl_dum = cmds.createNode('transform')
    # ikPvCtrl_dup = cmds.duplicate(ikPvCtrl, po=1)[0]
    # cmds.setAttr('{}.rotateX'.format(ikPvCtrl_dup), k=True)
    # cmds.setAttr('{}.rotateY'.format(ikPvCtrl_dup), k=True)
    # cmds.setAttr('{}.rotateZ'.format(ikPvCtrl_dup), k=True)

    # cmds.xform('{}'.format(ikPvCtrl_dup) , ws = 1 , rotation = ((rot.x/math.pi*180.0),(rot.y/math.pi*180.0),(rot.z/math.pi*180.0)))
    cmds.xform('{}'.format(ikPvCtrl_dum) , ws = 1 , rotation = ((rot.x/math.pi*180.0),(rot.y/math.pi*180.0),(rot.z/math.pi*180.0)))
    getSetTransform_api(src=ikPvCtrl, dst=ikPvCtrl_dum)
    cmds.select(ikPvCtrl_dum)
    cmds.move(move, 0, 0, r=1, os=1, wd=1)
    getSetTransform_api(src=ikPvCtrl_dum, dst=ikPvCtrl)
    """
    wt = cmds.xform(ikPvCtrl_dum, q=1, t=1, ws=1)
    cmds.xform(ikPvCtrl, t=wt, ws=1, a=1)
    """
    cmds.delete(ikPvCtrl_dum)

    if foot == 1:
        # [Main Solve] What IK Foot Rot?
        # foot FK query
        # pelvis = 'ply00_m_999_000:pelvis_C_fk_ctrl'
        thighFkRot = getRotation_api(startJnt)
        calfFkRot = getRotation_api(middleJnt)
        footFkRot = getRotation_api(endJnt)
        ballFkRot = getRotation_api(ballFkCtrl)
        pelvisRot = getRotation_api(pelvis)
        # foot IK query
        footIkPos = cmds.xform(endJnt, ws=1, q=1, t=1)
        kneeIkPos = cmds.xform(ikPvCtrl, ws=1, q=1, t=1)
        # duplicate
        for obj in [startJnt, middleJnt, endJnt, ballFkCtrl, ikCtrl, ikPvCtrl]:
            cmds.xform(obj, t=[0, 0, 0], ro=[0, 0, 0], a=1)

        cmds.xform(pelvis, ro=[0, 0, 0], a=1)
        # getSetRotation_api(src=pelvis, dst=ikCtrl)
        cmds.xform(ikCtrl, t=footIkPos, a=1, ws=1)
        cmds.xform(ikPvCtrl, t=kneeIkPos, a=1, ws=1)
        footFk_dup = cmds.duplicate(endJnt, po=1)[0]
        unlock_transform_command(footFk_dup)
        footIk_dup = cmds.duplicate(ikCtrl, po=1)[0]
        unlock_transform_command(footIk_dup)

        cmds.orientConstraint(footFk_dup, footIk_dup, w=1, mo=1)

        # FK re Rot
        setRotation_api(dst=pelvis, value=pelvisRot)
        setRotation_api(dst=startJnt, value=thighFkRot)
        setRotation_api(dst=middleJnt, value=calfFkRot)
        setRotation_api(dst=endJnt, value=footFkRot)
        setRotation_api(dst=footFk_dup, value=footFkRot)
        setRotation_api(dst=ballFkCtrl, value=ballFkRot)

        # IK re Pos
        getSetRotation_api(src=footIk_dup, dst=ikCtrl)
        setRotation_api(dst=ballIkCtrl, value=ballFkRot)

        cmds.delete(footFk_dup, footIk_dup)

        ballFkCtrlValue = getTransform_api(ballFkCtrl)
        ballIkCtrlValue = getTransform_api(ballIkCtrl)

    elif foot == 0:
        rVal = cmds.xform(endJnt, ws=1, q=1, ro=1)
        cmds.xform(ikRotCtrl, ro=rVal, ws=1, a=1)

        clavicleFkRot = cmds.xform(clvFkCtrl, q=1, ro=1, ws=1)
        rotOrderA = cmds.getAttr('{}.rotateOrder'.format(clvFkCtrl))
        rotOrderB = cmds.getAttr('{}.rotateOrder'.format(clvIkCtrl))
        euler = OpenMaya.MEulerRotation(math.radians(clavicleFkRot[0]), math.radians(clavicleFkRot[1]), math.radians(clavicleFkRot[2]), rotOrderA)
        r = euler.reorder(rotOrderB)
        cmds.xform(clvIkCtrl, ro=[math.degrees(r.x), math.degrees(r.y), math.degrees(r.z)], a=1, ws=1)

        clvFkCtrlValue = getTransform_api(clvFkCtrl)
        clvIkCtrlValue = getTransform_api(clvIkCtrl)

    startJntValue = getTransform_api(startJnt)
    middleJntValue = getTransform_api(middleJnt)
    endJntValue = getTransform_api(endJnt)
    ikCtrlValue = getTransform_api(ikCtrl)
    ikPvCtrlValue = getTransform_api(ikPvCtrl)
    ikRotCtrlValue = getTransform_api(ikRotCtrl)

    if foot == 0:
        return {startJnt:startJntValue, middleJnt:middleJntValue, endJnt:endJntValue, ikCtrl:ikCtrlValue, ikPvCtrl:ikPvCtrlValue, ikRotCtrl:ikRotCtrlValue, clvFkCtrl:clvFkCtrlValue, clvIkCtrl:clvIkCtrlValue}
    elif foot == 1:
        return {startJnt:startJntValue, middleJnt:middleJntValue, endJnt:endJntValue, ikCtrl:ikCtrlValue, ikPvCtrl:ikPvCtrlValue, ikRotCtrl:ikRotCtrlValue, ballFkCtrl:ballFkCtrlValue, ballIkCtrl:ballIkCtrlValue}

def create_reverseFoot(bakeanimation=False):
    cmds.cycleCheck(e=0)

    footCtrl = cmds.ls(os=1)
    if footCtrl == []:
        cmds.cycleCheck(e=1)
        return
    ballCtrl = footCtrl[1]

    footPos = cmds.xform(footCtrl[0], q=1, t=1, ws=1)
    footRot = cmds.xform(footCtrl[0], q=1, ro=1, ws=1)

    ballPos = cmds.xform(ballCtrl, q=1, t=1, ws=1)
    ballRot = cmds.xform(ballCtrl, q=1, ro=1, ws=1)

    rev_footMain = cmds.spaceLocator(n='footMain')[0]
    rev_footHeel = cmds.spaceLocator(n='footHeel')[0]
    rev_footToe = cmds.spaceLocator(n='footToe')[0]
    rev_footSideIn = cmds.spaceLocator(n='footSideIn')[0]
    rev_footSideOut = cmds.spaceLocator(n='footSideOut')[0]
    rev_footBall = cmds.spaceLocator(n='footBall')[0]
    rev_footHoldBall = cmds.spaceLocator(n='footHoldBall')[0]
    rev_footHold = cmds.spaceLocator(n='footHold')[0]

    # const
    mainRevFootPo = cmds.pointConstraint(footCtrl[0], rev_footMain, w=1)
    mainRevFootOri = cmds.orientConstraint(footCtrl[0], rev_footMain, w=1)

    reverseList = [rev_footHeel, rev_footToe, rev_footSideIn, rev_footSideOut, rev_footBall, rev_footHoldBall, rev_footHold]
    revGrpBuf = []
    revCatBuf = []
    revBuf = []

    i = 0
    for rev in reverseList:
        rev_grp = cmds.createNode('transform', n='{}_rev_grp'.format(rev))
        cat_grp = cmds.createNode('transform', n='{}_catch_grp'.format(rev))
        offset_grp = cmds.createNode('transform', n='{}_offset_grp'.format(rev))
        cmds.parent(rev, offset_grp)
        cmds.parent(offset_grp, rev_grp)
        cmds.parent(cat_grp, rev_grp)
        cmds.parent(rev_grp, rev_footMain)
        revGrpBuf.append(rev_grp)
        revCatBuf.append(cat_grp)
        if i != 0:
            cmds.parent(revGrpBuf[i], revCatBuf[i-1])
            if rev == rev_footHold:
                cmds.parent(revGrpBuf[i], revCatBuf[i-2])
            elif rev == rev_footHoldBall:
                cmds.parent(revGrpBuf[i], revCatBuf[i-2])

        cmds.xform(revGrpBuf[i], t=[0, 0, 0], ro=[0, 0, 0], a=1)

        if rev == rev_footHoldBall:
            cmds.xform('{}_offset_grp'.format(rev), t=ballPos, ro=ballRot, a=1, ws=1)
        elif rev == rev_footBall:
            cmds.xform('{}_offset_grp'.format(rev), t=ballPos, ro=ballRot, a=1, ws=1)
        # connection
        cmds.connectAttr('{}.translate'.format(rev), '{}_rev_grp.rotatePivot'.format(rev), f=1)
        cmds.connectAttr('{}.translate'.format(rev), '{}_rev_grp.scalePivot'.format(rev), f=1)

        cmds.connectAttr('{}.translate'.format(rev), '{}_catch_grp.rotatePivot'.format(rev), f=1)
        cmds.connectAttr('{}.translate'.format(rev), '{}_catch_grp.scalePivot'.format(rev), f=1)

        cmds.connectAttr('{}.rotate'.format(rev), '{}_catch_grp.rotate'.format(rev), f=1)

        i += 1

    mainRevBallPo = cmds.pointConstraint(ballCtrl, rev_footHoldBall, w=1)
    mainRevBallOri = cmds.orientConstraint(ballCtrl, rev_footHoldBall, w=1)

    # matrix
    footBall_mat_tfn = '{}_mat_grp'.format(rev_footBall)
    dup = cmds.duplicate('{}_catch_grp'.format(rev_footBall), n=footBall_mat_tfn, po=1)[0]
    cmds.parent(dup, rev_footBall)

    mmx = '{}_mmx'.format(rev_footBall)
    dmx = '{}_dmx'.format(rev_footBall)
    cmds.createNode('multMatrix', n=mmx)
    cmds.createNode('decomposeMatrix', n=dmx)

    cmds.connectAttr('{}.matrix'.format(dup), '{}.matrixIn[0]'.format(mmx), f=1)
    cmds.connectAttr('{}.matrix'.format(rev_footBall), '{}.matrixIn[1]'.format(mmx), f=1)
    cmds.connectAttr('{}.matrix'.format('{}_offset_grp'.format(rev_footBall)), '{}.matrixIn[2]'.format(mmx), f=1)

    cmds.connectAttr('{}.matrixSum'.format(mmx), '{}.inputMatrix'.format(dmx), f=1)

    cmds.connectAttr('{}.outputTranslate'.format(dmx), '{}.translate'.format('{}_catch_grp'.format(rev_footBall)), f=1)
    cmds.connectAttr('{}.outputRotate'.format(dmx), '{}.rotate'.format('{}_catch_grp'.format(rev_footBall)), f=1)

    playmin = cmds.playbackOptions(q=1, min=1)
    playmax = cmds.playbackOptions(q=1, max=1)

    if bakeanimation == True:
        try:
            autokeySts = cmds.autoKeyframe(q=1, st=1)
            if autokeySts:
                cmds.autoKeyframe(st=0)
            cmds.refresh(su=1)
            cmds.bakeResults([rev_footMain, rev_footHoldBall], sm=1, t=(playmin, playmax), sb=1, osr=1, dic=1, pok=1, sac=0, ral=0, rba=0, bol=0, mr=1, cp=0, s=0)
            cmds.refresh(su=0)
            cmds.autoKeyframe(st=autokeySts)
        except Exception as e:
            print(e)

    cmds.delete(mainRevFootPo[0], mainRevFootOri[0], mainRevBallPo[0], mainRevBallOri[0])

    cmds.cycleCheck(e=1)

    noneSts =  {'skip': []}

    foot_rot_flags = rot_skippy(rev_footHold)
    try:
        if foot_rot_flags != noneSts:
            foot_ori = cmds.orientConstraint(rev_footHold, footCtrl[0], w=1, **foot_rot_flags)
        else:
            foot_ori = cmds.orientConstraint(rev_footHold, footCtrl[0], w=1)
    except Exception as e:
        pass

    foot_po_flags = rot_skippy(rev_footHold)
    try:
        if foot_po_flags != noneSts:
            foot_po = cmds.pointConstraint(rev_footHold, footCtrl[0], w=1, **foot_po_flags)
        else:
            foot_po = cmds.pointConstraint(rev_footHold, footCtrl[0], w=1)
    except Exception as e:
        pass

    ball_rot_flags = rot_skippy(rev_footHoldBall)
    try:
        if ball_rot_flags != noneSts:
            ball_ori = cmds.orientConstraint(rev_footHoldBall, ballCtrl, w=1, **ball_rot_flags)
        else:
            ball_ori = cmds.orientConstraint(rev_footHoldBall, ballCtrl, w=1)
    except Exception as e:
        pass

    ball_po_flags = rot_skippy(rev_footHoldBall)
    try:
        if ball_po_flags != noneSts:
            ball_po = cmds.pointConstraint(rev_footHoldBall, ballCtrl, w=1, **ball_po_flags)
        else:
            ball_po = cmds.pointConstraint(rev_footHoldBall, ballCtrl, w=1)
    except Exception as e:
        pass

def fkToIkMatch(startFkCtrl=None, middleFkCtrl=None, endFkCtrl=None, ikHandle=None, clvIkCtrl=None, clvFkCtrl=None, foot=None):
    objExists_sts = True
    objList = [startFkCtrl, middleFkCtrl, endFkCtrl, clvFkCtrl, clvIkCtrl]
    for obj in objList:
        if cmds.objExists(obj) == False:
            objExists_sts = False
    if objExists_sts == False:
        print('object not exists...')
        return

    if foot == None:
        clavicleIkRot = cmds.xform(clvIkCtrl, q=1, ro=1, ws=1)
        cmds.xform(clvFkCtrl, ro=clavicleIkRot, a=1, ws=1)

    jntList = cmds.ikHandle(ikHandle, q=1, jointList=1)
    endJnt = cmds.listRelatives(jntList[(len(jntList)-1)], children=1, type='joint')
    jntList.append(endJnt[0])

    srcFks = [startFkCtrl, middleFkCtrl, endFkCtrl]

    for j in range(len(jntList)):
        getSetRotation_api(src=jntList[j], dst=srcFks[j])

    if foot == True:
        clavicleIkRot = cmds.xform(clvIkCtrl, q=1, ro=1, ws=1)
        cmds.xform(clvFkCtrl, ro=clavicleIkRot, a=1, ws=1)

    startJntValue = getTransform_api(startFkCtrl)
    middleJntValue = getTransform_api(middleFkCtrl)
    endJntValue = getTransform_api(endFkCtrl)
    clvFkCtrlValue = getTransform_api(clvFkCtrl)
    clvIkCtrlValue = getTransform_api(clvIkCtrl)

    return {startFkCtrl:startJntValue, middleFkCtrl:middleJntValue, endFkCtrl:endJntValue, clvFkCtrl:clvFkCtrlValue, clvIkCtrl:clvIkCtrlValue}

def getTransform_api(name):
    selected = OpenMaya.MSelectionList()
    selected.add(name)
    obj = OpenMaya.MObject()
    selected.getDependNode(0,obj)
    nodeDagPath = OpenMaya.MDagPath()
    selected.getDagPath(0, nodeDagPath)
    # mTransformMtx = OpenMaya.MFnTransform(obj)

    transformFunc = OpenMaya.MFnTransform(nodeDagPath) # MFnTransform
    mTransformMtx = transformFunc.transformation() # MTransformationMatrix
    # Part 2, get the euler values
    # Get an MEulerRotation object
    eulerRot = mTransformMtx.eulerRotation() # MEulerRotation
    # note, we *don't* have to set the rot order here...
    # Convert from radians to degrees:
    angles = [math.degrees(angle) for angle in (eulerRot.x, eulerRot.y, eulerRot.z)]

    translate = OpenMaya.MVector()
    translate = transformFunc.getTranslation(OpenMaya.MSpace.kTransform)

    # print(translate.x, translate.y, translate.z, eulerRot.x, eulerRot.y, eulerRot.z)
    return [translate.x, translate.y, translate.z], [eulerRot.x, eulerRot.y, eulerRot.z]

def getSetTransform_api(src=None, dst=None):
    obj = src

    selection = OpenMaya2.MSelectionList()
    selection.add(obj)
    dag = selection.getDagPath(0)

    transform_fn = OpenMaya2.MFnTransform(dag)
    trans = transform_fn.translation(OpenMaya2.MSpace.kWorld)

    obj2 = dst
    selection2 = OpenMaya2.MSelectionList()
    selection2.add(obj2)
    dag2 = selection2.getDagPath(0)

    transform_fn2 = OpenMaya2.MFnTransform(dag2)
    transform_fn2.setTranslation(trans, OpenMaya2.MSpace.kWorld)

def getSetRotation_api(src=None, dst=None):
    obj = src

    selection = OpenMaya2.MSelectionList()
    selection.add(obj)
    dag = selection.getDagPath(0)

    transform_fn = OpenMaya2.MFnTransform(dag)
    quat = transform_fn.rotation(OpenMaya2.MSpace.kWorld, True)
    euler = transform_fn.rotation(OpenMaya2.MSpace.kTransform, False)
    m_quat = OpenMaya2.MQuaternion(quat)

    obj2 = dst
    selection2 = OpenMaya2.MSelectionList()
    selection2.add(obj2)
    dag2 = selection2.getDagPath(0)

    transform_fn2 = OpenMaya2.MFnTransform(dag2)
    transform_fn2.setRotation(m_quat, OpenMaya2.MSpace.kWorld)

def getRotation_api(src=None):
    obj = src

    selection = OpenMaya2.MSelectionList()
    selection.add(obj)
    dag = selection.getDagPath(0)

    transform_fn = OpenMaya2.MFnTransform(dag)
    quat = transform_fn.rotation(OpenMaya2.MSpace.kWorld, True)
    euler = transform_fn.rotation(OpenMaya2.MSpace.kTransform, False)
    m_quat = OpenMaya2.MQuaternion(quat)

    return quat

def setRotation_api(dst=None, value=None):
    obj2 = dst
    selection2 = OpenMaya2.MSelectionList()
    selection2.add(obj2)
    dag2 = selection2.getDagPath(0)

    transform_fn2 = OpenMaya2.MFnTransform(dag2)
    transform_fn2.setRotation(value, OpenMaya2.MSpace.kWorld)

def strToNum_list(src=None):
    str_num = src
    float_num = []
    for x in str_num.split(','):
        if '[' in x:
            x = x.strip('[')
        elif ']' in x:
            x = x.strip(']')
        float_num.append(float(x))
    return float_num

def rot_skippy(obj):
    flags = {}
    axis = ['x', 'y', 'z']
    attr = cmds.listAttr(obj, k=1, sn=1)
    for at in attr:
        if 'rx' in at:
            axis.remove('x')
        if 'ry' in at:
            axis.remove('y')
        if 'rz' in at:
            axis.remove('z')
    flags['skip'] = axis
    return flags

def trans_skippy(obj):
    flags = {}
    axis = ['x', 'y', 'z']
    attr = cmds.listAttr(obj, k=1, sn=1)
    for at in attr:
        if 'tx' in at:
            axis.remove('x')
        if 'ty' in at:
            axis.remove('y')
        if 'tz' in at:
            axis.remove('z')
    flags['skip'] = axis
    return flags



class IKtoFK():
    def __init__(self, namespace):
        self.namespace = namespace
        """
        left leg ############################################################
        """
        # ik ctrls
        self.l_legs_poleVector = '{}:proxy_L_shin_pv_ctrl'.format(self.namespace)
        self.l_legs_ik_ctrl = '{}:proxy_L_foot_ik_ctrl'.format(self.namespace)
        l_legs_ik_rot_ctrl = '{}:proxy_L_foot_ik_ctrl'.format(self.namespace)
        l_legs_ik_end_ctrl = '{}:proxy_L_foot_ik_ctrl_revFoot_holdBall_ctrl'.format(self.namespace)

        l_legs_hips = [u'{}:proxy_root_body_cog_lower_ctrl'.format(self.namespace),
                u'{}:proxy_root_body_cog_upper_ctrl'.format(self.namespace),
                u'{}:proxy_root_body_cog_main_ctrl'.format(self.namespace)]

        # fk ctrls
        l_legs_start_ctrl = '{}:proxy_L_thigh_fk_ctrl'.format(self.namespace)
        l_legs_mid_ctrl = '{}:proxy_L_shin_fk_ctrl'.format(self.namespace)
        l_legs_end_ctrl = '{}:proxy_L_foot_fk_ctrl'.format(self.namespace)
        l_legs_tip_ctrl = '{}:proxy_L_toe_fk_ctrl'.format(self.namespace)
        l_legs_fk_shoulder_ctrl = None
        l_legs_distance = 10

        self.left_legs = {}
        self.left_legs['poleVector'] = self.l_legs_poleVector
        self.left_legs['ik_ctrl'] = self.l_legs_ik_ctrl
        self.left_legs['ik_rot_ctrl'] = l_legs_ik_rot_ctrl
        self.left_legs['ik_end_ctrl'] = l_legs_ik_end_ctrl
        self.left_legs['hips'] = l_legs_hips
        self.left_legs['start_ctrl'] = l_legs_start_ctrl
        self.left_legs['mid_ctrl'] = l_legs_mid_ctrl
        self.left_legs['end_ctrl'] = l_legs_end_ctrl
        self.left_legs['tip_ctrl'] = l_legs_tip_ctrl
        self.left_legs['fk_shoulder_ctrl'] = l_legs_fk_shoulder_ctrl
        self.left_legs['distance'] = l_legs_distance

        """
        right leg ############################################################
        """
        # ik ctrls
        self.r_legs_poleVector = '{}:proxy_R_shin_pv_ctrl'.format(self.namespace)
        self.r_legs_ik_ctrl = '{}:proxy_R_foot_ik_ctrl'.format(self.namespace)
        r_legs_ik_rot_ctrl = '{}:proxy_R_foot_ik_ctrl'.format(self.namespace)
        r_legs_ik_end_ctrl = '{}:proxy_R_foot_ik_ctrl_revFoot_holdBall_ctrl'.format(self.namespace)

        r_legs_hips = [u'{}:proxy_root_body_cog_lower_ctrl'.format(self.namespace),
                u'{}:proxy_root_body_cog_upper_ctrl'.format(self.namespace),
                u'{}:proxy_root_body_cog_main_ctrl'.format(self.namespace)]

        # fk ctrls
        r_legs_start_ctrl = '{}:proxy_R_thigh_fk_ctrl'.format(self.namespace)
        r_legs_mid_ctrl = '{}:proxy_R_shin_fk_ctrl'.format(self.namespace)
        r_legs_end_ctrl = '{}:proxy_R_foot_fk_ctrl'.format(self.namespace)
        r_legs_tip_ctrl = '{}:proxy_R_toe_fk_ctrl'.format(self.namespace)
        r_legs_fk_shoulder_ctrl = None
        r_legs_distance = 10

        self.right_legs = {}
        self.right_legs['poleVector'] = self.r_legs_poleVector
        self.right_legs['ik_ctrl'] = self.r_legs_ik_ctrl
        self.right_legs['ik_rot_ctrl'] = r_legs_ik_rot_ctrl
        self.right_legs['ik_end_ctrl'] = r_legs_ik_end_ctrl
        self.right_legs['hips'] = r_legs_hips
        self.right_legs['start_ctrl'] = r_legs_start_ctrl
        self.right_legs['mid_ctrl'] = r_legs_mid_ctrl
        self.right_legs['end_ctrl'] = r_legs_end_ctrl
        self.right_legs['tip_ctrl'] = r_legs_tip_ctrl
        self.right_legs['fk_shoulder_ctrl'] = r_legs_fk_shoulder_ctrl
        self.right_legs['distance'] = r_legs_distance

        """
        left arm ############################################################
        """
        # ik ctrls
        self.l_arms_poleVector = '{}:proxy_L_upperarm_pv_ctrl'.format(self.namespace)
        self.l_arms_ik_ctrl = '{}:proxy_L_hand_ik_ctrl'.format(self.namespace)
        l_arms_ik_rot_ctrl = '{}:proxy_L_hand_ikRot_ctrl'.format(self.namespace)
        l_arms_ik_end_ctrl = '{}:proxy_L_shoulder_ikAutoShoulder_jnt_ikAutoShoulder_ctrl'.format(self.namespace)

        l_arms_hips = [u'{}:proxy_root_body_cog_main_ctrl'.format(self.namespace),
                 u'{}:proxy_root_body_cog_lower_ctrl'.format(self.namespace),
                 u'{}:proxy_waist_fk_ctrl'.format(self.namespace),
                 u'{}:proxy_spine_fk_ctrl'.format(self.namespace),
                 u'{}:proxy_chest_fk_ctrl'.format(self.namespace)]

        # fk ctrls
        l_arms_start_ctrl = '{}:proxy_L_upperarm_fk_ctrl'.format(self.namespace)
        l_arms_mid_ctrl = '{}:proxy_L_lowerarm_fk_ctrl'.format(self.namespace)
        l_arms_end_ctrl = '{}:proxy_L_hand_fk_ctrl'.format(self.namespace)
        l_arms_tip_ctrl = '{}:proxy_L_shoulder_fk_ctrl'.format(self.namespace)
        l_arms_fk_shoulder_ctrl = '{}:proxy_L_shoulder_fk_ctrl'.format(self.namespace)
        l_arms_distance = 10

        self.left_arms = {}
        self.left_arms['poleVector'] = self.l_arms_poleVector
        self.left_arms['ik_ctrl'] = self.l_arms_ik_ctrl
        self.left_arms['ik_rot_ctrl'] = l_arms_ik_rot_ctrl
        self.left_arms['ik_end_ctrl'] = l_arms_ik_end_ctrl
        self.left_arms['hips'] = l_arms_hips
        self.left_arms['ik_auto_rot'] = True
        self.left_arms['start_ctrl'] = l_arms_start_ctrl
        self.left_arms['mid_ctrl'] = l_arms_mid_ctrl
        self.left_arms['end_ctrl'] = l_arms_end_ctrl
        self.left_arms['tip_ctrl'] = l_arms_tip_ctrl
        self.left_arms['fk_shoulder_ctrl'] = l_arms_fk_shoulder_ctrl
        self.left_arms['distance'] = l_arms_distance

        """
        right arm ############################################################
        """
        # ik ctrls
        self.r_arms_poleVector = '{}:proxy_R_upperarm_pv_ctrl'.format(self.namespace)
        self.r_arms_ik_ctrl = '{}:proxy_R_hand_ik_ctrl'.format(self.namespace)
        r_arms_ik_rot_ctrl = '{}:proxy_R_hand_ikRot_ctrl'.format(self.namespace)
        r_arms_ik_end_ctrl = '{}:proxy_R_shoulder_ikAutoShoulder_jnt_ikAutoShoulder_ctrl'.format(self.namespace)

        r_arms_hips = [u'{}:proxy_root_body_cog_main_ctrl'.format(self.namespace),
                 u'{}:proxy_root_body_cog_lower_ctrl'.format(self.namespace),
                 u'{}:proxy_waist_fk_ctrl'.format(self.namespace),
                 u'{}:proxy_spine_fk_ctrl'.format(self.namespace),
                 u'{}:proxy_chest_fk_ctrl'.format(self.namespace)]

        # fk ctrls
        r_arms_start_ctrl = '{}:proxy_R_upperarm_fk_ctrl'.format(self.namespace)
        r_arms_mid_ctrl = '{}:proxy_R_lowerarm_fk_ctrl'.format(self.namespace)
        r_arms_end_ctrl = '{}:proxy_R_hand_fk_ctrl'.format(self.namespace)
        r_arms_tip_ctrl = '{}:proxy_R_shoulder_fk_ctrl'.format(self.namespace)
        r_arms_fk_shoulder_ctrl = '{}:proxy_R_shoulder_fk_ctrl'.format(self.namespace)
        r_arms_distance = 10

        self.right_arms = {}
        self.right_arms['poleVector'] = self.r_arms_poleVector
        self.right_arms['ik_ctrl'] = self.r_arms_ik_ctrl
        self.right_arms['ik_rot_ctrl'] = r_arms_ik_rot_ctrl
        self.right_arms['ik_end_ctrl'] = r_arms_ik_end_ctrl
        self.right_arms['hips'] = r_arms_hips
        self.right_arms['ik_auto_rot'] = True
        self.right_arms['start_ctrl'] = r_arms_start_ctrl
        self.right_arms['mid_ctrl'] = r_arms_mid_ctrl
        self.right_arms['end_ctrl'] = r_arms_end_ctrl
        self.right_arms['tip_ctrl'] = r_arms_tip_ctrl
        self.right_arms['fk_shoulder_ctrl'] = r_arms_fk_shoulder_ctrl
        self.right_arms['distance'] = r_arms_distance

    # ik to fk
    def ik_to_fk_match(self, poleVector=None, ik_ctrl=None, ik_rot_ctrl=None, ik_end_ctrl=None, hips=None, ik_auto_rot=False,
                 start_ctrl=None, mid_ctrl=None, end_ctrl=None, fk_shoulder_ctrl=None, tip_ctrl=None, distance=10):

        # ik ctrl [rotate]
        pos_dict = {}

        if hips != None:
            for obj in hips:
                pos_dict[obj] = {}
                pos_dict[obj]['translate'] = cmds.xform(obj, q=1, t=1, os=1)
                pos_dict[obj]['rotate'] = cmds.xform(obj, q=1, ro=1, os=1)
                keyable_attrs = cmds.listAttr(obj, k=1)
                if 'translateX' in keyable_attrs:
                    cmds.xform(obj,
                               t=[0, cmds.xform(obj, q=1, t=1, os=1, a=1)[1], cmds.xform(obj, q=1, t=1, os=1, a=1)[2]],
                               os=1, a=1)
                if 'translateY' in keyable_attrs:
                    cmds.xform(obj,
                               t=[cmds.xform(obj, q=1, t=1, os=1, a=1)[0], 0, cmds.xform(obj, q=1, t=1, os=1, a=1)[2]],
                               os=1, a=1)
                if 'translateZ' in keyable_attrs:
                    cmds.xform(obj,
                               t=[cmds.xform(obj, q=1, t=1, os=1, a=1)[0], cmds.xform(obj, q=1, t=1, os=1, a=1)[1], 0],
                               os=1, a=1)

                if 'rotateX' in keyable_attrs:
                    cmds.xform(obj,
                               ro=[0, cmds.xform(obj, q=1, ro=1, os=1, a=1)[1], cmds.xform(obj, q=1, ro=1, os=1, a=1)[2]],
                               os=1, a=1)
                if 'rotateY' in keyable_attrs:
                    cmds.xform(obj,
                               ro=[cmds.xform(obj, q=1, ro=1, os=1, a=1)[0], 0, cmds.xform(obj, q=1, ro=1, os=1, a=1)[2]],
                               os=1, a=1)
                if 'rotateZ' in keyable_attrs:
                    cmds.xform(obj,
                               ro=[cmds.xform(obj, q=1, ro=1, os=1, a=1)[0], cmds.xform(obj, q=1, ro=1, os=1, a=1)[1], 0],
                               os=1, a=1)

        for obj in [start_ctrl, mid_ctrl, end_ctrl, fk_shoulder_ctrl]:
            if obj == None:
                continue
            pos_dict[obj] = {}
            if cmds.objExists(obj):
                pos_dict[obj]['translate'] = cmds.xform(obj, q=1, t=1, os=1)
                pos_dict[obj]['rotate'] = cmds.xform(obj, q=1, ro=1, os=1)
            keyable_attrs = cmds.listAttr(obj, k=1)
            if 'translateX' in keyable_attrs:
                cmds.xform(obj,
                           t=[0, cmds.xform(obj, q=1, t=1, os=1, a=1)[1], cmds.xform(obj, q=1, t=1, os=1, a=1)[2]],
                           os=1, a=1)
            if 'translateY' in keyable_attrs:
                cmds.xform(obj,
                           t=[cmds.xform(obj, q=1, t=1, os=1, a=1)[0], 0, cmds.xform(obj, q=1, t=1, os=1, a=1)[2]],
                           os=1, a=1)
            if 'translateZ' in keyable_attrs:
                cmds.xform(obj,
                           t=[cmds.xform(obj, q=1, t=1, os=1, a=1)[0], cmds.xform(obj, q=1, t=1, os=1, a=1)[1], 0],
                           os=1, a=1)

            if 'rotateX' in keyable_attrs:
                cmds.xform(obj,
                           ro=[0, cmds.xform(obj, q=1, ro=1, os=1, a=1)[1], cmds.xform(obj, q=1, ro=1, os=1, a=1)[2]],
                           os=1, a=1)
            if 'rotateY' in keyable_attrs:
                cmds.xform(obj,
                           ro=[cmds.xform(obj, q=1, ro=1, os=1, a=1)[0], 0, cmds.xform(obj, q=1, ro=1, os=1, a=1)[2]],
                           os=1, a=1)
            if 'rotateZ' in keyable_attrs:
                cmds.xform(obj,
                           ro=[cmds.xform(obj, q=1, ro=1, os=1, a=1)[0], cmds.xform(obj, q=1, ro=1, os=1, a=1)[1], 0],
                           os=1, a=1)

        for obj in [poleVector, ik_ctrl, ik_rot_ctrl, ik_end_ctrl]:
            if obj == None:
                continue
            keyable_attrs = cmds.listAttr(obj, k=1)
            if 'translateX' in keyable_attrs:
                cmds.setAttr('{}.tx'.format(obj), 0)
            if 'translateY' in keyable_attrs:
                cmds.setAttr('{}.ty'.format(obj), 0)
            if 'translateZ' in keyable_attrs:
                cmds.setAttr('{}.tz'.format(obj), 0)

            if 'rotateX' in keyable_attrs:
                cmds.setAttr('{}.rx'.format(obj), 0)
            if 'rotateY' in keyable_attrs:
                cmds.setAttr('{}.ry'.format(obj), 0)
            if 'rotateZ' in keyable_attrs:
                cmds.setAttr('{}.rz'.format(obj), 0)

        ik_pos_loc = cmds.spaceLocator()[0]
        ik_rot_pos = cmds.xform(ik_rot_ctrl, q=1, t=1, ws=1)
        ik_rot_rot = cmds.xform(ik_rot_ctrl, q=1, ro=1, ws=1)
        cmds.xform(ik_pos_loc, t=ik_rot_pos, ro=ik_rot_rot, ws=1, a=1)
        cmds.parentConstraint(end_ctrl, ik_pos_loc, w=1, mo=1)
        # return poleVector, ik_ctrl, ik_rot_ctrl, ik_end_ctrl

        autokeyAts = cmds.autoKeyframe(q=1, st=1)
        if autokeyAts:
            cmds.autoKeyframe(st=False)
        for k, v in pos_dict.items():
            if cmds.objExists(k):
                cmds.xform(k, t=v['translate'], ro=v['rotate'], os=1, a=1)
        cmds.autoKeyframe(st=autokeyAts)
        cmds.xform(ik_rot_ctrl, ro=cmds.xform(ik_pos_loc, q=1, ro=1, ws=1), ws=1, a=1)
        cmds.delete(ik_pos_loc)

        # ik ctrl [translate]
        cmds.matchTransform(ik_ctrl, end_ctrl, pos=1)

        # ik end ctrl [translate] [rotate]
        if fk_shoulder_ctrl != None:
            cmds.matchTransform(ik_end_ctrl, fk_shoulder_ctrl)

        self.set_poleVector(start_ctrl, mid_ctrl, end_ctrl, poleVector, distance)

        # ik end ctrl [translate] [rotate]
        cmds.matchTransform(ik_end_ctrl, tip_ctrl)

        # ik Auto Rot
        if ik_auto_rot:
            cmds.matchTransform(ik_rot_ctrl, end_ctrl)

        return poleVector, ik_ctrl, ik_rot_ctrl, ik_end_ctrl

    def simple_match(self, poleVector=None, ik_ctrl=None, ik_rot_ctrl=None, ik_end_ctrl=None, hips=None, ik_auto_rot=False,
                 start_ctrl=None, mid_ctrl=None, end_ctrl=None, fk_shoulder_ctrl=None, tip_ctrl=None, distance=10):
        # match ctrl
        poleVector_list = [start_ctrl, mid_ctrl, end_ctrl, distance]
        fk_list = [tip_ctrl, mid_ctrl, end_ctrl]

        ikfk_relation = {}
        ikfk_relation[end_ctrl] = [ik_ctrl, ik_rot_ctrl]
        ikfk_relation[mid_ctrl] = ['poleVector', poleVector]
        ikfk_relation[tip_ctrl] = ik_end_ctrl

        for match_fk_ctrl in fk_list:
            match_Loc = cmds.spaceLocator()[0]
            cmds.matchTransform(match_Loc, match_fk_ctrl)
            if type(ikfk_relation[match_fk_ctrl]) == list:
                if ikfk_relation[match_fk_ctrl][0] != 'poleVector':
                    cmds.matchTransform(ikfk_relation[match_fk_ctrl][0], match_Loc, pos=1)
                    cmds.matchTransform(ikfk_relation[match_fk_ctrl][1], match_Loc, rot=1)
                else:
                    # polevector
                    self.set_poleVector(poleVector_list[0], poleVector_list[1], poleVector_list[2], ikfk_relation[match_fk_ctrl][1], poleVector_list[3])
            else:
                cmds.matchTransform(ikfk_relation[match_fk_ctrl], match_Loc)

            cmds.delete(match_Loc)

        return poleVector, ik_ctrl, ik_rot_ctrl, ik_end_ctrl


    def set_poleVector(self, start_ctrl, mid_ctrl, end_ctrl, poleVector, distance):
        # poleVector
        start = cmds.xform(start_ctrl ,q= 1 ,ws = 1,t =1 )
        mid = cmds.xform(mid_ctrl ,q= 1 ,ws = 1,t =1 )
        end = cmds.xform(end_ctrl ,q= 1 ,ws = 1,t =1 )

        startV = OpenMaya.MVector(start[0] ,start[1],start[2])
        midV = OpenMaya.MVector(mid[0] ,mid[1],mid[2])
        endV = OpenMaya.MVector(end[0] ,end[1],end[2])

        startEnd = endV - startV
        startMid = midV - startV

        dotP = startMid * startEnd
        proj = float(dotP) / float(startEnd.length())
        startEndN = startEnd.normal()
        projV = startEndN * proj

        arrowV = startMid - projV
        arrowV*= 0.5
        finalV = arrowV + midV

        cross1 = startEnd ^ startMid
        cross1.normalize()

        cross2 = cross1 ^ arrowV
        cross2.normalize()
        arrowV.normalize()

        matrixV = [arrowV.x , arrowV.y , arrowV.z , 0 ,
        cross1.x ,cross1.y , cross1.z , 0 ,
        cross2.x , cross2.y , cross2.z , 0,
        0,0,0,1]

        matrixM = OpenMaya.MMatrix()

        OpenMaya.MScriptUtil.createMatrixFromList(matrixV , matrixM)

        matrixFn = OpenMaya.MTransformationMatrix(matrixM)

        rot = matrixFn.eulerRotation()

        loc = cmds.spaceLocator()[0]
        cmds.xform(loc , ws =1 , t= (finalV.x , finalV.y ,finalV.z))

        cmds.xform ( loc , ws = 1 , rotation = ((rot.x/math.pi*180.0),
        (rot.y/math.pi*180.0),
        (rot.z/math.pi*180.0)))

        cmds.move(distance, 0, 0, loc, os=1, wd=1, r=1)

        cmds.xform(poleVector, t=cmds.xform(loc, q=1, t=1, ws=1), ws=1, a=1)
        cmds.delete(loc)

    def current_match(self, l_legs=True, r_legs=True, l_arms=True, r_arms=True):
        if l_arms:
            value = self.ik_to_fk_match(**self.left_arms)
        if r_arms:
            value = self.ik_to_fk_match(**self.right_arms)
        if l_legs:
            value = self.ik_to_fk_match(**self.left_legs)
        if r_legs:
            value = self.ik_to_fk_match(**self.right_legs)

        return value

    def bakeanim(self, select_timeslider=True, simplebake=False, l_legs=True, r_legs=True, l_arms=True, r_arms=True):
        playCur = cmds.currentTime(q=1)

        playmin = cmds.playbackOptions(q=1, min=1)
        playmax = cmds.playbackOptions(q=1, max=1)

        if select_timeslider:
            aPlayBackSliderPython = mel.eval('$tmpVar=$gPlayBackSlider')
            rangeArray = cmds.timeControl( aPlayBackSliderPython, q=True, rangeArray=True)

            playmin = rangeArray[0]
            playmax = rangeArray[1]

        cmds.cycleCheck(e=False)

        autokey_sts = cmds.autoKeyframe(q=1, st=1)
        if autokey_sts == True:
            cmds.autoKeyframe(st=False)

        cmds.refresh(suspend=True)
        x = int(playmin)
        for i in range(int(playmax)+1):
            f = i + x
            if f == int(playmax)+1:
                break
            else:
                cmds.currentTime(f)

            # options
            cmds.setAttr('{}.space'.format(self.l_legs_ik_ctrl), 0);cmds.setAttr('{}.space'.format(self.l_legs_poleVector), 0)
            cmds.setAttr('{}.space'.format(self.r_legs_ik_ctrl), 0);cmds.setAttr('{}.space'.format(self.r_legs_poleVector), 0)
            cmds.setAttr('{}.space'.format(self.l_arms_ik_ctrl), 0);cmds.setAttr('{}.space'.format(self.l_arms_poleVector), 0)
            cmds.setAttr('{}.space'.format(self.r_arms_ik_ctrl), 0);cmds.setAttr('{}.space'.format(self.r_arms_poleVector), 0)

            cmds.setAttr("{}:proxy_L_foot_ikRot_ctrl.rx".format(self.namespace), 0)
            cmds.setAttr("{}:proxy_L_foot_ikRot_ctrl.ry".format(self.namespace), 0)
            cmds.setAttr("{}:proxy_L_foot_ikRot_ctrl.rz".format(self.namespace), 0)
            cmds.setAttr("{}:proxy_R_foot_ikRot_ctrl.rx".format(self.namespace), 0)
            cmds.setAttr("{}:proxy_R_foot_ikRot_ctrl.ry".format(self.namespace), 0)
            cmds.setAttr("{}:proxy_R_foot_ikRot_ctrl.rz".format(self.namespace), 0)

            if l_legs:
                # print('left legs {}'.format(str(f)))
                if simplebake:
                    poleVector_buf, ik_ctrl_buf, ik_rot_ctrl_buf, ik_end_ctrl_buf = self.simple_match(**self.left_legs)
                else:
                    poleVector_buf, ik_ctrl_buf, ik_rot_ctrl_buf, ik_end_ctrl_buf = self.ik_to_fk_match(**self.left_legs)
                cmds.clearCache(allNodes=1)
                cmds.setKeyframe([poleVector_buf, ik_ctrl_buf, ik_rot_ctrl_buf, ik_end_ctrl_buf], breakdown=0, hierarchy='none', shape=0, controlPoints=0)

            if r_legs:
                # print('right legs {}'.format(str(f)))
                if simplebake:
                    poleVector_buf, ik_ctrl_buf, ik_rot_ctrl_buf, ik_end_ctrl_buf = self.simple_match(**self.right_legs)
                else:
                    poleVector_buf, ik_ctrl_buf, ik_rot_ctrl_buf, ik_end_ctrl_buf = self.ik_to_fk_match(**self.right_legs)
                cmds.clearCache(allNodes=1)
                cmds.setKeyframe([poleVector_buf, ik_ctrl_buf, ik_rot_ctrl_buf, ik_end_ctrl_buf], breakdown=0, hierarchy='none', shape=0, controlPoints=0)

            if l_arms:
                # print('left arms {}'.format(str(f)))
                if simplebake:
                    poleVector_buf, ik_ctrl_buf, ik_rot_ctrl_buf, ik_end_ctrl_buf = self.simple_match(**self.left_arms)
                else:
                    poleVector_buf, ik_ctrl_buf, ik_rot_ctrl_buf, ik_end_ctrl_buf = self.ik_to_fk_match(**self.left_arms)
                cmds.clearCache(allNodes=1)
                cmds.setKeyframe([poleVector_buf, ik_ctrl_buf, ik_rot_ctrl_buf, ik_end_ctrl_buf], breakdown=0, hierarchy='none', shape=0, controlPoints=0)

            if r_arms:
                # print('right arms {}'.format(str(f)))
                if simplebake:
                    poleVector_buf, ik_ctrl_buf, ik_rot_ctrl_buf, ik_end_ctrl_buf = self.simple_match(**self.right_arms)
                else:
                    poleVector_buf, ik_ctrl_buf, ik_rot_ctrl_buf, ik_end_ctrl_buf = self.ik_to_fk_match(**self.right_arms)
                cmds.clearCache(allNodes=1)
                cmds.setKeyframe([poleVector_buf, ik_ctrl_buf, ik_rot_ctrl_buf, ik_end_ctrl_buf], breakdown=0, hierarchy='none', shape=0, controlPoints=0)

        cmds.refresh(suspend=False)

        cmds.currentTime(playCur)

        cmds.autoKeyframe(st=autokey_sts)

        cmds.cycleCheck(e=True)

def main():
    app = QApplication.instance()
    ui = GUI()
    ui.show()

if __name__ == '__main__':
    main()
