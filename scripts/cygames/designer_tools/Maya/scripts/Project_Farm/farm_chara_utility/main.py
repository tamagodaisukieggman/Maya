# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import zip
    from builtins import str
    from builtins import range
    from builtins import object
    from importlib import reload
except:
    pass

import sys
import json

import maya.cmds as cmds
import maya.mel as mel

from .. import base_common
from ..base_common import classes as base_class
# from ..base_common import utility as base_utility

from .. import farm_common

from . import classes as chara_util_class

reload(base_common)
reload(farm_common)
reload(chara_util_class)


class Main(object):

    def __init__(self):
        """
        """

        self.window_name = 'FarmCharaUtilityNew'
        self.tool_version = '22080901'

        # ここにはclasses以下で表示したいクラス名を羅列する
        # この順番通りに並び、順番を入れ替えた場合はここではなくsettingを参照するようになる
        self.utility_class_param_list = []
        self.key_utility_class_param = self.window_name + 'UtilityClassParam'
        self.key_default_utility_class_param_list = self.window_name + 'DefaultUtilityClassParam'
        self.default_utility_class_param_list = [
            {
                'label':
                'Maya系ツール',
                'class_list': [
                    'scene_opener',
                    'open_explorer',
                    'texture_changer',
                    # 旧フェイシャルの項目を塞ぐ
                    # TODO: 全データが新仕様になったら消すか新仕様対応するか検討
                    # 'facial_viewer',
                    'vtx_color_utility',
                    'change_polygon_view',
                    'scene_cleaner',
                    'bind_rebind_skin',
                    'create_outline',
                    'transfer_normal',
                    'move_chara_light',
                    'cgfx_toon_param',
                    'add_chara_info_obj',
                ]
            },
            {
                'label': 'Unity系ツール',
                'class_list': ['transfer_to_unity']
            }
        ]

        # TODO: 191211以前のDefaultClassParamList
        # 191211以前に追加したclassはシステムの不備でUIに新規追加出来ていなかったので暫定的に設置
        # 全員が更新したことを確認したらこの変数は削除し通常フローに戻す
        self.old_default_utility_class_param_list = [{
            'label':
            'Maya系ツール',
            'class_list': [
                'scene_opener',
                'open_explorer',
                'texture_changer',
                'change_polygon_view',
                'vtx_color_utility',
                'scene_cleaner',
                'weight_copy_by_uv',
                'bind_rebind_skin',
                'create_outline',
                'transfer_normal',
                'move_chara_light',
                'cgfx_toon_param',
            ]
        }, {
            'label': 'Unity系ツール',
            'class_list': ['transfer_to_unity']
        }]

        # メニューアイテムに追加したい場合はここ
        # リストのラベルを横に増やしたい場合はさらに辞書型を増やすと増える
        self.menu_list = [
            {
                'label': 'Options',
                'item_param_list': [
                    {'label': 'シェルフに登録する', 'command': self.__show_setting_shelf_window},
                    {'label': 'UIの入れ替え/表示非表示', 'command': self.__show_sort_class_window},
                    {'label': 'UI設定をリセットする', 'command': self.reset_utility_class_param_list}
                ]
            }
        ]

        self.load_class_list = []

        self.setting = base_class.setting.Setting(self.window_name)
        self.window_width = 500
        self.window_height = 800
        self.first_frame_width = self.window_width - 300

        self.main_window_class = None
        self.shelf_window_class = None
        self.sort_class_window_class = None

        self.selected_class = None

        self.is_save = True

    def __close_function(self):
        """
        """

        if self.is_save:
            self.save_setting()

        # サブウィンドウ削除
        if self.shelf_window_class:
            self.shelf_window_class.close_window()

        if self.sort_class_window_class:
            self.sort_class_window_class.close_window()

    def save_setting(self):
        """
        """

        save_utility_default_class_param_list = json.dumps(self.default_utility_class_param_list)
        self.setting.save(self.key_default_utility_class_param_list, save_utility_default_class_param_list)

        save_utility_class_param_list = json.dumps(self.utility_class_param_list)
        self.setting.save(self.key_utility_class_param, save_utility_class_param_list)

        for load_class in self.load_class_list:

            try:
                load_class.save_settings()
            except Exception:
                pass

    def __pre_load_setting(self):
        """
        """

        loaded_default_utility_class_param_list = self.setting.load(
            self.key_default_utility_class_param_list,
            data_type=str,
            default_value=self.old_default_utility_class_param_list
        )
    
        if sys.version_info.major == 2:
            if type(loaded_default_utility_class_param_list) == str or type(loaded_default_utility_class_param_list) == unicode:
                loaded_default_utility_class_param_list = json.loads(str(loaded_default_utility_class_param_list))
        else:
            if type(loaded_default_utility_class_param_list) == str or type(loaded_default_utility_class_param_list) == bytes:
                loaded_default_utility_class_param_list = json.loads(str(loaded_default_utility_class_param_list))

        loaded_utility_class_param_list = self.setting.load(
            self.key_utility_class_param,
            data_type=str,
            default_value=self.default_utility_class_param_list
        )

        if sys.version_info.major == 2:
            if type(loaded_utility_class_param_list) == str or type(loaded_utility_class_param_list) == unicode:
                loaded_utility_class_param_list = json.loads(str(loaded_utility_class_param_list))
        else:
            if type(loaded_utility_class_param_list) == str or type(loaded_utility_class_param_list) == bytes:
                loaded_utility_class_param_list = json.loads(str(loaded_utility_class_param_list))

        # defaultListにないcategory、classがあったらリストから削除する
        tmp_class_param_list = []
        for class_param in loaded_utility_class_param_list:
            label = class_param['label']
            class_list = class_param['class_list']
            for default_class_param in self.default_utility_class_param_list:
                default_label = default_class_param['label']
                if label != default_label:
                    continue

                tmp_class_param = {
                    'label': label,
                    'class_list': []
                }

                default_class_list = default_class_param['class_list']
                for _class in class_list:
                    if _class not in default_class_list:
                        continue
                    tmp_class_param['class_list'].append(_class)

                tmp_class_param_list.append(tmp_class_param)

        # setting上のdefaultとself.default_utility_class_param_listの差異があったらリストに追加する
        for default_class_param in self.default_utility_class_param_list:

            class_list = []
            for class_param in loaded_default_utility_class_param_list:

                if class_param['label'] != default_class_param['label']:
                    continue

                class_list = class_param['class_list']
                break

            # setting上のdefault_utility_class_param_listにない新規のclass_paramがあった場合リストに追加
            else:

                tmp_class_param_list.append(default_class_param)

            if not class_list:
                continue

            for default_class in default_class_param['class_list']:

                if default_class not in class_list:

                    for i in range(len(tmp_class_param_list)):

                        if tmp_class_param_list[i]['label'] != default_class_param['label']:
                            continue

                        if default_class not in tmp_class_param_list[i]['class_list']:
                            tmp_class_param_list[i]['class_list'].append(default_class)
                            break

        self.utility_class_param_list = tmp_class_param_list

    def __post_load_setting(self):
        """
        """

        for load_class in self.load_class_list:

            try:
                load_class.load_settings()
            except Exception:
                pass

    def reset_utility_class_param_list(self, *args):
        """
        """

        for _class in self.load_class_list:

            try:
                _class.reset_setting()
            except Exception:
                pass

        self.utility_class_param_list = self.default_utility_class_param_list
        self.save_setting()
        self.is_save = False
        self.show_ui()

    def __show_setting_shelf_window(self, *args):
        """
        """

        self.shelf_window_class = SettingShelfWindow(self)
        self.shelf_window_class.show_ui()

    def __show_sort_class_window(self, *args):
        """
        """

        self.sort_class_window_class = SortClassWindow(self)
        self.sort_class_window_class.show_ui()

    def show_ui(self):
        """
        ui表示
        UIパーツは各クラスから引用してくる
        """

        self.__pre_load_setting()

        self.main_window_class = base_class.ui.window.Window(
            self.window_name, 'Farm Chara Utility ver {}'.format(self.tool_version), menu_list=self.menu_list,
            width=self.window_width, height=self.window_height, rtf=False)
        self.main_window_class.set_close_function(self.__close_function)

        cmds.columnLayout(adj=True, p=self.main_window_class.ui_body_layout_id, rs=5)

        # UIセット
        for utility_class_param in self.utility_class_param_list:

            utility_class_label = utility_class_param['label']
            utility_class_list = utility_class_param['class_list']

            cmds.frameLayout(l=utility_class_label, w=self.first_frame_width, cll=1, cl=0, bv=1, mw=5, mh=5)

            for utility_class in utility_class_list:

                class_str = 'chara_util_class.{0}.main.Main()'.format(utility_class)

                try:
                    class_obj = eval(class_str)
                    class_obj.show_ui()
                    self.load_class_list.append(class_obj)
                except Exception:
                    pass

            cmds.setParent('..')

        cmds.setParent('..')

        self.main_window_class.show()

        self.__post_load_setting()


class SettingShelfWindow(object):

    def __init__(self, main):
        """
        """

        self.main = main
        self.setting_shelf_window_name = 'FarmCharaUtilitySettingShelf'
        self.shelf_window_class = None

    def close_window(self):
        """
        """

        if self.shelf_window_class and cmds.window(self.shelf_window_class.ui_window_id, exists=True):
            cmds.deleteUI(self.shelf_window_class.ui_window_id)

    def show_ui(self, *args):
        """
        機能ごとにshelfに登録出来る設定を行うwindowを表示する
        """

        # 機能ごとのshelf設定を取得する
        shelf_command_param_dict_list = self.__get_shelf_command_param_dict_list()

        self.shelf_window_class = base_class.ui.window.Window(self.setting_shelf_window_name, 'シェルフ登録', width=600, height=700)

        cmds.columnLayout(adjustableColumn=True, p=self.shelf_window_class.ui_body_layout_id)

        for utility_class_param in self.main.utility_class_param_list:

            utility_class_list = utility_class_param['class_list']

            for utility_class in utility_class_list:

                if utility_class not in shelf_command_param_dict_list:
                    continue

                shelf_command_param_dict = shelf_command_param_dict_list[utility_class]

                main_shelf_command_param = shelf_command_param_dict['main']

                cmds.frameLayout(l=main_shelf_command_param.label, borderVisible=True, mh=5, mw=5)

                # メイン項目
                cmds.rowLayout(
                    numberOfColumns=2,
                    columnWidth2=(120, 75),
                    adjustableColumn=1,
                    columnAttach=[(1, 'left', 5), (2, 'right', 5)])

                cmds.text(l='{} Windowを開く'.format(main_shelf_command_param.label), align='left')
                cmds.button(l='登録', c=main_shelf_command_param.set_shelf)
                cmds.setParent('..')

                # サブ項目
                for sub_shelf_command_param in shelf_command_param_dict['sub_list']:

                    cmds.rowLayout(
                        numberOfColumns=2,
                        columnWidth2=(120, 75),
                        adjustableColumn=1,
                        columnAttach=[(1, 'left', 5), (2, 'right', 5)])

                    cmds.text(l='-> {0} 機能単体 {1}'.format(main_shelf_command_param.label, sub_shelf_command_param.label), align='left')
                    cmds.button(l='登録', c=sub_shelf_command_param.set_shelf)
                    cmds.setParent('..')

                cmds.setParent('..')

        cmds.setParent('..')

        self.shelf_window_class.show()

    def __get_shelf_command_param_dict_list(self):
        """
        """

        shelf_command_param_dict_list = {}

        for utility_class_param in self.main.utility_class_param_list:

            utility_class_list = utility_class_param['class_list']

            for utility_class in utility_class_list:

                main_commnad_str = 'chara_util_class.{0}.main.Main()'.format(utility_class)

                get_tool_label_str = '{0}.get_tool_label()'.format(main_commnad_str)
                get_shelf_main_command_str = '{0}.get_shelf_command_show_ui_with_window()'.format(main_commnad_str)

                # モジュールが見つからない場合はerrorとなるため
                # 念の為にtry-exceptを挿入する
                try:

                    label = eval(get_tool_label_str)
                    shelf_command = eval(get_shelf_main_command_str)
                    if not label or not shelf_command:
                        continue

                    shelf_command_param_class = ShelfCommandParam(label, shelf_command)
                    shelf_command_param_dict_list[utility_class] = {'main': None, 'sub_list': []}
                    shelf_command_param_dict_list[utility_class]['main'] = shelf_command_param_class

                except Exception:

                    continue

                if utility_class not in shelf_command_param_dict_list:
                    continue

                extra_shelf_command_param_list_str = '{0}.get_sub_shelf_command_param_list()'.format(main_commnad_str)

                try:

                    extra_shelf_command_param_list = eval(extra_shelf_command_param_list_str)

                except Exception:

                    continue

                for extra_shelf_command_param in extra_shelf_command_param_list:

                    label = extra_shelf_command_param['label']
                    shelf_command = extra_shelf_command_param['command']
                    if not label or not shelf_command:
                        continue

                    shelf_command_param_class = ShelfCommandParam(label, shelf_command)
                    shelf_command_param_dict_list[utility_class]['sub_list'].append(shelf_command_param_class)

        return shelf_command_param_dict_list


class SortClassWindow(object):

    def __init__(self, main):
        """
        """

        self.main = main
        self.sort_class_window_name = 'FarmCharaUtilitySortClass'
        self.sort_class_window_class = None

        self.utility_class_param_list = self.main.utility_class_param_list[:]
        self.unused_class_param_list = []

        self.current_category = None

        self.class_list = []
        self.class_label_list = []

    def close_window(self):
        """
        """

        if self.sort_class_window_class and cmds.window(self.sort_class_window_class.ui_window_id, exists=True):
            cmds.deleteUI(self.sort_class_window_class.ui_window_id)

    def show_ui(self, *args):
        """
        """

        self.sort_class_window_class = base_class.ui.window.Window(
            self.sort_class_window_name, 'UIの順番並び替え / 表示非表示', width=600, height=700)

        cmds.columnLayout(adj=True, p=self.sort_class_window_class.ui_body_layout_id, rowSpacing=10)

        cmds.frameLayout(l='カテゴリーの順番並び替え / 表示非表示')
        first_form = cmds.formLayout()

        src_category_list = self.__create_category_list(self.utility_class_param_list)
        if src_category_list:
            self.current_category = src_category_list[0]

        self.category_left_list_ui = cmds.textScrollList(
            numberOfRows=8, height=100,
            append=src_category_list,
            selectCommand=self.__change_category
        )
        first_left_up_button = base_class.ui.button.Button(
            '▲', self.__change_category_item_sort, 'up', width=16, height=16)
        first_left_down_button = base_class.ui.button.Button(
            '▼', self.__change_category_item_sort, 'down', width=16, height=16)

        dst_category_list = self.__create_category_list(
            self.main.default_utility_class_param_list, self.utility_class_param_list)

        self.category_right_list_ui = cmds.textScrollList(
            numberOfRows=8, height=100,
            append=dst_category_list
        )

        first_left_move_right_button = base_class.ui.button.Button(
            '＞', self.__remove_category)
        first_right_move_right_button = base_class.ui.button.Button(
            '＜', self.__add_category)

        cmds.formLayout(
            first_form,
            e=True,
            attachForm=[
                (first_left_up_button.ui_button_id, 'top', 5),
                (first_left_down_button.ui_button_id, 'top', 5),
                (self.category_left_list_ui, 'left', 0),
                (first_right_move_right_button.ui_button_id, 'bottom', 0),
                (self.category_right_list_ui, 'right', 0),
            ],
            attachPosition=[
                (first_left_move_right_button.ui_button_id, 'top', 26, 0),
                (first_left_move_right_button.ui_button_id, 'bottom', 0, 56),
                (first_left_move_right_button.ui_button_id, 'right', 2, 49),
                (first_left_move_right_button.ui_button_id, 'left', 2, 51),
                (first_right_move_right_button.ui_button_id, 'right', 2, 49),
                (first_right_move_right_button.ui_button_id, 'left', 2, 51),
            ],
            attachControl=[
                (self.category_left_list_ui, 'top', 5, first_left_down_button.ui_button_id),
                (self.category_left_list_ui, 'right', 5, first_left_move_right_button.ui_button_id),
                (self.category_right_list_ui, 'top', 5, first_left_up_button.ui_button_id),
                (self.category_right_list_ui, 'left', 5, first_right_move_right_button.ui_button_id),
                (first_left_down_button.ui_button_id, 'right', 5, first_left_move_right_button.ui_button_id),
                (first_left_up_button.ui_button_id, 'right', 5, first_left_down_button.ui_button_id),
                (first_right_move_right_button.ui_button_id, 'top', 5, first_left_move_right_button.ui_button_id),
            ]
        )

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.frameLayout(l='ツールの順番並び替え / 表示非表示')
        second_form = cmds.formLayout()

        src_class_list, src_class_label_list = self.__create_class_list(
            self.utility_class_param_list,
            [],
            self.current_category
        )

        self.class_left_list_ui = cmds.textScrollList(
            numberOfRows=8, height=200,
            append=src_class_label_list
        )
        second_left_up_button = base_class.ui.button.Button(
            '▲', self.__change_class_item_sort, 'up', width=16, height=16)
        second_left_down_button = base_class.ui.button.Button(
            '▼', self.__change_class_item_sort, 'down', width=16, height=16)

        dst_class_list, dst_class_label_list = self.__create_class_list(
            self.main.default_utility_class_param_list,
            self.utility_class_param_list,
            self.current_category
        )

        self.class_list = src_class_list + dst_class_list
        self.class_label_list = src_class_label_list + dst_class_label_list

        self.class_right_list_ui = cmds.textScrollList(
            numberOfRows=8, height=200,
            append=dst_class_label_list
        )

        second_left_move_right_button = base_class.ui.button.Button(
            '＞', self.__change_class_visible, self.class_left_list_ui, self.class_right_list_ui)
        second_right_move_right_button = base_class.ui.button.Button(
            '＜', self.__change_class_visible, self.class_right_list_ui, self.class_left_list_ui)

        cmds.formLayout(
            second_form,
            e=True,
            attachForm=[
                (second_left_up_button.ui_button_id, 'top', 5),
                (second_left_down_button.ui_button_id, 'top', 5),
                (self.class_left_list_ui, 'left', 0),
                (second_right_move_right_button.ui_button_id, 'bottom', 0),
                (self.class_right_list_ui, 'right', 0),
            ],
            attachPosition=[
                (second_left_move_right_button.ui_button_id, 'top', 26, 0),
                (second_left_move_right_button.ui_button_id, 'bottom', 0, 56),
                (second_left_move_right_button.ui_button_id, 'right', 2, 49),
                (second_left_move_right_button.ui_button_id, 'left', 2, 51),
                (second_right_move_right_button.ui_button_id, 'right', 2, 49),
                (second_right_move_right_button.ui_button_id, 'left', 2, 51),
            ],
            attachControl=[
                (self.class_left_list_ui, 'top', 5, second_left_down_button.ui_button_id),
                (self.class_left_list_ui, 'right', 5, second_left_move_right_button.ui_button_id),
                (self.class_right_list_ui, 'top', 5, second_left_up_button.ui_button_id),
                (self.class_right_list_ui, 'left', 5, second_right_move_right_button.ui_button_id),
                (second_left_down_button.ui_button_id, 'right', 5, second_left_move_right_button.ui_button_id),
                (second_left_up_button.ui_button_id, 'right', 5, second_left_down_button.ui_button_id),
                (second_right_move_right_button.ui_button_id, 'top', 5, second_left_move_right_button.ui_button_id),
            ]
        )

        cmds.setParent('..')
        cmds.setParent('..')

        base_class.ui.button.Button('パラメータを保存する', self.__save_class_param_list)
        base_class.ui.button.Button('パラメータを保存して再起動', self.__save_class_param_list, True)

        cmds.separator()

        base_class.ui.button.Button('UIを初期状態に戻す', self.main.reset_utility_class_param_list)

        cmds.setParent('..')

        self.sort_class_window_class.show()

    def __save_class_param_list(self, is_recreate=False):
        """
        """

        self.main.utility_class_param_list = self.utility_class_param_list
        self.main.save_setting()
        if is_recreate:
            self.main.is_save = False
            self.main.show_ui()

    def __create_category_list(self, src_param_list, dst_param_list=[], *args):
        """
        """

        category_list = []

        for src_param in src_param_list:

            src_category = src_param['label']

            if dst_param_list:
                dst_category_list = []
                for dst_param in dst_param_list:
                    dst_category = dst_param['label']
                    dst_category_list.append(dst_category)

                if src_category in dst_category_list:
                    continue

            category_list.append(src_category)

        return category_list

    def __create_class_list(self, src_param_list, dst_param_list=[], target_category=None, *args):
        """
        """

        if target_category is None:
            target_category = self.current_category

        class_list = []
        class_label_list = []

        for src_param_list in src_param_list:

            src_category = src_param_list['label']
            if src_category != target_category:
                continue

            src_class_list = src_param_list['class_list']

            if dst_param_list:
                for dst_param in dst_param_list:
                    dst_category = dst_param['label']
                    if src_category != dst_category:
                        continue
                    dst_class_list = dst_param['class_list']

                    for src_class in src_class_list:
                        if src_class in dst_class_list:
                            continue
                        class_list.append(src_class)

            else:
                class_list = src_param_list['class_list']

        for _class in class_list:

            get_tool_label_str = 'chara_util_class.{0}.main.Main().get_tool_label()'.format(_class)

            class_label = ''

            # class_listに沿ったラベルのリストを出力
            try:
                class_label = eval(get_tool_label_str)
            except Exception:
                pass

            class_label_list.append(class_label)

        return class_list, class_label_list

    def __change_category(self, *args):
        """
        """

        src_class_label_list = []
        dst_class_label_list = []

        category = cmds.textScrollList(self.category_left_list_ui, q=True, selectItem=True)
        if category is None:
            self.current_category = None
            self.class_list = []
            self.class_label_list = []
        else:
            self.current_category = category[0]
            src_class_list, src_class_label_list = self.__create_class_list(
                self.utility_class_param_list,
                [],
                self.current_category
            )
            dst_class_list, dst_class_label_list = self.__create_class_list(
                self.main.default_utility_class_param_list,
                self.utility_class_param_list,
                self.current_category
            )

            self.class_list = src_class_list + dst_class_list
            self.class_label_list = src_class_label_list + dst_class_label_list

        cmds.textScrollList(self.class_left_list_ui, e=True, removeAll=True)
        cmds.textScrollList(self.class_left_list_ui, e=True, append=src_class_label_list)

        cmds.textScrollList(self.class_right_list_ui, e=True, removeAll=True)
        cmds.textScrollList(self.class_right_list_ui, e=True, append=dst_class_label_list)

    def __change_visible(self, src_obj, dst_obj):
        """
        """

        src_select_item = cmds.textScrollList(src_obj, q=True, selectItem=True)
        src_select_index = cmds.textScrollList(src_obj, q=True, selectIndexedItem=True)

        if src_select_item is None or src_select_index is None:
            return

        cmds.textScrollList(src_obj, e=True, removeIndexedItem=src_select_index)
        cmds.textScrollList(dst_obj, e=True, append=src_select_item[0])
        dst_obj_item_len = cmds.textScrollList(dst_obj, q=True, numberOfItems=True)
        cmds.textScrollList(dst_obj, e=True, selectIndexedItem=dst_obj_item_len)

    def __add_category(self):
        """
        """

        self.__change_visible(self.category_right_list_ui, self.category_left_list_ui)

        category_list = cmds.textScrollList(self.category_left_list_ui, q=True, allItems=True)

        for category in category_list:

            for class_param in self.utility_class_param_list:

                label = class_param['label']

                if category == label:

                    break

            else:

                add_class_param = {}

                tmp_unused_class_param_list = []
                for unused_class_param in self.unused_class_param_list:
                    label = unused_class_param['label']
                    if category == label:
                        add_class_param = unused_class_param
                        continue
                    tmp_unused_class_param_list.append(unused_class_param)

                self.unused_class_param_list = tmp_unused_class_param_list

                if add_class_param:
                    self.utility_class_param_list.append(add_class_param)
                else:
                    for default_class_param in self.main.default_utility_class_param_list:
                        label = default_class_param['label']
                        if category == label:
                            self.utility_class_param_list.append(default_class_param)
                            break

        self.__change_category()

    def __remove_category(self):
        """
        """

        self.__change_visible(self.category_left_list_ui, self.category_right_list_ui)

        category_list = cmds.textScrollList(self.category_left_list_ui, q=True, allItems=True)

        tmp_class_param_list = []

        for class_param in self.utility_class_param_list:

            label = class_param['label']
            if category_list and label in category_list:
                tmp_class_param_list.append(class_param)
                continue

            self.unused_class_param_list.append(class_param)

        self.utility_class_param_list = tmp_class_param_list

        self.__change_category()

    def __change_class_visible(self, src_obj, dst_obj):
        """
        """

        self.__change_visible(src_obj, dst_obj)

        tmp_class_label_list = cmds.textScrollList(self.class_left_list_ui, q=True, allItems=True)
        tmp_class_list = []
        if tmp_class_label_list:
            for tmp_class_label in tmp_class_label_list:
                for _class, class_label in zip(self.class_list, self.class_label_list):
                    if class_label == tmp_class_label:
                        tmp_class_list.append(_class)
                        break

        tmp_class_param_list = []
        for class_param in self.utility_class_param_list:

            label = class_param['label']

            if label != self.current_category:
                tmp_class_param_list.append(class_param)
                continue

            tmp_class_param = {
                'label': label,
                'class_list': tmp_class_list
            }
            tmp_class_param_list.append(tmp_class_param)

        self.utility_class_param_list = tmp_class_param_list

    def __change_item_sort(self, obj, change_status):
        """
        """

        if change_status != 'up' and change_status != 'down':
            return

        item_list = cmds.textScrollList(obj, q=True, allItems=True)
        select_index = cmds.textScrollList(obj, q=True, selectIndexedItem=True)
        if select_index is None:
            return
        select_index = select_index[0]

        src_target_item_list_index = select_index - 1
        # 選択アイテムが一番上だったら処理しない
        if change_status == 'up' and src_target_item_list_index == 0:
            return
        # 選択アイテムが一番下だったら処理しない
        elif change_status == 'down' and src_target_item_list_index == len(item_list) - 1:
            return

        tmp_item_list = []
        for i in range(len(item_list)):

            if change_status == 'up':

                if i == src_target_item_list_index - 1:
                    continue
                elif i == src_target_item_list_index:
                    tmp_item_list.append(item_list[i])
                    tmp_item_list.append(item_list[i - 1])
                    continue

            elif change_status == 'down':

                if i == src_target_item_list_index + 1:
                    continue
                elif i == src_target_item_list_index:
                    tmp_item_list.append(item_list[i + 1])
                    tmp_item_list.append(item_list[i])
                    continue

            tmp_item_list.append(item_list[i])

        cmds.textScrollList(obj, e=True, removeAll=True)
        cmds.textScrollList(obj, e=True, append=tmp_item_list)

        if change_status == 'up':
            changed_item_index = select_index - 1
        elif change_status == 'down':
            changed_item_index = select_index + 1

        cmds.textScrollList(obj, e=True, selectIndexedItem=changed_item_index)

    def __change_category_item_sort(self, change_status):

        self.__change_item_sort(self.category_left_list_ui, change_status)

        category_list = cmds.textScrollList(self.category_left_list_ui, q=True, allItems=True)

        tmp_class_param_list = []
        for category in category_list:
            for class_param in self.utility_class_param_list:
                label = class_param['label']
                if category != label:
                    continue

                tmp_class_param_list.append(class_param)
                break

        self.utility_class_param_list = tmp_class_param_list

        self.__change_category()

    def __change_class_item_sort(self, change_status):
        """
        """

        self.__change_item_sort(self.class_left_list_ui, change_status)

        tmp_class_label_list = cmds.textScrollList(self.class_left_list_ui, q=True, allItems=True)
        tmp_class_list = []
        if tmp_class_label_list:
            for tmp_class_label in tmp_class_label_list:
                for _class, class_label in zip(self.class_list, self.class_label_list):
                    if class_label == tmp_class_label:
                        tmp_class_list.append(_class)
                        break

        tmp_class_param_list = []
        for class_param in self.utility_class_param_list:

            label = class_param['label']
            if label != self.current_category:
                tmp_class_param_list.append(class_param)
                continue
            tmp_class_param = {
                'label': label,
                'class_list': tmp_class_list
            }
            tmp_class_param_list.append(tmp_class_param)

        self.utility_class_param_list = tmp_class_param_list


class ShelfCommandParam(object):

    def __init__(self, label, shelf_command):
        """
        """

        self.label = label
        self.shelf_command = shelf_command

    def set_shelf(self, _):
        """
        """

        select_tab_name = self.__get_selected_shelf_tab_name()

        cmds.shelfButton(
            rpt=True,
            i1='pythonFamily.png',
            imageOverlayLabel=self.label,
            l=self.label,
            ann=self.label,
            c=self.shelf_command,
            stp='python',
            p=select_tab_name,
            style='iconAndTextVertical'
        )

        # iconのLabelを正常に表示するためにはShelfStyleの更新が必要
        mel.eval('setShelfStyle `optionVar -query shelfItemStyle` `optionVar -query shelfItemSize`;')

    def __get_selected_shelf_tab_name(self):
        """
        """

        shelf_top_level = mel.eval('$tmpVar=$gShelfTopLevel')
        select_tab_name = cmds.shelfTabLayout(shelf_top_level, q=True, selectTab=True)

        return select_tab_name
