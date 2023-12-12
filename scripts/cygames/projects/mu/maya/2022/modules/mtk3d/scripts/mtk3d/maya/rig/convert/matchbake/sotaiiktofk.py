# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as OpenMaya
import sys
import os
import codecs
import json
import timeit
import time
import math

class IKtoFK():
    def __init__(self, namespace):
        self.namespace = namespace
        """
        left leg ############################################################
        """
        # ik ctrls
        self.l_legs_poleVector = '{}:calf_L_ik_pv_ctrl'.format(self.namespace)
        self.l_legs_ik_ctrl = '{}:foot_L_ik_ctrl'.format(self.namespace)
        l_legs_ik_rot_ctrl = '{}:foot_L_ik_ctrl'.format(self.namespace)
        l_legs_ik_end_ctrl = '{}:foot_L_ik_ctrl_revFoot_holdBall_ctrl'.format(self.namespace)

        l_legs_hips = [u'{}:pelvis_C_fk_ctrl'.format(self.namespace),
                u'{}:pelvis_C_fkRot_ctrl'.format(self.namespace)]

        # fk ctrls
        l_legs_start_ctrl = '{}:thigh_L_fk_ctrl'.format(self.namespace)
        l_legs_mid_ctrl = '{}:calf_L_fk_ctrl'.format(self.namespace)
        l_legs_end_ctrl = '{}:foot_L_fk_ctrl'.format(self.namespace)
        l_legs_tip_ctrl = '{}:ball_L_fk_ctrl'.format(self.namespace)
        l_legs_fk_shoulder_ctrl = None
        l_legs_distance = 10

        self.left_legs = {}
        self.left_legs['poleVector'] = self.l_legs_poleVector
        self.left_legs['ik_ctrl'] = self.l_legs_ik_ctrl
        self.left_legs['ik_rot_ctrl'] = l_legs_ik_rot_ctrl
        self.left_legs['ik_end_ctrl'] = l_legs_ik_end_ctrl
        self.left_legs['hips'] = l_legs_hips
        self.left_legs['ik_auto_rot'] = False
        self.left_legs['start_ctrl'] = l_legs_start_ctrl
        self.left_legs['mid_ctrl'] = l_legs_mid_ctrl
        self.left_legs['end_ctrl'] = l_legs_end_ctrl
        self.left_legs['tip_ctrl'] = l_legs_tip_ctrl
        self.left_legs['fk_shoulder_ctrl'] = l_legs_fk_shoulder_ctrl
        self.left_legs['distance'] = l_legs_distance

        """
        right leg ############################################################
        """
        # ik ctrls
        self.r_legs_poleVector = '{}:calf_R_ik_pv_ctrl'.format(self.namespace)
        self.r_legs_ik_ctrl = '{}:foot_R_ik_ctrl'.format(self.namespace)
        r_legs_ik_rot_ctrl = '{}:foot_R_ik_ctrl'.format(self.namespace)
        r_legs_ik_end_ctrl = '{}:foot_R_ik_ctrl_revFoot_holdBall_ctrl'.format(self.namespace)

        r_legs_hips = [u'{}:pelvis_C_fk_ctrl'.format(self.namespace),
                u'{}:pelvis_C_fkRot_ctrl'.format(self.namespace)]

        # fk ctrls
        r_legs_start_ctrl = '{}:thigh_R_fk_ctrl'.format(self.namespace)
        r_legs_mid_ctrl = '{}:calf_R_fk_ctrl'.format(self.namespace)
        r_legs_end_ctrl = '{}:foot_R_fk_ctrl'.format(self.namespace)
        r_legs_tip_ctrl = '{}:ball_R_fk_ctrl'.format(self.namespace)
        r_legs_fk_shoulder_ctrl = None
        r_legs_distance = 10

        self.right_legs = {}
        self.right_legs['poleVector'] = self.r_legs_poleVector
        self.right_legs['ik_ctrl'] = self.r_legs_ik_ctrl
        self.right_legs['ik_rot_ctrl'] = r_legs_ik_rot_ctrl
        self.right_legs['ik_end_ctrl'] = r_legs_ik_end_ctrl
        self.right_legs['hips'] = r_legs_hips
        self.right_legs['ik_auto_rot'] = False
        self.right_legs['start_ctrl'] = r_legs_start_ctrl
        self.right_legs['mid_ctrl'] = r_legs_mid_ctrl
        self.right_legs['end_ctrl'] = r_legs_end_ctrl
        self.right_legs['tip_ctrl'] = r_legs_tip_ctrl
        self.right_legs['fk_shoulder_ctrl'] = r_legs_fk_shoulder_ctrl
        self.right_legs['distance'] = r_legs_distance

        """
        left arm ############################################################
        """
        # ik ctrls
        self.l_arms_poleVector = '{}:upperarm_L_ik_pv_ctrl'.format(self.namespace)
        self.l_arms_ik_ctrl = '{}:hand_L_ik_ctrl'.format(self.namespace)
        l_arms_ik_rot_ctrl = '{}:hand_L_ikRot_ctrl_ikRot_ctrl'.format(self.namespace)
        l_arms_ik_end_ctrl = '{}:clavicle_L_ikAutoRot_ctrl_ikAutoShoulder_ctrl'.format(self.namespace)

        l_arms_hips = [u'{}:pelvis_C_fk_ctrl'.format(self.namespace),
                 u'{}:spine_C_01_fk_ctrl'.format(self.namespace),
                 u'{}:spine_C_02_fk_ctrl'.format(self.namespace),
                 u'{}:spine_C_03_fk_ctrl'.format(self.namespace)]

        # fk ctrls
        l_arms_start_ctrl = '{}:upperarm_L_fk_ctrl'.format(self.namespace)
        l_arms_mid_ctrl = '{}:lowerarm_L_fk_ctrl'.format(self.namespace)
        l_arms_end_ctrl = '{}:hand_L_fk_ctrl'.format(self.namespace)
        l_arms_tip_ctrl = '{}:clavicle_L_fk_ctrl'.format(self.namespace)
        l_arms_fk_shoulder_ctrl = '{}:clavicle_L_fk_ctrl'.format(self.namespace)
        l_arms_distance = 10

        self.left_arms = {}
        self.left_arms['poleVector'] = self.l_arms_poleVector
        self.left_arms['ik_ctrl'] = self.l_arms_ik_ctrl
        self.left_arms['ik_rot_ctrl'] = l_arms_ik_rot_ctrl
        self.left_arms['ik_end_ctrl'] = l_arms_ik_end_ctrl
        self.left_arms['hips'] = l_arms_hips
        self.left_arms['ik_auto_rot'] = True
        self.left_arms['start_ctrl'] = l_arms_start_ctrl
        self.left_arms['mid_ctrl'] = l_arms_mid_ctrl
        self.left_arms['end_ctrl'] = l_arms_end_ctrl
        self.left_arms['tip_ctrl'] = l_arms_tip_ctrl
        self.left_arms['fk_shoulder_ctrl'] = l_arms_fk_shoulder_ctrl
        self.left_arms['distance'] = l_arms_distance

        """
        right arm ############################################################
        """
        # ik ctrls
        self.r_arms_poleVector = '{}:upperarm_R_ik_pv_ctrl'.format(self.namespace)
        self.r_arms_ik_ctrl = '{}:hand_R_ik_ctrl'.format(self.namespace)
        r_arms_ik_rot_ctrl = '{}:hand_R_ikRot_ctrl_ikRot_ctrl'.format(self.namespace)
        r_arms_ik_end_ctrl = '{}:clavicle_R_ikAutoRot_ctrl_ikAutoShoulder_ctrl'.format(self.namespace)

        r_arms_hips = [u'{}:pelvis_C_fk_ctrl'.format(self.namespace),
                 u'{}:spine_C_01_fk_ctrl'.format(self.namespace),
                 u'{}:spine_C_02_fk_ctrl'.format(self.namespace),
                 u'{}:spine_C_03_fk_ctrl'.format(self.namespace)]

        # fk ctrls
        r_arms_start_ctrl = '{}:upperarm_R_fk_ctrl'.format(self.namespace)
        r_arms_mid_ctrl = '{}:lowerarm_R_fk_ctrl'.format(self.namespace)
        r_arms_end_ctrl = '{}:hand_R_fk_ctrl'.format(self.namespace)
        r_arms_tip_ctrl = '{}:clavicle_R_fk_ctrl'.format(self.namespace)
        r_arms_fk_shoulder_ctrl = '{}:clavicle_R_fk_ctrl'.format(self.namespace)
        r_arms_distance = 10

        self.right_arms = {}
        self.right_arms['poleVector'] = self.r_arms_poleVector
        self.right_arms['ik_ctrl'] = self.r_arms_ik_ctrl
        self.right_arms['ik_rot_ctrl'] = r_arms_ik_rot_ctrl
        self.right_arms['ik_end_ctrl'] = r_arms_ik_end_ctrl
        self.right_arms['hips'] = r_arms_hips
        self.right_arms['ik_auto_rot'] = True
        self.right_arms['start_ctrl'] = r_arms_start_ctrl
        self.right_arms['mid_ctrl'] = r_arms_mid_ctrl
        self.right_arms['end_ctrl'] = r_arms_end_ctrl
        self.right_arms['tip_ctrl'] = r_arms_tip_ctrl
        self.right_arms['fk_shoulder_ctrl'] = r_arms_fk_shoulder_ctrl
        self.right_arms['distance'] = r_arms_distance

    # ik to fk
    def ik_to_fk_match(self, poleVector=None, ik_ctrl=None, ik_rot_ctrl=None, ik_end_ctrl=None, hips=None, ik_auto_rot=False,
                 start_ctrl=None, mid_ctrl=None, end_ctrl=None, fk_shoulder_ctrl=None, tip_ctrl=None, distance=10):

        # ik ctrl [rotate]
        pos_dict = {}

        if hips != None:
            for obj in hips:
                pos_dict[obj] = {}
                pos_dict[obj]['translate'] = cmds.xform(obj, q=1, t=1, os=1)
                pos_dict[obj]['rotate'] = cmds.xform(obj, q=1, ro=1, os=1)
                keyable_attrs = cmds.listAttr(obj, k=1)
                if 'translateX' in keyable_attrs:
                    cmds.xform(obj,
                               t=[0, cmds.xform(obj, q=1, t=1, os=1, a=1)[1], cmds.xform(obj, q=1, t=1, os=1, a=1)[2]],
                               os=1, a=1)
                if 'translateY' in keyable_attrs:
                    cmds.xform(obj,
                               t=[cmds.xform(obj, q=1, t=1, os=1, a=1)[0], 0, cmds.xform(obj, q=1, t=1, os=1, a=1)[2]],
                               os=1, a=1)
                if 'translateZ' in keyable_attrs:
                    cmds.xform(obj,
                               t=[cmds.xform(obj, q=1, t=1, os=1, a=1)[0], cmds.xform(obj, q=1, t=1, os=1, a=1)[1], 0],
                               os=1, a=1)

                if 'rotateX' in keyable_attrs:
                    cmds.xform(obj,
                               ro=[0, cmds.xform(obj, q=1, ro=1, os=1, a=1)[1], cmds.xform(obj, q=1, ro=1, os=1, a=1)[2]],
                               os=1, a=1)
                if 'rotateY' in keyable_attrs:
                    cmds.xform(obj,
                               ro=[cmds.xform(obj, q=1, ro=1, os=1, a=1)[0], 0, cmds.xform(obj, q=1, ro=1, os=1, a=1)[2]],
                               os=1, a=1)
                if 'rotateZ' in keyable_attrs:
                    cmds.xform(obj,
                               ro=[cmds.xform(obj, q=1, ro=1, os=1, a=1)[0], cmds.xform(obj, q=1, ro=1, os=1, a=1)[1], 0],
                               os=1, a=1)

        for obj in [start_ctrl, mid_ctrl, end_ctrl, fk_shoulder_ctrl]:
            if obj == None:
                continue
            pos_dict[obj] = {}
            if cmds.objExists(obj):
                pos_dict[obj]['translate'] = cmds.xform(obj, q=1, t=1, os=1)
                pos_dict[obj]['rotate'] = cmds.xform(obj, q=1, ro=1, os=1)
            keyable_attrs = cmds.listAttr(obj, k=1)
            if 'translateX' in keyable_attrs:
                cmds.xform(obj,
                           t=[0, cmds.xform(obj, q=1, t=1, os=1, a=1)[1], cmds.xform(obj, q=1, t=1, os=1, a=1)[2]],
                           os=1, a=1)
            if 'translateY' in keyable_attrs:
                cmds.xform(obj,
                           t=[cmds.xform(obj, q=1, t=1, os=1, a=1)[0], 0, cmds.xform(obj, q=1, t=1, os=1, a=1)[2]],
                           os=1, a=1)
            if 'translateZ' in keyable_attrs:
                cmds.xform(obj,
                           t=[cmds.xform(obj, q=1, t=1, os=1, a=1)[0], cmds.xform(obj, q=1, t=1, os=1, a=1)[1], 0],
                           os=1, a=1)

            if 'rotateX' in keyable_attrs:
                cmds.xform(obj,
                           ro=[0, cmds.xform(obj, q=1, ro=1, os=1, a=1)[1], cmds.xform(obj, q=1, ro=1, os=1, a=1)[2]],
                           os=1, a=1)
            if 'rotateY' in keyable_attrs:
                cmds.xform(obj,
                           ro=[cmds.xform(obj, q=1, ro=1, os=1, a=1)[0], 0, cmds.xform(obj, q=1, ro=1, os=1, a=1)[2]],
                           os=1, a=1)
            if 'rotateZ' in keyable_attrs:
                cmds.xform(obj,
                           ro=[cmds.xform(obj, q=1, ro=1, os=1, a=1)[0], cmds.xform(obj, q=1, ro=1, os=1, a=1)[1], 0],
                           os=1, a=1)

        for obj in [poleVector, ik_ctrl, ik_rot_ctrl, ik_end_ctrl]:
            if obj == None:
                continue
            keyable_attrs = cmds.listAttr(obj, k=1)
            if 'translateX' in keyable_attrs:
                cmds.setAttr('{}.tx'.format(obj), 0)
            if 'translateY' in keyable_attrs:
                cmds.setAttr('{}.ty'.format(obj), 0)
            if 'translateZ' in keyable_attrs:
                cmds.setAttr('{}.tz'.format(obj), 0)

            if 'rotateX' in keyable_attrs:
                cmds.setAttr('{}.rx'.format(obj), 0)
            if 'rotateY' in keyable_attrs:
                cmds.setAttr('{}.ry'.format(obj), 0)
            if 'rotateZ' in keyable_attrs:
                cmds.setAttr('{}.rz'.format(obj), 0)

        ik_pos_loc = cmds.spaceLocator()[0]
        cmds.setAttr('{}.rotateOrder'.format(ik_pos_loc), cmds.getAttr('{}.rotateOrder'.format(ik_rot_ctrl)))
        ik_rot_pos = cmds.xform(ik_rot_ctrl, q=1, t=1, ws=1)
        ik_rot_rot = cmds.xform(ik_rot_ctrl, q=1, ro=1, ws=1)
        cmds.xform(ik_pos_loc, t=ik_rot_pos, ro=ik_rot_rot, ws=1, a=1)
        cmds.parentConstraint(end_ctrl, ik_pos_loc, w=1, mo=1)
        # return poleVector, ik_ctrl, ik_rot_ctrl, ik_end_ctrl

        autokeyAts = cmds.autoKeyframe(q=1, st=1)
        if autokeyAts:
            cmds.autoKeyframe(st=False)
        for k, v in pos_dict.items():
            if cmds.objExists(k):
                cmds.xform(k, t=v['translate'], ro=v['rotate'], os=1, a=1)
        cmds.autoKeyframe(st=autokeyAts)
        cmds.xform(ik_rot_ctrl, ro=cmds.xform(ik_pos_loc, q=1, ro=1, ws=1), ws=1, a=1)
        cmds.delete(ik_pos_loc)

        # ik ctrl [translate]
        cmds.matchTransform(ik_ctrl, end_ctrl, pos=1)

        # ik end ctrl [translate] [rotate]
        if fk_shoulder_ctrl != None:
            cmds.matchTransform(ik_end_ctrl, fk_shoulder_ctrl)

        self.set_poleVector(start_ctrl, mid_ctrl, end_ctrl, poleVector, distance)

        # ik end ctrl [translate] [rotate]
        cmds.matchTransform(ik_end_ctrl, tip_ctrl)

        # ik Auto Rot
        if ik_auto_rot:
            cmds.matchTransform(ik_rot_ctrl, end_ctrl)

        return poleVector, ik_ctrl, ik_rot_ctrl, ik_end_ctrl

    def simple_match(self, poleVector=None, ik_ctrl=None, ik_rot_ctrl=None, ik_end_ctrl=None, hips=None, ik_auto_rot=False,
                 start_ctrl=None, mid_ctrl=None, end_ctrl=None, fk_shoulder_ctrl=None, tip_ctrl=None, distance=10):
        # match ctrl
        poleVector_list = [start_ctrl, mid_ctrl, end_ctrl, distance]
        fk_list = [tip_ctrl, mid_ctrl, end_ctrl]

        ikfk_relation = {}
        ikfk_relation[end_ctrl] = [ik_ctrl, ik_rot_ctrl]
        ikfk_relation[mid_ctrl] = ['poleVector', poleVector]
        ikfk_relation[tip_ctrl] = ik_end_ctrl

        for match_fk_ctrl in fk_list:
            match_Loc = cmds.spaceLocator()[0]
            cmds.matchTransform(match_Loc, match_fk_ctrl)
            if type(ikfk_relation[match_fk_ctrl]) == list:
                if ikfk_relation[match_fk_ctrl][0] != 'poleVector':
                    cmds.matchTransform(ikfk_relation[match_fk_ctrl][0], match_Loc, pos=1)
                    cmds.matchTransform(ikfk_relation[match_fk_ctrl][1], match_Loc, rot=1)
                else:
                    # polevector
                    self.set_poleVector(poleVector_list[0], poleVector_list[1], poleVector_list[2], ikfk_relation[match_fk_ctrl][1], poleVector_list[3])
            else:
                cmds.matchTransform(ikfk_relation[match_fk_ctrl], match_Loc)

            cmds.delete(match_Loc)

        return poleVector, ik_ctrl, ik_rot_ctrl, ik_end_ctrl


    def set_poleVector(self, start_ctrl, mid_ctrl, end_ctrl, poleVector, distance):
        # poleVector
        start = cmds.xform(start_ctrl ,q= 1 ,ws = 1,t =1 )
        mid = cmds.xform(mid_ctrl ,q= 1 ,ws = 1,t =1 )
        end = cmds.xform(end_ctrl ,q= 1 ,ws = 1,t =1 )

        startV = OpenMaya.MVector(start[0] ,start[1],start[2])
        midV = OpenMaya.MVector(mid[0] ,mid[1],mid[2])
        endV = OpenMaya.MVector(end[0] ,end[1],end[2])

        startEnd = endV - startV
        startMid = midV - startV

        dotP = startMid * startEnd
        proj = float(dotP) / float(startEnd.length())
        startEndN = startEnd.normal()
        projV = startEndN * proj

        arrowV = startMid - projV
        arrowV*= 0.5
        finalV = arrowV + midV

        cross1 = startEnd ^ startMid
        cross1.normalize()

        cross2 = cross1 ^ arrowV
        cross2.normalize()
        arrowV.normalize()

        matrixV = [arrowV.x , arrowV.y , arrowV.z , 0 ,
        cross1.x ,cross1.y , cross1.z , 0 ,
        cross2.x , cross2.y , cross2.z , 0,
        0,0,0,1]

        matrixM = OpenMaya.MMatrix()

        OpenMaya.MScriptUtil.createMatrixFromList(matrixV , matrixM)

        matrixFn = OpenMaya.MTransformationMatrix(matrixM)

        rot = matrixFn.eulerRotation()

        loc = cmds.spaceLocator()[0]
        cmds.xform(loc , ws =1 , t= (finalV.x , finalV.y ,finalV.z))

        cmds.xform ( loc , ws = 1 , rotation = ((rot.x/math.pi*180.0),
        (rot.y/math.pi*180.0),
        (rot.z/math.pi*180.0)))

        cmds.move(distance, 0, 0, loc, os=1, wd=1, r=1)

        cmds.xform(poleVector, t=cmds.xform(loc, q=1, t=1, ws=1), ws=1, a=1)
        cmds.delete(loc)

    def current_match(self, l_legs=True, r_legs=True, l_arms=True, r_arms=True):
        if l_arms:
            value = self.ik_to_fk_match(**self.left_arms)
        if r_arms:
            value = self.ik_to_fk_match(**self.right_arms)
        if l_legs:
            value = self.ik_to_fk_match(**self.left_legs)
        if r_legs:
            value = self.ik_to_fk_match(**self.right_legs)

        return value

    def bakeanim(self, select_timeslider=False, simplebake=False, l_legs=True, r_legs=True, l_arms=True, r_arms=True):
        playCur = cmds.currentTime(q=1)

        playmin = cmds.playbackOptions(q=1, min=1)
        playmax = cmds.playbackOptions(q=1, max=1)

        if select_timeslider:
            aPlayBackSliderPython = mel.eval('$tmpVar=$gPlayBackSlider')
            rangeArray = cmds.timeControl( aPlayBackSliderPython, q=True, rangeArray=True)

            playmin = rangeArray[0]
            playmax = rangeArray[1]

        cmds.cycleCheck(e=False)

        autokey_sts = cmds.autoKeyframe(q=1, st=1)
        if autokey_sts == True:
            cmds.autoKeyframe(st=False)

        cmds.refresh(suspend=True)
        x = int(playmin)
        for i in range(int(playmax)+1):
            f = i + x
            if f == int(playmax)+1:
                break
            else:
                cmds.currentTime(f)

            # options
            cmds.setAttr('{}.space'.format(self.l_legs_ik_ctrl), 0);cmds.setAttr('{}.space'.format(self.l_legs_poleVector), 0)
            cmds.setAttr('{}.space'.format(self.r_legs_ik_ctrl), 0);cmds.setAttr('{}.space'.format(self.r_legs_poleVector), 0)
            cmds.setAttr('{}.space'.format(self.l_arms_ik_ctrl), 0);cmds.setAttr('{}.space'.format(self.l_arms_poleVector), 0)
            cmds.setAttr('{}.space'.format(self.r_arms_ik_ctrl), 0);cmds.setAttr('{}.space'.format(self.r_arms_poleVector), 0)

            # コントローラによって変更する必要がある
            """
            cmds.setAttr("{}:proxy_L_foot_ikRot_ctrl.rx".format(self.namespace), 0)
            cmds.setAttr("{}:proxy_L_foot_ikRot_ctrl.ry".format(self.namespace), 0)
            cmds.setAttr("{}:proxy_L_foot_ikRot_ctrl.rz".format(self.namespace), 0)
            cmds.setAttr("{}:proxy_R_foot_ikRot_ctrl.rx".format(self.namespace), 0)
            cmds.setAttr("{}:proxy_R_foot_ikRot_ctrl.ry".format(self.namespace), 0)
            cmds.setAttr("{}:proxy_R_foot_ikRot_ctrl.rz".format(self.namespace), 0)
            """

            if l_legs:
                # print('left legs {}'.format(str(f)))
                if simplebake:
                    poleVector_buf, ik_ctrl_buf, ik_rot_ctrl_buf, ik_end_ctrl_buf = self.simple_match(**self.left_legs)
                else:
                    poleVector_buf, ik_ctrl_buf, ik_rot_ctrl_buf, ik_end_ctrl_buf = self.ik_to_fk_match(**self.left_legs)
                cmds.clearCache(allNodes=1)
                cmds.setKeyframe([poleVector_buf, ik_ctrl_buf, ik_rot_ctrl_buf, ik_end_ctrl_buf], breakdown=0, hierarchy='none', shape=0, controlPoints=0)

            if r_legs:
                # print('right legs {}'.format(str(f)))
                if simplebake:
                    poleVector_buf, ik_ctrl_buf, ik_rot_ctrl_buf, ik_end_ctrl_buf = self.simple_match(**self.right_legs)
                else:
                    poleVector_buf, ik_ctrl_buf, ik_rot_ctrl_buf, ik_end_ctrl_buf = self.ik_to_fk_match(**self.right_legs)
                cmds.clearCache(allNodes=1)
                cmds.setKeyframe([poleVector_buf, ik_ctrl_buf, ik_rot_ctrl_buf, ik_end_ctrl_buf], breakdown=0, hierarchy='none', shape=0, controlPoints=0)

            if l_arms:
                # print('left arms {}'.format(str(f)))
                if simplebake:
                    poleVector_buf, ik_ctrl_buf, ik_rot_ctrl_buf, ik_end_ctrl_buf = self.simple_match(**self.left_arms)
                else:
                    poleVector_buf, ik_ctrl_buf, ik_rot_ctrl_buf, ik_end_ctrl_buf = self.ik_to_fk_match(**self.left_arms)
                cmds.clearCache(allNodes=1)
                cmds.setKeyframe([poleVector_buf, ik_ctrl_buf, ik_rot_ctrl_buf, ik_end_ctrl_buf], breakdown=0, hierarchy='none', shape=0, controlPoints=0)

            if r_arms:
                # print('right arms {}'.format(str(f)))
                if simplebake:
                    poleVector_buf, ik_ctrl_buf, ik_rot_ctrl_buf, ik_end_ctrl_buf = self.simple_match(**self.right_arms)
                else:
                    poleVector_buf, ik_ctrl_buf, ik_rot_ctrl_buf, ik_end_ctrl_buf = self.ik_to_fk_match(**self.right_arms)
                cmds.clearCache(allNodes=1)
                cmds.setKeyframe([poleVector_buf, ik_ctrl_buf, ik_rot_ctrl_buf, ik_end_ctrl_buf], breakdown=0, hierarchy='none', shape=0, controlPoints=0)

        cmds.refresh(suspend=False)

        cmds.currentTime(playCur)

        cmds.autoKeyframe(st=autokey_sts)

        cmds.cycleCheck(e=True)

# Namespace取得
# print('get name space!')
nss_in_joints_proc = cmds.ls('*_proxy_jnt', type='joint', r=1)
nss_buf_proc = ['{}'.format(nss_in.replace(nss_in.split(':')[-1], '')) for nss_in in nss_in_joints_proc]
nss_list_proc = list(set(nss_buf_proc))
try:
    nss_list_proc.remove('')
except:
    pass
nss_proc = nss_list_proc[0]

ik_to_fk = IKtoFK(nss_proc)
ik_to_fk.bakeanim(select_timeslider=False, simplebake=False, l_legs=True, r_legs=True, l_arms=True, r_arms=True)
