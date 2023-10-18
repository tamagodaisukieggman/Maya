# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

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

import base64
import codecs
from collections import OrderedDict
import fnmatch
from functools import partial
import glob
from imp import reload
import json
import math
import os
import pickle
import re
import subprocess
import sys
import time
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR
from timeit import default_timer as timer
import traceback

from maya import cmds
from maya import mel
from maya import OpenMayaUI as omui
import maya.api.OpenMaya as om2

try:
    import bat.fromBat as fromBat
    import bat.toBat as toBat
    reload(fromBat)
    reload(toBat)
    tofrom_bat_dir = os.path.dirname(toBat.__file__.replace('\\', '/'))
except:
    print(traceback.format_exc())

try:
    import tkgrig.tkg_skinCluster as tkgScn
    reload(tkgScn)
except:
    print(traceback.format_exc())

maya_version = cmds.about(v=1)

"""
# -----------
# fileDirectory.py
# -----------
"""
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin, MayaQWidgetDockableMixin

WINDOW_TITLE = 'Multi File Browser'
WINDOW_OPTIONVAR = 'Multi_File_Browser'

class FileDirectoryTree(MayaQWidgetDockableMixin, QMainWindow):
    # QMainWindowを継承するとmenubarの使える幅が広い
    def __init__(self, *args, **kwargs):
        super(FileDirectoryTree, self).__init__(*args, **kwargs)

        # ウィジェットが閉じているときに、そのウィジェットを削除する
        # self.setAttribute(Qt.WA_DeleteOnClose, True)

        self.nss = ':'
        self.recentFiles_actions = None
        self.cur_paths = []
        self.config = OrderedDict()
        self.dir_path = '/'.join(__file__.replace('\\', '/').split('/')[0:-1])
        self.data_path = '{}/{}'.format(self.dir_path, 'data')
        self.icons_path = '{}/{}'.format(self.dir_path, 'icons')
        self.history_path = '{}/history.json'.format(self.data_path)
        self.load_bookmarks = OrderedDict()
        self.bookmark_pj_menus = []
        self.bookmark_id_menus = []
        self.bookmark_pj_QMenus = []
        self.bookmark_id_QMenus = []
        self.listDir_in_cur_path = []
        self.curTreeRowCount = 0
        self.root_index = None
        self.cur_index = None
        self.set_path_stock = OrderedDict()
        self.undo_redo_path_idx = -1
        self.undo_redo_idx = 0
        self.anim_sequences = []
        self.play_sts = None

        self.clipboard = QClipboard()

        self.setWindowTitle(WINDOW_TITLE)


    def layout(self):
        self.setGeometry(10, 10, 960, 540) # (left, top, width, height)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.main_qvbl = QVBoxLayout(self)
        self.main_widget.setLayout(self.main_qvbl)

        self.main_qhbl = QHBoxLayout(self)
        self.main_qvbl.addLayout(self.main_qhbl)

        self.path_nss_qvbl = QVBoxLayout(self)
        self.main_qhbl.addLayout(self.path_nss_qvbl)

        self.btnsqvbl = QVBoxLayout(self)
        self.main_qhbl.addLayout(self.btnsqvbl)

    def widgets(self):
        # QLine
        self.searchline_le = QLineEdit()
        self.searchline_le.setEditable = True # Ctrl+Zで戻れるようになる
        self.path_nss_qvbl.addWidget(QLabel('FilePath'))
        self.path_nss_qvbl.addWidget(self.searchline_le)

        # QLine
        self.history_search_le = QLineEdit()
        self.history_search_le.setEditable = True # Ctrl+Zで戻れるようになる
        self.path_nss_qvbl.addWidget(QLabel('History Search'))
        self.path_nss_qvbl.addWidget(self.history_search_le)

        # self.completer = QCompleter(self)
        self.completer = QCompleter(self)
        # self.completer.setModel(QStringListModel((self.load_values['path'])))
        # self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        # self.completer.setWrapAround(False)
        # self.searchline_le.textChanged.connect(lambda wildcard: self.completer.updatePattern(wildcard))
        self.searchline_le.textChanged.connect(self.search_paths)

        self.history_search_le.textChanged.connect(self.search_history)
        # self.completer.setCompletionMode( QCompleter.UnfilteredPopupCompletion )
        # self.completer.setCompletionMode(QCompleter.PopupCompletion)
        # self.completer.setFilterMode(Qt.MatchContains)
        # self.completer.setPopup( self.view() )
        self.searchline_le.setCompleter(self.completer)
        # self.searchline_le.textChanged.connect(self.view)


        self.referencename_le = QLineEdit()
        self.referencename_le.setEditable = True
        self.path_nss_qvbl.addWidget(QLabel('NameSpace'))
        self.path_nss_qvbl.addWidget(self.referencename_le)

        self.searchFiles_cbx = QComboBox()
        self.searchFiles_cbx.setEditable(True)
        self.path_nss_qvbl.addWidget(QLabel('SearchFiles'))
        self.path_nss_qvbl.addWidget(self.searchFiles_cbx)

        self.curPathCompleter = QCompleter(self)
        self.curPathCompleter.setModel(QStringListModel((self.listDir_in_cur_path)))
        self.curPathCompleter.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.searchFiles_cbx.currentTextChanged.connect(self.search_cur_paths)
        self.searchFiles_cbx.setCompleter(self.curPathCompleter)

        # self.checkBox_qhbl = QHBoxLayout(self)
        # self.path_nss_qvbl.addLayout(self.checkBox_qhbl)
        #
        # self.lockHistoryFile_cbx = QCheckBox('Update History All Times', self)
        # self.lockHistoryFile_cbx.stateChanged.connect(self.lock_update_files)
        # self.lockHistoryFile_cbx.setToolTip('Update History All Times')
        # self.checkBox_qhbl.addWidget(self.lockHistoryFile_cbx)

        self.action_btn_gridl = QGridLayout()
        self.btnsqvbl.addLayout(self.action_btn_gridl)

        self.undoPath_btn = QPushButton('', self)
        self.undoPath_btn.clicked.connect(partial(self.undo_redo_paths, 'undo'))
        self.undoPath_btn.setIcon(QIcon('{}/UndoPath.png'.format(self.icons_path)))
        self.undoPath_btn.setToolTip('Undo Path')
        self.action_btn_gridl.addWidget(self.undoPath_btn, 0, 1)

        self.redoPath_btn = QPushButton('', self)
        self.redoPath_btn.clicked.connect(partial(self.undo_redo_paths, 'redo'))
        self.redoPath_btn.setIcon(QIcon('{}/RedoPath.png'.format(self.icons_path)))
        self.redoPath_btn.setToolTip('Redo Path')
        self.action_btn_gridl.addWidget(self.redoPath_btn, 0, 2)

        self.openFile_btn = QPushButton('', self)
        self.openFile_btn.clicked.connect(partial(self._file, 'open'))
        self.openFile_btn.setIcon(QIcon('{}/OpenFile.png'.format(self.icons_path)))
        self.openFile_btn.setToolTip('Open File')
        self.action_btn_gridl.addWidget(self.openFile_btn, 0, 3)

        self.saveFile_btn = QPushButton('', self)
        self.saveFile_btn.clicked.connect(partial(self._file, 'save'))
        self.saveFile_btn.setIcon(QIcon('{}/SaveFile.png'.format(self.icons_path)))
        self.saveFile_btn.setToolTip('Save File')
        self.action_btn_gridl.addWidget(self.saveFile_btn, 0, 4)

        self.fileDialogToParent_btn = QPushButton('', self)
        self.fileDialogToParent_btn.clicked.connect(self.go_to_parent)
        self.fileDialogToParent_btn.setIcon(QIcon('{}/FileDialogToParent.png'.format(self.icons_path)))
        self.fileDialogToParent_btn.setToolTip('Go to Parent Path')
        self.action_btn_gridl.addWidget(self.fileDialogToParent_btn, 1, 1)

        self.browseFolder_btn = QPushButton('', self)
        self.browseFolder_btn.clicked.connect(self.show_explorer)
        self.browseFolder_btn.setIcon(QIcon('{}/BrowseFolder.png'.format(self.icons_path)))
        self.browseFolder_btn.setToolTip('Show in Explorer')
        self.action_btn_gridl.addWidget(self.browseFolder_btn, 1, 2)

        self.createNewFolder_btn = QPushButton('', self)
        self.createNewFolder_btn.clicked.connect(partial(self.create_dir_dialog)) # QDialogはpartialから起動したほうがいい
        self.createNewFolder_btn.setIcon(QIcon('{}/CreateNewFolder.png'.format(self.icons_path)))
        self.createNewFolder_btn.setToolTip('Create New Folder')
        self.action_btn_gridl.addWidget(self.createNewFolder_btn, 1, 3)

        self.setCurScenePath_btn = QPushButton('', self)
        self.setCurScenePath_btn.clicked.connect(partial(self.set_current_scene_path)) # QDialogはpartialから起動したほうがいい
        self.setCurScenePath_btn.setIcon(QIcon('{}/SetCurrentScenePath.png'.format(self.icons_path)))
        self.setCurScenePath_btn.setToolTip('Set Current Scene Path')
        self.action_btn_gridl.addWidget(self.setCurScenePath_btn, 1, 4)

        self.copyPath_btn = QPushButton('', self)
        self.copyPath_btn.clicked.connect(partial(self.copy_path)) # QDialogはpartialから起動したほうがいい
        self.copyPath_btn.setIcon(QIcon('{}/CopyPath.png'.format(self.icons_path)))
        self.copyPath_btn.setToolTip('Copy Path')
        self.action_btn_gridl.addWidget(self.copyPath_btn, 2, 1)

        self.pastePath_btn = QPushButton('', self)
        self.pastePath_btn.clicked.connect(partial(self.paste_path)) # QDialogはpartialから起動したほうがいい
        self.pastePath_btn.setIcon(QIcon('{}/PastePath.png'.format(self.icons_path)))
        self.pastePath_btn.setToolTip('Paste Path')
        self.action_btn_gridl.addWidget(self.pastePath_btn, 2, 2)


        # self.searchpath_le = QLineEdit()
        # self.searchpath_le.setEditable = True
        # self.main_searchfiles_qhbl.addWidget(QLabel('SearchFiles'))
        # self.main_searchfiles_qhbl.addWidget(self.searchpath_le)
        # self.searchfiles_btn = QPushButton('Search')
        # self.main_searchfiles_qhbl.addWidget(self.searchfiles_btn)


        # QLine connect
        self.searchline_le.textChanged.connect(self.set_path)
        # self.searchline_le.textChanged.connect(self.search_paths)
        self.searchline_le.returnPressed.connect(self.set_path_by_pressing_enter)

        self.referencename_le.textChanged.connect(self.set_ref_path)


        # QSplitter
        self.splitterHorizontal = QSplitter(Qt.Horizontal)
        self.main_qvbl.addWidget(self.splitterHorizontal)

        # QTreeView
        self.main_tree_left = QTreeView()
        self.splitterHorizontal.addWidget(self.main_tree_left)
        self.main_tree_left.setVisible(False)

        self.main_tree_middle = QTreeView()
        self.splitterHorizontal.addWidget(self.main_tree_middle)

        self.splitterVertical = QSplitter(Qt.Vertical)
        self.splitterHorizontal.addWidget(self.splitterVertical)

        self.main_qvbl_right_wid = QWidget()
        self.splitterVertical.addWidget(self.main_qvbl_right_wid)

        self.main_qvbl_right = QVBoxLayout()
        self.main_qvbl_right_wid.setLayout(self.main_qvbl_right)


        # animation
        self.animLabel = QLabel()
        self.animLabel.adjustSize()
        self.animLabel.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.animLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.main_qvbl_right.addWidget(self.animLabel)

        self.anim_play_btn = QPushButton('Play <> Stop')
        self.main_qvbl_right.addWidget(self.anim_play_btn)
        self.anim_play_btn.clicked.connect(self.play_animSeqence)

        self.timeslider_qhbl = QHBoxLayout()
        self.main_qvbl_right.addLayout(self.timeslider_qhbl)

        self.anim_slider = QSlider(Qt.Horizontal, self)
        self.timeslider_qhbl.addWidget(self.anim_slider)
        self.anim_slider.valueChanged.connect(self.animSeqence_from_path)

        self.anim_speed_slider = QSlider(Qt.Horizontal, self)
        self.anim_speed_slider.setMaximum(100)
        self.anim_speed_slider.setMinimum(10)
        self.anim_speed_slider.setValue(10)
        self.timeslider_qhbl.addWidget(self.anim_speed_slider)
        self.anim_speed_slider.valueChanged.connect(self.play_animSeqence)
        # animation --

        self.main_tree_left.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.main_tree_middle.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # self.main_tree_right.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.main_tree_left.setSortingEnabled(True) # QTreeVeiwでsortをONにする
        self.main_tree_middle.setSortingEnabled(True) # QTreeVeiwでsortをONにする
        # self.main_tree_right.setSortingEnabled(True) # QTreeVeiwでsortをONにする

        # Model
        self.sort_model = QSortFilterProxyModel()
        self.sort_model.sort(3)
        self.file_model = QFileSystemModel()
        self.sort_model.setSourceModel(self.file_model)
        self.file_model.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot | QDir.Files)
        # self.file_model.setRootPath(self.file_model.myComputer())
        self.set_rootPath_from_config()
        self.file_model.setRootPath(self.root_path)
        self.file_model.setNameFilterDisables(False)
        self.file_model.directoryLoaded.connect(self._loaded) # setRootPathをリフレッシュするためにdirectoryLoadedが必要になる

        self.search_list_model = QStandardItemModel()
        self.search_list_model.setColumnCount(1)
        self.search_list_model.setHeaderData(0, Qt.Horizontal, 'Search Files')

        # Model set
        self.main_tree_left.setModel(self.file_model)
        self.main_tree_middle.setModel(self.file_model)
        # self.main_tree_right.setModel(self.search_list_model)

        # QTreeView connect
        self.main_tree_left.clicked.connect(self.get_path_left_middle)
        self.main_tree_middle.clicked.connect(self.get_path_left_middle)
        # self.main_tree_right.clicked.connect(self.get_path_right)

        # self.searchpath_le.editingFinished.connect(self.search_files)
        # self.searchfiles_btn.clicked.connect(self.search_files)

        # QTreeView connect context menu
        self.main_tree_left.setContextMenuPolicy(Qt.CustomContextMenu) # QTreeViewにコンテキストメニューを追加する設定
        self.main_tree_left.customContextMenuRequested.connect(self.list_menu_available_sender) # QTreeViewで設定するコンテキストメニュー

        self.main_tree_middle.setContextMenuPolicy(Qt.CustomContextMenu) # QTreeViewにコンテキストメニューを追加する設定
        self.main_tree_middle.customContextMenuRequested.connect(self.list_menu_available_sender) # QTreeViewで設定するコンテキストメニュー

        # self.main_tree_right.setContextMenuPolicy(Qt.CustomContextMenu) # QTreeViewにコンテキストメニューを追加する設定
        # self.main_tree_right.customContextMenuRequested.connect(self.list_menu_available_sender) # QTreeViewで設定するコンテキストメニュー

        # # Status
        # self.status_qhbl = QGridLayout(self)
        # self.main_qvbl.addLayout(self.status_qhbl)
        # self.main_qvbl.addWidget(QLabel('SearchFiles'))


    def get_config(self):
        try:
            self.config_file = '{}/config.json'.format(self.data_path)

            with open(self.config_file) as f:
                self.config = json.load(f, object_pairs_hook=OrderedDict)

        except Exception as e:
            print(traceback.format_exc())

    def set_rootPath_from_config(self):
        self.root_path = self.config['path']['rootPath']
        if self.root_path == '':
            self.root_path = self.file_model.myComputer()

    def buildUI(self):
        # config
        self.get_config()

        # UI
        self.layout()
        self.widgets()

        self.create_menubar()

        self._loaded()

        self.load_settings()

        # self.set_current_path()

        self.set_text_from_recentFiles(self.searchline_le.text())


    def list_menu_available_sender(self, pos):
        sender = self.sender()
        # menus
        self.context_menu = QMenu(sender)

        # addAction
        context_menu = OrderedDict()
        context_menu['File Open'] = {'cmd':partial(self._file, 'open')}
        context_menu['File Import'] = {'cmd':partial(self._file, 'import')}
        context_menu['File Reference'] = {'cmd':partial(self._file, 'reference')}
        context_menu['Reference Editor'] = {'cmd':partial(cmds.ReferenceEditor)}
        context_menu['File Save'] = {'cmd':partial(self._file, 'save')}
        context_menu['File SaveWithPlayblast'] = {'cmd':partial(self._file, 'saveWithPb')}
        context_menu['SavePlayblast'] = {'cmd':partial(self.save_with_playblast)}
        context_menu['SaveSnapShot'] = {'cmd':partial(self.save_with_playblast, True)}
        context_menu['Open Explorer'] = {'cmd':partial(self.show_explorer)}
        context_menu['Set Current Path'] = {'cmd':partial(self.set_current_path)}
        context_menu['Go to Parent'] = {'cmd':partial(self.go_to_parent)}
        context_menu['Add Bookmark'] = {'cmd':partial(self.add_bookmark_dialog)}
        context_menu['importSkinweights(.json)'] = {'cmd':partial(self.import_skinWeights)}
        context_menu['importAttributes(.json)'] = {'cmd':partial(self.import_attributes)}

        for menu_name, menu_cmd in context_menu.items():
            action = self.context_menu.addAction(menu_name)
            action.triggered.connect(menu_cmd['cmd'])

        # QMenuの表示
        self.context_menu.exec_(sender.mapToGlobal(pos))

    def create_menubar(self):
        self.menu_bar = self.menuBar()
        # File
        self.file_menu = self.menu_bar.addMenu('File')

        # bookmarks
        self.bookmarks_menu = QMenu('Bookmarks')
        self.file_menu.addMenu(self.bookmarks_menu) # QMenuに一回継承させないとサブメニュー系はうまくいかない
        self.bookmarks_menu.aboutToShow.connect(partial(self.show_bookmarks_for_file_menu))

        # recentFiles
        self.recentFiles_menu = QMenu('Recent Files') # QMenuに一回継承させないとサブメニュー系はうまくいかない
        self.file_menu.addMenu(self.recentFiles_menu)
        self.recentFiles_menu.aboutToShow.connect(partial(self.show_history_for_file_menu))

        # Edit
        self.edit_menu = self.menu_bar.addMenu('Edit')
        # Save Settings
        self.ss_action = QAction(QIcon(''),
                                 'Save Settings',
                                 self,
                                 statusTip='Save Settings',
                                 triggered=partial(self.save_settings))
        self.edit_menu.addAction(self.ss_action)

        # Load Settings
        self.ls_action = QAction(QIcon(''),
                                 'Load Settings',
                                 self,
                                 statusTip='Load Settings',
                                 triggered=partial(self.load_settings))
        self.edit_menu.addAction(self.ls_action)

        # show dir path in Explorer
        self.sdp_action = QAction(QIcon(''),
                                 'Show dir path',
                                 self,
                                 statusTip='Go to this script path in explorer',
                                 triggered=partial(self.show_explorer, True))
        self.edit_menu.addAction(self.sdp_action)

        # shoe bat path in Explorer
        self.sdp_action = QAction(QIcon(''),
                                 'Show bat path',
                                 self,
                                 statusTip='Go to this script path in explorer',
                                 triggered=partial(self.show_explorer, False, True))
        self.edit_menu.addAction(self.sdp_action)

        # show hide self.main_tree_left
        self.aftv_action = QAction(QIcon(''),
                                 'Left Files Tree Visibility',
                                 self,
                                 statusTip='Left Files Tree Visibility',
                                 triggered=partial(self.all_files_tree_visible))
        self.edit_menu.addAction(self.aftv_action)


    def _file(self, file_by):
        if not self.cur_paths:
            self.cur_paths.append(self.searchline_le.text())

        print('READ', self.cur_paths)
        if self.cur_paths:
            for cur_path in self.cur_paths:
                if not self.load_paths:
                    self.load_paths = []
                else:
                    if 500 < len(self.load_paths):
                        self.load_paths.pop(0)

                if cur_path in self.load_paths:
                    self.load_paths.remove(cur_path)
                    self.load_paths.append(cur_path)
                else:
                    self.load_paths.append(cur_path)

                if file_by == 'open':
                    if cur_path.endswith('.py'):
                        if 2022 <= float(maya_version):
                            exec(open(str(cur_path), encoding="utf-8").read())
                        else:
                            execfile(cur_path)
                    elif cur_path.endswith('.bat'):
                            # Python3
                            if sys.version_info.major == 3:
                                subprocess.run([cur_path])

                            # Python2
                            if sys.version_info.major == 2:
                                os.system(cur_path)

                    else:
                        cmds.file(cur_path, ignoreVersion=1, options="v=0;p=17;f=0", o=1, f=1)
                elif file_by == 'import':
                    cmds.file(cur_path, pr=1, ignoreVersion=1, i=1, importTimeRange="combine", mergeNamespacesOnClash=False, options="v=0;p=17;f=0")
                elif file_by == 'reference':
                    cmds.file(cur_path, ignoreVersion=1, namespace=str(self.nss), r=1, gl=1, mergeNamespacesOnClash=1, options="v=0;")
                elif file_by == 'save' or file_by == 'saveWithPb':
                    save_path = self.searchline_le.text()

                    if save_path.endswith('.mb'):
                        file_type = 'mayaBinary'
                    elif save_path.endswith('.ma'):
                        file_type = 'mayaAscii'
                    else:
                        print('Incorrect File Type')
                        return

                    save_sts = None
                    if os.path.isfile(save_path):
                        qmessage_info = QMessageBox.information(None, "Exists File", "Override?", QMessageBox.Yes, QMessageBox.No)

                        if qmessage_info == QMessageBox.Yes:
                            save_sts = True

                        elif qmessage_info == QMessageBox.No:
                            save_sts = False
                            print('NotSaved:{0}'.format(save_path))
                            return

                    else:
                        save_sts = True

                    if save_sts:
                        cmds.file(rn=save_path)
                        cmds.file(f=1, save=1, options='v=0', type=file_type)
                        if file_by == 'saveWithPb':
                            self.save_with_playblast()

                        print('Saved:{0}'.format(save_path))

                        self.searchline_le.setText(str(save_path))
                        self.set_text_from_recentFiles(str(save_path))


        # print('LOAD_PATHS:', self.load_paths)

        self.save_settings()
        self.load_settings()


    def all_files_tree_visible(self):
        if not self.main_tree_left.isVisible():
            self.main_tree_left.setVisible(True)
        elif self.main_tree_left.isVisible():
            self.main_tree_left.setVisible(False)

    def set_text_from_recentFiles(self, path):
        self.searchline_le.setText('/'.join(path.split('/')[0:-1]))
        self.searchline_le.setText(path)
        tree_selection = path.split('/')
        sum_path = '{}/'.format(tree_selection[0])
        for i, si in enumerate(tree_selection):
            if not i == 0:
                sum_path = '{}{}/'.format(sum_path, si)
            index = self.file_model.index(sum_path) # パスからindexを取得
            self.main_tree_middle.selectionModel().select(index, QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows) # indexから選択
            self.main_tree_left.expand(index)

        self.cur_paths = []
        self.cur_paths.append(path)

        # undo redo
        if not path in self.set_path_stock.values():
            self.undo_redo_path_idx = self.undo_redo_path_idx + 1
            self.set_path_stock[self.undo_redo_path_idx] = path
            self.undo_redo_idx = self.undo_redo_path_idx


        self.get_sequenceFiles()

        self.save_settings()
        self.load_settings()

        # self.iterItems(index)
        # print(index.data())
        # print(self.main_tree_middle.rowCount())

    def get_sequenceFiles(self):
        cur_path = self.searchline_le.text()
        if os.path.isfile(cur_path):
            cur_dir = os.path.split(cur_path)
            mayaSwatches_path = cur_dir[0] + '/.mayaSwatches/' + cur_dir[1]
            if os.path.isdir(mayaSwatches_path):
                self.anim_sequences = [os.path.join(curDir, file).replace('\\', '/') for curDir, dirs, files in os.walk(mayaSwatches_path) for file in files if os.path.isfile(os.path.join(curDir, file))]

                if self.anim_sequences:
                    self.splitterVertical.setVisible(True)

                    # self.anim_sequences = os.listdir(mayaSwatches_path)
                    self.anim_sequences.sort()
                    # print(self.anim_sequences)

                    # pixmap_path = 'C:/Users/kesun/Documents/maya/scripts/tkgTools/launchers/maya/tkgTools/python/tkgrig/data/.mayaSwatches/twist_range_180_with_sin_anim.ma/twist_range_180_with_sin_anim.ma.0001.png'
                    self.anim_slider.setMaximum(len(self.anim_sequences))
                    self.anim_slider.setMinimum(0)
                    self.anim_slider.setValue(0)

                    # self.anim_sequences = [mayaSwatches_path + '/' + path for path in self.anim_sequences]

                    pixmap_path = self.anim_sequences[0]
                    self.animPixmap = QPixmap(pixmap_path)
                    self.animLabel.setPixmap(self.animPixmap.scaled(self.splitterVertical.height(), self.splitterVertical.width(), Qt.KeepAspectRatio, Qt.FastTransformation))

            else:
                self.splitterVertical.setVisible(False)

    def animSeqence_from_path(self):
        try:
            pixmap_path = self.anim_sequences[self.sender().value()]
        except IndexError:
            return

        self.animPixmap = QPixmap(pixmap_path)
        self.animLabel.setPixmap(self.animPixmap.scaled(self.splitterVertical.height(), self.splitterVertical.width(), Qt.KeepAspectRatio, Qt.FastTransformation))

    def iter_anim_slider(self):
        self.anim_slider.setValue(self.anim_frame)
        if self.anim_frame == len(self.anim_sequences) - 1:
            self.anim_frame = 0
        else:
            self.anim_frame = self.anim_frame + 1

    def play_animSeqence(self):
        if not self.play_sts:
            self.timer = QTimer()
            self.timer.setInterval(self.anim_speed_slider.value())
            self.timer.timeout.connect(self.iter_anim_slider)
            self.timer.start()
            self.anim_frame = 0

            self.play_sts = True

        else:
            self.timer.stop()
            self.play_sts = False


    def set_path_by_pressing_enter(self):
        path = self.sender().text()
        self.searchline_le.setText('/'.join(path.split('/')[0:-1]))
        self.searchline_le.setText(path)
        tree_selection = path.split('/')
        sum_path = '{}/'.format(tree_selection[0])
        for i, si in enumerate(tree_selection):
            if not i == 0:
                sum_path = '{}{}/'.format(sum_path, si)
            index = self.file_model.index(sum_path) # パスからindexを取得
            self.main_tree_middle.selectionModel().select(index, QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows) # indexから選択
            self.main_tree_left.expand(index)

        clipboard_spl = self.clipboard.text().replace('\\', '/')
        path_spl = path.replace('\\', '/')

        if clipboard_spl == path_spl:
            self.set_text_from_recentFiles(path_spl)

        self.cur_paths = []
        self.cur_paths.append(path)
        self.save_settings()
        self.load_settings()


    def _loaded(self):
        path = self.file_model.rootPath()
        index = self.file_model.index(path)
        self.main_tree_left.setRootIndex(index)
        # self.main_tree_middle.setRootIndex(index)

    def on_textChanged(self, text):
        print('TEXTCHANGED', text)

    def get_path_left_middle(self):
        sender = self.sender()
        indexes = sender.selectionModel().selectedIndexes()

        self.cur_paths = []
        for index in indexes:
            path = self.file_model.filePath(index)
            if not self.file_model.filePath(index) in self.cur_paths:
                self.cur_paths.append(path)

        self.set_current_path()
        # print(self.cur_paths)

    def get_path_right(self):
        sender = self.sender()
        indexes = sender.selectionModel().selectedIndexes()
        self.cur_paths = [index.data() for index in indexes]
        # print(self.cur_paths)

    def iterItems(self, index):
        map_index = self.file_model.mapToSource(index)
        # print('ROWCOUNT', self.file_model.rowCount(map_index))
        for row in range(self.file_model.rowCount(map_index)):
            print(row)

    def search_files(self):
        path = self.searchpath_le.text()
        if ':' in path and '/' in path:
            self.search_list_model.clear()

            directory = '{}/{}'.format(path.split('/')[0], '/'.join(path.split('/')[1:-1]))
            pattern = path.split('/')[-1]
            search_paths = [QStandardItem(filename.replace('\\', '/')) for filename in find_files(directory, pattern)]

            # self.search_list_model.appendColumn(search_paths)
            self.search_list_model.setColumnCount(1)
            self.search_list_model.setHeaderData(0, Qt.Horizontal, 'Search Files')
            # timeout = timer() + 30 # もう一回考えてみる
            timeout = time.time() + 60*5 # 5 minutes from now
            for i, item in enumerate(search_paths):
                test = 0
                if test == 5 or time.time() > timeout:
                    break
                test = test - 1

                self.search_list_model.setItem(i, 0, item)
                # if timeout < timer():
                #     print('SearchFiles > Timeout!')
                #     break

    def set_path(self, text):
        if os.path.isfile(text):
            text = str('/'.join(text.split('/')[0:-1]))

        if os.path.exists(text):
            self.root_index = self.file_model.index(text)
            self.cur_path = self.file_model.fileInfo(self.root_index).absoluteFilePath()
            self.cur_index = self.file_model.index(self.cur_path)
            if os.path.isdir(self.cur_path):
                self.main_tree_middle.setRootIndex(self.cur_index)
                # print(self.cur_path)

        # print(self.file_model.lastModified(self.root_index).toString())

        # search files
        searchFiles_cbx_allItems = {}
        for i in range(self.searchFiles_cbx.count()):
            searchFiles_cbx_allItems[self.searchFiles_cbx.itemText(i)] = i

        searchFiles_allPathItems = list(searchFiles_cbx_allItems.keys())
        searchFiles_allPathItems.sort()

        self.listDir_in_cur_path = os.listdir(self.cur_path)
        self.listDir_in_cur_path.sort()

        if not searchFiles_allPathItems == self.listDir_in_cur_path:
            self.searchFiles_cbx.clear()

        for item in self.listDir_in_cur_path:
            if not item in searchFiles_cbx_allItems.keys():
                self.searchFiles_cbx.addItem(item)

    def copy_path(self):
        self.clipboard.setText(self.searchline_le.text())

    def paste_path(self):
        mime_data = self.clipboard.mimeData()
        if mime_data.hasUrls():
            url = mime_data.urls()[0]
            file_path = url.toLocalFile()

            # text = self.clipboard.text().replace('\\', '/')
            self.searchline_le.setText(file_path)
            self.set_text_from_recentFiles(file_path)

    def show_explorer(self, dir_path=None, bat_path=None):
        path = self.searchline_le.text().replace('\\', '/')

        # if os.path.isfile(path):
        if dir_path:
            path = self.dir_path

        if bat_path:
            path = tofrom_bat_dir

        if os.name == 'nt':
            path = path.replace('/', '\\')
            subprocess.Popen('explorer /select,"{}"'.format(path))
        elif os.name == 'posix':
            subprocess.Popen(['open', '-R', path])

        # os.startfile(path)

    def set_current_path(self):
        self.searchline_le.setText(str(self.cur_paths[0]))
        self.set_text_from_recentFiles(str(self.cur_paths[0]))

    def set_current_scene_path(self):
        if cmds.file(q=1, sn=1):
            self.searchline_le.setText(cmds.file(q=1, sn=1))
            self.set_text_from_recentFiles(cmds.file(q=1, sn=1))

    def undo_redo_paths(self, operation=None):
        if operation == 'undo':
            self.undo_redo_idx = self.undo_redo_idx - 1
        elif operation == 'redo':
            self.undo_redo_idx = self.undo_redo_idx + 1

        try:
            # self.set_path(self.set_path_stock[self.undo_redo_idx])
            self.searchline_le.setText(str(self.set_path_stock[self.undo_redo_idx]))
            self.set_text_from_recentFiles(str(self.set_path_stock[self.undo_redo_idx]))
        except KeyError:
            if operation == 'undo':
                self.undo_redo_idx = self.undo_redo_idx + 1
            elif operation == 'redo':
                self.undo_redo_idx = self.undo_redo_idx - 1

        # print(self.undo_redo_idx, self.undo_redo_path_idx)

    def go_to_parent(self):
        cur_text = self.searchline_le.text()
        path = str('/'.join(cur_text.split('/')[0:-1]))
        self.searchline_le.setText(path)
        if os.path.isfile(cur_text):
            cur_text = self.searchline_le.text()
            self.searchline_le.setText(path)

        # undo redo
        if not path in self.set_path_stock.values():
            self.undo_redo_path_idx = self.undo_redo_path_idx + 1
            self.set_path_stock[self.undo_redo_path_idx] = path
            self.undo_redo_idx = self.undo_redo_path_idx


    def set_ref_path(self, text):
        self.nss = text

    def save_settings(self):
        # self.load_settings()
        if not self.load_paths:
            self.load_paths = []
        else:
            if 100 < len(self.load_paths):
                self.load_paths.pop(0)

        if self.cur_paths[0] in self.load_paths:
            self.load_paths.remove(self.cur_paths[0])
            if os.path.isfile(self.cur_paths[0]):
                self.load_paths.append(self.cur_paths[0])
        # self.load_paths = list(set(self.load_paths))

        self.save_items = OrderedDict()
        self.save_items[WINDOW_OPTIONVAR] = OrderedDict()
        self.save_items[WINDOW_OPTIONVAR]['path'] = self.load_paths
        self.save_items[WINDOW_OPTIONVAR]['bookmark'] = self.load_bookmarks
        self.save_items[WINDOW_OPTIONVAR]['curpath'] = self.cur_paths[0]

        # print('SAVE PATH', self.save_items[WINDOW_OPTIONVAR]['path'])

        for key, value in self.save_items.items():
            v = str(value)
            cmds.optionVar(sv=[key, v])

        # if self.lockHistoryFile_cbx.isChecked():
        # if os.access(self.history_path, os.W_OK):
        json_transfer(self.history_path, 'export', export_values=self.save_items, export_type='utf-8')

        # print('History Saved:', self.history_path)
        # print('Save Settings')

    def load_settings(self):
        try:
            self.get_history = json_transfer(self.history_path, 'import', import_type='utf-8')
            self.load_values = self.get_history[WINDOW_OPTIONVAR]

        except:
            print(traceback.format_exc())
            # json_transfer(self.history_path, 'export', export_values={}, export_type='utf-8')
            self.load_values = load_optionvar(WINDOW_OPTIONVAR)
            print('RecentFiles Loaded From optionVar')

        self.show_history()
        self.show_bookmarks()

        for key, value in self.load_values.items():
            if key == 'curpath':
                if os.path.isdir(value) or os.path.isfile(value):
                    # self.set_text_from_recentFiles(value)
                    self.searchline_le.setText(value)
                    index = self.file_model.index(value) # パスからindexを取得
                    # if os.access(self.history_path, os.W_OK):
                    self.main_tree_middle.selectionModel().select(index, QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows) # indexから選択
                    # self.cur_paths.append(value)

        # print('Load Settings')

    def search_paths(self):
        # path = str(path.split('*')[-1])
        search_paths = [s for s in self.load_values['path']]
        filtered = list(set(fnmatch.filter(search_paths, self.sender().text())))
        # self.model().setStringList(filtered)
        if not filtered:
            self.completer.model().setStringList(self.load_values['path'])

        else:
            self.completer.model().setStringList(filtered)

        self.completer.popup()

    def search_cur_paths(self):
        self.curTreeRowCount = self.main_tree_middle.model().rowCount(self.root_index)

        # path = str(path.split('*')[-1])
        search_paths = [s for s in self.listDir_in_cur_path]
        filtered = list(set(fnmatch.filter(search_paths, self.sender().currentText())))
        # self.model().setStringList(filtered)
        # print(self.listDir_in_cur_path)
        if not filtered:
            self.curPathCompleter.model().setStringList(self.listDir_in_cur_path)
            for i in range(self.curTreeRowCount):
                try:
                    ix = self.main_tree_middle.model().index(i, 0, self.root_index)
                    self.main_tree_middle.selectionModel().select(ix, QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows) # indexから選択
                except NotImplementedError:
                    pass
                # self.main_tree_middle.setRowHidden(i, self.root_index, False)

        else:
            self.curPathCompleter.model().setStringList(filtered)

            # index = QModelIndex()
            for i in range(self.curTreeRowCount):
                try:
                    ix = self.main_tree_middle.model().index(i, 0, self.root_index)
                    if ix.data() in filtered:
                        self.main_tree_middle.selectionModel().select(ix, QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows) # indexから選択
                    # self.main_tree_middle.setRowHidden(i, self.root_index, False)
                    # print('{}/{}'.format(self.cur_path, ix.data()))
                    # print('{}/{}'.format(self.cur_path, ix.data()))
                    # self.searchline_le.setText('{}/{}'.format(self.cur_path, ix.data()))
                    # self.set_path('{}/{}'.format(self.cur_path, ix.data()))
                except NotImplementedError:
                    pass


                # else:
                #     self.main_tree_middle.setRowHidden(i, self.root_index, True)


        self.curPathCompleter.popup()


    def add_bookmark_dialog(self):
        self.add_dialog = QDialog(self)
        dcpt_lay = QVBoxLayout()
        ids_lay = QVBoxLayout()

        dcpt_lay.addLayout(ids_lay)

        pj_lay = QHBoxLayout()
        ids_lay.addLayout(pj_lay)

        pj_qlabel = QLabel('Project')
        pj_lay.addWidget(pj_qlabel)

        self.add_bookmark_pj_textbox = QComboBox()
        self.add_bookmark_pj_textbox.setEditable(True)
        self.add_bookmark_pj_textbox.addItems(self.load_bookmarks.keys())
        self.add_bookmark_pj_textbox.currentTextChanged.connect(self.add_bookmark_id_from_pj)
        pj_lay.addWidget(self.add_bookmark_pj_textbox)

        id_lay = QHBoxLayout()
        ids_lay.addLayout(id_lay)

        id_qlabel = QLabel('ID')
        id_lay.addWidget(id_qlabel)

        self.add_bookmark_id_textbox = QComboBox()
        self.add_bookmark_id_textbox.setEditable(True)
        try:
            id_paths = self.load_bookmarks[self.add_bookmark_pj_textbox.currentText()]
            self.add_bookmark_id_textbox.addItems(id_paths.keys())
        except KeyError:
            pass

        id_lay.addWidget(self.add_bookmark_id_textbox)

        # self.add_bookmark_pj_textbox = QLineEdit()
        # self.dcpt_editor.setPlainText('Hellow PySide!!') # plain_text

        self.add_dialog.setLayout(dcpt_lay)

        dcpt_ok_btn = QPushButton('OK')
        dcpt_ok_btn.clicked.connect(self.add_bookmark)
        dcpt_lay.addWidget(dcpt_ok_btn)

        self.add_dialog.setWindowTitle('Add Bookmark')

        self.add_dialog.exec_()

    def add_bookmark_id_from_pj(self):
        try:
            id_paths = self.load_bookmarks[self.add_bookmark_pj_textbox.currentText()]
            self.add_bookmark_id_textbox.clear()
            self.add_bookmark_id_textbox.addItems(id_paths.keys())
        except KeyError:
            pass

    def add_bookmark(self, fromHistory=None):
        # print(self.bookmark_pj_QMenus)
        # print(self.bookmarks_menu)
        if fromHistory:
            for bookmark_pj, bookmark_ids in self.load_bookmarks.items():
                bookmark_pj_menu = QMenu(bookmark_pj) # QMenuに一回継承させないとサブメニュー系はうまくいかない
                self.bookmarks_menu.addMenu(bookmark_pj_menu)
                for bookmark_id, paths in bookmark_ids.items():
                    bookmark_id_menu = QMenu(bookmark_id) # QMenuに一回継承させないとサブメニュー系はうまくいかない
                    bookmark_pj_menu.addMenu(bookmark_id_menu)
                    self.set_bookmark_actions(bookmark_id_menu, paths)

        elif not fromHistory:
            # print(self.add_bookmark_pj_textbox.text())
            bookmark_pj = self.add_bookmark_pj_textbox.currentText()
            bookmark_id = self.add_bookmark_id_textbox.currentText()
            if not self.cur_paths:
                self.cur_paths.append(self.searchline_le.text())

            paths = self.cur_paths

            get_expaths = None
            for expj, id_paths in self.load_bookmarks.items():
                if expj == bookmark_pj:
                    for exid, expaths in id_paths.items():
                        if exid == bookmark_id:
                            get_expaths = expaths
                            break

            if get_expaths:
                for curp in paths:
                    if not curp in get_expaths:
                        get_expaths.append(curp)

            else:
                get_expaths = paths

            if not bookmark_pj in self.load_bookmarks.keys():
                self.load_bookmarks[bookmark_pj] = OrderedDict()

            if not bookmark_id in self.load_bookmarks[bookmark_pj].keys():
                self.load_bookmarks[bookmark_pj][bookmark_id] = []

            self.load_bookmarks[bookmark_pj][bookmark_id] = get_expaths

            # return self.add_bookmark_pj_textbox.text()
            self.add_dialog.close()
            self.save_settings()
            self.load_settings()

            # print(self.bookmarks_menu.findChildren())

    def set_bookmark_actions(self, parentQMenu=None, paths=None):
        expaths = self.get_children_menu(parentQMenu)
        for path in paths:
            if not path in expaths:
                if os.path.isfile(path):
                    action = QAction(QIcon(''),
                                             path,
                                             self,
                                             statusTip=path,
                                             triggered=partial(self.set_text_from_recentFiles, path))
                    parentQMenu.addAction(action)


    def get_children_menu(self, parentQMenu):
        actions = []
        for a in parentQMenu.actions():
            if not a.text() in actions:
                actions.append(a.text())
        return actions

    def get_match_menu(self, parentQMenu, name):
        for a in parentQMenu.actions():
            if name == a.text():
                return a


    def create_dir_dialog(self):
        self.create_dir_dialog = QDialog(self)
        dcpt_lay = QVBoxLayout()

        self.cd_folder_name_text = QLineEdit()
        # self.add_bookmark_pj_textbox.setEditable(True)
        # self.cd_folder_name_text.addItems(self.load_bookmarks.keys())

        # self.add_bookmark_pj_textbox = QLineEdit()
        # self.dcpt_editor.setPlainText('Hellow PySide!!') # plain_text

        self.create_dir_dialog.setLayout(dcpt_lay)
        dcpt_lay.addWidget(self.cd_folder_name_text)

        dcpt_ok_btn = QPushButton('OK')
        dcpt_ok_btn.clicked.connect(self.create_dir_in_cur_path)
        dcpt_lay.addWidget(dcpt_ok_btn)

        self.create_dir_dialog.setWindowTitle('Create New Folder')

        self.create_dir_dialog.exec_()

    def create_dir_in_cur_path(self):
        folder_name = self.cd_folder_name_text.text()
        cur_text = self.searchline_le.text()
        if os.path.isfile(cur_text):
            cur_text = '/'.join(cur_text.split('/')[0:-1])

        # print('{}/{}'.format(cur_text, folder_name))
        new_folder = '{}/{}'.format(cur_text, folder_name)
        if not os.path.isdir(new_folder):
            os.makedirs(new_folder)
        else:
            print('already exists:{}'.format(new_folder))

        self.create_dir_dialog.close()

    def lock_update_files(self):
        if self.lockHistoryFile_cbx.isChecked():
            os.chmod(self.history_path, S_IREAD|S_IRGRP|S_IROTH)
        else:
            os.chmod(self.history_path, S_IWUSR|S_IREAD)

    def iterItems(self, root):
        if root is not None:
            stack = [root]
            while stack:
                parent = stack.pop(0)
                for row in range(parent.rowCount()):
                    for column in range(parent.columnCount()):
                        child = parent.child(row, column)
                        yield child
                        if child.hasChildren():
                            stack.append(child)

    def save_with_playblast(self, snapshot=None):
        cur_time=cmds.currentTime(q=1)
        if cmds.autoKeyframe(q=True, st=True):
            autoKeyState = 1
        else:
            autoKeyState = 0

        cmds.autoKeyframe(st=0)

        playmin = cmds.playbackOptions(q=1, min=1)
        playmax = cmds.playbackOptions(q=1, max=1)

        cur_path = cmds.file(q=1, sn=1)
        cur_dir = os.path.split(cur_path)

        mayaSwatches_path = cur_dir[0] + '/.mayaSwatches/' + cur_dir[1]
        try:
            os.makedirs(mayaSwatches_path)
        except FileExistsError:
            pass

        if snapshot:
            playmin = cur_time
            playmax = playmin

        cmds.playblast(st=playmin,
                       et=playmax,
                       fmt='image',
                       f="{}/{}".format(mayaSwatches_path, cur_dir[1]),
                       p=50,
                       v=False,
                       fo=True,
                       fp=4)

        cmds.currentTime(cur_time)
        cmds.autoKeyframe(st=autoKeyState)

    def import_skinWeights(self):
        weight_json = self.searchline_le.text()
        if not weight_json.endswith('.json'):
            return

        reload(tkgScn)
        tkgSkinCluster = tkgScn.TKGSkinWeights()
        tkgSkinCluster.import_file = True
        getWeightsValues = tkgScn.json_transfer(weight_json, 'import')
        tkgSkinCluster.set_objects_weights(getWeightsValues)

    def import_attributes(self):
        at_json = self.searchline_le.text()
        if not at_json.endswith('.json'):
            return

        reload(fromBat)
        batFunc = fromBat.BatFunc()
        batFunc.set_object_values(at_json, 'Attributes')

    def show_history(self):
        try:
            for key, value in self.load_values.items():
                if key == 'path':
                    self.recentFiles_menu.clear()
                    self.load_paths = [path for path in value]
                    filtered = self.search_history()
                    for path in filtered[::-1]:
                        if os.path.isfile(path):
                            action = QAction(QIcon(''),
                                                     path,
                                                     self,
                                                     statusTip=path,
                                                     triggered=partial(self.set_text_from_recentFiles, path))
                            self.recentFiles_menu.addAction(action)

                    self.completer.setModel(QStringListModel((self.load_values[key])))
        except:
            self.load_paths = []
            print(traceback.format_exc())

    def show_history_for_file_menu(self):
        self.load_settings()
        self.show_history()

    def show_bookmarks(self):
        for key, value in self.load_values.items():
            if key == 'bookmark':
                self.bookmarks_menu.clear()
                for pj_label, id_paths in value.items():
                    self.load_bookmarks[pj_label] = OrderedDict()
                    for id_label, paths in id_paths.items():
                        self.load_bookmarks[pj_label][id_label] = paths

                self.add_bookmark(True)

    def show_bookmarks_for_file_menu(self):
        self.load_settings()
        self.show_bookmarks()

    def search_history(self):
        # sender = self.sender()
        # search_text = sender.text()

        search_text = self.history_search_le.text()

        if search_text == '':
            return self.load_paths

        search_txt_list = [
            '*{}*'.format(search_text)
        ]

        return filter_items(source_items=self.load_paths, search_txt_list=search_txt_list, remover=False)

    def hello_world(self):
        print('Hello World!')

class PathCompleter(QCompleter):
    def __init__(self, *args):
        super().__init__(*args)

    def setModel(self, model):
        self.proxyModel = QSortFilterProxyModel()
        self.proxyModel.setSourceModel(model)
        self.proxyModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
        super().setModel(self.proxyModel)

    def updatePattern(self, patternStr):
        self.proxyModel.setFilterWildcard(patternStr)


# search_files = [filename for filename in find_files('F:/', '*wpbase*.fbx')]
def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename

def load_optionvar(key):
    if cmds.optionVar(ex=key):
        return eval(cmds.optionVar(q=key))
    else:
        return None

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
                return json.load(f, object_pairs_hook=OrderedDict)

        elif import_type == 'pickle':
            with open(fileName) as f:
                d = json.load(f)
            s = d["pickle"]
            return pickle.loads(base64.b64decode(s.encode()))

if __name__ == '__main__':
    ui = FileDirectoryTree()
    ui.buildUI()
    ui.show(dockable=True)
