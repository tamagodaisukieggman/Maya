# -*- coding: utf-8 -*-

from __future__ import absolute_import

try:
    # Maya 2022-
    from builtins import range
    from builtins import object
except Exception:
    pass

import maya.cmds as cmds
import maya.mel as mel

from ..utility import common as utility_common
from ..utility import attribute as utility_attribute
from ..utility import uvset as utility_uvset
from ..utility import colorset as utility_colorset

from .. import utility as cmn_utility

from ..ui import icon_button as ui_icon_button
from ..ui import dialog as ui_dialog

from . import param_item_group

from . import bake_common_param_list as cp
from . import bake_setting_param_list as sp
from . import bake_group_param_list as gp
from . import bake_object_param_list as op

from . import bake_object


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BakeObjectRoot(object):

    # ===========================================
    def __init__(self, main):

        self.main = main

        self.param_item_group_for_link = None
        self.param_item_group = None
        self.param_key_list = None

        self.ui_object_text_scroll_list = None
        self.current_select_index_list = [1]

        self.target_object_list = None

    # ===========================================
    def initialize(self):

        self.param_item_group_for_link = param_item_group.ParamItemGroup()
        self.param_item_group = param_item_group.ParamItemGroup()

        self.param_item_group_for_link.attr_prefix = \
            self.main.attr_prefix + "obj_"
        self.param_item_group_for_link.ui_prefix = \
            self.main.ui_prefix + "obj_"
        self.param_item_group_for_link.function = \
            self.main.change_ui

        self.param_item_group.attr_prefix = \
            self.main.attr_prefix + "obj_"
        self.param_item_group.ui_prefix = \
            self.main.ui_prefix + "obj_"
        self.param_item_group.function = \
            self.main.change_ui

        self.param_key_list = []
        self.param_key_list.append(op.group_link)

        for key in self.param_key_list:

            self.param_item_group_for_link.add_item(
                op.get_name(key),
                op.get_type(key),
                op.get_value(key),
                op.get_ui_label(key),
                op.get_ui_type(key)
            )

        self.param_key_list = []
        self.param_item_group.param_item_list = []

        for key in self.param_key_list:

            self.param_item_group.add_item(
                op.get_name(key),
                op.get_type(key),
                op.get_value(key),
                op.get_ui_label(key),
                op.get_ui_type(key)
            )

    # ===========================================
    def create_ui(self):

        icon_size = (40, 40)

        cmds.frameLayout(l=u'対象メッシュリスト', cll=0, cl=0, bv=1, mw=5, mh=5)

        self.ui_object_text_scroll_list = cmds.textScrollList(
            ams=True, w=50, h=200,
            sc=self.select_object_from_ui)

        cmds.flowLayout(columnSpacing=0)

        ui_icon_button.IconButton(
            'menuIconSelected.png',
            'Sel',
            u'全て選択',
            icon_size,
            None,
            self.select_all_object_from_ui,
            None
        )

        ui_icon_button.IconButton(
            'menuIconSelected.png',
            'Add',
            u'選択しているオブジェクトをリストに追加',
            icon_size,
            None,
            self.add_object_from_ui,
            None
        )

        ui_icon_button.IconButton(
            'menuIconSelected.png',
            'Rem',
            u'リストから除外',
            icon_size,
            None,
            self.remove_object_from_ui,
            None
        )

        ui_icon_button.IconButton(
            'menuIconSelected.png',
            'Clr',
            u'リストクリア',
            icon_size,
            None,
            self.remove_all_object_from_ui,
            None
        )

        ui_icon_button.IconButton('openBar.png', None)

        ui_icon_button.IconButton(
            'polySphere.png',
            None,
            u'選択中グループの乗算頂点カラーを編集',
            icon_size,
            (0.5, 0.5, 0.6),
            self.set_colorset_from_ui,
            cp.colorset_multiply
        )

        ui_icon_button.IconButton(
            'polySphere.png',
            None,
            u'選択中グループの加算頂点カラーを編集',
            icon_size,
            (0.6, 0.5, 0.5),
            self.set_colorset_from_ui,
            cp.colorset_add
        )

        ui_icon_button.IconButton(
            'polySphere.png',
            None,
            u'選択中グループのオーバーレイ頂点カラーを編集',
            icon_size,
            (0.5, 0.6, 0.5),
            self.set_colorset_from_ui,
            cp.colorset_overlay
        )

        cmds.setParent('..')

        cmds.setParent('..')

    # ===========================================
    def update_ui(self):

        self.current_select_index_list = cmds.textScrollList(
            self.ui_object_text_scroll_list,
            q=True,
            sii=True)

        self.update_target_object_list()

        cmds.textScrollList(self.ui_object_text_scroll_list, e=True, ra=True)

        for cnt in range(0, len(self.target_object_list)):

            cmds.textScrollList(
                self.ui_object_text_scroll_list,
                e=True,
                a=self.target_object_list[cnt]
            )

        if self.current_select_index_list is not None:
            try:
                cmds.textScrollList(
                    self.ui_object_text_scroll_list,
                    e=True,
                    sii=self.current_select_index_list)
            except Exception:
                pass

        select_object_list = cmds.textScrollList(
            self.ui_object_text_scroll_list, q=True, si=True)

        if utility_common.ListMethod.exist_list(select_object_list):

            self.set_target(select_object_list[0])

            self.param_item_group_for_link.set_ui_from_attr_all()
            self.param_item_group.set_ui_from_attr_all()

    # ===========================================
    def change_ui(self):

        self.param_item_group_for_link.set_attr_from_ui_all()
        self.param_item_group.set_attr_from_ui_all()

    # ===========================================
    def select_object_from_ui(self):

        select_object_list = cmds.textScrollList(
            self.ui_object_text_scroll_list, q=True, si=True)

        if select_object_list is None:
            return

        if len(select_object_list) == 0:
            return

        self.main.update_ui()

        cmds.select(select_object_list, r=True)

    # ===========================================
    def select_all_object_from_ui(self):

        all_object_list = cmds.textScrollList(
            self.ui_object_text_scroll_list, q=True, ai=True)

        if all_object_list is None:
            return

        if len(all_object_list) == 0:
            return

        self.main.update_ui()

        cmds.select(all_object_list, r=True)

    # ===========================================
    def add_object_from_ui(self):

        select_object_list = cmds.ls(sl=True, l=True, typ='transform')

        if not utility_common.ListMethod.exist_list(select_object_list):
            return

        cmds.select(hi=True)

        select_object_list = cmds.ls(sl=True, l=True, typ='transform')

        if not utility_common.ListMethod.exist_list(select_object_list):
            return

        for select in select_object_list:

            this_mesh = utility_common.NodeMethod.get_mesh_shape(
                select
            )

            if this_mesh is None:
                continue

            self.link_object(select)

        self.main.update_ui()

    # ===========================================
    def remove_object_from_ui(self):

        select_object_list = cmds.textScrollList(
            self.ui_object_text_scroll_list, q=True, si=True)

        if select_object_list is None:
            return

        if len(select_object_list) == 0:
            return

        for select in select_object_list:

            self.unlink_object(select)

        self.main.update_ui()

    # ===========================================
    def remove_all_object_from_ui(self):

        all_object_list = cmds.textScrollList(
            self.ui_object_text_scroll_list, q=True, ai=True)

        if all_object_list is None:
            return

        if len(all_object_list) == 0:
            return

        for select in all_object_list:

            self.unlink_object(select)

        self.main.update_ui()

    # ===========================================
    def set_colorset_from_ui(self, colorset_type):

        self.update_target_object_list()

        for target_object in self.target_object_list:

            bake_object.Method.set_colorset(
                target_object, self.main.bake_group_root.target_group, colorset_type)

    # ===========================================
    def set_target(self, target_transform):

        self.param_item_group_for_link.set_target(target_transform)
        self.param_item_group.set_target(target_transform)

        link_attr_prefix = \
            self.main.attr_prefix + 'obj_'

        attr_prefix = \
            self.main.attr_prefix + \
            'obj_set{0:02d}_grp{1:02d}_'.format(
                self.main.bake_setting_root.target_setting.index,
                self.main.bake_group_root.target_group.index)

        self.param_item_group_for_link.set_attr_prefix_all(link_attr_prefix)
        self.param_item_group.set_attr_prefix_all(attr_prefix)

    # ===========================================
    def link_object(self, target_transform):

        self.set_target(target_transform)

        utility_attribute.Method.connect_attr(
            self.main.bake_group_root.target_group.target,
            self.main.bake_group_root.param_item_group.get_attr_name(
                gp.get_name(gp.group_link)),
            target_transform,
            self.param_item_group_for_link.get_attr_name(
                op.get_name(op.group_link))
        )

    # ===========================================
    def unlink_object(self, target_transform):

        self.set_target(target_transform)

        utility_attribute.Method.disconnect_attr(
            self.main.bake_group_root.target_group.target,
            self.main.bake_group_root.param_item_group.get_attr_name(
                gp.get_name(gp.group_link)),
            target_transform,
            self.param_item_group_for_link.get_attr_name(
                op.get_name(op.group_link))
        )

    # ===========================================
    def update_target_object_list(self):

        self.target_object_list = self.get_target_object_list()

        if not cmn_utility.list.Method.exist_list(self.target_object_list):
            self.target_object_list = []

        return self.target_object_list

    # ===========================================
    def get_target_object_list(self):

        link_attr_name = \
            self.main.bake_group_root.param_item_group.get_attr_name(
                gp.get_name(gp.group_link))

        if not utility_attribute.Method.exist_attr(
                self.main.bake_group_root.target_group.target, link_attr_name):
            return

        connect_object_list = cmds.listConnections(
            self.main.bake_group_root.target_group.target + '.' + link_attr_name, d=True, s=True)

        if connect_object_list is None:
            return

        if len(connect_object_list) == 0:
            return

        self.target_object_list = []

        for cnt in range(0, len(connect_object_list)):

            this_object = utility_common.NameMethod.get_long_name(
                connect_object_list[cnt])

            if utility_common.NodeMethod.exist_transform(this_object) is None:
                continue

            self.target_object_list.append(this_object)

        self.target_object_list.sort()

        return self.target_object_list
