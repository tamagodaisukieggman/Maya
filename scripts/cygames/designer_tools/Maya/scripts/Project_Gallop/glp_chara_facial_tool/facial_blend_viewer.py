# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
    from builtins import range
    from builtins import object
    from importlib import reload
except Exception:
    pass

import maya.cmds as cmds

from . import target_info
from . import facial_combine

reload(target_info)
reload(facial_combine)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FacialBlendViewer(object):
    """
    表情のブレンドをMaya上で確認するビュワー
    """

    # ===============================================
    def __init__(self, parent_ui):

        self.target_info_csv_name = 'facial_target_info'
        self.controller_info_csv_name = 'facial_controller_info'

        self.parent_ui = parent_ui
        self.update_button = None

        self.target_info = None
        self.facial_combine = None
        self.blend_part_list = []

    # ===============================================
    def initialize(self):

        self.update_button = None

        self.target_info = None
        self.facial_combine = None
        self.blend_part_list = []

        self.target_info = target_info.TargetInfo()
        self.target_info.create_info_from_csv(self.target_info_csv_name, self.controller_info_csv_name)

        self.facial_combine = facial_combine.FacialCombine()
        self.facial_combine.initialize_only_parts_trs(self.target_info_csv_name, self.controller_info_csv_name)

        if not self.target_info.info_item_list:
            return

        eyebrow_l_label_list = []
        eyebrow_r_label_list = []
        eye_l_label_list = []
        eye_r_label_list = []
        mouth_label_list = []

        for info_item in self.target_info.info_item_list:

            target_list = None

            if info_item.part == 'Eyebrow_L':
                target_list = eyebrow_l_label_list
            elif info_item.part == 'Eyebrow_R':
                target_list = eyebrow_r_label_list
            elif info_item.part == 'Eye_L':
                target_list = eye_l_label_list
            elif info_item.part == 'Eye_R':
                target_list = eye_r_label_list
            elif info_item.part == 'Mouth':
                target_list = mouth_label_list
            else:
                continue

            if info_item.animation_layer_name:
                target_list.append(info_item.animation_layer_name)
            else:
                target_list.append(info_item.label)

        eyebrow_l_part = BlendPartViewer(self)
        eyebrow_r_part = BlendPartViewer(self)
        eye_l_part = BlendPartViewer(self)
        eye_r_part = BlendPartViewer(self)
        mouth_part = BlendPartViewer(self)

        eyebrow_l_part.initialize('eyebrow_l', eyebrow_l_label_list)
        eyebrow_r_part.initialize('eyebrow_r', eyebrow_r_label_list)
        eye_l_part.initialize('eye_l', eye_l_label_list)
        eye_r_part.initialize('eye_r', eye_r_label_list)
        mouth_part.initialize('mouth', mouth_label_list)

        self.blend_part_list = [
            eyebrow_l_part,
            eyebrow_r_part,
            eye_l_part,
            eye_r_part,
            mouth_part,
        ]

    # ===============================================
    def create_ui(self):

        cmds.setParent(self.parent_ui)

        self.update_button = cmds.button(label=u'表情ブレンドを再読み込み', c=self.__reboot_ui)

        if not self.blend_part_list:
            return

        for blend_part in self.blend_part_list:
            blend_part.create_ui()

    # ===============================================
    def __reboot_ui(self, arg):

        cmds.deleteUI(self.update_button, ctl=True)
        for blend_part in self.blend_part_list:
            cmds.deleteUI(blend_part.parent_layout, lay=True)

        self.initialize()
        self.create_ui()
        self.call_when_ui_update()

    # ===============================================
    def call_when_ui_update(self):

        face_blend_info_dict = self.__create_face_blend_info_dict()
        self.facial_combine.apply_blend_face([face_blend_info_dict])

    # ===============================================
    def __create_face_blend_info_dict(self):

        if not self.blend_part_list:
            return {}

        parts_dict = {}

        for blend_part in self.blend_part_list:

            blend_dict = {}

            for blend_item in blend_part.item_list:
                blend_dict[blend_item.current_menu] = blend_item.current_value

            parts_dict[blend_part.part] = blend_dict

        face_type_info_dict_list = {
            'label': 'user_blend_facial',
            'parts': parts_dict,
            'group': 0,
        }

        return face_type_info_dict_list


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BlendPartViewer(object):
    """
    
    """

    # ===============================================
    def __init__(self, root):

        self.root = root
        self.parent_layout = None

        self.slider_num = 3

        self.part = ''
        self.label_list = []
        self.anm_layer_list = []

        self.item_list = []

    # ===============================================
    def initialize(self, part, label_list):

        self.part = part
        self.label_list = label_list
        self.item_list = []

        self.parent_layout = None

        for item_num in range(self.slider_num):

            this_item = BlendPartItem(self)
            this_item.initialize(self.part, self.label_list)
            self.item_list.append(this_item)

    # ===============================================
    def create_ui(self):

        if not self.item_list:
            return

        self.parent_layout = cmds.columnLayout(adj=True, rs=4)
        cmds.frameLayout(label=self.part, cll=True, bv=True, cl=True, mw=10, mh=10, bgc=[0.3, 0.4, 0.5])
        cmds.columnLayout(adj=True, rs=4)

        for item in self.item_list:
            item.create_ui()

        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')

    # ===============================================
    def call_when_ui_update(self):

        self.root.call_when_ui_update()


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BlendPartItem(object):
    """

    """

    # ===============================================
    def __init__(self, root):

        self.root = root

        self.label = ''
        self.pull_down_list = []

        self.current_menu = ''
        self.current_value = 0.0

        self.pull_down_ui = None
        self.slider_ui = None
        self.edit_value_ui = None

    # ===============================================
    def initialize(self, label, pull_down_list):

        self.label = label
        self.pull_down_list = []
        self.pull_down_ui = None
        self.slider_ui = None
        self.edit_value_ui = None

        if pull_down_list:
            self.pull_down_list = pull_down_list
            self.current_menu = self.pull_down_list[0]

        self.current_value = 1.0

    # ===============================================
    def create_ui(self):

        slider_width = 270
        text_width = 90

        cmds.rowLayout(nc=3)

        self.pull_down_ui = cmds.optionMenu(
            label=self.label,
            width=text_width * 2,
            cc=self.__call_when_ui_update,
        )
        for item in self.pull_down_list:
            cmds.menuItem(label=item)

        self.slider_ui = cmds.floatSlider(
            min=0,
            max=1.0,
            value=1.0,
            step=0.001,
            width=slider_width,
            dc=self.__call_when_slider_update,
        )

        self.edit_value_ui = cmds.textField(
            text=str(self.current_value),
            width=text_width,
            changeCommand=self.__call_when_text_update)

        cmds.setParent('..')

    # ===============================================
    def __call_when_slider_update(self, arg):

        slider_value = cmds.floatSlider(self.slider_ui, q=True, v=True)
        cmds.textField(self.edit_value_ui, e=True, text=str(slider_value))
        self.__call_when_ui_update(None)

    # ===============================================
    def __call_when_text_update(self, arg):

        text = cmds.textField(self.edit_value_ui, q=True, text=True)
        value = 1.0

        try:
            value = float(text)
        except:
            pass

        cmds.floatSlider(self.slider_ui, e=True, v=value)
        self.__call_when_ui_update(None)

    # ===============================================
    def __call_when_ui_update(self, arg):

        self.current_menu = cmds.optionMenu(self.pull_down_ui, q=True, v=True)
        self.current_value = cmds.floatSlider(self.slider_ui, q=True, v=True)
        self.root.call_when_ui_update()
