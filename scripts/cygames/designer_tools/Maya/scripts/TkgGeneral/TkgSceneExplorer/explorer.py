# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

from PySide2 import QtWidgets, QtCore

import os
import re

import maya.cmds as cmds

from . import view
from . import utility
from . import const
from . import scene_opener
from . import scene_collector
from .ui import model

try:
    # Maya2022-
    from builtins import str
    from builtins import object
    from builtins import range
    from importlib import reload
except Exception:
    pass

reload(view)
reload(utility)
reload(const)
reload(scene_opener)
reload(scene_collector)
reload(model)


class Explorer(object):

    def __init__(self, main):
        """
        """

        self.main = main
        self.view = main.view

        self.ext_pattern = const.EXTENT_PATTERN
        self.search_root_path = ''
        self.search_str = ''
        self.is_incomplete_search = False

        self.ext_filter_buttons = []
        self.current_ext_filter = []
        self.file_path_pool = []

        self.prev_target_col_id = None

    def initialize_ui(self):

        # ファイルツリー
        self.file_system_model = QtWidgets.QFileSystemModel(self.view)
        self.file_system_model.setRootPath('')
        self.view.ui.dir_tree.setModel(self.file_system_model)
        self.view.ui.dir_tree.setRootIndex(QtCore.QModelIndex())
        self.view.ui.dir_tree.setHeaderHidden(True)
        self.view.ui.dir_tree.hideColumn(1)
        self.view.ui.dir_tree.hideColumn(2)
        self.view.ui.dir_tree.hideColumn(3)
        self.view.ui.dir_tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.view.ui.dir_tree.setExpandsOnDoubleClick(False)

        # ブックマーク
        self.view.ui.bookmark_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        # 最近使ったファイル
        self.update_recent_file_list()
        self.view.ui.recent_file_list_2.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        # 拡張子フィルターボタンは可変できるように後付け
        horizontalLayout = QtWidgets.QHBoxLayout(self.view.ui.filter_button_group)
        horizontalLayout.setContentsMargins(0, 0, 0, 0)
        horizontalLayout.setSpacing(0)
        for ext in const.EXTENT_LIST:
            button = QtWidgets.QPushButton(self.view.ui.filter_button_group)
            button.setMinimumWidth(30)
            button.setText(ext)
            button.setCheckable(True)
            button.setToolTip('.{} ファイルを表示します'.format(ext))
            horizontalLayout.addWidget(button)
            self.ext_filter_buttons.append(button)
            # 初期拡張子フィルターを設定
            if ext in const.INIT_ON_EXTENT_LIST:
                self.current_ext_filter.append('.' + ext)

        # ファイルテーブル
        self.file_table_model = model.FileTableModel(self.view)
        self.proxy_model = QtCore.QSortFilterProxyModel()
        self.proxy_model.setDynamicSortFilter(True)
        self.proxy_model.setSortCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.proxy_model.setSourceModel(self.file_table_model)
        self.view.ui.file_table.setModel(self.proxy_model)
        self.view.ui.file_table.setColumnWidth(0, 200)
        self.view.ui.file_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        # パラメータをUIに反映
        self.view.ui.root_dir_line.setText(self.search_root_path)
        self.view.ui.search_line.setText(self.search_str)
        self.set_ext_filter(self.current_ext_filter)

        # 前回の検索が不完全に終了している場合は起動時には検索しない
        if self.is_incomplete_search:
            self.tree_path_sync()
            cmds.confirmDialog(
                m='前回の検索で問題があったため検索結果を表示しません\nこのルートフォルダで検索する場合はリロードボタンを押してください'
            )
        else:
            self.search_root_path_update_event()

        # search_lineの削除ボタン押下時のイベント・アクション設定
        self.view.setUiSearchLine(self.search_word_update_event)

        self.update_info_label()

    def setup_view_event(self):
        """UIのevent設定
        """

        # ツリービュー
        self.view.ui.dir_tree.clicked.connect(self.dir_tree_click_event)
        self.view.ui.dir_tree.doubleClicked.connect(self.dir_tree_double_click_event)
        self.view.ui.dir_tree.customContextMenuRequested.connect(self.dir_tree_context_menu)

        # ブックマーク
        self.view.ui.bookmark_list.doubleClicked.connect(self.bookmark_double_click_event)
        self.view.ui.bookmark_list.customContextMenuRequested.connect(self.bookmark_context_menu)
        self.view.ui.up_button.clicked.connect(self.up_bookmark)
        self.view.ui.down_button.clicked.connect(self.down_bookmark)
        self.view.ui.add_button.clicked.connect(self.add_bookmark_from_tree)
        self.view.ui.del_button.clicked.connect(self.remove_bookmark)

        # 最近使ったファイル
        self.view.ui.recent_file_list_2.customContextMenuRequested.connect(self.recent_file_context_menu)
        self.view.ui.recent_file_list_2.doubleClicked.connect(self.recent_file_double_click_event)
        self.view.ui.update_recent_file_button.clicked.connect(self.update_recent_file_list)

        # 拡張子フィルター
        for ext_button in self.ext_filter_buttons:
            ext_button.toggled.connect(self.ext_button_event)

        # 検索ディレクトリ
        self.view.ui.root_dir_line.editingFinished.connect(self.search_root_path_update_event)
        self.view.ui.set_root_button.clicked.connect(self.set_root_button_event)
        self.view.ui.update_button.clicked.connect(self.search_root_path_update_event)

        # 検索文字列
        self.view.ui.search_line.editingFinished.connect(self.search_word_update_event)

        # テーブルビュー
        self.view.ui.file_table.clicked.connect(self.file_table_click_event)
        self.view.ui.file_table.doubleClicked.connect(self.file_table_double_click_event)
        self.view.ui.file_table.customContextMenuRequested.connect(self.file_table_context_menu)
        self.view.ui.copy_to_clipboard_button.clicked.connect(self.copy_to_clipboard_button_event)

    def dir_tree_click_event(self, index):

        if not index.isValid():
            return

        self.view.ui.dir_tree.setExpanded(index, True)

    def dir_tree_double_click_event(self, index):
        """ツリーダブルクリック時の処理
        """

        if not index.isValid():
            return

        path = self.file_system_model.filePath(index)

        if os.path.isfile(path):
            self.main.open_operation_begin([path])
        else:

            if self.main.set_rootdir_on_double_clicked:
                self.view.ui.root_dir_line.setText(path)
                self.search_root_path_update_event()

    def bookmark_double_click_event(self):
        """ブックマークダブルクリック時の処理
        """

        item = self.view.ui.bookmark_list.currentItem()

        if item:
            path = self.view.ui.bookmark_list.itemWidget(item).path

            if os.path.isdir(path):
                self.set_search_root_path(path)
            else:
                if os.path.splitext(path)[-1].replace('.', '') in const.EXTENT_LIST:
                    self.main.open_operation_begin([path])

    def recent_file_double_click_event(self):
        """最近使ったファイルダブルクリック時の処理
        """

        item = self.view.ui.recent_file_list_2.currentItem()

        if item:
            self.main.open_operation_begin([self.view.ui.recent_file_list_2.itemWidget(item).path])

    def file_table_click_event(self, index):
        """ファイルテーブルクリック時の処理
        """

        indexes = self.view.ui.file_table.selectedIndexes()
        current_paths = []

        for index in indexes:

            if index.column() != 0:
                continue

            if index.isValid():
                maped_index = self.proxy_model.mapToSource(index)
                item = self.file_table_model.items[maped_index.row()]
                current_paths.append(item.path)

        if current_paths:
            self.view.ui.selection_path_line.setText(current_paths[0])
        else:
            self.view.ui.selection_path_line.setText('')

    def file_table_double_click_event(self, index):
        """ファイルテーブルダブルクリック時の処理
        """

        indexes = self.view.ui.file_table.selectedIndexes()
        current_paths = []

        for index in indexes:

            if index.column() != 0:
                continue

            if index.isValid():
                maped_index = self.proxy_model.mapToSource(index)
                item = self.file_table_model.items[maped_index.row()]
                current_paths.append(item.path)

        if current_paths:
            self.view.ui.selection_path_line.setText(current_paths[0])
        else:
            self.view.ui.selection_path_line.setText('')

        self.main.open_operation_begin(current_paths)

    def set_root_button_event(self):
        """セットルートボタンをクリック時の処理
        """

        current_path = ''
        index = self.view.ui.dir_tree.currentIndex()
        if index.isValid():
            current_path = self.file_system_model.filePath(index)

        if not current_path:
            return

        self.set_search_root_path(current_path)

    def copy_to_clipboard_button_event(self):
        """クリップボードにコピーボタンのイベント
        """

        path = self.view.ui.selection_path_line.text()
        self.main.copy_path_to_clipboard([path])

    def ext_button_event(self):
        """拡張子フィルターボタンクリック時の処理
        """

        # ボタンのトグル情報から拡張子フィルターを作成して、リストを更新
        new_filter = self.get_ext_filter_from_ui()

        if new_filter != self.current_ext_filter:
            self.current_ext_filter = new_filter
            self.search_word_update_event()

        self.set_ext_button_tip()

    def get_ext_filter_from_ui(self):
        """ボタンのトグル情報から拡張子フィルターを作成

        Returns:
            [str]: フィルタリングする拡張子のリスト
        """

        results = []
        for ext_button in self.ext_filter_buttons:
            if ext_button.isChecked():
                results.append('.' + ext_button.text())

        return results

    def set_ext_filter(self, filter):
        """拡張子フィルターをセット

        Args:
            filter ([str]): フィルタリングする拡張子のリスト
        """

        self.current_ext_filter = filter

        for ext_button in self.ext_filter_buttons:
            if '.' + ext_button.text() in self.current_ext_filter:
                ext_button.setChecked(True)

        self.set_ext_button_tip()

    def set_ext_button_tip(self):

        for ext_button in self.ext_filter_buttons:
            if ext_button.isChecked():
                ext_button.setToolTip('.{} ファイルを非表示にします'.format(ext_button.text()))
            else:
                ext_button.setToolTip('.{} ファイルを表示します'.format(ext_button.text()))

    def search_root_path_update_event(self):
        """検索ルートパス更新時処理
        """

        self.search_root_path = self.view.ui.root_dir_line.text()
        self.tree_path_sync()
        self.update_path_pool()
        self.update_file_table()
        self.view.ui.selection_path_line.setText('')

    def set_search_root_path(self, path):
        """検索ルートパスをセット

        Args:
            path (str): 検索ルートパス
        """

        if not path or not os.path.exists(path):
            return

        self.view.ui.root_dir_line.setText(path)
        self.search_root_path_update_event()

    def tree_path_sync(self):
        """ルートが更新された際にツリーのパスも合わせる

        Args:
            path (str): 合わせるパス
        """

        index = self.file_system_model.index(self.search_root_path)
        self.view.ui.dir_tree.setCurrentIndex(index)
        self.view.ui.dir_tree.scrollTo(index, QtWidgets.QAbstractItemView.EnsureVisible)

    def update_path_pool(self):
        """ルートフォルダ以下を走査し対象ファイルのリストを更新
        """

        self.is_incomplete_search = False

        if not os.path.exists(self.search_root_path):
            self.file_path_pool = []
            return

        ext_re = re.compile(self.ext_pattern)

        walk_file_count = 0
        file_paths = []

        for curDir, dirs, files in os.walk(self.search_root_path):
            for file in files:

                if walk_file_count > self.main.walk_file_limit:
                    # 走査するファイル上限を超えた場合は、不完全なサーチフラグを立て、そこまでのリストを返す
                    message = 'ルートフォルダ以下のファイル数が上限（{}）を超えたため途中結果を表示します\n'.format(self.main.walk_file_limit)
                    message += 'ルートフォルダを変更するか、メニューの「設定」から上限を引き上げてください'
                    cmds.confirmDialog(m=message)
                    self.file_path_pool = file_paths
                    self.is_incomplete_search = True
                    return

                walk_file_count += 1
                if ext_re.search(file):
                    file_paths.append(os.path.join(curDir, file))

        self.file_path_pool = file_paths

    def update_file_table(self):
        """ファイルテーブルを更新
        """

        self.search_str = self.view.ui.search_line.text()
        search_result = self.search_files(self.file_path_pool, self.search_str, self.current_ext_filter, self.main.replace_dict)
        self.file_table_model.refresh(search_result)
        self.update_info_label()

    def search_files(self, path_pool, search_str, ext_filter=[], replace_dict={}):
        """ファイル一覧から特定のファイルを探索する

        Args:
            path_pool (list): ファイルパス一覧
            search_str (str): 検索ワード
            ext_filter (list): 検索対象にするファイル拡張子
            replace_dict (dict): 検索ワードを置換する辞書
        Returns:
            list: 検索結果のパスリスト
        """

        if not path_pool:
            return []

        str_filter_paths = path_pool
        if search_str:
            str_filter_paths = [x for x in str_filter_paths if utility.is_hit_text(os.path.basename(x), search_str, replace_dict)]

        if not ext_filter:
            return str_filter_paths
        else:
            return [x for x in str_filter_paths if os.path.splitext(x)[-1] in ext_filter]

    def search_word_update_event(self):
        """検索ワード更新時処理
        """

        if not self.file_path_pool:
            self.search_root_path_update_event()

        self.update_file_table()

    def update_info_label(self):
        """情報表示ラベルの更新
        """

        if not self.search_root_path:
            self.view.ui.info_label.setText('ルートフォルダを指定してください')
        if not self.file_path_pool:
            self.view.ui.info_label.setText('該当データなし')
            return

        source_length_str = str(len(self.file_path_pool))
        if self.is_incomplete_search:
            source_length_str += '( ※不完全な検索結果※ )'

        result_length_str = str(self.file_table_model.rowCount(None))

        self.view.ui.info_label.setText('検索結果 : {} / {}'.format(result_length_str, source_length_str))

    def update_recent_file_list(self):
        """最近使用したファイルリストを更新
        MayaのoptionVarから取得してくる
        """

        recent_file_list = self.view.ui.recent_file_list_2
        recent_file_list.clear()

        recent_files = cmds.optionVar(q='RecentFilesList')

        if not recent_files:
            return

        for recent_file in reversed(recent_files):

            item = QtWidgets.QListWidgetItem()
            item_widget = view.BookmarkListItemWidget(recent_file, recent_file_list)
            item_widget.setEnabled(os.path.exists(recent_file))
            item.setSizeHint(item_widget.sizeHint())
            recent_file_list.addItem(item)
            recent_file_list.setItemWidget(item, item_widget)

    def add_bookmark_from_tree(self):
        """ツリーで選択しているパスをブックマークに追加
        """

        current_path = ''
        index = self.view.ui.dir_tree.currentIndex()
        if index.isValid():
            current_path = self.file_system_model.filePath(index)

        if not current_path:
            return

        self.add_bookmarks([current_path])

    def add_bookmarks(self, paths):
        """ブックマークに追加

        Args:
            paths ([str]): ブックマークするファイルパスリスト
        """

        for path in paths:

            # すでに入っている場合は追加せず選択
            for i in range(self.view.ui.bookmark_list.count()):
                item = self.view.ui.bookmark_list.item(i)
                item_widget = self.view.ui.bookmark_list.itemWidget(item)
                if item_widget.path == path:
                    self.view.ui.bookmark_list.setItemSelected(item, True)
                    return

            this_item = QtWidgets.QListWidgetItem()
            custom_item_widget = view.BookmarkListItemWidget(path, self.view.ui.bookmark_list)
            this_item.setSizeHint(custom_item_widget.sizeHint())
            self.view.ui.bookmark_list.addItem(this_item)
            self.view.ui.bookmark_list.setItemWidget(this_item, custom_item_widget)

        self.save_bookmark()

    def remove_bookmark(self):
        '''
        選択しているブックマークを削除する
        '''
        item = self.view.ui.bookmark_list.currentItem()
        if item:
            self.view.ui.bookmark_list.takeItem(self.view.ui.bookmark_list.row(item))
            self.save_bookmark()

    def down_bookmark(self):
        '''
        選択しているブックマークを下に移動
        '''
        row = self.view.ui.bookmark_list.currentRow()
        if row < self.view.ui.bookmark_list.count() - 1:
            new_item = QtWidgets.QListWidgetItem()
            new_path = self.view.ui.bookmark_list.itemWidget(self.view.ui.bookmark_list.item(row + 1)).path
            new_item_widget = view.BookmarkListItemWidget(new_path, self.view.ui.bookmark_list)
            self.view.ui.bookmark_list.insertItem(row, new_item)
            self.view.ui.bookmark_list.setItemWidget(new_item, new_item_widget)
            self.view.ui.bookmark_list.takeItem(row + 2)
            self.view.ui.bookmark_list.setCurrentRow(row + 1)
            self.save_bookmark()

    def up_bookmark(self):
        '''
        選択しているブックマークを上に移動
        '''
        row = self.view.ui.bookmark_list.currentRow()
        if row > 0:
            new_item = QtWidgets.QListWidgetItem()
            new_path = self.view.ui.bookmark_list.itemWidget(self.view.ui.bookmark_list.currentItem()).path
            new_item_widget = view.BookmarkListItemWidget(new_path, self.view.ui.bookmark_list)
            self.view.ui.bookmark_list.insertItem(row - 1, new_item)
            self.view.ui.bookmark_list.setItemWidget(new_item, new_item_widget)
            self.view.ui.bookmark_list.takeItem(row + 1)
            self.view.ui.bookmark_list.setCurrentRow(row - 1)
            self.save_bookmark()

    def dir_tree_context_menu(self, pos):
        """ツリービューのコンテキストメニューを作成

        Args:
            pos (Qpoint): シグナルで送られてくるポジション
        """

        current_path = ''
        index = self.view.ui.dir_tree.currentIndex()
        if index.isValid():
            current_path = self.file_system_model.filePath(index)

        if not current_path:
            return

        action_dict_list = []

        if os.path.isfile(current_path):

            ext = os.path.splitext(current_path)[-1]

            if ext.replace('.', '') in const.EXTENT_LIST:
                action_dict_list = self.main.get_file_action_dict_list([current_path], True, const.MENU_TYPE_EXPLORER)
            else:
                action_dict_list = self.main.get_file_action_dict_list([current_path], False, const.MENU_TYPE_EXPLORER)

        else:
            action_dict_list = self.main.get_dir_action_dict_list([current_path], const.MENU_TYPE_EXPLORER)

        utility.create_qt_context_menu(self.view.ui.dir_tree, pos, action_dict_list)

    def bookmark_context_menu(self, pos):
        """ブックマークリストのコンテキストメニューを作成

        Args:
            pos (Qpoint): シグナルで送られてくるポジション
        """

        current_path = ''
        item = self.view.ui.bookmark_list.currentItem()
        if item:
            current_path = self.view.ui.bookmark_list.itemWidget(item).path

        if not current_path:
            return

        if os.path.isfile(current_path):

            ext = os.path.splitext(current_path)[-1]

            if ext.replace('.', '') in const.EXTENT_LIST:
                action_dict_list = self.main.get_file_action_dict_list([current_path], True, const.MENU_TYPE_BOOKMARK)
            else:
                action_dict_list = self.main.get_file_action_dict_list([current_path], False, const.MENU_TYPE_BOOKMARK)
        else:
            action_dict_list = self.main.get_dir_action_dict_list([current_path], const.MENU_TYPE_BOOKMARK)

        utility.create_qt_context_menu(self.view.ui.bookmark_list, pos, action_dict_list)

    def recent_file_context_menu(self, pos):
        """最近使用したファイルリストのコンテキストメニューを作成

        Args:
            pos (Qpoint): シグナルで送られてくるポジション
        """

        recent_file_list = self.view.ui.recent_file_list_2

        current_paths = []
        sel_items = recent_file_list.selectedItems()
        current_paths = [recent_file_list.itemWidget(x).path for x in sel_items]

        if not current_paths:
            return

        action_dict_list = self.main.get_file_action_dict_list(current_paths, True, const.MENU_TYPE_EXPLORER)

        utility.create_qt_context_menu(recent_file_list, pos, action_dict_list)

    def file_table_context_menu(self, pos):
        """ファイルテーブルのコンテキストメニューを作成

        Args:
            pos (Qpoint): シグナルで送られてくるポジション
        """

        indexes = self.view.ui.file_table.selectedIndexes()
        current_paths = []

        for index in indexes:

            if index.column() != 0:
                continue

            if index.isValid():
                item = self.file_table_model.items[index.row()]
                current_paths.append(item.path)

        action_dict_list = self.main.get_file_action_dict_list(current_paths, True, const.MENU_TYPE_EXPLORER)

        utility.create_qt_context_menu(self.view.ui.file_table, pos, action_dict_list)

    def add_collection(self, paths):
        """パスをコレクションに追加

        Args:
            paths ([str]): コピーするパスリスト
        """

        scene_collector = self.main.scene_collector
        collection = self.main.collection_tab

        label_names = []
        new_col_label = '新規コレクションを作成して追加'

        col_ids = scene_collector.get_collection_ids_by_order()

        default_target_index = 0

        if col_ids:
            for i, col_id in enumerate(col_ids):
                col = scene_collector.get_collection(col_id)
                if col:
                    label_names.append(str(i + 1) + ': ' + col['Name'])

                    # 前回追加時のターゲットがあればデフォルトで選択されているようにする
                    if col_id == self.prev_target_col_id:
                        default_target_index = i

        label_names.append(new_col_label)

        sel, result = QtWidgets.QInputDialog.getItem(
            None,
            'コレクション選択',
            '追加するコレクションを選択してください',
            label_names,
            editable=False,
            current=default_target_index
        )

        if not result:
            return

        target_col_id = ''

        if sel == new_col_label:
            target_col_id = collection.col_add_event()

        else:
            sel_num = int(sel.split(':')[0])
            target_col_id = col_ids[sel_num - 1]

        if not target_col_id:
            return

        add_results = collection.add_col_item(target_col_id, paths)
        if not add_results:
            cmds.warning('Add item failed to {}'.format(sel))
        else:
            self.prev_target_col_id = target_col_id

    def save_setting(self):
        """ツール情報の保存
        """

        setting = self.main.setting

        # splitter
        setting.setValue(const.SETTING_MAIN_SPLITTER, self.view.ui.main_splitter.saveState())
        setting.setValue(const.SETTING_SUB_SPLITTER, self.view.ui.sub_splitter.saveState())

        # self.search_root_path
        setting.setValue(const.SETTING_ROOT_PATH, self.search_root_path)
        # self.search_str
        setting.setValue(const.SETTING_SEARCH_STR, self.search_str)
        # self.current_ext_filter
        setting.setValue(const.SETTING_EXT_FILTER, ','.join(self.current_ext_filter))
        # self.is_incomplete_search
        setting.setValue(const.SETTING_IS_PREVIOUS_INCOMPLETE, str(self.is_incomplete_search))

    def load_setting(self):
        """ツール情報の読み込み
        """

        setting = self.main.setting

        # splitter
        if setting.value(const.SETTING_MAIN_SPLITTER):
            self.view.ui.main_splitter.restoreState(setting.value(const.SETTING_MAIN_SPLITTER))

        if setting.value(const.SETTING_SUB_SPLITTER):
            self.view.ui.sub_splitter.restoreState(setting.value(const.SETTING_SUB_SPLITTER))

        # self.search_root_path
        if setting.value(const.SETTING_ROOT_PATH):
            self.search_root_path = setting.value(const.SETTING_ROOT_PATH)

        # self.search_str
        if setting.value(const.SETTING_SEARCH_STR):
            self.search_str = setting.value(const.SETTING_SEARCH_STR)

        # self.current_ext_filter
        if setting.value(const.SETTING_EXT_FILTER):
            self.current_ext_filter = setting.value(const.SETTING_EXT_FILTER).split(',')

        # self.is_incomplete_search
        if setting.value(const.SETTING_IS_PREVIOUS_INCOMPLETE):
            val = utility.str_setting_to_bool(setting.value(const.SETTING_IS_PREVIOUS_INCOMPLETE))
            self.is_incomplete_search = val

    def save_bookmark(self):
        """ブックマーク情報の保存
        """

        save_paths = []
        bookmark_count = self.view.ui.bookmark_list.count()

        if not bookmark_count:
            return

        for i in range(bookmark_count):
            item = self.view.ui.bookmark_list.item(i)
            save_paths.append(self.view.ui.bookmark_list.itemWidget(item).path)

        book_mark_file_path = utility.get_bookmark_file_path()

        if not os.path.exists(os.path.dirname(book_mark_file_path)):
            os.makedirs(os.path.dirname(book_mark_file_path))

        with open(book_mark_file_path, 'w') as f:
            f.write(','.join(save_paths))

    def load_bookmark(self):
        """ブックマーク情報の読み込み
        """

        self.view.ui.bookmark_list.clear()
        load_paths = []

        if not os.path.exists(utility.get_bookmark_file_path()):

            # TkgSceneOpenerのブックマークがあれば読み込む
            load_paths = self.read_tkg_scene_opener_bookmark()

        else:
            load_paths = self.read_bookmark()

        self.add_bookmarks(load_paths)

    def read_bookmark(self):
        """ブックマークを取得

        Returns:
            [str]: ブックマークパスのリスト
        """

        if not os.path.exists(utility.get_bookmark_file_path()):
            return []

        bookmark_paths = []

        with open(utility.get_bookmark_file_path(), 'r') as f:
            bookmark_paths = f.read().split(',')

        return [utility.normalize_path(x) for x in bookmark_paths]

    def read_tkg_scene_opener_bookmark(self):
        """TkgSceneOpenerのブックマークを取得
        初めてツールを起動したときにTkgSceneOpenerのブックマークを復元する

        Returns:
            [str]: TkgSceneOpenerのブックマークパスリスト
        """

        load_paths = []
        cy_scene_opener_file_path = utility.get_tkg_scene_opener_bookmark_file_path()

        if os.path.exists(cy_scene_opener_file_path):

            confirm = cmds.confirmDialog(
                title='TkgSceneOpenerからの読み込み',
                message='TkgSceneOpenerからブックマークを読み込みますか？',
                button=['読み込む', 'キャンセル'],
                defaultButton='読み込む',
                cancelButton='キャンセル',
                dismissString='キャンセル')

            if confirm == 'キャンセル':
                return []

            with open(cy_scene_opener_file_path, 'r') as f:
                tmp_paths = f.read().split('\n')

            load_paths = [x for x in tmp_paths if os.path.exists(x)]

        return load_paths
