# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os

import maya.cmds as cmds

from . import common
from . import classes

try:
    # for maya2022-
    from importlib import reload
    from builtins import str
    from builtins import range
    from builtins import object
except Exception:
    pass

reload(common)
reload(classes)


# ==================================================
def main():

    this_main = Main()
    this_main.create_ui()


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Main(object):

    # ==================================================
    def __init__(self):

        self.isInit = False

        self.tool_id = 'cdt_recorder_data_importer'
        self.tool_name = 'RecorderDataImporter'
        self.tool_version = '18101201'

        self.ui_window = None

        self.ui_target_data_dir_path = None
        self.ui_bake_frame = None
        self.ui_sampling_frame = None

        self.ui_selected_transform = None
        self.ui_target_transform = None
        self.ui_target_transform_layout = None

        self.ui_replace_target_node_count = 0
        self.ui_another_platform_replacement_field = None

        self.ui_default_setting = None
        self.ui_filter_count = 10
        self.ui_filter_list = None

        self.ui_updating = False

        self.setting = None

    # ==================================================
    def initialize(self):

        self.isInit = False

        self.setting = common.classes.other.setting.Setting(self.tool_id)

        self.isInit = True

    # ==================================================
    def create_ui(self):

        self.initialize()

        if not self.isInit:
            return

        self.ui_window = common.classes.maya.ui.window.Window(
            'win_' + self.tool_id, title=self.tool_name + ' ' + self.tool_version, width=450, height=750)

        self.ui_window.set_show_function(self.load_setting)
        self.ui_window.set_close_function(self.save_setting)

        cmds.frameLayout(l=u"フォルダ設定", cll=0, cl=0, bv=1,
                         mw=5, mh=5, parent=self.ui_window.ui_body_main)

        self.ui_target_data_dir_path = common.classes.maya.ui.data_selector.DataSelector(
            '対象データフォルダ', '', True, False)

        cmds.setParent('..')

        cmds.frameLayout(l=u"フレーム設定", cll=0, cl=0, bv=1,
                         mw=5, mh=5, parent=self.ui_window.ui_body_main)

        self.ui_bake_frame = common.classes.maya.ui.value_multi_field.ValueMultiField(
            'ベイクフレーム', [['Start', '開始', 0], ['End', '終了', 100]], True)

        common.classes.maya.ui.button.Button(
            'タイムラインからフレーム取得', self.set_bake_frame_ui_from_timeline)

        self.ui_sampling_frame = common.classes.maya.ui.value_multi_field.ValueMultiField(
            'サンプリング開始フレーム', [['Start', '開始', 0]], True)

        cmds.setParent('..')

        cmds.frameLayout(l=u"対象設定", cll=0, cl=0, bv=1,
                         mw=5, mh=5, parent=self.ui_window.ui_body_main)

        self.ui_selected_transform = common.classes.maya.ui.check_box.CheckBox(
            '選択トランスフォームを対象', True)

        self.ui_selected_transform.set_function(self.change_ui)

        self.ui_target_transform_layout = cmds.columnLayout(adj=True)

        self.ui_target_transform = common.classes.maya.ui.text_field.TextField(
            '対象トランスフォーム名', ''
        )

        cmds.rowLayout(numberOfColumns=3)

        common.classes.maya.ui.button.Button(
            '選択から設定(名前のみ)', self.set_target_transform_ui_from_selected, 'name', w=150)

        common.classes.maya.ui.button.Button(
            '選択から設定(フルパス)', self.set_target_transform_ui_from_selected, 'full', w=150)

        cmds.setParent('..')

        cmds.setParent('..')

        cmds.setParent('..')

        # Unityのノード名ではなく、代わりにMayaのノード名でXMLの名前と照合する為の置換リストUI
        self.ui_another_platform_replacement_field_frame = cmds.frameLayout(l='Unity⇔Maya置換対象ノード設定', cll=0, cl=0, bv=1, mw=5, mh=5, parent=self.ui_window.ui_body_main)

        description_text = 'UnityとMayaで異なるノードにベイクを行う為の置換対象を設定します\n' \
                           + '例)Unity側のノードが「オブジェクト」でMaya側のノードが「object」の場合\n' \
                           + '対象Unityノード「オブジェクト」対象Mayaノード「object」'

        cmds.text(label=description_text, align='left')

        common.classes.maya.ui.button.Button('追加', self.add_another_platform_replacement_field, self.ui_another_platform_replacement_field_frame, w=150)

        self.ui_another_platform_replacement_field = []
        for i in range(self.ui_replace_target_node_count):
            self.add_another_platform_replacement_field(self.ui_another_platform_replacement_field_frame)

        cmds.setParent('..')

        cmds.frameLayout(l=u"ベイクフィルタ設定", cll=0, cl=0, bv=1,
                         mw=5, mh=1, parent=self.ui_window.ui_body_main)

        self.ui_default_setting = common.classes.maya.ui.custom_multi_field.CustomMultiField(
            'デフォルト設定',
            [
                ['Translate', 'Translate', True, 'checkBox'],
                ['Rotate', 'Rotate', True, 'checkBox'],
                ['Scale', 'Scale', True, 'checkBox']
            ]
        )

        cmds.separator(height=5, style='in')

        self.ui_filter_list = []
        for p in range(self.ui_filter_count):

            this_ui_filter = common.classes.maya.ui.custom_multi_field.CustomMultiField(
                'フィルタ' + str(p + 1),
                [
                    ['Enable', '使用', True, 'checkBox'],
                    ['Target', '対象', 0, 'textField'],
                    ['Translate', 'Translate', False, 'checkBox'],
                    ['Rotate', 'Rotate', False, 'checkBox'],
                    ['Scale', 'Scale', False, 'checkBox'],
                    ['GetButton', '選択から取得', False, 'button'],
                    ['UpButton', ' ↑ ', False, 'button'],
                    ['DownButton', ' ↓ ', False, 'button']
                ]
            )

            this_ui_filter.set_function(
                5, self.set_filter_ui_from_selected, p)

            this_ui_filter.set_function(
                6, self.sort_filter_ui_from_selected, p, True)

            this_ui_filter.set_function(
                7, self.sort_filter_ui_from_selected, p, False)

            self.ui_filter_list.append(this_ui_filter)

        cmds.setParent('..')

        common.classes.maya.ui.button.Button(
            'ベイク開始', self.execute_bake, parent=self.ui_window.ui_footer_main, height=40, bgc=[0.8, 0.6, 0.6])

        self.ui_window.show()

        self.update_ui()

    # ==================================================
    def update_ui(self):

        self.ui_updating = True

        is_selected_transform = self.ui_selected_transform.apply_check_box_param(
            q=True, v=True)

        if is_selected_transform:
            cmds.columnLayout(
                self.ui_target_transform_layout, e=True, enable=False)
        else:
            cmds.columnLayout(
                self.ui_target_transform_layout, e=True, enable=True)

        self.ui_updating = False

    # ==================================================
    def change_ui(self):

        if self.ui_updating:
            return

        self.update_ui()

    # ==================================================
    def set_filter_ui_from_selected(self, filter_index):

        select_string = ''

        select_list = cmds.ls(sl=True, l=True, typ='transform')

        if select_list:

            for select in select_list:

                short_name = select.split('|')[-1]
                select_string += short_name + ' '

        if select_string != '':
            select_string = select_string[0:-1]

        self.ui_filter_list[filter_index].set_value(1, select_string)

    # ==================================================
    def sort_filter_ui_from_selected(self, filter_index, is_up):

        dst_filter_index = filter_index

        if is_up:
            dst_filter_index -= 1
        else:
            dst_filter_index += 1

        if dst_filter_index < 0 or dst_filter_index >= len(self.ui_filter_list):
            return

        src_ui_filter = self.ui_filter_list[filter_index]
        dst_ui_filter = self.ui_filter_list[dst_filter_index]

        for cnt in range(len(src_ui_filter.ui_value_id_list)):

            src_value = dst_ui_filter.get_value(cnt)
            dst_value = src_ui_filter.get_value(cnt)

            self.ui_filter_list[filter_index].set_value(
                cnt, src_value)

            self.ui_filter_list[dst_filter_index].set_value(
                cnt, dst_value)

    # ==================================================
    def set_bake_frame_ui_from_timeline(self):

        start_time = cmds.playbackOptions(q=True, min=True)
        end_time = cmds.playbackOptions(q=True, max=True)

        self.ui_bake_frame.set_value(0, start_time)
        self.ui_bake_frame.set_value(1, end_time)

    # ==================================================
    def set_target_transform_ui_from_selected(self, name_type):

        select_string = ''

        select_list = cmds.ls(sl=True, l=True, typ='transform')

        if select_list:

            for select in select_list:

                fix_name = select

                if name_type == 'name':

                    fix_name = select.split('|')[-1]

                select_string += fix_name + ' '

        if select_string != '':
            select_string = select_string[0:-1]

        self.ui_target_transform.set_value(select_string)

    # ==================================================
    def add_another_platform_replacement_field(self, parent=None):

        another_platform_replacement_field = common.classes.maya.ui.custom_multi_field.CustomMultiField(
            '',
            [
                ['Enable', '使用', True, 'checkBox'],
                ['UnityTarget', '対象Unityノード名', '', 'textField'],
                ['MayaTarget', '対象Mayaノード名', '', 'textField'],
                ['DeleteButton', '削除', None, 'button']
            ],
            parent=parent
        )
        another_platform_replacement_field.set_function(3, self.delete_another_platform_replacement_field, another_platform_replacement_field)

        self.ui_another_platform_replacement_field.append(another_platform_replacement_field)

    # ==================================================
    def delete_another_platform_replacement_field(self, target_ui):

        self.ui_another_platform_replacement_field.remove(target_ui)
        target_ui.delete_ui()

    # ==================================================
    def load_setting(self):

        self.ui_window.load_setting(self.setting, 'MainWindow')

        self.ui_target_data_dir_path.load_setting(
            self.setting, 'TargetDirPath')

        self.ui_bake_frame.load_setting(
            self.setting, 'BakeFrame')

        self.ui_sampling_frame.load_setting(
            self.setting, 'SamplingFrame')

        self.ui_selected_transform.load_setting(
            self.setting, 'SelectedTransform')

        self.ui_target_transform.load_setting(
            self.setting, 'TargetTransform'
        )

        self.ui_default_setting.load_setting(
            self.setting, 'DefaultSetting'
        )

        count = -1
        for ui_filter in self.ui_filter_list:
            count += 1

            ui_filter.load_setting(
                self.setting, 'Filter' + str(count)
            )

    # ==================================================
    def save_setting(self):

        self.ui_window.save_setting(self.setting, 'MainWindow')

        self.ui_target_data_dir_path.save_setting(
            self.setting, 'TargetDirPath')

        self.ui_bake_frame.save_setting(
            self.setting, 'BakeFrame')

        self.ui_sampling_frame.save_setting(
            self.setting, 'SamplingFrame')

        self.ui_selected_transform.save_setting(
            self.setting, 'SelectedTransform')

        self.ui_target_transform.save_setting(
            self.setting, 'TargetTransform'
        )

        self.ui_default_setting.save_setting(
            self.setting, 'DefaultSetting'
        )

        count = -1
        for ui_filter in self.ui_filter_list:
            count += 1

            ui_filter.save_setting(
                self.setting, 'Filter' + str(count)
            )

    # ==================================================
    def execute_bake(self):

        target_transform_list = None

        if self.ui_selected_transform.apply_check_box_param(q=True, v=True):
            target_transform_list = cmds.ls(sl=True, l=True, typ='transform')
        else:
            target_transform_list = \
                self.ui_target_transform.get_value().split(' ')

        if not target_transform_list:

            common.utility.maya.ui.dialog.open_ok(
                '確認', '対象トランスフォームが見つかりません', self.ui_window.ui_window_id
            )

            return

        target_data_dir_path = self.ui_target_data_dir_path.get_path()

        if not os.path.isdir(target_data_dir_path):

            common.utility.maya.ui.dialog.open_ok(
                '確認', 'フォルダが存在しません', self.ui_window.ui_window_id
            )

            return

        if not common.utility.maya.ui.dialog.open_yes_no(
            '確認', 'ベイクしますか?', self.ui_window.ui_window_id
        ):
            return

        bake_info = classes.bake_root_info.BakeRootInfo(self)

        bake_info.target_transform_list = target_transform_list

        bake_info.target_data_dir_path = target_data_dir_path

        bake_info.bake_start_frame = self.ui_bake_frame.get_value(0)
        bake_info.bake_end_frame = self.ui_bake_frame.get_value(1)

        bake_info.sampling_start_frame = self.ui_sampling_frame.get_value(0)

        # カスタムフィルタ
        this_filter_list = []
        this_attr_filter_list = []

        for ui_filter in self.ui_filter_list:

            this_enable = ui_filter.get_value(0)

            if not this_enable:
                continue

            this_filter = ui_filter.get_value(1)

            if not this_filter:
                continue

            this_filter_split = this_filter.split(' ')

            this_trans = ui_filter.get_value(2)
            this_rotate = ui_filter.get_value(3)
            this_scale = ui_filter.get_value(4)

            if not this_filter_split:
                continue

            for split_filter in this_filter_split:

                if not split_filter:
                    continue

                this_attr_filter = ''

                if this_trans:
                    this_attr_filter += 'Translate '

                if this_rotate:
                    this_attr_filter += 'Rotate '

                if this_scale:
                    this_attr_filter += 'Scale '

                if this_attr_filter:
                    this_attr_filter = this_attr_filter[0:-1]

                this_filter_list.append(split_filter)
                this_attr_filter_list.append(this_attr_filter)

        # デフォルトフィルタ
        this_trans = self.ui_default_setting.get_value(0)
        this_rotate = self.ui_default_setting.get_value(1)
        this_scale = self.ui_default_setting.get_value(2)

        this_attr_filter = ''

        if this_trans:
            this_attr_filter += 'Translate '

        if this_rotate:
            this_attr_filter += 'Rotate '

        if this_scale:
            this_attr_filter += 'Scale '

        if this_attr_filter:
            this_attr_filter = this_attr_filter[0:-1]

        this_filter_list.append('.*')
        this_attr_filter_list.append(this_attr_filter)

        bake_info.transform_filter_list = this_filter_list
        bake_info.attr_filter_list = this_attr_filter_list

        replace_target_node_info_dict = {}
        # TranformRecorderから出力したXMLのTransformInfo Nameとは異なる名前でbakeするノードの対象リスト
        for field in self.ui_another_platform_replacement_field:

            if not field.get_value(0):
                continue

            unity_node = field.get_value(1)
            maya_node = field.get_value(2)

            replace_target_node_info_dict[unity_node] = {
                'maya_node': maya_node,
                'unity_node': unity_node
            }
        bake_info.another_platform_replacement_info_dict = replace_target_node_info_dict

        # ベイク
        bake_info.bake()
