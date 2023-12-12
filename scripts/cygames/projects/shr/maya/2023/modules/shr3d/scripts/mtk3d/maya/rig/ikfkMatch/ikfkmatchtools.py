# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
from collections import OrderedDict

# script source
try:
    import mtk3d.maya.rig.ikfkMatch.ikfkmatch as ikfkmatch
    print('mtk3d.maya.rig.ikfkMatch.ikfkmatch as ikfkmatch')
except:
    import ikfkmatch
    print('ikfkmatch')
else:
    reload(ikfkmatch)

reload(ikfkmatch)

class UI(object):
    def __init__(self, cmd=0, fk_or_ik_list=None, tags=None, pv_move=None, namespace=None):
        self.MAIN_WINDOW = 'IKFK Match Tool'

        self.fk_or_ik_list = fk_or_ik_list
        self.tags = tags
        self.time_range = None
        self.playbackSlider = None
        self.pv_move = pv_move
        self.ns = namespace
        self.cmd = cmd

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

        # checkBox
        cmds.rowLayout(nc=3, ad3=2)
        self.arms_L_cb = cmds.checkBox(l='arm L')
        self.arms_R_cb = cmds.checkBox(l='arm R')
        cmds.setParent('..')

        cmds.rowLayout(nc=3, ad3=2)
        self.legs_L_cb = cmds.checkBox(l='leg L')
        self.legs_R_cb = cmds.checkBox(l='leg R')
        cmds.setParent('..')

        cmds.separator()

        # radioButton
        self.operation_rbg = cmds.radioButtonGrp(l='Switch', la2=['IK', 'FK'], sl=0, nrb=2, cw3=[70, 30, 30])

        cmds.separator()

        # PoleVector
        self.pv_move_fsg = cmds.floatSliderGrp(l='PoleVector Move', f=1, v=20, cw3=[90, 50, 30])
        cmds.separator()

        # button
        cmds.rowLayout(nc=3, ad3=2)
        self.cur_check_cb = cmds.checkBox(l='Current Switch')
        cmds.button(l='Match', c=self.match)
        cmds.setParent('..')
        cmds.button(l='Match Bake', c=self.matchbake)

    def get_namespaces(self, *args, **kwargs):
        return ikfkmatch.get_current_namespaces()

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

    def get_match_values(self, *args, **kwargs):
        operation = cmds.radioButtonGrp(self.operation_rbg, q=1, sl=1)
        self.ns = cmds.optionMenu(self.namespaces_om, q=1, v=1)
        self.pv_move = cmds.floatSliderGrp(self.pv_move_fsg, q=1, v=1)

        # bakestatus
        self.tags = []
        self.fk_or_ik_list = []

        self.alcb_v = cmds.checkBox(self.arms_L_cb, q=1, v=1)
        self.arcb_v = cmds.checkBox(self.arms_R_cb, q=1, v=1)
        self.llcb_v = cmds.checkBox(self.legs_L_cb, q=1, v=1)
        self.lrcb_v = cmds.checkBox(self.legs_R_cb, q=1, v=1)

        # arms_L
        if self.alcb_v == 1:
            self.tags.append('arms_L_')
            if operation == 1:
                self.fk_or_ik_list.append('ik')
            else:
                self.fk_or_ik_list.append('fk')

        # arms_R
        if self.arcb_v == 1:
            self.tags.append('arms_R_')
            if operation == 1:
                self.fk_or_ik_list.append('ik')
            else:
                self.fk_or_ik_list.append('fk')

        # legs_L
        if self.llcb_v == 1:
            self.tags.append('legs_L_')
            if operation == 1:
                self.fk_or_ik_list.append('ik')
            else:
                self.fk_or_ik_list.append('fk')

        # legs_R
        if self.lrcb_v == 1:
            self.tags.append('legs_R_')
            if operation == 1:
                self.fk_or_ik_list.append('ik')
            else:
                self.fk_or_ik_list.append('fk')

    def match(self, *args, **kwargs):
        sel = cmds.ls(os=1)
        self.get_match_values()
        self.cur_check_v = cmds.checkBox(self.cur_check_cb, q=1, v=1)
        for i, (tag, fk_or_ik) in enumerate(zip(self.tags, self.fk_or_ik_list)):
            if fk_or_ik == 'fk':
                ikfkmatch.fk2ik(tag=tag, fk2ik_sets='fk2ik_sets', namespace=self.ns)
            elif fk_or_ik == 'ik':
                ikfkmatch.ik2fk(tag=tag, ik2fk_sets='ik2fk_sets', pv_move=self.pv_move, namespace=self.ns)
        cmds.select(sel, r=1)

        if self.cur_check_v:
            self.operation_v = cmds.radioButtonGrp(self.operation_rbg, q=1, sl=1)
            if self.operation_v == 1:
                cmds.radioButtonGrp(self.operation_rbg, e=1, sl=2)
            elif self.operation_v == 2:
                cmds.radioButtonGrp(self.operation_rbg, e=1, sl=1)

    def matchbake(self, *args, **kwargs):
        sel = cmds.ls(os=1)
        if self.cmd == 0:
            self.get_match_values()
            self.playbackSlider = True
        elif self.cmd == 1:
            pass
        try:
            cmds.refresh(su=1)
            ikfkmatch.matchbake(fk_or_ik_list=self.fk_or_ik_list,
                                tags=self.tags,
                                time_range=self.time_range,
                                playbackSlider=self.playbackSlider,
                                pv_move=self.pv_move,
                                namespace=self.ns)

            cmds.refresh(su=0)
        except Exception as e:
            print(e)
            cmds.refresh(su=0)
        else:
            print('IKFK Match Bake!')

        cmds.select(sel, r=1)


if __name__ == '__main__':
    ui = UI()
    ui.show()
