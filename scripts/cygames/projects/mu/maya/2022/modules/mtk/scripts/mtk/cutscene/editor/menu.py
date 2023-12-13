# -*- coding: utf-8 -*-
"""メニューの登録、解除などの機能"""
from __future__ import absolute_import as _absolute_import
from __future__ import unicode_literals as _unicode_literals
from __future__ import division as _division
from __future__ import print_function as _print_function

import abc
from mtk.cutscene import utility

import six

from maya import cmds


@six.add_metaclass(abc.ABCMeta)
class SequencerMenuRegister(object):
    """Sequencerのメニュー登録機能
    """
    @classmethod
    @abc.abstractmethod
    def add_menu(cls, name, label):
        pass

    @classmethod
    @abc.abstractmethod
    def add_menu_item(cls, menu_name, items_name, command=None, option_command=None):
        pass

    @classmethod
    @abc.abstractmethod
    def delete_menu(cls, menu_name):
        pass


class CameraSequencerMenuRegister(SequencerMenuRegister):
    """Camera Sequencer用のメニュー登録機能
    """

    @classmethod
    def add_menu(cls, name, label):
        camera_sequencer_panel = cmds.getPanel(withLabel="Camera Sequencer")

        if not utility.panel.is_active_panel(camera_sequencer_panel):
            return

        cmds.menu(name, parent=camera_sequencer_panel, tearOff=True, label=label, allowOptionBoxes=True)

    @classmethod
    def add_menu_item(cls, items_name, **kwargs):

        if not cmds.menu(kwargs["parent"], exists=True):
            return

        cmds.menuItem(items_name, **kwargs)

    @classmethod
    def delete_menu(cls, menu_name):
        if cmds.menu(menu_name, q=True, exists=True):
            cmds.menu(menu_name, e=True, deleteAllItems=True)

            cmds.deleteUI(menu_name, menu=True)

    @classmethod
    def add_tool_bar(cls, tool_bar_name, colum_count):
        # toolbar取得の為に必ず存在する既存のボタンを取得している
        if cls.__can_add_toolbar():
            camera_sequencer_tool_bar = cls.__get_toolbar_root()
            return cmds.rowLayout(tool_bar_name, numberOfColumns=colum_count, parent=camera_sequencer_tool_bar)

    @classmethod
    def add_tool_bar_icon_text_button(cls, tool_bar_name, button_name, image="Camera.png", command="print()"):
        """ツールバーにボタンを追加する

        :param tool_bar_name: ツールバー名
        :type tool_bar_name: str
        :param button_name: 作成するボタン名
        :type button_name: str
        :param image: アイコン名(例: Camera.png)
        :type image: str
        :param command: ボタン実行時のcommand
        :type command: str
        """
        if cls.__can_add_toolbar():
            cmds.iconTextButton(button_name, image=image, command=command, parent=tool_bar_name)

    @classmethod
    def delete_tool_bar(cls, target_toolbar_name):
        if cmds.rowLayout(target_toolbar_name, q=True, exists=True):
            cmds.deleteUI(target_toolbar_name, layout=True)

    @classmethod
    def __get_toolbar_root(cls):
        """ツールバールートを取得する

        CameraSequencerに必ず存在するボタン経由で親を取得する

        :return: CameraSequencerのToolbarルート名
        :rtype: str
        """
        camera_sequencer_tool_bar_sub_layout = cmds.symbolCheckBox("sequenceEditorIgnoreGapsCheckBox", query=True, parent=True)
        camera_sequencer_tool_bar_root = cmds.formLayout(camera_sequencer_tool_bar_sub_layout, query=True, parent=True)

        return camera_sequencer_tool_bar_root

    @classmethod
    def __can_add_toolbar(cls):
        """ツールバー追加確認

        CameraSequencerに存在するボタンが表示されている=追加可能なので、その条件で取得する

        :return: 追加可能かどうか
        :rtype: bool
        """
        return cmds.symbolCheckBox("sequenceEditorIgnoreGapsCheckBox", exists=True)
