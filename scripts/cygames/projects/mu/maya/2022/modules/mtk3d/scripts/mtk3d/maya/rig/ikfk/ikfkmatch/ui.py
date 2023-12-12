# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel

import os

from collections import OrderedDict

# script source
from . import common as ikfk_common

dir = '{}'.format(os.path.split(os.path.abspath(__file__))[0])
dir_path = dir.replace('\\', '/')

dataFolder = '{}/data/'.format(dir_path)

default_ik_to_fk_import_file = '{0}ply00_000_iktofk.json'.format(dataFolder)
default_fk_to_ik_import_file = '{0}ply00_000_fktoik.json'.format(dataFolder)
default_ikfk_switch_import_file = '{0}ply00_000_ikfk_switch.json'.format(dataFolder)


class UI(object):
    def __init__(self, IK2FKMatch_match_import_file=default_ik_to_fk_import_file,
                 FK2IKMatch_match_import_file=default_fk_to_ik_import_file,
                 IKFKMatch_switch_import_file=default_ikfk_switch_import_file):
        self.MAIN_WINDOW = 'IKFK Match Tool'

        self.IK2FKMatch_match_import_file = IK2FKMatch_match_import_file
        self.FK2IKMatch_match_import_file = FK2IKMatch_match_import_file
        self.IKFKMatch_switch_import_file = IKFKMatch_switch_import_file

    def show(self):
        if cmds.workspaceControl(self.MAIN_WINDOW, q=1, ex=1):
            cmds.deleteUI(self.MAIN_WINDOW)

        win = cmds.workspaceControl(self.MAIN_WINDOW, l=self.MAIN_WINDOW)

        self.layout()

        cmds.showWindow(win)
        cmds.scriptJob(e=['SceneOpened', self.namespaces_optionMenu], p=win, rp=True)

    def layout(self):

        cmds.columnLayout(adj=1, rs=7)
        # namespace
        cmds.rowLayout(nc=3, ad3=1)
        self.namespaces_om = cmds.optionMenu(label='Namespace', w=100)
        self.namespaces_optionMenu()
        cmds.button(l='Refresh', c=self.namespaces_optionMenu)
        cmds.setParent('..')

        cmds.separator()

        cmds.text(l=u'マッチさせる部位を選択します', al='left', fn='fixedWidthFont')

        # checkBox
        cmds.rowLayout(nc=5, ad3=5)
        self.all_cb = cmds.checkBox(l='All', cc=self.all_check_change_command)
        self.arms_cb = cmds.checkBox(l='arms', cc=self.arms_check_change_command)
        self.legs_cb = cmds.checkBox(l='legs', cc=self.legs_check_change_command)
        self.left_cb = cmds.checkBox(l='Left', cc=self.left_check_change_command)
        self.right_cb = cmds.checkBox(l='Right', cc=self.right_check_change_command)
        cmds.setParent('..')

        cmds.rowLayout(nc=3, ad3=2)
        self.arms_L_cb = cmds.checkBox(l='arm L')
        self.arms_R_cb = cmds.checkBox(l='arm R')
        cmds.setParent('..')

        cmds.rowLayout(nc=3, ad3=2)
        self.legs_L_cb = cmds.checkBox(l='leg L')
        self.legs_R_cb = cmds.checkBox(l='leg R')
        cmds.setParent('..')

        cmds.rowLayout(nc=3, ad3=2)
        self.spines_cb = cmds.checkBox(l='spines')
        cmds.setParent('..')

        cmds.separator()

        cmds.text(l=u'マッチさせるオペレーションを選択します\n >>(convert to)', al='left', fn='fixedWidthFont')

        # radioButton
        self.operation_rbg = cmds.radioButtonGrp(l='Switch', la2=['IK >> FK', 'FK >> IK'], sl=0, nrb=2,
                                                 cw3=[70, 70, 30])

        cmds.separator()

        # PoleVector
        cmds.text(l=u'PoleVectorの位置を指定します', al='left', fn='fixedWidthFont')
        self.pv_move_fsg = cmds.floatSliderGrp(l='PoleVector Move', f=1, v=20, cw3=[90, 50, 30])
        cmds.separator()

        # button
        cmds.text(l=u'現在のフレームでマッチさせます', al='left', fn='fixedWidthFont')
        cmds.button(l='Match', c=self.do_match)

        cmds.separator()

        cmds.text(l=u'マッチベイクします\nPlaybackSliderにチェックを打つと\n選択されたタイムスライダの範囲でベイクされます', al='left', fn='fixedWidthFont')

        cmds.rowLayout(nc=3, ad3=2)
        self.playbackSlider_cb = cmds.checkBox(l='PlaybackSlider')
        cmds.button(l='Match Bake', c=self.do_bake)
        cmds.setParent('..')

        cmds.separator()

        cmds.text(l=u'IKFKスイッチの値に応じてマッチベイクされます', al='left', fn='fixedWidthFont')
        cmds.button(l='Full Match Bake', c=self.full_matchbake)

        cmds.setParent('..')  # columnLayout

    def all_check_change_command(self, *args, **kwargs):
        all_cb_var = cmds.checkBox(self.all_cb, q=1, v=1)

        alcb_v = cmds.checkBox(self.arms_L_cb, q=1, v=1)
        arcb_v = cmds.checkBox(self.arms_R_cb, q=1, v=1)
        llcb_v = cmds.checkBox(self.legs_L_cb, q=1, v=1)
        lrcb_v = cmds.checkBox(self.legs_R_cb, q=1, v=1)
        spines_v = cmds.checkBox(self.spines_cb, q=1, v=1)

        if all_cb_var:
            cmds.checkBox(self.arms_L_cb, e=1, v=1)
            cmds.checkBox(self.arms_R_cb, e=1, v=1)
            cmds.checkBox(self.legs_L_cb, e=1, v=1)
            cmds.checkBox(self.legs_R_cb, e=1, v=1)
            cmds.checkBox(self.spines_cb, e=1, v=1)

        else:
            cmds.checkBox(self.arms_L_cb, e=1, v=0)
            cmds.checkBox(self.arms_R_cb, e=1, v=0)
            cmds.checkBox(self.legs_L_cb, e=1, v=0)
            cmds.checkBox(self.legs_R_cb, e=1, v=0)
            cmds.checkBox(self.spines_cb, e=1, v=0)

    def arms_check_change_command(self, *args, **kwargs):
        arms_cb_var = cmds.checkBox(self.arms_cb, q=1, v=1)

        alcb_v = cmds.checkBox(self.arms_L_cb, q=1, v=1)
        arcb_v = cmds.checkBox(self.arms_R_cb, q=1, v=1)

        if arms_cb_var:
            cmds.checkBox(self.arms_L_cb, e=1, v=1)
            cmds.checkBox(self.arms_R_cb, e=1, v=1)

        else:
            cmds.checkBox(self.arms_L_cb, e=1, v=0)
            cmds.checkBox(self.arms_R_cb, e=1, v=0)

    def legs_check_change_command(self, *args, **kwargs):
        legs_cb_var = cmds.checkBox(self.legs_cb, q=1, v=1)

        llcb_v = cmds.checkBox(self.legs_L_cb, q=1, v=1)
        lrcb_v = cmds.checkBox(self.legs_R_cb, q=1, v=1)

        if legs_cb_var:
            cmds.checkBox(self.legs_L_cb, e=1, v=1)
            cmds.checkBox(self.legs_R_cb, e=1, v=1)
        else:
            cmds.checkBox(self.legs_L_cb, e=1, v=0)
            cmds.checkBox(self.legs_R_cb, e=1, v=0)

    def left_check_change_command(self, *args, **kwargs):
        left_cb_var = cmds.checkBox(self.left_cb, q=1, v=1)

        alcb_v = cmds.checkBox(self.arms_L_cb, q=1, v=1)
        llcb_v = cmds.checkBox(self.legs_L_cb, q=1, v=1)

        if left_cb_var:
            cmds.checkBox(self.arms_L_cb, e=1, v=1)
            cmds.checkBox(self.legs_L_cb, e=1, v=1)
        else:
            cmds.checkBox(self.arms_L_cb, e=1, v=0)
            cmds.checkBox(self.legs_L_cb, e=1, v=0)

    def right_check_change_command(self, *args, **kwargs):
        right_cb_var = cmds.checkBox(self.right_cb, q=1, v=1)

        arcb_v = cmds.checkBox(self.arms_R_cb, q=1, v=1)
        lrcb_v = cmds.checkBox(self.legs_R_cb, q=1, v=1)

        if right_cb_var:
            cmds.checkBox(self.arms_R_cb, e=1, v=1)
            cmds.checkBox(self.legs_R_cb, e=1, v=1)
        else:
            cmds.checkBox(self.arms_R_cb, e=1, v=0)
            cmds.checkBox(self.legs_R_cb, e=1, v=0)

    def get_namespaces(self, *args, **kwargs):
        return self.get_current_namespaces()

    def namespaces_optionMenu(self, *args, **kwargs):
        itemList = cmds.optionMenu(self.namespaces_om, q=1, ill=1)
        if itemList:
            [cmds.deleteUI(item) for item in itemList or []]
        nss = self.get_namespaces()
        if nss == '':
            cmds.menuItem(label=nss, p=self.namespaces_om)
        else:
            cmds.menuItem(label='', p=self.namespaces_om)
            for ns in nss:
                cmds.menuItem(label=ns, p=self.namespaces_om)

    def get_current_namespaces(self):
        exclude_list = ['UI', 'shared']

        current = cmds.namespaceInfo(cur=True)
        cmds.namespace(set=':')
        namespaces = ['{}'.format(ns) for ns in cmds.namespaceInfo(lon=True) if ns not in exclude_list]
        cmds.namespace(set=current)

        # Reference Nodes
        rn = cmds.ls(type="reference", r=1)
        for i in rn:
            ref_ns = i.split("RN")
            ns = '{0}'.format(ref_ns[0])
            if not ns in namespaces:
                namespaces.append(ns)

        if namespaces == []:
            namespaces = ''

        return namespaces

    def get_match_values(self, *args, **kwargs):
        match_settings = {}

        operation = cmds.radioButtonGrp(self.operation_rbg, q=1, sl=1)
        ns = cmds.optionMenu(self.namespaces_om, q=1, v=1)
        pv_move = cmds.floatSliderGrp(self.pv_move_fsg, q=1, v=1)
        playbackSlider_var = cmds.checkBox(self.playbackSlider_cb, q=1, v=1)

        alcb_v = cmds.checkBox(self.arms_L_cb, q=1, v=1)
        arcb_v = cmds.checkBox(self.arms_R_cb, q=1, v=1)
        llcb_v = cmds.checkBox(self.legs_L_cb, q=1, v=1)
        lrcb_v = cmds.checkBox(self.legs_R_cb, q=1, v=1)

        spines_v = cmds.checkBox(self.spines_cb, q=1, v=1)

        match_settings['operation'] = operation
        match_settings['namespace'] = ns
        match_settings['pvvalue'] = pv_move
        match_settings['playbackSlider'] = playbackSlider_var
        match_settings['types'] = [alcb_v, arcb_v, llcb_v, lrcb_v, spines_v]

        return match_settings

    def do_match(self, *args, **kwargs):
        sel = cmds.ls(os=1)
        self.match_bake_functions(match=True, bake=False)
        cmds.select(sel)

    def do_bake(self, *args, **kwargs):
        sel = cmds.ls(os=1)
        self.match_bake_functions(match=False, bake=True)
        cmds.select(sel)

    def full_matchbake(self, *args, **kwargs):
        match_values = self.get_match_values()
        ns = match_values['namespace']
        operation = match_values["operation"]
        alcb_v, arcb_v, llcb_v, lrcb_v, spines_v = match_values['types']

        cut_key_list = []
        if llcb_v:
            cut_key_list.append("L")
        else:
            pass
        if lrcb_v:
            cut_key_list.append("R")
        else:
            pass

        ik2fk_fk2ik = ikfk_common.IKFKMatchMan(import_fk_to_ik_setting=self.FK2IKMatch_match_import_file,
                                               import_ik_to_fk_setting=self.IK2FKMatch_match_import_file,
                                               import_switch_setting=self.IKFKMatch_switch_import_file,
                                               namespace=ns)

        if operation is 2:
            if cut_key_list:
                self.delete_reverse_foot_controls_keys(cut_key=True, cut_key_list=cut_key_list)
        sel = cmds.ls(os=1)
        ik2fk_fk2ik.main()
        cmds.select(sel)

    def delete_reverse_foot_controls_keys(self, cut_key, cut_key_list, attrs=None):
        if attrs is None:
            attrs = ["rx", "ry", "rz", "IKFK"]
        ns = cmds.optionMenu(self.namespaces_om, q=1, v=1)
        _controls = ["foot_{}_ik_ctrl_revFoot_ball_ctrl",
                     "foot_{}_ik_ctrl_revFoot_toe_ctrl",
                     "foot_{}_ik_ctrl_revFoot_heel_ctrl"]
        reverse_controls = []
        nums = len(cut_key_list)
        for i in range(nums):
            for ctrl in _controls:
                reverse_controls.append(ctrl.format(cut_key_list[i]))

        for obj in reverse_controls:
            for attr in attrs:
                if cut_key is True:
                    cmds.cutKey('{}:{}'.format(ns, obj), attribute=attr, option="keys", cl=True)
                    cmds.setAttr("{}:{}.{}".format(ns, obj, attr), 0)
                elif cut_key is False:
                    cmds.setAttr("{}:{}.{}".format(ns, obj, attr), 0)
                    cmds.setKeyframe("{}:{}".format(ns, obj), attribute=attr)

    def match_bake_functions(self, match=None, bake=None):
        match_values = self.get_match_values()

        operation = match_values['operation']
        ns = match_values['namespace']
        pv_move = match_values['pvvalue']
        playbackSlider_var = match_values['playbackSlider']
        alcb_v, arcb_v, llcb_v, lrcb_v, spines_v = match_values['types']

        # ik2fk
        if operation == 1:
            ik2fk = ikfk_common.IK2FKMatch()
            if self.IK2FKMatch_match_import_file:
                ik2fk.import_ik_to_fk_setting = self.IK2FKMatch_match_import_file
                ik2fk.call_import_ik_to_fk_setting()
            # namespace
            ik2fk.namespace = ns
            # pv
            ik2fk.pole_vector_pos = pv_move
            # spines
            if spines_v:
                print('spines')
                ik2fk.spines_match = 'IK2FK'
                ik2fk.spines_match_func()

            if playbackSlider_var:
                ik2fk.playbackSlider = True

            if alcb_v and not arcb_v and not llcb_v and not lrcb_v:
                print('arms_L')
                ik2fk.types = ['arms']
                ik2fk.left_enable = ['arms']

            elif arcb_v and not alcb_v and not llcb_v and not lrcb_v:
                print('arms_R')
                ik2fk.types = ['arms']
                ik2fk.right_enable = ['arms']

            elif alcb_v and arcb_v and not llcb_v and not lrcb_v:
                print('arms')
                ik2fk.types = ['arms']
                ik2fk.left_enable = ['arms']
                ik2fk.right_enable = ['arms']

            elif llcb_v and not alcb_v and not arcb_v and not lrcb_v:
                print('legs_L')
                ik2fk.types = ['legs']
                ik2fk.left_enable = ['legs']

            elif lrcb_v and not alcb_v and not arcb_v and not llcb_v:
                print('legs_R')
                ik2fk.types = ['legs']
                ik2fk.right_enable = ['legs']

            elif llcb_v and lrcb_v and not alcb_v and not arcb_v:
                print('legs')
                ik2fk.types = ['legs']
                ik2fk.left_enable = ['legs']
                ik2fk.right_enable = ['legs']

            elif alcb_v and llcb_v and not arcb_v and not lrcb_v:
                print('arms_L, legs_L')
                ik2fk.types = ['arms', 'legs']
                ik2fk.left_enable = ['arms', 'legs']

            elif arcb_v and lrcb_v and not alcb_v and not llcb_v:
                print('arms_R, legs_R')
                ik2fk.types = ['arms', 'legs']
                ik2fk.right_enable = ['arms', 'legs']

            elif alcb_v and lrcb_v and not arcb_v and not llcb_v:
                print('arms_L, legs_R')
                ik2fk.types = ['arms', 'legs']
                ik2fk.left_enable = ['arms']
                ik2fk.right_enable = ['legs']

            elif arcb_v and llcb_v and not alcb_v and not lrcb_v:
                print('arms_R, legs_L')
                ik2fk.types = ['arms', 'legs']
                ik2fk.left_enable = ['legs']
                ik2fk.right_enable = ['arms']

            elif arcb_v and llcb_v and lrcb_v and not alcb_v:
                print('arms_R, legs_L, legs_R')
                ik2fk.types = ['arms', 'legs']
                ik2fk.left_enable = ['legs']
                ik2fk.right_enable = ['arms', 'legs']

            elif alcb_v and llcb_v and lrcb_v and not arcb_v:
                print('arms_L, legs_L, legs_R')
                ik2fk.types = ['arms', 'legs']
                ik2fk.left_enable = ['arms', 'legs']
                ik2fk.right_enable = ['legs']

            elif alcb_v and arcb_v and lrcb_v and not llcb_v:
                print('arms_L, arms_R, legs_R')
                ik2fk.types = ['arms', 'legs']
                ik2fk.left_enable = ['arms']
                ik2fk.right_enable = ['arms', 'legs']

            elif alcb_v and arcb_v and llcb_v and not lrcb_v:
                print('arms_L, arms_R, legs_L')
                ik2fk.types = ['arms', 'legs']
                ik2fk.left_enable = ['arms', 'legs']
                ik2fk.right_enable = ['arms']

            elif alcb_v and arcb_v and llcb_v and lrcb_v:
                print('arms_L, arms_R, legs_L, legs_R')
                ik2fk.types = ['arms', 'legs']
                ik2fk.left_enable = ['arms', 'legs']
                ik2fk.right_enable = ['arms', 'legs']

            if match:
                ik2fk.match_func()
            elif bake:
                ik2fk.main()


        # fk2ik
        elif operation == 2:
            fk2ik = ikfk_common.FK2IKMatch()
            if self.FK2IKMatch_match_import_file:
                fk2ik.import_fk_to_ik_setting = self.FK2IKMatch_match_import_file
                fk2ik.call_import_fk_to_ik_setting()
            # namespace
            fk2ik.namespace = ns
            # pv
            fk2ik.pole_vector_pos = pv_move
            # spines
            if spines_v:
                print('spines')
                fk2ik.spines_match = 'FK2IK'
                fk2ik.spines_match_func()

            if playbackSlider_var:
                fk2ik.playbackSlider = True

            if alcb_v and not arcb_v and not llcb_v and not lrcb_v:
                print('arms_L')
                fk2ik.types = ['arms']
                fk2ik.left_enable = ['arms']

            elif arcb_v and not alcb_v and not llcb_v and not lrcb_v:
                print('arms_R')
                fk2ik.types = ['arms']
                fk2ik.right_enable = ['arms']

            elif alcb_v and arcb_v and not llcb_v and not lrcb_v:
                print('arms')
                fk2ik.types = ['arms']
                fk2ik.left_enable = ['arms']
                fk2ik.right_enable = ['arms']

            elif llcb_v and not alcb_v and not arcb_v and not lrcb_v:
                print('legs_L')
                fk2ik.types = ['legs']
                fk2ik.left_enable = ['legs']

            elif lrcb_v and not alcb_v and not arcb_v and not llcb_v:
                print('legs_R')
                fk2ik.types = ['legs']
                fk2ik.right_enable = ['legs']

            elif llcb_v and lrcb_v and not alcb_v and not arcb_v:
                print('legs')
                fk2ik.types = ['legs']
                fk2ik.left_enable = ['legs']
                fk2ik.right_enable = ['legs']

            elif alcb_v and llcb_v and not arcb_v and not lrcb_v:
                print('arms_L, legs_L')
                fk2ik.types = ['arms', 'legs']
                fk2ik.left_enable = ['arms', 'legs']

            elif arcb_v and lrcb_v and not alcb_v and not llcb_v:
                print('arms_R, legs_R')
                fk2ik.types = ['arms', 'legs']
                fk2ik.right_enable = ['arms', 'legs']

            elif alcb_v and lrcb_v and not arcb_v and not llcb_v:
                print('arms_L, legs_R')
                fk2ik.types = ['arms', 'legs']
                fk2ik.left_enable = ['arms']
                fk2ik.right_enable = ['legs']

            elif arcb_v and llcb_v and not alcb_v and not lrcb_v:
                print('arms_R, legs_L')
                fk2ik.types = ['arms', 'legs']
                fk2ik.left_enable = ['legs']
                fk2ik.right_enable = ['arms']

            elif arcb_v and llcb_v and lrcb_v and not alcb_v:
                print('arms_R, legs_L, legs_R')
                fk2ik.types = ['arms', 'legs']
                fk2ik.left_enable = ['legs']
                fk2ik.right_enable = ['arms', 'legs']

            elif alcb_v and llcb_v and lrcb_v and not arcb_v:
                print('arms_L, legs_L, legs_R')
                fk2ik.types = ['arms', 'legs']
                fk2ik.left_enable = ['arms', 'legs']
                fk2ik.right_enable = ['legs']

            elif alcb_v and arcb_v and lrcb_v and not llcb_v:
                print('arms_L, arms_R, legs_R')
                fk2ik.types = ['arms', 'legs']
                fk2ik.left_enable = ['arms']
                fk2ik.right_enable = ['arms', 'legs']

            elif alcb_v and arcb_v and llcb_v and not lrcb_v:
                print('arms_L, arms_R, legs_L')
                fk2ik.types = ['arms', 'legs']
                fk2ik.left_enable = ['arms', 'legs']
                fk2ik.right_enable = ['arms']

            elif alcb_v and arcb_v and llcb_v and lrcb_v:
                print('arms_L, arms_R, legs_L, legs_R')
                fk2ik.types = ['arms', 'legs']
                fk2ik.left_enable = ['arms', 'legs']
                fk2ik.right_enable = ['arms', 'legs']

            # Check where to switch
            cut_key_list = []
            try:
                if "legs" in fk2ik.left_enable:
                    cut_key_list.append("L")
            except ZeroDivisionError:
                pass

            try:
                if "legs" in fk2ik.right_enable:
                    cut_key_list.append("R")
            except ZeroDivisionError:
                pass

            if match:
                if cut_key_list:
                    self.delete_reverse_foot_controls_keys(cut_key=False, cut_key_list=cut_key_list)
                fk2ik.match_func()
            elif bake:
                if cut_key_list:
                    self.delete_reverse_foot_controls_keys(cut_key=True, cut_key_list=cut_key_list)
                fk2ik.main()


if __name__ == '__main__':
    ui = UI()
    ui.show()
