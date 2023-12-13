# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os
import sys
import subprocess
import shiboken2

from PySide2 import QtCore, QtWidgets
from maya import OpenMayaUI

from . import view, model
from ..base_common.utility import simple_batch2

try:
    # Maya2022-
    from importlib import reload
except Exception:
    pass

reload(view)
reload(model)


SVN_MODEL_DIR_PATH = 'W:\\gallop\\svn\\svn_gallop\\80_3D\\01_character\\01_model'
TOOL_NAME = 'glpCreateUnionModel'
TOOL_VERSION = '1.0.0'
DRESS_DATA_CSV_PATH_KEY = TOOL_NAME + 'DRESSDATACSVPATHKEY'


def export():

    main = Main()
    main.exec_export_union_model_for_batch()


class Main(object):

    def __init__(self):

        self.view = None

    def show_ui(self):
        """UIを表示する
        """

        self.view = view.View()
        self.view.setWindowTitle('{} ver {}'.format(TOOL_NAME, TOOL_VERSION))

        self.delete_overlapping_window(self.view)
        self.__setup_signals()
        self.__initialize_ui()
        self.view.show()

    def delete_overlapping_window(self, target):
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
                widget.deleteLater()

    def __setup_signals(self):
        """UIのシグナルをセットする
        """

        self.view.ui.set_body_file_path_button.clicked.connect(lambda: self.select_path_from_ui(self.view.ui.body_file_path_edit, 'body'))
        self.view.ui.set_head_file_path_button.clicked.connect(lambda: self.select_path_from_ui(self.view.ui.head_file_path_edit, 'head'))
        self.view.ui.set_tail_file_path_button.clicked.connect(lambda: self.select_path_from_ui(self.view.ui.tail_file_path_edit, 'tail'))
        self.view.ui.set_save_union_file_path_button.clicked.connect(lambda: self.select_path_from_ui(self.view.ui.save_union_file_path_edit, is_dir=True))
        self.view.ui.set_dress_data_csv_path_button.clicked.connect(lambda: self.select_path_from_ui(self.view.ui.dress_data_csv_path_edit))

        self.view.ui.use_tool_dress_data_csv_cb.stateChanged.connect(lambda: self.change_dress_data_path_edit_disable())

        self.view.ui.open_body_file_path_button.clicked.connect(lambda: self.open_exprlorer_form_ui(self.view.ui.body_file_path_edit))
        self.view.ui.open_head_file_path_button.clicked.connect(lambda: self.open_exprlorer_form_ui(self.view.ui.head_file_path_edit))
        self.view.ui.open_tail_file_path_button.clicked.connect(lambda: self.open_exprlorer_form_ui(self.view.ui.tail_file_path_edit))
        self.view.ui.open_save_union_file_path_button.clicked.connect(lambda: self.open_exprlorer_form_ui(self.view.ui.save_union_file_path_edit))
        self.view.ui.open_dress_data_csv_path_button.clicked.connect(lambda: self.open_exprlorer_form_ui(self.view.ui.dress_data_csv_path_edit))

        self.view.ui.exec_set_union_file_path_button.clicked.connect(lambda: self.exec_set_union_file_path())
        self.view.ui.exec_create_union_model_button.clicked.connect(lambda: self.exec_create_union_model())

    def __initialize_ui(self):
        """UIの初期化
        """

        dress_data_csv_path = model.get_option_var(DRESS_DATA_CSV_PATH_KEY)
        if dress_data_csv_path and os.path.exists(dress_data_csv_path):
            self.view.ui.dress_data_csv_path_edit.setText(dress_data_csv_path)
            self.view.ui.use_tool_dress_data_csv_cb.setChecked(False)

    def exec_set_union_file_path(self):
        """合体モデル作成用のファイルパスを自動的に読み込む
        身体のモデルパスからIDを抜き出し、IDから合致する頭ID、尻尾IDをdress_data.csvから取得したのちに
        該当するモデルファイルを取得してくる
        """

        body_model_file_path = self.view.ui.body_file_path_edit.text()
        if not body_model_file_path:
            QtWidgets.QMessageBox.warning(None, '警告', 'bodyファイルパスが指定されていません')
            return

        dress_data_csv_file_path = self.view.ui.dress_data_csv_path_edit.text()
        if self.view.ui.use_tool_dress_data_csv_cb.checkState() == QtCore.Qt.Checked:
            dress_data_csv_file_path = ''
        elif not dress_data_csv_file_path or not os.path.exists(dress_data_csv_file_path):
            QtWidgets.QMessageBox.warning(None, '警告', '保存パスが指定されていないか、パスが存在しません')
            return

        main_id, sub_id = model.search_chara_model_id(body_model_file_path)
        if main_id is None or sub_id is None:
            QtWidgets.QMessageBox.warning(None, '警告', 'bodyファイル名が命名規則に沿っていません')
            return

        is_unique_chara = model.get_is_unique_chara(body_model_file_path)
        # 汎用衣装だったら何もしない
        if is_unique_chara is None or not is_unique_chara:
            QtWidgets.QMessageBox.warning(None, '警告', 'bodyファイルの指定が汎用衣装の為、処理を終了します')
            return

        fetch_files = model.fetch_type_id(main_id, sub_id, body_model_file_path, dress_data_csv_file_path)
        if not fetch_files and len(fetch_files) > 1:
            return

        data = fetch_files[0]
        head_id = data.get('head_id')
        tail_id = data.get('tail_id')
        if head_id is None and tail_id is None:
            QtWidgets.QMessageBox.warning(None, '警告', 'bodyファイルから頭と尻尾のIDが取得できませんでした')
            return

        if head_id:
            head_ma_list = model.fetch_type_id_model_paths('head', head_id)
            self.set_type_file_path('Head', head_ma_list, self.view.ui.head_file_path_edit)
        if tail_id:
            tail_ma_list = model.fetch_type_id_model_paths('tail', tail_id)
            self.set_type_file_path('Tail', tail_ma_list, self.view.ui.tail_file_path_edit)

        model.set_option_var(DRESS_DATA_CSV_PATH_KEY, dress_data_csv_file_path)

    def exec_create_union_model(self):
        """合体モデルを作成する
        """

        body_file_path = self.view.ui.body_file_path_edit.text()
        head_file_path = self.view.ui.head_file_path_edit.text()
        tail_file_path = self.view.ui.tail_file_path_edit.text()
        save_union_file_path = self.view.ui.save_union_file_path_edit.text()

        if not os.path.exists(save_union_file_path):
            QtWidgets.QMessageBox.warning(None, '警告', '合体モデルの保存パスが指定されていないか、存在しません')
            return

        for path, model_type in zip([body_file_path, head_file_path, tail_file_path], ['body', 'head', 'tail']):

            # 尻尾は必須ではないので、パスが空なら検索しない
            if model_type == 'tail' and path == '':
                continue

            if not os.path.exists(path):
                QtWidgets.QMessageBox.warning(None, '警告', '{}タイプのファイルパスが指定されていないか、存在しません'.format(model_type))
                return
            if not model.determine_model_type(path, model_type):
                QtWidgets.QMessageBox.warning(None, '警告', '{}タイプのファイルパスが命名規則に一致しません'.format(model_type))
                return

        simple_batch2.execute_mayabatch(
            'Project_Gallop.glp_create_union_model.main',
            'export()',
            False,
            body_file_path=body_file_path,
            head_file_path=head_file_path,
            tail_file_path=tail_file_path,
            save_union_file_path=save_union_file_path,
        )

    def set_type_file_path(self, file_type, ma_list, edit):
        """タイプ別のBodyと合致したmaリストがあった時、ダイアログからどのmaを選択するかを設定する

        Args:
            file_type (str): ファイルの種別(head, tail)
            ma_list (list[str]): maのリスト
            edit (QtWidget.QLineEdit): maパスを設定したいLineEdit
        """

        ma_path = ''

        if len(ma_list) == 0:
            QtWidgets.QMessageBox.warning(None, '警告', 'Bodyとセットになる{}が見つかりませんでした'.format(file_type))
        elif len(ma_list) > 1:
            dialog = self.view_path_list_dialog(ma_list)
            if dialog.exec_():
                items = dialog.ui.path_list.selectedItems()
                if len(items) == 1:
                    ma_path = items[0].text()
        else:
            ma_path = ma_list[0]

        if ma_path:
            edit.setText(ma_path)

    def view_path_list_dialog(self, paths):
        """ファイルパスが複数ある時に１つ選択するためのダイアログを表示する

        Args:
            paths ([str]): ファイルパス
        """

        dialog = view.PathListDialog(self.view)
        dialog.ui.buttonBox.accepted.connect(dialog.accept)
        dialog.ui.buttonBox.rejected.connect(dialog.reject)

        for path in paths:
            dialog.ui.path_list.addItem(path)

        if len(path) > 0:
            dialog.ui.path_list.setCurrentRow(0)

        return dialog

    def exec_export_union_model_for_batch(self):
        """合体モデル作成をバッチ実行する
        """

        kwds = simple_batch2.get_kwargs()
        result = model.create_union_chara_model(**kwds)

        print_str = '完了しました'
        if not result:
            print_str = 'エラーが発生しました'

        if sys.version_info.major == 2:
            print(print_str.encode('cp932'))
        else:
            print(print_str)

    def select_path_from_ui(self, edit, path_type='', is_dir=False):
        """UIに設定するファイルパスを設定する

        Args:
            edit (QLineEdit): ファイルパスを設定するQLineEdit
            path_type (str): 設定するファイルパスのタイプ(body, head, tail)
            is_dir (bool): 設定するのがファイルかフォルダかどうか
        """

        file_filter = 'All Files(*.*)'

        current_file_path = edit.text()
        current_dir_path = ''
        if current_file_path:
            if os.path.isfile(current_file_path):
                current_dir_path = os.path.dirname(current_file_path).replace('\\', '/')
            else:
                current_dir_path = current_file_path.replace('\\', '/')
        else:
            if os.path.exists(SVN_MODEL_DIR_PATH):
                current_dir_path = SVN_MODEL_DIR_PATH
                if path_type:
                    current_dir_path += '/{}'.format(path_type)

        if is_dir:
            select_file_path = QtWidgets.QFileDialog.getExistingDirectory(self.view, 'select folder', current_dir_path)
        else:
            select_file_path, file_filter = QtWidgets.QFileDialog.getOpenFileName(self.view, 'select file', current_dir_path, file_filter, file_filter)

        if not select_file_path:
            return

        if path_type:
            if not model.determine_model_type(select_file_path, path_type):
                QtWidgets.QMessageBox.warning(None, '警告', '{}ファイルパスの命名規則に一致するファイルが設定されていません'.format(path_type))
                return

        edit.setText(select_file_path)

    def open_exprlorer_form_ui(self, edit):
        """UIにセットされているパスをエクスプローラーで開く

        Args:
            edit (QLineEdit): パスがセットされているUI
        """

        path = edit.text()
        if not os.path.exists(path):
            return

        target_dir_path = path
        if os.path.isfile(path):
            target_dir_path = os.path.dirname(path)

        target_dir_path = target_dir_path.replace('/', '\\')
        subprocess.Popen('explorer "' + target_dir_path + '"')

    def change_dress_data_path_edit_disable(self):
        """dress_data_path_editの表示状態をチェックボックスによって変更する
        """

        disabled = self.view.ui.use_tool_dress_data_csv_cb.checkState() == QtCore.Qt.Checked

        self.view.ui.dress_data_csv_path_edit.setDisabled(disabled)
        self.view.ui.set_dress_data_csv_path_button.setDisabled(disabled)
        self.view.ui.open_dress_data_csv_path_button.setDisabled(disabled)


if __name__ == '__main__':

    main = Main()
    main.show_ui()
