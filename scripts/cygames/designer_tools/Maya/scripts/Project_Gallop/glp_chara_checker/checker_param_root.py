# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
    from builtins import range
    from builtins import object
    from importlib import reload
except Exception:
    pass

import os

import maya.cmds as cmds

from ..base_common import utility as base_utility
from ..base_common import classes as base_class

from . import checker_param_list
from . import checker_param_item
from . import checker_info_window

reload(checker_param_list)
reload(checker_param_item)
reload(checker_info_window)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CheckerParamRoot(object):

    # ==================================================
    def __init__(self, main):

        self.main = main

        self.ui_window = None

        self.checker_param_item_list = None
        self.selection_batch_checker_param_item_list = None

        self.info_window = None

        self.batch_ui_dict = None
        self.selection_batch_ui_dict = None

        self.batch_root_dir_path = None
        self.batch_data_path_list = None
        self.batch_output_file_path = None
        self.batch_should_output_each_info = None

        self.batch_error_data_list = None
        self.batch_count_data_list = None

        # 0,1のstrに変換して送信する
        self.selection_batch_binary_str = None

        self.is_selection_mode = None
        self.is_reloaded_with_checker = None

    # ==================================================
    def initialize(self):

        self.checker_param_item_list = []
        self.selection_batch_checker_param_item_list = []

        # 一部実行バッチ関連情報初期化
        self.selection_batch_binary_str = ''
        self.is_selection_mode = False
        self.is_reloaded_with_checker = False

        check_index = 0
        for param_value in checker_param_list.param_value_list:
            new_checker_param_item = checker_param_item.CheckerParamItem(self, param_value)
            new_checker_param_item.initialize()

            new_batch_checker_param_item = checker_param_item.CheckerParamItem(self, param_value, for_batch_list=True)
            new_batch_checker_param_item.initialize()

            if not new_checker_param_item.is_init:
                continue

            if new_checker_param_item.ui_type == 'checker':
                new_checker_param_item.check_index = check_index
                new_batch_checker_param_item.check_index = check_index
                check_index += 1

            self.checker_param_item_list.append(new_checker_param_item)
            self.selection_batch_checker_param_item_list.append(new_batch_checker_param_item)

        self.info_window = checker_info_window.CheckerInfoWindow(self)
        self.info_window.initialize()

    # ==================================================
    def create_ui(self):

        # ui関連dict初期化
        self.batch_ui_dict = {}
        self.selection_batch_ui_dict = {}

        # ウィンドウ
        self.ui_window = \
            base_class.ui.window.Window(
                self.main.window_name,
                self.main.tool_name + '  ' + self.main.tool_version,
                ['個別チェック', 'バッチチェック', 'バッチチェック(一部)'],
                width=600, height=900
            )

        self.ui_window.set_close_function(self.close_window)
        self.ui_window.set_show_function(self.show_window)

        self.ui_window.set_job('SceneOpened', self.change_scene)

        # ------------------------------
        # ヘッダーアタッチ

        cmds.columnLayout(adj=True, p=self.ui_window.ui_body_header_layout_id)

        # 現在のキャラの情報をユーザーに表示 # TDN-5662
        cmds.frameLayout(borderVisible=True, labelVisible=False, marginHeight=5, marginWidth=5)
        cmds.text('lbl_current_chara', label='', align='left')
        cmds.setParent('..')

        cmds.rowLayout(numberOfColumns=2, adj=1)

        form = cmds.formLayout(numberOfDivisions=100)

        all_button = base_class.ui.button.Button(
            '全チェック', self.on_check_all_button, bgc=[0.7, 0.5, 0.5], height=40)

        all_and_csv_button = base_class.ui.button.Button(
            '全チェック + 個別CSV出力', self.on_check_all_and_output_csv_button, bgc=[0.7, 0.5, 0.5], height=40)

        cmds.setParent('..')

        base_class.ui.button.Button(
            'リセット', self.on_reset_button, height=40)

        cmds.setParent('..')

        cmds.formLayout(
            form,
            edit=True,
            attachForm=[(all_button.ui_button_id, 'left', 0), (all_and_csv_button.ui_button_id, 'right', 0)],
            attachPosition=[(all_button.ui_button_id, 'right', 1, 50), (all_and_csv_button.ui_button_id, 'left', 1, 50)],
        )

        # ------------------------------
        # ボディへアタッチ

        cmds.columnLayout(adj=True, p=self.ui_window.ui_body_layout_id)

        for p in range(len(self.checker_param_item_list)):
            self.checker_param_item_list[p].create_ui()

        cmds.setParent('..')

        cmds.setParent('..')

        # ------------------------------
        # フッターアタッチ

        cmds.columnLayout(adj=True, p=self.ui_window.ui_body_footer_layout_id)

        cmds.rowLayout(numberOfColumns=3)

        base_class.ui.button.Button(
            '全チェック', self.on_set_enable_button, True, self.checker_param_item_list, w=100)

        base_class.ui.button.Button(
            'チェックを外す', self.on_set_enable_button, False, self.checker_param_item_list, w=100)

        base_class.ui.button.Button(
            'チェックを反転', self.on_invert_enable_button, self.checker_param_item_list, w=100)

        cmds.setParent('..')

        cmds.setParent('..')

        # ------------------------------
        # バッチ項目のアタッチ

        cmds.columnLayout(
            adj=True, rs=5, p=self.ui_window.ui_body_layout_id_list[1])

        cmds.rowLayout(numberOfColumns=6)

        button_width = 80

        base_class.ui.button.Button(
            'Head設定', self.on_default_batch_setting, 'head', self.batch_ui_dict, w=button_width)

        base_class.ui.button.Button(
            'Body設定', self.on_default_batch_setting, 'body', self.batch_ui_dict, w=button_width)

        base_class.ui.button.Button(
            'Prop設定', self.on_default_batch_setting, 'prop', self.batch_ui_dict, w=button_width)

        base_class.ui.button.Button(
            'ToonProp設定', self.on_default_batch_setting, 'toonprop', self.batch_ui_dict, w=button_width)

        base_class.ui.button.Button(
            'Tail設定', self.on_default_batch_setting, 'tail', self.batch_ui_dict, w=button_width)

        base_class.ui.button.Button(
            'Facial target設定', self.on_default_batch_setting, 'facial_target', self.batch_ui_dict, w=button_width + 20)

        cmds.setParent('..')

        self.batch_ui_dict['ui_input_dir'] = base_class.ui.data_selector.DataSelector(
            '対象フォルダ指定', '', False, True)

        self.batch_ui_dict['ui_input_dir'].set_change_function(self.change_input_dir_path, self.batch_ui_dict)

        self.batch_ui_dict['ui_output_file'] = base_class.ui.data_selector.DataSelector(
            '出力ファイル指定', '', False, False)
        self.batch_ui_dict['ui_output_file'].set_extension_filter('.csv')

        base_class.ui.button.Button(
            'バッチチェック実行', self.execute_batch, bgc=[0.7, 0.5, 0.5], height=40)

        base_class.ui.button.Button(
            'バッチチェック実行 + 個別CSV出力', self.execute_batch_and_output_csv, bgc=[0.7, 0.5, 0.5], height=40)

        cmds.setParent('..')

        # ------------------------------
        # バッチ(一部)項目のアタッチ

        cmds.columnLayout(
            adj=True, rs=5, p=self.ui_window.ui_body_layout_id_list[2])

        cmds.rowLayout(numberOfColumns=6)

        button_width = 80

        base_class.ui.button.Button(
            'Head設定', self.on_default_batch_setting, 'head', self.selection_batch_ui_dict, w=button_width)

        base_class.ui.button.Button(
            'Body設定', self.on_default_batch_setting, 'body', self.selection_batch_ui_dict, w=button_width)

        base_class.ui.button.Button(
            'Prop設定', self.on_default_batch_setting, 'prop', self.selection_batch_ui_dict, w=button_width)

        base_class.ui.button.Button(
            'ToonProp設定', self.on_default_batch_setting, 'toonprop', self.selection_batch_ui_dict, w=button_width)

        base_class.ui.button.Button(
            'Tail設定', self.on_default_batch_setting, 'tail', self.selection_batch_ui_dict, w=button_width)

        base_class.ui.button.Button(
            'Facial target設定', self.on_default_batch_setting, 'facial_target', self.selection_batch_ui_dict, w=button_width + 20)

        cmds.setParent('..')

        self.selection_batch_ui_dict['ui_input_dir'] = base_class.ui.data_selector.DataSelector(
            '対象フォルダ指定', '', False, True)

        self.selection_batch_ui_dict['ui_input_dir'].set_change_function(self.change_input_dir_path, self.selection_batch_ui_dict)

        self.selection_batch_ui_dict['ui_output_file'] = base_class.ui.data_selector.DataSelector(
            '出力ファイル指定', '', False, False)
        self.selection_batch_ui_dict['ui_output_file'].set_extension_filter('.csv')

        target_check_area_lo = cmds.frameLayout(self.ui_window.ui_body_layout_id_list[2], lv=False, bv=True, mw=10, mh=10)

        cmds.columnLayout(adj=True, p=target_check_area_lo)

        base_class.ui.label.Label('対象チェック項目')

        for p in range(len(self.selection_batch_checker_param_item_list)):
            self.selection_batch_checker_param_item_list[p].create_ui()

        cmds.setParent('..')

        cmds.columnLayout(adj=True, p=self.ui_window.ui_body_footer_layout_id_list[2])

        cmds.rowLayout(numberOfColumns=3)

        base_class.ui.button.Button(
            '全チェック', self.on_set_enable_button, True, self.selection_batch_checker_param_item_list, w=100)

        base_class.ui.button.Button(
            'チェックを外す', self.on_set_enable_button, False, self.selection_batch_checker_param_item_list, w=100)

        base_class.ui.button.Button(
            'チェックを反転', self.on_invert_enable_button, self.selection_batch_checker_param_item_list, w=100)

        cmds.setParent('..')

        base_class.ui.button.Button(
            '一部バッチチェック実行', self.execute_selection_batch, bgc=[0.7, 0.5, 0.5], height=40)

        cmds.setParent('..')

        self.set_visible_button()

        self.update_ui()

        self.ui_window.show()

    # ==================================================
    def set_visible_button(self):

        view_error_btn_visible = False
        select_error_btn_visible = False
        fix_error_btn_visible = False

        view_unerror_btn_visible = False
        select_unerror_btn_visible = False

        view_target_btn_visible = False
        select_target_btn_visible = False

        for item in self.checker_param_item_list:

            if item.ui_type != 'checker':
                continue

            view_error_visible = item.ui_error_view_button.apply_button_param(
                q=True, vis=True)

            select_error_visible = item.ui_error_select_button.apply_button_param(
                q=True, vis=True)

            fix_error_visible = item.ui_error_fix_button.apply_button_param(
                q=True, vis=True)

            view_unerror_visible = item.ui_unerror_view_button.apply_button_param(
                q=True, vis=True)

            select_unerror_visible = item.ui_unerror_select_button.apply_button_param(
                q=True, vis=True)

            view_target_visible = item.ui_target_view_button.apply_button_param(
                q=True, vis=True)

            select_target_visible = item.ui_target_select_button.apply_button_param(
                q=True, vis=True)

            if view_error_visible:
                view_error_btn_visible = True

            if select_error_visible:
                select_error_btn_visible = True

            if fix_error_visible:
                fix_error_btn_visible = True

            if view_unerror_visible:
                view_unerror_btn_visible = True

            if select_unerror_visible:
                select_unerror_btn_visible = True

            if view_target_visible:
                view_target_btn_visible = True

            if select_target_visible:
                select_target_btn_visible = True

        for item in self.checker_param_item_list:

            if item.ui_type != 'checker':
                continue

            if not view_error_btn_visible:

                item.ui_error_view_button.apply_button_param(
                    e=True, width=1)

            if not select_error_btn_visible:

                item.ui_error_select_button.apply_button_param(
                    e=True, width=1)

            if not fix_error_btn_visible:

                item.ui_error_fix_button.apply_button_param(
                    e=True, width=1)

            if not view_unerror_btn_visible:

                item.ui_unerror_view_button.apply_button_param(
                    e=True, width=1)

            if not select_unerror_btn_visible:

                item.ui_unerror_select_button.apply_button_param(
                    e=True, width=1)

            if not view_target_btn_visible:

                item.ui_target_view_button.apply_button_param(
                    e=True, width=1)

            if not select_target_btn_visible:

                item.ui_target_select_button.apply_button_param(
                    e=True, width=1)

    # ==================================================
    def update_ui(self):
        """
        UIの更新
        """
        # 現在のシーンパスに合わせCharaInfoを更新
        self.main.update_chara_info()

        target_file_name = '-'
        txt_height = '-'
        txt_shape = '-'
        txt_bust = '-'
        txt_mini_bust = ''
        txt_use_user_chara_data_csv = 'なし'

        # ユーザーに表示する現在のキャラの情報を更新 # TDN-5662
        if self.main.chara_info and self.main.chara_info.exists:

            chara_info = self.main.chara_info
            data_info = self.main.chara_info.data_info

            target_file_name = str(chara_info.file_name_without_ext)

            if self.main.chara_info.data_info.exists:

                if not [v for v in [data_info.height_id, data_info.shape_id, data_info.bust_id] if v is None or v == '']:
                    # 表示テキスト準備
                    txt_height = '{}({})'.format(chara_info.height_lbls[data_info.height_id], str(data_info.height_id))
                    txt_shape = '{}({})'.format(chara_info.body_type_lbls[data_info.shape_id], str(data_info.shape_id))
                    txt_bust = '{}({})'.format(chara_info.bust_lbls[data_info.bust_id], str(data_info.bust_id))

                    if chara_info.is_mini:
                        if data_info.mini_bust_id:
                            txt_mini_bust += '\tミニバスト: {}({})'.format(chara_info.mini_bust_lbls[data_info.mini_bust_id], str(data_info.mini_bust_id))
                        else:
                            txt_mini_bust += '\tミニバスト: unknown'

                if self.main.is_use_user_create_chara_data_csv:
                    txt_use_user_chara_data_csv = 'ユーザーが同階層に格納したchara_data.csv'
                else:
                    txt_use_user_chara_data_csv = 'ツール本体側のchara_data.csv'

            else:
                if self.main.chara_info.is_unique_chara:
                    txt_use_user_chara_data_csv = 'なし(キャラクターの情報がchara_data.csvから取得できません)'

        lbl_text = '現在の対象: {}\n身長: {}\t体型: {}\tバスト: {}{}\n現在読み込んでいるデータ: {}'.format(
            target_file_name, txt_height, txt_shape, txt_bust, txt_mini_bust, txt_use_user_chara_data_csv)
        cmds.text('lbl_current_chara', e=True, label=lbl_text)

        # ウィンドウのチェック項目を更新
        for item in self.checker_param_item_list:
            item.update_ui()

    # ==================================================
    def reset_ui(self):

        for item in self.checker_param_item_list:
            item.reset_info()

        self.update_ui()

    # ==================================================
    def show_window(self):

        self.load_setting()

    # ==================================================
    def close_window(self):

        self.info_window.close()

        self.save_setting()

    # ==================================================
    def change_scene(self):

        if not self.is_reloaded_with_checker:
            self.info_window.close()
            self.reset_ui()

        # 全check後のScene changedは複数回発生していても、
        # 一つのシグナル送出のみのためフラグを戻して問題ない。
        self.is_reloaded_with_checker = False

    # ==================================================
    def on_check_all_button(self):
        self._on_check_all_button_base(False)

    # ==================================================
    def on_check_all_and_output_csv_button(self):
        self._on_check_all_button_base(True)

    # ==================================================
    def _on_check_all_button_base(self, should_output_csv):

        if should_output_csv:
            confirm_text = '全チェック＋CSV出力しますか?'
        else:
            confirm_text = '全チェックしますか?'

        if not base_utility.ui.dialog.open_ok_cancel(
                '確認', confirm_text, self.main.window_name):
            return

        if not cmds.file(q=True, sn=True):
            cmds.confirmDialog(
                title='Warning',
                message='ファイルをセーブして再度実行してください。',
                button=['OK'],
                defaultButton='OK',
                icon='warning'
            )
            return

        # チェック前にセーブ
        cmds.file(save=True, type='mayaAscii')

        self.reset_ui()

        base_utility.ui.progressbar.start('全チェック')

        max_count = 0

        for item in self.checker_param_item_list:

            if item.ui_type != 'checker' and item.ui_type != 'info':
                continue

            max_count += 1

        count = 0
        for item in self.checker_param_item_list:
            count += 1

            if not base_utility.ui.progressbar.update(
                    item.label, count, max_count, 1, 1):
                break

            result = item.update_error_target_list()
            if result != '':
                error_message = 'チェッカー番号:{}\n項目名:{}\nのチェック実行時にエラーが発生しました。\nダイアログをスクリーンショット撮影し、TA班までご連絡ください。\n\n{}'.format(
                    item.check_index + 1, item.label, result
                )
                cmds.confirmDialog(
                    title='CheckerError',
                    message=error_message,
                    button=['OK'],
                    defaultButton='OK',
                    icon='critical'
                )
                base_utility.ui.progressbar.end()
                return

        if should_output_csv:
            self.export_each_info_csv(True)

        base_utility.ui.progressbar.end()

        self.update_ui()

    # ==================================================
    def on_reset_button(self):

        self.reset_ui()

    # ==================================================
    def export_each_info_csv(self, should_open_dir):

        self.main.each_info_logger.clear_log()

        info_item_list = []

        for item in self.checker_param_item_list:

            if item.ui_type != 'info':
                continue

            if not item.is_check_data:
                continue

            info_item_list.append(item)

        if not info_item_list:
            return

        export_dir = self.main.chara_info.file_root_dir
        export_file_name = self.main.chara_info.file_name_without_ext + '_info.csv'

        # infoデータの書き出し
        for item in info_item_list:

            this_str = self._create_info_str(item) + '\n'
            self.main.each_info_logger.write_log(this_str)

        # エラー詳細の書き出し
        error_header = '【エラー詳細】'
        error_count = 0
        error_bdy = ''

        for item in self.checker_param_item_list:

            if item.ui_type != 'checker':
                continue

            if item.error_target_list and not item.is_warning:

                error_bdy += item.label
                error_count += 1

                for error_target in item.error_target_list:

                    if not error_target:
                        continue

                    error_bdy += (',' + error_target)

                error_bdy += '\n'

        error_str = error_header + '\nエラー総数 : ' + self._convert_to_unicode(error_count) + '\n' + error_bdy
        self.main.each_info_logger.write_log(error_str)

        # warning詳細の書き出し
        warning_header = '【警告詳細】'
        warning_count = 0
        warning_bdy = ''

        for item in self.checker_param_item_list:

            if item.ui_type != 'checker':
                continue

            if item.error_target_list and item.is_warning:

                warning_bdy += item.label
                warning_count += 1

                for warning_target in item.error_target_list:

                    if not warning_target:
                        continue

                    warning_bdy += (',' + warning_target)

                warning_bdy += '\n'

        warning_str = warning_header + '\n警告総数 : ' + self._convert_to_unicode(warning_count) + '\n' + warning_bdy
        self.main.each_info_logger.write_log(warning_str)

        # csv出力
        try:
            # Python2ではエンコーディング指定必要
            self.main.each_info_logger.encode_type = 'shift-jis'
            self.main.each_info_logger.output_log(export_dir + '\\' + export_file_name)

            if should_open_dir:
                base_utility.io.open_directory(export_dir + '\\' + export_file_name)
        except Exception:
            base_utility.ui.dialog.open_ok('CSV出力エラー', 'CSVが開かれていないことを確認してください')
            return

    # ==================================================
    def _create_info_str(self, info_item):

        result_str = ''

        # タイトル
        if info_item.info_title:
            result_str += (info_item.info_title + '\n')

        # ヘッダー
        if info_item.info_column_list:
            result_str += (','.join(info_item.info_column_list) + '\n')

        # infoデータ
        if not info_item.info_dict_list:
            return result_str

        for info_dict in info_item.info_dict_list:

            if not info_dict.get('item') or not info_dict.get('value_list'):
                continue

            result_str += (info_dict['item'] + ',')

            for value in info_dict['value_list']:
                result_str += (self._convert_to_unicode(value) + ',')

            # チェッカーからエラーを取得
            if not info_dict.get('link_check_label_list'):
                result_str += '\n'
                continue

            error_visible = False
            error_list = []

            if info_dict['link_check_label_list']:

                error_visible = True
                error_list = self._get_error_label_list_from_checker(info_dict, info_item.info_has_link_to_error_target)

            if error_visible:
                if not error_list:
                    result_str += ('正常' + ',')
                else:
                    result_str += ('エラー : ' + ' | '.join(error_list) + ',')

            result_str += '\n'

        return result_str

    # ==================================================
    def _get_error_label_list_from_checker(self, info_dict, item_links_to_error_target):

        error_list = []

        for target_label in info_dict['link_check_label_list']:

            for checker_item in self.checker_param_item_list:

                if target_label == checker_item.label:

                    if not item_links_to_error_target:

                        # リンクしていなければエラーの有無のみでラベルを表示
                        if checker_item.error_target_list:
                            error_list.append(target_label)

                        break

                    else:

                        # リンクしているならエラーの有無+アイテム名との一致でラベルを表示
                        for error_target in checker_item.error_target_list:

                            if not error_target:
                                continue

                            if error_target.find(info_dict['item']) >= 0:
                                error_list.append(target_label)
                        break

        return error_list

    # ==================================================
    def export_csv(self):

        self.batch_root_dir_path = \
            base_utility.simple_batch.get_param_value(
                'batch_root_dir_path')

        self.batch_data_path_list = \
            base_utility.simple_batch.get_param_value(
                'batch_data_path_list')

        self.batch_output_file_path = \
            base_utility.simple_batch.get_param_value(
                'batch_output_file_path')

        self.batch_should_output_each_info = \
            base_utility.simple_batch.get_param_value(
                'batch_should_output_each_info')

        self.selection_batch_binary_str = \
            base_utility.simple_batch.get_param_value(
                'selection_batch_binary_str'
            )

        if self.selection_batch_binary_str:
            self.is_selection_mode = True

        if not self.batch_root_dir_path:
            return

        if not self.batch_data_path_list:
            return

        if not self.batch_output_file_path:
            return

        if self.batch_should_output_each_info == 'True':
            self.batch_should_output_each_info = True
        else:
            self.batch_should_output_each_info = False

        self.main.logger.clear_log()

        self.write_header_to_logger()

        self.write_check_info_to_logger(self.batch_should_output_each_info)

        self.output_from_logger()

    # ==================================================
    def write_header_to_logger(self):

        log_header_string = 'ファイル名,'

        if not self.is_selection_mode:
            for param_value in checker_param_list.param_value_list:

                this_ui_type = 'checker'
                if 'ui_type' in param_value:
                    this_ui_type = param_value['ui_type']

                if this_ui_type != 'checker':
                    continue

                this_target_count_info = ''
                if 'target_count_info' in param_value:
                    this_target_count_info = param_value['target_count_info']

                if this_target_count_info:
                    log_header_string += this_target_count_info + ','

            log_header_string += 'エラーチェック結果,'

        current_index = 0
        for param_value in checker_param_list.param_value_list:

            this_ui_type = 'checker'
            if 'ui_type' in param_value:
                this_ui_type = param_value['ui_type']

            if this_ui_type != 'checker':
                continue

            this_label = ''
            if 'label' in param_value:
                this_label = param_value['label']

            if this_label:
                if not self.is_selection_mode or self.selection_batch_binary_str[current_index] == '1':
                    log_header_string += this_label + ','

            current_index += 1

        self.main.logger.write_log(log_header_string)

    # ==================================================
    def write_check_info_to_logger(self, should_output_each_info):

        max_count = len(self.batch_data_path_list)
        count = -1
        for data_path in self.batch_data_path_list:
            count += 1

            fix_data_path = self.batch_root_dir_path + '/' + data_path

            if not base_utility.file.open(fix_data_path):
                continue

            self.main.update_chara_info()

            self.batch_error_data_list = []
            self.batch_count_data_list = []

            this_info = ' ' + str(count + 1) + '/' + str(max_count) + '  '
            this_info += os.path.basename(fix_data_path)

            base_utility.batch.batch_print('')
            base_utility.batch.batch_print('=' * 60)

            base_utility.batch.batch_print(this_info)

            base_utility.batch.batch_print('=' * 60)
            base_utility.batch.batch_print('')

            base_utility.batch.batch_print((' チェック開始......\n'))

            param_item_index = -1
            for item in self.checker_param_item_list:

                if item.ui_type != 'checker' and item.ui_type != 'info':
                    continue

                # infoはindexに含まれていないため選択実行モードはカウントしてしまうと範囲外参照が起きる
                if item.ui_type == 'checker':
                    param_item_index += 1
                    if self.is_selection_mode and self.selection_batch_binary_str[param_item_index] == '0':
                        continue

                item.update_enable_flag()
                result = item.update_error_target_list()
                if result != '':
                    error_message = '\nチェッカー番号:{}\n項目名:{}\nのチェック実行時にエラーが発生しました。\nバッチ画面をスクリーンショット撮影し、TA班までご連絡ください !\n\n{}'.format(
                        item.check_index + 1, item.label, result
                    )
                    base_utility.batch.batch_print((error_message))
                    return
                item.write_to_result_data_list()

            result_string = self.main.chara_info.file_name + ','

            if not self.is_selection_mode:
                error_count = 0
                for error_data in self.batch_error_data_list:

                    if error_data.find('×') >= 0:
                        error_count += 1

                for batch_count_data in self.batch_count_data_list:
                    result_string += batch_count_data + ','

                if error_count != 0:
                    result_string += '× (' + str(error_count) + '),'
                else:
                    result_string += '◎,'

            if self.batch_error_data_list:
                for batch_error_data in self.batch_error_data_list:
                    if self.is_selection_mode and '×' in batch_error_data:
                        batch_error_data = '×'
                    result_string += batch_error_data + ','

            self.main.logger.write_log(result_string)

            if should_output_each_info:
                self.export_each_info_csv(False)

            base_utility.batch.batch_print(('\n チェック終了 !\n'))

    # ==================================================
    def output_from_logger(self):

        self.main.logger.encode_type = 'shift-jis'
        self.main.logger.output_log(self.batch_output_file_path)

        base_utility.io.open_directory(self.batch_output_file_path)

    # ==================================================
    def on_set_enable_button(self, enable, target_param_item_list):

        for item in target_param_item_list:
            item.set_enable_button(enable)

    # ==================================================
    def on_invert_enable_button(self, target_param_item_list):

        for item in target_param_item_list:

            if not item.ui_enable_button:
                continue

            if item.ui_enable_button.get_value():
                item.set_enable_button(False)
            else:
                item.set_enable_button(True)

    # ==================================================
    def change_input_dir_path(self, ui_dict):

        input_dir_path = ui_dict['ui_input_dir'].get_path()
        output_file_path = ui_dict['ui_output_file'].get_path()

        if not output_file_path and input_dir_path:
            if os.path.isdir(input_dir_path):
                ui_dict['ui_output_file'].set_path(input_dir_path + '/output.csv')

    # ==================================================
    def on_default_batch_setting(self, this_type, ui_dict):

        this_input_dir_path = None
        this_filter = None
        this_nofilter = None
        this_ext_filter = '.ma'
        this_output_file_path = None

        if this_type == 'head':

            this_input_dir_path = 'W:/gallop/svn/svn_gallop/80_3D/01_character/01_model/head'
            this_output_file_path = 'W:/gallop/svn/svn_gallop/80_3D/01_character/01_model/check_head.csv'

            this_filter = r'mdl_chr\d{4}_\d{2}\.ma,mdl_chr\d{4}_\d{2}_(face\d{3}|hair\d{3})\.ma'
            this_nofilter = 'face_target,ear_target,rig,old,temp,_99'

        elif this_type == 'facial_target':

            this_input_dir_path = 'W:/gallop/svn/svn_gallop/80_3D/01_character/01_model/head'
            this_output_file_path = 'W:/gallop/svn/svn_gallop/80_3D/01_character/01_model/check_facial_target.csv'

            this_filter = r'mdl_chr\d{4}_\d{2}\_facial_target\.ma'
            this_nofilter = 'ear_target,rig,old,temp,_99'

        elif this_type == 'body':

            this_input_dir_path = 'W:/gallop/svn/svn_gallop/80_3D/01_character/01_model/body'
            this_output_file_path = 'W:/gallop/svn/svn_gallop/80_3D/01_character/01_model/check_body.csv'

            this_filter = r'mdl_bdy\d{4}_\d{2}(|_\d{2})(|_BustL|_BustM)\.ma'
            this_nofilter = 'old,temp,bdy0000'

        elif this_type == 'prop':

            this_input_dir_path = 'W:/gallop/svn/svn_gallop/80_3D/01_character/01_model/prop'
            this_output_file_path = 'W:/gallop/svn/svn_gallop/80_3D/01_character/01_model/check_prop.csv'

            this_filter = r'mdl_chr_prop\d{4}_\d{2}\.ma'
            this_nofilter = 'old,temp'

        elif this_type == 'toonprop':

            this_input_dir_path = 'W:/gallop/svn/svn_gallop/80_3D/01_character/01_model/toon_prop'
            this_output_file_path = 'W:/gallop/svn/svn_gallop/80_3D/01_character/01_model/check_toon_prop.csv'

            this_filter = r'mdl_toon_prop\d{4}_\d{2}\.ma'
            this_nofilter = 'old,temp'

        elif this_type == 'tail':

            this_input_dir_path = 'W:/gallop/svn/svn_gallop/80_3D/01_character/01_model/tail'
            this_output_file_path = 'W:/gallop/svn/svn_gallop/80_3D/01_character/01_model/check_tail.csv'

            this_filter = r'mdl_tail\d{4}_\d{2}\.ma'
            this_nofilter = 'old,temp'

        ui_dict['ui_input_dir'].set_path(this_input_dir_path)

        ui_dict['ui_input_dir'].set_file_filter(
            this_filter, this_nofilter)

        ui_dict['ui_input_dir'].set_extension_filter(this_ext_filter)
        ui_dict['ui_input_dir'].set_dir_filter('', 'old,temp')
        ui_dict['ui_input_dir'].set_contain_lower(True)

        ui_dict['ui_output_file'].set_path(this_output_file_path)

    # ==================================================
    def execute_batch(self):
        self._execute_batch_base('False', self.batch_ui_dict)

    # ==================================================
    def execute_selection_batch(self):
        self.selection_batch_binary_str = ''
        for item in self.selection_batch_checker_param_item_list:
            if item.ui_type == 'checker':
                if item.is_root_enable:
                    self.selection_batch_binary_str += '1'
                else:
                    self.selection_batch_binary_str += '0'

        self._execute_batch_base('False', self.selection_batch_ui_dict)

        self.selection_batch_binary_str = ''

    # ==================================================
    def execute_batch_and_output_csv(self):
        self._execute_batch_base('True', self.batch_ui_dict)

    # ==================================================
    def _execute_batch_base(self, should_output_each_info, ui_dict):

        output_file_path = ui_dict['ui_output_file'].get_path()

        if not output_file_path:
            base_utility.ui.dialog.open_ok(
                '確認', '出力ファイルパスが設定されていません', self.ui_window.ui_window_id)
            return

        if output_file_path.find('.csv') <= 0:
            base_utility.ui.dialog.open_ok(
                '確認', '出力ファイルパスが設定されていません', self.ui_window.ui_window_id)
            return

        data_path_list = ui_dict['ui_input_dir'].get_data_path_list()

        if not data_path_list:
            base_utility.ui.dialog.open_ok(
                '確認', '対象となるパスが見つかりませんでした', self.ui_window.ui_window_id)
            return

        if not base_utility.ui.dialog.open_ok_cancel(
            '確認', 'バッチ処理を実行しますか ?', self.ui_window.ui_window_id
        ):
            return

        root_dir_path = ui_dict['ui_input_dir'].get_path()

        fix_data_path_list = []

        for data_path in data_path_list:

            fix_data_path = data_path.replace(root_dir_path + '/', '')
            fix_data_path_list.append(fix_data_path)

        base_utility.simple_batch.execute(
            'import Project_Gallop.glp_chara_checker.main;Project_Gallop.glp_chara_checker.main.export_csv();',
            False,
            batch_root_dir_path=root_dir_path,
            batch_data_path_list=fix_data_path_list,
            batch_output_file_path=output_file_path,
            batch_should_output_each_info=should_output_each_info,
            selection_batch_binary_str=self.selection_batch_binary_str)

    # ==================================================
    def load_setting(self):

        self.ui_window.load_setting(self.main.setting, 'MainWindow')
        self.batch_ui_dict['ui_input_dir'].load_setting(self.main.setting, 'InputDir')
        self.batch_ui_dict['ui_output_file'].load_setting(self.main.setting, 'OutputFile')
        self.selection_batch_ui_dict['ui_input_dir'].load_setting(self.main.setting, 'InputDirSelection')
        self.selection_batch_ui_dict['ui_output_file'].load_setting(self.main.setting, 'OutputFileSelection')

    # ==================================================
    def save_setting(self):

        self.ui_window.save_setting(self.main.setting, 'MainWindow')
        self.batch_ui_dict['ui_input_dir'].save_setting(self.main.setting, 'InputDir')
        self.batch_ui_dict['ui_output_file'].save_setting(self.main.setting, 'OutputFile')
        self.selection_batch_ui_dict['ui_input_dir'].save_setting(self.main.setting, 'InputDirSelection')
        self.selection_batch_ui_dict['ui_output_file'].save_setting(self.main.setting, 'OutputFileSelection')

    # ==================================================
    def _convert_to_unicode(self, value):

        if type(value) is int:
            return str(value)
        else:
            return value
