# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

from PySide2 import QtWidgets
from maya import OpenMayaUI

import sys
import shiboken2

import maya.cmds as cmds

from . import view
from . import item
from . import define

from .process_widget import base_widget
from .process_model import base_model

from .process_widget import rotation_2_hierarchy as r2h_widget
from .process_model import rotation_2_hierarchy as r2h_model

from .process_widget import transform_from_angle as tfa_widget
from .process_model import transform_from_angle as tfa_model

try:
    # Maya2022-
    from builtins import object
    from importlib import reload
except Exception:
    pass

reload(view)
reload(item)
reload(define)
reload(base_widget)
reload(base_model)
reload(r2h_widget)
reload(r2h_model)
reload(tfa_widget)
reload(tfa_model)


class Main(object):

    def __init__(self):
        """
        """

        self.view = view.View(self)
        self.view.setWindowTitle(define.TOOL_NAME + define.TOOL_VERSION)

        self.tp_process_datas = [
            {
                'label': 'None',
                'widget': None,
                'model': None,
            },
            {
                'label': 'Inverse Y Rotation To Hierarchy',
                'widget': r2h_widget.Rotation2HierarchyWidget,
                'model': r2h_model.Rotation2HierarchyModel,
            },
            {
                'label': 'Add Position From Angle',
                'widget': tfa_widget.TransformFromAngeleWidget,
                'model': tfa_model.TransformFlomAngleModel,
            },
        ]

    def deleteOverlappingWindow(self, target):
        """Windowの重複削除処理
        """

        main_window = OpenMayaUI.MQtUtil.mainWindow()
        if main_window is None:
            return

        if sys.version_info.major == 2:
            main_window = shiboken2.wrapInstance(long(main_window), QtWidgets.QMainWindow)
        else:
            main_window = shiboken2.wrapInstance(int(main_window), QtWidgets.QMainWindow)

        for widget in main_window.children():
            if str(type(target)) == str(type(widget)):
                widget.deleteLater()

    def close_event(self):
        """viewのクローズイベントから呼ばれるメソッド
        """
        self.all_disable(True)

    def show_ui(self):
        """UI描画
        """

        # windowの重複削除処理
        self.deleteOverlappingWindow(self.view)
        self.setup_view_event()
        self.restore_tp_process_item()
        self.view.show()
        self.save_all_items()

    def tp_process_items(self):
        """リストされているプロセスアイテムを取得

        Returns:
            [item.Item]: プロセスアイテムリスト
        """

        return self.view.widgets()

    def restore_tp_process_item(self):
        """シーン内のスクリプトノードからtpプロセスを復元
        """

        def __get_item_order(node):
            return cmds.getAttr(node + '.itemOrder') if cmds.attributeQuery('itemOrder', n=node, ex=True) else -1

        save_nodes = cmds.ls(define.ITEM_NODE_BASE_NAME + '*', typ='script') or []
        if save_nodes:
            save_nodes.sort(key=__get_item_order)

        for save_node in save_nodes:
            self.add_item(save_node)

    def setup_view_event(self):
        """UIのevent設定
        """
        self.view.addCallback('SceneOpened', self.reload_items)
        self.view.ui.add_item_button.clicked.connect(self.add_item)
        self.view.ui.update_item_button.clicked.connect(self.reload_items)
        self.view.ui.all_enable_button.clicked.connect(self.all_enable)
        self.view.ui.all_disable_button.clicked.connect(self.all_disable)

    def reload_items(self, arg=None):
        """アイテムリストの更新
        """

        self.all_disable(True)
        self.view.clear_item_widgets()
        self.restore_tp_process_item()

    def add_item(self, save_node=None):
        """新規プロセスアイテムの追加

        Args:
            save_node (str, optional): アイテム情報をセーブしているノード. Defaults to None.

        Returns:
            item.Item: 作成したアイテムウィジェット
        """

        new_item = item.Item(self.view, self.tp_process_datas, save_node)
        new_item.delete_process_item.connect(self.delete_item)

        self.view.add_item_widget(new_item)
        new_item.save_item()

        return new_item

    def delete_item(self, widget):
        """プロセスアイテムの削除

        Args:
            widget (item.Item): アイテムウィジェット
        """

        self.view.remove_item_widget(widget)

    def all_enable(self):
        """全アイテムを有効
        """

        process_items = self.tp_process_items()
        if process_items:
            for process_item in process_items:
                process_item.set_activated(True)

    def all_disable(self, no_save=False):
        """全アイテムを無効

        Args:
            no_save (bool): 状態をセーブするか.ツール終了時など状態を保存せずに無効化する時にTrueにする
        """

        process_items = self.tp_process_items()
        if process_items:
            for process_item in process_items:
                if no_save:
                    process_item.set_save_block(True)
                    process_item.set_activated(False)
                    process_item.set_save_block(False)
                else:
                    process_item.set_activated(False)

    def save_all_items(self):
        """全アイテムを情報をセーブノードにセーブ
        """

        process_items = self.tp_process_items()
        if process_items:
            for process_item in process_items:
                process_item.save_item()


