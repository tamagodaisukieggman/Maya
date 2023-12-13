# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
except Exception:
    pass

import math

import maya.cmds as cmds
from maya import OpenMayaUI
import shiboken2
from PySide2 import QtWidgets

from . import view
from ..base_common import classes as base_class

# ツールマニュアル
# GallopSymmetricalWeightChecker：スキニングの対称性チェック
# https://wisdom.cygames.jp/pages/viewpage.action?pageId=164733995


class Main(object):

    def __init__(self):
        self.tool_name = 'GlpSymmetricalPositionChecker'
        self.tool_version = '22041901'

        self.view = view.View()
        self.view.setting = base_class.setting.Setting(self.tool_name)
        self.view.setWindowTitle(self.tool_name + self.tool_version)

        self.controller = VtxDataController(self.update_status)

        self.base_direction = None

    # ==================================================
    def delete_overlapping_window(self, target):
        """
        Windowの重複削除処理
        Args:
            target : view : 重複していないか確認する対象のview
        """
        main_window = OpenMayaUI.MQtUtil.mainWindow()
        if main_window is None:
            return
        try:
            main_window = shiboken2.wrapInstance(
                long(main_window), QtWidgets.QMainWindow)
        except Exception:
            # Maya 2022-
            main_window = shiboken2.wrapInstance(
                int(main_window), QtWidgets.QMainWindow)
        for widget in main_window.children():
            if type(target) == type(widget):
                widget.deleteLater()

    # ==================================================
    def show_ui(self):
        """
        uiを表示
        """
        self.controller.initialize(self.__create_setting_dict())

        # windowの重複削除処理
        self.delete_overlapping_window(self.view)

        self.setup_view_event()
        self.view.load_setting()
        self.view.show()

    # ==================================================
    def setup_view_event(self):
        """
        イベント接続
        """
        # 「非対称な頂点を選択」
        self.view.ui.selectAsymmetryBtn.clicked.connect(lambda: self.select_asymmetry())
        # 「選択頂点を「-」に合わせる」
        self.view.ui.toMinusBySelectionBtn.clicked.connect(lambda: self.exec_symmetry(base_direction="-"))
        # 「選択頂点を「+」に合わせる」
        self.view.ui.toPlusBySelectionBtn.clicked.connect(lambda: self.exec_symmetry(base_direction="+"))

    # ==================================================
    def combine_undo_deco(func):
        """
        ファンクション実行時にundoが一発で行えるようデコレートする
        """
        def wrapper(*args, **kwargs):
            cmds.undoInfo(openChunk=True)
            func(*args, **kwargs)
            cmds.undoInfo(closeChunk=True)

        return wrapper

    # ==================================================
    @combine_undo_deco
    def select_asymmetry(self):
        """
        作成したcontrollerを用いて、アシンメトリーであるものを選択する
        """
        self.view.save_setting()
        status = self.check_pos_symmetry()
        if not status:
            return

        assynmet_verts = self.controller.get_asymmetry()
        if len(assynmet_verts) > 0:
            cmds.select(assynmet_verts)
            self.update_status(0, '非対称な頂点を選択完了')
        else:
            cmds.select(clear=True)
            self.update_status(0, '非対称な頂点はありませんでした')

    # ==================================================
    @combine_undo_deco
    def exec_symmetry(self, base_direction):
        """
        シンメトリ化を実行する
        Args:
            base_direction : str : 移動時に基にする頂点を(+/-)で指定する
        """
        self.view.save_setting()
        self.base_direction = base_direction
        status = self.check_pos_symmetry()
        if not status:
            return

        # UIに「選択頂点を」と書かれているのでオブジェクトモードでメッシュが選択されている場合
        # 全頂点に実行されるのを防ぐためコンポーネントモードへ切り替え
        cmds.selectMode(component=True)
        selected_vtx_list = cmds.polyListComponentConversion(tv=True)
        selected_vtx_list = cmds.ls(selected_vtx_list, fl=True)
        if len(selected_vtx_list) == 0:
            self.update_status(0, '対象を選択してから実行してください')
            return

        pos_vtx_list, nega_vtx_list = self.controller.plus_minus_grouping(selected_vtx_list)

        if base_direction == '+':
            move_vtx_list = nega_vtx_list
            reference_vtx_data_dict = self.controller.positive_vertex_data_dict
            move_vtx_data_dict = self.controller.negative_vertex_data_dict
        else:
            move_vtx_list = pos_vtx_list
            reference_vtx_data_dict = self.controller.negative_vertex_data_dict
            move_vtx_data_dict = self.controller.positive_vertex_data_dict

        if not move_vtx_list:
            self.update_status(0, '選択されている頂点では実行できません')
            return

        interval = 100 / len(move_vtx_list)
        current_value = 0
        self.update_status(0, '移動を実行中')

        for move_vtx in move_vtx_list:
            self.update_status(current_value)
            move_vtx_data = move_vtx_data_dict[move_vtx]
            if move_vtx_data.closest_name in reference_vtx_data_dict:
                reference_vtx_data = reference_vtx_data_dict[move_vtx_data.closest_name]
                if reference_vtx_data.closest_name:
                    self.exec_vertex_move(reference_vtx_data, move_vtx_data)
            else:
                cmds.warning('対になる頂点が見つかりません: ' + move_vtx_data.name)
            current_value += interval

        self.update_status(0, '移動を完了')

    def check_pos_symmetry(self):
        """
        頂点データを収集し、対称性のチェックを実行する
        """

        target_mesh = self.__get_selected_mesh()
        vertexed_mesh_list = cmds.polyListComponentConversion(target_mesh, tv=True)
        vertexed_mesh_list = cmds.ls(vertexed_mesh_list, fl=True)
        if len(vertexed_mesh_list) == 0:
            self.update_status(0, 'チェック対象を選択して実行してください')
            cmds.warning('チェック対象を選択して実行してください')
            return False

        self.view.save_setting()

        # データ作成
        self.controller.initialize(self.__create_setting_dict())
        status = self.controller.create_data(vertexed_mesh_list)
        if not status:
            return False

        self.update_status(0, '頂点データ更新完了')

        return True

    # ==================================================
    def exec_vertex_move(self, base_vtx_data, tgt_vtx_data):
        """
        設定に基づいて頂点移動を実行。
        Args:
            base_vtx_data : VtxData : 元となる頂点
            tgt_vtx_data : VtxData : 移動する頂点
        """
        # お互いがペアと認めた頂点同士ではなく、誤差範囲より離れた頂点に移動する場合は念のためお知らせ。
        # 重複頂点はキャラチェッカーでチェックされる。
        # 重複していてもスカートの裏側のフェイスなどは仕様としてあり。
        if (tgt_vtx_data.closest_name != base_vtx_data.closest_name) and not tgt_vtx_data.is_paired:
            cmds.warning("頂点が重複したかもしれません（両面ポリゴンならOK）: " + tgt_vtx_data.name)
        x_pos = base_vtx_data.position[0]
        y_pos = base_vtx_data.position[1]
        z_pos = base_vtx_data.position[2]
        tgt_name = tgt_vtx_data.name

        if self.controller.target_axis == 'X':
            x_pos *= -1
        elif self.controller.target_axis == 'Y':
            y_pos *= -1
        else:
            z_pos *= -1

        cmds.move(x_pos, y_pos, z_pos, tgt_name, ws=True)

    # ==================================================
    def get_current_axis(self):
        """
        Radioボタンから、対象の軸を取得
        """
        if self.view.ui.XAxisRadio.isChecked():
            target_axis = 'X'
        elif self.view.ui.YAxisRadio.isChecked():
            target_axis = 'Y'
        else:
            target_axis = 'Z'

        return target_axis

    # ==================================================
    def __get_selected_mesh(self):
        """
        選択されているメッシュ名を取得する
        """

        select_transform = cmds.ls(selection=True, et='transform', l=True)
        if select_transform:
            return select_transform[0]

        vertexed_mesh_list = cmds.polyListComponentConversion(tv=True)
        vertexed_mesh_list = cmds.ls(vertexed_mesh_list, fl=True)
        if vertexed_mesh_list:
            return vertexed_mesh_list[0].split(".")[0]

        return None

    # ==================================================
    def __create_setting_dict(self):
        """
        コントローラの設定に用いるデータをUIから集める
        """
        tool_setting_dict = {
            'target_axis': self.get_current_axis(),
            'position_allowance': self.view.ui.posAllowranceBox.value()
        }
        return tool_setting_dict

    # ==================================================
    def update_status(self, current_percentage, rewrite_lbl_to=None):
        """
        statusのラベルとプログレスバーの更新はここから行う
        Args:
            current_percentage : float : プログレスバーに設定するパーセンテージ
            rewrite_lbl_to : str : ステータスのラベルに設定したい文字列(指定なし時は更新しない)
        """
        if rewrite_lbl_to:
            self.view.ui.statusLabel.setText(rewrite_lbl_to)
        self.view.ui.progressBar.setValue(current_percentage)


class VtxData(object):
    """
    各頂点のデータを保持しておくためのクラス
    """

    def __init__(self, name, pos):
        # この頂点の名前
        self.name = name
        # この頂点の位置
        self.position = pos
        # 反転した時「類似頂点検出の誤差範囲」以内の誤差のペアを持っているか
        self.is_paired = False
        # 反転した時とりあえず一番近い頂点との距離
        self.closest_distance_square = -1
        # 反転した時とりあえず一番近い頂点の名前
        self.closest_name = None


class VtxDataController(object):
    """
    controller内にVtxDataを格納し、各種の操作を行う際はcontrollerで行う。
    """

    def __init__(self, update_progress_ui_func):
        # UIより設定する設定群
        self.target_axis = None
        self.position_tolerance_square = 0.0

        # 対象パートごとにvtxDataを入れておくための辞書
        self.positive_vertex_data_dict = None
        self.border_vertex_data_dict = None
        self.negative_vertex_data_dict = None

        # 軸の名前からindexを引く際に利用
        self.char_to_num_mapping = {
            'X': 0, 'Y': 1, 'Z': 2
        }

        self.__is_setup_done = None

        self.update_progress_ui_func = update_progress_ui_func

    # ==================================================
    def initialize(self, setting_dict):
        """
        controller内の全てのデータの初期化とセットアップ
        """
        self.__data_init()
        self.__update_setting(setting_dict)

    # ==================================================
    def __data_init(self):
        """
        頂点情報類の初期化
        """
        self.__is_setup_done = False
        self.positive_vertex_data_dict = {}
        self.border_vertex_data_dict = {}
        self.negative_vertex_data_dict = {}

    # ==================================================
    def __update_setting(self, setting_dict):
        """
        UIから設定する設定の更新
        Args:
            setting_dict: dict : 設定に使用する辞書
        """
        self.target_axis = setting_dict['target_axis']
        self.position_tolerance_square = setting_dict['position_allowance'] ** 2

    # ==================================================
    def create_data(self, target_vertex_list):
        """
        頂点情報データを作成する
        Args:
            target_vertex_list: list : 対称の頂点リスト
        """

        self.__data_init()
        # セットアップ未了での実行を抑止する
        if self.target_axis is None:
            return False

        self.__create_data_array(target_vertex_list)
        return self.__is_setup_done

    # ==================================================
    def __create_data_array(self, target_vertex_list):
        """
        頂点位置情報を作成したのち、距離データを作成
        Args:
            target_vertex_list : list : 対称の頂点リスト
        """

        self.update_progress_ui_func(0, '頂点データ作成中')
        interval = 100 / len(target_vertex_list)
        current_value = 0

        for vertexed_mesh in target_vertex_list:
            self.update_progress_ui_func(current_value)
            current_pos = cmds.pointPosition(vertexed_mesh)
            # 真ん中（対称軸で0）にある頂点は比較対象外
            if abs(current_pos[self.char_to_num_mapping[self.target_axis]]) < self.position_tolerance_square:
                self.border_vertex_data_dict[vertexed_mesh] = VtxData(vertexed_mesh, current_pos)
            # 対称軸のプラス側の頂点をリスト
            elif current_pos[self.char_to_num_mapping[self.target_axis]] > 0:
                self.positive_vertex_data_dict[vertexed_mesh] = VtxData(vertexed_mesh, current_pos)
            # 対称軸のマイナス側の頂点をリスト
            else:
                self.negative_vertex_data_dict[vertexed_mesh] = VtxData(vertexed_mesh, current_pos)
            current_value += interval
        self.update_progress_ui_func(0)

        self.__register_distance_data()

    # ==================================================
    def __register_distance_data(self):
        """
        事前に作成された頂点位置データから、距離データを作成
        「対称座標選択」ラジオボタンで選択された軸のプラス側とマイナス側の頂点を比べ
        反転した際「類似頂点検出の誤差範囲 (UIでユーザーが決められる)」(position_tolerance_square)内にある
        マイナス側の頂点をプラス側のリストのclosest_name（一番シンメトリーに近い頂点）に登録していく。
        プラス側の頂点(VtxData)リストに一番シンメトリに近いマイナス側の頂点名をclosest_nameに登録する。
        同じようにマイナス側の頂点(VtxData)リストに一番シンメトリに近いマイナス側の頂点名をclosest_nameに登録する。
        closest_nameの位置が「類似頂点検出の誤差範囲」以内の誤差だったらペア確定という意味でis_pairedをTrueにする。
        """

        # あらかじめ、create_data_arrayされ、データが登録されていない場合はreturn
        if self.negative_vertex_data_dict == {} or self.positive_vertex_data_dict == {}:
            self.update_progress_ui_func(0, '頂点データの作成に失敗:\nオブジェクトがワールド座標で対称となるよう置かれているかご確認ください')
            return

        self.update_progress_ui_func(0, '距離データ作成中')
        interval = 100 / len(self.positive_vertex_data_dict.keys())
        current_value = 0
        # プラス側の頂点(VtxData)を起点としてシンメトリのペアとなるマイナス側の頂点を調べる
        for pos_vtx_data in self.positive_vertex_data_dict.values():
            self.update_progress_ui_func(current_value)
            # マイナス側の頂点(VtxData)
            for neg_vtx_data in self.negative_vertex_data_dict.values():
                current_distance_square = self.__get_misalignment_square(pos_vtx_data.position, neg_vtx_data.position)
                # (+側)未登録(closest_distance_squareが初期値の-1)もしくは登録済みのよりもっと近い対称を見つけたらとりあえず登録
                if pos_vtx_data.closest_distance_square == -1 or current_distance_square < pos_vtx_data.closest_distance_square:
                    pos_vtx_data.closest_name = neg_vtx_data.name
                    pos_vtx_data.closest_distance_square = current_distance_square
                # (-側)未登録(closest_distance_squareが初期値の-1)もしくは登録済みのよりもっと近い対称を見つけたらとりあえず登録
                if neg_vtx_data.closest_distance_square == -1 or current_distance_square < neg_vtx_data.closest_distance_square:
                    neg_vtx_data.closest_name = pos_vtx_data.name
                    neg_vtx_data.closest_distance_square = current_distance_square
                # 「類似頂点検出の誤差範囲」以内の誤差だったらペア確定
                if current_distance_square <= self.position_tolerance_square:
                    # 重複した位置に頂点がある場合の対応(スカートの裏側など両面ポリゴン対応)
                    if pos_vtx_data.is_paired:
                        # 法線の向きでペアを判定
                        mirror_index = self.char_to_num_mapping[self.target_axis]
                        better_pair = self.get_better_mirrored_vtx(
                            pos_vtx_data.name, pos_vtx_data.closest_name, neg_vtx_data.name, mirror_index)
                        if better_pair != pos_vtx_data.closest_name:
                            # ペアを取られたマイナス側の情報を更新
                            self.negative_vertex_data_dict[pos_vtx_data.closest_name].closest_name = self.negative_vertex_data_dict[neg_vtx_data.name].closest_name
                            self.negative_vertex_data_dict[pos_vtx_data.closest_name].closest_distance_square = self.negative_vertex_data_dict[neg_vtx_data.name].closest_distance_square
                            self.negative_vertex_data_dict[pos_vtx_data.closest_name].is_paired = self.negative_vertex_data_dict[neg_vtx_data.name].is_paired
                            # ペア更新
                            pos_vtx_data.closest_name = neg_vtx_data.name
                            pos_vtx_data.closest_distance_square = current_distance_square
                            neg_vtx_data.closest_name = pos_vtx_data.name
                            neg_vtx_data.closest_distance_square = current_distance_square
                        pos_vtx_data.is_paired = True
                        neg_vtx_data.is_paired = True
                        # 重複が2個以上ある場合には対応していないのでbreak
                        break
                    else:
                        neg_vtx_data.closest_name = pos_vtx_data.name
                        neg_vtx_data.closest_distance_square = current_distance_square
                    pos_vtx_data.is_paired = True
                    neg_vtx_data.is_paired = True
                    # ペアは見つかったが重複した頂点対応の為breakしない
            current_value += interval

        self.update_progress_ui_func(0)
        self.__is_setup_done = True

    # ==================================================
    def get_better_mirrored_vtx(self, target_vtx, candidate_vtx1, candidate_vtx2, mirror_index):
        """
        target_vtxを「ミラーした際」、法線の向きが近い候補の頂点はどちらかを調べる。頂点の位置は関係ない。
        __register_distance_dataで頂点の位置を調べる際、重複している頂点のどちらが対称の頂点で
        あるかを調べる際、向きが同じフェイスの頂点同士をペアにするために使っている。
        Args:
            target_vtx (str): vertex名。この頂点の法線と向きが近い候補を探す。
            candidate_vtx1 (str): vertex名。候補1
            candidate_vtx2 (str): vertex名。候補2
            mirror_index (int): 0:x, 1:y, 2:z どの方向のミラーか
        Returns:
            str: target_vtxと法線の向きが近い方の候補のvertex名
        """
        normal_target = self.get_average_vtx_normal(target_vtx)
        normal_target[mirror_index] = normal_target[mirror_index] * -1
        normal_candidate1 = self.get_average_vtx_normal(candidate_vtx1)
        normal_candidate2 = self.get_average_vtx_normal(candidate_vtx2)
        if normal_target and normal_candidate1 and normal_candidate2:
            diff_x1 = normal_target[0] - normal_candidate1[0]
            diff_y1 = normal_target[1] - normal_candidate1[1]
            diff_z1 = normal_target[2] - normal_candidate1[2]
            diff_x2 = normal_target[0] - normal_candidate2[0]
            diff_y2 = normal_target[1] - normal_candidate2[1]
            diff_z2 = normal_target[2] - normal_candidate2[2]
            total_diff1 = abs(diff_x1) + abs(diff_y1) + abs(diff_z1)
            total_diff2 = abs(diff_x2) + abs(diff_y2) + abs(diff_z2)
            if total_diff1 < total_diff2:
                return candidate_vtx1
            else:
                return candidate_vtx2
        else:
            return None

    # ==================================================
    def get_average_vtx_normal(self, vtx):
        """
        頂点の法線のノーマライズされた平均法線を返す
        Args:
            vtx (str): vertex名
        Returns:
            float[]: 法線[x, y, z]
        """
        if not vtx:
            return None
        x_normals = cmds.polyNormalPerVertex(vtx, q=True, normalX=True)
        y_normals = cmds.polyNormalPerVertex(vtx, q=True, normalY=True)
        z_normals = cmds.polyNormalPerVertex(vtx, q=True, normalZ=True)
        normal_x = float(sum(x_normals)/len(x_normals))
        normal_y = float(sum(y_normals)/len(y_normals))
        normal_z = float(sum(z_normals)/len(z_normals))
        length = math.sqrt(normal_x**2 + normal_y**2 + normal_z**2)
        if length == 0:
            length = 1
        return [normal_x / length, normal_y / length, normal_z / length]

    # ==================================================
    def __get_misalignment_square(self, pos1, pos2):
        """
        2点間の対称のずれを返す
        Args:
            pos1 : list : 距離を求めたい頂点一つ目の座標
            pos2 : list : 距離を求めたい頂点二つ目の座標
        """

        x_diff = abs(pos1[0] - pos2[0])
        y_diff = abs(pos1[1] - pos2[1])
        z_diff = abs(pos1[2] - pos2[2])

        # 対称である箇所を修正
        if self.target_axis == 'X':
            x_diff = abs(pos1[0] - (-1 * pos2[0]))
        elif self.target_axis == 'Y':
            y_diff = abs(pos1[1] - (-1 * pos2[1]))
        else:
            z_diff = abs(pos1[2] - (-1 * pos2[2]))

        return (x_diff + y_diff + z_diff) ** 2

    # ==================================================
    def get_asymmetry(self):
        """
        事前に作成されているデータをもとにアシンメトリである頂点群を返します。
        """
        asymmetry_list = []
        for pos_vtx in self.positive_vertex_data_dict.keys():
            if not self.positive_vertex_data_dict[pos_vtx].is_paired:
                asymmetry_list.append(pos_vtx)
        for nega_vtx in self.negative_vertex_data_dict.keys():
            if not self.negative_vertex_data_dict[nega_vtx].is_paired:
                asymmetry_list.append(nega_vtx)

        return asymmetry_list

    # ==================================================
    def plus_minus_grouping(self, target_vtx_list):
        """
        事前に作成されているデータをもとに、与えられた頂点が +, -のどちらに属しているか分類して返します
        Args:
            target_vtx_list : list : 分類対象の頂点のリスト
        """
        positive_vtx_list = []
        negative_vtx_list = []

        for target_vtx in target_vtx_list:
            if target_vtx in self.positive_vertex_data_dict.keys():
                positive_vtx_list.append(target_vtx)
            elif target_vtx in self.negative_vertex_data_dict.keys():
                negative_vtx_list.append(target_vtx)

        return positive_vtx_list, negative_vtx_list
