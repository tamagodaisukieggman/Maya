# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

from maya import cmds, mel
from maya import OpenMayaUI as omui
import maya.api.OpenMaya as om2

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide import __version__
    from shiboken import wrapInstance

from maya.app.general.mayaMixin import MayaQWidgetBaseMixin, MayaQWidgetDockableMixin

import base64
import codecs
import fnmatch
import glob
import json
import math
import os
import pickle
import re
import subprocess
import sys
import time
import traceback

from collections import OrderedDict
from functools import partial
import functools
from imp import reload
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR
from timeit import default_timer as timer

import tkgfile.fbxMixer.commands as fbxMixer
reload(fbxMixer)

maya_version = cmds.about(v=True)

TOOL_VERSION = '1.0.0'
PROJ = 'wizard2'
WINDOW_TITLE = 'FBX Mixer'
WINDOW_OPTIONVAR = WINDOW_TITLE.replace(' ', '_')
try:
    DIR_PATH = '/'.join(__file__.replace('\\', '/').split('/')[0:-1])
except:
    DIR_PATH = ''

"""
import tkgfile.fbxMixer.ui as fbxMixerUI
reload(fbxMixerUI)
fbx_mxui = fbxMixerUI.FBXMixer()
fbx_mxui.buildUI()
fbx_mxui.show(dockable=True)
"""

class FBXMixer(MayaQWidgetDockableMixin, QMainWindow):
    # QMainWindowを継承するとmenubarの使える幅が広い
    def __init__(self, *args, **kwargs):
        super(FBXMixer, self).__init__(*args, **kwargs)

        self.setWindowTitle('{}:{}:{}'.format(WINDOW_TITLE, TOOL_VERSION, PROJ))

        self.ui_items = {}
        self.ui_get_list = []

        self.set_path_dict = {
            'base_fbx':{
                'title':'Set Base Motion FBX',
                'file_mode':'open',
                'file_filter':'FBX Files (*.fbx);;All Files (*.*)'
            },
            'combine_fbx':{
                'title':'Set Combine Motion FBX',
                'file_mode':'open',
                'file_filter':'FBX Files (*.fbx);;All Files (*.*)'
            },
            'extract_fbx':{
                'title':'Set Extract Motion FBX',
                'file_mode':'open',
                'file_filter':'FBX Files (*.fbx);;All Files (*.*)'
            },
            'save_fbx':{
                'title':'Set Save FBX',
                'file_mode':'save',
                'file_filter':'FBX Files (*.fbx);;All Files (*.*)'
            },
        }

        self.hip_poses = {
            'p1':[0, 81.371, 0],
            'p2':[0, 81.371, 0],
            'chr0005_00':[0, 81.371, 0],
            'chr0006_00':[0, 81.371, 0]
        }

        self.set_inits = {
            'p1':'p1_joint_values.json',
            'p2':'p2_joint_values.json',
            'chr0005_00':'chr0005_00_joint_values.json',
            'chr0006_00':'chr0006_00_joint_values.json'
        }

        self.hip_pos = [0, 81.371, 0]
        self.set_init_path = 'p1_joint_values.json'
        self.set_init_qcbx_state = True

        self.history_base_motion = list()
        self.history_combine_motion = list()
        self.history_extract_motion = list()
        self.history_save_motion = list()

    def layout(self):
        # 全体の大きさの変更
        self.setGeometry(10, 10, 500, 100) # (left, top, width, height)

        self.main_widget = QWidget() # 1
        self.setCentralWidget(self.main_widget)

        self.main_qvbl = QVBoxLayout()
        self.main_widget.setLayout(self.main_qvbl) # 2 上下にウィジェットを追加するレイアウトを追加

        self.hip_pos_qhbl = QHBoxLayout()
        self.main_qvbl.addLayout(self.hip_pos_qhbl) # 3 左右にウィジェットを追加するレイアウトを追加

        self.set_init_qhbl = QHBoxLayout()
        self.main_qvbl.addLayout(self.set_init_qhbl) # 3 左右にウィジェットを追加するレイアウトを追加

        self.base_qhbl = QHBoxLayout()
        self.main_qvbl.addLayout(self.base_qhbl) # 3 左右にウィジェットを追加するレイアウトを追加

        self.combine_qhbl = QHBoxLayout()
        self.main_qvbl.addLayout(self.combine_qhbl) # 3 左右にウィジェットを追加するレイアウトを追加

        self.extract_qhbl = QHBoxLayout()
        self.main_qvbl.addLayout(self.extract_qhbl) # 3 左右にウィジェットを追加するレイアウトを追加

        self.save_qhbl = QHBoxLayout()
        self.main_qvbl.addLayout(self.save_qhbl) # 3 左右にウィジェットを追加するレイアウトを追加

        self.dcp_qhbl = QHBoxLayout()
        self.main_qvbl.addLayout(self.dcp_qhbl) # 3 左右にウィジェットを追加するレイアウトを追加

        self.apply_qhbl = QHBoxLayout()
        self.main_qvbl.addLayout(self.apply_qhbl) # 3 左右にウィジェットを追加するレイアウトを追加

    def widgets(self):
        # QLabel
        self.hip_pos_ql = QLabel('Hip Position')
        self.hip_pos_qhbl.addWidget(self.hip_pos_ql)

        self.set_init_qcbx = QCheckBox('Set init translate for Extract')
        self.set_init_qhbl.addWidget(self.set_init_qcbx)
        self.set_init_qcbx.setChecked(True)
        self.set_init_qcbx.stateChanged.connect(self.get_init_extract_state)

        self.base_ql = QLabel('Base Motion')
        self.base_qhbl.addWidget(self.base_ql)
        self.base_ql.setAlignment(Qt.AlignRight)

        self.combine_ql = QLabel('Combine Motion')
        self.combine_qhbl.addWidget(self.combine_ql)
        self.combine_ql.setAlignment(Qt.AlignRight)

        self.extract_ql = QLabel('Extract Motion')
        self.extract_qhbl.addWidget(self.extract_ql)
        self.extract_ql.setAlignment(Qt.AlignRight)

        self.save_ql = QLabel('Save Motion')
        self.save_qhbl.addWidget(self.save_ql)
        self.save_ql.setAlignment(Qt.AlignRight)

        # QLineEdit
        self.hip_pos_qcmbx = QComboBox()
        self.hip_pos_qhbl.addWidget(self.hip_pos_qcmbx)
        self.hip_pos_qcmbx.addItems(self.hip_poses.keys())
        self.hip_pos_qcmbx.currentTextChanged.connect(self.get_hip_pos_from_qcmbx)

        self.set_init_qcmbx = QComboBox()
        self.set_init_qhbl.addWidget(self.set_init_qcmbx)
        self.set_init_qcmbx.addItems(self.set_inits.keys())
        self.set_init_qcmbx.currentTextChanged.connect(self.get_inits_from_qcmbx)

        self.base_qle = QLineEdit('')
        self.base_qhbl.addWidget(self.base_qle)
        self.ui_get_list.append(self.base_qle)

        self.combine_qle = QLineEdit('')
        self.combine_qhbl.addWidget(self.combine_qle)
        self.ui_get_list.append(self.combine_qle)

        self.extract_qle = QLineEdit('')
        self.extract_qhbl.addWidget(self.extract_qle)
        self.ui_get_list.append(self.extract_qle)

        self.save_qle = QLineEdit('')
        self.save_qhbl.addWidget(self.save_qle)
        self.ui_get_list.append(self.save_qle)

        [qle_item.textChanged.connect(self.change_slash_text) for qle_item in self.ui_get_list]

        # QPushButton
        # base motion
        self.base_qbtn = QPushButton('Set')
        self.base_qhbl.addWidget(self.base_qbtn)
        self.base_qbtn.clicked.connect(partial(self.set_path_qle, 'base_fbx', self.base_qle))
        self.base_qbtn.setContextMenuPolicy(Qt.CustomContextMenu) # QTreeViewにコンテキストメニューを追加する設定
        self.base_qbtn.customContextMenuRequested.connect(self.set_path_from_history) # QTreeViewで設定するコンテキストメニュー

        self.base_clear_qbtn = QPushButton('Clear')
        self.base_qhbl.addWidget(self.base_clear_qbtn)
        self.base_clear_qbtn.clicked.connect(partial(self.clear_qle, self.base_qle))

        self.base_import_qbtn = QPushButton('Import')
        self.base_qhbl.addWidget(self.base_import_qbtn)
        self.base_import_qbtn.clicked.connect(partial(self.import_fbx_qle, self.base_qle))

        # combine motion
        self.combine_qbtn = QPushButton('Set')
        self.combine_qhbl.addWidget(self.combine_qbtn)
        self.combine_qbtn.clicked.connect(partial(self.set_path_qle, 'combine_fbx', self.combine_qle))
        self.combine_qbtn.setContextMenuPolicy(Qt.CustomContextMenu) # QTreeViewにコンテキストメニューを追加する設定
        self.combine_qbtn.customContextMenuRequested.connect(self.set_path_from_history) # QTreeViewで設定するコンテキストメニュー

        self.combine_clear_qbtn = QPushButton('Clear')
        self.combine_qhbl.addWidget(self.combine_clear_qbtn)
        self.combine_clear_qbtn.clicked.connect(partial(self.clear_qle, self.combine_qle))

        self.combine_import_qbtn = QPushButton('Import')
        self.combine_qhbl.addWidget(self.combine_import_qbtn)
        self.combine_import_qbtn.clicked.connect(partial(self.import_fbx_qle, self.combine_qle))

        # extrace motion
        self.extract_qbtn = QPushButton('Set')
        self.extract_qhbl.addWidget(self.extract_qbtn)
        self.extract_qbtn.clicked.connect(partial(self.set_path_qle, 'extract_fbx', self.extract_qle))
        self.extract_qbtn.setContextMenuPolicy(Qt.CustomContextMenu) # QTreeViewにコンテキストメニューを追加する設定
        self.extract_qbtn.customContextMenuRequested.connect(self.set_path_from_history) # QTreeViewで設定するコンテキストメニュー

        self.extract_clear_qbtn = QPushButton('Clear')
        self.extract_qhbl.addWidget(self.extract_clear_qbtn)
        self.extract_clear_qbtn.clicked.connect(partial(self.clear_qle, self.extract_qle))

        self.extract_import_qbtn = QPushButton('Import')
        self.extract_qhbl.addWidget(self.extract_import_qbtn)
        self.extract_import_qbtn.clicked.connect(partial(self.import_fbx_qle, self.extract_qle))

        # save motion
        self.save_qbtn = QPushButton('Set')
        self.save_qhbl.addWidget(self.save_qbtn)
        self.save_qbtn.clicked.connect(partial(self.set_path_qle, 'save_fbx', self.save_qle))
        self.save_qbtn.setContextMenuPolicy(Qt.CustomContextMenu) # QTreeViewにコンテキストメニューを追加する設定
        self.save_qbtn.customContextMenuRequested.connect(self.set_path_from_history) # QTreeViewで設定するコンテキストメニュー

        self.save_clear_qbtn = QPushButton('Clear')
        self.save_qhbl.addWidget(self.save_clear_qbtn)
        self.save_clear_qbtn.clicked.connect(partial(self.clear_qle, self.save_qle))

        self.save_import_qbtn = QPushButton('Import')
        self.save_qhbl.addWidget(self.save_import_qbtn)
        self.save_import_qbtn.clicked.connect(partial(self.import_fbx_qle, self.save_qle))

        # apply
        self.extract_apply_qbtn = QPushButton('Extract')
        self.apply_qhbl.addWidget(self.extract_apply_qbtn)
        self.extract_apply_qbtn.clicked.connect(partial(self.extract_apply))

        self.combine_apply_qbtn = QPushButton('Combine')
        self.apply_qhbl.addWidget(self.combine_apply_qbtn)
        self.combine_apply_qbtn.clicked.connect(partial(self.combine_apply))

        self.dcp_extract_ql = QLabel('Extract = Combine Motion - Base Motion')
        self.dcp_qhbl.addWidget(self.dcp_extract_ql)

        self.dcp_combine_ql = QLabel('Combine = Base Motion + Extract Motion')
        self.dcp_qhbl.addWidget(self.dcp_combine_ql)

    def buildUI(self):
        # UI
        self.layout()
        self.widgets()

        # load setting
        self.load_setting()

    def load_setting(self):
        get_load_setting = load_optionVar(key=WINDOW_OPTIONVAR)
        if get_load_setting:
            self.ui_items[WINDOW_OPTIONVAR] = get_load_setting
        else:
            self.ui_items[WINDOW_OPTIONVAR] = OrderedDict()

        if not 'history' in self.ui_items[WINDOW_OPTIONVAR].keys():
            self.ui_items[WINDOW_OPTIONVAR]['history'] = OrderedDict()
            for i, ui_item in enumerate(self.ui_get_list):
                self.ui_items[WINDOW_OPTIONVAR]['history'][str(i).zfill(3)] = list()

        # set items
        try:
            [ui_item.setText(get_load_setting[str(i).zfill(3)]) for i, ui_item in enumerate(self.ui_get_list)]
        except:
            print(traceback.print_exc())

        # history items
        try:
            for i, ui_item in enumerate(self.ui_get_list):
                if i == 0:
                    self.history_base_motion = self.ui_items[WINDOW_OPTIONVAR]['history'][str(i).zfill(3)]
                elif i == 1:
                    self.history_combine_motion = self.ui_items[WINDOW_OPTIONVAR]['history'][str(i).zfill(3)]
                elif i == 2:
                    self.history_extract_motion = self.ui_items[WINDOW_OPTIONVAR]['history'][str(i).zfill(3)]
                elif i == 3:
                    self.history_save_motion = self.ui_items[WINDOW_OPTIONVAR]['history'][str(i).zfill(3)]
        except:
            print(traceback.print_exc())

    def save_setting(self):
        save_optionVar(self.ui_items)

    def get_ui_items(func):
        def wrapper(*args, **kwargs):
            values = func(*args, **kwargs)
            for i, ui_item in enumerate(args[0].ui_get_list):
                args[0].ui_items[WINDOW_OPTIONVAR][str(i).zfill(3)] = ui_item.text()
                if ui_item.text():
                    if not ui_item.text() in args[0].ui_items[WINDOW_OPTIONVAR]['history'][str(i).zfill(3)]:
                        args[0].ui_items[WINDOW_OPTIONVAR]['history'][str(i).zfill(3)].append(ui_item.text())
            args[0].save_setting()
            return values
        return wrapper

    def check_save_file(func):
        def wrapper(*args, **kwargs):
            save_path = args[0].save_qle.text()
            if os.path.isfile(save_path):
                message = '{} already exists.\nDo you want to replace it?'.format(os.path.basename(save_path))
                qmessage_info = QMessageBox.warning(None, u"Save As", message, QMessageBox.Yes, QMessageBox.No)
                if qmessage_info == QMessageBox.Yes:
                    func(*args, **kwargs)
                elif qmessage_info == QMessageBox.No:
                    return
            else:
                func(*args, **kwargs)
        return wrapper

    @get_ui_items
    @check_save_file
    def extract_apply(self):
        check_files = [self.base_qle.text(), self.combine_qle.text()]
        for i, cf in enumerate(check_files):
            if i == 0:
                text = 'Base Motion'
            elif i == 1:
                text = 'Combine Motion'
            if not os.path.isfile(cf):
                print('{}: {} not found.'.format(text, cf))
                return

        if not self.set_init_qcbx_state:
            self.set_init_path = False

        cmds.file(new=True, f=True)
        fbxMixer.extract_fbx_(
            self.combine_qle.text(),
            self.base_qle.text(),
            self.hip_pos,
            self.save_qle.text(),
            self.set_init_path
        )

    @get_ui_items
    @check_save_file
    def combine_apply(self):
        check_files = [self.base_qle.text(), self.extract_qle.text()]
        for i, cf in enumerate(check_files):
            if i == 0:
                text = 'Base Motion'
            elif i == 1:
                text = 'Extract Motion'
            if not os.path.isfile(cf):
                print('{}: {} not found.'.format(text, cf))
                return

        cmds.file(new=True, f=True)
        fbxMixer.combine_fbx_(
            self.base_qle.text(),
            self.extract_qle.text(),
            self.save_qle.text()
        )

    @get_ui_items
    def set_path_qle(self, file_type=None, qle=None):
        settings = self.set_path_dict[file_type]
        file_path = self.file_dialog(**settings)
        if file_path:
            qle.setText(file_path[0])

    def set_path_qle_from_history(self, qle=None, text=None):
        qle.setText(text)

    def set_path_from_history(self, pos):
        sender = self.sender()
        # menus
        self.context_menu = QMenu(sender)

        # self.history_base_motion = list()
        # self.history_combine_motion = list()
        # self.history_extract_motion = list()
        # self.history_save_motion = list()

        # addAction
        context_menu = OrderedDict()

        if self.base_qbtn == sender:
            for base_motion in self.history_base_motion:
                context_menu[base_motion] = {'cmd':partial(self.set_path_qle_from_history, self.base_qle, base_motion)}
        elif self.combine_qbtn == sender:
            for base_motion in self.history_combine_motion:
                context_menu[base_motion] = {'cmd':partial(self.set_path_qle_from_history, self.combine_qle, base_motion)}
        elif self.extract_qbtn == sender:
            for base_motion in self.history_extract_motion:
                context_menu[base_motion] = {'cmd':partial(self.set_path_qle_from_history, self.extract_qle, base_motion)}
        elif self.save_qbtn == sender:
            for base_motion in self.history_save_motion:
                context_menu[base_motion] = {'cmd':partial(self.set_path_qle_from_history, self.save_qle, base_motion)}

        for menu_name, menu_cmd in context_menu.items():
            action = self.context_menu.addAction(menu_name)
            action.triggered.connect(menu_cmd['cmd'])

        # QMenuの表示
        self.context_menu.exec_(sender.mapToGlobal(pos))

    @get_ui_items
    def import_fbx_qle(self, qle=None):
        fbxMixer.import_fbx(qle.text(), nss=':', new_scene=None)

    def change_slash_text(self):
        sender = self.sender()
        item_text = sender.text()
        if os.sep in item_text:
            replaced_text = item_text.replace(os.sep,'/')
            sender.setText(replaced_text)

    def clear_qle(self, qle=None):
        qle.clear()

    def get_hip_pos_from_qcmbx(self):
        sender = self.sender()
        self.hip_pos = self.hip_poses[sender.currentText()]

    def get_inits_from_qcmbx(self):
        sender = self.sender()
        self.set_init_path = self.set_inits[sender.currentText()]

    def get_init_extract_state(self):
        sender = self.sender()
        if sender.isChecked():
            self.set_init_qcbx_state = True
        else:
            self.set_init_qcbx_state = False

    def file_dialog(self, title=None, file_mode=None, file_filter='Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;All Files (*.*)'):
        u"""
        title = 'test'
        file_filter = 'FBX Files (*.fbx);;All Files (*.*)'
        """

        if file_mode == 'open':
            fm = 4
        elif file_mode == 'save':
            fm = 0
        elif file_mode == 'set':
            fm = 2

        files = cmds.fileDialog2(
            ff=file_filter,
            ds=1,
            okc='OK',
            cc='Cancel',
            fm=fm,
            cap=title,
        )

        if files:
            if fm == 2:
                return files[0]
            else:
                return files


def load_optionVar(key=None):
    return eval(cmds.optionVar(q=key)) if cmds.optionVar(ex=key) else False

def save_optionVar(ui_items=None):
    for key, value in ui_items.items():
        cmds.optionVar(sv=[key, str(value)])

def get_time_slider():
    min_time = cmds.playbackOptions(q=True, min=True)
    max_time = cmds.playbackOptions(q=True, max=True)
    start_time = cmds.playbackOptions(q=True, ast=True)
    end_time = cmds.playbackOptions(q=True, aet=True)
    return min_time, max_time, start_time, end_time

def set_time_from_key(range_type=None):
    min_time, max_time, start_time, end_time = get_time_slider()

    sel = cmds.ls(os=True)
    if not sel: return min_time, max_time, start_time, end_time
    selected_frame_range = cmds.keyframe(sel[0], q=True)

    fcurve_frame_range = cmds.keyframe(q=True)
    if len(fcurve_frame_range) > 1:
        cmds.playbackOptions(
            min=fcurve_frame_range[0],
            max=fcurve_frame_range[-1]
        )

    else:
        if range_type == 'min':
            cmds.playbackOptions(
                min=fcurve_frame_range[0],
            )
        elif range_type == 'max':
            cmds.playbackOptions(
                max=fcurve_frame_range[0],
            )

    return min_time, max_time, start_time, end_time

def set_time_slider(range_type='both'):
    min_time, max_time, start_time, end_time = get_time_slider()

    if range_type == 'both':
        cmds.playbackOptions(ast=min_time)
        cmds.playbackOptions(aet=max_time)
    elif range_type == 'start':
        cmds.playbackOptions(ast=min_time)
    elif range_type == 'end':
        cmds.playbackOptions(aet=max_time)

def replace_square_brackets(text=None):
    return text.replace('[', '').replace(']', '')


if __name__ == '__main__':
    ui = FBXMixer()
    ui.buildUI()
    ui.show(dockable=True)
