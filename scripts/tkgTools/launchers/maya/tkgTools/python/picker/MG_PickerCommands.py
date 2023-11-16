# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel

import traceback

DEFAULT_CTRL_SPACES = {
    'Cog_ctrl.space':'main',
    'ik_Ankle_L_ctrl.space':'main',
    'ik_Ankle_R_ctrl.space':'main',
    'ik_Knee_L_ctrl.space':'main',
    'ik_Knee_R_ctrl.space':'main',
    'ik_Wrist_L_ctrl.space':'main',
    'ik_Wrist_R_ctrl.space':'main',
    'ik_Elbow_L_ctrl.space':'main',
    'ik_Elbow_R_ctrl.space':'main',

    'Neck_ctrl.space':'spine',

    'Handattach_L_ctrl.space':'wrist',
    'Handattach_R_ctrl.space':'wrist',

    'ik_Wrist_L_ctrl.autoRot':1,
    'ik_Wrist_R_ctrl.autoRot':1
}

IK_AUTO_ROT_CTRLS = {
    'Wrist_L':'ik_rot_Wrist_L_ctrl',
    'Wrist_R':'ik_rot_Wrist_R_ctrl'
}

def order_dags(dags=None):
    parent_dag = cmds.ls(dags[0], l=1, type='transform')[0].split('|')[1]

    all_hir = cmds.listRelatives(parent_dag, ad=True, f=True)
    hir_split_counter = {}
    parent_node = '|' + parent_dag
    hir_split_counter[parent_node] = len(parent_node.split('|'))
    for fp_node in all_hir:
        hir_split_counter[fp_node] = len(fp_node.split('|'))

    hir_split_counter_sorted = sorted(hir_split_counter.items(), key=lambda x:x[1])

    sorted_joint_list = [dag_count[0] for dag_count in hir_split_counter_sorted]

    all_ordered_dags = cmds.ls(sorted_joint_list)
    return [dag for dag in all_ordered_dags if dag in dags]

def set_enum_attr(ctrl=None, attr=None, val=None, rot_ctrl=None):
    wt = cmds.xform(ctrl, q=True, t=True, ws=True)
    if rot_ctrl:
        wr = cmds.xform(rot_ctrl, q=True, ro=True, ws=True)
    else:
        wr = cmds.xform(ctrl, q=True, ro=True, ws=True)

    list_attrs = cmds.listAttr(ctrl, ud=True, k=True) or list()

    if attr in list_attrs:
        get_en_attrs = cmds.addAttr(ctrl + '.' + attr, q=True, en=True)
        spl_get_en_attrs = get_en_attrs.split(':')
        if val in spl_get_en_attrs:
            enum_idx = spl_get_en_attrs.index(val)
            cmds.setAttr(ctrl+'.'+attr, enum_idx)

        cmds.xform(ctrl, t=wt, ro=wr, ws=True, a=True, p=True)
        if rot_ctrl:
            cmds.xform(rot_ctrl, ro=wr, ws=True, a=True, p=True)

class MGP:
    def __init__(self):
        self.cur_mgp_btn = None
        self.mgp_btn_members = []

    def get_current_picker_items(self):
        self.cur_mgp_btn = cmds.MGPicker(q=True, currentItem=True)
        self.mgp_btn_members = cmds.MGPickerItem(self.cur_mgp_btn, q=True, selectMembers=True)


class Namespace:
    def __init__(self):
        self.cur_nss = None

        try:
            self.get_current_picker_namespace()
        except:
            print(traceback.format_exc())

    def get_current_picker_namespace(self):
        self.cur_nss = mel.eval('MGP_GetCurrentPickerNamespace')

        if self.cur_nss:
            self.cur_nss = self.cur_nss + ':'
        else:
            self.cur_nss = ''

    def set_namespace_via_selection(self):
        sel = cmds.ls(os=True)
        if sel:
            mel.eval("MGP_SetPickerNamespace_Via_Selection;")
        else:
            cmds.MGPickerView(e=1, namespace='')


class Ctrl(Namespace, MGP):
    def __init__(self, prefix=None, suffix=None, cur_nss=None):
        # Namespace Activate
        self.get_current_picker_namespace()

        self.prefix = prefix
        self.suffix = suffix

        self.all_ctrls = []

        self.get_ctrls()

    def get_ctrls(self):
        all_suffix_ctrls = cmds.ls('{}*{}'.format(self.cur_nss, self.suffix))
        all_prefix_ctrls = cmds.ls('{}{}*'.format(self.cur_nss, self.prefix))

        if all_suffix_ctrls: [self.all_ctrls.append(n) for n in all_suffix_ctrls]
        if all_prefix_ctrls: [self.all_ctrls.append(n) for n in all_prefix_ctrls]

        self.all_ctrls.sort()
        self.all_ctrls = order_dags(self.all_ctrls)

    def zero_out(self):
        for ctrl in self.all_ctrls:
            try:
                cmds.xform(ctrl, t=[0,0,0], ro=[0,0,0], s=[1,1,1])
            except:
                print(traceback.format_exc())

    def reset_spaces(self):
        for ctrl_at, sp_at in DEFAULT_CTRL_SPACES.items():
            if type(sp_at) == str:
                get_en_attrs = cmds.addAttr(self.cur_nss + ctrl_at, q=True, en=True)
                spl_get_en_attrs = get_en_attrs.split(':')
                if sp_at in spl_get_en_attrs:
                    enum_idx = spl_get_en_attrs.index(sp_at)
                    cmds.setAttr(self.cur_nss + ctrl_at, enum_idx)

            elif type(sp_at) == int:
                cmds.setAttr(self.cur_nss + ctrl_at, sp_at)

    def space_match(self, attr=None, val=None, auto_side=None):
        self.get_current_picker_items()
        rot_ctrl = self.cur_nss + IK_AUTO_ROT_CTRLS[auto_side]
        [set_enum_attr(ctrl=ctrl, attr=attr, val=val, rot_ctrl=rot_ctrl) for ctrl in self.mgp_btn_members]


ctrl = Ctrl(prefix=None, suffix='_ctrl')
ctrl.reset_spaces()


print(ctrl.all_ctrls)

mel.eval('MGP_GetCurrentPickerNamespace')
