# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os
import traceback

import maya.cmds as cmds

from . import outline_to_uv_chara_exporter
from ..base_common import classes as base_class
from ..base_common import utility as base_utility

try:
    from builtins import object
except Exception:
    pass


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

        self.tool_version = '23030201'
        self.tool_name = 'OutlineToUVCharaExporter'

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
        self.ui_root_node_prefix = None
        self.ui_mesh_prefix = None

        self.ui_batch_folder_path = None
        self.ui_logframe = None

        self.ui_updating = False

        self.window_width = 450
        self.window_height = 400

    # ==================================================
    def initialize(self):

        self.script_file_path = os.path.abspath(__file__)
        self.script_dir_path = os.path.dirname(self.script_file_path)

        self.export_flag_file_path = self.script_dir_path + '/export_flag.txt'
        self.export_log_file_path = self.script_dir_path + '/export_log.txt'

        if not cmds.pluginInfo('fbxmaya', query=True, loaded=True):
            cmds.loadPlugin('fbxmaya.mll')
            cmds.warning(u'FBXプラグインをロードしました')

        self.logger = base_class.logger.Logger()

        self.setting = base_class.setting.Setting(self.tool_name)

        return True

    # ==================================================
    def create_ui(self):

        if not self.initialize():
            return

        base_utility.ui.window.remove_same_id_window(self.window_name)

        cmds.window(
            self.window_name, title=self.tool_name + ' Ver ' + self.tool_version,
            widthHeight=(self.window_width, self.window_height),
            s=1,
            mnb=True,
            mxb=False,
            rtf=True,
            cc=self.save_setting
        )

        # 全体コンテナ Start
        container = cmds.paneLayout(configuration='horizontal2', ps=[2, 100, 99], shp=2, st=1)
        cmds.columnLayout(adjustableColumn=True)

        # 共通セクション
        cmds.frameLayout(l=u'共通設定', cll=1, cl=0, bv=1, mw=10, mh=5)
        cmds.columnLayout(adjustableColumn=True, rs=4)
        self.ui_is_combine_export = base_class.ui.check_box.CheckBox('頭部と身体を一体化して出力', True)
        self.ui_show_in_explorer = base_class.ui.check_box.CheckBox('出力後エクスプローラを開く', False)
        self.ui_keep_temp_file = base_class.ui.check_box.CheckBox('一時ファイルを保持', False)
        self.ui_output_log = base_class.ui.check_box.CheckBox('出力後ログファイル作成、閲覧', False)
        self.ui_is_ascii = base_class.ui.check_box.CheckBox('ASCIIフォーマットで出力', False)
        self.ui_root_node_prefix = base_class.ui.text_field.TextField('対象のルートノードの接頭辞', 'mdl_')
        self.ui_mesh_prefix = base_class.ui.text_field.TextField('対象のメッシュの接頭辞', 'M_')
        cmds.setParent('..')
        cmds.setParent('..')

        # 通常エクスポートセクション
        cmds.frameLayout(l=u'通常エクスポート', cll=1, cl=0, bv=1, mw=10, mh=10)
        cmds.columnLayout(adjustableColumn=True, rs=4)
        base_class.ui.button.Button(u'ファイル名から判定してエクスポート', self.export_data)
        cmds.setParent('..')
        cmds.setParent('..')

        # ログセクション
        cmds.frameLayout(l='ログ', cll=1, cl=0, bv=1, mw=10, mh=10)
        self.ui_logframe = cmds.scrollField(editable=False, wordWrap=True)
        cmds.scrollField(self.ui_logframe, e=True, height=100)
        base_class.ui.button.Button('クリア', self.__clear_log)
        cmds.setParent('..')

        # 全体コンテナ End
        cmds.setParent('..')
        cmds.setParent('..')

        cmds.showWindow(self.window_name)

        self.load_setting()

    # ==================================================
    def __clear_log(self):

        cmds.scrollField(self.ui_logframe, e=True, text='')

    # ==================================================
    def export_data(self):

        base_utility.select.save_selection()

        self.logger.clear_log()

        self.logger.print_log = False
        self.logger.encode_type = None

        execute_flag = False

        self.save_setting()

        self.export_current()

        if self.exist_flag_file():
            self.remove_flag_file()
            self.logger.write_log()
            self.logger.write_error(u'出力中にエラーが発生しました')
        elif execute_flag:
            self.logger.write_log()
            self.logger.write_log(u'出力が完了しました')

        cmds.scrollField(self.ui_logframe, e=True, text=self.logger.get_log())

        base_utility.select.load_selection()

    # ==================================================
    def export_current(self):

        current_path = cmds.file(q=True, sn=True)

        this_exporter = outline_to_uv_chara_exporter.OutlineToUVCharaExporter(
            current_path,
            self.logger,
            False, False, False,
            self.ui_root_node_prefix.get_value(),
            self.ui_mesh_prefix.get_value(),
            self.ui_is_combine_export.get_value(),
        )

        if not this_exporter.check_data():
            base_utility.ui.dialog.open_ok('', u'{0}'.format(self.logger.get_log()), self.window_name)
            return False

        this_log = self.logger.get_log()
        this_info = ''

        file_modified = cmds.file(q=True, modified=True)

        if file_modified:

            this_info = u'{0}\n\n{1}\nシーンが保存されていませんが出力しますか？\n(最後に保存したシーンで出力されます)\n{1}'.format(this_log, '!' * 40)

        else:
            this_info = u'{0}\n\n上記設定で出力しますか?'.format(this_log)

        if not base_utility.ui.dialog.open_ok_cancel(u'確認', this_info, self.window_name):
            self.logger.write_log(u'\n出力をキャンセルしました')
            return False

        self.create_flag_file()

        base_utility.simple_batch.execute(
            '{0}{1}'.format('import Project_DesignerDivision.outline_to_uv_chara_exporter.outline_to_uv_chara_exporter.main;',
                            'Project_DesignerDivision.outline_to_uv_chara_exporter.outline_to_uv_chara_exporter.main.batch_export();'),
            True,
            target_file_path_list=[current_path],
            show_in_exprorer=self.ui_show_in_explorer.get_value(),
            keep_file=self.ui_keep_temp_file.get_value(),
            is_ascii=self.ui_is_ascii.get_value(),
            output_log=self.ui_output_log.get_value(),
            root_node_prefix=self.ui_root_node_prefix.get_value(),
            mesh_prefix=self.ui_mesh_prefix.get_value(),
            is_combine_export=self.ui_is_combine_export.get_value(),
        )

        return True

    # ==================================================
    def batch_export(self):

        # 初期化
        if not self.initialize():
            return

        target_file_path_list = base_utility.simple_batch.get_param_value('target_file_path_list')
        is_ascii = base_utility.simple_batch.get_param_value('is_ascii')
        keep_file = base_utility.simple_batch.get_param_value('keep_file')
        show_in_exprorer = base_utility.simple_batch.get_param_value('show_in_exprorer')
        output_log = base_utility.simple_batch.get_param_value('output_log')
        root_node_prefix = base_utility.simple_batch.get_param_value('root_node_prefix')
        mesh_prefix = base_utility.simple_batch.get_param_value('mesh_prefix')
        is_combine_export = base_utility.simple_batch.get_param_value('is_combine_export')

        # ログ準備
        self.logger.clear_log()
        self.logger.print_log = True
        self.logger.encode_type = 'shift_jis'

        # フラグファイル作成
        self.create_flag_file()

        try:
            self.batch_export_base(target_file_path_list, is_ascii, keep_file, show_in_exprorer, root_node_prefix, mesh_prefix, is_combine_export)
        except Exception:
            self.logger.write_log(traceback.format_exc())
        else:
            # フラグファイル除去
            self.remove_flag_file()

        # ログ表示
        if output_log:
            self.logger.output_log(self.export_log_file_path)
            base_utility.io.open_notepad(self.export_log_file_path)

    # ==================================================
    def batch_export_base(self, target_file_path_list, is_ascii, keep_temp_file, show_in_exprorer, target_root_node_prefix, target_mesh_prefix, is_combine_export):

        self.logger.write_log('######')
        self.logger.write_log('{0} バージョン {1}'.format(self.tool_name, self.tool_version))
        self.logger.write_log('######')
        self.logger.write_log()

        for target_file_path in target_file_path_list:

            exporter = outline_to_uv_chara_exporter.OutlineToUVCharaExporter(
                target_file_path, self.logger, is_ascii, keep_temp_file, show_in_exprorer, target_root_node_prefix, target_mesh_prefix, is_combine_export)
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

        self.ui_is_combine_export.save_setting(self.setting, 'IsCombineExport')
        self.ui_show_in_explorer.save_setting(self.setting, 'ShowInExplorer')
        self.ui_keep_temp_file.save_setting(self.setting, 'KeepTempFile')
        self.ui_output_log.save_setting(self.setting, 'OutputLog')
        self.ui_is_ascii.save_setting(self.setting, 'IsAscii')
        # 211101 ツール移行時未検証の為一旦非表示(コメントアウト処理のみ)
        # self.ui_batch_folder_path.save_setting(self.setting, 'BatchFolderPath')
        self.ui_root_node_prefix.save_setting(self.setting, 'RootNodePrefix')
        self.ui_mesh_prefix.save_setting(self.setting, 'MeshPrefix')

    # ==================================================
    def load_setting(self):

        self.ui_is_combine_export.load_setting(self.setting, 'IsCombineExport')
        self.ui_show_in_explorer.load_setting(self.setting, 'ShowInExplorer')
        self.ui_keep_temp_file.load_setting(self.setting, 'KeepTempFile')
        self.ui_output_log.load_setting(self.setting, 'OutputLog')
        self.ui_is_ascii.load_setting(self.setting, 'IsAscii')
        # 211101 ツール移行時未検証の為一旦非表示(コメントアウト処理のみ)
        # self.ui_batch_folder_path.load_setting(self.setting, 'BatchFolderPath')
        self.ui_root_node_prefix.load_setting(self.setting, 'RootNodePrefix')
        self.ui_mesh_prefix.load_setting(self.setting, 'MeshPrefix')
