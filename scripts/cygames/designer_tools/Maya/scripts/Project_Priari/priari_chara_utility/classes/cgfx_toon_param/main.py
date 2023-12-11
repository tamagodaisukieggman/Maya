# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import range
except:
    pass

import os
from functools import partial

import maya.cmds as cmds

from ....base_common import classes as base_class

from . import cgfx_toon_param
from .. import main_template

from ....priari_common.classes.info import chara_info


class Main(main_template.Main):

    def __init__(self):
        """
        """

        super(self.__class__, self).__init__(os.path.basename(os.path.dirname(__file__)))

        self.tool_name = 'PriariCharaUtilityTestClass'
        self.tool_label = 'CGFXのパラメータ変更'
        self.tool_version = '19112201'

        self.cgfx_toon_param = cgfx_toon_param.CgfxToonParam()

    def ui_body(self):
        """
        UI要素のみ
        """

        # spec_infoが髪限定になっているのを共通部分に
        # speculer_colorをつけたタイミングでspec_infoをつける

        _chara_info = chara_info.CharaInfo()
        _chara_info.create_info()

        data_id = None

        if _chara_info.exists:
            data_id = _chara_info.part_info.data_id

        self.attr_param_list = [
            {'attr': '_CheekPretenseThreshold', 'part': 'face', 'type': 'float', 'ui': None},
            {'attr': '_NosePretenseThreshold', 'part': 'face', 'type': 'float', 'ui': None},
            {'attr': '_CylinderBlend', 'part': 'face', 'type': 'float', 'ui': None},
            {'attr': '_HairNormalBlend', 'part': 'hair', 'type': 'float', 'ui': None},
            {'attr': '_SpecularColor', 'part': 'face_all', 'type': 'color', 'ui': None},
            {'attr': '_SpecularColor', 'part': 'hair_all', 'type': 'color', 'ui': None},
            {'attr': '_SpecularColor', 'part': 'bdy_all', 'type': 'color', 'ui': None}
        ]

        cmds.columnLayout(adjustableColumn=True)
        base_class.ui.button.Button('cgfxパラメータ ロード', self._reset_cgfx_param)
        cmds.setParent('..')

        self.ui_cgfx_param_face = cmds.frameLayout(l='顔部分', cll=1, cl=0, bv=1, mw=5, mh=5)
        cmds.columnLayout(adjustableColumn=True)

        for i in range(len(self.attr_param_list)):
            attr_param = self.attr_param_list[i]
            if attr_param['part'] != 'face':
                continue

            attr = attr_param['attr']
            value = self.cgfx_toon_param.get_cgfx_toon_param('face', attr, data_id=data_id)
            slider = self._create_cgfx_param_float_slider('face', attr, value)
            self.attr_param_list[i]['ui'] = slider

        cmds.setParent('..')
        cmds.setParent('..')

        self.ui_cgfx_param_head = cmds.frameLayout(l='髪部分', cll=1, cl=0, bv=1, mw=5, mh=5)
        cmds.columnLayout(adjustableColumn=True)

        for i in range(len(self.attr_param_list)):
            attr_param = self.attr_param_list[i]
            attr = attr_param['attr']
            if attr_param['part'] != 'hair':
                continue

            value = self.cgfx_toon_param.get_cgfx_toon_param('hair', attr, data_id=data_id)

            if attr_param['type'] == 'color':
                value = self.cgfx_toon_param.get_cgfx_toon_param('hair', attr, [(0, 0, 0)], data_id=data_id)
                slider = cmds.colorSliderGrp(
                    label=attr, rgbValue=value[0],
                    columnAttach=([1, 'right', 5]), columnWidth=([1, 160], [2, 50]),
                )
                self.attr_param_list[i]['ui'] = slider
                cmds.colorSliderGrp(
                    slider, e=True,
                    dragCommand=partial(self.set_cgfx_toon_color_param, 'hair', attr, 'double3', self.attr_param_list[i]['ui']),
                    changeCommand=partial(self.set_cgfx_toon_color_param, 'hair', attr, 'double3', self.attr_param_list[i]['ui'])
                )
            else:
                slider = self._create_cgfx_param_float_slider('hair', attr, value)
                self.attr_param_list[i]['ui'] = slider

        cmds.setParent('..')
        cmds.setParent('..')

        self.ui_cgfx_param_face = cmds.frameLayout(l='共通', cll=1, cl=0, bv=1, mw=5, mh=5)
        cmds.columnLayout(adjustableColumn=True)

        # all
        for i in range(len(self.attr_param_list)):
            attr_param = self.attr_param_list[i]
            attr = attr_param['attr']
            part = attr_param['part']
            attr_part = part.split('_')[0]
            if not part.endswith('all'):
                continue

            if attr_param['type'] == 'color':
                value = self.cgfx_toon_param.get_cgfx_toon_param(attr_part, attr, [(0, 0, 0)], data_id=data_id)
                slider = cmds.colorSliderGrp(
                    label='{0}_{1}'.format(attr_part, attr), rgbValue=value[0],
                    columnAttach=([1, 'right', 5]), columnWidth=([1, 160], [2, 50]),
                )
                self.attr_param_list[i]['ui'] = slider
                cmds.colorSliderGrp(
                    slider, e=True,
                    dragCommand=partial(self.set_cgfx_toon_color_param, attr_part, attr, 'double3', self.attr_param_list[i]['ui']),
                    changeCommand=partial(self.set_cgfx_toon_color_param, attr_part, attr, 'double3', self.attr_param_list[i]['ui'])
                )
            else:
                slider = self._create_cgfx_param_float_slider(attr_part, attr, value)
                self.attr_param_list[i]['ui'] = slider

        cmds.setParent('..')
        cmds.setParent('..')

        self.ui_cgfx_param_center_offset = cmds.frameLayout(l='center offset locator 選択', cll=1, cl=0, bv=1, mw=5, mh=5)
        cmds.columnLayout(adjustableColumn=True, rs=4)

        base_class.ui.button.Button(
            'head_center_offsetを選択', self.select_center_offset_locator, 'Head_center_offset')
        base_class.ui.button.Button(
            'head_tube_center_offsetを選択', self.select_center_offset_locator, 'Head_tube_center_offset')

        cmds.setParent('..')
        cmds.setParent('..')

    def _reset_cgfx_param(self):

        _chara_info = chara_info.CharaInfo()
        _chara_info.create_info()

        data_id = None

        if _chara_info.exists:
            data_id = _chara_info.part_info.data_id

        for i in range(len(self.attr_param_list)):

            attr_param = self.attr_param_list[i]
            attr = attr_param['attr']
            attr_part = attr_param['part'].split('_')[0]
            ui_obj = attr_param['ui']

            if attr_param['type'] == 'color':

                if _chara_info.part_info.data_type == 'bdy0001_body' and attr_part == 'bdy':
                    value = self.cgfx_toon_param.get_cgfx_toon_param(attr_part, attr, [(0, 0, 0)], True, data_id=data_id)
                else:
                    value = self.cgfx_toon_param.get_cgfx_toon_param(attr_part, attr, [(0, 0, 0)], data_id=data_id)

                cmds.colorSliderGrp(ui_obj, e=True, rgbValue=value[0])

            else:

                value = self.cgfx_toon_param.get_cgfx_toon_param(attr_part, attr, data_id=data_id)
                cmds.floatSliderGrp(ui_obj, e=True, v=value)

    def _create_cgfx_param_float_slider(self, target_part, target_attr, value):

        slider = cmds.floatSliderGrp(
            label=target_attr,
            field=True,
            columnAttach=([1, 'right', 5]),
            columnWidth=([1, 160], [2, 50]),
            minValue=0, maxValue=1.0, fieldMinValue=0, fieldMaxValue=1.0, value=value, precision=3,
            dragCommand=partial(self.set_cgfx_toon_param, target_part, target_attr, 'float'),
            changeCommand=partial(self.set_cgfx_toon_param, target_part, target_attr, 'float'))

        return slider

    def set_cgfx_toon_color_param(self, target_part, target_attr, value_type, ui_obj, *args):

        value = cmds.colorSliderGrp(ui_obj, q=True, rgbValue=True)

        self.set_cgfx_toon_param(target_part, target_attr, value_type, value)

    def set_cgfx_toon_param(self, target_part, target_attr, value_type, value):

        _chara_info = chara_info.CharaInfo()
        _chara_info.create_info()

        data_id = None

        if _chara_info.exists:
            data_id = _chara_info.part_info.data_id

        selection = cmds.ls(sl=True)

        self.cgfx_toon_param.set_cgfx_toon_param(target_part, target_attr, value_type, value, data_id=data_id)

        if selection:
            cmds.select(selection)

    def select_center_offset_locator(self, target):

        if not cmds.objExists(target):
            return

        target_list = cmds.ls(target)
        if len(target_list) > 1:
            return

        cmds.select(target_list)
