# -*- coding: utf-8 -*-
u"""InsertEdges (GUI)

.. END__CYGAMES_DESCRIPTION
"""
from distutils.util import strtobool

import maya.cmds as cmds

from .command import InsertEdgesCmd
from mtku.maya.mtklog import MtkLog
from mtku.maya.base.window import BaseWindow


logger = MtkLog(__name__)


class InsertEdges(BaseWindow):

    def __init__(self, *args, **kwargs):
        u"""初期化"""
        # OptionName
        self._key_radio_group = '{0}.radio_btn'.format(__package__)
        self._key_checkbox = '{0}.checkbox'.format(__package__)
        self._key_length_slider = '{0}.length_slider'.format(__package__)
        self._key_angle_slider = '{0}.angle_slider'.format(__package__)

        self._url = 'https://wisdom.cygames.jp/pages/viewpage.action?pageId=37552769'

        super(InsertEdges, self).__init__(*args, **kwargs)

    def create(self):
        u"""Windowのレイアウト作成"""
        self._add_layout()
        self._read_settings()
        self._change_radio_command()
        self._connect()

    def _add_layout(self):
        u"""レイアウトの追加"""
        cmds.frameLayout(l='Settings')
        self._radio_group = cmds.radioButtonGrp(
            l='Split Mode:', nrb=2, sl=1,
            la2=['One Side', 'Both Sides'],
            cw3=[100, 120, 120], ct3=['right', 'left', 'left'], co3=[0, 10, 10],
        )
        self._checkbox = cmds.checkBoxGrp(
            l='', l1='Invert', ncb=1,
            cw2=[100, 80], co2=[0, 10], ct2=['right', 'left'],
            v1=False,
        )
        self._length_slider = cmds.floatSliderGrp(
            l='Length (cm):',
            cw3=[100, 80, 256], co3=[0, 10, 10], ct3=['right', 'right', 'right'],
            f=True, v=0.5, min=0.001, fmn=0.001, max=100, fmx=100000, pre=3, s=0.01,
        )
        self._angle_slider = cmds.floatSliderGrp(
            l='Smoothing angle :',
            cw3=[100, 80, 256], co3=[0, 10, 10], ct3=['right', 'right', 'right'],
            f=True, v=0.0, min=0, fmn=0, max=180, fmx=180, pre=3, s=0.01,
        )
        cmds.setParent('..')

    def help(self, *args):
        u"""help表示"""
        cmds.showHelp(self._url, a=True)

    def save_settings(self, *args):
        u"""設定の保存

        :return: {
            __package__+.'radio_btn': int,
            __package__+'.checkbox': bool,
            __package__+'.length_slider': float,
            __package__+'.angle_slider': float,
        }
        :rtype: dict
        """
        settings = {
            self._key_radio_group: cmds.radioButtonGrp(self._radio_group, q=True, sl=True),
            self._key_checkbox: cmds.checkBoxGrp(self._checkbox, q=True, v1=True),
            self._key_length_slider: cmds.floatSliderGrp(self._length_slider, q=True, v=True),
            self._key_angle_slider: cmds.floatSliderGrp(self._angle_slider, q=True, v=True),
        }
        # mayaPrefsに保存
        [cmds.optionVar(sv=(k, v)) for k, v in settings.items()]

        logger.debug(settings)
        return settings

    def reset_settings(self, *args):
        u"""設定のリセット"""
        cmds.radioButtonGrp(self._radio_group, e=True, sl=1)
        cmds.checkBoxGrp(self._checkbox, e=True, v1=False)
        cmds.floatSliderGrp(self._length_slider, e=True, v=0.5)
        cmds.floatSliderGrp(self._angle_slider, e=True, v=0.0)

        self.save_settings()

    def _read_settings(self):
        """設定の読み込み"""
        value_radio_group = int(cmds.optionVar(q=self._key_radio_group))
        value_checkbox = strtobool(str(cmds.optionVar(q=self._key_checkbox)))
        value_length_slider = float(cmds.optionVar(q=self._key_length_slider))
        value_angle_slider = float(cmds.optionVar(q=self._key_angle_slider))

        if value_radio_group:
            cmds.radioButtonGrp(self._radio_group, e=True, sl=value_radio_group)
        cmds.checkBoxGrp(self._checkbox, e=True, v1=value_checkbox)
        if value_length_slider:
            cmds.floatSliderGrp(self._length_slider, e=True, v=value_length_slider)
        if value_angle_slider:
            cmds.floatSliderGrp(self._angle_slider, e=True, v=value_angle_slider)

    def _change_radio_command(self, *args):
        u"""Radio Buttonの切り替え時の処理"""
        if cmds.radioButtonGrp(self._radio_group, q=True, sl=True) == 1:
            cmds.checkBoxGrp(self._checkbox, e=True, enable=True)
        else:
            cmds.checkBoxGrp(self._checkbox, e=True, enable=False)
        self.save_settings()

    def _connect(self):
        u"""UIとコマンドの接続"""
        cmds.radioButtonGrp(self._radio_group, e=True, cc=self._change_radio_command)
        cmds.checkBoxGrp(self._checkbox, e=True, cc=self.save_settings)
        cmds.floatSliderGrp(self._length_slider, e=True, cc=self.save_settings)
        cmds.floatSliderGrp(self._angle_slider, e=True, cc=self.save_settings)

    def apply_(self, *args):
        u"""Applyボタンの実行コマンド"""
        edges = cmds.ls(sl=True, fl=True)
        if not edges:
            return

        settings = self.save_settings()
        mode = settings[self._key_radio_group]
        inverse = settings[self._key_checkbox]
        distance = settings[self._key_length_slider]
        angle = settings[self._key_angle_slider]

        InsertEdgesCmd.main(edges, mode, inverse, distance, angle)
        cmds.select(edges)
