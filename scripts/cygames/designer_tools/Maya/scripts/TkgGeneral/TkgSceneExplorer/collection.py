# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

from PySide2 import QtWidgets, QtCore

import os
import copy

import maya.cmds as cmds

from . import view
from . import utility
from . import const
from . import scene_opener
from . import scene_collector
from .ui import model

try:
    # Maya2022-
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


class Collection(object):

    def __init__(self, main):

        self.main = main
        self.view = main.view
        self.setting = main.setting
        self.scene_collector = main.scene_collector
        self.replace_dict = []
        self.set_col_dirty(False)

        self.init_col_sel_ids = []
        self.init_col_item_sel_ids = []

        self.__col_list_drag_filter = view.DragItemFilter()
        self.__col_item_list_drag_filter = view.DragItemFilter()

        self.__col_widget_cache = {}
        self.__col_item_widget_cache = {}

    def initialize_ui(self):

        # コレクションリスト
        self.view.col_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.view.col_list.installEventFilter(self.__col_list_drag_filter)

        # コレクションアイテムリスト
        self.view.col_file_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.view.col_file_list.installEventFilter(self.__col_item_list_drag_filter)

        # search_lineの削除ボタン押下時のイベント・アクション設定
        self.view.setColUiSearchLine(self.item_search_line_change_event)

        # mainでパラメーターがloadされていることがあるのでUIを更新しておく
        self.update_collection_list()
        self.set_init_col_selection()
        self.update_collection_item_list()
        self.set_init_col_item_selection()

    def setup_view_event(self):
        """UIのevent設定
        """

        # 読み込みボタン
        self.view.ui.col_new_button.clicked.connect(self.col_new_event)
        self.view.ui.col_load_button.clicked.connect(self.col_load_event)
        self.view.ui.col_save_button.clicked.connect(self.col_save_event)
        self.view.ui.col_save_as_button.clicked.connect(self.col_save_as_event)

        # コレクションの操作ボタン
        self.view.ui.col_add_button.clicked.connect(self.col_add_event)

        # コレクションリスト
        self.view.col_list.clicked.connect(self.col_list_click_event)
        self.__col_list_drag_filter.drop_item.connect(self.col_list_drag_event)
        self.view.col_list.customContextMenuRequested.connect(self.col_context_menu)

        # 検索バー
        self.view.ui.item_search_line.editingFinished.connect(self.item_search_line_change_event)

        # コレクションアイテムリスト
        self.view.col_file_list.clicked.connect(self.col_item_list_change_event)
        self.view.col_file_list.doubleClicked.connect(self.col_item_list_double_click_event)
        self.view.col_file_list.customContextMenuRequested.connect(self.col_item_context_menu)
        self.__col_item_list_drag_filter.drop_item.connect(self.col_item_list_drag_event)

        self.view.ui.copy_item_to_clipboard_button.clicked.connect(self.copy_item_to_clipboard_button_event)

    def col_list_click_event(self):
        """コレクションリスト操作時イベント
        """

        # コレクションアイテムリスト更新
        self.update_collection_base(False, True, force_col_item_scroll=True)

        # クリップボードコピーのパス更新
        self.update_path_line()

    def col_list_drag_event(self):
        """コレクションリストドラッグ時イベント
        """

        # コレクションアイテムリスト更新
        self.update_collection_base(True, True)

        # コレクション順序の入れ替えの可能性があるので変更フラグを立てる
        self.set_col_dirty(True)

        # クリップボードコピーのパス更新
        self.update_path_line()

    def item_search_line_change_event(self):
        """検索バー更新イベント
        """

        self.update_collection_base(False, True, force_col_item_scroll=True)

    def col_item_list_change_event(self):
        """コレクションアイテムリスト操作時イベント
        """

        self.update_path_line()

    def col_item_list_drag_event(self):
        """コレクションアイテムリストドラッグ時イベント
        """

        self.col_item_list_change_event()
        self.update_collection_item_order_from_ui()

        # コレクション順序の入れ替えの可能性があるので変更フラグを立てる
        self.set_col_dirty(True)

    def col_item_list_double_click_event(self):
        """コレクションアイテムのダブルクリック時イベント
        """

        col_file_list = self.view.col_file_list
        col_file_sel_items = col_file_list.selectedItems()
        col_item_sel_paths = [col_file_list.itemWidget(x).path for x in col_file_sel_items]

        self.main.open_operation_begin(col_item_sel_paths)

    def set_init_col_selection(self):
        """col_listに初期選択を反映
        """

        col_list = self.view.col_list
        scroll_col_target = None

        for i in range(col_list.count()):

            item = col_list.item(i)
            widget = col_list.itemWidget(item)

            if widget.col_id in self.init_col_sel_ids:

                item.setSelected(True)
                widget.is_active = True

                if not scroll_col_target:
                    scroll_col_target = item
            else:
                item.setSelected(False)
                widget.is_active = False

            widget.set_color()

        col_list.scrollToItem(scroll_col_target)

    def set_init_col_item_selection(self):
        """col_item_listに初期選択を反映
        """

        col_file_list = self.view.col_file_list
        scroll_item_target = None

        for i in range(col_file_list.count()):

            item = col_file_list.item(i)

            if col_file_list.itemWidget(item).item_id in self.init_col_item_sel_ids:

                item.setSelected(True)

                if not scroll_item_target:
                    scroll_item_target = item
            else:
                item.setSelected(False)

        col_file_list.scrollToItem(scroll_item_target)

    def update_collection_base(self, need_col_list_update, need_col_item_list_update, force_col_scroll=False, force_col_item_scroll=False):
        """コレクション、コレクションアイテムを更新
        self.scene_collectorに最新を記録して、UIを再構築する

        Args:
            need_col_list_update (bool):コレクションリストを再構築する必要があるか
            need_col_item_list_update (bool):コレクションアイテムリストを再構築する必要があるか
            force_col_scroll (bool, optional): コレクションリストを選択項目へスクロールするか. Defaults to False.
            force_col_item_scroll (bool, optional): コレクションアイテムリストを選択項目へスクロールするか. Defaults to False.
        """

        self.update_collection_order_from_ui()
        self.update_collection_item_order_from_ui()

        # コレクションリストの選択を保存
        col_list = self.view.col_list
        col_sel_items = col_list.selectedItems()
        col_sel_ids = [col_list.itemWidget(x).col_id for x in col_sel_items]

        # コレクションリストの再構築
        if need_col_list_update:
            self.update_collection_list()

        # コレクションリストの選択を反映（カラー適用があるので再構築関係なく実行）
        scroll_col_target = None

        for i in range(col_list.count()):

            item = col_list.item(i)
            widget = col_list.itemWidget(item)

            if widget.col_id in col_sel_ids:

                item.setSelected(True)
                widget.is_active = True

                if not scroll_col_target:
                    scroll_col_target = item
            else:
                item.setSelected(False)
                widget.is_active = False

            widget.set_color()

        # コレクションリストの再構築が行われたら選択へスクロール
        if scroll_col_target and need_col_list_update and force_col_scroll:
            col_list.scrollToItem(scroll_col_target)

        # コレクションアイテムリストの選択を保存
        col_file_list = self.view.col_file_list
        col_file_sel_items = col_file_list.selectedItems()
        col_item_sel_ids = [col_file_list.itemWidget(x).item_id for x in col_file_sel_items]

        # コレクションアイテムリストの再構築
        if need_col_item_list_update:

            self.update_collection_item_list()

            # コレクションアイテムリストの選択を復元
            scroll_item_target = None

            for i in range(col_file_list.count()):

                item = col_file_list.item(i)

                if col_file_list.itemWidget(item).item_id in col_item_sel_ids:

                    item.setSelected(True)

                    if not scroll_item_target:
                        scroll_item_target = item
                else:
                    item.setSelected(False)

            # 選択項目へスクロール
            if scroll_item_target and force_col_item_scroll:
                col_file_list.scrollToItem(scroll_item_target)

    def update_collection_list(self):
        """コレクションリストの構築
        """

        collection_list = self.view.col_list
        collection_list.clear()
        self.__col_widget_cache = {}

        if not self.scene_collector:
            self.scene_collector.initialize(None)

        ordered_col_ids = self.scene_collector.get_collection_ids_by_order()

        for col_id in ordered_col_ids:

            col_dict = self.scene_collector.get_collection(col_id)
            col_id = col_id
            name = col_dict['Name']
            color = col_dict['Color']

            item_widget = view.CollectionWidget(col_id, name, [color['r'], color['g'], color['b']])
            item = QtWidgets.QListWidgetItem()
            item.setSizeHint(item_widget.sizeHint())
            collection_list.addItem(item)
            collection_list.setItemWidget(item, item_widget)

            item_widget.change_collection_name.connect(self.col_change_name_event)
            item_widget.change_color.connect(self.col_change_color_event)
            item_widget.add_collection_item.connect(self.add_col_item_event)
            item_widget.del_collection.connect(self.col_del_event)

            self.__col_widget_cache[id(item)] = item_widget

    def update_collection_item_list(self):
        """コレクションアイテムリストの構築
        """

        self.view.col_file_list.clear()
        self.__col_item_widget_cache = {}

        col_list = self.view.col_list
        sel_items = col_list.selectedItems()
        sel_col_ids = [col_list.itemWidget(x).col_id for x in sel_items]

        # 選択中のコレクションリストを取得
        col_item_ids = []

        for col_id in sel_col_ids:

            col_file_ids = self.scene_collector.get_child_collection_item_ids(col_id)

            if not col_file_ids:
                continue

            col_item_ids.extend(col_file_ids)

        col_item_ids = self.scene_collector.get_sorted_collection_item_ids(col_item_ids)

        # 検索ワード取得
        search_str = self.view.ui.item_search_line.text()
        replace_dict = self.main.replace_dict

        # アイテムリストを更新
        for col_item_id in col_item_ids:

            col_id, col = self.scene_collector.get_parent_collection(col_item_id)
            col_item = self.scene_collector.get_collection_item(col_item_id)

            # 検索ワード入力があればフィルター
            if search_str:
                name_hit = utility.is_hit_text(os.path.basename(col_item['Path']), search_str, replace_dict)
                desc_hit = utility.is_hit_text(os.path.basename(col_item['Desc']), search_str, replace_dict)
                if not name_hit and not desc_hit:
                    continue

            item_widget = view.CollectionFileItemWidget(
                col_item_id,
                col_item['Path'],
                col_item['Desc'],
                [col['Color']['r'], col['Color']['g'], col['Color']['b']]
            )

            item_widget.change_collection_desc.connect(self.col_item_change_desc_event)
            item_widget.delete_collection_item.connect(self.delete_collection_item)

            item = QtWidgets.QListWidgetItem()
            item.setSizeHint(item_widget.sizeHint())
            self.view.col_file_list.addItem(item)
            self.view.col_file_list.setItemWidget(item, item_widget)

            self.__col_item_widget_cache[id(item)] = item_widget

    def update_collection_order_from_ui(self):
        """コレクションのUIオーダー情報をself.scene_collectorに記録
        """

        collection_list = self.view.col_list

        current_col_ids = []
        current_col_orders = []

        for i in range(collection_list.count()):

            item = collection_list.item(i)

            # QlistWidgetitemWidget(item)でメモリリークしていたのでキャッシュからとる
            widget = self.__col_widget_cache.get(id(item))

            if not widget:
                continue

            current_col_ids.append(widget.col_id)

            # 現在の並び順を取得.削除されている場合は取得できないので-1を入れる
            currnt_order = self.scene_collector.get_collection_order(widget.col_id)
            if not currnt_order:
                currnt_order = -1

            current_col_orders.append(currnt_order)

        # 表示されているコレクションのオーダーを表示順に入れ替える
        new_col_orders = sorted(current_col_orders)
        self.scene_collector.direct_reorder_collection(current_col_ids, new_col_orders)

    def update_collection_item_order_from_ui(self):
        """コレクションアイテムのUIオーダー情報をself.scene_collectorに記録
        """

        collection_item_list = self.view.col_file_list

        current_item_ids = []
        current_item_orders = []

        for i in range(collection_item_list.count()):

            item = collection_item_list.item(i)

            # QlistWidgetitemWidget(item)でメモリリークしていたのでキャッシュからとる
            widget = self.__col_item_widget_cache.get(id(item))

            if not widget:
                continue

            item_id = widget.item_id
            current_item_ids.append(item_id)

            # 現在の並び順を取得.削除されている場合は取得できないので-1を入れる
            current_order = self.scene_collector.get_collection_item_order(item_id)
            if not current_order:
                current_order = -1

            current_item_orders.append(current_order)

        # 表示されているコレクションアイテムのオーダーを表示順に入れ替える
        new_item_orders = sorted(current_item_orders)
        self.scene_collector.direct_reorder_collection_item(current_item_ids, new_item_orders)

    def get_item_paths(self, col_ids):
        """コレクションからアイテムのパスリストを取得
        """

        return self.scene_collector.get_colletion_item_paths(col_ids)

    def col_change_name_event(self, col_id):
        """コレクション名の変更イベント
        """

        current_name = self.scene_collector.get_collection_name(col_id)

        new_name, ok = QtWidgets.QInputDialog.getText(
            None,
            'コレクション名の変更',
            '新しいコレクション名',
            QtWidgets.QLineEdit.Normal,
            current_name
        )
        if ok:
            self.scene_collector.set_collection_name(col_id, new_name)
            self.update_collection_base(True, False)

            self.set_col_dirty(True)

    def col_change_color_event(self, col_id):
        """コレクションカラー変更イベント

        Args:
            col_id (str): コレクションID
        """

        color_dialog = QtWidgets.QColorDialog()
        response = color_dialog.exec_()
        if response == QtWidgets.QDialog.Accepted:
            # OKが押された時は処理を続ける
            chosen = color_dialog.currentColor()
            rgb = chosen.getRgb()
            self.scene_collector.set_collection_color(col_id, rgb)
            self.update_collection_base(True, True)

            self.set_col_dirty(True)

    def col_item_change_desc_event(self, col_item_id):
        """コレクションアイテムの説明の変更イベント
        """

        current_desc = self.scene_collector.get_collection_item_desc(col_item_id)

        new_desc, ok = QtWidgets.QInputDialog.getText(
            None,
            'シーン説明の追加',
            'シーンの説明',
            QtWidgets.QLineEdit.Normal,
            current_desc
        )
        if ok:
            self.scene_collector.set_collection_item_desc(col_item_id, new_desc)
            self.update_collection_base(False, True)

            self.set_col_dirty(True)

    def delete_collection_item(self, col_item_id):
        """コレクションアイテムの削除
        """

        if self.main.col_obj_del_confirm:

            del_confirm_dialog = view.ColObjDelConfirmDialog(self.view)
            result = del_confirm_dialog.exec_()
            never_show_again = del_confirm_dialog.never_show_again_check.isChecked()

            if never_show_again:
                self.main.col_obj_del_confirm = False

            if not result:
                return

        self.scene_collector.del_collection_item(col_item_id)
        self.update_collection_base(False, True)

        self.set_col_dirty(True)

    def col_add_event(self):
        """コレクションの追加イベント
        """

        text, ok = QtWidgets.QInputDialog.getText(
            self.view,
            'コレクション追加',
            '追加するコレクション名',
            QtWidgets.QLineEdit.Normal,
        )
        if ok:
            add_id = self.scene_collector.add_collection(text)
            self.update_collection_base(True, False)

            self.set_col_dirty(True)
            return add_id

    def col_del_event(self, id):
        """コレクションの削除イベント
        """

        if self.main.col_obj_del_confirm:

            del_confirm_dialog = view.ColObjDelConfirmDialog(self.view)
            result = del_confirm_dialog.exec_()
            never_show_again = del_confirm_dialog.never_show_again_check.isChecked()

            if never_show_again:
                self.main.col_obj_del_confirm = False

            if not result:
                return

        self.scene_collector.del_collection(id)
        self.update_collection_base(True, True)

        self.set_col_dirty(True)

    def add_col_item_event(self, col_id):
        """コレクションアイテムの追加イベント
        """

        # ファイルを選択させる
        filter = 'Scene Files (*.ma *.mb *.fbx)'
        files = cmds.fileDialog2(cap='コレクションに追加するファイルを選択', fm=1, ff=filter)

        if files:
            add_col_item = self.add_col_item(col_id, files)

            if add_col_item:
                self.set_col_dirty(True)

            return add_col_item

    def add_col_item(self, col_id, paths):
        """コレクションにアイテムを追加

        Args:
            col_id (str): アイテムを追加するコレクションID
            path (str): 追加するアイテムのパス
        """

        add_paths = []

        for path in paths:
            if os.path.splitext(path)[-1].replace('.', '') in const.EXTENT_LIST:
                add_paths.append(path)

        add_ids = self.scene_collector.add_collection_item(col_id, add_paths)
        self.update_collection_base(False, True)

        if add_ids:
            self.set_col_dirty(True)

        return add_ids

    def col_context_menu(self, pos):
        """コレクションリストのコンテキストメニューを作成

        Args:
            pos (Qpoint): シグナルで送られてくるポジション
        """

        collection_list = self.view.col_list

        sel_cols = collection_list.selectedItems()
        sel_col_ids = [collection_list.itemWidget(x).col_id for x in sel_cols]

        if not sel_col_ids:
            return

        action_dict_list = self.main.get_collection_action_dict_list(sel_col_ids)

        utility.create_qt_context_menu(collection_list, pos, action_dict_list)

    def col_item_context_menu(self, pos):
        """コレクションアイテムリストのコンテキストメニューを作成

        Args:
            pos (Qpoint): シグナルで送られてくるポジション
        """

        collection_item_list = self.view.col_file_list

        sel_items = collection_item_list.selectedItems()
        sel_col_item_paths = [collection_item_list.itemWidget(x).path for x in sel_items]

        if not sel_col_item_paths:
            return

        action_dict_list = self.main.get_file_action_dict_list(sel_col_item_paths, True, const.MENU_TYPE_COLLECTION)

        utility.create_qt_context_menu(collection_item_list, pos, action_dict_list)

    def update_path_line(self):
        """クリップボードコピーパスを更新
        """

        col_file_list = self.view.col_file_list
        col_file_sel_items = col_file_list.selectedItems()
        col_item_sel_paths = [col_file_list.itemWidget(x).path for x in col_file_sel_items]

        if col_item_sel_paths:
            self.view.ui.selection_item_path_line.setText(col_item_sel_paths[0])
        else:
            self.view.ui.selection_item_path_line.setText('')

    def copy_item_to_clipboard_button_event(self):
        """クリップボードにコピーボタンイベント
        """

        path = self.view.ui.selection_item_path_line.text()
        self.main.copy_path_to_clipboard([path])

    def col_new_event(self):
        """新規コレクション作成イベント
        """

        if self.is_dirty:
            result = self.col_save_confirm_event()

            if result == 'Save':
                self.col_save_event()
            elif result == 'Cancel':
                return

        self.scene_collector.reset()
        self.update_collection_base(True, True)
        self.view.ui.col_json_path_label.setText('')

        self.set_col_dirty(False)

    def col_load_event(self):
        """コレクション読み込みイベント
        """

        if self.is_dirty:
            result = self.col_save_confirm_event()

            if result == 'Save':
                self.col_save_event()
            elif result == 'Cancel':
                return

        current_dir = os.path.dirname(self.scene_collector.json_path)
        if os.path.exists(current_dir):
            files = cmds.fileDialog2(cap='Select Json Path', fm=1, dir=current_dir)
        else:
            files = cmds.fileDialog2(cap='Select Json Path', fm=1)

        if files:

            self.load_collection(files[0])

    def set_col_dirty(self, is_dirty):
        """未保存フラグの設定

        Args:
            is_dirty (bool): 未保存フラグを立てるか
        """

        self.is_dirty = is_dirty

        if self.is_dirty:
            self.view.ui.dirty_label.setText('(未保存)')
        else:
            self.view.ui.dirty_label.setText('')

    def col_save_event(self):
        """コレクション保存イベント
        """

        if self.scene_collector.json_path:
            self.scene_collector.save_collection()
            self.set_col_dirty(False)
        else:
            self.col_save_as_event()

    def col_save_as_event(self):
        """コレクション別名保存イベント
        """

        save_paths = cmds.fileDialog2(cap='Select Json Path', fm=0, spe=False, ff='*.json')

        if save_paths:
            self.scene_collector.save_collection(save_paths[0])
            self.view.ui.col_json_path_label.setText(save_paths[0])
            self.set_col_dirty(False)

    def col_save_confirm_event(self):
        """保存確認イベント
        """

        result = QtWidgets.QMessageBox.information(
            self.view,
            '確認',
            'コレクションに未保存の編集があります。保存しますか？',
            QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Discard | QtWidgets.QMessageBox.Cancel,
            QtWidgets.QMessageBox.Save
        )

        if result == QtWidgets.QMessageBox.Save:
            return 'Save'
        elif result == QtWidgets.QMessageBox.Discard:
            return 'NotSave'
        else:
            return 'Cancel'

    def save_setting(self):
        """ツール情報の保存
        """

        setting = self.main.setting

        # splitter
        setting.setValue(const.SETTING_COLLECTION_SPLITTER, self.view.ui.collection_splitter.saveState())

        # json_path
        setting.setValue(const.SETTING_COLLECTION_JSON_PATH, self.view.ui.col_json_path_label.text())

        # selection
        col_list = self.view.col_list
        sel_items = col_list.selectedItems()
        sel_col_ids = [col_list.itemWidget(x).col_id for x in sel_items]
        setting.setValue(const.SETTING_COLLECTION_COL_SEL, ','.join(sel_col_ids))

        col_item_list = self.view.col_file_list
        sel_items = col_item_list.selectedItems()
        sel_col_item_ids = [col_item_list.itemWidget(x).item_id for x in sel_items]
        setting.setValue(const.SETTING_COLLECTION_COL_ITEM_SEL, ','.join(sel_col_item_ids))

    def load_setting(self):
        """ツール情報の読み込み
        """

        setting = self.main.setting

        # splitter
        if setting.value(const.SETTING_COLLECTION_SPLITTER):
            self.view.ui.collection_splitter.restoreState(setting.value(const.SETTING_COLLECTION_SPLITTER))

        # json_path
        if setting.value(const.SETTING_COLLECTION_JSON_PATH):
            self.load_collection(setting.value(const.SETTING_COLLECTION_JSON_PATH))

        # selection
        if setting.value(const.SETTING_COLLECTION_COL_SEL):
            self.init_col_sel_ids = setting.value(const.SETTING_COLLECTION_COL_SEL).split(',')

        if setting.value(const.SETTING_COLLECTION_COL_ITEM_SEL):
            self.init_col_item_sel_ids = setting.value(const.SETTING_COLLECTION_COL_ITEM_SEL).split(',')

    def load_collection(self, json_path):
        """読み込み

        Args:
            json_path (str): 読み込むjsonパス
        """

        if not os.path.exists(json_path):
            return

        init_result = self.scene_collector.initialize(json_path)

        if init_result:
            self.view.ui.col_json_path_label.setText(json_path)
        else:
            self.view.ui.col_json_path_label.setText('')

        self.update_collection_base(True, True)
        self.set_col_dirty(False)
