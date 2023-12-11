# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os
import maya.cmds as cmds
from functools import partial

from ....base_common import classes as base_class
from . import shader_toon_param
from .. import main_template


class Main(main_template.Main):

    def __init__(self, main=None):

        super(self.__class__, self).__init__(main, os.path.basename(os.path.dirname(__file__)))

        self.tool_name = 'GlpShaderToonParam'
        self.tool_label = 'Toonシェーダーのパラメータ変更'
        self.tool_version = '19112201'

        self.shader_toon_param = shader_toon_param.ShaderToonParam()

        self.param = None

        self.attr_info_list = [{
            'label':
            '顔部分',
            'attr_list': [
                {
                    'attr': 'xCheekPretenseThreshold',
                    'part': 'face',
                    'data_type': 'head',
                    'type': 'float',
                    'default_value': 0.0,
                    'max_value': 1.0,
                    'ui': None,
                    'param': {}
                },
                {
                    'attr': 'xNosePretenseThreshold',
                    'part': 'face',
                    'data_type': 'head',
                    'type': 'float',
                    'default_value': 0.0,
                    'max_value': 1.0,
                    'ui': None,
                    'param': {}
                },
                {
                    'attr': 'xCylinderBlend',
                    'part': 'face',
                    'data_type': 'head',
                    'type': 'float',
                    'default_value': 0.0,
                    'max_value': 1.0,
                    'ui': None,
                    'param': {}
                },
            ]
        }, {
            'label':
            '髪部分',
            'attr_list': [
                {
                    'attr': 'xHairNormalBlend',
                    'part': 'hair',
                    'data_type': 'head',
                    'type': 'float',
                    'default_value': 0.0,
                    'max_value': 1.0,
                    'ui': None,
                    'param': {}
                },
            ]
        }, {
            'label':
            '共通',
            'attr_list': [
                {
                    'attr': 'xSpecularColorRGB',
                    'part': 'face',
                    'data_type': 'head',
                    'type': 'double3',
                    'default_value': (0.0, 0.0, 0.0),
                    'max_value': 1.0,
                    'ui': None,
                    'param': {}
                },
                {
                    'attr': 'xSpecularColorRGB',
                    'part': 'hair',
                    'data_type': 'head',
                    'type': 'double3',
                    'default_value': (0.0, 0.0, 0.0),
                    'max_value': 1.0,
                    'ui': None,
                    'param': {}
                },
                {
                    'attr': 'xSpecularColorRGB',
                    'part': 'bdy',
                    'data_type': 'body',
                    'type': 'double3',
                    'default_value': (0.0, 0.0, 0.0),
                    'max_value': 1.0,
                    'ui': None,
                    'param': {}
                },
                {
                    'attr': 'xSpecularColorRGB',
                    'part': 'toon_prop',
                    'data_type': 'toon_prop',
                    'type': 'double3',
                    'default_value': (0.0, 0.0, 0.0),
                    'max_value': 1.0,
                    'ui': None,
                    'param': {}
                },
            ]
        }, {
            'label':
            'リフレクション',
            'attr_list': [
                {
                    'attr': 'xReflectionAddColor',
                    'part': 'hair',
                    'data_type': 'head',
                    'type': 'double3',
                    'default_value': (0.0, 0.0, 0.0),
                    'max_value': 1.0,
                    'ui': None,
                    'param': {}
                },
                {
                    'attr': 'xReflectionMulColor',
                    'part': 'hair',
                    'data_type': 'head',
                    'type': 'double3',
                    'default_value': (1.0, 1.0, 1.0),
                    'max_value': 1.0,
                    'ui': None,
                    'param': {}
                },
                {
                    'attr': 'xReflectionPowVal',
                    'part': 'hair',
                    'data_type': 'head',
                    'type': 'float',
                    'default_value': 1.0,
                    'min_value': 0.001,
                    'max_value': 5.0,
                    'ui': None,
                    'param': {}
                },
                {
                    'attr': 'xReflectionAddColor',
                    'part': 'bdy',
                    'data_type': 'body',
                    'type': 'double3',
                    'default_value': (0.0, 0.0, 0.0),
                    'max_value': 1.0,
                    'ui': None,
                    'param': {}
                },
                {
                    'attr': 'xReflectionMulColor',
                    'part': 'bdy',
                    'data_type': 'body',
                    'type': 'double3',
                    'default_value': (1.0, 1.0, 1.0),
                    'max_value': 1.0,
                    'ui': None,
                    'param': {}
                },
                {
                    'attr': 'xReflectionPowVal',
                    'part': 'bdy',
                    'data_type': 'body',
                    'type': 'float',
                    'default_value': 1.0,
                    'min_value': 0.001,
                    'max_value': 5.0,
                    'ui': None,
                    'param': {}
                },
                {
                    'attr': 'xReflectionAddColor',
                    'part': 'tail',
                    'data_type': 'tail',
                    'type': 'double3',
                    'default_value': (0.0, 0.0, 0.0),
                    'max_value': 1.0,
                    'ui': None,
                    'param': {}
                },
                {
                    'attr': 'xReflectionMulColor',
                    'part': 'tail',
                    'data_type': 'tail',
                    'type': 'double3',
                    'default_value': (1.0, 1.0, 1.0),
                    'max_value': 1.0,
                    'ui': None,
                    'param': {}
                },
                {
                    'attr': 'xReflectionPowVal',
                    'part': 'tail',
                    'data_type': 'tail',
                    'type': 'float',
                    'default_value': 1.0,
                    'min_value': 0.001,
                    'max_value': 5.0,
                    'ui': None,
                    'param': {}
                },
                {
                    'attr': 'xReflectionAddColor',
                    'part': 'toon_prop',
                    'data_type': 'toon_prop',
                    'type': 'double3',
                    'default_value': (0.0, 0.0, 0.0),
                    'max_value': 1.0,
                    'ui': None,
                    'param': {}
                },
                {
                    'attr': 'xReflectionMulColor',
                    'part': 'toon_prop',
                    'data_type': 'toon_prop',
                    'type': 'double3',
                    'default_value': (1.0, 1.0, 1.0),
                    'max_value': 1.0,
                    'ui': None,
                    'param': {}
                },
                {
                    'attr': 'xReflectionPowVal',
                    'part': 'toon_prop',
                    'data_type': 'toon_prop',
                    'type': 'float',
                    'default_value': 1.0,
                    'min_value': 0.001,
                    'max_value': 5.0,
                    'ui': None,
                    'param': {}
                },
            ]
        }]

    def reset_param(self):
        """各アトリビュートのパラメータを再設定する
        """

        print('※※※※※ パラメータ再設定中 ※※※※※')

        for attr_info in self.attr_info_list:
            for attr in attr_info['attr_list']:
                param = self.shader_toon_param.get_shader_toon_param(
                    attr['attr'],
                    attr['part'],
                    attr['default_value'],
                    attr['data_type'])
                attr['param'] = param

        self.__reset_ui()

    def __reset_ui(self):
        """UIの状態を再設定する
        """

        for attr_info in self.attr_info_list:
            for attr in attr_info['attr_list']:
                if attr['type'] == 'double3':
                    if attr['param']['value']:
                        cmds.colorSliderGrp(attr['ui'], e=True, rgbValue=attr['param']['value'])
                    else:
                        cmds.colorSliderGrp(attr['ui'], e=True, rgbValue=(0.0, 0.0, 0.0))
                elif attr['type'] == 'float':
                    if attr['param']['value']:
                        cmds.floatSliderGrp(attr['ui'], e=True, value=attr['param']['value'])
                    else:
                        cmds.floatSliderGrp(attr['ui'], e=True, value=0.0)

    def __set_shader_param_value(self, attr, *args):
        """スライダーの値に応じてcgfxの値を設定する

        Args:
            attr (dict): 対象のアトリビュートの設定が入った辞書型
        """

        value = None
        if attr['type'] == 'double3':
            value = cmds.colorSliderGrp(attr['ui'], q=True, rgbValue=True)
        elif attr['type'] == 'float':
            value = cmds.floatSliderGrp(attr['ui'], q=True, value=True)
        else:
            return

        self.shader_toon_param.set_shader_toon_param(attr['attr'], attr['param']['toon_material_list'], attr['type'], value)

    def ui_body(self):
        """UI要素のみ
        """

        # spec_infoが髪限定になっているのを共通部分に
        # speculer_colorをつけたタイミングでspec_infoをつける

        self.container = cmds.columnLayout(adjustableColumn=True)
        base_class.ui.button.Button('shaderパラメータ ロード', self.reset_param)
        cmds.setParent('..')

        for attr_info in self.attr_info_list:

            cmds.frameLayout(l=attr_info['label'], cll=1, cl=0, bv=1, mw=5, mh=5)
            cmds.columnLayout(adjustableColumn=True)

            for attr in attr_info['attr_list']:

                if attr['type'] == 'double3':
                    slider = cmds.colorSliderGrp(
                        label='{0} {1}'.format(attr['part'], attr['attr']),
                        rgbValue=attr['default_value'],
                        columnAttach=([1, 'right', 5]),
                        columnWidth=([1, 170], [2, 50]),
                        changeCommand=partial(self.__set_shader_param_value, attr),
                        dragCommand=partial(self.__set_shader_param_value, attr)
                    )
                elif attr['type'] == 'float':
                    slider = cmds.floatSliderGrp(
                        label='{0} {1}'.format(attr['part'], attr['attr']),
                        field=True,
                        columnAttach=([1, 'right', 5]),
                        columnWidth=([1, 170], [2, 50]),
                        minValue=attr['min_value'] if 'min_value' in attr else 0,
                        maxValue=attr['max_value'],
                        fieldMinValue=attr['min_value'] if 'min_value' in attr else 0,
                        fieldMaxValue=attr['max_value'],
                        value=attr['default_value'],
                        precision=3,
                        changeCommand=partial(self.__set_shader_param_value, attr),
                        dragCommand=partial(self.__set_shader_param_value, attr)
                    )
                else:
                    continue

                # slider作成メソッド
                attr['ui'] = slider

            cmds.setParent('..')
            cmds.setParent('..')

        self.ui_cgfx_param_center_offset = cmds.frameLayout(l='center offset locator 選択', cll=1, cl=0, bv=1, mw=5, mh=5)
        cmds.columnLayout(adjustableColumn=True, rs=4)

        base_class.ui.button.Button(
            'head_center_offsetを選択', self.__select_center_offset_locator, 'Head_center_offset')
        base_class.ui.button.Button(
            'head_tube_center_offsetを選択', self.__select_center_offset_locator, 'Head_tube_center_offset')

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.scriptJob(event=['SceneOpened', self.reset_param], protected=True, parent=self.container)

    def __select_center_offset_locator(self, target):
        """center_offsetロケーターを選択する

        Args:
            target (str): 選択する対象のロケーター名
        """

        cmds.select(cmds.ls(target))

    def post_process(self):
        self.reset_param()
