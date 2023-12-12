# -*- coding: utf-8 -*-
from maya import cmds


class FramerateSettings:
    def __init__(self, time):
        self.project_time = time
        self.scene_time = cmds.currentUnit(q=True, time=True)

    def _set_option_framerate(self):
        """optionVarに入る、ローカル環境のfps設定を変更"""
        cmds.optionVar(stringValue=("workingUnitTimeDefault", self.project_time))

    def _set_current_framerate(self):
        """現在のシーンのフレームレートを変更"""
        if self.scene_time != self.project_time:
            cmds.currentUnit(time=self.project_time)

    def set_framerate(self):
        """フレームレートの設定
        環境の設定と現在のシーンの設定を行う
        """
        self._set_option_framerate()
        self._set_current_framerate()
