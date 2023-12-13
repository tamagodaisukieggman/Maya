# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
    from builtins import object
    from importlib import reload
except Exception:
    pass

import sys
import os
import subprocess

import maya.cmds as cmds
import maya.mel as mel
import shiboken2

from maya import OpenMayaUI
from PySide2 import QtWidgets

from .. import base_common
from ..base_common import classes as base_class

from ..glp_common.classes.info import chara_info

from . import view
from . import eye_cover_setup
from . import attribute_transfer
from . import eye_cover_facial_setup
from . import texture_bake_to_eye_cover

reload(view)
reload(base_common)
reload(eye_cover_setup)
reload(attribute_transfer)
reload(eye_cover_facial_setup)
reload(texture_bake_to_eye_cover)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Main(object):

    # ===============================================
    def __init__(self):
        """コンストラクタ
        """

        self.view = view.View()
        self.tool_version = '22061501'
        self.tool_name = 'GallopEyeCoverTool'
        self.window_name = self.tool_name + 'Win'
        self.view.setWindowTitle(self.window_name)

        # フェイシャルセットアップ用の値
        # 初期値を入れておくが、実行時にUIから拾う値
        self.x_offset = 1.5
        self.z_offset = -2.5
        self.bind_joint = 'Eye_bottom_01_L'

        # セットアップデータ関連
        self.is_setup_data_loaded = False
        self.data_file_name = 'eye_cover_setup_data.txt'
        self.data_separater = ','
        self.x_offset_header = 'X_OFFSET:'
        self.bind_header = 'BIND:'

    # ===============================================
    def deleteOverlappingWindow(self, target):
        """Windowの重複削除処理
        """

        main_window = OpenMayaUI.MQtUtil.mainWindow()
        if main_window is None:
            return

        if sys.version_info.major == 2:
            main_window = shiboken2.wrapInstance(long(main_window), QtWidgets.QMainWindow)
        else:
            # for Maya 2022-
            main_window = shiboken2.wrapInstance(int(main_window), QtWidgets.QMainWindow)

        for widget in main_window.children():
            if str(type(target)) == str(type(widget)):
                widget.closeEvent(None)
                widget.deleteLater()

    # ===============================================
    def show_ui(self):
        """UI描画
        """

        # windowの重複削除処理
        self.deleteOverlappingWindow(self.view)

        # 初期化
        self.initialize_view_param()
        self.setup_view_event()

        # 表示
        self.update_view()
        self.view.show()

    # ===============================================
    def initialize_view_param(self):
        """UIパラメーターの初期化
        """

        self.view.ui.BindLineEdit.setText(self.bind_joint)
        self.view.ui.XOffsetSpinBox.setValue(self.x_offset)
        self.view.ui.MFaceSetupLabel2.setStyleSheet('QLabel { color : yellow; }')

        self.tex_bake_selection_change_event()

    # ===============================================
    def setup_view_event(self):
        """イベントのセット
        """

        self.view.connectCallback(self.tex_bake_selection_change_event)
        self.view.ui.TexBakeButton.clicked.connect(self.tex_bake_button_event)
        self.view.ui.NormalColorSetupButton.clicked.connect(self.normal_color_setup_button_event)
        self.view.ui.MFaceSetupButton.clicked.connect(self.m_face_setup_button_event)
        self.view.ui.GetDataButton.clicked.connect(self.get_data_button_event)
        self.view.ui.BindLineEdit.textChanged.connect(self.data_set_event)
        self.view.ui.XOffsetSpinBox.valueChanged.connect(self.data_set_event)
        self.view.ui.FacialSetupButton.clicked.connect(self.facial_setup_button_event)
        self.view.ui.CreateNewDataButton.clicked.connect(self.create_new_data_button_event)

    # ===============================================
    def update_view(self):
        """UIの更新
        """

        if self.is_setup_data_loaded:
            self.view.ui.DataInfoLabel.setText('セットアップデータの値を使用しています')
            self.view.ui.DataInfoLabel.setStyleSheet('QLabel { color : #55ff00; }')
        else:
            self.view.ui.DataInfoLabel.setText('セットアップデータの値を使用していません')
            self.view.ui.DataInfoLabel.setStyleSheet('QLabel { color : yellow; }')

    # ===============================================
    def tex_bake_selection_change_event(self, *args, **kwargs):
        """選択変更時にテクスチャベイク情報を更新するコールバックイベント

        ベイクにはベイク先・ベイク元のメッシュを順番に選択する必要があるため、
        選択状態を表示し、2つそろった時点で緑表示にする
        """

        self.view.ui.BakeDstEditLabel.clear()
        self.view.ui.BakeSrcEditLabel.clear()
        self.view.ui.BakeDstEditLabel.setStyleSheet('QLabel { color : yellow; }')
        self.view.ui.BakeSrcEditLabel.setStyleSheet('QLabel { color : yellow; }')

        selection_list = cmds.ls(sl=True, type='transform')

        if not selection_list:
            return

        self.view.ui.BakeDstEditLabel.setText(selection_list[0])

        if len(selection_list) < 2:
            return

        self.view.ui.BakeSrcEditLabel.setText(selection_list[1])
        self.view.ui.BakeDstEditLabel.setStyleSheet('QLabel { color : #55ff00; }')
        self.view.ui.BakeSrcEditLabel.setStyleSheet('QLabel { color : #55ff00; }')

    # ===============================================
    def tex_bake_button_event(self):
        """テクスチャベイクボタンイベント
        """

        # ベイク先・ベイク元のメッシュが表示されているはずなので、テキストを取得する
        src = self.view.ui.BakeSrcEditLabel.text()
        dst = self.view.ui.BakeDstEditLabel.text()

        if not src or not dst:
            cmds.warning('ベイク先・ベイク元が選択されていません')
            return

        self.bake_texture(src, dst)

    # ===============================================
    def normal_color_setup_button_event(self):
        """法線・頂点カラーのセットアップボタンイベント
        """

        self.normal_color_setup()

    # ===============================================
    def m_face_setup_button_event(self):
        """M_Faceへの仕込みボタンイベント
        """

        # セットアップ実行
        left_x_offset, bind_joint = self.m_face_setup()

        # セットアップデータの出力とUI更新
        setup_data_path = self.__get_setup_data_path()
        if not setup_data_path:
            cmds.warning('セットアップデータのパスが取得できませんでした')
            return

        self.__output_setup_data(setup_data_path, left_x_offset, bind_joint)
        self.__load_setup_data_to_ui(setup_data_path)
        self.update_view()

    # ===============================================
    def get_data_button_event(self):
        """セットアップデータの取得ボタンイベント
        """

        setup_data_path = self.__get_setup_data_path()
        if not setup_data_path:
            cmds.warning('セットアップデータのパスが取得できませんでした')
            return

        self.__load_setup_data_to_ui(setup_data_path)
        self.update_view()

    # ===============================================
    def data_set_event(self):
        """パラメーター変更時イベント
        """

        self.is_setup_data_loaded = False
        self.update_view()

    # ===============================================
    def facial_setup_button_event(self):
        """フェイシャルセットアップボタンイベント
        """

        self.x_offset = float(self.view.ui.XOffsetSpinBox.value())
        self.bind_joint = str(self.view.ui.BindLineEdit.text())
        self.facial_setup()

    # ===============================================
    def create_new_data_button_event(self):
        """セットアップデータ新規生成ボタンイベント
        """

        setup_data_path = self.__get_setup_data_path()
        if not setup_data_path:
            cmds.warning('セットアップデータのパスが取得できませんでした')
            return

        # 既存のセットアップデータがある場合は上書きしない
        if os.path.exists(setup_data_path):
            cmds.warning('既にセットアップデータが存在しているため作成できません')
            return

        self.__output_setup_data(
            setup_data_path,
            self.view.ui.XOffsetSpinBox.value(),
            self.view.ui.BindLineEdit.text(),
        )
        self.__load_setup_data_to_ui(setup_data_path)
        self.update_view()

    # ===============================================
    def bake_texture(self, src, dst):
        """テクスチャのベイク

        Args:
            src: ベイク元メッシュ
            dst: ベイク先メッシュ
        """

        output_path = texture_bake_to_eye_cover.texture_bake(src, dst)

        if not os.path.exists(output_path):
            cmds.warning('ベイクに失敗しました')
        else:
            subprocess.Popen(['start', '', output_path], shell=True)

    # ===============================================
    def normal_color_setup(self):
        """法線・頂点カラーの転写実行
        """

        transform_list = []
        transform_list = cmds.ls(sl=True, l=True, typ='transform')

        if not len(transform_list) == 1:
            cmds.warning('目隠しのメッシュを選択してください')
            return

        target = transform_list[0]

        this_chara_info = self.__get_chara_info()

        if not this_chara_info:
            cmds.warning('キャラ情報を取得できません')
            return

        if target in this_chara_info.part_info.mesh_list:
            cmds.warning('キャラのメッシュが選択されています')
            return

        attr_trans = attribute_transfer.AttributeTransfer()
        attr_trans.initialize(target, this_chara_info)
        attr_trans.transfer()

    # ===============================================
    def m_face_setup(self):
        """M_Faceへの目隠し仕込み実行
        """

        # フェイシャルセットアップに必要な値を返却するための変数
        left_x_offset, bind_joint = None, None

        # 初期情報を確認
        this_chara_info = self.__get_chara_info()
        if not this_chara_info:
            cmds.warning('キャラ情報を取得できません')
            return left_x_offset, bind_joint

        selection_list = cmds.ls(sl=True, l=True)
        if not selection_list:
            cmds.warning('目隠しのメッシュと少なくとも左右どちらかのジョイントを選択してください')
            return left_x_offset, bind_joint

        # セットアップ用のリスト作成
        transform_list = []
        joint_list = []

        for item in selection_list:

            if cmds.objectType(item, isType='transform'):
                transform_list.append(item)
            elif cmds.objectType(item, isType='joint'):
                joint_list.append(item)

        for joint in joint_list:
            if joint.find('Eye_bottom') < 0:
                cmds.warning('Eye_bottom以外のジョイントが選択されています')
                return left_x_offset, bind_joint

        # セットアップ実行。ジョイントは左右どちらかで良いがどちらも選択することが考えられるので冗長性を持たせている。
        if len(transform_list) == 1 and len(joint_list) >= 1:

            cover_setup = eye_cover_setup.EyeCoverSetup()
            cover_setup.initialize(transform_list[0], joint_list[0], this_chara_info)
            left_x_offset, bind_joint = cover_setup.setup()
            return left_x_offset, bind_joint

        else:
            cmds.warning('目隠しのメッシュと少なくとも左右どちらかのジョイントを選択してください')
            return left_x_offset, bind_joint

    # ===============================================
    def facial_setup(self):
        """目隠し表情になるようにコントローラーを設定
        """

        eye_cover_facial_setup.setup(self.bind_joint, self.x_offset, self.z_offset)

    # ===============================================
    def __get_chara_info(self):
        """キャラインフォの取得
        """

        this_chara_info = chara_info.CharaInfo()
        this_chara_info.create_info()

        if not this_chara_info.exists:
            return None
        else:
            return this_chara_info

    # ===============================================
    def __get_setup_data_path(self):
        """セットアップデータのパス取得
        """

        scene_path = cmds.file(q=True, sn=True)
        if not scene_path:
            return
        scene_dir_path = os.path.dirname(scene_path)
        return os.path.join(scene_dir_path, self.data_file_name)

    # ===============================================
    def __output_setup_data(self, output_path, left_x_offset, bind_joint):
        """仕込み時のセットアップデータを出力

        セットアップデータは目隠し表情をコントローラーに設定する時に使用する
        """

        if not left_x_offset or not bind_joint:
            return

        output_str = '{0}{1}{2}{3}{4}'.format(self.x_offset_header, str(left_x_offset), self.data_separater, self.bind_header, bind_joint)

        try:
            f = open(output_path, 'w')
            f.write(output_str)
            f.close()
        except Exception:
            cmds.warning('セットアップデータの出力に失敗しました')

    # ===============================================
    def __load_setup_data_to_ui(self, load_path):
        """セットアップデータをUIにロード
        """

        # セットアップデータの読み込み
        scene_path = cmds.file(q=True, sn=True)

        if not os.path.exists(load_path):
            cmds.warning('セットアップデータファイルがありません')
            self.is_setup_data_loaded = False
            return

        data_str = ''
        try:
            f = open(load_path)
            data_str = f.read()
            f.close()
        except Exception:
            cmds.warning('セットアップデータの読み取りに失敗しました')
            self.is_setup_data_loaded = False
            return

        # UIにセット
        data_list = data_str.split(self.data_separater)

        for data in data_list:
            if data.startswith(self.x_offset_header):
                x_offset = float(data.replace(self.x_offset_header, ''))
                self.view.ui.XOffsetSpinBox.setValue(x_offset)
            elif data.startswith(self.bind_header):
                bind_joint = data.replace(self.bind_header, '').split('|')[-1]
                self.view.ui.BindLineEdit.setText(bind_joint)

        # 読み込み完了フラグをたてる
        self.is_setup_data_loaded = True
