# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya2022-
    from importlib import reload
except Exception:
    pass

import sys

import maya.api.OpenMaya as om
import maya.cmds as cmds
import shiboken2
from maya import OpenMayaUI
from PySide2 import QtWidgets

from . import remap_influence_joint, view, weight_manager, utility, holder
reload(remap_influence_joint)
reload(view)
reload(weight_manager)
reload(utility)


def main():
    skin_weight_editor = Main()
    skin_weight_editor.show_ui()


class Main(object):
    def __init__(self):
        self.version = "23072402"
        self.view = view.View()
        self.joint_edit_view = None
        # reloadしないモジュールにweight_managerを保持しておく
        # weight_managerモジュール編集中はholderモジュールもreloadすれば毎回更新される
        if holder.weight_manager is None:
            holder.weight_manager = weight_manager.WeightManager()
        self.weight_manager = holder.weight_manager

    def deleteOverlappingWindow(self, target):
        """Windowの重複削除処理
        """
        main_window = OpenMayaUI.MQtUtil.mainWindow()
        if main_window is None:
            return

        if sys.version_info.major == 2:
            main_window = shiboken2.wrapInstance(long(main_window), QtWidgets.QMainWindow)
        else:
            # for Maya 2022 or later
            main_window = shiboken2.wrapInstance(int(main_window), QtWidgets.QMainWindow)

        for widget in main_window.children():
            if str(type(target)) == str(type(widget)):
                widget.custom_delete()

    def show_ui(self):
        """UI表示
        """
        # windowの重複削除処理
        self.deleteOverlappingWindow(self.view)
        self.ui_event_setup()
        self.view.add_linked_window(self.joint_edit_view)
        self.view.show()

    def ui_event_setup(self):
        """uiをクリックした際などに発生するイベントを設定
        """
        # Copy & Paste mode
        self.view.ui.copy_btn.clicked.connect(lambda: self.copy_weight_info())
        self.view.ui.paste_by_select_btn.clicked.connect(lambda: self.paste_weight_info(mode='order'))
        self.view.ui.paste_by_index_btn.clicked.connect(lambda: self.paste_weight_info(mode='index'))
        self.view.ui.paste_by_pos_btn.clicked.connect(lambda: self.paste_weight_info(mode='position'))
        self.view.ui.paste_by_uv_pos_btn.clicked.connect(lambda: self.paste_weight_info(mode='uv_position'))
        self.view.ui.paste_mirror_x_btn.clicked.connect(lambda: self.mirror_paste_weight_info(mode='mirror-x'))
        self.view.ui.paste_mirror_y_btn.clicked.connect(lambda: self.mirror_paste_weight_info(mode='mirror-y'))
        self.view.ui.paste_mirror_z_btn.clicked.connect(lambda: self.mirror_paste_weight_info(mode='mirror-z'))

        # Export & import mode
        self.view.ui.export_btn.clicked.connect(lambda: self.export_weight_info())
        self.view.ui.import_by_select_btn.clicked.connect(lambda: self.import_and_paste_weight_info(mode='order'))
        self.view.ui.import_by_index_btn.clicked.connect(lambda: self.import_and_paste_weight_info(mode='index'))
        self.view.ui.import_by_pos_btn.clicked.connect(lambda: self.import_and_paste_weight_info(mode='position'))
        self.view.ui.import_by_uv_pos_btn.clicked.connect(lambda: self.import_and_paste_weight_info(mode='uv_position'))
        self.view.ui.import_mirror_x_btn.clicked.connect(lambda: self.import_and_paste_weight_info(mode='mirror-x'))
        self.view.ui.import_mirror_y_btn.clicked.connect(lambda: self.import_and_paste_weight_info(mode='mirror-y'))
        self.view.ui.import_mirror_z_btn.clicked.connect(lambda: self.import_and_paste_weight_info(mode='mirror-z'))

        # utility
        self.view.ui.check_round_weight_btn.clicked.connect(lambda: self.check_round())
        self.view.ui.round_weight_btn.clicked.connect(lambda: self.round_weight())
        self.view.ui.check_max_inf_btn.clicked.connect(lambda: self.check_influence_count())
        self.view.ui.set_max_inf_btn.clicked.connect(lambda: self.set_incluence_count())
        self.view.ui.round_digits_spin.valueChanged.connect(lambda: self.value_changed_callback(self.view.ui.round_digits_spin, self.view.ui.round_digits_sl))
        self.view.ui.round_digits_sl.sliderReleased.connect(lambda: self.value_changed_callback(self.view.ui.round_digits_sl, self.view.ui.round_digits_spin))
        self.view.ui.inf_num_spin.valueChanged.connect(lambda: self.value_changed_callback(self.view.ui.inf_num_spin, self.view.ui.inf_num_sl))
        self.view.ui.inf_num_sl.sliderReleased.connect(lambda: self.value_changed_callback(self.view.ui.inf_num_sl, self.view.ui.inf_num_spin))

        # common
        self.view.ui.paste_distance_sl.sliderReleased.connect(lambda: self.value_changed_callback(self.view.ui.paste_distance_sl, self.view.ui.paste_distance_ds))
        self.view.ui.paste_distance_ds.valueChanged.connect(lambda: self.value_changed_callback(self.view.ui.paste_distance_ds, self.view.ui.paste_distance_sl))

    def value_changed_callback(self, sender, receiver):
        """スライダーとSpinboxを連動

        Args:
            sender (QtWidgets.QSpinBox|QtWidgets.QDoubleSpinBox|QtWidgets.QSlider): 呼び出し元
            receiver (QtWidgets.QSpinBox|QtWidgets.QDoubleSpinBox|QtWidgets.QSlider): 接続先
        """
        receiver.blockSignals(True)
        receiver.setValue(sender.value())
        receiver.blockSignals(False)

    def copy_weight_info(self):
        """weight情報をコピー
        """
        if self.view.ui.copy_obj_space_rb.isChecked():
            self.weight_manager.om_pos_mode = om.MSpace.kObject
        else:
            self.weight_manager.om_pos_mode = om.MSpace.kWorld

        status = self.weight_manager.create_info()
        if not status:
            return

        om.MGlobal.displayInfo('ウェイトのコピーが完了しました')
        cmds.headsUpMessage('ウェイトのコピーが完了しました', time=5.0)

    def paste_weight_info(self, mode):
        """スキンウェイトをペースト

        Args:
            mode (str): どのモードを使って貼り付けを実施するか
        """
        self.weight_manager.paste_distance = self.view.ui.paste_distance_ds.value()
        status = self.weight_manager.create_info(for_distanation=True)
        if not status:
            return

        # ペースト実行する際の関数設定
        paste_process = None
        if mode == 'order':
            paste_process = self.weight_manager.paste_weight_by_order
        elif mode == 'index':
            paste_process = self.weight_manager.paste_weight_by_index
        elif mode == 'position':
            paste_process = self.weight_manager.paste_weight_by_position
        elif mode == 'uv_position':
            paste_process = self.weight_manager.paste_weight_by_uv_position

        # もし、EditJointmodeが有効だったら、そちらに処理を移す
        if self.view.ui.edit_joint_map_cb.isChecked():
            self.joint_edit_view = remap_influence_joint.RemapInfluenceJoint(self.view)
            status = self.joint_edit_view.set_data(self.weight_manager, lambda: self.view.set_enable_components(True), paste_process)
            if not status:
                om.MGlobal.displayWarning('情報が不足しています。実行できません')
                return

            # EditJoint Window表示中はメインウィンドはボタンなどを押されたくないため無効化
            self.view.set_enable_components(False)

            # modalで出すとMaya上での選択などができないためwindowとして表示
            self.joint_edit_view.show_ui()
            return

        # validateで失敗しているとpaste_processが発行されない
        if paste_process:
            paste_process()

    def mirror_paste_weight_info(self, mode):
        """ミラーモードでペーストを実施

        Args:
            mode (str): 書き出しモードを指定
        """
        self.weight_manager.paste_distance = self.view.ui.paste_distance_ds.value()
        status = self.weight_manager.create_info(for_distanation=True)
        if not status:
            return

        if mode == 'mirror-x':
            self.weight_manager.mirror_paste_weight(True, False, False)
        elif mode == 'mirror-y':
            self.weight_manager.mirror_paste_weight(False, True, False)
        elif mode == 'mirror-z':
            self.weight_manager.mirror_paste_weight(False, False, True)

    def export_weight_info(self):
        """XML形式でweight情報を書き出す
        """
        if self.view.ui.export_obj_space_rb.isChecked():
            self.weight_manager.om_pos_mode = om.MSpace.kObject
        else:
            self.weight_manager.om_pos_mode = om.MSpace.kWorld

        status = self.weight_manager.create_info()
        if not status:
            return

        if not self.weight_manager.src_vtxdatas or not self.weight_manager.src_skinweight_dict:
            om.MGlobal.displayWarning('書き出し対象のスキンウェイトのデータが見つかりません')
            return

        basicFilter = '*.json'
        target_path = cmds.fileDialog2(fileFilter=basicFilter, dialogStyle=2)
        if not target_path:
            return

        self.weight_manager.export_as_json(target_path[0])

        self.weight_manager.src_data_initialize()

        om.MGlobal.displayInfo('ウェイトのエクスポート処理を完了しました')
        cmds.headsUpMessage('ウェイトのエクスポート処理を完了しました', time=5.0)

    def import_and_paste_weight_info(self, mode):
        """weightをXMLから読み込む

        Args:
            mode (str): 読み込んだ後にどの方式でペーストするか指定
        """
        # vtx情報収集できないときは読み込み中止
        vtx_list = utility.get_selected_vertex_list()
        if not vtx_list:
            om.MGlobal.displayWarning('対象の頂点を取得できません')
            return

        status = self.load_weight_info()
        if not status:
            om.MGlobal.displayError('有効なファイルを選択してください')
            return

        # ファイル自体は有効でも正しい値が書き込まれなかった時のための処理
        if not self.weight_manager.src_vtxdatas or not self.weight_manager.src_skinweight_dict:
            om.MGlobal.displayError('ウェイトの取り込みに失敗しました。処理を中止します')
            return

        if mode == 'uv_position' and not self.weight_manager.src_vtxdatas[0].face_vtx_datas:
            om.MGlobal.displayError('旧バージョンのデータではUVモードは利用できません')
            return

        if not mode.startswith('mirror-'):
            self.paste_weight_info(mode)
        else:
            self.mirror_paste_weight_info(mode)

        # import実施時にはsrc側も実行後に残っているべきではないのでリセットを実施
        self.weight_manager.custom_post_process = self.weight_manager.src_data_initialize

    def load_weight_info(self):
        """XMLをロードする

        Returns:
            bool: 読み込みを行えたか
        """
        basicFilter = '*.json'
        target_path = cmds.fileDialog2(fileFilter=basicFilter, dialogStyle=2, fileMode=1)
        if not target_path:
            return False

        self.weight_manager.import_from_json(target_path[0])
        return True

    def check_round(self):
        """小数点以下の桁数が指定数いないかチェックする
        """
        fraction_digits = self.view.ui.round_digits_spin.value()
        self.weight_manager.check_round_weight(fraction_digits)

    def round_weight(self):
        """小数点以下の桁数が指定数以下になるように調整を実施する
        """
        fraction_digits = self.view.ui.round_digits_spin.value()
        self.weight_manager.round_weight(fraction_digits)

    def check_influence_count(self):
        """ウェイトが入っているインフルエンス数が指定数以下かチェックする
        """
        influence_count = self.view.ui.inf_num_spin.value()
        self.weight_manager.check_max_influence(influence_count)

    def set_incluence_count(self):
        """ウェイトが入っているインフルエンス数が指定数以下になるように調整を実施する
        """
        influence_count = self.view.ui.inf_num_spin.value()
        self.weight_manager.set_max_influence(influence_count)
