# -*- coding: utf-8 -*-

from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

import os
import sys
import itertools

try:
    # Maya 2022-
    from importlib import reload
except Exception:
    pass

from maya import cmds
from maya import OpenMayaUI as omui
from maya.app.general import mayaMixin

from PySide2 import QtWidgets
import shiboken2

from . import node_widget
from . import main_window

from . import constants
from . import commands

reload(node_widget)
reload(main_window)

reload(constants)
reload(commands)


def _set_property(object, name, value):
    """UIのプロパティに値をセット

    Args:
        name (str): プロパティ名
        value (Any): セットする値
    """

    object.setProperty(str(name), value)
    object.style().unpolish(object)
    object.style().polish(object)


class FolderPathLineEdit(object):
    def __init__(self, ui):

        self.line_edit = ui.folderPathLineEdit
        self.select_folder_button = ui.selectFolderButton
        self.open_explorer_button = ui.openExplorerButton

        self.make_dir = None

    def __dir_exists(self, folder_path):
        """フォルダが存在するかを返す

        Args:
            folder_path (str): フォルダパス

        Returns:
            bool: フォルダが存在するか
        """

        return os.path.isdir(folder_path)

    def __root_dir_exists(self, folder_path):
        """ルートフォルダが存在するかを返す

        Args:
            folder_path (str): フォルダパス

        Returns:
            bool: ルートフォルダが存在するか
        """

        return self.__dir_exists(folder_path.replace('\\', '/').split('/')[0])

    def __can_make_dir(self, folder_path, makeDir):
        """フォルダが作成できるかを返す

        Args:
            folder_path (str): フォルダパス
            makeDir (bool): フォルダを作成するか

        Returns:
            bool: フォルダが作成できるか
        """

        return makeDir and self.__root_dir_exists(folder_path)

    def __select_folder(self):
        """フォルダ選択ダイアログを表示する
        """

        inputted_path = self.line_edit.text()
        target_path = inputted_path if self.__dir_exists(inputted_path) else cmds.file(q=True, sceneName=True)
        selected_folder_paths = cmds.fileDialog2(fileMode=3, caption='エクスポート先フォルダを選択して下さい。', startingDirectory=target_path)

        if selected_folder_paths and len(selected_folder_paths) == 1:
            self.line_edit.setText(selected_folder_paths[0])

    def setup(self):
        """初期化
        """

        self.line_edit.textChanged.connect(self.update_dir_exists)
        # update_can_make_dirにテキストが渡ってしまうためlambdaを介す
        self.line_edit.textChanged.connect(lambda _: self.update_can_make_dir())
        self.select_folder_button.clicked.connect(self.__select_folder)
        self.open_explorer_button.clicked.connect(lambda: commands.open_explorer('', self.line_edit.text()))

        self.update()

    def update(self):
        """更新
        """

        self.update_dir_exists()
        self.update_can_make_dir()

    def update_dir_exists(self):
        """フォルダ存在チェックを更新
        """

        text = self.text()
        dir_exists = self.__root_dir_exists(text) and self.__dir_exists(text)

        _set_property(self.line_edit, 'dirExists', dir_exists)

    def update_can_make_dir(self, make_dir=None):
        """フォルダ作成チェックを更新
        """

        if (make_dir is not None):
            self.make_dir = make_dir

        text = self.text()
        can_make_dir = self.__can_make_dir(text, self.make_dir)

        _set_property(self.line_edit, 'canMakeDir', can_make_dir)

    def is_error(self):
        """入力パスがエラー状態かを返す

        Returns:
            bool: 入力パスがエラー状態か
        """

        text = self.text()
        dir_exists = self.__root_dir_exists(text) and self.__dir_exists(text)
        can_make_dir = self.__can_make_dir(text, self.make_dir)

        return not dir_exists and not can_make_dir

    def text(self):
        """入力パスを返す

        Returns:
            str: 入力パス
        """

        return self.line_edit.text()


class FolderPathAttribute(object):
    def __init__(self, node, ui):

        self.line_edit = ui.folderPathLineEdit
        self.set_node(node)

    def set_node(self, node):
        """ノードをセット

        Args:
            node (str): ノード名
        """

        self.node = node
        self.get_node_attribute()

    def has_node_attribute(self):
        """アトリビュートが存在するかを返す

        Returns:
            bool: アトリビュートが存在するか
        """

        return cmds.attributeQuery(constants.FOLDER_PATH_ATTR_NAME, node=self.node, exists=True)

    def get_node_attribute(self):
        """テキストにアトリビュートの値を設定
        """

        if not cmds.objExists(self.node):
            return

        if self.has_node_attribute():
            attr_name = '{}.{}'.format(self.node, constants.FOLDER_PATH_ATTR_NAME)
            text = cmds.getAttr(attr_name)
            self.line_edit.setText(text)

    def toggle_node_attribute(self, state):
        """アトリビュートの追加状態を切り替え

        Args:
            state (bool): アトリビュートの追加状態
        """

        if state:
            self.update_node_attribute()
        else:
            self.delete_node_attribute()

    def add_node_attribute(self):
        """ノードにアトリビュートを追加

        Returns:
            bool: アトリビュートの追加に成功
        """

        if not cmds.objExists(self.node):
            return False

        if not self.has_node_attribute():
            cmds.addAttr(self.node, longName=constants.FOLDER_PATH_ATTR_NAME, niceName=constants.FOLDER_PATH_ATTR_NAME, dataType='string')

        return True

    def delete_node_attribute(self):
        """ノードからアトリビュートを削除

        Returns:
            bool: アトリビュートの削除に成功
        """

        if not cmds.objExists(self.node):
            return False

        if self.has_node_attribute():
            cmds.deleteAttr(self.node, at=constants.FOLDER_PATH_ATTR_NAME)

        return True

    def update_node_attribute(self):
        """アトリビュートの値を更新
        """

        if not self.add_node_attribute():
            return

        attr_name = '{}.{}'.format(self.node, constants.FOLDER_PATH_ATTR_NAME)
        text = self.line_edit.text()

        cmds.setAttr(attr_name, text, type='string')


class NodeWidget(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(NodeWidget, self).__init__(*args, **kwargs)

        self.node = ''
        self.file_type = ''

        self.has_hierarchy_error = False

        self.ui = node_widget.Ui_Form()
        self.ui.setupUi(self)

        self.folder_path_line_edit = FolderPathLineEdit(self.ui)
        self.folder_path_line_edit.setup()

        self.folder_path_attribute = FolderPathAttribute(self.node, self.ui)

        self.ui.folderPathLineEdit.textChanged.connect(self.update_node_error_label)
        self.ui.folderPathLineEdit.textChanged.connect(self.folder_path_attribute.update_node_attribute)

        self.ui.removeItemButton.clicked.connect(self.deleteLater)
        self.ui.selectNodeButton.clicked.connect(self.__select_node)

        self.ui.folderButton.toggled.connect(lambda checked: self.ui.folderButton.setText('-' if checked else '+'))
        self.ui.folderButton.toggled.connect(self.update_node_error_label)
        self.ui.folderButton.toggled.connect(self.folder_path_attribute.toggle_node_attribute)
        self.ui.folderButton.setChecked(False)

    def update_node_error_label(self):
        """エラー表示を更新
        """

        self.ui.nodeErrorLabel.setVisible(self.is_error())

    def __select_node(self):
        """ノードを選択
        """

        if cmds.objExists(self.node):
            cmds.select(self.node)

    def __update(self):
        """UIを更新
        """

        self.ui.nodeNameLabel.setText(self.node)
        file_name = self.node.split('|')[-1].split('__')[0]

        normal_bake = False
        if commands.is_normal_process_target(self.node):
            normal_bake = True
        self.ui.fileNameLabel.setText('( ファイル名: {}.{} ,アウトライン法線ベイク: {})'.format(file_name, self.file_type, str(normal_bake)))

    def set_node(self, node):
        """ノードをセット

        Args:
            node (str): ノード名
        """

        self.node = node
        self.folder_path_attribute.set_node(node)
        self.ui.folderButton.setChecked(self.folder_path_attribute.has_node_attribute())
        self.__update()

    def set_file_type(self, file_type):
        """ファイルタイプをセット

        Args:
            file_type (str): ファイルタイプ
        """

        self.file_type = file_type
        self.__update()

    def is_error(self):
        """入力パスがエラー状態かを返す

        Returns:
            bool: 入力パスがエラー状態か
        """

        return self.ui.folderButton.isChecked() and self.folder_path_line_edit.is_error()


class MainWindow(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.ui = main_window.Ui_MainWindow()
        self.ui.setupUi(self)

        self.setProperty(str('saveWindowPref'), True)

        self.setWindowTitle(commands.get_tool_name())

        self.set_file_types(constants.FILE_TYPES)
        self.set_file_type(constants.DEFAULT_FILE_TYPE)

        self.folder_path_line_edit = FolderPathLineEdit(self.ui)
        self.folder_path_line_edit.setup()

        self.folder_path_attribute = FolderPathAttribute(commands.get_setting_locator_name(), self.ui)

        self.ui.fileTypeComboBox.currentIndexChanged.connect(self.__set_widgets_file_type)

        self.ui.makeDirCheckBox.toggled.connect(self.folder_path_line_edit.update_can_make_dir)
        self.ui.makeDirCheckBox.toggled.connect(self.__set_widgets_can_make_dir)
        self.ui.makeDirCheckBox.toggled.connect(lambda checked: cmds.optionVar(iv=(constants.MAKE_DIR_OPTION_KEY, int(checked))))

        self.ui.helpButton.clicked.connect(lambda: commands.open_url(constants.HELP_URL))

        self.ui.refreshNodeListButton.clicked.connect(self.__refresh_node_widgets)
        self.ui.selectAllNodeButton.clicked.connect(self.__select_all_nodes)

        self.ui.folderPathLineEdit.textChanged.connect(self.folder_path_attribute.update_node_attribute)

        self.ui.multiDstComboBox.currentIndexChanged.connect(lambda index: cmds.optionVar(iv=(constants.MULTI_DST_MODE_OPTION_KEY, index)))

        self.ui.singleExportButton.clicked.connect(lambda: self.__export(False))
        self.ui.multiExportButton.clicked.connect(lambda: self.__export(True))

        if cmds.optionVar(ex=constants.MAKE_DIR_OPTION_KEY):
            make_dir = cmds.optionVar(q=constants.MAKE_DIR_OPTION_KEY)
            self.ui.makeDirCheckBox.setChecked(bool(make_dir))

        if cmds.optionVar(ex=constants.MULTI_DST_MODE_OPTION_KEY):
            multi_dst_mode = cmds.optionVar(q=constants.MULTI_DST_MODE_OPTION_KEY)
            self.ui.multiDstComboBox.setCurrentIndex(multi_dst_mode)

        self.__setup_setting_locator()
        self.__refresh_node_widgets()

    def show(self):
        ptr = omui.MQtUtil.mainWindow()

        if sys.version_info.major == 2:
            main_window = shiboken2.wrapInstance(long(ptr), QtWidgets.QMainWindow)
        else:
            # for Maya 2022-
            main_window = shiboken2.wrapInstance(int(ptr), QtWidgets.QMainWindow)

        for widget in main_window.children():
            if str(type(self)) == str(type(widget)):
                widget.deleteLater()    # Mayaウインドウの子からインスタンスを削除

        super(MainWindow, self).show()

    def __setup_setting_locator(self):
        """ツール設定用ロケーターを作成
        """

        sel_nodes = cmds.ls(sl=True, long=True)

        setting_locator = commands.get_setting_locator_name()

        node_names = setting_locator.split('|')[1:]
        current_node_name = ''

        for node_name in node_names:
            temp_node_name = current_node_name + '|{}'.format(node_name)

            if not cmds.objExists(temp_node_name):
                temp_locator = cmds.spaceLocator(position=(0, 0, 0))
                if cmds.objExists(current_node_name):
                    temp_locator = cmds.parent(temp_locator, current_node_name)
                cmds.rename(temp_locator, node_name)

            current_node_name = temp_node_name

        cmds.select(sel_nodes)

    def __export(self, multi_export):
        """エクスポート

        Args:
            multi_export (bool): 複数の保存先に出力するか
        """

        export_info = self.__get_export_info(multi_export)

        if not self.__compare_node_list_with_selection(export_info):
            return

        if not self.__check_export_error(export_info, multi_export):
            return

        if not self.__confirm_export(export_info):
            return

        commands.export_all(export_info)

        self.__set_widgets_dir_exists()

    def __compare_node_list_with_selection(self, export_info):
        """ノードリストの内容と現在の選択ノードを比較する

        Args:
            export_info (dict[str, Any]): エクスポート情報

        Returns:
            bool: 処理を続行するか
        """

        export_nodes = set(export_info['allNodes'])

        sel_nodes = set(cmds.ls(sl=True, transforms=True, long=True))

        matched_nodes = export_nodes & sel_nodes

        if len(export_nodes) == len(sel_nodes) == len(matched_nodes):
            return True

        message = 'ノードリストの内容と選択ノードが一致しません。\n\n'
        message += ' [Yes] 現在のノードリストの内容でエクスポートを実行します。\n'
        message += ' [No] エクスポートをキャンセルします。\n'
        message += '          → ノードリストを更新してから再び実行して下さい。'

        return cmds.confirmDialog(title=commands.get_tool_name(), message=message, button=['Yes', 'No'], defaultButton='Yes', cancelButton='No', dismissString='No') == 'Yes'

    def __check_export_error(self, export_info, multi_export):
        """エクスポート時のエラーチェック

        Args:
            export_info (dict[str, Any]): エクスポート情報
            multi_export (bool): 複数の保存先に出力するか

        Returns:
            bool: 処理を続行するか
        """

        message = ''

        # メインフォルダのチェック
        main_folder_error_flg = False

        if self.folder_path_line_edit.is_error():
            if multi_export:
                if export_info['useMainNodeLines']:
                    main_folder_error_flg = True
            else:
                main_folder_error_flg = True

        if main_folder_error_flg:
            message += '\n\n ・ 「 A : メインの保存先 」 が無効です。'

        # エクスポート可能なノードがあるかどうかのチェック
        if not export_info['exportNodes']:
            message += '\n\n ・ エクスポート可能なノードが1つもありません。'

        # 全ノードのエラーチェック
        if multi_export:
            folder_error_nodes = [widget.node for widget in self.__get_all_widgets() if widget.is_error()]

            if folder_error_nodes:
                message += '\n\n ・ 保存先フォルダパスが無効です。'
                message += '\n    '.join([''] + folder_error_nodes)

        self.__set_widgets_hierarchy_error()

        hierarchy_error_nodes = [widget.node for widget in self.__get_all_widgets() if widget.has_hierarchy_error]

        if hierarchy_error_nodes:
            message += '\n\n ・ 親子関係のあるノードを同時にエクスポートすることは出来ません。'
            message += '\n    '.join([''] + hierarchy_error_nodes)

        if message:
            message = 'エラー！' + message
            cmds.confirmDialog(title=commands.get_tool_name(), message=message)
            return False

        return True

    def __confirm_export(self, export_info):
        """出力内容の確認

        Args:
            export_info (dict[str, Any]): エクスポート情報

        Returns:
            bool: 処理を続行するか
        """

        file_type = export_info['fileType']
        sorted_folder_path = sorted(export_info['exportNodeName_dstFolderPath'].items(), key=lambda x: x[1])
        grouped_folder_path = itertools.groupby(sorted_folder_path, lambda x: x[1])
        folder_path_node_names = {key: [node_name for node_name, _ in group] for key, group in grouped_folder_path}

        message = '以下の内容でエクスポートします。\n'
        message += '実行しますか？\n'

        for folder_path, node_names in folder_path_node_names.items():
            file_names = ['{}.{}'.format(file_name.split('|')[-1].split('__')[0], file_type) for file_name in node_names]

            message += '\n'
            if not os.path.isdir(folder_path):
                message += '[フォルダ自動作成]' + '\n'
            message += folder_path
            message += '\n   → '.join([''] + sorted(file_names))
            message += '\n'

        return cmds.confirmDialog(title=commands.get_tool_name(), message=message, button=['Yes', 'No'], defaultButton='Yes', cancelButton='No', dismissString='No') == 'Yes'

    def __clear_main_layout(self):
        """ノードリストをクリア
        """

        layout = self.ui.nodeListLayout
        widgets = [layout.itemAt(i).widget() for i in range(layout.count())]

        for widget in widgets:
            if not widget:
                continue

            widget.deleteLater()

    def __refresh_node_widgets(self):
        """ノードリストを更新
        """

        sel_nodes = cmds.ls(sl=True, transforms=True, long=True)
        file_type = self.ui.fileTypeComboBox.currentData()
        make_dir = self.ui.makeDirCheckBox.isChecked()

        self.__clear_main_layout()

        for sel_node in sel_nodes:
            widget = NodeWidget()
            widget.set_node(sel_node)
            widget.set_file_type(file_type)
            widget.folder_path_line_edit.update_can_make_dir(make_dir)

            layout = self.ui.nodeListLayout
            layout.insertWidget(layout.count() - 1, widget)

    def __get_all_widgets(self):
        """すべてのノードウィジェットを取得
        """

        layout = self.ui.nodeListLayout
        widgets = (layout.itemAt(i).widget() for i in range(layout.count()))
        return [widget for widget in widgets if widget]

    def __select_all_nodes(self):
        """ノードリストに含まれるすべてのノードを選択
        """

        nodes = [widget.node for widget in self.__get_all_widgets() if cmds.objExists(widget.node)]

        cmds.select(nodes)

    def __get_export_info(self, multi_export):
        """UIからエクスポート情報を取得

        Args:
            multi_export (bool): 複数の保存先に出力するか
        """

        file_type = self.ui.fileTypeComboBox.currentData()
        make_dirs_flg = self.ui.makeDirCheckBox.isChecked()
        main_folder_path = self.folder_path_line_edit.text()
        # 0: 何もしない、1: 「 A : メインの保存先 」 に保存
        multi_dst_mode = self.ui.multiDstComboBox.currentIndex()

        all_nodes = []
        export_nodes = []
        node_name_to_dst_folder_path = {}
        use_main_node_lines = []

        for widget in self.__get_all_widgets():
            node = widget.node

            all_nodes.append(node)

            dst_folder_path = ''

            if multi_export:
                if widget.ui.folderButton.isChecked():
                    dst_folder_path = widget.folder_path_line_edit.text()

                elif multi_dst_mode == 1:
                    dst_folder_path = main_folder_path
                    use_main_node_lines.append(widget)

            else:
                dst_folder_path = main_folder_path
                use_main_node_lines.append(widget)

            if dst_folder_path:
                export_nodes.append(node)
                node_name_to_dst_folder_path[node] = dst_folder_path

        export_info = {
            'fileType': file_type,
            'makedirsFlg': make_dirs_flg,
            'mainFolderPath': main_folder_path,
            'multiDstMode': multi_dst_mode,
            'allNodes': all_nodes,
            'exportNodes': export_nodes,
            'exportNodeName_dstFolderPath': node_name_to_dst_folder_path,
            'useMainNodeLines': use_main_node_lines,
        }

        return export_info

    def __set_widgets_dir_exists(self):
        """すべてのノードウィジェットのフォルダ存在チェックを更新
        """

        for widget in self.__get_all_widgets():
            widget.folder_path_line_edit.update_dir_exists()
            widget.update_node_error_label()

    def __set_widgets_can_make_dir(self, make_dir):
        """すべてのノードウィジェットのフォルダ作成チェックを更新

        Args:
            make_dir (bool): フォルダを作成するか
        """

        for widget in self.__get_all_widgets():
            widget.folder_path_line_edit.update_can_make_dir(make_dir)
            widget.update_node_error_label()

    def __set_widgets_file_type(self, file_type_index):
        """すべてのノードウィジェットのファイルタイプを更新

        Args:
            file_type_index (int): ファイルタイプリストのインデックス
        """

        for widget in self.__get_all_widgets():
            widget.set_file_type(self.ui.fileTypeComboBox.itemData(file_type_index))

    def __set_widgets_hierarchy_error(self):
        """すべてのノードウィジェットの親子関係エラーを更新
        """

        widgets = self.__get_all_widgets()

        for widget in widgets:
            widget.has_hierarchy_error = False

        for widget_a in widgets:
            node_a = widget_a.node

            parent_check_str = '{}|'.format(node_a)

            for widget_b in widgets:
                node_b = widget_b.node

                if node_b == node_a:
                    continue

                if node_b.startswith(parent_check_str):
                    widget_a.has_hierarchy_error = True
                    widget_b.has_hierarchy_error = True

    def set_file_types(self, file_types):
        """ファイルタイプリストを設定

        Args:
            file_types (list[str]): ファイルタイプリスト
        """

        for file_type in file_types:
            text = ' File Type : {}'.format(file_type.upper())
            self.ui.fileTypeComboBox.addItem(text, file_type)

    def set_file_type(self, file_type):
        """ファイルタイプを設定

        Args:
            file_type (str): ファイルタイプ
        """

        index = self.ui.fileTypeComboBox.findData(file_type)
        if index > -1:
            self.ui.fileTypeComboBox.setCurrentIndex(index)
