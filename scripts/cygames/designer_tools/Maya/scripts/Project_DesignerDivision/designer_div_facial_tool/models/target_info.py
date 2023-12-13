# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os
import csv

import maya.cmds as cmds

from . import target_controller_info, util

# Python3-
try:
    from importlib import reload
    from builtins import object
except Exception:
    pass

reload(target_controller_info)
reload(util)


class TargetInfo(object):

    def __init__(self):

        self.target_csv_file_path = None
        self.controller_csv_file_name = None

        self.target_dir_path = None

        self.target_controller_info = None

        # 基準になるTargetInfoItem
        self.base_info_item = None

        self.animation_layer_name_list = None
        self.animation_layer_value_dict = None

        self.current_frame = None

        self.info_item_list = []
        self.animation_layer_name_list = []

        self.start_frame = 100000
        self.end_frame = -100000

        self.start_index = 100000
        self.end_index = -100000

        self.namespace = None

        self.is_created = False

    def create_info_from_csv(self, target_csv_file_name, controller_csv_file_name=None, target_dir_path=None, namespace=None):
        """CSVからフェイシャルのパーツやフレーム値、インデックス値等を内包する情報クラスを作成する

        facial(ear)_target_info.csv(フェイシャルターゲットのframeやindex値等が書かれているCSV)
        facial(ear)_blend_shape_target_info.csv(フェイシャルターゲットからblendShapeを作成する為のframe値やblendShape名のlabel等が書かれているCSV)
        等を読み込み、各行をTargetInfoItemに値をセット・格納しself.info_item_listに追加

        また、フェイシャル/耳リグの値のコントローラーがどの部位に対応しているかを記した
        facial(ear)_controller_info.csv
        も同時に読み込むことで、コントローラーのtransform値を取得・設定したり、controllerのコンストレイン先の値をbakeしたりが出来る
        """

        self.is_created = False

        self.namespace = namespace

        # xxx_target_info.csv名が無いと作成できないため返す
        if not target_csv_file_name:
            return False

        # 初期化と基本情報の読み込み
        if not self.__check_data_path(target_dir_path):
            util.debug_print('初期化、基本情報の読み込みが出来ませんでした')
            return

        # xxx_target_info.csv を読む
        if not self.__read_info_from_csv(target_csv_file_name):
            util.debug_print('csvの読み込みに失敗しました: {}'.format(target_csv_file_name))
            return

        # xxx_controller_info.csvの方を読む
        if controller_csv_file_name:
            self.target_controller_info = target_controller_info.TargetControllerInfo(self)
            self.target_controller_info.create_info_from_csv(controller_csv_file_name, target_dir_path)
            if not self.target_controller_info.is_created:
                util.debug_print('csvの読み込みに失敗しました: {}'.format(controller_csv_file_name))
                return

        self.is_created = True

    def __check_data_path(self, target_dir_path):
        """TargetInfo作成に必要なファイルパスがセットし、パスに問題があればFalseを返す

        Args:
            target_dir_path (String): csvを読み込む対象ディレクトリ名(ここに該当のCSVが存在しなければresouceのパスを読み込む)

        Returns:
            bool: パスチェックに問題があったか
        """

        if target_dir_path is None:
            target_dir_path = cmds.file(q=True, sn=True)
        self.target_dir_path = target_dir_path.replace(os.path.sep, '/') if target_dir_path is not None else ''

        script_file_path = os.path.abspath(__file__).replace(os.path.sep, '/')
        script_dir_path = os.path.dirname(os.path.dirname(script_file_path))
        self.csv_resource_dir = script_dir_path + '/resource'
        if not os.path.exists(self.csv_resource_dir):
            return False

        return True

    def __read_info_from_csv(self, target_csv_file_name):
        """xxx_target_info.csvを読み込み、各行の値をTargetItemInfoに格納し、self.info_item_listに追加していく

        Args:
            csv_file_name (String): 読み込むcsvの名前

        Returns:
            bool: TargetInfoItemが正常に作成できたか(self.info_item_listに値があるか)
        """

        # まず指定されたディレクトリにcsvがあるかを確認し、無ければscript自体のresourceフォルダのcsvを参照する
        self.target_csv_file_path = os.path.join(self.target_dir_path, '{}.csv'.format(target_csv_file_name))
        if not os.path.exists(self.target_csv_file_path):
            self.target_csv_file_path = os.path.join(self.csv_resource_dir, '{}.csv'.format(target_csv_file_name))
            if not os.path.exists(self.target_csv_file_path):
                return False

        # 表情リスト作成のために必要なindex番号
        current_list_index = 0

        with open(self.target_csv_file_path, 'r') as f:

            # CSVを辞書型で読み込み
            target_info_dict_list = csv.DictReader(f)

            for target_info_dict in target_info_dict_list:

                if target_info_dict.get('Enable') != '1':
                    continue

                target_info_item = TargetInfoItem(self)
                target_info_item.create_info_item(target_info_dict, self.namespace)

                # アニメーションレイヤー追加
                if target_info_item.animation_layer_name not in self.animation_layer_name_list:
                    if target_info_item.animation_layer_name:
                        if cmds.animLayer(target_info_item.animation_layer_name, q=True, exists=True):
                            self.animation_layer_name_list.append(target_info_item.animation_layer_name)

                # current_list_indexを追加
                target_info_item.list_index = current_list_index
                current_list_index += 1

                # TargetInfoItemをTargetInfoのinfo_item_listに追加
                self.info_item_list.append(target_info_item)

                # それぞれのframe/indexを比較して最初のframe/indexと最後のframe/indexをセット
                if target_info_item.index > self.end_index:
                    self.end_index = target_info_item.index
                if target_info_item.index < self.start_index:
                    self.start_index = target_info_item.index
                if target_info_item.frame > self.end_frame:
                    self.end_frame = target_info_item.frame
                if target_info_item.frame < self.start_frame:
                    self.start_frame = target_info_item.frame

        return self.info_item_list != []

    def update_info(self, update_controller, update_target):
        """TargetInfoItem並びにTargetInfoItem.controller_item_listにある
        TargetControllerInfoItemの各種情報(transform等)をupdate_info時点の状態に更新する

        Args:
            update_controller (bool)): TargetControllerInfoItemのControllerの情報を更新するかどうか
            update_target (_type_): TargetControllerInfoItemのTargetの情報を更新するかどうか
        """

        if not self.is_created:
            return

        self.current_frame = cmds.currentTime(q=True)

        # 現在のAnimationLayerの設定を保存
        self.save_animation_layer_setting()
        # 全てのAnimationLayerをミュート
        self.mute_all_animation_layer()

        for i, info_item in enumerate(self.info_item_list):
            if i == 0:
                self.base_info_item = info_item
                info_item.is_base = True
                self.mute_all_animation_layer()
                # 対象のTargetInfoItemにAnimationLayerの記載があればミュート解除
                self.set_mute_animation_layer(self.base_info_item.animation_layer_name, False)
            else:
                prev_info_item = self.info_item_list[i - 1]
                if info_item.animation_layer_name != prev_info_item.animation_layer_name:
                    self.mute_all_animation_layer()
                    # 対象のTargetInfoItemにAnimationLayerの記載があればミュート解除
                    self.set_mute_animation_layer(info_item.animation_layer_name, False)

            info_item.update_info(update_controller, update_target)

        # AnimationLayer情報を元に戻す
        self.revert_animation_layer_setting()

        # 元のFrameに戻す
        cmds.currentTime(self.current_frame)

    def save_animation_layer_setting(self):
        """現在のアニメーションレイヤーの状態を保存する
        """

        self.animation_layer_value_dict = {}

        if not self.animation_layer_name_list:
            return

        for animation_layer_name in self.animation_layer_name_list:

            if not animation_layer_name:
                continue

            if not cmds.animLayer(animation_layer_name, q=True, exists=True):
                continue

            this_mute = cmds.animLayer(
                animation_layer_name, q=True, mute=True)

            this_weight = cmds.animLayer(
                animation_layer_name, q=True, weight=True)

            self.animation_layer_value_dict[animation_layer_name] = [this_mute, this_weight]

    def revert_animation_layer_setting(self):
        """save_animation_layer_setting()を実行した時点のアニメーションレイヤーの状態に戻す
        """

        if not self.animation_layer_name_list:
            return

        if not self.animation_layer_value_dict:
            return

        for animation_layer_name in self.animation_layer_name_list:

            if not animation_layer_name:
                continue

            if not cmds.animLayer(animation_layer_name, q=True, exists=True):
                continue

            if animation_layer_name not in self.animation_layer_value_dict:
                continue

            this_value_list = self.animation_layer_value_dict[animation_layer_name]

            cmds.animLayer(animation_layer_name, e=True, mute=this_value_list[0], weight=this_value_list[1])

    def mute_all_animation_layer(self):
        """全てのアニメーションレイヤーをミュートする
        """

        if not self.animation_layer_name_list:
            return

        for animation_layer_name in self.animation_layer_name_list:

            if not animation_layer_name:
                continue

            if not cmds.animLayer(animation_layer_name, q=True, exists=True):
                continue

            cmds.animLayer(animation_layer_name, e=True, mute=True, weight=1.0)

    def set_weight_to_all_animation_layer(self, weight_value):
        """全てのアニメーションレイヤーのweight値をweight_valueの値にセットする

        Args:
            weight_value (float): アニメーションレイヤーにセットするweight値
        """

        if not self.animation_layer_name_list:
            return

        for animation_layer_name in self.animation_layer_name_list:

            if not animation_layer_name:
                continue

            if not cmds.animLayer(animation_layer_name, q=True, exists=True):
                continue

            cmds.animLayer(animation_layer_name, e=True, weight=weight_value)

    def set_active_animation_layer(self, animation_layer_name):
        """アクティブにするアニメーションレイヤーを設定する
        animation_layer_nameが設定されていない場合(Noneか空)の場合は「BaseAnimation」が設定される

        Args:
            animation_layer_name (String): アクティブにするアニメーションレイヤー名
        """

        if not animation_layer_name:
            animation_layer_name = 'BaseAnimation'

        if not animation_layer_name:
            return

        animation_layer_list = cmds.ls(l=True, type='animLayer')

        if not animation_layer_list:
            return

        for animation_layer in animation_layer_list:

            cmds.animLayer(animation_layer, e=True, selected=False)

            if animation_layer != animation_layer_name:
                continue

            cmds.animLayer(animation_layer, e=True, selected=True, prf=True)

    def delete_all_animation_layer(self):
        """「BaseAnimation」以外の全てのアニメーションレイヤーを削除する
        """

        self.set_active_animation_layer(None)

        animation_layer_list = cmds.ls(l=True, type='animLayer')
        for animation_layer in animation_layer_list:

            if animation_layer == 'BaseAnimation':
                continue

            cmds.delete(animation_layer)

    def set_mute_animation_layer(self, animation_layer_name, mute_value):
        """アニメーションレイヤーのミュート状態を設定する

        Args:
            animation_layer_name (String): ミュート状態を設定するアニメーションレイヤー名
            mute_value (bool)): ミュート状態の値
        """

        if not animation_layer_name:
            return

        if not cmds.animLayer(animation_layer_name, q=True, exists=True):
            return

        cmds.animLayer(animation_layer_name, e=True, mute=mute_value)

    def bake_transform(self, is_controller, is_index, is_base):
        """コントローラーまたはコントローラーの接続先(Target)に値をセットしてsetKeyFrame(Bake)を行う

        Args:
            is_controller (bool): コントローラーに対してベイクを行うか(Falseの場合はコントローラーの接続先の骨がベイクされる)
            is_index (bool): TargetInfoItem.indexのFrameにベイクするか(Falseの場合はTargetInfoItem.frameのFrameにベイクされる)
            is_base (bool): TargetInfo.base_info_itemの値でベイクするか(Falseの場合はTargetControllerItemのtransform値でベイクされる)
        """

        if not self.is_created:
            return

        # シーンのフレームの設定
        if is_index:
            cmds.playbackOptions(minTime=self.start_index, maxTime=self.end_index)
            cmds.playbackOptions(ast=self.start_index, aet=self.end_index)
        else:
            cmds.playbackOptions(minTime=self.start_frame, maxTime=self.end_frame)
            cmds.playbackOptions(ast=self.start_frame, aet=self.end_frame)

        for info_item in self.info_item_list:
            info_item.set_transform(is_controller, True, is_index, is_base, 1.0)

    def create_info_locator(self, locator_name, parent):
        """Unityで各frameの情報を読み込むための情報ロケーターを作成する
        ロケーター名には表情名、scaleXにはindex値、scaleYにはframe値が入る

        Args:
            locator_name (String)): 情報ロケーターの親ロケーター名
            parent (String): 親ロケーターの更に親のオブジェクト名
        """

        if not self.is_created:
            return

        if not locator_name or not cmds.objExists(parent):
            return

        cmds.spaceLocator(name=locator_name)
        cmds.parent(locator_name, parent)

        for info_item in self.info_item_list:
            info_item._create_info_locator(locator_name)


class TargetInfoItem(object):

    def __init__(self, target_info):

        self.target_info = target_info

        self.controller_info_item_list = None

        self.list_index = -1
        self.is_base = False

        self.part = None
        self.part_key = 'Part'

        self.label = None
        self.label_key = 'Label'

        self.index = None
        self.index_key = 'Index'

        self.frame = None
        self.frame_key = 'Frame'

        self.driver_attr_name = None
        self.driver_attr_name_key = 'DriverAttribute'

        self.driver_attr_type = float
        self.driver_attr_type_key = 'DriverType'

        self.driver_attr_max_value = 1
        self.driver_attr_max_value_key = 'DriverMax'

        self.animation_layer_name = None
        self.animation_layer_name_key = 'AnimationLayer'

        self.translate_offset_multiply = None
        self.translate_offset_multiply_key = 'TranslateMultiply'

        self.rotate_offset_multiply = None
        self.rotate_offset_multiply_key = 'RotateMultiply'

        self.scale_offset_multiply = None
        self.scale_offset_multiply_key = 'ScaleMultiply'

        self.color = None
        self.color_key = 'Color'

        self.attr_name = None

        self.namespace = None

    def create_info_item(self, info_dict, namespace):
        """辞書型に入った情報からTargetInfoItemを作成する

        Args:
            info_dict (dict): 情報が入った辞書型変数

        Returns:
            bool: TargetInfoItemを作成できたか
        """

        self.namespace = namespace

        self.label = info_dict.get(self.label_key)
        if not self.label:
            return False

        self.part = info_dict.get(self.part_key)
        self.index = int(info_dict.get(self.index_key)) if info_dict.get(self.index_key) is not None else None
        self.frame = int(info_dict.get(self.frame_key)) if info_dict.get(self.frame_key) is not None else None
        self.driver_attr_name = info_dict.get(self.driver_attr_name_key)

        # DriverAttr
        this_value = info_dict.get(self.driver_attr_type_key)
        if this_value:
            if this_value == 'float':
                self.driver_attr_type = float
            elif this_value == 'int':
                self.driver_attr_type = int

        self.driver_attr_max_value = float(info_dict.get(self.driver_attr_max_value_key)) if info_dict.get(self.driver_attr_max_value_key) is not None else -1
        self.animation_layer_name = info_dict.get(self.animation_layer_name_key)
        if self.animation_layer_name and self.namespace:
            self.animation_layer_name = '{}:{}'.format(self.namespace, self.animation_layer_name)

        # translateMultiply
        this_value = info_dict.get(self.translate_offset_multiply_key)
        if this_value:
            self.translate_offset_multiply = [float(value) for value in this_value[1:].split('_')]

        # rotateMultiply
        this_value = info_dict.get(self.rotate_offset_multiply_key)
        if this_value:
            self.rotate_offset_multiply = [float(value) for value in this_value[1:].split('_')]

        # scaleMultiply
        this_value = info_dict.get(self.scale_offset_multiply_key)
        if this_value:
            self.scale_offset_multiply = [float(value) for value in this_value[1:].split('_')]

        # color
        this_value = info_dict.get(self.color_key)
        if this_value:
            self.color = [float(value) for value in this_value[1:].split('_')]

        self.attr_name = self.part + '_' + self.label

        return True

    def update_info(self, update_controller, update_target):
        """controller_info.info_item_list内のTargetControllerItemInfoの各種情報(Transform等)の状態を現在のシーンの状態に更新する
        更に自身のself.controller_info_item_listにこのTargetInfoItemのFrame値を利用して作成したControllerInfoItemを格納する

        Args:
            update_controller (bool)): TargetControllerInfoItemのControllerの情報を更新するかどうか
            update_target (_type_): TargetControllerInfoItemのTargetの情報を更新するかどうか
        """

        if not self.target_info.target_controller_info.info_item_list:
            return

        for controller_info_item in self.target_info.target_controller_info.info_item_list:

            if self.translate_offset_multiply:
                controller_info_item.translate_offset_multiply = self.translate_offset_multiply

            if self.rotate_offset_multiply:
                controller_info_item.rotate_offset_multiply = self.rotate_offset_multiply

            if self.scale_offset_multiply:
                controller_info_item.scale_offset_multiply = self.scale_offset_multiply

            controller_info_item.animation_layer_name = self.animation_layer_name if self.animation_layer_name else None

        self.target_info.target_controller_info.update_info(self.frame, update_controller, update_target)

        self.controller_info_item_list = self.target_info.target_controller_info.get_clone_info_item_list()

    def get_clone(self):
        """このTargetInfoItemの複製を作成する

        Returns:
            複製されたTargetInfoItem
        """

        clone_info_item = TargetInfoItem(self.target_info)

        clone_info_item.part = self.part
        clone_info_item.label = self.label

        clone_info_item.index = self.index
        clone_info_item.frame = self.frame

        clone_info_item.driver_attr_name = self.driver_attr_name

        clone_info_item.animation_layer_name = self.animation_layer_name

        if self.controller_info_item_list:

            clone_info_item.controller_info_item_list = []

            for ctrl_info_item in self.controller_info_item_list:

                this_clone = ctrl_info_item.get_clone()

                clone_info_item.controller_info_item_list.append(this_clone)

        return clone_info_item

    def set_transform(self, is_controller, is_bake_key, is_bake_index, is_base, multiply_value):
        """controller_info_item_listのコントローラーまたはコントローラーの接続先(Target)のTransform値をセットする
        セットする値はself.info_item.base_info_itemの値かcontroller_info_item自体に保存されている対象Frameの値どちらか
        (is_baseで設定する)
        is_bake_keyをTrueにすると、indexかframeの値のフレームにsetKeyFrameを行う

        Args:
            is_controller (bool): コントローラーに対してベイクを行うか(Falseの場合はコントローラーの接続先の骨がベイクされる)
            is_bake_key (bool): setKeyFrameを行うかどうか(Falseの場合は行わずに値をセットするのみ)
            is_bake_index (bool): TargetInfoItem.indexのフレームにベイクするか(Falseの場合はTargetInfoItem.frameのフレームにベイクされる)
            is_base (bool): TargetInfo.base_info_itemの値でベイクするか(Falseの場合はTargetControllerItemのtransform値でベイクされる)
            multiply_value (float)): offset値
        """

        if not self.controller_info_item_list:
            return

        for controller_info_item in self.controller_info_item_list:

            if controller_info_item.part != self.part:
                continue

            if is_bake_key:

                if is_bake_index:
                    controller_info_item.set_transform(
                        is_controller, self.index, is_base, multiply_value)
                else:
                    controller_info_item.set_transform(
                        is_controller, self.frame, is_base, multiply_value)

            else:

                controller_info_item.set_transform(
                    is_controller, None, is_base, multiply_value)

    def _create_info_locator(self, parent):
        """Unityで各frameの情報を読み込むための情報ロケーターを作成する
        ロケーター名には表情名、scaleXにはindex値、scaleYにはframe値が入る

        Args:
            parent (String): 親のオブジェクト名
        """

        if not cmds.objExists(parent):
            return

        locator_name = ''

        if self.part:

            locator_name += self.part
            locator_name = locator_name.replace('_L', '')
            locator_name = locator_name.replace('_R', '')

        if self.label:

            if locator_name:
                locator_name += '__'

            locator_name += self.label

        if not locator_name:
            return

        if cmds.objExists(locator_name):
            return

        cmds.spaceLocator(name=locator_name)
        cmds.setAttr('{}.scaleX'.format(locator_name), self.index)
        cmds.setAttr('{}.scaleY'.format(locator_name), self.frame)
        cmds.parent(locator_name, parent)
