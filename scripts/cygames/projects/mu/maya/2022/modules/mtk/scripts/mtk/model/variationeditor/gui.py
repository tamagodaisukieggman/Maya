# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

from collections import OrderedDict
import os
from functools import partial
import json

import sys
import importlib

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader

from maya.app.general.mayaMixin import MayaQWidgetBaseMixin

import maya.cmds as cmds


from . import command
from . import TITLE
from . import NAME


# 開発中はTrue、リリース時にFalse
DEV_MODE = False

if DEV_MODE:
    importlib.reload(command)
else:
    from . import logger


UI_FILE = os.path.join(os.path.dirname(__file__),
                       'variation_editor_ui.ui').replace(os.sep, '/')


VARIATION_SETTINGS = "{}_variation_settings"

COVERTER_FILE_NAME = "convert.py"


class ProgressWindowBlock(object):
    """ProgressWindowを表示させるコンテキストマネージャー
    """

    def __init__(self, title='', progress=0,  minValue=0, maxValue=100, isInterruptable=True, show_progress=True):
        self._show_progress = show_progress and (
            not cmds.about(q=True, batch=True))

        self.title = title
        self.progress = progress
        self.minValue = minValue
        self.maxValue = maxValue
        self.isInterruptable = isInterruptable

        self._start_time = None

    def __enter__(self):

        if self._show_progress:
            cmds.progressWindow(
                title=self.title,
                progress=int(self.progress),
                status='[ {} ] : Start'.format(self.title),
                isInterruptable=self.isInterruptable,
                min=self.minValue,
                max=self.maxValue + 1
            )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._show_progress:
            cmds.progressWindow(e=True, status='End ')
            cmds.progressWindow(ep=1)

    def step(self, step):
        if self._show_progress:
            cmds.progressWindow(e=True, step=step)

    def _set_status(self, status):
        if self._show_progress:
            cmds.progressWindow(
                e=True, status='[ {} / {} ] : {}'.format(self.progress, self.maxValue, status))

    def _get_status(self):
        if self._show_progress:
            return cmds.progressWindow(q=True, status=True)

    status = property(_get_status, _set_status)

    def _set_progress(self, progress):
        if self._show_progress:
            cmds.progressWindow(e=True, progress=progress)

    def _get_progress(self):
        if self._show_progress:
            return cmds.progressWindow(q=True, progress=True)

    progress = property(_get_progress, _set_progress)

    def is_cancelled(self):
        if self._show_progress:
            return cmds.progressWindow(q=True, ic=True)

    @staticmethod
    def wait(sec=1.0):
        cmds.pause(sec=sec)


class PromptDialog(QtWidgets.QInputDialog):

    def __init__(self, *args, **kwargs):
        super(PromptDialog, self).__init__(
            parent=kwargs.setdefault('parent', None),
            flags=QtCore.Qt.WindowFlags(),
        )

        self.setWindowTitle(kwargs.setdefault('title', 'title'))
        self.setLabelText(kwargs.setdefault('message', 'message'))
        self.setTextValue(kwargs.setdefault('default', ''))


TOP_GROUP_NAMES = ["top_grp"]


class VariationEditor(MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    UI = None

    cbox_default = "[ Default ]"
    variation = "variation_{}"

    def clear_memory(self):
        # column = OrderedDict()
        # column["name"] = "sub_meshes"
        # column["type"] = "S"
        # column["is_array"] = True

        # row = OrderedDict()
        # row["id"] = self.variation
        # row["sub_meshes"] = []

        # json ファイルの場所
        # シーン名と紐づけている
        self.json_path = ""

        # 読み込んだjson ファイルの内容
        self.preset_data = ""

        # サブメッシュを持ったグループノード
        # head_grp など
        self.group_nodes = []

        # サブメッシュを持ったグループノードとサブメッシュの辞書
        # グループ名はショートネーム
        # サブメッシュはロングネーム
        self.group_inside_nodes = dict()

        # シーン名を覚えておく
        self.scene_name = ""

        # mdl_mob00_m_000.ma
        self.scene_basename = ""

        # mdl_mob00_m_000
        self.scene_file_name = ""

        # mob00_m_000
        self.scene_type = ""

        self.texture_path = ""

        # サブメッシュのショートネームとUI のチェックボックスの辞書
        # チェックボックスを構築する際に初期化している
        self.node_check_box = dict()

        # 各プリセットで表示がオンになるサブメッシュ
        # sbm のプレフィックスを外したショートネームを入れる
        # 最終的にjson にsubmesh として書き出す目的
        # 最初はリストでやっていたがOrderedDictに変更
        # ID [variation_0] str:  submeshes list

        self.preset_variations = OrderedDict()

        # マテリアルのバリエーションプリセット
        # ID [variation_0] str:  name path OrderedDict
        # "mtl_mob03_m_000_face01"
        # "content/mtk/runtime/resources/characters/mtl_mob03_m_000_face01_a.mtl"

        self.preset_variation_materials = OrderedDict()

        # json ファイルのp4　での状態
        self.file_status_ext = None

        # None add checkout stale latest other などのP4 の状態
        self.stat = ""

        # 現在チェックアウトしているユーザーを取得
        self.current_users = []

        # 現在表示しているチェックボックスのグループを入れる
        self.current_group_btn = ""

        # mob_variation_settings などの文字列が入る
        # jsonファイル名の[]の中に使う
        self.json_setting_name = ""
        self._converter_path = ""
        self._converter_rer_path = ""

        # マテリアルとそれに接続されるノード（ファイルノード）の辞書
        self.material_texture = {}

        # マテリアルコンボボックスの辞書（名前とインスタンス）
        self.material_combobox = {}

        # マテリアルのパーツ名とテクスチャパスのリスト
        # マテリアルのパーツ名は一意で決まっている
        # タイプは[tops]など、[_a]などが入るものを更に区分
        # tops [u'z:/mtk/work/resources/characters/mob/03/000/texture/tex_mob03_f_000_tops_alb.tga',
        # u'z:/mtk/work/resources/characters/mob/03/000/texture/tex_mob03_f_000_tops_a_alb.tga',
        # u'z:/mtk/work/resources/characters/mob/03/000/texture/tex_mob03_f_000_tops_b_alb.tga']
        self.mat_part_texturepath = OrderedDict()

        self.material_file_node = {}

        self.group_materials = {}

        self.variation_data = command.VariationDatas()
        self.variation_data.variations = []

        self.variation_data.submeshdata = OrderedDict()
        self.variation_data.materialdata = OrderedDict()
        self.submesh_group_list = []
        self.variation_materials = OrderedDict()

    def __init__(self, parent=None):
        self.clear_memory()
        super(self.__class__, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        loader = QUiLoader()
        uiFilePath = UI_FILE
        self.UI = loader.load(uiFilePath)

        self.UI.select_preset_cbox.currentIndexChanged.connect(
            partial(self.change_preset_combo_box))
        self.UI.add_preset_btn.clicked.connect(partial(self.add_preset))
        self.UI.edit_preset_btn.clicked.connect(partial(self.edit_preset))
        self.UI.delete_preest_btn.clicked.connect(partial(self.delete_preset))
        self.UI.change_preset_name_btn.clicked.connect(
            partial(self.change_preset_name))
        # self.UI.convert_btn.clicked.connect(partial(self.convert_json))
        # self.UI.convert_btn.setEnabled(False)

        self.UI.save_btn.clicked.connect(partial(self.save_json))
        self.UI.submit_btn.clicked.connect(partial(self.submit_data))
        self.UI.rename_submesh_btn.clicked.connect(
            partial(self.rename_submeshes))
        self.UI.refresh_btn.clicked.connect(partial(self.refresh))
        self.build_buttons()
        self.read_preset()

        self.resize(530, 760)
        self.setWindowTitle(TITLE)
        self.setCentralWidget(self.UI)

        cmds.scriptJob(event=("SceneOpened", self.read_preset),
                       parent=self.objectName())

    def refresh(self):
        self.get_material_textures()
        self.get_groups()
        self.init_ui_setting()
        self.change_preset_combo_box()

    def convert_json(self):
        """Cyllista モジュールを使える3系Pythonで[convert.py]を実行させる

        """
        command.convert_json(self.json_path)

    def rename_submeshes(self, *args):
        """
        sbm1_head_001_grp のsbm1 部分をモデルエディタで見るときは変える必要があるため
        sbm1　で表示sbm0 で非表示
        """

        for i, group in enumerate(self.submesh_group_list):
            if group.visible:
                group.change_switch(1)
            else:
                group.change_switch(0)

        self.change_preset_combo_box()

    def init_ui_setting(self):
        self.check_boxs = []
        self.verticalSpacer = None

    def reset_cbox(self):
        self.UI.select_preset_cbox.clear()
        self.UI.select_preset_cbox.addItem(self.cbox_default)

    def change_preset_name(self, *args):
        """プリセットの名前の編集
        """
        _current_preset = self.UI.select_preset_cbox.currentText()
        _current_preset_index = self.UI.select_preset_cbox.currentIndex()

        if _current_preset == self.cbox_default:
            command._message_dialog(
                u" {}  は変更することができません".format(self.cbox_default))
            return

        dialog = PromptDialog(title=u'Input New Preset Name',
                              message=u'新たなバリエーション名を入力してください',
                              default=_current_preset)
        result = dialog.exec_()
        if not result:
            return
        _text = dialog.textValue()

        for _t in _text:
            if _t in u':;/\|,*?"<>':
                command._message_dialog(u'「　]:;/\|,*?"<>　」  の含まれるテキストは使用できません')
                return

        if _text in self.preset_variations.keys():
            command._message_dialog(u"[ {} ] は既に存在する名前です".format(_text))
            return

        _new_submesh_groups = self.variation_data.submeshdata[_current_preset]

        self.variation_data.variations[_current_preset_index-1] = _text

        self.variation_data.submeshdata[_text] = _new_submesh_groups
        del self.variation_data.submeshdata[_current_preset]

        if _current_preset in self.variation_data.materialdata:
            variation_materials = self.variation_data.materialdata[_current_preset]
            self.variation_data.materialdata[_text] = variation_materials
            del self.variation_data.materialdata[_current_preset]

        self.UI.select_preset_cbox.removeItem(_current_preset_index)
        self.UI.select_preset_cbox.setCurrentIndex(_current_preset_index-1)

        self.UI.select_preset_cbox.clear()
        self.UI.select_preset_cbox.addItem(self.cbox_default)
        for variation_id in self.variation_data.variations:
            self.UI.select_preset_cbox.addItem(variation_id)
        self.UI.select_preset_cbox.setCurrentText(_text)

    def add_preset(self, *args):
        """
        プリセットの追加
        """
        _new_submesh_groups = []
        variation_materials = OrderedDict()
        for group in self.submesh_group_list:
            if group.visible:
                _new_submesh_groups.append(group.no_switch_name)
            for mat in group.material_obj:
                if mat.current_texture != mat.default_texture:
                    variation_materials[mat.material] = mat.current_texture
        _ids = self.variation_data.variations
        if _ids:
            _last_id = _ids[-1]
            _next_num = int(_last_id.split("_")[-1])+1
        else:
            _next_num = 0
        _next_id = self.variation.format(_next_num)
        self.variation_data.variations.append(_next_id)
        self.variation_data.submeshdata[_next_id] = _new_submesh_groups
        self.variation_data.materialdata[_next_id] = variation_materials
        self.UI.select_preset_cbox.addItem(_next_id)
        self.UI.select_preset_cbox.setCurrentIndex(
            len(self.variation_data.variations))
        command._message_dialog(u"プリセット [ {} ] を追加しました".format(_next_id))

    def edit_preset(self, *args):
        """プリセットの編集
        """

        _current_preset = self.UI.select_preset_cbox.currentText()
        if _current_preset == self.cbox_default:
            command._message_dialog(
                u" {}  は変更することができません".format(self.cbox_default))
            return

        if not command._confirm_dialog(u"[ {} ] の内容を変更しますか？".format(_current_preset)):
            return

        _new_submesh_groups = []
        variation_materials = OrderedDict()

        for i, group in enumerate(self.submesh_group_list):
            if group.visible:

                _new_submesh_groups.append(group.no_switch_name)

            for mat in group.material_obj:
                if mat.current_texture != mat.default_texture:
                    variation_materials[mat.material] = mat.current_texture

        self.variation_data.submeshdata[_current_preset] = _new_submesh_groups
        self.variation_data.materialdata[_current_preset] = variation_materials

        command._message_dialog(
            u"プリセット [ {} ] の修正を記憶しました".format(_current_preset))

    def delete_preset(self, *args):
        """プリセットの削除
        """
        _current_preset = self.UI.select_preset_cbox.currentText()
        _current_preset_index = self.UI.select_preset_cbox.currentIndex()
        if _current_preset == self.cbox_default:
            command._message_dialog(
                u" {}  は削除することができません".format(self.cbox_default))
            return

        if not command._confirm_dialog(u"[ {} ] を削除しますか？".format(_current_preset)):
            return

        del self.variation_data.variations[_current_preset_index-1]
        del self.variation_data.submeshdata[_current_preset]

        if _current_preset in self.variation_data.materialdata:
            del self.variation_data.materialdata[_current_preset]

        self.UI.select_preset_cbox.removeItem(_current_preset_index)
        self.UI.select_preset_cbox.setCurrentIndex(_current_preset_index-1)

    def change_preset_combo_box(self, *args):
        """combo box で選択したプリセットに合わせて
        サブメッシュグループの表示を切り替える
        プリセットが存在しない場合は[ default ]が表示される
        その場合は001のノードが表示
        表示に合わせてチェックボックスがあればチェックボックスの値も変化
        """

        _current_preset = self.UI.select_preset_cbox.currentText()

        current_group = None
        _current_submesh_setting = None

        if _current_preset in self.variation_data.submeshdata:
            _current_submesh_setting = self.variation_data.submeshdata[_current_preset]

        for i, group in enumerate(self.submesh_group_list):

            _vis_flag = False
            if group.check_box:
                current_group = group.group_short_name

            if not _current_submesh_setting:
                if group.id == "001":
                    _vis_flag = True
            else:
                if group.no_switch_name in _current_submesh_setting:
                    _vis_flag = True

            for mat in group.material_obj:

                mat.chenge_assign_texture()
                current_material = self.variation_data.materialdata.get(
                    _current_preset)

                if current_material and mat.material in current_material:
                    change_texture = current_material.get(mat.material)
                    if mat.current_texture != change_texture:
                        mat.chenge_assign_texture(change_texture)

            if _vis_flag:
                group.set_visible(True)
            else:
                group.set_visible(False)

        self.delete_ckeck_boxs()
        if current_group:
            self.build_checkboxs(current_group)
        self.delete_combo_boxs()
        self.build_combo_boxs()

    def closeEvent(self, event):

        if self.UI.select_preset_cbox.count() == 1:
            self.UI.select_preset_cbox.setCurrentIndex(0)
        else:
            self.UI.select_preset_cbox.setCurrentIndex(1)
        self.rename_submeshes()
        for mat_name, mat_obj in self.variation_materials.items():
            mat_obj.chenge_assign_texture()
        event.accept()

    def build_buttons(self):
        all_btns = self.UI.findChildren(QtWidgets.QPushButton)
        for _btn in all_btns:
            _name = _btn.objectName().rsplit("_", 1)

            if "shoes" in _name[0]:
                _btn.clicked.connect(lambda: self._on_button_clicked("shoes"))

            if len(_name) != 1 and _name[-1] == "btn" and _name[0] in command.GROUP_NAMES:
                _btn.clicked.connect(
                    partial(self._on_button_clicked, _name[0]))

    def _on_button_clicked(self, btn):
        """グループの基本的な名前[head]

        Args:
            btn (str): head
        """

        self.delete_ckeck_boxs()
        self.delete_combo_boxs()

        if btn in [x.group_short_name for x in self.submesh_group_list]:
            self.build_checkboxs(btn)
        self.build_combo_boxs()

    def delete_ckeck_boxs(self):
        for i in reversed(range(self.UI.checkBox_verticalLayout.count())):
            _widget = self.UI.checkBox_verticalLayout.itemAt(i)
            if isinstance(_widget, QtWidgets.QSpacerItem):
                self.UI.checkBox_verticalLayout.removeItem(_widget)
            else:
                _widget.widget().setParent(None)
                # _widget.widget().deleteLater()

    def delete_combo_boxs(self):

        for i in reversed(range(self.UI.material_combobox_layout.count())):
            _widget = self.UI.material_combobox_layout.itemAt(i)

            if isinstance(_widget, QtWidgets.QSpacerItem):
                self.UI.material_combobox_layout.removeItem(_widget)
            else:
                _widget.widget().deleteLater()

    def build_checkboxs(self, group_name):
        for i, group in enumerate(self.submesh_group_list):
            if group.group_short_name == group_name:
                _check_box = QtWidgets.QCheckBox('{}'.format(group.short_name))
                _check_box.clicked.connect(
                    partial(self.check_box_click, i, group.short_name))
                self.UI.checkBox_verticalLayout.addWidget(_check_box)

                if group.visible:
                    _check_box.setChecked(1)
                else:
                    _check_box.setChecked(0)

                self.submesh_group_list[i].check_box = _check_box
            else:
                self.submesh_group_list[i].check_box = ""

        self.verticalSpacer = QtWidgets.QSpacerItem(20, 40,
                                                    QtWidgets.QSizePolicy.Minimum,
                                                    QtWidgets.QSizePolicy.Expanding)
        self.UI.checkBox_verticalLayout.addItem(self.verticalSpacer)

    def check_box_click(self, num, group):
        if self.submesh_group_list[num].check_box.isChecked():
            self.submesh_group_list[num].set_visible(True)
        else:
            self.submesh_group_list[num].set_visible(False)

        self.delete_combo_boxs()
        self.build_combo_boxs()

    def on_combobox_changed(self, *args):
        if not args:
            return
        current_select = args[0]

        for group in self.submesh_group_list:
            if group.check_box and group.check_box.isChecked():
                for mat in group.material_obj:
                    mat.chenge_assign_texture(current_select)

    def build_combo_boxs(self):
        if not self.UI.checkBox_verticalLayout.count():
            return
        _pool = []
        for i, group in enumerate(self.submesh_group_list):
            if group.check_box and group.check_box.isChecked():
                for n, mat in enumerate(group.material_obj):
                    if mat not in _pool:
                        _pool.append(mat)
                        _combo_box = QtWidgets.QComboBox()
                        self.submesh_group_list[i].material_obj[n].combo_box = _combo_box
                        _current_material = self.submesh_group_list[i].material_obj[n].current_texture

                        for _ in mat.variation_textures.keys():
                            _combo_box.addItem(_)
                        _combo_box.currentTextChanged.connect(
                            partial(self.on_combobox_changed))

                        _combo_box.setCurrentIndex(
                            list(mat.variation_textures.keys()).index(_current_material))
                        self.UI.material_combobox_layout.addWidget(_combo_box)
                    else:
                        self.submesh_group_list[i].material_obj[n].combo_box = None
        verticalSpacer = QtWidgets.QSpacerItem(20, 40,
                                               QtWidgets.QSizePolicy.Minimum,
                                               QtWidgets.QSizePolicy.Expanding)
        self.UI.material_combobox_layout.addItem(verticalSpacer)

    def get_scene_name(self):
        """シーン名取得
        cmds で取得できない時のためにOpenMayaでもやってみる
        シーン名からjsonファイルを特定
        """
        self.clear_memory()
        scene_names = command.get_scene_name()
        self.scene_name = scene_names[0]

        # mdl_mob00_m_000.ma
        self.scene_basename = scene_names[1]

        # mdl_mob00_m_000
        self.scene_file_name = scene_names[2]

        # mob00_m_000
        self.scene_type = scene_names[3]

        # mob00_m
        self.charactor_type = scene_names[4]

        return scene_names[0]

    def get_json_path(self):
        print(" ----------  get_material_textures")
        json_datas = command.get_json_path(
            self.scene_name, self.scene_file_name, self.charactor_type)
        if not json_datas:
            return
        print(json_datas, " --- json_datas")
        self.json_path = json_datas[0]
        self._converter_rer_path = json_datas[1]
        self.variation_data.name = json_datas[2]

    def get_material_textures(self):
        print(" ----------  get_material_textures")
        variation_materials = command.get_material_obj(self.scene_name)
        print(variation_materials, " --- variation_materials")
        self.variation_materials = variation_materials
        return variation_materials

    def get_groups(self):
        print(" ----------  get_groups")
        submesh_group_list = command.get_groups(self.variation_materials)
        print(submesh_group_list, " --- submesh_group_list")
        self.submesh_group_list = submesh_group_list
        return submesh_group_list

    def read_preset(self):
        """script job によりシーンを開くごとに呼び出される

        シーン名取得
        UIの初期化（ボタンとチェックボックス）
        シーン内のグループ取得
        P4で最新取得
            json読み込み
            チェックボックス構築

        適切なシーンでない場合
            ウィンドウを閉じてメッセージ表示
        """
        _m = ""
        preset_data = None

        if not self.get_scene_name():
            self.close()
            _m = u"シーンを開いてから実行してください\n"
            _m += u"ウィンドウを閉じます"
            command._message_dialog(_m)
            print(_m)
            return

        print("scene name ---- ", self.scene_name)
        print("scene_basename ---- ", self.scene_basename)
        print("scene_file_name ---- ", self.scene_file_name)
        print("scene_type ---- ", self.scene_type)
        print("self.charactor_type --- ", self.charactor_type)

        self.get_json_path()

        if not self.get_newest_file():
            return

        if not self.get_material_textures():
            self.close()
            _m = u"適切なテクスチャを見つけられませんでした\n"
            _m += u"ウィンドウを閉じます"
            command._message_dialog(_m)
            print(_m)
            return

        if not self.get_groups():
            self.close()
            _m = u"適切なジオメトリを見つけられませんでした\n"
            _m += u"ウィンドウを閉じます"
            command._message_dialog(_m)
            print(_m)
            return

        self.init_ui_setting()

        if self.json_path and os.path.exists(self.json_path):
            with open(self.json_path, "r") as json_data:
                preset_data = json.load(json_data)

        if preset_data:
            if preset_data["row"]:
                for i, _rows in enumerate(preset_data["row"]):
                    if _rows:
                        variation_materials = OrderedDict()
                        for k, v in _rows.items():

                            if k == "id":
                                self.variation_data.variations.append(v)

                            elif k.startswith("sub_meshes"):
                                self.variation_data.submeshdata[_rows["id"]] = v
                            elif k.startswith("mtl"):
                                if not v:
                                    texture_variation_name = k[4:]
                                    texture_variation_name = self.scene_type + "_" + texture_variation_name
                                    variation_materials[k] = texture_variation_name
                                else:
                                    runtime_path = v
                                    basename = runtime_path.rsplit("/", 1)[-1]
                                    if "." in basename:
                                        basename, ext = basename.rsplit(".", 1)
                                    texture_variation_name = basename[4:]
                                    variation_materials[k] = texture_variation_name
                        self.variation_data.materialdata[_rows["id"]
                                                         ] = variation_materials
        # else:
        #     _m = u"json データがありません"
        #     command._message_dialog(_m)
        #     print(_m)

        self.set_up_preset_combobox()

    def set_up_preset_combobox(self):
        if self.variation_data:
            self.reset_cbox()
            for var in self.variation_data.variations:
                self.UI.select_preset_cbox.addItem(var)

        if self.UI.select_preset_cbox.count() == 1:
            self.UI.select_preset_cbox.setCurrentIndex(0)
        else:
            self.UI.select_preset_cbox.setCurrentIndex(1)

    def get_p4_file_state(self):
        """
        P4のファイルステータス取得
        ドライブレターが大文字の場合に取れないケースがあった
        しかし、小文字にして取ると、取ることはできるが別のファイルと認識される
        Mayaを再起動すると取れたりする
        """
        p4_state = command.get_p4_file_state(self.json_path)
        self.file_status_ext = p4_state[0]
        self.stat = p4_state[1]
        self.current_users = p4_state[2]

    def get_newest_file(self):
        """
        p4 での最新データ取得
        """
        flag = command.get_newest_file(self.json_path)
        return flag

    def submit_data(self, *args):
        command.submit_data(self.json_path)

    def save_json(self, *args):
        command.save_json(self.json_path, self.variation_data,
                          self.variation_materials)


def main():

    for _obj in QtWidgets.QApplication.allWidgets():
        if _obj.__class__.__name__ == NAME:
            _obj.close()
            del _obj

    if not os.path.exists(UI_FILE):
        cmds.warning(u"UI ファイルが見つかりません")
        return

    ui = VariationEditor()
    ui.show()
