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
import re

import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om

from .. import base_common
from ..base_common import classes as base_class
from ..base_common import utility as base_utility

from ..glp_common.classes.info import chara_info

from . import target_info
from . import target_controller_info

from . import blend_target_info

from . import facial_rig_head_attach
from . import facial_copy_info
from . import facial_target_exporter
from . import eye_controller_creator
from . import facial_target_renderer

from . import ear_target_exporter
from . import ear_target_renderer
from . import ear_controller_creator

from . import cheek_driven_key_creator
from . import eye_driven_key_creator
from . import facial_ctrl_rig_creator

from . import facial_mirror_transform

from . import facial_tear_attach
from . import facial_tear_anim_controller

from . import facial_blend_viewer

reload(base_common)

reload(chara_info)

reload(target_info)
reload(target_controller_info)

reload(blend_target_info)

reload(facial_rig_head_attach)
reload(facial_copy_info)
reload(facial_target_exporter)
reload(eye_controller_creator)
reload(facial_target_renderer)

reload(ear_target_exporter)
reload(ear_target_renderer)
reload(ear_controller_creator)

reload(cheek_driven_key_creator)
reload(eye_driven_key_creator)
reload(facial_ctrl_rig_creator)

reload(facial_mirror_transform)

reload(facial_tear_attach)
reload(facial_tear_anim_controller)

reload(facial_blend_viewer)

# ツールマニュアルページ
# https://wisdom.cygames.jp/pages/viewpage.action?pageId=364265323#GallopCharaFaicialTool:キャラフェイシャルツール

# ===============================================


def main():

    this_main = Main()
    this_main.create_ui()


# ===============================================
def batch(command_type):

    this_main = Main()

    if command_type == '':
        this_main.batch_export_ear_target()

    elif command_type == 'export_facial_target':
        this_main.batch_export_facial_target()

    elif command_type == 'create_facial_blend_target':
        this_main.batch_create_facial_blend_target()

    elif command_type == 'render_facial_target':
        this_main.batch_render_facial_target()

    elif command_type == 'render_face_type':
        this_main.batch_render_face_type()

    elif command_type == 'recreate_ear_target_rig_ma':
        this_main.batch_recreate_ear_target_rig_ma()

    elif command_type == 'create_ear_target_rig_ma':
        this_main.batch_create_ear_target_rig_ma()

    elif command_type == 'export_ear_target':
        this_main.batch_export_ear_target()

    elif command_type == 'render_ear_target':
        this_main.batch_render_ear_target()

    elif command_type == 'update_ctrl_rig':
        this_main.batch_update_ctrl_rig()


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Main(object):

    # ==================================================
    def __init__(self):

        self.tool_version = '23121401'
        self.tool_name = 'GallopFacialTool'

        self.window_name = self.tool_name + 'Win'

        self.manual_url = 'https://wisdom.cygames.jp/pages/viewpage.action?pageId=364265323#GallopCharaFaicialTool:キャラフェイシャルツール'

        # スクリプトのパス関連
        self.script_file_path = os.path.abspath(__file__)
        self.script_dir_path = os.path.dirname(self.script_file_path)

        # 設定関連
        self.setting = base_class.setting.Setting(self.tool_name)

        # UI関連
        self.ui_show_in_explorer = None
        self.ui_keep_temp_file = None
        self.ui_is_ascii = None

        self.ui_root_layout = None

        self.ui_export_facial_target_selector = None
        self.ui_create_facial_blend_target_selector = None

        self.ui_recreate_ear_target_rig_selector = None
        self.ui_create_ear_target_rig_selector = None
        self.ui_export_ear_target_selector = None
        self.ui_render_ear_target_selector = None

        self.ui_update_ctrl_rig_selector = None
        self.ui_update_ctrl_rig_state_list = None
        self.ui_update_ctrl_rig_target_list = None
        self.ui_update_ctrl_rig_state_filter_list = None

        self.previous_facial_view_info_items = None
        self.current_facial_view_info_items = None

        self.ui_previous_facial_view_scroll_list = None
        self.ui_current_facial_view_scroll_list = None

        self.base_frame = 0
        self.previous_frame = None
        self.current_frame = None

        self.category = None

        self.ctrl_rig_state_list = None
        self.ctrl_rig_target_list = None

        # 初期化フラグ
        self.init = False

        # クラス
        self.facial_copy_info = None

        self.facial_blend_viewer = None

        self.initialize()

    # ==================================================
    def initialize(self):

        if not cmds.pluginInfo('fbxmaya', query=True, loaded=True):
            cmds.warning(u'FBXプラグインをロードしました')
            cmds.loadPlugin('fbxmaya.mll')

        self.update_category()

    def update_category(self):

        this_file_path = cmds.file(q=True, sn=True, exn=True)

        if this_file_path.endswith('_facial_target.ma'):
            self.category = 'facial'
        elif this_file_path.endswith('_ear_target.ma'):
            self.category = 'ear'
        else:
            self.category = None

# region UI作成

    # ==================================================
    def create_ui(self):

        # メニューアイテム
        self.menu_list = [
            {
                'label': 'Help',
                'item_param_list': [
                    {'label': 'マニュアル', 'command': self.show_manual},
                ]
            }
        ]
        # (self, ui_window_id, title, tab_list=None, menu_list=[], **window_edit_param)
        self.ui_window = base_class.ui.window.Window(
            self.window_name,
            self.tool_name + '  ' + self.tool_version,
            menu_list=self.menu_list,
            width=600, height=500
        )

        self.ui_window.set_close_function(self.save_setting)

        self.ui_root_layout = \
            base_class.ui.multi_frame_layout.MultiFrameLayout(
                '',
                False,
                [

                    {
                        'key': 'FacailTargetTool',
                        'label': 'フェイシャルターゲット系ツール',
                        'color': [0.3, 0.5, 0.3]
                    },

                    {
                        'key': 'FacialEditTool',
                        'label': '編集ツール',
                        'close': True,
                        'parent': 'FacailTargetTool',
                        'color': [0.3, 0.475, 0.3]
                    },

                    {
                        'key': 'FacialViewTool',
                        'label': '確認ツール',
                        'close': True,
                        'parent': 'FacailTargetTool',
                        'color': [0.3, 0.45, 0.3]
                    },

                    {
                        'key': 'FacialViewToolEyebrow',
                        'label': '眉',
                        'close': True,
                        'parent': 'FacialViewTool',
                        'color': [0.3, 0.3, 0.5]
                    },

                    {
                        'key': 'FacialViewToolEye',
                        'label': '目',
                        'close': True,
                        'parent': 'FacialViewTool',
                        'color': [0.3, 0.3, 0.5]
                    },

                    {
                        'key': 'FacialViewToolMouth',
                        'label': '口',
                        'close': True,
                        'parent': 'FacialViewTool',
                        'color': [0.3, 0.3, 0.5]
                    },

                    {
                        'key': 'FacialTarget',
                        'label': 'facial_target.fbxエクスポート',
                        'close': True,
                        'parent': 'FacailTargetTool',
                        'color': [0.3, 0.425, 0.3]
                    },

                    {
                        'key': 'FacialBlendTarget',
                        'label': 'facial_blend_target.maの作成',
                        'close': True,
                        'parent': 'FacailTargetTool',
                        'color': [0.3, 0.4, 0.3]
                    },

                    {
                        'key': 'RenderFacialTarget',
                        'label': 'facial_targetのレンダリング',
                        'close': True,
                        'parent': 'FacailTargetTool',
                        'color': [0.3, 0.4, 0.3]
                    },

                    {
                        'key': 'EarTargetTool',
                        'label': '耳ターゲット系ツール',
                        'color': [0.3, 0.3, 0.5],
                    },

                    {
                        'key': 'EarTargetEditTool',
                        'label': '編集ツール',
                        'close': True,
                        'parent': 'EarTargetTool',
                        'color': [0.3, 0.3, 0.475],
                    },

                    {
                        'key': 'EarViewTool',
                        'label': '確認ツール',
                        'close': True,
                        'parent': 'EarTargetTool',
                        'color': [0.3, 0.3, 0.45]
                    },

                    {
                        'key': 'FacialViewToolEar',
                        'label': '耳',
                        'close': True,
                        'parent': 'EarViewTool',
                        'color': [0.3, 0.3, 0.5]
                    },

                    {
                        'key': 'ExportEarTarget',
                        'label': 'ear_target.fbxエクスポート',
                        'close': True,
                        'parent': 'EarTargetTool',
                        'color': [0.3, 0.3, 0.425],
                    },

                    {
                        'key': 'RenderEarTarget',
                        'label': 'ear_targetのレンダリング',
                        'close': True,
                        'parent': 'EarTargetTool',
                        'color': [0.3, 0.3, 0.4],
                    },

                    {
                        'key': 'MotionTool',
                        'label': 'モーション系ツール',
                        'color': [0.5, 0.3, 0.3],
                    },

                    {
                        'key': 'UpdateCtrlRig',
                        'label': '_Ctrl_RIG.maの作成・更新',
                        'close': True,
                        'parent': 'MotionTool',
                        'color': [0.475, 0.3, 0.3],
                    },

                    {
                        'key': 'CommonSetting',
                        'label': '共通設定',
                        'color': [0.5, 0.5, 0.3],
                    },
                ],
                bv=False,
                mw=2,
                mh=2)

        cmds.frameLayout(
            self.ui_root_layout.ui_layout_id,
            e=True, parent=self.ui_window.ui_body_layout_id)

        # ------- フェイシャルターゲット系ツール ------
        # 編集ツール
        self.create_facial_editor_ui()

        self.create_change_frame_ui()
        self.create_facial_copy_ui()
        self.create_facial_mirror_ui()

        # 確認ツール
        self.create_facial_view_ui(self.category)

        self.create_export_facial_target_ui()
        self.create_create_facial_blend_ui()
        self.create_render_facial_target_ui()

        # ------- 耳ターゲット系ツール ------
        self.create_ear_target_editor_ui()
        self.create_export_ear_target_ui()
        self.create_render_ear_target_ui()

        # ------- モーション系ツール ------
        self.create_update_ctrl_rig_ui()

        # ------- 共通設定 ------
        self.create_common_setting_ui()

        self.set_scene_opened_script_job()

        self.load_setting()

        self.ui_window.show()

    # ==================================================
    def create_facial_editor_ui(self):

        this_column = cmds.columnLayout(adj=True, rs=4)

        base_class.ui.button.Button(
            'Head_Rigのジョイントのアタッチ',
            self.attach_rig_head_from_ui)

        base_class.ui.button.Button(
            'Head_Rigのジョイントをデタッチ',
            self.detach_rig_head_from_ui)

        base_class.ui.button.Button(
            'Head_Rigのコントローラをリセット',
            self.reset_rig_head_from_ui)

        base_class.ui.button.Button(
            '目のハイライトリグを作成・更新',
            self.create_eye_high_rig_from_ui)

        base_class.ui.button.Button(
            'リファレンス先を最適化',
            self.fix_reference_from_ui)

        cmds.setParent('..')

        cmds.columnLayout(
            this_column,
            e=True,
            parent=self.ui_root_layout.ui_lower_layout_id_dict['FacialEditTool'])

    # ==================================================
    def create_change_frame_ui(self):

        this_frame = base_class.ui.frame_layout.FrameLayout(
            'フレーム変更ツール', False)

        this_column = cmds.columnLayout(adj=True, rs=4)

        btn_width = 60
        label_width = 70

        cmds.rowLayout(
            nc=7, cw=(label_width, btn_width))

        base_class.ui.button.Button(
            '0~', self.switch_facial_timeline, 0, width=btn_width)

        base_class.ui.button.Button(
            '100~', self.switch_facial_timeline, 100, width=btn_width)

        base_class.ui.button.Button(
            '200~', self.switch_facial_timeline, 200, width=btn_width)

        base_class.ui.button.Button(
            '300~', self.switch_facial_timeline, 300, width=btn_width)

        base_class.ui.button.Button(
            '400~', self.switch_facial_timeline, 400, width=btn_width)

        base_class.ui.button.Button(
            '1000~', self.switch_facial_timeline, 1000, width=btn_width)

        base_class.ui.button.Button(
            '1100~', self.switch_facial_timeline, 1100, width=btn_width)

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.columnLayout(
            this_column, e=True, parent=this_frame.ui_layout_id)

        cmds.frameLayout(
            this_frame.ui_layout_id,
            e=True,
            parent=self.ui_root_layout.ui_lower_layout_id_dict['FacialEditTool'])

    # ==================================================
    def create_facial_copy_ui(self):

        this_frame = base_class.ui.frame_layout.FrameLayout(
            'フェイシャルコピーツール', False)

        this_column = cmds.columnLayout(adj=True, rs=4)

        cmds.rowLayout(nc=9)

        base_class.ui.button.Button(
            'コピー',
            self.copy_facial_key_from_ui, width=100)

        btn_width = 40

        base_class.ui.button.Button(
            '全て',
            self.paste_facial_key_from_ui, [True, True, True, True, True],
            width=btn_width)

        base_class.ui.button.Button(
            '両眉',
            self.paste_facial_key_from_ui, [True, True, False, False, False],
            width=btn_width)

        base_class.ui.button.Button(
            '両目',
            self.paste_facial_key_from_ui, [False, False, True, True, False],
            width=btn_width)

        base_class.ui.button.Button(
            '口',
            self.paste_facial_key_from_ui, [False, False, False, False, True],
            width=btn_width)

        base_class.ui.button.Button(
            '左眉',
            self.paste_facial_key_from_ui, [True, False, False, False, False],
            width=btn_width)

        base_class.ui.button.Button(
            '右眉',
            self.paste_facial_key_from_ui, [False, True, False, False, False],
            width=btn_width)

        base_class.ui.button.Button(
            '左目',
            self.paste_facial_key_from_ui, [False, False, True, False, False],
            width=btn_width)

        base_class.ui.button.Button(
            '右目',
            self.paste_facial_key_from_ui, [False, False, False, True, False],
            width=btn_width)

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.columnLayout(
            this_column, e=True, parent=this_frame.ui_layout_id)

        cmds.frameLayout(
            this_frame.ui_layout_id,
            e=True,
            parent=self.ui_root_layout.ui_lower_layout_id_dict['FacialEditTool'])

    # ==================================================
    def create_facial_mirror_ui(self):

        this_frame = base_class.ui.frame_layout.FrameLayout(
            'フェイシャルミラーツール', False)

        this_column = cmds.columnLayout(adj=True, rs=4)

        base_class.ui.button.Button(
            '選択を左右ミラーコピー',
            self.mirror_facial_rig_from_ui)

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.columnLayout(
            this_column, e=True, parent=this_frame.ui_layout_id)

        cmds.frameLayout(
            this_frame.ui_layout_id,
            e=True,
            parent=self.ui_root_layout.ui_lower_layout_id_dict['FacialEditTool'])

    # ==================================================
    def create_export_facial_target_ui(self):

        this_column = cmds.columnLayout(adj=True, rs=4)

        base_class.ui.button.Button(
            '_facial_target.fbxを出力', self.export_facial_target_from_ui, False)

        cmds.frameLayout(label='バッチ', cll=True, bv=True, cl=True, mw=10, mh=10)
        cmds.columnLayout(adj=True, rs=4)

        self.ui_export_facial_target_selector = \
            base_class.ui.data_selector.DataSelector(
                'フォルダ', '', False, True)
        self.ui_export_facial_target_selector.set_path(
            'W:/gallop/svn/svn_gallop/80_3D/01_character/01_model/head')

        self.ui_export_facial_target_selector.set_file_filter(
            '_facial_target', 'temp')
        self.ui_export_facial_target_selector.set_extension_filter('.ma')
        self.ui_export_facial_target_selector.set_contain_lower(True)

        base_class.ui.button.Button(
            '_facial_target.fbxをバッチ出力',
            self.export_facial_target_from_ui, True)

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.setParent('..')

        cmds.columnLayout(
            this_column,
            e=True,
            parent=self.ui_root_layout.ui_lower_layout_id_dict['FacialTarget'])

    # ==================================================
    def create_create_facial_blend_ui(self):
        """
        facial_blend_target.maの作成
        """
        this_column = cmds.columnLayout(adj=True, rs=4)

        base_class.ui.button.Button(
            '_facial_blend_target.maを出力',
            self.create_facial_blend_target_from_ui, False)

        cmds.frameLayout(label='バッチ', cll=True, bv=True, cl=True, mw=10, mh=10)
        cmds.columnLayout(adj=True, rs=4)

        self.ui_create_facial_blend_target_selector = \
            base_class.ui.data_selector.DataSelector(
                'フォルダ', '', False, True)
        self.ui_create_facial_blend_target_selector.set_path(
            'W:/gallop/svn/svn_gallop/80_3D/01_character/01_model/head')

        self.ui_create_facial_blend_target_selector.set_file_filter(
            '_facial_target', 'temp')
        self.ui_create_facial_blend_target_selector.set_extension_filter('.ma')
        self.ui_create_facial_blend_target_selector.set_contain_lower(True)

        base_class.ui.button.Button(
            '_facial_blend_target.maをバッチ出力',
            self.create_facial_blend_target_from_ui, True)

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.setParent('..')

        cmds.columnLayout(
            this_column,
            e=True,
            parent=self.ui_root_layout.ui_lower_layout_id_dict['FacialBlendTarget'])

    # ==================================================
    def create_facial_view_ui(self, category):
        """
        フェイシャルターゲット系ツール/確認ツール
        """

        this_category = category
        target_info_csv_name = None
        controller_info_csv_name = None
        view_info_list = []
        parent_ui_name = None

        # UIのリセット
        reset_layouts = ['FacialViewTool', 'FacialViewToolEyebrow', 'FacialViewToolEye', 'FacialViewToolMouth', 'EarViewTool', 'FacialViewToolEar']

        for reset_layout in reset_layouts:
            reset_layout_name = self.ui_root_layout.ui_lower_layout_id_dict.get(reset_layout, '')

            if not cmds.layout(reset_layout_name, ex=True):
                continue

            layout_children = cmds.layout(reset_layout_name, q=True, ca=True) or []

            for layout_child in layout_children:

                if layout_child in self.ui_root_layout.ui_lower_layout_id_dict.values():
                    continue

                cmds.deleteUI(layout_child)

        # フェイシャルターゲット系ツール/確認ツール/眉、目、口
        # 現在開いているシーンが xxx_facial_target.ma でないとUIの中身は表示されない
        if this_category == 'facial':

            target_info_csv_name = 'facial_target_info'
            controller_info_csv_name = 'facial_controller_info'
            view_info_list = [
                {'title': '眉', 'part': 'Eyebrow_L', 'parent': 'FacialViewToolEyebrow'},
                {'title': '目', 'part': 'Eye_L', 'parent': 'FacialViewToolEye'},
                {'title': '口', 'part': 'Mouth', 'parent': 'FacialViewToolMouth'},
            ]
            parent_ui_name = 'FacialViewTool'
            # 耳ターゲット系ツール/確認ツール/耳 の方にUIが表示されない説明
            cmds.columnLayout(
                adj=True, rs=4, parent=self.ui_root_layout.ui_lower_layout_id_dict['EarViewTool'])
            cmds.text(
                l='mdl_xxx_ear_target のシーンを開くとUIが表示されます', align='left')

        # 耳ターゲット系ツール/確認ツール/耳
        # 現在開いているシーンが xxx_ear_target.ma でないとUIの中身は表示されない
        elif this_category == 'ear':

            target_info_csv_name = 'ear_target_info'
            controller_info_csv_name = 'ear_controller_info'
            view_info_list = [
                {'title': '耳', 'part': 'Ear_L', 'parent': 'FacialViewToolEar'},
            ]
            parent_ui_name = 'EarViewTool'
            # フェイシャルターゲット系ツール/確認ツール/眉、目、口 の方にUIが表示されない説明
            cmds.columnLayout(
                adj=True, rs=4, parent=self.ui_root_layout.ui_lower_layout_id_dict['FacialViewTool'])
            cmds.text(
                l='mdl_xxx_facial_target のシーンを開くとUIが表示されます', align='left')
        else:
            # フェイシャルターゲット系ツール/確認ツール/眉、目、口 の方にUIが表示されない説明
            cmds.columnLayout(
                adj=True, rs=4, parent=self.ui_root_layout.ui_lower_layout_id_dict['FacialViewTool'])
            cmds.text(
                l='mdl_xxx_facial_target のシーンを開くとUIが表示されます', align='left')
            # 耳ターゲット系ツール/確認ツール/耳 の方にUIが表示されない説明
            cmds.columnLayout(
                adj=True, rs=4, parent=self.ui_root_layout.ui_lower_layout_id_dict['EarViewTool'])
            cmds.text(
                l='mdl_xxx_ear_target のシーンを開くとUIが表示されます', align='left')

        this_target_info = target_info.TargetInfo()

        this_target_info.create_info_from_csv(
            target_info_csv_name, controller_info_csv_name)

        if not this_target_info.info_item_list:
            return

        this_column = cmds.columnLayout(adj=True, rs=4)

        # ---------------

        for view_info in view_info_list:

            this_part = view_info['part']
            this_parent = view_info['parent']

            this_part_column = cmds.columnLayout(adj=True, rs=4)

            cmds.rowColumnLayout(nc=5)

            animation_layer_info_item_list = []

            for info_item in this_target_info.info_item_list:

                if info_item.part != this_part:
                    continue

                if info_item.animation_layer_name:
                    animation_layer_info_item_list.append(info_item)
                    continue

                this_label = '{0}\t({1})'.format(
                    info_item.label, info_item.frame)

                this_button = base_class.ui.button.Button(
                    this_label,
                    self.change_facial_view_from_ui,
                    *[this_target_info.info_item_list, info_item.frame, category, False],
                    width=100)

                if info_item.color:

                    this_button.apply_button_param(e=True, bgc=info_item.color)

            cmds.setParent('..')

            if animation_layer_info_item_list:

                cmds.separator()

                cmds.rowColumnLayout(nc=5)

                for animation_info_item in animation_layer_info_item_list:

                    this_label = '{0}\t({1})'.format(
                        animation_info_item.label, animation_info_item.frame)

                    this_button = base_class.ui.button.Button(
                        this_label,
                        self.change_facial_animation_layer_view,
                        animation_info_item.animation_layer_name,
                        width=100)

                    if animation_info_item.color:

                        this_button.apply_button_param(e=True, bgc=animation_info_item.color)

                this_button = base_class.ui.button.Button(
                    'Reset',
                    self.reset_facial_animation_layer,
                    animation_layer_info_item_list,
                    width=100,
                    bgc=[0.8, 0.0, 0.0])

                cmds.setParent('..')

            cmds.separator()

            cmds.rowColumnLayout(nc=5, co=([1, 'right', 6]))

            base_class.ui.button.Button(
                '前の表情', self.change_next_facial_from_ui, *[this_target_info.info_item_list, True, this_category, this_part], width=247)

            base_class.ui.button.Button(
                '次の表情', self.change_next_facial_from_ui, *[this_target_info.info_item_list, False, this_category, this_part], width=247)

            cmds.setParent('..')

            cmds.setParent('..')

            cmds.columnLayout(
                this_part_column,
                e=True,
                parent=self.ui_root_layout.ui_lower_layout_id_dict[this_parent])

        # ---------------

        cmds.separator()

        base_class.ui.button.Button(
            'アニメーションレイヤーをリセットする', self.reset_facial_animation_layer, this_target_info.info_item_list)

        base_class.ui.button.Button(
            '1つ前の表情に戻る', self.go_previous_facial_from_ui, *[this_target_info.info_item_list, this_category])

        cmds.columnLayout(adj=True)

        tmp_form = cmds.formLayout()
        tmp_reverse = base_class.ui.button.Button(
            '全戻し', self.change_next_facial_from_ui, *[this_target_info.info_item_list, True, this_category])
        tmp_moveon = base_class.ui.button.Button(
            '全送り', self.change_next_facial_from_ui, *[this_target_info.info_item_list, False, this_category])

        cmds.formLayout(
            tmp_form,
            e=True,
            attachForm=[
                (tmp_reverse.ui_button_id, 'top', 0),
                (tmp_reverse.ui_button_id, 'left', 0),
                (tmp_moveon.ui_button_id, 'top', 0),
                (tmp_moveon.ui_button_id, 'right', 0),
            ],
            attachPosition=[
                (tmp_reverse.ui_button_id, 'right', 0, 49),
                (tmp_moveon.ui_button_id, 'left', 0, 51)
            ])
        cmds.setParent('..')

        cmds.setParent('..')

        cmds.rowColumnLayout(nc=2, adj=True)

        if this_category == 'facial':
            cmds.columnLayout(adj=True)
            self.ui_previous_facial_label = cmds.text(l='1つ前の表情 Frame (-)', align='left')
            self.ui_previous_facial_view_scroll_list = \
                base_class.ui.text_scroll_list.TextScrollList(e=True, h=50, enable=False)
            cmds.setParent('..')

            cmds.columnLayout(adj=True)
            self.ui_current_facial_label = cmds.text(l='現在の表情 Frame (-)', align='left')
            self.ui_current_facial_view_scroll_list = \
                base_class.ui.text_scroll_list.TextScrollList(e=True, h=50, enable=False)
            cmds.setParent('..')

        elif this_category == 'ear':
            cmds.columnLayout(adj=True)
            self.ui_previous_ear_label = cmds.text(l='1つ前の表情 Frame (-)', align='left')
            self.ui_previous_ear_view_scroll_list = \
                base_class.ui.text_scroll_list.TextScrollList(e=True, h=50, enable=False)
            cmds.setParent('..')

            cmds.columnLayout(adj=True)
            self.ui_current_ear_label = cmds.text(l='現在の表情 Frame (-)', align='left')
            self.ui_current_ear_view_scroll_list = \
                base_class.ui.text_scroll_list.TextScrollList(e=True, h=50, enable=False)
            cmds.setParent('..')

        cmds.setParent('..')

        if this_category == 'facial':
            self.create_tear_ui()
            self.create_facial_blend_ui(None)

        cmds.setParent('..')

        cmds.setParent('..')

        cmds.columnLayout(
            this_column,
            e=True,
            parent=self.ui_root_layout.ui_lower_layout_id_dict[parent_ui_name])

    # ==================================================
    def create_tear_ui(self):
        """
        フェイシャルターゲット系ツール/確認ツール/涙関連の確認
        現在開いているシーンが xxx_facial_target.ma でないと表示されないUI
        """

        label_width = 60
        button_whole_width = 360

        cmds.frameLayout(label='涙の確認', cll=True, bv=True, cl=True, mw=10, mh=10, bgc=[0.3, 0.4, 0.5])

        cmds.columnLayout(adj=True, rs=4)

        # ---------------

        cmds.rowLayout(nc=3)

        cmds.text(label='涙モデル', width=label_width, align='left')

        base_class.ui.button.Button(
            'モデル涙の表示',
            self.set_tear_mesh_visible, True, width=button_whole_width / 2)

        base_class.ui.button.Button(
            'モデル涙の非表示',
            self.set_tear_mesh_visible, False, width=button_whole_width / 2)

        cmds.setParent('..')

        # ---------------

        cmds.separator()

        # ---------------

        cmds.rowLayout(nc=3)

        cmds.text(label='うるうる涙', width=label_width, align='left')

        base_class.ui.button.Button(
            '読み込み',
            self.attach_tear_effect, True, width=button_whole_width / 2)

        base_class.ui.button.Button(
            'アンロード',
            self.attach_tear_effect, False, width=button_whole_width / 2)

        cmds.setParent('..')

        # ---------------

        cmds.rowLayout(nc=4)

        cmds.text(label='', width=label_width, align='left')

        base_class.ui.button.Button(
            '見え方を戻す',
            self.set_tear_effect_visibility, 1, False, width=button_whole_width / 3)

        base_class.ui.button.Button(
            '見えやすく',
            self.set_tear_effect_visibility, 10, False, width=button_whole_width / 3)

        base_class.ui.button.Button(
            'さらに見えやすく',
            self.set_tear_effect_visibility, 10, True, width=button_whole_width / 3)

        cmds.setParent('..')

        # ---------------

        tear_controller = facial_tear_anim_controller.FacialTearAnimController()
        tear_controller.update()

        cmds.rowLayout(nc=2)

        cmds.text(label='', width=label_width, align='left')

        self.ui_tear_frame_slider = cmds.floatSlider(
            min=0,
            max=127,
            value=tear_controller.current_frame,
            step=1,
            dc=self.update_tear_frame_from_slider,
            width=button_whole_width,
        )

        cmds.setParent('..')

        # ---------------

        cmds.rowLayout(nc=4)

        cmds.text(label='', width=label_width, align='left')

        base_class.ui.button.Button(
            '< 前のコマ',
            self.update_tear_frame_in_order, False, width=button_whole_width / 3)

        base_class.ui.button.Button(
            '次のコマ >',
            self.update_tear_frame_in_order, True, width=button_whole_width / 3)

        self.ui_tear_frame_field = cmds.textField(
            text=str(tear_controller.current_frame),
            width=button_whole_width / 3,
            changeCommand=self.update_tear_frame_from_text)

        cmds.setParent('..')

        # ---------------

        cmds.setParent('..')
        cmds.setParent('..')

    # ==================================================
    def create_facial_blend_ui(self, arg):
        """
        フェイシャルターゲット系ツール/確認ツール/表情ブレンドの確認
        現在開いているシーンが xxx_facial_target.ma でないと表示されないUI
        """

        cmds.frameLayout(label='表情ブレンドの確認', cll=True, bv=True, cl=True, mw=10, mh=10, bgc=[0.3, 0.4, 0.5])
        self.facial_blend_parent = cmds.columnLayout(adj=True, rs=4)
        # 「表情ブレンドを読み込み」ボタンを押すと更に眉、目、口の表情スライダーバーのUIが追加される
        self.blend_enable_check = cmds.button(label='表情ブレンドを読み込み', c=self.__create_facial_blend_ui)

        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')

    # ==================================================
    def __create_facial_blend_ui(self, arg):
        """
        フェイシャルターゲット系ツール/確認ツール/表情ブレンドの確認
        で「表情ブレンドを読み込み」ボタンを押した際に表示される眉、目、口の表情スライダーバーのUIの作成
        """
        cmds.deleteUI(self.blend_enable_check, ctl=True)

        self.facial_blend_viewer = facial_blend_viewer.FacialBlendViewer(self.facial_blend_parent)
        self.facial_blend_viewer.initialize()
        self.facial_blend_viewer.create_ui()

    # ==================================================
    def reset_facial_animation_layer(self, info_item_list):

        for info_item in info_item_list:

            if not info_item.animation_layer_name:
                continue

            if not cmds.animLayer(info_item.animation_layer_name, q=True, exists=True):
                return

            cmds.animLayer(info_item.animation_layer_name, e=True, weight=0.0, mute=False)

    # ==================================================
    def change_facial_animation_layer_view(self, animation_layer_name):

        if not cmds.animLayer(animation_layer_name, q=True, exists=True):
            return

        this_weight = cmds.animLayer(animation_layer_name, q=True, weight=True)

        this_weight += 1.0

        if this_weight > 1:
            this_weight = 0

        this_weight = cmds.animLayer(animation_layer_name, e=True, weight=this_weight, mute=False)

    # ==================================================
    def change_facial_view_from_ui(self, info_item_list, target_frame, category, is_keep_anim_layer=True):

        cmds.currentTime(target_frame)

        if self.current_frame is not None:
            self.previous_frame = self.current_frame
            self.previous_facial_view_info_items = self.current_facial_view_info_items

        self.current_frame = target_frame
        self.current_facial_view_info_items = []

        for info_item in info_item_list:

            if info_item.frame != target_frame:
                continue

            if target_frame == self.base_frame and not is_keep_anim_layer:
                info_item.root.set_weight_to_all_animation_layer(0)

            self.current_facial_view_info_items.append(info_item)

        part_param_list = []
        ui_previous_label = None
        ui_previous_view_scroll_list = None
        ui_current_label = None
        ui_current_view_scroll_list = None

        if category == 'facial':
            part_param_list = [
                {'target': 'Eyebrow_', 'label_name': '眉'},
                {'target': 'Eye_', 'label_name': '目'},
                {'target': 'Mouth', 'label_name': '口'}
            ]
            ui_previous_label = self.ui_previous_facial_label
            ui_previous_view_scroll_list = self.ui_previous_facial_view_scroll_list
            ui_current_label = self.ui_current_facial_label
            ui_current_view_scroll_list = self.ui_current_facial_view_scroll_list

        elif category == 'ear':
            part_param_list = [
                {'target': 'Ear_L', 'label_name': '耳'},
            ]
            ui_previous_label = self.ui_previous_ear_label
            ui_previous_view_scroll_list = self.ui_previous_ear_view_scroll_list
            ui_current_label = self.ui_current_ear_label
            ui_current_view_scroll_list = self.ui_current_ear_view_scroll_list

        if self.previous_frame is not None:
            previous_frame_text_list = []
            for part_param in part_param_list:
                target_part_prefix = part_param['target']
                target_label_name = part_param['label_name']

                item_label = '-'
                for previous_info_item in self.previous_facial_view_info_items:
                    if not previous_info_item.part.startswith(target_part_prefix):
                        continue
                    item_label = previous_info_item.label
                    break

                previous_frame_text_list.append(
                    '{0}:{1}'.format(target_label_name, item_label))

            ui_previous_view_scroll_list.set_item_list(previous_frame_text_list)
            cmds.text(
                ui_previous_label,
                e=True,
                l='1つ前の表情 Frame ({0})'.format(str(self.previous_frame)))

        if self.current_frame is not None:
            current_frame_text_list = []

            for part_param in part_param_list:
                target_part_prefix = part_param['target']
                target_label_name = part_param['label_name']

                item_label = '-'

                for current_info_item in self.current_facial_view_info_items:
                    if not current_info_item.part.startswith(target_part_prefix):
                        continue
                    item_label = current_info_item.label
                    break

                current_frame_text_list.append(
                    '{0}:{1}'.format(target_label_name, item_label))

            ui_current_view_scroll_list.set_item_list(current_frame_text_list)
            cmds.text(
                ui_current_label,
                e=True,
                l='現在の表情 Frame ({0})'.format(str(self.current_frame)))

    # ==================================================
    def change_next_facial_from_ui(self, info_item_list, is_inverse_order, category, this_part=''):

        if not info_item_list:
            return

        # アニメーションレイヤーのアイテムを除外
        info_list_exclude_anim_layer = []

        first_frame = None
        last_frame = None

        for info_item in info_item_list:

            if info_item.animation_layer_name:
                continue

            if this_part and info_item.part != this_part:
                continue

            info_list_exclude_anim_layer.append(info_item)
            if first_frame is None or first_frame > info_item.frame:
                first_frame = info_item.frame
            elif last_frame is None or last_frame < info_item.frame:
                last_frame = info_item.frame

        if first_frame is None or last_frame is None:
            return

        current_time = cmds.currentTime(q=True)

        if not is_inverse_order:

            if current_time >= last_frame:

                self.change_facial_view_from_ui(info_item_list, first_frame, category)
                return

        else:

            if current_time <= first_frame:

                self.change_facial_view_from_ui(info_item_list, last_frame, category)
                return

        target_frame = None

        if not is_inverse_order:

            for info_item in info_list_exclude_anim_layer:

                if info_item.frame <= current_time:
                    continue

                if current_time < info_item.frame <= last_frame:
                    if target_frame is None or info_item.frame < target_frame:
                        target_frame = info_item.frame

        else:

            for info_item in info_list_exclude_anim_layer:

                if info_item.frame >= current_time:
                    continue

                if first_frame <= info_item.frame < current_time:
                    if target_frame is None or info_item.frame > target_frame:
                        target_frame = info_item.frame

        if target_frame is not None:
            self.change_facial_view_from_ui(info_item_list, target_frame, category)

    # ==================================================
    def go_previous_facial_from_ui(self, info_item_list, category):

        if not self.previous_frame:
            return

        self.change_facial_view_from_ui(info_item_list, self.previous_frame, category)

    # ==================================================
    def set_tear_mesh_visible(self, visible):
        """
        M_Tear_L,M_Tear_Rの表示を設定
        """

        tear_l = cmds.ls('M_Tear_L', l=True, r=True)

        if not tear_l:
            return

        tear_l = tear_l[0]

        tear_r = cmds.ls('M_Tear_R', l=True, r=True)

        if not tear_r:
            return

        tear_r = tear_r[0]

        base_utility.attribute.set_value(tear_l, 'visibility', visible)
        base_utility.attribute.set_value(tear_r, 'visibility', visible)

    # ==================================================
    def attach_tear_effect(self, is_attach):
        """
        tearモデルをロードし、アタッチ
        """

        tear_attach = facial_tear_attach.FacialTearAttach()

        if is_attach:
            tear_attach.attach()
        else:
            tear_attach.dettach()

        self.__update_tear_frame_ui()

    # ==================================================
    def set_tear_effect_visibility(self, alpha_gain, show_vertex):
        """
        tearモデルを見え方を変更
        alpha_gainでファイルノードのアルファゲインを変更
        show_vertexで頂点表示
        """

        tear_transform_list = cmds.ls('M_Tear', l=True, r=True)

        if tear_transform_list:

            for tear_transform in tear_transform_list:

                tear_shape = \
                    base_utility.mesh.get_mesh_shape(tear_transform)

                if not tear_shape:
                    continue

                if show_vertex:
                    base_utility.attribute.set_value(tear_shape, 'displayVertices', True)
                    base_utility.attribute.set_value(tear_shape, 'vertexSize', 5)
                    base_utility.attribute.set_value(tear_shape, 'displayCenter', True)
                    base_utility.attribute.set_value(tear_shape, 'displayTriangles', True)
                else:
                    base_utility.attribute.set_value(tear_shape, 'displayVertices', False)
                    base_utility.attribute.set_value(tear_shape, 'vertexSize', 1)
                    base_utility.attribute.set_value(tear_shape, 'displayCenter', False)
                    base_utility.attribute.set_value(tear_shape, 'displayTriangles', False)

        tear_material_list = cmds.ls('mtl_chr_tear*', l=True, r=True)

        if tear_material_list:

            for tear_material in tear_material_list:

                file_node = cmds.listConnections(
                    tear_material + '.color', s=True, d=False)

                if not file_node:
                    continue

                file_node = file_node[0]

                base_utility.attribute.set_value(file_node, 'alphaGain', alpha_gain)

    # ==================================================
    def update_tear_frame_in_order(self, is_next):
        """
        涙のUVアニメーションを1フレームずつ進める
        """

        tear_controller = facial_tear_anim_controller.FacialTearAnimController()

        if is_next:
            tear_controller.go_to_next_frame()
        else:
            tear_controller.go_to_previous_frame()

        self.__update_tear_frame_ui()

    # ==================================================
    def update_tear_frame_from_text(self, arg):
        """
        涙のUVアニメーションをテキストフィールドから操作する
        """

        tear_controller = facial_tear_anim_controller.FacialTearAnimController()
        frame = cmds.textField(self.ui_tear_frame_field, q=True, text=True)
        tear_controller.go_to_frame(int(frame))

        self.__update_tear_frame_ui()

    # ==================================================
    def update_tear_frame_from_slider(self, arg):
        """
        涙のUVアニメーションをテキストフィールドから操作する
        """

        tear_controller = facial_tear_anim_controller.FacialTearAnimController()
        frame = cmds.floatSlider(self.ui_tear_frame_slider, q=True, v=True)
        tear_controller.go_to_frame(int(frame))

        self.__update_tear_frame_ui()

    # ==================================================
    def __update_tear_frame_ui(self):
        """
        涙確認用のUIを現在の涙の状況に合わせて更新する
        """

        tear_controller = facial_tear_anim_controller.FacialTearAnimController()
        tear_controller.update()

        cmds.textField(self.ui_tear_frame_field, e=True, text=str(tear_controller.current_frame))
        cmds.floatSlider(self.ui_tear_frame_slider, e=True, v=tear_controller.current_frame)

    # ==================================================
    def create_render_facial_target_ui(self):

        this_column = cmds.columnLayout(adj=True, rs=4)

        base_class.ui.button.Button(
            'フェイシャル一覧を出力', self.render_facial_target_from_ui, False)

        base_class.ui.button.Button(
            '各フェイシャル画像のみ出力', self.render_facial_png_from_ui, False)

        cmds.separator()

        base_class.ui.button.Button(
            'フェイスタイプ一覧を出力', self.render_face_type_from_ui, False)

        base_class.ui.button.Button(
            '各フェイスタイプ画像のみ出力', self.render_face_type_png_from_ui, False)

        cmds.frameLayout(label='バッチ', cll=True, bv=True, cl=True, mw=10, mh=10)
        cmds.columnLayout(adj=True, rs=4)

        self.ui_render_facial_target_selector = \
            base_class.ui.data_selector.DataSelector(
                'フォルダ', '', False, True)
        self.ui_render_facial_target_selector.set_path(
            'W:/gallop/svn/svn_gallop/80_3D/01_character/01_model/head')

        self.ui_render_facial_target_selector.set_file_filter(
            'facial_target', 'temp')
        self.ui_render_facial_target_selector.set_extension_filter('.ma')
        self.ui_render_facial_target_selector.set_contain_lower(True)

        base_class.ui.button.Button(
            'フェイシャル一覧をバッチ出力', self.render_facial_target_from_ui, True)

        base_class.ui.button.Button(
            '各フェイシャル画像のみバッチ出力', self.render_facial_png_from_ui, True)

        cmds.separator()

        base_class.ui.button.Button(
            'フェイスタイプ一覧をバッチ出力', self.render_face_type_from_ui, True)

        base_class.ui.button.Button(
            '各フェイスタイプ画像のみバッチ出力', self.render_face_type_png_from_ui, True)

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.setParent('..')

        cmds.columnLayout(
            this_column,
            e=True,
            parent=self.ui_root_layout.ui_lower_layout_id_dict['RenderFacialTarget'])

    # ==================================================
    def create_ear_target_editor_ui(self):

        this_column = cmds.columnLayout(adj=True, rs=4)

        base_class.ui.button.Button(
            'ear_target用リグ作成', self.create_ear_target_rig_from_ui)

        cmds.frameLayout(label='バッチ', cll=True, bv=True, cl=True, mw=10, mh=10)
        cmds.columnLayout(adj=True, rs=4)

        self.ui_recreate_ear_target_rig_selector = \
            base_class.ui.data_selector.DataSelector(
                'フォルダ', '', True, False)
        self.ui_recreate_ear_target_rig_selector.set_path(
            'W:/gallop/svn/svn_gallop/80_3D/01_character/01_model/head')

        base_class.ui.button.Button(
            'ear_target用リグ作成(TA実装用)', self.recreate_ear_target_rig_ma_by_batch_from_ui)

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.separator()

        base_class.ui.button.Button(
            'モデルmaからリグがアタッチされたear_target.maを作成 ※モデルmaを開いて実行してください', self.create_ear_target_rig_ma)

        cmds.frameLayout(label='バッチ', cll=True, bv=True, cl=True, mw=10, mh=10)
        cmds.columnLayout(adj=True, rs=4)

        self.ui_create_ear_target_rig_selector = \
            base_class.ui.data_selector.DataSelector(
                'フォルダ', '', True, False)
        self.ui_create_ear_target_rig_selector.set_path(
            'W:/gallop/svn/svn_gallop/80_3D/01_character/01_model/head')

        base_class.ui.button.Button(
            'モデルmaからバッチでear_target.maを作成', self.create_ear_target_rig_ma_by_batch_from_ui)

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.setParent('..')

        cmds.columnLayout(
            this_column,
            e=True,
            parent=self.ui_root_layout.ui_lower_layout_id_dict['EarTargetEditTool'])

    # ==================================================
    def create_export_ear_target_ui(self):

        this_column = cmds.columnLayout(adj=True, rs=4)

        base_class.ui.button.Button(
            'ear_target.fbxを出力', self.export_ear_target_from_ui, False)

        cmds.frameLayout(label='バッチ', cll=True, bv=True, cl=True, mw=10, mh=10)
        cmds.columnLayout(adj=True, rs=4)

        self.ui_export_ear_target_selector = \
            base_class.ui.data_selector.DataSelector(
                'フォルダ', '', False, True)
        self.ui_export_ear_target_selector.set_path(
            'W:/gallop/svn/svn_gallop/80_3D/01_character/01_model/head')

        self.ui_export_ear_target_selector.set_file_filter(
            'ear_target', 'temp')
        self.ui_export_ear_target_selector.set_extension_filter('.ma')
        self.ui_export_ear_target_selector.set_contain_lower(True)

        base_class.ui.button.Button(
            'ear_target.fbxをバッチ出力', self.export_ear_target_from_ui, True)

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.setParent('..')

        cmds.columnLayout(
            this_column,
            e=True,
            parent=self.ui_root_layout.ui_lower_layout_id_dict['ExportEarTarget'])

    # ==================================================
    def create_render_ear_target_ui(self):

        this_column = cmds.columnLayout(adj=True, rs=4)

        base_class.ui.button.Button(
            '耳一覧を出力', self.render_ear_target_from_ui, False, True)

        base_class.ui.button.Button(
            '各耳画像のみ出力', self.render_ear_target_from_ui, False, False)

        cmds.frameLayout(label='バッチ', cll=True, bv=True, cl=True, mw=10, mh=10)
        cmds.columnLayout(adj=True, rs=4)

        self.ui_render_ear_target_selector = \
            base_class.ui.data_selector.DataSelector(
                'フォルダ', '', False, True)
        self.ui_render_ear_target_selector.set_path(
            'W:/gallop/svn/svn_gallop/80_3D/01_character/01_model/head')

        self.ui_render_ear_target_selector.set_file_filter(
            'ear_target', 'temp')
        self.ui_render_ear_target_selector.set_extension_filter('.ma')
        self.ui_render_ear_target_selector.set_contain_lower(True)

        base_class.ui.button.Button(
            '耳一覧をバッチ出力', self.render_ear_target_from_ui, True, True)

        base_class.ui.button.Button(
            '各耳画像のみバッチ出力', self.render_ear_target_from_ui, True, False)

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.setParent('..')

        cmds.columnLayout(
            this_column,
            e=True,
            parent=self.ui_root_layout.ui_lower_layout_id_dict['RenderEarTarget'])

    # ==================================================
    def create_update_ctrl_rig_ui(self):

        state_filter_list = ['更新有り', '最新', 'RIG未作成']

        this_column = cmds.columnLayout(adj=True, rs=4)

        base_class.ui.button.Button(
            '_Ctrl_RIG.maの作成・更新', self.update_ctrl_rig_from_ui, False)

        cmds.frameLayout(label='バッチ', cll=True, bv=True, cl=True, mw=10, mh=10)
        cmds.columnLayout(adj=True, rs=4)

        self.ui_update_ctrl_rig_selector = \
            base_class.ui.data_selector.DataSelector(
                'フォルダ', '', False, True)

        self.ui_update_ctrl_rig_selector.set_path(
            'W:/gallop/svn/svn_gallop/80_3D/01_character/01_model/head')

        self.ui_update_ctrl_rig_selector.set_file_filter(
            'chr[1-9][0-9]{3}_[0-9]{2}_facial_target', 'temp')
        self.ui_update_ctrl_rig_selector.set_extension_filter('.ma')
        self.ui_update_ctrl_rig_selector.set_contain_lower(True)

        base_class.ui.button.Button(
            '_Ctrl_RIGの作成・更新', self.update_ctrl_rig_from_ui, True)

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.frameLayout(label='バッチ（対象選択）', cll=True, bv=True, cl=True, mw=10, mh=10)
        cmds.columnLayout(adj=True, rs=4)

        cmds.text(l='上の『バッチ』フレームで指定されたfacial_targetを対象に、更新状態を確認します', align='left')
        base_class.ui.button.Button(
            'facial_targetの更新状態を確認', self.check_facial_target_state)

        cmds.rowLayout(nc=3, adj=1)

        cmds.columnLayout(adj=True)
        cmds.text(l='更新状態', align='left')
        self.ui_update_ctrl_rig_state_list = base_class.ui.text_scroll_list.TextScrollList(nr=8)
        cmds.rowLayout(nc=len(state_filter_list) + 1)
        cmds.text(l='フィルタ: ', align='left')
        self.ui_update_ctrl_rig_state_filter_list = [(label, base_class.ui.check_box.CheckBox(label, False)) for label in state_filter_list]
        for _, button in self.ui_update_ctrl_rig_state_filter_list:
            button.set_change_function(self.update_facial_target_state_ui)
        cmds.setParent('..')
        cmds.setParent('..')

        cmds.columnLayout(adj=True, rs=4)
        base_class.ui.button.Button('>>', self.move_facial_target_state, True, True)
        base_class.ui.button.Button('>', self.move_facial_target_state, True, False)
        base_class.ui.button.Button('<', self.move_facial_target_state, False, False)
        base_class.ui.button.Button('<<', self.move_facial_target_state, False, True)
        cmds.setParent('..')

        cmds.columnLayout(adj=True)
        cmds.text(l='バッチ実行対象', align='left')
        self.ui_update_ctrl_rig_target_list = base_class.ui.text_scroll_list.TextScrollList(nr=8)
        base_class.ui.button.Button(
            '_Ctrl_RIGの作成・更新', self.update_ctrl_rig_from_ui, True, True)
        cmds.setParent('..')

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.setParent('..')

        cmds.columnLayout(
            this_column,
            e=True,
            parent=self.ui_root_layout.ui_lower_layout_id_dict['UpdateCtrlRig'])

    # ==================================================
    def create_common_setting_ui(self):

        this_column = cmds.columnLayout(adj=True, rs=4)

        self.ui_show_in_explorer = base_class.ui.check_box.CheckBox(
            '出力後エクスプローラを開く', False)

        self.ui_keep_temp_file = base_class.ui.check_box.CheckBox(
            '一時ファイルを保持', False)

        self.ui_is_ascii = base_class.ui.check_box.CheckBox(
            'ASCIIフォーマットで出力', False)

        cmds.setParent('..')

        cmds.columnLayout(
            this_column,
            e=True,
            parent=self.ui_root_layout.ui_lower_layout_id_dict['CommonSetting'])

    def on_scene_opened(self):

        self.update_category()

        self.create_facial_view_ui(self.category)

    def set_scene_opened_script_job(self):

        cmds.scriptJob(event=['SceneOpened', self.on_scene_opened], protected=True, parent=self.ui_window.ui_window_id)

    # ==================================================
    def load_setting(self):

        self.ui_window.load_setting(self.setting, 'MainWindow')

        self.ui_root_layout.load_setting(self.setting, 'RootLayout')

        self.ui_show_in_explorer.load_setting(self.setting, 'ShowInExplorer')
        self.ui_keep_temp_file.load_setting(self.setting, 'KeepTempFile')
        self.ui_is_ascii.load_setting(self.setting, 'IsAscii')

    # ==================================================
    def save_setting(self):

        self.ui_window.save_setting(self.setting, 'MainWindow')

        self.ui_root_layout.save_setting(self.setting, 'RootLayout')

        self.ui_show_in_explorer.save_setting(self.setting, 'ShowInExplorer')
        self.ui_keep_temp_file.save_setting(self.setting, 'KeepTempFile')
        self.ui_is_ascii.save_setting(self.setting, 'IsAscii')

    def show_manual(self, *args):
        import webbrowser
        try:
            webbrowser.open(self.manual_url)
        except Exception:
            cmds.warning('マニュアルページがみつかりませんでした')

# endregion

# region フェイシャル編集ツール

    # ==================================================
    def attach_rig_head_from_ui(self):

        if not base_utility.ui.dialog.open_ok_cancel(
                '確認', 'Rig_headとジョイントをアタッチしますか？', self.window_name):
            return

        rig_attach = facial_rig_head_attach.FacialRigHeadAttach()

        rig_attach.attach_rig()

    # ==================================================
    def detach_rig_head_from_ui(self):

        if not base_utility.ui.dialog.open_ok_cancel(
                '確認', 'Rig_headとジョイントをデタッチしますか？', self.window_name):
            return

        rig_attach = facial_rig_head_attach.FacialRigHeadAttach()

        rig_attach.detach_rig()

    # ==================================================
    def reset_rig_head_from_ui(self):

        if not base_utility.ui.dialog.open_ok_cancel(
                '確認', 'Rig_headをリセットしますか？', self.window_name):
            return

        rig_attach = facial_rig_head_attach.FacialRigHeadAttach()

        rig_attach.reset_rig()

    # ==================================================
    def create_eye_high_rig_from_ui(self):

        if not base_utility.ui.dialog.open_ok_cancel(
                '確認', '目のハイライトリグを作成しますか？', self.window_name):
            return

        controller_creator = \
            eye_controller_creator.EyeControllerCreator()

        controller_creator.create()

    # ==================================================
    def fix_reference_from_ui(self):

        if not base_utility.ui.dialog.open_ok_cancel('確認',
                                                     'リファレンス先を最適化しますか?',
                                                     self.window_name):
            return

        _chara_info = chara_info.CharaInfo()
        _chara_info.create_info()

        if not _chara_info.exists:
            return

        this_namespace = 'mdl_' + _chara_info.part_info.data_id

        reference_path = _chara_info.part_info.maya_scenes_dir_path + '/' + \
            'mdl_' + _chara_info.part_info.data_id + '.ma'

        base_utility.reference.change_reference_file_path_by_namespace(
            this_namespace, reference_path)

    # ==================================================
    def switch_facial_timeline(self, min_frame):

        max_frame = min_frame + 99

        cmds.playbackOptions(
            min=min_frame, max=max_frame, ast=min_frame, aet=max_frame)
        cmds.currentTime(min_frame)
        cmds.play(f=False, w=True, ps=False)

    # ==================================================
    def copy_facial_key_from_ui(self):
        """タイムラインの現在のフレームの表情のキーフレーム情報をコピーする。
        各表情のパーツ（例：左目）などがどのコントロールリグで構成されているかは
        csvを読み込んで対象コントロールリグやロケータ等を割り出している。
        """
        copyFrame = cmds.currentTime(q=True)

        self.facial_copy_info = facial_copy_info.FacialCopyInfo()

        self.facial_copy_info.create_info_from_frame(copyFrame)

        self.facial_copy_info.update_info(True, False)

    # ==================================================
    def paste_facial_key_from_ui(self, target_list):
        """コントロールリグを設定した表情のアニメーションをペーストする。
        表情全部ではなくパーツを指定できる。
        Args:
            target_list (list<bool>[5]): 左眉、右眉、左目、右目、口のどのパーツに
        コピーするかboolで指定。
        """
        if not target_list:
            cmds.error('target_listが未定義(TAに連絡)')
            return

        if len(target_list) < 5:
            cmds.error('target_listが5より少ない(TAに連絡)')
            return

        is_eyebrow_l = target_list[0]
        is_eyebrow_r = target_list[1]
        is_eye_l = target_list[2]
        is_eye_r = target_list[3]
        is_mouth = target_list[4]

        paste_frame = cmds.currentTime(q=True)

        if not self.facial_copy_info:
            cmds.warning('コピーしたいフレームで「コピー」ボタンを押し、' +
                         'ペーストしたいフレームに移動してからペーストする' +
                         'パーツのボタンを押してください')
            return

        self.facial_copy_info.set_transform(
            paste_frame,
            True,
            is_eyebrow_l, is_eyebrow_r,
            is_eye_l, is_eye_r,
            is_mouth
        )

        cmds.currentTime(paste_frame)

# endregion

# region facial_rigの左右ミラー

    # ==================================================
    def mirror_facial_rig_from_ui(self):

        mirror_transform = facial_mirror_transform.FacialMirrorTransform()
        mirror_transform.x_mirror_transform()

# endregion

# region facial_target.fbxの出力

    # ==================================================
    def export_facial_target_from_ui(self, is_batch):
        """
        フェイシャルターゲット系ツール/facial_target.fbxエクスポート/
        「_facial_target.fbxを出力」もしくは「_facial_target.fbxをバッチ出力」実行
        """
        if not base_utility.ui.dialog.open_ok_cancel(
                '確認', 'facial_target.fbxを出力しますか?',
                self.ui_window.ui_window_id):
            return

        if is_batch:
            # 範囲が広いとファイルのリストに時間がかかり無反応に思えるのでメッセージを表示
            om.MGlobal.displayInfo('対象ファイルをリスト中...')
        else:
            # get_target_file_path_list_from_selectorは現在のシーンのファイル名のチェックをしないので
            # バッチ処理に行く前にチェック
            current_file_path = cmds.file(q=True, sn=True)
            if current_file_path.find('_facial_target') < 0:
                cmds.confirmDialog(
                    title='Usage', message='_facial_targetのシーンを開いてから実行してください', button=['OK'])
                return

        # 実行対象ファイルのリスト
        # ____temp_xxx.ma というシーンが作られそのリストが返っている(is_create_temp=Trueなので)
        target_file_path_list = self.get_target_file_path_list_from_selector(
            self.ui_export_facial_target_selector, is_batch, is_create_temp=True)

        if not target_file_path_list:
            cmds.confirmDialog(title='Confirm',
                               message='対象ファイルがありませんでした            ',
                               button=['OK'])
            return

        om.MGlobal.displayInfo('')
        base_utility.simple_batch2.execute_mayabatch(
            'Project_Gallop.glp_chara_facial_tool.main',
            'batch(\'export_facial_target\')',
            False,
            target_file_path_list=target_file_path_list)

    # ==================================================
    def batch_export_facial_target(self):
        """
        フェイシャルターゲット系ツール/facial_target.fbxエクスポート/
        「_facial_target.fbxを出力」もしくは「_facial_target.fbxをバッチ出力」で
        コマンドラインから実行される関数。
        """
        kwargs = base_utility.simple_batch2.get_kwargs()
        target_file_path_list = []
        if kwargs:
            target_file_path_list = kwargs['target_file_path_list']

        if not target_file_path_list:
            print('対象ファイルがありませんでした'.encode('shift-jis'))
            return
        exporter = facial_target_exporter.FacialTargetExporter(self)
        errorScenes = []
        for target_file_path in target_file_path_list:
            if not os.path.exists(target_file_path):
                errorScenes.append(target_file_path)
                cmds.warning('ファイルパスが存在しません: ' + target_file_path)
                continue
            cmds.file(new=True, force=True)  # RuntimeError: Unsaved changes 対応
            cmds.file(target_file_path, o=True)
            if not exporter.export():
                errorScenes.append(target_file_path)
            if target_file_path.find('____temp') >= 0:
                os.remove(target_file_path)
        if errorScenes:
            cmds.warning('\n完了\nエラーのあったシーン')
            for path in errorScenes:
                cmds.warning(path)
        else:
            om.MGlobal.displayInfo('_facial_target.fbx出力完了')

# endregion

# region facial_blend_target.maの作成

    # ==================================================
    def create_facial_blend_target_from_ui(self, is_batch):
        """
        フェイシャルターゲット系ツール/facial_blend_target.maの作成/
        「_facial_blend_target.maを出力」もしくは「_facial_blend_target.maをバッチ出力」実行
        """
        if not base_utility.ui.dialog.open_ok_cancel(
                '確認', 'facial_blend_target.maを作成しますか?',
                self.ui_window.ui_window_id):
            return

        if is_batch:
            # 範囲が広いとファイルのリストに時間がかかり無反応に思えるのでメッセージを表示
            om.MGlobal.displayInfo('対象ファイルをリスト中...')
        else:
            # get_target_file_path_list_from_selectorは現在のシーンのファイル名のチェックをしないので
            # バッチ処理に行く前にチェック
            current_file_path = cmds.file(q=True, sn=True)
            if current_file_path.find('_facial_target') < 0:
                cmds.confirmDialog(
                    title='Usage', message='_facial_targetのシーンを開いてから実行してください', button=['OK'])
                return

        # 実行対象ファイルのリスト
        # ____temp_xxx.ma というシーンが作られそのリストが返っている(is_create_temp=Trueなので)
        target_file_path_list = self.get_target_file_path_list_from_selector(
            self.ui_create_facial_blend_target_selector, is_batch, is_create_temp=True)

        if not target_file_path_list:
            cmds.confirmDialog(title='Confirm',
                               message='対象ファイルがありませんでした            ',
                               button=['OK'])
            return

        om.MGlobal.displayInfo('')
        base_utility.simple_batch2.execute_mayabatch(
            'Project_Gallop.glp_chara_facial_tool.main',
            'batch(\'create_facial_blend_target\')',
            False,
            target_file_path_list=target_file_path_list)

    # ==================================================
    def batch_create_facial_blend_target(self):
        """
        フェイシャルターゲット系ツール/facial_blend_target.maの作成/
        「_facial_blend_target.maを出力」もしくは「_facial_blend_target.maをバッチ出力」実行で
        コマンドラインから実行される関数。
        """
        kwargs = base_utility.simple_batch2.get_kwargs()
        target_file_path_list = []
        if kwargs:
            target_file_path_list = kwargs['target_file_path_list']

        if not target_file_path_list:
            print('対象ファイルがありませんでした'.encode('shift-jis'))
            return

        for target_file_path in target_file_path_list:

            base_utility.file.open(target_file_path)

            self.create_facial_blend_target()

            if target_file_path.find('____temp') >= 0:
                os.remove(target_file_path)

    # ==================================================
    def create_facial_blend_target(self):

        current_file_path = cmds.file(q=True, sn=True)

        if not current_file_path:
            return

        current_file_path = current_file_path.replace('\\', ' / ')

        if current_file_path.find('_facial_target.ma') < 0:
            return

        this_target_info = target_info.TargetInfo()

        this_target_info.create_info_from_csv('facial_target_info',
                                              'facial_controller_info')

        this_target_info.update_info(True, False)

        this_blend_target_info = blend_target_info.BlendTargetInfo()
        this_blend_target_info.create_info_from_csv(this_target_info,
                                                    'facial_blend_info')
        this_blend_target_info.update_info(True, False)

        new_file_path = current_file_path.replace('_facial_target.ma',
                                                  '_facial_blend_target.ma')

        new_file_path = new_file_path.replace('____temp_', '')

        cmds.file(rn=new_file_path)
        cmds.file(save=True)

        self.clear_facial_key(False)

        this_blend_target_info.set_transform(True, 0)

        cmds.file(save=True)

    # ==================================================
    def clear_facial_key(self, keep_eye_animation):

        cmds.currentTime(0)

        cmds.select(clear=True)

        if cmds.objExists('Rig_head'):
            cmds.select(['Rig_head'], add=True)

        if cmds.objExists('Rig_eye_high'):
            cmds.select(['Rig_eye_high'], add=True)

        cmds.select(hi=True)

        target_transform_list = cmds.ls(sl=True, l=True, typ='transform')

        if not target_transform_list:
            return

        target_attr_list = [
            'tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz', 'v'
        ]

        if not keep_eye_animation:

            for target_transform in target_transform_list:

                for target_attr in target_attr_list:

                    self.cut_keyframe(target_transform, target_attr, 0, 100000)
            return

        copy_start_frame = 200
        copy_end_frame = 400
        paste_frame = 600

        for target_transform in target_transform_list:

            for target_attr in target_attr_list:

                self.cut_keyframe(target_transform, target_attr, 0,
                                  copy_start_frame - 1)

                self.cut_keyframe(target_transform, target_attr,
                                  copy_end_frame + 1, copy_end_frame + 2000)

        for target_transform in target_transform_list:

            for target_attr in target_attr_list:

                self.copy_paste_keyframe(target_transform, target_attr,
                                         copy_start_frame, copy_end_frame,
                                         paste_frame, True)

    # ==================================================
    def cut_keyframe(self, target_node, target_attribute, start_frame,
                     end_frame):

        if not target_node:
            return

        if not target_attribute:
            return

        keyframe_list = cmds.keyframe(
            target_node,
            q=True,
            attribute=target_attribute,
            timeChange=True,
            absolute=True)

        if not keyframe_list:
            return

        current_value = base_utility.attribute.get_value(
            target_node, target_attribute)

        cmds.cutKey(
            target_node,
            attribute=target_attribute,
            time=(start_frame, end_frame))

        base_utility.attribute.set_value(target_node, target_attribute,
                                         current_value)

    # ==================================================

    def copy_paste_keyframe(self, target_node, target_attribute, start_frame,
                            end_frame, paste_frame, is_cut):

        if not target_node:
            return

        if not target_attribute:
            return

        keyframe_list = cmds.keyframe(
            target_node,
            q=True,
            attribute=target_attribute,
            timeChange=True,
            absolute=True)

        if not keyframe_list:
            return

        if is_cut:
            cmds.cutKey(
                target_node,
                time=(start_frame, end_frame),
                attribute=target_attribute,
                option='curve')
        else:
            cmds.copyKey(
                target_node,
                time=(start_frame, end_frame),
                attribute=target_attribute,
                option='curve')

        try:
            cmds.pasteKey(
                target_node,
                time=(paste_frame, paste_frame),
                attribute=target_attribute)
        except Exception:
            pass

# endregion

# region facial_targetのレンダリング

    # ==================================================
    def render_facial_target_from_ui(self, is_batch, should_output_psd=True):
        """
        フェイシャルターゲット系ツール/facial_targetのレンダリング
        「フェイシャル一覧を出力」「フェイシャル一覧をバッチ出力」
        眉、目、口の表情パーツの一覧をレンダリングする
        should_output_psd: bool. Falseならscemesフォルダと同階層の
        images/facial_target/キャラIDフォルダ内にpngを書き出し終了。
        TrueならPhotoshopへ処理を引き渡し、書き出したpngをpsdにまとめ、
        80_3D/01_character/02_faical_list/facialフォルダにjpgを出力。
        """
        if not base_utility.ui.dialog.open_ok_cancel(
                '確認', 'facial_targetをレンダリングしますか?', self.ui_window.ui_window_id):
            return

        if is_batch:
            # 範囲が広いとファイルのリストに時間がかかり無反応に思えるのでメッセージを表示
            om.MGlobal.displayInfo('対象ファイルをリスト中...')
        else:
            # get_target_file_path_list_from_selectorは現在のシーンのファイル名のチェックをしないので
            # バッチ処理に行く前にチェック
            current_file_path = cmds.file(q=True, sn=True)
            if current_file_path.find('_facial_target') < 0:
                cmds.confirmDialog(title='Usage',
                                   message='_facial_targetのシーンを開いてから実行してください',
                                   button=['OK'])
                return

        target_file_path_list = self.get_target_file_path_list_from_selector(
            self.ui_render_facial_target_selector, is_batch, is_create_temp=True)

        if not target_file_path_list:
            cmds.confirmDialog(title='Confirm',
                               message='対象ファイルがありませんでした            ',
                               button=['OK'])
            return

        om.MGlobal.displayInfo('')
        base_utility.simple_batch2.execute_mayabatch(
            'Project_Gallop.glp_chara_facial_tool.main',
            'batch(\'render_facial_target\')',
            False,
            target_file_path_list=target_file_path_list,
            should_output_psd=should_output_psd)

    # ==================================================

    def render_facial_png_from_ui(self, is_batch):

        self.render_facial_target_from_ui(is_batch, False)

    # ==================================================
    def batch_render_facial_target(self):
        """
        フェイシャルターゲット系ツール/facial_targetのレンダリング
        「フェイシャル一覧を出力」「フェイシャル一覧をバッチ出力」
        コマンドラインから実行される関数。
        """
        kwargs = base_utility.simple_batch2.get_kwargs()
        target_file_path_list = []
        should_output_psd = True
        if kwargs:
            target_file_path_list = kwargs['target_file_path_list']
            should_output_psd = kwargs['should_output_psd']

        if not target_file_path_list:
            print('対象ファイルがありませんでした'.encode('shift-jis'))
            return

        for target_file_path in target_file_path_list:

            base_utility.file.open(target_file_path)

            if not self.render_facial_target(should_output_psd):
                cmds.warning('表情パーツのレンダリングに失敗しました: ' + target_file_path)

            if target_file_path.find('____temp') >= 0:
                os.remove(target_file_path)

        if should_output_psd:
            self.render_facial_target_subprocess()

    # ==================================================
    def render_facial_target(self, should_output_psd):
        """
        眉、目、口の表情pngをfacial_targetフォルダに書き出す
        should_output_psd: bool がTrueならrenderの最後にxxx_facial_target_tmp.psdを
        フォルダ内にダウンロードするので、render_facial_target_subprocess がそれを拾って
        処理をつづけるようになっている。
        TODO: win32com (pywin32) モジュールを使い、パラメータ付きでPhotoshop.exeで処理できるようにする。
        Mayapy2.7だとwin32comに必要なwin32appが使えなかったのでMayapy3以降の課題
        """
        renderer = facial_target_renderer.FacialTargetRenderer()
        return renderer.render(should_output_psd)

    # ==================================================
    def render_facial_target_subprocess(self):

        renderer = facial_target_renderer.FacialTargetRenderer()
        renderer.exe_subprocess()

# endregion

# region face_typeのレンダリング

    # ==================================================
    def render_face_type_from_ui(self, is_batch, should_output_psd=True):
        """
        「フェイスタイプ一覧を出力」「フェイスタイプ一覧をバッチ出力」
        各パーツを組み合わせた各種「表情」をレンダリングする
        should_output_psd: bool. Falseならscemesフォルダと同階層のimages/face_type/キャラIDフォルダ内にpngを書き出し終了。
        TrueならPhotoshopへ処理を引き渡し、書き出したpngをpsdにまとめ、80_3D/01_character/02_faical_list/face_typeフォルダにjpgを出力。
        """
        if not os.path.isdir(self.ui_render_facial_target_selector.get_path()):
            base_utility.ui.dialog.open_ok(
                '確認', 'フォルダが存在しません\n' +
                self.ui_render_facial_target_selector.get_path())
            return

        if not base_utility.ui.dialog.open_ok_cancel(
                '確認', 'face_typeをレンダリングしますか?', self.ui_window.ui_window_id):
            return

        if is_batch:
            # 範囲が広いとファイルのリストに時間がかかり無反応に思えるのでメッセージを表示
            om.MGlobal.displayInfo('対象ファイルをリスト中...')
        else:
            # get_target_file_path_list_from_selectorは現在のシーンのファイル名のチェックをしないので
            # バッチ処理に行く前にチェック
            current_file_path = cmds.file(q=True, sn=True)
            if current_file_path.find('_facial_target') < 0:
                cmds.confirmDialog(
                    title='Usage', message='_facial_targetのシーンを開いてから実行してください',
                    button=['OK'])
                return

        target_file_path_list = self.get_target_file_path_list_from_selector(
            self.ui_render_facial_target_selector, is_batch, is_create_temp=True)

        if not target_file_path_list:
            cmds.confirmDialog(title='Confirm',
                               message='対象ファイルがありませんでした            ',
                               button=['OK'])
            return

        om.MGlobal.displayInfo('')
        base_utility.simple_batch2.execute_mayabatch(
            'Project_Gallop.glp_chara_facial_tool.main',
            'batch(\'render_face_type\')',
            False,
            target_file_path_list=target_file_path_list,
            should_output_psd=should_output_psd)

    # ==================================================
    def render_face_type_png_from_ui(self, is_batch):

        self.render_face_type_from_ui(is_batch, False)

    # ==================================================
    def batch_render_face_type(self):
        kwargs = base_utility.simple_batch2.get_kwargs()
        target_file_path_list = []
        should_output_psd = True
        if kwargs:
            target_file_path_list = kwargs['target_file_path_list']
            should_output_psd = kwargs['should_output_psd']

        if not target_file_path_list:
            cmds.warning('対象ファイルがありませんでした')
            return

        for target_file_path in target_file_path_list:

            base_utility.file.open(target_file_path)

            if not self.render_face_type(should_output_psd):
                cmds.warning('表情のレンダリングに失敗しました: ' + target_file_path)

            if target_file_path.find('____temp') >= 0:
                os.remove(target_file_path)
        # Photoshopでの処理開始。_tmpファイル名で対象を選り分けている。
        if should_output_psd:
            self.render_face_type_subprocess()

    # ==================================================
    def render_face_type(self, should_output_psd):
        """
        眉、目、口を組み合わせた表情pngをface_typeフォルダに書き出す
        """
        renderer = facial_target_renderer.FacialTargetRenderer()
        return renderer.render_face_type(should_output_psd)

    # ==================================================
    def render_face_type_subprocess(self):
        """
        出力済みのpng画像を使いPhotoshop側で画像をまとめる
        """
        renderer = facial_target_renderer.FacialTargetRenderer()
        renderer.exe_subprocess()

# endregion

# region ear_target.fbxの出力

    # ==================================================
    def export_ear_target_from_ui(self, is_batch):

        if not base_utility.ui.dialog.open_ok_cancel(
                '確認', 'ear_target.fbxを出力しますか?', self.ui_window.ui_window_id):
            return

        if is_batch:
            # 範囲が広いとファイルのリストに時間がかかり無反応に思えるのでメッセージを表示
            om.MGlobal.displayInfo('対象ファイルをリスト中...')
        else:
            # get_target_file_path_list_from_selectorは現在のシーンのファイル名のチェックをしないので
            # バッチ処理に行く前にチェック
            current_file_path = cmds.file(q=True, sn=True)
            if current_file_path.find('_ear_target') < 0:
                cmds.confirmDialog(
                    title='Usage', message='_ear_targetのシーンを開いてから実行してください',
                    button=['OK'])
                return

        target_file_path_list = self.get_target_file_path_list_from_selector(
            self.ui_export_ear_target_selector, is_batch, is_create_temp=True)

        if not target_file_path_list:
            cmds.confirmDialog(title='Confirm',
                               message='対象ファイルがありませんでした            ',
                               button=['OK'])
            return

        om.MGlobal.displayInfo('')
        base_utility.simple_batch2.execute_mayabatch(
            'Project_Gallop.glp_chara_facial_tool.main',
            'batch(\'export_ear_target\')',
            False,
            target_file_path_list=target_file_path_list)

    # ==================================================
    def batch_export_ear_target(self):

        kwargs = base_utility.simple_batch2.get_kwargs()
        target_file_path_list = []
        if kwargs:
            target_file_path_list = kwargs['target_file_path_list']

        if not target_file_path_list:
            print('対象ファイルがありませんでした'.encode('shift-jis'))
            return

        for target_file_path in target_file_path_list:

            base_utility.file.open(target_file_path)

            self.export_ear_target()

            if target_file_path.find('____temp') >= 0:
                os.remove(target_file_path)

    # ==================================================
    def export_ear_target(self):

        exporter = ear_target_exporter.EarTargetExporter(self)
        exporter.export()

# endregion

# region ear_targetのレンダリング

    # ==================================================
    def render_ear_target_from_ui(self, is_batch, should_output_psd=True):
        """
        「耳一覧を出力」「各耳画像のみ出力」「耳一覧をバッチ出力」「各耳画像のみバッチ出力」
        80_3D/01_character/02_faical_list/ear に キャラID_ear_target.jpg を書き出す。
        まずMayaシーンから 80_3D/01_character/01_model/head/chr1010_00/images フォルダにpngを書き出し
        それからPhotoshopを起動し_ear_target.psdの中に各耳の画像を貼り付けjpgとして書き出す。
        """
        if not base_utility.ui.dialog.open_ok_cancel(
                '確認', 'ear_targetをレンダリングしますか?', self.ui_window.ui_window_id):
            return

        if is_batch:
            # 範囲が広いとファイルのリストに時間がかかり無反応に思えるのでメッセージを表示
            om.MGlobal.displayInfo('対象ファイルをリスト中...')
        else:
            # get_target_file_path_list_from_selectorは現在のシーンのファイル名のチェックをしないので
            # バッチ処理に行く前にチェック
            current_file_path = cmds.file(q=True, sn=True)
            if current_file_path.find('_ear_target') < 0:
                cmds.confirmDialog(title='Usage', message='_ear_targetのシーンを開いてから実行してください', button=['OK'])
                return

        target_file_path_list = self.get_target_file_path_list_from_selector(
            self.ui_render_ear_target_selector, is_batch, is_create_temp=True)

        if not target_file_path_list:
            cmds.confirmDialog(title='Confirm',
                               message='対象ファイルがありませんでした            ',
                               button=['OK'])
            return

        om.MGlobal.displayInfo('')
        base_utility.simple_batch2.execute_mayabatch(
            'Project_Gallop.glp_chara_facial_tool.main',
            'batch(\'render_ear_target\')',
            False,
            target_file_path_list=target_file_path_list,
            should_output_psd=should_output_psd)

    # ==================================================
    def batch_render_ear_target(self):
        """
        80_3D/01_character/02_faical_list/ear に 耳一覧を出力（バッチでも現在のシーンでも）
        """
        kwargs = base_utility.simple_batch2.get_kwargs()
        target_file_path_list = []
        should_output_psd = True
        if kwargs:
            target_file_path_list = kwargs['target_file_path_list']
            should_output_psd = kwargs['should_output_psd']

        if not target_file_path_list:
            print('対象ファイルがありませんでした'.encode('shift-jis'))
            return

        for target_file_path in target_file_path_list:

            base_utility.file.open(target_file_path)

            self.render_ear_target(should_output_psd)

            if target_file_path.find('____temp') >= 0:
                os.remove(target_file_path)
        # ps_target_maker.jsx を実行
        if should_output_psd:
            self.render_ear_target_subprocess()

    # ==================================================
    def render_ear_target(self, should_output_psd):

        renderer = ear_target_renderer.EarTargetRenderer()
        renderer.render(should_output_psd)

    # ==================================================
    def render_ear_target_subprocess(self):

        renderer = ear_target_renderer.EarTargetRenderer()
        renderer.exe_subprocess()

# endregion

# region ear_targetのリグ作成

    # ==================================================
    def create_ear_target_rig_from_ui(self):
        """
        耳ターゲット系ツール/編集ツール「ear_target用リグ作成」
        """

        if not base_utility.ui.dialog.open_ok_cancel(
                '確認', 'ear_target用リグを作成しますか?', self.ui_window.ui_window_id):
            return

        self.create_ear_target_rig()

    # ==================================================
    def create_ear_target_rig(self):

        ctrl_creator = ear_controller_creator.EarControllerCreator()
        ctrl_creator.create()

    # ==================================================
    def recreate_ear_target_rig_ma_by_batch_from_ui(self):
        """
        耳ターゲット系ツール/編集ツール「ear_target用リグ作成(TA実装用)」
        """
        if not base_utility.ui.dialog.open_ok_cancel(
                '確認', '再アタッチ?', self.ui_window.ui_window_id):
            return

        model_dir_regex = re.compile(r'scenes(/hair|)/mdl_chr[0-9]{4}_[0-9]{2}(_hair[0-9]{3}|)_ear_target.ma$')

        target_dir_path = self.ui_create_ear_target_rig_selector.get_path()

        # 範囲が広いとファイルのリストに時間がかかり無反応に思えるのでメッセージを表示
        om.MGlobal.displayInfo('対象ファイルをリスト中...')

        target_file_path_list = []
        for root, dirs, files in os.walk(target_dir_path):
            for filename in files:
                file_full_path = os.path.join(root, filename).replace('\\', '/')
                if not model_dir_regex.search(file_full_path):
                    continue
                target_file_path_list.append(file_full_path)   # ファイルのみ再帰でいい場合はここまででOK

        if not target_file_path_list:
            cmds.confirmDialog(title='Confirm',
                               message='対象ファイルがありませんでした            ',
                               button=['OK'])
            return

        om.MGlobal.displayInfo('')
        base_utility.simple_batch2.execute_mayabatch(
            'Project_Gallop.glp_chara_facial_tool.main',
            'batch(\'recreate_ear_target_rig_ma\')',
            False,
            target_file_path_list=target_file_path_list)

    # ==================================================
    def batch_recreate_ear_target_rig_ma(self):

        kwargs = base_utility.simple_batch2.get_kwargs()
        target_file_path_list = []
        if kwargs:
            target_file_path_list = kwargs['target_file_path_list']

        if not target_file_path_list:
            print('対象ファイルがありませんでした'.encode('shift-jis'))
            return

        for target_file_path in target_file_path_list:

            cmds.file(force=True, new=True)
            base_utility.file.open(target_file_path)

            if cmds.objExists('Rig_ear'):

                # 2回掛ける
                self.create_ear_target_rig()
                self.create_ear_target_rig()

                base_utility.file.save(target_file_path)

    # ==================================================
    def create_ear_target_rig_ma(self, target_file_path='', is_batch=False):
        """
        耳ターゲット系ツール/編集ツール
        「ear_target用リグ作成」
        「ear_target用リグ作成(TA実装用)」
        「モデルmaからバッチでear_target.maを作成」
        「モデルmaからリグがアタッチされたear_target.maを作成 ※モデルmaを開いて実行してください」
        """
        if not is_batch:
            if not base_utility.ui.dialog.open_ok_cancel(
                    '確認', 'モデル用maからear_target用リグがアタッチされたmaを作成しますか?', self.ui_window.ui_window_id):
                return

        ma_file_path = ''

        if not target_file_path:

            ma_file_path = cmds.file(sn=True, q=True)
            if not ma_file_path:
                cmds.warning('ファイルからパスが取得できません')
                return 'not export {}'.format(ma_file_path)

            match_obj = re.search(r'mdl_chr[0-9]{4}_[0-9]{2}(_hair[0-9]{3}|).ma$', ma_file_path)
            if not match_obj:
                cmds.warning('ファイルの命名規則が合っていません')
                return 'not export {}'.format(ma_file_path)

            ma_file_dir = os.path.dirname(ma_file_path)
            ma_file_name, ma_file_ext = os.path.splitext(os.path.basename(ma_file_path))
            target_file_path = os.path.join(
                ma_file_dir,
                '{}_ear_target{}'.format(ma_file_name, ma_file_ext)
            )

        match_obj = re.search(r'_ear_target.ma$', target_file_path)
        if not match_obj:
            cmds.warning('ターゲットの命名規則が合っていません')
            return 'not export {}'.format(ma_file_path)

        # ear_tagetの対になるmodel maのpath
        if not ma_file_path:

            ma_file_path = target_file_path.replace('_ear_target', '')
            if not os.path.exists(ma_file_path):
                cmds.warning('モデルのmaが存在しません')
                return 'not export {}'.format(ma_file_path)

        # 現在のファイルをoldとして保存
        if os.path.exists(target_file_path):
            target_file_name, target_file_ext = os.path.splitext(os.path.basename(target_file_path))
            base_utility.file.create_temp(target_file_path, '{}____old{}'.format(target_file_name, target_file_ext))

        ma_file_name, ma_file_ext = os.path.splitext(os.path.basename(ma_file_path))

        # new sceneを開いてreferenceとしてmodel maを読み込む
        cmds.file(force=True, new=True)
        cmds.file(ma_file_path, reference=True, mergeNamespacesOnClash=True, namespace=':{}'.format(ma_file_name))

        self.create_ear_target_rig()

        # ダイアログが表示されてしまうので出ない様にする
        mel.eval('putenv "MAYA_TESTING_CLEANUP" "1";')

        # unknownノードを最適化
        self.optimize_node(['unknownNodesOption'])

        # 元のear_targetファイルを削除
        if os.path.exists(target_file_path):
            os.remove(target_file_path)

        # ear_targetとして保存　
        cmds.file(rename=target_file_path)
        cmds.file(force=True, type='mayaAscii', save=True)

        if not is_batch:
            base_utility.ui.dialog.open_ok('完了', 'ear_target用のリグアタッチモデルの出力が完了しました')

        return ma_file_path

    # ==================================================
    def create_ear_target_rig_ma_by_batch_from_ui(self):
        """
        「モデルmaからバッチでear_target.maを作成」
        """

        if not base_utility.ui.dialog.open_ok_cancel(
                '確認', 'モデル用maからear_target用リグがアタッチされたmaを作成しますか?', self.ui_window.ui_window_id):
            return

        model_dir_regex = re.compile(r'scenes(/hair|)/mdl_chr[0-9]{4}_[0-9]{2}(_hair[0-9]{3}|)_ear_target.ma$')

        # 範囲が広いとファイルのリストに時間がかかり無反応に思えるのでメッセージを表示
        om.MGlobal.displayInfo('対象ファイルをリスト中...')

        target_dir_path = self.ui_create_ear_target_rig_selector.get_path()
        target_file_path_list = []
        for root, dirs, files in os.walk(target_dir_path):
            for filename in files:
                file_full_path = os.path.join(root, filename).replace('\\', '/')
                if not model_dir_regex.search(file_full_path):
                    continue
                target_file_path_list.append(file_full_path)   # ファイルのみ再帰でいい場合はここまででOK

        if not target_file_path_list:
            cmds.confirmDialog(title='Confirm',
                               message='対象ファイルがありませんでした            ',
                               button=['OK'])
            return

        om.MGlobal.displayInfo('')
        base_utility.simple_batch2.execute_mayabatch(
            'Project_Gallop.glp_chara_facial_tool.main',
            'batch(\'create_ear_target_rig_ma\')',
            False,
            target_file_path_list=target_file_path_list)

        base_utility.ui.dialog.open_ok('完了', 'ear_target用のリグアタッチモデルの出力が完了しました')

    # ==================================================
    def batch_create_ear_target_rig_ma(self):

        kwargs = base_utility.simple_batch2.get_kwargs()
        target_file_path_list = []
        if kwargs:
            target_file_path_list = kwargs['target_file_path_list']

        if not target_file_path_list:
            print('対象ファイルがありませんでした'.encode('shift-jis'))
            return

        for target_file_path in target_file_path_list:

            self.create_ear_target_rig_ma(target_file_path, True)

    # ==================================================
    def optimize_node(self, true_option_list):

        option_list = [
            'nurbsSrfOption', 'nurbsCrvOption', 'unusedNurbsSrfOption', 'locatorOption', 'ptConOption',
            'pbOption', 'deformerOption', 'unusedSkinInfsOption', 'expressionOption', 'groupIDnOption',
            'animationCurveOption', 'clipOption', 'poseOption', 'snapshotOption', 'unitConversionOption',
            'shaderOption', 'cachedOption', 'transformOption', 'displayLayerOption', 'renderLayerOption',
            'setsOption', 'partitionOption', 'referencedOption', 'brushOption', 'shadingNetworksOption',
            'unknownNodesOption'
        ]

        option_value_dict = {}

        # optionを設定
        for option in option_list:

            option_value_dict[option] = cmds.optionVar(q=option)
            if option in true_option_list:
                cmds.optionVar(intValue=(option, 1))
            else:
                cmds.optionVar(intValue=(option, 0))

        # 最適化
        mel.eval('OptimizeScene;')

        # 元に戻す
        for option in option_list:

            cmds.optionVar(intValue=(option, option_value_dict[option]))

# endregion

# region ドリブンキー更新

    # ==================================================
    def update_ctrl_rig_from_ui(self, is_batch, use_ui_target_list=False):
        """
        _Ctrl_Rig.maの更新
        80_3D/03_motion/Chara/キャラID_00 に md_キャラID_Ctrl_RIG.ma を書き出す。
        """

        if not base_utility.ui.dialog.open_ok_cancel(
                '確認', 'Ctrl_RIGを作成・更新しますか？', self.ui_window.ui_window_id):
            return

        if is_batch:
            # 範囲が広いとファイルのリストに時間がかかり無反応に思えるのでメッセージを表示
            om.MGlobal.displayInfo('対象ファイルをリスト中...')
        else:
            # get_target_file_path_list_from_selectorは現在のシーンのファイル名のチェックをしないので
            # バッチ処理に行く前にチェック
            target_file_path = cmds.file(q=True, sn=True)
            if target_file_path.find('_facial_target') < 0 and \
                    target_file_path.find('_Ctrl_RIG') < 0:
                cmds.warning('「_facial_target」か「_Ctrl_RIG」のシーンが対象です')
                return

        target_file_path_list = []

        # ターゲットリストの使用が指定された場合はそちらを使用する
        if use_ui_target_list:
            target_file_path_list = [path for path, _ in self.ctrl_rig_target_list or []]
        else:
            # パスチェックはfacial_ctrl_rig_creatorのcreateの__check_path でもう一回される
            target_file_path_list = self.get_target_file_path_list_from_selector(
                self.ui_update_ctrl_rig_selector, is_batch, is_create_temp=False)

        if not target_file_path_list:
            cmds.confirmDialog(title='Confirm',
                               message='対象ファイルがありませんでした            ',
                               button=['OK'])
            return

        folder_path = self.ui_update_ctrl_rig_selector.get_path()

        om.MGlobal.displayInfo('')
        base_utility.simple_batch2.execute_mayabatch(
            'Project_Gallop.glp_chara_facial_tool.main',
            'batch(\'update_ctrl_rig\')',
            False,
            target_file_path_list=target_file_path_list,
            folder_path=folder_path)

    # ==================================================
    def batch_update_ctrl_rig(self):
        kwargs = base_utility.simple_batch2.get_kwargs()
        target_file_path_list = []
        folder_path = ''
        if kwargs:
            target_file_path_list = kwargs['target_file_path_list']
            folder_path = kwargs['folder_path']

        if not target_file_path_list:
            print('対象ファイルがありませんでした'.encode('shift-jis'))
            return

        for target_file_path in target_file_path_list:
            self.update_ctrl_rig(target_file_path, folder_path)

    # ==================================================
    def update_ctrl_rig(self, target_file_path, folder_path):

        this_creator = facial_ctrl_rig_creator.FacialCtrlRigCreator()
        this_creator.create(target_file_path, folder_path)

    def check_facial_target_state(self):
        """facial_targetの更新状態を確認する
        """

        if not base_utility.ui.dialog.open_ok_cancel(
                '確認', 'facial_targetの更新状態を確認しますか？', self.ui_window.ui_window_id):
            return

        folder_path = self.ui_update_ctrl_rig_selector.get_path()

        target_file_path_list = self.get_target_file_path_list_from_selector(
            self.ui_update_ctrl_rig_selector, True, False)

        self.ctrl_rig_state_list = []
        self.ctrl_rig_target_list = []

        base_utility.ui.progressbar.start('更新チェック')

        target_count = len(target_file_path_list)

        for i, path in enumerate(target_file_path_list):
            if not base_utility.ui.progressbar.update('', i, target_count, 1, 1):
                break
            state = facial_ctrl_rig_creator.FacialCtrlRigCreator.get_target_update_state(path, folder_path)
            self.ctrl_rig_state_list.append((path, state))

        base_utility.ui.progressbar.end()

        self.update_facial_target_state_ui()

    def update_facial_target_state_ui(self):
        """facial_targetの更新状態UIを更新する
        """

        filtered_state_list, _ = self.get_filtered_facial_target_state_list()

        state_list = ['{}: {}'.format(os.path.basename(path), state) for path, state in filtered_state_list]
        target_list = ['{}: {}'.format(os.path.basename(path), state) for path, state in self.ctrl_rig_target_list or []]

        self.ui_update_ctrl_rig_state_list.set_item_list(state_list)
        self.ui_update_ctrl_rig_state_list.deselect_all_item()
        self.ui_update_ctrl_rig_target_list.set_item_list(target_list)
        self.ui_update_ctrl_rig_target_list.deselect_all_item()

    def move_facial_target_state(self, to_target, is_all):
        """facial_targetの更新状態をリスト間で移動する

        Args:
            to_target (bool): Trueなら更新状態リスト -> バッチ対象リストへの移動 Falseなら逆
            is_all (bool): リストのすべての項目を移動するか
        """

        if self.ctrl_rig_state_list is None or self.ctrl_rig_target_list is None:
            return

        if to_target:
            filtered_state_list, excluded_state_list = self.get_filtered_facial_target_state_list()

            if is_all:
                self.ctrl_rig_state_list = excluded_state_list
                self.ctrl_rig_target_list = sorted(self.ctrl_rig_target_list + filtered_state_list, key=lambda x: x[0])
            else:
                selected_index_list = self.ui_update_ctrl_rig_state_list.selected_index_list
                selected_state_list = [state for i, state in enumerate(filtered_state_list) if i in selected_index_list]
                unselected_state_list = [state for i, state in enumerate(filtered_state_list) if i not in selected_index_list]
                self.ctrl_rig_state_list = sorted(excluded_state_list + unselected_state_list, key=lambda x: x[0])
                self.ctrl_rig_target_list = sorted(self.ctrl_rig_target_list + selected_state_list, key=lambda x: x[0])
        else:
            if is_all:
                self.ctrl_rig_state_list = sorted(self.ctrl_rig_state_list + self.ctrl_rig_target_list, key=lambda x: x[0])
                self.ctrl_rig_target_list = []
            else:
                selected_index_list = self.ui_update_ctrl_rig_target_list.selected_index_list
                selected_state_list = [state for i, state in enumerate(self.ctrl_rig_target_list) if i in selected_index_list]
                unselected_state_list = [state for i, state in enumerate(self.ctrl_rig_target_list) if i not in selected_index_list]
                self.ctrl_rig_state_list = sorted(self.ctrl_rig_state_list + selected_state_list, key=lambda x: x[0])
                self.ctrl_rig_target_list = unselected_state_list

        self.update_facial_target_state_ui()

    def get_filtered_facial_target_state_list(self):
        """フィルタリングしたfacial_targetの更新状態リストを取得する

        Returns:
            tuple[list[tuple[str, str]], list[tuple[str, str]]]: フィルタリングした項目リストと除外した項目リストのタプル
        """

        state_list = self.ctrl_rig_state_list or []

        filtered_state_list = state_list
        excluded_state_list = []

        # 有効な更新状態フィルタを取得
        enable_filter_list = [label for label, button in self.ui_update_ctrl_rig_state_filter_list if button.get_value()]
        if enable_filter_list:
            filtered_state_list = [(path, state) for path, state in state_list if state in enable_filter_list]
            excluded_state_list = [(path, state) for path, state in state_list if state not in enable_filter_list]

        return filtered_state_list, excluded_state_list

# endregion

# region その他

    # ==================================================
    def get_target_file_path_list_from_selector(self, selector, is_batch,
                                                is_create_temp):
        """
        selector: base_common.classes.ui.data_selector.DataSelector
        is_create_temp がTrueの時は____temp_xxx.maがついたファイルを作成しそのパスが返る。
        """
        target_file_path_list = None
        if is_batch:
            target_file_path_list = selector.get_data_path_list()
            tmp_file_paths = []
            if is_create_temp:
                for path in target_file_path_list:
                    temp_file_path = base_utility.file.create_temp(path)
                    if temp_file_path:
                        tmp_file_paths.append(temp_file_path)
                target_file_path_list = tmp_file_paths
        else:
            target_file_path = cmds.file(q=True, sn=True)
            if target_file_path:
                if is_create_temp:
                    temp_file_path = base_utility.file.create_temp(target_file_path)
                    if temp_file_path:
                        target_file_path = temp_file_path
                target_file_path_list = [target_file_path]
        return target_file_path_list

    # ===============================================
    def apply_euler_filter(self):

        all_target_list = cmds.ls(typ='joint', fl=True, l=True)
        all_target_list.extend(cmds.ls(typ='transform', fl=True, l=True))

        if not all_target_list:
            return None

        target_list = []
        target_attr_list = []
        tmp_frame_time_list = []
        tmp_cut_time_list = []
        last_time = 0
        result = None

        for target in all_target_list:

            if target.find('|Neck') < 0:
                continue

            this_target_name = target.split('|')[-1]

            this_last_time = None
            has_keyframe = False

            if not cmds.keyframe('{}.rotateX'.format(target), q=True, keyframeCount=True) == 0:
                has_keyframe = True
                target_attr_list.append(this_target_name + '_rotateX')
                this_last_time = cmds.findKeyframe('{}.rotateX'.format(target), which='last')
            if not cmds.keyframe('{}.rotateY'.format(target), q=True, keyframeCount=True) == 0:
                has_keyframe = True
                target_attr_list.append(this_target_name + '_rotateY')
                this_last_time = cmds.findKeyframe('{}.rotateX'.format(target), which='last')
            if not cmds.keyframe('{}.rotateZ'.format(target), q=True, keyframeCount=True) == 0:
                has_keyframe = True
                target_attr_list.append(this_target_name + '_rotateZ')
                this_last_time = cmds.findKeyframe('{}.rotateX'.format(target), which='last')

            if this_last_time and this_last_time > last_time:
                last_time = this_last_time

            if has_keyframe:
                target_list.append(target)

        if not last_time:
            return result

        # filterで振り切ってしまうことがあるため、間に0キーを挿入
        for time in range(int(last_time)):
            tmp_frame_time_list.append(time + 0.5)
            tmp_cut_time_list.append((time + 0.5, time + 0.5))

        cmds.setKeyframe(target_list, at=['rx', 'ry', 'rz'], v=0, t=tmp_frame_time_list)

        # filter実行
        # pythonコマンドが動かないことがあったためmelコマンドを使用する
        target_attr_str = ' '.join(target_attr_list)
        result = mel.eval('filterCurve {}'.format(target_attr_str))

        # 挿入した0キーを除去
        cmds.cutKey(target_list, at=['rx', 'ry', 'rz'], t=tmp_cut_time_list, option='keys')

        return result

    # ===============================================
    def transfer_local_pivot_to_translate(self, target):

        if self.__has_locked_translate(target):
            return

        if self.__has_skin_obj(target):
            return

        # ローカルピボットとトランスレートから原点からのベクトルと原点へのベクトルを計算
        pivs = cmds.xform(target, q=True, piv=True)[:3]
        trans = cmds.xform(target, q=True, t=True)
        sum_trans = [pivs[0] + trans[0], pivs[1] + trans[1], pivs[2] + trans[2]]
        inv_trans = [-sum_trans[0], -sum_trans[1], -sum_trans[2]]

        # 原点でフリーズしてローカルピボットの値をトランスレートにいれる
        cmds.xform(target, r=True, t=inv_trans)
        cmds.makeIdentity(target, a=True, t=True)
        cmds.xform(target, r=True, t=sum_trans)

    # ===============================================
    def __has_locked_translate(self, target):

        all_transform = [target]
        add_transform = cmds.listRelatives(target, ad=True, type='transform', f=True)

        if add_transform:
            all_transform.extend(add_transform)

        for transform in all_transform:

            locked_attr_list = cmds.listAttr(transform, locked=True)

            if not locked_attr_list:
                continue

            for attr in locked_attr_list:
                if attr.endswith('translateX') or attr.endswith('translateY') or attr.endswith('translateZ'):
                    return True

        return False

    # ===============================================
    def __has_skin_obj(self, target):

        all_child_list = [target]
        add_child_list = cmds.listRelatives(target, ad=True, f=True)

        if add_child_list:
            all_child_list.extend(add_child_list)

        for child in all_child_list:

            if cmds.objectType(child) == 'joint':
                return True

            node_list = cmds.listHistory(child)

            if not node_list:
                continue

            for node in node_list:
                if node.find('skinCluster') >= 0:
                    return True

        return False

# endregion
