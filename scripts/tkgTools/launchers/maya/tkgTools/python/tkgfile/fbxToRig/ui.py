# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel

import codecs
from collections import OrderedDict
import csv
import datetime
import fnmatch
from functools import partial
import getpass
from imp import reload
import json
import os
import re
import shutil
import subprocess
import traceback
import pdb

import tkgfile.fbxToRig.commands as fbxToRig
reload(fbxToRig)

"""
from imp import reload
import tkgfile.fbxToRig.ui as fbxToRig_UI
reload(fbxToRig_UI)
ftr = fbxToRig_UI.FbxToRigWindow()
ftr.show()
"""

prj_id = 'wizard2'
version = '1.0.0'
window_title = 'FBX to Rig'

class FbxToRigWindow():
    def __init__(self):
        self.window_title = window_title
        self.prj_id = prj_id
        self.version = version

        self.main_window = '{} : {} : {}'.format(self.window_title, self.prj_id, self.version)
        spl_win = '_'.join(self.window_title.split(' '))
        self.optionVar_key = '{}'.format(spl_win)

        self.module_dir_path = '/'.join(__file__.replace('\\', '/').split('/')[0:-1])

        self.settings_json = self.module_dir_path + '/settings.json'
        self.settings = None
        self.rig = list()
        try:
            self.settings = json_transfer(file_name=self.settings_json, operation='import')
            self.rig = [rig for rig in self.settings['rig']['id'].keys()]
        except:
            print(traceback.format_exc())

        self.user = os.getenv('USER')
        self.maya_path = 'C:/Users/{}/Documents/maya'.format(self.user)
        self.dir_path = self.maya_path + '/' + self.optionVar_key
        os.makedirs(self.dir_path) if not os.path.isdir(self.dir_path) else None

        self.dir_bookmark = self.dir_path + '/bookmarks'
        self.dir_log = self.dir_path + '/log'
        self.dir_cur = self.dir_path + '/current'
        self.dir_bookmark_old = self.dir_bookmark + '/old'

        make_dirs = [
            self.dir_bookmark,
            self.dir_log,
            self.dir_cur,
            self.dir_bookmark_old
        ]
        [os.makedirs(m_dir) for m_dir in make_dirs if not os.path.isdir(m_dir)]


        self.bookmarks_json = self.dir_path + '/bookmarks.json'
        self.current_csv = self.dir_path + '/current.csv'

        self.fbx_files_key = 'fbx_files'
        self.bookmark_files_key = 'bookmark_files'
        self.change_fbx_name_key = 'change_fbx_name'
        self.savepath_key = 'savepath'

        self.cur_bookmarks = OrderedDict()
        self.select_fbx_item_indices = None
        self.cur_bookmark_name = None
        self.fbx_view_cbx_val = False
        self.cur_savepath = None

        self.save_items = {}

        self.log_data = OrderedDict()


    def show(self):
        if cmds.workspaceControl(self.main_window, q=1, ex=1):
            cmds.deleteUI(self.main_window)

        self.win = cmds.workspaceControl(self.main_window, l=self.main_window)

        self.layout()
        self.layout_edit()
        self.load_settings()

        self.reload_fbx_list()
        self.reload_bookmark_list()
        self.reload_savepath()

        cmds.showWindow(self.win)

    def layout(self):
        # menu
        menuBarLayout = cmds.menuBarLayout(p=self.win)
        cmds.menu(label='Edit', to=True)
        self.save_setting_menu = cmds.menuItem(label='Save Settings')
        # cmds.menuItem(label='Reset Settings', c=self.reset_settings)
        self.load_setting_menu = cmds.menuItem(label='Load Settings')
        cmds.menuItem(d=1)
        self.reload_setting_menu = cmds.menuItem(label='Reload')
        cmds.menuItem(label='ReferenceEditor', c='cmds.ReferenceEditor()')
        self.presets_menuitems = cmds.menuItem(label='Presets', sm=True)
        self.delete_preset_menuitem = cmds.menuItem(label='Delete Current Preset')
        cmds.menuItem(d=True)
        cmds.setParent('..', menu=True)
        self.history_menuitems = cmds.menuItem(label='History', sm=True)

        # main
        self.main_rowcol_lay = cmds.rowColumnLayout(adj=1, p=self.win)
        self.main_pane_lay = cmds.paneLayout(cn='vertical3', p=self.main_rowcol_lay)

        # left
        self.main_col_L_lay = cmds.rowColumnLayout(adj=1, nr=4, rat=[(1, 'both', 26)], p=self.main_pane_lay)
        self.bookmark_btn = cmds.button(l='Add Bookmark', p=self.main_col_L_lay)
        self.bookmark_tsl = cmds.textScrollList(p=self.main_col_L_lay, ams=True)
        self.bookmark_pop = cmds.popupMenu(p=self.bookmark_tsl)

        # center
        self.main_col_C_lay = cmds.rowColumnLayout(adj=1, nr=4, rat=[(2, 'both', 12)], p=self.main_pane_lay)
        self.savepath_tfbg = cmds.textFieldButtonGrp(l='Save Path', bl='SET', ad3=2, cw=[(1, 50), (2, 30)], cat=[(1, 'left', 0), (2, 'left', 0)], p=self.main_col_C_lay)
        self.main_col_C_row_lay = cmds.rowColumnLayout(nc=6,
                                                       cat=[
                                                        (1, 'left', 10),
                                                        (2, 'left', 10),
                                                        (3, 'left', 10),
                                                        (4, 'both', 10),
                                                        (5, 'left', 0),
                                                        (6, 'left', 0)
                                                        ],
                                                       adj=4,
                                                       p=self.main_col_C_lay)
        cmds.text(l='FBX:', p=self.main_col_C_row_lay)
        self.add_fbx_btn = cmds.button(l='ADD', p=self.main_col_C_row_lay)
        self.fbx_view_cbx = cmds.checkBox(l='FileName', p=self.main_col_C_row_lay)
        cmds.text(l='-'*10+'>', p=self.main_col_C_row_lay)
        self.rig_ops_menu = cmds.optionMenu(l='Rig', p=self.main_col_C_row_lay)

        self.fbx_tsl = cmds.textScrollList(p=self.main_col_C_lay, ams=True)
        self.fbx_pop = cmds.popupMenu(p=self.fbx_tsl)

        self.apply_row_lay = cmds.rowColumnLayout(nc=2, adj=1, p=self.main_rowcol_lay)

        self.apply_btn = cmds.button(l='Apply', p=self.apply_row_lay)

    def layout_edit(self):
        ##############
        # Bookmark
        ##############
        bookmark_pop_items = [
            {
                'l':'Delete Bookmark',
                'c':partial(self.remove_bookmark_from_list)
            },

        ]
        self.add_menuItems(parent=self.bookmark_pop, items=bookmark_pop_items)

        cmds.button(self.bookmark_btn, e=True, c=partial(self.add_bookmark))

        cmds.textScrollList(self.bookmark_tsl, e=True, sc=partial(self.selected_items_in_bookmark_list))

        ##############
        # FBX
        ##############
        cmds.textFieldButtonGrp(self.savepath_tfbg, e=True, bc=partial(self.set_savepath))

        cmds.checkBox(self.fbx_view_cbx, e=True, cc=partial(self.reload_fbx_list))
        if self.fbx_view_cbx_val:
            cmds.checkBox(self.fbx_view_cbx, e=True, v=self.fbx_view_cbx_val)

        rig_items = [{'l':rig} for rig in self.rig]
        self.add_menuItems(parent=self.rig_ops_menu, items=rig_items)

        fbx_pop_items = [
            {
                'l':'Delete Items',
                'c':partial(self.remove_fbx_from_list)
            },
            {
                'l':'Show in Explorer',
                'c':partial(self.show_in_explorer_from_selection, self.fbx_tsl, 'textScrollList')
            },

        ]
        self.add_menuItems(parent=self.fbx_pop, items=fbx_pop_items)

        cmds.button(self.add_fbx_btn, e=True, c=partial(self.add_fbx))

        cmds.textScrollList(self.fbx_tsl, e=True, sc=partial(self.selected_items_in_fbx_list))

        ##############
        # Apply
        ##############
        cmds.button(self.apply_btn, e=True, c=partial(self.apply_))

    def import_csv_files(self, csvs=None):
        values = []
        for cur_b in csvs:
            cur_b = cur_b.replace('\\', '/')
            values.append(csv_transfer(file_name=cur_b, operation='import', append_list=None))

        return values

    def load_settings(self, *args, **kwargs):
        get_load_values = load_optionVar(key=self.optionVar_key)

        if get_load_values:
            self.save_items[self.optionVar_key] = get_load_values

        elif type(self.save_items) == dict:
            if not self.optionVar_key in self.save_items.keys():
                self.save_items[self.optionVar_key] = {}

        # import current csv
        try:
            self.cur_fbx_files = csv_transfer(file_name=self.current_csv, operation='import', append_list=None)
            self.save_items[self.optionVar_key][self.fbx_files_key] = self.cur_fbx_files
        except:
            print(traceback.format_exc())
            if self.fbx_files_key in self.save_items[self.optionVar_key].keys():
                self.cur_fbx_files = self.save_items[self.optionVar_key][self.fbx_files_key]
            else:
                self.cur_fbx_files = list()

        cur_bookmark_files = find_files(self.dir_bookmark, '*.csv', 'old')
        self.cur_bookmark_files = [cbf for cbf in cur_bookmark_files]
        # print('self.cur_bookmark_files', self.cur_bookmark_files)
        if self.cur_bookmark_files:
            imported_values = self.import_csv_files(csvs=self.cur_bookmark_files)
            for cur_b, values in zip(self.cur_bookmark_files, imported_values):
                cur_b = cur_b.replace('\\', '/')
                cur_b_name = os.path.basename(cur_b)
                self.cur_bookmarks[cur_b_name.split('.csv')[0]] = values

        # change fbx file name
        if self.change_fbx_name_key in self.save_items[self.optionVar_key].keys():
            self.fbx_view_cbx_val = self.save_items[self.optionVar_key][self.change_fbx_name_key]
        else:
            self.save_items[self.optionVar_key][self.change_fbx_name_key] = self.fbx_view_cbx_val

        # savepath
        if self.savepath_key in self.save_items[self.optionVar_key].keys():
            self.cur_savepath = self.save_items[self.optionVar_key][self.savepath_key]
        else:
            self.save_items[self.optionVar_key][self.savepath_key] = self.cur_savepath


    def save_settings(self, *args, **kwargs):
        # fbx file name in list
        self.save_items[self.optionVar_key][self.change_fbx_name_key] = self.fbx_view_cbx_val

        # fbx files
        self.save_items[self.optionVar_key][self.fbx_files_key] = self.cur_fbx_files

        save_optionVar(save_items=self.save_items)

        # export current csv
        try:
            csv_transfer(file_name=self.current_csv, operation='export', append_list=self.cur_fbx_files)
        except:
            print(traceback.format_exc())

        self.update_bookmarks()

    def delete_settings(self, *args, **kwargs):
        cmds.optionVar(rm=self.optionVar_key)

    # def load_save_settings(self, func=None):
    #     def wrapper(*args, **kwargs):
    #         self.load_settings()
    #         func(*args, **kwargs)
    #         self.save_settings()
    #     return wrapper

    def add_menuItems(self, parent=None, items=None):
        [cmds.menuItem(p=parent, **item) for item in items]

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

        if self.cur_savepath:
            set_start_dir = self.cur_savepath
        else:
            set_start_dir = cmds.textFieldButtonGrp(self.savepath_tfbg, q=True, tx=True)

        files = cmds.fileDialog2(
            ff=file_filter,
            ds=1,
            okc='OK',
            cc='Cancel',
            fm=fm,
            cap=title,
            dir=set_start_dir
        )

        if files:
            if fm == 2:
                return files[0]
            else:
                return files

    def get_items_from_selection(self, parent=None, type=None):
        items = cmds.textScrollList(parent, q=True, si=True)
        return cmds.textScrollList(parent, q=True, si=True) if type == 'textScrollList' else False

    def show_in_explorer_from_selection(self, *args, **kwargs):
        if not self.fbx_view_cbx_val:
            items = self.get_items_from_selection(parent=args[0], type=args[1])
            [os.startfile(os.path.realpath('/'.join(path.split('/')[:-1]))) for path in items]
            # [subprocess.run('explorer /select,{}'.format(path)) for path in items]

    def create_current_csv(self, *args, **kwargs):
        try:
            now = datetime.datetime.now()
            d = now.strftime('%y%m%d%H%M%S')
            self.current_date_csv = self.dir_cur + '/current_{}.csv'.format(d)
            csv_transfer(file_name=self.current_date_csv, operation='export', append_list=self.cur_fbx_files)
        except:
            print(traceback.format_exc())

    ####
    # Bookmarks
    ####
    def add_promptDialog(self, prompt_settings=None):
        result = cmds.promptDialog(**prompt_settings)
        return cmds.promptDialog(query=True, text=True) if result == 'OK' else False

    def add_bookmark(self, *args, **kwargs):
        bookmark_prompt = {
            't':'Add Bookmark',
    		'm':'Enter Name:',
    		'b':['OK', 'Cancel'],
    		'db':'OK',
    		'cb':'Cancel',
    		'ds':'Cancel'
        }
        self.cur_bookmark_name = self.add_promptDialog(prompt_settings=bookmark_prompt)
        if self.cur_bookmark_name:
            self.current_bookmark_csv = self.dir_bookmark + '/' + self.cur_bookmark_name + '.csv'
            self.cur_bookmarks[self.cur_bookmark_name] = list()

        self.save_settings()

        self.reload_bookmark_list()

        self.create_current_csv()

        # self.reload_fbx_list()

    def reload_bookmark_list(self, *args, **kwargs):
        cmds.textScrollList(self.bookmark_tsl, e=True, ra=True)
        self.bookmark_items = [item for item in self.cur_bookmarks.keys()]
        cmds.textScrollList(self.bookmark_tsl, e=True, a=self.bookmark_items)

    def selected_items_in_bookmark_list(self, *args, **kwargs):
        self.select_bookmark_item_indices = cmds.textScrollList(self.bookmark_tsl, q=True, sii=True)
        cur_idx = self.select_bookmark_item_indices[0]
        self.cur_bookmark_name = self.bookmark_items[int(cur_idx)-1]
        self.current_bookmark_csv = self.dir_bookmark + '/' + self.cur_bookmark_name + '.csv'

        self.cur_fbx_files = self.cur_bookmarks[self.cur_bookmark_name]

        self.save_settings()

        self.reload_fbx_list()

    def remove_bookmark_from_list(self, *args, **kwargs):
        remove_items = [self.bookmark_items[i-1] for i in self.select_bookmark_item_indices]
        [self.cur_bookmarks.pop(item) for item in remove_items]
        # [self.cur_fbx_files.remove(item) for item in remove_items]
        cmds.textScrollList(self.bookmark_tsl, e=True, da=True)

        for item in remove_items:
            current_bookmark_csv = self.dir_bookmark + '/' + item + '.csv'
            current_bookmark_old_csv = self.dir_bookmark_old + '/' + item + '.csv'
            # os.makedirs(self.dir_bookmark_old)
            if os.path.isfile(current_bookmark_csv):
                shutil.move(current_bookmark_csv, current_bookmark_old_csv)
                # os.remove(current_bookmark_csv)

        # self.save_settings()

        self.reload_bookmark_list()

    def update_bookmarks(self, *args, **kwargs):
        try:
            for cur_b, cur_fbx_files in self.cur_bookmarks.items():
                cur_b_csv = self.dir_bookmark + '/' + cur_b + '.csv'
                csv_transfer(file_name=cur_b_csv, operation='export', append_list=cur_fbx_files)
        except:
            print(traceback.format_exc())

    ####
    # Save Path
    ####
    def set_savepath(self, *args, **kwargs):
        self.cur_savepath = self.save_items[self.optionVar_key][self.savepath_key] if self.savepath_key in self.save_items[self.optionVar_key].keys() else None

        save_path_args = {
            'title':'Set Save Path',
            'file_mode':'set',
            'file_filter':'FBX Files (*.fbx);;All Files (*.*)'
        }

        self.cur_savepath = self.file_dialog(**save_path_args)
        if self.cur_savepath:
            self.save_items[self.optionVar_key][self.savepath_key] = self.cur_savepath

        self.save_settings()

        self.reload_savepath()

    def reload_savepath(self, *args, **kwargs):
        cmds.textFieldButtonGrp(self.savepath_tfbg, e=True, tx=self.cur_savepath)

    ####
    # FBX
    ####
    def add_fbx(self, *args, **kwargs):
        self.cur_fbx_files = self.save_items[self.optionVar_key][self.fbx_files_key] if self.fbx_files_key in self.save_items[self.optionVar_key].keys() else list()

        fbx_dialog_args = {
            'title':'Add FBX',
            'file_mode':'open',
            'file_filter':'FBX Files (*.fbx);;CSV Files (*.csv);;All Files (*.*)'
        }

        get_files = self.file_dialog(**fbx_dialog_args)
        if get_files:
            csv_files = [file for file in get_files if '.csv' in file]
            imported_values = self.import_csv_files(csv_files)

            if imported_values:
                for values in imported_values:
                    for value in values:
                        if not value in get_files:
                            get_files.append(value)

            [get_files.remove(csv) for csv in csv_files]

            [self.cur_fbx_files.append(file) for file in get_files if not file in self.cur_fbx_files]
            self.save_items[self.optionVar_key][self.fbx_files_key] = self.cur_fbx_files

        if self.cur_bookmark_name:
            self.cur_bookmarks[self.cur_bookmark_name] = self.cur_fbx_files

        self.save_settings()

        self.reload_fbx_list()

        self.create_current_csv()


    def reload_fbx_list(self, *args, **kwargs):
        cmds.textScrollList(self.fbx_tsl, e=True, ra=True)
        items = [item for item in self.cur_fbx_files]
        self.fbx_view_cbx_val = cmds.checkBox(self.fbx_view_cbx, q=True, v=True)
        if self.fbx_view_cbx_val:
            items = [os.path.basename(item) for item in items]
            cmds.textScrollList(self.fbx_tsl, e=True, a=items)
        else:
            cmds.textScrollList(self.fbx_tsl, e=True, a=items)

        try:
            cmds.textScrollList(self.fbx_tsl, e=True, sii=self.select_fbx_item_indices) if self.select_fbx_item_indices else False
        except:
            # not selected
            pass
            # print(traceback.format_exc())

    def remove_fbx_from_list(self, *args, **kwargs):
        remove_items = [self.cur_fbx_files[i-1] for i in self.select_fbx_item_indices]
        self.cur_fbx_files = [item for item in self.cur_fbx_files if not item in remove_items]
        # [self.cur_fbx_files.remove(item) for item in remove_items]
        cmds.textScrollList(self.fbx_tsl, e=True, da=True)

        if self.cur_bookmark_name:
            self.cur_bookmarks[self.cur_bookmark_name] = self.cur_fbx_files

        self.save_settings()

        self.reload_fbx_list()

    def selected_items_in_fbx_list(self, *args, **kwargs):
        self.select_fbx_item_indices = cmds.textScrollList(self.fbx_tsl, q=True, sii=True)

    ####
    # Apply
    ####
    def apply_(self, *args, **kwargs):
        rig_id = cmds.optionMenu(self.rig_ops_menu, q=True, v=True)
        to_rig_file = self.settings['rig']['id'][rig_id]
        save_path = cmds.textFieldButtonGrp(self.savepath_tfbg, q=True, tx=True)

        saved_files, errors = fbxToRig.run_fbx_to_rig(fbx_files=self.cur_fbx_files,
                                              to_rig_file=to_rig_file,
                                              save_path=save_path,
                                              extension='ma',
                                              override=True)

        print('Saved:', '-'*20, len(saved_files))
        [print(f) for f in saved_files]
        print('Errors:', '-'*20, len(errors.keys()))
        [print(e) for e in errors]

        now = datetime.datetime.now()
        d = now.strftime('%y%m%d%H%M%S')
        d_w = now.strftime('%Y/%m/%d %H:%M:%S')
        log = self.dir_log + '/log_{}.json'.format(d)

        self.log_data['Date'] = d_w
        self.log_data['User'] = self.user
        self.log_data['Rig'] = to_rig_file
        self.log_data['SourceFiles'] = self.cur_fbx_files
        self.log_data['SaveFiles'] = saved_files
        self.log_data['Errors'] = errors

        # csv_transfer(file_name=log, operation='export', append_list=saved_files)
        json_transfer(file_name=log, operation='export', export_values=self.log_data)

        temp_window(temp_win='Temp Window: {}'.format(d_w), append_list=saved_files)


def temp_window(temp_win=None, append_list=None):
    if cmds.workspaceControl(temp_win, q=1, ex=1):
        cmds.deleteUI(temp_win)

    win = cmds.workspaceControl(temp_win, l=temp_win)

    main_col_lay = cmds.columnLayout(adj=1, p=win)
    saved_path_tsl = cmds.textScrollList(a=append_list, p=main_col_lay)
    saved_pop = cmds.popupMenu(p=saved_path_tsl)

    saved_pop_items = [
        {
            'l':'Open File',
            'c':partial(temp_open, saved_path_tsl)
        },
    ]

    [cmds.menuItem(p=saved_pop, **item) for item in saved_pop_items]

    cmds.showWindow(win)

def temp_open(*args, **kwargs):
    items = cmds.textScrollList(args[0], q=True, si=True)
    cmds.file(items[0], o=True, f=True) if items else False

def load_optionVar(key=None):
    return eval(cmds.optionVar(q=key)) if cmds.optionVar(ex=key) else False

def save_optionVar(save_items=None):
    for key, value in save_items.items():
        cmds.optionVar(sv=[key, str(value)])

def find_files(directory=None, pattern=None, exact=None):
    for root, dirs, files in os.walk(directory):
        if root.endswith(exact):
            continue
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename

def json_transfer(file_name=None, operation=None, export_values=None):
    u"""
    param:
        file_name = 'file_path'
        operation = 'import' or 'export'
        export_values = dict

    dict = json_transfer(file_name, 'import')
    json_transfer(file_name, 'export', dict)
    """
    if operation == 'export':
        try:
            with codecs.open(file_name, 'w', encoding='utf-8') as f:
                json.dump(export_values, f, indent=4, ensure_ascii=False)
        except:
            # print(traceback.format_exc())
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(export_values, f, indent=4, ensure_ascii=False)

    elif operation == 'import':
        try:
            with codecs.open(file_name, 'r', encoding='utf-8') as f:
                return json.load(f, 'utf-8', object_pairs_hook=OrderedDict)
        except:
            # print(traceback.format_exc())
            with open(file_name, 'r', encoding="utf-8") as f:
                return json.load(f, object_pairs_hook=OrderedDict)

def csv_transfer(file_name=None, operation=None, append_list=None):
    if operation == 'export':
        with open(file_name, 'w', newline='') as f:
            writer = csv.writer(f)
            [writer.writerow([al]) for al in append_list]

    elif operation == 'import':
        with open(file_name) as f:
            reader = csv.reader(f)
            return [''.join(r) for r in reader]


if __name__ == '__main__':
    ui = FbxToRigWindow()
    ui.show()
