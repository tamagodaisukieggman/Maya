# -*- coding: utf-8 -*-
u"""キャラ用のツールをまとめたウィンドウ

..
    BEGIN__CYGAMES_MENU
    label=CyCharaTools ... : キャラツール
    command=main()
    order=1000
    END__CYGAMES_MENU

:詳細: file:///Z:/mtku/tools/maya/doc/manual/sources/window/charatools.rst

"""
import os
from distutils.util import strtobool

import maya.cmds as cmds
import maya.mel as mel

import mtku.maya.menus.modeling.checkpadding as checkpadding
import mtku.maya.menus.modeling.checkweights.command as checkweights
import mtku.maya.menus.modeling.copyhairweight as copyhairweight
import mtku.maya.menus.modeling.deformhair as deformhair
# import mtku.maya.menus.modeling.deletehistory as deletehistory
import mtku.maya.menus.modeling.duplicatekeepingweight as duplicatekeeping
import mtku.maya.menus.modeling.insertedges as insertedges
import mtku.maya.menus.modeling.reductedgering as reductedgering
import mtku.maya.menus.select.selectedgering.gui as selectedgering
from mtku.maya.base.window import BaseWindow
from mtku.maya.constant import MTK_MAYA_MANUAL_HELP_URL
from mtku.maya.utils.history import MtkHistory


class CharaTools(BaseWindow):

    def __init__(self, *args, **kwargs):
        u"""初期化"""
        super(CharaTools, self).__init__(*args, **kwargs)

        self._url = '{}/window/charatools.html'.format(MTK_MAYA_MANUAL_HELP_URL)

        dirpath = os.path.dirname(__file__)
        # UI File
        self._hair_file = '{0}/hair.ui'.format(dirpath)
        self._weight_file = '{0}/weight.ui'.format(dirpath)
        self._modeling_file = '{0}/modeling.ui'.format(dirpath)
        # Layout, Control
        self._setup_ui = None
        self._hair_ui = None
        self._weight_ui = None
        self._modeling_ui = None
        self._options_frames = {}  # {option名: frameLayout名}

    def _read_settings(self):
        u"""設定の読み込み(mayaPrefsからUIへ)"""
        # 各UIに値をセットするための関数
        def set_values_to_uis(optionvars, uis, func):
            for option, ui in zip(optionvars, uis):
                func(ui, cmds.optionVar(q=option))

        def set_bool(value):
            return strtobool(value) if value else False

        def set_frame(frame, value):
            return cmds.frameLayout(frame, e=True, cl=set_bool(value)) if value else None
        set_values_to_uis(self._options_frames.keys(), self._options_frames.values(), set_frame)

    def save_settings(self, *args):
        u"""設定の保存

        :param args:
        :return: {option名: 設定値}
        :rtype: dict
        """
        # 各UIから値を読むための関数
        def set_values_to_dict(dict_, optionnames, uis, func):
            for option, ui in zip(optionnames, uis):
                dict_[option] = func(ui)

        def read_frame(frame):
            return cmds.frameLayout(frame, q=True, cl=True)
        # ----

        settings = {}
        # UIの値をDictにセット
        set_values_to_dict(
            settings, self._options_frames.keys(), self._options_frames.values(), read_frame,
        )
        # mayaPrefsに保存
        [cmds.optionVar(sv=(k, v)) for k, v in settings.items()]

        return settings

    def reset_settings(self, *args):
        u"""設定のリセット"""
        # frameLayoutの初期値は折りたたまない
        for frame in self._options_frames.values():
            cmds.frameLayout(frame, e=True, cl=False)

    def help(self, *args):
        u"""help表示"""
        cmds.showHelp(self._url, a=True)

    def _connect(self):
        u"""UIとコマンドの接続"""
        # frameLayout
        for ui in self._options_frames.values():
            cmds.frameLayout(ui, e=True, cc=self.save_settings, ec=self.save_settings)

        print(self._options_frames.values())
        self._weight_ui.push_button_check.clicked.connect(self.click_check_weights)
        self._weight_ui.push_button_modify.clicked.connect(self.click_set_weights)
        self._weight_ui.push_button_delete_history.clicked.connect(self.click_delete_history)
        self._weight_ui.push_button_tool_copy.clicked.connect(self.click_oepn_weighteditor)

        self._modeling_ui.push_button_select.clicked.connect(self.click_select_edgerings)
        self._modeling_ui.push_button_insert.clicked.connect(self.click_insert_edges)
        self._modeling_ui.push_button_duplicatekeepingweight.clicked.connect(self.click_duplicate_keeping_weight)
        self._modeling_ui.push_button_checkpadding.clicked.connect(self.click_check_padding)

        self._hair_ui.push_button_reduct.clicked.connect(self.click_reduct_hair)
        self._hair_ui.push_button_copyweights.clicked.connect(self.click_copy_hairweight)
        self._hair_ui.push_button_deform.clicked.connect(self.click_deform_hair)

    def click_check_padding(self, *args):
        checkpadding.main()

    def click_check_weights(self, *args):
        checkweights.check_weights()

    def click_set_weights(self, *args):
        checkweights.set_weights()

    def click_delete_history(self, *args):
        # deletehistory.main()
        MtkHistory.delete_history()

    def click_oepn_weighteditor(self, *args):
        mel.eval('python("import CyWeightEditor;CyWeightEditor.UI()")')

    def click_select_edgerings(self, *args):
        selectedgering.main()

    def click_insert_edges(self, *args):
        insertedges.main()

    def click_duplicate_keeping_weight(self, *arg):
        duplicatekeeping.main()

    def click_reduct_hair(self, *arg):
        reductedgering.main()

    def click_copy_hairweight(self, *arg):
        copyhairweight.main()

    def click_deform_hair(self, *arg):
        deformhair.main()

    def create(self):
        u"""Windowのレイアウト作成"""
        # レイアウト生成
        self._weight_ui = self._add_framelayout('weightFrame', 'Weight', (0.0, 0.5, 0.5), self._weight_file)
        self._modeling_ui = self._add_framelayout('modelingFrame', 'Modeling', (0.0, 0.5, 0.5), self._modeling_file)
        self._hair_ui = self._add_framelayout('hairFrame', 'Hair', (0.0, 0.5, 0.5), self._hair_file)
        # 設定の読み込み
        self._read_settings()
        # UIとコマンドの接続
        self._connect()

    def _add_framelayout(self, optionname, label, bgc=(0.3, 0.3, 0.3), ui_file=None):
        u"""frameLayoutの追加関数

        :param optionname: mayaPrefsに保存する際のoption名
        :type optionname: str
        :param label: frameLayoutのラベル名
        :type label: str
        :param bgc: background color
        :type bgc: list or tuple
        :param ui_file: ui_fileのフルパス
        :type ui_file: str
        :return: ui
        :rtype: QWidget
        """
        # Layout
        frame = cmds.frameLayout(l=label, bgc=bgc, cll=True)
        if ui_file:
            ui = self.load_file(ui_file)
        cmds.setParent('..')

        # optionVar名とコントロール名を設定
        option = '{0}.{1}'.format(__package__, optionname)  # パッケージ名の補完(重複防止)
        self._options_frames[option] = frame
        return ui


def main():
    u"""ウィンドウ表示"""
    win = CharaTools(typ=2)
    win.width = 300
    win.height = 520
    win.show()
