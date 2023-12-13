# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import re
import glob
import yaml
import collections

import workman_world_custom
from workfile_manager import cmds as  wcmds, p4utils,postproc_utils
from workfile_manager_maya import assetutils_maya
from workfile_manager.plugin_utils import PostProcBase, PluginType, Application

from PySide2 import QtWidgets,QtGui,QtCore 
from PySide2.QtUiTools import QUiLoader
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

#shibokenの読み込み
try :
    import shiboken2 as shiboken
except:
    import shiboken

import pymel.core as pm
import maya.cmds as cmds
import maya.OpenMayaUI as OpenMayaUI

# パスを指定
filePath = os.path.dirname(__file__).replace("\\","/") + "/ui"
UIFILEPATH = filePath+'/workman_checker_tools.ui'
SUBUIFILEPATH = filePath+'/workman_checker_tools_slot.ui'


## WorkmanCheckerToolMainWindowを作るクラス
class WorkmanCheckerToolMainWindow(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    @staticmethod
    def get_maya_window():
        maya_main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
        return shiboken.wrapInstance(int(maya_main_window_ptr), QtWidgets.QWidget)

    @property
    def absolute_name(self):
        return '{}.{}'.format(self.__module__, self.__class__.__name__)
    
    def __init__(self, parent=None):
        super(WorkmanCheckerToolMainWindow, self).__init__(parent)
        self.qs_main = super(WorkmanCheckerToolMainWindow, self)  
        #ウィンドウの重複の回避
        maya_window = WorkmanCheckerToolMainWindow.get_maya_window()
        for child in maya_window.children():
            # reload でポインタが変わったときのために名前で比較する
            if self.absolute_name == child.objectName():
                child.close()
                child.deleteLater()

        self.setObjectName(self.absolute_name)

        # UIのパスを指定
        self.UI = QUiLoader().load(UIFILEPATH)
        # ウィンドウタイトルをUIから取得
        self.setWindowTitle("WorkmanCheckerToolMainWindow")
        # ウィジェットをセンターに配置
        self.setCentralWidget(self.UI)
        
        self.change_state = True
        self.set_defaultsettings_yaml_path()
        self.set_develop_mode()
        
        self.asset = assetutils_maya.ModelAssetMaya()
        self.UI.assetgroup_type_CMBBOX.currentIndexChanged.connect(self.refreshUI)
        self.UI.task_type_CMBBTN.currentIndexChanged.connect(self.refreshUI)
        self.UI.ProcessType_CMBBOX.currentIndexChanged.connect(self.refreshUI)
        self.UI.list_clear_BTN.clicked.connect(self.clear_list)
        self.UI.log_listWidget.itemSelectionChanged.connect(self.log_listWidget_selection_changed)
        self.UI.All_Run_BTN.clicked.connect(self.all_run_process)
        self.UI.export_current_propery_preset_BTN.clicked.connect(self.export_current_propery_preset)
        self.UI.reset_default_settings_BTN.clicked.connect(self.set_default_settings)
        self.UI.develop_CBOX.stateChanged.connect(self.set_develop_mode)
        self.load_ui_settings()
        self.refreshUI()

    def closeEvent(self, event):
        self.qs_main.closeEvent(event)
        self.save_ui_settings()
        self.deleteLater()
        
    def save_ui_settings(self):
        self.export_ui_settings(self.UI.task_type_CMBBTN)
        self.export_ui_settings(self.UI.assetgroup_type_CMBBOX)
        self.export_ui_settings(self.UI.exec_command_TBOX)
        self.export_ui_settings(self.UI.export_path_LEDIT)


    def load_ui_settings(self):
        self.import_ui_settings(self.UI.task_type_CMBBTN)
        self.import_ui_settings(self.UI.assetgroup_type_CMBBOX)
        if self.import_ui_settings(self.UI.exec_command_TBOX) == 0:
            self.UI.exec_command_TBOX.setText('self.args = {}\nself.args["global_args"] = {"selection":cmds.ls()}')

    def refreshUI(self):
        self.change_state = False
        self.initialize_ui()

    def initialize_ui(self):
        self.set_current_assetgroup_type()
        self.set_current_task_type()

        #processtype
        if self.UI.ProcessType_CMBBOX.currentText() == "Preprocess":
            plugin_type = PluginType.PublishPreProcess
        elif self.UI.ProcessType_CMBBOX.currentText() == "Postprocess":
            plugin_type = PluginType.PublishPostProcess
            
        layout = self.UI.verticalLayout_5

        for i in reversed(range(layout.count())):
            if layout.itemAt(i).widget():
                layout.itemAt(i).widget().setParent(None)
            else:
                layout.removeItem(layout.itemAt(i))

        subUIs = []
        for pp,key in postproc_utils.get_all_plugins(plugin_type=plugin_type):
            #print ("skip",pp.apps_executable_on(),key)
            if pp.is_asset_eligible(self.asset) == False:
                continue
            
            if Application.Maya not in pp.apps_executable_on():
                #print ("skip",pp.apps_executable_on(),key)
                continue

            CurrentSlot = WorkmanCheckerToolSubWindow()
            
            CurrentSlot.parent_main = self
            checked = None
            if self.get_usersettings_value(key) != None:
                checked = self.get_usersettings_value(key)
            else:
                try:
                    if self.get_current_defaultsetting()[key] != None:
                        checked = self.get_current_defaultsetting()[key]
                    else:
                        checked = pp.default_checked()
                        CurrentSlot.Is_nothing_default = True
                except:
                    checked = pp.default_checked()
                    CurrentSlot.Is_nothing_default = True
                
            CurrentSlot.UI.ProcessName_CBOX.setChecked(checked)
            CurrentSlot.set_data(pp,key)
            subUIs.append(CurrentSlot)

        subUIs = sorted(subUIs, key=lambda x:x.currentprocess.order())
        for subUI in subUIs:
            layout.addWidget(subUI)
        self.change_state = True

    def set_develop_mode(self):
        checked = self.UI.develop_CBOX.isChecked()
        self.UI.developtool_GBOX.setEnabled(checked)
    
    def set_defaultsettings_yaml_path(self):
        if self.import_ui_settings(self.UI.export_path_LEDIT) == 0:
            # appdata_path = __file__.rsplit("\\",1)[0]
            # default_yaml_path = r"{}\default_checkertool_settings.yaml".format(appdata_path)
            default_yaml_path = r"P:\production\team\environment\config\pipeline\default_checkertool_settings.yaml"
            self.UI.export_path_LEDIT.setText(default_yaml_path)

    def get_defaultsettings_yaml_path(self):  
        # appdata_path = __file__.rsplit("\\",1)[0]
        # default_yaml_path = r"{}\default_checkertool_settings.yaml".format(appdata_path)
        default_yaml_path = str(self.UI.export_path_LEDIT.text())
        return default_yaml_path
    
    def get_usersettings_yaml_path(self):

        appdata_path = os.getenv('APPDATA')
        yaml_path = r"{}\Cygames\Default\workfile_manager\user_checkertool_settings.yaml".format(appdata_path)
        
        if os.path.exists(yaml_path) is False:
            userfile = open(yaml_path, 'w')
            userfile.close()
        
        return yaml_path

    def get_current_defaultsetting(self):
        default_yaml_path = self.get_defaultsettings_yaml_path()
        
        with open(default_yaml_path, 'r') as defaultfile:
            #print('defaultfile>>'+str(defaultfile))
            try:
                #print(default_yaml_path)
                rtn = yaml.safe_load(defaultfile)[self.get_current_task_type().lower()][self.get_current_assetgroup().lower()]
                return rtn
            except:
                return None

    def set_current_assetgroup_type(self):
        current_assetgroup = self.UI.assetgroup_type_CMBBOX.currentText()
        self.asset.assetgroup = current_assetgroup.lower()

    def set_current_task_type(self):
        current_task = self.UI.task_type_CMBBTN.currentText()
        self.asset.task = current_task.lower()

    def addList(self,text,indet=0,color = "white"):
        for i in range(indet):
            text = u"    "+text

        if indet == 0 and text != "" and color is not "gray":
            text = u"■ "+text

        Item = QtWidgets.QListWidgetItem()
        Item.setText(text)

        color = QtGui.QColor(color)
        Item.setTextColor(color)

        self.UI.log_listWidget.addItem(Item)

    def clear_list(self):
        self.UI.log_listWidget.clear()

    def log_listWidget_selection_changed(self):
        items = self.UI.log_listWidget.selectedItems()
        currentTexts = []
        for i in range(len(items)):
            currentTexts.append(str(self.UI.log_listWidget.selectedItems()[i].text()))

        cmds.select(clear=True)
        for currentText in currentTexts:
            if cmds.objExists(currentText):
                cmds.select(currentText,add=True)

    def set_args(self):
        #self.args = {}
        #self.args['global_args'] = {'selection':cmds.ls()}
        exec_command = str(self.UI.exec_command_TBOX.toPlainText())
        exec(exec_command)
        
    def all_run_process(self):
        self.set_args()

        subUIs = []
        for i in range(self.UI.verticalLayout_5.count()):
            subUI = self.UI.verticalLayout_5.itemAt(i).widget()
            subUIs.append(subUI)
        subUIs = sorted(subUIs, key=lambda x:x.currentprocess.order())
        for subUI in subUIs:
            if subUI.UI.ProcessName_CBOX.isChecked():
                try:
                    subUI.run_process()
                    self.addList("")
                except Exception as e:
                    print(u"例外args:", e.args)
                    #cmds.warning(u"実行に必要な設定が足りていない可能性があります。ツールの管理者にご連絡ください")
                    process_name = subUI.get_current_process_label_jp()
                    
                    self.addList(process_name)
                    self.addList(" >> The settings required for execution may not be sufficient. Contact the tool administrator",1,color = "yellow")
                    self.addList("")
                    continue

    def get_usersettings_value(self,key):
        user_yaml_path = self.get_usersettings_yaml_path()
        use_default = False
        rtn = None
        with open(user_yaml_path, 'r') as userfile:
            user_workman_datas = yaml.safe_load(userfile)
            try:
                rtn = user_workman_datas[str(key)]
            except:
                use_default = True
        #user_settingに存在しなかった場合、デフォルトから参照する
        if use_default:
            default_yaml_path = self.get_defaultsettings_yaml_path()
            try:
                with open(default_yaml_path, 'r') as defaultfile:               
                    rtn = default_yaml_path["checktool_ui_settings"][str(key)]
            except:
                rtn = None
        return rtn

    def set_usersettings_value(self,key,value):
        user_yaml_path = self.get_usersettings_yaml_path()
        user_workman_datas = None
        if os.path.exists(user_yaml_path) is False:
            userfile = open(user_yaml_path, 'w')
            userfile.close()

        with open(user_yaml_path, 'r') as userfile:
            user_workman_datas = yaml.safe_load(userfile)
        
        if user_workman_datas == None:
            user_workman_datas = {}

        with open(user_yaml_path, 'w') as userfile:
            user_workman_datas[key] = value
            yaml.dump(user_workman_datas,userfile, default_flow_style=False)


    def update_usersettings(self):
        user_yaml_path = self.get_usersettings_yaml_path()
        workman_datas = {}

        #存在していなければ作成
        if os.path.exists(user_yaml_path) is False:
            userfile = open(user_yaml_path, 'w')
            userfile.close()
        
        #書き込み
        default_workman_datas = self.get_current_defaultsetting()

        with open(user_yaml_path, 'w') as userfile:
            for i in range(self.UI.verticalLayout_5.count()):
                subUI = self.UI.verticalLayout_5.itemAt(i).widget()
                workman_datas[subUI.process_name] = subUI.UI.ProcessName_CBOX.isChecked()
                if workman_datas[subUI.process_name] == default_workman_datas[subUI.process_name]:
                    workman_datas[subUI.process_name] = None

            yaml.dump(workman_datas,userfile, default_flow_style=False)
    def get_current_assetgroup(self):
        return str(self.UI.assetgroup_type_CMBBOX.currentText())
    
    def get_current_task_type(self):
        return str(self.UI.task_type_CMBBTN.currentText())

    def export_current_propery_preset(self):
        def deepupdate(source, overrides):
            for key, value in overrides.iteritems():
                if isinstance(value, collections.Mapping) and value:
                    returned = deepupdate(source.get(key, {}), value)
                    source[key] = returned
                else:
                    source[key] = overrides[key]
            return source

        default_yaml_path = self.get_defaultsettings_yaml_path()
        process_datas = {}
        #存在していなければ作成
        if os.path.exists(default_yaml_path) is False:
            userfile = open(default_yaml_path, 'w')
            userfile.close()

        with open(default_yaml_path, 'r') as userfile:
            user_workman_datas = yaml.safe_load(userfile)
            if user_workman_datas != None:
                process_datas.update(user_workman_datas)

        with open(default_yaml_path, 'w') as userfile:
            for i in range(self.UI.verticalLayout_5.count()):
                subUI = self.UI.verticalLayout_5.itemAt(i).widget()
                deepupdate(process_datas,{self.get_current_task_type():{self.get_current_assetgroup():{subUI.process_name:subUI.UI.ProcessName_CBOX.isChecked()}}})
            yaml.dump(process_datas,userfile, default_flow_style=False)

    def set_default_settings(self):
        for i in range(self.UI.verticalLayout_5.count()):
            subUI = self.UI.verticalLayout_5.itemAt(i).widget()
            subUI.set_default_settings()
    
    def import_ui_settings(self,widget):
        if self.get_usersettings_value(str(widget.objectName())) == None:
            return 0

        if type(widget) == QtWidgets.QComboBox:
            value = self.get_usersettings_value(str(widget.objectName()))
            widget.setCurrentIndex(self.get_usersettings_value(str(widget.objectName())))
            return value

        elif type(widget) == QtWidgets.QTextEdit:
            value = self.get_usersettings_value(str(widget.objectName()))
            widget.setText(value)
            return value
        
        elif type(widget) == QtWidgets.QLineEdit:
            value = self.get_usersettings_value(str(widget.objectName()))
            widget.setText(value)
            return value
        

    def export_ui_settings(self,widget):
        if type(widget) == QtWidgets.QComboBox:
            self.set_usersettings_value(str(widget.objectName()),widget.currentIndex())
        
        elif type(widget) == QtWidgets.QTextEdit:
            self.set_usersettings_value(str(widget.objectName()),str(widget.toPlainText()))
        
        elif type(widget) == QtWidgets.QLineEdit:
            self.set_usersettings_value(str(widget.objectName()),str(widget.text()))
            


class WorkmanCheckerToolSubWindow(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(WorkmanCheckerToolSubWindow, self).__init__(parent)
        self.is_showUIMode = True
        # UIのパスを指定
        self.UI = QUiLoader().load(SUBUIFILEPATH)
        # ウィンドウタイトルをUIから取得
        self.setWindowTitle(self.UI.windowTitle())

        # UIのパスを指定
        self.UI = QUiLoader().load(SUBUIFILEPATH)
        # ウィンドウタイトルをUIから取得
        self.setWindowTitle("workman_checker_tool")
        # ウィジェットをセンターに配置
        self.setCentralWidget(self.UI)
        self.currentprocess = None
        self.process_name   = None
        self.args = {}
        self.Is_nothing_default = False
        self.parent_main= None

        self.UI.Run_BTN.clicked.connect(self.single_run_process)
        
        self.UI.ProcessName_CBOX.stateChanged.connect(self.change_checked_state)
        
    def set_data(self,process,processs_name):
        self.currentprocess = process
        self.process_name = processs_name
        self.UI.ProcessName_CBOX.setText(self.get_current_process_label_jp())
        self.set_checkertool_state_color()
        self.UI.ProcessName_CBOX.setToolTip(self.currentprocess.get_discription())
    
    def deco_run_process(func):
        def wrapper(self,*args, **kwargs):
            color = "gray"
            self.parent_main.addList("------ Start Check Process ------",color=color)
            self.parent_main.addList("")
            func(self,*args, **kwargs)
            self.parent_main.addList("")
            self.parent_main.addList("----- Finished Check Process -----",color=color)
            self.parent_main.addList("")
        return wrapper
    
    @deco_run_process
    def single_run_process(self):
        self.parent_main.set_args()
        self.run_process()
        #self.set_tab("log")

    def run_process(self):
        color = "white"
        result = self.currentprocess.execute(self.parent_main.args)
        if result[0] == False:
            color = "red"

        self.parent_main.addList(self.get_current_process_label_jp(),color=color)
        self.parent_main.addList("result : "+str(result[0]),1,color)
        if result[0] == False:
            for lp in result[1]:
                self.parent_main.addList(lp,2,color)
    def get_current_process_label_jp(self):
        if self.currentprocess.get_label_jp() == None:
            process_name = self.currentprocess.getlabel()
        else:
            process_name = self.currentprocess.get_label_jp()
        
        return process_name

    def get_current_process_label(self):
        process_name = self.currentprocess.getlabel()
        return process_name

    def set_enabled(self,value):
        self.UI.ProcessName_CBOX.setChecked(value)
        return value

    def set_tab(self,tabname = "log"): 
        if tabname == "checker_tool":
            index = 0
        elif tabname == "log":
            index = 1
        self.parent_main.UI.tabWidget.setCurrentIndex(index)
        
    def change_checked_state(self):
        self.update_usersetting()
        self.set_checkertool_state_color()
    
    def set_default_settings(self):
        default_settings = self.parent_main.get_current_defaultsetting()
        self.set_enabled(default_settings[self.process_name])

    def set_checkertool_state_color(self):
        if self.Is_nothing_default == False:
            if self.parent_main.get_usersettings_value(self.process_name) != None:
                self.UI.ProcessName_CBOX.setStyleSheet("color: orange")
            else :
                self.UI.ProcessName_CBOX.setStyleSheet("color: white")
        else:
            self.UI.ProcessName_CBOX.setStyleSheet("color: lightgreen")
            

    def update_usersetting(self):
        if self.parent_main.change_state == False or self.Is_nothing_default == True:
            return 0

        user_yaml_path = self.parent_main.get_usersettings_yaml_path()
        workman_datas = {}

        #存在していなければ作成
        if os.path.exists(user_yaml_path) is False:
            userfile = open(user_yaml_path, 'w')
            userfile.close()
        
        #読み込み
        with open(user_yaml_path,'r') as userfile:
            user_workman_datas = yaml.safe_load(userfile)
        
        default_workman_datas = self.parent_main.get_current_defaultsetting()
        
        with open(user_yaml_path, 'w') as userfile:
            subUI = self
            workman_datas = {}
            if user_workman_datas != None:
                workman_datas = user_workman_datas
            workman_datas[subUI.process_name] = subUI.UI.ProcessName_CBOX.isChecked()
            if workman_datas[subUI.process_name] == default_workman_datas[subUI.process_name]:
                workman_datas.update({subUI.process_name:None})
            if user_workman_datas != None:
                workman_datas.update(user_workman_datas)

            yaml.dump(workman_datas,userfile, default_flow_style=False)

## PhysMatAssighToolMainWindowの起動
def main():
    window = WorkmanCheckerToolMainWindow()
    window.show()

if __name__ == '__main__':
    main()