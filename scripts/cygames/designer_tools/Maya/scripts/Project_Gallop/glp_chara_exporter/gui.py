# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os
import itertools
from functools import partial
from datetime import datetime

import maya.cmds as cmds
from maya import utils

from ..base_common import classes as base_class
from ..base_common import utility as base_utility

from ..glp_common.classes.info import chara_info
from ..glp_common.utility import batch

from . import constants
from . import chara_exporter

try:
    # maya 2022-
    from builtins import str
    from builtins import object
    from importlib import reload
except Exception:
    pass

reload(base_class)
reload(base_utility)
reload(chara_info)
reload(batch)
reload(constants)
reload(chara_exporter)


class MainWindow(object):

    def __init__(self):

        self.window_name = constants.TOOL_NAME + 'Win'

        # 設定関連
        self.setting = None

        # UI関連
        self.ui_show_subprocess_window = None
        self.ui_show_in_explorer = None
        self.ui_keep_temp_file = None
        self.ui_is_ascii = None
        self.ui_is_icon_model = None
        self.ui_output_log = None
        self.ui_export_base_setting = None
        self.ui_asset_num_menu = None
        self.ui_general_cloth_export_option = None
        self.ui_general_cloth_additional_option = None
        self.ui_allow_all_body_shape = None

        self.ui_batch_folder_path = None
        self.ui_logframe = None

        self.ui_updating = False

        # 初期化フラグ
        self.init = False

    def initialize(self):

        self.init = False

        self.logger = base_class.logger.Logger()

        self.setting = base_class.setting.Setting(constants.TOOL_NAME)

        self.init = True

        self.general_cloth_export_property_list = [
            {
                'label': '身長',
                'ui': None,
                'dafault_value': True,
                'is_mini': False,
                'param_list': [
                    {'label': 'SS', 'index': 0, 'ui': None, 'dafault_value': True},
                    {'label': 'M', 'index': 1, 'ui': None, 'dafault_value': True},
                    {'label': 'L', 'index': 2, 'ui': None, 'dafault_value': True},
                    {'label': 'LL', 'index': 3, 'ui': None, 'dafault_value': True},
                ]
            },
            {
                'label': '体型',
                'ui': None,
                'dafault_value': True,
                'is_mini': False,
                'param_list': [
                    {'label': '通常', 'index': 0, 'ui': None, 'dafault_value': True},
                    {'label': '細い', 'index': 1, 'ui': None, 'dafault_value': True},
                    {'label': '太い', 'index': 2, 'ui': None, 'dafault_value': True},
                ]
            },
            {
                'label': 'バスト',
                'ui': None,
                'dafault_value': True,
                'is_mini': True,
                'param_list': [
                    {'label': 'SS', 'index': 0, 'mini_index': 0, 'ui': None, 'dafault_value': True},
                    {'label': 'S', 'index': 1, 'mini_index': 0, 'ui': None, 'dafault_value': True},
                    {'label': 'M', 'index': 2, 'mini_index': 1, 'ui': None, 'dafault_value': True},
                    {'label': 'L', 'index': 3, 'mini_index': 2, 'ui': None, 'dafault_value': True},
                    {'label': 'LL', 'index': 4, 'mini_index': 2, 'ui': None, 'dafault_value': True},
                ]
            },
        ]

        self.general_cloth_export_option_preset_list = [
            {
                'label': '全てON',
                'command': partial(self.__set_general_cloth_option_ui, 'all', True),
                'ui': None
            },
            {
                'label': '全てOFF',
                'command': partial(self.__set_general_cloth_option_ui, 'all', False),
                'ui': None
            },
            {
                'label': '1001体型のみ',
                'command': partial(self.__set_general_cloth_option_ui, 'only', True, [[1], [0], [2]]),
                'ui': None
            }
        ]

    def create_ui(self):

        self.initialize()

        if not self.init:
            return

        width = 450
        height = 800

        base_utility.ui.window.remove_same_id_window(self.window_name)

        window = cmds.window(
            self.window_name, title=constants.TOOL_NAME + '  ' + constants.TOOL_VERSION,
            widthHeight=(width, height),
            s=1,
            mnb=True,
            mxb=False,
            rtf=True,
            cc=self.save_setting
        )

        form = cmds.formLayout()

        common_setting_frame = cmds.frameLayout(l=u'共通設定', cll=1, cl=0, bv=1, mw=10, mh=5)
        cmds.columnLayout(adjustableColumn=True, rs=4)

        self.ui_show_subprocess_window = base_class.ui.check_box.CheckBox(
            '出力ウィンドウを表示する', False)

        self.ui_show_in_explorer = base_class.ui.check_box.CheckBox(
            '出力後エクスプローラを開く', False)

        self.ui_keep_temp_file = base_class.ui.check_box.CheckBox(
            '一時ファイルを保持', False)

        self.ui_output_log = base_class.ui.check_box.CheckBox(
            '出力後ログファイル作成、閲覧', False)

        self.ui_is_ascii = base_class.ui.check_box.CheckBox(
            'ASCIIフォーマットで出力', False)

        self.ui_is_icon_model = base_class.ui.check_box.CheckBox(
            'アイコンモデルの出力', False)

        self.ui_export_base_setting = base_class.ui.check_box.CheckBox('エクスポートする体型を選択する', False)
        self.ui_export_base_setting.set_change_function(self.__set_general_cloth_option_ui_enable)

        self.__create_general_cloth_option_ui()

        cmds.setParent('..')
        cmds.setParent('..')

        export_file_frame = cmds.frameLayout(l=u'通常エクスポート', cll=1, cl=0, bv=1, mw=10, mh=10)
        cmds.columnLayout(adjustableColumn=True, rs=4)

        base_class.ui.button.Button(u'ファイル名から判定してエクスポート', self.export_data, 'current')

        cmds.setParent('..')
        cmds.setParent('..')

        export_folder_frame = cmds.frameLayout(l=u'フォルダ指定エクスポート', cll=1, cl=1,
                         bv=1, mw=10, mh=10, visible=True)
        self.ui_batch_folder_path = base_class.ui.data_selector.DataSelector(
            '対象フォルダ', '', False, True
        )

        base_class.ui.button.Button('フォルダ指定出力', self.export_data, 'folder')

        cmds.setParent('..')

        log_frame = cmds.frameLayout(l='ログ', cll=1, cl=0, bv=1, mw=10, mh=10)
        self.ui_logframe = cmds.scrollField(editable=False, wordWrap=True)
        cmds.scrollField(self.ui_logframe, e=True, height=140)
        base_class.ui.button.Button('クリア', self.__clear_log)

        cmds.setParent('..')

        cmds.formLayout(
            form, e=True,
            attachForm=[
                (common_setting_frame, 'top', 0),
                (common_setting_frame, 'left', 0),
                (common_setting_frame, 'right', 0),
                (export_file_frame, 'left', 0),
                (export_file_frame, 'right', 0),
                (export_folder_frame, 'left', 0),
                (export_folder_frame, 'right', 0),
                (log_frame, 'left', 0),
                (log_frame, 'right', 0),
                (log_frame, 'bottom', 0),
            ],
            attachControl=[
                (export_file_frame, 'top', 0, common_setting_frame),
                (export_folder_frame, 'top', 0, export_file_frame),
                (log_frame, 'top', 0, export_folder_frame),
            ]
        )

        cmds.setParent('..')

        cmds.showWindow(self.window_name)

        self.load_setting()

        self.__reset_general_cloth_option_ui()

        cmds.scriptJob(event=['SceneOpened', self.__reset_general_cloth_option_ui], protected=True, parent=window)

    def __create_general_cloth_option_ui(self):
        """汎用衣装オプションUIを作成する
        """

        self.ui_general_cloth_export_option = cmds.frameLayout(l=u'エクスポートする体型 ※汎用衣装のみ', cll=1, cl=0, bv=1, mw=10, mh=10)

        # アセット番号のプルダウン群
        self.ui_asset_num_menu = cmds.optionMenu(label='対象の体型', cc=self.__set_general_cloth_option_for_model_num_menu)
        self.__set_model_num_menu()

        # チェックボックス群
        for _property in self.general_cloth_export_property_list:

            cmds.rowColumnLayout(numberOfRows=1)

            _property['ui'] = cmds.checkBox(
                l=_property['label'], width=80, value=_property['dafault_value'],
                changeCommand=partial(self.__set_param_checkbox_enable, _property))

            for param in _property['param_list']:
                param['ui'] = cmds.checkBox(label=param['label'], width=60, value=param['dafault_value'])

            cmds.setParent('..')

        # プリセットボタン群
        cmds.rowColumnLayout(numberOfRows=1)
        for preset in self.general_cloth_export_option_preset_list:
            preset['ui'] = cmds.button(l=preset['label'], command=preset['command'], width=80)
        cmds.setParent('..')

        self.ui_general_cloth_additional_option = cmds.frameLayout(l=u'追加設定', cll=1, cl=1, bv=1, mw=10, mh=10)
        self.ui_allow_all_body_shape = base_class.ui.check_box.CheckBox('未実装体型のエクスポートを許可する', False)
        cmds.setParent('..')

        cmds.setParent('..')

    def __set_general_cloth_option_ui_enable(self, *args):
        """汎用衣装オプションUIの有効/無効設定
        """

        if self.ui_export_base_setting is None or self.ui_general_cloth_export_option is None:
            return

        value = self.ui_export_base_setting.get_value()
        cmds.frameLayout(self.ui_general_cloth_export_option, e=True, enable=value)

    def __set_param_checkbox_enable(self, _property, *args):
        """カテゴリー以下の有効/無効設定
        """

        value = cmds.checkBox(_property['ui'], q=True, value=True)
        for param in _property['param_list']:
            cmds.checkBox(param['ui'], e=True, enable=value)

    def __reset_general_cloth_option_ui(self, *args):
        """汎用衣装オプションUIの状態をリセットする
        """

        is_mini = False

        _chara_info = chara_info.CharaInfo()
        _chara_info.create_info()
        if _chara_info.exists:
            is_mini = _chara_info.is_mini

        if _chara_info.is_common_body:
            cmds.checkBox(self.ui_export_base_setting.ui_check_box_id, e=True, enable=True)
        else:
            self.ui_export_base_setting.set_value(False)
            cmds.checkBox(self.ui_export_base_setting.ui_check_box_id, e=True, enable=False)

        self.__set_general_cloth_option_ui_enable()

        for _property in self.general_cloth_export_property_list:
            property_value = True
            if is_mini and not _property['is_mini']:
                property_value = False
            cmds.checkBox(_property['ui'], e=True, enable=property_value)
            use_mini_index = is_mini and _property['is_mini']
            for param in _property['param_list']:
                label = param['label'] + ' ({})'.format(param['index'] if not use_mini_index else param['mini_index'])
                cmds.checkBox(param['ui'], e=True, label=label)
                cmds.checkBox(param['ui'], e=True, enable=property_value)

        self.__set_model_num_menu()

    def __set_model_num_menu(self):
        """アセットの差分IDメニューをセットする
        """

        menu_items = cmds.optionMenu(self.ui_asset_num_menu, q=True, itemListLong=True)
        if menu_items:
            cmds.deleteUI(menu_items)

        _chara_info = chara_info.CharaInfo()
        _chara_info.create_info()

        if not _chara_info.exists:
            return

        model_num_list = _chara_info.part_info.model_num_list
        for model_num in model_num_list:
            cmds.menuItem(label=model_num, parent=self.ui_asset_num_menu)

    def __set_general_cloth_option_for_model_num_menu(self, *args):
        """アセットの差分IDメニューから汎用衣装オプションを設定する
        """

        if self.ui_asset_num_menu is None:
            return

        model_num = cmds.optionMenu(self.ui_asset_num_menu, q=True, v=True)
        model_num_list = model_num.split('_')

        target_list = []
        for model_num in model_num_list:
            target_list.append([int(model_num)])

        if not target_list:
            return

        self.__set_general_cloth_option_ui('only', True, target_list)

    def __set_general_cloth_option_ui(self, change_type, status, target_list=None, *args):
        """target_listの対象に対応した汎用衣装オプション内の各checkBoxの状態を設定

        Args:
            change_type (string): 変更する設定 all=全てのチェックボックス only=特定のチェックボックス
            status (string)): 設定対象の値
            target_list (list, optional): 変更する対象のindexリスト。Defaults to None.
                                          target_listの例: [[0], [1], [2, 3]] -> 0_1_2, 0_1_3の対応するチェックボックス
        """

        is_mini = False

        _chara_info = chara_info.CharaInfo()
        _chara_info.create_info()
        if _chara_info.exists:
            is_mini = _chara_info.is_mini

        if change_type == 'all' or change_type == 'only':

            for _property in self.general_cloth_export_property_list:

                if is_mini and not _property['is_mini']:
                    continue

                tmp_status = status
                if change_type == 'only':
                    tmp_status = not status

                # ONにする時のみ再設定
                if tmp_status:
                    cmds.checkBox(_property['ui'], e=True, value=True)

                self.__set_param_checkbox_enable(_property)

                for param in _property['param_list']:

                    cmds.checkBox(param['ui'], e=True, value=tmp_status)

        if change_type == 'only':

            count = 0
            for _property in self.general_cloth_export_property_list:

                if is_mini and not _property['is_mini']:
                    continue

                if len(target_list) <= count or not target_list[count]:
                    continue

                for param in _property['param_list']:

                    index = param['index']
                    if is_mini and _property['is_mini']:
                        index = param['mini_index']

                    if index not in target_list[count]:
                        continue

                    if cmds.checkBox(_property['ui'], q=True, value=True) != status:
                        cmds.checkBox(_property['ui'], e=True, value=status)
                        self.__set_param_checkbox_enable(_property)

                    cmds.checkBox(param['ui'], e=True, value=status)

                count += 1

    def __create_export_bodydiff_id_list(self):
        """汎用衣装エクスポートを行う体型差分IDリストの作成

        Returns:
            list: 汎用衣装エクスポートを行う体型差分IDリスト
        """

        export_bodydiff_id_list = []

        _chara_info = chara_info.CharaInfo()
        _chara_info.create_info()
        if not _chara_info.exists or not _chara_info.is_common_body:
            return []

        if not self.ui_export_base_setting.get_value():
            return []

        is_mini = _chara_info.is_mini

        export_bodydiff_ids_list = []
        for _property in self.general_cloth_export_property_list:

            if is_mini and not _property['is_mini']:
                continue

            export_ids = []
            property_ui_value = cmds.checkBox(_property['ui'], q=True, value=True)

            for param in _property['param_list']:

                param_ui_value = cmds.checkBox(param['ui'], q=True, value=True)
                if property_ui_value is True and param_ui_value is False:
                    continue

                index = param['index']
                if is_mini:
                    index = param['mini_index']

                if index not in export_ids:
                    export_ids.append(index)

            export_bodydiff_ids_list.append(export_ids)

        export_bodydiff_id_set_list = [id_combi for id_combi in itertools.product(*export_bodydiff_ids_list)]
        for exported_bodydiff_id_set in export_bodydiff_id_set_list:
            export_bodydiff_id_list.append('_' + '_'.join([str(exported_id) for exported_id in exported_bodydiff_id_set]))

        return export_bodydiff_id_list

    def __get_body_shape_check_enabled(self):
        """未実装体型のチェックを行うかを返す

        Returns:
            bool: 未実装体型のチェックを行うか
        """

        return not (self.ui_export_base_setting.get_value() and self.ui_allow_all_body_shape.get_value())

    def __clear_log(self):

        cmds.scrollField(self.ui_logframe, e=True, text='')

    def __print_log(self):

        if cmds.scrollField(self.ui_logframe, ex=True):
            cmds.scrollField(self.ui_logframe, e=True, cl=True)
            # スクロールさせるため、テキストを挿入フラグで指定
            cmds.scrollField(self.ui_logframe, e=True, it=self.logger.get_log())

    def on_complete(self, success):

        message = '出力が完了しました' if success else '出力中にエラーが発生しました'
        message_and_time = '{} [{}]\n'.format(message, datetime.now().strftime('%y-%m-%d %H:%M:%S'))

        self.logger.write_log()
        self.logger.write_log(message_and_time)

        def post_process():
            print(end='{}: {}\n'.format(constants.TOOL_NAME, message_and_time))
            cmds.inViewMessage(amg='{}: <hl>{}</hl>'.format(constants.TOOL_NAME, message), pos='topCenter', fade=True)
            self.__print_log()

        # メインスレッドではないのでMayaのアイドル状態まで待機してから実行する
        utils.executeDeferred(post_process)

    def export_data(self, input_type):

        self.save_setting()

        self.logger.clear_log()

        self.logger.print_log = False
        self.logger.encode_type = None

        export_settings = None

        if input_type == 'current':
            export_settings = self.export_current()
        elif input_type == 'folder':
            export_settings = self.export_folder()

        if not export_settings:
            self.__print_log()
            return

        self.__clear_log()

        print(end='{}: {} [{}]\n'.format(constants.TOOL_NAME, '出力を開始します', datetime.now().strftime('%y-%m-%d %H:%M:%S')))
        cmds.inViewMessage(amg='{}: <hl>{}</hl>'.format(constants.TOOL_NAME, '出力を開始します'), pos='topCenter', fade=True)

        main_module = '{}.{}'.format(__package__, 'main')
        options = batch.get_options_from_dict(export_settings)
        show_window = self.ui_show_subprocess_window.get_value()

        batch.exec_mayapy(main_module, options, on_complete=self.on_complete, show_window=show_window)

    def export_current(self):

        current_path = cmds.file(q=True, sn=True)

        this_exporter = chara_exporter.CharaExporter(current_path)
        this_exporter.logger = self.logger

        this_exporter.export_base_setting = self.ui_export_base_setting.get_value()

        export_bodydiff_id_list = self.__create_export_bodydiff_id_list()
        this_exporter.export_bodydiff_id_list = export_bodydiff_id_list

        this_exporter.body_shape_check_enabled = self.__get_body_shape_check_enabled()

        if not this_exporter.check_data():
            base_utility.ui.dialog.open_ok(
                '',
                u'{0}'.format(self.logger.get_log()),
                self.window_name
            )
            return None

        this_info = self.logger.get_log()

        if self.ui_is_icon_model.get_value():
            this_info += u'\n\n{0}\nアイコン撮影用モデルを出力します。このモデルは実装できません。\n{0}'.format('!' * 40)

        file_modified = cmds.file(q=True, modified=True)

        if file_modified:

            this_info += \
                u'\n\n{0}\nシーンが保存されていませんが出力しますか？\n(最後に保存したシーンで出力されます)\n{0}'\
                .format('!' * 40)

        else:
            this_info += u'\n\n上記設定で出力しますか?'

        if not base_utility.ui.dialog.open_ok_cancel(u'確認', this_info, self.window_name):
            self.logger.write_log(u'\n出力をキャンセルしました')
            return None

        return {
            'target_files': [current_path],
            'target_objects': [],
            'show_in_exprorer': self.ui_show_in_explorer.get_value(),
            'keep_temp_file': self.ui_keep_temp_file.get_value(),
            'output_log': self.ui_output_log.get_value(),
            'is_ascii': self.ui_is_ascii.get_value(),
            'is_icon_model': self.ui_is_icon_model.get_value(),
            'export_base_setting': self.ui_export_base_setting.get_value(),
            'export_bodydiff_ids': export_bodydiff_id_list,
            'body_shape_check_enabled': self.__get_body_shape_check_enabled(),
        }

    def export_folder(self):

        target_folder_path = self.ui_batch_folder_path.get_path()

        if not os.path.isdir(target_folder_path):
            base_utility.ui.dialog.open_ok('', '対象フォルダが存在しません')
            return None

        target_file_path_list = self.ui_batch_folder_path.get_data_path_list()
        if len(target_file_path_list) == 0:
            base_utility.ui.dialog.open_ok('', '対象ファイルが見つかりませんでした')
            return None

        dialog_info = u'以下のファイルが対象となります。出力しますか?'

        if not base_utility.ui.dialog.open_ok_cancel_with_scroll('', dialog_info, target_file_path_list, self.window_name):
            self.logger.write_log(u'出力をキャンセルしました')
            return None

        export_bodydiff_id_list = self.__create_export_bodydiff_id_list()

        return {
            'target_files': target_file_path_list,
            'target_objects': [],
            'show_in_exprorer': self.ui_show_in_explorer.get_value(),
            'keep_temp_file': self.ui_keep_temp_file.get_value(),
            'output_log': self.ui_output_log.get_value(),
            'is_ascii': self.ui_is_ascii.get_value(),
            'is_icon_model': self.ui_is_icon_model.get_value(),
            'export_base_setting': self.ui_export_base_setting.get_value(),
            'export_bodydiff_ids': export_bodydiff_id_list,
            'body_shape_check_enabled': self.__get_body_shape_check_enabled(),
        }

    def save_setting(self):

        self.ui_show_subprocess_window.save_setting(self.setting, 'ShowSubprocessWindow')
        self.ui_show_in_explorer.save_setting(self.setting, 'ShowInExplorer')
        self.ui_keep_temp_file.save_setting(self.setting, 'KeepTempFile')
        self.ui_output_log.save_setting(self.setting, 'OutputLog')
        self.ui_is_ascii.save_setting(self.setting, 'IsAscii')
        self.ui_is_icon_model.save_setting(self.setting, 'IsIconModel')
        self.ui_export_base_setting.save_setting(self.setting, 'ExportBaseSetting')
        self.ui_batch_folder_path.save_setting(self.setting, 'BatchFolderPath')

    def load_setting(self):

        self.ui_show_subprocess_window.load_setting(self.setting, 'ShowSubprocessWindow')
        self.ui_show_in_explorer.load_setting(self.setting, 'ShowInExplorer')
        self.ui_keep_temp_file.load_setting(self.setting, 'KeepTempFile')
        self.ui_output_log.load_setting(self.setting, 'OutputLog')
        self.ui_is_ascii.load_setting(self.setting, 'IsAscii')
        self.ui_is_icon_model.load_setting(self.setting, 'IsIconModel')
        self.ui_export_base_setting.load_setting(self.setting, 'ExportBaseSetting')
        self.ui_batch_folder_path.load_setting(self.setting, 'BatchFolderPath')
