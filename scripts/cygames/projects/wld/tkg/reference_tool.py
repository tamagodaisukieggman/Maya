# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel

import codecs
from collections import OrderedDict
from datetime import datetime
from functools import partial
import getpass
import json
import os
import re
import subprocess
import traceback
import pdb

class UI(object):
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
                            pass


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
            pass


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
            pass


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


if __name__ == '__main__':
    ui = UI()
    ui.show()
