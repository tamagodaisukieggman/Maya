# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

from PySide2 import QtWidgets, QtCore
from maya import OpenMayaUI

import sys
import shiboken2
import os
import json

import maya.cmds as cmds

from . import view
from . import utility
from . import const
from . import explorer
from . import collection
from . import scene_opener
from . import scene_collector
from .ui import model

try:
    # Maya2022-
    from builtins import str
    from builtins import object
    from importlib import reload
except Exception:
    pass

reload(view)
reload(utility)
reload(const)
reload(explorer)
reload(collection)
reload(scene_opener)
reload(scene_collector)
reload(model)


class Main(object):

    def __init__(self):
        """
        """

        # 設定
        self.setting = QtCore.QSettings(utility.get_setting_path(), QtCore.QSettings.IniFormat)
        self.setting.setIniCodec('utf-8')

        self.scene_collector = scene_collector.SceneCollector()

        # メインウインドウ
        self.view = view.View(self)
        self.view.setWindowTitle(const.TOOL_NAME + const.TOOL_VERSION)

        # 各UIタブ
        self.explorer_tab = explorer.Explorer(self)
        self.collection_tab = collection.Collection(self)

        # ツール設定
        self.walk_file_limit = const.DEFAULT_WALK_LIMIT
        self.set_rootdir_on_double_clicked = const.DEFAULT_SET_ROOT_ON_DOUBLE_CLICK
        self.separate_path_with_slash = const.DEFAULT_SEP_WITH_SLASH
        self.col_obj_del_confirm = const.DEFAULT_COL_OBJ_DEL_CONFIRM
        self.exec_script_node_on_open = const.DEFAULT_EXEC_SCRIPT_NODE
        self.uses_namespace = const.DEFAULT_USE_NAMESPACE
        self.exec_set_project = const.DEFAULT_EXEC_SET_PROJECT
        self.exec_fix_texture_path = const.DEFAULT_EXEC_FIX_TEX_PATH
        self.project_setting_path = const.DEFAULT_PROJECT_SETTING_FILE_PATH

        # プロジェクト固有設定
        self.replace_dict = []

    def deleteOverlappingWindow(self, target):
        """Windowの重複削除処理
        """

        main_window = OpenMayaUI.MQtUtil.mainWindow()
        if main_window is None:
            return

        if sys.version_info.major == 2:
            main_window = shiboken2.wrapInstance(long(main_window), QtWidgets.QMainWindow)
        else:
            main_window = shiboken2.wrapInstance(int(main_window), QtWidgets.QMainWindow)

        for widget in main_window.children():
            if str(type(target)) == str(type(widget)):
                widget.saveCollectionConfirm()
                widget.saveRootSetting()
                widget.deleteLater()

    def show_ui(self):
        """UI描画
        """

        # windowの重複削除処理
        self.deleteOverlappingWindow(self.view)

        # 設定の読み込み
        self.load_setting()
        self.explorer_tab.load_bookmark()

        # UIの初期設定
        self.initialize_ui_main()

        # イベント設定
        self.setup_view_event_main()

        self.view.show()

    def initialize_ui_main(self):

        self.setting_dialog = view.SettingDialog(self.view)
        self.setting_dialog.setWindowTitle('settings')
        self.setup_setting_dialog_event()

        # 各タブの設定
        self.explorer_tab.initialize_ui()
        self.collection_tab.initialize_ui()

    def setup_view_event_main(self):
        """UIのevent設定
        """

        self.view.ui.setting_action.triggered.connect(self.open_setting_dialog)
        self.view.ui.setting_dir_open_action.triggered.connect(self.open_setting_dir)

        # 各タブの設定
        self.explorer_tab.setup_view_event()
        self.collection_tab.setup_view_event()

    def open_setting_dialog(self):
        """設定ダイアログを開く
        """

        self.initialize_setting_dialog()
        self.setting_dialog.show()

    def open_setting_dir(self):
        """設定ファイルのフォルダを開く
        """

        utility.show_in_explorer([utility.get_setting_path()])

    def open_operation_begin(self, paths):
        """ファイルに対して開く処理を実行

        Args:
            paths ([str]): 処理を実行するファイルパスリスト
        """

        final_paths = [x for x in paths if os.path.exists(x) and os.path.isfile(x)]
        if not final_paths:
            return

        ops = []
        if len(final_paths) == 1:
            ops = [
                const.EXEC_BUTTON_OPEN_NEW,
                const.EXEC_BUTTON_REFERENCE,
                const.EXEC_BUTTON_IMPORT,
                const.EXEC_BUTTON_CANCEL,
            ]
        else:
            ops = [
                const.EXEC_BUTTON_REFERENCE,
                const.EXEC_BUTTON_IMPORT,
                const.EXEC_BUTTON_CANCEL,
            ]

        confirm = cmds.confirmDialog(
            title='読み込み確認',
            message='読み込み方を選択してください',
            button=ops,
            cancelButton=const.EXEC_BUTTON_CANCEL,
            dismissString=const.EXEC_BUTTON_CANCEL)

        if confirm == const.EXEC_BUTTON_OPEN_NEW:

            # 開くのは一つのパスのみ
            scene_opener.open_as_new_scene(
                final_paths[0],
                self.exec_script_node_on_open,
                self.exec_set_project,
                self.exec_fix_texture_path,)

        elif confirm == const.EXEC_BUTTON_REFERENCE:

            for path in final_paths:
                namespace = ''
                if self.uses_namespace:
                    namespace = os.path.splitext(os.path.basename(path))[0]

                scene_opener.create_reference(
                    path,
                    namespace,
                    self.exec_script_node_on_open,
                    self.exec_fix_texture_path)

        elif confirm == const.EXEC_BUTTON_IMPORT:

            for path in final_paths:
                namespace = ''
                if self.uses_namespace:
                    namespace = os.path.splitext(os.path.basename(path))[0]

                scene_opener.import_file(
                    path,
                    namespace,
                    self.exec_script_node_on_open,
                    self.exec_fix_texture_path,)

        self.explorer_tab.update_recent_file_list()

    def copy_path_to_clipboard(self, paths):
        """パスをクリップボードにコピー

        Args:
            paths ([str]): コピーするパスリスト
        """

        paths = [utility.normalize_path(x, self.separate_path_with_slash) for x in paths]
        utility.copy_to_clipboard(','.join(paths))

    def get_file_action_dict_list(self, paths, is_scene_file, menu_type=''):
        """ファイルのコンテキストメニュー用の辞書リストを作成

        Args:
            path (str): ファイルのパス
            is_scene_file (bool): シーンファイルかどうか
            menu_type (str): メニューのタイプ

        Returns:
            [{'label': str, 'function': function, 'arg': any, 'enable': bool}]: ラベル名、処理、引数、有効か？の辞書リスト
        """

        action_dict_list = []

        action_dict_list.append({'label': const.MENU_OPEN, 'function': self.open_operation_begin, 'arg': paths, 'enable': is_scene_file})

        if menu_type == const.MENU_TYPE_EXPLORER:
            action_dict_list.append({'label': const.MENU_SEPARATOR})
            action_dict_list.append({'label': const.MENU_BOOKMARK, 'function': self.explorer_tab.add_bookmarks, 'arg': paths, 'enable': True})
        elif menu_type == const.MENU_TYPE_BOOKMARK:
            action_dict_list.append({'label': const.MENU_SEPARATOR})
            action_dict_list.append({'label': const.MENU_REM_BOOKMARK, 'function': self.explorer_tab.remove_bookmark, 'arg': None, 'enable': True})

        action_dict_list.append({'label': const.MENU_SEPARATOR})

        action_dict_list.append({'label': const.MENU_SHOW_IN_EXP, 'function': utility.show_in_explorer, 'arg': paths, 'enable': len(paths) == 1})
        action_dict_list.append({'label': const.MENU_COPY_PAHT, 'function': self.copy_path_to_clipboard, 'arg': paths, 'enable': True})

        if menu_type == const.MENU_TYPE_EXPLORER or menu_type == const.MENU_TYPE_BOOKMARK:
            action_dict_list.append({'label': const.MENU_SEPARATOR})
            action_dict_list.append({'label': const.MENU_ADD_COLLECTION_PAHT, 'function': self.explorer_tab.add_collection, 'arg': paths, 'enable': True})

        return action_dict_list

    def get_dir_action_dict_list(self, paths, menu_type=''):
        """フォルダのコンテキストメニュー用の辞書リストを作成

        Args:
            path (str): ファイルのパス
            menu_type (str): メニューのタイプ

        Returns:
            [{'label': str, 'function': function, 'arg': any, 'enable': bool}]: ラベル名、処理、引数、有効か？の辞書リスト
        """

        action_dict_list = []

        action_dict_list.append({'label': const.MENU_SET_ROOT, 'function': self.explorer_tab.set_search_root_path, 'arg': paths[0], 'enable': len(paths) == 1})

        if menu_type == const.MENU_TYPE_EXPLORER:
            action_dict_list.append({'label': const.MENU_SEPARATOR})
            action_dict_list.append({'label': const.MENU_BOOKMARK, 'function': self.explorer_tab.add_bookmarks, 'arg': paths, 'enable': True})
        elif menu_type == const.MENU_TYPE_BOOKMARK:
            action_dict_list.append({'label': const.MENU_SEPARATOR})
            action_dict_list.append({'label': const.MENU_REM_BOOKMARK, 'function': self.explorer_tab.remove_bookmark, 'arg': None, 'enable': True})

        action_dict_list.append({'label': const.MENU_SEPARATOR})

        action_dict_list.append({'label': const.MENU_SHOW_IN_EXP, 'function': utility.show_in_explorer, 'arg': paths, 'enable': len(paths) == 1})
        action_dict_list.append({'label': const.MENU_COPY_PAHT, 'function': self.copy_path_to_clipboard, 'arg': paths, 'enable': True})

        return action_dict_list

    def get_collection_action_dict_list(self, ids):

        action_dict_list = []
        action_dict_list.append({'label': const.MENU_OPEN_ALL_ITEMS, 'function': self.open_operation_begin, 'arg': self.collection_tab.get_item_paths(ids), 'enable': True})
        action_dict_list.append({'label': const.MENU_SEPARATOR})
        action_dict_list.append({'label': const.MENU_CHANGE_COLLECTION_NAME, 'function': self.collection_tab.col_change_name_event, 'arg': ids[0], 'enable': len(ids) == 1})

        return action_dict_list

    def initialize_setting_dialog(self):
        """設定ダイアログの初期化
        """

        dialog = self.setting_dialog.ui

        dialog.walk_file_limit_spin.setValue(self.walk_file_limit)

        if self.set_rootdir_on_double_clicked:
            dialog.tree_double_click_set_root_radio.setChecked(True)
        else:
            dialog.tree_double_click_expand_radio.setChecked(True)

        if self.separate_path_with_slash:
            dialog.sep_slash_radio.setChecked(True)
        else:
            dialog.sep_back_slash_radio.setChecked(True)

        dialog.col_obj_del_confirm_check.setChecked(self.col_obj_del_confirm)

        dialog.exec_script_node_on_open_check.setChecked(self.exec_script_node_on_open)

        if self.uses_namespace:
            dialog.use_file_namespace_radio.setChecked(True)
        else:
            dialog.no_use_namespace_radio.setChecked(True)

        dialog.exec_set_project_check.setChecked(self.exec_set_project)
        dialog.exec_fix_texture_path_check.setChecked(self.exec_fix_texture_path)
        dialog.project_setting_file_path_edit.setText(self.project_setting_path)

    def setup_setting_dialog_event(self):
        """設定ダイアログのevent設定
        """

        dialog = self.setting_dialog.ui

        dialog.walk_file_limit_spin.valueChanged.connect(self.apply_setting_dialog)
        dialog.tree_double_click_expand_radio.clicked.connect(self.apply_setting_dialog)
        dialog.tree_double_click_set_root_radio.clicked.connect(self.apply_setting_dialog)
        dialog.sep_slash_radio.clicked.connect(self.apply_setting_dialog)
        dialog.col_obj_del_confirm_check.stateChanged.connect(self.apply_setting_dialog)
        dialog.sep_back_slash_radio.clicked.connect(self.apply_setting_dialog)
        dialog.exec_script_node_on_open_check.stateChanged.connect(self.apply_setting_dialog)
        dialog.use_file_namespace_radio.clicked.connect(self.apply_setting_dialog)
        dialog.no_use_namespace_radio.clicked.connect(self.apply_setting_dialog)
        dialog.exec_set_project_check.stateChanged.connect(self.apply_setting_dialog)
        dialog.exec_fix_texture_path_check.stateChanged.connect(self.apply_setting_dialog)

        dialog.reset_setting_button.clicked.connect(self.reset_dialog_setting)

        dialog.set_project_setting_file_path_button.clicked.connect(self.set_project_setting_path)
        dialog.open_project_setting_file_dir_button.clicked.connect(self.open_project_setting_path)
        dialog.project_setting_file_path_edit.textChanged.connect(self.apply_setting_dialog)

    def apply_setting_dialog(self):
        """ダイアログの設定を適用
        """

        self.walk_file_limit = self.setting_dialog.ui.walk_file_limit_spin.value()

        if self.setting_dialog.ui.tree_double_click_expand_radio.isChecked():
            self.set_rootdir_on_double_clicked = False
        else:
            self.set_rootdir_on_double_clicked = True

        if self.setting_dialog.ui.sep_slash_radio.isChecked():
            self.separate_path_with_slash = True
        else:
            self.separate_path_with_slash = False

        self.col_obj_del_confirm = self.setting_dialog.ui.col_obj_del_confirm_check.isChecked()

        self.exec_script_node_on_open = self.setting_dialog.ui.exec_script_node_on_open_check.isChecked()

        if self.setting_dialog.ui.use_file_namespace_radio.isChecked():
            self.uses_namespace = True
        else:
            self.uses_namespace = False

        self.exec_set_project = self.setting_dialog.ui.exec_set_project_check.isChecked()
        self.exec_fix_texture_path = self.setting_dialog.ui.exec_fix_texture_path_check.isChecked()
        self.project_setting_path = self.setting_dialog.ui.project_setting_file_path_edit.text()

    def reset_dialog_setting(self):
        """ダイアログの設定を初期値に戻す
        """

        dialog = self.setting_dialog.ui

        dialog.walk_file_limit_spin.setValue(const.DEFAULT_WALK_LIMIT)

        if const.DEFAULT_SET_ROOT_ON_DOUBLE_CLICK:
            dialog.tree_double_click_set_root_radio.setChecked(True)
        else:
            dialog.tree_double_click_expand_radio.setChecked(True)

        if const.DEFAULT_SEP_WITH_SLASH:
            dialog.sep_slash_radio.setChecked(True)
        else:
            dialog.sep_back_slash_radio.setChecked(True)

        dialog.exec_script_node_on_open_check.setChecked(const.DEFAULT_EXEC_SCRIPT_NODE)

        if const.DEFAULT_USE_NAMESPACE:
            dialog.use_file_namespace_radio.setChecked(True)
        else:
            dialog.no_use_namespace_radio.setChecked(True)

        dialog.exec_set_project_check.setChecked(const.DEFAULT_EXEC_SET_PROJECT)
        dialog.exec_fix_texture_path_check.setChecked(const.DEFAULT_EXEC_FIX_TEX_PATH)

        dialog.project_setting_file_path_edit.setText(const.DEFAULT_PROJECT_SETTING_FILE_PATH)

        self.apply_setting_dialog()

    def set_project_setting_path(self):
        """プロジェクト設定ファイルのパスを設定するファイルダイアログを実行する
        """

        default_explorer_path = self.project_setting_path
        if not os.path.exists(default_explorer_path):
            default_explorer_path = 'D:\\'

        # ディレクトリ選択ダイアログを表示
        path, _ = QtWidgets.QFileDialog.getOpenFileName(None, 'プロジェクト設定ファイルを選択してください', default_explorer_path)
        if path:
            if not path.endswith('.json'):
                QtWidgets.QMessageBox.warning(None, 'ファイル形式が違います', 'プロジェクト設定ファイルにはjsonファイルのみ指定できます')
                return

            self.setting_dialog.ui.project_setting_file_path_edit.setText(path)
            self.project_setting_path = path

            self.setup_project_setting()

    def setup_project_setting(self):
        """プロジェクト設定をセットアップする
        """

        self.replace_dict = self.create_replace_dict()

    def open_project_setting_path(self):
        """プロジェクト設定ファイルのパスをエクスプローラーで開く
        """

        if os.path.exists(self.project_setting_path):
            utility.show_in_explorer([self.project_setting_path])

    def save_setting(self):
        """ツール情報の保存
        """

        # メインウインドウUI
        # geometry
        self.setting.setValue(const.SETTING_GEOMETRY, self.view.saveGeometry())

        # ツール設定
        # self.walk_file_limit
        self.setting.setValue(const.SETTING_WALK_FILE_LIMIT_LABEL, self.walk_file_limit)
        # self.set_rootdir_on_double_clicked
        self.setting.setValue(const.SETTING_DOUBLE_CLICK_ROOT_OP_LABEL, str(self.set_rootdir_on_double_clicked))
        # self.separate_path_with_slash
        self.setting.setValue(const.SETTING_SEP_WITH_SLASH, str(self.separate_path_with_slash))
        # self.col_obj_del_confirm
        self.setting.setValue(const.SETTING_COL_OBJ_DEL_CONFIRM, str(self.col_obj_del_confirm))
        # self.exec_script_node_on_open
        self.setting.setValue(const.SETTING_EXEC_SCRIPT_NODE_LABEL, str(self.exec_script_node_on_open))
        # self.uses_namespace
        self.setting.setValue(const.SETTING_USE_NAMESPACE_LABEL, str(self.uses_namespace))
        # self.exec_set_project
        self.setting.setValue(const.SETTING_EXEC_SET_PROJECT, str(self.exec_set_project))
        # self.exec_fix_texture_path
        self.setting.setValue(const.SETTING_EXEC_FIX_TEXTURE_PATH, str(self.exec_fix_texture_path))
        # self.project_setting_file_path
        self.setting.setValue(const.SETTING_PROJECT_SETTING_FILE_PATH, self.project_setting_path)
        # self.view_ui_main_tab
        self.setting.setValue(const.SETTING_MAIN_TAB_INDEX, self.view.ui.main_tab.currentIndex())

        # 各タブの情報
        self.explorer_tab.save_setting()
        self.collection_tab.save_setting()

    def load_setting(self):
        """ツール情報の読み込み
        """

        # メインウインドウUI
        # geometry
        if self.setting.value(const.SETTING_GEOMETRY):
            self.view.restoreGeometry(self.setting.value(const.SETTING_GEOMETRY))

        # ツール設定
        # self.main.walk_file_limit
        if self.setting.value(const.SETTING_WALK_FILE_LIMIT_LABEL):
            try:
                self.walk_file_limit = int(self.setting.value(const.SETTING_WALK_FILE_LIMIT_LABEL))
            except Exception:
                self.walk_file_limit = const.DEFAULT_WALK_LIMIT

        # self.set_rootdir_on_double_clicked
        if self.setting.value(const.SETTING_DOUBLE_CLICK_ROOT_OP_LABEL):
            val = utility.str_setting_to_bool(self.setting.value(const.SETTING_DOUBLE_CLICK_ROOT_OP_LABEL))
            self.set_rootdir_on_double_clicked = val
            if val:
                self.view.ui.dir_tree.setExpandsOnDoubleClick(False)
            else:
                self.view.ui.dir_tree.setExpandsOnDoubleClick(True)

        # self.separate_path_with_slash
        if self.setting.value(const.SETTING_SEP_WITH_SLASH):
            val = utility.str_setting_to_bool(self.setting.value(const.SETTING_SEP_WITH_SLASH))
            self.separate_path_with_slash = val

        # self.col_obj_del_confirm
        if self.setting.value(const.SETTING_COL_OBJ_DEL_CONFIRM):
            val = utility.str_setting_to_bool(self.setting.value(const.SETTING_COL_OBJ_DEL_CONFIRM))
            self.col_obj_del_confirm = val

        # self.exec_script_node_on_open
        if self.setting.value(const.SETTING_EXEC_SCRIPT_NODE_LABEL):
            val = utility.str_setting_to_bool(self.setting.value(const.SETTING_EXEC_SCRIPT_NODE_LABEL))
            self.exec_script_node_on_open = val

        # self.uses_namespace
        if self.setting.value(const.SETTING_USE_NAMESPACE_LABEL):
            val = utility.str_setting_to_bool(self.setting.value(const.SETTING_USE_NAMESPACE_LABEL))
            self.uses_namespace = val

        # self.exec_set_project
        if self.setting.value(const.SETTING_EXEC_SET_PROJECT):
            val = utility.str_setting_to_bool(self.setting.value(const.SETTING_EXEC_SET_PROJECT))
            self.exec_set_project = val

        # self.exec_fix_texture_path
        if self.setting.value(const.SETTING_EXEC_FIX_TEXTURE_PATH):
            val = utility.str_setting_to_bool(self.setting.value(const.SETTING_EXEC_FIX_TEXTURE_PATH))
            self.exec_fix_texture_path = val

        # self.project_setting_file_path
        if self.setting.value(const.SETTING_PROJECT_SETTING_FILE_PATH):
            self.project_setting_path = self.setting.value(const.SETTING_PROJECT_SETTING_FILE_PATH)
            self.setup_project_setting()

        # self.view_ui_main_tab
        if self.setting.value(const.SETTING_MAIN_TAB_INDEX) is not None:
            val = int(self.setting.value(const.SETTING_MAIN_TAB_INDEX))
            if val >= 0:
                self.view.ui.main_tab.setCurrentIndex(val)

        # 各タブの情報
        self.explorer_tab.load_setting()
        self.collection_tab.load_setting()

    def create_replace_dict(self):
        """ワード検索置換用の辞書を作成する
        """

        if not os.path.exists(self.project_setting_path) or not self.project_setting_path.endswith('.json'):
            return {}

        settings = None
        with open(self.project_setting_path, 'r') as f:
            settings = json.load(f)

        replace_dict_settings = settings.get('ReplaceDictSettings')
        if not replace_dict_settings:
            return {}

        path = replace_dict_settings.get('ReplaceDictPath')
        key_field_name = replace_dict_settings.get('ReplaceDictKeyFieldName')
        value_field_name = replace_dict_settings.get('ReplaceDictValueFieldName')
        if None in [path, key_field_name, value_field_name]:
            return {}

        csv_path = os.path.normpath(os.path.join(os.path.dirname(self.project_setting_path) + path))
        if not os.path.exists(csv_path):
            return {}

        replace_dict = {}
        csv_dict_list = utility.create_csv_dict_list(csv_path)
        if not csv_dict_list:
            return {}

        for csv_dict in csv_dict_list:
            key = csv_dict.get(key_field_name)
            value = csv_dict.get(value_field_name)
            if None in [key, value]:
                continue
            replace_dict[key] = value

        return replace_dict
