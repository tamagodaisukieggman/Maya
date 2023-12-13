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

import rig.avatarReferenceTool.commands as avatarReferenceTool
reload(avatarReferenceTool)

import rig.avatarReferenceTool.simple_picker.ui as avatarReferenceToolPicker
reload(avatarReferenceToolPicker)

maya_version = cmds.about(v=True)

TOOL_VERSION = '1.0.0'
PROJ = 'wizard2'
WINDOW_TITLE = 'Avatar Reference Tool'
WINDOW_OPTIONVAR = WINDOW_TITLE.replace(' ', '_')
try:
    DIR_PATH = '/'.join(__file__.replace('\\', '/').split('/')[0:-1])
except:
    DIR_PATH = ''

AVATAR_COLLECTION_FILE = 'c:/cygames/wiz2/tools/maya/scripts/rig/avatarReferenceTool/data/avatar_collection.json'

# from P4 import P4, P4Exception
# # p4のインスタンスを作っておく
# p4 = P4()

try:
    if 'ssl:wizard2-perforce.cygames.jp:1666' != avatarReferenceTool.WIZARD2_P4V_PORT:
        print('\n>>P4V Information>>')
        print('古い設定が読み込まれている可能性があります。\nリストを更新する際は、手動で\n{}\nをチェックアウトしてから更新してください。\nウィンドウを閉じたらリバートをお願いします。\n'.format(AVATAR_COLLECTION_FILE))
        print('|現在の設定|\nServer:{}\nUser:{}\nWorkspace:{}\n'.format(p4.port, p4.user, p4.client))
        print('|wizard2のポート|\np4.port:{}\n'.format(avatarReferenceTool.WIZARD2_P4V_PORT))
except:
    print(traceback.format_exc())

"""
import rig.avatarReferenceTool.ui as avatarReferenceToolUI
reload(avatarReferenceToolUI)
fbx_mxui = avatarReferenceToolUI.AvatarReferenceTool()
fbx_mxui.buildUI()
fbx_mxui.show(dockable=True)

# ファイル捜査で設定を書き出し
import rig.avatarReferenceTool.commands as avatarReferenceToolCmd
reload(avatarReferenceToolCmd)
avatarReferenceToolCmd.export_avatar_collection()
"""

class AvatarReferenceTool(MayaQWidgetDockableMixin, QMainWindow):
    # QMainWindowを継承するとmenubarの使える幅が広い
    def __init__(self, *args, **kwargs):
        super(AvatarReferenceTool, self).__init__(*args, **kwargs)

        self.setWindowTitle('{}:{}:{}'.format(WINDOW_TITLE, TOOL_VERSION, PROJ))

        self.ui_items = {}

        self.data_path = DIR_PATH + '/data'

        self.set_path_dict = {
            'import_settings':{
                'title':'Import Settings',
                'file_mode':'open',
                'file_filter':'json Files (*.json);;All Files (*.*)'
            },
            'export_settings':{
                'title':'Export Settings',
                'file_mode':'save',
                'file_filter':'json Files (*.json);;All Files (*.*)'
            },
        }

        self.reference_dict = avatarReferenceTool.avatar_collection()

        try:
            self.reference_list = avatarReferenceTool.avatar_parts()
        except Exception as e:
            print(traceback.format_exc())
            print('{} からパーツ名を読み込みます.'.format(__file__))
            self.reference_list = OrderedDict({
                "face": "顔",
                "eyebrow": "眉",
                "hair": "髪",
                "onepiece": "ワンピース",
                "tops": "トップス",
                "bottoms": "ボトムス",
                "shoes": "靴",
                "accessory": "アクセサリ",
                "costume": "なりきりセット"
            })

        # self.reference_list = OrderedDict({
        #     'face':'顔',
        #     'eyebrow':'眉',
        #     'hair':'髪',
        #     'onepiece':'ワンピース',
        #     'tops':'トップス',
        #     'bottoms':'ボトムス',
        #     'shoes':'靴',
        #     'accessory':'アクセサリ',
        #     'costume':'なりきりセット'
        # })

        self.reference_btn_dict = OrderedDict()
        self.reference_set_dict = OrderedDict()
        self.reference_set_value_dict = OrderedDict()
        self.reference_cbox_dict = OrderedDict()
        self.reference_cbox_values_list = list()

        self.save_keys = [
            'reference_set_dict',
            'reference_cbox_dict'
        ]

        self.errors = OrderedDict()

        self.p4v_status = None

        self.picker = None
        self.picker_items = OrderedDict()
        self.picker_objects = OrderedDict()

        self.prop_dialog = None

    def layout(self):
        # 全体の大きさの変更
        self.setGeometry(10, 10, 500, 100) # (left, top, width, height)

        self.main_widget = QWidget() # 1
        self.setCentralWidget(self.main_widget)

        self.main_qvbl = QVBoxLayout()
        self.main_widget.setLayout(self.main_qvbl) # 2 上下にウィジェットを追加するレイアウトを追加

    def widgets(self):
        self.update_fbx_qbtn = QPushButton('読み込む着せ替えのリストの更新')
        self.main_qvbl.addWidget(self.update_fbx_qbtn)
        self.update_fbx_qbtn.clicked.connect(partial(self.update_fbx_list))

        self.import_settings_qbtn = QPushButton('設定の読み込み')
        self.main_qvbl.addWidget(self.import_settings_qbtn)
        self.import_settings_qbtn.clicked.connect(partial(self.import_settings))

        self.check_from_current_scene_qbtn = QPushButton('現在のシーンからパーツを設定する')
        self.main_qvbl.addWidget(self.check_from_current_scene_qbtn)
        self.check_from_current_scene_qbtn.clicked.connect(partial(self.check_from_current_scene))

        self.all_check_qcbox = QCheckBox('一括チェック')
        self.main_qvbl.addWidget(self.all_check_qcbox)
        # self.all_check_qcbox.setChecked(True)
        self.all_check_qcbox.stateChanged.connect(self.all_check_func)

        for part, part_text in self.reference_list.items():
            # print('part, part_text', part, part_text)
            # encoded_text = part_text.encode("utf-8")
            # detected_encoding = chardet.detect(encoded_text)
            # print('detected_encoding', detected_encoding)

            try:
                type_path = self.reference_dict[part]

                self.parts_widget = PartsWidget(self)
                self.parts_widget.main_qcbox.setText(part_text)
                self.main_qvbl.addWidget(self.parts_widget)

                self.parts_widget.main_change_qdialog.items = type_path
                self.reference_btn_dict[part] = self.parts_widget.main_change_qdialog.cur_btn
                self.reference_cbox_dict[part] = self.parts_widget.main_change_qdialog.cur_cbx
                self.parts_widget.main_change_qdialog.add_items()
            except Exception as e:
                self.errors[part] = traceback.format_exc()

        self.avatar_update_qbtn = QPushButton('Avatar Update')
        self.main_qvbl.addWidget(self.avatar_update_qbtn)
        self.avatar_update_qbtn.clicked.connect(partial(self.avatar_update))

        self.avatar_picker_qbtn = QPushButton('Picker')
        self.main_qvbl.addWidget(self.avatar_picker_qbtn)
        self.avatar_picker_qbtn.clicked.connect(partial(self.show_picker))

        self.avatar_prop_qbtn = QPushButton('Prop')
        self.main_qvbl.addWidget(self.avatar_prop_qbtn)
        self.avatar_prop_qbtn.clicked.connect(partial(self.show_prop_list))

        self.export_settings_qbtn = QPushButton('現在の設定を保存')
        self.main_qvbl.addWidget(self.export_settings_qbtn)
        self.export_settings_qbtn.clicked.connect(partial(self.export_settings))


        # print('self.reference_btn_dict', self.reference_btn_dict)

    def buildUI(self):
        # UI
        self.layout()
        self.widgets()

        # load setting
        self.load_setting()

        # set loaded
        self.set_loaded()

        # reload
        self.reload_set_dict()

        # error_dialog = ErrorDialog()
        # if self.errors:
        #     error_dialog.errors = self.errors
        #     error_dialog.build()
        #     error_dialog.show()

    def reload_set_dict(self):
        for type, btn in self.reference_btn_dict.items():
            if btn.text() in self.reference_dict[type].keys():
                path = self.reference_dict[type][btn.text()]
            else:
                path = None

            self.reference_set_dict[type] = [btn.text(), path]

        # print('self.reference_set_dict', self.reference_set_dict)

        self.save_items()

    def save_items(self):
        self.ui_items[WINDOW_OPTIONVAR] = OrderedDict()

        for key in self.save_keys:
            # reference_set_dict
            if key == 'reference_set_dict':
                self.ui_items[WINDOW_OPTIONVAR][key] = self.reference_set_dict

            # reference_cbox_dict
            elif key == 'reference_cbox_dict':
                self.reference_cbox_values_list = [cbox.isChecked() for part, cbox in self.reference_cbox_dict.items()]
                self.ui_items[WINDOW_OPTIONVAR][key] = self.reference_cbox_values_list

        self.save_setting()

    def save_setting(self):
        save_optionVar(self.ui_items)

    def load_setting(self):
        get_load_setting = load_optionVar(key=WINDOW_OPTIONVAR)
        if get_load_setting:
            self.ui_items[WINDOW_OPTIONVAR] = get_load_setting
        else:
            self.ui_items[WINDOW_OPTIONVAR] = OrderedDict()

        for key in self.save_keys:
            if not key in self.ui_items[WINDOW_OPTIONVAR].keys():
                self.ui_items[WINDOW_OPTIONVAR][key] = OrderedDict()

            if get_load_setting:
                if key == 'reference_set_dict':
                    self.reference_set_value_dict = get_load_setting[key]

                elif key == 'reference_cbox_dict':
                    self.reference_cbox_values_list = get_load_setting[key]

        # print('self.reference_set_dict', self.reference_set_dict)
        # print('self.reference_cbox_dict', self.reference_cbox_dict)
        # print('self.reference_cbox_values_list', self.reference_cbox_values_list)
        #
        # # set items
        # try:
        #     [ui_item.setText(get_load_setting[str(i).zfill(3)]) for i, ui_item in enumerate(self.ui_get_list)]
        # except:
        #     print(traceback.print_exc())
        #
        # # history items
        # try:
        #     for i, ui_item in enumerate(self.ui_get_list):
        #         if i == 0:
        #             self.history_base_motion = self.ui_items[WINDOW_OPTIONVAR]['history'][str(i).zfill(3)]
        #         elif i == 1:
        #             self.history_combine_motion = self.ui_items[WINDOW_OPTIONVAR]['history'][str(i).zfill(3)]
        #         elif i == 2:
        #             self.history_extract_motion = self.ui_items[WINDOW_OPTIONVAR]['history'][str(i).zfill(3)]
        #         elif i == 3:
        #             self.history_save_motion = self.ui_items[WINDOW_OPTIONVAR]['history'][str(i).zfill(3)]
        # except:
        #     print(traceback.print_exc())

    def set_loaded(self):
        # set check
        cboxes = [cbox for cbox in self.reference_cbox_dict.values()]
        for cbox, state in zip(cboxes, self.reference_cbox_values_list):
            cbox.setChecked(state)

        # print('self.reference_btn_dict', self.reference_btn_dict)
        # print('self.reference_set_dict', self.reference_set_dict)
        # set type
        for part, btn in self.reference_btn_dict.items():
            if part in self.reference_set_value_dict.keys():
                btn.setText(self.reference_set_value_dict[part][0])
                btn.setToolTip(self.reference_set_value_dict[part][1])

    # def closeEvent(self, event):
    #     self.reload_set_dict()
    #     super(AvatarReferenceTool, self).closeEvent(event)

    def avatar_update(self):
        avatarReferenceTool.avatar_update(
            self.reference_set_dict,
            self.reference_cbox_dict
        )

        # self.show_picker()

    def show_picker(self):
        if self.picker_objects:
            for picker in self.picker_objects.values():
                picker.close()

        types = [type for type in self.reference_set_dict.keys()]

        part_picks = OrderedDict()

        for type in types:
            sim_ctrl_sets = '{}_sim_temp_ctrl_sets'.format(type)
            if not cmds.objExists(sim_ctrl_sets):
                continue

            self.picker = avatarReferenceToolPicker.PickerAnimTools()
            self.picker_objects[type] = self.picker

            cmds.select(sim_ctrl_sets, r=True, ne=True)
            ctrls = cmds.pickWalk(d='down')

            part_picks[type] = OrderedDict()

            ctrls.sort()
            for ctrl in ctrls:
                removed_nss = ctrl.replace(type + ':', '')
                splited = removed_nss.split('_')[1::]

                side_picker_name = type + '_' + splited[0]
                part_sets = side_picker_name + '_ctrl_sets'
                # cmds.sets(part_sets, add=sim_ctrl_sets)

                if '_L_' in ctrl or '_R_' in ctrl:
                    side_picker_name = type + '_' + splited[0] + '_' + splited[2]
                    part_side_sets = side_picker_name + '_ctrl_sets'
                    part_picks[type][side_picker_name] = part_side_sets

                else:
                    part_picks[type][side_picker_name] = part_sets

                    # cmds.sets(part_side_sets, add=part_sets)

                    # cmds.sets(ctrl, add=part_side_sets)

            #     cmds.select(part_sets, r=True, ne=True)
            #     part_ctrls = cmds.pickWalk(d='down')
            #
            #
            #
            # self.picker_items

        picker_jsons = OrderedDict()
        text_at_pos = OrderedDict()
        for type, part_sets in part_picks.items():
            self.picker_items = OrderedDict()
            text_at_pos[type] = OrderedDict()
            i = 0
            for sides, picker_sets in part_sets.items():
                x_pos = 220.0 - i*50

                cmds.select(picker_sets, r=True, ne=True)
                ctrls = cmds.pickWalk(d='down')

                ctrls.sort()
                j = 0
                for ctrl in ctrls:
                    removed_nss = ctrl.replace(type + ':', '')

                    part_name = removed_nss.split('_')[1]
                    # if not part_name in text_at_pos.keys():
                    text_at_pos[type][part_name] = [x_pos, -30]

                    if '_R_' in removed_nss:
                        if cmds.objExists('{}:{}'.format(type, removed_nss)):
                            plus_x_pos = x_pos + 25
                            text_at_pos[type][part_name] = [plus_x_pos, -30]

                    self.picker_items[removed_nss] = OrderedDict()
                    self.picker_items[removed_nss]['item_name'] = removed_nss
                    self.picker_items[removed_nss]['rect'] = [x_pos, j*40, 30, 30]
                    if '_L_' in removed_nss:
                        color = [255, 50, 50]
                        edge_color = [255, 100, 100]
                    elif '_R_' in removed_nss:
                        color = [50, 50, 255]
                        edge_color = [100, 100, 255]
                    else:
                        color = [212, 212, 50]
                        edge_color = [255, 255, 100]

                    self.picker_items[removed_nss]['color'] = color
                    self.picker_items[removed_nss]['edge_color'] = edge_color
                    self.picker_items[removed_nss]['width'] = 4

                    j += 1

                i += 1

            type_json = self.data_path + '/{}_picker.json'.format(type)
            avatarReferenceToolPicker.json_transfer(self.data_path + '/{}_picker.json'.format(type), operation='export', export_values=self.picker_items, export_type='utf-8')
            picker_jsons[type] = type_json

        for type, picker in self.picker_objects.items():
            if type in picker_jsons.keys():
                picker.buildUI()
                picker.setWindowTitle('{}:Controller Picker'.format(type))
                picker.import_picker_func(picker_jsons[type])
                picker.set_picker_namespace_qle.setText('{}:'.format(type))
                picker.items_tree_view.setVisible(False)
                picker.setting_widget.setVisible(False)

                for part_name, pos in text_at_pos[type].items():
                    _text = picker.scene.addText(part_name)
                    _text.setPos(*pos)

                picker.show(dockable=True)

    def all_check_func(self):
        sender = self.sender()
        if sender.isChecked():
            [cbox.setChecked(True) for cbox in self.reference_cbox_dict.values()]
        else:
            [cbox.setChecked(False) for cbox in self.reference_cbox_dict.values()]

    def check_from_current_scene(self):
        [cbox.setChecked(False) for cbox in self.reference_cbox_dict.values()]
        ref_info, ret_no_files = avatarReferenceTool.get_reference_info()
        for ref_i in ref_info:
            if ref_i['namespace'].startswith(':'):
                ex_nss = ref_i['namespace'].lstrip(':')
                if ex_nss in self.reference_cbox_dict.keys():
                    cbox = self.reference_cbox_dict[ex_nss]
                    cbox.setChecked(True)

                    if ex_nss in self.reference_btn_dict.keys():
                        file_name = ref_i['filename']
                        basename_without_ext = os.path.splitext(os.path.basename(file_name))[0]
                        btn = self.reference_btn_dict[ex_nss]
                        btn.setText(basename_without_ext)

        if ret_no_files:
            pick_files = avatarReferenceTool.in_line_for_files(ret_no_files)
            nf_dialog = NoFilesDialog()
            nf_dialog.build(pick_files=pick_files)

            nf_dialog.reference_set_dict = self.reference_set_dict
            nf_dialog.reference_cbox_dict = self.reference_cbox_dict
            nf_dialog.reference_btn_dict = self.reference_btn_dict

            nf_dialog.show()

    def import_settings(self):
        settings = self.set_path_dict['import_settings']
        file_path = self.file_dialog(**settings)
        if file_path:
            import_dict = avatarReferenceTool.json_transfer(file_path[0], 'import')
            self.reference_set_value_dict = import_dict['set']
            self.reference_cbox_values_list = import_dict['cbox']
            self.set_loaded()
            self.reload_set_dict()

    def export_settings(self):
        settings = self.set_path_dict['export_settings']
        file_path = self.file_dialog(**settings)
        if file_path:
            export_dict = OrderedDict()
            self.reload_set_dict()
            export_dict['set'] = self.ui_items[WINDOW_OPTIONVAR]['reference_set_dict']
            export_dict['cbox'] = self.ui_items[WINDOW_OPTIONVAR]['reference_cbox_dict']
            avatarReferenceTool.json_transfer(file_path[0], 'export', export_dict)

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

    def update_fbx_list(self):
        text1_ = 'がチェックアウトされますので、誤ってサブミットしないようにしてください\n'
        text2_ = 'P4Vで古い設定が読み込まれていたら、手動でチェックアウトしてください\n'
        text3_ = '更新したらP4V上で更新(refresh)ボタンを押してください\n'
        text4_ = '正式なアップデートはリグ側で行いますので、ご連絡いただけますと幸いです\n'
        text5_ = '{}を閉じると上記のファイルはリバートされます\n'.format(WINDOW_TITLE)
        confirm_result = cmds.confirmDialog(
            title='FBXのリストを更新しますか？',
            message='{}{}{}{}{}'.format(AVATAR_COLLECTION_FILE, text1_, text2_, text3_, text4_),
            button=['Yes','No'],
            defaultButton='Yes',
            cancelButton='No',
            dismissString='No'
        )

        if confirm_result == 'Yes':
            self.p4v_status = avatarReferenceTool.export_avatar_collection(type='avatar')
            avatarReferenceTool.export_avatar_collection(type='prop')
            if self.p4v_status:
                self.close()
                # self.buildUI()
                # self.show(dockable=True)
                ui = AvatarReferenceTool()
                ui.buildUI()
                ui.show(dockable=True)

            self.p4v_status = False

    def show_prop_list(self):
        sel = cmds.ls(os=True)
        sel = cmds.ls('*:PropAttach_*_ctrl') or cmds.ls('*PropAttach_*_ctrl')
        attach_ctrls = cmds.ls('*:Handattach_*_ctrl') or cmds.ls('*Handattach_*_ctrl')
        [sel.append(c) for c in attach_ctrls]
        sel.sort()
        if sel:
            if self.prop_dialog:
                self.prop_dialog.close()

            self.prop_dialog = PropDialog()
            self.prop_dialog.prop_ctrls = sel
            self.prop_dialog.build()
            self.prop_dialog.show(dockable=True)

    def closeEvent(self, *args):
        if not self.p4v_status:
            avatarReferenceTool.revert_file(AVATAR_COLLECTION_FILE)
        super(AvatarReferenceTool, self).closeEvent(*args)
        self.close()

    def hideEvent(self, *args):
        self.closeEvent(QCloseEvent())
        return

    # def show(self, dockable=None):
    #     super(AvatarReferenceTool, self).show(dockable=dockable)
    #     self.show()

def load_optionVar(key=None):
    return eval(cmds.optionVar(q=key)) if cmds.optionVar(ex=key) else False

def save_optionVar(ui_items=None):
    for key, value in ui_items.items():
        cmds.optionVar(sv=[key, str(value)])

def filter_items(source_items=None, search_txt_list=None, remover=None):
    """
    source_items = cmds.ls(os=True, type='joint', dag=True)

    search_txt_list = [
        '*cloth_test*',
        '*proxy_*',
        '*ik_*'
    ]

    filtered_items = filter_items(source_items=source_items, search_txt_list=search_txt_list, remover=False)
    """

    filtered_items = list()
    filters = list()
    for search_txt in search_txt_list:
        filtered = list(set(fnmatch.filter(source_items, search_txt)))
        [filters.append(fil) for fil in filtered]

    if remover:
        [filtered_items.append(item) for item in source_items if not item in filters]
    else:
        [filtered_items.append(item) for item in source_items if item in filters]

    return filtered_items

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

class RefChangeDialog(MayaQWidgetDockableMixin, QDialog):
    def __init__(self, parent=None):
        super(RefChangeDialog, self).__init__(parent)

        self.setWindowTitle('Type List')

        self.main_h_layout = QHBoxLayout(self)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumHeight(1)
        self.main_h_layout.addWidget(self.scroll_area)

        self.main_widget = QWidget()
        self.scroll_area.setWidget(self.main_widget)

        self.main_v_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_v_layout)
        # widgetの配置を上側に固定
        self.main_v_layout.setAlignment(Qt.AlignTop)

        self.search_qle = QLineEdit()
        self.search_qle.textChanged.connect(self.search_paths)
        self.main_v_layout.addWidget(self.search_qle)

        self.completer = QCompleter(self)
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.search_qle.setCompleter(self.completer)

        self.items = OrderedDict()

        self.btn_items = OrderedDict()

        self.cur_cbx = None
        self.cur_btn = None
        self.import_atom_btn = None

    def add_items(self):
        completer_list = list()
        for type, path in self.items.items():
            btn = QPushButton(type)
            btn.clicked.connect(partial(self.set_parts, type, path))
            btn.setToolTip(path)
            self.main_v_layout.addWidget(btn)

            self.btn_items[type] = btn

            [completer_list.append(t) for t in type.split('_')]

        # widgetを最後に追加したところからストレッチさせる
        self.main_v_layout.addStretch()

        completer_list = list(set(completer_list))
        completer_list.sort()
        self.completer.setModel(QStringListModel(completer_list))

    def set_parts(self, type=None, path=None):
        # sender = self.sender()
        # type = sender.text()
        # print('self.items', self.items)
        self.cur_btn.setText(type)
        self.cur_btn.setToolTip(path)

        self.parent().reload_set_dict()

    def search_paths(self):
        sender = self.sender()
        cur_text = sender.text()

        search_txt_list = ['*{}*'.format(cur_text)]
        source_items = [type for type in self.btn_items.keys()]

        filtered_items = filter_items(source_items=source_items, search_txt_list=search_txt_list, remover=False)

        for type, btn in self.btn_items.items():
            if type in filtered_items:
                btn.setVisible(True)
            elif not type in filtered_items:
                btn.setVisible(False)

class PartsWidget(QWidget):
    def __init__(self, parent=None):
        super(PartsWidget, self).__init__(parent)

        self.main_h_layout = QHBoxLayout(parent)
        self.setLayout(self.main_h_layout)

        self.main_qcbox = QCheckBox()
        self.main_h_layout.addWidget(self.main_qcbox)
        self.main_qcbox.setChecked(True)
        self.main_qcbox.stateChanged.connect(self.parent().reload_set_dict)

        self.main_qbtn = QPushButton()
        self.main_h_layout.addWidget(self.main_qbtn)
        self.main_qbtn.clicked.connect(partial(self.show_list_dialog))

        # self.import_atom_qbtn = QPushButton('Import atom')
        # self.main_h_layout.addWidget(self.import_atom_qbtn)
        # self.import_atom_qbtn.clicked.connect(partial(avatarReferenceTool.anim_temp_save, self.part, type, 'import'))

        # # import
        # self.import_qbtn = QPushButton('import')
        # self.main_h_layout.addWidget(self.import_qbtn)
        # self.import_qbtn.clicked.connect(partial(self.show_list_dialog))
        #
        # # reference
        # self.reference_qbtn = QPushButton('reference')
        # self.main_h_layout.addWidget(self.reference_qbtn)
        # self.reference_qbtn.clicked.connect(partial(self.show_list_dialog))

        self.main_change_qdialog = RefChangeDialog(parent)
        self.main_change_qdialog.cur_cbx = self.main_qcbox
        self.main_change_qdialog.cur_btn = self.main_qbtn
        # self.main_change_qdialog.import_atom_btn = self.import_atom_qbtn

    def show_list_dialog(self):
        self.main_change_qdialog.show()

    # def set_checked(self):
    #     self.parent().reload_set_dict()

class NoFilesDialog(MayaQWidgetDockableMixin, QDialog):
    # QMainWindowを継承するとmenubarの使える幅が広い
    def __init__(self, *args, **kwargs):
        super(NoFilesDialog, self).__init__(*args, **kwargs)

        self.reference_set_dict = OrderedDict()
        self.reference_cbox_dict = OrderedDict()
        self.reference_btn_dict = OrderedDict()

        self.setWindowTitle('Reference Dialog')

    def build(self, pick_files=None):
        main_v_layout = QVBoxLayout(self)
        not_nss_label = QLabel('以下のファイルが見つかりませんでした。\n{}'.format(','.join([p for p in pick_files.keys()])))
        main_v_layout.addWidget(not_nss_label)

        say_pick_label = QLabel('失ったファイルのディレクトから存在するファイルをピックアップしました。\nボタンを押すとそのファイルがリファレンスされます。')
        main_v_layout.addWidget(say_pick_label)

        for nss, files in pick_files.items():
            nss_label = QLabel('{}'.format(nss))
            main_v_layout.addWidget(nss_label)
            for file in files:
                btn = QPushButton('{}'.format(file))
                main_v_layout.addWidget(btn)
                btn.clicked.connect(partial(self.reload_pick_ref, nss, file))

            btn = QPushButton('{}を使用しない'.format(nss))
            main_v_layout.addWidget(btn)
            btn.clicked.connect(partial(self.remove_ref, nss))

    def reload_pick_ref(self, nss=None, file=None):
        cbox = self.reference_cbox_dict[nss]
        cbox.setChecked(True)
        basename_without_ext = os.path.splitext(os.path.basename(file))[0]
        btn = self.reference_btn_dict[nss]
        btn.setText(basename_without_ext)
        self.reference_set_dict[nss] = [btn.text(), file]

        avatarReferenceTool.replace_ref(ref_name=nss, path=file)

    def remove_ref(self, nss=None):
        avatarReferenceTool.delete_ref(ref_name=nss)
        cbox = self.reference_cbox_dict[nss]
        cbox.setChecked(False)

class ErrorDialog(MayaQWidgetDockableMixin, QDialog):
    # QMainWindowを継承するとmenubarの使える幅が広い
    def __init__(self, *args, **kwargs):
        super(ErrorDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle('Error Dialog')

        self.errors = OrderedDict()

    def build(self):
        if self.errors:
            main_v_layout = QVBoxLayout(self)
            btn = QPushButton('エラー文をコピー', self)
            main_v_layout.addWidget(btn)
            btn.clicked.connect(partial(self.get_error_text))

            self.qpte = QPlainTextEdit(self)
            main_v_layout.addWidget(self.qpte)

            for part, error_text in self.errors.items():
                self.qpte.insertPlainText("{}\n".format(error_text))

    def get_error_text(self):
        self.clipboard = QClipboard()
        self.clipboard.setText(self.qpte.toPlainText())


class PropDialog(MayaQWidgetDockableMixin, QMainWindow):
    def __init__(self, *args, **kwargs):
        super(PropDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle('Prop Dialog')

        self.prop_ctrls = list()
        self.prop_collection = avatarReferenceTool.prop_collection()
        self.prop_part_list = [part for part in self.prop_collection.keys()]
        default_id_path = self.prop_collection[self.prop_part_list[0]]
        self.prop_id_list = [id for id in default_id_path.keys()]

        self.nss_list = list()
        self.nss_pad = 3
        self.nss_num = 10
        self.nss_num_dict = OrderedDict()
        for i in range(self.nss_num):
            self.nss_num_dict[i] = None

        self.attach_node = 'offSet_Root'

        self.data_path = DIR_PATH + '/data'

        self.prop_ui_object_dict = OrderedDict()
        self.picker_objects = OrderedDict()

        self.ftr_bake_objects = []
        self.ftr_delete_objects = []

    def build(self):
        self.main_central_widget = QWidget(self)
        self.main_layout = QVBoxLayout(self)
        self.main_central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_central_widget)

        self.main_scroll = QScrollArea(self)
        self.main_layout.addWidget(self.main_scroll)

        self.main_content_widget = QWidget(self)
        self.main_v_layout = QVBoxLayout(self)

        self.add_selection()

        self.main_content_widget.setLayout(self.main_v_layout)
        self.main_scroll.setWidget(self.main_content_widget)

        self.resize(900, 600)

    def add_selection(self):
        main_nss_layout = QHBoxLayout(self)
        self.main_v_layout.addLayout(main_nss_layout)

        label_bold_font = QFont()
        label_bold_font.setBold(True)

        ##################
        # Namespaceのレイアウト
        nss_ql = QLabel('Namespace_{}: '.format('#' * self.nss_pad))
        nss_ql.setFont(label_bold_font)
        nss_tooltip = '<img src="{}/images/nss_tooltip.JPG">'.format(self.data_path)
        nss_ql.setToolTip(nss_tooltip)
        main_nss_layout.addWidget(nss_ql)

        nss_pad_ql = QLabel('Padding')
        main_nss_layout.addWidget(nss_pad_ql)

        nss_pad_cmbox = QComboBox(self)
        main_nss_layout.addWidget(nss_pad_cmbox)

        nss_num_ql = QLabel('Num')
        main_nss_layout.addWidget(nss_num_ql)

        nss_num_cmbox = QComboBox(self)
        main_nss_layout.addWidget(nss_num_cmbox)

        nss_text_ql = QLabel('Text Namespace >> ')
        main_nss_layout.addWidget(nss_text_ql)

        nss_text_qle = QLineEdit(self)
        main_nss_layout.addWidget(nss_text_qle)

        main_nss_layout.setAlignment(Qt.AlignLeft)

        ##################
        # Namespaceのアイテム設定
        nss_pad_cmbox.addItems([str(i+1) for i in range(self.nss_pad)])
        num_list = ['pro_' + str(i).zfill(1) for i in range(self.nss_num) if not cmds.objExists('pro_' + str(i).zfill(1) + ':Root')]
        for i, n in enumerate(num_list):
            self.nss_num_dict[i] = n
        nss_num_cmbox.addItems(num_list)

        ##################
        # Namespaceのシグナル
        nss_pad_cmbox.currentTextChanged.connect(partial(self.prop_nss_from_pad, nss_pad_cmbox, nss_num_cmbox))
        nss_text_qle.textChanged.connect(partial(self.nss_sts_changing, nss_text_qle, nss_pad_ql, nss_pad_cmbox, nss_num_ql, nss_num_cmbox))

        # self.prop_ctrlsはプロップ用のコントローラを代入している
        for prop_ctrl in self.prop_ctrls:
            self.prop_ui_object_dict[prop_ctrl] = {}

            ################
            # propに関連するオブジェクト用のレイアウト
            prop_items_layout = QHBoxLayout(self)
            self.main_v_layout.addLayout(prop_items_layout)

            # Controllerレイアウト
            prop_ctrl_ql = QLabel('Prop Controller')
            prop_ctrl_ql.setFont(label_bold_font)
            prop_ctrl_tooltip = '<img src="{}/images/prop_ctrl_tooltip.JPG">'.format(self.data_path)
            prop_ctrl_ql.setToolTip(prop_ctrl_tooltip)
            # prop_items_layout.addWidget(prop_ctrl_ql)

            # Controllerレイアウトに色々追加するようのレイアウト
            prop_ctrl_layout = QVBoxLayout(self)
            prop_ctrl_layout.setAlignment(Qt.AlignTop)
            prop_items_layout.addLayout(prop_ctrl_layout)
            prop_ctrl_layout.addWidget(prop_ctrl_ql)

            # コントローラ選択ボタン
            prop_ctrl_sel_btn = QPushButton('Select Controller')
            prop_ctrl_layout.addWidget(prop_ctrl_sel_btn)

            # コントローラ操作用レイアウト
            prop_ctrl_set_layout = QHBoxLayout(self)
            prop_ctrl_layout.addLayout(prop_ctrl_set_layout)

            # コントローラのlineEdit
            prop_ctrl_qle = FlexLineEdit(self)
            prop_ctrl_qle.setText(prop_ctrl)
            prop_ctrl_qle.setToolTip(prop_ctrl)
            # prop_ctrl_qle.setReadOnly(True)

            # コントローラを選択するボタンのシグナル
            prop_ctrl_sel_btn.clicked.connect(partial(self.select_object, prop_ctrl_qle))

            # コントローラsetボタン
            prop_ctrl_set_btn = QPushButton('<< Set')

            prop_ctrl_set_layout.addWidget(prop_ctrl_qle)
            prop_ctrl_set_layout.addWidget(prop_ctrl_set_btn)

            # コントローラのSpace用レイアウト
            prop_ctrl_space_layout = QHBoxLayout(self)
            prop_ctrl_layout.addLayout(prop_ctrl_space_layout)
            prop_ctrl_space_ql = QLabel('Space:')
            prop_ctrl_space_layout.addWidget(prop_ctrl_space_ql)

            # コントローラのspace用ComboBox
            prop_ctrl_space_cmbox = QComboBox(self)
            prop_ctrl_space_layout.addWidget(prop_ctrl_space_cmbox)
            prop_ctrl_space_cmbox.currentTextChanged.connect(partial(self.switch_prop_space, prop_ctrl_qle, prop_ctrl_space_cmbox))

            # コントローラのSpace用レイアウト
            prop_ctrl_get_set_space_layout = QHBoxLayout(self)
            prop_ctrl_layout.addLayout(prop_ctrl_get_set_space_layout)

            prop_ctrl_get_space_btn = QPushButton('Get Space')
            prop_ctrl_get_set_space_layout.addWidget(prop_ctrl_get_space_btn)
            prop_ctrl_get_space_btn.clicked.connect(partial(self.get_prop_space, prop_ctrl_qle, prop_ctrl_space_cmbox))

            prop_ctrl_set_space_btn = QPushButton('Set Space')
            prop_ctrl_get_set_space_layout.addWidget(prop_ctrl_set_space_btn)
            prop_ctrl_set_space_btn.clicked.connect(partial(self.switch_prop_space, prop_ctrl_qle, prop_ctrl_space_cmbox))

            self.prop_ui_object_dict[prop_ctrl]['name'] = prop_ctrl_qle
            self.prop_ui_object_dict[prop_ctrl]['space'] = prop_ctrl_space_cmbox

            # コントローラのrotate用レイアウト
            prop_ctrl_rot_layout = QHBoxLayout(self)
            prop_ctrl_layout.addLayout(prop_ctrl_rot_layout)
            prop_ctrl_rot_ql = QLabel('Rotate:')
            prop_ctrl_rot_cmbox = QComboBox(self)

            prop_ctrl_rot_layout.addWidget(prop_ctrl_rot_ql)
            prop_ctrl_rot_layout.addWidget(prop_ctrl_rot_cmbox)

            # 区切り用のSplitter
            v_splitter = QSplitter(Qt.Vertical)
            v_bottom = QFrame()
            v_bottom.setFrameShape(QFrame.VLine)
            v_splitter.addWidget(v_bottom)
            prop_items_layout.addWidget(v_splitter)

            # 読み込むprop用のレイアウト
            prop_layout = QVBoxLayout(self)
            prop_layout.setAlignment(Qt.AlignTop)
            prop_ql = QLabel('Prop Reference')
            prop_ql.setFont(label_bold_font)
            prop_ref_tooltip = '<img src="{}/images/prop_ref_tooltip.JPG">'.format(self.data_path)
            prop_ql.setToolTip(prop_ref_tooltip)
            # prop_items_layout.addWidget(prop_ql)
            prop_items_layout.addLayout(prop_layout)
            prop_layout.addWidget(prop_ql)

            # propとコントローラのマッチ用チェックボックス
            prop_match_cbox = QCheckBox('Match')
            prop_layout.addWidget(prop_match_cbox)
            prop_match_cbox.setChecked(True)

            # propとコントローラの接続用チェックボックス
            prop_connect_cbox = QCheckBox('Connect')
            prop_layout.addWidget(prop_connect_cbox)
            prop_connect_cbox.setChecked(True)

            # リファレンスするprop用のレイアウト
            prop_ref_layout = QVBoxLayout(self)
            prop_ref_layout.setAlignment(Qt.AlignTop)
            prop_items_layout.addLayout(prop_ref_layout)

            # propのパートのComboBox
            prop_ref_part_cmbox = QComboBox(self)
            # prop_ref_layout.addWidget(prop_ref_part_cmbox)
            prop_layout.addWidget(prop_ref_part_cmbox)

            prop_ref_id_cmbox = QComboBox(self)
            # prop_ref_layout.addWidget(prop_ref_id_cmbox)
            prop_layout.addWidget(prop_ref_id_cmbox)

            # アイテムの追加
            prop_ref_part_cmbox.addItems(self.prop_part_list)
            prop_ref_id_cmbox.addItems(self.prop_id_list)

            # リファレンスを読み込むComboBoxのシグナル
            prop_ref_part_cmbox.currentTextChanged.connect(partial(self.prop_list, prop_ref_part_cmbox, prop_ref_id_cmbox))

            self.prop_ui_object_dict[prop_ctrl]['propPart'] = prop_ref_part_cmbox
            self.prop_ui_object_dict[prop_ctrl]['propID'] = prop_ref_id_cmbox

            # 読み込むpropの操作用レイアウト
            prop_ref_func_layout = QVBoxLayout(self)
            prop_ref_func_layout.setAlignment(Qt.AlignTop)
            prop_items_layout.addLayout(prop_ref_func_layout)

            # リファレンスのボタン群
            prop_ref_func_ref_btn = QPushButton('Reference')
            # prop_ref_func_layout.addWidget(prop_ref_func_ref_btn)
            prop_layout.addWidget(prop_ref_func_ref_btn)

            prop_ref_func_remref_btn = QPushButton('RemoveReference')
            # prop_ref_func_layout.addWidget(prop_ref_func_remref_btn)
            prop_layout.addWidget(prop_ref_func_remref_btn)

            prop_ref_func_editor_btn = QPushButton('ReferenceEditor')
            # prop_ref_func_layout.addWidget(prop_ref_func_editor_btn)
            prop_layout.addWidget(prop_ref_func_editor_btn)
            prop_ref_func_editor_btn.clicked.connect(cmds.ReferenceEditor)

            # propの選択用のレイアウト
            prop_ref_sel_layout = QVBoxLayout(self)
            prop_ref_sel_layout.setAlignment(Qt.AlignTop)
            prop_items_layout.addLayout(prop_ref_sel_layout)

            # propのroot選択用のレイアウト
            prop_ref_func_ql = QLabel('Prop Reference Function')
            prop_ref_func_tooltip = '<img src="{}/images/prop_ref_func_tooltip.JPG">'.format(self.data_path)
            prop_ref_func_ql.setToolTip(prop_ref_func_tooltip)

            prop_ref_func_ql.setFont(label_bold_font)
            prop_ref_sel_layout.addWidget(prop_ref_func_ql)

            prop_ref_sel_root_btn = QPushButton('Select Root')
            prop_ref_sel_layout.addWidget(prop_ref_sel_root_btn)

            prop_ref_sel_root_layout = QHBoxLayout(self)
            prop_ref_sel_layout.addLayout(prop_ref_sel_root_layout)

            prop_ref_sel_qle = FlexLineEdit(self)
            prop_ref_sel_root_layout.addWidget(prop_ref_sel_qle)
            prop_ref_sel_root_btn.clicked.connect(partial(self.select_object, prop_ref_sel_qle))

            # propのRootをsetするボタン
            prop_ref_sel_btn = QPushButton('<< Set')
            prop_ref_sel_root_layout.addWidget(prop_ref_sel_btn)
            prop_ref_sel_btn.clicked.connect(partial(self.set_selection, prop_ref_sel_qle))

            self.prop_ui_object_dict[prop_ctrl]['Root'] = prop_ref_sel_qle

            # propのroot_ctrl選択用のレイアウト
            prop_ref_sel_root_ctrl_btn = QPushButton('Select Root Ctrl')
            prop_ref_sel_layout.addWidget(prop_ref_sel_root_ctrl_btn)

            prop_ref_sel_root_ctrl_layout = QHBoxLayout(self)
            prop_ref_sel_layout.addLayout(prop_ref_sel_root_ctrl_layout)

            prop_ref_sel_root_ctrl_qle = FlexLineEdit(self)
            prop_ref_sel_root_ctrl_layout.addWidget(prop_ref_sel_root_ctrl_qle)
            prop_ref_sel_root_ctrl_btn.clicked.connect(partial(self.select_object, prop_ref_sel_root_ctrl_qle))

            prop_ref_set_root_ctrl_btn = QPushButton('<< Set')
            prop_ref_sel_root_ctrl_layout.addWidget(prop_ref_set_root_ctrl_btn)
            prop_ref_set_root_ctrl_btn.clicked.connect(partial(self.set_selection, prop_ref_sel_root_ctrl_qle))

            prop_ref_func_picker_btn = QPushButton('Picker')
            # prop_ref_func_layout.addWidget(prop_ref_func_picker_btn)
            prop_ref_sel_layout.addWidget(prop_ref_func_picker_btn)
            # pickerを起動するシグナル
            prop_ref_func_picker_btn.clicked.connect(partial(self.show_picker, prop_ref_sel_qle))

            prop_fbx_to_rig_btn = QPushButton('FBX to Rig')
            prop_ref_sel_layout.addWidget(prop_fbx_to_rig_btn)
            prop_fbx_to_rig_btn.clicked.connect(partial(self.fbx_to_rig, prop_ctrl_qle, prop_ref_sel_qle))

            prop_cleanup_fbx_to_rig_btn = QPushButton('CleanUp FBX to Rig')
            prop_ref_sel_layout.addWidget(prop_cleanup_fbx_to_rig_btn)
            prop_cleanup_fbx_to_rig_btn.clicked.connect(partial(self.cleanup_fbx_to_rig))

            self.prop_ui_object_dict[prop_ctrl]['RootCtrl'] = prop_ref_sel_root_ctrl_qle

            # 区切り用のSplitter
            v_splitter = QSplitter(Qt.Vertical)
            v_bottom = QFrame()
            v_bottom.setFrameShape(QFrame.VLine)
            v_splitter.addWidget(v_bottom)
            prop_items_layout.addWidget(v_splitter)

            # propのattachNode用のレイアウト
            prop_attach_layout = QVBoxLayout(self)
            prop_attach_layout.setAlignment(Qt.AlignTop)
            prop_attach_ql = QLabel('Attach Node')
            prop_attach_ql.setFont(label_bold_font)
            prop_attach_tooltip = '<img src="{}/images/prop_attach_tooltip.JPG">'.format(self.data_path)
            prop_attach_ql.setToolTip(prop_attach_tooltip)
            # prop_items_layout.addWidget(prop_attach_ql)
            prop_attach_layout.addWidget(prop_attach_ql)
            prop_items_layout.addLayout(prop_attach_layout)

            prop_attach_sel_btn = QPushButton('Select Attach Node')
            prop_attach_layout.addWidget(prop_attach_sel_btn)

            prop_attach_sel_layout = QHBoxLayout(self)
            prop_attach_layout.addLayout(prop_attach_sel_layout)

            prop_attach_sel_qle = FlexLineEdit(self)
            prop_attach_sel_layout.addWidget(prop_attach_sel_qle)
            prop_attach_sel_btn.clicked.connect(partial(self.select_object, prop_attach_sel_qle))

            prop_attach_set_btn = QPushButton('<< Set')
            prop_attach_sel_layout.addWidget(prop_attach_set_btn)

            prop_attach_func_layout = QHBoxLayout(self)
            prop_attach_layout.addLayout(prop_attach_func_layout)

            prop_attach_ctrl_match_btn = QPushButton('Controller Match')
            prop_attach_func_layout.addWidget(prop_attach_ctrl_match_btn)
            prop_attach_ctrl_match_btn.clicked.connect(partial(self.match_transform, prop_ctrl_qle, prop_ref_sel_qle, prop_attach_sel_qle, 1))

            prop_attach_root_match_btn = QPushButton('Root Match')
            prop_attach_func_layout.addWidget(prop_attach_root_match_btn)
            prop_attach_root_match_btn.clicked.connect(partial(self.match_transform, prop_ctrl_qle, prop_ref_sel_qle, prop_attach_sel_qle, 0))

            prop_gobp_btn = QPushButton('Go to bindPose')
            prop_attach_layout.addWidget(prop_gobp_btn)
            prop_gobp_btn.clicked.connect(partial(self.go_to_bindPose, prop_ctrl_qle))

            self.prop_ui_object_dict[prop_ctrl]['attachNode'] = prop_attach_sel_qle

            # 区切り用のSplitter
            v_splitter = QSplitter(Qt.Vertical)
            v_bottom = QFrame()
            v_bottom.setFrameShape(QFrame.VLine)
            v_splitter.addWidget(v_bottom)
            prop_items_layout.addWidget(v_splitter)

            # tools
            prop_tools_ql = QLabel('Tools')
            prop_tools_ql.setFont(label_bold_font)
            prop_tools_tooltip = '<img src="{}/images/prop_tools_tooltip.JPG">'.format(self.data_path)
            prop_tools_ql.setToolTip(prop_tools_tooltip)
            prop_tools_space_match_bake_layout = QVBoxLayout(self)
            # prop_items_layout.addWidget(prop_tools_ql)
            prop_tools_space_match_bake_layout.addWidget(prop_tools_ql)

            # Space Match Bake
            prop_tools_space_match_bake_layout.setAlignment(Qt.AlignTop)
            prop_items_layout.addLayout(prop_tools_space_match_bake_layout)

            prop_tools_set_match_space_ql = QLabel('Set Match Space')
            prop_tools_space_match_bake_layout.addWidget(prop_tools_set_match_space_ql)

            prop_tools_space_match_bake_cmbox = QComboBox(self)
            prop_tools_space_match_bake_layout.addWidget(prop_tools_space_match_bake_cmbox)

            prop_tools_space_match_bake_btn = QPushButton('Space Match Bake')
            prop_tools_space_match_bake_layout.addWidget(prop_tools_space_match_bake_btn)
            prop_tools_space_match_bake_btn.clicked.connect(partial(self.space_match_bake, prop_ctrl_qle, prop_ctrl_space_cmbox, prop_tools_space_match_bake_cmbox))

            self.prop_ui_object_dict[prop_ctrl]['spaceMatchBake'] = prop_tools_space_match_bake_cmbox

            # コントローラごとの区切り用のSplitter
            h_splitter = QSplitter(Qt.Horizontal)
            h_bottom = QFrame()
            h_bottom.setFrameShape(QFrame.HLine)
            h_splitter.addWidget(h_bottom)
            self.main_v_layout.addWidget(h_splitter)

            # prop更新用のシグナル
            prop_ref_func_ref_btn.clicked.connect(partial(self.ref_prop, prop_ctrl_qle, prop_ref_part_cmbox, prop_ref_id_cmbox, nss_num_cmbox, nss_text_qle, prop_ref_sel_qle, prop_ref_sel_root_ctrl_qle, 'ref', prop_match_cbox, prop_connect_cbox, prop_attach_sel_qle, prop_ctrl_space_cmbox, prop_tools_space_match_bake_cmbox))
            prop_ref_func_remref_btn.clicked.connect(partial(self.ref_prop, prop_ctrl_qle, prop_ref_part_cmbox, prop_ref_id_cmbox, nss_num_cmbox, nss_text_qle, prop_ref_sel_qle, prop_ref_sel_root_ctrl_qle, 'remove_ref', prop_match_cbox, prop_connect_cbox, prop_attach_sel_qle, prop_ctrl_space_cmbox, prop_tools_space_match_bake_cmbox))

            #
            prop_ctrl_set_btn.clicked.connect(partial(self.set_selection, prop_ctrl_qle, prop_ctrl_space_cmbox, prop_tools_space_match_bake_cmbox))
            prop_attach_set_btn.clicked.connect(partial(self.set_selection, prop_attach_sel_qle, prop_ctrl_space_cmbox, prop_tools_space_match_bake_cmbox))

            # spaceの更新
            self.set_spaces(prop_ctrl_qle=prop_ctrl_qle, prop_ctrl_space_cmbox=prop_tools_space_match_bake_cmbox, dum=None)
            self.set_spaces(prop_ctrl_qle=prop_ctrl_qle, prop_ctrl_space_cmbox=prop_ctrl_space_cmbox, dum=None)

            # rotateの更新
            self.add_prop_rotate_values(prop_ctrl_qle, prop_ctrl_rot_cmbox)
            prop_ctrl_rot_cmbox.currentTextChanged.connect(partial(self.prop_rotate_from, prop_ctrl_qle, prop_ctrl_rot_cmbox))

        # シーン内にpropを設定したノードがあるか確認
        prop_has_dict = None
        try:
            prop_has_dict = self.set_from_prop_network()
        except Exception as e:
            print(traceback.format_exc())

        if prop_has_dict:
            for prop_ctrl, values in prop_has_dict.items():
                if prop_ctrl in self.prop_ui_object_dict.keys():
                    src_ui_objects = self.prop_ui_object_dict[prop_ctrl]
                else:
                    continue
                # Values
                prop_ctrl_space_cmbox_val = values['space']
                prop_ref_part_cmbox_val = values['propPart']
                prop_ref_id_cmbox_val = values['propID']
                prop_ctrl_qle_val = values['name']
                prop_ref_sel_qle_val = values['Root']
                prop_ref_sel_root_ctrl_qle_val = values['RootCtrl']
                prop_attach_sel_qle_val = values['attachNode']

                prop_ref_path = values['propPath']


                # UI
                prop_ctrl_space_cmbox = src_ui_objects['space']
                prop_ref_part_cmbox = src_ui_objects['propPart']
                prop_ref_id_cmbox = src_ui_objects['propID']
                prop_ctrl_qle = src_ui_objects['name']
                prop_ref_sel_qle = src_ui_objects['Root']
                prop_ref_sel_root_ctrl_qle = src_ui_objects['RootCtrl']
                prop_attach_sel_qle = src_ui_objects['attachNode']

                prop_tools_space_match_bake_cmbox = src_ui_objects['spaceMatchBake']

                # set values
                prop_ctrl_space_cmbox.setCurrentText(prop_ctrl_space_cmbox_val)
                prop_ref_part_cmbox.setCurrentText(prop_ref_part_cmbox_val)
                prop_ref_id_cmbox.setCurrentText(prop_ref_id_cmbox_val)
                prop_ctrl_qle.setText(prop_ctrl_qle_val)
                prop_ref_sel_qle.setText(prop_ref_sel_qle_val)
                prop_ref_sel_root_ctrl_qle.setText(prop_ref_sel_root_ctrl_qle_val)
                prop_attach_sel_qle.setText(prop_attach_sel_qle_val)

                self.set_spaces(prop_ctrl_qle=prop_ctrl_qle, prop_ctrl_space_cmbox=prop_ctrl_space_cmbox, dum=None)
                self.set_spaces(prop_ctrl_qle=prop_ctrl_qle, prop_ctrl_space_cmbox=prop_tools_space_match_bake_cmbox, dum=None)

                avatarReferenceTool.create_prop_network(prop_ctrl,
                                                        prop_ref_sel_qle_val,
                                                        prop_ref_sel_root_ctrl_qle_val,
                                                        prop_attach_sel_qle_val,
                                                        prop_ref_part_cmbox_val,
                                                        prop_ref_id_cmbox_val,
                                                        prop_ctrl_space_cmbox_val,
                                                        prop_ref_path)

    def set_selection(self, qle=None, prop_ctrl_space_cmbox=None, prop_tools_space_match_bake_cmbox=None):
        sel = cmds.ls(os=True)
        if sel:
            qle.setText(sel[0])
            qle.setToolTip(sel[0])

        if prop_ctrl_space_cmbox:
            self.set_spaces(prop_ctrl_qle=qle, prop_ctrl_space_cmbox=prop_ctrl_space_cmbox, dum=None)
            self.set_spaces(prop_ctrl_qle=qle, prop_ctrl_space_cmbox=prop_tools_space_match_bake_cmbox, dum=None)


    def set_spaces(self, prop_ctrl_qle=None, prop_ctrl_space_cmbox=None, dum=None):
        prop_ctrl_space_cmbox.clear()
        ctrl = prop_ctrl_qle.text()
        ctrl_enums_list, current = avatarReferenceTool.get_prop_enum_spaces(ctrl)
        prop_ctrl_space_cmbox.addItems(ctrl_enums_list)
        prop_ctrl_space_cmbox.setCurrentText(ctrl_enums_list[current])

    def select_object(self, qle_object=None):
        text = qle_object.text()
        if cmds.objExists(text):
            cmds.select(text, r=True)

    def fbx_to_rig(self, prop_ctrl_qle=None, prop_ref_sel_qle=None):
        attach_ctrl = prop_ctrl_qle.text()
        jnt = prop_ref_sel_qle.text()
        ref_name = '{}'.format(':'.join(jnt.split(':')[0:-1]))
        self.ftr_bake_objects, self.ftr_delete_objects = avatarReferenceTool.fbx_to_rig_for_prop(attach_ctrl=attach_ctrl, ref_name=ref_name)

    def cleanup_fbx_to_rig(self):
        if self.ftr_bake_objects and self.ftr_delete_objects:
            avatarReferenceTool.fullbake(self.ftr_bake_objects)
            [cmds.delete(n) for n in self.ftr_delete_objects if cmds.objExists(n)]
            self.ftr_bake_objects = []
            self.ftr_delete_objects = []

    def select_attach_node(self, qle_object=None):
        text = qle_object.text()
        attach_node = '{}:{}'.format(':'.join(text.split(':')[0:-1]), self.attach_node)
        if cmds.objExists(attach_node):
            cmds.select(attach_node, r=True)

    def prop_list(self, part_cmbox=None, id_cmbox=None, dum=None):
        part_text = part_cmbox.currentText()
        id_path = self.prop_collection[part_text]
        prop_id_list = [id for id in id_path.keys()]
        id_cmbox.clear()
        id_cmbox.addItems(prop_id_list)

    def prop_nss_from_pad(self, nss_pad_cmbox=None, nss_num_cmbox=None, dum=None):
        cur_nss_num = nss_num_cmbox.currentText()
        cur_num_key = None
        for key, val in self.nss_num_dict.items():
            if val == cur_nss_num:
                cur_num_key = key

        nss_pad = int(nss_pad_cmbox.currentText())
        num_list = ['pro_' + str(i).zfill(nss_pad) for i in range(self.nss_num) if not cmds.objExists('pro_' + str(i).zfill(nss_pad) + ':Root')]
        for i, n in enumerate(num_list):
            self.nss_num_dict[i] = n

        nss_num_cmbox.clear()
        nss_num_cmbox.addItems(num_list)
        nss_num_cmbox.setCurrentText(self.nss_num_dict[cur_num_key])

    def nss_sts_changing(self, nss_text_qle, nss_pad_ql, nss_pad_cmbox, nss_num_ql, nss_num_cmbox, dum):
        if nss_text_qle.text():
            nss_pad_ql.setVisible(False)
            nss_pad_cmbox.setVisible(False)
            nss_num_ql.setVisible(False)
            nss_num_cmbox.setVisible(False)
        else:
            nss_pad_ql.setVisible(True)
            nss_pad_cmbox.setVisible(True)
            nss_num_ql.setVisible(True)
            nss_num_cmbox.setVisible(True)

    def match_transform(self, prop_ctrl_qle=None, prop_ref_sel_qle=None, prop_attach_sel_qle=None, type=0):
        ctrl = prop_ctrl_qle.text()
        ctrl_nss = '{}:'.format(':'.join(ctrl.split(':')[0:-1]))
        jnt = prop_ref_sel_qle.text()
        attach_node = prop_attach_sel_qle.text()

        if type == 0:
            avatarReferenceTool.match_transform(jnt, attach_node, ctrl_nss)
        elif type == 1:
            avatarReferenceTool.match_transform(ctrl, attach_node, ctrl_nss)

    def go_to_bindPose(self, prop_ctrl_qle=None):
        ctrl = prop_ctrl_qle.text()
        ctrl_nss = '{}:'.format(':'.join(ctrl.split(':')[0:-1]))
        avatarReferenceTool.go_to_bindPose_for_rig(namespace=ctrl_nss)

    def get_prop_space(self, prop_ctrl_qle=None, prop_ctrl_space_cmbox=None, dum=None):
        ctrl = prop_ctrl_qle.text()
        enums_list, current = avatarReferenceTool.get_prop_enum_spaces(ctrl)
        prop_ctrl_space_cmbox.setCurrentText(enums_list[current])

    def switch_prop_space(self, prop_ctrl_qle=None, prop_ctrl_space_cmbox=None, dum=None):
        ctrl = prop_ctrl_qle.text()
        space = prop_ctrl_space_cmbox.currentText()
        avatarReferenceTool.switch_prop_space(ctrl, space)

    # リファレンスさせる際にthe worldしているが、
    # UIの処理もthe worldしないといけない
    @avatarReferenceTool.the_world
    def ref_prop(self, prop_ctrl_qle=None, prop_ref_part_cmbox=None, prop_ref_id_cmbox=None, nss_num_cmbox=None,
                 nss_text_qle=None, prop_ref_sel_qle=None, prop_ref_sel_root_ctrl_qle=None, type='ref', prop_match_cbox=None,
                 prop_connect_cbox=None, prop_attach_sel_qle=None, prop_ctrl_space_cmbox=None, prop_tools_space_match_bake_cmbox=None):

        # カレント値の取得
        part = prop_ref_part_cmbox.currentText()
        id = prop_ref_id_cmbox.currentText()
        ctrl = prop_ctrl_qle.text()
        ctrl_nss = '{}:'.format(':'.join(ctrl.split(':')[0:-1]))
        jnt = prop_ref_sel_qle.text()
        ref_name = '{}'.format(':'.join(jnt.split(':')[0:-1]))
        root_ctrl = prop_ref_sel_root_ctrl_qle.text()
        space = prop_ctrl_space_cmbox.currentText()

        # カレント値からfbxのパスを取得
        path = self.prop_collection[part][id]

        # 数字ベースのNamespaceの数を取得する
        nss_num_items = [nss_num_cmbox.itemText(i) for i in range(nss_num_cmbox.count())]

        if type == 'remove_ref':
            if cmds.objExists(ref_name + '_prop_temp_grp'):
                cmds.delete(ref_name + '_prop_temp_grp')

            ctrl_prop_network = '{}_prop_network'.format(ctrl)
            constraints = cmds.getAttr(ctrl_prop_network + '.constraints').split(',')
            for cnst in constraints:
                if cmds.objExists(cnst):
                    cmds.delete(cnst)
            if cmds.objExists(ctrl_prop_network):
                cmds.delete(ctrl_prop_network)
            # prop_ref_sel_qle.setText('')
            avatarReferenceTool.prop_update(ref_name, path, True, ctrl_nss)

            ref_name = ''.join(ref_name.split(':'))
            nss_num_items.append(ref_name)
            nss_num_items.sort()

            nss_num_cmbox.clear()
            nss_num_cmbox.addItems(nss_num_items)
            prop_ref_sel_qle.setText('')
            prop_ref_sel_root_ctrl_qle.setText('')
            prop_attach_sel_qle.setText('')

            return

        # 数字ベースのpropのNamespaceの取得
        if nss_text_qle.text():
            ref_name = '{}'.format(nss_text_qle.text())
        else:
            ref_name = '{}'.format(nss_num_cmbox.currentText())

        # 使われているNamespaceとして削除して入れ直す
        nss_num_items.remove(ref_name)
        nss_num_cmbox.clear()
        nss_num_cmbox.addItems(nss_num_items)

        # Namespaceを元に設定
        prop_ref_sel_qle.setText('{}:{}'.format(ref_name, 'Root'))
        prop_ref_sel_root_ctrl_qle.setText('{}:{}'.format(ref_name, 'Root_ctrl'))

        # 再度カレント値の取得
        ctrl = prop_ctrl_qle.text()
        ctrl_nss = '{}:'.format(':'.join(ctrl.split(':')[0:-1]))
        jnt = prop_ref_sel_qle.text()
        ref_name = '{}'.format(':'.join(jnt.split(':')[0:-1]))
        root_ctrl = prop_ref_sel_root_ctrl_qle.text()

        # propの更新
        if type == 'ref':
            avatarReferenceTool.prop_update(ref_name, path, False, ctrl_nss)
            avatarReferenceTool.prop_scale_connection(ctrl, ctrl_nss, ref_name)

            # offsetRootのgetとSet
            offSet_Root = avatarReferenceTool.get_offSet_Root(attach_node='*{}*'.format(self.attach_node), filter=ref_name+':')
            prop_attach_sel_qle.setText('{}'.format(offSet_Root))

            attach_node = prop_attach_sel_qle.text()

            self.set_spaces(prop_ctrl_qle=prop_ctrl_qle, prop_ctrl_space_cmbox=prop_tools_space_match_bake_cmbox, dum=None)
            self.set_spaces(prop_ctrl_qle=prop_ctrl_qle, prop_ctrl_space_cmbox=prop_ctrl_space_cmbox, dum=None)

        # マッチするかしないか
        if prop_match_cbox.isChecked():
            avatarReferenceTool.match_transform(jnt, attach_node, ctrl_nss)
            avatarReferenceTool.match_transform(ctrl, attach_node, ctrl_nss)

        # コンストレイントするかしないか
        if prop_connect_cbox.isChecked():
            pos_con, ori_con = avatarReferenceTool.parent_constraint(ctrl, ref_name+':Root_ctrl_grp')

        avatarReferenceTool.switch_prop_space(ctrl, space)
        prop_ctrl_space_cmbox.setCurrentText(space)

        avatarReferenceTool.create_prop_network(ctrl, jnt, root_ctrl, attach_node, part, id, space, path, pos_con, ori_con)

    def show_picker(self, prop_ref_sel_qle):
        jnt = prop_ref_sel_qle.text()

        ref_name = '{}'.format(':'.join(jnt.split(':')[0:-1]))

        if self.picker_objects:
            for picker in self.picker_objects.values():
                picker.close()

        # types = [type for type in self.reference_set_dict.keys()]

        part_picks = OrderedDict()

        sim_ctrl_sets = '{}_prop_temp_ctrl_sets'.format(ref_name)
        if not cmds.objExists(sim_ctrl_sets):
            return

        self.picker = avatarReferenceToolPicker.PickerAnimTools()
        self.picker_objects[ref_name] = self.picker

        cmds.select(sim_ctrl_sets, r=True, ne=True)
        ctrls = cmds.pickWalk(d='down')

        part_picks[ref_name] = OrderedDict()

        ctrls.sort()
        for ctrl in ctrls:
            removed_nss = ctrl.replace(ref_name + ':', '')
            splited = removed_nss.split('_')[0::]

            side_picker_name = ref_name + '_' + splited[0]
            part_sets = side_picker_name + '_ctrl_sets'

            if '_L_' in ctrl or '_R_' in ctrl:
                side_picker_name = ref_name + '_' + splited[0] + '_' + splited[2]
                part_side_sets = side_picker_name + '_ctrl_sets'
                part_picks[ref_name][side_picker_name] = part_side_sets

            else:
                part_picks[ref_name][side_picker_name] = part_sets

        print('Prop Picker:{}'.format(part_picks))

        picker_jsons = OrderedDict()
        text_at_pos = OrderedDict()
        for type, part_sets in part_picks.items():
            self.picker_items = OrderedDict()
            text_at_pos[type] = OrderedDict()
            i = 0
            for sides, picker_sets in part_sets.items():
                x_pos = 220.0 - i*50

                cmds.select(picker_sets, r=True, ne=True)
                ctrls = cmds.pickWalk(d='down')

                ctrls.sort()
                j = 0
                for ctrl in ctrls:
                    removed_nss = ctrl.replace(type + ':', '')

                    part_name = removed_nss.split('_')[0]
                    # if not part_name in text_at_pos.keys():
                    text_at_pos[type][part_name] = [x_pos, -30]

                    if '_R_' in removed_nss:
                        if cmds.objExists('{}:{}'.format(type, removed_nss)):
                            plus_x_pos = x_pos + 25
                            text_at_pos[type][part_name] = [plus_x_pos, -30]

                    self.picker_items[removed_nss] = OrderedDict()
                    self.picker_items[removed_nss]['item_name'] = removed_nss
                    self.picker_items[removed_nss]['rect'] = [x_pos, j*40, 30, 30]
                    if '_L_' in removed_nss:
                        color = [255, 50, 50]
                        edge_color = [255, 100, 100]
                    elif '_R_' in removed_nss:
                        color = [50, 50, 255]
                        edge_color = [100, 100, 255]
                    else:
                        color = [212, 212, 50]
                        edge_color = [255, 255, 100]

                    self.picker_items[removed_nss]['color'] = color
                    self.picker_items[removed_nss]['edge_color'] = edge_color
                    self.picker_items[removed_nss]['width'] = 4

                    j += 1

                i += 1

            print('text_at_pos', text_at_pos)

            type_json = self.data_path + '/{}_prop_picker.json'.format(type)
            avatarReferenceToolPicker.json_transfer(self.data_path + '/{}_prop_picker.json'.format(type), operation='export', export_values=self.picker_items, export_type='utf-8')
            picker_jsons[type] = type_json

        for type, picker in self.picker_objects.items():
            if type in picker_jsons.keys():
                picker.buildUI()
                picker.setWindowTitle('{}:Controller Picker'.format(type))
                picker.import_picker_func(picker_jsons[type])
                picker.set_picker_namespace_qle.setText('{}:'.format(type))
                picker.items_tree_view.setVisible(False)
                picker.setting_widget.setVisible(False)

                for part_name, pos in text_at_pos[type].items():
                    _text = picker.scene.addText(part_name)
                    _text.setPos(*pos)

                picker.show(dockable=True)


    def space_match_bake(self, prop_ctrl_qle=None, prop_ctrl_space_cmbox=None, prop_tools_space_match_bake_cmbox=None):
        ctrl = prop_ctrl_qle.text()
        space = prop_ctrl_space_cmbox.currentText()
        match_space = prop_tools_space_match_bake_cmbox.currentText()
        avatarReferenceTool.fullbake([ctrl])
        avatarReferenceTool.space_match_bake(ctrl, space, match_space)
        prop_ctrl_space_cmbox.setCurrentText(match_space)

    def set_from_prop_network(self):
        prop_network_sets = 'prop_network_sets'
        prop_has_dict = OrderedDict()
        if cmds.objExists(prop_network_sets):
            cmds.select(prop_network_sets, ne=True, r=True)
            ctrl_prop_networks = cmds.pickWalk(d='down');cmds.ls(os=True)
            for cp_net in ctrl_prop_networks:
                ctrl = cmds.getAttr(cp_net + '.ctrl')
                nss = '{}:'.format(':'.join(ctrl.split(':')[0:-1]))
                ctrl_removed_nss = ctrl.replace(nss, '')
                search_ctrls = cmds.ls('*:{}'.format(ctrl_removed_nss))
                searched_ctrl = search_ctrls[0]

                prop_has_dict[searched_ctrl] = OrderedDict()

                prop_has_dict[searched_ctrl]['name'] = searched_ctrl

                try:
                    part = cmds.getAttr(cp_net + '.propPart')
                    prop_has_dict[searched_ctrl]['propPart'] = part
                except Exception as e:
                    print(traceback.format_exc())

                try:
                    id = cmds.getAttr(cp_net + '.propID')
                    prop_has_dict[searched_ctrl]['propID'] = id
                except Exception as e:
                    print(traceback.format_exc())

                try:
                    space = cmds.getAttr(cp_net + '.space')
                    prop_has_dict[searched_ctrl]['space'] = space
                except Exception as e:
                    print(traceback.format_exc())

                try:
                    jnt = cmds.getAttr(cp_net + '.Root')
                    prop_has_dict[searched_ctrl]['Root'] = jnt
                except Exception as e:
                    print(traceback.format_exc())

                try:
                    root_ctrl = cmds.getAttr(cp_net + '.RootCtrl')
                    prop_has_dict[searched_ctrl]['RootCtrl'] = root_ctrl
                except Exception as e:
                    print(traceback.format_exc())

                try:
                    attach_node = cmds.getAttr(cp_net + '.attachNode')
                    prop_has_dict[searched_ctrl]['attachNode'] = attach_node
                except Exception as e:
                    print(traceback.format_exc())

                try:
                    path = cmds.getAttr(cp_net + '.propPath')
                    prop_has_dict[searched_ctrl]['propPath'] = path
                except Exception as e:
                    print(traceback.format_exc())

        return prop_has_dict

    def add_prop_rotate_values(self, prop_ctrl_qle, prop_ctrl_rot_cmbox):
        # rot_values = [
        #     'default',
        #     'X_90_Y_90',
        #     'X_90_Z_90',
        #     'Y_90_Z_90',
        #     'X_n90_Y_90',
        #     'X_n90_Z_90',
        #     'Y_n90_Z_90',
        #     'X_90_Y_n90',
        #     'X_90_Z_n90',
        #     'Y_90_Z_n90',
        #     'X_n90_Y_n90',
        #     'X_n90_Z_n90',
        #     'Y_n90_Z_n90'
        #     ]

        rot_values = [
            'default',
            '(90, 90, 0)',
            '(90, 0, 90)',
            '(0, 90, 90)',

            '(-90, 90, 0)',
            '(-90, 0, 90)',
            '(0, -90, 90)',

            '(90, -90, 0)',
            '(90, 0, -90)',
            '(0, 90, -90)',

            '(-90, -90, 0)',
            '(-90, 0, -90)',
            '(0, -90, -90)'
            ]


        prop_ctrl_rot_cmbox.addItems(rot_values)

        ctrl = prop_ctrl_qle.text()
        ro = tuple([int(n) for n in cmds.getAttr(ctrl+'.r')[0]])
        if str(ro) in rot_values:
            prop_ctrl_rot_cmbox.setCurrentText(str(ro))

    def prop_rotate_from(self, prop_ctrl_qle, prop_ctrl_rot_cmbox, dum=None):
        ctrl = prop_ctrl_qle.text()
        rot_val = prop_ctrl_rot_cmbox.currentText()

        avatarReferenceTool.prop_rotate_from(ctrl, rot_val)

    # def resizeEvent(self, event):
    #     # MainWindowがリサイズされたときに呼び出されるメソッドです。
    #     # ここでcontent_widgetのサイズをscrollのサイズに合わせて調整します。
    #     self.main_content_widget.resize(self.main_scroll.size())
    #     super().resizeEvent(event)

class FlexLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super(FlexLineEdit, self).__init__(*args, **kwargs)

        # 入力内容が変更されたときにtextChangedシグナルをトリガーします。
        self.textChanged.connect(self.adjustSizeToText)

    def adjustSizeToText(self, text):
        # テキスト幅を計算します。
        text_width = self.fontMetrics().boundingRect(text).width()

        # QLineEditの幅をテキスト幅に適応させます（右に少し余白を追加）。
        self.setFixedWidth(text_width + 10)


if __name__ == '__main__':
    ui = AvatarReferenceTool()
    ui.buildUI()
    ui.show(dockable=True)
