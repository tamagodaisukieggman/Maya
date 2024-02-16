# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os
import csv

import maya.cmds as cmds

from . import util, vector

# Python3-
try:
    from importlib import reload
    from builtins import range
    from builtins import object
except Exception:
    pass

reload(util)
reload(vector)


class TargetControllerInfo(object):

    def __init__(self, target_info=None):

        self.target_info = target_info

        self.info_item_list = []

        self.target_controller_csv_file_path = None
        self.target_dir_path = None
        self.resource_dir_path = None

        self.controller_root_name = None
        self.target_root_name = None

        self.is_created = False

    def create_info_from_csv(self, csv_file_name, target_dir_path=None):
        """CSVからコントローラーの部位(Part)やコントローラーの接続元(Target)等の値等を取得し内包する情報クラスを作成する

        Args:
            csv_file_name (String): 値を取得するCSV名
            target_dir_path (String, None): csvの取得先のディレクトリ名、Noneの場合はscript/resourceフォルダ内のcsvが使用される
        """

        self.is_created = False

        if not csv_file_name:
            return

        if not self.__check_data_path(target_dir_path):
            return

        if not self.__read_info_from_csv(csv_file_name):
            return

        self.is_created = True

    def __check_data_path(self, target_dir_path):
        """TargetControllerInfo作成に必要なファイルパスがセットし、パスに問題があればFalseを返す

        Args:
            target_dir_path (String): csvを読み込む対象ディレクトリ名(ここに該当のCSVが存在しなければresouceのパスを読み込む)

        Returns:
            bool: パスチェックに問題があったか
        """

        if target_dir_path is None:
            target_dir_path = cmds.file(q=True, sn=True)
        self.target_dir_path = target_dir_path.replace(os.path.sep, '/') if target_dir_path is not None else ''

        script_file_path = os.path.abspath(__file__)
        script_dir_path = os.path.dirname(os.path.dirname(script_file_path))
        self.resource_dir_path = script_dir_path + '/resource/'

        return True

    def __read_info_from_csv(self, csv_file_name):
        """xxx_controller_info.csvを読み込み、各行の値をTargetControllerInfoItemに格納し、self.info_item_listに追加していく

        Args:
            csv_file_name (String): 読み込むcsvの名前

        Returns:
            bool: TargetControllerInfoItemが正常に作成できたか(self.info_item_listに値があるか)
        """

        self.target_controller_csv_file_path = os.path.join(self.target_dir_path, '{}.csv'.format(csv_file_name))
        if not os.path.exists(self.target_controller_csv_file_path):
            self.target_controller_csv_file_path = os.path.join(self.resource_dir_path, '{}.csv'.format(csv_file_name))
            if not os.path.exists(self.target_controller_csv_file_path):
                return

        current_list_index = 0
        with open(self.target_controller_csv_file_path, 'r') as f:

            this_controller_dict_list = csv.DictReader(f)
            for this_controller_dict in this_controller_dict_list:

                if this_controller_dict.get('Enable') != '1':
                    continue

                new_info_item = TargetControllerInfoItem(self)
                if not new_info_item.create_info_item(this_controller_dict):
                    continue

                new_info_item.list_index = current_list_index
                current_list_index += 1
                self.info_item_list.append(new_info_item)

        return self.info_item_list != []

    def update_info(self, target_frame, update_controller, update_target):
        """self.info_item_listにあるTargetControllerInfoItemの各種情報(transform等)をupdate_info時点の状態に更新する

        Args:
            update_controller (bool)): TargetControllerInfoItemのControllerの情報を更新するかどうか
            update_target (_type_): TargetControllerInfoItemのTargetの情報を更新するかどうか
        """

        if self.is_created:
            for info_item in self.info_item_list:
                info_item.update_info(target_frame, update_controller, update_target)

    def get_clone_info_item_list(self):
        """info_item_list内のinfo_itemを全て複製したリストを作成し、返す

        Returns:
            list: self.info_item_list内にあるTargetControllerInfoItemを複製したもののリスト
        """

        clone_info_item_list = []
        if self.is_created:
            for info_item in self.info_item_list:

                this_clone = info_item.get_clone()
                clone_info_item_list.append(this_clone)

        return clone_info_item_list

    def get_target_info_index_list(self, target_part_type):
        """self.info_item_list内のTargetControllerInfoItemのindex値のリストを作成し返す

        Args:
            target_part_type (String): 対象の部位

        Returns:
            list: partが合致するself.info_item_list内のTargetControllerInfoItemのindex値のリスト
        """

        info_index_list = []

        for p in range(len(self.info_item_list)):

            this_info = self.info_item_list[p]
            if this_info.part_type == target_part_type:
                info_index_list.append(p)

        return info_index_list


class TargetControllerInfoItem(object):

    def __init__(self, target_controller_info):

        self.target_controller_info = target_controller_info

        self.list_index = -1

        self.base_controller_info_item = None

        self.part = None
        self.part_key = 'Part'

        self.controller = None
        self.controller_name = None
        self.controller_name_key = 'ControllerName'

        self.target = None
        self.target_name = None
        self.target_name_key = 'TargetName'

        self.driver = None
        self.driver_name = None
        self.driver_name_key = 'DriverName'

        self.controller_translate = None
        self.controller_rotate = None
        self.controller_scale = None

        self.controller_translate_base = None
        self.controller_rotate_base = None
        self.controller_scale_base = None

        self.controller_translate_offset = None
        self.controller_rotate_offset = None
        self.controller_scale_offset = None

        self.target_translate = None
        self.target_rotate = None
        self.target_scale = None

        self.target_translate_base = None
        self.target_rotate_base = None
        self.target_scale_base = None

        self.target_translate_offset = None
        self.target_rotate_offset = None
        self.target_scale_offset = None

        self.animation_layer_name = None

        self.translate_offset_multiply = None
        self.rotate_offset_multiply = None
        self.scale_offset_multiply = None

    def create_info_item(self, info_dict):
        """辞書型に入った情報からTargetControllerInfoItemを作成する

        Args:
            info_dict (dict): 情報が入った辞書型変数

        Returns:
            bool: TargetControllerInfoItemを作成できたか
        """

        referenced_nodes = cmds.ls(referencedNodes=True)
        dag_nodes = cmds.ls(dagObjects=True)

        # target_indexが存在し、targetが存在しない場合はcontinueで返す
        if info_dict.get(self.target_name_key) is not None:

            target_name = info_dict.get(self.target_name_key)

            # importされている場合とリファレンスされている場合があるので両方とも検索する
            target_list = [target_node for target_node in dag_nodes if target_node.endswith(target_name)]
            ref_target_list = [target_node for target_node in referenced_nodes if target_node.endswith(target_name)]

            if not target_list and not ref_target_list:
                return False

            self.target_name = target_name

        self.controller_name = info_dict.get(self.controller_name_key)
        self.part = info_dict.get(self.part_key)
        self.driver_name = info_dict.get(self.driver_name_key)

        return True

    def update_info(self, target_frame, update_controller, update_target):
        """TargetControllerItemInfoの各種情報(Transform等)の状態を現在のシーンの状態に更新する

        Args:
            target_frame (bool): 値を取得するフレーム値
            update_controller (bool): TargetControllerInfoItemのControllerの情報を更新するかどうか
            update_target (_type_): TargetControllerInfoItemのTargetの情報を更新するかどうか
        """

        self.__update_base_controller_info_item()
        self.__update_controller_and_target()
        self.__update_current(target_frame, update_controller, update_target)
        self.__update_base(update_controller, update_target)
        self.__update_offset(update_controller, update_target)

    def __update_base_controller_info_item(self):
        """トランスフォームのBASE値を取得するcontrollerのtarget_info_itemを現在のシーンの状態に更新する
        """

        self.base_controller_info_item = None

        if not self.target_controller_info.target_info:
            return

        if not self.target_controller_info.target_info.base_info_item:
            return

        if not self.target_controller_info.target_info.base_info_item.controller_info_item_list:
            return

        if self.list_index < 0 or self.list_index >= len(self.target_controller_info.target_info.base_info_item.controller_info_item_list):
            return

        self.base_controller_info_item = self.target_controller_info.target_info.base_info_item.controller_info_item_list[self.list_index]

    def __update_controller_and_target(self):
        """コントローラーとターゲットのノードを取得する
        self.base_controller_info_itemがNoneの時はtarget_controller_infoのcontroller_root_nameとtarget_root_name名を取得する
        """

        if not self.base_controller_info_item:

            self.controller = util.find_node(self.controller_name, self.target_controller_info.controller_root_name)
            self.target = util.find_node(self.target_name, self.target_controller_info.target_root_name)

        else:

            self.controller = self.base_controller_info_item.controller
            self.target = self.base_controller_info_item.target

            self.controller_name = self.base_controller_info_item.controller_name
            self.target_name = self.base_controller_info_item.target_name

    def __update_current(self, target_frame, update_controller, update_target):
        """コントローラー/コントローラーの接続元のトランスフォーム情報を現在のシーンの状態に更新する
        target_frameが設定されている場合は、その値のフレームのトランスフォーム情報を取得・更新する

        Args:
            target_frame (int): 値を取得するフレーム
            update_controller (bool): TargetControllerInfoItemのControllerの情報を更新するかどうか
            update_target (_type_): TargetControllerInfoItemのTargetの情報を更新するかどうか
        """

        current_frame = cmds.currentTime(q=True)

        if target_frame is not None:
            if target_frame != current_frame:
                cmds.currentTime(target_frame)

        if update_controller and self.controller:

            self.controller_translate = cmds.xform(self.controller, q=True, ws=False, t=True)
            self.controller_rotate = cmds.xform(self.controller, q=True, ws=False, ro=True)
            self.controller_scale = cmds.xform(self.controller, q=True, ws=False, r=True, s=True)

        if update_target and self.target:

            self.target_translate = cmds.xform(self.target, q=True, ws=False, t=True)
            self.target_rotate = cmds.xform(self.target, q=True, ws=False, ro=True)
            self.target_scale = cmds.xform(self.target, q=True, ws=False, r=True, s=True)

    def __update_base(self, update_controller, update_target):
        """コントローラー/コントローラーの接続元のベーストランスフォーム情報をtarget_info.base_item_infoのtransform値に更新する

        Args:
            update_controller (bool): TargetControllerInfoItemのControllerのBaseのトランスフォーム情報を更新するかどうか
            update_target (_type_): TargetControllerInfoItemのTargetの情報を更新するかどうか
        """

        self.controller_translate_base = self.controller_translate
        self.controller_rotate_base = self.controller_rotate
        self.controller_scale_base = self.controller_scale

        self.target_translate_base = self.target_translate
        self.target_rotate_base = self.target_rotate
        self.target_scale_base = self.target_scale

        if self.animation_layer_name:

            if cmds.animLayer(self.animation_layer_name, q=True, exists=True):

                is_anim_layer_mute = cmds.animLayer(self.animation_layer_name, q=True, mute=True)

                if not is_anim_layer_mute:
                    cmds.animLayer(self.animation_layer_name, e=True, mute=True)

                if update_controller and self.controller:

                    self.controller_translate_base = cmds.xform(self.controller, q=True, ws=False, t=True)
                    self.controller_rotate_base = cmds.xform(self.controller, q=True, ws=False, ro=True)
                    self.controller_scale_base = cmds.xform(self.controller, q=True, ws=False, r=True, s=True)

                if update_target and self.target:

                    self.target_translate_base = cmds.xform(self.target, q=True, ws=False, t=True)
                    self.target_rotate_base = cmds.xform(self.target, q=True, ws=False, ro=True)
                    self.target_scale_base = cmds.xform(self.target, q=True, ws=False, r=True, s=True)

                if not is_anim_layer_mute:
                    cmds.animLayer(self.animation_layer_name, e=True, mute=False)

                return

        if not self.base_controller_info_item:
            return

        if update_controller:

            self.controller_translate_base = self.base_controller_info_item.controller_translate
            self.controller_rotate_base = self.base_controller_info_item.controller_rotate
            self.controller_scale_base = self.base_controller_info_item.controller_scale

        if update_target:

            self.target_translate_base = self.base_controller_info_item.target_translate
            self.target_rotate_base = self.base_controller_info_item.target_rotate
            self.target_scale_base = self.base_controller_info_item.target_scale

    def __update_offset(self, update_controller, update_target):
        """コントローラー/コントローラーの接続元の
        「フレームのトランスフォーム値とbase_itemのトランスフォーム値」のオフセット値を現在のシーンの状態に更新する

        Args:
            update_controller (bool): TargetControllerInfoItemのControllerのBaseのトランスフォーム情報を更新するかどうか
            update_target (_type_): TargetControllerInfoItemのTargetの情報を更新するかどうか
        """

        if update_controller:

            if self.controller_translate and self.controller_translate_base:

                self.controller_translate_offset = vector.sub(self.controller_translate, self.controller_translate_base)

            if self.controller_rotate and self.controller_rotate_base:

                self.controller_rotate_offset = vector.sub(self.controller_rotate, self.controller_rotate_base)

            if self.controller_scale and self.controller_scale_base:

                self.controller_scale_offset = vector.sub(self.controller_scale, self.controller_scale_base)

        if update_target:

            if self.target_translate and self.target_translate_base:

                self.target_translate_offset = vector.sub(self.target_translate, self.target_translate_base)

            if self.target_rotate and self.target_rotate_base:

                self.target_rotate_offset = vector.sub(self.target_rotate, self.target_rotate_base)

            if self.target_scale and self.target_scale_base:

                self.target_scale_offset = vector.sub(self.target_scale, self.target_scale_base)

    def get_clone(self):
        """このTargetControllerInfoItemの複製を作成する

        Returns:
            複製されたTargetControllerInfoItem
        """

        clone_info_item = TargetControllerInfoItem(self.target_controller_info)

        clone_info_item.part = self.part
        clone_info_item.controller = self.controller
        clone_info_item.controller_name = self.controller_name
        clone_info_item.target = self.target
        clone_info_item.target_name = self.target_name
        clone_info_item.driver = self.driver
        clone_info_item.driver_name = self.driver_name

        clone_info_item.animation_layer_name = self.animation_layer_name

        if self.controller_translate:
            clone_info_item.controller_translate = self.controller_translate[:]

        if self.controller_rotate:
            clone_info_item.controller_rotate = self.controller_rotate[:]

        if self.controller_scale:
            clone_info_item.controller_scale = self.controller_scale[:]

        if self.controller_translate_base:
            clone_info_item.controller_translate_base = self.controller_translate_base[:]

        if self.controller_rotate_base:
            clone_info_item.controller_rotate_base = self.controller_rotate_base[:]

        if self.controller_scale_base:
            clone_info_item.controller_scale_base = self.controller_scale_base[:]

        if self.controller_translate_offset:
            clone_info_item.controller_translate_offset = self.controller_translate_offset[:]

        if self.controller_rotate_offset:
            clone_info_item.controller_rotate_offset = self.controller_rotate_offset[:]

        if self.controller_scale_offset:
            clone_info_item.controller_scale_offset = self.controller_scale_offset[:]

        if self.target_translate:
            clone_info_item.target_translate = self.target_translate[:]

        if self.target_rotate:
            clone_info_item.target_rotate = self.target_rotate[:]

        if self.target_scale:
            clone_info_item.target_scale = self.target_scale[:]

        if self.target_translate_base:
            clone_info_item.target_translate_base = self.target_translate_base[:]

        if self.target_rotate_base:
            clone_info_item.target_rotate_base = self.target_rotate_base[:]

        if self.target_scale_base:
            clone_info_item.target_scale_base = self.target_scale_base[:]

        if self.target_translate_offset:
            clone_info_item.target_translate_offset = self.target_translate_offset[:]

        if self.target_rotate_offset:
            clone_info_item.target_rotate_offset = self.target_rotate_offset[:]

        if self.target_scale_offset:
            clone_info_item.target_scale_offset = self.target_scale_offset[:]

        return clone_info_item

    def set_transform(self, is_controller, bake_frame, is_base, multiply_value):
        """コントローラーまたはコントローラーの接続先(Target)のTransform値をセットする
        is_bake_keyをTrueにすると、フレームにsetKeyFrameを行う

        Args:
            is_controller (bool): コントローラーに対してベイクを行うか(Falseの場合はコントローラーの接続先の骨がベイクされる)
            bake_frame (bool): トランスフォームをセットするフレーム値 Noneの場合はベイクされない
            is_base (bool): TargetInfo.base_info_itemの値でベイクするか(Falseの場合はTargetControllerItemのtransform値でベイクされる)
            multiply_value (float)): offset値
        """

        this_target = None

        this_translate = None
        this_rotate = None
        this_scale = None

        this_translate_offset = None
        this_rotate_offset = None
        this_scale_offset = None

        self.__update_controller_and_target()

        if is_controller:

            this_target = self.controller

            if is_base:

                this_translate = self.controller_translate_base
                this_rotate = self.controller_rotate_base
                this_scale = self.controller_scale_base

            else:

                this_translate = self.controller_translate
                this_rotate = self.controller_rotate
                this_scale = self.controller_scale

            this_translate_offset = self.controller_translate_offset
            this_rotate_offset = self.controller_rotate_offset
            this_scale_offset = self.controller_scale_offset

        else:

            this_target = self.target

            if is_base:

                this_translate = self.target_translate_base
                this_rotate = self.target_rotate_base
                this_scale = self.target_scale_base

            else:

                this_translate = self.target_translate
                this_rotate = self.target_rotate
                this_scale = self.target_scale

            this_translate_offset = self.target_translate_offset
            this_rotate_offset = self.target_rotate_offset
            this_scale_offset = self.target_scale_offset

        if not this_target:
            return

        if not cmds.objExists(this_target):
            return

        if bake_frame is not None:

            current_frame = cmds.currentTime(q=True)

            if bake_frame != current_frame:
                cmds.currentTime(bake_frame)

        if this_translate:

            if multiply_value != 1.0 and this_translate_offset:

                this_offset = vector.multiply_value(this_translate_offset, multiply_value - 1.0)
                this_translate = vector.add(this_translate, this_offset)

            cmds.xform(this_target, ws=False, t=this_translate)

            if bake_frame is not None:

                cmds.setKeyframe(this_target + '.tx')
                cmds.setKeyframe(this_target + '.ty')
                cmds.setKeyframe(this_target + '.tz')

        if this_rotate:

            if multiply_value != 1.0 and this_rotate_offset:

                this_offset = vector.multiply_value(this_rotate_offset, multiply_value - 1.0)
                this_rotate = vector.add(this_rotate, this_offset)

            cmds.xform(this_target, ws=False, ro=this_rotate)

            if bake_frame is not None:

                cmds.setKeyframe(this_target + '.rx')
                cmds.setKeyframe(this_target + '.ry')
                cmds.setKeyframe(this_target + '.rz')

        if this_scale:

            if multiply_value != 1.0 and this_scale_offset:

                this_offset = vector.multiply_value(this_scale_offset, multiply_value - 1.0)
                this_scale = vector.add(this_scale, this_offset)

            cmds.xform(this_target, ws=False, s=this_scale)

            if bake_frame is not None:

                cmds.setKeyframe(this_target + '.sx')
                cmds.setKeyframe(this_target + '.sy')
                cmds.setKeyframe(this_target + '.sz')
