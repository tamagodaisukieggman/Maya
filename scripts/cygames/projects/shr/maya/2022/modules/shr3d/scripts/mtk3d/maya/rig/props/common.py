# -*- coding: utf-8 -*-
from maya import cmds, mel
from maya import OpenMayaUI as omui

from PySide2 import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance

class PropSpace(object):

    # mtk template
    piv_obj = 'hand01_L_mtp_ctrl'
    piv_hand_obj = 'hand_L_ikRot_ctrl_ikRot_ctrl'
    rot_obj = 'hand_R_ikRot_ctrl_ikRot_ctrl'
    hand01_R_mtp_ctrl = 'hand01_R_mtp_ctrl'

    def __init__(self):
        self.bake_objs = []
        self.bake_consts = []
        self.ik_match_obj = []
        self.parentConst_piv_hand_obj = False
        self.namespace = ''
        self.sword_enable = None
        self.space_loc = None

    def main(self, mtk=True):
        cmds.undoInfo(openChunk=True)
        cmds.refresh(su=1)
        try:
            if mtk:
                self.ply00_mtk_bakes()

            cmds.refresh(su=0)
        except:
            cmds.refresh(su=0)
            return
        cmds.undoInfo(closeChunk=True)

    def ply00_mtk_bakes(self):
        ps_loc_rot, ps_loc_space_rot = self.create_loc('{0}{1}'.format(self.namespace, self.rot_obj))
        if self.sword_enable:
            ps_loc_piv, ps_loc_space_piv = self.create_loc(self.piv_obj)
        else:
            ps_loc_piv, ps_loc_space_piv = self.create_loc('{0}{1}'.format(self.namespace, self.piv_obj))

        self.bakes()
        self.create_ikHandle()

        cmds.parent(self.ikHandle_space, ps_loc_piv)
        cmds.pointConstraint('{0}{1}'.format(self.namespace, self.rot_obj), self.rot_j)
        cmds.orientConstraint(self.rot_j, '{0}{1}'.format(self.namespace, self.rot_obj))
        if self.parentConst_piv_hand_obj:
            cmds.parentConstraint('{0}{1}'.format(self.namespace, self.piv_hand_obj), self.ikHandle_space, mo=1, w=1)

        prop_space_grp = 'prop_space_grp'
        if not cmds.objExists(prop_space_grp):
            cmds.createNode('transform', n=prop_space_grp, ss=1)

        # cmds.parent(ps_loc_space_rot, prop_space_grp)
        cmds.delete(ps_loc_space_rot)
        cmds.parent(ps_loc_space_piv, prop_space_grp)
        cmds.parent(self.rot_j, prop_space_grp)

        prop_space_set = 'prop_space_set'
        if not cmds.objExists(prop_space_set):
            cmds.sets(em=1, n=prop_space_set)

        cmds.sets(self.ikHandle_loc[0], add=prop_space_set)

        prop_space_bake_set = 'prop_space_bake_set'
        if not cmds.objExists(prop_space_bake_set):
            cmds.sets(em=1, n=prop_space_bake_set)

        cmds.sets('{0}{1}'.format(self.namespace, self.rot_obj), add=prop_space_bake_set)
        cmds.sets(prop_space_bake_set, add=prop_space_set)


    def ply00_mtk_bakes_v2(self):
        # mtp対応
        if cmds.objExists('prop_space_set'):
            cmds.delete('prop_space_set')
        if cmds.objExists('prop_space_grp'):
            cmds.delete('prop_space_grp')
        if cmds.objExists('prop_space_bake_set'):
            cmds.delete('prop_space_bake_set')

        self.ikHandle_loc = []
        def create_space(obj):
            prop_space = cmds.createNode('transform', n='{0}_ps_space'.format(obj), ss=1)
            prop_loc = cmds.spaceLocator(n='{0}_ps_loc'.format(obj))[0]
            prop_aim_loc = cmds.spaceLocator(n='{0}_ps_aim_loc'.format(obj))[0]
            prop_aimbase_loc = cmds.spaceLocator(n='{0}_ps_aimbase_loc'.format(obj))[0]
            cmds.parent(prop_loc, prop_space)
            cmds.parent(prop_aimbase_loc, prop_space)
            cmds.parent(prop_aim_loc, prop_aimbase_loc)
            cmds.parentConstraint('{0}'.format(obj), prop_space, w=1)

            return prop_space, prop_loc, prop_aim_loc, prop_aimbase_loc


        def bake(objects):
            try:
                cmds.refresh(su=1)
                curTime = cmds.currentTime(q=1)
                cmds.currentTime(cmds.playbackOptions(q=1, min=1))

                cmds.bakeResults(objects,
                         sparseAnimCurveBake=False,
                         minimizeRotation=False,
                         removeBakedAttributeFromLayer=False,
                         removeBakedAnimFromLayer=False,
                         oversamplingRate=1,
                         bakeOnOverrideLayer=False,
                         preserveOutsideKeys=True,
                         simulation=True,
                         sampleBy=1,
                         shape=False,
                         t=(cmds.playbackOptions(q=1, min=1), cmds.playbackOptions(q=1, max=1)),
                         disableImplicitControl=True,
                         controlPoints=False,
                         at=[u'tx', u'ty', u'tz', u'rx', u'ry', u'rz', u'sx', u'sy', u'sz'])

                cmds.currentTime(curTime)
                cmds.refresh(su=0)
            except:
                cmds.refresh(su=0)


        loc_spaces = []
        locs = []
        loc_aims = []
        loc_aimbases = []
        pos_hand_r = self.namespace +'hand_R_ik_ctrl'
        sel = ['{0}{1}'.format(self.namespace, self.rot_obj),
         '{0}{1}'.format(self.namespace, self.hand01_R_mtp_ctrl),
         self.space_loc]
        for i, obj in enumerate(sel):
            prop_space, prop_loc, prop_aim_loc, prop_aimbase_loc = create_space(obj)
            loc_spaces.append(prop_space)
            locs.append(prop_loc)
            loc_aims.append(prop_aim_loc)
            loc_aimbases.append(prop_aimbase_loc)
            if i == 0:
                pass
            else:
                cmds.parent(loc_spaces[i], loc_spaces[i-1])

        # bake

        bake(loc_spaces)

        # hand ik
        hand_r_jnt = cmds.createNode('joint', n='hand_R_ikRot_con_jnt', ss=1)
        cmds.matchTransform(hand_r_jnt, loc_spaces[0])
        cmds.parent(hand_r_jnt, loc_spaces[0])
        cmds.makeIdentity(hand_r_jnt, n=0, s=0, r=1, t=0, apply=True, pn=1)
        hand_r_jnt_dup = cmds.duplicate(hand_r_jnt, po=1)
        cmds.parent(hand_r_jnt_dup, hand_r_jnt)
        cmds.xform(hand_r_jnt_dup, t=[-120, 0, 0], a=1)
        hand_r_ikh = cmds.ikHandle(sj=hand_r_jnt, ee=hand_r_jnt_dup[0])

        # mtp ik
        mtp_r_jnt = cmds.createNode('joint', n='mtp_R_con_jnt', ss=1)
        cmds.matchTransform(mtp_r_jnt, loc_spaces[1])
        cmds.parent(mtp_r_jnt, loc_spaces[1])
        cmds.makeIdentity(mtp_r_jnt, n=0, s=0, r=1, t=0, apply=True, pn=1)
        mtp_r_jnt_dup = cmds.duplicate(mtp_r_jnt, po=1)
        cmds.parent(mtp_r_jnt_dup, mtp_r_jnt)
        cmds.matchTransform(mtp_r_jnt_dup[0], loc_spaces[2])
        mtp_r_ikh = cmds.ikHandle(sj=mtp_r_jnt, ee=mtp_r_jnt_dup[0])


        cmds.parent(loc_aims[0], loc_aims[1], loc_aimbases[1], w=1)

        loc_aimbases_dup = loc_aimbases[1]+'dup'
        cmds.duplicate(loc_aimbases[1], n=loc_aimbases_dup)

        loc_aimbases_dupaim = loc_aimbases[1]+'dupaim'
        cmds.duplicate(loc_aimbases[1], n=loc_aimbases_dupaim)

        cmds.parent(loc_aimbases_dup, loc_aimbases[1])
        cmds.parent(loc_aimbases_dupaim, loc_aimbases[1])
        cmds.parent(loc_aims[1], loc_aimbases_dup)
        cmds.parent(loc_aims[0], loc_aims[1])


        cmds.parentConstraint(loc_spaces[1], loc_aimbases[1], w=1)
        cmds.parentConstraint(hand_r_jnt_dup[0], loc_aims[0], w=1)
        cmds.parentConstraint(mtp_r_jnt_dup[0], loc_aims[1], w=1)


        mtp_point_loc = locs[1]+'dup'
        cmds.duplicate(locs[1], n=mtp_point_loc)
        cmds.parent(mtp_point_loc, locs[0])
        cmds.parentConstraint(sel[1], mtp_point_loc, w=1, mo=1)

        # polevector Offset
        hand_r_ikh_ofst1 = cmds.createNode('transform', n=hand_r_ikh[0]+'_ofst_01', ss=1)
        hand_r_ikh_ofst2 = cmds.createNode('transform', n=hand_r_ikh[0]+'_ofst_02', ss=1)
        cmds.parent(hand_r_ikh_ofst2, hand_r_ikh_ofst1)
        cmds.matchTransform(hand_r_ikh_ofst1, hand_r_ikh[0])
        cmds.parent(hand_r_ikh[0], hand_r_ikh_ofst2)

        mtp_r_ikh_ofst1 = cmds.createNode('transform', n=mtp_r_ikh[0]+'_ofst_01', ss=1)
        mtp_r_ikh_ofst2 = cmds.createNode('transform', n=mtp_r_ikh[0]+'_ofst_02', ss=1)
        cmds.parent(mtp_r_ikh_ofst2, mtp_r_ikh_ofst1)
        cmds.matchTransform(mtp_r_ikh_ofst1, mtp_r_ikh[0])
        cmds.parent(mtp_r_ikh[0], mtp_r_ikh_ofst2)

        cmds.parentConstraint(loc_spaces[0], hand_r_ikh_ofst1, w=1, mo=1)
        cmds.parentConstraint(loc_spaces[1], mtp_r_ikh_ofst1, w=1, mo=1)

        bake([loc_aims[0], loc_aims[1], loc_aimbases[1], mtp_point_loc, hand_r_ikh_ofst1, mtp_r_ikh_ofst1])

        cmds.connectAttr(hand_r_jnt+'.r', locs[0]+'.r', f=1)
        cmds.connectAttr(mtp_r_jnt+'.r', locs[1]+'.r', f=1)


        cmds.setAttr(hand_r_ikh[0]+".poleVectorZ", 0)
        cmds.setAttr(hand_r_ikh[0]+".poleVectorX", 0)
        cmds.setAttr(hand_r_ikh[0]+".poleVectorY", 0)

        cmds.setAttr(mtp_r_ikh[0]+".poleVectorZ", 0)
        cmds.setAttr(mtp_r_ikh[0]+".poleVectorX", 0)
        cmds.setAttr(mtp_r_ikh[0]+".poleVectorY", 0)

        # cnst
        cmds.pointConstraint(loc_aims[0], hand_r_ikh_ofst1, w=1)
        cmds.pointConstraint(loc_aims[1], mtp_r_ikh_ofst1, w=1)



        cmds.setAttr(loc_aimbases_dupaim+'.tz', 70)
        # cmds.poleVectorConstraint(loc_aimbases_dupaim, mtp_r_ikh[0], w=1)
        mdl = cmds.createNode('multDoubleLinear', ss=1)
        cmds.addAttr(loc_aimbases_dupaim, ln="twistTweak", dv=0.5, at='double', min=0, k=1)

        cmds.connectAttr(loc_aimbases_dupaim+'.translateX', mdl+'.input1', f=1)
        cmds.connectAttr(loc_aimbases_dupaim+'.twistTweak', mdl+'.input2', f=1)
        cmds.connectAttr(mdl+'.output', mtp_r_ikh[0]+'.twist', f=1)

        cmds.aimConstraint(loc_aimbases_dupaim, loc_aimbases_dup, weight=1, upVector=(0, 1, 0), worldUpObject=loc_aims[2], worldUpType="objectrotation", offset=(0, 0, 0), aimVector=(0, 0, 1), worldUpVector=(0, 1, 0))

        # grp
        prop_space_grp = 'prop_space_grp'
        if not cmds.objExists(prop_space_grp):
            cmds.createNode('transform', n=prop_space_grp, ss=1)

        cmds.parent(loc_aimbases[1], prop_space_grp)
        cmds.parent(hand_r_ikh_ofst1, prop_space_grp)
        cmds.parent(mtp_r_ikh_ofst1, prop_space_grp)
        cmds.parent(loc_spaces[0], prop_space_grp)


        cmds.setAttr(loc_spaces[0]+'.v', 0)
        cmds.setAttr(hand_r_ikh[0]+'.v', 0)
        cmds.setAttr(mtp_r_ikh[0]+'.v', 0)

        prop_space_set = 'prop_space_set'
        if not cmds.objExists(prop_space_set):
            cmds.sets(em=1, n=prop_space_set)

        cmds.sets(loc_aims[1], add=prop_space_set)

        prop_space_bake_set = 'prop_space_bake_set'
        if not cmds.objExists(prop_space_bake_set):
            cmds.sets(em=1, n=prop_space_bake_set)

        cmds.sets(sel[0], add=prop_space_bake_set)
        cmds.sets(sel[1], add=prop_space_bake_set)
        cmds.sets(sel[2], add=prop_space_bake_set)
        cmds.sets(pos_hand_r, add=prop_space_bake_set)
        cmds.sets(prop_space_bake_set, add=prop_space_set)

        scalelocs = [loc_aims[0], loc_aims[1], loc_aimbases[1], loc_aimbases_dupaim]
        for lc in scalelocs:
            sh = cmds.listRelatives(lc, s=1)
            cmds.setAttr(sh[0]+".localScaleZ", 10)
            cmds.setAttr(sh[0]+".localScaleX", 10)
            cmds.setAttr(sh[0]+".localScaleY", 10)

        # to ctrls cnst
        for i, (cnst_loc, ctrl) in enumerate(zip(locs, sel)):
            if i >= 2:
                pass
            else:
                cmds.orientConstraint(cnst_loc, ctrl, w=1, mo=1)

        cmds.pointConstraint(mtp_point_loc, sel[1], w=1, mo=1)
        cmds.pointConstraint(sel[0], locs[0], w=1, mo=1)

        cmds.setAttr(loc_aimbases_dupaim+".rx", lock=True, channelBox=False, keyable=False)
        cmds.setAttr(loc_aimbases_dupaim+".ry", lock=True, channelBox=False, keyable=False)
        cmds.setAttr(loc_aimbases_dupaim+".rz", lock=True, channelBox=False, keyable=False)
        cmds.setAttr(loc_aimbases_dupaim+".sx", lock=True, channelBox=False, keyable=False)
        cmds.setAttr(loc_aimbases_dupaim+".sy", lock=True, channelBox=False, keyable=False)
        cmds.setAttr(loc_aimbases_dupaim+".sz", lock=True, channelBox=False, keyable=False)
        cmds.setAttr(loc_aimbases_dupaim+".v", lock=True, channelBox=False, keyable=False)


        cmds.pointConstraint(pos_hand_r, hand_r_jnt, w=1, mo=1)
        cmds.pointConstraint(sel[1], mtp_r_jnt, w=1, mo=1)

        self.ikHandle_loc.append(loc_aims[1])

    def bakes(self):
        if not self.bake_objs:
            return

        curTime = cmds.currentTime(q=1)
        cmds.currentTime(cmds.playbackOptions(q=1, min=1))

        cmds.bakeResults(self.bake_objs,
                 sparseAnimCurveBake=False,
                 minimizeRotation=False,
                 removeBakedAttributeFromLayer=False,
                 removeBakedAnimFromLayer=False,
                 oversamplingRate=1,
                 bakeOnOverrideLayer=False,
                 preserveOutsideKeys=True,
                 simulation=True,
                 sampleBy=1,
                 shape=False,
                 t=(cmds.playbackOptions(q=1, min=1), cmds.playbackOptions(q=1, max=1)),
                 disableImplicitControl=True,
                 controlPoints=False,
                 at=[u'tx', u'ty', u'tz', u'rx', u'ry', u'rz', u'sx', u'sy', u'sz'])

        cmds.currentTime(curTime)

        cmds.delete(self.bake_consts)

    def create_loc(self, obj):
        if not cmds.objExists(obj):
            return
        ps_loc = cmds.spaceLocator(n='{0}_ps_loc'.format(obj))
        ps_loc_space = cmds.createNode('transform', ss=1, n='{0}_bake_space'.format(ps_loc[0]))
        cmds.parent(ps_loc, ps_loc_space)
        # cmds.matchTransform(ps_loc_space, obj)
        con = cmds.parentConstraint(obj, ps_loc_space)

        self.bake_objs.append(ps_loc_space)
        self.bake_consts.append(con[0])
        self.ik_match_obj.append(ps_loc[0])

        return ps_loc[0], ps_loc_space

    def create_ikHandle(self):
        start = self.ik_match_obj[0]
        end = self.ik_match_obj[-1]

        self.rot_j = cmds.createNode('joint', ss=1, n='{0}_st_rot_jnt'.format(start))
        self.piv_j = cmds.createNode('joint', ss=1, n='{0}_ed_piv_jnt'.format(end))

        cmds.matchTransform(self.rot_j, start)
        cmds.matchTransform(self.piv_j, end)

        cmds.parent(self.piv_j, self.rot_j)

        cmds.makeIdentity(self.rot_j, a=1, t=0, r=1, s=0, n=0, pn=1)

        self.ikHandle = cmds.ikHandle(sj=self.rot_j, ee=self.piv_j, sol='ikRPsolver', s='sticky', n='{0}_ikh'.format(self.piv_j))
        self.ikHandle_space = cmds.createNode('transform', ss=1, n='{0}_space'.format(self.ikHandle[0]))
        self.ikHandle_loc = cmds.spaceLocator(n='{0}_loc'.format(self.ikHandle[0]))

        cmds.parent(self.ikHandle_loc[0], self.ikHandle_space)
        cmds.matchTransform(self.ikHandle_space, self.ikHandle[0])

        cmds.parent(self.ikHandle[0], self.ikHandle_loc[0])

    def delete_prop_space_grp(self):
        if cmds.objExists('prop_space_grp'):
            cmds.delete('prop_space_grp')
        if cmds.objExists('prop_space_set'):
            cmds.delete('prop_space_set')
        if cmds.objExists('prop_space_bake_set'):
            cmds.delete('prop_space_bake_set')

    def bake_set(self):
        cmds.select('prop_space_bake_set', ne=1, r=1)
        cmds.pickWalk(d='down')
        bake_obj = cmds.ls(os=1)
        try:
            cmds.refresh(su=1)
            cmds.bakeResults(bake_obj,
                     sparseAnimCurveBake=False,
                     minimizeRotation=False,
                     removeBakedAttributeFromLayer=False,
                     removeBakedAnimFromLayer=False,
                     oversamplingRate=1,
                     bakeOnOverrideLayer=False,
                     preserveOutsideKeys=True,
                     simulation=True,
                     sampleBy=1,
                     shape=False,
                     t=(cmds.playbackOptions(q=1, min=1), cmds.playbackOptions(q=1, max=1)),
                     disableImplicitControl=True,
                     controlPoints=False,
                     at=[u'tx', u'ty', u'tz', u'rx', u'ry', u'rz', u'sx', u'sy', u'sz'])
            cmds.refresh(su=0)
        except:
            cmds.refresh(su=0)

if __name__ == "__main__":
    try:
        ui.close()
        ui.deleteLater()
    except:
        pass

    ui = PropSpaceDialog()
    ui.show()
