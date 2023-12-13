# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import

u"""
name: autocreate_rig/ui.py
data: 2021/10/18
ussage: priari 用 Rig 自動作成ツール UI
version: 2.72
​
"""
try:
    # Maya 2022-
    from builtins import range
    from importlib import reload
except:
    pass

import imp
import logging
from PySide2 import QtWidgets, QtGui, QtCore
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
import re
import maya.cmds as cmds
import pymel.core as pm
from . import command
from . import fix_joint
from . import check
reload(command)
reload(fix_joint)
reload(check)
Check = check.Check

logger = logging.getLogger(__name__)
TOOL_NAME = 'autocreate_rig'
TOOL_VERSION = 'Ver 2.72'
TOOL_TITLE = 'AutoCreate Rig' + '   ' + TOOL_VERSION

QLINE_SS_DICT = {}
QLINE_SS_DICT["default"] = 'QLineEdit { color: rgb(255, 255, 255);background-color: rgb(128, 128, 128);}'
QLINE_SS_DICT["good"] = 'QLineEdit { color: rgb(255, 255, 255);background-color: rgb(0, 128, 128);}'
QLINE_SS_DICT["error"] = 'QLineEdit { color: rgb(255, 255, 255);background-color: rgb(75, 0, 0);}'
# 命名規則数字桁数の変更の可能性がある為、先頭文字列の判定のみ v2.1~: avt追加
ID_PATTERN = r"(mdl)_(unt|wpn|prp|avt)_.*"
ID_PATTERN_WPN = r"(mdl)_(wpn|prp)_.*"


def get_maya_win():
    u"""
    Mayaのメインウィンドウを取得する関数
    """
    try:
        from maya import OpenMayaUI

    except ImportError:
        return None

    try:
        imp.find_module("shiboken2")
        import shiboken2
        return shiboken2.wrapInstance(long(OpenMayaUI.MQtUtil.mainWindow()), QtWidgets.QWidget)

    except ImportError:
        import shiboken
        return shiboken.wrapInstance(long(OpenMayaUI.MQtUtil.mainWindow()), QtWidgets.QWidget)


class AutoCreateRigUI(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(AutoCreateRigUI, self).__init__(parent)

        self.setObjectName(TOOL_NAME)
        self.setWindowTitle(TOOL_TITLE)
        self.ex_sik_list = []
        self.ex_fk_list = []
        self.ex_dict = {}
        self._initUI()
        self.target_group = None
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        # self.job_id = cmds.scriptJob(event=["SelectionChanged", self.selectchanged], protected=True)
        self.selectchanged()

    def selectchanged(self):
        sel = []
        try:
            sel = cmds.ls(sl=True, type="transform")

        except Exception as e:
            print(("error: ", e))

        if len(sel) == 1:

            is_topnode = True if not cmds.listRelatives(sel, p=True) else False
            is_null = True if cmds.listRelatives(sel, type="shape") is None else False
            is_correct_id = True if re.match(ID_PATTERN, sel[0]) else False
            is_wpn_id = True if re.match(ID_PATTERN_WPN, sel[0]) else False
            # print(sel[0], is_topnode, is_null, is_correct_id)

            if is_topnode and is_null and is_correct_id:
                self.target_group = sel[0]
                print('Selected_Group : {}'.format(self.target_group))
                grp_rig_name = 'grp_rig'
                rig_exists = False

                # reference or not
                if cmds.referenceQuery(self.target_group, isNodeReferenced=True):
                    # ref_file = cmds.referenceQuery(self.target_group, f=True)
                    # cmds.referenceQuery(self.target_group, nodes=True)
                    # namespace = cmds.referenceQuery(ref_file, referenceNode=True)
                    # grp_rig = '{}grp_rig'.format(namespace.replace("RN", ":"))
                    grp_rig_pynode = pm.PyNode(self.target_group)
                    rig_exists = command.get_pynode(grp_rig_pynode, grp_rig_name)
                else:
                    rig_exists = fix_joint.check_grp_node(self.target_group, grp_rig_name)

                if not rig_exists:
                    self.selitem_textline.setText('{}'.format(self.target_group))
                    self.selitem_textline.setStyleSheet(QLINE_SS_DICT["good"])
                    if not is_wpn_id:
                        # command.check_fix_name()
                        self.get_ex_joint()
                    # print("debug: {}".format(sel))
                else:
                    self.selitem_textline.setText('{} : Aready "grp_rig" Exists'.format(self.target_group))
                    self.selitem_textline.setStyleSheet(QLINE_SS_DICT["error"])

            else:
                self.selitem_textline.setText('{} : Not Top Group of Null or invalid Name'.format(sel[0]))
                self.selitem_textline.setStyleSheet(QLINE_SS_DICT["error"])
                self.get_ex_joint()

        elif len(sel) > 1:
            self.selitem_textline.setText('Muliti Selection > Select Single Group ')
            self.selitem_textline.setStyleSheet(QLINE_SS_DICT["error"])
            self.get_ex_joint()

        else:
            self.selitem_textline.setText('No Selection Group')
            self.selitem_textline.setStyleSheet(QLINE_SS_DICT["error"])
            self.get_ex_joint()

    def _initUI(self):
        widget = QtWidgets.QWidget()
        mainLayout = QtWidgets.QVBoxLayout()
        buttonLayout = QtWidgets.QHBoxLayout()
        createLayout = QtWidgets.QHBoxLayout()
        size_layout = QtWidgets.QHBoxLayout()

        self.setCentralWidget(widget)
        # self.fix_size_button = QtWidgets.QPushButton(u" Fix Size ")
        # self.fix_size_button.clicked.connect(self.fix_size)

        # self.fix_joint_button = QtWidgets.QPushButton(u" Fix Joint ")
        # self.fix_joint_button.clicked.connect(self.fix_joint)

        self.create_wpn_button = QtWidgets.QPushButton(u" Create Wpn Rig ")
        self.create_wpn_button.clicked.connect(self.create_wpn_rig)

        # self.get_button = QtWidgets.QPushButton(u" List Up EX ")
        # self.get_button.clicked.connect(self.get_ex_joint)

        self.sik_label = QtWidgets.QLabel(' - SplineIK Can Be Created - ')
        self.ex_sik_list_widget = QtWidgets.QListWidget()
        self.ex_sik_list_widget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        sub_button_color = "background-color: rgb(95, 95, 95)"

        # self.fk_label = QtWidgets.QLabel('Unable To Create SplineIK')
        # self.ex_fk_list_widget = QtWidgets.QListWidget()
        # self.ex_fk_list_widget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

        self.create_button = QtWidgets.QPushButton(u" Fix Joint + AutoCreate Rig ")
        self.create_button.clicked.connect(self.create_rig)
        self.delete_button = QtWidgets.QPushButton(u" Delete Rig ")
        self.delete_button.clicked.connect(self.delete_rig)
        self.delete_button.setStyleSheet(sub_button_color)

        '''
        self.add_sim_attr_button = QtWidgets.QPushButton(u" Add SIM Attribute (only joints) ")
        self.add_sim_attr_button.clicked.connect(self.add_sim_attributes)
        self.delete_sim_attr_button = QtWidgets.QPushButton(u" Delete SIM Attribute")
        self.delete_sim_attr_button.clicked.connect(self.remove_sim_attributes)'''

        self.size_radioGroup = QtWidgets.QButtonGroup()
        self.xs_rBtn = QtWidgets.QRadioButton("XS")
        self.size_radioGroup.addButton(self.xs_rBtn)
        self.s_rBtn = QtWidgets.QRadioButton("S")
        self.size_radioGroup.addButton(self.s_rBtn)
        self.m_rBtn = QtWidgets.QRadioButton("M")
        self.size_radioGroup.addButton(self.m_rBtn)
        self.l_rBtn = QtWidgets.QRadioButton("L")
        self.size_radioGroup.addButton(self.l_rBtn)

        self.m_rBtn.setChecked(True)

        self.sel_label = QtWidgets.QLabel(' - Selected Group -')
        self.selitem_textline = QtWidgets.QLineEdit('....')
        self.selitem_textline.setReadOnly(True)
        self.selitem_textline.setStyleSheet(QLINE_SS_DICT["default"])
        self.create_label = QtWidgets.QLabel(' - Create -')
        self.option_label = QtWidgets.QLabel(' - Option -')
        self.extra_label = QtWidgets.QLabel(' - Extra Attribute -')

        # SplineIK の チェックボックス
        self.ex_check = QtWidgets.QCheckBox("Create SplineIK For EX Node")
        self.ex_check.setChecked(False)

        self.t_ctrl_button = QtWidgets.QPushButton(u" Translate CTRL Select ")
        self.t_ctrl_button.clicked.connect(self.t_ctrl_selection)
        self.t_ctrl_button.setStyleSheet('background-color: {};'.format(sub_button_color))

        self.r_ctrl_button = QtWidgets.QPushButton(u" Rotate CTRL Select ")
        self.r_ctrl_button.clicked.connect(self.r_ctrl_selection)
        self.r_ctrl_button.setStyleSheet('background-color: {};'.format(sub_button_color))

        self.reset_ctrl_button = QtWidgets.QPushButton(u" Reset CTRL Pose ")
        self.reset_ctrl_button.clicked.connect(self.reset_rig)
        self.reset_ctrl_button.setStyleSheet('background-color: {};'.format(sub_button_color))

        self.separator = QtWidgets.QFrame()
        self.separator.setFrameShape(QtWidgets.QFrame.HLine)
        self.separator.setFrameShadow(QtWidgets.QFrame.Sunken)

        buttonLayout.addWidget(self.t_ctrl_button)
        buttonLayout.addWidget(self.r_ctrl_button)

        createLayout.addWidget(self.create_button)
        createLayout.addWidget(self.create_wpn_button)

        size_layout.addWidget(self.xs_rBtn)
        size_layout.addWidget(self.s_rBtn)
        size_layout.addWidget(self.m_rBtn)
        size_layout.addWidget(self.l_rBtn)

        # mainLayout.addWidget(self.fix_label)
        # mainLayout.addWidget(self.fix_joint_button)
        mainLayout.addWidget(self.sel_label)
        mainLayout.addWidget(self.selitem_textline)
        # mainLayout.addWidget(self.fix_size_button)
        # mainLayout.addWidget(self.create_wpn_button)
        # mainLayout.addWidget(self.get_button)
        mainLayout.addWidget(self.sik_label)
        mainLayout.addWidget(self.ex_sik_list_widget)
        # mainLayout.addWidget(self.fk_label)
        # mainLayout.addWidget(self.ex_fk_list_widget)
        # mainLayout.addLayout(size_layout)
        # mainLayout.addWidget(self.ex_check)
        # mainLayout.addWidget(self.create_button)
        mainLayout.addWidget(self.create_label)
        mainLayout.addLayout(createLayout)
        mainLayout.addWidget(self.separator)
        mainLayout.addWidget(self.option_label)
        mainLayout.addWidget(self.delete_button)
        mainLayout.addLayout(buttonLayout)
        mainLayout.addWidget(self.reset_ctrl_button)
        ''' SIM Attribute　操作が必要な場合
        mainLayout.addWidget(self.extra_label)
        mainLayout.addWidget(self.add_sim_attr_button)
        mainLayout.addWidget(self.delete_sim_attr_button)'''
        widget.setLayout(mainLayout)

    def closeEvent(self, event):
        print("Close UI: {}".format(TOOL_TITLE))
        # cmds.scriptJob(kill=self.job_id, force=True)
        # super( MainWindow, self ).closeEvent( event )

    def fix_size(self):
        if command.topnode_check():
            fix = fix_joint.fix_size_main()
            if fix:
                self.comp_dialog(w_text='Fix Size が完了しました。')

    def create_wpn_rig(self):

        comp, error_list = command.wpn_main()
        print((comp, error_list))
        self.msg_dialog(error_list, success=comp)

    def get_ex_joint(self):

        self.ex_sik_list_widget.clear()
        self.ex_dict = command.get_main()

        self.ex_sik_list = [k for k, v in list(self.ex_dict.items()) if v["sik"]]
        self.ex_fk_list = [k for k, v in list(self.ex_dict.items()) if not v["sik"]]

        if self.ex_sik_list:
            self.ex_sik_list_widget.addItems(self.ex_sik_list)

        self.ex_fk_list = command.get_main(target = 'fk')
        if self.ex_fk_list:
            self.ex_sik_list_widget.addItems(self.ex_fk_list)

        if self.ex_sik_list_widget.count() > 0:
            for i in range(self.ex_sik_list_widget.count()):
                item = self.ex_sik_list_widget.item(i)

                if item.text() in self.ex_sik_list:
                    self.ex_sik_list_widget.setItemSelected(item, True)
                    item.setForeground(QtGui.QColor('lightGray'))
                else:
                    item.setSelected(False)
                    item.setForeground(QtGui.QColor('orange'))
        '''
        self.ex_sik_list = command.get_main(target='sik')
        
        # print("self.ex_sik_list:", self.ex_sik_list)
        if self.ex_sik_list:
            self.ex_sik_list_widget.addItems(self.ex_sik_list)

        self.ex_fk_list = command.get_main(target='fk')
        # print("self.ex_fk_list:", self.ex_fk_list)
        if self.ex_fk_list:
            self.ex_sik_list_widget.addItems(self.ex_fk_list)

        if self.ex_sik_list_widget.count() > 0:
            for i in range(self.ex_sik_list_widget.count()):
                item = self.ex_sik_list_widget.item(i)

                if item.text() in self.ex_sik_list:
                    self.ex_sik_list_widget.setItemSelected(item, True)
                    item.setForeground(QtGui.QColor('lightGray'))
                else:
                    item.setSelected(False)
                    item.setForeground(QtGui.QColor('orange'))'''

    def create_rig(self):
        # ex_sik = []

        if self.ex_sik_list_widget.count() > 0:
            for i in range(self.ex_sik_list_widget.count()):
                item = self.ex_sik_list_widget.item(i)
                if item.isSelected() and self.ex_dict.get(item.text()):
                    self.ex_dict[item.text()]["sik"] = True
                else:
                    self.ex_dict[item.text()]["sik"] = False
                '''if item.isSelected() and item.text() in self.ex_sik_list:
                    ex_sik.append(item.text())'''

        ex_s_flag = True

        if not ex_s_flag:
            ex_dict = {}

        comp, error_list = command.main(ex_s_flag, self.ex_dict)
        print((comp, error_list))
        self.msg_dialog(error_list, success=comp)

    def delete_rig(self):
        if Check.delete():
            self.msgbox = QtWidgets.QMessageBox
            msgBox = self.msgbox(self)
            msgBox.setWindowTitle(u"Delete Rig")
            msgBox.setText(u"Rig を削除しますか？")
            msgBox.setIcon(self.msgbox.Question)

            # ボタンの追加
            delButton = msgBox.addButton(u"削除", self.msgbox.ActionRole)
            # cancelButton = msgBox.addButton(u"キャンセル", self.msgbox.ActionRole)
            msgBox.exec_()

            # 削除 ボタンを押したとき
            if msgBox.clickedButton() == delButton:
                if command.delete_main():
                    logger.info(u'Rig を削除しました。')
                    self.selectchanged()
                else:
                    logger.warning(u'Rig を削除できませんでした。')

        else:
            logger.warning(u'Rig 関連ノードがありません。')

    def t_ctrl_selection(self):
        if self.target_group:
            command.select_ctrl_main(grp=self.target_group, pos=True, rot=False)
        else:
            command.select_ctrl_main(pos=True, rot=False)

    def r_ctrl_selection(self):
        if self.target_group:
            command.select_ctrl_main(grp=self.target_group, pos=False, rot=True)
        else:
            command.select_ctrl_main(pos=True, rot=False)

    def reset_rig(self):
        if self.target_group:
            command.reset_main(grp=self.target_group)
        else:
            command.reset_main()
        logger.info(u'コントローラーの移動値、回転値をリセットしました。')

    def msg_dialog(self, msg_list=[], success=None):

        self.msgbox = QtWidgets.QMessageBox
        msgbox = self.msgbox(self)
        msgbox.setWindowTitle('Dialog')
        inf_text = r"="*32
        detail_text = ""

        if success:
            msg_type = msgbox.Information
            inf_text += u"正常にRigが作成されました。"
            text = u" AutoCreateRig: Success "
            ok_button = msgbox.addButton(u"OK", self.msgbox.ActionRole)

        else:
            msg_type = msgbox.Warning
            inf_text += u"\nError Count: {}\n詳細を確認してください。".format(len(msg_list))
            text = u" AutoCreateRig: Failed"
            ok_button = msgbox.addButton(u"OK", self.msgbox.ActionRole)
            for i, msg in enumerate(msg_list):
                print((i, msg[1]))
                detail_text += u"{}: {} {}\n".format(i + 1, msg[0], msg[1])

        msgbox.setDetailedText(detail_text)
        msgbox.setIcon(msg_type)
        msgbox.setText(text)
        msgbox.setInformativeText(inf_text)

        if msgbox.clickedButton() == ok_button:
            return True

        msgbox.exec_()


def main():
    '''連続起動でscriptjobに不具合があるのでコメントアウト
    for widget in QtWidgets.QApplication.topLevelWidgets():
        if widget.windowTitle() == TOOL_TITLE:
            widget.deleteLater()'''

    if cmds.window(TOOL_NAME, ex=True):
        cmds.deleteUI(TOOL_NAME)

    # maya_win = get_maya_win()
    window = AutoCreateRigUI()
    # set scriptjob whili window exists
    job_id = cmds.scriptJob(event=["SelectionChanged", window.selectchanged], protected=True, p=window.objectName())
    print("scriptJob ID: {}".format(job_id))
    window.show()
