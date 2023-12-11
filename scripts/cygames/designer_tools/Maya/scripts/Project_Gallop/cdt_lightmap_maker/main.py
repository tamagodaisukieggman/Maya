# -*- coding: utf-8 -*-
from __future__ import absolute_import

try:
    # Maya 2022-
    from builtins import object
    from importlib import reload
except Exception:
    pass

import time
from multiprocessing import Process

import maya.cmds as cmds
import maya.mel as mel

import os
import shutil
import subprocess
import time

from .utility import common as util_common
from .utility import attribute
from .utility import colorset
from .utility import uvset
from .utility import fbx_exporter
from .utility import file
from .utility import batch_render
from .utility import vector

from .ui import common as ui_common
from .ui import window
from .ui import logframe
from .ui import label
from .ui import button
from .ui import icon_button
from .ui import dialog
from .ui import radio_button

from .bake import param_item
from .bake import param_item_group

from .bake import bake_common_setting
from .bake import bake_common_param_list as cp

from .bake import bake_setting_root
from .bake import bake_setting
from .bake import bake_setting_param_list

from .bake import bake_group_root
from .bake import bake_group
from .bake import bake_group_param_list

from .bake import bake_object_param_list
from .bake import bake_object_root
from .bake import bake_object

from .bake import bake_override_param
from .bake import bake_override_param_list

from . import export_object

from .utility import setting as cmn_utility_setting
from .utility import material as cmn_utility_material

from .bake import bake_export_object_param_list
from .bake import bake_export_object_root

from .bake import bake_visible_object_param_list
from .bake import bake_visible_object_root

reload(util_common)
reload(attribute)
reload(colorset)
reload(uvset)
reload(fbx_exporter)
reload(file)
reload(batch_render)
reload(vector)

reload(ui_common)
reload(window)
reload(logframe)
reload(label)
reload(button)
reload(icon_button)
reload(dialog)
reload(radio_button)

reload(param_item)
reload(param_item_group)

reload(cp)
reload(bake_common_setting)

reload(bake_setting_param_list)
reload(bake_setting_root)
reload(bake_setting)

reload(bake_group_param_list)
reload(bake_group_root)
reload(bake_group)

reload(bake_object_param_list)
reload(bake_object_root)
reload(bake_object)

reload(bake_override_param_list)
reload(bake_override_param)

reload(export_object)

reload(cmn_utility_setting)
reload(cmn_utility_material)

reload(bake_export_object_param_list)
reload(bake_export_object_root)

reload(bake_visible_object_param_list)
reload(bake_visible_object_root)


# ===========================================
def main():

    main = Main()
    main.create_ui()


# ===========================================
def batch():

    main = Main()
    main.batch()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Main(object):

    # ===========================================
    def __init__(self):

        self.version = '19040501'

        self.tool_name = 'LightMapMaker'
        self.tool_id = 'lmm'

        self.is_init = False

        self.script_file_path = None
        self.script_dir_path = None

        # name
        self.object_prefix = "LightMapMaker_"
        self.attr_prefix = self.tool_id + "_attr_"
        self.attr_nice_name_prefix = "lmm_"
        self.ui_prefix = self.tool_id + "_ui_"

        self.target_name = self.object_prefix + "Root"
        self.bake_common_setting_root_name = self.object_prefix + 'Common'
        self.bake_setting_root_name = self.object_prefix + "Setting"
        self.bake_group_root_name = self.object_prefix + "Group"

        self.target = ''

        # bake
        self.bake_common_setting = \
            bake_common_setting.BakeCommonSetting(self)

        self.bake_setting_root = None
        self.bake_group_root = None

        # UI
        self.ui_window = None
        self.ui_logframe = None

        self.ui_current_group_name = None
        self.ui_current_setting_name = None

        self.ui_current_selector = None
        self.ui_setting_selector_width = 200

        self.ui_header_root = None
        self.ui_header_main = None

        self.ui_center_root = None
        self.ui_center_main = None

        self.ui_footer_root = None
        self.ui_footer_main = None

        self.ui_radio_button = None
        self.ui_bake_setting = None
        self.ui_bake_group = None
        self.ui_bake_common_setting = None

        self.updating_ui = False

        # Setting
        self.setting = cmn_utility_setting.Setting(self.tool_name)

        self.setting_target_file_path_key = 'TargetFilePath'
        self.setting_target_file_path_value = None

        self.setting_export_model_key = 'ExportModel'
        self.setting_export_model_value = False

        self.setting_export_texture_key = 'ExportTexture'
        self.setting_export_texture_value = False

        self.setting_bake_texture_key = 'BakeTexture'
        self.setting_bake_texture_value = False

        self.setting_current_setting_index_key = 'CurrentSettingIndex'
        self.setting_current_setting_index_value = 0

        self.setting_current_group_index_key = 'CurrentGroupIndex'
        self.setting_current_group_index_value = 0

        self.batch_render_manager = None

    # ===========================================
    def initialize(self):

        self.is_init = False

        self.script_file_path = os.path.abspath(__file__)
        self.script_dir_path = os.path.dirname(self.script_file_path)

        maya_version = cmds.about(v=True)
        maya_build_date = cmds.about(d=True)

        self.batch_file_path = None
        if maya_version == '2015':
            self.batch_file_path = self.script_dir_path + \
                '/batch/mayabatch2015.bat'

        elif maya_version == '2016':
            self.batch_file_path = self.script_dir_path + \
                '/batch/mayabatch2016.bat'

        elif maya_version == '2017':
            self.batch_file_path = self.script_dir_path + \
                '/batch/mayabatch2017.bat'

        elif maya_version == '2018':
            self.batch_file_path = self.script_dir_path + \
                '/batch/mayabatch2018.bat'

        elif maya_version == '2019':
            self.batch_file_path = self.script_dir_path + \
                '/batch/mayabatch2019.bat'

        elif maya_version == '2022':
            self.batch_file_path = self.script_dir_path + \
                '/batch/mayabatch2022.bat'

        elif maya_version == '2024':
            self.batch_file_path = self.script_dir_path + \
                '/batch/mayabatch2024.bat'

        if self.batch_file_path is None or \
                not os.path.isfile(self.batch_file_path):
            cmds.warning(u'バッチファイルが見つからないので起動できません')
            return

        if not cmds.pluginInfo('fbxmaya', query=True, loaded=True):
            cmds.warning(u'FBXプラグインをロードしました')
            cmds.loadPlugin('fbxmaya.mll')

        if not cmds.pluginInfo('Turtle', query=True, loaded=True):
            cmds.warning(u'Turtleプラグインをロードしました')
            cmds.loadPlugin('Turtle.mll')

        self.load_turtle_renderer()

        if not util_common.NodeMethod.exist_transform(
                self.target_name):

            util_common.NodeMethod.create_group(
                self.target_name, None)

        self.target = '|' + self.target_name

        self.bake_common_setting.target_name = \
            self.bake_common_setting_root_name

        self.bake_common_setting.initialize()

        self.bake_setting_root = \
            bake_setting_root.BakeSettingRoot(self)

        self.bake_setting_root.target_name = self.bake_setting_root_name

        self.bake_setting_root.initialize()

        self.bake_group_root = \
            bake_group_root.BakeGroupRoot(self)

        self.bake_group_root.target_name = self.bake_group_root_name

        self.bake_group_root.initialize()

        self.batch_render_manager = batch_render.BatchRenderManager()

        self.is_init = True

    # ===========================================
    def create_ui(self):

        self.initialize()

        if not self.is_init:
            return

        self.ui_window = \
            window.Window(
                self.tool_name + 'Win',
                self.tool_name + ' ' + self.version,
                [600, 950])

        this_form = cmds.formLayout()

        self.ui_header_root = cmds.columnLayout(adj=True)
        self.ui_header_main = cmds.columnLayout(adj=True)
        cmds.setParent("..")
        cmds.separator(height=5, style='in')
        cmds.setParent("..")

        self.ui_center_root = cmds.scrollLayout(cr=True)
        self.ui_center_main = cmds.columnLayout(adj=True)
        cmds.setParent("..")
        cmds.setParent("..")

        self.ui_footer_root = cmds.columnLayout(adj=True)
        cmds.separator(height=5, style='in')
        self.ui_footer_main = cmds.columnLayout(adj=True)
        cmds.setParent("..")
        cmds.setParent("..")

        cmds.formLayout(
            this_form, e=True, attachForm=[self.ui_header_root, 'top', 0])
        cmds.formLayout(
            this_form, e=True, attachForm=[self.ui_header_root, 'left', 0])
        cmds.formLayout(
            this_form, e=True, attachForm=[self.ui_header_root, 'right', 0])

        cmds.formLayout(
            this_form, e=True, attachForm=[self.ui_footer_root, 'left', 0])
        cmds.formLayout(
            this_form, e=True, attachForm=[self.ui_footer_root, 'right', 0])
        cmds.formLayout(
            this_form, e=True, attachForm=[self.ui_footer_root, 'bottom', 0])

        cmds.formLayout(
            this_form, e=True, attachForm=[self.ui_center_root, 'left', 0])
        cmds.formLayout(
            this_form, e=True, attachForm=[self.ui_center_root, 'right', 0])

        cmds.formLayout(
            this_form, e=True,
            attachControl=[
                self.ui_center_root, 'top', 0, self.ui_header_root])

        cmds.formLayout(
            this_form, e=True,
            attachControl=[
                self.ui_center_root, 'bottom', 0, self.ui_footer_root])

        self.create_ui_main()

        self.bake_common_setting.create_ui_later()
        self.bake_setting_root.create_ui_later()
        self.bake_group_root.create_ui_later()

        self.change_tab_index(cp.main_tab_bake_setting)

        self.load_current()

        self.ui_window.show()

        self.update_ui()

    # ===========================================
    def create_ui_main(self):

        # Header
        cmds.columnLayout(adjustableColumn=True, p=self.ui_header_main)

        self.create_header_ui()
        self.create_current_selector_ui()

        cmds.separator(height=20, style='in')

        self.ui_radio_button = radio_button.RadioButton(
            cp.main_tab_label_list, self.change_tab_index)
        self.ui_radio_button.set_size([100, None])

        cmds.setParent("..")

        # Center
        cmds.columnLayout(adj=True, p=self.ui_center_main)

        self.ui_bake_common_setting = \
            cmds.columnLayout(adj=True, vis=False)
        cmds.setParent("..")

        self.ui_bake_setting = \
            cmds.columnLayout(adj=True, vis=False)
        cmds.setParent("..")

        self.ui_bake_group = \
            cmds.columnLayout(adj=True, vis=False)
        cmds.setParent("..")

        cmds.setParent("..")

        self.create_common_setting_ui()
        self.create_bake_setting_ui()
        self.create_bake_group_ui()

    # ===========================================
    def create_header_ui(self):

        icon_size = (30, 30)

        cmds.frameLayout(l='Bake', cll=1, cl=0, bv=0, mw=5, mh=5, lv=0)
        cmds.columnLayout(adjustableColumn=True)

        cmds.flowLayout(columnSpacing=2)

        icon_button.IconButton(
            'menuIconRender.png',
            'Bake',
            u'選択中のグループをベイク',
            icon_size,
            cp.bg_warn_color0,
            self.bake_scene,
            (cp.bake_scene_setting_current,
             cp.bake_scene_group_current,
             cp.bake_quality_product)
        )

        icon_button.IconButton(
            'menuIconRender.png',
            'Test',
            u'選択中のグループをテストベイク',
            icon_size,
            cp.bg_safe_color0,
            self.bake_scene,
            (cp.bake_scene_setting_current,
             cp.bake_scene_group_current,
             cp.bake_quality_test)
        )

        icon_button.IconButton(
            'openBar.png', None, None, (10, icon_size[1]))

        icon_button.IconButton(
            'menuIconRender.png',
            'Bake',
            u'選択中の設定で全てのグループをベイク',
            icon_size,
            cp.bg_warn_color1,
            self.bake_scene,
            (cp.bake_scene_setting_current,
             cp.bake_scene_group_all,
             cp.bake_quality_product)
        )

        icon_button.IconButton(
            'menuIconRender.png',
            'Test',
            u'選択中の設定で全てのグループをテストベイク',
            icon_size,
            cp.bg_safe_color1,
            self.bake_scene,
            (cp.bake_scene_setting_current,
             cp.bake_scene_group_all,
             cp.bake_quality_test)
        )

        icon_button.IconButton(
            'openBar.png', None, None, (10, icon_size[1]))

        icon_button.IconButton(
            'render_lambert.png',
            None,
            u'オリジナルマテリアルに変更',
            icon_size,
            None,
            self.change_material,
            cp.material_reset_original
        )

        icon_button.IconButton(
            'render_phong.png',
            None,
            u'ライトマップマテリアルに変更',
            icon_size,
            None,
            self.change_material,
            cp.material_reset_bake_with_lightmap
        )

        icon_button.IconButton(
            'render_phong.png',
            None,
            u'頂点カラーを再計算してライトマップマテリアルに変更',
            icon_size,
            (0.7, 0.5, 0.5),
            self.change_material,
            cp.material_reset_bake_with_lightmap_and_calc_vertex_color
        )

        icon_button.IconButton(
            'openBar.png', None, None, (10, icon_size[1]))

        icon_button.IconButton(
            'rvRender.png',
            None,
            u'シーンをレンダリング',
            icon_size,
            None,
            self.render_scene
        )

        icon_button.IconButton(
            'rvRenderGlobals.png',
            None,
            u'レンダー設定を開く',
            icon_size,
            None,
            self.view_render_setting
        )

        icon_button.IconButton(
            'openBar.png', None, None, (10, icon_size[1]))

        icon_button.IconButton(
            'polySphere.png',
            None,
            u'選択中グループの共通乗算頂点カラーを編集',
            icon_size,
            (0.5, 0.5, 0.6),
            self.set_common_colorset_from_ui,
            cp.colorset_common_multiply
        )

        icon_button.IconButton(
            'polySphere.png',
            None,
            u'選択中グループの共通加算頂点カラーを編集',
            icon_size,
            (0.6, 0.5, 0.5),
            self.set_common_colorset_from_ui,
            cp.colorset_common_add
        )

        icon_button.IconButton(
            'polySphere.png',
            None,
            u'選択中グループの共通オーバーレイ頂点カラーを編集',
            icon_size,
            (0.5, 0.6, 0.5),
            self.set_common_colorset_from_ui,
            cp.colorset_common_overlay
        )

        icon_button.IconButton(
            'polySphere.png',
            None,
            u'選択中グループの共通頂点アルファを編集',
            icon_size,
            (0.5, 0.5, 0.5),
            self.set_common_colorset_from_ui,
            cp.colorset_common_alpha
        )

        icon_button.IconButton(
            'openBar.png', None, None, (10, icon_size[1]))

        icon_button.IconButton(
            'timeplay.png',
            None,
            u'選択中の設定のオブジェクトをFBXで出力',
            icon_size,
            (0.6, 0.5, 0.5),
            self.export_object,
            None
        )

        icon_button.IconButton(
            'timeplay.png',
            None,
            u'選択中の設定の統合したテクスチャを出力',
            icon_size,
            (0.5, 0.6, 0.5),
            self.export_texture,
            None
        )

        cmds.setParent('..')

        cmds.separator(height=10, style='in')

        cmds.setParent('..')
        cmds.setParent('..')

    # ===========================================
    def create_current_selector_ui(self):

        self.ui_current_selector = cmds.rowLayout(
            nc=2, adj=2, cw2=[self.ui_setting_selector_width, 100])
        cmds.setParent('..')

        self.bake_setting_root.create_selector_ui()
        self.bake_group_root.create_selector_ui()

        cmds.setParent('..')

    # ===========================================
    def create_common_setting_ui(self):

        cmds.columnLayout(adj=True, p=self.ui_bake_common_setting)

        self.bake_common_setting.create_ui()

        cmds.setParent("..")

    # ===========================================
    def create_bake_setting_ui(self):

        cmds.columnLayout(adj=True, p=self.ui_bake_setting)

        self.bake_setting_root.create_ui()

        cmds.setParent("..")

    # ===========================================
    def create_bake_group_ui(self):

        cmds.columnLayout(adj=True, p=self.ui_bake_group)

        self.bake_group_root.create_ui()

        cmds.setParent("..")

    # ===========================================
    def update_ui(self):

        self.updating_ui = True

        self.bake_common_setting.update_ui()
        self.bake_setting_root.update_ui()
        self.bake_group_root.update_ui()

        self.updating_ui = False

    # ===========================================
    def change_ui(self):

        if self.updating_ui:
            return

        self.bake_common_setting.change_ui()
        self.bake_setting_root.change_ui()
        self.bake_group_root.change_ui()

        self.update_ui()

    # ===========================================
    def change_tab_index(self, index):

        cmds.columnLayout(
            self.ui_bake_common_setting, e=True, vis=False)

        cmds.columnLayout(
            self.ui_bake_setting, e=True, vis=False)

        cmds.columnLayout(
            self.ui_bake_group, e=True, vis=False)

        if index == cp.main_tab_bake_setting:
            cmds.columnLayout(
                self.ui_bake_setting, e=True, vis=True)

        elif index == cp.main_tab_bake_group:
            cmds.columnLayout(
                self.ui_bake_group, e=True, vis=True)

        elif index == cp.main_tab_common_setting:
            cmds.columnLayout(
                self.ui_bake_common_setting, e=True, vis=True)

        self.ui_radio_button.set_current_index(index)

    # ===========================================
    def bake_scene(self, arg):

        cmds.setAttr("TurtleRenderOptions.renderer", 1)

        bake_scene_setting_type = arg[0]
        bake_scene_group_type = arg[1]
        self.bake_setting_root.bake_quality_type = arg[2]

        target_setting_list = []

        if bake_scene_setting_type == cp.bake_scene_setting_current:
            target_setting_list.append(self.bake_setting_root.current_index)
        elif bake_scene_setting_type == cp.bake_scene_setting_all:
            target_setting_list = []

        target_group_list = []

        if bake_scene_group_type == cp.bake_scene_group_current:
            target_group_list.append(self.bake_group_root.current_index)
        elif bake_scene_group_type == cp.bake_scene_group_all:
            target_group_list = []

        temp_dir_path = os.path.dirname(cmds.file(q=True, sn=True)) + '/temp'

        if not os.path.isdir(temp_dir_path):
            os.makedirs(temp_dir_path)

        self.batch_render_manager.clear_all_target()
        self.batch_render_manager.root_dir_path = temp_dir_path
        self.batch_render_manager.delete_file_after_render = True

        self.bake_setting_root.bake_scene(
            target_setting_list,
            target_group_list
        )

        self.batch_render_manager.execute_batch_render()

    # ===========================================
    def change_material(self, arg):

        self.bake_setting_root.reset_material_and_object(arg)

    # ===========================================
    def render_scene(self):

        self.bake_setting_root.reset_material_and_object(
            cp.material_reset_original)

        cmds.setAttr("TurtleRenderOptions.renderer", 0)

        mel.eval("RenderIntoNewWindow;")

    # ===========================================
    def view_render_setting(self):

        self.bake_setting_root.reset_material_and_object(
            cp.material_reset_original
        )

        mel.eval("unifiedRenderGlobalsWindow;")
        mel.eval("ilrUpdateBakingTab;")

    # ===========================================
    def load_turtle_renderer(self):

        current_renderer = attribute.Method.get_attr(
            'defaultRenderGlobals', 'currentRenderer', 'string'
        )

        if current_renderer == 'turtle':
            return

        attribute.Method.set_attr(
            'defaultRenderGlobals',
            'currentRenderer', 'string', 'turtle'
        )

        mel.eval('rendererChanged;')

        cmds.warning(u'レンダラ―をTurtleに設定しました')

    # ===========================================
    def set_common_colorset_from_ui(self, colorset_type):

        self.bake_group_root.set_colorset_all(colorset_type)

    # ===========================================
    def export_object(self):

        if not dialog.open_yes_no(
                u'確認', u'選択中の設定のオブジェクトをFBXで出力しますか？',
                self.ui_window.ui_id):
            return

        temp_file_path = \
            file.create_temp_file_from_current_file(
                'lmm_', '_export_obj', 'temp')

        if temp_file_path is None:
            return

        self.reset_batch_setting()

        self.setting_target_file_path_value = temp_file_path

        self.setting_export_model_value = True

        self.setting_current_setting_index_value = self.bake_setting_root.current_index

        self.setting_current_group_index_value = self.bake_group_root.current_index

        self.save_batch_setting()

        subprocess.Popen(self.batch_file_path)

    # ===========================================
    def export_texture(self):

        if not dialog.open_yes_no(
                u'確認', u'選択中の設定の統合したテクスチャを出力しますか？',
                self.ui_window.ui_id):
            return

        temp_file_path = \
            file.create_temp_file_from_current_file(
                'lmm_', '_export_tex', 'temp')

        if temp_file_path is None:
            return

        self.reset_batch_setting()

        self.setting_target_file_path_value = temp_file_path

        self.setting_export_texture_value = True

        self.setting_current_setting_index_value = self.bake_setting_root.current_index

        self.setting_current_group_index_value = self.bake_group_root.current_index

        self.save_batch_setting()

        subprocess.Popen(self.batch_file_path)

    # ===========================================
    def reset_batch_setting(self):

        self.setting_target_file_path_value = ''
        self.setting_export_model_value = False
        self.setting_export_texture_value = False
        self.setting_bake_texture_value = False

        self.setting_current_setting_index_value = 0
        self.setting_current_group_index_value = 0

        self.save_batch_setting()

    # ===========================================
    def save_batch_setting(self):

        self.setting.save(
            self.setting_target_file_path_key,
            self.setting_target_file_path_value
        )

        self.setting.save(
            self.setting_export_model_key,
            self.setting_export_model_value
        )

        self.setting.save(
            self.setting_export_texture_key,
            self.setting_export_texture_value
        )

        self.setting.save(
            self.setting_bake_texture_key,
            self.setting_bake_texture_value
        )

        self.setting.save(
            self.setting_current_setting_index_key,
            self.setting_current_setting_index_value
        )

        self.setting.save(
            self.setting_current_group_index_key,
            self.setting_current_group_index_value
        )

    # ===========================================
    def load_batch_setting(self):

        self.setting_target_file_path_value = self.setting.load(
            self.setting_target_file_path_key)

        self.setting_export_model_value = self.setting.load(
            self.setting_export_model_key, 'bool')

        self.setting_export_texture_value = self.setting.load(
            self.setting_export_texture_key, 'bool')

        self.setting_bake_texture_value = self.setting.load(
            self.setting_bake_texture_key, 'bool')

        self.setting_current_setting_index_value = self.setting.load(
            self.setting_current_setting_index_key, 'int')

        self.setting_current_group_index_value = self.setting.load(
            self.setting_current_setting_index_key, 'int')

    # ===========================================
    def batch(self):

        self.initialize()

        if not self.is_init:
            return

        self.load_batch_setting()

        if not os.path.isfile(self.setting_target_file_path_value):
            return

        # 一時ファイル作成
        temp_file_path = self.setting_target_file_path_value

        if temp_file_path is None:
            return

        if not os.path.isfile(temp_file_path):
            return

        cmds.file(
            temp_file_path,
            open=True,
            force=True,
            options="v=1;",
            ignoreVersion=True)

        # ツールのリブート
        self.initialize()

        if not self.is_init:
            return

        # 対象ターゲットの取得
        setting_index_list = []
        if self.setting_current_setting_index_value >= 0:
            setting_index_list.append(self.setting_current_setting_index_value)

        group_index_list = []
        if self.setting_current_group_index_value >= 0:
            group_index_list.append(self.setting_current_group_index_value)

        if self.setting_export_model_value:
            # モデルエクスポート

            self.bake_setting_root.export_object(setting_index_list)

        elif self.setting_export_texture_value:
            # テクスチャエクスポート

            self.bake_setting_root.export_composite_texture(setting_index_list)

        elif self.setting_bake_texture_value:
            # テクスチャベイク
            pass

        cmds.file(save=True)

        if os.path.isfile(temp_file_path):
            os.remove(temp_file_path)

    # ===========================================
    def load_current(self):

        current_setting_index = self.bake_common_setting.param_item_group.get_attr_value(
            cp.get_name(cp.current_setting_index)
        )

        current_group_index = self.bake_common_setting.param_item_group.get_attr_value(
            cp.get_name(cp.current_group_index)
        )

        self.bake_setting_root.current_index = current_setting_index
        self.bake_group_root.current_index = current_group_index

        self.bake_setting_root.change_current_index()

        self.update_ui()

    # ===========================================
    def save_current(self):

        self.bake_common_setting.param_item_group.set_attr_value(
            cp.get_name(cp.current_setting_index),
            self.bake_setting_root.current_index
        )

        self.bake_common_setting.param_item_group.set_attr_value(
            cp.get_name(cp.current_group_index),
            self.bake_group_root.current_index
        )
