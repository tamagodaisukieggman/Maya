# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os
import datetime
import glob
import sys
from functools import partial

import maya.cmds as cmds

from .. import base_common
from ..base_common import utility as base_utility

try:
    # Maya2022-
    from builtins import str
    from builtins import object
    from importlib import reload
except Exception:
    pass

reload(base_common)


class CheckerUIReferer(object):
    """
    チェッカー系のUIの継承用クラス
    主にUIの作成(V部分)を行う
    """

    def __init__(self):
        """
        """
        # ツール名
        self.tool_name = 'checker_ui_referer'
        # version
        self.tool_version = '00000000'

        # windowの初期サイズ
        self.window_min_size = 600

        # fremeのマージン
        self.frame_margin = 5
        # チェックボタンのサイズ
        self.checker_button_width = 40

        # # チェックアイテムの一覧
        self.check_item_list = []

        # # チェックアイテムのパラメータ一覧
        self.check_item_param_list = []

        # 内製かどうか
        self.is_internal = False

        # ログ領域
        self.log_field = None

        # バッチ起動かどうか
        self.is_batch_exec = False

        # バッチ起動時のデフォ値
        self.dir_path = ''
        self.file_name_filter = ''
        self.file_name_ignore_filter = ''
        self.is_exec_child_dir = False
        self.log_save_dir_path = ''

        # このスクリプト自身のパス、ディレクトリ
        self.script_file_path = os.path.abspath(__file__)
        self.script_dir_path = os.path.dirname(self.script_file_path)

        # mayaのバージョン
        self.maya_version = cmds.about(v=True)

        self.batch_cmd_str = '{0}{1}'.format(
            'import Project_Gallop.checker_ui_referer;',
            'Project_Gallop.checker_ui_referer.CheckerUIReferer().batch_exec();'
        )

    # ------------------------------------------------------------

    def initialize(self):
        """
        create_uiの前に実行したい事があればこちらに
        基本的には空
        """

        return True

    # ------------------------------------------------------------

    def delayedInitialize(self):
        """
        create_uiの後に実行したいことがあればこちらに
        基本的には空
        """

        return True

    # ------------------------------------------------------------

    def _set_ui_setting(self):
        """
        """

        if not self.is_batch_exec:

            self.dir_path = cmds.textFieldGrp(self.ui_target_dir_path, q=True, tx=True)
            self.file_name_filter = cmds.textFieldGrp(self.ui_target_filter, q=True, tx=True)
            self.file_name_ignore_filter = cmds.textFieldGrp(self.ui_target_ignore_filter, q=True, tx=True)
            self.log_save_dir_path = cmds.textFieldGrp(self.ui_log_save_dir, q=True, tx=True)
            self.is_exec_child_dir = cmds.checkBox(self.ui_is_exec_child_dir_checkbox, q=True, v=True)

            self._save_setting()

    # ------------------------------------------------------------

    def _load_setting(self, *args, **keywords):
        """
        何らかの設定をロードしたいときに使用する
        基本的に空
        """

        pass
    # ------------------------------------------------------------

    def _save_setting(self, *args, **keywords):
        """
        何らかの設定をセーブしたいときに使用する
        また、フォルダ指定チェックでテキストフィールド上でenterを押したときの挙動
        基本的には空
        """

        pass

    # ------------------------------------------------------------

    def reset_ui(self, *args, **keywords):
        """
        UIの状態を初期状態に戻す
        """

        for check_item_param in self.check_item_param_list:

            if check_item_param.is_internal and not self.is_internal:
                continue

            if 'is_target' in check_item_param.ui_info:
                cmds.checkBox(check_item_param.ui_info['is_target'], e=True, v=True)
            if 'individual_check' in check_item_param.ui_info:
                cmds.button(check_item_param.ui_info['individual_check'], e=True, bgc=[0.37, 0.37, 0.37])
            if 'log' in check_item_param.ui_info:
                cmds.button(check_item_param.ui_info['log'], e=True, enable=False)
            if 'list' in check_item_param.ui_info:
                cmds.button(check_item_param.ui_info['list'], e=True, enable=False)
            if 'select' in check_item_param.ui_info:
                cmds.button(check_item_param.ui_info['select'], e=True, enable=False)
            if 'correction' in check_item_param.ui_info:
                cmds.button(check_item_param.ui_info['correction'], e=True, enable=False)

    # ------------------------------------------------------------

    def change_all_check_box_value(self, *args, **keywords):
        """
        checkBoxの状態を変更する
        """

        check_value = True

        if 'value' in keywords:
            check_value = keywords['value']

        for check_item_param in self.check_item_param_list:

            if check_item_param.is_internal and not self.is_internal:
                continue

            cmds.checkBox(check_item_param.ui_info['is_target'], e=True, v=check_value)

    # ------------------------------------------------------------

    def all_exec(self, *args, **keywords):
        """
        すべて実行
        """

        for check_item_param in self.check_item_param_list:

            if check_item_param.is_internal and not self.is_internal:
                continue

            if not cmds.checkBox(check_item_param.ui_info['is_target'], q=True, v=True):
                continue

            self.exec_cmd(item_param=check_item_param)

    # ------------------------------------------------------------

    def show_log(self, *args, **keywords):
        """
        ログ表示
        """

        if not self.log_field:
            return

        item_param = keywords['item_param']
        log_str = '{0}\n\n{1}\n\n{2}'.format(
            item_param.label,
            item_param.check_answer_info.error_message,
            '\n'.join(item_param.check_answer_info.invalid_item_list)
        )

        cmds.scrollField(self.log_field, e=True, tx=log_str)

    def clear_log(self, *args, **keywords):
        """
        ログを消去する
        """

        if not self.log_field:
            return

        cmds.scrollField(self.log_field, e=True, tx='')

    # ------------------------------------------------------------

    def create_ui(self):
        """
        ui作成
        """

        # window名
        self.window_name = '{0}Window'.format(self.tool_name)
        # windowタイトル
        self.window_title = '{0} ver {1}'.format(self.tool_name, self.tool_version)

        if not self.initialize():
            return

        # window重複削除
        if cmds.window(self.window_name, exists=True):
            cmds.deleteUI(self.window_name, window=True)

        self.window_name = cmds.window(self.window_name, t=self.window_title)
        cmds.window(self.window_name, e=True, w=self.window_min_size, h=800)

        self.create_ui_container()

        cmds.showWindow(self.window_name)

        self.delayedInitialize()

    # ------------------------------------------------------------

    def create_ui_container(self):
        """
        ui 全体コンテナ部分
        """
        container = cmds.formLayout()

        check_part = self.create_ui_check_part()

        batch_check_part = self.create_ui_batch_check_part()

        log_part = self.create_ui_log_part()

        cmds.formLayout(
            container, e=True,
            attachForm=[
                (check_part, 'top', 0),
                (check_part, 'left', 0),
                (check_part, 'right', 0),
                (batch_check_part, 'left', 0),
                (batch_check_part, 'right', 0),
                (log_part, 'left', 0),
                (log_part, 'right', 0),
                (log_part, 'bottom', 0)
            ],
            attachControl=[
                (check_part, 'bottom', 0, batch_check_part),
                (batch_check_part, 'bottom', 0, log_part)
            ],
            attachNone=[
                (batch_check_part, 'top'),
            ]
        )

        return container

    # ------------------------------------------------------------

    def create_ui_check_part(self):
        """
        ui 通常チェック部分作成
        """
        container = cmds.frameLayout(l='通常チェック', cll=False, cl=False, mh=self.frame_margin, mw=self.frame_margin, bv=True)

        form = cmds.formLayout(numberOfDivisions=100)
        scroll = cmds.scrollLayout(childResizable=True, vsb=True, hst=0)

        for check_param_item in self.check_item_param_list:
            if check_param_item.is_internal and not self.is_internal:
                continue
            check_param_item = self.checker_ui_group(check_param_item)

        cmds.setParent('..')

        exec_button = cmds.button(l='すべて実行', c=partial(self.all_exec))
        reset_button = cmds.button(l='状態をリセット', c=partial(self.reset_ui))
        check_button = cmds.button(l='すべてチェック', c=partial(self.change_all_check_box_value, value=True))
        uncheck_button = cmds.button(l='チェックを外す', c=partial(self.change_all_check_box_value, value=False))

        cmds.formLayout(
            form, e=True, attachForm=[
                (scroll, 'top', 0), (scroll, 'left', 0), (scroll, 'right', 0),
                (exec_button, 'left', 2), (exec_button, 'right', 2),
                (reset_button, 'left', 2), (reset_button, 'bottom', 2),
                (check_button, 'bottom', 2),
                (uncheck_button, 'right', 2), (uncheck_button, 'bottom', 2)
            ],
            attachControl=[
                (scroll, 'bottom', 5, exec_button),
                (exec_button, 'bottom', 5, reset_button),
                (check_button, 'left', 2, reset_button),
                (check_button, 'right', 2, uncheck_button),
            ],
            attachPosition=[
                (reset_button, 'right', 0, 33),
                (uncheck_button, 'left', 0, 67)
            ]
        )
        cmds.setParent('..')

        cmds.setParent('..')

        return container

    # ------------------------------------------------------------

    def checker_ui_group(self, item_param):
        """
        チェッカー単体のUIセット
        """

        cmds.rowLayout(adjustableColumn=1, numberOfColumns=2, cal=[1, 'left'], h=40)

        cmds.rowLayout(
            adjustableColumn=4, numberOfColumns=4, cal=[4, 'left'],
            columnAttach4=['left', 'left', 'left', 'left'],
            columnOffset4=[0, 5, 0, 5]
        )

        is_target_check_box = cmds.checkBox(l='', v=True)
        individual_check_button = cmds.button(l='実行', c=partial(self.exec_cmd, item_param=item_param))
        info_button = cmds.button(l='情報', c=partial(self.show_info_window, item_param=item_param))
        label_text = cmds.text(l=item_param.label, h=22)
        if item_param.is_internal:
            cmds.text(label_text, e=True, backgroundColor=[0, 0.8, 0])
        cmds.setParent('..')

        cmds.rowLayout(
            numberOfColumns=4,
            columnAttach4=['right', 'right', 'right', 'right'],
            columnOffset4=[2, 2, 2, 5]
        )

        # ログボタン
        if item_param.is_log_button_view:
            log_button = cmds.button(l='ログ', enable=False, w=self.checker_button_width, c=partial(self.show_log, item_param=item_param))
        else:
            log_button = cmds.button(l='', enable=False, w=self.checker_button_width)

        # リストボタン
        if item_param.is_list_button_view:
            list_button = cmds.button(l='リスト', enable=False, w=self.checker_button_width, c=partial(self.show_target_list_window, item_param=item_param))
        else:
            list_button = cmds.button(l='', enable=False, w=self.checker_button_width)

        if item_param.is_select_button_view:
            select_button = cmds.button(l='選択', w=self.checker_button_width, enable=False, c=partial(self.select_button_cmd, item_param=item_param))
        else:
            select_button = cmds.button(l='', enable=False, w=self.checker_button_width)

        if item_param.is_correction_button_view:
            correction_button = cmds.button(l='修正', w=self.checker_button_width, enable=False, c=partial(self.revise_button_cmd, item_param=item_param))
        else:
            correction_button = cmds.button(l='', enable=False, w=self.checker_button_width)

        cmds.setParent('..')

        cmds.setParent('..')
        cmds.separator(style='in')

        # item_paramにUI情報を入れる
        item_param.ui_info['is_target'] = is_target_check_box
        item_param.ui_info['individual_check'] = individual_check_button
        item_param.ui_info['info'] = info_button
        item_param.ui_info['log'] = log_button
        item_param.ui_info['list'] = list_button
        item_param.ui_info['correction'] = correction_button
        item_param.ui_info['select'] = select_button

        return item_param

    # ------------------------------------------------------------

    def show_checker_option_window(self, description, item_list):
        """
        """

        list_window_name = 'StageCheckerOptionWindow'

        # window重複削除
        self.close_window(window_name=list_window_name)

        cmds.window(list_window_name, t='チェックリスト')
        cmds.window(list_window_name, e=True, w=400, h=400)
        form = cmds.formLayout()

        desc_ui = cmds.text(l=description, align='left')
        scroll_ui = cmds.textScrollList(numberOfRows=8, append=item_list)
        close_ui = cmds.button(l='閉じる', c=partial(self.close_window, window_name=list_window_name))

        cmds.formLayout(
            form, e=True,
            attachForm=[
                (desc_ui, 'top', 5),
                (desc_ui, 'left', 5),
                (desc_ui, 'right', 5),
                (scroll_ui, 'left', 5),
                (scroll_ui, 'right', 5),
                (close_ui, 'left', 5),
                (close_ui, 'right', 5),
                (close_ui, 'bottom', 5)
            ],
            attachControl=[
                (scroll_ui, 'top', 5, desc_ui),
                (scroll_ui, 'bottom', 5, close_ui),
            ]
        )
        cmds.setParent('..')
        cmds.showWindow(list_window_name)

    # ------------------------------------------------------------

    def close_window(self, *args, **keywords):
        """
        windowを閉じるコマンド
        """

        if 'window_name' not in keywords:
            return

        window_name = keywords['window_name']

        if cmds.window(window_name, exists=True):
            cmds.deleteUI(window_name, window=True)

    # ------------------------------------------------------------

    def show_info_window(self, *args, **keywords):
        """
        情報ボタン押したときの挙動
        """

        if 'item_param' not in keywords:
            return

        item_param = keywords['item_param']
        check_answer_info = item_param.func(True)

        self.show_checker_option_window(
            item_param.description,
            check_answer_info.check_target_item_list
        )

    # ------------------------------------------------------------

    def show_target_list_window(self, *args, **keywords):
        """
        リストボタンを押したときの挙動
        """

        if 'item_param' not in keywords:
            return

        item_param = keywords['item_param']
        item_param.func(True)

        self.show_checker_option_window(
            item_param.check_answer_info.error_message,
            item_param.check_answer_info.invalid_item_list
        )

    # ------------------------------------------------------------

    def select_button_cmd(self, *args, **keywords):
        """
        選択ボタンを押した挙動
        """

        if 'item_param' not in keywords:
            return

        item_param = keywords['item_param']
        if item_param.check_answer_info.invalid_item_list:
            select_target = cmds.ls(item_param.check_answer_info.invalid_item_list)
            cmds.select(select_target)

    # ------------------------------------------------------------

    def revise_button_cmd(self, *args, **keywords):
        """
        修正ボタンを押した挙動
        """

        if 'item_param' not in keywords:
            return

        item_param = keywords['item_param']
        is_success, result_str = item_param.func(False, True)

        cmds.confirmDialog(title='完了', message=result_str, defaultButton='OK')

        if self.log_field:
            cmds.scrollField(self.log_field, e=True, tx=result_str)

        if is_success:
            cmds.button(item_param.ui_info['individual_check'], e=True, bgc=[0, 0, 1])
            if item_param.is_log_button_view:
                cmds.button(item_param.ui_info['log'], e=True, enable=False)
            if item_param.is_list_button_view:
                cmds.button(item_param.ui_info['list'], e=True, enable=False)
            if item_param.is_select_button_view:
                cmds.button(item_param.ui_info['select'], e=True, enable=False)
            if item_param.is_correction_button_view:
                cmds.button(item_param.ui_info['correction'], e=True, enable=False)

            # 全ての項目の再チェックを行う
            self.all_exec()

    # ------------------------------------------------------------

    def create_ui_batch_check_part(self):
        """
        ui フォルダ指定チェック部分作成
        """

        container = cmds.frameLayout(l='フォルダ指定チェック', cll=True, cl=False, mh=self.frame_margin, mw=self.frame_margin, bv=True)

        form = cmds.formLayout()

        ui_target_dir_path_column = cmds.rowLayout(numberOfColumns=2, adjustableColumn=1)
        self.ui_target_dir_path = cmds.textFieldGrp(
            l='対象フォルダ', columnAlign=[1, 'left'], columnWidth=[(1, 80)], text=self.dir_path,
            adjustableColumn=2, changeCommand=partial(self._save_setting))
        cmds.button(l='選択', w=40, h=20, command=partial(self._show_path_dialog, self.ui_target_dir_path, 'dir'))
        cmds.setParent('..')

        self.ui_target_filter = cmds.textFieldGrp(
            l='フィルタ(含む)', cal=[1, 'left'], cw=[(1, 80)], adj=2, text=self.file_name_filter)

        self.ui_target_ignore_filter = cmds.textFieldGrp(
            l='フィルタ(含まない)', cal=[1, 'left'], cw=[(1, 80)], adj=2, text=self.file_name_ignore_filter)

        info_text = cmds.text(align='left', l='※フィルタはカンマ( , )区切りで複数指定できます')

        ui_log_save_dir_column = cmds.rowLayout(numberOfColumns=2, adjustableColumn=1)
        self.ui_log_save_dir = cmds.textFieldGrp(
            l='ログ保存場所', columnAlign=[1, 'left'], columnWidth=[(1, 80)], text=self.log_save_dir_path,
            adjustableColumn=2, changeCommand=partial(self._save_setting))
        cmds.button(l='選択', w=40, h=20, command=partial(self._show_path_dialog, self.ui_log_save_dir, 'dir'))
        cmds.setParent('..')

        caution_text = cmds.text(align='left', l='※ログの保存先が設定されていない場合、自動的にドキュメント直下に保存されます')

        self.ui_is_exec_child_dir_checkbox = cmds.checkBox(
            l='下層フォルダも含む', value=self.is_exec_child_dir)

        exec_button = cmds.button(l='実行', c=partial(self.batch_cmd))

        cmds.formLayout(
            form, e=True,
            attachForm=[
                (ui_target_dir_path_column, 'top', 5),
                (ui_target_dir_path_column, 'left', 5),
                (ui_target_dir_path_column, 'right', 5),
                (self.ui_target_filter, 'left', 5),
                (self.ui_target_filter, 'right', 0),
                (self.ui_target_ignore_filter, 'left', 5),
                (self.ui_target_ignore_filter, 'right', 0),
                (info_text, 'left', 90),
                (info_text, 'right', 5),
                (ui_log_save_dir_column, 'left', 5),
                (ui_log_save_dir_column, 'right', 5),
                (caution_text, 'left', 90),
                (caution_text, 'right', 5),
                (self.ui_is_exec_child_dir_checkbox, 'left', 5),
                (self.ui_is_exec_child_dir_checkbox, 'right', 5),
                (exec_button, 'left', 5),
                (exec_button, 'right', 5),
                (exec_button, 'bottom', 5)
            ],
            attachControl=[
                (ui_target_dir_path_column, 'bottom', 5, self.ui_target_filter),
                (self.ui_target_filter, 'bottom', 5, self.ui_target_ignore_filter),
                (self.ui_target_ignore_filter, 'bottom', 0, info_text),
                (info_text, 'bottom', 5, ui_log_save_dir_column),
                (ui_log_save_dir_column, 'bottom', 0, caution_text),
                (caution_text, 'bottom', 5, self.ui_is_exec_child_dir_checkbox),
                (self.ui_is_exec_child_dir_checkbox, 'bottom', 5, exec_button),
            ]
        )

        cmds.setParent('..')
        cmds.setParent('..')

        return container

    # ------------------------------------------------------------

    def _show_path_dialog(self, target_text_field, mode='file', *args):
        """
        ファイルorフォルダ選択ダイアログを表示
        """
        file_mode_value = 1
        dialog_caption = '対象のファイルを選択してください'
        file_filter = "*.ma"
        if mode == 'dir':
            file_mode_value = 3
            dialog_caption = '対象のフォルダを選択してください'
            file_filter = 'All Files (*.*)'

        result = cmds.fileDialog2(
            caption=dialog_caption,
            fileFilter=file_filter, dialogStyle=2, fileMode=file_mode_value)

        if result:
            cmds.textFieldGrp(target_text_field, e=True, tx=result[0])
            self._set_ui_setting()

    # ------------------------------------------------------------

    def create_ui_extra_part(self):
        """
        ui 特殊処理部分作成
        基本的には空のcolumnLayoutが入っているだけ
        利用するときにはoverrideして使用する
        """

        container = cmds.columnLayout()

        cmds.setParent('..')

        return container

    # ------------------------------------------------------------

    def create_ui_log_part(self):
        """
        ui log部分作成
        """

        container = cmds.frameLayout(l='ログ', cll=True, cl=False, mh=self.frame_margin, mw=self.frame_margin, bv=True)
        form = cmds.formLayout()

        self.log_field = cmds.scrollField(h=100)
        log_clear_button = cmds.button(l='ログクリア', c=partial(self.clear_log))

        cmds.formLayout(
            form, e=True,
            attachForm=[
                (self.log_field, 'top', 0),
                (self.log_field, 'left', 0),
                (self.log_field, 'right', 0),
                (log_clear_button, 'left', 0),
                (log_clear_button, 'right', 0),
                (log_clear_button, 'bottom', 0)
            ],
            attachControl=[
                (self.log_field, 'bottom', 5, log_clear_button),
            ],
            attachNone=[
                (log_clear_button, 'top'),
            ]
        )
        cmds.setParent('..')

        return container

    # ------------------------------------------------------------

    def exec_cmd_initialize(self):
        """
        関数実行前処理
        基本的に空で、オーバーライドして実行する
        """

        return True

    # ------------------------------------------------------------

    def exec_cmd(self, *args, **keywords):
        """
        渡された関数を実行する
        argsまたはkeywordがあればそれも利用する
        buttonコマンドから渡される*argsの最終引数は利用不可(cmdsの仕様)
        """

        if not self.exec_cmd_initialize():
            if self.log_field:
                cmds.scrollField(self.log_field, e=True, tx='キャラの情報が取得できませんでした\nチェッカーが起動できません')
            return None

        if 'item_param' not in keywords:
            return None

        item_param = keywords['item_param']
        func = item_param.func

        if item_param.is_internal and not self.is_internal:
            return None

        if item_param.args:
            func_args = item_param.args
            check_answer_info = func(False, func_args)
        else:
            check_answer_info = func()

        item_param.check_answer_info = check_answer_info

        if not self.is_batch_exec:

            if not check_answer_info.result:

                cmds.button(
                    item_param.ui_info['individual_check'], e=True,
                    bgc=item_param.ui_button_for_error_bcg)
                if item_param.is_log_button_view:
                    cmds.button(item_param.ui_info['log'], e=True, enable=True)
                if item_param.is_list_button_view:
                    cmds.button(item_param.ui_info['list'], e=True, enable=True)
                if item_param.is_select_button_view:
                    cmds.button(item_param.ui_info['select'], e=True, enable=True)
                if item_param.is_correction_button_view:
                    cmds.button(item_param.ui_info['correction'], e=True, enable=True)

            else:
                cmds.button(item_param.ui_info['individual_check'], e=True, bgc=[0, 0, 1])
                if item_param.is_log_button_view:
                    cmds.button(item_param.ui_info['log'], e=True, enable=False)
                if item_param.is_list_button_view:
                    cmds.button(item_param.ui_info['list'], e=True, enable=False)
                if item_param.is_select_button_view:
                    cmds.button(item_param.ui_info['select'], e=True, enable=False)
                if item_param.is_correction_button_view:
                    cmds.button(item_param.ui_info['correction'], e=True, enable=False)

        # バッチ処理
        else:

            pass

        if self.log_field:
            cmds.scrollField(self.log_field, e=True, tx='チェックが完了しました')

        return check_answer_info

    # ------------------------------------------------------------

    def batch_cmd(self, *args, **keywords):
        """
        バッチ前処理
        """

        self.dir_path = cmds.textFieldGrp(self.ui_target_dir_path, q=True, text=True)
        self.file_name_filter = cmds.textFieldGrp(self.ui_target_filter, q=True, text=True)
        self.file_name_ignore_filter = cmds.textFieldGrp(self.ui_target_ignore_filter, q=True, text=True)
        self.is_exec_child_dir = cmds.checkBox(self.ui_is_exec_child_dir_checkbox, q=True, v=True)
        self.log_save_dir_path = cmds.textFieldGrp(self.ui_log_save_dir, q=True, text=True)

        if not os.path.exists(self.dir_path):
            cmds.warning('対象フォルダが空、もしくは見つかりません')
            return

        # checker_ui_referer.py内ではself._save_setting()は空
        self._save_setting()

        base_utility.simple_batch.execute(
            self.batch_cmd_str,
            True
        )

    # ------------------------------------------------------------

    def batch_exec(self):
        """
        バッチ処理
        """

        self.batch_exec_initialize()

        self._load_setting()

        self.is_batch_exec = True

        if not os.path.exists(self.dir_path):
            return

        target_files = []

        # 下層フォルダも処理を行うか
        if self.is_exec_child_dir:
            target_files = self.find_all_files(self.dir_path)
        else:
            target_files = glob.glob(self.dir_path + '/*')

        target_param_list = []

        for target_file in target_files:

            # 対象をmaに絞る
            if not target_file.endswith('.ma'):
                continue

            # 含むに該当しなかったら戻す
            non_hit_flg = False
            filter_list = self.file_name_filter.split(',')
            for filter_name in filter_list:

                if filter_name == '':
                    continue

                filter_name = filter_name.strip()
                if target_file.find(filter_name) == -1:
                    non_hit_flg = True
                    break

            if non_hit_flg:
                continue

            # 含まないに該当したら戻す
            hit_ignore_flg = False
            ignore_filter_list = self.file_name_ignore_filter.split(',')
            for ignore_filter_name in ignore_filter_list:

                if ignore_filter_name == '':
                    continue

                ignore_filter_name = ignore_filter_name.strip()
                if target_file.find(ignore_filter_name) > -1:
                    hit_ignore_flg = True
                    break

            if hit_ignore_flg:
                continue

            target_param = {
                'file_name': target_file,
                'answer_info_list': []
            }

            cmds.file(target_file, o=True, f=True, returnNewNodes=True)
            for check_item_param in self.check_item_param_list:
                check_answer_info = self.exec_cmd(item_param=check_item_param)
                if check_answer_info is None:
                    continue

                if check_answer_info.result is True:
                    continue

                target_param['answer_info_list'].append(check_answer_info)

            if target_param['answer_info_list']:
                target_param_list.append(target_param)

        target_dir_path = ''

        if self.log_save_dir_path and os.path.exists(self.log_save_dir_path):

            if os.path.isdir(self.log_save_dir_path):
                target_dir_path = self.log_save_dir_path
            else:
                target_dir_path = os.path.dirname(self.log_save_dir_path)

        else:

            target_dir_path = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + "\\Documents"

            print('--------------------')
            print(target_dir_path.encode('utf_8'))
            print('--------------------')

        now_data = datetime.datetime.today()
        now_data = now_data.strftime("%Y%m%d%H%M%S")
        path_w = target_dir_path + '\\' + self.tool_name + now_data + '_log.txt'

        with open(path_w, mode='w') as f:

            if sys.version_info.major == 2:

                f.write('Target Path        : ')
                f.write(self.dir_path.encode('utf-8'))
                f.write('\r\nFilter             : ')
                f.write(self.file_name_filter.encode('utf_8'))
                f.write('\r\nIgnore Filter      : ')
                f.write(self.file_name_ignore_filter.encode('utf_8'))
                f.write('\r\nIs Exec Child Path : ')
                f.write(str(self.is_exec_child_dir))
                f.write('\r\n\r\n=======================')

                for target_param in target_param_list:

                    f.write('\r\n\r\n--------------------\r\n\r\n')
                    file_name = target_param['file_name']
                    f.write(file_name)
                    if not target_param['answer_info_list']:

                        f.write('\r\n-----\r\n')
                        f.write('検出中にエラーが発生したため中断しました'.encode('utf_8'))
                        continue

                    answer_info_list = target_param['answer_info_list']
                    for answer_info in answer_info_list:

                        f.write('\r\n-----\r\n')
                        f.write(answer_info.error_message.encode('utf_8'))
                        f.write('\r\nチェック対象　: '.encode('utf_8'))
                        f.write(', '.join(answer_info.check_target_item_list))
                        f.write('\r\n検出対象　　　: '.encode('utf_8'))
                        f.write(', '.join(answer_info.invalid_item_list))

            else:

                f.write('Target Path        : ')
                f.write(self.dir_path)
                f.write('\r\nFilter             : ')
                f.write(self.file_name_filter)
                f.write('\r\nIgnore Filter      : ')
                f.write(self.file_name_ignore_filter)
                f.write('\r\nIs Exec Child Path : ')
                f.write(str(self.is_exec_child_dir))
                f.write('\r\n\r\n=======================')

                f.write(' / '.join(target_files))
                f.write('\r\n\r\n')

                for target_param in target_param_list:

                    f.write('\r\n\r\n--------------------\r\n\r\n')
                    file_name = target_param['file_name']
                    f.write(file_name)
                    if not target_param['answer_info_list']:

                        f.write('\r\n-----\r\n')
                        f.write('検出中にエラーが発生したため中断しました')
                        continue

                    answer_info_list = target_param['answer_info_list']
                    for answer_info in answer_info_list:

                        f.write('\r\n-----\r\n')
                        f.write(answer_info.error_message)
                        f.write('\r\nチェック対象　: ')
                        f.write(', '.join(answer_info.check_target_item_list))
                        f.write('\r\n検出対象　　　: ')
                        f.write(', '.join(answer_info.invalid_item_list))

        os.system(path_w)

    # ------------------------------------------------------------

    def find_all_files(self, directory):
        """
        directory以下のファイルをすべて取得する
            :param directory: 自身以下の階層を取得したいディレクトリファイル
        """

        for root, dirs, files in os.walk(directory):
            yield root
            for file in files:
                yield os.path.join(root, file)

    # ------------------------------------------------------------

    def batch_exec_initialize(self):
        """
        バッチ処理前に実行される前処理
        継承先で書く必要がある
        """

        pass
