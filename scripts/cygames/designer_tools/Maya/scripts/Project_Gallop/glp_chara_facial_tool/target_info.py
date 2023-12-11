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
except Exception:
    pass

import os
import csv

import maya.cmds as cmds

from ..base_common import utility as base_utility

from . import target_controller_info


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TargetInfo(object):

    # ===============================================
    def __init__(self):

        self.target_csv_file_path = None

        self.controller_csv_file_name = None

        self.script_file_path = None
        self.script_dir_path = None

        self.target_file_path = None
        self.target_file_name = None
        self.target_file_name_noext = None
        self.target_file_ext = None
        self.target_dir_path = None

        self.target_controller_info = \
            target_controller_info.TargetControllerInfo(self)

        self.base_info_item = None
        self.info_item_list = None

        self.current_frame = None

        self.animation_layer_name_list = None
        self.animation_layer_value_dict = None

        self.csv_enable_index = -1
        self.csv_part_index = -1
        self.csv_label_index = -1
        self.csv_frame_index = -1
        self.csv_index_index = -1

        self.csv_driver_attr_index = -1
        self.csv_driver_attr_type_index = -1
        self.csv_driver_attr_max_index = -1

        self.csv_animation_layer_index = -1
        self.csv_translate_multiply_index = -1
        self.csv_rotate_multiply_index = -1
        self.csv_scale_multiply_index = -1

        self.csv_color_index = -1

        self.start_frame = 0
        self.end_frame = 0

        self.start_index = 0
        self.end_index = 0

        self.is_created = False

    # ===============================================
    def create_info_from_csv(self,
                             csv_file_name, controller_csv_file_name):
        """
        glp_chara_facial_tool/resource フォルダに入っているxxx_target_info.csv と xxx_controller_info.csv
        を読み取り TargetInfo.info_item_list と TargetInfo.target_controller_info.info_item_list を作る。
        """
        self.is_created = False
        # 初期化と基本情報の読み込み
        if not self.__check_data(csv_file_name, controller_csv_file_name):
            return

        # xxx_target_info.csv を読む
        self.__read_info_from_csv(csv_file_name)

        if not self.info_item_list:
            base_utility.logger.write("csvの読み込みに失敗しました: " + str(csv_file_name))
            return

        # xxx_controller_info.csvの方を読む
        self.target_controller_info.create_info_from_csv(
            controller_csv_file_name)

        if not self.target_controller_info.is_created:
            base_utility.logger.write(
                "csvの読み込みに失敗しました: " + str(controller_csv_file_name))
            return

        self.is_created = True

    # ===============================================
    def __check_data(self, csv_file_name, controller_csv_file_name):
        """
        現在開かれているMayaシーンを処理する為に必要な変数を初期化し、必要なパスがあるか確認している。
        必要なパスが揃っていればTrueを返す。
        """
        if not csv_file_name:
            base_utility.logger.write("csv_file_nameが未定義でした")
            return False

        if not controller_csv_file_name:
            base_utility.logger.write("controller_csv_file_nameが未定義でした")
            return False

        current_path = cmds.file(q=True, sn=True)

        self.target_file_path = None

        if not current_path:
            base_utility.logger.write("現在のシーン名の取得に失敗しました")
            return False

        if not os.path.isfile(current_path):
            base_utility.logger.write("現在のシーンパスが不正でした: " + str(current_path))
            return False

        self.script_file_path = os.path.abspath(__file__)
        self.script_dir_path = os.path.dirname(self.script_file_path)

        self.target_file_path = current_path.replace('\\', '/')
        self.target_file_name = os.path.basename(self.target_file_path)
        self.target_dir_path = os.path.dirname(self.target_file_path)
        self.target_file_name_noext, self.target_file_ext = \
            os.path.splitext(self.target_file_name)

        self.info_item_list = []
        self.animation_layer_name_list = []

        self.start_frame = 100000
        self.end_frame = -100000

        self.start_index = 100000
        self.end_index = -100000

        if not self.target_file_path:
            base_utility.logger.write("target_file_pathが未定義でした")
            return False

        return True

    # ===============================================
    def __read_info_from_csv(self, csv_file_name):
        """
        csvを読みEnable列が1になっているパーツ情報をTargetInfoItemオブジェクトにして
        self.info_item_list に追加している。
        """
        self.target_csv_file_path = \
            self.target_dir_path + '/' + csv_file_name + '.csv'

        if not os.path.isfile(self.target_csv_file_path):
            self.target_csv_file_path = \
                self.script_dir_path + '/resource/' + \
                csv_file_name + '.csv'

        if not os.path.isfile(self.target_csv_file_path):
            return

        current_list_index = 0
        with open(self.target_csv_file_path, 'r') as read_obj:
            csv_reader = csv.reader(read_obj)
            isFirstLine = True
            for csv_line_arr in csv_reader:
                # 最初の行でカラムのインデックスを取得
                if isFirstLine:
                    # csvから読み取る項目
                    self.csv_enable_index = -1
                    self.csv_part_index = -1
                    self.csv_label_index = -1
                    self.csv_frame_index = -1
                    self.csv_index_index = -1
                    self.csv_driver_attr_index = -1
                    self.csv_driver_attr_type_index = -1
                    self.csv_driver_attr_max_index = -1
                    self.csv_animation_layer_index = -1
                    self.csv_translate_multiply_index = -1
                    self.csv_rotate_multiply_index = -1
                    self.csv_scale_multiply_index = -1
                    self.csv_color_index = -1
                    for col in range(len(csv_line_arr)):
                        this_text = csv_line_arr[col]
                        if this_text == 'Enable':
                            self.csv_enable_index = col
                        elif this_text == 'Part':
                            self.csv_part_index = col
                        elif this_text == 'Label':
                            self.csv_label_index = col
                        elif this_text == 'Frame':
                            self.csv_frame_index = col
                        elif this_text == 'Index':
                            self.csv_index_index = col
                        elif this_text == 'DriverAttribute':
                            self.csv_driver_attr_index = col
                        elif this_text == 'DriverType':
                            self.csv_driver_attr_type_index = col
                        elif this_text == 'DriverMax':
                            self.csv_driver_attr_max_index = col
                        elif this_text == 'AnimationLayer':
                            self.csv_animation_layer_index = col
                        elif this_text == 'TranslateMultiply':
                            self.csv_translate_multiply_index = col
                        elif this_text == 'RotateMultiply':
                            self.csv_rotate_multiply_index = col
                        elif this_text == 'ScaleMultiply':
                            self.csv_scale_multiply_index = col
                        elif this_text == 'Color':
                            self.csv_color_index = col
                    isFirstLine = False

                if not csv_line_arr:
                    continue

                if csv_line_arr[self.csv_enable_index] != '1':
                    continue

                # Maya側でレンダリングした表情毎のパーツpngと照合するファイル名リスト
                part_list = []

                if self.csv_part_index >= 0:

                    this_part = csv_line_arr[1]

                    if this_part == 'Eye' or this_part == 'Eyebrow' or this_part == 'Ear':
                        part_list = [this_part + '_L', this_part + '_R']
                    else:
                        part_list = [this_part]

                else:

                    part_list = ['']

                for part in part_list:

                    new_item = TargetInfoItem(self)

                    new_item.part = part

                    if self.csv_index_index >= 0:
                        new_item.index = \
                            int(csv_line_arr[self.csv_index_index])

                    if self.csv_label_index >= 0:
                        new_item.label = \
                            csv_line_arr[self.csv_label_index]

                    if self.csv_frame_index >= 0:
                        new_item.frame = \
                            int(csv_line_arr[self.csv_frame_index])

                    if self.csv_driver_attr_index >= 0:
                        new_item.driver_attr_name = \
                            csv_line_arr[self.csv_driver_attr_index]

                    if self.csv_driver_attr_type_index >= 0:

                        this_value = \
                            csv_line_arr[self.csv_driver_attr_type_index]

                        if this_value:

                            if this_value == 'float':
                                this_value = float
                            elif this_value == 'int':
                                this_value = int

                            new_item.driver_attr_type = this_value

                    if self.csv_driver_attr_max_index >= 0:

                        this_value = \
                            csv_line_arr[self.csv_driver_attr_max_index]

                        if this_value:
                            new_item.driver_attr_max_value = float(this_value)

                    if self.csv_animation_layer_index >= 0:
                        new_item.animation_layer_name = \
                            csv_line_arr[self.csv_animation_layer_index]

                    if self.csv_translate_multiply_index >= 0:

                        this_value = \
                            csv_line_arr[self.csv_translate_multiply_index]

                        if this_value:

                            this_value = this_value[1:].replace('_', ',')

                            new_item.translate_offset_multiply = \
                                base_utility.list.convert_from_string(
                                    this_value, float)

                    if self.csv_rotate_multiply_index >= 0:

                        this_value = \
                            csv_line_arr[self.csv_rotate_multiply_index]

                        if this_value:

                            this_value = this_value[1:].replace('_', ',')

                            new_item.rotate_offset_multiply = \
                                base_utility.list.convert_from_string(
                                    this_value, float)

                    if self.csv_scale_multiply_index >= 0:

                        this_value = \
                            csv_line_arr[self.csv_scale_multiply_index]

                        if this_value:

                            this_value = this_value[1:].replace('_', ',')

                            new_item.scale_offset_multiply = \
                                base_utility.list.convert_from_string(
                                    this_value, float)

                    if self.csv_color_index >= 0:

                        this_value = \
                            csv_line_arr[self.csv_color_index]

                        if this_value:

                            this_value = this_value[1:].replace('_', ',')

                            new_item.color = \
                                base_utility.list.convert_from_string(
                                    this_value, float)

                    new_item.attr_name = new_item.part + '_' + new_item.label

                    if new_item.animation_layer_name not in self.animation_layer_name_list:

                        if new_item.animation_layer_name:

                            if cmds.animLayer(new_item.animation_layer_name, q=True, exists=True):

                                self.animation_layer_name_list.append(
                                    new_item.animation_layer_name)

                    if not new_item.label:
                        continue

                    new_item.list_index = current_list_index
                    current_list_index += 1

                    # TargetInfoItemをTargetInfoのinfo_item_listに追加
                    self.info_item_list.append(new_item)

                    if new_item.index > self.end_index:
                        self.end_index = new_item.index

                    if new_item.index < self.start_index:
                        self.start_index = new_item.index

                    if new_item.frame > self.end_frame:
                        self.end_index = new_item.index

                    if new_item.frame < self.start_frame:
                        self.start_frame = new_item.frame


    # ===============================================
    def update_info(self, update_controller, update_target):
        """
        glp_chara_facial_tool/resource フォルダに入っているxxx_target_info.csv と xxx_controller_info.csv
        を読み取って作られた TargetInfo.info_item_list と TargetInfo.target_controller_info.info_item_list を更新する。
        これは TargetInfo.update_info だが、TargetInfoItem.update_info もある。
        update_controller: bool
        update_target: bool
        """
        if not self.is_created:
            return

        self.current_frame = cmds.currentTime(q=True)
        self.save_animation_layer_setting()
        self.mute_all_animation_layer()
        # mdl_xxx_facial_target.ma などAnimationLayerがあるシーンで、
        # facial_target_info.csvのようにAnimationLayer列があり、レイヤー名が指定してある場合切り替える
        for i, info_item in enumerate(self.info_item_list):
            if i == 0:
                self.base_info_item = info_item
                info_item.is_base = True
                self.mute_all_animation_layer()
                self.set_mute_animation_layer(self.base_info_item.animation_layer_name, False)
            else:
                prev_info_item = self.info_item_list[i - 1]
                if info_item.animation_layer_name != prev_info_item.animation_layer_name:
                    self.mute_all_animation_layer()
                    self.set_mute_animation_layer(
                        info_item.animation_layer_name, False)
            info_item.update_info(update_controller, update_target)

        self.revert_animation_layer_setting()
        cmds.currentTime(self.current_frame)

    # ===============================================
    def save_animation_layer_setting(self):

        self.animation_layer_value_dict = {}

        if not self.animation_layer_name_list:
            return

        count = -1
        for animation_layer_name in self.animation_layer_name_list:
            count += 1

            if not animation_layer_name:
                continue

            if not cmds.animLayer(animation_layer_name, q=True, exists=True):
                continue

            this_mute = cmds.animLayer(
                animation_layer_name, q=True, mute=True)

            this_weight = cmds.animLayer(
                animation_layer_name, q=True, weight=True)

            self.animation_layer_value_dict[animation_layer_name] = \
                [this_mute, this_weight]

    # ===============================================
    def revert_animation_layer_setting(self):

        if not self.animation_layer_name_list:
            return

        if not self.animation_layer_value_dict:
            return

        count = -1
        for animation_layer_name in self.animation_layer_name_list:
            count += 1

            if not animation_layer_name:
                continue

            if not cmds.animLayer(animation_layer_name, q=True, exists=True):
                continue

            if animation_layer_name not in self.animation_layer_value_dict:
                continue

            this_value_list = \
                self.animation_layer_value_dict[animation_layer_name]

            cmds.animLayer(animation_layer_name,
                           e=True,
                           mute=this_value_list[0], weight=this_value_list[1]
                           )

    # ===============================================
    def mute_all_animation_layer(self):

        if not self.animation_layer_name_list:
            return

        for animation_layer_name in self.animation_layer_name_list:

            if not animation_layer_name:
                continue

            if not cmds.animLayer(animation_layer_name, q=True, exists=True):
                continue

            cmds.animLayer(animation_layer_name, e=True, mute=True, weight=1.0)

    # ===============================================
    def set_weight_to_all_animation_layer(self, weight_value):

        if not self.animation_layer_name_list:
            return

        for animation_layer_name in self.animation_layer_name_list:

            if not animation_layer_name:
                continue

            if not cmds.animLayer(animation_layer_name, q=True, exists=True):
                continue

            cmds.animLayer(animation_layer_name, e=True, weight=weight_value)

    # ===============================================
    def set_active_animation_layer(self, animation_layer_name):

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

    # ===============================================
    def delete_all_animation_layer(self):

        self.set_active_animation_layer(None)

        animation_layer_list = cmds.ls(l=True, type='animLayer')

        if not animation_layer_list:
            return

        for animation_layer in animation_layer_list:

            if animation_layer == 'BaseAnimation':
                continue

            cmds.delete(animation_layer)

    # ===============================================
    def set_mute_animation_layer(self, animation_layer_name, mute_value):

        if not animation_layer_name:
            return

        if not cmds.animLayer(animation_layer_name, q=True, exists=True):
            return

        cmds.animLayer(animation_layer_name, e=True, mute=mute_value)

    # ===============================================
    def bake_transform(self, is_controller, is_index, is_base):

        if not self.is_created:
            return

        cmds.playbackOptions(minTime=self.start_index, maxTime=self.end_index)
        cmds.playbackOptions(ast=self.start_index, aet=self.end_index)

        for info_item in self.info_item_list:
            info_item.set_transform(
                is_controller, True, is_index, is_base, 1.0)

    # ===============================================
    def write_xml(self, xml_file_name, output_dir_path):

        if not self.is_created:
            return

        if not xml_file_name:
            return

        xml_file_path = None

        if output_dir_path:

            xml_file_path = \
                output_dir_path + '/' + xml_file_name

        else:

            xml_file_path = \
                self.target_dir_path + '/' + xml_file_name

        if not xml_file_path:
            return

        root_element = base_utility.xml.create_element('TargetInfo', None)

        this_list_root_element = base_utility.xml.add_element(
            root_element, 'TargetInfoItemList', None)

        for info_item in self.info_item_list:
            info_item.write_xml(this_list_root_element)

        base_utility.xml.write(xml_file_path, root_element)

    # ===============================================
    def update_info_from_xml(self, xml_file_path):

        if not self.is_created:
            return

        if not xml_file_path:
            return

        if not os.path.isfile(xml_file_path):
            return

        self.update_info(False, False)

        root_element = base_utility.xml.read(xml_file_path)

        if root_element is None:
            return

        this_list_root_element = \
            base_utility.xml.search_element(
                root_element, 'TargetInfoItemList')

        if this_list_root_element is None:
            return

        this_child_element_list = base_utility.xml.search_element_list(
            this_list_root_element, 'TargetInfoItem')

        for child_element in this_child_element_list:

            this_part = base_utility.xml.get_element_value(
                child_element, 'Part')

            this_label = base_utility.xml.get_element_value(
                child_element, 'Label')

            for info_item in self.info_item_list:

                if info_item.part != this_part:
                    continue

                if info_item.label != this_label:
                    continue

                info_item.update_info_from_xml(child_element)

                break

    # ===============================================
    def create_info_locator(self, locator_name, parent):

        if not self.is_created:
            return

        if not locator_name:
            return

        if not base_utility.node.exists(parent):
            return

        cmds.spaceLocator(name=locator_name)

        cmds.parent(locator_name, parent)

        for info_item in self.info_item_list:
            info_item._create_info_locator(locator_name)

    # ===============================================
    def delete_driven_key(self):

        for info_item in self.info_item_list:

            info_item._delete_driver_attribute()

    # ===============================================
    def create_driven_key(self, is_controller):

        self.delete_all_animation_layer()

        for info_item in self.info_item_list:

            info_item._create_driven_key(is_controller)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TargetInfoItem(object):

    # ===============================================
    def __init__(self, root):

        self.root = root

        self.list_index = -1

        self.is_base = False

        self.part = None
        self.label = None

        self.index = None
        self.frame = None

        self.driver_attr_name = None
        self.driver_attr_type = float
        self.driver_attr_max_value = 1

        self.animation_layer_name = None

        self.translate_offset_multiply = None
        self.rotate_offset_multiply = None
        self.scale_offset_multiply = None

        self.color = None

        self.controller_info_item_list = None

    # ===============================================
    def update_info(self, update_controller, update_target):
        """
        コントロールリグのTargetInfoItemの設定
        update_controller: bool
        update_target: bool
        """
        if not self.root.target_controller_info.info_item_list:
            print("target_info 723 ターゲットコントローラインフォのアイテムリストがありません".encode("shift-jis"))
            return

        for controller_info_item in \
                self.root.target_controller_info.info_item_list:

            if self.translate_offset_multiply:
                controller_info_item.translate_offset_multiply = \
                    self.translate_offset_multiply

            if self.rotate_offset_multiply:
                controller_info_item.rotate_offset_multiply = \
                    self.rotate_offset_multiply

            if self.scale_offset_multiply:
                controller_info_item.scale_offset_multiply = \
                    self.scale_offset_multiply

            controller_info_item.animation_layer_name = None
            if self.animation_layer_name:
                controller_info_item.animation_layer_name = \
                    self.animation_layer_name

        self.root.target_controller_info.update_info(
            self.frame, update_controller, update_target)

        self.controller_info_item_list = \
            self.root.target_controller_info.get_clone_info_item_list()

    # ===============================================
    def get_clone(self):

        clone_info_item = TargetInfoItem(self.root)

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

    # ===============================================
    def set_transform(self,
                      is_controller,
                      is_bake_key, is_bake_index, is_base,
                      multiply_value):

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

    # ===============================================
    def write_xml(self, parent_element):

        this_root_element = base_utility.xml.add_element(
            parent_element, 'TargetInfoItem', None)

        if this_root_element is None:
            return

        base_utility.xml.add_element(
            this_root_element, 'Part', self.part)
        base_utility.xml.add_element(
            this_root_element, 'Label', self.label)
        base_utility.xml.add_element(
            this_root_element, 'Frame', self.frame)
        base_utility.xml.add_element(
            this_root_element, 'Index', self.index)
        base_utility.xml.add_element(
            this_root_element, 'AnimLayerName', self.animation_layer_name)

        this_list_root_element = base_utility.xml.add_element(
            this_root_element, 'ControllerInfoItemList', None)

        for controller_info_item in self.controller_info_item_list:
            controller_info_item.write_info(this_list_root_element)

    # ===============================================
    def update_info_from_xml(self, parent_element):

        this_list_root_element = base_utility.xml.search_element(
            parent_element, 'ControllerInfoItemList'
        )

        if this_list_root_element is None:
            return

        child_element_list = base_utility.xml.search_element_list(
            this_list_root_element, 'ControllerInfoItem'
        )

        if child_element_list is None:
            return

        for child_element in child_element_list:

            this_controller_name = base_utility.xml.get_element_value(
                child_element, 'ControllerName')

            this_target_name = base_utility.xml.get_element_value(
                child_element, 'TargetName')

            for controller_info_item in self.controller_info_item_list:

                if controller_info_item.controller_name != \
                        this_controller_name:
                    continue

                if controller_info_item.target_name != this_target_name:
                    continue

                controller_info_item.update_info_from_xml(child_element)
                break

    # ===============================================
    def _create_info_locator(self, parent):

        if not base_utility.transform.exists(parent):
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

        if base_utility.transform.exists(locator_name):
            return

        cmds.spaceLocator(name=locator_name)

        base_utility.attribute.set_value(
            locator_name, 'scaleX', self.index)
        base_utility.attribute.set_value(
            locator_name, 'scaleY', self.frame)

        cmds.parent(locator_name, parent)

    # ===============================================
    def _delete_driver_attribute(self):

        if not self.controller_info_item_list:
            return

        for controller_info_item in self.controller_info_item_list:

            if controller_info_item.part != self.part:
                continue

            controller_info_item._delete_driver_attribute(
                self.driver_attr_name)

    # ===============================================
    def _create_driven_key(self, is_controller):

        self.__add_driver_attribute()

        self.__set_driven_attribute_value(0)

        self.set_transform(is_controller, False, False, True, 1.0)

        self.__connect_driver_to_driven(is_controller)

        self.__set_driven_attribute_value(1)

        self.set_transform(is_controller, False, False, False, 1.0)

        self.__connect_driver_to_driven(is_controller)

        if self.driver_attr_max_value > 1:

            self.__set_driven_attribute_value(self.driver_attr_max_value)

            self.set_transform(
                is_controller, False, False, False, self.driver_attr_max_value)

            self.__connect_driver_to_driven(is_controller)

        self.set_transform(is_controller, False, False, True, 1.0)

        self.__set_driven_attribute_value(0)

    # ==================================================
    def __add_driver_attribute(self):

        if not self.controller_info_item_list:
            return

        for controller_info_item in self.controller_info_item_list:

            if controller_info_item.part != self.part:
                continue

            controller_info_item._add_driver_attribute(
                self.driver_attr_name,
                self.driver_attr_type,
                0, self.driver_attr_max_value)

    # ==================================================
    def __set_driven_attribute_value(self, driven_value):

        if not self.controller_info_item_list:
            return

        for controller_info_item in self.controller_info_item_list:

            if controller_info_item.part != self.part:
                continue

            controller_info_item._set_driven_attribute_value(
                self.driver_attr_name, driven_value)

    # ==================================================
    def __connect_driver_to_driven(self, is_controller):

        if not self.driver_attr_name:
            return

        if not self.controller_info_item_list:
            return

        for controller_info_item in self.controller_info_item_list:

            if controller_info_item.part != self.part:
                continue

            controller_info_item._connect_driver_to_driven(
                self.driver_attr_name, is_controller)
