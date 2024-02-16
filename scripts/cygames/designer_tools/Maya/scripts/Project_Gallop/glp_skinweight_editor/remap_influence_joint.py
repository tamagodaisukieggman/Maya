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
import collections

import maya.api.OpenMaya as om
import maya.cmds as cmds
import shiboken2
from maya import OpenMayaUI
from PySide2 import QtWidgets

from . import remap_influence_joint_view, utility
reload(remap_influence_joint_view)
reload(utility)


class RemapInfluenceJoint(object):
    """Influenceのジョイントの紐づけを変更する
    """

    def __init__(self, linked_window):
        self.view = remap_influence_joint_view.RemapInfluenceJointView()
        self._weight_manager = []
        self.src_joint_names = []
        self.dest_joint_names = []
        self._org_dest_joint_names = []

        self.linked_window = linked_window
        self.linked_window.add_linked_window(self.view)

        self.paste_function = None
        self.is_ready = False

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
                widget.deleteLater()

    def show_ui(self):
        """UI表示
        """
        if not self.is_ready:
            om.MGlobal.displayError("RemapInfuenceJoint Windowの初期設定が正常に完了していません")
            return

        self.deleteOverlappingWindow(self.view)
        self.ui_event_setup()
        self.set_joint_list_widget_items()

        src_overlaps, dst_overlaps = self.get_overlap_influence_name()
        if src_overlaps or dst_overlaps:
            self.show_inf_overlap_confirm_dialog(src_overlaps, dst_overlaps)

        self.view.show()

    def get_overlap_influence_name(self):
        """ショートネームが重複しているインフルエンスを取得

        Returns:
            list, list: コピー元の重複しているインフルエンス名、コピー先の重複しているインフルエンス名
        """

        counter = collections.Counter(self.src_joint_names)
        src_overlap_infs = []
        for key, val in counter.items():
            if val > 1:
                src_overlap_infs.append(key)

        counter = collections.Counter(self._org_dest_joint_names)
        dst_overlap_infs = []
        for key, val in counter.items():
            if val > 1:
                dst_overlap_infs.append(key)

        return src_overlap_infs, dst_overlap_infs

    def show_inf_overlap_confirm_dialog(self, src_overlap_infs, dst_overlap_infs):
        """インフルエンス名の重複を警告するダイアログを表示

        Args:
            src_overlap_infs (list): コピー元の重複しているインフルエンス名
            dst_overlap_infs (list): コピー先の重複しているインフルエンス名
        """

        msg = ''

        if src_overlap_infs:
            msg += 'コピー元で以下のインフルエンス名が重複しています' + '\n'
            for src_overlap_inf in src_overlap_infs:
                msg += ' -' + src_overlap_inf + '\n'

        if dst_overlap_infs:
            msg += 'コピー先で以下のインフルエンス名が重複しています' + '\n'
            for dst_overlap_inf in dst_overlap_infs:
                msg += ' -' + dst_overlap_inf + '\n'

        if msg:
            msg += '\nインフルエンス名の重複により正しくJointMapが行えない可能性があります'
            cmds.confirmDialog(t='インフルエンス名重複警告', m=msg, icn='warning')

    def set_data(self, weight_manager, end_process, paste_function):
        """ウィンドウを利用するための情報を格納

        Args:
            weight_manager (weightManager.WeightManager): ウェイトを管理するマネージャー
            end_process (function): ウィンドウがCloseされた際に実行される関数
            paste_function (function): ウェイトのペーストを実施するための関数

        Returns:
            bool: 登録がすべて完了できたか
        """
        self.is_ready = False
        self._weight_manager = weight_manager

        if not self._weight_manager.dest_skinweight_dict or not self._weight_manager.src_skinweight_dict:
            return False

        self.src_joint_names = self.get_joint_name_list(self._weight_manager.src_skinweight_dict)
        self.dest_joint_names = self.get_joint_name_list(self._weight_manager.dest_skinweight_dict)
        self._org_dest_joint_names = self.dest_joint_names

        self.view.end_process = end_process
        self.paste_function = paste_function
        self.is_ready = True

        return True

    def ui_event_setup(self):
        """UIイベントの登録
        """
        self.view.ui.set_joint_name_btn.clicked.connect(self.set_entered_name_to_selected_items_dest)
        self.view.ui.select_item_from_maya_btn.clicked.connect(self.select_list_item_from_maya_selection)
        self.view.ui.swap_item_from_maya_btn.clicked.connect(self.swap_dest_joint_on_maya_selection)
        self.view.ui.swap_joint_name_btn.clicked.connect(self.swap_selected_items_dest)
        self.view.ui.set_selected_obj_btn.clicked.connect(self.set_selected_joint_to_selected_items)
        self.view.ui.reset_btn.clicked.connect(self.reset_joints_list_widget)
        self.view.ui.continue_btn.clicked.connect(self.do_pase_and_close_window)
        self.view.ui.joint_list_widget.itemSelectionChanged.connect(self.set_selected_item_to_le)

    def set_joint_list_widget_items(self):
        """jointリストウィジェットを更新
        """
        self.view.ui.joint_list_widget.clear()
        if not self._weight_manager:
            om.MGlobal.displayWarning('EditJointにWeight Managerがセットされていません')
            return

        for src_joint_name in self.src_joint_names:
            short_name = utility.get_namespace_removed_shortname(src_joint_name)
            dest = ''

            # もし、マッチするものがあったら名前を入れる
            if self.get_index_shortname_matched_joint(short_name, self.dest_joint_names) != -1:
                dest = short_name

            self.view.ui.joint_list_widget.addItem('{0} -> {1}'.format(short_name, utility.get_namespace_removed_shortname(dest)))

    def select_list_item_from_maya_selection(self):
        """Maya上で選択しているジョイントに対応するitemをリストウィジェット上で選択する
        """
        selected_joints = cmds.ls(sl=True, type='joint')
        if len(selected_joints) != 1:
            om.MGlobal.displayWarning('ジョイントを1つ選択したうえで実行してください')
            return

        for item in self.view.ui.joint_list_widget.selectedItems():
            item.setSelected(False)

        has_matched_item = False
        for i in range(self.view.ui.joint_list_widget.count()):
            current_item = self.view.ui.joint_list_widget.item(i)
            src_joint = current_item.text().split(' -> ')[0]
            if utility.get_namespace_removed_shortname(src_joint) == utility.get_namespace_removed_shortname(selected_joints[0]):
                current_item.setSelected(True)
                has_matched_item = True
                self.view.ui.joint_list_widget.scrollToItem(current_item, QtWidgets.QAbstractItemView.PositionAtTop)
                break

        if not has_matched_item:
            om.MGlobal.displayInfo('選択されたいるジョイントは、インフルエンスに含まれていません')

    def swap_dest_joint_on_maya_selection(self):
        """Mayaで選択しているジョイント同士でペースト先ジョイントを入れ替える
        """
        selected_joints = cmds.ls(sl=True, type='joint')
        if len(selected_joints) != 2:
            om.MGlobal.displayWarning('ジョイントを2つ選択したうえで実行してください')
            return

        selected_list_items = [None] * 2
        for idx, joint in enumerate(selected_joints):
            for i in range(self.view.ui.joint_list_widget.count()):
                current_item = self.view.ui.joint_list_widget.item(i)
                src_joint = current_item.text().split(' -> ')[0]
                if utility.get_namespace_removed_shortname(src_joint) == utility.get_namespace_removed_shortname(joint):
                    selected_list_items[idx] = current_item
                    break

        if not all(selected_list_items):
            om.MGlobal.displayWarning('選択された2つのジョイントに対応するアイテムが見つかりません')
            return

        self.swap_two_dest_item(selected_list_items)

    def reset_joints_list_widget(self):
        """jointのリストウィジェットを初期状態にする
        """
        self.dest_joint_names = self._org_dest_joint_names
        self.set_joint_list_widget_items()

    def set_selected_item_to_le(self):
        """リスト上で選択されているアイテムが一つだけの場合、joint nameのline editに反映させる
        """
        selected_item = self.view.ui.joint_list_widget.selectedItems()
        if len(selected_item) != 1:
            return

        item = selected_item[0].text().split(' -> ')[1]
        self.view.ui.joint_name_le.setText(item)

    def set_entered_name_to_selected_items_dest(self):
        """line editに入力された値をもとにジョイント名のセット
        """
        input_name = self.view.ui.joint_name_le.text()
        match_index = self.get_index_shortname_matched_joint(input_name, self.dest_joint_names)

        if match_index == -1:
            om.MGlobal.displayWarning('指定されたオブジェクトはスキンクラスター上に存在しません')
            return

        selected_item = self.view.ui.joint_list_widget.selectedItems()
        if len(selected_item) == 0:
            om.MGlobal.displayWarning('リストからアイテムを選択してから実行してください')
            return

        for i in range(len(selected_item)):
            former_text = selected_item[i].text()
            selected_item[i].setText('{0} -> {1}'.format(former_text.split(' -> ')[0], input_name))

    def swap_selected_items_dest(self):
        """リスト内の選択している2つのアイテムのペースト先ジョイントを入れ替える
        """
        selected_items = self.view.ui.joint_list_widget.selectedItems()
        if len(selected_items) != 2:
            om.MGlobal.displayWarning('オブジェクトを2つ選択して実行してください')
            return

        self.swap_two_dest_item(selected_items)

    def swap_two_dest_item(self, swap_items):
        """2つのリストのペースト先を入れ替える

        Args:
            swap_items (list(QListWidgetItem)): 入れ替えるアイテム
        """
        item1 = swap_items[0].text().split(' -> ')[1]
        item2 = swap_items[1].text().split(' -> ')[1]
        swap_items[0].setText('{0} -> {1}'.format(swap_items[0].text().split(' -> ')[0], item2))
        swap_items[1].setText('{0} -> {1}'.format(swap_items[1].text().split(' -> ')[0], item1))

    def set_selected_joint_to_selected_items(self):
        """Mayaのウィンドウ上で選択しているジョイントを選択しているアイテムのペースト先に登録
        """
        selected_obj = cmds.ls(selection=True, type='joint')
        if len(selected_obj) != 1:
            om.MGlobal.displayWarning('ジョイントを1つ選んだ上で実行してください')
            return

        selected_item = self.view.ui.joint_list_widget.selectedItems()
        if len(selected_item) == 0:
            om.MGlobal.displayWarning('リストからアイテムを選択してから実行してください')
            return

        search_target_short_name = utility.get_namespace_removed_shortname(selected_obj[0])
        match_index = self.get_index_shortname_matched_joint(search_target_short_name, self.dest_joint_names)
        if match_index == -1:
            om.MGlobal.displayWarning('インフルエンス内に当該ジョイントがありません')
            return

        for i in range(len(selected_item)):
            former_text = selected_item[i].text()
            selected_item[i].setText('{0} -> {1}'.format(former_text.split(' -> ')[0], search_target_short_name))

    def do_pase_and_close_window(self):
        """ペーストを実行しウィンドウを閉じる
        """
        remaped_list = self.create_joint_index_list()
        # リマップ後のインフルエンスに存在しないものを含む場合にはウェイトの合計が1にならなくなってしまう恐れがあるため警告する
        if -1 in remaped_list:
            status = QtWidgets.QMessageBox.question(self.view, '確認', 'ペースト先のジョイントに存在しないジョイントが含まれていますが強制的にペーストを続行しますか？', QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Cancel)
            if status != QtWidgets.QMessageBox.Ok:
                return
        self._weight_manager.remap_active = True
        self._weight_manager.remaped_joint = remaped_list
        self.paste_function()
        self._weight_manager.remap_active = False
        self._weight_manager.remaped_joint = []
        self.linked_window.remove_linked_window(self)
        self.view.close()

    def create_joint_index_list(self):
        """jointのIndexのリストを作成

        Returns:
            list(int): Listに設定されている値からjointのindexリストを作成する
        """
        indexes = []

        for i in range(self.view.ui.joint_list_widget.count()):
            current_item = self.view.ui.joint_list_widget.item(i)
            target_name = current_item.text().split(' -> ')[1]
            indexes.append(self.get_index_shortname_matched_joint(target_name, self.dest_joint_names))

        return indexes

    def get_joint_name_list(self, skinweight_dict):
        """skinweightのdictからjointの名前のリストを作成する

        Args:
            skinweight_dict (dict): skinweightのdict

        Returns:
            list(str): ジョイント名のリスト
        """
        joints = []
        influences = skinweight_dict[list(skinweight_dict.keys())[0]].jointdatas
        for joint in influences:
            joints.append(joint.name)

        return joints

    def get_index_shortname_matched_joint(self, short_name, joint_list):
        """ジョイント名のリストでショートネーム以外がマッチするものを探す

        Args:
            short_name (str): 検索する名前
            joint_list (list[str]): 検索対象のジョイント名を格納したリスト

        Returns:
            int: マッチしたインデックスを返します.見つからない場合は-1が返されます
        """
        match_index = -1

        for index, joint_name in enumerate(joint_list):
            current_joint_name = utility.get_namespace_removed_shortname(joint_name)
            if short_name == current_joint_name:
                match_index = index
                break

        return match_index
