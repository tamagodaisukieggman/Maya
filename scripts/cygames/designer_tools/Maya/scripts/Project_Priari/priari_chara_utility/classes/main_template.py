# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
except:
    pass
import maya.cmds as cmds
import sys

from ...base_common import classes as base_class


class Main(object):

    def __init__(self, class_name=''):
        """
        """

        # 必須項目 呼び出し先でも記述する必要がある
        self.tool_name = ''
        self.tool_label = ''
        self.tool_version = ''
        self.window_name = ''
        self.window_title = ''

        # 任意項目 このクラスのSystemPath class_nameを渡すと自動的に設定される
        self.this_class_str = ''
        # 任意項目 UIを別Windowで開くコマンドのstr class_nameを渡すと自動的に設定される
        self.shelf_command_show_ui_with_window = ''

        if sys.version_info.major == 2:
            self.this_base_common_reload_str = 'import Project_Priari.base_common;reload(Project_Priari.base_common);'
        else:
            self.this_base_common_reload_str = 'import Project_Priari.base_common;from importlib import reload;reload(Project_Priari.base_common);'
        if sys.version_info.major == 2:
            self.this_priari_common_reload_str = 'import Project_Priari.priari_common;reload(Project_Priari.priari_common);'
        else:
            self.this_priari_common_reload_str = 'import Project_Priari.priari_common;from importlib import reload;reload(Project_Priari.priari_common);'

        # 任意項目 他にshelfに自動で登録したいものがあればここにparamを登録すればリスト化される
        self.sub_shelf_command_param_list = []

        # 自動でshelfの開いた時のコマンドを生成する
        if class_name:
            self.this_class_str = 'Project_Priari.priari_chara_utility.classes.{}'.format(class_name)
            self.shelf_command_show_ui_with_window = self._create_shelf_command_str(
                'main',
                'show_ui_with_window'
            )

        # 任意項目 window単体で開くときのwindowSize 変更したい場合はoverride先で
        self.default_single_window_width = 500
        self.default_single_window_height = 300

        # Setting用のtool名とsettingの宣言
        self.setting_tool_name = 'PriariCharaUtilityNew'
        self.setting = base_class.setting.Setting(self.setting_tool_name)

        # show_uiに存在するframeのobject
        self.show_ui_frame = None
        # show_uiに存在するframeのsetting用key(__initializeで自動定義、特にいじる必要なし)
        self.key_frame_open = None
        # show_uiに存在するframeの開閉状態をsave, loadするか
        self.is_use_frame_open_status = True

        self.window = None

        base_class.ui.button.Button = UtilityButton

    def _create_shelf_command_str(self, exec_module_str, exec_func_str, *exec_func_args):
        """
        main_template.MainTemplate().show_ui()のようなシェルフコマンド文字列を生成する

        Parameters
        ----------
        exec_module_str : str
            実行するコマンドのモジュール名並びにクラス名
        exec_func_str : str
            実行するメソッド名
        exec_func_args : list
            メソッドの引数

        Returns
        ----------
        shelf_command : str
            シェルフに登録するコマンドを文字列にしたもの
        """

        pascal_exec_class_str = self.__convert_camel_to_pascal(exec_module_str)

        shelf_command = '{0}{1}'.format(
            self.this_base_common_reload_str,
            self.this_priari_common_reload_str
        )

        import_reload_str = ""
        if sys.version_info.major != 2:
            import_reload_str = 'from importlib import reload;'

        if exec_func_args:

            shelf_command += 'import {0}.{1};{5}reload({0}.{1});{0}.{1}.{2}().{3}({4})'.format(
                self.this_class_str,
                exec_module_str,
                pascal_exec_class_str,
                exec_func_str,
                ','.join(exec_func_args),
                import_reload_str
            )

        else:

            shelf_command += 'import {0}.{1};{4}reload({0}.{1});{0}.{1}.{2}().{3}()'.format(
                self.this_class_str,
                exec_module_str,
                pascal_exec_class_str,
                exec_func_str,
                import_reload_str
            )

        return shelf_command

    def _create_shelf_func_command_str(self, exec_module_str, exec_func_str, *exec_func_args):
        """
        main_template.show_ui()のようなシェルフコマンド文字列を生成する

        Parameters
        ----------
        exec_module_str : str
            実行するコマンドのモジュール名
        exec_func_str : str
            実行するメソッド名
        exec_func_args : list
            メソッドの引数

        Returns
        ----------
        shelf_command : str
            シェルフに登録するコマンドを文字列にしたもの
        """

        import_reload_str = ""
        if sys.version_info.major != 2:
            import_reload_str = 'from importlib import reload;'

        if exec_func_args:

            shelf_command = 'import {0}.{1};{4}reload({0}.{1});{0}.{1}.{2}({3})'.format(
                self.this_class_str,
                exec_module_str,
                exec_func_str,
                ','.join(exec_func_args),
                import_reload_str
            )

        else:

            shelf_command = 'import {0}.{1};{3}reload({0}.{1});{0}.{1}.{2}()'.format(
                self.this_class_str,
                exec_module_str,
                exec_func_str,
                import_reload_str
            )

        return shelf_command

    def __convert_camel_to_pascal(self, camel_str):
        """
        """

        camel_split_str_list = camel_str.split('_')

        pascal_str = ''
        for camel_split_str in camel_split_str_list:
            pascal_str += camel_split_str.capitalize()

        return pascal_str

    def __initialze(self):
        """
        tool_name等が定義されないと作れない変数を作る場所
        """

        self.key_frame_open = 'Setting{0}FrameOpen'.format(self.tool_name)
        self.key_window_width = 'Setting{0}WindowWidth'.format(self.tool_name)
        self.key_window_height = 'Setting{0}WindowHeight'.format(self.tool_name)

    def save_settings(self):
        """
        required_save_settingとsave_settingを実行する
        """

        self.__required_save_setting()
        self.save_setting()

    def __required_save_setting(self):
        """
        全ての継承先でsaveしてほしい項目を入れておく
        外部からの変更不可
        """

        if not self.setting:
            self.__initialze()

        if self.show_ui_frame and self.is_use_frame_open_status:
            is_frame_open = cmds.frameLayout(self.show_ui_frame, q=True, collapse=True)
            self.setting.save(self.key_frame_open, is_frame_open)

        # 設定したwindowのサイズを保存する
        if self.window:
            window_width = cmds.window(
                self.window.ui_window_id, q=True, width=True
            )
            window_height = cmds.window(
                self.window.ui_window_id, q=True, height=True
            )
            self.setting.save(self.key_window_width, window_width)
            self.setting.save(self.key_window_height, window_height)

    def save_setting(self):
        """
        任意項目 saveしたい項目があれば設定する
        """

        pass

    def load_settings(self):
        """
        required_load_settingとload_settingを実行する
        """

        self.__required_load_setting()
        self.load_setting()

    def __required_load_setting(self):
        """
        全ての継承先でloadしてほしい項目を入れておく
        外部からの変更不可
        """

        if not self.setting:
            self.__initialze()

        if self.show_ui_frame and self.is_use_frame_open_status:
            is_frame_open = self.setting.load(self.key_frame_open, bool, False)
            cmds.frameLayout(self.show_ui_frame, e=True, collapse=is_frame_open)

        # 前回設定したwindowサイズを呼び出す
        if self.window:
            window_width = self.setting.load(
                self.key_window_width, int, self.default_single_window_width
            )
            window_height = self.setting.load(
                self.key_window_height, int, self.default_single_window_height
            )
            cmds.window(
                self.window.ui_window_id, e=True, width=window_width, height=window_height
            )

    def load_setting(self):
        """
        任意項目 loadしたい項目があれば設定する
        """

        pass

    def reset_setting(self):
        """
        任意項目 UI状態のリセットを行いたい項目があれば設定する
        利用する際は必ずoverrideして使用すること
        """

        if self.show_ui_frame:
            cmds.frameLayout(self.show_ui_frame, e=True, collapse=False)

    def show_ui_with_window(self, *args):
        """
        単体表示
        """

        # window単体表示の時は必ずFrameは畳まない
        self.is_use_frame_open_status = False

        self.window_name = '{}Window'.format(self.tool_name)
        self.window_title = '{0} ver {1}'.format(self.tool_label, self.tool_version)

        self.window = base_class.ui.window.Window(
            self.window_name,
            self.window_title
        )
        self.window.set_close_function(self.save_settings)

        cmds.columnLayout(adjustableColumn=True, p=self.window.ui_body_layout_id, width=300)

        self.show_ui()

        cmds.setParent('..')

        self.load_settings()

        self.window.show()

    def show_ui(self):
        """
        UI要素 入力必須項目
        """

        self.__initialze()

        # window単体表示の時はFrameを畳めないように
        self.show_ui_frame = cmds.frameLayout(
            l=self.tool_label, cll=self.is_use_frame_open_status, cl=0, bv=1, mw=5, mh=5
        )

        self.ui_body()

        cmds.setParent('..')

    def ui_body(self):
        """
        UI要素 ここにUIの中身を書いていく
        """

        pass

    def get_shelf_command_show_ui_with_window(self):
        """
        """

        return self.shelf_command_show_ui_with_window

    def get_tool_label(self):
        """
        """

        return self.tool_label

    def get_sub_shelf_command_param_list(self):
        """
        """

        return self.sub_shelf_command_param_list


class UtilityButton(base_class.ui.button.Button):

    def __init__(self, label, function=None, *on_function_arg, **button_edit_param):

        self.function = function
        self.function_arg = on_function_arg

        self.draw()

        if 'height' not in button_edit_param:
            button_edit_param['height'] = 20

        if button_edit_param:
            button_edit_param['edit'] = True
            self.apply_button_param(**button_edit_param)

        self.apply_button_param(e=True, label=label)

    def draw(self):

        self.ui_button_id = cmds.button(c=self.on_function)

    def on_function(self, value):

        if self.function is None:
            return

        if self.function_arg is None:
            self.function()
            return

        self.function(*self.function_arg)
