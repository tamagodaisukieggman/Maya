# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
    from builtins import object
except Exception:
    pass

import re
import traceback

import maya.cmds as cmds

from ..base_common import utility as base_utility
from ..base_common import classes as base_class


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CheckerParamItem(object):

    # ==================================================
    def __init__(self, root, param_value, for_batch_list=False):

        # ------------------------------
        # 変数

        self.root = root
        self.main = root.main
        self.param_value = param_value

        self.is_init = False

        self.info_target_list = None
        self.check_target_list = None

        self.error_target_list = None
        self.unerror_target_list = None

        self.is_check_data = False

        self.is_hit = False
        self.is_checked = False

        self.is_top_enable = True
        self.is_root_enable = True

        self.info_title = None
        self.info_column_list = None
        self.info_dict_list = None
        self.info_has_link_to_error_target = None

        self.for_batch_list = for_batch_list

        # ------------------------------
        # param_valueから割り当てられる変数

        self.ui_type = 'checker'

        self.enable = True

        self.data_type_list = None

        self.view_type = 'attribute'

        self.check_index = 0

        self.label = ''
        self.check_info = ''
        self.error_info = ''
        self.unerror_info = ''
        self.target_info = ''

        self.target_count_info = ''

        self.is_error_view = True
        self.is_error_select = True
        self.is_error_fix = False

        self.is_unerror_view = True
        self.is_unerror_select = True

        self.is_target_view = True
        self.is_target_select = True

        self.function = None
        self.function_arg = None

        self.is_warning = False

        # ------------------------------
        # UI

        self.ui_top_layout_id = None

        self.ui_root_layout_id = None

        self.ui_enable_button = None
        self.ui_info = None
        self.ui_info_button = None

        self.ui_check_button = None

        self.ui_error_view_button = None
        self.ui_error_select_button = None
        self.ui_error_fix_button = None

        self.ui_unerror_label = None
        self.ui_unerror_view_button = None
        self.ui_unerror_select_button = None

        self.ui_target_label = None
        self.ui_target_view_button = None
        self.ui_target_select_button = None

        # ------------------------------
        # UI変数

        self.ui_button_width = 40
        self.ui_sub_button_width = 15

        self.start_color = [0.4, 0.4, 0.4]
        self.hit_color = [0.8, 0.5, 0.5]
        self.warn_color = [0.8, 0.8, 0.0]
        self.no_hit_color = [0.5, 0.5, 0.8]
        self.green_active_color = [0.1, 0.9, 0.1]

        self.info_tips = 'チェック情報を表示'

        self.view_error_tips = 'エラーデータを表示'
        self.select_error_tips = 'エラーデータを選択'
        self.fix_error_tips = 'エラーデータを修正'

        self.view_unerror_tips = '通過データを表示'
        self.select_unerror_tips = '通過データを選択'

        self.view_target_tips = '対象データを表示'
        self.select_target_tips = '対象データを選択'

    # ==================================================
    def initialize(self):

        self.is_init = False

        self.read_param_value()

        if not self.enable:
            return

        if self.ui_type == 'checker':
            if not self.function:
                return

        self.is_init = True

    # ==================================================
    def read_param_value(self):

        if not self.param_value:
            return

        if 'enable' in self.param_value:
            self.enable = self.param_value['enable']

        if 'data_type' in self.param_value:
            self.data_type_list = self.param_value['data_type']

        if 'ui_type' in self.param_value:
            self.ui_type = self.param_value['ui_type']

        if 'view_type' in self.param_value:
            self.view_type = self.param_value['view_type']

        if 'label' in self.param_value:
            self.label = self.param_value['label']

        if 'check_info' in self.param_value:
            self.check_info = self.param_value['check_info']

        if 'error_info' in self.param_value:
            self.error_info = self.param_value['error_info']

        if 'unerror_info' in self.param_value:
            self.unerror_info = self.param_value['unerror_info']

        if 'target_info' in self.param_value:
            self.target_info = self.param_value['target_info']

        if 'target_count_info' in self.param_value:
            self.target_count_info = self.param_value['target_count_info']

        if 'error_view' in self.param_value:
            self.is_error_view = self.param_value['error_view']

        if 'error_select' in self.param_value:
            self.is_error_select = self.param_value['error_select']

        if 'is_warning' in self.param_value:
            self.is_warning = self.param_value['is_warning']

        if 'error_fix' in self.param_value:
            self.is_error_fix = self.param_value['error_fix']

        if 'unerror_view' in self.param_value:
            self.is_unerror_view = self.param_value['unerror_view']

        if 'unerror_select' in self.param_value:
            self.is_unerror_select = self.param_value['unerror_select']

        if 'target_view' in self.param_value:
            self.is_target_view = self.param_value['target_view']

        if 'target_select' in self.param_value:
            self.is_target_select = self.param_value['target_select']

        if 'func' in self.param_value:
            self.function = self.param_value['func']

        if 'func_arg' in self.param_value:
            self.function_arg = self.param_value['func_arg']

    # ==================================================
    def create_ui(self):

        if not self.is_init:
            return

        if self.ui_type == 'info':
            return

        if self.ui_type == 'frame':

            cmds.setParent('..')
            self.ui_top_layout_id = cmds.frameLayout(mw=2, mh=2, l=self.label)

            return

        self.ui_top_layout_id = cmds.columnLayout(adj=True)

        cmds.rowLayout(nc=3, adj=3)

        base_class.ui.label.Label('{0:02d} '.format(self.check_index + 1))

        self.ui_enable_button = \
            base_class.ui.check_button.CheckButton(
                '有効', '無効', self.is_root_enable, self.on_enable_button, width=30
            )

        self.ui_enable_button.set_bg_color(self.green_active_color, [0.4] * 3)

        self.ui_root_layout_id = cmds.rowLayout(nc=13, adj=2)

        self.ui_info_button = \
            base_class.ui.button.Button(
                '情報', self.on_info_button, width=30)

        base_class.ui.label.Label(' ' + self.label)

        self.ui_check_button = \
            base_class.ui.button.Button(
                'チェック', self.on_check_button, width=self.ui_button_width)

        self.ui_error_view_button = \
            base_class.ui.button.Button(
                '表示', self.on_error_view_button,
                width=self.ui_button_width, visible=False, ann='エラーデータを表示')

        self.ui_error_select_button = \
            base_class.ui.button.Button(
                '選択', self.on_error_select_button,
                width=self.ui_button_width, visible=False, ann='エラーデータを選択')

        self.ui_error_fix_button = \
            base_class.ui.button.Button(
                '修正', self.on_error_fix_button,
                width=self.ui_button_width, visible=False)

        self.ui_unerror_label = base_class.ui.label.Label(' 通過:')

        self.ui_unerror_view_button = \
            base_class.ui.button.Button(
                'V', self.on_unerror_view_button,
                width=self.ui_sub_button_width, visible=False, ann='通過データを表示')

        self.ui_unerror_select_button = \
            base_class.ui.button.Button(
                'S', self.on_unerror_select_button,
                width=self.ui_sub_button_width, visible=False, ann='通過データを選択')

        self.ui_target_label = base_class.ui.label.Label(' 対象:')

        self.ui_target_view_button = \
            base_class.ui.button.Button(
                'V', self.on_target_view_button,
                width=self.ui_sub_button_width, visible=False, ann='対象データを表示')

        self.ui_target_select_button = \
            base_class.ui.button.Button(
                'S', self.on_target_select_button,
                width=self.ui_sub_button_width, visible=False, ann='対象データを選択')

        cmds.setParent('..')

        cmds.setParent('..')

        cmds.separator(style='in')

        cmds.setParent('..')

        if self.is_error_view:
            self.ui_error_view_button.apply_button_param(
                e=True, visible=True)

        if self.is_error_select:
            self.ui_error_select_button.apply_button_param(
                e=True, visible=True)

        if self.is_error_fix:
            self.ui_error_fix_button.apply_button_param(
                e=True, visible=True)

        if self.is_unerror_view:
            self.ui_unerror_view_button.apply_button_param(
                e=True, visible=True)

        if self.is_unerror_select:
            self.ui_unerror_select_button.apply_button_param(
                e=True, visible=True)

        if self.is_target_view:
            self.ui_target_view_button.apply_button_param(
                e=True, visible=True)

        if self.is_target_select:
            self.ui_target_select_button.apply_button_param(
                e=True, visible=True)

        if self.for_batch_list:
            self.reduction_ui_for_batch_list()

    # ==================================================
    def reduction_ui_for_batch_list(self):

        # widthはなぜか1以下にできないため最小値の1
        minimum_width = 1

        self.ui_info_button.apply_button_param(e=True, visible=False)
        self.ui_info_button.apply_button_param(e=True, width=minimum_width)
        self.ui_check_button.apply_button_param(e=True, visible=False)
        self.ui_check_button.apply_button_param(e=True, width=minimum_width)

        self.ui_unerror_label.apply_label_param(e=True, visible=False)
        self.ui_unerror_label.apply_label_param(e=True, width=minimum_width)
        self.ui_target_label.apply_label_param(e=True, visible=False)
        self.ui_target_label.apply_label_param(e=True, width=minimum_width)

        if self.is_error_view:
            self.ui_error_view_button.apply_button_param(e=True, visible=False)
            self.ui_error_view_button.apply_button_param(e=True, width=minimum_width)

        if self.is_error_select:
            self.ui_error_select_button.apply_button_param(e=True, visible=False)
            self.ui_error_select_button.apply_button_param(e=True, width=minimum_width)

        if self.is_error_fix:
            self.ui_error_fix_button.apply_button_param(e=True, visible=False)
            self.ui_error_fix_button.apply_button_param(e=True, width=minimum_width)

        if self.is_unerror_view:
            self.ui_unerror_view_button.apply_button_param(e=True, visible=False)
            self.ui_unerror_view_button.apply_button_param(e=True, width=minimum_width)

        if self.is_unerror_select:
            self.ui_unerror_select_button.apply_button_param(e=True, visible=False)
            self.ui_unerror_select_button.apply_button_param(e=True, width=minimum_width)

        if self.is_target_view:
            self.ui_target_view_button.apply_button_param(e=True, visible=False)
            self.ui_target_view_button.apply_button_param(e=True, width=minimum_width)

        if self.is_target_select:
            self.ui_target_select_button.apply_button_param(e=True, visible=False)
            self.ui_target_select_button.apply_button_param(e=True, width=minimum_width)

    # ==================================================
    def update_ui(self):

        self.update_enable_flag()

        if self.ui_type == 'checker':

            if self.is_top_enable:
                cmds.columnLayout(self.ui_top_layout_id, e=True, en=True)
            else:
                cmds.columnLayout(self.ui_top_layout_id, e=True, en=False)

            if self.is_root_enable:
                cmds.rowLayout(self.ui_root_layout_id, e=True, en=True)
            else:
                cmds.rowLayout(self.ui_root_layout_id, e=True, en=False)

            self.update_check_button_ui()

    # ==================================================
    def update_enable_flag(self):

        self.is_top_enable = True

        data_type = None

        if self.for_batch_list:
            self.is_top_enable = True
            return

        if self.main.chara_info.exists:

            data_type = self.main.chara_info.data_type

        if data_type:

            self.is_top_enable = True

            if self.data_type_list and data_type not in self.data_type_list:

                self.is_top_enable = False

                if data_type in self.data_type_list:
                    self.is_top_enable = True

            # facial_target検出対応:
            # facial_targetはfacial_target用のチェッカーしか動作確認が取れていないため、
            # data_type_listが空のものも実行できてはいけない。
            if self.main.chara_info.is_facial_target:

                # infoなども無効化してしまうとcsv出力などに問題を生じるため、checkerに限定
                if self.ui_type == 'checker':
                    self.is_top_enable = False

                    if self.data_type_list and 'facial_target' in self.data_type_list:
                        self.is_top_enable = True

        else:

            self.is_top_enable = False

        if self.ui_type == 'checker':

            if data_type:

                self.update_info_target_list()

                if not self.info_target_list:
                    self.is_top_enable = False

    # ==================================================
    def update_info_target_list(self):

        if self.ui_type != 'checker':
            return

        self.info_target_list = []

        self.is_check_data = False

        self.function(self, self.function_arg)

        self.info_target_list = \
            base_utility.list.get_unique_list(self.info_target_list)

    # ==================================================
    def update_check_button_ui(self):

        if self.ui_type != 'checker':
            return

        self.ui_check_button.apply_button_param(e=True, enable=True)
        self.ui_check_button.apply_button_param(e=True, bgc=self.start_color)

        self.ui_error_view_button.apply_button_param(e=True, enable=False)
        self.ui_error_select_button.apply_button_param(e=True, enable=False)
        self.ui_error_fix_button.apply_button_param(e=True, enable=False)

        self.ui_unerror_label.apply_label_param(e=True, enable=False)
        self.ui_unerror_view_button.apply_button_param(e=True, enable=False)
        self.ui_unerror_select_button.apply_button_param(e=True, enable=False)

        self.ui_target_label.apply_label_param(e=True, enable=False)
        self.ui_target_view_button.apply_button_param(e=True, enable=False)
        self.ui_target_select_button.apply_button_param(e=True, enable=False)

        if self.is_checked:

            self.ui_check_button.apply_button_param(
                e=True, bgc=self.no_hit_color)

            self.ui_target_view_button.apply_button_param(
                e=True, enable=True)

            self.ui_unerror_view_button.apply_button_param(
                e=True, enable=True)

            self.ui_unerror_select_button.apply_button_param(
                e=True, enable=True)

            self.ui_target_view_button.apply_button_param(
                e=True, enable=True)

            self.ui_target_select_button.apply_button_param(
                e=True, enable=True)

        if self.is_hit:

            self.ui_check_button.apply_button_param(
                e=True, bgc=self.hit_color)

            if self.is_warning:
                self.ui_check_button.apply_button_param(
                    e=True, bgc=self.warn_color)

            self.ui_error_view_button.apply_button_param(
                e=True, enable=True)

            self.ui_error_select_button.apply_button_param(
                e=True, enable=True)

            self.ui_error_fix_button.apply_button_param(
                e=True, enable=True)

        self.add_annotion_to_ui()

    # ==================================================
    def add_require_value_to_label(self, req_str):
        """
        情報ウィンドウ上に規定値を追加する
        """

        # 頭の半角空白を消すと更新が入るたびに半角空白が入ることになるので消さないこと
        pattern = r' \(規定値:.*\)$'

        match_part = re.search(pattern, self.check_info)

        if match_part is not None:
            self.check_info = self.check_info[0:match_part.start()]

        self.check_info += ' (規定値:{0})'.format(req_str)

    # ==================================================
    def add_annotion_to_ui(self):

        if self.info_target_list is not None:

            add_tips = ' 件数:' + str(len(self.info_target_list))

            self.ui_info_button.apply_button_param(
                e=True, ann=self.info_tips + add_tips)
        else:

            self.ui_info_button.apply_button_param(
                e=True, ann=self.info_tips)

        if not self.is_checked:

            self.ui_error_view_button.apply_button_param(
                e=True, ann=self.view_error_tips)
            self.ui_error_select_button.apply_button_param(
                e=True, ann=self.select_error_tips)
            self.ui_error_fix_button.apply_button_param(
                e=True, ann=self.fix_error_tips)

            self.ui_unerror_view_button.apply_button_param(
                e=True, ann=self.view_unerror_tips)
            self.ui_unerror_select_button.apply_button_param(
                e=True, ann=self.select_unerror_tips)

            self.ui_target_view_button.apply_button_param(
                e=True, ann=self.view_target_tips)
            self.ui_target_select_button.apply_button_param(
                e=True, ann=self.select_target_tips)

            return

        if self.error_target_list is not None:

            add_tips = ' 件数:' + str(len(self.error_target_list))

            self.ui_error_view_button.apply_button_param(
                e=True, ann=self.view_error_tips + add_tips)

            self.ui_error_select_button.apply_button_param(
                e=True, ann=self.select_error_tips + add_tips)

            self.ui_error_fix_button.apply_button_param(
                e=True, ann=self.fix_error_tips + add_tips)

        if self.unerror_target_list is not None:

            add_tips = ' 件数:' + str(len(self.unerror_target_list))

            self.ui_unerror_view_button.apply_button_param(
                e=True, ann=self.view_unerror_tips + add_tips)

            self.ui_unerror_select_button.apply_button_param(
                e=True, ann=self.select_unerror_tips + add_tips)

        if self.check_target_list is not None:

            add_tips = ' 件数:' + str(len(self.check_target_list))

            self.ui_target_view_button.apply_button_param(
                e=True, ann=self.view_target_tips + add_tips)

            self.ui_target_select_button.apply_button_param(
                e=True, ann=self.select_target_tips + add_tips)

    # ==================================================
    def on_enable_button(self):

        self.is_root_enable = self.ui_enable_button.get_value()

        self.update_ui()

    # ==================================================
    def on_info_button(self):

        self.root.info_window.view_type = self.view_type
        self.root.info_window.info = self.check_info
        self.root.info_window.target_list = self.info_target_list

        self.root.info_window.show()

    # ==================================================
    def on_check_button(self):

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

        result = self.update_error_target_list()
        if result != '':
            error_message = 'チェッカー番号:{}\n項目名:{}\nのチェック実行時にエラーが発生しました。\nダイアログをスクリーンショット撮影し、TA班までご連絡ください。\n\n{}'.format(
                self.check_index + 1, self.label, result
            )
            cmds.confirmDialog(
                title='CheckerError',
                message=error_message,
                button=['OK'],
                defaultButton='OK',
                icon='critical'
            )
            return

        self.update_ui()

    # ==================================================
    def on_error_view_button(self):

        self.root.info_window.view_type = self.view_type
        self.root.info_window.info = self.error_info
        self.root.info_window.target_list = self.error_target_list

        self.root.info_window.show()

    # ==================================================
    def on_error_select_button(self):

        self.select_target(self.error_target_list)

    # ==================================================
    def on_error_fix_button(self):

        if not self.error_target_list:
            return

    # ==================================================
    def on_unerror_view_button(self):

        self.root.info_window.view_type = self.view_type
        self.root.info_window.info = self.unerror_info
        self.root.info_window.target_list = self.unerror_target_list

        self.root.info_window.show()

    # ==================================================
    def on_unerror_select_button(self):

        self.select_target(self.unerror_target_list)

    # ==================================================
    def on_target_view_button(self):

        self.root.info_window.view_type = self.view_type
        self.root.info_window.info = self.target_info
        self.root.info_window.target_list = self.check_target_list

        self.root.info_window.show()

    # ==================================================
    def on_target_select_button(self):

        self.select_target(self.check_target_list)

    # ==================================================
    def select_target(self, target_list):

        cmds.select(cl=True)

        if not target_list:
            return

        select_list = []

        for target in target_list:

            if not base_utility.node.exists(target):
                continue

            select_list.append(target)

        if not select_list:
            return

        cmds.select(select_list, r=True)

    # ==================================================
    def update_error_target_list(self):

        if self.ui_type != 'checker' and self.ui_type != 'info':
            return ''

        self.is_checked = False
        self.is_hit = False
        self.is_check_data = False

        self.info_target_list = []
        self.error_target_list = []
        self.unerror_target_list = []
        self.check_target_list = []

        self.info_title = ''
        self.info_column_list = []
        self.info_dict_list = []
        self.info_has_link_to_error_target = False

        if not self.is_top_enable:
            return ''

        if not self.is_root_enable:
            return ''

        self.is_check_data = True

        try:
            self.function(self, self.function_arg)
        except Exception:
            self.error_target_list = [traceback.format_exc()]
            return traceback.format_exc()

        if not self.info_target_list:
            self.is_hit = False

        if not self.check_target_list:
            self.is_hit = False

        if self.error_target_list:
            self.is_hit = True

        self.info_target_list = \
            base_utility.list.get_unique_list(self.info_target_list)

        self.check_target_list = \
            base_utility.list.get_unique_list(self.check_target_list)

        self.error_target_list = \
            base_utility.list.get_unique_list(self.error_target_list)

        self.unerror_target_list = \
            base_utility.list.get_unique_list(self.unerror_target_list)

        self.is_checked = True

        return ''

    # ==================================================
    def set_enable_button(self, enable):

        if not self.ui_enable_button:
            return

        self.is_root_enable = enable

        self.ui_enable_button.set_value(self.is_root_enable)

        self.update_ui()

    # ==================================================
    def reset_info(self):

        self.info_target_list = []
        self.check_target_list = []
        self.error_target_list = []
        self.unerror_target_list = []

        self.info_title = ''
        self.info_column_list = []
        self.info_dict_list = []
        self.info_has_link_to_error_target = False

        self.is_checked = False
        self.is_hit = False

    # ==================================================
    def write_to_result_data_list(self):

        if self.ui_type != 'checker':
            return

        # エラーの数値チェック

        this_error_info = None
        this_count_info = None

        if self.error_target_list:
            if self.is_warning:
                this_error_info = '△ (' + str(len(self.error_target_list)) + ')'
            elif self.error_target_list == ['! エラー']:
                this_error_info = '! エラー'
            else:
                this_error_info = '× (' + str(len(self.error_target_list)) + ')'

        else:

            if self.is_checked:
                this_error_info = '〇'
            else:
                this_error_info = '----'

        self.root.batch_error_data_list.append(this_error_info)

        # 対象カウント情報がある場合は記述
        if self.target_count_info:

            if self.check_target_list:
                this_count_info = str(len(self.check_target_list))
            else:
                this_count_info = '0'

            self.root.batch_count_data_list.append(this_count_info)
