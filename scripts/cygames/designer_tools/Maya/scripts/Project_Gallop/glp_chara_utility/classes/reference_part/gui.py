# -*- coding: utf-8 -*-

from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

import sys
import itertools

try:
    # Maya 2022-
    from importlib import reload
except Exception:
    pass

from maya import cmds
from maya import OpenMayaUI as omui
from maya.app.general import mayaMixin

from PySide2 import QtWidgets
import shiboken2

from . import reference_widget
from . import manager_window

from . import reference_part

reload(reference_widget)
reload(manager_window)


class ReferenceWidget(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(ReferenceWidget, self).__init__(*args, **kwargs)

        self.is_main = False
        self.is_mini = False
        self.data_id = None
        self.parent_window = None
        self.buttons_visible = True

        self.ui = reference_widget.Ui_Form()
        self.ui.setupUi(self)

        self.ui.removeReferenceButton.clicked.connect(self.__remove_references)
        self.ui.selectJointButton.clicked.connect(self.__select_root_joints)
        self.ui.resetYButton.clicked.connect(self.reset_position_y)

    def __update(self):
        """UIを更新
        """

        self.ui.typeLabel.setText('ミニ' if self.is_mini else 'デカ')
        self.ui.idLabel.setText(self.data_id)
        self.ui.selectJointButton.setVisible(self.buttons_visible)
        self.ui.resetYButton.setVisible(self.buttons_visible)

    def setup(self, is_main, is_mini, data_id, parent_window):
        """初期化
        """

        self.is_main = is_main
        self.is_mini = is_mini
        self.data_id = data_id
        self.parent_window = parent_window

        if self.parent_window.is_general:
            self.buttons_visible = self.is_mini != self.parent_window.is_mini
        else:
            self.buttons_visible = not self.is_main

        self.__update()

    def get_base_position_y(self):
        """Y座標を取得する
        """

        body_ref_node = next((node for node in self.__get_target_ref_nodes() if reference_part.is_ref_data_type(node, 'bdy')), None)

        if body_ref_node is None:
            return 0

        namespace = cmds.referenceQuery(body_ref_node, ns=True, shn=True)
        top_nodes = cmds.ls(namespace + ':*', assemblies=True, l=True)

        if not top_nodes:
            return 0

        body_mesh_nodes = (reference_part.get_node_target_word(top_node, 'M_Body') for top_node in top_nodes)
        body_mesh_node = next((joint for joint in body_mesh_nodes if joint), '')

        if not body_mesh_node:
            return 0

        return cmds.xform(cmds.ls(body_mesh_node, l=True)[0], q=True, ws=True, bb=True)[1]

    def __get_target_ref_nodes(self):
        """対象リファレンスを取得
        """

        all_ref_nodes = reference_part.get_loaded_ref_nodes()

        if not all_ref_nodes:
            return []

        target_ref_nodes = []

        for ref_node in all_ref_nodes:

            if reference_part.is_ref_mini(ref_node) != self.is_mini:
                continue

            if not reference_part.get_ref_data_id(ref_node) == self.data_id:
                continue

            target_ref_nodes.append(ref_node)

        return target_ref_nodes

    def __remove_references(self):
        """リファレンスを削除
        """

        for ref_node in self.__get_target_ref_nodes():

            namespace = cmds.referenceQuery(ref_node, ns=True, shn=True)
            reference_part.unload_ref_path(namespace)

            self.deleteLater()

    def __get_root_joints(self):
        """ルートジョイントを取得
        """

        root_joints = []

        for ref_node in self.__get_target_ref_nodes():

            namespace = cmds.referenceQuery(ref_node, ns=True, shn=True)
            top_nodes = cmds.ls(namespace + ':*', assemblies=True, l=True)

            if not top_nodes:
                continue

            temp_root_joints = (reference_part.get_root_joint_node(top_node) for top_node in top_nodes)
            root_joint = next((joint for joint in temp_root_joints if joint), '')

            if not root_joint:
                continue

            root_joints.append(root_joint)

        return root_joints

    def __select_root_joints(self):
        """ジョイントを選択
        """

        root_joints = self.__get_root_joints()

        cmds.select(root_joints, r=True)

    def reset_position_y(self, base_position_y=None):
        """Y位置を再設定
        """

        if base_position_y is None:
            base_position_y = self.parent_window.get_base_position_y()

        root_joints = self.__get_root_joints()

        body_root_joint = next((joint for joint in root_joints if reference_part.is_ref_data_type(joint, 'bdy')), None)

        if body_root_joint is None:
            return

        diff_y = base_position_y - cmds.xform(body_root_joint, q=True, ws=True, t=True)[1]

        cmds.xform(root_joints, ws=True, t=[0, diff_y, 0], r=True)


class ManagerWindow(mayaMixin.MayaQWidgetBaseMixin, QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(ManagerWindow, self).__init__(*args, **kwargs)

        self.is_mini = False
        self.data_id = None
        self.is_general = False

        self.ui = manager_window.Ui_GallopCharaUtilityReferenceManagerWindow()
        self.ui.setupUi(self)

        self.setProperty(str('saveWindowPref'), True)

        self.ui.refreshReferenceListButton.clicked.connect(self.__refresh_reference_widgets)
        self.ui.resetYButton.clicked.connect(self.__reset_position_y)

        self.__refresh_reference_widgets()

    def show(self):
        ptr = omui.MQtUtil.mainWindow()

        if sys.version_info.major == 2:
            main_window = shiboken2.wrapInstance(long(ptr), QtWidgets.QMainWindow)
        else:
            # for Maya 2022-
            main_window = shiboken2.wrapInstance(int(ptr), QtWidgets.QMainWindow)

        for widget in main_window.children():
            if str(type(self)) == str(type(widget)):
                widget.deleteLater()    # Mayaウインドウの子からインスタンスを削除

        super(ManagerWindow, self).show()

    def get_base_position_y(self):
        """リファレンスのY座標を取得する
        """

        if self.is_general:
            main_widget = next((widget for widget in self.__get_all_widgets() if widget.is_mini == self.is_mini), None)
        else:
            main_widget = next((widget for widget in self.__get_all_widgets() if widget.is_main), None)

        if main_widget is None:
            return 0

        return main_widget.get_base_position_y()

    def __update_dress_id(self):
        """衣装IDをシーンから取得して更新
        """

        is_normal, data_id, is_general = reference_part.get_scene_dress_id()

        self.is_mini = not is_normal
        self.data_id = data_id
        self.is_general = is_general

    def __get_all_widgets(self):
        """すべてのノードウィジェットを取得
        """

        layout = self.ui.referenceListLayout
        widgets = (layout.itemAt(i).widget() for i in range(layout.count()))
        return [widget for widget in widgets if widget]

    def __clear_main_layout(self):
        """ノードリストをクリア
        """

        layout = self.ui.referenceListLayout
        widgets = [layout.itemAt(i).widget() for i in range(layout.count())]

        for widget in widgets:
            if not widget:
                continue

            widget.deleteLater()

    def __refresh_reference_widgets(self):
        """ノードリストを更新
        """

        self.__update_dress_id()

        self.__clear_main_layout()

        ref_nodes = reference_part.get_loaded_ref_nodes()

        if ref_nodes:
            ref_data = [(reference_part.is_ref_mini(ref_node), reference_part.get_ref_data_id(ref_node)) for ref_node in ref_nodes]

            for key, _ in itertools.groupby(sorted(ref_data)):
                is_mini, data_id = key
                is_main = is_mini == self.is_mini and data_id == self.data_id

                widget = ReferenceWidget()
                widget.setup(is_main, is_mini, data_id, self)

                layout = self.ui.referenceListLayout
                layout.insertWidget(layout.count() - 1, widget)

        reset_button_visible = any(widget.buttons_visible for widget in self.__get_all_widgets())

        self.ui.resetYButton.setVisible(reset_button_visible)

    def __reset_position_y(self):
        """Y位置を再設定
        """

        self.__refresh_reference_widgets()

        position_y = self.get_base_position_y()

        for widget in self.__get_all_widgets():

            if widget.is_main:
                continue

            widget.reset_position_y(position_y)
