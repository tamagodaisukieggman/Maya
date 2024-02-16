# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys

import shiboken2

import maya.cmds as cmds
from maya import OpenMayaUI
from PySide2 import QtWidgets

from . import view
from .model import mob_audience_setting, placement_mob_audience_objs, aim_mob_audience_direction, mob_audience_select
from ..glp_random_obj_placement.main import PlacementValueInfo


class Main(object):
    """3Dモブ観客配置用の設定ツール
    """

    def __init__(self):

        self.parent = self.__get_parent()

        self.__delete_overlapping_window([view.View()])
        self.view = view.View()

        self.target_group_list = []
        self.avoidance_obj_view_list = []

    def __get_parent(self):

        main_window = OpenMayaUI.MQtUtil.mainWindow()
        if main_window is None:
            return None

        if sys.version_info.major == 2:
            parent = shiboken2.wrapInstance(long(main_window), QtWidgets.QMainWindow)
        else:
            # for Maya 2022-
            parent = shiboken2.wrapInstance(int(main_window), QtWidgets.QMainWindow)

        if parent is None:
            return None

        return parent

    def __delete_overlapping_window(self, target_list):
        """Windowの重複削除処理
        """

        if self.parent is None:
            return

        for widget in self.parent.children():
            for target in target_list:
                if type(target) == type(widget):
                    widget.deleteLater()

    def show_ui(self):
        """UI表示
        """

        self.__setup_event()
        self.view.show()

        # 最初から1つmob配置のターゲットグループを作成しておく
        self.__add_random_placement_target_mesh_view_event()

    def __setup_event(self):
        """PySide UIのclick Eventを設定する
        """

        # 関数実行系のイベント
        self.view.ui.exec_set_setting_button.clicked.connect(
            lambda: self.__exec_mob_audience_setting_event('set_rein_gear_setting'))

        self.view.ui.exec_set_random_setting_button.clicked.connect(
            lambda: self.__exec_mob_audience_setting_event('set_random_rein_gear_setting'))

        self.view.ui.select_normal_locator_button.clicked.connect(
            lambda: self.__exec_select_mob_audience_locator_event('normal'))

        self.view.ui.select_rein_gear_button.clicked.connect(
            lambda: self.__exec_select_mob_audience_locator_event('rain_gear'))

        self.view.ui.select_reincort_button.clicked.connect(
            lambda: self.__exec_select_mob_audience_locator_event('raincort'))

        self.view.ui.exec_aim_const_button.clicked.connect(
            lambda: self.__exec_aim_mob_audience_direction_event())

        self.view.ui.exec_rp_button.clicked.connect(
            lambda: self.__exec_mob_audience_placement_event())

        self.view.ui.select_mob_audience_on_mesh_button.clicked.connect(
            lambda: self.__exec_select_mob_audience_on_mesh_button_event())

        self.view.ui.exec_shave_mob_audience_button.clicked.connect(
            lambda: self.__exec_shave_mob_audience_event())

        # UI系のイベント
        self.view.ui.reset_rpt_setting_button.clicked.connect(
            lambda: self.__reset_random_placement_setting_event())

        self.view.ui.add_rpt_button.clicked.connect(
            lambda: self.__add_random_placement_target_mesh_view_event())

        self.view.ui.add_aim_target_object_button.clicked.connect(
            lambda: self.__add_aim_target_obj_event())

        self.view.ui.del_aim_target_object_button.clicked.connect(
            lambda: self.__delete_aim_target_obj_event())

        self.view.ui.add_avoidance_obj_button.clicked.connect(
            lambda: self.__add_avoidance_obj_view_event())

        self.view.ui.reset_shave_ui_value_button.clicked.connect(
            lambda: self.__reset_shave_ui_value_event())

    def undo_chank_decorator(func):
        """イベント実行前後にUndoInfoを実行し、1回の戻る/進むで移行できるようにするデコレータ

        Args:
            func (function): 実行する関数
        """

        def undo_chank(self, *args, **kwargs):

            result = None

            try:
                cmds.undoInfo(openChunk=True)
                result = func(self, *args)
            except Exception as e:
                print(e)
            finally:
                cmds.undoInfo(closeChunk=True)

            return result

        return undo_chank

    @undo_chank_decorator
    def __exec_mob_audience_setting_event(self, setting_type):
        """モブ観客ロケーターの雨具設定等を行うイベント

        Args:
            setting_type (string): 設定の振り分けを行う文字列
        """

        limit_tgt_to_loc = self.view.ui.limit_tgt_to_loc_cb.isChecked()

        settings = []

        if setting_type == 'set_rein_gear_setting':

            # X方向のどちら側から処理を実行するか
            direction = '-X'
            if self.view.ui.distance_sort_rbg.checkedButton().objectName() == 'plus_x_rb':
                direction = 'X'

            setting = {
                'type': setting_type,
                'option': {
                    'do_umbrella_distance_setting': self.view.ui.rein_gear_distance_setting_cb.isChecked(),  # 傘同士の距離制限処理を実行するか
                    'umbrella_distance': self.view.ui.audience_distance_setting_sb.value(),  # 傘同士の制限距離
                    'direction': direction
                }
            }

        elif setting_type == 'set_random_rein_gear_setting':

            setting = {
                'type': setting_type,
                'option': {
                    'rain_gear_ratio': self.view.ui.rain_gear_ratio_sb.value(),
                    'normal_gear_ratio': self.view.ui.normal_gear_ratio_sb.value()
                }
            }

        settings.append(setting)

        mob_audience_setting.MobAudienceSetting().exec_mob_audience_setting(limit_tgt_to_loc, settings)

    @undo_chank_decorator
    def __exec_mob_audience_placement_event(self):
        """モブ観客の一括配置を行うイベント
        """

        max_count = self.view.ui.max_placement_value_sb.value()
        if max_count <= 0:
            QtWidgets.QMessageBox.warning(None, u'警告', u'配置個数を設定してください')
            return

        obj_distance = self.view.ui.rpt_obj_distance_sb.value()
        surface_area_ratio = self.view.ui.surface_area_ratio_sb.value()

        shade_flag = self.view.get_scalex_value()
        weather_flag = self.view.get_scaley_value()

        placement_info_list = []
        for target_group in self.target_group_list:
            placement_info = self.__create_placement_info(obj_distance, target_group)
            if placement_info.ratio <= 0.0:
                continue
            if not placement_info.mesh_list:
                continue

            placement_info_list.append(placement_info)

        if not placement_info_list:
            QtWidgets.QMessageBox.warning(None, u'警告', u'ターゲットが設定されていません')
            return

        placement_mob_audience_objs.PlacementMobAudienceObjs().placement_mob_audience_objs(
            max_count=max_count,
            shade_flag=shade_flag,
            weather_flag=weather_flag,
            surface_area_ratio=surface_area_ratio,
            placement_info_list=placement_info_list)

    @undo_chank_decorator
    def __exec_aim_mob_audience_direction_event(self):
        """モブ観客のオブジェクトに対するエイムを行うイベント
        """

        aim_target_list = self.__get_aim_target_obj_list()
        if not aim_target_list:
            QtWidgets.QMessageBox.warning(None, u'警告', u'ターゲットが設定されていません')
            return

        aim_mob_audience_direction.AimMobAudienceDirection().aim_mob_audience_direction(aim_target_list)

    @undo_chank_decorator
    def __exec_select_mob_audience_locator_event(self, select_type):
        """モブ観客ロケーターの簡易選択を行うイベント

        Args:
            select_type (string): 設定の振り分けを行う文字列
        """

        mob_audience_select.MobAudienceSelect().select_mob_audience_locator(select_type)

    @undo_chank_decorator
    def __exec_select_mob_audience_on_mesh_button_event(self):
        """選択メッシュ上のモブ観客選択を行うイベント
        """

        mob_audience_select.MobAudienceSelect().select_mob_audience_locator_on_mesh()

    @undo_chank_decorator
    def __exec_shave_mob_audience_event(self):
        """選択したモブ観客ロケーターを割合または実数で間引く処理を実行するイベント
        """

        ratio = self.view.ui.shave_ratio_sb.value()
        count = self.view.ui.shave_count_sb.value()

        if ratio == 0 and count == 0:
            QtWidgets.QMessageBox.warning(None, u'警告', u'割合または実数に1以上の数値を入力してください。')
            return

        result = placement_mob_audience_objs.PlacementMobAudienceObjs().shave_mob_audience_objs_from_selected(ratio, count)

        if result:
            QtWidgets.QMessageBox.information(
                None, u'完了', u'処理が完了しました。\n対象オブジェクト数: {}\n間引いたオブジェクト数: {}'.format(str(result[0]), str(result[1])))
        else:
            QtWidgets.QMessageBox.warning(None, u'警告', u'対象が見つかりませんでした\nモブ観客ロケーター(pos*****)を選択しているか確認してください。')

    def __add_random_placement_target_mesh_view_event(self):
        """ランダム配置の対象メッシュリストをスクロールレイアウト以下に追加するイベント
        """

        tmp_box_layout = view.RandomPlacementTargetMeshView()
        tmp_box_layout.delete_widget_event_hook_fanc = self.__delete_random_placement_target_mesh_view_event
        self.target_group_list.append(tmp_box_layout)
        self.view.ui.rpt_widget_lauout.insertWidget(
            self.view.ui.rpt_widget_lauout.count() - 1, tmp_box_layout)

    def __delete_random_placement_target_mesh_view_event(self, delete_target_group):
        """ランダム配置の対象メッシュリストを削除する際に実行されるイベント
        """

        for target_group in self.target_group_list:
            if target_group == delete_target_group:
                self.target_group_list.remove(target_group)
                break

    def __reset_random_placement_setting_event(self):
        """ランダム配置の対象メッシュリストの中身と天候スイッチをリセットするイベント
        """

        self.view.reset_scale_button_event()
        for target_group in self.target_group_list:
            target_group.clear_mesh_list()

    def __add_aim_target_obj_event(self):
        """エイム元対象オブジェクトをリストに追加するイベント
        """

        selected = cmds.ls(sl=True, l=True)
        if not selected:
            return

        mesh_list = self.__get_aim_target_obj_list()
        for sel in selected:
            if sel not in mesh_list:
                self.view.ui.aim_target_object_list_wedget.addItem(sel)

    def __delete_aim_target_obj_event(self):
        """エイム元対象オブジェクトをリストから削除するイベント
        """

        select_items = self.view.ui.aim_target_object_list_wedget.selectedItems()
        for select_item in select_items:
            model_index = self.view.ui.aim_target_object_list_wedget.indexFromItem(select_item)
            self.view.ui.aim_target_object_list_wedget.takeItem(model_index.row())

    def __add_avoidance_obj_view_event(self):
        """重複回避オブジェクトリストをスクロールレイアウトに追加するイベント
        """

        selected = cmds.ls(sl=True, l=True)

        avoidance_obj_name_list = self.__get_avoidance_obj_name_list()

        for sel in selected:

            if sel in avoidance_obj_name_list:
                continue

            avoidance_obj_view = view.AvoidanceObjView(sel)
            avoidance_obj_view.delete_widget_event_hook_fanc = self.__del_avoidance_obj_view_event
            self.avoidance_obj_view_list.append(avoidance_obj_view)
            self.view.ui.avoidance_obj_widget_layout.insertLayout(
                self.view.ui.avoidance_obj_widget_layout.count() - 1, avoidance_obj_view)

    def __del_avoidance_obj_view_event(self, delete_avoidance_obj_view):
        """特定の重複回避オブジェクトをレイアウトから削除するイベント
        """

        for avoidance_obj_view in self.avoidance_obj_view_list:
            if avoidance_obj_view == delete_avoidance_obj_view:
                self.avoidance_obj_view_list.remove(avoidance_obj_view)
                break

    def __reset_shave_ui_value_event(self):
        """間引き関連のUI状態を初期にリセットする
        """

        self.view.ui.shave_ratio_sb.setValue(0)
        self.view.ui.shave_count_sb.setValue(0)

    def __get_aim_target_obj_list(self):
        """エイム元対象オブジェクト名のリストをUI上から取得する

        Returns:
            list: エイム元対象オブジェクト名のリスト
        """

        target_list = []
        for i in range(self.view.ui.aim_target_object_list_wedget.count()):
            target_list.append(self.view.ui.aim_target_object_list_wedget.item(i).text())

        return target_list

    def __get_avoidance_obj_name_list(self):
        """重複回避オブジェクト名のリストをUI上から取得する

        Returns:
            [type]: [description]
        """

        avoidance_obj_name_list = []

        for avoidance_obj_view in self.avoidance_obj_view_list:
            obj_name = avoidance_obj_view.avoidance_obj_label.text()
            avoidance_obj_name_list.append(obj_name)

        return avoidance_obj_name_list

    def __create_placement_info(self, obj_distance, item):
        """ランダム配置に必要な情報クラスに値をセットする
        ランダム配置ツールを間借りするうえで設定する必要があり

        Args:
            obj_distance (float): ランダム配置するオブジェクト同士の最低距離
            item (RandomPlacementTargetMeshView): 配置用設定が入っているUI

        Returns:
            PlacementInfo: ランダム配置に必要な情報クラス
        """

        placement_info = PlacementInfo()
        placement_info.ratio = item.get_ratio()
        placement_info.mesh_list = item.get_mesh_list()

        height = item.get_height()
        rot = item.get_rot()

        placement_info.placement_value_info.avoidance_obj_list = []
        placement_info.placement_value_info.avoidance_distance_list = []
        for avoidance_obj_view in self.avoidance_obj_view_list:
            avoidance_obj = avoidance_obj_view.avoidance_obj_label.text()
            avoidance_distance = avoidance_obj_view.avoidance_distance_sb.value()

            placement_info.placement_value_info.avoidance_obj_list.append(avoidance_obj)
            placement_info.placement_value_info.avoidance_distance_list.append(avoidance_distance)

        placement_info.placement_value_info.obj_distance = obj_distance
        placement_info.placement_value_info.rand_max_height = height
        placement_info.placement_value_info.rand_min_height = height
        placement_info.placement_value_info.rand_max_rotate_x = rot[0]
        placement_info.placement_value_info.rand_min_rotate_x = rot[0]
        placement_info.placement_value_info.rand_min_rotate_y = rot[1]
        placement_info.placement_value_info.rand_min_rotate_y = rot[1]
        placement_info.placement_value_info.rand_min_rotate_z = rot[2]
        placement_info.placement_value_info.rand_min_rotate_z = rot[2]

        return placement_info


class PlacementInfo(object):

    def __init__(self, placement_count=0, ratio=0, mesh_list=[]):

        self.placement_count = placement_count
        self.ratio = ratio
        self.mesh_list = mesh_list

        self.is_mesh_unite = False

        self.placement_value_info = PlacementValueInfo()
        self.placement_value_info.reset_value()
