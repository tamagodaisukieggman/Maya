# -*- coding: utf-8 -*-
# ----------------------------------
# Project : Tsubasa
# Name    : tsubasaJointTools
# Author  : toi
# Update  : 2022/6/16
# ----------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import maya.cmds as cmds
import maya.mel as mm
import os
from functools import partial
from dccUserMayaSharePythonLib import common as cm
from attrWatcher import attrWatcher
import tsubasa.maya.rig.mergerotation as mergerotation


class JointTools(object):
    def __init__(self):
        self.window_name = os.path.basename(os.path.dirname(__file__))

    def delOverwrapWindow(self):
        if cmds.window(self.window_name, ex=True):
            cmds.deleteUI(self.window_name)

    def _frameLayout(self, *args, **kwrgs):
        cmds.setParent(self.top_cl)
        fl = cmds.frameLayout(bgc=(0.2, 0.2, 0.8), mw=2, mh=2, cll=True, *args, **kwrgs)
        cl = cmds.columnLayout(adj=True, co=['both', 2], bgc=[0.2, 0.2, 0.2])
        return fl, cl

    def _button(self, *args, **kwrgs):
        return cmds.button(bgc=[0.4, 0.4, 0.4], *args, **kwrgs)

    def _initUi(self):
        self.delOverwrapWindow()
        cmds.window(self.window_name, t=self.window_name, mb=True)
        cmds.menu(l='Help')
        cmds.menuItem(l='Tool help', c="os.startfile('https://wisdom.cygames.jp/x/sU7AEw')")
        self.top_cl = cmds.columnLayout(adj=True, co=['both', 2])

        self.cb_pc = cmds.checkBox(l='Preverse Children', cc=partial(self._pc_onoff))

        # -------------------------------
        self._frameLayout(l='Select')
        cmds.rowLayout(nc=2)
        self._button(l='All', w=150, c=partial(self._selAllJoint))
        self._button(l='Hierarchy', w=150, c=partial(self._selUnderHierarchy))

        # -------------------------------
        self._frameLayout(l='Delete all keys')
        cmds.rowLayout(nc=1)
        self._button(l='Delete', w=300, c=partial(self._deleteKey))

        # -------------------------------
        self._frameLayout(l='Preferred Angle')
        cmds.rowLayout(nc=2)
        self._button(l='Set', w=150, c=partial(self._preferredOnOff, 0))
        self._button(l='Assume', w=150, c=partial(self._preferredOnOff, 1))

        # -------------------------------
        self._frameLayout(l='SegmentScale')
        cmds.rowLayout(nc=2)
        self._button(l='On', w=150, c=partial(self._segmentScaleOnOff, 1))
        self._button(l='Off', w=150, c=partial(self._segmentScaleOnOff, 0))

        # -------------------------------
        self._frameLayout(l='Label')
        cmds.rowLayout(nc=2)
        self._button(l='Show', w=150, c=partial(self._showLabelOnOff, 1))
        self._button(l='Off', w=150, c=partial(self._showLabelOnOff, 0))

        # -------------------------------
        self._frameLayout(l='Axis')
        cmds.rowLayout(nc=2)
        self._button(l='Show', w=150, c=partial(self._showAxisOnOff, 1))
        self._button(l='Off', w=150, c=partial(self._showAxisOnOff, 0))

        # -------------------------------
        self._frameLayout(l='Joint Orient Check')
        cmds.rowLayout(nc=1)
        self._button(l='Check', w=300, c=partial(self._jointOrientCheck))

        # -------------------------------
        self._frameLayout(l='Add joint')
        cmds.rowLayout(nc=2)
        self._button(l='to Parent', w=150, c=partial(self._addJoint2Parent))
        self._button(l='to Child', w=150, c=partial(self._addJoint2Child))

        # -------------------------------
        self._frameLayout(l='Merge Rotation')
        cmds.rowLayout(nc=2)
        self._button(l='to Joint Orient', w=150, c=partial(self._mergeRotation, 'jointOrient'))
        self._button(l='to Rotate', w=150, c=partial(self._mergeRotation, 'rotate'))

        # -------------------------------
        _, cl = self._frameLayout(
            l='Aim to target',
            ann='ジョイントの向きをsrcの方向へ向ける（tgt, src, upv の順に3つ選択して実行 : 2つの場合upvはNone）')
        cmds.text(l='select : tgt > src > upv', al='left', h=22)

        cmds.setParent(cl)
        self.rc = cmds.radioCollection()
        cmds.rowLayout(nc=7)
        cmds.text(l='aim :   ')
        self.rb_x = cmds.radioButton(l='X', cl=self.rc, sl=True).split('|')[-1]
        self.rb_y = cmds.radioButton(l='Y', cl=self.rc).split('|')[-1]
        self.rb_z = cmds.radioButton(l='Z', cl=self.rc).split('|')[-1]
        self.rb_mx = cmds.radioButton(l='-X', cl=self.rc).split('|')[-1]
        self.rb_my = cmds.radioButton(l='-Y', cl=self.rc).split('|')[-1]
        self.rb_mz = cmds.radioButton(l='-Z', cl=self.rc).split('|')[-1]

        cmds.setParent(cl)
        self.rc_u = cmds.radioCollection()
        cmds.rowLayout(nc=7)
        cmds.text(l='upv :   ')
        self.rb_x_u = cmds.radioButton(l='X', cl=self.rc_u).split('|')[-1]
        self.rb_y_u = cmds.radioButton(l='Y', cl=self.rc_u, sl=True).split('|')[-1]
        self.rb_z_u = cmds.radioButton(l='Z', cl=self.rc_u).split('|')[-1]
        self.rb_mx_u = cmds.radioButton(l='-X', cl=self.rc_u).split('|')[-1]
        self.rb_my_u = cmds.radioButton(l='-Y', cl=self.rc_u).split('|')[-1]
        self.rb_mz_u = cmds.radioButton(l='-Z', cl=self.rc_u).split('|')[-1]

        #cmds.iconTextButton(w=26, i='gameFbxExporterHelp.png', st='iconOnly')
        cmds.setParent(cl)
        self._button(l='Apply', c=partial(self._aimToChild))

        # -------------------------------
        _, cl = self._frameLayout(l='Mirror joint')
        self.rc_mj = cmds.radioCollection()
        cmds.rowLayout(nc=3)
        cmds.text(l='mode :   ')
        self.rb_cre_mj = cmds.radioButton(l='Create', sl=True)
        self.rb_setval_mj = cmds.radioButton(l='Set value')

        cmds.setParent(cl)
        self.rc_mj = cmds.radioCollection()
        cmds.rowLayout(nc=4)
        cmds.text(l='mirror axis :   ')
        cmds.radioButton(l='X', sl=True).split('|')[-1]
        cmds.radioButton(l='Y').split('|')[-1]
        cmds.radioButton(l='Z').split('|')[-1]
        cmds.setParent(cl)

        self.rc_mj_fst = cmds.radioCollection()
        cmds.rowLayout(nc=4)
        cmds.text(l='first priority axis :   ')
        cmds.radioButton(l='X').split('|')[-1]
        cmds.radioButton(l='Y').split('|')[-1]
        cmds.radioButton(l='Z', sl=True).split('|')[-1]
        cmds.setParent(cl)

        self.rc_mj_scd = cmds.radioCollection()
        cmds.rowLayout(nc=4)
        cmds.text(l='second priority axis :   ')
        cmds.radioButton(l='X').split('|')[-1]
        cmds.radioButton(l='Y', sl=True).split('|')[-1]
        cmds.radioButton(l='Z').split('|')[-1]

        cmds.setParent(cl)
        self._button(l='Apply', c=partial(self.startMirrorJoint))

        # -------------------------------
        cmds.showWindow(self.window_name)

    @staticmethod
    def _getJoints():
        sels = cmds.ls(sl=True)
        if not sels:
            return cmds.ls(type='joint')
        else:
            joint_list = []
            for node in sels:
                if cmds.nodeType(node) == 'joint':
                    joint_list.append(node)
            return joint_list

    def _pc_onoff(self, *args):
         onoff = 'true' if cmds.checkBox(self.cb_pc, q=True, v=True) else 'false'
         mm.eval('setTRSPreserveChildPosition {0};'.format(onoff))

    def _selAllJoint(self, *args):
        joints = cmds.ls(type='joint')
        cmds.select(joints)

    def _selUnderHierarchy(self, *args):
        joints = cmds.ls(sl=True, dag=True, type='joint')
        cmds.select(joints)

    def _preferredOnOff(self, *args):
        joint_list = self._getJoints()
        if not joint_list:
            return

        if args[0]:
            cmds.joint('null', e=True, apa=True, ch=True)
        else:
            for node in joint_list:
                rot_val = cmds.getAttr(node + '.r')[0]
                cmds.setAttr(node + '.preferredAngle', rot_val[0], rot_val[1], rot_val[2], type='double3')

    def _jointOrientCheck(self, *args):
        sels = cmds.ls(sl=True)
        if not sels:
            return

        self._selUnderHierarchy(sels)
        aw = attrWatcher.Ui()
        aw.nodes = cmds.ls(sl=True)
        at_rl_list = aw.initAcg(['jointOrient'])
        for at, rl in at_rl_list:
            val = cmds.getAttr(at)[0]
            if val[0] != 0.0 or val[1] != 0.0 or val[2] != 0.0:
                cmds.rowLayout(rl, e=True, bgc=[1, 0, 0])

    def _addJoint2Parent(self, *args):
        sels = cmds.ls(sl=True)
        dupnodes = []
        for sel in sels:
            parent_ = cmds.listRelatives(sel, p=True)
            dupnode = cmds.duplicate(sel, parentOnly=True, inputConnections=False)
            cmds.parent(dupnode, w=True)
            dupnode = cmds.rename(dupnode, sel + '_parent')
            cmds.parent(dupnode, parent_[0])
            cmds.parent(sel, dupnode)
            mergerotation.merge_rotation(sel, 'rotate', 1)
            #cm.resetTransform(dupnode)
            dupnodes.append(dupnode)
        cmds.select(dupnodes)

    def _addJoint2Child(self, *args):
        sels = cmds.ls(sl=True)
        dupnodes = []
        for sel in sels:
            dupnode = cmds.duplicate(sel, parentOnly=True, inputConnections=False)
            dupnode = cmds.rename(dupnode, sel + '_child')
            cmds.parent(dupnode, sel)
            mergerotation.merge_rotation(dupnode, 'rotate', 1)
            cm.resetTransform(dupnode)
            dupnodes.append(dupnode)
        cmds.select(dupnodes)

    def _mergeRotation(self, *args):
        sels = cmds.ls(sl=True)
        mergerotation.merge_rotation(sels, args[0], 1)

    def _deleteKey(self, *args):
        joint_list = self._getJoints()
        for node in joint_list:
            cmds.cutKey(node)

    def _segmentScaleOnOff(self, *args):
        joint_list = self._getJoints()
        done_list = []
        for node in joint_list:
            if cmds.getAttr(node + '.segmentScaleCompensate') != args[0]:
                cmds.setAttr(node + '.segmentScaleCompensate', args[0])
                done_list.append(node)
        cm.hum('{0} joints done'.format(len(done_list)))

    def _showLabelOnOff(self, *args):
        joint_list = self._getJoints()
        done_list = []
        for node in joint_list:
            cmds.setAttr(node + '.drawLabel', args[0])
            done_list.append(node)
        cm.hum('{0} joints done'.format(len(done_list)))

    def _showAxisOnOff(self, *args):
        joint_list = self._getJoints()
        done_list = []
        for node in joint_list:
            cmds.setAttr(node + '.displayLocalAxis', args[0])
            done_list.append(node)
        cm.hum('{0} joints done'.format(len(done_list)))

    def _aimToChild(self, *args):
        sels = cmds.ls(sl=True)
        if not sels:
            return

        # aim ----------------
        aimval = 1
        axis = cmds.radioCollection(self.rc, q=True, sl=True)
        if axis == self.rb_mx or axis == self.rb_my or axis == self.rb_mz:
            aimval = -1

        aimvec = (0, 0, 0)
        if axis == self.rb_x or axis == self.rb_mx:
            aimvec = (aimval, 0, 0)
        elif axis == self.rb_y or axis == self.rb_my:
            aimvec = (0, aimval, 0)
        elif axis == self.rb_z or axis == self.rb_mz:
            aimvec = (0, 0, aimval)

        # upv ----------------
        upvval = 1
        axis_u = cmds.radioCollection(self.rc_u, q=True, sl=True)
        if axis_u == self.rb_mx_u or axis_u == self.rb_my_u or axis_u == self.rb_mz_u:
            upvval = -1

        upvvec = (0, 0, 0)
        if axis_u == self.rb_x_u or axis_u == self.rb_mx_u:
            print()
            upvvec = (upvval, 0, 0)
        elif axis_u == self.rb_y_u or axis_u == self.rb_my_u:
            upvvec = (0, upvval, 0)
        elif axis_u == self.rb_z_u or axis_u == self.rb_mz_u:
            upvvec = (0, 0, upvval)

        # ----------------
        if len(sels) == 3:
            tgt, src, upv = sels
            cm.aimToChild(tgt, src, upv, vec=[aimvec, upvvec])
            print(tgt, src, upv, aimvec, upvvec)
        else:
            tgt, src = sels
            cm.aimToChild(tgt, src, vec=[aimvec, upvvec])
            print(tgt, src, aimvec, upvvec)

        cmds.select(tgt)

    def startMirrorJoint(self, *args):
        sels = cmds.ls(sl=True)
        if not sels:
            return

        src = sels[0]
        if len(sels) == 1:
            tgt = cmds.duplicate(src, parentOnly=True, inputConnections=False)
            tgt = cmds.rename(tgt, src + '_mirror')
            try:
                cmds.parent(tgt, w=True)
            except:
                pass
            mergerotation.merge_rotation(tgt, 'rotate', 1)
        else:
            tgt = sels[1]

        mirror_axis = cmds.radioButton(cmds.radioCollection(self.rc_mj, q=True, sl=True), q=True, l=True)
        fst_priority_axis = cmds.radioButton(cmds.radioCollection(self.rc_mj_fst, q=True, sl=True), q=True, l=True)
        scd_priority_axis = cmds.radioButton(cmds.radioCollection(self.rc_mj_scd, q=True, sl=True), q=True, l=True)
        print(src, tgt, mirror_axis, fst_priority_axis, scd_priority_axis)
        self._mirrorJoint(src, tgt, mirror_axis, fst_priority_axis, scd_priority_axis)

    def _mirrorJoint(self, *args):
        src = args[0]
        tgt = args[1]
        mirror_axis = args[2]
        fst_priority_axis = args[3]
        scd_priority_axis = args[4]

        # ----------------
        tmp_aim_loc = cmds.spaceLocator(n='tmp_aim_loc')[0]
        tmp_upv_loc = cmds.spaceLocator(n='tmp_upv_loc')[0]
        cmds.parent(tmp_aim_loc, src)
        cmds.parent(tmp_upv_loc, src)
        cm.resetTransform(tmp_aim_loc)
        cm.resetTransform(tmp_upv_loc)

        wld_val = cmds.xform(src, q=True, t=True, ws=True)

        if mirror_axis == 'X':
            cmds.xform(tgt, t=(wld_val[0] * -1, wld_val[1], wld_val[2]), ws=True)
        elif mirror_axis == 'Y':
            cmds.xform(tgt, t=(wld_val[0], wld_val[1] * -1, wld_val[2]), ws=True)
        elif mirror_axis == 'Z':
            cmds.xform(tgt, t=(wld_val[0], wld_val[1], wld_val[2] * -1), ws=True)

        if fst_priority_axis == 'X':
            aim_axis = (1, 0, 0)
        elif fst_priority_axis == 'Y':
            aim_axis = (0, 1, 0)
        elif fst_priority_axis == 'Z':
            aim_axis = (0, 0, 1)

        if scd_priority_axis == 'X':
            upv_axis = (1, 0, 0)
        elif scd_priority_axis == 'Y':
            upv_axis = (0, 1, 0)
        elif scd_priority_axis == 'Z':
            upv_axis = (0, 0, 1)

        cmds.setAttr(tmp_aim_loc + '.t{0}'.format(fst_priority_axis.lower()), 50)
        cmds.parent(tmp_aim_loc, w=True)
        cmds.setAttr(
            tmp_aim_loc + '.t{0}'.format(mirror_axis.lower()),
            cmds.getAttr(tmp_aim_loc + '.t{0}'.format(mirror_axis.lower())) * -1
        )
        cmds.setAttr(tmp_upv_loc + '.t{0}'.format(scd_priority_axis.lower()), 50)
        cmds.parent(tmp_upv_loc, w=True)
        cmds.setAttr(
            tmp_upv_loc + '.t{0}'.format(mirror_axis.lower()),
            cmds.getAttr(tmp_upv_loc + '.t{0}'.format(mirror_axis.lower())) * -1
        )

        aim_c = cmds.aimConstraint(tmp_aim_loc, tgt, aim=aim_axis, u=upv_axis, wut='object', wuo=tmp_upv_loc)

        cmds.delete(tmp_aim_loc, tmp_upv_loc, aim_c)
        cmds.select(tgt)


def main():
    JointTools()._initUi()

