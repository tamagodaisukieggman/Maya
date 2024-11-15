# -*- coding: utf-8 -*-
from maya import cmds, mel
import maya.OpenMaya as om
import maya.OpenMayaAnim as oma
import maya.OpenMayaUI as omui

import maya.api.OpenMaya as om2
import maya.api.OpenMayaAnim as oma2

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


import codecs
from collections import OrderedDict
from datetime import datetime
from distutils.util import strtobool
from functools import partial, wraps
import fnmatch
import functools
import getpass
import json
from logging import getLogger
import math
import os
import re
import subprocess
import traceback
import pdb


CONTROLLERS_FOR_MGPICKER = [
'world_ctrl',
'main_ctrl',
'Root_ctrl',
'ik_Ankle_L_ctrl',
'ik_Ankle_R_ctrl',
'ik_Elbow_L_ctrl',
'ik_Elbow_R_ctrl',
'ik_Knee_L_ctrl',
'ik_Knee_R_ctrl',
'ik_Wrist_L_ctrl',
'ik_Wrist_R_ctrl',
'Cog_ctrl',
'roll_main_Ankle_L_ctrl',
'roll_main_Ankle_R_ctrl',
'ik_rot_Ankle_L_ctrl',
'ik_rot_Ankle_R_ctrl',
'ik_rot_Wrist_L_ctrl',
'ik_rot_Wrist_R_ctrl',
'Hip_ctrl',
'Spine1_ctrl',
'roll_tippytoe_Ankle_L_ctrl',
'roll_tippytoe_Ankle_R_ctrl',
'ik_Toe_L_ctrl',
'ik_Toe_R_ctrl',
'Thigh_L_ctrl',
'Thigh_R_ctrl',
'Spine2_ctrl',
'roll_heel_Ankle_L_ctrl',
'roll_heel_Ankle_R_ctrl',
'ikfk_Ankle_L_ctrl',
'ikfk_Ankle_R_ctrl',
'Knee_L_ctrl',
'Knee_R_ctrl',
'Spine3_ctrl',
'roll_in_Ankle_L_ctrl',
'roll_in_Ankle_R_ctrl',
'Ankle_L_ctrl',
'Ankle_R_ctrl',
'Neck_ctrl',
'Shoulder_L_ctrl',
'Shoulder_R_ctrl',
'roll_out_Ankle_L_ctrl',
'roll_out_Ankle_R_ctrl',
'Toe_L_ctrl',
'Toe_R_ctrl',
'Head_ctrl',
'Arm_L_ctrl',
'Arm_R_ctrl',
'Thumb_01_L_ctrl',
'Index_01_L_ctrl',
'Middle_01_L_ctrl',
'Ring_01_L_ctrl',
'Pinky_01_L_ctrl',
'HandattachOffset_L_ctrl',
'ikfk_Wrist_L_ctrl',
'Thumb_01_R_ctrl',
'Index_01_R_ctrl',
'Middle_01_R_ctrl',
'Ring_01_R_ctrl',
'Pinky_01_R_ctrl',
'HandattachOffset_R_ctrl',
'ikfk_Wrist_R_ctrl',
'roll_Toe_L_ctrl',
'roll_stoptoe_Toe_L_ctrl',
'roll_Toe_R_ctrl',
'roll_stoptoe_Toe_R_ctrl',
'Elbow_L_ctrl',
'Elbow_R_ctrl',
'Thumb_02_L_ctrl',
'Index_02_L_ctrl',
'Middle_02_L_ctrl',
'Ring_02_L_ctrl',
'Pinky_02_L_ctrl',
'Handattach_L_ctrl',
'Thumb_02_R_ctrl',
'Index_02_R_ctrl',
'Middle_02_R_ctrl',
'Ring_02_R_ctrl',
'Pinky_02_R_ctrl',
'Handattach_R_ctrl',
'roll_Ankle_L_ctrl',
'roll_Ankle_R_ctrl',
'Wrist_L_ctrl',
'Wrist_R_ctrl',
'Thumb_03_L_ctrl',
'Index_03_L_ctrl',
'Middle_03_L_ctrl',
'Ring_03_L_ctrl',
'Pinky_03_L_ctrl',
'Thumb_03_R_ctrl',
'Index_03_R_ctrl',
'Middle_03_R_ctrl',
'Ring_03_R_ctrl',
'Pinky_03_R_ctrl',
 ]

def force_zeroout(namespace=None):
    #get the namespace of current picker file.
    if not namespace:
        namespace = get_mgpickernamespace()
    ctrls = [namespace + ctrl for ctrl in CONTROLLERS_FOR_MGPICKER]
    for ctrl in ctrls:
        try:
            cmds.xform(ctrl, t=[0,0,0], ro=[0,0,0], s=[1,1,1])
        except:
            pass

def reset_spaces(attr='space', namespace=None):
    if not namespace:
        namespace = get_mgpickernamespace()
    reset_space_dict = {
        namespace + 'Cog_ctrl':'main',
        namespace + 'ik_Ankle_L_ctrl':'main',
        namespace + 'ik_Ankle_R_ctrl':'main',
        namespace + 'ik_Knee_L_ctrl':'main',
        namespace + 'ik_Knee_R_ctrl':'main',
        namespace + 'ik_Wrist_L_ctrl':'main',
        namespace + 'ik_Wrist_R_ctrl':'main',
        namespace + 'ik_Elbow_L_ctrl':'main',
        namespace + 'ik_Elbow_R_ctrl':'main',

        namespace + 'Neck_ctrl':'spine',

        namespace + 'Handattach_L_ctrl':'wrist',
        namespace + 'Handattach_R_ctrl':'wrist'
    }

    for ctrl, sp_at in reset_space_dict.items():
        get_en_attrs = cmds.addAttr(ctrl + '.' + attr, q=True, en=True)
        spl_get_en_attrs = get_en_attrs.split(':')
        if sp_at in spl_get_en_attrs:
            enum_idx = spl_get_en_attrs.index(sp_at)
            cmds.setAttr(ctrl+'.'+attr, enum_idx)

    # reset_spaces(attr='space')

    cmds.setAttr(namespace + 'ik_Wrist_L_ctrl.autoRot', 1)
    cmds.setAttr(namespace + 'ik_Wrist_R_ctrl.autoRot', 1)

class ReplaceReferenceTool(object):
    def __init__(self):
        self.MAIN_WINDOW = 'Replace Reference Tool'

    def show(self):
        if cmds.workspaceControl(self.MAIN_WINDOW, q=1, ex=1):
            cmds.deleteUI(self.MAIN_WINDOW)

        self.win = cmds.workspaceControl(self.MAIN_WINDOW, l=self.MAIN_WINDOW)

        self.layout()

        cmds.showWindow(self.win)

    def layout(self):
        self.init_txtfield_asset_filter = 'ply*male*female'
        self.init_work_tab_label = 'Work'
        self.init_share_tab_label = 'Share'
        self.init_txtfield_file_filter = 'mdl'
        self.init_txtfield_exclude_filter = 'head*test*tmp*maya*ui*1000'

        menuBarLayout = cmds.menuBarLayout(p=self.win)
        cmds.menu(label='Edit')
        cmds.menuItem(label='Save Settings', c=self.save_settings)
        cmds.menuItem(label='Reset Settings', c=self.reset_settings)
        cmds.menuItem(label='Reload Settings', c=self.load_settings)
        cmds.menuItem(d=1)
        cmds.menuItem(label='Reload', c=self.all_reload)
        cmds.menuItem(label='ReferenceEditor', c='cmds.ReferenceEditor()')
        self.history_menuitems = cmds.menuItem(label='History', sm=1)
        self.history_items_buff = []

        self.col_layout_00 = cmds.columnLayout(adj=1, rs=7)

        self.txtfield_asset_filter = cmds.textFieldGrp(l='Assets Filter', tx=self.init_txtfield_asset_filter, tcc=self.all_reload, ad2=2, cat=[1, 'left', 50], p=self.col_layout_00)

        self.rowCol_layout_00 = cmds.rowColumnLayout(nr=1)

        self.opsmenu_tab = cmds.optionMenu( l='Tab', cc=self.all_reload)
        cmds.menuItem(l=self.init_work_tab_label, p=self.opsmenu_tab)
        cmds.menuItem(l=self.init_share_tab_label, p=self.opsmenu_tab)

        self.opsmenu_sub = cmds.optionMenu( l='Sub Cat', cc=self.load_assets_list)
        self.opsmenu_ast = cmds.optionMenu( l='Asset', cc=self.load_assets_list)

        self.txtfield_file_filter = cmds.textFieldGrp(l='List Filter', tx=self.init_txtfield_file_filter, tcc=self.load_assets_list, ad2=2, cat=[1, 'left', 50], p=self.col_layout_00)
        self.txtfield_exclude_filter = cmds.textFieldGrp(l='Exclude Filter', tx=self.init_txtfield_exclude_filter, tcc=self.load_assets_list, ad2=2, cat=[1, 'left', 50], p=self.col_layout_00)

        self.pan_layout_00 = cmds.paneLayout(cn='vertical2', p=self.col_layout_00)

        self.texSclLst_layout_src = cmds.textScrollList()
        self.texSclLst_layout_dst = cmds.textScrollList()

        self.apply_button = cmds.button(l='Apply', p=self.col_layout_00, c=self.apply_replace)

        self.list_sub_cat_array, self.list_asset_array, self.list_vari_array, self.list_file_array = self.search_work_path()
        self.ref_path_dict = self.search_references()

        self.load_assets_list()

        cmds.popupMenu(p=self.texSclLst_layout_src)
        cmds.menuItem(l='Show in Explorer', c=self.show_in_explorer_src)

        cmds.popupMenu(p=self.texSclLst_layout_dst)
        cmds.menuItem(l='Show in Explorer', c=self.show_in_explorer_dst)

        self.get_history_items()
        self.add_history_items()

        # load settings
        self.load_settings()


    def search_work_path(self):
        self.opsmenu_tab_value = cmds.optionMenu(self.opsmenu_tab, q=1, v=1)
        if self.opsmenu_tab_value == 'Work':
            search_path = 'W:/production/work/asset/character'
        else:
            search_path = '//CGS-STR-FAS05/100_projects/051_world/production/share/asset/character'
            result = cmds.confirmDialog(title='Change Share Tab',
                                       message='ファイル取得に時間がかかる場合があります。Share領域を検索しますか？',
                                       button=['OK', 'Cancel'],
                                       defaultButton='OK',
                                       cancelButton='Cancel',
                                       dismissString='Cancel')

            if not result == 'OK':
                cmds.optionMenu(self.opsmenu_tab, e=1, v='Work')
                return


        if not os.path.exists(search_path):
            cmds.error("Unable to find folder.{}".format(search_path))
            return

        self.filter_words = cmds.textFieldGrp(self.txtfield_asset_filter, q=1, tx=1)

        sub_cat_array = []
        asset_array = []
        vari_array = []
        file_array = []
        exclude = ['animation', 'hair', 'head', 'rig', 'test']
        for root, dirs, files in os.walk(search_path, topdown=True):
            dirs[:] = [d for d in dirs if d not in exclude]
            for fname in files:
                for fw in self.filter_words.split('*'):
                    if fw in fname:
                        file_path = os.path.join(root, fname)
                        search_file = file_path.replace('\\', '/')

                        if self.opsmenu_tab_value == 'Work':
                            sub_cat_array.append('/'.join(search_file.split('/')[:6]))
                            asset_array.append('/'.join(search_file.split('/')[:7]))
                            vari_array.append('/'.join(search_file.split('/')[:8]))

                            if search_file.split('/')[9] == 'model':
                                if search_file.endswith('.mb') or search_file.endswith('.ma'):
                                    file_array.append('/'.join(search_file.split('/')[:14]))

                        else:
                            sub_cat_array.append('/'.join(search_file.split('/')[:10]))
                            asset_array.append('/'.join(search_file.split('/')[:11]))
                            vari_array.append('/'.join(search_file.split('/')[:12]))

                            if search_file.split('/')[13] == 'model':
                                if search_file.endswith('.mb') or search_file.endswith('.ma'):
                                    file_array.append('/'.join(search_file.split('/')[:18]))


        list_sub_cat_array = list(set(sub_cat_array))
        list_asset_array = list(set(asset_array))
        list_vari_array = list(set(vari_array))
        list_file_array = list(set(file_array))

        # for menuItems
        items_list_sub_cat_array = [i_sub_cat.split('/')[-1] for i_sub_cat in list_sub_cat_array]
        items_list_asset_cat_array = [i_asset_cat.split('/')[-1] for i_asset_cat in list_asset_array]

        items_list_sub_cat_array.sort()
        items_list_asset_cat_array.sort()

        cmds.optionMenu(self.opsmenu_sub, e=1, dai=1)
        cmds.optionMenu(self.opsmenu_ast, e=1, dai=1)

        self.load_menuItems(array=items_list_sub_cat_array, parent=self.opsmenu_sub)
        self.load_menuItems(array=items_list_asset_cat_array, parent=self.opsmenu_ast)

        return list_sub_cat_array, list_asset_array, list_vari_array, list_file_array


    def search_references(self):
        ref_path_dict = OrderedDict()
        for rf in cmds.ls(rf=True, r=1):
            ref_path_dict[rf] = cmds.referenceQuery(rf, f=True)

        return ref_path_dict


    def load_assets_list(self, *args):
        cmds.textScrollList(self.texSclLst_layout_src, e=1, ra=1)
        cmds.textScrollList(self.texSclLst_layout_dst, e=1, ra=1)

        self.opsmenu_tab_value = cmds.optionMenu(self.opsmenu_tab, q=1, v=1)
        self.opsmenu_sub_value = cmds.optionMenu(self.opsmenu_sub, q=1, v=1)
        self.opsmenu_ast_value = cmds.optionMenu(self.opsmenu_ast, q=1, v=1)

        self.file_filter_words = cmds.textFieldGrp(self.txtfield_file_filter, q=1, tx=1)
        self.exclude_filter_words = cmds.textFieldGrp(self.txtfield_exclude_filter, q=1, tx=1)

        self.set_asset_items = OrderedDict()
        for file_name in self.list_file_array:
            if self.opsmenu_sub_value in file_name and self.opsmenu_ast_value in file_name:
                for fw in self.file_filter_words.split('*'):
                    if fw in file_name.split('/')[-1]:
                        self.set_asset_items[file_name.split('/')[-1]] = file_name

            if self.exclude_filter_words:
                for ew in self.exclude_filter_words.split('*'):
                    if ew in file_name.split('/')[-1]:
                        try:
                            self.set_asset_items.pop(file_name.split('/')[-1])
                        except KeyError:
                            print(traceback.format_exc())


        self.asset_items_sorted_list = self.set_asset_items.keys()
        self.asset_items_sorted_list.sort(reverse=True)

        self.ref_items_sorted_list = self.ref_path_dict.keys()
        self.ref_items_sorted_list.sort()

        cmds.textScrollList(self.texSclLst_layout_src, e=1, a=self.ref_items_sorted_list)
        cmds.textScrollList(self.texSclLst_layout_dst, e=1, a=self.asset_items_sorted_list)


    def load_menuItems(self, array=None, parent=None):
        for item in array:
            cmds.menuItem(l=item, p=parent)


    def all_reload(self, *args):
        try:
            self.list_sub_cat_array, self.list_asset_array, self.list_vari_array, self.list_file_array = self.search_work_path()
            self.ref_path_dict = self.search_references()
            self.load_assets_list()
        except:
            print(traceback.format_exc())


    def apply_replace(self, *args):
        sel_src_item = cmds.textScrollList(self.texSclLst_layout_src, q=1, si=1)
        sel_dst_item = cmds.textScrollList(self.texSclLst_layout_dst, q=1, si=1)

        if sel_dst_item is None or sel_src_item is None:
            cmds.error('You have to select items on lists.')
            return


        replace_path = self.set_asset_items[sel_dst_item[0]]
        ref_node = sel_src_item[0]

        if replace_path.endswith('.ma'):
            asset_type = 'mayaAscii'
        elif replace_path.endswith('.mb'):
            asset_type = 'mayaBinary'

        cmds.file(replace_path,
                  type=asset_type,
                  options="v=0;p=17;f=0",
                  loadReference=ref_node)


        self.save_settings()


    def add_history_items(self, *args):
        if self.history_items_buff:
            for del_mi in self.history_items_buff:
                cmds.deleteUI(del_mi)

        dreversed = OrderedDict()
        for k in reversed(self.history_items):
            dreversed[k] = self.history_items[k]

        for k, v in dreversed.items():
            mi = cmds.menuItem(l=k, c=partial(self.load_partial_historyItems, v[0], v[1], v[2], v[3], v[4], v[5], k.split('>>')[0], k.split('>>')[1]), p=self.history_menuitems)
            self.history_items_buff.append(mi)


    def load_partial_historyItems(self, txt_ast, tab_value, sub_value, ast_value, file_value, ex_value, src_refnode, dst_data, *args):
        cmds.textFieldGrp(self.txtfield_asset_filter, e=1, tx=txt_ast)
        cmds.optionMenu(self.opsmenu_tab, e=1, sl=int(tab_value))
        cmds.optionMenu(self.opsmenu_sub, e=1, sl=int(sub_value))
        cmds.optionMenu(self.opsmenu_ast, e=1, sl=int(ast_value))
        cmds.textFieldGrp(self.txtfield_file_filter, e=1, tx=file_value)
        cmds.textFieldGrp(self.txtfield_exclude_filter, e=1, tx=ex_value)

        self.load_assets_list()

        cmds.textScrollList(self.texSclLst_layout_src, e=1, si=src_refnode)
        cmds.textScrollList(self.texSclLst_layout_dst, e=1, si=dst_data)


    def get_history_items(self, *args):
        try:
            self.history_items = load_optionvar('Replace_Reference_Tool_for_world')[6]
        except:
            print(traceback.format_exc())
            self.history_items = OrderedDict()


    def get_files(self, path='.'):
        total = []
        for p in os.listdir(path):
            full_path = os.path.join(path, p)
            if os.path.isfile(full_path):
                search_file = full_path.replace('\\', '/')
                total.append(search_file)
            elif os.path.isdir(full_path):
                for search_file in get_files(full_path):
                    total.append(search_file)
        return total


    def save_settings(self, *args):
        asset_filter_value = cmds.textFieldGrp(self.txtfield_asset_filter, q=1, tx=1)
        opsmenu_tab_value = cmds.optionMenu(self.opsmenu_tab, q=1, sl=1)
        opsmenu_sub_value = cmds.optionMenu(self.opsmenu_sub, q=1, sl=1)
        opsmenu_ast_value = cmds.optionMenu(self.opsmenu_ast, q=1, sl=1)
        txtfield_file_filter_value = cmds.textFieldGrp(self.txtfield_file_filter, q=1, tx=1)
        txtfield_exclude_filter_value = cmds.textFieldGrp(self.txtfield_exclude_filter, q=1, tx=1)


        sel_src_item = cmds.textScrollList(self.texSclLst_layout_src, q=1, si=1)
        sel_dst_item = cmds.textScrollList(self.texSclLst_layout_dst, q=1, si=1)

        try:
            self.get_history_items()
            self.history_items['{}>>{}'.format(sel_src_item[0], sel_dst_item[0])] = [asset_filter_value,
                                                              opsmenu_tab_value,
                                                              opsmenu_sub_value,
                                                              opsmenu_ast_value,
                                                              txtfield_file_filter_value,
                                                              txtfield_exclude_filter_value,]

            self.add_history_items()

            if 10 < len(self.history_items.keys()):
                self.history_items.pop(self.history_items.keys()[-1])


        except:
            print(traceback.format_exc())


        save_items = OrderedDict()
        save_items['Replace_Reference_Tool_for_world'] = [asset_filter_value,
                                                          opsmenu_tab_value,
                                                          opsmenu_sub_value,
                                                          opsmenu_ast_value,
                                                          txtfield_file_filter_value,
                                                          txtfield_exclude_filter_value,
                                                          self.history_items]


        for key, value in save_items.items():
            v = str(value)
            cmds.optionVar(sv=[key, v])


    def show_in_explorer_dst(self, *args):
        sel_dst_item = cmds.textScrollList(self.texSclLst_layout_dst, q=1, si=1)
        replace_path = self.set_asset_items[sel_dst_item[0]]
        path = os.path.realpath('/'.join(replace_path.split('/')[:-1]))
        os.startfile(path)


    def show_in_explorer_src(self, *args):
        sel_src_item = cmds.textScrollList(self.texSclLst_layout_src, q=1, si=1)
        replace_path = self.ref_path_dict[sel_src_item[0]]
        path = os.path.realpath('/'.join(replace_path.split('/')[:-1]))
        os.startfile(path)


    def load_settings(self, *args):
        try:
            values = load_optionvar('Replace_Reference_Tool_for_world')

            for i, value in enumerate(values):
                # print(value)
                if i == 0:
                    cmds.textFieldGrp(self.txtfield_asset_filter, e=1, tx=value)
                elif i == 1:
                    cmds.optionMenu(self.opsmenu_tab, e=1, sl=int(value))
                elif i == 2:
                    cmds.optionMenu(self.opsmenu_sub, e=1, sl=int(value))
                elif i == 3:
                    cmds.optionMenu(self.opsmenu_ast, e=1, sl=int(value))
                elif i == 4:
                    cmds.textFieldGrp(self.txtfield_file_filter, e=1, tx=value)
                elif i == 5:
                    cmds.textFieldGrp(self.txtfield_exclude_filter, e=1, tx=value)

            self.load_assets_list()

        except Exception as e:
            print(traceback.format_exc())
            print('Load settings Error:{}'.format(e))


    def reset_settings(self, *args):
        cmds.textFieldGrp(self.txtfield_asset_filter, e=1, tx=self.init_txtfield_asset_filter)
        cmds.optionMenu(self.opsmenu_tab, e=1, v=self.init_work_tab_label)
        cmds.textFieldGrp(self.txtfield_file_filter, e=1, tx=self.init_txtfield_file_filter)
        cmds.textFieldGrp(self.txtfield_exclude_filter, e=1, tx=self.init_txtfield_exclude_filter)

        self.all_reload()

        self.save_settings()


def load_optionvar(key):
    if cmds.optionVar(ex=key):
        return eval(cmds.optionVar(q=key))
    else:
        return None


class RefreshTool(object):
    def __init__(self):
        self.MAIN_WINDOW = 'Refresh Tool'

    def show(self):
        if cmds.workspaceControl(self.MAIN_WINDOW, q=1, ex=1):
            cmds.deleteUI(self.MAIN_WINDOW)

        self.win = cmds.workspaceControl(self.MAIN_WINDOW, l=self.MAIN_WINDOW, rt=1)

        self.layout()

        cmds.showWindow(self.win)

        cmds.scriptJob(e=['SceneOpened', self.add_items_in_namespace_menu], p=self.win, rp=1)


    def layout(self):
        self.row_lay_common_settings = {'cw2':(80, 100),
                                   'cl2':['center', 'left'],
                                   'ct2':['right', 'left'],
                                   'h':24}

        self.frm_lay_common_settings = {'cll':1}

        menuBarLayout = cmds.menuBarLayout(p=self.win)
        cmds.menu(label='Maya Menu')
        cmds.menuItem(label='Optimize Scene', c='mel.eval("OptimizeSceneOptions;")')

        # cmds.menuItem(label='Save Settings', c=self.save_settings)
        # cmds.menuItem(label='Reset Settings', c=self.reset_settings)
        # cmds.menuItem(label='Reload Settings', c=self.load_settings)
        # cmds.menuItem(d=1)
        # cmds.menuItem(label='Reload', c=self.all_reload)
        # cmds.menuItem(label='ReferenceEditor', c='cmds.ReferenceEditor()')

        self.scl_lay = cmds.scrollLayout(p=self.MAIN_WINDOW, cr=1)

        self.nss_ops_menu = cmds.optionMenu(l='NameSpace')
        self.add_items_in_namespace_menu()

        self.plot_lay(self.scl_lay)
        self.del_animLayers_lay(self.scl_lay)
        self.run_all_lay(self.scl_lay)

        cmds.setParent('..')


    def list_namespaces(self):
        exclude_list = ['UI', 'shared']

        current = cmds.namespaceInfo(cur=1)
        cmds.namespace(set=':')
        namespaces = ['{}'.format(ns) for ns in cmds.namespaceInfo(lon=1) if ns not in exclude_list]
        cmds.namespace(set=current)

        return namespaces

    def load_menuItems(self, array=None, parent=None):
        for item in array:
            cmds.menuItem(l=item, p=parent)

    def add_items_in_namespace_menu(self):
        namespaces = self.list_namespaces()
        cmds.optionMenu(self.nss_ops_menu, e=1, dai=1)
        cmds.menuItem(l='', p=self.nss_ops_menu)
        self.load_menuItems(array=namespaces, parent=self.nss_ops_menu)

    def change_managed(self, *args, **kwargs):
        print(args, kwargs)

    # Plot
    def plot_lay(self, parent=None):
        # correct
        # self.cor_mch_frm_lay = cmds.frameLayout(p=parent, l='Correct Match', **self.frm_lay_common_settings)

        cmds.separator(p=parent, st='in')
        self.cor_mch_all_cb = cmds.checkBox(l='Correct Match', v=1, p=parent)
        self.cor_mch_row = cmds.rowLayout(adj=5, p=parent, nc=6, **self.row_lay_common_settings)

        self.l_hand_cor_mch_cb = cmds.checkBox(l='Left Hand', v=1, p=self.cor_mch_row)
        self.r_hand_cor_mch_cb = cmds.checkBox(l='Right Hand', v=1, p=self.cor_mch_row)
        self.l_foot_cor_mch_cb = cmds.checkBox(l='Left Foot', v=1, p=self.cor_mch_row)
        self.r_foot_cor_mch_cb = cmds.checkBox(l='Right Foot', v=1, p=self.cor_mch_row)
        cmds.button(l='Done!', c=self.cor_mch_main)


    def cor_mch_main(self, *args):
        namespace = cmds.optionMenu(self.nss_ops_menu, q=1, v=1)
        if not namespace:
            namespace = ''
        elif not namespace.endswith(':'):
            namespace = namespace + ':'

        self.l_hand_cor_mch_val = cmds.checkBox(self.l_hand_cor_mch_cb, q=1, v=1)
        self.r_hand_cor_mch_val = cmds.checkBox(self.r_hand_cor_mch_cb, q=1, v=1)
        self.l_foot_cor_mch_val = cmds.checkBox(self.l_foot_cor_mch_cb, q=1, v=1)
        self.r_foot_cor_mch_val = cmds.checkBox(self.r_foot_cor_mch_cb, q=1, v=1)

        try:
            refresh_tool_correctMatch(namespace=namespace,
                              l_hand=self.l_hand_cor_mch_val,
                              r_hand=self.r_hand_cor_mch_val,
                              l_foot=self.l_foot_cor_mch_val,
                              r_foot=self.r_foot_cor_mch_val)
        except:
            print(traceback.format_exc())


    # Delete AnimationLayers
    def del_animLayers_lay(self, parent=None):
        # correct
        # self.dal_frm_lay = cmds.frameLayout(p=parent, l='Delete AnimLayers', **self.frm_lay_common_settings)

        cmds.separator(p=parent, st='in')
        self.dal_all_cb = cmds.checkBox(l='Delete AnimLayers', v=1, p=parent)
        self.dal_row = cmds.rowLayout(adj=3, p=parent, nc=6, **self.row_lay_common_settings)

        self.dal_cb = cmds.checkBox(l='Exclude BaseAnimation', v=1, p=self.dal_row)
        self.dar_cb = cmds.checkBox(l='Rename animCurves', v=1, p=self.dal_row)
        cmds.button(l='Done!', c=self.del_animLayers_main)


    def del_animLayers_main(self, *args):
        self.dal_cb_val = cmds.checkBox(self.dal_cb, q=1, v=1)
        self.dar_cb_val = cmds.checkBox(self.dar_cb, q=1, v=1)
        try:
            refresh_tool_delete_all_animLayers(exclude_baseAnimation=self.dal_cb_val, rename_animCurves=self.dar_cb_val)
        except:
            print(traceback.format_exc())


    # Run All
    def run_all_lay(self, parent=None):
        cmds.separator(p=parent, st='in')

        self.check_all_row = cmds.rowLayout(adj=2, p=parent, nc=6, **self.row_lay_common_settings)
        self.check_all_cb = cmds.checkBox(l='All Check', v=1, p=self.check_all_row, cc=self.all_check)
        cmds.button(l='Run All!', p=self.check_all_row, c=self.run_all)


    def all_check(self, args):
        cmds.checkBox(self.cor_mch_all_cb, e=1, v=args)
        cmds.checkBox(self.dal_all_cb, e=1, v=args)


    def run_all(self, *args):
        self.cor_mch_all_cb_val = cmds.checkBox(self.cor_mch_all_cb, q=1, v=1)
        if self.cor_mch_all_cb_val:
            self.cor_mch_main()

        self.dal_all_cb_val = cmds.checkBox(self.dal_all_cb, q=1, v=1)
        if self.dal_all_cb_val:
            self.del_animLayers_main()


def get_trs_attrs(obj=None, local=None, pos=True, rot=True, scl=True, roo=True):
    """
    return translate, rotate, scale, rotateOrder, jointOrient
    """
    if not obj:
        sel = cmds.ls(os=1)
        if sel:
            obj = sel[0]
        else:
            return

    rel = 0
    wld = 1

    get_t = None
    get_ro = None
    get_s = None
    get_roo = None
    get_jo = None

    if local:
        rel = 1
        wld = 0

    if pos:
        get_t = cmds.xform(obj, q=1, t=1, ws=wld, os=rel)
    if rot:
        get_ro = cmds.xform(obj, q=1, ro=1, ws=wld, os=rel)
    if scl:
        get_s = cmds.xform(obj, q=1, s=1, ws=wld, os=rel)
    if roo:
        get_roo = cmds.xform(obj, q=1, roo=1)

    if cmds.objectType(obj) == 'joint':
        get_jo = cmds.getAttr(obj+'.jo')
        get_jo = get_jo[0]
        # cmds.setAttr(sel[0]+'.jo', *get_jo[0])

    return get_t, get_ro, get_s, get_roo, get_jo


def set_pole_vec(start=None, mid=None, end=None, move=None, obj=None):
    start = cmds.xform(start, q=True, t=True, ws=True)
    mid = cmds.xform(mid, q=True, t=True, ws=True)
    end = cmds.xform(end, q=True, t=True, ws=True)

    startV = om.MVector(start[0] ,start[1],start[2])
    midV = om.MVector(mid[0] ,mid[1],mid[2])
    endV = om.MVector(end[0] ,end[1],end[2])
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
    matrixM = om.MMatrix()
    om.MScriptUtil.createMatrixFromList(matrixV , matrixM)
    matrixFn = om.MTransformationMatrix(matrixM)
    rot = matrixFn.eulerRotation()

    pvLoc = cmds.spaceLocator(n='poleVecPosLoc')
    cmds.xform(pvLoc[0] , ws =1 , t= (finalV.x , finalV.y ,finalV.z))
    cmds.xform(pvLoc[0] , ws = 1 , rotation = ((rot.x/math.pi*180.0),(rot.y/math.pi*180.0),(rot.z/math.pi*180.0)))
    cmds.select(pvLoc[0])
    cmds.move(move, 0, 0, r=1, os=1, wd=1)

    cmds.matchTransform(obj, pvLoc[0])
    cmds.delete(pvLoc[0])


def refresh_tool_delete_all_animLayers(exclude_baseAnimation=None, rename_animCurves=None):
    mel.eval('source "C:/Program Files/Autodesk/Maya{}/scripts/others/performAnimLayerMerge.mel"'.format(cmds.about(version=True)))

    deleteMerged = True
    if cmds.optionVar(exists='animLayerMergeDeleteLayers'):
        deleteMerged = cmds.optionVar(query='animLayerMergeDeleteLayers')

    cmds.optionVar(intValue=('animLayerMergeDeleteLayers', 1))

    animLayers = cmds.ls(type='animLayer')
    if animLayers:
        mel.eval('animLayerMerge {"%s"}' % '","'.join(animLayers))

        if exclude_baseAnimation:
            if 'BaseAnimation' in animLayers:
                animLayers.remove('BaseAnimation')

        [cmds.delete(anl) for anl in animLayers if cmds.objExists(anl)]

    if rename_animCurves:
        def custom_rename(obj=None, rplname=None):
            if cmds.objExists(obj):
                cmds.rename(obj, rplname)

        animCurves = cmds.ls(type=['animCurveTL', 'animCurveTA', 'animCurveTU'])
        not_connects = []
        error_crvs = []
        for ancv in animCurves:
            connected_plug = cmds.listConnections(ancv, d=1, p=1, scn=1) or None
            if not connected_plug:
                not_connects.append(ancv)

            else:
                spl_connected_plugs = re.split('[:\[\].]', connected_plug[0].split(':')[-1])
                spl_connected_plugs_remove_empty = [cprm for cprm in spl_connected_plugs if not cprm == '']
                spl_connected_plug = '_'.join(spl_connected_plugs_remove_empty)
                custom_rename(ancv, spl_connected_plug)

def renameDuplicates(duplicated=None, prefix=''):
    #Find all objects that have the same shortname as another
    #We can indentify them because they have | in the name
    duplicates = [f for f in duplicated if '|' in f]
    #Sort them by hierarchy so that we don't rename a parent before a child.
    duplicates.sort(key=lambda obj: obj.count('|'), reverse=True)

    #if we have duplicates, rename them
    renamed = []
    if duplicates:
        for name in duplicates:
            # extract the base name
            m = re.compile("[^|]*$").search(name)
            shortname = m.group(0)

            # extract the numeric suffix
            m2 = re.compile(".*[^0-9]").match(shortname)
            if m2:
                stripSuffix = m2.group(0)
            else:
                stripSuffix = shortname

            #rename, adding '#' as the suffix, which tells maya to find the next available number
            newname = cmds.rename(name, (prefix + stripSuffix))

            renamed.append(newname)

        return renamed

    else:
        return duplicated

def simplebake(objects, start):
    try:
        cmds.refresh(su=1)
        cmds.bakeResults(objects,
                         at=['rx', 'ry', 'rz', 'tx', 'ty', 'tz'],
                         sparseAnimCurveBake=False,
                         minimizeRotation=False,
                         removeBakedAttributeFromLayer=False,
                         removeBakedAnimFromLayer=False,
                         oversamplingRate=1,
                         bakeOnOverrideLayer=False,
                         preserveOutsideKeys=True,
                         simulation=True,
                         sampleBy=1,
                         shape=False,
                         t=((cmds.playbackOptions(q=1, min=1), cmds.playbackOptions(q=1, max=1))),
                         disableImplicitControl=True,
                         controlPoints=False)
        cmds.refresh(su=0)

    except:
        print(traceback.format_exc())
        cmds.refresh(su=0)

    cmds.currentTime(start)


def euler_to_quaternion(yaw, pitch, roll, order):
    yaw = math.radians(yaw)
    pitch = math.radians(pitch)
    roll = math.radians(roll)

    if (order == 'xyz'):
        qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
        qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
        qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
        qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)

    elif (order == 'yzx'):
        qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
        qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) - math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
        qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
        qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)

    elif (order == 'zxy'):
        qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
        qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) - math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
        qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
        qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)

    elif (order == 'xzy'):
        qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
        qy = math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) + math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
        qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
        qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)

    elif (order == 'yxz'):
        qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
        qy = math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) + math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
        qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
        qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)

    elif (order == 'zyx'):
        qx = math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2) + math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2)
        qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) - math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
        qz = math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) + math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
        qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)


    return [qx, qy, qz, qw]

def quaternion_to_euler(x, y, z, w):
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    X = math.degrees(math.atan2(t0, t1))

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    Y = math.degrees(math.asin(t2))

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    Z = math.degrees(math.atan2(t3, t4))

    return X, Y, Z


def crop_rotation(degree):
    if (degree > 180):
        return degree -360

    elif (degree < -180):
        return degree + 360

    else:
        return degree


def convertRotateOrderFunc(sel=None, root_jnt = 'ref:root_jnt', prefix = 'dummybake_', nss = 'ref:', ik_pv=True,
                       startFrame = None, endFrame = None, order = 'xyz', delete_dummy=None, correct_anim=None,
                       external=None):
    try:
        cmds.refresh(su=1)
        convertRotateOrder(sel, root_jnt, prefix, nss, ik_pv, startFrame, endFrame, order, delete_dummy, correct_anim, external)
        cmds.refresh(su=0)
    except Exception as e:
        print(traceback.format_exc())
        cmds.refresh(su=0)


# convertRotateOrderFunc(sel=None, root_jnt = 'male00_all1000_mdl_def:root_jnt', prefix = '', nss = 'male00_all1000_mdl_def:', ik_pv=False,
#                        startFrame = None, endFrame = None, order = 'yxz', delete_dummy=False, correct_anim=True, external=True)

# get joints distance
def get_distance(objA, objB):
    gObjA = cmds.xform(objA, q=True, t=True, ws=True)
    gObjB = cmds.xform(objB, q=True, t=True, ws=True)

    return math.sqrt(math.pow(gObjA[0]-gObjB[0],2)+math.pow(gObjA[1]-gObjB[1],2)+math.pow(gObjA[2]-gObjB[2],2))

# def build_softik(self):
def create_softik_locators(nss=None, jointList=None, softik_ik_ctrl=None):
    jointList = [nss+jt for jt in jointList]
    softik_ik_ctrl = nss+softik_ik_ctrl
    softik_value = 20
    softik_axis = 'translateX'

    softik_loc_sets = '{}_softik_loc_sets'.format(softik_ik_ctrl)
    if not cmds.objExists(softik_loc_sets):
        cmds.sets(n=softik_loc_sets, em=1)

    else:
        cmds.select(softik_loc_sets, ne=1)
        [cmds.delete(obj) for obj in cmds.pickWalk(d='down') if cmds.objExists(obj)]
        cmds.sets(n=softik_loc_sets, em=1)


    softik_loc_gp = '{}_softik_loc_gp'.format(softik_ik_ctrl)
    if not cmds.objExists(softik_loc_gp):
        cmds.createNode('transform', n=softik_loc_gp, ss=1)

    length = 0.0
    i = 0
    for jnt in jointList:
        if i == 0:
            pass
        else:
            length += get_distance(jointList[i-1], jnt)
        i += 1

    # locators
    loc_a = '{}_softIkLoc'.format(jointList[0])
    loc_b = '{}_softIkLoc'.format(jointList[-1])
    loc_c = '{}_exp_softIkLoc'.format(jointList[-1])
    loc_d = '{}_aimobj_softIkLoc'.format(jointList[-1])

    locs = [loc_a, loc_b, loc_c, loc_d]

    [cmds.spaceLocator(n='{}'.format(loc)) for loc in locs]

    cmds.parent(loc_b, loc_a)
    cmds.parent(loc_c, loc_a)
    cmds.parent(loc_d, loc_a)

    # const
    const_loc = cmds.spaceLocator(n='{0}_const_softIkloc'.format(jointList[-1]))
    # cmds.matchTransform(const_loc[0], softik_ik_ctrl)

    pac = cmds.parentConstraint(softik_ik_ctrl, const_loc[0], w=1)
    simplebake([const_loc[0]], cmds.currentTime(q=1))
    cmds.delete(pac)

    cmds.pointConstraint(jointList[0], loc_a, w=1)
    cmds.pointConstraint(const_loc[0], loc_b, w=1)
    cmds.matchTransform(loc_d, const_loc[0])
    cmds.parent(loc_d, const_loc[0])
    cmds.move(0, 0, 10, loc_d, r=1, os=1, wd=1)
    cmds.setAttr('{0}.v'.format(loc_a), 0)
    cmds.setAttr('{0}.v'.format(loc_d), 0)

    aimConst_options = {}
    aimConst_options['offset'] = [0,0,0]
    aimConst_options['aimVector'] = [1,0,0]
    aimConst_options['upVector'] = [0,0,1]
    aimConst_options['worldUpType'] = "object"
    aimConst_options['worldUpObject'] = loc_d

    cmds.aimConstraint(const_loc[0], loc_a, w=1, **aimConst_options)
    cmds.pointConstraint(loc_c, softik_ik_ctrl, w=1)

    # softik_ik_ctrl = const_loc[0]
    # addAttr
    if 'softIk' not in cmds.listAttr(const_loc[0]):
        cmds.addAttr(const_loc[0], ln='softIk', k=1, at='double', dv=0, min=0, max=softik_value)
        cmds.setAttr('{}.{}'.format(const_loc[0], 'softIk'), l=0)
    else:
        cmds.deleteAttr(const_loc[0], at='softIk')
        cmds.addAttr(const_loc[0], ln='softIk', k=1, at='double', dv=0, min=0, max=softik_value)
        cmds.setAttr('{}.{}'.format(const_loc[0], 'softIk'), l=0)

    exp = cmds.createNode('expression', n='{}_softIkExp'.format(softik_ik_ctrl))
    cmds.expression(exp, e=1, s=u"""\nif ({0}.{1} > ({2} - {3}.softIk))\n\t{4}.{1} = ({2} - {3}.softIk) + {3}.softIk * (1-exp( -({0}.{1} - ({2} - {3}.softIk)) /{5}));\nelse\n\t{4}.{1} = {0}.{1}""".format(loc_b, softik_axis, length, const_loc[0], loc_c, softik_value), ae=0, uc='all')

    cmds.parent(const_loc[0], softik_loc_gp)
    cmds.parent(loc_a, softik_loc_gp)

    cmds.sets(softik_loc_gp, add=softik_loc_sets)
    cmds.sets(const_loc[0], add=softik_loc_sets)
    cmds.sets(loc_a, add=softik_loc_sets)
    cmds.sets(exp, add=softik_loc_sets)

    cmds.select(const_loc[0], r=1)


def create_distance_weight(nodes=None):
    connect_dict = {}
    connect_dict['s_m'] = list()
    connect_dict['m_e'] = list()
    connect_dict['s_e'] = list()
    disbs = list()
    for i, obj in enumerate(nodes):
        disb = cmds.createNode('distanceBetween', ss=True)
        dcmx = cmds.createNode('decomposeMatrix', ss=True)
        disbs.append(disb)
        cmds.connectAttr(
            '{}.worldMatrix[0]'.format(obj),
            '{}.inputMatrix'.format(dcmx),
            f=True
            )
        if i == 0 or i == 1:
            connect_dict['s_m'].append(dcmx)
        if i == 1 or i == 2:
            connect_dict['m_e'].append(dcmx)
        if i == 0 or i == 2:
            connect_dict['s_e'].append(dcmx)


    dcmxs = list()
    dcmxs.append(connect_dict['s_m'])
    dcmxs.append(connect_dict['m_e'])
    dcmxs.append(connect_dict['s_e'])

    for dis, dcmx in zip(disbs, dcmxs):
        cmds.connectAttr(
            '{}.outputTranslate'.format(dcmx[0]),
            '{}.point1'.format(dis),
            f=True
            )

        cmds.connectAttr(
            '{}.outputTranslate'.format(dcmx[1]),
            '{}.point2'.format(dis),
            f=True
            )


    dis_pma = cmds.createNode('plusMinusAverage', ss=True)
    dis_md = cmds.createNode('multiplyDivide', ss=True)
    dis_w_md = cmds.createNode('multiplyDivide', ss=True)
    weight_param_md = cmds.createNode('multiplyDivide', ss=True)

    cmds.connectAttr(
        disbs[0] + '.distance',
        dis_pma + '.input1D[0]',
        f=True
    )
    cmds.connectAttr(
        disbs[1] + '.distance',
        dis_pma + '.input1D[1]',
        f=True
    )

    # md
    cmds.setAttr(
        dis_md + '.operation',
        2
    )

    cmds.connectAttr(
        disbs[2] + '.distance',
        dis_md + '.input1X',
        f=True
    )

    cmds.connectAttr(
        disbs[0] + '.distance',
        dis_md + '.input1Y',
        f=True
    )

    cmds.connectAttr(
        disbs[1] + '.distance',
        dis_md + '.input1Z',
        f=True
    )

    #
    cmds.connectAttr(
        dis_pma + '.output1D',
        dis_md + '.input2X',
        f=True
    )

    cmds.connectAttr(
        disbs[2] + '.distance',
        dis_md + '.input2Y',
        f=True
    )

    cmds.connectAttr(
        disbs[2] + '.distance',
        dis_md + '.input2Z',
        f=True
    )

    #
    cmds.connectAttr(
        dis_md + '.output',
        dis_w_md + '.input1',
        f=True
    )

    # md
    cmds.connectAttr(
        dis_w_md + '.outputX',
        weight_param_md + '.input1Y',
        f=True
    )

    cmds.connectAttr(
        dis_w_md + '.outputX',
        weight_param_md + '.input1Z',
        f=True
    )

    cmds.connectAttr(
        dis_w_md + '.outputY',
        weight_param_md + '.input2Y',
        f=True
    )

    cmds.connectAttr(
        dis_w_md + '.outputZ',
        weight_param_md + '.input2Z',
        f=True
    )

    return weight_param_md


def create_angle_dim(start=None, middle=None, end=None):
    angle_dim = cmds.createNode('angleDimension', ss=True)
    dim_p = cmds.listRelatives(angle_dim, p=True)[0]
    cmds.parent(dim_p, start)
    for i, obj in enumerate([start, middle, end]):
        dcmx = cmds.createNode('decomposeMatrix', ss=True)
        cmds.connectAttr(
            '{}.worldMatrix[0]'.format(obj),
            '{}.inputMatrix'.format(dcmx),
            f=True
            )

        angle_dim_connect = 'start'
        if i == 0:
            pass
        elif i == 1:
            angle_dim_connect = 'middle'
        elif i == 2:
            angle_dim_connect = 'end'

        cmds.connectAttr(
            '{}.outputTranslate'.format(dcmx),
            '{}.{}Point'.format(angle_dim, angle_dim_connect),
            f=True
            )


    return angle_dim


def create_angle_dim_to_weight(joints=None):
    angle_dim = create_angle_dim(*joints)

    angle_pma = cmds.createNode('plusMinusAverage', ss=True)
    angle_md = cmds.createNode('multiplyDivide', ss=True)
    weight_md = cmds.createNode('multiplyDivide', ss=True)

    # pma
    cmds.setAttr(
        angle_pma + '.operation',
        2
    )

    cmds.setAttr(
        angle_pma + '.input1D[0]',
        180
    )

    cmds.connectAttr(
        angle_dim + '.angle',
        angle_pma + '.input1D[1]',
        f=True
    )

    # md
    cmds.setAttr(
        angle_md + '.operation',
        2
    )

    cmds.setAttr(
        angle_md + '.input2X',
        180
    )

    cmds.connectAttr(
        angle_pma + '.output1D',
        angle_md + '.input1X',
        f=True
    )

    cmds.connectAttr(
        angle_md + '.outputX',
        weight_md + '.input1X',
        f=True
    )

    return weight_md


def create_pv_locators(joints=None, aim=None, up=None,
                       set_prim=None, set_scnd=None, ik_pv_ctrl=None):

    aim_settings = {
        'w':True,
        'offset':[0,0,0],
        'aimVector':set_prim,
        'upVector':set_scnd,
        'worldUpType':'object',
        'worldUpObject':up
    }

    angle_md = create_angle_dim_to_weight(joints=joints)
    dis_w_md = create_distance_weight(nodes=joints)

    dis_w_pb = cmds.createNode('pairBlend', ss=True)
    aim_dis_loc = joints[1] + '_p_match_loc'
    loc = cmds.spaceLocator()[0]
    cmds.rename(loc, aim_dis_loc)
    cmds.parent(aim_dis_loc, joints[0])

    end_dis_loc = joints[2] + '_end_match_loc'
    loc = cmds.spaceLocator()[0]
    cmds.rename(loc, end_dis_loc)
    cmds.pointConstraint(joints[2], end_dis_loc)
    cmds.parent(end_dis_loc, joints[0])
    cmds.connectAttr(
        end_dis_loc + '.t',
        dis_w_pb + '.inTranslate2',
        f=True
    )
    cmds.connectAttr(
        dis_w_md + '.outputY',
        dis_w_pb + '.weight',
        f=True
    )
    cmds.connectAttr(
        dis_w_pb + '.outTranslate',
        aim_dis_loc + '.t',
        f=True
    )

    aim_cnst = cmds.aimConstraint(aim, aim_dis_loc, **aim_settings)

    cnd = cmds.createNode('condition', ss=True)
    cmds.setAttr(
        cnd + '.operation',
        2
    )
    cmds.setAttr(
        cnd + '.colorIfTrueR',
        1
    )
    cmds.setAttr(
        cnd + '.colorIfFalseR',
        0
    )

    cmds.connectAttr(
        angle_md + '.outputX',
        cnd + '.firstTerm',
        f=True
    )

    aim_const_pb = cmds.createNode('pairBlend', ss=True)

    cmds.connectAttr(
        aim_cnst[0] + '.constraintRotate',
        aim_const_pb + '.inRotate2',
        f=True
    )

    cmds.disconnectAttr(
        aim_cnst[0] + '.constraintRotateX',
        aim_dis_loc + '.rx'
    )
    cmds.disconnectAttr(
        aim_cnst[0] + '.constraintRotateY',
        aim_dis_loc + '.ry'
    )
    cmds.disconnectAttr(
        aim_cnst[0] + '.constraintRotateZ',
        aim_dis_loc + '.rz'
    )

    cmds.connectAttr(
        aim_const_pb + '.outRotate',
        aim_dis_loc + '.r',
        f=True
    )

    cmds.connectAttr(
        cnd + '.outColorR',
        aim_const_pb + '.weight',
        f=True
    )

    new_name = joints[1] + '_match_loc'
    pv_loc = cmds.spaceLocator()[0]
    cmds.rename(pv_loc, new_name)
    cmds.matchTransform(new_name, joints[1], pos=True, rot=False, scl=False)
    cmds.xform(new_name, **ik_pv_ctrl)
    cmds.parent(new_name, aim_dis_loc)

    return new_name


class MatchConstraint():
    def __init__(self, namespace=None):
        self.parent_const_ops = {
            'mo':True,
            'w':True
        }

        self.point_const_ops = {
            'mo':False,
            'w':True
        }

        self.orient_const_ops = {
            'mo':True,
            'w':True
        }


        self.orient_setAttr_ops = {
            'interpType':2
        }

        self.namespace = namespace

        self.root_ctrl = self.namespace + 'Root_ctrl'
        self.hip_ctrl = self.namespace + 'Cog_ctrl'
        self.spine01_ctrl = self.namespace + 'Spine1_ctrl'
        self.spine02_ctrl = self.namespace + 'Spine2_ctrl'
        self.spine03_ctrl = self.namespace + 'Spine3_ctrl'
        self.neck_ctrl = self.namespace + 'Neck_ctrl'
        self.head_ctrl = self.namespace + 'Head_ctrl'

        self.shoulder_L_ctrl = self.namespace + 'Shoulder_L_ctrl'
        self.arm_L_ctrl = self.namespace + 'Arm_L_ctrl'
        self.elbow_L_ctrl = self.namespace + 'Elbow_L_ctrl'
        self.wrist_L_ctrl = self.namespace + 'Wrist_L_ctrl'

        self.thumb01_L_ctrl = self.namespace + 'Thumb_01_L_ctrl'
        self.thumb02_L_ctrl = self.namespace + 'Thumb_02_L_ctrl'
        self.thumb03_L_ctrl = self.namespace + 'Thumb_03_L_ctrl'
        self.index01_L_ctrl = self.namespace + 'Index_01_L_ctrl'
        self.index02_L_ctrl = self.namespace + 'Index_02_L_ctrl'
        self.index03_L_ctrl = self.namespace + 'Index_03_L_ctrl'
        self.middle01_L_ctrl = self.namespace + 'Middle_01_L_ctrl'
        self.middle02_L_ctrl = self.namespace + 'Middle_02_L_ctrl'
        self.middle03_L_ctrl = self.namespace + 'Middle_03_L_ctrl'
        self.ring01_L_ctrl = self.namespace + 'Ring_01_L_ctrl'
        self.ring02_L_ctrl = self.namespace + 'Ring_02_L_ctrl'
        self.ring03_L_ctrl = self.namespace + 'Ring_03_L_ctrl'
        self.pinky01_L_ctrl = self.namespace + 'Pinky_01_L_ctrl'
        self.pinky02_L_ctrl = self.namespace + 'Pinky_02_L_ctrl'
        self.pinky03_L_ctrl = self.namespace + 'Pinky_03_L_ctrl'

        self.thigh_L_ctrl = self.namespace + 'Thigh_L_ctrl'
        self.knee_L_ctrl = self.namespace + 'Knee_L_ctrl'
        self.ankle_L_ctrl = self.namespace + 'Ankle_L_ctrl'
        self.toe_L_ctrl = self.namespace + 'Toe_L_ctrl'

        self.ik_wrist_L_switch = self.namespace + 'ikfk_Wrist_L_ctrl'
        self.ik_wrist_L_ctrl = self.namespace + 'ik_Wrist_L_ctrl'
        self.ik_wrist_rot_L_ctrl = self.namespace + 'ik_rot_Wrist_L_ctrl'
        self.ik_elbow_L_ctrl = self.namespace + 'ik_Elbow_L_ctrl'
        self.ik_wrist_L_match_loc = 'Wrist_L_match_loc'
        self.ik_elbow_L_match_loc = 'Elbow_L_match_loc'

        self.ik_ankle_L_switch = self.namespace + 'ikfk_Ankle_L_ctrl'
        self.ik_ankle_L_ctrl = self.namespace + 'ik_Ankle_L_ctrl'
        self.ik_toe_L_ctrl = self.namespace + 'ik_Toe_L_ctrl'
        self.ik_knee_L_ctrl = self.namespace + 'ik_Knee_L_ctrl'
        self.ik_ankle_L_match_loc = 'Ankle_L_match_loc'
        self.ik_knee_L_match_loc = 'Knee_L_match_loc'

        self.weapon01_L_ctrl = self.namespace + 'Handattach_L_ctrl'

        self.const_settings = {
            'Root':{
                'targets':['{}'.format(self.root_ctrl)],
                'const_type':'parent',
                'const_ops':self.parent_const_ops
            },
            'Hip':{
                'targets':['{}'.format(self.hip_ctrl)],
                'const_type':'parent',
                'const_ops':self.parent_const_ops
            },
            'Spine1':{
                'targets':['{}'.format(self.spine01_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },
            'Spine2':{
                'targets':['{}'.format(self.spine02_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },
            'Spine3':{
                'targets':['{}'.format(self.spine03_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },
            'Neck':{
                'targets':['{}'.format(self.neck_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },
            'Head':{
                'targets':['{}'.format(self.head_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },

            # arm
            'Shoulder_L':{
                'targets':['{}'.format(self.shoulder_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },
            '{}'.format(self.ik_wrist_L_match_loc):{
                'targets':['{}'.format(self.ik_wrist_L_ctrl)],
                'const_type':'point',
                'const_ops':self.point_const_ops,
            },
            'Wrist_L':{
                'targets':['{}'.format(self.ik_wrist_rot_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },
            '{}'.format(self.ik_elbow_L_match_loc):{
                'targets':['{}'.format(self.ik_elbow_L_ctrl)],
                'const_type':'point',
                'const_ops':self.point_const_ops,
            },

            # leg
            '{}'.format(self.ik_ankle_L_match_loc):{
                'targets':['{}'.format(self.ik_ankle_L_ctrl)],
                'const_type':'parent',
                'const_ops':self.parent_const_ops,
            },
            '{}'.format(self.ik_knee_L_match_loc):{
                'targets':['{}'.format(self.ik_knee_L_ctrl)],
                'const_type':'point',
                'const_ops':self.point_const_ops,
            },
            'Toe_L':{
                'targets':['{}'.format(self.ik_toe_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },

            # finger
            'Thumb_01_L':{
                'targets':['{}'.format(self.thumb01_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },
            'Thumb_02_L':{
                'targets':['{}'.format(self.thumb02_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },
            'Thumb_03_L':{
                'targets':['{}'.format(self.thumb03_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },

            'Index_01_L':{
                'targets':['{}'.format(self.index01_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },
            'Index_02_L':{
                'targets':['{}'.format(self.index02_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },
            'Index_03_L':{
                'targets':['{}'.format(self.index03_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },

            'Middle_01_L':{
                'targets':['{}'.format(self.middle01_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },
            'Middle_02_L':{
                'targets':['{}'.format(self.middle02_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },
            'Middle_03_L':{
                'targets':['{}'.format(self.middle03_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },

            'Ring_01_L':{
                'targets':['{}'.format(self.ring01_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },
            'Ring_02_L':{
                'targets':['{}'.format(self.ring02_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },
            'Ring_03_L':{
                'targets':['{}'.format(self.ring03_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },

            'Pinky_01_L':{
                'targets':['{}'.format(self.pinky01_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },
            'Pinky_02_L':{
                'targets':['{}'.format(self.pinky02_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },
            'Pinky_03_L':{
                'targets':['{}'.format(self.pinky03_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },

            # weapon
            'Handattach_L':{
                'targets':['{}'.format(self.weapon01_L_ctrl)],
                'const_type':'parent',
                'const_ops':self.parent_const_ops,
            },

        }

        self.mirror_src = [
            'Shoulder_L',
            '{}'.format(self.ik_wrist_L_match_loc),
            'Wrist_L',
            '{}'.format(self.ik_elbow_L_match_loc),
            '{}'.format(self.ik_ankle_L_match_loc),
            '{}'.format(self.ik_knee_L_match_loc),
            'Toe_L',
            'Thumb_01_L',
             'Thumb_02_L',
             'Thumb_03_L',
             'Index_01_L',
             'Index_02_L',
             'Index_03_L',
             'Middle_01_L',
             'Middle_02_L',
             'Middle_03_L',
             'Ring_01_L',
             'Ring_02_L',
             'Ring_03_L',
             'Pinky_01_L',
             'Pinky_02_L',
             'Pinky_03_L',
            'Handattach_L'
        ]

        self.mirrors = ['_L', '_R']

    def mirror_character(self, mirrors=['_L', '_R'], replace_src=None):
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


    def order_joints(self, joints=None):
        parent_jnt = cmds.ls(joints[0], l=1, type='joint')[0].split('|')[1]

        all_hir = cmds.listRelatives(parent_jnt, ad=True, f=True)
        hir_split_counter = {}
        for fp_node in all_hir:
            hir_split_counter[fp_node] = len(fp_node.split('|'))

        hir_split_counter_sorted = sorted(hir_split_counter.items(), key=lambda x:x[1])

        sorted_joint_list = [jnt_count[0] for jnt_count in hir_split_counter_sorted]

        all_ordered_jnts = cmds.ls(sorted_joint_list)
        return [jnt for jnt in all_ordered_jnts if jnt in joints]

    def create_dummy_bind_joints(self):
        ref_top_nodes = cmds.ls(rn=True, assemblies=True, type='joint')

        search_txt_list = [
            '*cloth_test*',
            '*proxy_*',
            '*ik_*'
        ]

        for search_txt in search_txt_list:
            filtered = list(set(fnmatch.filter(ref_top_nodes, search_txt)))
            [ref_top_nodes.remove(filt) for filt in filtered]

        self.ordered_jnts = self.order_joints(joints=ref_top_nodes)

        dup_jnts = cmds.duplicate(self.ordered_jnts[0])
        self.ordered_jnts = self.order_joints(joints=dup_jnts)

        cmds.parent(self.ordered_jnts[0], w=True)

        consts = cmds.listRelatives(self.ordered_jnts[0], type='constraint', ad=True, f=True)
        cmds.delete(consts)

        # aim locs
        create_aim_locs = {
            'Arm_L':{
                'type':'wld',
                'suffix':'_aim_match_loc',
                'offset':{

                    },
                'rev_pointConstraint':{
                    'sources':['Arm_L', 'Wrist_L'],
                    'dest':'offset',
                    'settings':{
                        'mo':False,
                        'w':True
                    },
                    'setAttrs':{

                    }
                }
            },
            'Arm_R':{
                'type':'wld',
                'suffix':'_aim_match_loc',
                'offset':{

                    },
                'rev_pointConstraint':{
                    'sources':['Arm_R', 'Wrist_R'],
                    'dest':'offset',
                    'settings':{
                        'mo':False,
                        'w':True
                    },
                    'setAttrs':{

                    }
                }
            },
            'Thigh_L':{
                'type':'wld',
                'suffix':'_aim_match_loc',
                'offset':{

                    },
                'rev_pointConstraint':{
                    'sources':['Thigh_L', 'Ankle_L'],
                    'dest':'offset',
                    'settings':{
                        'mo':False,
                        'w':True
                    },
                    'setAttrs':{

                    }
                }
            },
            'Thigh_R':{
                'type':'wld',
                'suffix':'_aim_match_loc',
                'offset':{

                    },
                'rev_pointConstraint':{
                    'sources':['Thigh_R', 'Ankle_R'],
                    'dest':'offset',
                    'settings':{
                        'mo':False,
                        'w':True
                    },
                    'setAttrs':{

                    }
                }
            },
        }

        self.create_ikfk_match_locs(create_aim_locs)

        create_match_locs = {
            'Wrist_L':{
                'type':'wld',
                'suffix':'_match_loc'
            },
            'Wrist_R':{
                'type':'wld',
                'suffix':'_match_loc'
            },

            'Ankle_L':{
                'type':'wld',
                'suffix':'_match_loc'
            },
            'Ankle_R':{
                'type':'wld',
                'suffix':'_match_loc'
            },
        }

        self.create_ikfk_match_locs(create_match_locs)

        # hand L
        joints = [
            'Arm_L',
            'Elbow_L',
            'Wrist_L'
        ]

        aim = 'Elbow_L'
        up = 'Wrist_L'
        set_prim = [0,0,-1]
        set_scnd = [1,0,0]

        create_pv_locators(
            joints=joints,
            aim=aim,
            up=up,
            set_prim=set_prim,
            set_scnd=set_scnd,
            ik_pv_ctrl={
                't':[0,0,-50],
                'ws':True,
                'r':True
            }
        )

        # hand R
        joints = [
            'Arm_R',
            'Elbow_R',
            'Wrist_R'
        ]

        aim = 'Elbow_R'
        up = 'Wrist_R'
        set_prim = [0,0,-1]
        set_scnd = [-1,0,0]

        create_pv_locators(
            joints=joints,
            aim=aim,
            up=up,
            set_prim=set_prim,
            set_scnd=set_scnd,
            ik_pv_ctrl={
                't':[0,0,-50],
                'ws':True,
                'r':True
            }
        )

        # foot L
        joints = [
            'Thigh_L',
            'Knee_L',
            'Ankle_L'
        ]

        aim = 'Knee_L'
        up = 'Ankle_L'
        set_prim = [0,0,1]
        set_scnd = [0,-1,0]

        create_pv_locators(
            joints=joints,
            aim=aim,
            up=up,
            set_prim=set_prim,
            set_scnd=set_scnd,
            ik_pv_ctrl={
                't':[0,0,50],
                'ws':True,
                'r':True
            }
        )

        # foot R
        joints = [
            'Thigh_R',
            'Knee_R',
            'Ankle_R'
        ]

        aim = 'Knee_R'
        up = 'Ankle_R'
        set_prim = [0,0,1]
        set_scnd = [0,-1,0]

        create_pv_locators(
            joints=joints,
            aim=aim,
            up=up,
            set_prim=set_prim,
            set_scnd=set_scnd,
            ik_pv_ctrl={
                't':[0,0,50],
                'ws':True,
                'r':True
            }
        )


    def create_ikfk_match_locs(self, create_match_locs=None):
        u"""
        create_ikfk_match_locs(self.create_match_locs)
        """
        for obj, settings in create_match_locs.items():
            loc = cmds.spaceLocator()
            suffix = settings['suffix']
            match_loc = obj+suffix
            cmds.rename(loc[0], match_loc)

            cmds.matchTransform(match_loc, obj, pos=True, rot=False, scl=False)

            cmds.parent(match_loc, obj)


            if 'offset' in settings.keys():
                p_loc = cmds.spaceLocator()
                p_match_loc = obj+'_p'+suffix
                cmds.rename(p_loc[0], p_match_loc)

                cmds.matchTransform(p_match_loc, obj, pos=True, rot=False, scl=False)

                cmds.parent(p_match_loc, obj)
                cmds.parent(match_loc, p_match_loc)

                for attr, val in settings['offset'].items():
                    cmds.setAttr(match_loc+'.'+attr, val)


            if 'orientConstraint' in settings.keys():
                for const, const_set in settings.items():
                    if 'orient' in const:
                        const_srcs = const_set['sources']
                        const_dst = const_set['dest']
                        const_settings = const_set['settings']
                        const_setAttrs = const_set['setAttrs']
                        if const_dst == 'offset':
                            const_dst = p_match_loc
                        for const_src in const_srcs:
                            ori_const = cmds.orientConstraint(const_src, const_dst, **const_settings)
                            for set_const_at, set_const_at_val in const_setAttrs.items():
                                cmds.setAttr(ori_const[0]+'.'+set_const_at, set_const_at_val)

            elif 'rev_pointConstraint' in settings.keys():
                for const, const_set in settings.items():
                    if 'point' in const:
                        const_srcs = const_set['sources']
                        const_dst = const_set['dest']
                        const_settings = const_set['settings']
                        const_setAttrs = const_set['setAttrs']
                        if const_dst == 'offset':
                            const_dst = p_match_loc
                        for const_src in const_srcs:
                            rev_po_const = cmds.pointConstraint(const_src, const_dst, **const_settings)
                            for set_const_at, set_const_at_val in const_setAttrs.items():
                                cmds.setAttr(rev_po_const[0]+'.'+set_const_at, set_const_at_val)

            elif 'rev_aimConstraint' in settings.keys():
                for const, const_set in settings.items():
                    if 'aim' in const:
                        const_srcs = const_set['sources']
                        const_dst = const_set['dest']
                        const_settings = const_set['settings']
                        const_setAttrs = const_set['setAttrs']
                        if const_dst == 'offset':
                            const_dst = p_match_loc
                        for const_src in const_srcs:
                            rev_po_const = cmds.aimConstraint(const_src, const_dst, **const_settings)
                            for set_const_at, set_const_at_val in const_setAttrs.items():
                                cmds.setAttr(rev_po_const[0]+'.'+set_const_at, set_const_at_val)

    def match_bind_joints_to_ctrls(self):

        self.create_dummy_bind_joints()

        mirror_const_settings = {}
        for src, const_set in self.const_settings.items():
            if src in self.mirror_src:
                mirror_obj = self.mirror_character(mirrors=self.mirrors, replace_src=src)
                targets = const_set['targets']
                mirror_targets = []
                for tgt in targets:
                    mirror_tgt = self.mirror_character(mirrors=self.mirrors, replace_src=tgt)
                    mirror_targets.append(mirror_tgt)

                mirror_const_settings[mirror_obj] = {}
                mirror_const_settings[mirror_obj]['targets'] = mirror_targets
                for mir_key, mir_val in const_set.items():
                    if not mir_key == 'targets':
                        mirror_const_settings[mirror_obj][mir_key] = mir_val

        for mir_set_key, mir_set_val in mirror_const_settings.items():
            self.const_settings[mir_set_key] = mir_set_val

        bake_cnst_sets = 'bake_cnst_sets'
        if not cmds.objExists(bake_cnst_sets):
            cmds.sets(n=bake_cnst_sets, em=True)

        cmds.sets(self.ordered_jnts[0], add=bake_cnst_sets)

        for src, const_set in self.const_settings.items():
            targets = const_set['targets']
            if 'const_type' in const_set.keys():
                const_ops = const_set['const_ops']
                setAttr_ops = None
                if 'setAttr_ops' in const_set.keys():
                    setAttr_ops = const_set['setAttr_ops']

                if 'point' == const_set['const_type']:
                    for target in targets:
                        print('src:', src, 'dst:', target)
                        const = cmds.pointConstraint(src, target, **const_ops)

                elif 'orient' == const_set['const_type']:
                    for target in targets:
                        print('src:', src, 'dst:', target)
                        const = cmds.orientConstraint(src, target, **const_ops)

                elif 'parent' == const_set['const_type']:
                    for target in targets:
                        print('src:', src, 'dst:', target)
                        const = cmds.parentConstraint(src, target, **const_ops)

                cmds.sets(const, add=bake_cnst_sets)

                if setAttr_ops:
                    for const_at, const_val in setAttr_ops.items():
                        cmds.setAttr(const[0] + '.' + const_at, const_val)

        cmds.joint(self.ordered_jnts[0], e=True, apa=True, ch=True)

    def hand_fk_const(self, side=None):
        hand_fk_const = {
            'L':[
                {
                    'src':'Arm_L',
                    'target':self.arm_L_ctrl,
                    'const_ops':{
                        'w':True,
                        'mo':True
                    },
                    'set_attr':{
                        'interpType':2
                    }
                },
                {
                    'src':'Elbow_L',
                    'target':self.elbow_L_ctrl,
                    'const_ops':{
                        'w':True,
                        'mo':True,
                        'skip':['x', 'z']
                    },
                    'set_attr':{
                        'interpType':2
                    }
                },
                {
                    'src':'Wrist_L',
                    'target':self.wrist_L_ctrl,
                    'const_ops':{
                        'w':True,
                        'mo':True
                    },
                    'set_attr':{
                        'interpType':2
                    }
                },
            ],
            'R':[
                {
                    'src':'Arm_R',
                    'target':self.mirror_character(self.mirrors, self.arm_L_ctrl),
                    'const_ops':{
                        'w':True,
                        'mo':True
                    },
                    'set_attr':{
                        'interpType':2
                    }
                },
                {
                    'src':'Elbow_R',
                    'target':self.mirror_character(self.mirrors, self.elbow_L_ctrl),
                    'const_ops':{
                        'w':True,
                        'mo':True,
                        'skip':['x', 'z']
                    },
                    'set_attr':{
                        'interpType':2
                    }
                },
                {
                    'src':'Wrist_R',
                    'target':self.mirror_character(self.mirrors, self.wrist_L_ctrl),
                    'const_ops':{
                        'w':True,
                        'mo':True
                    },
                    'set_attr':{
                        'interpType':2
                    }
                },
            ]
        }

        if side in hand_fk_const.keys():
            fk_items = hand_fk_const[side]
            for item in fk_items:
                src = item['src']
                target = item['target']
                const_ops = item['const_ops']
                const = cmds.orientConstraint(src, target, **const_ops)
                if 'set_attr' in item.keys():
                    for at, val in item['set_attr'].items():
                        cmds.setAttr(const[0] + '.' + at, val)

            cmds.sets(const, add='bake_cnst_sets')

    def foot_fk_const(self, side=None):
        foot_fk_const = {
            'L':[
                {
                    'src':'Thigh_L',
                    'target':self.thigh_L_ctrl,
                    'const_ops':{
                        'w':True,
                        'mo':True
                    },
                    'set_attr':{
                        'interpType':2
                    }
                },
                {
                    'src':'Knee_L',
                    'target':self.knee_L_ctrl,
                    'const_ops':{
                        'w':True,
                        'mo':True,
                        'skip':['x', 'z']
                    },
                    'set_attr':{
                        'interpType':2
                    }
                },
                {
                    'src':'Ankle_L',
                    'target':self.ankle_L_ctrl,
                    'const_ops':{
                        'w':True,
                        'mo':True
                    },
                    'set_attr':{
                        'interpType':2
                    }
                },
                {
                    'src':'Toe_L',
                    'target':self.toe_L_ctrl,
                    'const_ops':{
                        'w':True,
                        'mo':True
                    },
                    'set_attr':{
                        'interpType':2
                    }
                },
            ],
            'R':[
                {
                    'src':'Thigh_R',
                    'target':self.mirror_character(self.mirrors, self.thigh_L_ctrl),
                    'const_ops':{
                        'w':True,
                        'mo':True
                    },
                    'set_attr':{
                        'interpType':2
                    }
                },
                {
                    'src':'Knee_R',
                    'target':self.mirror_character(self.mirrors, self.knee_L_ctrl),
                    'const_ops':{
                        'w':True,
                        'mo':True,
                        'skip':['x', 'z']
                    },
                    'set_attr':{
                        'interpType':2
                    }
                },
                {
                    'src':'Ankle_R',
                    'target':self.mirror_character(self.mirrors, self.ankle_L_ctrl),
                    'const_ops':{
                        'w':True,
                        'mo':True
                    },
                    'set_attr':{
                        'interpType':2
                    }
                },
                {
                    'src':'Toe_R',
                    'target':self.mirror_character(self.mirrors, self.toe_L_ctrl),
                    'const_ops':{
                        'w':True,
                        'mo':True
                    },
                    'set_attr':{
                        'interpType':2
                    }
                },
            ]
        }

        if side in foot_fk_const.keys():
            fk_items = foot_fk_const[side]
            for item in fk_items:
                src = item['src']
                target = item['target']
                const_ops = item['const_ops']
                const = cmds.orientConstraint(src, target, **const_ops)
                if 'set_attr' in item.keys():
                    for at, val in item['set_attr'].items():
                        cmds.setAttr(const[0] + '.' + at, val)

            cmds.sets(const, add='bake_cnst_sets')


    def fk_base_constraint(self, fk_parts=None):
        if ('foot_L' in fk_parts
            or 'foot_R' in fk_parts
            or 'hand_L' in fk_parts
            or 'hand_R' in fk_parts):

                if 'foot_L' in fk_parts:
                    cmds.setAttr(self.ik_ankle_L_switch + '.ikfk', 0)
                    self.foot_fk_const(side='L')

                if 'foot_R' in fk_parts:
                    cmds.setAttr(self.mirror_character(self.mirrors,
                                 self.ik_ankle_L_switch) + '.ikfk', 0)
                    self.foot_fk_const(side='R')

                if 'hand_L' in fk_parts:
                    cmds.setAttr(self.ik_wrist_L_switch + '.ikfk', 0)
                    self.hand_fk_const(side='L')

                if 'hand_R' in fk_parts:
                    cmds.setAttr(self.mirror_character(self.mirrors,
                                 self.ik_wrist_L_switch) + '.ikfk', 0)
                    self.hand_fk_const(side='R')

# if __name__ == '__main__':
#     match_const = MatchConstraint()
#     match_const.match_bind_joints_to_ctrls()

def root_position_under_cog(namespace=None):
    """
    cog_ctrl = 'Cog_ctrl'
    root_ctrl = 'Root_ctrl'
    root_position_under_cog(cog_ctrl, root_ctrl)
    """
    if not namespace:
        namespace = get_mgpickernamespace()

    cog_ctrl = namespace + 'Cog_ctrl'
    root_ctrl = namespace + 'Root_ctrl'

    root_match_constraints_sets = 'root_match_constraints_sets'
    if not cmds.objExists(root_match_constraints_sets):
        cmds.sets(n=root_match_constraints_sets, em=True)


    cog_loc = cmds.spaceLocator()
    ground_loc = cmds.spaceLocator()

    cmds.sets([cog_loc[0], ground_loc[0]], add=root_match_constraints_sets)

    cog_wt = cmds.xform(cog_ctrl, q=True, t=True, ws=True)
    cmds.xform(root_ctrl, t=[cog_wt[0], 0, cog_wt[2]], ws=True)

    cmds.matchTransform(cog_loc, cog_ctrl)
    cmds.pointConstraint(cog_loc, ground_loc, w=True, skip=['y'])

    cmds.xform(cog_loc, t=[0,0,50], r=True, os=True)

    cmds.parentConstraint(cog_ctrl, cog_loc, w=True, mo=True)

    aim_const = cmds.aimConstraint(ground_loc,
                       root_ctrl,
                       w=True,
                       offset=[0,0,0],
                       aimVector=[0,0,1],
                       upVector=[0,1,0],
                       worldUpType='object',
                       worldUpObject=cog_ctrl,
                       skip=['x', 'z'])

    po_const = cmds.pointConstraint(cog_ctrl, root_ctrl, w=True, mo=True, skip=['y'])

    cmds.sets([aim_const[0], po_const[0]], add=root_match_constraints_sets)


class AutoOverlap(object):
    def __init__(self):
        self.MAIN_WINDOW = 'attachOverlap'

    def ui(self):
        if cmds.workspaceControl(self.MAIN_WINDOW, q=True, ex=True):
            cmds.deleteUI(self.MAIN_WINDOW)

        win = cmds.workspaceControl(self.MAIN_WINDOW, l=self.MAIN_WINDOW)

        self.layout()

        cmds.showWindow(win)
        cmds.scriptJob(e=['SelectionChanged', self.select_nucleus_object], p=win, rp=True)

    def layout(self):
        cmds.columnLayout(adj=True, rs=3)
        self.cten_cb = cmds.checkBox(l='Connect to exist nucleus')
        cmds.rowLayout(nc=2, adj=True)
        self.ncls_tfbg = cmds.textFieldButtonGrp(l='Base Ctrl:', tx='', cw3=[50, 150, 50], ad3=2, bl='Set', bc=self.set_base_ctrl)
        cmds.button(l='Clear', c='cmds.textFieldButtonGrp("{0}", e=True, tx="")'.format(self.ncls_tfbg))
        cmds.setParent('..')

        self.ncls_tfg = cmds.textFieldGrp(l='Nucleus:', tx='', cw2=[50, 150], ad2=2)
        cmds.button(l='Create Dynamics', c=self.create_dynamics)
        cmds.button(l='Create RigidBody', c=self.do_create_rigidBody)
        self.ctrl_size_fsg = cmds.floatSliderGrp(l='Controll Size', f=True, v=1, cw3=[70, 30, 60])
        cmds.rowLayout(nc=4)
        cmds.text(l='InteractivePlayback:')
        cmds.iconTextButton(l='InteractivePlayback', c="mel.eval('InteractivePlayback;')", i='interactivePlayback.png')

    def set_base_ctrl(self, *args, **kwargs):
        sel = cmds.ls(os=True)
        if 1 < len(sel):
            cmds.textFieldButtonGrp(self.ncls_tfbg, e=True, tx='{0}'.format(','.join(sel)))
        else:
            cmds.textFieldButtonGrp(self.ncls_tfbg, e=True, tx='{0}'.format(''.join(sel[0])))

    def select_nucleus_object(self, *args, **kwargs):
        u"""
        ui()のscriptJobのSelectionChangedのイベント
        """
        sel = cmds.ls(os=True, type='nucleus')
        if sel:
            cmds.textFieldGrp(self.ncls_tfg, e=True, tx='{0}'.format(sel[0]))

    def createCurveFromJoints(self, jointChain):
        u"""ジョイントに合わせてカーブが作成されます

        params
        ----------------
        jointChain: list
            ['joint1', 'joint2', 'joint3' ...]
        ----------------

        return
        ----------------
        driverCurve: string
        ----------------

        """
        jointPositions = []

        for joints in jointChain:
            if cmds.objectType( joints, isType='joint' ):
                pos = cmds.xform(joints, q=True, ws=True, t=True)
                jointPositions.append(tuple(pos))
            else:
                raise RuntimeError("Method 'createCurveFromJoints()' expects a joint chain.")

        crv = cmds.curve(ep=jointPositions)
        driverCurve = '{0}_aol_driver_crv'.format(jointChain[0])
        cmds.rename(crv, driverCurve)
        return driverCurve

    def makeCurveDynamic(self, driverCurve, nucleus):
        u"""カーブにnHairを割り当てます

        params
        ----------------
        driverCurve: string
            'driverCurve'
        nucleus: string
            'nucleus1'
        ----------------

        return
        ----------------
        createAutoOverlapChain()に必要な値を返します
        return outputCurve, hairSystem, nucleus, follicle, rebuildCurve1, rebuiltCurveOutput
        ----------------

        """

        driverCurveShape = cmds.listRelatives(driverCurve, shapes=True)[0]

        if cmds.objectType( driverCurveShape, isType='nurbsCurve' ):
            outputCurve = '{0}_{1}'.format(driverCurve, 'output')
            baseCurve = cmds.createNode('nurbsCurve')
            cmds.rename(cmds.listRelatives(baseCurve, p=True)[0], outputCurve)
            hairSystem = cmds.createNode( 'hairSystem', n='{0}_{1}'.format(driverCurve, 'hairSystemShape') )
            follicle = cmds.createNode( 'follicle', n='{0}_{1}'.format(driverCurve, 'follicleShape') )
            cmds.setAttr('{0}.restPose'.format(follicle), 1)
            cmds.setAttr('{0}.active'.format(hairSystem), 1)

            # Connect nodes to set up simulation

            # Rebuild driverCurve
            rebuildCurve1 = cmds.createNode('rebuildCurve', n='rebuildCurve1')
            rebuiltCurveOutput = cmds.createNode( 'nurbsCurve', n=( driverCurve + 'rebuiltCurveShape1') )


            # Generate curve output
            cmds.connectAttr((driverCurveShape + '.worldSpace[0]'), (rebuildCurve1 + '.inputCurve'))
            cmds.connectAttr((rebuildCurve1 + '.outputCurve'), (rebuiltCurveOutput + '.create'))

            # Connect curves to follicle
            cmds.connectAttr((driverCurve + '.worldMatrix[0]'), (follicle + '.startPositionMatrix'))
            cmds.connectAttr((rebuiltCurveOutput + '.local'), (follicle + '.startPosition'))

            # Connect follicle to output curve
            cmds.connectAttr((follicle + '.outCurve'), (outputCurve + '.create'))

            # Connect time to hair system and nucleus
            if not nucleus:
                nucleus = cmds.createNode( 'nucleus', n='{0}_{1}'.format(driverCurve, 'nucleus'))
                cmds.connectAttr('time1.outTime', (nucleus + '.currentTime'))
            cmds.connectAttr('time1.outTime', (hairSystem + '.currentTime'))

            # Connect hair system and nucleus together
            nucleus_connections_ia = cmds.listConnections('{0}.inputActive'.format(nucleus))
            nucleus_connections_ias = cmds.listConnections('{0}.inputActiveStart'.format(nucleus))
            if nucleus_connections_ia == None:
                con = 0
            else:
                con = len(nucleus_connections_ia)
            cmds.connectAttr((hairSystem + '.currentState'), (nucleus + '.inputActive[{0}]'.format(str(con))))
            cmds.connectAttr((hairSystem + '.startState'), (nucleus + '.inputActiveStart[{0}]'.format(str(con))))
            cmds.connectAttr((nucleus + '.outputObjects[0]'), (hairSystem + '.nextState'))
            cmds.connectAttr((nucleus + '.startFrame'), (hairSystem + '.startFrame'))

            # Connect hair system to follicle
            cmds.connectAttr((hairSystem + '.outputHair[0]'), (follicle + '.currentPosition'))
            cmds.connectAttr((follicle + '.outHair'), (hairSystem + '.inputHair[0]'))

            # rename outputCurve
            # Return all created objects from simulation.
            # return [outputCurve, hairSystem, nucleus, follicle, rebuildCurve1, rebuiltCurveOutput]
            return outputCurve, hairSystem, nucleus, follicle, rebuildCurve1, rebuiltCurveOutput

        else:
            raise RuntimeError("Method 'makeCurveDynamic()' expects a curve.")

    def createControlCurve(self, jointChain):
        u"""シミュレーション用のコントローラを作成します

        params
        ----------------
        jointChain: list
        ----------------
        """
        if cmds.objectType( jointChain[0], isType='joint' ):
            baseCtrlName = '{0}_aol_ctrl'.format(jointChain[0])

            # Create control curve
            baseControl = cmds.curve(d=1,n='BASE_CTL',p=[(0,0,0),(0.75,0,0),(1,0.25,0),(1.25,0,0),(1,-0.25,0),(0.75,0,0),(1,0,0.25),(1.25,0,0),(1,0,-0.25),(1,0.25,0),(1,0,0.25),(1,-0.25,0),(1,0,-0.25),(0.75,0,0),(0,0,0),(-0.75,0,0),(-1,0.25,0),(-1.25,0,0),(-1,-0.25,0),(-0.75,0,0),(-1,0,0.25),(-1.25,0,0),(-1,0,-0.25),(-1,0.25,0),(-1,0,0.25),(-1,-0.25,0),(-1,0,-0.25),(-0.75,0,0),(0,0,0),(0,0.75,0),(0,1,-0.25),(0,1.25,0),(0,1,0.25),(0,0.75,0),(-0.25,1,0),(0,1.25,0),(0.25,1,0),(0,1,0.25),(-0.25,1,0),(0,1,-0.25),(0.25,1,0),(0,0.75,0),(0,0,0),(0,-0.75,0),(0,-1,-0.25),(0,-1.25,0),(0,-1,0.25),(0,-0.75,0),(-0.25,-1,0),(0,-1.25,0),(0.25,-1,0),(0,-1,-0.25),(-0.25,-1,0),(0,-1,0.25),(0.25,-1,0),(0,-0.75,0),(0,0,0),(0,0,-0.75),(0,0.25,-1),(0,0,-1.25),(0,-0.25,-1),(0,0,-0.75),(-0.25,0,-1),(0,0,-1.25),(0.25,0,-1),(0,0.25,-1),(-0.25,0,-1),(0,-0.25,-1),(0.25,0,-1),(0,0,-0.75),(0,0,0),(0,0,0.75),(0,0.25,1),(0,0,1.25),(0,-0.25,1),(0,0,0.75),(-0.25,0,1),(0,0,1.25),(0.25,0,1),(0,0.25,1),(-0.25,0,1),(0,-0.25,1),(0.25,0,1),(0,0,0.75)],k=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83])
            # baseControl = cmds.circle( n=baseCtrlName, nr=(1, 0, 0) )
            cmds.rename(baseControl, baseCtrlName)
            cmds.rename(cmds.listRelatives(baseCtrlName, s=True)[0], '{0}Shape'.format(baseCtrlName))

            # Set attributes on control curve
            # dynamicOptions
            cmds.addAttr(baseCtrlName, ln='dynamicJoints', keyable=True, at='enum', en='____________')
            cmds.setAttr('{0}.dynamicJoints'.format(baseCtrlName), l=True)
            cmds.addAttr(ln='autoOverlap', sn='autoOverlap', at='bool', k=True, h=False)
            cmds.addAttr(ln='stopFollicle', sn='stopFollicle', at='float', k=True)
            cmds.setAttr('{0}.stopFollicle'.format(baseCtrlName), l=True)

            # Snap control curve to base joint and clean up control curve
            ctrlOffset = cmds.createNode('transform', n='{0}_offset'.format(baseCtrlName), ss=True)
            cmds.parent(baseCtrlName, ctrlOffset)
            baseJointConstraint = cmds.parentConstraint(jointChain[0], ctrlOffset, mo=False)
            cmds.delete(baseJointConstraint)
            # cmds.makeIdentity( baseCtrlName, apply=True, t=True, r=True, s=True, n=2 )

            return baseCtrlName, ctrlOffset

        else:
            raise RuntimeError("Method 'createControlCurve()' expects a joint as the first index.")

    def createAutoOverlapExpression(self, baseCtrl, hairSystem, nucleus):
        u"""インタラクティブにシミュレーションさせるエクスプレッションを設定します
        シミュレーション用のコントローラのautoOverlapアトリビュートでON, OFFを切り替えます

        params
        ----------------
        baseCtrl: string
        hairSystem: string
        nucleus: string
        ----------------
        """

        # set nucleusShare
        base = cmds.textFieldButtonGrp(self.ncls_tfbg, q=True, tx=True)
        exp_name = '{0}_autoOverlap_exp'.format(base)
        if base == '':
            base = baseCtrl
            exp_name = '{0}_autoOverlap_exp'.format(base)
        elif base != '':
            exp_name = '{0}_autoOverlap_exp'.format(base)
            cmds.checkBox(self.cten_cb, e=True, v=True)
        if not cmds.objExists(base):
            print('{0} is not exists.'.format(base))
            return

        listAttr = cmds.listAttr(base, ud=True)
        if not 'nucleusShare' in listAttr:
            cmds.addAttr(base, ln='nucleusShare', dt='string', multi=True)

        multi_indices = cmds.getAttr('{0}.nucleusShare'.format(base), mi=True)
        if not multi_indices:
            cmds.setAttr('{0}.nucleusShare[0]'.format(base), baseCtrl, type='string')
        else:
            cmds.setAttr('{0}.nucleusShare[{1}]'.format(base, str(len(multi_indices))), baseCtrl, type='string')

        # Break time connections from hair system and nucleus
        nucCurrTime = '%s.currentTime' % nucleus
        hairCurrTime = '%s.currentTime' % hairSystem
        try:
            cmds.disconnectAttr('time1.outTime', hairCurrTime)
            cmds.disconnectAttr('time1.outTime', nucCurrTime)
        except Exception as e:
            print(e)

        if cmds.objExists(exp_name):
            cmds.delete(exp_name)

        multi_indices = cmds.getAttr('{0}.nucleusShare'.format(base), mi=True)

        # refresh string
        refresh_string_buf = []
        for i in range(len(multi_indices)):
            baseCtrl = cmds.getAttr('{0}.nucleusShare[{1}]'.format(base, str(i)))
            if not base == baseCtrl:
                listAttr = cmds.listAttr(baseCtrl, ud=True)
                if not 'nucleusShareParent' in listAttr:
                    cmds.addAttr(baseCtrl, ln='nucleusShareParent', dt='string')
                cmds.setAttr('{0}.nucleusShareParent'.format(baseCtrl), base, type='string')
            if ':' in baseCtrl:
                set_refresh = baseCtrl.split(':')[-1]
            else:
                set_refresh = baseCtrl
            refresh_string = ('\tfloat $'+set_refresh+'refresh_tx = ' + baseCtrl + '.translateX; \n'
                              '\tfloat $'+set_refresh+'refresh_ty = ' + baseCtrl + '.translateY; \n'
                              '\tfloat $'+set_refresh+'refresh_tz = ' + baseCtrl + '.translateZ; \n'
                              '\tfloat $'+set_refresh+'refresh_rx = ' + baseCtrl + '.rotateX; \n'
                              '\tfloat $'+set_refresh+'refresh_ry = ' + baseCtrl + '.rotateY; \n'
                              '\tfloat $'+set_refresh+'refresh_rz = ' + baseCtrl + '.rotateZ; \n\n')

            refresh_string_buf.append(refresh_string)

        # playbackDynamic
        cmds.addAttr(baseCtrl, ln="playbackDynamic", keyable=True, at='bool')
        cmds.addAttr(baseCtrl, ln="startFrame", keyable=True, at='float', k=True)
        cmds.connectAttr('{0}.startFrame'.format(baseCtrl), '{0}.startFrame'.format(nucleus), f=True)
        cmds.setAttr('{0}.startFrame'.format(baseCtrl), cmds.currentTime(q=True))

        listAttr = cmds.listConnections('{0}.currentTime'.format(nucleus), s=True)
        aoExpression = ('if (' + base + '.autoOverlap == 1 && ' + base + '.playbackDynamic == 0) { \n'
                        '\t' + nucleus + '.currentTime += 1; \n'
                        '' + ''.join(refresh_string_buf) + ''
                        '} else if (' + base + '.autoOverlap == 0 && ' + base + '.playbackDynamic == 0) { \n'
                        '\t' + nucleus + '.currentTime = ' + base + '.stopFollicle; \n'
                        '} else if (' + base + '.autoOverlap == 0 && ' + base + '.playbackDynamic == 1) { \n'
                        '\t' + nucleus + '.currentTime = frame; \n}'
                        )
        # Set up auto overlap expression
        cmds.expression(n =exp_name, string=aoExpression, ae=False)

        # Connect current time of nucleus to current time of hair system
        cmds.connectAttr(nucCurrTime, hairCurrTime)

    def createAutoOverlapChain(self, jointHierarchy, nucleus=None):
        u"""コア関数になります
        jointHierarchy引数に渡されたFKジョイント、またはFKコントローラに対してシミュレーションを設定します

        以下の順に実行されます
        createCurveFromJoints()
        makeCurveDynamic()
        createControlCurve()
        createAutoOverlapExpression()

        params
        ----------------
        jointHierarchy: list
            2つ以上指定しなければエラーが返されます
        nucleus: string
            既存のnucleusに適用させたい場合に設定します
        ----------------
        """

        # Create auto overlap chain from joint hierarchy. If one joint or no joints are selected, stop the script and prompt the user.
        if jointHierarchy and cmds.objectType( jointHierarchy[0], isType='joint' ) and len(jointHierarchy) > 1:
            # ao = AutoOverlap()

            # We can now call our createCurve method to generate our curve.
            driverCurve = self.createCurveFromJoints(jointHierarchy)
            print('createCurveFromJoints:{0}'.format(driverCurve))


            # Make our generated curve dynamic.
            # dynamicCurveObjects = ao.makeCurveDynamic(driverCurve, nucleus)
            outputCurve, hairSystem, nucleus, follicle, rebuildCurve1, rebuiltCurveOutput = self.makeCurveDynamic(driverCurve, nucleus)
            print(outputCurve, hairSystem, nucleus, follicle, rebuildCurve1, rebuiltCurveOutput)
            # print('makeCurveDynamic:{0}'.format(dynamicCurveObjects))

            # Create spline IK handle from a base joint, an end joint, and a curve.
            splineIK = cmds.ikHandle(sj=jointHierarchy[0], ee=jointHierarchy[-1], sol='ikSplineSolver', c=outputCurve, ccv=False, p=2, w=.5, n='{0}_aol_ikHandle'.format(jointHierarchy[0]))

            # Create control curve.
            controlCurve, ctrlOffset = self.createControlCurve(jointHierarchy)
            print('createControlCurve:{0}'.format(controlCurve))


            # Parent constrain control curve to follicle curve.
            cmds.parentConstraint(controlCurve, driverCurve, mo=True)

            # Create auto overlap expression.
            self.createAutoOverlapExpression(controlCurve, hairSystem, nucleus)
            print('createAutoOverlapExpression:{0}, {1}, {2}'.format(controlCurve, hairSystem, nucleus))


            # Group all objects created by makeCurvesDynamic command.
            dynamicCurveObjects = [outputCurve, hairSystem, nucleus, follicle, rebuildCurve1, rebuiltCurveOutput]
            dynamicGrp = cmds.group(dynamicCurveObjects, n='dynamicCurve_' + controlCurve + '_grp' )
            cmds.parent(driverCurve, dynamicGrp)
            cmds.parent(splineIK[0], dynamicGrp)

            """
            CreateCollisions
            """
            # collision = cmds.polySphere(cuv=2, sy=20, sx=20, r=10, ax=(0, 1, 0), n='collision_{0}'.format(jointHierarchy[0]))
            # rigidBody = 'collide_{0}'.format(collision[0])
            # cmds.delete(ch=True)
            # rigidBodies = cmds.ls(type='nRigid')
            # if rigidBodies == []:
                # collide = mel.eval('makeCollideNCloth;')
            # elif len(rigidBodies) > 0:
                # mel.eval('string $nucleus = "{0}";'.format(nucleus))
                # mel.eval('setActiveNucleusNode( $nucleus );')
                # collide = mel.eval('makeCollideNCloth;')
            # cmds.setAttr('{0}.thickness'.format(collide[0]), 1)
            # cmds.rename(cmds.listRelatives(collide[0], p=True)[0], rigidBody)
            # cmds.parent(rigidBody, dynamicGrp)
            # cmds.parent(collision[0], dynamicGrp)
            cmds.parent(ctrlOffset, dynamicGrp)

            # Hide any unused nodes from view port.
            unusedObjects = cmds.listRelatives( dynamicGrp, allDescendents=True )
            for objects in unusedObjects:
                cmds.setAttr((objects + '.visibility'), 0)

            # collision vis
            # cmds.setAttr("{0}.visibility".format(collision[0]), 1)
            # cmds.setAttr("{0}Shape.visibility".format(collision[0]), 1)
            # ctrl vis
            cmds.setAttr("{0}.visibility".format(ctrlOffset), 1)
            cmds.setAttr("{0}.visibility".format(controlCurve), 1)
            cmds.setAttr("{0}Shape.visibility".format(controlCurve), 1)

            """
            Add attributes and connections
            """
            # cmds.setAttr("{0}.active".format(hairSystem), 1)
            cmds.setAttr("{0}.startDirection".format(follicle), 1)

            # ikOptions
            cmds.addAttr(controlCurve, ln='ikOptions', keyable=True, at='enum', en='____________')
            cmds.setAttr('{0}.ikOptions'.format(controlCurve), l=True)
            cmds.addAttr(controlCurve, ln='roll', keyable=True, at='float', dv=0.0)
            cmds.addAttr(controlCurve, ln='twist',  keyable=True, at='float', dv=0.0)
            # dynamicOptions
            cmds.addAttr(controlCurve, ln='dynamicOptions', keyable=True, at='enum', en='____________')
            cmds.setAttr('{0}.dynamicOptions'.format(controlCurve), l=True)
            # Add attributes to controller for the dynamics
            cmds.addAttr(controlCurve, min=0, ln='stiffness', max=1, keyable=True, at='double', dv=0.15)
            cmds.addAttr(controlCurve, min=0, ln='lengthFlex', max=1, keyable=True, at='double', dv=0)
            cmds.addAttr(controlCurve, ln="pointLock", en="No Attach:Base:Tip:BothEnds:", at="enum", k=True)
            cmds.setAttr('{0}.pointLock'.format(controlCurve), 1)
            cmds.addAttr(controlCurve, min=0, ln="drag", max=1, keyable=True, at='double', dv=.05)
            cmds.addAttr(controlCurve, min=0, ln='friction', max=1, keyable=True, at='double', dv=0.5)
            cmds.addAttr(controlCurve, min=0, ln="gravity", max=10, keyable=True, at='double', dv=1)
            cmds.addAttr(controlCurve, min=0, ln="turbulenceStrength", max=1, keyable=True, at='double', dv=0)
            cmds.addAttr(controlCurve, min=0, ln="turbulenceFrequency", max=2, keyable=True, at='double', dv=0.2)
            cmds.addAttr(controlCurve, min=0, ln="turbulenceSpeed", max=2, keyable=True, at='double', dv=0.2)
            cmds.addAttr(controlCurve, min=0, ln="damp", max=10, keyable=True, at='double', dv=0, k=True)
            cmds.addAttr(controlCurve, min=0, ln="mass", max=10, keyable=True, at='double', dv=1.0, k=True)
            cmds.addAttr(controlCurve, min=0, ln="attractionDamp", max=1, keyable=True, at='double', dv=0, k=True)
            cmds.addAttr(controlCurve, min=0, ln="startCurveAttract", max=1, keyable=True, at='double', dv=0, k=True)
            cmds.addAttr(controlCurve, min=0, ln="motionDrag", max=1, keyable=True, at='double', dv=0, k=True)
            # collisions
            cmds.addAttr(controlCurve, ln='collisionOptions', keyable=True, at='enum', en='____________')
            cmds.setAttr('{0}.collisionOptions'.format(controlCurve), l=True)
            cmds.addAttr(controlCurve, ln="useNucleusSolver", keyable=True, at='bool')
            cmds.addAttr(controlCurve, min=0, ln="stickiness", keyable=True, at='double', dv=0.0, k=True)

            cmds.connectAttr(controlCurve + ".roll", splineIK[0] + ".roll", f=True)
            cmds.connectAttr(controlCurve + ".twist", splineIK[0] + ".twist", f=True)
            #Connect attributes on the controller sphere to the follicle node
            cmds.connectAttr(controlCurve + ".pointLock", follicle + ".pointLock", f=True)
            #Connect attribute on the controller sphere to the hair system node
            cmds.connectAttr(controlCurve + ".stiffness", hairSystem + ".stiffness", f=True)
            cmds.connectAttr(controlCurve + ".lengthFlex", hairSystem + ".lengthFlex", f=True)
            cmds.connectAttr(controlCurve + ".damp", hairSystem + ".damp", f=True)
            cmds.connectAttr(controlCurve + ".drag", hairSystem + ".drag", f=True)
            cmds.connectAttr(controlCurve + ".friction", hairSystem + ".friction", f=True)
            cmds.connectAttr(controlCurve + ".mass", hairSystem + ".mass", f=True)
            cmds.connectAttr(controlCurve + ".gravity", hairSystem + ".gravity", f=True)
            cmds.connectAttr(controlCurve + ".turbulenceStrength", hairSystem + ".turbulenceStrength", f=True)
            cmds.connectAttr(controlCurve + ".turbulenceFrequency", hairSystem + ".turbulenceFrequency", f=True)
            cmds.connectAttr(controlCurve + ".turbulenceSpeed", hairSystem + ".turbulenceSpeed", f=True)
            cmds.connectAttr(controlCurve + ".attractionDamp", hairSystem + ".attractionDamp", f=True)
            cmds.connectAttr(controlCurve + ".startCurveAttract", hairSystem + ".startCurveAttract", f=True)
            cmds.connectAttr(controlCurve + ".motionDrag", hairSystem + ".motionDrag", f=True)
            # collisions
            cmds.connectAttr(controlCurve + ".useNucleusSolver", hairSystem + ".active", f=True)
            cmds.connectAttr(controlCurve + ".stickiness", hairSystem + ".stickiness", f=True)

            # scale lock
            cmds.setAttr(controlCurve + '.sx', l=True, cb=False, k=False)
            cmds.setAttr(controlCurve + '.sy', l=True, cb=False, k=False)
            cmds.setAttr(controlCurve + '.sz', l=True, cb=False, k=False)

            # Return group containing all needed objects to make curve dynamic.
            return dynamicGrp, controlCurve
        else:
            cmds.confirmDialog( title='Please select joint.', message='Please make sure to select a joint with at least one child joint.' )
            raise RuntimeError("Selection was not a joint with at least one child joint.")

    def create_dynamics(self, *args, **kwargs):
        u"""UIから実行するための関数になります
        createAutoOverlapChain()を実行します
        """
        sel = cmds.ls(os=True, r=True)
        if not sel or not 1 < len(sel):
            cmds.warning('Please select FK ctrls.')
            return

        bake_sets = '{0}_aol_bake_sets'.format(sel[0])
        if not cmds.objExists(bake_sets):
            cmds.sets(em=True, n=bake_sets)

        aol_joints = []
        for i, obj in enumerate(sel):
            aol_jnt = cmds.createNode('joint', n='{0}_aol_dynamic_jnt'.format(obj), ss=True)
            cmds.matchTransform(aol_jnt, obj)
            cmds.makeIdentity(aol_jnt, n=False, s=False, r=True, t=False, apply=True, pn=True)
            if i == 0:
                pass
            else:
                cmds.parent(aol_jnt, aol_joints[-1])

            aol_joints.append(aol_jnt)
            cmds.sets(obj, add=bake_sets)

        for i, (aol_jnt, obj) in enumerate(zip(aol_joints, sel)):
            cmds.orientConstraint(aol_jnt, obj, w=True, mo=True)

        for j in aol_joints[0]:
            if j == '|':
                cmds.confirmDialog( title='Please rename joint.', message=('Joint "' + aol_joints[0] + '" has | characters dividing the name. Please rename the joint.') )
                raise RuntimeError("Joint cannot have dividers in name.")

        cten_cb = cmds.checkBox(self.cten_cb, q=True, v=True)
        if cten_cb:
            ncls_tfg = cmds.textFieldGrp(self.ncls_tfg, q=True, tx=True)
            if cmds.objExists(ncls_tfg):
                nucleus_name = ncls_tfg
            else:
                nucleus_name = None

        else:
            nucleus_name = None

        dynamicGrp, ctrl = self.createAutoOverlapChain(aol_joints, nucleus=nucleus_name)
        cmds.parent(aol_joints[0], dynamicGrp)

        ctrl_sets = '{0}_aol_ctrl_sets'.format(sel[0])
        if not cmds.objExists(ctrl_sets):
            cmds.sets(em=True, n=ctrl_sets)

        cmds.sets(ctrl, add=ctrl_sets)
        cmds.sets(bake_sets, add=ctrl_sets)

        ctrl_size = cmds.floatSliderGrp(self.ctrl_size_fsg, q=True, v=1)
        cmds.select('{0}.cv[*]'.format(ctrl), r=True)
        cmds.scale(ctrl_size, ctrl_size, ctrl_size)

        cmds.select(ctrl, r=True)

    def create_rigidBody(self, selection=None, nucleus=None):
        u"""nucleusとオブジェクトを選択してリジッドボディを設定します
        """
        if selection and nucleus:
            if 'nucleus' == cmds.objectType(nucleus) and cmds.objExists(nucleus):
                for obj in selection:
                    if cmds.objExists(obj):
                        rigidBody = 'rigidBody_{0}'.format(obj)
                        if not cmds.objExists(rigidBody):
                            cmds.select(obj, r=True)
                            rigidBodies = cmds.ls(type='nRigid')
                            if rigidBodies == []:
                                collide = mel.eval('makeCollideNCloth;')
                            else:
                                sh = cmds.listRelatives(obj, s=True)
                                if sh:
                                    mesh_shape = sh[0]
                                    listConnections = cmds.listConnections('{0}.worldMesh[0]'.format(mesh_shape), d=True)

                                collide = cmds.ls(cmds.listRelatives(listConnections, s=True), type='nRigid')

                                if collide:
                                    cmds.connectAttr('{0}.currentState'.format(collide[0]), '{0}.inputPassive[0]'.format(nucleus), f=True)
                                    cmds.connectAttr('{0}.startState'.format(collide[0]), '{0}.inputPassiveStart[0]'.format(nucleus), f=True)
                                else:
                                    mel.eval('string $nucleus = "{0}";'.format(nucleus))
                                    mel.eval('setActiveNucleusNode( $nucleus );')
                                    collide = mel.eval('makeCollideNCloth;')

                            if collide == []:
                                continue
                            else:
                                cmds.setAttr('{0}.thickness'.format(collide[0]), 1)
                                cmds.rename(cmds.listRelatives(collide[0], p=True)[0], rigidBody)
                        else:
                            cmds.warning('"{0}" is already exists.'.format(rigidBody))
        else:
            cmds.warning('Set "selection" and "nucleus".')

    def do_create_rigidBody(self, *args, **kwargs):
        u"""UIから実行するための関数になります
        create_rigidBody()を実行します
        """
        sel = cmds.ls(os=True)
        nucleus = sel[0]
        selection = sel[1::]

        self.create_rigidBody(selection=selection, nucleus=nucleus)

# if __name__ == '__main__':
#     aol = AutoOverlap()
#     aol.ui()

# -*- coding: utf-8 -*-
u"""モーション反転ツール(GUI)"""

# from .command import ReverseMotionCmd
# from wzdx.maya.anim.bake import Bake

WORLD_OFFSET = 'main_ctrl'

logger = getLogger(__name__)

# ---------------------------------------------------
# decorator
def suspend(func):
    u"""リフレッシュ イベントをsuspend"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = None
        cmds.refresh(su=True)
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            logger.error('{}'.format(e))
            logger.error(traceback.format_exc())
        finally:
            cmds.refresh(su=False)
            return result
    return wrapper


def keep_selections(func):
    u"""選択を保持するdecorator"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        return _keep_selections_wrapper(func, *args, **kwargs)
    return wrapper


def _keep_selections_wrapper(func, *args, **kwargs):
    u"""選択を保持"""
    selection = cmds.ls(sl=True)
    result = func(*args, **kwargs)
    if selection:
        cmds.select(selection, ne=True)
    return result

# ---------------------------------------------------


class Bake(object):

    @classmethod
    def _get_keyable_attrs(cls, node, attrs=None):
        u"""キー設定が可能なアトリビュートの取得

        :param node: ノード
        :return: キー設定
        """
        if attrs:
            key_attrs = cmds.listAnimatable(['{}.{}'.format(node, attr) for attr in attrs])
        else:
            key_attrs = cmds.listAnimatable(node)
        if key_attrs:
            key_attrs = [key_attr.split('.')[-1] for key_attr in key_attrs]
            return key_attrs
        else:
            return []

    @classmethod
    def _is_constraint(cls, node):
        u"""コンストレインかどうか

        :param node:
        :return: bool
        """
        constraint_type = (
            om2.MFn.kAimConstraint,
            om2.MFn.kConstraint,
            om2.MFn.kDynamicConstraint,
            om2.MFn.kGeometryConstraint,
            om2.MFn.kHairConstraint,
            om2.MFn.kNormalConstraint,
            om2.MFn.kOldGeometryConstraint,
            om2.MFn.kOrientConstraint,
            om2.MFn.kParentConstraint,
            om2.MFn.kPluginConstraintNode,
            om2.MFn.kPointConstraint,
            om2.MFn.kPointOnPolyConstraint,
            om2.MFn.kPoleVectorConstraint,
            om2.MFn.kRigidConstraint,
            om2.MFn.kScaleConstraint,
            om2.MFn.kSymmetryConstraint,
            om2.MFn.kTangentConstraint,
        )

        sel = om2.MGlobal.getSelectionListByName(node)
        depend_node = sel.getDependNode(0)
        # logger.debug('{} {}'.format(node, depend_node.apiTypeStr))
        if depend_node.apiType() in constraint_type:
            return True
        else:
            return False

    @classmethod
    def _disconnect_constraint(cls, node):
        u"""コンストレインを切断

        :param node: ノード
        """
        # キー設定前にコンストレインなどの接続があれば切断
        attrs = cls._get_keyable_attrs(node)

        for attr in attrs:
            # Transform => Shape の場合アトリビュートが違う場合
            try:
                connections = cmds.listConnections(
                    '{}.{}'.format(node, attr), s=True, d=False, p=True,
                )
                if not connections:
                    continue

                for connection in connections:
                    connect_node = connection.split('.')[0]
                    if cls._is_constraint(connect_node):
                        cmds.disconnectAttr(connection, '{}.{}'.format(node, attr))
            except Exception as e:
                logger.error('{}'.format(e))

    @classmethod
    def _is_delete_attrs(cls, attr):
        u"""削除して良いアトリビュートか"""
        delete_words = ('blendPoint', 'blendOrient', 'blendParent')
        for word in delete_words:
            if re.search(word, attr):
                return True
        return False

    @classmethod
    def _delete_attrs(cls, node):
        u"""不要なアトリビュートを削除"""
        attrs = cls._get_keyable_attrs(node)
        for attr in attrs:
            if cls._is_delete_attrs(attr):
                cmds.deleteAttr('{}.{}'.format(node, attr))

    @classmethod
    def _rotate_filter(cls, rotate, order):
        u"""rotateの値を変換

        :param rotate: (x, y, z) radians
        :return: (x, y, z) radians
        """
        e = om2.MEulerRotation(*rotate, order=order)
        q = e.asQuaternion()
        qua = om2.MQuaternion(q)
        rad_order = qua.asEulerRotation().reorder(order)

        return rad_order[0], rad_order[1], rad_order[2]

    @classmethod
    def get_values(cls, nodes, start, end, **kwargs):
        u"""値の取得

        :param nodes: ノードのリスト
        :param start: start
        :param end: end
        :return: {node: ({attr: type}, dataFrame), ...}
        """
        time_array = om.MTimeArray()
        [time_array.append(om.MTime(i, om.MTime.uiUnit())) for i in range(start, end + 1)]

        results = {
            'node': {node: {} for node in nodes},
            'time': time_array,
        }
        node_transform = {}

        selection_list = om2.MSelectionList()
        [selection_list.add(node) for node in nodes]
        iter_ = om2.MItSelectionList(selection_list)

        # attributeと型の取得
        while not iter_.isDone():
            dagpath = iter_.getDagPath()
            mobject = dagpath.node()
            dependency_node = om2.MFnDependencyNode(mobject)
            name = dagpath.partialPathName()

            attrs = results['node'][name]
            keyable_attrs = cls._get_keyable_attrs(name, kwargs.setdefault('attrs', None))
            if (
                'rotateX' in keyable_attrs and
                'rotateY' in keyable_attrs and
                'rotateZ' in keyable_attrs
            ):
                node_transform[name] = True
            else:
                node_transform[name] = False

            for i in range(dependency_node.attributeCount()):
                plug = om2.MPlug(mobject, dependency_node.attribute(i))
                attr = plug.info.split('.')[-1]

                if attr in keyable_attrs:
                    attrs[attr] = {
                        'plug': plug,
                        'type': cmds.getAttr('{}.{}'.format(name, attr), typ=True),
                        'values': om.MDoubleArray(),
                    }

            iter_.next()
        iter_.reset()

        # フレームごとの値をdataFrameに格納
        for i in range(start, end + 1, 1):
            oma2.MAnimControl.setCurrentTime(om2.MTime(i, om2.MTime.uiUnit()))
            while not iter_.isDone():
                dagpath = iter_.getDagPath()
                name = dagpath.partialPathName()
                attr_items = results['node'][name]

                if node_transform[name]:
                    mfn_transform = om2.MFnTransform(dagpath)
                    r = mfn_transform.rotation(om2.MSpace.kTransform, False)
                    # MEluerRotationのorderはMTransformationMatrixのorderと値が1違うので引く
                    order = mfn_transform.rotationOrder() - 1
                    r = cls._rotate_filter((r.x, r.y, r.z), order)
                    rotate = {'rotateX': round(r[0], 5), 'rotateY': round(r[1], 5), 'rotateZ': round(r[2], 5)}

                    for attr, items in attr_items.items():
                        values = items['values']
                        if attr in ('rotateX', 'rotateY', 'rotateZ'):
                            values.append(rotate[attr])
                        else:
                            values.append(round(items['plug'].asDouble(), 5))
                else:
                    for attr, items in attr_items.items():
                        values = items['values']
                        values.append(round(items['plug'].asDouble(), 5))

                iter_.next()
            iter_.reset()

        return results

    @classmethod
    def _delete_anim_curves(cls, nodes):
        # アニメーションカーブの削除
        connections = cmds.listConnections(nodes, s=True, d=True)
        if not connections:
            return

        connection_lists = om2.MSelectionList()
        [connection_lists.add(connection) for connection in connections]
        iter_ = om2.MItSelectionList(connection_lists, om2.MFn.kAnimCurve)
        while not iter_.isDone():
            cmds.delete(iter_.getStrings())
            iter_.next()

    @classmethod
    def _get_double_angle_curves(cls, nodes):
        connections = cmds.listConnections(nodes, s=True, d=False)
        if not connections:
            return []
        curves = cmds.ls(connections, typ='animCurveTA')

        return curves

    @classmethod
    def _cleanup_nodes(cls, nodes):
        u"""不要な接続などを除去"""
        for node in nodes:
            # コンストレインの削除
            cls._disconnect_constraint(node)
            cls._delete_attrs(node)

        # 古いアニメーションカーブを削除
        cls._delete_anim_curves(nodes)

    @classmethod
    def _set_keys(cls, nodes, start, end, **kwargs):
        u"""キーフレームの作成

        :param nodes: ノードのリスト
        :param start: start
        :param end: end
        :return: {node: ({attr: type}, dataFrame), ...}
        """
        filter_curves = []
        euler_filter = kwargs.setdefault('euler_filter', False)
        remove_static_channels = kwargs.setdefault('remove_static_channels', False)

        results = cls.get_values(nodes, start, end, attrs=kwargs.setdefault('attrs', None))
        node_items = results['node']
        times = results['time']

        # ベイク前に不要な接続などを除去
        cls._cleanup_nodes(nodes)

        for node, node_items in node_items.items():
            for attr, attr_items in node_items.items():
                # コンストレイン削除時にblend関連のアトリビュートが消えるので事前にチェック
                if not cmds.attributeQuery(attr, node=node, ex=True):
                    continue

                if attr_items['type'] == 'doubleLinear':
                    anim_curve = cmds.createNode('animCurveTL', n='{}_{}'.format(node, attr))
                elif attr_items['type'] == 'doubleAngle':
                    anim_curve = cmds.createNode('animCurveTA', n='{}_{}'.format(node, attr))
                    filter_curves.append(anim_curve)
                else:
                    anim_curve = cmds.createNode('animCurveTU', n='{}_{}'.format(node, attr))

                curve_selection = om.MSelectionList()
                om.MGlobal.getSelectionListByName(anim_curve, curve_selection)
                mobj = om.MObject()
                curve_selection.getDependNode(0, mobj)
                anim_curve_fn = oma.MFnAnimCurve(mobj)
                anim_curve_fn.addKeys(times, attr_items['values'])

                # スタティックチャンネルの除去(先頭１フレームのキーは残す)
                if remove_static_channels:
                    if anim_curve_fn.isStatic():
                        for i in range(anim_curve_fn.numKeys() - 1, 0, -1):
                            anim_curve_fn.remove(i)

                cmds.connectAttr('{}.output'.format(anim_curve), '{}.{}'.format(node, attr), f=True)

        # Euler Filter
        if euler_filter:
            cmds.filterCurve(filter_curves)

    @classmethod
    @suspend
    def main2015(cls, root_nodes, **kwargs):
        u"""BakeしてEuler Filterをかける

        :param root_nodes: ノードのリスト
        :param start: 開始フレーム
        :param end: 終了フレーム
        :param hierarchy: 階層展開オプション ('below' or 'none')
        :param attrs: ベイクするアトリビュート
        """
        start = int(kwargs.setdefault('start', cmds.playbackOptions(q=True, min=True)))
        end = int(kwargs.setdefault('end', cmds.playbackOptions(q=True, max=True)))
        hierarchy = kwargs.setdefault('hierarchy', 'below')
        attrs = kwargs.setdefault('attrs', None)
        euler_filter = kwargs.setdefault('euler_filter', False)

        # logger.debug('Bake Option\nstart: {s} end:{e}\nhierarcy: {h}\nattrs: {a}'.format(
        #     s=start, e=end, h=hierarchy, a=attrs,
        # ))
        nodes = cmds.ls(root_nodes, dag=True) if hierarchy == 'below' else cmds.ls(root_nodes)
        nodes = [node for node in nodes if not cls._is_constraint(node) and cmds.listAnimatable(node)]

        current = cmds.currentTime(q=True)
        cls._set_keys(nodes, start, end, attrs=attrs, euler_filter=euler_filter)
        # 最初のフレームにリセット
        oma2.MAnimControl.setCurrentTime(om2.MTime(current, om2.MTime.uiUnit()))

    @classmethod
    def main2018(cls, root_nodes, **kwargs):
        u"""BakeしてEuler Filterをかける

        :param root_nodes: ノードのリスト
        :param start: 開始フレーム
        :param end: 終了フレーム
        :param hierarchy: 階層展開オプション ('below' or 'none')
        :param attrs: ベイクするアトリビュート
        """
        evaluation = cmds.evaluationManager(q=True, m=True)[0]
        cmds.evaluationManager(m='off')

        cls.main2015(root_nodes, **kwargs)
        cmds.evaluationManager(m=evaluation)

    @classmethod
    def main(cls, root_nodes, **kwargs):

        autokey_stat = cmds.autoKeyframe(q=True, st=True)

        cmds.autoKeyframe(st=False)

        current_time = cmds.currentTime(q=True)
        # cycleCheck Off
        cycle_check = cmds.cycleCheck(q=True, e=True)
        cmds.cycleCheck(e=False)
        cmds.currentTime(current_time, e=True)
        cmds.cycleCheck(e=cycle_check)

        if int(cmds.about(v=True)) < 2018:
            # logger.debug('Bake Mode: Maya2015')
            cls.main2015(root_nodes, **kwargs)
        else:
            # logger.debug('Bake Mode: Maya2018')
            cls.main2018(root_nodes, **kwargs)

        cmds.currentTime(current_time)
        cmds.autoKeyframe(st=autokey_stat)


def _get_selections():
    u"""選択情報を取得する

    リグのセットを選んでいるときはリグのノードに展開する

    :return: 選択ノード
    """
    selections = []
    nodes = cmds.ls(sl=True)
    for node in nodes:
        if cmds.objectType(node) == 'objectSet':
            temp_nodes = cmds.sets(node, q=True)
            if temp_nodes:
                selections.extend(temp_nodes)
        else:
            selections.append(node)

    return selections


@keep_selections
def main():
    u"""Animation > ベイクアニメーション"""

    nodes = _get_selections()
    if not nodes:
        logger.warning('Please Select Node')
        return

    Bake.main(nodes, hierarchy='none', euler_filter=True)


class ReverseMotionCmd(object):

    type_at = (
        'bool',
        'long', 'long2', 'long3',
        'short', 'short2', 'short3',
        'byte', 'char', 'enum',
        'float', 'float2', 'float3',
        'double', 'double2', 'doubleAngle', 'doubleLinear',
        'compound', 'message', 'time',
    )
    type_dt = (
        'string', 'stringArray', 'matrix', 'ftMatrix',
        'doubleArray', 'floatArray', 'Int32Array', 'vectorArray',
    )

    # 一時凌ぎの処理の判定に使うノード
    temp_check_words = (
        'shoulder',
        'hand',
        'thumb',
        'index',
        'middle',
        'ring',
        'pinky',
    )

    temp_check_words = (
        'Shoulder',
        'Wrist',
        'Thumb',
        'Index',
        'Middle',
        'Ring',
        'Pinky',
    )

    # ########################################
    #  Math
    # ########################################
    @staticmethod
    def _conv_degrees(degrees):
        u"""角度を-180度～180度の範囲に変換し直す

        :param degrees: degrees
        :return: degrees
        """
        degrees_ = degrees % 360
        degrees_ = degrees_ - 360 if degrees_ > 180 else degrees_
        return round(degrees_, 1)

    @classmethod
    def _get_rotate_matrix(cls, node):
        u"""回転行列の取得

        :param node: ノード
        :return: 回転行列
        """
        cos = lambda degrees: round(math.cos(math.radians(degrees)), 3)
        sin = lambda degrees: round(math.sin(math.radians(degrees)), 3)

        order = cmds.getAttr('{}.rotateOrder'.format(node))
        x, y, z = cmds.xform(node, q=True, ws=True, ro=True)
        x = cls._conv_degrees(x)
        y = cls._conv_degrees(y)
        z = cls._conv_degrees(z)
        rx = [
            [1, 0, 0],
            [0, cos(x), sin(x)],
            [0, -1 * sin(x), cos(x)],
        ]
        ry = [
            [cos(y), 0, -1 * sin(y)],
            [0, 1, 0],
            [sin(y), 0, cos(y)],
        ]
        rz = [
            [cos(z), sin(z), 0],
            [-1 * sin(z), cos(z), 0],
            [0, 0, 1],
        ]
        if order == 0:
            rmatrix = (rx, ry, rz)
        elif order == 1:
            rmatrix = (ry, rz, rx)
        elif order == 2:
            rmatrix = (rz, rx, ry)
        elif order == 3:
            rmatrix = (rx, rz, ry)
        elif order == 4:
            rmatrix = (ry, rx, rz)
        else:
            rmatrix = (rz, ry, rx)

        return rmatrix

    @staticmethod
    def _vec3_x_matrix3x3(vec3, mat3x3):
        u"""vector3 × matrix3x3 の計算

        :param vec3: vector3
        :param mat3x3: matrix3x3
        :return: vector3
        """
        return (
            vec3[0] * mat3x3[0][0] + vec3[1] * mat3x3[1][0] + vec3[2] * mat3x3[2][0],
            vec3[0] * mat3x3[0][1] + vec3[1] * mat3x3[1][1] + vec3[2] * mat3x3[2][1],
            vec3[0] * mat3x3[0][2] + vec3[1] * mat3x3[1][2] + vec3[2] * mat3x3[2][2],
        )

    # ########################################
    #  Rig
    # ########################################
    @classmethod
    def _is_behavior(cls, node, right_id, left_id, primary_axis='x', secondary_axis='y'):
        u"""behaivorか

        :param node: ノード
        :param right_id: 右の識別子
        :param left_id: 左の識別子
        :param primary_axis: primary axis
        :param secondary_axis: secondary axis
        :return: bool
        """
        mirror_node = cls._get_mirror_node(node, right_id, left_id)
        if not mirror_node or cmds.ls(mirror_node, tr=True):
            return False

        primary_index = cls._get_index_from_axis(primary_axis)
        secondary_index = cls._get_index_from_axis(secondary_axis)

        local_axis = cls._get_local_axis(node, primary_axis, secondary_axis)
        mirror_local_axis = cls._get_local_axis(mirror_node, primary_axis, secondary_axis)

        primary_v = local_axis['primary_vector']
        secondary_v = local_axis['secondary_vector']
        mirror_main_v = mirror_local_axis['primary_vector']
        mirror_secondary_v = mirror_local_axis['secondary_vector']

        if (
            round(primary_v[primary_index], 2) == round(mirror_main_v[primary_index], 2) and
            round(secondary_v[secondary_index], 2) == round(mirror_secondary_v[secondary_index], 2)
        ):
            return False
        else:
            return True

    @staticmethod
    def _get_index_from_axis(axis):
        u"""軸に対応するindexを返す

        :param axis: 'x', 'y', 'z'
        :return: x 0, y 1, z 2 (それ以外の入力亜はx軸をデフォルトして「0」を返す)
        """
        axis_index = {'x': 0, 'y': 1, 'z': 2}
        if axis in axis_index:
            return axis_index[axis]
        else:
            return 0

    @classmethod
    def _get_local_axis(cls, node, primary_axis='x', secondary_axis='y'):
        u"""ローカル軸の取得

        :param node: ノード
        :param primary_axis: primary axis
        :param secondary_axis: secondary axis
        :return:{'primary_axis': axis, 'secondary_axis': axis, 'primary_vector': vector, 'secondary_vector': vector}
        """
        round_vec = lambda vec3, n: (round(vec3[0], n), round(vec3[1], n), round(vec3[2], n))

        vector_x = (1, 0, 0)
        vector_y = (0, 1, 0)
        vector_z = (0, 0, 1)

        primary_index = cls._get_index_from_axis(primary_axis)
        secondary_index = cls._get_index_from_axis(secondary_axis)

        rmatrix = cls._get_rotate_matrix(node)
        for r in rmatrix:
            vector_x = cls._vec3_x_matrix3x3(vector_x, r)
            vector_y = cls._vec3_x_matrix3x3(vector_y, r)
            vector_z = cls._vec3_x_matrix3x3(vector_z, r)

        vector_x = round_vec(vector_x, 3)
        vector_y = round_vec(vector_y, 3)
        vector_z = round_vec(vector_z, 3)

        max_ = max((abs(vector_x[primary_index]), abs(vector_y[primary_index]), abs(vector_z[primary_index])))
        if round(max_, 3) == round(abs(vector_x[primary_index]), 3):
            primary_a = 'x'
            primary_v = vector_x
        elif round(max_, 3) == round(abs(vector_y[primary_index]), 3):
            primary_a = 'y'
            primary_v = vector_y
        else:
            primary_a = 'z'
            primary_v = vector_z

        max_ = max((abs(vector_x[secondary_index]), abs(vector_y[secondary_index]), abs(vector_z[secondary_index])))
        if round(max_, 3) == round(abs(vector_x[secondary_index]), 3):
            secondary_a = 'x'
            secondary_v = vector_x
        elif round(max_, 3) == round(abs(vector_y[secondary_index]), 3):
            secondary_a = 'y'
            secondary_v = vector_y
        else:
            secondary_a = 'z'
            secondary_v = vector_z

        return {
            'primary_axis': primary_a, 'secondary_axis': secondary_a,
            'primary_vector': primary_v, 'secondary_vector': secondary_v,
        }

    @staticmethod
    def _get_world_offset(nodes):
        u"""ノードのリストからworldOffsetを取得

        :param nodes: ノードのリスト
        :return: worldOffset
        """
        for node in nodes:
            if node.find(WORLD_OFFSET) != -1:
                return node

    @staticmethod
    def _has_keyframe(node):
        u"""キーフレームを持っているか

        :param node: ノード名
        :return: bool
        """
        key_index = cmds.keyframe(node, q=True, iv=True)
        return True if key_index else False

    @staticmethod
    def _get_anim_curve(node):
        u"""animCurveの取得

        :param node: ノード名
        :return: {アトリビュート名: カーブ名}
        """
        attr_curve = {}  # アトリビュート名: カーブ名
        attrs = ('tx', 'ty', 'tz', 'rx', 'ry', 'rz')
        # 初期化
        for attr in attrs:
            attr_curve[attr] = None

        for attr in attrs:
            curves = cmds.listConnections('{node}.{attr}'.format(node=node, attr=attr))
            if curves:
                for curve in curves:
                    if cmds.objectType(curve).find('animCurve') != -1:
                        attr_curve[attr] = curve
                        break
            else:
                attr_curve[attr] = None

        return attr_curve

    @staticmethod
    def _is_id_node(node, id_):
        u"""識別子を持つノードかどうか

        :param node: ノード名
        :param id_: 識別子
        :return: bool
        """
        return True if re.search(id_, node) else False

    @staticmethod
    def _get_mirror_node(node, right_id, left_id):
        u"""対称のノードの取得

        :param node: ノード名
        :param right_id: 右側の識別子
        :param left_id: 左側の識別子
        :return:
        """
        left_node = re.sub(right_id, left_id, node)
        right_node = re.sub(left_id, right_id, node)
        if left_node == right_node:
            return None
        elif left_node != node:
            return left_node
        else:
            return right_node

    # ########################################
    #  Reverse
    # ########################################
    @staticmethod
    def _get_reverse_attrs(axis, copytype, is_behavior):
        u"""指定した軸に対して反転するアトリビュートを取得

        :param axis: 軸
        :param copytype: 1: ミラーコピー, 2 ミラー反転
        :param is_behavior: behaviorか
        :return: 反転するアトリビュート
        """
        if copytype == 1:
            if is_behavior:
                axis_attrs = {
                    'x': ('tx', ),
                    'y': ('ty', ),
                    'z': ('tz', ),
                }
            else:
                axis_attrs = {
                    'x': ('tx', 'ry', 'rz'),
                    'y': ('ty', 'rx', 'rz'),
                    'z': ('tz', 'rx', 'ry'),
                }
            if axis in axis_attrs:
                return axis_attrs[axis]
            else:
                return None

        elif copytype == 2:
            axis_attrs = {
                'x': ('tx', 'ry', 'rz'),
                'y': ('ty', 'rx', 'rz'),
                'z': ('tz', 'rx', 'ry'),
            }
            if axis in axis_attrs:
                return axis_attrs[axis]
            else:
                return None
        else:
            return None

    @staticmethod
    def _reverse_pose(node, reverse_attrs, time):
        u"""ポーズを反転

        :param node: ノード名
        :param reverse_attrs: 反転するアトリビュート
        :param time: time
        """
        for attr in reverse_attrs:
            if not cmds.getAttr('{}.{}'.format(node, attr), l=True):
                value = cmds.getAttr('{}.{}'.format(node, attr), t=time)
                cmds.setAttr('{}.{}'.format(node, attr), -1 * value)
                cmds.setKeyframe('{}.{}'.format(node, attr))

    @classmethod
    def _reverse_motion(cls, node, reverse_attrs):
        u"""モーションを反転

        :param node: ノード名
        :param reverse_attrs: 反転するアトリビュート
        """
        attr_curve = cls._get_anim_curve(node)
        for attr in reverse_attrs:
            if attr_curve[attr]:
                cmds.scaleKey(attr_curve[attr], time=(':',), float=(':',), valueScale=-1, valuePivot=0)

    @classmethod
    def _reverse(cls, node, axis, animtype, **kwargs):
        u"""ポーズまたはモーションの反転

        :param node: ノード名
        :param axis: 軸
        :param animtype: 1 pose, 2 motion
        :param copytype: 1: ミラーコピー, 2 ミラー反転
        :param time: 反転時のtime
        """
        logger.debug('Reverse: {} {} {}'.format(node, axis, animtype))

        copytype = kwargs.setdefault('copytype', 2)
        time = kwargs.setdefault('time', 0)
        is_behavior = kwargs.setdefault('is_behavior', True)

        negative_objects = kwargs.setdefault('negative_objects', list())
        negative_attrs = kwargs.setdefault('negative_attrs', list())

        neg_attr_dict = {
            0: 'tx',
            1: 'ty',
            2: 'tz',
            3: 'rx',
            4: 'ry',
            5: 'rz',
        }

        negative_attrs_stock = []
        for i, neg_sts in enumerate(negative_attrs):
            if neg_sts:
                negative_attrs_stock.append(neg_attr_dict[i])

        # ノードの存在判定
        if not cmds.ls(node):
            logger.warning(u'ノードが存在しないため反転をスキップしました: {}'.format(node))
            return
        # 反転するアトリビュートの取得
        reverse_attrs = cls._get_reverse_attrs(axis, copytype, is_behavior)

        # ここから下に一時対処の処理を差し込む
        # ------------------------------------------------------
        for word in cls.temp_check_words:
            if word in node:
                reverse_attrs = ('tx', 'ry', 'rz')  # mirrorもreverseも同じ
                break

        ############# world extend start
        # world用に追加したダミー処理
        world_extend_words = ['hand', 'shoulder']
        for word in world_extend_words:
            if word in node:
                reverse_attrs = ('tx', 'tx', 'tx') # ダミーの値
                break
        ############# end

        ############# wizard2 extend start
        if negative_attrs_stock:
            for word in negative_objects:
                if word in node:
                    reverse_attrs = negative_attrs_stock # ダミーの値
                    break
        else:
            wizard2_extend_words = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
            for word in wizard2_extend_words:
                if word in node:
                    reverse_attrs = ('tx', 'ry', 'rz') # ダミーの値
                    break

        ############# end

        # ------------------------------------------------------
        # ここまで

        if not reverse_attrs:
            logger.warning(u'{}: 軸の指定が不正なので終了します'.format(node))
            return

        if animtype == 1:
            cls._reverse_pose(node, reverse_attrs, time)
        else:
            cls._reverse_motion(node, reverse_attrs)

    @classmethod
    def _reverse_world_offset(cls, world_offset, axis, mode, **kwargs):
        u"""WorldOffsetの反転

        :param world_offset: worldOffsetノード
        :param axis: 反転の軸
        :param mode: 1 Pose, 2 Motion
        :param kwargs: 'time' 反転時のtime
        """
        time = kwargs.setdefault('time', 0)
        # Pose
        if mode == 1:
            if axis == 'x':
                tx = cmds.getAttr('{}.tx'.format(world_offset), t=time)
                cmds.setAttr('{}.tx'.format(world_offset), -1 * tx)
                cmds.setKeyframe('{}.tx'.format(world_offset))
                ry = cmds.getAttr('{}.ry'.format(world_offset), t=time)
                cmds.setAttr('{}.ry'.format(world_offset), -1 * ry)
                cmds.setKeyframe('{}.ry'.format(world_offset))
            elif axis == 'z':
                tz = cmds.getAttr('{}.tz'.format(world_offset), t=time)
                cmds.setAttr('{}.tz'.format(world_offset), -1 * tz)
                cmds.setKeyframe('{}.tz'.format(world_offset))
                ry = cmds.getAttr('{}.ry'.format(world_offset), t=time)
                cmds.setAttr('{}.ry'.format(world_offset), cls._conv_degrees(ry + 180))
                cmds.setKeyframe('{}.ry'.format(world_offset))
        # Motion
        else:
            if axis == 'x':
                cls._reverse_motion(world_offset, ('tx', 'ry'))
            elif axis == 'z':
                cls._reverse_motion(world_offset, ('tz',))
                cmds.keyframe(world_offset, time=(':',), float=(':',), at='ry', vc=180, r=True)

    # ########################################
    #  Mirror
    # ########################################
    @classmethod
    def _copy_animation(cls, node1, node2, **kwargs):
        u"""アニメーションキーをコピー、交換

        :param node1: ノード名1
        :param node2: ノード名2
        :param animtype: 1: ポーズ, 2: モーション
        :param copytype: 1: ミラーコピー, 2 ミラー反転
        :param time: time
        """
        animtype = kwargs.setdefault('animtype', 1)
        copytype = kwargs.setdefault('copytype', 2)
        time = kwargs.setdefault('time', 0)
        times = (time, time)

        # ノードの存在判定
        for node in (node1, node2):
            if not cmds.ls(node):
                logger.debug(u'ノードが存在しないため反転をスキップしました: {}'.format(node))
                return
        # キーフレームの存在判定
        for node in (node1, node2):
            if not cls._has_keyframe(node):
                logger.debug(u'キーが存在しないため反転をスキップしました: {}'.format(node))
                return

        logger.debug(u'アニメーション入れ替え: {}, {}, frame: {}'.format(node1, node2, time))

        # キーの保存用の一時ノードの作成
        temp_node = cmds.spaceLocator()[0]
        try:
            # 一時ノードにキーの保存に必要なカスタムアトリビュートをnode1から取得して追加
            custom_attrs = cmds.listAttr(node1, ud=True, k=True) or []
            for attr in custom_attrs:
                attr_type = cmds.getAttr('{}.{}'.format(node1, attr), typ=True)
                logger.debug(u'カスタムアトリビュート: {}, {}'.format(attr, attr_type))
                if attr_type in cls.type_at:
                    cmds.addAttr(temp_node, ln=attr, k=True, at=attr_type)
                elif attr_type in cls.type_dt:
                    cmds.addAttr(temp_node, ln=attr, k=True, dt=attr_type)
                else:
                    logger.warning(u'カスタムアトリビュートのタイプが判別できませんでした: {}'.format(attr_type))
            # node1のキーを保存
            cmds.copyKey(node1, time=(':',), float=(':',))
            cmds.pasteKey(temp_node, option='replace')

            if animtype == 1:  # pose
                if copytype == 1:
                    # node1のキーをnode2へコピー
                    cmds.copyKey(node1, time=times)
                    cmds.pasteKey(node2, option='replace')

                else:
                    # node1のキーをnode2へコピー
                    cmds.copyKey(node2, time=times)
                    cmds.pasteKey(node1, option='replace')
                    # node2のキーをnode1へコピー
                    cmds.copyKey(temp_node, time=times)
                    cmds.pasteKey(node2, option='replace')

            else:  # motion
                if copytype == 1:
                    # node1のキーをnode2へコピー
                    cmds.cutKey(node2, clear=True)
                    cmds.copyKey(node1, time=(':',), float=(':',))
                    cmds.pasteKey(node2, option='replace')

                else:
                    # node1のキーをnode2へコピー
                    cmds.cutKey(node1, clear=True)
                    cmds.copyKey(node2, time=(':',), float=(':',))
                    cmds.pasteKey(node1, option='replace')
                    # node2のキーをnode1へコピー
                    cmds.cutKey(node2, clear=True)
                    cmds.copyKey(temp_node, time=(':',), float=(':',))
                    cmds.pasteKey(node2, option='replace')

        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            logger.error(u'キーの入れ替え失敗: {}, {}'.format(node1, node2))
        finally:
            cmds.delete(temp_node)

    @staticmethod
    def _reset_controller(nodes):
        for node in nodes:
            for attr in ('tx', 'ty', 'tz', 'rx', 'ry', 'rz'):
                if not cmds.attributeQuery(attr, node=node, ex=True):
                    continue
                if cmds.getAttr('{}.{}'.format(node, attr), l=True):
                    continue
                cmds.setAttr('{}.{}'.format(node, attr), 0)

    @staticmethod
    def _get_time_range():
        u"""Time Rangeの取得

        :return: start, end
        """
        range_set = cmds.ls('rangeSet', typ='objectSet')
        if range_set:
            start = cmds.getAttr('rangeSet.startFrame')
            end = cmds.getAttr('rangeSet.endFrame')
        else:
            start = cmds.playbackOptions(q=True, min=True)
            end = cmds.playbackOptions(q=True, max=True)

        return start, end

    # ########################################
    #  Set
    # ########################################
    @classmethod
    def _is_set(cls, node):
        u"""セットか

        :param node: ノード
        :return: bool
        """
        if cmds.ls(node, typ='objectSet'):
            return True
        else:
            return False

    @classmethod
    def _get_nodes_from_selections(cls, selections):
        u"""指定したセット名からノードを取得

        :param set_: セット名
        :return: ノードのリスト
        """
        nodes = []
        for selection in selections:
            if cls._is_set(selection):
                temp_nodes = cmds.sets(selection, q=True)
                temp_nodes = cls._get_nodes_from_selections(temp_nodes)
                if temp_nodes:
                    nodes.extend(temp_nodes)
            else:
                nodes.append(selection)
        return nodes

    @classmethod
    def _classify_nodes(cls, nodes, right_id, left_id):
        u"""指定したノードからセンター、右、左のノードに分類する

        :param nodes: ノードのリスト
        :param right_id: 右側のノードの識別子
        :param left_id: 左側のノードの識別子
        :return: {'center': center_nodes, 'right': right_nodes, 'left': left_nodes}
        """
        center_nodes = []
        right_nodes = []
        left_nodes = []

        for node in nodes:
            if cls._is_id_node(node, right_id):
                if node not in right_nodes:
                    right_nodes.append(node)
                left_node = cls._get_mirror_node(node, right_id, left_id)
                if left_node not in left_nodes:
                    left_nodes.append(left_node)
            elif cls._is_id_node(node, left_id):
                if node not in left_nodes:
                    left_nodes.append(node)
                right_node = cls._get_mirror_node(node, right_id, left_id)
                if right_node not in right_nodes:
                    right_nodes.append(right_node)
            else:
                if node.find(WORLD_OFFSET) == -1:
                    center_nodes.append(node)

        return {'center': center_nodes, 'right': right_nodes, 'left': left_nodes}

    # ########################################
    #  Exec
    # ########################################
    @classmethod
    def main(cls, nodes_or_sets, **kwargs):
        u"""反転実行用関数

        :param nodes_or_sets: ノードまたはセット (文字列、リストどちらでも可)

        :param right_id: 右側のノードの識別子
        :param left_id: 左側のノードの識別子
        :param animtype: 1: ポーズ, 2: モーション
        :param copytype: 1: ミラーコピー, 2 ミラー反転
        :param function: 1 local, 2 worldOffsetのみ, 3, local反転後、worldoffset反転
        :param axis: 反転の基準軸 'x', 'y', 'z'
        :param l_to_r: LeftノードがソースでRightノードがターゲットか (boolでFalseの場合は逆の処理)
        :param bakes: bakeするか
        """
        right_id = kwargs.setdefault('right_id', 'R_')
        left_id = kwargs.setdefault('left_id', 'L_')
        animtype = kwargs.setdefault('animtype', 1)
        copytype = kwargs.setdefault('copytype', 2)
        function = kwargs.setdefault('function', 1)
        axis = kwargs.setdefault('axis', 'x')
        l_to_r = kwargs.setdefault('l_to_r', True)
        bakes = kwargs.setdefault('bake', False)

        negative_objects = kwargs.setdefault('negative_objects', list())
        negative_attrs = kwargs.setdefault('negative_attrs', list())

        # auto keyかどうかチェック
        state = cmds.autoKeyframe(q=True, st=True)
        cmds.autoKeyframe(st=False)
        # 現在のtimeの記憶
        current = cmds.currentTime(q=True)

        nodes = cls._get_nodes_from_selections(nodes_or_sets)
        world_offset = cls._get_world_offset(nodes)

        # アニメーションのBake
        # poseの場合はbakeのフラグに関わらず必ずベイク
        if animtype == 1 or bakes:
            Bake.main(nodes, hierarchy='none')

        # local
        # if typ == 'local' or typ == 'both':
        if function == 1 or function == 3:
            logger.debug('reverse: local')

            # worldOffsetのリセット
            if world_offset:
                pos = cmds.getAttr('{}.t'.format(world_offset))[0]
                rot = cmds.getAttr('{}.r'.format(world_offset))[0]

                cmds.mute('{}.t'.format(world_offset))
                cmds.mute('{}.r'.format(world_offset))

                cmds.setAttr('{}.t'.format(world_offset), 0, 0, 0)
                cmds.setAttr('{}.r'.format(world_offset), 0, 0, 0)

            classified_nodes = cls._classify_nodes(nodes, right_id, left_id)
            center_nodes = classified_nodes['center']
            right_nodes = classified_nodes['right']
            left_nodes = classified_nodes['left']
            nodes = center_nodes + right_nodes + left_nodes

            node_axis = {}
            node_behavior = {}
            cls._reset_controller(nodes)

            for node in nodes:
                local_axis = cls._get_local_axis(node)
                node_axis[node] = local_axis['primary_axis']
                node_behavior[node] = cls._is_behavior(node, right_id, left_id)

            # mirror
            if copytype == 1:
                # 右、左のノードのミラー
                for right, left in zip(right_nodes, left_nodes):
                    if l_to_r:
                        cls._copy_animation(left, right, animtype=animtype, copytype=copytype, time=current)
                        cls._reverse(right,
                                     node_axis[right],
                                     animtype,
                                     copytype=copytype,
                                     time=current,
                                     is_behavior=node_behavior[right],
                                     negative_objects=negative_objects,
                                     negative_attrs=negative_attrs)
                    else:
                        cls._copy_animation(right, left, animtype=animtype, copytype=copytype, time=current)
                        cls._reverse(left,
                                     node_axis[left],
                                     animtype,
                                     copytype=copytype,
                                     time=current,
                                     is_behavior=node_behavior[left],
                                     negative_objects=negative_objects,
                                     negative_attrs=negative_attrs)

            # reverse
            else:
                # センターノードの反転
                for node in center_nodes:
                    cls._reverse(node,
                                 node_axis[node],
                                 animtype,
                                 time=current,
                                 negative_objects=negative_objects,
                                 negative_attrs=negative_attrs)

                # 右、左のノードの反転
                for right, left in zip(right_nodes, left_nodes):
                    cls._copy_animation(right, left, animtype=animtype, copytype=copytype, time=current)
                    if not node_behavior[right]:
                        cls._reverse(right, node_axis[right], animtype, copytype=copytype, time=current, negative_objects=negative_objects, negative_attrs=negative_attrs)
                        cls._reverse(left, node_axis[left], animtype, copytype=copytype, time=current, negative_objects=negative_objects, negative_attrs=negative_attrs)
                    else:
                        logger.info('skipped reverse: {}, {}'.format(right, left))

            if world_offset:
                cmds.mute('{}.t'.format(world_offset), d=True, f=True)
                cmds.mute('{}.r'.format(world_offset), d=True, f=True)

                cmds.setAttr('{}.t'.format(world_offset), *pos)
                cmds.setAttr('{}.r'.format(world_offset), *rot)

            # if typ == 'both':
            if function == 3:
                logger.debug('reverse: world')
                if world_offset:
                    cls._reverse_world_offset(world_offset, axis, animtype, time=current)

        # worldOffset
        else:
            logger.debug('reverse: world')
            if world_offset:
                cls._reverse_world_offset(world_offset, axis, animtype, time=current)

        cmds.currentTime(current)
        cmds.autoKeyframe(st=state)
    # ########################################
    #  Debug
    # ########################################
    @classmethod
    def debug_reset_controller(cls, *args, **kwargs):
        u"""コントローラーのリセット"""
        selections = cmds.ls(sl=True, typ='objectSet')
        if not selections:
            return

        # ctrl_set = selections[0]
        # nodes = cls._get_nodes_from_selections(ctrl_set)
        nodes = cls._get_nodes_from_selections(selections)

        # auto keyかどうかチェック
        state = cmds.autoKeyframe(q=True, st=True)
        cmds.autoKeyframe(st=False)
        cls._reset_controller(nodes)
        cmds.autoKeyframe(st=state)

    @classmethod
    def debug_show_info(cls, *args, **kwargs):
        u"""ScriptEditorにコントローラーの情報を表示

        :param kwargs: 'mode' 0: Both, 1: behavior, 2: orientation
        """
        # コントローラーの取得

        # 0: Both, 1: behavior, 2: orientation
        mode = kwargs.setdefault('mode', 0)
        displays_left_only = kwargs.setdefault('displays_left_only', False)

        selections = cmds.ls(sl=True, typ='objectSet')
        if not selections:
            return

        ctrl_set = selections[0]
        right_id = 'L_'
        left_id = 'R_'

        # nodes = cls._get_nodes_from_selections(ctrl_set)
        nodes = cls._get_nodes_from_selections([ctrl_set])
        nodes.sort()
        info = u'\n{:^35s} {:^6s} {:^6s} {:^7s} {:^30s} {:^30s}\n'.format(
            'node', 'p_axis', 's_axis', 'behavior', 'p_v', 's_v',
        )
        info += u'{:-<35s} {:-<6s} {:-<6s} {:-<7s} {:-<30s} {:-<30s}\n'.format('', '', '', '', '', '')

        cls.debug_reset_controller()
        for node in nodes:
            if displays_left_only and (not cls._is_id_node(node, right_id) or cls._is_id_node(node, left_id)):
                continue

            is_behavior = cls._is_behavior(node, right_id, left_id)
            if (mode == 1 and not is_behavior) or (mode == 2 and is_behavior):
                continue

            local_axis = cls._get_local_axis(node)
            primary_axis = local_axis['primary_axis']
            secondary_axis = local_axis['secondary_axis']

            primary_vector = local_axis['primary_vector']
            secondary_vector = local_axis['secondary_vector']

            info += u'{:35s} {:6s} {:6s} {:7} {:30s} {:30s}\n'.format(
                node, primary_axis, secondary_axis, is_behavior, primary_vector, secondary_vector,
            )

        logger.info(info)


class ReverseMotion(object):

    def __init__(self, *args, **kwargs):
        u"""初期化"""
        self.window = self.__class__.__name__
        self.close()

        self.main_layout = None

        self.ui = None
        self.url = 'https://wisdom2.cygames.jp/pages/viewpage.action?pageId=30421204'

        self._tool_name = 'mirrormotion'
        self.title = 'MirrorMotion'

        self._animtype_key = '{}.animtype'.format(__package__)
        self._animtype_control = None

        self._copytype_key = '{}.copytype'.format(__package__)
        self._copytype_control = None

        self._l_to_r_key = '{}.l_to_r'.format(__package__)
        self._l_to_r_control = None
        self._num_l_to_r = {1: True, 2: False}

        self._left_id_key = '{}.left_id'.format(__package__)
        self._left_id_control = None

        self._right_id_key = '{}.right_id'.format(__package__)
        self._right_id_control = None

        self._bakes_key = '{}.bakes'.format(__package__)
        self._bakes_control = None

        self._function_key = '{}.function'.format(__package__)
        self._function_control = None

        self._axis_key = '{}.axis'.format(__package__)
        self._axis_control = None
        self._num_axis = {1: 'x', 2: 'y', 3: 'z'}

        self._negative_objects_key = '{}.negative_objects'.format(__package__)
        self._negative_attrs_key = '{}.negative_attrs'.format(__package__)

        self.width = 540
        self.height = 360

    def _initialize_window(self):
        u"""Windowの初期化"""
        if not cmds.window(self.window, ex=True):
            self.window = cmds.window(self.window, mb=True)

    def _add_baselayout(self):
        u"""基本レイアウトの追加"""
        # メニューバー
        self._add_editmenu()
        self._add_helpmenu()
        self._add_debugmenu()

        mainform = cmds.formLayout(nd=100)
        maintab = cmds.tabLayout(tv=False, scr=True, cr=True, h=1)
        self.main_layout = cmds.columnLayout(adj=1)
        # レイアウト作成 ====
        self._create()
        # ====
        cmds.setParent(mainform)

        execform = self._add_execform()
        cmds.formLayout(
            mainform, e=True,
            af=(
                [maintab, 'top', 0],
                [maintab, 'left', 2],
                [maintab, 'right', 2],
                [execform, 'left', 2],
                [execform, 'right', 2],
                [execform, 'bottom', 0],
            ),
            ac=(
                [maintab, 'bottom', 5, execform],
            ),
        )
        cmds.setParent(self.main_layout)

    def _create(self):
        u"""Windowのレイアウト作成"""
        form = cmds.formLayout()
        column = cmds.columnLayout(adj=1)
        cmds.frameLayout(l='Basic Options', mh=5)
        # animtype
        self._animtype_control = cmds.radioButtonGrp(
            l='Anim Type:', la2=('Pose', 'Motion'),
            cw3=(80, 150, 150), nrb=2, sl=1,
            cc=self._animtype_control_command,
        )
        # copytype
        self._copytype_control = cmds.radioButtonGrp(
            # la2=('Mirror', 'Reverse'), ラベル名をアニメーター要望に合わせて変更
            # コマンド側の名称は時間の都合で昔のまま
            l='Copy Type:', la2=('Copy', 'Mirror'),
            cw3=(80, 150, 150), nrb=2, sl=1,
            cc=self._copytype_control_command,
        )
        # l_tor_r
        self._l_to_r_control = cmds.radioButtonGrp(
            l='', la2=('L -> R', 'R -> L'),
            cw3=(80, 150, 150), nrb=2, sl=1,
            cc=self._save_settings,
        )

        # ID
        cmds.rowLayout(
            adj=5, nc=5,
            cat=[(1, 'right', 0), (2, 'left', 0), (3, 'right', 0), (4, 'left', 0)],
            cw=((1, 80), (2, 70), (3, 80), (4, 70)),
        )
        # left_id
        cmds.text(l='Left ID:')
        self._left_id_control = cmds.textField(tx='L_', cc=self._save_settings)
        cmds.text(l='Right ID:')
        self._right_id_control = cmds.textField(tx='R_', cc=self._save_settings)
        cmds.text(l='')  # スペーサー
        cmds.setParent('..')  # rowLayout

        # Negative Objects
        cmds.rowLayout(
            adj=5, nc=5,
            cat=[(1, 'right', 0), (2, 'left', 0), (3, 'right', 0), (4, 'left', 0)],
            cw=((1, 80), (2, 70), (3, 80), (4, 70)),
        )
        cmds.text(l='Neg Objects:')
        self._negative_objects = cmds.textField(tx='Thumb, Index, Middle, Ring, Pinky', cc=self._save_settings, w=400)
        cmds.text(l='')  # スペーサー
        cmds.setParent('..')  # rowLayout

        # Negative Objects
        cmds.rowLayout(
            adj=8, nc=8,
            cat=[(1, 'right', 0)],
            cw=((1, 80)),
        )
        cmds.text(l='Neg Attrs:')
        self._negative_attrs_tx = cmds.checkBox(l='tx', cc=self._save_settings)
        self._negative_attrs_ty = cmds.checkBox(l='ty', cc=self._save_settings)
        self._negative_attrs_tz = cmds.checkBox(l='tz', cc=self._save_settings)
        self._negative_attrs_rx = cmds.checkBox(l='rx', cc=self._save_settings)
        self._negative_attrs_ry = cmds.checkBox(l='ry', cc=self._save_settings)
        self._negative_attrs_rz = cmds.checkBox(l='rz', cc=self._save_settings)
        cmds.text(l='')  # スペーサー
        cmds.setParent('..')  # rowLayout

        cmds.setParent('..')  # frame

        cmds.frameLayout(l='Extra Options', mh=5)
        # function
        self._function_control = cmds.radioButtonGrp(
            l='Function:', la3=('Local', 'WorldOffset Only', 'Local && WorldOffset'),
            cw4=(80, 150, 150, 150), nrb=3, sl=1,
            cc=self._function_control_command,
        )
        # axis
        self._axis_control = cmds.radioButtonGrp(
            l='Axis:', la3=('X (YZ)', 'Y (XZ)', 'Z (XY)'),
            cw4=(80, 150, 150, 150), nrb=3, sl=1,
            cc=self._save_settings,
        )
        self._bakes_control = cmds.checkBoxGrp(l='Bakes:', v1=False, cw2=(80, 150), cc=self._save_settings)
        cmds.setParent('..')

        cmds.setParent('..')  # column
        cmds.formLayout(
            form, e=True,
            af=(
                [column, 'top', 10],
                [column, 'left', 0],
                [column, 'bottom', 50],
            ),
        )
        cmds.setParent('..')  # form

    def _boot_event(self):
        self._animtype_control_command()
        self._copytype_control_command()
        self._function_control_command()

    def _animtype_control_command(self, *args):
        if cmds.radioButtonGrp(self._animtype_control, q=True, sl=True) == 2:
            cmds.checkBoxGrp(self._bakes_control, e=True, en=True)
        else:
            cmds.checkBoxGrp(self._bakes_control, e=True, en=False)
        self._save_settings()

    def _copytype_control_command(self, *args):
        if cmds.radioButtonGrp(self._copytype_control, q=True, sl=True) == 1:
            cmds.radioButtonGrp(self._l_to_r_control, e=True, en=True)
        else:
            cmds.radioButtonGrp(self._l_to_r_control, e=True, en=False)
        self._save_settings()

    def _function_control_command(self, *args):
        if cmds.radioButtonGrp(self._function_control, q=True, sl=True) == 1:
            cmds.radioButtonGrp(self._axis_control, e=True, en=False)
        else:
            cmds.radioButtonGrp(self._axis_control, e=True, en=True)
        self._save_settings()

    def _add_execform(self):
        u"""Apply Closeボタンの追加

        :return: フォーム名
        """
        execform = cmds.formLayout(nd=100)
        # ボタン
        apply_close_btn = cmds.button(l='Apply and Close', h=26, c=self._apply_close)
        apply_btn = cmds.button(l='Apply', h=26, c=self._apply)
        close_btn = cmds.button(l='Close', h=26, c=self.close)
        # レイアウト
        cmds.formLayout(
            execform, e=True,
            af=(
                [apply_close_btn, 'left', 0],
                [apply_close_btn, 'bottom', 5],
                [apply_btn, 'bottom', 5],
                [close_btn, 'bottom', 5],
                [close_btn, 'right', 0],
            ),
            ap=(
                [apply_close_btn, 'right', 1, 33],
                [close_btn, 'left', 0, 67],
            ),
            ac=(
                [apply_btn, 'left', 4, apply_close_btn],
                [apply_btn, 'right', 4, close_btn],
            ),
        )
        cmds.setParent('..')
        return execform

    def _help(self, *args):
        u"""help表示"""
        cmds.showHelp(self.url, a=True)

    def _add_editmenu(self):
        u"""menu「Edit」を追加"""
        cmds.menu(l='Edit')
        cmds.menuItem(l='Save Settings', c=self._save_settings)
        cmds.menuItem(l='Reset Settings', c=self._reset_settings)

    def _add_helpmenu(self):
        u"""menu「Help」を追加"""
        cmds.menu(l='Help')
        cmds.menuItem(l='Help on {0}'.format(self.title), c=self._help)

    def _add_debugmenu(self):
        u"""メニューアイテムを追加"""
        cmds.menu(l='Debug', to=True)
        cmds.menuItem(l=u'コントローラーのリセット', c=ReverseMotionCmd.debug_reset_controller)
        cmds.menuItem(l=u'コントローラーの情報を表示', c=ReverseMotionCmd.debug_show_info)
        cmds.menuItem(l=u'コントローラーの情報を表示(behaviorのみ)', c=partial(ReverseMotionCmd.debug_show_info, mode=1))
        cmds.menuItem(
            l=u'コントローラーの情報を表示(leftノードのみ)',
            c=partial(ReverseMotionCmd.debug_show_info, displays_left_only=True),
        )
        cmds.menuItem(
            l=u'コントローラーの情報を表示(behavior, leftノードのみ)',
            c=partial(ReverseMotionCmd.debug_show_info, mode=1, displays_left_only=True),
        )

    def _read_settings(self, *args):
        u"""設定の読み込み"""
        animtype = int(cmds.optionVar(q=self._animtype_key))
        if animtype:
            cmds.radioButtonGrp(self._animtype_control, e=True, sl=animtype)
        l_to_r = int(cmds.optionVar(q=self._copytype_key))
        if l_to_r:
            cmds.radioButtonGrp(self._copytype_control, e=True, sl=l_to_r)
        copytype = int(cmds.optionVar(q=self._copytype_key))
        if copytype:
            cmds.radioButtonGrp(self._copytype_control, e=True, sl=copytype)
        function = int(cmds.optionVar(q=self._function_key))
        if function:
            cmds.radioButtonGrp(self._function_control, e=True, sl=function)
        axis = int(cmds.optionVar(q=self._axis_key))
        if axis:
            cmds.radioButtonGrp(self._axis_control, e=True, sl=axis)
        left_id = cmds.optionVar(q=self._left_id_key)
        if left_id:
            cmds.textField(self._left_id_control, e=True, tx=left_id)
        right_id = cmds.optionVar(q=self._right_id_key)
        if right_id:
            cmds.textField(self._right_id_control, e=True, tx=right_id)
        bakes = strtobool(str(cmds.optionVar(q=self._bakes_key)))
        if bakes:
            cmds.checkBoxGrp(self._bakes_control, e=True, v1=True)
        else:
            cmds.checkBoxGrp(self._bakes_control, e=True, v1=False)

        try:
            negative_objects = eval(cmds.optionVar(q=self._negative_objects_key))
            if negative_objects:
                text_negative_objects = ','.join(negative_objects)
                cmds.textField(self._negative_objects, e=True, tx=text_negative_objects)

            negative_attrs = eval(cmds.optionVar(q=self._negative_attrs_key))
            if negative_attrs:
                if negative_attrs[0]:
                    cmds.checkBox(self._negative_attrs_tx, e=True, v=True)
                if negative_attrs[1]:
                    cmds.checkBox(self._negative_attrs_ty, e=True, v=True)
                if negative_attrs[2]:
                    cmds.checkBox(self._negative_attrs_tz, e=True, v=True)
                if negative_attrs[3]:
                    cmds.checkBox(self._negative_attrs_rx, e=True, v=True)
                if negative_attrs[4]:
                    cmds.checkBox(self._negative_attrs_ry, e=True, v=True)
                if negative_attrs[5]:
                    cmds.checkBox(self._negative_attrs_rz, e=True, v=True)

        except:
            print(traceback.format_exc())

    def get_negative_object_values(self):
        _negative_objects = cmds.textField(self._negative_objects, q=True, tx=True)
        _neg_tx = cmds.checkBox(self._negative_attrs_tx, q=True, v=True)
        _neg_ty = cmds.checkBox(self._negative_attrs_ty, q=True, v=True)
        _neg_tz = cmds.checkBox(self._negative_attrs_tz, q=True, v=True)
        _neg_rx = cmds.checkBox(self._negative_attrs_rx, q=True, v=True)
        _neg_ry = cmds.checkBox(self._negative_attrs_ry, q=True, v=True)
        _neg_rz = cmds.checkBox(self._negative_attrs_rz, q=True, v=True)

        _negative_objects = [ng_ob.replace(' ', '') for ng_ob in _negative_objects.split(',')]

        return _negative_objects, [_neg_tx, _neg_ty, _neg_tz, _neg_rx, _neg_ry, _neg_rz]

    def _save_settings(self, *args):
        u"""設定の保存

        :return: 設定 (dict)
        """

        neg_objects, neg_attrs = self.get_negative_object_values()

        settings = {
            self._animtype_key: cmds.radioButtonGrp(self._animtype_control, q=True, sl=True),
            self._copytype_key: cmds.radioButtonGrp(self._copytype_control, q=True, sl=True),
            self._l_to_r_key: cmds.radioButtonGrp(self._l_to_r_control, q=True, sl=True),
            self._function_key: cmds.radioButtonGrp(self._function_control, q=True, sl=True),
            self._axis_key: cmds.radioButtonGrp(self._axis_control, q=True, sl=True),
            self._left_id_key: cmds.textField(self._left_id_control, q=True, tx=True),
            self._right_id_key: cmds.textField(self._right_id_control, q=True, tx=True),
            self._bakes_key: cmds.checkBoxGrp(self._bakes_control, q=True, v1=True),

            self._negative_objects_key: neg_objects,
            self._negative_attrs_key: neg_attrs,
        }

        # print('Save Settings: ', settings)

        # mayaPrefs.melに保存
        [cmds.optionVar(sv=(k, str(v))) for k, v in settings.items()]
        logger.debug(settings)
        return settings

    def _reset_settings(self, *args):
        u"""設定のリセット"""
        cmds.radioButtonGrp(self._animtype_control, e=True, sl=1)
        cmds.radioButtonGrp(self._copytype_control, e=True, sl=1)
        cmds.radioButtonGrp(self._l_to_r_control, e=True, sl=1)
        cmds.radioButtonGrp(self._function_control, e=True, sl=1)
        cmds.radioButtonGrp(self._axis_control, e=True, sl=1)
        cmds.textField(self._left_id_control, e=True, tx='_L_')
        cmds.textField(self._right_id_control, e=True, tx='_R_')

        cmds.textField(self._negative_objects, e=True, tx='Thumb, Index, Middle, Ring, Pinky')

        cmds.checkBox(self._negative_attrs_tx, e=True, v=True)
        cmds.checkBox(self._negative_attrs_ty, e=True, v=False)
        cmds.checkBox(self._negative_attrs_tz, e=True, v=False)
        cmds.checkBox(self._negative_attrs_rx, e=True, v=False)
        cmds.checkBox(self._negative_attrs_ry, e=True, v=True)
        cmds.checkBox(self._negative_attrs_rz, e=True, v=True)

        # リセット後に設定を保存
        self._save_settings()
        self._boot_event()

    def _apply(self, *args):
        u"""「現在のシーンを反転」ボタンのコマンド"""
        settings = self._save_settings()
        settings[self._l_to_r_key] = self._num_l_to_r[settings[self._l_to_r_key]]
        settings[self._axis_key] = self._num_axis[settings[self._axis_key]]
        settings = {re.sub('{}.'.format(__package__), '', k): v for k, v in settings.items()}

        logger.debug('Option')
        for k, v in settings.items():
            logger.debug('{}: {}'.format(k, v))

        selections = cmds.ls(sl=True)
        ReverseMotionCmd.main(selections, **settings)
        cmds.select(selections, ne=True)

    def _apply_close(self, *args):
        u"""ApplyCloseボタンの実行コマンド"""
        self._apply()
        self.close()

    def show(self, *args):
        u"""Windowの表示"""
        self._initialize_window()
        self._add_baselayout()

        self._read_settings()
        self._boot_event()

        cmds.showWindow(self.window)
        cmds.window(self.window, e=True, t=self.title, wh=(self.width, self.height))

    def close(self, *args):
        u"""Windowのclose"""
        if cmds.window(self.window, ex=True):
            cmds.deleteUI(self.window)

# if __name__ == '__main__':
#     mirror_tool = ReverseMotion()
#     mirror_tool.show()


def mirror_character(mirrors=['_L', '_R'], replace_src=None):
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

def match_foot_roll(setkey=None, side='_L_', main_to_foot=None, namespace=None):
    if not namespace:
        namespace = get_mgpickernamespace()
    foot_roll_match = {
        namespace + 'ik_Ankle_L_ctrl':
            {
                'matchloc':namespace + 'proxy_Ankle_L_match_loc',
                'main':namespace + 'roll_main_Ankle_L_ctrl',
                'tippytoe':namespace + 'roll_tippytoe_Ankle_L_ctrl',
                'heel':namespace + 'roll_heel_Ankle_L_ctrl',
                'inside':namespace + 'roll_in_Ankle_L_ctrl',
                'outside':namespace + 'roll_out_Ankle_L_ctrl',
                'rolltoe':namespace + 'roll_Toe_L_ctrl',
                'toe':namespace + 'ik_Toe_L_ctrl',
                'rollankle':namespace + 'roll_Ankle_L_ctrl',
                'stoptoe':namespace + 'roll_stoptoe_Toe_L_ctrl',
            },
        namespace + 'ik_Ankle_R_ctrl':
            {
                'matchloc':namespace + 'proxy_Ankle_R_match_loc',
                'main':namespace + 'roll_main_Ankle_R_ctrl',
                'tippytoe':namespace + 'roll_tippytoe_Ankle_R_ctrl',
                'heel':namespace + 'roll_heel_Ankle_R_ctrl',
                'inside':namespace + 'roll_in_Ankle_R_ctrl',
                'outside':namespace + 'roll_out_Ankle_R_ctrl',
                'rolltoe':namespace + 'roll_Toe_R_ctrl',
                'toe':namespace + 'ik_Toe_R_ctrl',
                'rollankle':namespace + 'roll_Ankle_R_ctrl',
                'stoptoe':namespace + 'roll_stoptoe_Toe_R_ctrl',
            },
    }

    for foot_ctrl, match_settings in foot_roll_match.items():
        if side in foot_ctrl:
            matchloc = match_settings['matchloc']
            main = match_settings['main']
            tippytoe = match_settings['tippytoe']
            heel = match_settings['heel']
            inside = match_settings['inside']
            outside = match_settings['outside']
            rolltoe = match_settings['rolltoe']
            toe = match_settings['toe']
            rollankle = match_settings['rollankle']
            stoptoe = match_settings['stoptoe']

            matchloc_wt = cmds.xform(matchloc, q=True, t=True, ws=True)
            matchloc_wr = cmds.xform(matchloc, q=True, ro=True, ws=True)

            footroll_wt = cmds.xform(rolltoe, q=True, t=True, ws=True)
            footroll_wr = cmds.xform(rolltoe, q=True, ro=True, ws=True)

            toe_wr = cmds.xform(toe, q=True, ro=True, ws=True)

            foot_roll_ctrls = [
                main,
                tippytoe,
                heel,
                inside,
                outside,
                rolltoe,
                toe,
                rollankle,
                stoptoe,
            ]

            [cmds.xform(obj, t=[0,0,0], ro=[0,0,0], a=True) for obj in foot_roll_ctrls]

            if main_to_foot:
                # main > footroll
                cmds.xform(foot_ctrl, t=[0,0,0], ro=[0,0,0], a=True)
                cmds.xform(rolltoe, t=footroll_wt, ro=footroll_wr, ws=True, p=True, a=True)

            else:
                # footroll > main
                cmds.xform(foot_ctrl, t=matchloc_wt, ro=matchloc_wr, ws=True, p=True, a=True)

            cmds.xform(toe, ro=toe_wr, ws=True, p=True, a=True)

            if setkey:
                [cmds.setKeyframe(obj) for obj in foot_roll_ctrls]
                cmds.setKeyframe(foot_ctrl)


def bake_with_func(func):
    def wrapper(*args, **kwargs):
        try:
            cmds.refresh(su=1)

            cur_time=cmds.currentTime(q=1)
            if cmds.autoKeyframe(q=True, st=True):
                autoKeyState = True
            else:
                autoKeyState = False

            cmds.autoKeyframe(st=0)

            playmin = cmds.playbackOptions(q=1, min=1)
            playmax = cmds.playbackOptions(q=1, max=1)

            start = playmin
            end = playmax

            for i in range (int(start), int(end+1)):
                cmds.currentTime(i, e=True)
                func(*args, **kwargs)

            cmds.currentTime(cur_time)
            cmds.autoKeyframe(state=autoKeyState)

            cmds.refresh(su=0)

        except:
            cmds.refresh(su=0)
            print(traceback.format_exc())

    return wrapper

def bake_with_func_for_timeSlider(func):
    def wrapper(*args, **kwargs):
        cur_time=cmds.currentTime(q=1)
        if cmds.autoKeyframe(q=True, st=True):
            autoKeyState = 1
        else:
            autoKeyState = 0

        cmds.autoKeyframe(st=0)

        try:
            cmds.refresh(su=1)

            playmin = cmds.playbackOptions(q=1, min=1)
            playmax = cmds.playbackOptions(q=1, max=1)

            start = playmin
            end = playmax-1

            gPlayBackSlider = mel.eval('$temp=$gPlayBackSlider')
            if gPlayBackSlider:
                if cmds.timeControl(gPlayBackSlider, q=True, rv=True):
                    frameRange = cmds.timeControl(gPlayBackSlider, q=True, ra=True)
                    start = frameRange[0]
                    end = frameRange[1]
                else:
                    frameRange = cmds.currentTime(q=1)
                    start = frameRange
                    end = frameRange-1
            else:
                end = playmax

            if playmax < end:
                end = playmax

            setkey_attrs = mel.eval('string $selectedChannelBox[] = `channelBox -query -selectedMainAttributes mainChannelBox`;')
            if setkey_attrs == []:
                setkey_attrs =  [u'tx', u'ty', u'tz', u'rx', u'ry', u'rz', u'sx', u'sy', u'sz']

            for i in range (int(start), int(end+1)):
                cmds.currentTime(i, e=True)
                func(*args, **kwargs)

            cmds.refresh(su=0)

        except:
            cmds.refresh(su=0)
            print(traceback.format_exc())

        cmds.currentTime(cur_time)
        cmds.autoKeyframe(state=autoKeyState)

    return wrapper

def get_mgpickernamespace():
    #get the namespace of current picker file.
    currentPickerNamespace = mel.eval('MGP_GetCurrentPickerNamespace')

    if currentPickerNamespace:
        currentPickerNamespace = currentPickerNamespace + ':'
    else:
        currentPickerNamespace = ''

    return currentPickerNamespace


def get_hand_L_ctrl_values(namespace=None):
    if namespace == '<from_picker>':
        currentPickerNamespace = get_mgpickernamespace()
    else:
        currentPickerNamespace = namespace

    ikfk_switch = currentPickerNamespace+'ikfk_Wrist_L_ctrl.ikfk'
    state = cmds.getAttr(ikfk_switch)
    jnts = [currentPickerNamespace+'proxy_Arm_L',
            currentPickerNamespace+'proxy_Elbow_L',
            currentPickerNamespace+'proxy_Wrist_L']
    ctrls = [currentPickerNamespace+'Arm_L_ctrl',
             currentPickerNamespace+'Elbow_L_ctrl',
             currentPickerNamespace+'Wrist_L_ctrl']

    ik_pos_ctrl = currentPickerNamespace+'ik_Wrist_L_ctrl'
    ik_rot_ctrl = currentPickerNamespace+'ik_rot_Wrist_L_ctrl'
    ikpv_ctrl = currentPickerNamespace+'ik_Elbow_L_ctrl'

    pos_match_loc = currentPickerNamespace+'proxy_Wrist_L_match_loc'
    ikpv_match_loc = currentPickerNamespace+'proxy_Elbow_L_match_loc'

    return ikfk_switch, state, jnts, ctrls, ik_pos_ctrl, ik_rot_ctrl, ikpv_ctrl, pos_match_loc, ikpv_match_loc, currentPickerNamespace

def get_foot_L_ctrl_values(namespace=None):
    if namespace == '<from_picker>':
        currentPickerNamespace = get_mgpickernamespace()
    else:
        currentPickerNamespace = namespace

    ikfk_switch = currentPickerNamespace+'ikfk_Ankle_L_ctrl.ikfk'
    state = cmds.getAttr(ikfk_switch)
    jnts = [currentPickerNamespace+'proxy_Thigh_L',
            currentPickerNamespace+'proxy_Knee_L',
            currentPickerNamespace+'proxy_Ankle_L',
            currentPickerNamespace+'proxy_Toe_L',]
    ctrls = [currentPickerNamespace+'Thigh_L_ctrl',
             currentPickerNamespace+'Knee_L_ctrl',
             currentPickerNamespace+'Ankle_L_ctrl',
             currentPickerNamespace+'Toe_L_ctrl']

    ik_pos_ctrl = currentPickerNamespace+'ik_Ankle_L_ctrl'
    ik_rot_ctrl = currentPickerNamespace+'ik_Toe_L_ctrl'
    ikpv_ctrl = currentPickerNamespace+'ik_Knee_L_ctrl'

    pos_match_loc = currentPickerNamespace+'proxy_Ankle_L_match_loc'
    ikpv_match_loc = currentPickerNamespace+'proxy_Knee_L_match_loc'

    return ikfk_switch, state, jnts, ctrls, ik_pos_ctrl, ik_rot_ctrl, ikpv_ctrl, pos_match_loc, ikpv_match_loc, currentPickerNamespace


def ik2fk_match(ctrls=None, jnts=None, ikfk_switch=None, match=None):
    sel = cmds.ls(os=True)
    # IK to FK
    if match:
        [cmds.matchTransform(ctrl, jt, rot=1, pos=0, scl=0) for ctrl, jt in zip(ctrls, jnts)]
    cmds.setAttr(ikfk_switch, 0)

    cmds.select(sel, r=True)

def fk2ik_match(match_type=None,
                ik_pos_ctrl=None,
                pos_match_loc=None,
                ikpv_ctrl=None,
                ikpv_match_loc=None,
                ik_rot_ctrl=None,
                rot_match_jnt=None,
                ikfk_switch=None,
                match=None,
                start=None,
                mid=None,
                end=None,
                move=None,
                loc_match=None):

    sel = cmds.ls(os=True)
    # FK to IK
    if match:
        if loc_match:
            cmds.matchTransform(ik_pos_ctrl, pos_match_loc)
            cmds.matchTransform(ikpv_ctrl, ikpv_match_loc)
            cmds.matchTransform(ik_rot_ctrl, rot_match_jnt)
        else:
            cmds.matchTransform(ik_pos_ctrl, pos_match_loc, rot=1, pos=1, scl=0)
            set_pole_vec(start=start, mid=mid, end=end, move=move, obj=ikpv_ctrl)
            # cmds.matchTransform(ikpv_ctrl, ikpv_match_loc, rot=1, pos=1, scl=0)
            cmds.matchTransform(ik_rot_ctrl, rot_match_jnt, rot=1, pos=1, scl=0)

    cmds.setAttr(ikfk_switch, 1)

    cmds.select(sel, r=True)

def ikfk_hand_L(picker=None, match=None, force_state=None, force_state_key=None, namespace=None):
    ikfk_switch, state, jnts, ctrls, ik_pos_ctrl, ik_rot_ctrl, ikpv_ctrl, pos_match_loc, ikpv_match_loc, namespace = get_hand_L_ctrl_values(namespace)

    if force_state:
        if force_state == 'ik2fk':
            state = 1
        elif force_state == 'fk2ik':
            state = 0
        cmds.setAttr(ikfk_switch, state)

        cmds.setKeyframe(ikfk_switch) if force_state_key else False

    if state == 1:
        ik2fk_match(ctrls=ctrls,
                    jnts=jnts,
                    ikfk_switch=ikfk_switch,
                    match=match)

        if picker:
            # IK
            mel.eval('MGPickerItem -e -vis false selectButton79;')
            mel.eval('MGPickerItem -e -vis false selectButton88;')
            mel.eval('MGPickerItem -e -vis false selectButton101;')

            # FK
            mel.eval('MGPickerItem -e -vis true selectButton99;')
            mel.eval('MGPickerItem -e -vis true selectButton94;')
            mel.eval('MGPickerItem -e -vis true selectButton91;')

    else:
        fk2ik_match(ik_pos_ctrl=ik_pos_ctrl,
                    pos_match_loc=pos_match_loc,
                    ikpv_ctrl=ikpv_ctrl,
                    ikpv_match_loc=ikpv_match_loc,
                    ik_rot_ctrl=ik_rot_ctrl,
                    rot_match_jnt=jnts[2],
                    ikfk_switch=ikfk_switch,
                    match=match,
                    start=jnts[0],
                    mid=jnts[1],
                    end=jnts[2],
                    move=50,
                    loc_match=True)

        if picker:
            # IK
            mel.eval('MGPickerItem -e -vis true selectButton79;')
            mel.eval('MGPickerItem -e -vis true selectButton88;')
            mel.eval('MGPickerItem -e -vis true selectButton101;')

            # FK
            mel.eval('MGPickerItem -e -vis false selectButton99;')
            mel.eval('MGPickerItem -e -vis false selectButton94;')
            mel.eval('MGPickerItem -e -vis false selectButton91;')

    ctrls.append(ik_pos_ctrl)
    ctrls.append(ik_rot_ctrl)
    ctrls.append(ikpv_ctrl)

    ctrls.append(ikfk_switch) if force_state_key else False

    return ctrls



def ikfk_hand_R(picker=None, match=None, force_state=None, force_state_key=None, namespace=None):
    ikfk_switch, state, jnts, ctrls, ik_pos_ctrl, ik_rot_ctrl, ikpv_ctrl, pos_match_loc, ikpv_match_loc, namespace = get_hand_L_ctrl_values(namespace)

    ikfk_switch = mirror_character(['_L', '_R'], ikfk_switch)
    ik_pos_ctrl = mirror_character(['_L', '_R'], ik_pos_ctrl)
    ik_rot_ctrl = mirror_character(['_L', '_R'], ik_rot_ctrl)
    ikpv_ctrl = mirror_character(['_L', '_R'], ikpv_ctrl)
    pos_match_loc = mirror_character(['_L', '_R'], pos_match_loc)
    ikpv_match_loc = mirror_character(['_L', '_R'], ikpv_match_loc)

    jnts = [mirror_character(['_L', '_R'], jnt) for jnt in jnts]
    ctrls = [mirror_character(['_L', '_R'], ctrl) for ctrl in ctrls]

    state = cmds.getAttr(ikfk_switch)

    if force_state:
        if force_state == 'ik2fk':
            state = 1
        elif force_state == 'fk2ik':
            state = 0
        cmds.setAttr(ikfk_switch, state)

        cmds.setKeyframe(ikfk_switch) if force_state_key else False

    if state == 1:
        ik2fk_match(ctrls=ctrls,
                    jnts=jnts,
                    ikfk_switch=ikfk_switch,
                    match=match)

        if picker:
            # IK
            mel.eval('MGPickerItem -e -vis false selectButton110;')
            mel.eval('MGPickerItem -e -vis false selectButton118;')
            mel.eval('MGPickerItem -e -vis false selectButton102;')

            # FK
            mel.eval('MGPickerItem -e -vis true selectButton115;')
            mel.eval('MGPickerItem -e -vis true selectButton75;')
            mel.eval('MGPickerItem -e -vis true selectButton109;')

    else:
        fk2ik_match(ik_pos_ctrl=ik_pos_ctrl,
                    pos_match_loc=pos_match_loc,
                    ikpv_ctrl=ikpv_ctrl,
                    ikpv_match_loc=ikpv_match_loc,
                    ik_rot_ctrl=ik_rot_ctrl,
                    rot_match_jnt=jnts[2],
                    ikfk_switch=ikfk_switch,
                    match=match,
                    start=jnts[0],
                    mid=jnts[1],
                    end=jnts[2],
                    move=50,
                    loc_match=True)

        if picker:
            # IK
            mel.eval('MGPickerItem -e -vis true selectButton110;')
            mel.eval('MGPickerItem -e -vis true selectButton118;')
            mel.eval('MGPickerItem -e -vis true selectButton102;')

            # FK
            mel.eval('MGPickerItem -e -vis false selectButton115;')
            mel.eval('MGPickerItem -e -vis false selectButton75;')
            mel.eval('MGPickerItem -e -vis false selectButton109;')

    ctrls.append(ik_pos_ctrl)
    ctrls.append(ik_rot_ctrl)
    ctrls.append(ikpv_ctrl)

    ctrls.append(ikfk_switch) if force_state_key else False

    return ctrls



def ikfk_foot_L(picker=None, match=None, force_state=None, force_state_key=None, namespace=None):
    ikfk_switch, state, jnts, ctrls, ik_pos_ctrl, ik_rot_ctrl, ikpv_ctrl, pos_match_loc, ikpv_match_loc, namespace = get_foot_L_ctrl_values(namespace)

    roll_Toe_ctrl = namespace + 'roll_Toe_L_ctrl'

    if force_state:
        if force_state == 'ik2fk':
            state = 1
        elif force_state == 'fk2ik':
            state = 0
        cmds.setAttr(ikfk_switch, state)

        cmds.setKeyframe(ikfk_switch) if force_state_key else False

    if state == 1:
        ik2fk_match(ctrls=ctrls,
                    jnts=jnts,
                    ikfk_switch=ikfk_switch,
                    match=match)

        cmds.xform(roll_Toe_ctrl, t=[0,0,0], ro=[0,0,0], p=True, a=True) if match else False

        if picker:
            # IK
            mel.eval('MGPickerItem -e -vis false selectButton87;')
            mel.eval('MGPickerItem -e -vis false selectButton81;')
            mel.eval('MGPickerItem -e -vis false selectButton111;')
            mel.eval('MGPickerItem -e -vis false selectButton258;')

            # FK
            mel.eval('MGPickerItem -e -vis true selectButton107;')
            mel.eval('MGPickerItem -e -vis true selectButton77;')
            mel.eval('MGPickerItem -e -vis true selectButton90;')
            mel.eval('MGPickerItem -e -vis true selectButton98;')

    else:
        fk2ik_match(ik_pos_ctrl=ik_pos_ctrl,
                    pos_match_loc=pos_match_loc,
                    ikpv_ctrl=ikpv_ctrl,
                    ikpv_match_loc=ikpv_match_loc,
                    ik_rot_ctrl=ik_rot_ctrl,
                    rot_match_jnt=jnts[3],
                    ikfk_switch=ikfk_switch,
                    match=match,
                    start=jnts[0],
                    mid=jnts[1],
                    end=jnts[2],
                    move=50,
                    loc_match=True)

        cmds.xform(roll_Toe_ctrl, t=[0,0,0], ro=[0,0,0], p=True, a=True) if match else False

        if picker:
            # IK
            mel.eval('MGPickerItem -e -vis true selectButton87;')
            mel.eval('MGPickerItem -e -vis true selectButton81;')
            mel.eval('MGPickerItem -e -vis true selectButton111;')
            mel.eval('MGPickerItem -e -vis true selectButton258;')

            # FK
            mel.eval('MGPickerItem -e -vis false selectButton107;')
            mel.eval('MGPickerItem -e -vis false selectButton77;')
            mel.eval('MGPickerItem -e -vis false selectButton90;')
            mel.eval('MGPickerItem -e -vis false selectButton98;')

    ctrls.append(ik_pos_ctrl)
    ctrls.append(ik_rot_ctrl)
    ctrls.append(ikpv_ctrl)
    ctrls.append(roll_Toe_ctrl)

    ctrls.append(ikfk_switch) if force_state_key else False

    return ctrls



def ikfk_foot_R(picker=None, match=None, force_state=None, force_state_key=None, namespace=None):
    ikfk_switch, state, jnts, ctrls, ik_pos_ctrl, ik_rot_ctrl, ikpv_ctrl, pos_match_loc, ikpv_match_loc, namespace = get_foot_L_ctrl_values(namespace)

    ikfk_switch = mirror_character(['_L', '_R'], ikfk_switch)
    ik_pos_ctrl = mirror_character(['_L', '_R'], ik_pos_ctrl)
    ik_rot_ctrl = mirror_character(['_L', '_R'], ik_rot_ctrl)
    ikpv_ctrl = mirror_character(['_L', '_R'], ikpv_ctrl)
    pos_match_loc = mirror_character(['_L', '_R'], pos_match_loc)
    ikpv_match_loc = mirror_character(['_L', '_R'], ikpv_match_loc)

    jnts = [mirror_character(['_L', '_R'], jnt) for jnt in jnts]
    ctrls = [mirror_character(['_L', '_R'], ctrl) for ctrl in ctrls]

    state = cmds.getAttr(ikfk_switch)

    roll_Toe_ctrl = namespace + 'roll_Toe_R_ctrl'

    if force_state:
        if force_state == 'ik2fk':
            state = 1
        elif force_state == 'fk2ik':
            state = 0
        cmds.setAttr(ikfk_switch, state)

        cmds.setKeyframe(ikfk_switch) if force_state_key else False

    if state == 1:
        ik2fk_match(ctrls=ctrls,
                    jnts=jnts,
                    ikfk_switch=ikfk_switch,
                    match=match)

        cmds.xform(roll_Toe_ctrl, t=[0,0,0], ro=[0,0,0], p=True, a=True) if match else False

        if picker:
            # IK
            mel.eval('MGPickerItem -e -vis false selectButton86;')
            mel.eval('MGPickerItem -e -vis false selectButton93;')
            mel.eval('MGPickerItem -e -vis false selectButton112;')
            mel.eval('MGPickerItem -e -vis false selectButton259;')

            # FK
            mel.eval('MGPickerItem -e -vis true selectButton92;')
            mel.eval('MGPickerItem -e -vis true selectButton114;')
            mel.eval('MGPickerItem -e -vis true selectButton106;')
            mel.eval('MGPickerItem -e -vis true selectButton108;')

    else:
        fk2ik_match(ik_pos_ctrl=ik_pos_ctrl,
                    pos_match_loc=pos_match_loc,
                    ikpv_ctrl=ikpv_ctrl,
                    ikpv_match_loc=ikpv_match_loc,
                    ik_rot_ctrl=ik_rot_ctrl,
                    rot_match_jnt=jnts[3],
                    ikfk_switch=ikfk_switch,
                    match=match,
                    start=jnts[0],
                    mid=jnts[1],
                    end=jnts[2],
                    move=50,
                    loc_match=True)

        cmds.xform(roll_Toe_ctrl, t=[0,0,0], ro=[0,0,0], p=True, a=True) if match else False

        if picker:
            # IK
            mel.eval('MGPickerItem -e -vis true selectButton86;')
            mel.eval('MGPickerItem -e -vis true selectButton93;')
            mel.eval('MGPickerItem -e -vis true selectButton112;')
            mel.eval('MGPickerItem -e -vis true selectButton259;')

            # FK
            mel.eval('MGPickerItem -e -vis false selectButton92;')
            mel.eval('MGPickerItem -e -vis false selectButton114;')
            mel.eval('MGPickerItem -e -vis false selectButton106;')
            mel.eval('MGPickerItem -e -vis false selectButton108;')


    ctrls.append(ik_pos_ctrl)
    ctrls.append(ik_rot_ctrl)
    ctrls.append(ikpv_ctrl)
    ctrls.append(roll_Toe_ctrl)

    ctrls.append(ikfk_switch) if force_state_key else False

    return ctrls


def add_ctrls_namespace(*args, **kwargs):
    ctrls = []
    added_namespaces = {}
    for key, value in kwargs.items():
        if key == 'namespace':
            namespace = value
        else:
            ctrls.append(value)
            added_namespaces[key] = value

    if 'namespace' in kwargs.keys():
        kwargs.pop('namespace')

    for key, value in kwargs.items():
        added_namespaces[key] = namespace + value

    return added_namespaces


def fullbake(sel=None):
    try:
        cmds.refresh(su=True)
        cmds.cycleCheck(e=False)

        playmin = cmds.playbackOptions(q=True, min=True)
        playmax = cmds.playbackOptions(q=True, max=True)

        if not sel:
            sel = cmds.ls(os=True)
        cmds.bakeResults(sel, sm=True, t=(playmin, playmax), sb=True, osr=True, dic=True, pok=True, sac=False, ral=False, rba=False, bol=False, mr=True, cp=False, s=False)

        cmds.filterCurve(sel, f='euler')

        cmds.refresh(su=False)
        cmds.cycleCheck(e=True)
    except:
        cmds.refresh(su=False)
        cmds.cycleCheck(e=True)


@bake_with_func
def ikfk_match_with_bake(hand_L=None, hand_L_ikfk=None, hand_R=None, hand_R_ikfk=None,
                         foot_L=None, foot_L_ikfk=None, foot_R=None, foot_R_ikfk=None,
                         force_state_key=None, namespace=None):

    hand_L_ctrls = ikfk_hand_L(picker=False, match=True, force_state=hand_L_ikfk, force_state_key=force_state_key, namespace=namespace) if hand_L else False
    hand_R_ctrls = ikfk_hand_R(picker=False, match=True, force_state=hand_R_ikfk, force_state_key=force_state_key, namespace=namespace) if hand_R else False
    foot_L_ctrls = ikfk_foot_L(picker=False, match=True, force_state=foot_L_ikfk, force_state_key=force_state_key, namespace=namespace) if foot_L else False
    foot_R_ctrls = ikfk_foot_R(picker=False, match=True, force_state=foot_R_ikfk, force_state_key=force_state_key, namespace=namespace) if foot_R else False

    cmds.setKeyframe(hand_L_ctrls) if hand_L_ctrls else False
    cmds.setKeyframe(hand_R_ctrls) if hand_R_ctrls else False
    cmds.setKeyframe(foot_L_ctrls) if foot_L_ctrls else False
    cmds.setKeyframe(foot_R_ctrls) if foot_R_ctrls else False

@bake_with_func_for_timeSlider
def ikfk_match_with_bake_for_timeSlider(hand_L=None, hand_L_ikfk=None, hand_R=None, hand_R_ikfk=None,
                         foot_L=None, foot_L_ikfk=None, foot_R=None, foot_R_ikfk=None,
                         force_state_key=None, namespace=None):

    hand_L_ctrls = ikfk_hand_L(picker=False, match=True, force_state=hand_L_ikfk, force_state_key=force_state_key, namespace=namespace) if hand_L else False
    hand_R_ctrls = ikfk_hand_R(picker=False, match=True, force_state=hand_R_ikfk, force_state_key=force_state_key, namespace=namespace) if hand_R else False
    foot_L_ctrls = ikfk_foot_L(picker=False, match=True, force_state=foot_L_ikfk, force_state_key=force_state_key, namespace=namespace) if foot_L else False
    foot_R_ctrls = ikfk_foot_R(picker=False, match=True, force_state=foot_R_ikfk, force_state_key=force_state_key, namespace=namespace) if foot_R else False

    cmds.setKeyframe(hand_L_ctrls) if hand_L_ctrls else False
    cmds.setKeyframe(hand_R_ctrls) if hand_R_ctrls else False
    cmds.setKeyframe(foot_L_ctrls) if foot_L_ctrls else False
    cmds.setKeyframe(foot_R_ctrls) if foot_R_ctrls else False

@bake_with_func_for_timeSlider
def fk2ik_ik2fk_matchbake(force_state_key=None, namespace='<from_picker>'):
    force_state_key=force_state_key

    # fk2ik
    hand_L=True
    hand_L_ikfk='fk2ik'

    hand_R=True
    hand_R_ikfk='fk2ik'

    foot_L=True
    foot_L_ikfk='fk2ik'

    foot_R=True
    foot_R_ikfk='fk2ik'

    hand_L_ctrls = ikfk_hand_L(picker=False, match=True, force_state=hand_L_ikfk, force_state_key=force_state_key, namespace=namespace) if hand_L else False
    hand_R_ctrls = ikfk_hand_R(picker=False, match=True, force_state=hand_R_ikfk, force_state_key=force_state_key, namespace=namespace) if hand_R else False
    foot_L_ctrls = ikfk_foot_L(picker=False, match=True, force_state=foot_L_ikfk, force_state_key=force_state_key, namespace=namespace) if foot_L else False
    foot_R_ctrls = ikfk_foot_R(picker=False, match=True, force_state=foot_R_ikfk, force_state_key=force_state_key, namespace=namespace) if foot_R else False

    cmds.setKeyframe(hand_L_ctrls) if hand_L_ctrls else False
    cmds.setKeyframe(hand_R_ctrls) if hand_R_ctrls else False
    cmds.setKeyframe(foot_L_ctrls) if foot_L_ctrls else False
    cmds.setKeyframe(foot_R_ctrls) if foot_R_ctrls else False

    # ik2fk
    hand_L=True
    hand_L_ikfk='ik2fk'

    hand_R=True
    hand_R_ikfk='ik2fk'

    foot_L=True
    foot_L_ikfk='ik2fk'

    foot_R=True
    foot_R_ikfk='ik2fk'

    hand_L_ctrls = ikfk_hand_L(picker=False, match=True, force_state=hand_L_ikfk, force_state_key=force_state_key, namespace=namespace) if hand_L else False
    hand_R_ctrls = ikfk_hand_R(picker=False, match=True, force_state=hand_R_ikfk, force_state_key=force_state_key, namespace=namespace) if hand_R else False
    foot_L_ctrls = ikfk_foot_L(picker=False, match=True, force_state=foot_L_ikfk, force_state_key=force_state_key, namespace=namespace) if foot_L else False
    foot_R_ctrls = ikfk_foot_R(picker=False, match=True, force_state=foot_R_ikfk, force_state_key=force_state_key, namespace=namespace) if foot_R else False

    cmds.setKeyframe(hand_L_ctrls) if hand_L_ctrls else False
    cmds.setKeyframe(hand_R_ctrls) if hand_R_ctrls else False
    cmds.setKeyframe(foot_L_ctrls) if foot_L_ctrls else False
    cmds.setKeyframe(foot_R_ctrls) if foot_R_ctrls else False

@bake_with_func_for_timeSlider
def ik2fk_fk2ik_matchbake(force_state_key=None, namespace='<from_picker>'):
    force_state_key=force_state_key

    # ik2fk
    hand_L=True
    hand_L_ikfk='ik2fk'

    hand_R=True
    hand_R_ikfk='ik2fk'

    foot_L=True
    foot_L_ikfk='ik2fk'

    foot_R=True
    foot_R_ikfk='ik2fk'

    hand_L_ctrls = ikfk_hand_L(picker=False, match=True, force_state=hand_L_ikfk, force_state_key=force_state_key, namespace=namespace) if hand_L else False
    hand_R_ctrls = ikfk_hand_R(picker=False, match=True, force_state=hand_R_ikfk, force_state_key=force_state_key, namespace=namespace) if hand_R else False
    foot_L_ctrls = ikfk_foot_L(picker=False, match=True, force_state=foot_L_ikfk, force_state_key=force_state_key, namespace=namespace) if foot_L else False
    foot_R_ctrls = ikfk_foot_R(picker=False, match=True, force_state=foot_R_ikfk, force_state_key=force_state_key, namespace=namespace) if foot_R else False

    cmds.setKeyframe(hand_L_ctrls) if hand_L_ctrls else False
    cmds.setKeyframe(hand_R_ctrls) if hand_R_ctrls else False
    cmds.setKeyframe(foot_L_ctrls) if foot_L_ctrls else False
    cmds.setKeyframe(foot_R_ctrls) if foot_R_ctrls else False

    # fk2ik
    hand_L=True
    hand_L_ikfk='fk2ik'

    hand_R=True
    hand_R_ikfk='fk2ik'

    foot_L=True
    foot_L_ikfk='fk2ik'

    foot_R=True
    foot_R_ikfk='fk2ik'

    hand_L_ctrls = ikfk_hand_L(picker=False, match=True, force_state=hand_L_ikfk, force_state_key=force_state_key, namespace=namespace) if hand_L else False
    hand_R_ctrls = ikfk_hand_R(picker=False, match=True, force_state=hand_R_ikfk, force_state_key=force_state_key, namespace=namespace) if hand_R else False
    foot_L_ctrls = ikfk_foot_L(picker=False, match=True, force_state=foot_L_ikfk, force_state_key=force_state_key, namespace=namespace) if foot_L else False
    foot_R_ctrls = ikfk_foot_R(picker=False, match=True, force_state=foot_R_ikfk, force_state_key=force_state_key, namespace=namespace) if foot_R else False

    cmds.setKeyframe(hand_L_ctrls) if hand_L_ctrls else False
    cmds.setKeyframe(hand_R_ctrls) if hand_R_ctrls else False
    cmds.setKeyframe(foot_L_ctrls) if foot_L_ctrls else False
    cmds.setKeyframe(foot_R_ctrls) if foot_R_ctrls else False

@bake_with_func_for_timeSlider
def space_match_bake(ctrls=None,
                     space_match=None,
                     space_attr=None,
                     set_space=None,
                     auto_rot_match=None,
                     auto_rot_attr=None,
                     auto_rot_force_set=None):

    ctrls = order_dags(ctrls)

    namespace = get_mgpickernamespace()

    rot_ctrls = {
        namespace + 'ik_Wrist_L_ctrl':namespace + 'ik_rot_Wrist_L_ctrl',
        namespace + 'ik_Wrist_R_ctrl':namespace + 'ik_rot_Wrist_R_ctrl',
    }

    if space_match:
        for ctrl in ctrls:
            if ctrl in rot_ctrls.keys():
                set_enum_attr(ctrl=ctrl, attr=space_attr, val=set_space, rot_ctrl=rot_ctrls[ctrl])
            else:
                set_enum_attr(ctrl=ctrl, attr=space_attr, val=set_space)

        cmds.setKeyframe(ctrls)

    elif auto_rot_match:
        if len(auto_rot_attr) == 2 and type(auto_rot_attr) == list:
            for j, artr in enumerate(auto_rot_attr):
                for autorot_ctrls in ctrls:
                    match_autorot_ctrl(ctrl=autorot_ctrls[0], set_ctrl_and_attr=artr, force_set=auto_rot_force_set)
                    cmds.setKeyframe(autorot_ctrls)
        else:
            [match_autorot_ctrl(ctrl=ctrl, set_ctrl_and_attr=auto_rot_attr, force_set=auto_rot_force_set) for ctrl in ctrls]

            cmds.setKeyframe(ctrls)

def set_enum_attr(ctrl=None, attr=None, val=None, rot_ctrl=None):
    wt = cmds.xform(ctrl, q=True, t=True, ws=True)
    if rot_ctrl:
        wr = cmds.xform(rot_ctrl, q=True, ro=True, ws=True)
    else:
        wr = cmds.xform(ctrl, q=True, ro=True, ws=True)

    list_attrs = cmds.listAttr(ctrl, ud=True, k=True) or list()

    if attr in list_attrs:
        get_en_attrs = cmds.addAttr(ctrl + '.' + attr, q=True, en=True)
        spl_get_en_attrs = get_en_attrs.split(':')
        if val in spl_get_en_attrs:
            enum_idx = spl_get_en_attrs.index(val)
            cmds.setAttr(ctrl+'.'+attr, enum_idx)

        cmds.xform(ctrl, t=wt, ro=wr, ws=True, a=True, p=True)
        if rot_ctrl:
            cmds.xform(rot_ctrl, ro=wr, ws=True, a=True, p=True)

def space_match(attr=None, val=None, rot_ctrl=None):
    parentButton = cmds.MGPicker(q=True, currentItem=True)
    members = cmds.MGPickerItem(parentButton, q=True, selectMembers=True)
    currentPickerNamespace = get_mgpickernamespace()
    members = [currentPickerNamespace + mem for mem in members]
    if rot_ctrl:
        rot_ctrl = currentPickerNamespace + rot_ctrl
    [set_enum_attr(ctrl=ctrl, attr=attr, val=val, rot_ctrl=rot_ctrl) for ctrl in members]

def match_autorot_ctrl(ctrl=None, set_ctrl_and_attr='autoRot', force_set=None):

    wt = cmds.xform(ctrl, q=True, t=True, ws=True)
    wr =cmds.xform(ctrl, q=True, ro=True, ws=1)

    if force_set:
        if force_set == 'on':
            cmds.setAttr(set_ctrl_and_attr, 1)
        elif force_set == 'off':
            cmds.setAttr(set_ctrl_and_attr, 0)

    else:
        if cmds.getAttr(set_ctrl_and_attr):
            cmds.setAttr(set_ctrl_and_attr, 0)
        else:
            cmds.setAttr(set_ctrl_and_attr, 1)

    cmds.xform(ctrl, t=wt, ws=True, a=True, p=True)
    cmds.xform(ctrl, ro=wr, ws=True, a=True, p=True)

@bake_with_func_for_timeSlider
def ik_autorot_match_bake(ik_autorot_dict=None):
    if ik_autorot_dict:
        for ctrl, ik_auto in ik_autorot_dict.items():
            attr = ik_auto['attr']
            force_set = ik_auto['force_set']
            match_autorot_ctrl(ctrl=ctrl, set_ctrl_and_attr=attr, force_set=force_set)
            cmds.setKeyframe([ctrl, attr.split('.')[0]])

@bake_with_func_for_timeSlider
def foot_roll_match_bake(side=['_L_', '_R_'], main_to_foot=None, namespace=None):
    [match_foot_roll(setkey=True, side=s, main_to_foot=main_to_foot, namespace=namespace) for s in side]

def cog_hip_matchbake(bake_to=None, namespace=None):
    if not namespace:
        namespace = get_mgpickernamespace()
    ctrls = add_ctrls_namespace(namespace = namespace,
                             cog_ctrl = 'Cog_ctrl',
                             hip_ctrl = 'Hip_ctrl',
                             spine_ctrl = 'Spine1_ctrl',
                             hip_jnt = 'Hip_ctrl_con')


    cog_ctrl = ctrls['cog_ctrl']
    hip_ctrl = ctrls['hip_ctrl']
    spine_ctrl = ctrls['spine_ctrl']

    hip_jnt = ctrls['hip_jnt']

    cog_hip_match_sets = 'cog_hip_match_sets'
    cmds.sets(em=True, n=cog_hip_match_sets) if not cmds.objExists(cog_hip_match_sets) else False

    cog_match_loc_p = cmds.spaceLocator()[0]
    cog_match_loc = cmds.spaceLocator()[0]
    cmds.parent(cog_match_loc, cog_match_loc_p)

    hip_match_loc_p = cmds.spaceLocator()[0]
    hip_match_loc = cmds.spaceLocator()[0]
    cmds.parent(hip_match_loc, hip_match_loc_p)

    spine_match_loc_p = cmds.spaceLocator()[0]
    spine_match_loc = cmds.spaceLocator()[0]
    cmds.parent(spine_match_loc, spine_match_loc_p)

    cmds.matchTransform(cog_match_loc_p, cog_ctrl)
    cmds.matchTransform(hip_match_loc_p, hip_ctrl)
    cmds.matchTransform(spine_match_loc_p, spine_ctrl)

    spine_cog_match_loc_p = cmds.spaceLocator()[0]
    spine_cog_match_loc = cmds.spaceLocator()[0]
    cmds.parent(spine_cog_match_loc, spine_cog_match_loc_p)
    cmds.parentConstraint(spine_ctrl, spine_cog_match_loc_p, w=True, mo=False)
    cmds.sets(spine_cog_match_loc_p, add=cog_hip_match_sets)

    ########
    # Cog > Hip
    ########
    if bake_to == 'hip':
        cmds.parent(hip_match_loc_p, cog_match_loc)
        cmds.parent(spine_match_loc_p, hip_match_loc)

        cmds.sets(cog_match_loc_p, add=cog_hip_match_sets)

        cmds.parentConstraint(cog_ctrl, cog_match_loc_p, w=True, mo=True)
        cmds.parentConstraint(spine_ctrl, spine_match_loc_p, w=True, mo=True)
        fullbake([cog_match_loc_p, spine_match_loc_p])
        cmds.parentConstraint(hip_match_loc, hip_ctrl, st=['x', 'y', 'z'], w=True, mo=True)
        set_zero(sel=[cog_ctrl], xform_set={'ro':[0,0,0], 'a':True})

        fullbake([spine_cog_match_loc_p])
        cmds.pointConstraint(spine_cog_match_loc_p, cog_ctrl, w=True, mo=True)
        cmds.pointConstraint(spine_match_loc_p, spine_cog_match_loc_p, w=True, mo=False)
        ori = cmds.orientConstraint(spine_match_loc_p, spine_ctrl, w=True, mo=False)
        cmds.setAttr('{}.interpType'.format(ori[0]), 2)

    ########
    # Hip > Cog
    ########
    if bake_to == 'cog':
        cmds.parent(cog_match_loc_p, hip_match_loc)
        cmds.parent(spine_match_loc_p, cog_match_loc)

        cmds.sets(hip_match_loc_p, add=cog_hip_match_sets)

        cmds.parentConstraint(hip_jnt, cog_match_loc_p, w=True, mo=False)
        cmds.parentConstraint(hip_ctrl, hip_match_loc_p, w=True, mo=False)
        cmds.parentConstraint(spine_ctrl, spine_match_loc_p, w=True, mo=False)
        fullbake([cog_match_loc_p, hip_match_loc_p, spine_match_loc_p])
        cmds.parentConstraint(cog_match_loc, cog_ctrl, w=True, mo=False)
        set_zero(sel=[hip_ctrl], xform_set={'ro':[0,0,0], 'a':True})
        ori = cmds.orientConstraint(spine_match_loc_p, spine_ctrl, w=True, mo=False)
        cmds.setAttr('{}.interpType'.format(ori[0]), 2)


    fullbake([cog_ctrl, hip_ctrl, spine_ctrl])
    cmds.select(cog_hip_match_sets, r=True, ne=True)
    bake_objs = cmds.pickWalk(d='down')
    cmds.delete(bake_objs)

@bake_with_func
def correctkeys(objects=None):
    [quaternionToEuler(obj=obj) for obj in objects] if objects else False

@bake_with_func
def set_zero(sel=None, xform_set=None):
    [cmds.xform(obj, **xform_set) for obj in sel] if sel else False
    cmds.setKeyframe(sel)

def quaternionToEuler(obj=None):
    rot = cmds.xform(obj, q=True, ro=True, os=True)
    rotOrder = cmds.getAttr('{}.rotateOrder'.format(obj))
    euler = om2.MEulerRotation(math.radians(rot[0]), math.radians(rot[1]), math.radians(rot[2]), rotOrder)
    quat = euler.asQuaternion()
    euler = quat.asEulerRotation()
    r = euler.reorder(rotOrder)

    cmds.xform(obj, ro=[math.degrees(r.x), math.degrees(r.y), math.degrees(r.z)], os=True, a=True)

    cmds.setKeyframe(obj, at='rotate')

    return math.degrees(r.x), math.degrees(r.y), math.degrees(r.z)

def quaternionToEuler_no_key(obj=None):
    rot = cmds.xform(obj, q=True, ro=True, os=True)
    rotOrder = cmds.getAttr('{}.rotateOrder'.format(obj))
    euler = om2.MEulerRotation(math.radians(rot[0]), math.radians(rot[1]), math.radians(rot[2]), rotOrder)
    quat = euler.asQuaternion()
    euler = quat.asEulerRotation()
    r = euler.reorder(rotOrder)

    cmds.xform(obj, ro=[math.degrees(r.x), math.degrees(r.y), math.degrees(r.z)], os=True, a=True)

    return math.degrees(r.x), math.degrees(r.y), math.degrees(r.z)

def order_dags(dags=None):
    parent_dag = cmds.ls(dags[0], l=1, type='transform')[0].split('|')[1]

    all_hir = cmds.listRelatives(parent_dag, ad=True, f=True)
    hir_split_counter = {}
    for fp_node in all_hir:
        hir_split_counter[fp_node] = len(fp_node.split('|'))

    hir_split_counter_sorted = sorted(hir_split_counter.items(), key=lambda x:x[1])

    sorted_joint_list = [dag_count[0] for dag_count in hir_split_counter_sorted]

    all_ordered_dags = cmds.ls(sorted_joint_list)
    return [dag for dag in all_ordered_dags if dag in dags]

def go_to_bindPose_for_rig(namespace=None):
    if not namespace:
        namespace = get_mgpickernamespace()

    cmds.select(namespace + 'ctrl_sets', r=True, ne=True)
    ctrls = cmds.pickWalk(d='down')

    ctrls = order_dags(ctrls)

    for ctrl in ctrls:
        bt = cmds.getAttr(ctrl + '.bindPoseTranslate')[0]
        br = cmds.getAttr(ctrl + '.bindPoseRotate')[0]
        cmds.xform(ctrl, t=bt, ro=br, ws=True, p=True, a=True)


def get_world_values(obj=None):
    wt = cmds.xform(obj, q=True, t=True, ws=True)
    wr = cmds.xform(obj, q=True, ro=True, ws=True)
    wt_at = obj + '.t'
    wr_at = obj + '.r'
    return {wt_at:wt, wr_at:wr}

def get_ud_values(obj=None):
    ud_attrs = OrderedDict()
    list_attrs = cmds.listAttr(obj, k=True, ud=True)
    if list_attrs:
        for at in list_attrs:
            obj_at = obj + '.' + at
            ud_attrs[obj_at] = cmds.getAttr(obj_at)
    return ud_attrs

def get_values(obj=None):
    w_pos_rot = get_world_values(obj)
    ud_attrs = get_ud_values(obj)
    return w_pos_rot, ud_attrs


@bake_with_func
def get_values_per_frame(ctrl_values=None, ctrls=None):
    frame = cmds.currentTime(q=True)
    ctrl_values[frame] = OrderedDict()
    for ctrl in ctrls:
        ctrl_values[frame][ctrl] = get_values(ctrl)

def merge_ctrl_values(merge_ctrl_dict=None, namespace=None):
    ctrls = [
        'world_ctrl',
        'main_ctrl',
        'Root_ctrl',
        'ik_Ankle_L_ctrl',
        'ik_Ankle_R_ctrl',
        'ik_Elbow_L_ctrl',
        'ik_Elbow_R_ctrl',
        'ik_Knee_L_ctrl',
        'ik_Knee_R_ctrl',
        'ik_Wrist_L_ctrl',
        'ik_Wrist_R_ctrl',
        'Cog_ctrl',
        'roll_main_Ankle_L_ctrl',
        'roll_main_Ankle_R_ctrl',
        'ik_rot_Ankle_L_ctrl',
        'ik_rot_Ankle_R_ctrl',
        'ik_rot_Wrist_L_ctrl',
        'ik_rot_Wrist_R_ctrl',
        'Hip_ctrl',
        'Spine1_ctrl',
        'roll_tippytoe_Ankle_L_ctrl',
        'roll_tippytoe_Ankle_R_ctrl',
        'ik_Toe_L_ctrl',
        'ik_Toe_R_ctrl',
        'Thigh_L_ctrl',
        'Thigh_R_ctrl',
        'Spine2_ctrl',
        'roll_heel_Ankle_L_ctrl',
        'roll_heel_Ankle_R_ctrl',
        'ikfk_Ankle_L_ctrl',
        'ikfk_Ankle_R_ctrl',
        'Knee_L_ctrl',
        'Knee_R_ctrl',
        'Spine3_ctrl',
        'roll_in_Ankle_L_ctrl',
        'roll_in_Ankle_R_ctrl',
        'Ankle_L_ctrl',
        'Ankle_R_ctrl',
        'Neck_ctrl',
        'Shoulder_L_ctrl',
        'Shoulder_R_ctrl',
        'roll_out_Ankle_L_ctrl',
        'roll_out_Ankle_R_ctrl',
        'Toe_L_ctrl',
        'Toe_R_ctrl',
        'Head_ctrl',
        'Arm_L_ctrl',
        'Arm_R_ctrl',
        'Thumb_01_L_ctrl',
        'Index_01_L_ctrl',
        'Middle_01_L_ctrl',
        'Ring_01_L_ctrl',
        'Pinky_01_L_ctrl',
        'HandattachOffset_L_ctrl',
        'ikfk_Wrist_L_ctrl',
        'Thumb_01_R_ctrl',
        'Index_01_R_ctrl',
        'Middle_01_R_ctrl',
        'Ring_01_R_ctrl',
        'Pinky_01_R_ctrl',
        'HandattachOffset_R_ctrl',
        'ikfk_Wrist_R_ctrl',
        'roll_Toe_L_ctrl',
        'roll_stoptoe_Toe_L_ctrl',
        'roll_Toe_R_ctrl',
        'roll_stoptoe_Toe_R_ctrl',
        'Elbow_L_ctrl',
        'Elbow_R_ctrl',
        'Thumb_02_L_ctrl',
        'Index_02_L_ctrl',
        'Middle_02_L_ctrl',
        'Ring_02_L_ctrl',
        'Pinky_02_L_ctrl',
        'Handattach_L_ctrl',
        'Thumb_02_R_ctrl',
        'Index_02_R_ctrl',
        'Middle_02_R_ctrl',
        'Ring_02_R_ctrl',
        'Pinky_02_R_ctrl',
        'Handattach_R_ctrl',
        'roll_Ankle_L_ctrl',
        'roll_Ankle_R_ctrl',
        'Wrist_L_ctrl',
        'Wrist_R_ctrl',
        'Thumb_03_L_ctrl',
        'Index_03_L_ctrl',
        'Middle_03_L_ctrl',
        'Ring_03_L_ctrl',
        'Pinky_03_L_ctrl',
        'Thumb_03_R_ctrl',
        'Index_03_R_ctrl',
        'Middle_03_R_ctrl',
        'Ring_03_R_ctrl',
        'Pinky_03_R_ctrl'
     ]

    ctrls = [namespace + ctrl for ctrl in ctrls]

    ctrl_values = OrderedDict()
    get_values_per_frame(ctrl_values=ctrl_values, ctrls=ctrls)

    for merge_da in merge_ctrl_dict:
        merge_src = merge_da['merge_src']
        merge_dst = merge_da['merge_dst']

        for frame, values in ctrl_values.items():
            src_w_val = ctrl_values[frame][merge_src][0]
            dst_w_val = ctrl_values[frame][merge_dst][0]

            src_w_val[merge_src + '.t'] = dst_w_val[merge_dst + '.t']
            src_w_val[merge_src + '.r'] = dst_w_val[merge_dst + '.r']


    for frame, values in ctrl_values.items():
        cmds.currentTime(frame, e=True)
        for ctrl, ctrl_at in values.items():
            ctrl_val = ctrl_at[0]
            wt_val = ctrl_val[ctrl + '.t']
            wr_val = ctrl_val[ctrl + '.r']
            cmds.xform(ctrl, t=wt_val, ro=wr_val, p=True, ws=True, a=True)
            cmds.setKeyframe(ctrl)

def get_animCurve(obj=None, attrs=None):
    settings = {
        'p':True,
        's':True,
        'type':'animCurve'
    }
    anim_curves_list = list()
    for at in attrs:
        anim_curves = cmds.listConnections('{}.{}'.format(obj, at), **settings) or None
        if anim_curves: anim_curves_list.append(anim_curves[0])

    return anim_curves_list


def fix_pos_anim(chr_joints=None, chr_nss=None):
    # 移動値を残すノード
    delete_pos_nodes = [
        'Root',
        'Hip',
        'Handattach_L',
        'Handattach_R'
    ]

    delete_pos_attrs = [
        'tx',
        'ty',
        'tz'
    ]

    # 回転のアニメーションを削除するノード
    delete_rot_nodes = [
        'HandattachOffset_L',
        'HandattachOffset_R'
    ]

    delete_rot_attrs = [
        'rx',
        'ry',
        'rz'
    ]

    # スケールのアニメーションを削除するノード
    delete_scl_nodes = [
        'HandattachOffset_L',
        'HandattachOffset_R'
    ]

    delete_scl_attrs = [
        'sx',
        'sy',
        'sz'
    ]

    chr_joints = [j for j in chr_joints if cmds.objExists(j)]

    for ch_j in chr_joints:
        if cmds.objectType(ch_j) == 'joint':
            if not ch_j in delete_pos_nodes:
                anim_curves = get_animCurve(obj=ch_j, attrs=delete_pos_attrs)
                [cmds.delete(ac.split('.')[0]) for ac in anim_curves]

                try:
                    cmds.setAttr(ch_j + '.t', *cmds.getAttr(chr_nss + ch_j + '.t')[0])
                except:
                    print(traceback.format_exc())

            if ch_j in delete_rot_nodes:
                anim_curves = get_animCurve(obj=ch_j, attrs=delete_rot_attrs)
                [cmds.delete(ac.split('.')[0]) for ac in anim_curves]

                try:
                    cmds.setAttr(ch_j + '.r', *cmds.getAttr(chr_nss + ch_j + '.r')[0])
                    # cmds.xform(ch_j, ro=cmds.xform(chr_nss + ch_j, q=True, ro=True, ws=True), ws=True, a=True)
                    quaternionToEuler_no_key(obj=ch_j)
                except:
                    print(traceback.format_exc())

            if ch_j in delete_scl_nodes:
                anim_curves = get_animCurve(obj=ch_j, attrs=delete_scl_attrs)
                [cmds.delete(ac.split('.')[0]) for ac in anim_curves]

                try:
                    cmds.setAttr(ch_j + '.s', *cmds.getAttr(chr_nss + ch_j + '.s')[0])
                except:
                    print(traceback.format_exc())

def fix_fbx_anim(namespace=None):
    if not namespace:
        namespace = get_mgpickernamespace()
    chr_nss = '{}:chr:'.format(namespace)

    chr_joints = ['Ankle_L',
     'Ankle_R',
     'ArmRoll_L',
     'ArmRoll_R',
     'Arm_L',
     'Arm_R',
     'Elbow_L',
     'Elbow_R',
     'HandattachOffset_L',
     'HandattachOffset_R',
     'Handattach_L',
     'Handattach_R',
     'Head',
     'Hip',
     'Index_01_L',
     'Index_01_R',
     'Index_02_L',
     'Index_02_R',
     'Index_03_L',
     'Index_03_R',
     'Knee_L',
     'Knee_R',
     'Middle_01_L',
     'Middle_01_R',
     'Middle_02_L',
     'Middle_02_R',
     'Middle_03_L',
     'Middle_03_R',
     'Neck',
     'Pinky_01_L',
     'Pinky_01_R',
     'Pinky_02_L',
     'Pinky_02_R',
     'Pinky_03_L',
     'Pinky_03_R',
     'Ring_01_L',
     'Ring_01_R',
     'Ring_02_L',
     'Ring_02_R',
     'Ring_03_L',
     'Ring_03_R',
     'Root',
     'Shoulder_L',
     'Shoulder_R',
     'Spine1',
     'Spine2',
     'Spine3',
     'Thigh_L',
     'Thigh_R',
     'Thumb_01_L',
     'Thumb_01_R',
     'Thumb_02_L',
     'Thumb_02_R',
     'Thumb_03_L',
     'Thumb_03_R',
     'Toe_L',
     'Toe_R',
     'WristRoll_L',
     'WristRoll_R',
     'Wrist_L',
     'Wrist_R']

    fix_pos_anim(chr_joints=chr_joints, chr_nss=chr_nss)

def merge_ctrl_values_per_frames(merge_ctrl_dict, namespace):
    try:
        cmds.refresh(su=1)

        cur_time=cmds.currentTime(q=1)
        if cmds.autoKeyframe(q=True, st=True):
            autoKeyState = True
        else:
            autoKeyState = False

        cmds.autoKeyframe(st=0)

        merge_ctrl_values(merge_ctrl_dict, namespace)

        cmds.currentTime(cur_time)
        cmds.autoKeyframe(state=autoKeyState)

        cmds.refresh(su=0)

    except:
        cmds.refresh(su=0)
        print(traceback.format_exc())

def before_bakes_hand(side=None, namespace=None, time_range=None):
    if not namespace:
        namespace = '<from_picker>'

    before_bakes = list()
    ikfk_switch, state, jnts, ctrls, ik_pos_ctrl, ik_rot_ctrl, ikpv_ctrl, pos_match_loc, ikpv_match_loc, namespace = get_hand_L_ctrl_values(namespace)

    # left append
    if 'left' == side or 'both' == side:
        before_bakes.append(ik_pos_ctrl)
        before_bakes.append(ik_rot_ctrl)
        before_bakes.append(ikpv_ctrl)
        [before_bakes.append(ctrl) for ctrl in ctrls]

    # right append
    if 'right' == side or 'both' == side:
        R_ik_pos_ctrl = mirror_character(['_L', '_R'], ik_pos_ctrl)
        R_ik_rot_ctrl = mirror_character(['_L', '_R'], ik_rot_ctrl)
        R_ikpv_ctrl = mirror_character(['_L', '_R'], ikpv_ctrl)
        R_ctrls = [mirror_character(['_L', '_R'], ctrl) for ctrl in ctrls]

        before_bakes.append(R_ik_pos_ctrl)
        before_bakes.append(R_ik_rot_ctrl)
        before_bakes.append(R_ikpv_ctrl)
        [before_bakes.append(r_ctrl) for r_ctrl in R_ctrls]

    # before bake
    fullbake(before_bakes)
    if 1 < time_range[1] - time_range[0]:
        select_time_slider_range(*time_range)

def before_bakes_foot(side=None, namespace=None, time_range=None):
    if not namespace:
        namespace = '<from_picker>'

    before_bakes = list()
    ikfk_switch, state, jnts, ctrls, ik_pos_ctrl, ik_rot_ctrl, ikpv_ctrl, pos_match_loc, ikpv_match_loc, namespace = get_foot_L_ctrl_values(namespace)

    # left append
    if 'left' == side or 'both' == side:
        before_bakes.append(ik_pos_ctrl)
        before_bakes.append(ik_rot_ctrl)
        before_bakes.append(ikpv_ctrl)
        [before_bakes.append(ctrl) for ctrl in ctrls]

        roll_Toe_L_ctrl = namespace + 'roll_Toe_L_ctrl'
        before_bakes.append(roll_Toe_L_ctrl)

    # right append
    if 'right' == side or 'both' == side:
        R_ik_pos_ctrl = mirror_character(['_L', '_R'], ik_pos_ctrl)
        R_ik_rot_ctrl = mirror_character(['_L', '_R'], ik_rot_ctrl)
        R_ikpv_ctrl = mirror_character(['_L', '_R'], ikpv_ctrl)
        R_ctrls = [mirror_character(['_L', '_R'], ctrl) for ctrl in ctrls]

        before_bakes.append(R_ik_pos_ctrl)
        before_bakes.append(R_ik_rot_ctrl)
        before_bakes.append(R_ikpv_ctrl)
        [before_bakes.append(r_ctrl) for r_ctrl in R_ctrls]

        roll_Toe_R_ctrl = namespace + 'roll_Toe_R_ctrl'
        before_bakes.append(roll_Toe_R_ctrl)

    # before bake
    fullbake(before_bakes)
    if 1 < time_range[1] - time_range[0]:
        select_time_slider_range(*time_range)

def select_time_slider_range(start, end):

    app = QApplication.instance()

    widgetStr = mel.eval('$gPlayBackSlider=$gPlayBackSlider')
    ptr = omui.MQtUtil.findControl(widgetStr)
    slider = wrapInstance(int(ptr), QWidget)

    slider_width = slider.size().width()
    slider_height = slider.size().height()

    # Store time slider settings
    min_time = cmds.playbackOptions(query=True, minTime=True)
    max_time = cmds.playbackOptions(query=True, maxTime=True)
    animation_start_time = cmds.playbackOptions(query=True, animationStartTime=True)
    animation_end_time = cmds.playbackOptions(query=True, animationEndTime=True)
    t = cmds.currentTime(query=True)

    # Set the time slider to the range we want so we have
    # perfect precision to click at the start and end of the
    # time slider.
    cmds.playbackOptions(minTime=start)
    cmds.playbackOptions(maxTime=end-1)

    a_pos = QPoint(0, slider_height / 2.0)
    b_pos = QPoint(slider_width, slider_height / 2.0)

    # Trigger some mouse events on the Time Control
    # Somehow we need to have some move events around
    # it so the UI correctly understands it stopped
    # clicking, etc.
    event = QMouseEvent(QEvent.MouseMove,
                              a_pos,
                              Qt.MouseButton.LeftButton,
                              Qt.MouseButton.LeftButton,
                              Qt.NoModifier)
    app.sendEvent(slider, event)

    event = QMouseEvent(QEvent.MouseButtonPress,
                              a_pos,
                              Qt.MouseButton.LeftButton,
                              Qt.MouseButton.LeftButton,
                              Qt.ShiftModifier)
    app.sendEvent(slider, event)

    event = QMouseEvent(QEvent.MouseMove,
                              b_pos,
                              Qt.MouseButton.LeftButton,
                              Qt.MouseButton.LeftButton,
                              Qt.ShiftModifier)
    app.sendEvent(slider, event)

    event = QMouseEvent(QEvent.MouseButtonRelease,
                              b_pos,
                              Qt.MouseButton.LeftButton,
                              Qt.MouseButton.LeftButton,
                              Qt.ShiftModifier)
    app.sendEvent(slider, event)

    event = QMouseEvent(QEvent.MouseMove,
                              b_pos,
                              Qt.MouseButton.LeftButton,
                              Qt.MouseButton.LeftButton,
                              Qt.NoModifier)
    app.sendEvent(slider, event)
    app.processEvents()

    # Reset time slider settings
    cmds.playbackOptions(minTime=min_time)
    cmds.playbackOptions(maxTime=max_time)
    cmds.playbackOptions(animationStartTime=animation_start_time)
    cmds.playbackOptions(animationEndTime=animation_end_time)
    cmds.currentTime(t)
