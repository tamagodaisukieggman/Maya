# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
    from importlib import reload
except:
    pass

import os
import subprocess
import sys
import traceback

import maya.cmds as cmds

from .. import base_common
from ..base_common import classes as base_class
from ..base_common import utility as base_utility

from .utility import normal_to_uv as utility_normal_to_uv

from . import chara_exporter

reload(base_common)
reload(utility_normal_to_uv)
reload(chara_exporter)


# ==================================================
def main():

    this_main = Main()
    this_main.create_ui()


# ==================================================
def batch_export():

    this_main = Main()
    this_main.batch_export()


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Main(object):

    # ==================================================
    def __init__(self):

        self.tool_version = '20091801'
        self.tool_name = 'PriariCharaExporter'

        self.window_name = self.tool_name + 'Win'

        # スクリプトのパス関連
        self.script_file_path = None
        self.script_dir_path = None

        self.export_flag_file_path = None
        self.export_log_file_path = None

        # 設定関連
        self.setting = None

        # UI関連
        self.ui_show_in_explorer = None
        self.ui_keep_temp_file = None
        self.ui_is_ascii = None
        self.ui_output_log = None

        self.ui_batch_folder_path = None
        self.ui_logframe = None

        self.ui_updating = False

        # 初期化フラグ
        self.init = False

    # ==================================================
    def initialize(self):

        self.init = False

        self.script_file_path = os.path.abspath(__file__)
        self.script_dir_path = os.path.dirname(self.script_file_path)

        self.export_flag_file_path = self.script_dir_path + '/export_flag.txt'
        self.export_log_file_path = self.script_dir_path + '/export_log.txt'

        if not cmds.pluginInfo('fbxmaya', query=True, loaded=True):
            cmds.warning(u'FBXプラグインをロードしました')
            cmds.loadPlugin('fbxmaya.mll')

        self.logger = base_class.logger.Logger()

        self.setting = base_class.setting.Setting(self.tool_name)

        self.init = True

    # ==================================================
    def create_ui(self):

        self.initialize()

        if not self.init:
            return

        width = 450
        height = 800

        base_utility.ui.window.remove_same_id_window(self.window_name)

        cmds.window(
            self.window_name, title=self.tool_name + '  ' + self.tool_version,
            widthHeight=(width, height),
            s=1,
            mnb=True,
            mxb=False,
            rtf=True,
            cc=self.save_setting
        )

        cmds.paneLayout(
            configuration='horizontal2', ps=[2, 100, 99], shp=2, st=1)

        cmds.columnLayout(adjustableColumn=True)

        cmds.frameLayout(l=u'共通設定', cll=1, cl=0, bv=1, mw=10, mh=5)
        cmds.columnLayout(adjustableColumn=True, rs=4)

        self.ui_show_in_explorer = base_class.ui.check_box.CheckBox(
            '出力後エクスプローラを開く', False)

        self.ui_keep_temp_file = base_class.ui.check_box.CheckBox(
            '一時ファイルを保持', False)

        self.ui_output_log = base_class.ui.check_box.CheckBox(
            '出力後ログファイル作成、閲覧', False)

        self.ui_is_ascii = base_class.ui.check_box.CheckBox(
            'ASCIIフォーマットで出力', False)

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.frameLayout(l=u'通常エクスポート', cll=1, cl=0, bv=1, mw=10, mh=10)
        cmds.columnLayout(adjustableColumn=True, rs=4)

        base_class.ui.button.Button(u'ファイル名から判定してエクスポート', self.export_data, 'current')

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.frameLayout(l=u'フォルダ指定エクスポート', cll=1, cl=0,
                         bv=1, mw=10, mh=10, visible=True)
        self.ui_batch_folder_path = base_class.ui.data_selector.DataSelector(
            '対象フォルダ', '', False, True
        )

        base_class.ui.button.Button('フォルダ指定出力', self.export_data, 'folder')

        cmds.setParent('..')

        cmds.frameLayout(l='ログ', cll=1, cl=0, bv=1, mw=10, mh=10)
        self.ui_logframe = cmds.scrollField(editable=False, wordWrap=True)
        cmds.scrollField(self.ui_logframe, e=True, height=280)
        base_class.ui.button.Button('クリア', self.__clear_log)

        cmds.setParent('..')

        cmds.showWindow(self.window_name)

        self.load_setting()

    # ==================================================
    def __clear_log(self):

        cmds.scrollField(self.ui_logframe, e=True, text='')

    # ==================================================
    def export_data(self, input_type):

        base_utility.select.save_selection()

        self.logger.clear_log()

        self.logger.print_log = False
        self.logger.encode_type = None

        execute_flag = False

        self.save_setting()

        if input_type == 'current':
            execute_flag = self.export_current()
        elif input_type == 'folder':
            execute_flag = self.export_folder()

        if self.exist_flag_file():

            self.remove_flag_file()
            self.logger.write_log()
            self.logger.write_error(u'出力中にエラーが発生しました')

        else:

            if execute_flag:

                self.logger.write_log()
                self.logger.write_log(u'出力が完了しました')

        cmds.scrollField(self.ui_logframe, e=True, text=self.logger.get_log())

        base_utility.select.load_selection()

    # ==================================================
    def export_current(self):

        current_path = cmds.file(q=True, sn=True)

        this_exporter = chara_exporter.CharaExporter(self, current_path)
        this_exporter.logger = self.logger

        if not this_exporter.check_data():
            base_utility.ui.dialog.open_ok(
                '',
                u'{0}'.format(self.logger.get_log()),
                self.window_name
            )
            return False

        this_log = self.logger.get_log()
        this_info = ''

        file_modified = cmds.file(q=True, modified=True)

        if file_modified:

            this_info = \
                u'{0}\n\n{1}\nシーンが保存されていませんが出力しますか？\n(最後に保存したシーンで出力されます)\n{1}'\
                .format(this_log, '!' * 40)

        else:
            this_info = u'{0}\n\n上記設定で出力しますか?'.format(this_log)

        if not base_utility.ui.dialog.open_ok_cancel(u'確認', this_info, self.window_name):
            self.logger.write_log(u'\n出力をキャンセルしました')
            return False

        self.create_flag_file()

        import_reload_str = ""
        if sys.version_info.major != 2:
            import_reload_str = 'from importlib import reload;'

        base_utility.simple_batch.execute(
            '{0}{3}{1}{2}'.format(
                'import Project_Priari.priari_chara_exporter.main;',
                'reload(Project_Priari.priari_chara_exporter.main);',
                'Project_Priari.priari_chara_exporter.main.batch_export();',
                import_reload_str
            ),
            True,
            target_object_list_string='',
            target_file_path_list=[current_path],
            show_in_exprorer=self.ui_show_in_explorer.get_value(),
            keep_file=self.ui_keep_temp_file.get_value(),
            is_ascii=self.ui_is_ascii.get_value(),
            output_log=self.ui_output_log.get_value(),
        )

        return True

    # ==================================================
    def export_folder(self):

        target_folder_path = self.ui_batch_folder_path.get_path()

        if not os.path.isdir(target_folder_path):
            base_utility.ui.dialog.open_ok('', '対象フォルダが存在しません')
            return False

        target_file_path_list = self.ui_batch_folder_path.get_data_path_list()
        if len(target_file_path_list) == 0:
            base_utility.ui.dialog.open_ok('', '対象ファイルが見つかりませんでした')
            return False

        dialog_info = u'以下のファイルが対象となります。出力しますか?'

        if not base_utility.ui.dialog.open_ok_cancel_with_scroll('', dialog_info, target_file_path_list, self.window_name):
            self.logger.write_log(u'出力をキャンセルしました')
            return False

        base_utility.simple_batch.execute(
            '{0}{1}{2}'.format(
                'import Project_Priari.priari_chara_exporter.main;',
                'reload(Project_Priari.priari_chara_exporter.main);',
                'Project_Priari.priari_chara_exporter.main.batch_export();'
            ),
            True,
            target_file_path_list=target_file_path_list,
            target_object_list_string='',
            show_in_exprorer=self.ui_show_in_explorer.get_value(),
            keep_file=self.ui_keep_temp_file.get_value(),
            is_ascii=self.ui_is_ascii.get_value(),
            output_log=self.ui_output_log.get_value(),
        )

        return True

    # ==================================================
    def batch_export(self):

        # 初期化
        self.initialize()

        if not self.init:
            return

        target_file_path_list = \
            base_utility.simple_batch.get_param_value('target_file_path_list')

        target_object_list_string = \
            base_utility.simple_batch.get_param_value('target_object_list_string')

        is_ascii = \
            base_utility.simple_batch.get_param_value('is_ascii')

        keep_file = \
            base_utility.simple_batch.get_param_value('keep_file')

        show_in_exprorer = \
            base_utility.simple_batch.get_param_value('show_in_exprorer')

        output_log = \
            base_utility.simple_batch.get_param_value('output_log')

        # ログ準備
        self.logger.clear_log()
        self.logger.print_log = True
        self.logger.encode_type = 'shift_jis'

        # フラグファイル作成
        self.create_flag_file()

        try:
            self.batch_export_base(
                target_file_path_list, target_object_list_string, is_ascii, keep_file, show_in_exprorer
            )
        except Exception:
            self.logger.write_log(traceback.format_exc())
        else:
            # フラグファイル除去
            self.remove_flag_file()

        # ログ表示
        if output_log:
            self.logger.output_log(self.export_log_file_path)
            
            if not self.export_log_file_path:
                return

            if not os.path.isfile(self.export_log_file_path):
                return

            subprocess.Popen('notepad "' + self.export_log_file_path + '"')

    # ==================================================
    def batch_export_base(self, target_file_path_list, target_object_list_string, is_ascii, keep_file, show_in_exprorer):

        self.logger.write_log('######')
        self.logger.write_log(
            u'{0} バージョン {1}'.format(self.tool_name, self.tool_version))
        self.logger.write_log('######')
        self.logger.write_log()

        target_object_list = []
        if target_object_list_string:
            target_object_list = target_object_list_string.split(',')

        for target_file_path in target_file_path_list:

            exporter = chara_exporter.CharaExporter(self, target_file_path)

            exporter.logger = self.logger
            exporter.export_target_list = target_object_list
            exporter.is_ascii = is_ascii
            exporter.keep_temp_file = keep_file
            exporter.show_in_explorer = show_in_exprorer

            exporter.export()

    # ==================================================
    def create_flag_file(self):

        self.remove_flag_file()

        flag_file = open(self.export_flag_file_path, 'w')
        flag_file.close()

    # ==================================================
    def exist_flag_file(self):

        if os.path.isfile(self.export_flag_file_path):
            return True

        return False

    # ==================================================
    def remove_flag_file(self):

        if os.path.isfile(self.export_flag_file_path):
            os.remove(self.export_flag_file_path)

    # ==================================================
    def save_setting(self):

        self.ui_show_in_explorer.save_setting(self.setting, 'ShowInExplorer')
        self.ui_keep_temp_file.save_setting(self.setting, 'KeepTempFile')
        self.ui_output_log.save_setting(self.setting, 'OutputLog')
        self.ui_is_ascii.save_setting(self.setting, 'IsAscii')
        self.ui_batch_folder_path.save_setting(self.setting, 'BatchFolderPath')

    # ==================================================
    def load_setting(self):

        self.ui_show_in_explorer.load_setting(self.setting, 'ShowInExplorer')
        self.ui_keep_temp_file.load_setting(self.setting, 'KeepTempFile')
        self.ui_output_log.load_setting(self.setting, 'OutputLog')
        self.ui_is_ascii.load_setting(self.setting, 'IsAscii')
        self.ui_batch_folder_path.load_setting(self.setting, 'BatchFolderPath')
