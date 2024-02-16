# -*- coding: utf-8 -*-
u"""
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
    from builtins import object
    from builtins import range
    from importlib import reload
except Exception:
    pass

import sys
import os

import maya.cmds as cmds
import maya.mel as mel

import shiboken2

from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui
from maya.app.general import mayaMixin
from maya import OpenMayaUI

from . import view
from . import light_map_maker
from . import bake_setting
from . import preview
from . import tool_define
from . import tool_utility
from . import export_model

reload(view)
reload(light_map_maker)
reload(bake_setting)
reload(preview)
reload(tool_define)
reload(tool_utility)
reload(export_model)


class Main(object):

    def __init__(self):
        """コンストラクタ
        """

        self.tool_name = 'GlpLightmapMaker'
        self.tool_version = '23090101'

        self.view = view.View()
        self.view.setWindowTitle(self.tool_name + self.tool_version)
        self.tb_setting = view.TextureSettingWidget(self.view)
        self.vb_setting = view.VerticesSettingWidget(self.view)

        self.lmm = light_map_maker.LightMapMaker()
        self.lmm.initialize()

        script_dir = os.path.dirname(os.path.realpath(__file__))
        icon_dir = os.path.join(script_dir, 'ui', 'icon')

        self.icon_texture_pixmap = QtGui.QPixmap(os.path.join(icon_dir, 'texture.png'))
        self.icon_vertex_color_pixmap = QtGui.QPixmap(os.path.join(icon_dir, 'vertex_color.png'))
        self.icon_delete_pixmap = QtGui.QPixmap(os.path.join(icon_dir, 'delete.png'))
        self.icon_info_pixmap = QtGui.QPixmap(os.path.join(icon_dir, 'info.png'))
        self.icon_rename_pixmap = QtGui.QPixmap(os.path.join(icon_dir, 'rename.png'))
        self.icon_add_pixmap = QtGui.QPixmap(os.path.join(icon_dir, 'add.png'))
        self.icon_remove_pixmap = QtGui.QPixmap(os.path.join(icon_dir, 'remove.png'))
        self.icon_on_preview = QtGui.QPixmap(os.path.join(icon_dir, 'on_preview.png'))
        self.icon_not_preview = QtGui.QPixmap(os.path.join(icon_dir, 'not_preview.png'))

    def deleteOverlappingWindow(self, target):
        """Windowの重複削除処理
        """

        main_window = OpenMayaUI.MQtUtil.mainWindow()
        if main_window is None:
            return

        if sys.version_info.major == 2:
            main_window = shiboken2.wrapInstance(long(main_window), QtWidgets.QMainWindow)
        else:
            # for Maya 2022-
            main_window = shiboken2.wrapInstance(int(main_window), QtWidgets.QMainWindow)

        for widget in main_window.children():
            if str(type(target)) == str(type(widget)):
                widget.deleteLater()

    def show_ui(self):
        """UI描画
        """

        # windowの重複削除処理
        self.deleteOverlappingWindow(self.view)

        self.initialize_ui()
        self.setup_view_event()
        self.setup_texture_setting_widget_event()
        self.setup_vertex_setting_widget_event()
        self.__update_bake_layer_node_list()
        self.view.show()

    def initialize_ui(self):
        """UIの初期設定
        """

        self.view.ui.create_bake_layer_label.setText(tool_define.BAKE_LAYER_PREFIX)

        self.view.ui.info_bake_setting_area.setMinimumHeight(130)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        self.tex_bake_setting_area = QtWidgets.QScrollArea(self.view.ui.groupBox_3)
        self.tex_bake_setting_area.setWidgetResizable(True)
        self.tex_bake_setting_area.setSizePolicy(sizePolicy)
        self.view.ui.setting_vertical_layout.addWidget(self.tex_bake_setting_area)
        self.tex_bake_setting_area.setWidget(self.tb_setting)
        self.tex_bake_setting_area.setMinimumHeight(130)
        self.tex_bake_setting_area.setMaximumHeight(130)
        self.tex_bake_setting_area.hide()

        self.vtx_bake_setting_area = QtWidgets.QScrollArea(self.view.ui.groupBox_3)
        self.vtx_bake_setting_area.setWidgetResizable(True)
        self.vtx_bake_setting_area.setSizePolicy(sizePolicy)
        self.view.ui.setting_vertical_layout.addWidget(self.vtx_bake_setting_area)
        self.vtx_bake_setting_area.setWidget(self.vb_setting)
        self.vtx_bake_setting_area.setMinimumHeight(130)
        self.vtx_bake_setting_area.setMaximumHeight(130)
        self.vtx_bake_setting_area.hide()

        self.view.ui.bake_layer_create_button.setIcon(self.icon_add_pixmap)
        self.view.ui.bake_obj_add_button.setText('')

        self.view.ui.bake_obj_add_button.setIcon(self.icon_add_pixmap)
        self.view.ui.bake_obj_add_button.setText('')

        self.view.ui.bake_obj_rem_button.setIcon(self.icon_remove_pixmap)
        self.view.ui.bake_obj_rem_button.setText('')

        self.view.ui.bake_type_tex_radio.setIcon(self.icon_texture_pixmap)
        self.view.ui.bake_type_vtx_radio.setIcon(self.icon_vertex_color_pixmap)

        self.view.ui.add_fbx_export_button.setIcon(self.icon_add_pixmap)
        self.view.ui.add_fbx_export_button.setText('')

        self.view.ui.rem_fbx_export_button.setIcon(self.icon_remove_pixmap)
        self.view.ui.rem_fbx_export_button.setText('')

    def setup_view_event(self):
        """UIのevent設定
        """

        self.view.addCallback('SceneOpened', self.scene_change_event)

        self.view.ui.bake_layer_create_button.clicked.connect(self.bake_layer_create_button_event)
        self.view.ui.bake_obj_add_button.clicked.connect(self.bake_obj_add_button_event)
        self.view.ui.bake_obj_rem_button.clicked.connect(self.bake_obj_rem_button_event)

        self.view.ui.bake_layer_node_custom_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.view.ui.bake_layer_node_custom_list.itemSelectionChanged.connect(self.bake_layer_node_list_select_event)

        self.view.ui.bake_obj_node_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.view.ui.bake_obj_node_list.itemSelectionChanged.connect(self.bake_obj_node_list_select_event)

        self.view.ui.bake_type_tex_radio.toggled.connect(self.bake_type_radio_event)
        self.view.ui.bake_type_vtx_radio.toggled.connect(self.bake_type_radio_event)

        self.view.ui.light_set_line.textEdited.connect(self.light_set_line_change_event)
        self.view.ui.light_set_select_button.clicked.connect(self.light_set_select_button_event)

        self.view.ui.open_render_setting_button.clicked.connect(self.open_render_setting_button_event)

        self.view.ui.exe_bake_button.clicked.connect(self.exe_bake_button_event)
        self.view.ui.exe_test_bake_button.clicked.connect(self.exe_test_bake_button_event)

        self.view.ui.add_fbx_export_button.clicked.connect(self.add_fbx_export_button_event)
        self.view.ui.rem_fbx_export_button.clicked.connect(self.rem_fbx_export_button_event)
        self.view.ui.export_fbx_button.clicked.connect(self.export_fbx_button_event)

    def setup_texture_setting_widget_event(self):
        """setup_texture_setting_widgetのevent設定
        """

        self.tb_setting.ui.uv_set_line.textEdited.connect(self.tex_uv_setting_change_event)
        self.tb_setting.ui.tex_x_line.textEdited.connect(self.tex_res_setting_change_event)
        self.tb_setting.ui.test_tex_x_line.textEdited.connect(self.tex_test_res_setting_change_event)
        self.tb_setting.ui.tex_y_line.textEdited.connect(self.tex_res_setting_change_event)
        self.tb_setting.ui.test_tex_y_line.textEdited.connect(self.tex_test_res_setting_change_event)

        self.tb_setting.ui.update_uv_set_button.clicked.connect(self.update_uv_set_button_event)
        self.tb_setting.ui.layout_uvs_button.clicked.connect(self.layout_uvs_button_event)

        self.tb_setting.ui.tex_name_line.textEdited.connect(self.tex_name_setting_change_event)

    def setup_vertex_setting_widget_event(self):
        """setup_vertex_setting_widgetのevent設定
        """

        self.vb_setting.ui.bake_colort_set_line.setReadOnly(True)
        self.vb_setting.ui.open_colorset_editor_button.clicked.connect(self.open_colorset_editor_button_event)
        self.vb_setting.ui.ray_min_line.textEdited.connect(self.vtx_setting_change_event)
        self.vb_setting.ui.ray_max_line.textEdited.connect(self.vtx_setting_change_event)

    def scene_change_event(self, arg=None):
        """シーン切り替え時イベント
        """

        self.__update_bake_layer_node_list()
        self.__update_bake_obj_node_list()
        self.view.ui.fbx_export_list.clear()
        self.view.ui.fbx_export_suffix_line.setText('')

    def bake_layer_create_button_event(self):
        """ベイクレイヤー作成ボタンイベント
        """

        base_name = self.view.ui.bake_layer_suffix_line.text()

        if not base_name:
            cmds.warning('no name input')
            return

        new_bake_layer = self.lmm.create_new_bake_layer(base_name)

        # UI更新
        self.__update_bake_layer_node_list()

        # 作成されたベイクレイヤーが選択されるようにする
        if new_bake_layer:
            item_count = self.view.ui.bake_layer_node_custom_list.count()

            for i in range(item_count):
                this_item = self.view.ui.bake_layer_node_custom_list.item(i)
                item_widget = self.view.ui.bake_layer_node_custom_list.itemWidget(this_item)
                if item_widget.bake_layer_label.text() == new_bake_layer:
                    self.view.ui.bake_layer_node_custom_list.setItemSelected(this_item, True)
                else:
                    self.view.ui.bake_layer_node_custom_list.setItemSelected(this_item, False)

    def bake_layer_rename_button_event(self, bake_layer_item):
        """リネームボタンイベント

        Args:
            bake_layer_item (BakeLayerListItem): ベイクレイヤーリスト用のリストアイテムwidget
        """

        target_bake_layer = bake_layer_item.bake_layer_label.text()

        if not cmds.objExists(target_bake_layer):
            cmds.warning('no bake_layer: {}'.format(target_bake_layer))
            return

        # ユーザー入力を受付
        this_base_name = bake_layer_item.bake_layer_label.text().replace(tool_define.BAKE_LAYER_PREFIX, '')
        text, okPressed = QtWidgets.QInputDialog.getText(self.view, 'ベイクレイヤー名の変更', '新規ベイクレイヤー名:', QtWidgets.QLineEdit.Normal, this_base_name)

        if not okPressed or not text:
            return

        new_name = tool_define.BAKE_LAYER_PREFIX + text

        if cmds.objExists(new_name):
            cmds.warning('already exists: {}'.format(new_name))
            return

        # リネームを実行
        result_name = self.lmm.rename_bake_layer(target_bake_layer, new_name)
        bake_layer_item.bake_layer_label.setText(result_name)

        # UI更新
        self.__update_bake_layer_node_list()
        self.__update_bake_obj_node_list()

    def bake_layer_info_button_event(self, bake_layer_item):
        """情報ボタンイベント

        Args:
            bake_layer_item (BakeLayerListItem): ベイクレイヤーリスト用のリストアイテムwidget
        """

        target_bake_layer = bake_layer_item.bake_layer_label.text()

        if not cmds.objExists(target_bake_layer):
            cmds.warning('no bake_layer: {}'.format(target_bake_layer))
            return

        info_text_list = []

        if bake_setting.get_bake_type(target_bake_layer) == 1:

            this_texture = tool_utility.generate_conbine_texture_name(target_bake_layer)
            info_text_list.append(u'ベイクするテクスチャ: {}'.format(this_texture))

            this_uv_set = bake_setting.get_texture_bake_uv(target_bake_layer)
            info_text_list.append(u'ベイクで使用するUV: {}'.format(this_uv_set))

            this_material = tool_utility.generate_bake_material_name(target_bake_layer, u'BASE_MATERIAL')
            info_text_list.append(u'ベイクマテリアル: {}'.format(this_material))

        this_colorset = tool_utility.generate_bake_colorset_name(target_bake_layer)
        info_text_list.append(u'ベイクするカラーセット: {}'.format(this_colorset))

        this_lightset = bake_setting.get_light_set(target_bake_layer)
        info_text_list.append(u'使用するライトセット: {}'.format(this_lightset))

        cmds.confirmDialog(title=target_bake_layer + 'info', message='\n'.join(info_text_list))

    def bake_item_rem_button_event(self, bake_layer):
        """ベイクレイヤー削除ボタンイベント

        Args:
            bake_layer (str): 削除するベイクレイヤー
        """

        if preview.is_on_preview(bake_layer):
            preview.show_default(bake_layer)
        self.lmm.delete_bake_layers([bake_layer])

        # UI更新
        self.__update_bake_layer_node_list()
        self.__update_bake_obj_node_list()

    def preview_toggle_button_event(self, bake_layer):
        """ベイクレイヤー表示ボタンイベント

        Args:
            bake_layer (str): 表示するベイクレイヤー
        """

        if preview.is_on_preview(bake_layer):
            preview.show_default(bake_layer)
        else:
            preview.show_preview(bake_layer)

        self.__update_bake_layer_icon()

    def bake_obj_add_button_event(self):
        """レンダーターゲットサーフェイス追加ボタンイベント
        """

        selection_list = cmds.ls(sl=True, type='transform')
        selection_list.extend(cmds.ls(sl=True, type='mesh'))
        bake_layer_list = self.__get_selection_list_from_bake_layer_list(self.view.ui.bake_layer_node_custom_list)

        if not selection_list or not bake_layer_list:
            return

        for bake_layer in bake_layer_list:
            self.lmm.add_bake_target(bake_layer, selection_list)

        # UI更新
        self.__update_bake_obj_node_list()
        self.__update_bake_setting_area()

    def bake_obj_rem_button_event(self):
        """レンダーターゲットサーフェイス削除ボタンイベント
        """

        bake_layer_list = self.__get_selection_list_from_bake_layer_list(self.view.ui.bake_layer_node_custom_list)
        del_obj_list = self.__get_selection_list_from_list_widget(self.view.ui.bake_obj_node_list)

        if not bake_layer_list or not del_obj_list:
            return

        for bake_layer in bake_layer_list:
            self.lmm.delete_bake_target(bake_layer, del_obj_list)

        # UI更新
        self.__update_bake_obj_node_list()
        self.__update_bake_setting_area()

    def bake_layer_node_list_select_event(self):
        """ベイクレイヤーリスト選択時イベント
        """

        bake_layer_list = self.__get_selection_list_from_bake_layer_list(self.view.ui.bake_layer_node_custom_list)

        if bake_layer_list:
            # 確認しやすいようにMayaのレンダリング設定も変更しておく
            self.lmm.apply_bake_layer(bake_layer_list[-1])
            # 連続作成しやすいように作成欄にも表示しておく
            bake_layer_suffix = tool_utility.slice_bake_layer_suffix(bake_layer_list[-1])
            self.view.ui.bake_layer_suffix_line.setText(bake_layer_suffix)

        # UI更新
        self.__update_bake_obj_node_list()
        self.__update_bake_setting_area()

    def bake_obj_node_list_select_event(self):
        """レンダーターゲットサーフェイスリスト選択時イベント
        """

        selected_surface_list = self.__get_selection_list_from_list_widget(self.view.ui.bake_obj_node_list)

        if selected_surface_list:
            transform_list = [
                cmds.listRelatives(x, p=True, f=True, type='transform')[0] for x in selected_surface_list if cmds.listRelatives(x, p=True, type='transform')
            ]
            cmds.select(transform_list, r=True)

    def bake_type_radio_event(self):
        """ベイクタイプラジオボタン選択時イベント
        """

        bake_layer_list = self.__get_selection_list_from_bake_layer_list(self.view.ui.bake_layer_node_custom_list)

        # 対象のベイクレイヤーが選択されていない場合は処理しない
        if bake_layer_list:

            bake_type_num = 1  # BakeToTexture
            if self.view.ui.bake_type_vtx_radio.isChecked():
                bake_type_num = 2  # BakeToVertices

            self.lmm.set_bake_type(bake_layer_list, bake_type_num)

        self.__update_bake_setting_area()
        self.__update_bake_layer_icon()

    def light_set_line_change_event(self):
        """ライトセット変更時イベント
        """

        light_set_input = self.view.ui.light_set_line.text()

        bake_layer_list = self.__get_selection_list_from_bake_layer_list(self.view.ui.bake_layer_node_custom_list)
        for bake_layer in bake_layer_list:
            self.lmm.set_light_set(bake_layer, light_set_input)

    def light_set_select_button_event(self):
        """ライトセット選択ボタンイベント
        """

        light_set_list = cmds.ls(sl=True, type='objectSet')

        if light_set_list:
            self.view.ui.light_set_line.setText(light_set_list[0])

        self.light_set_line_change_event()

    def open_render_setting_button_event(self):
        """レンダーセッティングを開くボタンのイベント
        """

        mel.eval('unifiedRenderGlobalsWindow;')

    def open_colorset_editor_button_event(self):
        """カラーセットエディタ―を開くボタンのイベント
        """

        mel.eval('OpenColorSetEditor;')

    def exe_bake_button_event(self):
        """ベイク実行ボタンのイベント
        """
        self.__exe_bake(False)

    def exe_test_bake_button_event(self):
        """ベイクテスト実行ボタンのイベント
        """
        self.__exe_bake(True)

    def __exe_bake(self, is_test=False):
        """ベイク実行処理
        """

        bake_layer_list = self.__get_selection_list_from_bake_layer_list(self.view.ui.bake_layer_node_custom_list)

        if not bake_layer_list:
            return

        # ベイクレイヤーのメッシュとライトのチェック
        for bake_layer in bake_layer_list:

            member_validation = bake_setting.validate_layer_members(bake_layer)
            if not member_validation:
                cmds.confirmDialog(
                    t=u'ベイクレイヤー:{} エラー'.format(bake_layer),
                    m=u'メンバーにシェイプ以外が指定されていないか確認してください',
                    icn='critical'
                )
                return

            light_validation = bake_setting.validate_lightset(bake_layer)
            if not light_validation:
                light_set = bake_setting.get_light_set(bake_layer) or 'defaultLightSet'
                cmds.confirmDialog(
                    t=u'ベイクレイヤー:{} エラー'.format(bake_layer),
                    m=u'ライトセット:{} にライトがセットされているか確認してください'.format(light_set),
                    icn='critical'
                )
                return

        use_legacy_method = True
        if self.view.ui.output_new_tool_radio.isChecked():
            use_legacy_method = False

        use_gi = self.view.ui.use_gi_check.isChecked()

        # 確認ダイアログを表示
        confirm_message = u'以下のベイクレイヤーに対してベイクを実行します\n'

        for bake_layer in bake_layer_list:
            bake_type_str = u''
            if bake_setting.get_bake_type(bake_layer) == 1:
                bake_type_str = u'テクスチャ'
            elif bake_setting.get_bake_type(bake_layer) == 2:
                bake_type_str = u'頂点カラー'
            confirm_message += bake_layer + ' : ' + bake_type_str + '\n'

        confirm_result = cmds.confirmDialog(
            title=u'ベイク確認',
            message=confirm_message,
            button=['Yes', 'No'],
            cancelButton='No',
            dismissString='No'
        )

        if confirm_result == 'No':
            return

        # プログレスバーを表示
        progress_window = cmds.window(title=u'ライトマップベイク')
        cmds.columnLayout(adjustableColumn=True)
        cmds.text(label=u'ベイク実行中', align='center')
        progress_control = cmds.progressBar(width=300, maxValue=len(bake_layer_list))
        cmds.showWindow(progress_window)

        # ベイク実行
        self.lmm.bake_by_bake_layer(bake_layer_list, use_legacy_method, use_gi, is_test, progress_control)
        self.__update_bake_layer_icon()

        # プログレスバーの削除と完了通知
        cmds.deleteUI(progress_window)
        cmds.confirmDialog(message=u'ベイク完了')

    def tex_uv_setting_change_event(self):
        """テクスチャベイク設定のUV設定変更時イベント
        """

        uv_set = self.tb_setting.ui.uv_set_line.text()

        # ベイクレイヤーに設定を反映
        bake_layer_list = self.__get_selection_list_from_bake_layer_list(self.view.ui.bake_layer_node_custom_list)
        self.lmm.set_texture_bake_uv(bake_layer_list, uv_set)

    def tex_res_setting_change_event(self):
        """テクスチャベイク設定の解像度設定変更時イベント
        """

        res_x = int(self.tb_setting.ui.tex_x_line.text()) if self.tb_setting.ui.tex_x_line.text() else 1
        res_y = int(self.tb_setting.ui.tex_y_line.text()) if self.tb_setting.ui.tex_y_line.text() else 1

        # テスト解像度を入力に合わせて変更
        test_res_x = self.__get_test_bake_size(res_x)
        test_res_y = self.__get_test_bake_size(res_y)
        self.tb_setting.ui.test_tex_x_line.setText(str(test_res_x))
        self.tb_setting.ui.test_tex_y_line.setText(str(test_res_y))

        # ベイクレイヤーに設定を反映
        bake_layer_list = self.__get_selection_list_from_bake_layer_list(self.view.ui.bake_layer_node_custom_list)
        self.lmm.set_texture_bake_res(bake_layer_list, res_x, res_y)
        self.lmm.set_texture_bake_test_res(bake_layer_list, test_res_x, test_res_y)

    def tex_test_res_setting_change_event(self):
        """テクスチャベイク設定のテスト解像度設定変更時イベント
        """

        test_res_x = int(self.tb_setting.ui.test_tex_x_line.text()) if self.tb_setting.ui.test_tex_x_line.text() else 1
        test_res_y = int(self.tb_setting.ui.test_tex_y_line.text()) if self.tb_setting.ui.test_tex_y_line.text() else 1

        # ベイクレイヤーに設定を反映
        bake_layer_list = self.__get_selection_list_from_bake_layer_list(self.view.ui.bake_layer_node_custom_list)
        self.lmm.set_texture_bake_test_res(bake_layer_list, test_res_x, test_res_y)

    def tex_name_setting_change_event(self):
        """テクスチャベイク設定のテクスチャ名設定変更時イベント
        """

        tex_name = self.tb_setting.ui.tex_name_line.text()

        # ベイクレイヤーに設定を反映
        bake_layer_list = self.__get_selection_list_from_bake_layer_list(self.view.ui.bake_layer_node_custom_list)

        if bake_layer_list:
            self.lmm.set_texture_name(bake_layer_list[0], tex_name)

    def vtx_setting_change_event(self):
        """テクスチャベイク設定変更時イベント
        """

        ray_min = int(self.vb_setting.ui.ray_min_line.text())
        ray_max = int(self.vb_setting.ui.ray_max_line.text())
        ray_test_min = int(self.vb_setting.ui.test_ray_min_line.text())
        ray_test_max = int(self.vb_setting.ui.test_ray_max_line.text())

        # ベイクレイヤーに設定を反映
        bake_layer_list = self.__get_selection_list_from_bake_layer_list(self.view.ui.bake_layer_node_custom_list)

        self.lmm.set_ray_min_max_value(bake_layer_list, [ray_min, ray_max])
        self.lmm.set_test_ray_min_max_value(bake_layer_list, [ray_test_min, ray_test_max])

    def update_uv_set_button_event(self):
        """UVセットを追加ボタンのイベント
        """

        bake_layer_list = self.__get_selection_list_from_bake_layer_list(self.view.ui.bake_layer_node_custom_list)
        uv_set = self.tb_setting.ui.uv_set_line.text()

        if not bake_layer_list or not uv_set:
            return

        shape_list = []

        for bake_layer in bake_layer_list:
            this_shapes = cmds.sets(bake_layer, q=True)
            if this_shapes:
                shape_list.extend(this_shapes)

        confirm_message = ''

        for shape in shape_list:
            confirm_message += shape + '\n'

        confirm_message += u'上記シェイプのUVセット {} を再展開します。\nUVセットが存在していない場合は生成され展開されます。'.format(uv_set)

        confirm_result = cmds.confirmDialog(
            title=u'UVセットの更新',
            message=confirm_message,
            button=['Yes', 'No'],
            cancelButton='No',
            dismissString='No')

        if confirm_result == 'No':
            return

        self.lmm.create_uv_set(bake_layer_list, uv_set)
        self.lmm.projection_uv(bake_layer_list, uv_set)

    def layout_uvs_button_event(self):
        """UVを再配置ボタンのイベント
        """

        bake_layer_list = self.__get_selection_list_from_bake_layer_list(self.view.ui.bake_layer_node_custom_list)
        uv_set = self.tb_setting.ui.uv_set_line.text()

        if not bake_layer_list or not uv_set:
            return

        shape_list = []

        for bake_layer in bake_layer_list:
            this_shapes = cmds.sets(bake_layer, q=True)
            if this_shapes:
                shape_list.extend(this_shapes)

        confirm_message = ''

        for shape in shape_list:
            confirm_message += shape + '\n'

        confirm_message += u'上記シェイプのUVセット {} の再配置を行います。'.format(uv_set)

        confirm_result = cmds.confirmDialog(
            title=u'UVの再配置',
            message=confirm_message,
            button=['Yes', 'No'],
            cancelButton='No',
            dismissString='No'
        )

        if confirm_result == 'No':
            return

        self.lmm.layout_uvs(bake_layer_list, uv_set)

    def add_fbx_export_button_event(self):
        """FBX出力オブジェクト追加ボタンイベント
        """

        selections = cmds.ls(sl=True, l=True, type='transform')

        if not selections:
            return

        list_texts = self.__get_selection_list_from_list_widget(self.view.ui.fbx_export_list)

        for selection in selections:
            if selection not in list_texts:
                this_item = QtWidgets.QListWidgetItem(selection)
                self.view.ui.fbx_export_list.addItem(this_item)

    def rem_fbx_export_button_event(self):
        """FBX出力オブジェクト削除ボタンイベント
        """

        selections = self.view.ui.fbx_export_list.selectedItems()

        for item in selections:

            this_row = self.view.ui.fbx_export_list.row(item)
            self.view.ui.fbx_export_list.takeItem(this_row)
            self.view.ui.fbx_export_list.removeItemWidget(item)

    def export_fbx_button_event(self):
        """FBX出力ボタンイベント
        """

        scene_dir = cmds.file(q=True, sn=True)
        scene_dir = os.path.dirname(os.path.dirname(scene_dir))
        export_dir = os.path.join(scene_dir, tool_define.FBX_OUTPUT_DIRNAME)

        if not scene_dir:
            confirm_result = cmds.confirmDialog(
                title=u'エラー',
                message=u'シーンパスが取得できません。一度保存してください。')
            return

        # 確認画面表示
        confirm_message = export_dir + u'\nに以下のモデルを出力します\n'

        for row in range(self.view.ui.fbx_export_list.count()):

            target = self.view.ui.fbx_export_list.item(row).text()

            if not cmds.objExists(target):
                continue

            file_name = target.split('|')[-1].split('__')[0] + '.fbx'

            suffix = self.view.ui.fbx_export_suffix_line.text()
            if suffix:
                file_name = target.split('|')[-1].split('__')[0] + '_' + suffix + '.fbx'

            confirm_message += file_name + '\n'

        confirm_result = cmds.confirmDialog(
            title=u'FBX出力確認',
            message=confirm_message,
            button=['Yes', 'No'],
            cancelButton='No',
            dismissString='No'
        )

        if confirm_result == 'No':
            return

        # FBX出力時にUVやカラーの設定を反映するために現在アクティブになっているベイクレイヤーを取得
        active_bake_layers = []
        item_count = self.view.ui.bake_layer_node_custom_list.count()

        for i in range(item_count):

            list_item = self.view.ui.bake_layer_node_custom_list.item(i)
            this_item = self.view.ui.bake_layer_node_custom_list.itemWidget(list_item)
            bake_layer = this_item.bake_layer_label.text()

            if not cmds.objExists(bake_layer):
                continue
            if preview.is_on_preview(bake_layer):
                active_bake_layers.append(bake_layer)

        # 出力実行
        for row in range(self.view.ui.fbx_export_list.count()):

            target = self.view.ui.fbx_export_list.item(row).text()

            if not cmds.objExists(target):
                continue

            file_name = target.split('|')[-1].split('__')[0] + '.fbx'

            suffix = self.view.ui.fbx_export_suffix_line.text()
            if suffix:
                file_name = target.split('|')[-1].split('__')[0] + '_' + suffix + '.fbx'

            output_path = os.path.join(export_dir, file_name).replace('\\', '/')

            export_model.export_fbx(target, output_path, active_bake_layers)

        confirm_result = cmds.confirmDialog(title=u'FBX出力完了', message=u'出力終了')

    def __update_bake_layer_node_list(self):
        """ベイクレイヤーリストを更新
        """

        # 更新後に復帰するために選択項目を保持
        selected_item_text_list = self.__get_selection_list_from_bake_layer_list(self.view.ui.bake_layer_node_custom_list)

        self.view.ui.bake_layer_node_custom_list.clear()

        bake_layer_list = self.lmm.import_bake_layers()

        for bake_layer in bake_layer_list:

            this_item = QtWidgets.QListWidgetItem(self.view.ui.bake_layer_node_custom_list)
            custom_item = BakeLayerListItem(self, bake_layer, self.view.ui.bake_layer_node_custom_list)

            this_item.setSizeHint(custom_item.sizeHint())
            self.view.ui.bake_layer_node_custom_list.addItem(this_item)
            self.view.ui.bake_layer_node_custom_list.setItemWidget(this_item, custom_item)

        item_count = self.view.ui.bake_layer_node_custom_list.count()

        # 選択項目の復元
        for i in range(item_count):
            this_item = self.view.ui.bake_layer_node_custom_list.item(i)
            item_widget = self.view.ui.bake_layer_node_custom_list.itemWidget(this_item)
            if item_widget.bake_layer_label.text() in selected_item_text_list:
                self.view.ui.bake_layer_node_custom_list.setItemSelected(this_item, True)

        self.__update_bake_layer_icon()

    def __update_bake_layer_icon(self):
        """ベイクレイヤーリストのアイコンを更新
        """

        item_count = self.view.ui.bake_layer_node_custom_list.count()

        for i in range(item_count):

            list_item = self.view.ui.bake_layer_node_custom_list.item(i)
            this_item = self.view.ui.bake_layer_node_custom_list.itemWidget(list_item)
            bake_layer = this_item.bake_layer_label.text()

            if not cmds.objExists(bake_layer):
                continue

            # 1=BakeToTexture, 2=BakeToVertices
            bake_type = bake_setting.get_bake_type(bake_layer)

            is_on_preview = preview.is_on_preview(bake_layer)

            if bake_type == 1:
                if is_on_preview:
                    this_item.set_icon(self.icon_on_preview, self.icon_texture_pixmap)
                else:
                    this_item.set_icon(self.icon_not_preview, self.icon_texture_pixmap)
            elif bake_type == 2:
                if is_on_preview:
                    this_item.set_icon(self.icon_on_preview, self.icon_vertex_color_pixmap)
                else:
                    this_item.set_icon(self.icon_not_preview, self.icon_vertex_color_pixmap)

    def __update_bake_obj_node_list(self):
        """ベイク対象のシェイプリストを更新
        """

        bake_layer_list = self.__get_selection_list_from_bake_layer_list(self.view.ui.bake_layer_node_custom_list)

        # 無選択 or 複数のベイクレイヤーが選択されていた場合はボタン操作できないようにする
        self.view.ui.bake_obj_node_list.clear()
        self.view.ui.bake_obj_add_button.setEnabled(False)
        self.view.ui.bake_obj_rem_button.setEnabled(False)

        if len(bake_layer_list) == 0:
            this_item = QtWidgets.QListWidgetItem(u'ベイクレイヤーが選択されていません')
            self.view.ui.bake_obj_node_list.addItem(this_item)
            return
        elif len(bake_layer_list) > 1:
            this_item = QtWidgets.QListWidgetItem(u'複数ベイクレイヤーが選択されています')
            self.view.ui.bake_obj_node_list.addItem(this_item)
            return

        # ボタンを解放する
        self.view.ui.bake_obj_add_button.setEnabled(True)
        self.view.ui.bake_obj_rem_button.setEnabled(True)

        if not cmds.objExists(bake_layer_list[0]):
            return

        surface_list = cmds.sets(bake_layer_list[0], q=True)

        if not surface_list:
            return

        for surface in surface_list:
            this_item = QtWidgets.QListWidgetItem(surface)
            self.view.ui.bake_obj_node_list.addItem(this_item)

    def __update_bake_setting_area(self):
        """ベイク設定の項目を更新する
        """

        self.view.ui.info_bake_setting_area.hide()
        self.tex_bake_setting_area.hide()
        self.vtx_bake_setting_area.hide()
        self.view.ui.bake_type_tex_radio.setEnabled(False)
        self.view.ui.bake_type_vtx_radio.setEnabled(False)
        self.view.ui.light_set_line.setEnabled(False)
        self.view.ui.light_set_select_button.setEnabled(False)

        bake_layer_list = self.__get_selection_list_from_bake_layer_list(self.view.ui.bake_layer_node_custom_list)

        # 無選択や複数選択では個別の設定を塞ぐ
        if not bake_layer_list:
            self.view.ui.info_bake_setting_area.show()
            self.view.ui.info_bake_setting_label_2.setText(u'ベイクレイヤーが選択されていません')
            return
        elif len(bake_layer_list) > 1:
            self.view.ui.info_bake_setting_area.show()
            self.view.ui.info_bake_setting_label_2.setText(u'複数ベイクレイヤー選択中は設定を変更できません')
            return

        self.view.ui.bake_type_tex_radio.setEnabled(True)
        self.view.ui.bake_type_vtx_radio.setEnabled(True)
        self.view.ui.light_set_line.setEnabled(True)
        self.view.ui.light_set_select_button.setEnabled(True)

        # 1つ選択の場合はそのベイクレイヤーのベイクタイプを反映
        if len(bake_layer_list) == 1:
            bake_type = bake_setting.get_bake_type(bake_layer_list[0])
            if bake_type == 1:  # BakeToTexture
                self.view.ui.bake_type_tex_radio.setChecked(True)
            elif bake_type == 2:  # BakeToVertices
                self.view.ui.bake_type_vtx_radio.setChecked(True)

        if self.view.ui.bake_type_tex_radio.isChecked():
            self.tex_bake_setting_area.show()
        elif self.view.ui.bake_type_vtx_radio.isChecked():
            self.vtx_bake_setting_area.show()

        if not bake_layer_list:
            self.__init_tex_bake_setting(None)
            self.__init_vtx_bake_setting(None)
        else:
            self.__init_tex_bake_setting(bake_layer_list[0])
            self.__init_vtx_bake_setting(bake_layer_list[0])

        if bake_layer_list:
            self.view.ui.light_set_line.setText(bake_setting.get_light_set(bake_layer_list[0]))

    def __init_tex_bake_setting(self, bake_layer=None):
        """テクスチャベイク設定をベイクレイヤーの値で初期化する

        Args:
            bake_layer (str): 初期化に使用するturtleベイクレイヤーノード
        """

        self.tb_setting.ui.uv_set_line.setText('')
        self.tb_setting.ui.uv_set_line.setCompleter(None)
        self.tb_setting.ui.tex_x_line.setText('')
        self.tb_setting.ui.test_tex_x_line.setText('')
        self.tb_setting.ui.tex_y_line.setText('')
        self.tb_setting.ui.test_tex_y_line.setText('')
        self.tb_setting.ui.tex_name_line.setText('')

        if not cmds.objExists(bake_layer):
            return

        res_x_y = bake_setting.get_texture_bake_res(bake_layer)
        test_res_x_y = bake_setting.get_texture_bake_test_res(bake_layer)

        # bake用のturtleの置き換え文字を取り除いたベース名を表示する
        bake_tex_base_name = self.lmm.get_texture_name(bake_layer)

        self.tb_setting.ui.uv_set_line.setText(bake_setting.get_texture_bake_uv(bake_layer))
        self.tb_setting.ui.tex_x_line.setText(str(res_x_y[0]))
        self.tb_setting.ui.tex_y_line.setText(str(res_x_y[1]))
        self.tb_setting.ui.test_tex_x_line.setText(str(test_res_x_y[0]))
        self.tb_setting.ui.test_tex_y_line.setText(str(test_res_x_y[1]))
        self.tb_setting.ui.tex_name_line.setText(bake_tex_base_name)

        # シェイプが持っているUVセットをcompleterに設定する
        shape_list = cmds.sets(bake_layer, q=True) if cmds.sets(bake_layer, q=True) else []
        uv_set_list = []

        for shape in shape_list:
            all_uv_set_list = cmds.polyUVSet(shape, q=True, auv=True)
            if all_uv_set_list:
                uv_set_list.extend(all_uv_set_list)

        uv_set_list = list(set(uv_set_list))

        self.__set_completer(self.tb_setting.ui.uv_set_line, uv_set_list, self.tex_uv_setting_change_event)

    def __get_test_bake_size(self, org_value):
        """テストベイク用のテクスチャサイズを返す

        Args:
            org_value (int): 元のテクスチャサイズ

        Returns:
            int: テスト用のテクスチャサイズ
        """

        if not org_value:
            return 0
        return int(org_value * tool_define.TEST_TEX_RES_SCALE)

    def __init_vtx_bake_setting(self, bake_layer=None):
        """頂点カラーベイク設定をベイクレイヤーの値で初期化する

        Args:
            bake_layer (str): 初期化に使用するturtleベイクレイヤーノード
        """

        self.vb_setting.ui.bake_colort_set_line.setText('')
        self.vb_setting.ui.ray_min_line.setText('')
        self.vb_setting.ui.test_ray_min_line.setText('')
        self.vb_setting.ui.ray_max_line.setText('')
        self.vb_setting.ui.test_ray_max_line.setText('')

        if not cmds.objExists(bake_layer):
            return

        ray_min_max = bake_setting.get_ray_min_max_value(bake_layer)
        test_ray_min_max = bake_setting.get_test_ray_min_max_value(bake_layer)

        self.vb_setting.ui.bake_colort_set_line.setText(tool_utility.generate_bake_colorset_name(bake_layer))
        self.vb_setting.ui.ray_min_line.setText(str(ray_min_max[0]))
        self.vb_setting.ui.ray_max_line.setText(str(ray_min_max[1]))
        self.vb_setting.ui.test_ray_min_line.setText(str(test_ray_min_max[0]))
        self.vb_setting.ui.test_ray_max_line.setText(str(test_ray_min_max[1]))

    def __get_selection_list_from_bake_layer_list(self, bake_layer_list_widget):
        """q_list_widget内の選択中のitemのテキストのリストを取得する

        Args:
            bake_layer_list_widget (QListWidget): bake_layerのQListWidgetオブジェクト

        Returns:
            list: 選択中のテキストリスト
        """

        selections = bake_layer_list_widget.selectedItems()
        return [bake_layer_list_widget.itemWidget(x).bake_layer_label.text() for x in selections]

    def __get_selection_list_from_list_widget(self, q_list_widget):
        """q_list_widget内の選択中のitemのテキストのリストを取得する

        Args:
            q_list_widget (QListWidget): QListWidgetオブジェクト

        Returns:
            list: 選択中のテキストリスト
        """

        selections = q_list_widget.selectedItems()
        return [x.text() for x in selections]

    def __set_completer(self, line_edit, str_list, connection_func=None):
        """QCompleterを設定する

        Args:
            line_edit (QLineEdit): QCompleterを設定するQLineEdit
            str_list (list): QCompleterがポップアップ表示する文字列のリスト
            connection_func (function, optional): ポップアップ選択時シグナルで実行される処理. Defaults to None.
        """

        completer = QtWidgets.QCompleter(line_edit)
        model = QtGui.QStandardItemModel(line_edit)

        for elm in str_list:
            item = QtGui.QStandardItem(elm)
            model.setItem(model.rowCount(), 0, item)

        completer.setModel(model)
        completer.setFilterMode(QtCore.Qt.MatchContains)

        if connection_func:
            completer.activated.connect(connection_func)

        line_edit.setCompleter(completer)


class BakeLayerListItem(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QWidget):
    """ベイクレイヤーリストアイテムのカスタムウィジェット
    """

    def __init__(self, main, bake_layer, parent=None):

        super(BakeLayerListItem, self).__init__(parent)

        self.main = main
        self.bake_layer_label = None
        self.preview_toggle_button = None
        self.icon = None
        self.info_button = None
        self.rename_button = None
        self.delete_button = None

        self.set_ui(bake_layer)
        self.setup_view_event()

    def set_ui(self, bake_layer):
        """UIの設定

        Args:
            bake_layer (str): このアイテムで扱うベイクレイヤー
        """

        horizontalLayout = QtWidgets.QHBoxLayout()
        horizontalLayout.setContentsMargins(0, 0, 0, 0)
        horizontalLayout.setSpacing(0)

        self.preview_toggle_button = QtWidgets.QPushButton(self.main.icon_not_preview, '')
        self.preview_toggle_button.setFlat(True)

        self.bake_type_icon = QtWidgets.QLabel()
        self.bake_type_icon.setScaledContents(True)
        self.bake_type_icon.setMaximumSize(QtCore.QSize(20, 20))

        self.bake_layer_label = QtWidgets.QLabel()
        self.bake_layer_label.setText(bake_layer)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.rename_button = QtWidgets.QPushButton(self.main.icon_rename_pixmap, '')
        self.rename_button.setIconSize(QtCore.QSize(36, 18))
        self.rename_button.setFlat(True)
        self.info_button = QtWidgets.QPushButton(self.main.icon_info_pixmap, '')
        self.info_button.setIconSize(QtCore.QSize(18, 18))
        self.info_button.setFlat(True)
        self.delete_button = QtWidgets.QPushButton(self.main.icon_delete_pixmap, '')
        self.delete_button.setIconSize(QtCore.QSize(18, 18))
        self.delete_button.setFlat(True)

        horizontalLayout.addWidget(self.preview_toggle_button)
        horizontalLayout.addWidget(self.bake_type_icon)
        horizontalLayout.addWidget(self.bake_layer_label)
        horizontalLayout.addItem(spacerItem)
        horizontalLayout.addWidget(self.rename_button)
        horizontalLayout.addWidget(self.info_button)
        horizontalLayout.addWidget(self.delete_button)

        self.setLayout(horizontalLayout)

    def setup_view_event(self):
        """UIのevent設定
        """

        self.rename_button.clicked.connect(self.__rename_button_event)
        self.info_button.clicked.connect(self.__info_button_event)
        self.delete_button.clicked.connect(self.__delete_button_event)
        self.preview_toggle_button.clicked.connect(self.__preview_toggle_button_event)

    def set_icon(self, q_pixmap_preview, q_pixmap_type):
        """アイコンをセットする

        Args:
            q_pixmap_preview (QtGui.QPixmap): プレビューアイコン
            q_pixmap_type (QtGui.QPixmap): ベイクタイプアイコン
        """

        self.preview_toggle_button.setIcon(q_pixmap_preview)
        self.bake_type_icon.setPixmap(q_pixmap_type)

    def __delete_button_event(self):
        """削除ボタンイベント
        """

        self.main.bake_item_rem_button_event(self.bake_layer_label.text())

    def __rename_button_event(self):
        """リネームボタンイベント
        """

        self.main.bake_layer_rename_button_event(self)

    def __info_button_event(self):
        """情報ボタンイベント
        """

        self.main.bake_layer_info_button_event(self)

    def __preview_toggle_button_event(self):
        """プレビューボタンイベント
        """

        self.main.preview_toggle_button_event(self.bake_layer_label.text())
