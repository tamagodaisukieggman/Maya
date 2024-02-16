# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
    from builtins import object
    from builtins import range
    from importlib import reload
except Exception:
    pass

import sys
import os

import maya.cmds as cmds
import shiboken2

from PySide2 import QtWidgets
from maya import OpenMayaUI

from . import view
from . import snap_importer
from . import unity_snap_data
from . import obj_mapping_data
from . import const

reload(view)
reload(snap_importer)
reload(unity_snap_data)
reload(obj_mapping_data)
reload(const)


class Main(object):

    def __init__(self):
        """コンストラクタ
        """

        self.view = view.View(self)
        self.tool_name = 'GlpUnitySnapImporter'
        self.tool_version = '23091301'

        # 利用可能なUnityの記録データのバージョン範囲
        self.valid_snap_version_range = [230927, 230927]

        self.view.setWindowTitle(self.tool_name + self.tool_version)
        self.view.setObjectName(self.tool_name + self.tool_version)
        self.script_jobs = []

        # mapping時に指定できるオプション
        self.obj_option_dicts = [
            {'Flag': const.FLAG_ROOT_TRANS, 'Value': True, 'Visible': True},
            {'Flag': const.FLAG_ROOT_ROT, 'Value': True, 'Visible': True},
            {'Flag': const.FLAG_ROOT_SCALE, 'Value': False, 'Visible': True}
        ]
        self.mat_option_dicts = [
            {'Flag': const.FLAG_USE_ORG_LIGHT, 'Value': True, 'Visible': True},
        ]
        self.light_option_dicts = [
            {'Flag': const.FLAG_USE_CHAR_LIGHT, 'Value': True, 'Visible': True},
            {'Flag': const.FLAG_ROOT_TRANS, 'Value': True, 'Visible': False},
            {'Flag': const.FLAG_ROOT_ROT, 'Value': True, 'Visible': False},
        ]

        self.current_json_file_name = ''
        self.block_connect_ui_update = False
        self.snap_importer = snap_importer.SnapImporter()

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
                # 破棄する前にクローズイベントを実行する
                widget.closeEvent(None)
                widget.deleteLater()

    def show_ui(self):
        """UI描画
        """

        # windowの重複削除処理
        self.deleteOverlappingWindow(self.view)

        self.initialize_ui()
        self.setup_view_event()
        self.load_json_dir_path()
        self.view.show()

    def initialize_ui(self):
        """UIの初期設定
        """

        ui = self.view.ui
        ui.axis_obj_connection_list.setVisible(False)

        if self.snap_importer.root_orient_key == const.ROOT_ORIENT_AXIS_OBJ:
            ui.orient_axis_obj_radio.setChecked(True)
            ui.axis_obj_connection_list.setVisible(True)
        elif self.snap_importer.root_orient_key == const.ROOT_ORIENT_LOCAL:
            ui.orient_local_radio.setChecked(True)
        else:
            ui.orient_world_radio.setChecked(True)

        self.__set_connect_button_text()

    def setup_view_event(self):
        """UIのevent設定
        """

        ui = self.view.ui

        ui.snap_dir_path_line.textEdited.connect(self.update_snap_data_event)
        ui.snap_dir_set_button.clicked.connect(self.snap_dir_set_button_event)
        ui.snap_dir_update_button.clicked.connect(self.update_snap_data_event)
        ui.snap_file_list.itemSelectionChanged.connect(self.snap_data_select_event)
        ui.auto_set_root_button.clicked.connect(self.auto_set_root_button_event)
        ui.orient_axis_obj_radio.clicked.connect(self.root_orient_radio_event)
        ui.orient_world_radio.clicked.connect(self.root_orient_radio_event)
        ui.orient_local_radio.clicked.connect(self.root_orient_radio_event)
        ui.connect_button.clicked.connect(self.connect_button_event)
        ui.frame_slider.valueChanged.connect(self.frame_slider_event)

        self.script_jobs.append(cmds.scriptJob(e=['SceneOpened', self.on_scene_open_event]))

    def on_close_event(self):
        """ツールクローズ時に呼ばれる処理
        """

        # 読み込みを止める
        if self.snap_importer.is_initialized:
            self.snap_importer.set_connection_state(False)

        # スクリプトジョブの削除
        for job_num in self.script_jobs:
            if cmds.scriptJob(ex=job_num):
                cmds.scriptJob(kill=job_num, force=True)

    def on_scene_open_event(self):
        """シーンが開かれた時に呼ばれる処理
        """

        if self.snap_importer.is_initialized:

            # 復元用データを破棄して、読み込みを停止
            org_connect_state = self.snap_importer.is_connecting
            self.snap_importer.scene_org_snap_data = None
            self.snap_importer.set_connection_state(False)

            # 再マッピング
            self.update_mapping_event()

            # 前のシーンで読み込み中なら読み込みを再開
            if org_connect_state:
                self.snap_importer.set_connection_state(True)

            self.__set_connect_button_text()

    def update_snap_data_event(self):
        """snap_data情報更新イベント
        """

        self.save_json_dir_path()

        ui = self.view.ui
        ui.snap_file_list.clear()
        snap_dir = ui.snap_dir_path_line.text()

        if not os.path.exists(snap_dir):
            return

        files = os.listdir(snap_dir)
        snap_file_names = [file for file in files if file.endswith('json')]
        ui.snap_file_list.addItems(snap_file_names)

    def snap_dir_set_button_event(self):
        """登録ボタンイベント
        """

        dirs = cmds.fileDialog2(cap='Select Unity ObjSnap Folder', fm=3)

        if dirs:
            ui = self.view.ui
            ui.snap_dir_path_line.setText(dirs[0])
            self.update_snap_data_event()

    def snap_data_select_event(self):
        """スナップデータ選択時の処理
        """

        if self.block_connect_ui_update:
            return

        ui = self.view.ui

        current_item = ui.snap_file_list.currentItem()
        if not current_item:
            return

        # 選択jsonで新規インポーターを初期化
        json_path = os.path.join(ui.snap_dir_path_line.text(), current_item.text())
        new_snap_importer = snap_importer.SnapImporter()
        new_snap_importer.initialize(json_path, self.valid_snap_version_range)

        # 新規インポーターが読み取れなかった場合はjsonの選択を戻す
        if not new_snap_importer.is_initialized:

            # 戻す際に更新処理が走らないようにブロック
            self.block_connect_ui_update = True

            cmds.confirmDialog(m=u'正しく読み込むことができませんでした\n読み込みを中止します')
            if self.current_json_file_name:
                for i in range(ui.snap_file_list.count()):
                    item = ui.snap_file_list.item(i)
                    if item.text() == self.current_json_file_name:
                        item.setSelected(True)

            # 更新ブロック解除
            self.block_connect_ui_update = False
            return

        # 新規インポーターを適用する前に、再現を止めてオリジナルのポーズに戻しておく
        org_connect_state = False
        if self.snap_importer.is_connecting:
            org_connect_state = True
            self.snap_importer.set_connection_state(False)
            self.__set_connect_button_text()

        # 新規インポーターを適用
        self.snap_importer = new_snap_importer
        self.current_json_file_name = current_item.text()

        # 現在のコネクション情報を保存
        prev_root_mapping_infos = self.__get_mapping_dicts(ui.root_connection_list)
        prev_axis_mapping_infos = self.__get_mapping_dicts(ui.axis_obj_connection_list)

        # UIの初期化
        ui.root_connection_list.clear()
        ui.axis_obj_connection_list.clear()

        # ルートの紐づけ用のUIを生成
        for grp_info_dict in self.snap_importer.unity_snap_data.get_grp_info_dicts():

            root_name = grp_info_dict['RootName']
            grp_type = grp_info_dict['Type']
            grp_id = grp_info_dict['GrpId']

            item = QtWidgets.QListWidgetItem()
            ui.root_connection_list.addItem(item)

            option_dicts = []
            if grp_type == const.TYPE_CHARA_MATERIAL:
                option_dicts = self.mat_option_dicts
            elif grp_type == const.TYPE_LIGHT:
                option_dicts = self.light_option_dicts
            else:
                option_dicts = self.obj_option_dicts

            # 前回の記録があれば復元
            prev_mapping_dict = {}
            for prev_mapping_info in prev_root_mapping_infos:
                if prev_mapping_info['UnityRoot'] == root_name and prev_mapping_info['ObjType'] == grp_type:
                    prev_mapping_dict = prev_mapping_info

            prev_maya_root = ''
            prev_opts = []
            if prev_mapping_dict:
                prev_maya_root = prev_mapping_dict['MayaRoot']
                prev_opts = prev_mapping_dict['Opts']

            for opt_flag in prev_opts:
                for option_dict in option_dicts:
                    if option_dict['Flag'] == opt_flag:
                        option_dict['Value'] = True

            widget = view.ConnectionItem(grp_id, grp_type, root_name, option_dicts)
            if prev_maya_root and self.__check_valid_root_input(prev_maya_root, grp_type, ui.root_connection_list):
                widget.ui.maya_name_line.setText(prev_maya_root)
            widget.setButtonPushed.connect(lambda x=widget: self.__set_maya_root_button_event(x, ui.root_connection_list))
            widget.connectionUpdated.connect(self.update_mapping_event)
            item.setSizeHint(widget.sizeHint())
            ui.root_connection_list.setItemWidget(item, widget)

        # 参照用のUI生成
        axis_obj = self.snap_importer.unity_snap_data.get_axis_obj_name()
        if axis_obj != '':
            item = QtWidgets.QListWidgetItem()
            ui.axis_obj_connection_list.addItem(item)
            widget = view.ConnectionItem(-1, const.TYPE_OBJ, axis_obj, [])

            # 前回の記録があれば復元
            prev_maya_root = prev_axis_mapping_infos[0]['MayaRoot'] if prev_axis_mapping_infos else ''

            if prev_maya_root and self.__check_valid_root_input(prev_maya_root, const.TYPE_OBJ, ui.axis_obj_connection_list):
                widget.ui.maya_name_line.setText(prev_maya_root)
            widget.ui.maya_name_line.setText(prev_maya_root)
            widget.setButtonPushed.connect(lambda x=widget: self.__set_maya_root_button_event(x, ui.axis_obj_connection_list))
            widget.connectionUpdated.connect(self.update_mapping_event)
            item.setSizeHint(widget.sizeHint())
            ui.axis_obj_connection_list.setItemWidget(item, widget)
            spacing = widget.ui.horizontalLayout.spacing()
            ui.axis_obj_connection_list.setMaximumHeight(widget.sizeHint().height() + spacing)

        # スライダーの作成
        slider = ui.frame_slider
        frame_count = self.snap_importer.unity_snap_data.get_frame_count()
        slider.setMinimum(1)
        slider.setMaximum(frame_count)
        ui.frame_count_label.setText(str(frame_count))

        if frame_count == 1:
            slider.setEnabled(False)
        else:
            slider.setEnabled(True)

        # マッピングとルート再現座標の初期化
        self.update_mapping_event()
        self.root_orient_radio_event()

        # 元々読み込み中なら再読み込み
        if org_connect_state:
            self.snap_importer.set_connection_state(True)
            self.__set_connect_button_text()

    def __set_maya_root_button_event(self, event_widget, root_qlist):
        """ルートをセットボタンが呼ばれた時の処理

        Args:
            event_widget (QWidget): セットボタンを押したウィジェット
            root_qlist (QWidget): ウィジェットをリストしているリストウィジェット
        """

        sels = cmds.ls(sl=True)
        if not sels:
            return

        maya_root = sels[0]
        root_type = event_widget.ui.type_label.text()

        if not self.__check_valid_root_input(maya_root, root_type, root_qlist):
            cmds.warning(u'既に同じタイプで指定されているルートを指定することはできません')
            return

        event_widget.set_maya_root(maya_root)

    def __check_valid_root_input(self, input_root, root_type, root_qlist):
        """指定ルートが有効かチェックする

        Args:
            input_root (str): 指定ルート
            root_type (str): 指定ルートタイプ
            root_qlist (qListWidget): ルートリスト

        Returns:
            bool: is_valid
        """

        # 同じアトリビュートを操作するタイプにダブってルートを設定されないように判定を入れる
        conflict_types = []
        trans_affected_types = [const.TYPE_OBJ, const.TYPE_LIGHT, const.TYPE_CAMERA]
        mat_param_types = [const.TYPE_CHARA_MATERIAL]

        if root_type in trans_affected_types:
            conflict_types = trans_affected_types
        elif root_type in mat_param_types:
            conflict_types = mat_param_types

        for i in range(root_qlist.count()):
            item = root_qlist.item(i)
            this_widget = root_qlist.itemWidget(item)

            if not this_widget:
                continue

            this_root = this_widget.ui.maya_name_line.text()
            this_type = this_widget.ui.type_label.text()

            if this_type in conflict_types and this_root == input_root:
                return False

        return True

    def auto_set_root_button_event(self):
        """命名一致で自動ルート割り当てを行う
        """

        ui = self.view.ui
        for i in range(ui.root_connection_list.count()):

            # Unityのルート名を取得
            item = ui.root_connection_list.item(i)
            widget = ui.root_connection_list.itemWidget(item)
            obj_type = widget.ui.type_label.text()
            unity_obj = widget.ui.unity_name_label.text()

            # シーン上から命名で検索してチェック
            hit_objs = cmds.ls(unity_obj, type='transform')
            if not hit_objs or not self.__check_valid_root_input(hit_objs[0], obj_type, ui.root_connection_list):
                print(u'AUTO ROOT SET SKIP: {}'.format(unity_obj))
                continue

            widget.set_maya_root(hit_objs[0])

    def root_orient_radio_event(self):
        """ルート再現座標選択時の処理
        """

        ui = self.view.ui

        ui.axis_obj_connection_list.setVisible(False)

        if ui.orient_axis_obj_radio.isChecked():
            self.snap_importer.set_root_orient(const.ROOT_ORIENT_AXIS_OBJ)
            ui.axis_obj_connection_list.setVisible(True)
        elif ui.orient_local_radio.isChecked():
            self.snap_importer.set_root_orient(const.ROOT_ORIENT_LOCAL)
        else:
            self.snap_importer.set_root_orient(const.ROOT_ORIENT_WORLD)

    def connect_button_event(self):
        """読み込み開始/終了ボタンの処理
        """

        if not self.snap_importer.is_initialized:
            return

        set_state = True if not self.snap_importer.is_connecting else False
        self.update_mapping_event()
        self.snap_importer.set_connection_state(set_state)

        self.__set_connect_button_text()

    def __set_connect_button_text(self):
        """ボタン表示のセット処理
        """

        ui = self.view.ui
        if self.snap_importer.is_connecting:
            ui.connect_button.setText('再現終了')
            ui.connect_button.setStyleSheet('background-color:rgb(96,32,32)')
        else:
            ui.connect_button.setText('再現開始')
            ui.connect_button.setStyleSheet('background-color:rgb(32,96,32)')

    def frame_slider_event(self):
        """フレーム移動時の処理
        """

        self.snap_importer.set_frame_index(self.view.ui.frame_slider.value() - 1)
        self.view.ui.current_frame_label.setText(str(self.view.ui.frame_slider.value()))

    def update_mapping_event(self):
        """マッピング情報の更新処理
        """

        ui = self.view.ui

        self.__set_root_validation_to_item(ui.root_connection_list)
        self.__set_root_validation_to_item(ui.axis_obj_connection_list)

        root_mapptng_infos = self.__get_mapping_dicts(ui.root_connection_list)
        axis_mapping_infos = self.__get_mapping_dicts(ui.axis_obj_connection_list)
        axis_mapping_obj = axis_mapping_infos[0]['MayaRoot'] if axis_mapping_infos else None

        self.snap_importer.update_mapping(root_mapptng_infos, axis_mapping_obj)

    def __set_root_validation_to_item(self, connection_list_widget):
        """リストのアイテムにルートの有効/無効フラグをセット

        Args:
            connection_list_widget (QListWidget): マッピング情報を取得するリストウィジェット
        """

        for i in range(connection_list_widget.count()):
            item = connection_list_widget.item(i)
            widget = connection_list_widget.itemWidget(item)
            maya_root = widget.ui.maya_name_line.text()

            # 未入力はOK
            if not maya_root:
                widget.set_input_ok(True)
                continue

            maya_roots = cmds.ls(maya_root)
            if not maya_roots or len(maya_roots) > 1:
                widget.set_input_ok(False)
            else:
                widget.set_input_ok(True)

    def __get_mapping_dicts(self, connection_list_widget):
        """リスト内のマッピング情報を取得

        Args:
            connection_list_widget (QListWidget): マッピング情報を取得するリストウィジェット

        Returns:
            list: マッピング情報を持ったdictのリスト
        """

        mapping_dicts = []

        for i in range(connection_list_widget.count()):
            item = connection_list_widget.item(i)
            widget = connection_list_widget.itemWidget(item)
            obj_type = widget.ui.type_label.text()
            unity_obj = widget.ui.unity_name_label.text()
            maya_root = widget.ui.maya_name_line.text()
            opts = widget.get_use_opts()
            grp_id = widget.grp_id

            # 不正な入力はとらない
            if not widget.is_input_ok:
                maya_root = ''

            mapping_dicts.append(
                {
                    'ObjType': obj_type,
                    'UnityRoot': unity_obj,
                    'MayaRoot': maya_root,
                    'Opts': opts,
                    'GrpId': grp_id
                }
            )

        return mapping_dicts

    def save_json_dir_path(self):
        """jsonフォルダのパスを保存
        """

        ui = self.view.ui
        cmds.optionVar(sv=(const.OP_VAR_JSON_DIR, ui.snap_dir_path_line.text()))

    def load_json_dir_path(self):
        """jsonフォルダのパスをロード
        """

        if cmds.optionVar(exists=const.OP_VAR_JSON_DIR):
            self.view.ui.snap_dir_path_line.setText(cmds.optionVar(q=const.OP_VAR_JSON_DIR))
            self.update_snap_data_event()
