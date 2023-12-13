# -*- coding: utf-8 -*-

from __future__ import absolute_import

try:
    # Maya 2022-
    from builtins import str
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
from . import bake_export_object_param_list as eop


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BakeExportObjectRoot(object):

    # ===========================================
    def __init__(self):

        self.main = None

        self.param_item_group = None

        self.param_key_list = None

        self.export_item_num = 10

        self.ui_object_text_scroll_list = None
        self.current_select_index_list = [1]

        self.target_object_list = None

    # ===========================================
    def initialize(self):

        self.param_item_group = param_item_group.ParamItemGroup()

        self.param_item_group.attr_prefix = \
            self.main.attr_prefix + "exportobj_"
        self.param_item_group.ui_prefix = \
            self.main.ui_prefix + "exportobj_"
        self.param_item_group.function = \
            self.main.change_ui

        self.param_key_list = []

        self.param_key_list.append(eop.link)
        # self.param_key_list.append(eop.transform_replace_key)
        # self.param_key_list.append(eop.transform_replace_value)
        self.param_key_list.append(eop.material_replace_key)
        self.param_key_list.append(eop.material_replace_value)
        # self.param_key_list.append(eop.texture_replace_key)
        # self.param_key_list.append(eop.texture_replace_value)

        for key in self.param_key_list:

            self.param_item_group.add_item(
                eop.get_name(key),
                eop.get_type(key),
                eop.get_value(key),
                eop.get_ui_label(key),
                eop.get_ui_type(key)
            )

        self.param_key_list = []

        self.param_key_list.append(eop.export_item_enable)
        self.param_key_list.append(eop.export_item_name)
        self.param_key_list.append(eop.export_item_start_frame)
        self.param_key_list.append(eop.export_item_end_frame)

        for key in self.param_key_list:

            for p in range(self.export_item_num):

                self.param_item_group.add_item(
                    eop.get_name(key) + str(p),
                    eop.get_type(key),
                    eop.get_value(key),
                    eop.get_ui_label(key),
                    eop.get_ui_type(key)
                )

    # ===========================================
    def create_ui(self):

        icon_size = (40, 40)

        cmds.frameLayout(
            l=u'出力オブジェクトリスト', cll=0, cl=0, bv=1, mw=4, mh=4)

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

        cmds.setParent('..')

        # self.param_item_group.draw_ui(
        #    eop.get_name(eop.transform_replace_key))

        # self.param_item_group.draw_ui(
        #     eop.get_name(eop.transform_replace_value))

        cmds.separator(height=5, style='in')

        self.param_item_group.draw_ui(
            eop.get_name(eop.material_replace_key))

        self.param_item_group.draw_ui(
            eop.get_name(eop.material_replace_value))

        cmds.separator(height=5, style='in')

        # self.param_item_group.draw_ui(
        #    eop.get_name(eop.texture_replace_key))

        # self.param_item_group.draw_ui(
        #    eop.get_name(eop.texture_replace_value))

        cmds.frameLayout(
            l=u'出力設定リスト', cll=1, cl=0, bv=1, mw=5, mh=5)

        for p in range(self.export_item_num):

            num_string = str(p)

            this_open = True

            if p == 0:
                this_open = False

            cmds.frameLayout(
                l=u'出力設定 ' + str(p + 1), cll=1, cl=this_open, bv=1, mw=5, mh=5)

            self.param_item_group.draw_ui(
                eop.get_name(eop.export_item_enable) + num_string)

            self.param_item_group.draw_ui(
                eop.get_name(eop.export_item_name) + num_string)

            self.param_item_group.draw_ui(
                eop.get_name(eop.export_item_start_frame) + num_string)

            self.param_item_group.draw_ui(
                eop.get_name(eop.export_item_end_frame) + num_string)

            cmds.setParent('..')

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

        target_setting = self.main.bake_setting_root.target_setting

        select_object_list = cmds.ls(sl=True, l=True)

        if not utility_common.ListMethod.exist_list(select_object_list):
            return

        for select in select_object_list:

            self.link_object_to_bake_setting(select)

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

            self.unlink_object_from_bake_setting(select)

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

            self.unlink_object_from_bake_setting(select)

        self.main.update_ui()

    # ===========================================
    def set_target(self, target):

        self.param_item_group.set_target(target)

        target_setting = self.main.bake_setting_root.target_setting

        attr_prefix = \
            self.main.attr_prefix + \
            'exportobj_set{0:02d}_'.format(target_setting.index)

        self.param_item_group.set_attr_prefix_all(attr_prefix)

    # ===========================================
    def link_object_to_bake_setting(self, target_node):

        self.set_target(target_node)

        target_setting = self.main.bake_setting_root.target_setting

        utility_attribute.Method.connect_attr(
            target_setting.target,
            target_setting.setting_root.param_item_group.get_attr_name(
                sp.get_name(sp.export_link)),
            target_node,
            self.param_item_group.get_attr_name(eop.get_name(eop.link))
        )

    # ===========================================
    def unlink_object_from_bake_setting(self, target_node):

        self.set_target(target_node)

        target_setting = self.main.bake_setting_root.target_setting

        utility_attribute.Method.disconnect_attr(
            target_setting.target,
            target_setting.setting_root.param_item_group.get_attr_name(
                sp.get_name(sp.export_link)),
            target_node,
            self.param_item_group.get_attr_name(eop.get_name(eop.link))
        )

    # ===========================================
    def update_target_object_list(self):

        self.target_object_list = []

        target_setting = self.main.bake_setting_root.target_setting

        link_attr_name = \
            target_setting.setting_root.param_item_group.get_attr_name(
                sp.get_name(sp.export_link))

        if not utility_attribute.Method.exist_attr(
                target_setting.target, link_attr_name):
            return

        connect_object_list = cmds.listConnections(
            target_setting.target + '.' + link_attr_name, d=True, s=False)

        if connect_object_list is None:
            return

        if len(connect_object_list) == 0:
            return

        for cnt in range(0, len(connect_object_list)):

            this_object = utility_common.NameMethod.get_long_name(
                connect_object_list[cnt])

            if utility_common.NodeMethod.exist_transform(this_object) is None:
                continue

            self.target_object_list.append(this_object)

        self.target_object_list.sort()
