# -*- coding: utf-8 -*-

from __future__ import absolute_import

try:
    # Maya 2022-
    from builtins import object
except Exception:
    pass

import maya.cmds as cmds

from . import bake_override_param_list as ovp

from . import param_item_group


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BakeOverrideParam(object):

    # ===========================================
    def __init__(self):

        self.main = None

        self.target = None

        self.parent_param = None

        self.attr_prefix = None
        self.ui_prefix = None

        self.param_item_group = None

        self.key_list = []

        self.key_list.append(ovp.ttl_bc_bakelayername)
        self.key_list.append(ovp.ttl_bc_ao_sampler_name)

        self.key_list.append(ovp.ttl_bc_orthreflect)
        self.key_list.append(ovp.ttl_bc_bakeshadows)
        self.key_list.append(ovp.ttl_bc_bgcolor)

        self.key_list.append(ovp.ttl_bc_ao_mincolor)
        self.key_list.append(ovp.ttl_bc_ao_maxcolor)

        self.key_list.append(ovp.ttl_bc_ao_maxdistance)
        self.key_list.append(ovp.ttl_bc_ao_contrast)
        self.key_list.append(ovp.ttl_bc_ao_scale)
        self.key_list.append(ovp.ttl_bc_ao_accuracy)
        self.key_list.append(ovp.ttl_bc_ao_smooth)

        self.key_list.append(ovp.ttl_bv_samplemode)
        self.key_list.append(ovp.ttl_bv_minsample)
        self.key_list.append(ovp.ttl_bv_maxsample)
        self.key_list.append(ovp.ttl_bv_vtxbias)
        self.key_list.append(ovp.ttl_bv_clamp)
        self.key_list.append(ovp.ttl_bv_rgbscale)
        self.key_list.append(ovp.ttl_bv_rgbmin)
        self.key_list.append(ovp.ttl_bv_rgbmax)
        self.key_list.append(ovp.ttl_bv_enablefilter)
        self.key_list.append(ovp.ttl_bv_filtersize)
        self.key_list.append(ovp.ttl_bv_filtershape)
        self.key_list.append(ovp.ttl_bv_filterdeviation)

        self.key_list.append(ovp.ttl_bt_width)
        self.key_list.append(ovp.ttl_bt_height)
        self.key_list.append(ovp.ttl_bt_bilinear)
        self.key_list.append(ovp.ttl_bt_edgedilation)

        self.key_list.append(ovp.com_bc_colorsetprefix)
        self.key_list.append(ovp.com_bc_settingcolorsetsuffix)
        self.key_list.append(ovp.com_bc_groupcolorsetsuffix)

        self.key_list.append(ovp.com_bc_common_colorset_multi)
        self.key_list.append(ovp.com_bc_common_colorset_add)
        self.key_list.append(ovp.com_bc_common_colorset_overlay)
        self.key_list.append(ovp.com_bc_common_colorset_alpha)

        self.key_list.append(ovp.com_bc_common_colorset_gray)

        self.key_list.append(ovp.com_bc_export_object_dir_path)
        self.key_list.append(ovp.com_bc_export_texture_dir_path)

        self.key_list.append(ovp.com_bc_light_enable)
        self.key_list.append(ovp.com_bc_light_alpha)
        self.key_list.append(ovp.com_bc_light_color_multi)
        self.key_list.append(ovp.com_bc_light_color_offset)

        self.key_list.append(ovp.com_bc_ao_enable)
        self.key_list.append(ovp.com_bc_ao_alpha)
        self.key_list.append(ovp.com_bc_ao_color_multi)
        self.key_list.append(ovp.com_bc_ao_color_offset)

        self.key_list.append(ovp.com_bc_indirect_enable)
        self.key_list.append(ovp.com_bc_indirect_alpha)
        self.key_list.append(ovp.com_bc_indirect_color_multi)
        self.key_list.append(ovp.com_bc_indirect_color_offset)

        self.key_list.append(ovp.com_bt_width)
        self.key_list.append(ovp.com_bt_height)
        self.key_list.append(ovp.com_bt_testwidth)
        self.key_list.append(ovp.com_bt_testheight)
        self.key_list.append(ovp.com_bt_texouptputpath)

        self.key_list.append(ovp.com_bt_textureprefix)
        self.key_list.append(ovp.com_bt_settingtexturesuffix)
        self.key_list.append(ovp.com_bt_grouptexturesuffix)

        self.key_list.append(ovp.com_bt_materialsuffix)
        self.key_list.append(ovp.com_bt_settingmaterialsuffix)
        self.key_list.append(ovp.com_bt_groupmaterialsuffix)

        self.key_list.append(ovp.com_bt_lightmapuv)
        self.key_list.append(ovp.com_bt_customlightmapuv)
        self.key_list.append(ovp.com_bt_unwrapuvmel)
        self.key_list.append(ovp.com_bt_layoutuvmel)

        self.texbake_output_ui_0 = None
        self.texbake_output_ui_1 = None

        self.texbake_lightmapuv_ui_0 = None
        self.texbake_lightmapuv_ui_1 = None

        self.combake_colorset_ui_0 = None
        self.combake_colorset_ui_1 = None

        self.texbake_frame_ui = None
        self.vtxbake_frame_ui = None

        self.is_init = False

    # ===========================================
    def initialize(self):

        self.is_init = False

        if not cmds.objExists(self.target):
            return

        self.param_item_group = param_item_group.ParamItemGroup()
        self.param_item_group.target = self.target
        self.param_item_group.attr_prefix = self.attr_prefix
        self.param_item_group.ui_prefix = self.ui_prefix
        self.param_item_group.function = self.main.change_ui

        for key in self.key_list:
            self.add_item_from_opv(key)

        self.is_init = True

    # ===========================================
    def create_ui(self):

        cmds.columnLayout(adjustableColumn=True)

        cmds.frameLayout(l=u'共通ベイク設定',
                         cll=1, cl=0, bv=1, mw=10, mh=5)
        cmds.columnLayout(adjustableColumn=True)

        cmds.frameLayout(l=u'カラーセット設定', cll=1, cl=0, bv=1, mw=10, mh=5)
        cmds.columnLayout(adjustableColumn=True)

        self.combake_colorset_ui_0 = cmds.columnLayout(adjustableColumn=True)
        cmds.setParent('..')

        self.draw_ui_from_opv(ovp.com_bc_common_colorset_multi)
        self.draw_ui_from_opv(ovp.com_bc_common_colorset_add)
        self.draw_ui_from_opv(ovp.com_bc_common_colorset_overlay)
        self.draw_ui_from_opv(ovp.com_bc_common_colorset_alpha)        
        self.draw_ui_from_opv(ovp.com_bc_common_colorset_gray)

        self.draw_ui_from_opv(ovp.com_bc_colorsetprefix)
        self.draw_ui_from_opv(ovp.com_bc_settingcolorsetsuffix)
        self.draw_ui_from_opv(ovp.com_bc_groupcolorsetsuffix)

        self.combake_colorset_ui_1 = cmds.columnLayout(adjustableColumn=True)
        cmds.setParent('..')

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.frameLayout(l=u'出力設定', cll=1, cl=0, bv=1, mw=10, mh=5)
        cmds.columnLayout(adjustableColumn=True)

        self.draw_ui_from_opv(ovp.com_bc_export_object_dir_path)
        self.draw_ui_from_opv(ovp.com_bc_export_texture_dir_path)

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.frameLayout(l=u'ブレンド設定', cll=1, cl=0, bv=1, mw=5, mh=5)
        cmds.columnLayout(adjustableColumn=True)

        self.draw_ui_from_opv(ovp.com_bc_light_enable)
        self.draw_ui_from_opv(ovp.com_bc_light_alpha)
        self.draw_ui_from_opv(ovp.com_bc_light_color_multi)
        self.draw_ui_from_opv(ovp.com_bc_light_color_offset)

        self.draw_ui_from_opv(ovp.com_bc_ao_enable)
        self.draw_ui_from_opv(ovp.com_bc_ao_alpha)
        self.draw_ui_from_opv(ovp.com_bc_ao_color_multi)
        self.draw_ui_from_opv(ovp.com_bc_ao_color_offset)

        self.draw_ui_from_opv(ovp.com_bc_indirect_enable)
        self.draw_ui_from_opv(ovp.com_bc_indirect_alpha)
        self.draw_ui_from_opv(ovp.com_bc_indirect_color_multi)
        self.draw_ui_from_opv(ovp.com_bc_indirect_color_offset)

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.frameLayout(l=u'Turtle共通ベイク設定',
                         cll=1, cl=0, bv=1, mw=10, mh=5)
        cmds.columnLayout(adjustableColumn=True)

        self.draw_ui_from_opv(ovp.ttl_bc_bakelayername)
        self.draw_ui_from_opv(ovp.ttl_bc_ao_sampler_name)

        self.draw_ui_from_opv(ovp.ttl_bc_orthreflect)
        self.draw_ui_from_opv(ovp.ttl_bc_bakeshadows)
        self.draw_ui_from_opv(ovp.ttl_bc_bgcolor)

        cmds.frameLayout(l=u'アンビエントオクルージョン設定',
                         cll=1, cl=0, bv=1, mw=10, mh=5)
        cmds.columnLayout(adjustableColumn=True)

        self.draw_ui_from_opv(ovp.ttl_bc_ao_mincolor)
        self.draw_ui_from_opv(ovp.ttl_bc_ao_maxcolor)
        self.draw_ui_from_opv(ovp.ttl_bc_ao_maxdistance)
        self.draw_ui_from_opv(ovp.ttl_bc_ao_contrast)
        self.draw_ui_from_opv(ovp.ttl_bc_ao_scale)
        self.draw_ui_from_opv(ovp.ttl_bc_ao_accuracy)
        self.draw_ui_from_opv(ovp.ttl_bc_ao_smooth)

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.setParent('..')
        cmds.setParent('..')

        self.texbake_frame_ui = cmds.frameLayout(
            l=u'テクスチャベイク設定', cll=1, cl=0, bv=1, mw=10, mh=5)
        cmds.columnLayout(adjustableColumn=True)

        cmds.frameLayout(l=u'出力設定', cll=1, cl=0, bv=1, mw=10, mh=5)
        cmds.columnLayout(adjustableColumn=True)

        self.texbake_output_ui_0 = cmds.columnLayout(adjustableColumn=True)
        cmds.setParent('..')

        self.draw_ui_from_opv(ovp.com_bt_width)
        self.draw_ui_from_opv(ovp.com_bt_height)
        self.draw_ui_from_opv(ovp.com_bt_testwidth)
        self.draw_ui_from_opv(ovp.com_bt_testheight)

        self.draw_ui_from_opv(ovp.com_bt_texouptputpath)

        self.draw_ui_from_opv(ovp.com_bt_textureprefix)
        self.draw_ui_from_opv(ovp.com_bt_settingtexturesuffix)
        self.draw_ui_from_opv(ovp.com_bt_grouptexturesuffix)

        self.draw_ui_from_opv(ovp.com_bt_materialsuffix)
        self.draw_ui_from_opv(ovp.com_bt_settingmaterialsuffix)
        self.draw_ui_from_opv(ovp.com_bt_groupmaterialsuffix)

        self.texbake_output_ui_1 = cmds.columnLayout(adjustableColumn=True)
        cmds.setParent('..')

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.frameLayout(l=u'ライトマップUV設定',
                         cll=1, cl=0, bv=1, mw=10, mh=5)
        cmds.columnLayout(adjustableColumn=True)

        self.texbake_lightmapuv_ui_0 = cmds.columnLayout(adjustableColumn=True)
        cmds.setParent('..')

        self.draw_ui_from_opv(ovp.com_bt_lightmapuv)
        self.draw_ui_from_opv(ovp.com_bt_customlightmapuv)
        self.draw_ui_from_opv(ovp.com_bt_unwrapuvmel)
        self.draw_ui_from_opv(ovp.com_bt_layoutuvmel)

        self.texbake_lightmapuv_ui_1 = cmds.columnLayout(adjustableColumn=True)
        cmds.setParent('..')

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.frameLayout(l=u'Turtleテクスチャベイク設定',
                         cll=1, cl=0, bv=1, mw=10, mh=5)
        cmds.columnLayout(adjustableColumn=True)

        self.draw_ui_from_opv(ovp.ttl_bt_bilinear)
        self.draw_ui_from_opv(ovp.ttl_bt_edgedilation)

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.setParent('..')
        cmds.setParent('..')

        self.vtxbake_frame_ui = cmds.frameLayout(
            l=u'頂点カラーベイク設定', cll=1, cl=0, bv=1, mw=10, mh=5)
        cmds.columnLayout(adjustableColumn=True)

        cmds.frameLayout(l=u'Turtle頂点カラーベイク設定',
                         cll=1, cl=0, bv=1, mw=10, mh=5)
        cmds.columnLayout(adjustableColumn=True)

        self.draw_ui_from_opv(ovp.ttl_bv_samplemode)
        self.draw_ui_from_opv(ovp.ttl_bv_minsample)
        self.draw_ui_from_opv(ovp.ttl_bv_maxsample)
        self.draw_ui_from_opv(ovp.ttl_bv_vtxbias)
        self.draw_ui_from_opv(ovp.ttl_bv_clamp)
        self.draw_ui_from_opv(ovp.ttl_bv_rgbscale)
        self.draw_ui_from_opv(ovp.ttl_bv_rgbmin)
        self.draw_ui_from_opv(ovp.ttl_bv_rgbmax)
        self.draw_ui_from_opv(ovp.ttl_bv_enablefilter)
        self.draw_ui_from_opv(ovp.ttl_bv_filtersize)
        self.draw_ui_from_opv(ovp.ttl_bv_filtershape)
        self.draw_ui_from_opv(ovp.ttl_bv_filterdeviation)

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.setParent('..')
        cmds.setParent('..')

        cmds.setParent('..')

    # ===========================================
    def update_ui(self):

        self.param_item_group.set_ui_from_attr()

        for key in self.key_list:
            self.update_ui_from_opv(key)

    # ===========================================
    def change_ui(self):

        for key in self.key_list:
            self.change_ui_from_opv(key)

    # ===========================================
    def update_attr_value(self):

        for key in self.key_list:
            self.__update_attr_from_opv(key)

    # ===========================================
    def add_item_from_opv(self, key):

        self.param_item_group.add_item(
            ovp.get_name(key + 1),
            ovp.get_type(key + 1),
            ovp.get_value(key + 1),
            ovp.get_ui_label(key + 1),
            ovp.get_ui_type(key + 1)
        )

        self.param_item_group.add_item(
            ovp.get_name(key),
            ovp.get_type(key),
            ovp.get_value(key),
            ovp.get_ui_label(key),
            ovp.get_ui_type(key)
        )

    # ===========================================
    def draw_ui_from_opv(self, key):

        cmds.columnLayout(self.ui_prefix + ovp.get_name(key) +
                          '_root', adjustableColumn=True)

        cmds.separator(height=5, style='in')

        if self.parent_param is not None:
            cmds.rowLayout(numberOfColumns=2, adj=2)
            self.param_item_group.draw_ui(ovp.get_name(key + 1))
            self.param_item_group.draw_ui(ovp.get_name(key))
            cmds.setParent('..')
        else:
            self.param_item_group.draw_ui(ovp.get_name(key))

        cmds.setParent('..')

    # ===========================================
    def visible_override_ui(self, key, visible):

        self.param_item_group.visible_ui(ovp.get_name(key + 1), visible)

    # ===========================================
    def visible_ui(self, key, visible):

        cmds.columnLayout(self.ui_prefix + ovp.get_name(key) +
                          '_root', e=True, vis=visible)

    # ===========================================
    def set_override(self, key, override):

        self.param_item_group.set_attr_value(ovp.get_name(key + 1), override)

    # ===========================================
    def set_attr_prefix(self, key, attr_prefix):

        self.param_item_group.get_param_item(
            ovp.get_name(key + 1)).set_attr_prefix(attr_prefix)
        self.param_item_group.get_param_item(
            ovp.get_name(key)).set_attr_prefix(attr_prefix)

    # ===========================================
    def set_attr_value(self, key, value):

        self.param_item_group.set_attr_value(ovp.get_name(key), value)

    # ===========================================
    def set_attr_value_once(self, key, value):

        set_default_value = False
        this_value = None

        if not self.param_item_group.exist_attr(ovp.get_name(key)):
            set_default_value = True
        else:
            this_value = self.param_item_group.get_attr_value(
                ovp.get_name(key))

        if this_value is None:
            set_default_value = True

        if this_value == '****':
            set_default_value = True

        if not set_default_value:
            return

        self.param_item_group.set_attr_value(ovp.get_name(key), value)

    # ===========================================
    def update_ui_from_opv(self, key):

        if not self.param_item_group.get_attr(ovp.get_name(key + 1)) and \
                self.parent_param is not None:

            self.param_item_group.enable_ui(ovp.get_name(key), False)

            this_parent_value = \
                self.parent_param.param_item_group.get_attr_value(
                    ovp.get_name(key))

            self.param_item_group.set_ui_from_custom_value(
                ovp.get_name(key), this_parent_value)

        else:

            self.param_item_group.enable_ui(ovp.get_name(key), True)

    # ===========================================
    def change_ui_from_opv(self, key):

        this_override = self.param_item_group.get_ui_value(
            ovp.get_name(key + 1))

        is_override = True
        if this_override is not None:

            if not this_override and self.parent_param is not None:

                this_parent_value = \
                    self.parent_param.param_item_group.get_attr_value(
                        ovp.get_name(key))

                self.param_item_group.set_ui_from_custom_value(
                    ovp.get_name(key), this_parent_value)

                is_override = False

            self.param_item_group.enable_ui(ovp.get_name(key), this_override)

        self.param_item_group.set_attr_from_ui(ovp.get_name(key + 1))
        self.param_item_group.set_attr_from_ui(ovp.get_name(key))

    # ===========================================
    def get_attr_value(self, key):

        if self.parent_param is None:
            return self.param_item_group.get_attr_value(ovp.get_name(key))

        if self.param_item_group.get_attr_value(ovp.get_name(key + 1)):
            return self.param_item_group.get_attr_value(ovp.get_name(key))

        this_parent_param = self.parent_param

        if this_parent_param.parent_param is None:
            return this_parent_param.param_item_group.get_attr_value(
                ovp.get_name(key))

        if this_parent_param.param_item_group.get_attr_value(
                ovp.get_name(key + 1)):
            return this_parent_param.param_item_group.get_attr_value(
                ovp.get_name(key))

        this_parent_param = this_parent_param.parent_param

        if this_parent_param.parent_param is None:
            return this_parent_param.param_item_group.get_attr_value(
                ovp.get_name(key))

        if this_parent_param.param_item_group.get_attr_value(
                ovp.get_name(key + 1)):
            return this_parent_param.param_item_group.get_attr_value(
                ovp.get_name(key))
