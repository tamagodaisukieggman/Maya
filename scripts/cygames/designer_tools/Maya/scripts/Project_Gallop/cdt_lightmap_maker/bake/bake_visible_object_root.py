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

from ..ui import icon_button as ui_icon_button
from ..ui import dialog as ui_dialog

from . import param_item_group

from . import bake_setting_param_list as sp
from . import bake_group_param_list as gp
from . import bake_visible_object_param_list as vop


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BakeVisibleObjectRoot(object):

    # ===========================================
    def __init__(self):

        self.main = None
        self.is_group = False

        self.param_item_group = None

        self.param_key_list = None

        self.ui_object_text_scroll_list = None
        self.current_select_index_list = [1]

        self.target_object_list = None

    # ===========================================
    def initialize(self):

        self.param_item_group = param_item_group.ParamItemGroup()

        self.param_item_group.attr_prefix = \
            self.main.attr_prefix + "visibleobj_"
        self.param_item_group.ui_prefix = \
            self.main.ui_prefix + "visibleobj_"
        self.param_item_group.function = \
            self.main.change_ui

        self.param_key_list = []

        self.param_key_list.append(vop.visible_link)

        for key in self.param_key_list:

            self.param_item_group.add_item(
                vop.get_name(key),
                vop.get_type(key),
                vop.get_value(key),
                vop.get_ui_label(key),
                vop.get_ui_type(key)
            )

    # ===========================================
    def create_ui(self):

        icon_size = (40, 40)

        cmds.frameLayout(l=u'表示オブジェクトリスト', cll=0, cl=0, bv=1, mw=5, mh=5)

        self.ui_object_text_scroll_list = cmds.textScrollList(
            ams=True, w=50, h=150,
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

        cmds.setParent('..')

        cmds.setParent('..')

    # ===========================================
    def update_ui(self):

        self.current_select_index_list = cmds.textScrollList(
            self.ui_object_text_scroll_list,
            q=True,
            sii=True)

        self.create_target_object_list()

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
            except:
                pass

        select_object_list = cmds.textScrollList(
            self.ui_object_text_scroll_list, q=True, si=True)

        if utility_common.ListMethod.exist_list(select_object_list):

            self.set_target(select_object_list[0])

            self.param_item_group.set_ui_from_attr_all()

    # ===========================================
    def change_ui(self):

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

        select_object_list = cmds.ls(sl=True, l=True)

        if not utility_common.ListMethod.exist_list(select_object_list):
            return

        for select in select_object_list:

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
    def set_target(self, target):

        self.param_item_group.set_target(target)

        attr_prefix = None

        if self.is_group:

            attr_prefix = \
                self.main.attr_prefix + \
                'visibleobj_set{0:02d}_grp{1:02d}_'.format(
                    self.main.bake_setting_root.target_setting.index,
                    self.main.bake_group_root.target_group.index)

        else:

            attr_prefix = \
                self.main.attr_prefix + \
                'visibleobj_set{0:02d}_'.format(
                    self.main.bake_setting_root.target_setting.index)

        if attr_prefix is None:
            return

        self.param_item_group.set_attr_prefix_all(attr_prefix)

    # ===========================================
    def link_object(self, target_node):

        self.set_target(target_node)

        if self.is_group:

            utility_attribute.Method.connect_attr(
                self.main.bake_group_root.target_group.target,
                self.main.bake_group_root.param_item_group.get_attr_name(
                    gp.get_name(gp.visible_link)),
                target_node,
                self.param_item_group.get_attr_name(
                    vop.get_name(vop.visible_link))
            )

        else:

            utility_attribute.Method.connect_attr(
                self.main.bake_setting_root.target_setting.target,
                self.main.bake_setting_root.param_item_group.get_attr_name(
                    sp.get_name(sp.visible_link)),
                target_node,
                self.param_item_group.get_attr_name(
                    vop.get_name(vop.visible_link))
            )

    # ===========================================
    def unlink_object(self, target_node):

        self.set_target(target_node)

        if self.is_group:

            utility_attribute.Method.disconnect_attr(
                self.main.bake_group_root.target_group.target,
                self.main.bake_group_root.param_item_group.get_attr_name(
                    gp.get_name(gp.visible_link)),
                target_node,
                self.param_item_group.get_attr_name(
                    vop.get_name(vop.visible_link))
            )

        else:

            utility_attribute.Method.disconnect_attr(
                self.main.bake_setting_root.target_setting.target,
                self.main.bake_setting_root.param_item_group.get_attr_name(
                    sp.get_name(sp.visible_link)),
                target_node,
                self.param_item_group.get_attr_name(
                    vop.get_name(vop.visible_link))
            )

    # ===========================================
    def is_link_object(self, target_node):

        self.set_target(target_node)

        link_attr_name = None

        if self.is_group:

            link_attr_name = self.param_item_group.get_attr_name(
                vop.get_name(vop.visible_link))

        else:

            link_attr_name = self.param_item_group.get_attr_name(
                vop.get_name(vop.visible_link))

        if link_attr_name is None:
            return False

        connect_object_list = cmds.listConnections(
            target_node + '.' + link_attr_name, d=False, s=True)

        if connect_object_list is None:
            return False

        if len(connect_object_list) == 0:
            return False

        return True

    # ===========================================
    def create_target_object_list(self):

        self.target_object_list = []

        link_attr_name = None
        target_transform = None

        if self.is_group:

            link_attr_name = \
                self.main.bake_group_root.param_item_group.get_attr_name(
                    gp.get_name(gp.visible_link))

            if not utility_attribute.Method.exist_attr(
                    self.main.bake_group_root.target_group.target, link_attr_name):
                return

            target_transform = self.main.bake_group_root.target_group.target

        else:

            link_attr_name = \
                self.main.bake_setting_root.param_item_group.get_attr_name(
                    sp.get_name(sp.visible_link))

            if not utility_attribute.Method.exist_attr(
                    self.main.bake_setting_root.target_setting.target, link_attr_name):
                return

            target_transform = self.main.bake_setting_root.target_setting.target

        if link_attr_name is None:
            return

        connect_object_list = cmds.listConnections(
            target_transform + '.' + link_attr_name, d=True, s=False)

        if connect_object_list is None:
            return

        if len(connect_object_list) == 0:
            return

        for cnt in range(0, len(connect_object_list)):

            this_object = utility_common.NameMethod.get_long_name(
                connect_object_list[cnt])

            if utility_common.NodeMethod.exist_transform(this_object) is None:
                continue

            if not self.is_link_object(this_object):
                continue

            self.target_object_list.append(this_object)

        self.target_object_list.sort()

    # ===========================================
    def hide_target_object(self):

        self.create_target_object_list()

        if len(self.target_object_list) == 0:
            return

        for target_object in self.target_object_list:

            utility_attribute.Method.set_attr(
                target_object,
                'visibility',
                'bool',
                False
            )

    # ===========================================
    def show_target_object(self):

        self.create_target_object_list()

        if len(self.target_object_list) == 0:
            return

        for target_object in self.target_object_list:

            utility_attribute.Method.set_attr(
                target_object,
                'visibility',
                'bool',
                True
            )
