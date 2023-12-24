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
    from PySide2.QtMultimedia import *
    from PySide2.QtMultimediaWidgets import *
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
from imp import reload
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR
from timeit import default_timer as timer

# import tkgrig.picker.mgpicker_commands as wiz2PickCmd
# reload(wiz2PickCmd)

"""
import tkgrig.picker.ui as wiz2PickUi
reload(wiz2PickUi)
ui = wiz2PickUi.PickerAnimTools()
ui.buildUI()
ui.show(dockable=True)
"""

maya_version = cmds.about(v=True)

TOOL_VERSION = '1.0.0'
PROJ = ''
WINDOW_TITLE = 'Picker Anim Tools'
WINDOW_OPTIONVAR = WINDOW_TITLE.replace(' ', '_')
try:
    DIR_PATH = '/'.join(__file__.replace('\\', '/').split('/')[0:-1])
except:
    DIR_PATH = ''

# WIDTH_ = 650
# HEIGHT_ = 600
# VIEW_SIZE = [-WIDTH_/2, -HEIGHT_/2, WIDTH_, HEIGHT_]

class PickerAnimTools(MayaQWidgetDockableMixin, QMainWindow):
    # QMainWindowを継承するとmenubarの使える幅が広い
    def __init__(self, *args, **kwargs):
        super(PickerAnimTools, self).__init__(*args, **kwargs)

        self.time_range = list()

        self.setWindowTitle('{}:{}:{}'.format(WINDOW_TITLE, TOOL_VERSION, PROJ))

        self.nss = ''
        self.SETTINGLIST_VIS_STATE = None

        self.view = None

        self.resize(650, 600)

        self.set_path_dict = {
            'import_picker':{
                'title':'Import Picker File',
                'file_mode':'open',
                'file_filter':'Picker Files (*.json);;All Files (*.*)'
            },
            'export_picker':{
                'title':'Export Picker File',
                'file_mode':'save',
                'file_filter':'Picker Files (*.json);;All Files (*.*)'
            }
        }


    ############################
    # widgets
    ############################
    def layout(self):
        widget = QWidget(self)
        h_layout = QHBoxLayout(self)

        self.v_layout = QVBoxLayout(self)
        h_layout.addLayout(self.v_layout)

        widget.setLayout(h_layout)

        # item list
        self.items_tree_view = QTreeView(self)
        self.items_tree_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.items_tree_view.setSortingEnabled(True) # QTreeVeiwでsortをONにする
        self.items_tree_view.setGeometry(300, -250, 500, 500)
        self.v_layout.addWidget(self.items_tree_view)

        self.items_tree_view.setContextMenuPolicy(Qt.CustomContextMenu) # QTreeViewにコンテキストメニューを追加する設定
        self.items_tree_view.customContextMenuRequested.connect(self.tree_options_context_menu) # QTreeViewで設定するコンテキストメニュー

        # model
        self.items_model = QStandardItemModel()
        self.items_model.setColumnCount(1)
        self.items_model.setHeaderData(0, Qt.Horizontal, 'Items')
        self.items_tree_view.setModel(self.items_model)

        self.items_tree_view.selectionModel().selectionChanged.connect(self.create_setting_view)

        # settings
        self.setting_widget = SettingWidget(self)
        self.v_layout.addWidget(self.setting_widget)

        # view
        self.view = GraphicsView(self)
        self.scene = self.view.scene
        h_layout.addWidget(self.view)
        self.setCentralWidget(widget)
        self.view.updateCenter()

        self.setting_widget.view = self.view
        self.setting_widget.scene = self.scene
        self.setting_widget.items_tree_view = self.items_tree_view
        self.setting_widget.items_model = self.items_model

        # #################
        # # Alpha
        # #################
        # self.alpha_sdr = QSlider(Qt.Horizontal)
        # self.alpha_sdr.setRange(10,100)
        # self.alpha_sdr.setValue(100)
        # self.alpha_sdr.valueChanged.connect(self.change_ui_opacity)
        # self.alpha_sdr.setGeometry(-250, -300, 180, 35)
        # self.scene.addWidget(self.alpha_sdr)

        # # #################
        # # # Tool Options
        # # #################
        # self.set_picker_winops_btn = QPushButton('Window Options')
        # self.set_picker_winops_btn.clicked.connect(partial(self.set_namespace))
        # self.set_picker_winops_btn.setGeometry(-20, -300, 180, 35)
        # self.set_picker_winops_btn.setStyleSheet(
        #     "background-color: brown;"
        #     "selection-background-color: blue;"
        # )
        # self.scene_toolops_btn = self.scene.addWidget(self.set_picker_winops_btn)
        #
        # self.set_picker_winops_btn.setContextMenuPolicy(Qt.CustomContextMenu) # QTreeViewにコンテキストメニューを追加する設定
        # self.set_picker_winops_btn.customContextMenuRequested.connect(self.window_options_context_menu) # QTreeViewで設定するコンテキストメニュー

        # #################
        # # Namespace
        # #################
        self.set_picker_namespace_btn = QPushButton('Set Picker Namespace')
        self.set_picker_namespace_btn.clicked.connect(partial(self.set_namespace))
        self.set_picker_namespace_btn.setGeometry(-325, -100, 180, 35)
        self.set_picker_namespace_btn.setStyleSheet(
            "background-color: goldenrod;"
            "selection-background-color: blue;"
        )
        self.scene_namespace_btn = self.scene.addWidget(self.set_picker_namespace_btn)

        # # Set Namespace Qle
        self.set_picker_namespace_qle = QLineEdit()
        self.set_picker_namespace_qle.move(-135, -100)
        self.view.nss_qle = self.set_picker_namespace_qle
        self.scene_namespace_qle = self.scene.addWidget(self.set_picker_namespace_qle)

        # # Select All
        # self.set_picker_select_all_btn = QPushButton('Select All')
        # self.set_picker_select_all_btn.clicked.connect(partial(self._select_all))
        # self.set_picker_select_all_btn.setGeometry(195, -240, 120, 30)
        # self.scene_select_all_btn = self.scene.addWidget(self.set_picker_select_all_btn)
        #
        # # Bake
        # self.set_picker_bake_btn = QPushButton('Full Bake Selection')
        # self.set_picker_bake_btn.clicked.connect(partial(self._fullbake))
        # self.set_picker_bake_btn.setGeometry(195, -200, 120, 30)
        # self.scene_bake_btn = self.scene.addWidget(self.set_picker_bake_btn)
        #
        # # Zero out
        # self.set_picker_zero_btn = QPushButton('Zero out')
        # self.set_picker_zero_btn.clicked.connect(partial(self._force_zero_out))
        # self.set_picker_zero_btn.setGeometry(195, -160, 120, 30)
        # self.scene_zero_btn = self.scene.addWidget(self.set_picker_zero_btn)
        #
        # # Go to bindPose
        # self.set_picker_bindpose_btn = QPushButton('Go to bindPose')
        # self.set_picker_bindpose_btn.clicked.connect(partial(self._go_to_bindPose_for_rig))
        # self.set_picker_bindpose_btn.setGeometry(195, -120, 120, 30)
        # self.scene_bindpose_btn = self.scene.addWidget(self.set_picker_bindpose_btn)

        # # #################
        # # # Tools
        # # #################
        # # Delete Constraints
        # self.set_picker_delcon_btn = QPushButton('DelCon')
        # self.set_picker_delcon_btn.setStyleSheet(
        #     "background-color: MediumPurple;"
        #     "selection-background-color: black;"
        # )
        # self.set_picker_delcon_btn.setToolTip(u'<font color=white>右クリックでメニューを表示します。</font>')
        # self.set_picker_delcon_btn.setGeometry(-325, -160, 50, 30)
        # self.set_picker_delcon_btn.setContextMenuPolicy(Qt.CustomContextMenu) # QTreeViewにコンテキストメニューを追加する設定
        # self.set_picker_delcon_btn.customContextMenuRequested.connect(self.del_cons_context_menu) # QTreeViewで設定するコンテキストメニュー
        # self.scene_delcon_btn = self.scene.addWidget(self.set_picker_delcon_btn)
        #
        # # Tools
        # self.set_picker_tools_btn = QPushButton('Tools')
        # self.set_picker_tools_btn.setStyleSheet(
        #     "background-color: MediumPurple;"
        #     "selection-background-color: black;"
        # )
        # self.set_picker_tools_btn.setToolTip(u'<font color=white>右クリックでメニューを表示します。</font>')
        # self.set_picker_tools_btn.setGeometry(-325, -200, 50, 30)
        # self.set_picker_tools_btn.setContextMenuPolicy(Qt.CustomContextMenu) # QTreeViewにコンテキストメニューを追加する設定
        # self.set_picker_tools_btn.customContextMenuRequested.connect(self.tools_context_menu) # QTreeViewで設定するコンテキストメニュー
        # self.scene_tools_btn = self.scene.addWidget(self.set_picker_tools_btn)

        ############
        # Media Player
        ############
        # movie = QMovie('C:/Users/kesun/Desktop/Animation.gif')
        # self.movie_label = QLabel()
        # self.movie_label.setMovie(movie)
        # movie.start()
        # self.scene.addWidget(self.movie_label)

        # video_player = VideoPlayer();
        # video_player.resize(150, 150);
        # video_player.move(-20, 100);
        # self.scene.addWidget(video_player);
        # video_player.show();
        # video_player.addMedia("C:/Users/kesun/Desktop/Animation.gif");
        # video_player.openAndPlay();

        #######################
        # initialize optionVar
        #######################
        self.save_items = OrderedDict()
        # load optionVar
        load_settings = load_optionVar(key=WINDOW_OPTIONVAR)
        if load_settings:
            self.save_items[WINDOW_OPTIONVAR] = load_settings
        else:
            self.save_items[WINDOW_OPTIONVAR] = OrderedDict()

        #######################
        # load settings
        #######################
        # set namespace
        if 'NAMESPACE' in self.save_items[WINDOW_OPTIONVAR].keys():
            self.nss = self.save_items[WINDOW_OPTIONVAR]['NAMESPACE']
            self.set_picker_namespace_qle.setText(self.nss)

        # set view size
        if 'VIEW_SIZE' in self.save_items[WINDOW_OPTIONVAR].keys():
            self.LOCAL_VIEW_SIZE = self.save_items[WINDOW_OPTIONVAR]['VIEW_SIZE']
            if self.LOCAL_VIEW_SIZE:
                try:
                    self.resize(*self.LOCAL_VIEW_SIZE)
                except:
                    print(traceback.format_exc())

        # set list visibility
        if 'SETTINGLIST_VIS_STATE' in self.save_items[WINDOW_OPTIONVAR].keys():
            self.SETTINGLIST_VIS_STATE = self.save_items[WINDOW_OPTIONVAR]['SETTINGLIST_VIS_STATE']
            self.setting_list_visibility(state=self.SETTINGLIST_VIS_STATE)

    def create_menu_bar(self):
        self.menu_bar = self.menuBar()

        menus = OrderedDict()
        menus['File'] = {
            'parent':None
        }
        menus['Pickers'] = {
            'parent':'File'
        }
        menus['Import Picker File'] = {
            'parent':'Pickers',
            'cmd':partial(self.import_picker_file),
        }
        menus['Export Picker File'] = {
            'parent':'Pickers',
            'cmd':partial(self.export_picker_file),
        }

        menu_bar_stock = OrderedDict()
        for menu_name, menu_values in menus.items():
            menu_bar_stock[menu_name] = {}
            if menu_values['parent'] == None:
                menu_item = self.menu_bar.addMenu(menu_name)

            elif (menu_values['parent'] != None
                and not 'cmd' in menu_values.keys()):
                menu_item = QMenu(menu_name)
                parent_menu = menu_values['parent']
                parent_menu_item = menu_bar_stock[parent_menu]
                parent_menu_item.addMenu(menu_item)

            elif (menu_values['parent'] != None
                and 'cmd' in menu_values.keys()):
                parent_menu = menu_values['parent']
                parent_menu_item = menu_bar_stock[parent_menu]
                action = parent_menu_item.addAction(menu_name)
                action.triggered.connect(menu_values['cmd'])

            menu_bar_stock[menu_name] = menu_item

    def buildUI(self):
        self.layout()
        self.create_menu_bar()

    ############################
    # context menu
    ############################
    def create_context_menu(self, pos=None, menu=None, sender=None, context_menu=None):
        # 入れ物からQMenu.addAction(キー)、triggered.connect(menu_cmd['cmd'])で登録する
        for menu_name, menu_cmd in context_menu.items():
            action = menu.addAction(menu_name)
            action.triggered.connect(menu_cmd['cmd'])

        # QMenuの表示、sender.mapToGlobal(pos)
        menu.exec_(sender.mapToGlobal(pos))

    def tools_context_menu(self, pos):
        # senderからconnectでつながれたオブジェクトを取得
        sender = self.sender()
        # 取得したオブジェクトをQMenuの親に設定する
        menu = QMenu(sender)

        # 辞書型でコマンドを格納する入れ物を作る
        context_menu = OrderedDict()

        # 入れ物のキーにメニューの名前、バリューを辞書型にして、{'cmd':'コマンド'}にする
        # context_menu['File Import'] = {'cmd':partial(self.file_func, self.base_qle, 'import')}
        context_menu['Root Position Under Cog'] = {'cmd':partial(self._root_position_under_cog)}
        context_menu['Joints Convert to Rig'] = {'cmd':partial(self._joints_convert_to_rig)}
        context_menu['Fix Imported FBX Anim'] = {'cmd':partial(self._fix_fbx_anim)}
        context_menu['MirrorMotion'] = {'cmd':partial(self._mirror_motion)}
        context_menu['Replace Reference Tool'] = {'cmd':partial(self._replace_reference_tool)}
        context_menu['Attach Overlap Joints'] = {'cmd':partial(self._attach_overlap)}
        context_menu['Correct Keys'] = {'cmd':partial(self._correct_keys)}
        context_menu['Set Time From Key'] = {'cmd':partial(self._set_time_from_key)}

        self.create_context_menu(pos=pos, menu=menu, sender=sender, context_menu=context_menu)

    def del_cons_context_menu(self, pos):
        sender = self.sender()
        menu = QMenu(sender)
        context_menu = OrderedDict()

        context_menu['Root Position Under Cog'] = {'cmd':partial(self._del_root_position_under_cog)}
        context_menu['Joints Convert to Rig'] = {'cmd':partial(self._del_joints_convert_to_rig)}

        self.create_context_menu(pos=pos, menu=menu, sender=sender, context_menu=context_menu)

    def cog_hip_context_menu(self, pos):
        sender = self.sender()
        menu = QMenu(sender)
        context_menu = OrderedDict()

        context_menu['To Hip Bake'] = {'cmd':partial(self._cog_hip_matchbake, bake_to='hip')}
        context_menu['To Cog Bake'] = {'cmd':partial(self._cog_hip_matchbake, bake_to='cog')}

        self.create_context_menu(pos=pos, menu=menu, sender=sender, context_menu=context_menu)

    def foot_roll_L_context_menu(self, pos):
        sender = self.sender()
        menu = QMenu(sender)
        context_menu = OrderedDict()

        context_menu['Foot Roll Match(Foot Roll > Main)'] = {'cmd':partial(self._match_foot_roll, side='_L_')}
        context_menu['Foot Roll Match Bake(Foot Roll > Main)'] = {'cmd':partial(self._foot_roll_match_bake, side=['_L_'])}
        context_menu['Foot Roll Match(Main > Foot Roll)'] = {'cmd':partial(self._match_foot_roll_main_to_foot, side='_L_')}
        context_menu['Foot Roll Match Bake(Main > Foot Roll)'] = {'cmd':partial(self._foot_roll_match_bake_main_to_foot, side=['_L_'])}

        self.create_context_menu(pos=pos, menu=menu, sender=sender, context_menu=context_menu)

    def foot_roll_R_context_menu(self, pos):
        sender = self.sender()
        menu = QMenu(sender)
        context_menu = OrderedDict()

        context_menu['Foot Roll Match(Foot Roll > Main)'] = {'cmd':partial(self._match_foot_roll, side='_R_')}
        context_menu['Foot Roll Match Bake(Foot Roll > Main)'] = {'cmd':partial(self._foot_roll_match_bake, side=['_R_'])}
        context_menu['Foot Roll Match(Main > Foot Roll)'] = {'cmd':partial(self._match_foot_roll_main_to_foot, side='_R_')}
        context_menu['Foot Roll Match Bake(Main > Foot Roll)'] = {'cmd':partial(self._foot_roll_match_bake_main_to_foot, side=['_R_'])}

        self.create_context_menu(pos=pos, menu=menu, sender=sender, context_menu=context_menu)

    def window_options_context_menu(self, pos):
        sender = self.sender()
        menu = QMenu(sender)
        context_menu = OrderedDict()

        context_menu['List View > Open'] = {'cmd':partial(self.setting_list_visibility, True)}
        context_menu['List View > Close'] = {'cmd':partial(self.setting_list_visibility, False)}
        context_menu['Remove All Picker Items'] = {'cmd':partial(self.view.remove_all_items)}

        self.create_context_menu(pos=pos, menu=menu, sender=sender, context_menu=context_menu)

    def tree_options_context_menu(self, pos):
        sender = self.sender()
        menu = QMenu(sender)
        context_menu = OrderedDict()

        context_menu['Remove Items'] = {'cmd':partial(self.view.remove_items)}

        self.create_context_menu(pos=pos, menu=menu, sender=sender, context_menu=context_menu)

    ############################
    # setting list
    ############################
    def setting_list_visibility(self, state=None):
        self.SETTINGLIST_VIS_STATE = state
        self.save_items[WINDOW_OPTIONVAR]['SETTINGLIST_VIS_STATE'] = self.SETTINGLIST_VIS_STATE
        if self.SETTINGLIST_VIS_STATE:
            self.items_tree_view.setVisible(True)
            self.setting_widget.setVisible(True)
        else:
            self.items_tree_view.setVisible(False)
            self.setting_widget.setVisible(False)

    ############################
    # UI settings
    ############################
    def set_namespace(self):
        get_nss = cmds.ls(os=True)
        if get_nss:
            nss = get_nss[0]
            if not ':' in nss:
                self.nss = ''
            else:
                self.nss = ':'.join(nss.split(':')[0:-1]) + ':'
        else:
            self.nss = ''
        self.set_picker_namespace_qle.setText(self.nss)

        self.save_items[WINDOW_OPTIONVAR]['NAMESPACE'] = self.nss
        save_optionVar(save_items=self.save_items)

    def create_setting_view(self):
        sender = self.sender()
        indexes = sender.selectedIndexes()
        self.selected_items = [index.data() for index in indexes]

        if len(self.selected_items) == 0:
            return

        self.setting_widget.get_selected_settings(selected_items=self.selected_items)

    def change_ui_opacity(self):
        v = self.alpha_sdr.value()
        self.setWindowOpacity(v/100.0)

    ############################
    # anim function
    ############################
    def _root_position_under_cog(self):
        namespace = self.set_picker_namespace_qle.text()
        wiz2PickCmd.root_position_under_cog(namespace=namespace)

    def _del_root_position_under_cog(self):
        cmds.select('root_match_constraints_sets', r=1, ne=1)
        cnsts = cmds.pickWalk(d='down')
        for cnst in cnsts:
            try:
                cmds.delete(cnst)
            except:
                pass

    def _joints_convert_to_rig(self):
        namespace = self.set_picker_namespace_qle.text()

        try:
            match_const = wiz2PickCmd.MatchConstraint(namespace)
            match_const.match_bind_joints_to_ctrls()
            # match_const.fk_base_constraint(fk_parts=['hand_L', 'hand_R', 'foot_L', 'foot_R'])
        except Exception as e:
            print(traceback.format_exc())

    def _del_joints_convert_to_rig(self):
        cmds.cycleCheck(e=0)

        cmds.select('bake_cnst_sets', r=1, ne=1)
        cnsts = cmds.pickWalk(d='down')
        for cnst in cnsts:
            try:
                cmds.delete(cnst)
            except:
                pass

        cmds.cycleCheck(e=1)

    def _fix_fbx_anim(self):
        namespace = self.set_picker_namespace_qle.text()
        wiz2PickCmd.fix_fbx_anim(namespace=namespace)

    def _mirror_motion(self):
        mirror_tool = wiz2PickCmd.ReverseMotion()
        mirror_tool.show()

    def _replace_reference_tool(self):
        rrt = wiz2PickCmd.ReplaceReferenceTool()
        rrt.show()

    def _attach_overlap(self):
        aol = wiz2PickCmd.AutoOverlap()
        aol.ui()

    def _correct_keys(self):
        sel = cmds.ls(os=True)
        wiz2PickCmd.correctkeys(sel)

    def _root_to_main(self):
        merge_ctrl_dict = [
            {
                'merge_src':'main_ctrl',
                'merge_dst':'Root_ctrl',
            }
        ]

        namespace = self.set_picker_namespace_qle.text()

        for values in merge_ctrl_dict:
            values['merge_src'] = namespace + values['merge_src']
            values['merge_dst'] = namespace + values['merge_dst']

        wiz2PickCmd.merge_ctrl_values_per_frames(merge_ctrl_dict, namespace)

    def _set_time_from_key(self):
        ui = SetTimeFromKey()
        ui.buildUI()
        ui.show(dockable=True)

    def _select_all(self):
        namespace = self.set_picker_namespace_qle.text()
        cmds.select(namespace + 'ctrl_sets', r=True, ne=True)
        cmds.pickWalk(d='down')

    def _fullbake(self):
        sel = cmds.ls(os=True)
        wiz2PickCmd.fullbake(sel)

    def _force_zero_out(self):
        namespace = self.set_picker_namespace_qle.text()
        wiz2PickCmd.force_zeroout(namespace=namespace)
        wiz2PickCmd.reset_spaces(attr='space', namespace=namespace)

    def _go_to_bindPose_for_rig(self):
        namespace = self.set_picker_namespace_qle.text()
        wiz2PickCmd.go_to_bindPose_for_rig(namespace=namespace)
        cmds.select(cl=True)
        wiz2PickCmd.go_to_bindPose_for_rig(namespace=namespace)
        cmds.select(cl=True)

    def _ikfk_switch_hand_L(self):
        namespace = self.set_picker_namespace_qle.text()
        wiz2PickCmd.ikfk_hand_L(picker=False, match=False, namespace=namespace)

    def _ikfk_switch_hand_R(self):
        namespace = self.set_picker_namespace_qle.text()
        wiz2PickCmd.ikfk_hand_R(picker=False, match=False, namespace=namespace)

    def _ikfk_switch_foot_L(self):
        namespace = self.set_picker_namespace_qle.text()
        wiz2PickCmd.ikfk_foot_L(picker=False, match=False, namespace=namespace)

    def _ikfk_switch_foot_R(self):
        namespace = self.set_picker_namespace_qle.text()
        wiz2PickCmd.ikfk_foot_R(picker=False, match=False, namespace=namespace)

    def _ikfk_match_hand_L(self):
        namespace = self.set_picker_namespace_qle.text()
        wiz2PickCmd.ikfk_hand_L(picker=False, match=True, namespace=namespace)

    def _ikfk_match_hand_R(self):
        namespace = self.set_picker_namespace_qle.text()
        wiz2PickCmd.ikfk_hand_R(picker=False, match=True, namespace=namespace)

    def _ikfk_match_foot_L(self):
        namespace = self.set_picker_namespace_qle.text()
        wiz2PickCmd.ikfk_foot_L(picker=False, match=True, namespace=namespace)

    def _ikfk_match_foot_R(self):
        namespace = self.set_picker_namespace_qle.text()
        wiz2PickCmd.ikfk_foot_R(picker=False, match=True, namespace=namespace)

    def _Hand_FK_to_IK_Match_Bake(self):
        namespace = self.set_picker_namespace_qle.text()

        if self.set_picker_bake_before_chbx.isChecked():
            gPlayBackSlider = mel.eval('$temp=$gPlayBackSlider')
            times = cmds.timeControl(gPlayBackSlider, q=True, ra=True)
            wiz2PickCmd.before_bakes_hand(side='both', namespace=namespace, time_range=times)

        currentValue = self.set_picker_bake_key_switch_chbx.isChecked()

        wiz2PickCmd.ikfk_match_with_bake_for_timeSlider(
            hand_L=True, hand_L_ikfk='fk2ik',
            hand_R=True, hand_R_ikfk='fk2ik',
            foot_L=None, foot_L_ikfk='fk2ik',
            foot_R=None, foot_R_ikfk='fk2ik',
            force_state_key=currentValue, namespace=namespace
        )

    def _Hand_L_FK_to_IK_Match_Bake(self):
        namespace = self.set_picker_namespace_qle.text()

        if self.set_picker_bake_before_chbx.isChecked():
            gPlayBackSlider = mel.eval('$temp=$gPlayBackSlider')
            times = cmds.timeControl(gPlayBackSlider, q=True, ra=True)
            wiz2PickCmd.before_bakes_hand(side='left', namespace=namespace, time_range=times)

        currentValue = self.set_picker_bake_key_switch_chbx.isChecked()

        wiz2PickCmd.ikfk_match_with_bake_for_timeSlider(
            hand_L=True, hand_L_ikfk='fk2ik',
            hand_R=None, hand_R_ikfk='fk2ik',
            foot_L=None, foot_L_ikfk='fk2ik',
            foot_R=None, foot_R_ikfk='fk2ik',
            force_state_key=currentValue, namespace=namespace
        )

    def _Hand_R_FK_to_IK_Match_Bake(self):
        namespace = self.set_picker_namespace_qle.text()

        if self.set_picker_bake_before_chbx.isChecked():
            gPlayBackSlider = mel.eval('$temp=$gPlayBackSlider')
            times = cmds.timeControl(gPlayBackSlider, q=True, ra=True)
            wiz2PickCmd.before_bakes_hand(side='right', namespace=namespace, time_range=times)

        currentValue = self.set_picker_bake_key_switch_chbx.isChecked()

        wiz2PickCmd.ikfk_match_with_bake_for_timeSlider(
            hand_L=None, hand_L_ikfk='fk2ik',
            hand_R=True, hand_R_ikfk='fk2ik',
            foot_L=None, foot_L_ikfk='fk2ik',
            foot_R=None, foot_R_ikfk='fk2ik',
            force_state_key=currentValue, namespace=namespace
        )

    def _Foot_L_FK_to_IK_Match_Bake(self):
        namespace = self.set_picker_namespace_qle.text()

        if self.set_picker_bake_before_chbx.isChecked():
            gPlayBackSlider = mel.eval('$temp=$gPlayBackSlider')
            times = cmds.timeControl(gPlayBackSlider, q=True, ra=True)
            wiz2PickCmd.before_bakes_foot(side='left', namespace=namespace, time_range=times)

        currentValue = self.set_picker_bake_key_switch_chbx.isChecked()

        wiz2PickCmd.ikfk_match_with_bake_for_timeSlider(
            hand_L=None, hand_L_ikfk='fk2ik',
            hand_R=None, hand_R_ikfk='fk2ik',
            foot_L=True, foot_L_ikfk='fk2ik',
            foot_R=None, foot_R_ikfk='fk2ik',
            force_state_key=currentValue, namespace=namespace
        )

    def _Foot_R_FK_to_IK_Match_Bake(self):
        namespace = self.set_picker_namespace_qle.text()

        if self.set_picker_bake_before_chbx.isChecked():
            gPlayBackSlider = mel.eval('$temp=$gPlayBackSlider')
            times = cmds.timeControl(gPlayBackSlider, q=True, ra=True)
            wiz2PickCmd.before_bakes_foot(side='right', namespace=namespace, time_range=times)

        currentValue = self.set_picker_bake_key_switch_chbx.isChecked()

        wiz2PickCmd.ikfk_match_with_bake_for_timeSlider(
            hand_L=None, hand_L_ikfk='fk2ik',
            hand_R=None, hand_R_ikfk='fk2ik',
            foot_L=None, foot_L_ikfk='fk2ik',
            foot_R=True, foot_R_ikfk='fk2ik',
            force_state_key=currentValue, namespace=namespace
        )

    def _Hand_Foot_L_FK_to_IK_Match_Bake(self):
        namespace = self.set_picker_namespace_qle.text()

        if self.set_picker_bake_before_chbx.isChecked():
            gPlayBackSlider = mel.eval('$temp=$gPlayBackSlider')
            times = cmds.timeControl(gPlayBackSlider, q=True, ra=True)
            wiz2PickCmd.before_bakes_hand(side='left', namespace=namespace, time_range=times)
            wiz2PickCmd.before_bakes_foot(side='left', namespace=namespace, time_range=times)

        currentValue = self.set_picker_bake_key_switch_chbx.isChecked()

        wiz2PickCmd.ikfk_match_with_bake_for_timeSlider(
            hand_L=True, hand_L_ikfk='fk2ik',
            hand_R=None, hand_R_ikfk='fk2ik',
            foot_L=True, foot_L_ikfk='fk2ik',
            foot_R=None, foot_R_ikfk='fk2ik',
            force_state_key=currentValue, namespace=namespace
        )

    def _Hand_Foot_R_FK_to_IK_Match_Bake(self):
        namespace = self.set_picker_namespace_qle.text()

        if self.set_picker_bake_before_chbx.isChecked():
            gPlayBackSlider = mel.eval('$temp=$gPlayBackSlider')
            times = cmds.timeControl(gPlayBackSlider, q=True, ra=True)
            wiz2PickCmd.before_bakes_hand(side='right', namespace=namespace, time_range=times)
            wiz2PickCmd.before_bakes_foot(side='right', namespace=namespace, time_range=times)

        currentValue = self.set_picker_bake_key_switch_chbx.isChecked()

        wiz2PickCmd.ikfk_match_with_bake_for_timeSlider(
            hand_L=None, hand_L_ikfk='fk2ik',
            hand_R=True, hand_R_ikfk='fk2ik',
            foot_L=None, foot_L_ikfk='fk2ik',
            foot_R=True, foot_R_ikfk='fk2ik',
            force_state_key=currentValue, namespace=namespace
        )

    def _Foot_FK_to_IK_Match_Bake(self):
        namespace = self.set_picker_namespace_qle.text()

        if self.set_picker_bake_before_chbx.isChecked():
            gPlayBackSlider = mel.eval('$temp=$gPlayBackSlider')
            times = cmds.timeControl(gPlayBackSlider, q=True, ra=True)
            wiz2PickCmd.before_bakes_foot(side='both', namespace=namespace, time_range=times)

        currentValue = self.set_picker_bake_key_switch_chbx.isChecked()

        wiz2PickCmd.ikfk_match_with_bake_for_timeSlider(
            hand_L=None, hand_L_ikfk='fk2ik',
            hand_R=None, hand_R_ikfk='fk2ik',
            foot_L=True, foot_L_ikfk='fk2ik',
            foot_R=True, foot_R_ikfk='fk2ik',
            force_state_key=currentValue, namespace=namespace
        )

    def _FK_to_IK_Match_Bake(self):
        namespace = self.set_picker_namespace_qle.text()

        if self.set_picker_bake_before_chbx.isChecked():
            gPlayBackSlider = mel.eval('$temp=$gPlayBackSlider')
            times = cmds.timeControl(gPlayBackSlider, q=True, ra=True)
            wiz2PickCmd.before_bakes_hand(side='both', namespace=namespace, time_range=times)
            wiz2PickCmd.before_bakes_foot(side='both', namespace=namespace, time_range=times)

        currentValue = self.set_picker_bake_key_switch_chbx.isChecked()

        wiz2PickCmd.ikfk_match_with_bake_for_timeSlider(
            hand_L=True, hand_L_ikfk='fk2ik',
            hand_R=True, hand_R_ikfk='fk2ik',
            foot_L=True, foot_L_ikfk='fk2ik',
            foot_R=True, foot_R_ikfk='fk2ik',
            force_state_key=currentValue, namespace=namespace
        )

    def _Hand_IK_to_FK_Match_Bake(self):
        namespace = self.set_picker_namespace_qle.text()

        if self.set_picker_bake_before_chbx.isChecked():
            gPlayBackSlider = mel.eval('$temp=$gPlayBackSlider')
            times = cmds.timeControl(gPlayBackSlider, q=True, ra=True)
            wiz2PickCmd.before_bakes_hand(side='both', namespace=namespace, time_range=times)

        currentValue = self.set_picker_bake_key_switch_chbx.isChecked()

        wiz2PickCmd.ikfk_match_with_bake_for_timeSlider(
            hand_L=True, hand_L_ikfk='ik2fk',
            hand_R=True, hand_R_ikfk='ik2fk',
            foot_L=None, foot_L_ikfk='ik2fk',
            foot_R=None, foot_R_ikfk='ik2fk',
            force_state_key=currentValue, namespace=namespace
        )

    def _Hand_L_IK_to_FK_Match_Bake(self):
        namespace = self.set_picker_namespace_qle.text()

        if self.set_picker_bake_before_chbx.isChecked():
            gPlayBackSlider = mel.eval('$temp=$gPlayBackSlider')
            times = cmds.timeControl(gPlayBackSlider, q=True, ra=True)
            wiz2PickCmd.before_bakes_hand(side='left', namespace=namespace, time_range=times)

        currentValue = self.set_picker_bake_key_switch_chbx.isChecked()

        wiz2PickCmd.ikfk_match_with_bake_for_timeSlider(
            hand_L=True, hand_L_ikfk='ik2fk',
            hand_R=None, hand_R_ikfk='ik2fk',
            foot_L=None, foot_L_ikfk='ik2fk',
            foot_R=None, foot_R_ikfk='ik2fk',
            force_state_key=currentValue, namespace=namespace
        )

    def _Hand_R_IK_to_FK_Match_Bake(self):
        namespace = self.set_picker_namespace_qle.text()

        if self.set_picker_bake_before_chbx.isChecked():
            gPlayBackSlider = mel.eval('$temp=$gPlayBackSlider')
            times = cmds.timeControl(gPlayBackSlider, q=True, ra=True)
            wiz2PickCmd.before_bakes_hand(side='right', namespace=namespace, time_range=times)

        currentValue = self.set_picker_bake_key_switch_chbx.isChecked()

        wiz2PickCmd.ikfk_match_with_bake_for_timeSlider(
            hand_L=None, hand_L_ikfk='ik2fk',
            hand_R=True, hand_R_ikfk='ik2fk',
            foot_L=None, foot_L_ikfk='ik2fk',
            foot_R=None, foot_R_ikfk='ik2fk',
            force_state_key=currentValue, namespace=namespace
        )

    def _Foot_L_IK_to_FK_Match_Bake(self):
        namespace = self.set_picker_namespace_qle.text()

        if self.set_picker_bake_before_chbx.isChecked():
            gPlayBackSlider = mel.eval('$temp=$gPlayBackSlider')
            times = cmds.timeControl(gPlayBackSlider, q=True, ra=True)
            wiz2PickCmd.before_bakes_foot(side='left', namespace=namespace, time_range=times)

        currentValue = self.set_picker_bake_key_switch_chbx.isChecked()

        wiz2PickCmd.ikfk_match_with_bake_for_timeSlider(
            hand_L=None, hand_L_ikfk='ik2fk',
            hand_R=None, hand_R_ikfk='ik2fk',
            foot_L=True, foot_L_ikfk='ik2fk',
            foot_R=None, foot_R_ikfk='ik2fk',
            force_state_key=currentValue, namespace=namespace
        )

    def _Foot_R_IK_to_FK_Match_Bake(self):
        namespace = self.set_picker_namespace_qle.text()

        if self.set_picker_bake_before_chbx.isChecked():
            gPlayBackSlider = mel.eval('$temp=$gPlayBackSlider')
            times = cmds.timeControl(gPlayBackSlider, q=True, ra=True)
            wiz2PickCmd.before_bakes_foot(side='right', namespace=namespace, time_range=times)

        currentValue = self.set_picker_bake_key_switch_chbx.isChecked()

        wiz2PickCmd.ikfk_match_with_bake_for_timeSlider(
            hand_L=None, hand_L_ikfk='ik2fk',
            hand_R=None, hand_R_ikfk='ik2fk',
            foot_L=None, foot_L_ikfk='ik2fk',
            foot_R=True, foot_R_ikfk='ik2fk',
            force_state_key=currentValue, namespace=namespace
        )

    def _Hand_Foot_L_IK_to_FK_Match_Bake(self):
        namespace = self.set_picker_namespace_qle.text()

        if self.set_picker_bake_before_chbx.isChecked():
            gPlayBackSlider = mel.eval('$temp=$gPlayBackSlider')
            times = cmds.timeControl(gPlayBackSlider, q=True, ra=True)
            wiz2PickCmd.before_bakes_foot(side='left', namespace=namespace, time_range=times)

        currentValue = self.set_picker_bake_key_switch_chbx.isChecked()

        wiz2PickCmd.ikfk_match_with_bake_for_timeSlider(
            hand_L=True, hand_L_ikfk='ik2fk',
            hand_R=None, hand_R_ikfk='ik2fk',
            foot_L=True, foot_L_ikfk='ik2fk',
            foot_R=None, foot_R_ikfk='ik2fk',
            force_state_key=currentValue, namespace=namespace
        )

    def _Hand_Foot_R_IK_to_FK_Match_Bake(self):
        namespace = self.set_picker_namespace_qle.text()

        if self.set_picker_bake_before_chbx.isChecked():
            gPlayBackSlider = mel.eval('$temp=$gPlayBackSlider')
            times = cmds.timeControl(gPlayBackSlider, q=True, ra=True)
            wiz2PickCmd.before_bakes_foot(side='right', namespace=namespace, time_range=times)

        currentValue = self.set_picker_bake_key_switch_chbx.isChecked()

        wiz2PickCmd.ikfk_match_with_bake_for_timeSlider(
            hand_L=None, hand_L_ikfk='ik2fk',
            hand_R=True, hand_R_ikfk='ik2fk',
            foot_L=None, foot_L_ikfk='ik2fk',
            foot_R=True, foot_R_ikfk='ik2fk',
            force_state_key=currentValue, namespace=namespace
        )

    def _Foot_IK_to_FK_Match_Bake(self):
        namespace = self.set_picker_namespace_qle.text()

        if self.set_picker_bake_before_chbx.isChecked():
            gPlayBackSlider = mel.eval('$temp=$gPlayBackSlider')
            times = cmds.timeControl(gPlayBackSlider, q=True, ra=True)
            wiz2PickCmd.before_bakes_foot(side='both', namespace=namespace, time_range=times)

        currentValue = self.set_picker_bake_key_switch_chbx.isChecked()

        wiz2PickCmd.ikfk_match_with_bake_for_timeSlider(
            hand_L=None, hand_L_ikfk='ik2fk',
            hand_R=None, hand_R_ikfk='ik2fk',
            foot_L=True, foot_L_ikfk='ik2fk',
            foot_R=True, foot_R_ikfk='ik2fk',
            force_state_key=currentValue, namespace=namespace
        )

    def _IK_to_FK_Match_Bake(self):
        namespace = self.set_picker_namespace_qle.text()

        if self.set_picker_bake_before_chbx.isChecked():
            gPlayBackSlider = mel.eval('$temp=$gPlayBackSlider')
            times = cmds.timeControl(gPlayBackSlider, q=True, ra=True)
            wiz2PickCmd.before_bakes_hand(side='both', namespace=namespace, time_range=times)
            wiz2PickCmd.before_bakes_foot(side='both', namespace=namespace, time_range=times)

        currentValue = self.set_picker_bake_key_switch_chbx.isChecked()

        wiz2PickCmd.ikfk_match_with_bake_for_timeSlider(
            hand_L=True, hand_L_ikfk='ik2fk',
            hand_R=True, hand_R_ikfk='ik2fk',
            foot_L=True, foot_L_ikfk='ik2fk',
            foot_R=True, foot_R_ikfk='ik2fk',
            force_state_key=currentValue, namespace=namespace
        )

    def _FK2IK_IK2FK_Match_Bake(self):
        namespace = self.set_picker_namespace_qle.text()

        if self.set_picker_bake_before_chbx.isChecked():
            gPlayBackSlider = mel.eval('$temp=$gPlayBackSlider')
            times = cmds.timeControl(gPlayBackSlider, q=True, ra=True)
            wiz2PickCmd.before_bakes_hand(side='both', namespace=namespace, time_range=times)
            wiz2PickCmd.before_bakes_foot(side='both', namespace=namespace, time_range=times)

        currentValue = self.set_picker_bake_key_switch_chbx.isChecked()
        wiz2PickCmd.fk2ik_ik2fk_matchbake(force_state_key=currentValue, namespace=namespace)

    def _IK2FK_FK2IK_Match_bake(self):
        namespace = self.set_picker_namespace_qle.text()

        if self.set_picker_bake_before_chbx.isChecked():
            gPlayBackSlider = mel.eval('$temp=$gPlayBackSlider')
            times = cmds.timeControl(gPlayBackSlider, q=True, ra=True)
            wiz2PickCmd.before_bakes_hand(side='both', namespace=namespace, time_range=times)
            wiz2PickCmd.before_bakes_foot(side='both', namespace=namespace, time_range=times)

        currentValue = self.set_picker_bake_key_switch_chbx.isChecked()
        wiz2PickCmd.ik2fk_fk2ik_matchbake(force_state_key=currentValue, namespace=namespace)

    def _match_foot_roll(self, side=None):
        namespace = self.set_picker_namespace_qle.text()

        if self.set_picker_bake_before_chbx.isChecked():
            gPlayBackSlider = mel.eval('$temp=$gPlayBackSlider')
            times = cmds.timeControl(gPlayBackSlider, q=True, ra=True)
            wiz2PickCmd.before_bakes_hand(side='both', namespace=namespace, time_range=times)
            wiz2PickCmd.before_bakes_foot(side='both', namespace=namespace, time_range=times)

        wiz2PickCmd.match_foot_roll(setkey=None, side=side, main_to_foot=False, namespace=namespace)

    def _match_foot_roll_main_to_foot(self, side=None):
        namespace = self.set_picker_namespace_qle.text()
        wiz2PickCmd.match_foot_roll(setkey=None, side=side, main_to_foot=True, namespace=namespace)

    def _foot_roll_match_bake(self, side=None):
        namespace = self.set_picker_namespace_qle.text()
        wiz2PickCmd.foot_roll_match_bake(side=side, main_to_foot=False, namespace=namespace)

    def _foot_roll_match_bake_main_to_foot(self, side=None):
        namespace = self.set_picker_namespace_qle.text()
        wiz2PickCmd.foot_roll_match_bake(side=side, main_to_foot=True, namespace=namespace)

    def _cog_hip_matchbake(self, bake_to=None):
        namespace = self.set_picker_namespace_qle.text()
        wiz2PickCmd.cog_hip_matchbake(bake_to=bake_to, namespace=namespace)

    ############################
    # events
    ############################
    def resizeEvent(self, event):
        self.scene_size = self.size()
        # stock window size
        self.save_items[WINDOW_OPTIONVAR]['VIEW_SIZE'] = [self.scene_size.width(), self.scene_size.height()]
        save_optionVar(save_items=self.save_items)

        super(PickerAnimTools, self).resizeEvent(event)

    def closeEvent(self, event):
        # stock picker items
        self.save_items[WINDOW_OPTIONVAR]['PICKER_ITEMS'] = self.view.picker_items
        save_optionVar(save_items=self.save_items)

        super(PickerAnimTools, self).closeEvent(event)

    ############################
    # picker file command
    ############################
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

    def import_picker_file(self):
        print('IMPORT PICKER FILE')
        settings = self.set_path_dict['import_picker']
        file_path = self.file_dialog(**settings)
        self.import_picker_func(file_path[0])

    def import_picker_func(self, file_path):
        if file_path:
            self.view.picker_items = json_transfer(file_path, operation='import')

            self.view.remove_all_items()
            [self.view.add_pick_item(name=name, **item_values) for name, item_values in self.view.picker_items.items()]

            self.scene.update()

            self.save_items[WINDOW_OPTIONVAR]['PICKER_ITEMS'] = self.view.picker_items
            save_optionVar(save_items=self.save_items)


    def export_picker_file(self):
        print('EXPORT PICKER FILE')
        settings = self.set_path_dict['export_picker']
        file_path = self.file_dialog(**settings)
        if file_path: json_transfer(file_path[0], operation='export', export_values=self.view.picker_items, export_type='utf-8')

#############################
# tool tip class
# not use
#############################
# class ToolTipDialog(QDialog):
#     def __init__(self, text="", width=200, height=100, positionOffset=10, parent=None):
#         super(ToolTipDialog, self).__init__(parent)
#
#         self._text = text
#
#         self.color = [0, 0, 255]
#         self.tooltipWidth = width
#         self.tooltipHeight = height
#         self.positionOffset = positionOffset
#         # 枠を消して、透明にする
#         self.setWindowFlags(Qt.FramelessWindowHint)
#         self.setAttribute(Qt.WA_TranslucentBackground)
#
#         self.positionUpdate()
#
#     def setText(self, text):
#         self._text = text
#         self.update()
#
#     def getText(self):
#         return self._text
#
#     def positionUpdate(self):
#         pos = QCursor().pos()
#         self.setGeometry(pos.x() + self.positionOffset,
#                          pos.y() + self.positionOffset,
#                          self.tooltipWidth,
#                          self.tooltipHeight)
#
#     def paintEvent(self, event):
#         painter = QPainter(self)
#
#         pen = QPen(QColor(*self.color), 8)
#         bg_color = QColor(*self.color)
#         painter.setPen(pen)
#         painter.setBrush(bg_color)
#         rect = QRect(0, 0, self.geometry().width(), self.geometry().height())
#         painter.drawRoundedRect(rect, 20, 20)
#         # 文字を描画
#         painter.setFont(QFont(u'メイリオ', 20, QFont.Bold, False))
#         painter.setPen(Qt.white)
#         painter.drawText(QPoint(10, 30), self.getText())

#############################
# GraphicsScene class
#############################
class GraphicsScene(QGraphicsScene):
    def __init__(self, parent=None):
        super(GraphicsScene, self).__init__(parent)

        # settings
        self.gridSize = 10

        self._color_background = QColor("#393939")
        self._color_light = QColor("#2f2f2f")

        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)

        self.setBackgroundBrush(self._color_background)

    def drawBackground(self, painter, rect):
        super(GraphicsScene, self).drawBackground(painter, rect)

        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        first_left = left - (left % self.gridSize)
        first_top = top - (top % self.gridSize)

        lines_light = []
        for x in range(first_left, right, self.gridSize):
            lines_light.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.gridSize):
            lines_light.append(QLine(left, y, right, y))

        painter.setPen(self._pen_light)
        painter.drawLines(lines_light)

    def dropEvent(self, event):
        item = self.itemAt(event.scenePos())
        if item.setAcceptDrops == True:
            try:
               item.dropEvent(event)
            except RuntimeError:
                pass

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

#############################
# GraphicsProxyWidget class
# not use
#############################
# class GraphicsProxyWidget(QGraphicsProxyWidget):
#     def dragEnterEvent(self, event):
#         event.acceptProposedAction()
#
#     def dropEvent(self, event):
#         return self.widget().dropEvent(event)
#
#     def dragMoveEvent(self, event):
#         event.acceptProposedAction()


#############################
# GraphicsRectItem class
#############################
class GraphicsRectItem(QGraphicsRectItem):
    def __init__(self, *args, **kwargs):
        super(GraphicsRectItem, self).__init__(*args, **kwargs)

        self.setAcceptHoverEvents(True)

        self.block_size = -1
        self.init_rect = None
        self.rect_edit_mode = None
        self.rect_move = None

    def mouseMoveEvent(self, event):
        if self.rect_move:
            pos = event.pos()
            local_rect = self.mapToScene(pos.x(), pos.y())

            cur_x = local_rect.x() - self.init_rect.x()
            cur_y = local_rect.y() - self.init_rect.y()

            snap_pos = QPointF(cur_x, cur_y)

            new_pos_x = round(snap_pos.x(), self.block_size)
            new_pos_y = round(snap_pos.y(), self.block_size)

            cur_pos = QPointF(new_pos_x, new_pos_y)
            self.setPos(cur_pos)

            self.update()

        super(GraphicsRectItem, self).mouseMoveEvent(event)

    def mousePressEvent(self, event):
        self.init_rect = event.pos()

        view = self.scene().views()[0]
        self.rect_edit_mode = view.setting_widget.rect_edit_mode

        super(GraphicsRectItem, self).mousePressEvent(event)

#############################
# GraphicsView class
#############################
class GraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super(GraphicsView, self).__init__(parent)

        self.picker_items = {
            # Hand Left
            'thumb_L_000':{
                    'item_name':'Thumb_01_L_ctrl',
                    'rect':[225, 220, 15, 15],
                    'color':[255, 128, 255],
                    'edge_color':[0, 0, 0],
                    'width':1
            },
            'thumb_L_001':{
                    'item_name':'Thumb_02_L_ctrl',
                    'rect':[255, 220, 15, 15],
                    'color':[255, 128, 255],
                    'edge_color':[0, 0, 0],
                    'width':1
            },
            'thumb_L_002':{
                    'item_name':'Thumb_03_L_ctrl',
                    'rect':[285, 220, 15, 15],
                    'color':[255, 128, 255],
                    'edge_color':[0, 0, 0],
                    'width':1
            },
            'index_L_000':{
                    'item_name':'Index_01_L_ctrl',
                    'rect':[225, 190, 15, 15],
                    'color':[255, 128, 255],
                    'edge_color':[0, 0, 0],
                    'width':1
            },
            'index_L_001':{
                    'item_name':'Index_02_L_ctrl',
                    'rect':[255, 190, 15, 15],
                    'color':[255, 128, 255],
                    'edge_color':[0, 0, 0],
                    'width':1
            },
            'index_L_002':{
                    'item_name':'Index_03_L_ctrl',
                    'rect':[285, 190, 15, 15],
                    'color':[255, 128, 255],
                    'edge_color':[0, 0, 0],
                    'width':1
            },
            'middle_L_000':{
                    'item_name':'Middle_01_L_ctrl',
                    'rect':[225, 160, 15, 15],
                    'color':[255, 128, 255],
                    'edge_color':[0, 0, 0],
                    'width':1
            },
            'middle_L_001':{
                    'item_name':'Middle_02_L_ctrl',
                    'rect':[255, 160, 15, 15],
                    'color':[255, 128, 255],
                    'edge_color':[0, 0, 0],
                    'width':1
            },
            'middle_L_002':{
                    'item_name':'Middle_03_L_ctrl',
                    'rect':[285, 160, 15, 15],
                    'color':[255, 128, 255],
                    'edge_color':[0, 0, 0],
                    'width':1
            },
            'ring_L_000':{
                    'item_name':'Ring_01_L_ctrl',
                    'rect':[225, 130, 15, 15],
                    'color':[255, 128, 255],
                    'edge_color':[0, 0, 0],
                    'width':1
            },
            'ring_L_001':{
                    'item_name':'Ring_02_L_ctrl',
                    'rect':[255, 130, 15, 15],
                    'color':[255, 128, 255],
                    'edge_color':[0, 0, 0],
                    'width':1
            },
            'ring_L_002':{
                    'item_name':'Ring_03_L_ctrl',
                    'rect':[285, 130, 15, 15],
                    'color':[255, 128, 255],
                    'edge_color':[0, 0, 0],
                    'width':1
            },
            'pinky_L_000':{
                    'item_name':'Pinky_01_L_ctrl',
                    'rect':[225, 100, 15, 15],
                    'color':[255, 128, 255],
                    'edge_color':[0, 0, 0],
                    'width':1
            },
            'pinky_L_001':{
                    'item_name':'Pinky_02_L_ctrl',
                    'rect':[255, 100, 15, 15],
                    'color':[255, 128, 255],
                    'edge_color':[0, 0, 0],
                    'width':1
            },
            'pinky_L_002':{
                    'item_name':'Pinky_03_L_ctrl',
                    'rect':[285, 100, 15, 15],
                    'color':[255, 128, 255],
                    'edge_color':[0, 0, 0],
                    'width':1
            },

            # Hand Right
            'thumb_R_000':{
                    'item_name':'Thumb_01_R_ctrl',
                    'rect':[125, 220, 15, 15],
                    'color':[64, 128, 255],
                    'edge_color':[0, 0, 0],
                    'width':1
            },
            'thumb_R_001':{
                    'item_name':'Thumb_02_R_ctrl',
                    'rect':[95, 220, 15, 15],
                    'color':[64, 128, 255],
                    'edge_color':[0, 0, 0],
                    'width':1
            },
            'thumb_R_002':{
                    'item_name':'Thumb_03_R_ctrl',
                    'rect':[65, 220, 15, 15],
                    'color':[64, 128, 255],
                    'edge_color':[0, 0, 0],
                    'width':1
            },
            'index_R_000':{
                    'item_name':'Index_01_R_ctrl',
                    'rect':[125, 190, 15, 15],
                    'color':[64, 128, 255],
                    'edge_color':[0, 0, 0],
                    'width':1
            },
            'index_R_001':{
                    'item_name':'Index_02_R_ctrl',
                    'rect':[95, 190, 15, 15],
                    'color':[64, 128, 255],
                    'edge_color':[0, 0, 0],
                    'width':1
            },
            'index_R_002':{
                    'item_name':'Index_03_R_ctrl',
                    'rect':[65, 190, 15, 15],
                    'color':[64, 128, 255],
                    'edge_color':[0, 0, 0],
                    'width':1
            },
            'middle_R_000':{
                    'item_name':'Middle_01_R_ctrl',
                    'rect':[125, 160, 15, 15],
                    'color':[64, 128, 255],
                    'edge_color':[0, 0, 0],
                    'width':1
            },
            'middle_R_001':{
                    'item_name':'Middle_02_R_ctrl',
                    'rect':[95, 160, 15, 15],
                    'color':[64, 128, 255],
                    'edge_color':[0, 0, 0],
                    'width':1
            },
            'middle_R_002':{
                    'item_name':'Middle_03_R_ctrl',
                    'rect':[65, 160, 15, 15],
                    'color':[64, 128, 255],
                    'edge_color':[0, 0, 0],
                    'width':1
            },
            'ring_R_000':{
                    'item_name':'Ring_01_R_ctrl',
                    'rect':[125, 130, 15, 15],
                    'color':[64, 128, 255],
                    'edge_color':[0, 0, 0],
                    'width':1
            },
            'ring_R_001':{
                    'item_name':'Ring_02_R_ctrl',
                    'rect':[95, 130, 15, 15],
                    'color':[64, 128, 255],
                    'edge_color':[0, 0, 0],
                    'width':1
            },
            'ring_R_002':{
                    'item_name':'Ring_03_R_ctrl',
                    'rect':[65, 130, 15, 15],
                    'color':[64, 128, 255],
                    'edge_color':[0, 0, 0],
                    'width':1
            },
            'pinky_R_000':{
                    'item_name':'Pinky_01_R_ctrl',
                    'rect':[125, 100, 15, 15],
                    'color':[64, 128, 255],
                    'edge_color':[0, 0, 0],
                    'width':1
            },
            'pinky_R_001':{
                    'item_name':'Pinky_02_R_ctrl',
                    'rect':[95, 100, 15, 15],
                    'color':[64, 128, 255],
                    'edge_color':[0, 0, 0],
                    'width':1
            },
            'pinky_R_002':{
                    'item_name':'Pinky_03_R_ctrl',
                    'rect':[65, 100, 15, 15],
                    'color':[64, 128, 255],
                    'edge_color':[0, 0, 0],
                    'width':1
            },

            # Hand Attach Left
            'hand_attach_L_000':{
                    'item_name':'Handattach_L_ctrl',
                    'rect':[285, 0, 15, 15],
                    'color':[255, 128, 255],
                    'edge_color':[0, 0, 0],
                    'width':1
            },
            # Hand Attach Right
            'hand_attach_R_000':{
                    'item_name':'Handattach_R_ctrl',
                    'rect':[225, 0, 15, 15],
                    'color':[64, 128, 255],
                    'edge_color':[0, 0, 0],
                    'width':1
            },
        }

        self.picker_items = {}

        self.center = None
        self.zoom = 0
        self.selection_stock = list()
        self.nss_qle = None

        self.names = list()
        self.item_names = list()

        self.seleced_item_indexes = list()
        self.selected_item_names = list()
        self.selected_scene_items = OrderedDict()

        # GraphicsView settings
        self.setAcceptDrops(True)
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.setDragMode(QGraphicsView.RubberBandDrag) # 範囲選択

        # load optionVar
        self.save_items = OrderedDict()
        load_settings = load_optionVar(key=WINDOW_OPTIONVAR)
        if load_settings:
            self.save_items[WINDOW_OPTIONVAR] = load_settings
        else:
            self.save_items[WINDOW_OPTIONVAR] = OrderedDict()

        if 'PICKER_ITEMS' in self.save_items[WINDOW_OPTIONVAR].keys():
            self.picker_items = self.save_items[WINDOW_OPTIONVAR]['PICKER_ITEMS']

        # scene settings
        self.scene_size = None
        self.scene = GraphicsScene()
        self.setScene(self.scene)
        self.scene.selectionChanged.connect(self.selection_changed)

        ############
        # get setting list
        ############
        # get list
        self.items_tree_view = parent.items_tree_view
        # self.items_tree_view.selectionModel().selectionChanged.connect(self.selection_list_changed)

        self.items_model = parent.items_model

        # get list widget
        self.setting_widget = parent.setting_widget

        # Add Items
        self.items_model.clear()
        self.items_model.setColumnCount(1)
        self.items_model.setHeaderData(0, Qt.Horizontal, 'Items')

        self.get_located_items()
        [self.add_pick_item(name=name, **item_values) for name, item_values in self.picker_items.items()]

    ######################
    # add picker items
    ######################
    def add_pick_item(self, name='rectTest', item_name=None, rect=[-100, -100, 80, 100], color=[128, 220, 190], edge_color=[196, 255, 220], width=4):
        # create shape
        if name in self.selected_scene_items.keys():
            rect_item = self.selected_scene_items[name]

            pen = rect_item.pen()
            brush = rect_item.brush()
            gradient = brush.gradient()

            rect_item.setRect(*rect)
            pen.setColor(QColor(*edge_color))
            pen.setWidth(width)
            rect_item.setPen(pen)
            gradient.setColorAt(0.0, QColor(*color))

        else:
            rect_item = GraphicsRectItem(*rect)
            self.scene.addItem(rect_item)

            gradient = QLinearGradient(20, 180, 120, 260)
            gradient.setColorAt(0.0, QColor(*color))
            rect_item.setBrush(gradient)

            pen = QPen(QColor(*edge_color))
            pen.setWidth(width)
            rect_item.setPen(pen)

        rect_item.setFlags(QGraphicsItem.ItemIsSelectable)
        # rect_item.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
        rect_item.setData(0,
            {
                'name':name,
                'item_name':item_name
            }
        )

        # set and add tool tip
        self.set_tool_tip_item(
            rect_item,
            name,
            item_name,
            rect,
            color,
            edge_color,
            width
        )

        self.add_tool_tip_item(
            None,
            name,
            item_name,
            rect,
            color,
            edge_color,
            width
        )

        # set dict
        self.picker_items[name] = {
            'item_name':item_name,
            'rect':rect,
            'color':color,
            'edge_color':edge_color,
            'width':width
        }

        return rect_item

    def add_drop_items(self, event):
        selected_objects = cmds.ls(os=True)
        for obj in selected_objects:
            nss = ':'.join(obj.split(':')[0:-1]) + ':'
            obj = obj.replace(nss, '')
            self.add_pick_item(
                name=obj,
                item_name=obj,
                rect=[
                    -self.scene_size.width()/2+event.pos().x()-25,
                    -self.scene_size.height()/2+event.pos().y()-25,
                    50,
                    50],
                color=[128, 220, 190],
                edge_color=[196, 255, 220],
                width=4)
            self.setting_widget.get_located_items()

        self.save_items[WINDOW_OPTIONVAR]['PICKER_ITEMS'] = self.picker_items
        save_optionVar(save_items=self.save_items)

    ##################
    # remove items
    ##################
    def remove_items(self):
        # self.selection_changed()
        self.selection_list_changed()
        self.get_located_items()
        self.setting_widget.get_listed_items()
        # list
        for index, name in zip(self.seleced_item_indexes, self.selected_item_names):
            self.picker_items.pop(name)
            self.scene.removeItem(self.selected_scene_items[name])
            index = self.items_model.indexFromItem(self.setting_widget.list_items[name])
            self.items_model.removeRow(index.row())

        self.save_items[WINDOW_OPTIONVAR]['PICKER_ITEMS'] = self.picker_items
        save_optionVar(save_items=self.save_items)

    def remove_all_items(self):
        self.get_located_items()
        self.setting_widget.get_listed_items()
        for name, rect_item in self.selected_scene_items.items():
            index = self.items_model.indexFromItem(self.setting_widget.list_items[name])
            self.items_model.removeRow(index.row())

            self.scene.removeItem(rect_item)

        self.selected_scene_items = OrderedDict()
        self.get_located_items()
        self.setting_widget.get_listed_items()

    ##################
    # tool tips
    ##################
    def add_tool_tip_item(self, item=None, name='rectTest', item_name=None, rect=[-100, -100, 80, 100], color=[128, 220, 190], edge_color=[196, 255, 220], width=4):
        # tool tipを更新するために個別化
        if name in self.setting_widget.list_items.keys():
            item = self.setting_widget.list_items[name]

        if not item:
            item = QStandardItem(name)
            self.items_model.appendRow(item)

        keys_ = ['Name', 'ItemName', 'Geometory', 'Color', 'EdgeColor', 'width']
        values_ = [name, item_name, rect, color, edge_color, width]
        tool_tip = ['<p>{}'.format(key_) + ':' + '<b>{}</b></p>'.format(val_) for key_, val_ in zip(keys_, values_)]
        item.setToolTip('\n'.join(tool_tip))

    def set_tool_tip_item(self, rect_item, name, item_name, rect, color, edge_color, width):
        # tool tipを更新するために個別化
        keys_ = ['Name', 'ItemName', 'Geometory', 'Color', 'EdgeColor', 'width']
        values_ = [name, item_name, rect, color, edge_color, width]
        tool_tip = ['<p>{}'.format(key_) + ':' + '<b>{}</b></p>'.format(val_) for key_, val_ in zip(keys_, values_)]
        rect_item.setToolTip('\n'.join(tool_tip))
        return tool_tip

    #################
    # events
    #################
    def _fitInView(self):
        r = self.scene.sceneRect()
        self.fitInView(r, Qt.KeepAspectRatio)

    def resizeEvent(self, event):
        self.scene_size = self.size()
        self._fitInView()
        super(GraphicsView, self).resizeEvent(event)

    def updateCenter(self):
        center = self.geometry().center()
        self.center = self.mapToScene(center)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.viewport().setCursor(Qt.ArrowCursor)

        elif event.button() == Qt.MidButton:
            self.setDragMode(QGraphicsView.ScrollHandDrag)

            self.viewport().setCursor(Qt.ClosedHandCursor)
            handmade_event = QMouseEvent(QEvent.MouseButtonPress,QPointF(event.pos()),Qt.LeftButton,event.buttons(),Qt.KeyboardModifiers())
            self.mousePressEvent(handmade_event)

        super(GraphicsView, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.viewport().setCursor(Qt.ArrowCursor)
            self.setDragMode(QGraphicsView.RubberBandDrag)


        elif event.button() == Qt.MidButton:
            self.setDragMode(QGraphicsView.NoDrag)

            self.viewport().setCursor(Qt.OpenHandCursor)
            handmade_event = QMouseEvent(QEvent.MouseButtonRelease,QPointF(event.pos()),Qt.LeftButton,event.buttons(),Qt.KeyboardModifiers())
            self.mouseReleaseEvent(handmade_event)

        super(GraphicsView, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        super(GraphicsView, self).mouseMoveEvent(event)

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            factor = 1.25
            self.zoom += 1
        else:
            factor = 0.8
            self.zoom -= 1

        if self.zoom < 5:
            self.zoom = 5
        elif self.zoom > -5:
            self.zoom = -5

        if self.zoom > 0 or self.zoom < 0:
            self.scale(factor, factor)
        elif self.zoom == 0:
            self._fitInView()

        super(GraphicsView, self).wheelEvent(event)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.setAccepted(True)
            self.dragOver = True
            self.update()

        super(GraphicsView, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        # print('move event', event)
        super(GraphicsView, self).dragMoveEvent(event)

    def dropEvent(self, event):
        data = event.mimeData().text()
        if data: self.add_drop_items(event)
        event.accept()

    def selection_changed(self):
        self.names = list()
        self.item_names = list()
        self._current_selection = self.scene.selectedItems()
        self.nss = self.nss_qle.text()
        if not self._current_selection:
            cmds.select(cl=True)
            self.names = list()
            self.item_names = list()

        for sel in self._current_selection:
            name = sel.data(0)['name']
            if not name in self.names:
                self.names.append(name)

            item_name = sel.data(0)['item_name']
            if not item_name in self.item_names:
                self.item_names.append(item_name)

        # view select
        add_nss_list = [self.nss + n for n in self.item_names if cmds.objExists(self.nss + n)]
        if add_nss_list: cmds.select(add_nss_list, r=True)

        # tree select
        self.setting_widget.names = self.names
        self.setting_widget.item_names = self.item_names
        self.setting_widget.tree_selection_changed()
        # print('self.setting_widget.list_items', self.setting_widget.list_items)

        panel = cmds.getPanel(withFocus=True)
        cmds.setFocus('MayaWindow')

    def selection_list_changed(self):
        self.seleced_item_indexes = self.items_tree_view.selectionModel().selectedIndexes()
        selected_items = [self.items_model.itemFromIndex(sel_idx) for sel_idx in self.seleced_item_indexes]
        self.selected_item_names = [item.text() for item in selected_items]
        # print('self.selected_item_names', self.selected_item_names)

    def get_located_items(self):
        items = self.scene.items()
        for item in items:
            if 'GraphicsRectItem' == item.__class__.__name__:
                name = item.data(0)['name']
                self.selected_scene_items[name] = item


class SettingWidget(QWidget):
    def __init__(self, parent=None):
        super(SettingWidget, self).__init__(parent)

        self.v_layout = QVBoxLayout(self)
        self.setLayout(self.v_layout)

        self.setting_widget_stock = OrderedDict()
        self.item_widget_stock = OrderedDict()

        self.default_settings = OrderedDict()
        self.default_settings['object_name'] = OrderedDict()
        self.default_settings['object_name']['item_name'] = None
        self.default_settings['object_name']['rect'] = [0, 0, 0, 0]
        self.default_settings['object_name']['color'] = [0, 0, 0]
        self.default_settings['object_name']['edge_color'] = [1, 1, 1]
        self.default_settings['object_name']['width'] = 1

        self.add_layouts()

        self.view = None
        self.scene = None
        self.items_tree_view = None
        self.items_model = None
        self.selected_items = None
        self.list_items = OrderedDict()
        self.names = None
        self.item_names = None

        self.rect_edit_mode = None

        self.save_items = OrderedDict()
        # load optionVar
        load_settings = load_optionVar(key=WINDOW_OPTIONVAR)
        if load_settings:
            self.save_items[WINDOW_OPTIONVAR] = load_settings
        else:
            self.save_items[WINDOW_OPTIONVAR] = OrderedDict()

    def add_layouts(self):
        for object_name, items_values in self.default_settings.items():
            self.object_name_h_layout = QHBoxLayout(self)
            self.v_layout.addLayout(self.object_name_h_layout)

            # self.object_name_label = QLabel(object_name)
            # self.object_name_h_layout.addWidget(self.object_name_label)

            self.setting_widget_stock[object_name] = OrderedDict()

            for name, value in items_values.items():
                self.h_layout = QHBoxLayout(self)
                self.v_layout.addLayout(self.h_layout)

                if name == 'item_name':
                    set_name = 'Item Name'
                elif name == 'rect':
                    set_name = 'Rect'
                elif name == 'color':
                    set_name = 'Color'
                elif name == 'edge_color':
                    set_name = 'Edge Color'
                elif name == 'width':
                    set_name = 'Width'

                name_label = QLabel(str(set_name))
                self.h_layout.addWidget(name_label)

                value_label = QLabel(str(value))
                self.h_layout.addWidget(value_label)

                value_widget = QPushButton('Edit')
                self.h_layout.addWidget(value_widget)
                if (name == 'rect'):
                    origin_color_f = value_widget.palette().button().color()
                    origin_color = [origin_color_f.red(), origin_color_f.green(), origin_color_f.blue()]
                    # origin_color = [c for c in origin_color]
                    value_widget.clicked.connect(partial(self.set_rect, name=name, value_widget=value_widget, value_label=value_label, origin_color=origin_color))

                if (name == 'color'
                    or name == 'edge_color'):
                    value_widget.clicked.connect(partial(self.set_color, name=name, value_widget=value_widget, value_label=value_label))

                if (name == 'width'):
                    value_widget.clicked.connect(partial(self.set_width, name=name, widget=value_label))

                self.setting_widget_stock[object_name][name] = {
                    'label':value_label,
                    'widget':value_widget
                }

            delete_btn = QPushButton('Delete')
            self.v_layout.addWidget(delete_btn)

        # print('self.setting_widget_stock', self.setting_widget_stock)

    def get_selected_settings(self, selected_items=None):
        self.selected_items = selected_items
        for sel_item in self.selected_items:
            for name, widget_item in self.setting_widget_stock['object_name'].items():
                try:
                    widget_item['label'].setText(str(self.view.picker_items[sel_item][name]))

                    if (name == 'color'
                        or name == 'edge_color'):
                        bg_color = "background-color: rgb({}, {}, {});".format(*self.view.picker_items[sel_item][name])
                        widget_item['widget'].setStyleSheet(
                            '{}'.format(bg_color)
                        )

                except KeyError:
                    pass

        self.get_located_items()
        # print('self.scene.items()', self.item_widget_stock)
        # print('get_located_items', self.get_located_items())

    def set_rect(self, name=None, value_widget=None, value_label=None, origin_color=None):
        # print(self.items_model.rowCount())
        # print('origin_color', origin_color)
        # print(self.get_listed_items())
        self.get_listed_items()
        if not self.rect_edit_mode:
            self.rect_edit_mode = True
        else:
            self.rect_edit_mode = False

        if self.rect_edit_mode:
            self.size_dialog = SizeDialog(self.view)
            self.size_dialog.rect_items = [self.item_widget_stock[list_name] for list_name in self.selected_items]
            self.size_dialog.init_values()
            self.size_dialog.show()
            for list_name, list_item in self.list_items.items():
                if not self.selected_items:
                    self.rect_edit_mode = False
                    return

                if list_name in self.selected_items:
                    rect_item = self.item_widget_stock[list_name]
                    # rect_item.setFlags(QGraphicsItem.ItemIsSelectable)
                    rect_item.rect_move = True # GraphicsRectItemのメソッドに代入する

                else:
                    rect_item = self.item_widget_stock[list_name]
                    rect_item.setOpacity(0.5)

                    list_item.setEditable(False)
                    idx = list_item.index()
                    self.items_model.setData(idx, QBrush(QColor(128, 128, 128)), Qt.BackgroundRole)

            bg_color = "background-color: rgb({}, {}, {});".format(72, 54, 255)
            value_widget.setText('Edit Mode')

        else:
            self.size_dialog.close()
            for name, rect_item in self.item_widget_stock.items():
                # rect = [rect_item.rect().x(), rect_item.rect().y(), rect_item.rect().width(), rect_item.rect().height()]
                rect = rect_item.mapRectToScene(rect_item.rect())
                rect = [rect.x(), rect.y(), rect.width(), rect.height()]
                if name in self.view.picker_items.keys():
                    self.view.picker_items[name]['rect'] = rect
                    self.list_items[name].setEditable(True)
                    idx = self.list_items[name].index()
                    self.items_model.setData(idx, QBrush(QColor(43, 43, 43)), Qt.BackgroundRole)

                if name == self.selected_items[-1]:
                    value_label.setText("{}".format(rect))

                rect_item.setFlags(QGraphicsItem.ItemIsSelectable)
                rect_item.setOpacity(1.0)
                rect_item.rect_move = False

            bg_color = "background-color: rgb({}, {}, {});".format(*origin_color)
            value_widget.setText('Edit')

        value_widget.setStyleSheet(
            '{}'.format(bg_color)
        )

        self.set_tool_tip_item()

    def set_color(self, name=None, value_widget=None, value_label=None):
        color = QColorDialog.getColor()
        for item in self.selected_items:
            if color.isValid():
                set_color = [c for c in color.getRgb()[0:-1]]
                value_widget.setStyleSheet("background-color: rgb({}, {}, {})".format(*set_color))
                value_label.setText("{}".format(set_color))
                # print('self.item_widget_stock', self.item_widget_stock)
                rect_item = self.item_widget_stock[item]
                pen = rect_item.pen()
                brush = rect_item.brush()
                gradient = brush.gradient()
                if name == 'edge_color':
                    pen.setColor(QColor(*set_color))
                    rect_item.setPen(pen)
                if name == 'color':
                    gradient.setColorAt(0.0, QColor(*set_color))
                self.view.picker_items[item][name] = set_color

        self.set_tool_tip_item()

    def set_width(self, name=None, widget=None):
        value = int(widget.text())
        set_int, status = QInputDialog.getInt(self, 'Set Width', '', value)
        if status:
            for item in self.selected_items:
                rect_item = self.item_widget_stock[item]
                pen = rect_item.pen()
                brush = rect_item.brush()
                gradient = brush.gradient()
                widget.setText(str(set_int))
                if name == 'width':
                    pen.setWidth(set_int)
                    rect_item.setPen(pen)
                self.view.picker_items[item][name] = set_int

        self.set_tool_tip_item()

    def get_located_items(self):
        items = self.scene.items()
        for item in items:
            if 'GraphicsRectItem' == item.__class__.__name__:
                name = item.data(0)['name']
                self.item_widget_stock[name] = item
        # print('self.item_widget_stock', self.item_widget_stock)

    def get_listed_items(self):
        rows = self.items_model.rowCount()
        self.list_items = OrderedDict()
        for row in range(rows):
            idx = self.items_model.index(row, 0)
            item = self.items_model.itemFromIndex(idx)
            self.list_items[item.text()] = item

    def set_tool_tip_item(self):
        # tool tip picker
        for name, values in self.view.picker_items.items():
            rect_item = self.item_widget_stock[name]
            self.view.set_tool_tip_item(
                rect_item,
                name,
                values['item_name'],
                values['rect'],
                values['color'],
                values['edge_color'],
                values['width']
            )

        # tool tip list
        seleced_indexes = self.items_tree_view.selectionModel().selectedIndexes()
        selected_items = [self.items_model.itemFromIndex(sel_idx) for sel_idx in seleced_indexes]
        for item in selected_items:
            name = item.text()
            item_values = self.view.picker_items[name]
            self.view.add_tool_tip_item(item=item, name=name, **item_values)

        for index in seleced_indexes:
            self.items_tree_view.selectionModel().select(index, QItemSelectionModel.Select | QItemSelectionModel.Rows) # indexから選択

        self.update_items()

        # save items
        self.save_items[WINDOW_OPTIONVAR]['PICKER_ITEMS'] = self.view.picker_items
        save_optionVar(save_items=self.save_items)

    def tree_selection_changed(self):
        self.get_listed_items()
        # print('len(self.names)', len(self.names))
        seleced_indexes = [self.list_items[n].index() for n in self.names]
        # seleced_indexes = [self.items_model.itemFromIndex(idx) for idx in indexes]
        self.items_tree_view.selectionModel().clear()
        for index in seleced_indexes:
            self.items_tree_view.selectionModel().select(index, QItemSelectionModel.Select | QItemSelectionModel.Rows) # indexから選択

    def update_items(self):
        self.scene.update()
        self.items_tree_view.update()

class SizeDialog(MayaQWidgetDockableMixin, QDialog):
    def __init__(self, rect_items=None):
        super(SizeDialog, self).__init__(rect_items)

        self.setWindowTitle("Set Size")

        self.rect_items = None
        self.rect_size = [1, 1]

        layout = QHBoxLayout(self)
        self.setLayout(layout)

        self.width_qspbx = QDoubleSpinBox()
        self.height_qspbx = QDoubleSpinBox()

        self.width_qspbx.setRange(1, 50)
        self.height_qspbx.setRange(1, 50)

        layout.addWidget(QLabel('Width'))
        layout.addWidget(self.width_qspbx)
        layout.addWidget(QLabel('Height'))
        layout.addWidget(self.height_qspbx)

        self.width_qspbx.valueChanged.connect(self.set_size)
        self.height_qspbx.valueChanged.connect(self.set_size)

        self.store_rect = OrderedDict()

    def init_values(self):
        self.store_rect = OrderedDict()
        # print('self.rect_items', self.rect_items)
        if self.rect_items:
            for rect_item in self.rect_items:
                name = rect_item.data(0)['name']
                rect = rect_item.mapRectToScene(rect_item.rect())
                rect = [rect.x(), rect.y(), rect.width(), rect.height()]
                self.store_rect[name] = rect

            init_rect_item = self.rect_items[-1]
            init_width = self.store_rect[init_rect_item.data(0)['name']][2]
            init_height = self.store_rect[init_rect_item.data(0)['name']][3]

            self.width_qspbx.setValue(init_width)
            self.height_qspbx.setValue(init_height)

    def set_size(self):
        width, height = self.width_qspbx.value(), self.height_qspbx.value()
        for rect_item in self.rect_items:
            # init_x = self.store_rect[rect_item.data(0)['name']][0]
            # init_y = self.store_rect[rect_item.data(0)['name']][1]

            # rect = rect_item.mapRectToScene(rect_item.rect())
            rect = rect_item.rect()
            rect = [rect.x(), rect.y(), width, height]
            rect_item.setRect(*rect)

class VideoPlayer(QVideoWidget):
    def __init__(self, parent=None):
        super(VideoPlayer, self).__init__(parent)

        self._player = QMediaPlayer()
        self._playlist = QMediaPlaylist()
        self._stopped = True

    # プレイリストに動画を追加
    def addMedia(self, media_file):
        media_content = QMediaContent(QUrl.fromLocalFile(media_file))
        self._playlist.addMedia(media_content)

    # クリックでポーズ・再生の切り替え
    def mousePressEvent(self, event):
        if self._stopped:
            self.play()
        else:
            self._player.pause()
            self._stopped = True

    # ダブルクリックで動画を読み込み，再生
    def mouseDoubleClickEvent(self, event):
        self._player.setVideoOutput(self)
        self._player.setPlaylist(self._playlist)
        self.play()

    def play(self):
        self._player.play()
        self._stopped = False

    def openAndPlay(self):
        self._player.setVideoOutput(self)
        self._player.setPlaylist(self._playlist)
        self.play()



def _mirror(mirrors=['_L', '_R'], replace_src=None):
    mirrors_src_found = re.findall(mirrors[0], replace_src)

    renamed_char = replace_src.replace(mirrors[0], mirrors[1])

    if len(mirrors_src_found) > 1:
        splited_src = replace_src.split('_')
        splited_mir_src = [mir for mir in mirrors[0].split('_') if not mir == '']
        splited_mir_dst = [mir for mir in mirrors[1].split('_') if not mir == '']
        replace_src_idx = 0
        for spl_d in splited_src:
            for spl_ms in splited_mir_src:
                if spl_d == spl_ms:
                    replace_src_idx = splited_src.index(spl_d)
                    break

        combined = []
        for i, repl_d in enumerate(splited_src):
            if i == replace_src_idx:
                repl_d = ''.join(splited_mir_dst)

            combined.append(repl_d)

        renamed_char = '_'.join(combined)

    return renamed_char

def save_optionVar(save_items=None):
    for key, value in save_items.items():
        cmds.optionVar(sv=[key, str(value)])

def load_optionVar(key=None):
    return eval(cmds.optionVar(q=key)) if cmds.optionVar(ex=key) else False

def json_transfer(fileName=None, operation=None, export_values=None, export_type=None, import_type=None):
    if operation == 'export':
        if not export_type:
            with open(fileName, "w") as f:
                json.dump(export_values, f)

        if export_type == 'utf-8':
            with codecs.open(fileName, 'w', encoding='utf-8') as f:
                json.dump(export_values, f, indent=4, ensure_ascii=False)

        elif export_type == 'pickle':
            s = base64.b64encode(pickle.dumps(export_values)).decode("utf-8")
            d = {"pickle": s}
            with open(fileName, "w") as f:
                json.dump(d, f)

    elif operation == 'import':
        if not import_type:
            with open(fileName) as f:
                return json.load(f)

        elif import_type == 'utf-8':
            with codecs.open(fileName, 'r', encoding='utf-8') as f:
                return json.load(f, 'utf-8', object_pairs_hook=OrderedDict)

        elif import_type == 'pickle':
            with open(fileName) as f:
                d = json.load(f)
            s = d["pickle"]
            return pickle.loads(base64.b64decode(s.encode()))

###########################
# SetTimeFromKey
###########################
class SetTimeFromKey(MayaQWidgetDockableMixin, QMainWindow):
    # QMainWindowを継承するとmenubarの使える幅が広い
    def __init__(self, *args, **kwargs):
        super(SetTimeFromKey, self).__init__(*args, **kwargs)

        self.time_range = list()

        self.clipboard = QClipboard()

        TOOL_VERSION = '1.0.0'
        PROJ = 'wizard2'
        WINDOW_TITLE = 'Set Time From Key'
        WINDOW_OPTIONVAR = WINDOW_TITLE.replace(' ', '_')

        self.setWindowTitle('{}:{}:{}'.format(WINDOW_TITLE, TOOL_VERSION, PROJ))

    def layout(self):
        # 全体の大きさの変更
        self.setGeometry(10, 10, 300, 100) # (left, top, width, height)

        self.main_widget = QWidget() # 1
        self.setCentralWidget(self.main_widget)

        self.main_qvbl = QVBoxLayout()
        self.main_widget.setLayout(self.main_qvbl) # 2 上下にウィジェットを追加するレイアウトを追加

        self.main_qhbl = QHBoxLayout()
        self.main_qvbl.addLayout(self.main_qhbl) # 3 左右にウィジェットを追加するレイアウトを追加

        self.main_qgl = QGridLayout()
        self.main_qvbl.addLayout(self.main_qgl)

    def widgets(self):
        # QPushButton
        self.set_cur_time_btn = QPushButton('Save Current Time')
        self.set_cur_time_btn.clicked.connect(partial(self.save_history))
        self.main_qhbl.addWidget(self.set_cur_time_btn)

        # QTreeView
        self.main_tree = QTreeView()
        self.main_tree.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.main_tree.clicked.connect(self.get_tree_items)
        self.main_qhbl.addWidget(self.main_tree)

        # QStandardItemModel
        self.main_tree_model = QStandardItemModel()
        self.main_tree_model.setColumnCount(1)
        self.main_tree_model.setHeaderData(0, Qt.Horizontal, 'History')
        self.main_tree.setModel(self.main_tree_model)

        # QTreeView connect context menu
        self.main_tree.setContextMenuPolicy(Qt.CustomContextMenu) # QTreeViewにコンテキストメニューを追加する設定
        self.main_tree.customContextMenuRequested.connect(self.list_menu_available_sender) # QTreeViewで設定するコンテキストメニュー

        # QPushButton
        self.set_start_btn = QPushButton('|<')
        self.set_start_btn.clicked.connect(partial(set_time_from_key, 'min'))
        self.set_start_btn.setToolTip(u'Set the start time of the playback range')
        self.main_qgl.addWidget(self.set_start_btn, 0, 0)

        self.set_both_btn = QPushButton('|<  >|')
        self.set_both_btn.clicked.connect(partial(set_time_from_key, None))
        self.set_start_btn.setToolTip(u'Set the both times of the playback range')
        self.main_qgl.addWidget(self.set_both_btn, 0, 1)

        self.set_end_btn = QPushButton('>|')
        self.set_end_btn.clicked.connect(partial(set_time_from_key, 'max'))
        self.set_start_btn.setToolTip(u'Set the end time of the playback range')
        self.main_qgl.addWidget(self.set_end_btn, 0, 2)

        self.set_start_time_btn = QPushButton('|<<')
        self.set_start_time_btn.clicked.connect(partial(set_time_slider, 'start'))
        self.main_qgl.addWidget(self.set_start_time_btn, 1, 0)

        self.set_both_time_btn = QPushButton('|<< >>|')
        self.set_both_time_btn.clicked.connect(partial(set_time_slider, 'both'))
        self.main_qgl.addWidget(self.set_both_time_btn, 1, 1)

        self.set_end_time_btn = QPushButton('>>|')
        self.set_end_time_btn.clicked.connect(partial(set_time_slider, 'end'))
        self.main_qgl.addWidget(self.set_end_time_btn, 1, 2)

    def buildUI(self):
        # UI
        self.layout()
        self.widgets()

        # initial set
        self.save_history()

    def copy_times(self):
        self.clipboard.setText('\n'.join(self.cur_items))

    def list_menu_available_sender(self, pos):
        sender = self.sender()
        # menus
        self.context_menu = QMenu(sender)

        # addAction
        context_menu = OrderedDict()
        context_menu['Set Playback Range'] = {'cmd':partial(self.set_time_from_tree)}
        context_menu['Copy Clipboard'] = {'cmd':partial(self.copy_times)}

        for menu_name, menu_cmd in context_menu.items():
            action = self.context_menu.addAction(menu_name)
            action.triggered.connect(menu_cmd['cmd'])

        # QMenuの表示
        self.context_menu.exec_(sender.mapToGlobal(pos))

    def get_tree_items(self):
        sender = self.sender()
        indexes = sender.selectionModel().selectedIndexes()
        self.cur_items = [index.data() for index in indexes]

    def set_time_from_tree(self):
        set_time = self.cur_items[0]
        start_val, min_val = set_time.split('--')[0].split('|')
        max_val, end_val = set_time.split('--')[1].split('|')

        cor_start_val = float(replace_square_brackets(start_val))
        cor_min_val = float(replace_square_brackets(min_val))
        cor_max_val = float(replace_square_brackets(max_val))
        cor_end_val = float(replace_square_brackets(end_val))
        cmds.playbackOptions(ast=cor_start_val, min=cor_min_val, max=cor_max_val, aet=cor_end_val)

    def save_history(self, *args, **kwargs):
        self.time_range = get_time_slider()
        self.insert_row()

    def insert_row(self, *args, **kwargs):
        text = '[{}]|[{}]--[{}]|[{}]'.format(
            self.time_range[2],
            self.time_range[0],
            self.time_range[1],
            self.time_range[3],
            )
        std_item = QStandardItem(text)
        std_item.setEditable(False)
        self.main_tree_model.insertRow(0, std_item)

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
    ui = PickerAnimTools()
    ui.buildUI()
    ui.show(dockable=True)

"""
for method in dir(Qt):
    if 'Modifier' in method:
        print(method)

for method in dir(QGraphicsView):
    if 'scene' in method:
        print(method)

for method in dir(QPushButton):
    if 'set' in method:
        print(method)

for method in dir(QGraphicsScene):
    if 'video' in method:
        print(method)

for method in dir(QGraphicsRectItem):
    if 'set' in method:
        print(method)

QGridLayout.setAlignment.__doc__

"""
