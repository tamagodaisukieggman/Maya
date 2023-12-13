# -*- coding: utf-8 -*-
from maya import cmds, mel
import maya.OpenMaya as om
import maya.api.OpenMaya as om2

import codecs
from collections import OrderedDict
from datetime import datetime
from functools import partial
import functools
import getpass
import json
import math
import os
import re
import subprocess
import traceback
import pdb


def bake(fk_handL_jnts, fk_handL_ctrls, ik_handL_ctrls, ik_handL_matches, handL_match, handL_match_state, handL_ikfk_ctrl,
         fk_handR_jnts, fk_handR_ctrls, ik_handR_ctrls, ik_handR_matches, handR_match, handR_match_state, handR_ikfk_ctrl,
         fk_footL_jnts, fk_footL_ctrls, ik_footL_ctrls, ik_footL_matches, footL_match, footL_match_state, footL_ikfk_ctrl,
         fk_footR_jnts, fk_footR_ctrls, ik_footR_ctrls, ik_footR_matches, footR_match, footR_match_state, footR_ikfk_ctrl,
         fk_spine_ctrls, ik_spine_match_locs, spine_match,
         footrollL_ctl_pos_loc, footroll_footL_ctl, footroll_toebaseL_ctl, footrollR_ctl_pos_loc, footroll_footR_ctl, footroll_toebaseR_ctl, footlockL_loc, footlockR_loc, toelockL_loc, toelockR_loc, reverseFoot_match):
    cur_time=cmds.currentTime(q=1)
    if cmds.autoKeyframe(q=True, st=True):
        autoKeyState = 1
    else:
        autoKeyState = 0

    cmds.autoKeyframe(st=0)

    playmin = cmds.playbackOptions(q=1, min=1)
    playmax = cmds.playbackOptions(q=1, max=1)

    start = playmin
    end = playmax-1

    gPlayBackSlider = mel.eval('$temp=$gPlayBackSlider')
    if gPlayBackSlider:
        if cmds.timeControl(gPlayBackSlider, q=True, rv=True):
            frameRange = cmds.timeControl(gPlayBackSlider, q=True, ra=True)
            start = frameRange[0]
            end = frameRange[1]
        else:
            frameRange = cmds.currentTime(q=1)
            start = frameRange
            end = frameRange-1

    if playmax < end:
        end = playmax

    setkey_attrs = mel.eval('string $selectedChannelBox[] = `channelBox -query -selectedMainAttributes mainChannelBox`;')
    if setkey_attrs == []:
        setkey_attrs =  [u'tx', u'ty', u'tz', u'rx', u'ry', u'rz', u'sx', u'sy', u'sz']

    for i in range (int(start), int(end+1)):
        cmds.currentTime(i, e=True)
        # handL
        if handL_match:
            if handL_match_state == 0:
                cmds.setAttr(handL_ikfk_ctrl+'.ikfk', 1)
                ik2fk(fk_handL_jnts, fk_handL_ctrls)
                cmds.setAttr(handL_ikfk_ctrl+'.ikfk', 0)
                cmds.setKeyframe(handL_ikfk_ctrl, at='ikfk')
                cmds.setKeyframe(fk_handL_ctrls, at=setkey_attrs)
            elif handL_match_state == 1:
                cmds.setAttr(handL_ikfk_ctrl+'.ikfk', 0)
                fk2ik(ik_handL_ctrls, ik_handL_matches, False)
                cmds.setAttr(handL_ikfk_ctrl+'.ikfk', 1)
                cmds.setKeyframe(handL_ikfk_ctrl, at='ikfk')
                cmds.setKeyframe(ik_handL_ctrls, at=setkey_attrs)

        # handR
        if handR_match:
            if handR_match_state == 0:
                cmds.setAttr(handR_ikfk_ctrl+'.ikfk', 1)
                ik2fk(fk_handR_jnts, fk_handR_ctrls)
                cmds.setAttr(handR_ikfk_ctrl+'.ikfk', 0)
                cmds.setKeyframe(handR_ikfk_ctrl, at='ikfk')
                cmds.setKeyframe(fk_handR_ctrls, at=setkey_attrs)
            elif handR_match_state == 1:
                cmds.setAttr(handR_ikfk_ctrl+'.ikfk', 0)
                fk2ik(ik_handR_ctrls, ik_handR_matches, False)
                cmds.setAttr(handR_ikfk_ctrl+'.ikfk', 1)
                cmds.setKeyframe(handR_ikfk_ctrl, at='ikfk')
                cmds.setKeyframe(ik_handR_ctrls, at=setkey_attrs)

        # footL
        if footL_match:
            if footL_match_state == 0:
                cmds.setAttr(footL_ikfk_ctrl+'.ikfk', 1)
                ik2fk(fk_footL_jnts, fk_footL_ctrls)
                cmds.setAttr(footL_ikfk_ctrl+'.ikfk', 0)
                cmds.setKeyframe(footL_ikfk_ctrl, at='ikfk')
                cmds.setKeyframe(fk_footL_ctrls, at=setkey_attrs)
            elif footL_match_state == 1:
                cmds.setAttr(footL_ikfk_ctrl+'.ikfk', 0)
                fk2ik(ik_footL_ctrls, ik_footL_matches, True)
                cmds.setAttr(footL_ikfk_ctrl+'.ikfk', 1)
                cmds.setKeyframe(footL_ikfk_ctrl, at='ikfk')
                cmds.setKeyframe(ik_footL_ctrls, at=setkey_attrs)

        # footR
        if footR_match:
            if footR_match_state == 0:
                cmds.setAttr(footR_ikfk_ctrl+'.ikfk', 1)
                ik2fk(fk_footR_jnts, fk_footR_ctrls)
                cmds.setAttr(footR_ikfk_ctrl+'.ikfk', 0)
                cmds.setKeyframe(footR_ikfk_ctrl, at='ikfk')
                cmds.setKeyframe(fk_footR_ctrls, at=setkey_attrs)
            elif footR_match_state == 1:
                cmds.setAttr(footR_ikfk_ctrl+'.ikfk', 0)
                fk2ik(ik_footR_ctrls, ik_footR_matches, True)
                cmds.setAttr(footR_ikfk_ctrl+'.ikfk', 1)
                cmds.setKeyframe(footR_ikfk_ctrl, at='ikfk')
                cmds.setKeyframe(ik_footR_ctrls, at=setkey_attrs)

        # spines
        if spine_match:
            ik2fk_spines(fk_spine_ctrls, ik_spine_match_locs)
            cmds.setKeyframe(ik_spine_match_locs, at=setkey_attrs)

        # reverseFoot
        if reverseFoot_match:
            cmds.matchTransform(footrollL_ctl_pos_loc, footroll_footL_ctl, pos=1, rot=1, scl=0)
            cmds.matchTransform(footlockL_loc, footroll_footL_ctl, pos=1, rot=1, scl=0)
            cmds.matchTransform(toelockL_loc, footroll_toebaseL_ctl, pos=1, rot=1, scl=0)

            cmds.matchTransform(footrollR_ctl_pos_loc, footroll_footR_ctl, pos=1, rot=1, scl=0)
            cmds.matchTransform(footlockR_loc, footroll_footR_ctl, pos=1, rot=1, scl=0)
            cmds.matchTransform(toelockR_loc, footroll_toebaseR_ctl, pos=1, rot=1, scl=0)

            cmds.setKeyframe([footrollL_ctl_pos_loc, footrollR_ctl_pos_loc], at=setkey_attrs)

            # cmds.setKeyframe([footrollL_ctl_pos_loc, footrollR_ctl_pos_loc,
            #                   footlockL_loc, footlockR_loc,
            #                   toelockL_loc, toelockR_loc], at=setkey_attrs)


    cmds.currentTime(cur_time)
    cmds.autoKeyframe(state=autoKeyState)


def ik2fk(jnts, ctrls):
    for i, jt in enumerate(jnts):
        cmds.matchTransform(ctrls[i], jt, rot=1, pos=0, scl=0)

def ik2fk_spines(ctrls, locs):
    for i, ctrl in enumerate(ctrls):
        cmds.matchTransform(locs[i], ctrl, rot=1, pos=1, scl=0)

def ik2fk_spines_matchConstraints(ik_spine_ctrls, ik_spine_pos_ctrl, fk_spine_ctrls):
    spines_ikfk_constraints_sets = 'spines_ikfk_constraints_sets'
    if not cmds.objExists(spines_ikfk_constraints_sets):
        cmds.sets(em=1, n=spines_ikfk_constraints_sets)

    for i, (ik_s_ctrl, fk_s_ctrl) in enumerate(zip(ik_spine_ctrls, fk_spine_ctrls)):
        ori = cmds.orientConstraint(ik_s_ctrl, fk_s_ctrl, w=1, mo=1)
        cmds.sets(ori[0], add=spines_ikfk_constraints_sets)

    po = cmds.pointConstraint(fk_spine_ctrls[0], ik_spine_pos_ctrl, w=1, mo=1)
    cmds.sets(po[0], add=spines_ikfk_constraints_sets)


# const
def reverseFoot_matchConstraints(footroll_footL_ctl, footroll_toebaseL_ctl, footroll_footR_ctl, footroll_toebaseR_ctl, footlockL_loc, footlockR_loc, toelockL_loc, toelockR_loc):
    reverseFoot_constraints_sets = 'reverseFoot_constraints_sets'
    if not cmds.objExists(reverseFoot_constraints_sets):
        cmds.sets(em=1, n=reverseFoot_constraints_sets)

    # left
    ori = cmds.orientConstraint(footlockL_loc, footroll_footL_ctl, w=1, mo=1)
    cmds.sets(ori[0], add=reverseFoot_constraints_sets)

    po = cmds.pointConstraint(footlockL_loc, footroll_footL_ctl, w=1, mo=1)
    cmds.sets(po[0], add=reverseFoot_constraints_sets)

    ori = cmds.orientConstraint(toelockL_loc, footroll_toebaseL_ctl, w=1, mo=1)
    cmds.sets(ori[0], add=reverseFoot_constraints_sets)

    # right
    ori = cmds.orientConstraint(footlockR_loc, footroll_footR_ctl, w=1, mo=1)
    cmds.sets(ori[0], add=reverseFoot_constraints_sets)

    po = cmds.pointConstraint(footlockR_loc, footroll_footR_ctl, w=1, mo=1)
    cmds.sets(po[0], add=reverseFoot_constraints_sets)

    ori = cmds.orientConstraint(toelockR_loc, footroll_toebaseR_ctl, w=1, mo=1)
    cmds.sets(ori[0], add=reverseFoot_constraints_sets)


def root_matchConstraints(root_pos_ctl_loc, root_ctl, root_pos_ctl, cog_root_state):
    root_match_constraints_sets = 'root_match_constraints_sets'
    if not cmds.objExists(root_match_constraints_sets):
        cmds.sets(em=1, n=root_match_constraints_sets)

    if cog_root_state == 0:
        pa = cmds.parentConstraint(root_pos_ctl_loc, root_pos_ctl, w=1)
        cmds.sets(pa[0], add=root_match_constraints_sets)



def fk2ik(ctrls, matches, foot):
    cmds.matchTransform(ctrls[0], matches[0], rot=0, pos=1, scl=0)
    if foot:
        cmds.matchTransform(ctrls[0], matches[0], rot=1, pos=0, scl=0)
    cmds.matchTransform(ctrls[1], matches[1], rot=1, pos=0, scl=0)
    cmds.matchTransform(ctrls[2], matches[2], rot=0, pos=1, scl=0)


def matchbake(handL_ikfk_state=False, handR_ikfk_state=False, handL_fk_ik=0, handR_fk_ik=0,
              footL_ikfk_state=False, footR_ikfk_state=False, footL_fk_ik=0, footR_fk_ik=0,
              spine_ikfk_state=False,
              reverseFoot_state=False,
              cog_root_state=False, cog_root=0):

    """
    handL_ikfk_state=False, handR_ikfk_state=False, handL_fk_ik=fk:0,ik:1, handR_fk_ik=fk:0,ik:1,
    footL_ikfk_state=False, footR_ikfk_state=False, footL_fk_ik=fk:0,ik:1, footR_fk_ik=fk:0,ik:1,
    spine_ikfk_state=False,
    reverseFoot_state=False
    """

    #get the namespace of current picker file.
    # try:
    currentPickerNamespace = mel.eval('MGP_GetCurrentPickerNamespace')

    if currentPickerNamespace:
        currentPickerNamespace = currentPickerNamespace + ':'
    else:
        currentPickerNamespace = ''

    # sel = cmds.ls(os=1)
    # if ':' in sel[0]:
    #     spl_names = sel[0].split(':')
    #     currentPickerNamespace = ':'.join(spl_names[:-1:]) + ':'
    # else:
    #     currentPickerNamespace = ''


    ##################
    # HandL
    ##################

    ikfk_handL_switch_ctrl = currentPickerNamespace+'handL_ikfk_ctl'

    # IK to FK
    fk_handL_jnts = [currentPickerNamespace+'proxy_armL_jnt',
            currentPickerNamespace+'proxy_forearmL_jnt',
            currentPickerNamespace+'proxy_handL_jnt']

    fk_handL_ctrls = [currentPickerNamespace+'fk_armL_ctl',
             currentPickerNamespace+'fk_forearmL_ctl',
             currentPickerNamespace+'fk_handL_ctl']

    # FK to IK
    ik_handL_pos_ctrl = currentPickerNamespace+'handL_ctl'
    ik_handL_rot_ctrl = currentPickerNamespace+'handL_rot_ctl'
    ik_elbowL_ctrl = currentPickerNamespace+'forearmL_ctl'
    ik_handL_match_loc = currentPickerNamespace+'handL_match_loc'
    ik_forearmL_match_loc = currentPickerNamespace+'forearmL_match_loc'

    ik_handL_ctrls = [ik_handL_pos_ctrl, ik_handL_rot_ctrl, ik_elbowL_ctrl]
    ik_handL_matches = [ik_handL_match_loc, fk_handL_jnts[2], ik_forearmL_match_loc]


    ##################
    # HandR
    ##################

    ikfk_handR_switch_ctrl = currentPickerNamespace+'handR_ikfk_ctl'

    # IK to FK
    fk_handR_jnts = [currentPickerNamespace+'proxy_armR_jnt',
            currentPickerNamespace+'proxy_forearmR_jnt',
            currentPickerNamespace+'proxy_handR_jnt']

    fk_handR_ctrls = [currentPickerNamespace+'fk_armR_ctl',
             currentPickerNamespace+'fk_forearmR_ctl',
             currentPickerNamespace+'fk_handR_ctl']

    # FK to IK
    ik_handR_pos_ctrl = currentPickerNamespace+'handR_ctl'
    ik_handR_rot_ctrl = currentPickerNamespace+'handR_rot_ctl'
    ik_elbowR_ctrl = currentPickerNamespace+'forearmR_ctl'
    ik_handR_match_loc = currentPickerNamespace+'handR_match_loc'
    ik_forearmR_match_loc = currentPickerNamespace+'forearmR_match_loc'

    ik_handR_ctrls = [ik_handR_pos_ctrl, ik_handR_rot_ctrl, ik_elbowR_ctrl]
    ik_handR_matches = [ik_handR_match_loc, fk_handR_jnts[2], ik_forearmR_match_loc]


    ##################
    # FootL
    ##################

    ikfk_footL_switch_ctrl = currentPickerNamespace+'footL_ikfk_ctl'

    # IK to FK
    fk_footL_jnts = [currentPickerNamespace+'proxy_uplegL_jnt',
            currentPickerNamespace+'proxy_legL_jnt',
            currentPickerNamespace+'proxy_footL_jnt',
            currentPickerNamespace+'proxy_toebaseL_jnt']
    fk_footL_ctrls = [currentPickerNamespace+'fk_uplegL_ctl',
             currentPickerNamespace+'fk_legL_ctl',
             currentPickerNamespace+'fk_footL_ctl',
             currentPickerNamespace+'fk_toebaseL_ctl']

    # FK to IK
    ik_footL_pos_ctrl = currentPickerNamespace+'footL_ctl'
    ik_footL_rot_ctrl = currentPickerNamespace+'toebaseL_ctl'
    ik_kneeL_ctrl = currentPickerNamespace+'legL_ctl'
    ik_footL_match_loc = currentPickerNamespace+'footL_match_loc'
    ik_legL_match_loc = currentPickerNamespace+'legL_match_loc'

    ik_footL_ctrls = [ik_footL_pos_ctrl, ik_footL_rot_ctrl, ik_kneeL_ctrl]
    ik_footL_matches = [ik_footL_match_loc, fk_footL_jnts[3], ik_legL_match_loc]



    ##################
    # FootR
    ##################

    ikfk_footR_switch_ctrl = currentPickerNamespace+'footR_ikfk_ctl'

    # IK to FK
    fk_footR_jnts = [currentPickerNamespace+'proxy_uplegR_jnt',
            currentPickerNamespace+'proxy_legR_jnt',
            currentPickerNamespace+'proxy_footR_jnt',
            currentPickerNamespace+'proxy_toebaseR_jnt']
    fk_footR_ctrls = [currentPickerNamespace+'fk_uplegR_ctl',
             currentPickerNamespace+'fk_legR_ctl',
             currentPickerNamespace+'fk_footR_ctl',
             currentPickerNamespace+'fk_toebaseR_ctl']

    # FK to IK
    ik_footR_pos_ctrl = currentPickerNamespace+'footR_ctl'
    ik_footR_rot_ctrl = currentPickerNamespace+'toebaseR_ctl'
    ik_kneeR_ctrl = currentPickerNamespace+'legR_ctl'
    ik_footR_match_loc = currentPickerNamespace+'footR_match_loc'
    ik_legR_match_loc = currentPickerNamespace+'legR_match_loc'

    ik_footR_ctrls = [ik_footR_pos_ctrl, ik_footR_rot_ctrl, ik_kneeR_ctrl]
    ik_footR_matches = [ik_footR_match_loc, fk_footR_jnts[3], ik_legR_match_loc]

    ##################
    # Spine
    ##################
    # FK to IK
    fk_spine_ctrls = [currentPickerNamespace+'spine_01_ctl',
            currentPickerNamespace+'spine_02_ctl',
            currentPickerNamespace+'spine_03_ctl']

    ik_spine_match_locs = [currentPickerNamespace+'ik_spine_01_ctl_gp_loc',
             currentPickerNamespace+'ik_spine_02_ctl_gp_loc',
             currentPickerNamespace+'ik_spine_03_ctl_gp_loc']

    ik_spine_ctrls = [currentPickerNamespace+'ik_rot_spine_01_ctl',
             currentPickerNamespace+'ik_rot_spine_02_ctl',
             currentPickerNamespace+'ik_spine_03_ctl']

    ik_spine_pos_ctrl = currentPickerNamespace+'ik_spine_01_ctl'


    ##################
    # ReverseFoot
    ##################
    # Foot L
    footrollL_ctl_pos_loc = currentPickerNamespace+'footrollL_ctl_pos_loc'
    footroll_footL_ctl = currentPickerNamespace+'footL_ctl'
    footroll_toebaseL_ctl = currentPickerNamespace+'toebaseL_ctl'

    footlockL_loc = currentPickerNamespace+'footlockL_loc'
    toelockL_loc = currentPickerNamespace+'toelockL_loc'

    # Foot R
    footrollR_ctl_pos_loc = currentPickerNamespace+'footrollR_ctl_pos_loc'
    footroll_footR_ctl = currentPickerNamespace+'footR_ctl'
    footroll_toebaseR_ctl = currentPickerNamespace+'toebaseR_ctl'

    footlockR_loc = currentPickerNamespace+'footlockR_loc'
    toelockR_loc = currentPickerNamespace+'toelockR_loc'


    ##################
    # ReverseFoot
    ##################
    root_pos_ctl_loc = currentPickerNamespace+'root_pos_ctl_loc'
    root_pos_ctl = currentPickerNamespace+'root_pos_ctl'
    root_ctl = currentPickerNamespace+'root_ctl'



    try:
        cmds.refresh(su=1)

        bake(fk_handL_jnts, fk_handL_ctrls, ik_handL_ctrls, ik_handL_matches, handL_ikfk_state, handL_fk_ik, ikfk_handL_switch_ctrl,
             fk_handR_jnts, fk_handR_ctrls, ik_handR_ctrls, ik_handR_matches, handR_ikfk_state, handR_fk_ik, ikfk_handR_switch_ctrl,
             fk_footL_jnts, fk_footL_ctrls, ik_footL_ctrls, ik_footL_matches, footL_ikfk_state, footL_fk_ik, ikfk_footL_switch_ctrl,
             fk_footR_jnts, fk_footR_ctrls, ik_footR_ctrls, ik_footR_matches, footR_ikfk_state, footR_fk_ik, ikfk_footR_switch_ctrl,
             fk_spine_ctrls, ik_spine_match_locs, spine_ikfk_state,
             footrollL_ctl_pos_loc, footroll_footL_ctl, footroll_toebaseL_ctl, footrollR_ctl_pos_loc, footroll_footR_ctl, footroll_toebaseR_ctl, footlockL_loc, footlockR_loc, toelockL_loc, toelockR_loc, reverseFoot_state)

        cmds.refresh(su=0)
    except Exception as e:
        print(e)
        cmds.refresh(su=0)


    # ik2fk_spines
    if spine_ikfk_state:
        ik2fk_spines_matchConstraints(ik_spine_ctrls, ik_spine_pos_ctrl, fk_spine_ctrls)

    # reverseFoot
    if reverseFoot_state:
        reverseFoot_matchConstraints(footroll_footL_ctl, footroll_toebaseL_ctl, footroll_footR_ctl, footroll_toebaseR_ctl, footlockL_loc, footlockR_loc, toelockL_loc, toelockR_loc)

    # root constraint
    if cog_root_state:
        root_matchConstraints(root_pos_ctl_loc, root_ctl, root_pos_ctl, cog_root)


def force_zeroout():
    #get the namespace of current picker file.
    currentPickerNamespace = mel.eval('MGP_GetCurrentPickerNamespace')

    if currentPickerNamespace:
        currentPickerNamespace = currentPickerNamespace + ':'
    else:
        currentPickerNamespace = ''

    ctrls = [currentPickerNamespace + 'cog_ctl',
     currentPickerNamespace + 'fk_armL_ctl',
     currentPickerNamespace + 'fk_armR_ctl',
     currentPickerNamespace + 'fk_footL_ctl',
     currentPickerNamespace + 'fk_footR_ctl',
     currentPickerNamespace + 'fk_forearmL_ctl',
     currentPickerNamespace + 'fk_forearmR_ctl',
     currentPickerNamespace + 'fk_handL_ctl',
     currentPickerNamespace + 'fk_handR_ctl',
     currentPickerNamespace + 'fk_legL_ctl',
     currentPickerNamespace + 'fk_legR_ctl',
     currentPickerNamespace + 'fk_toebaseL_ctl',
     currentPickerNamespace + 'fk_toebaseR_ctl',
     currentPickerNamespace + 'fk_uplegL_ctl',
     currentPickerNamespace + 'fk_uplegR_ctl',
     currentPickerNamespace + 'footL_ctl',
     currentPickerNamespace + 'footL_ikfk_ctl',
     currentPickerNamespace + 'footR_ctl',
     currentPickerNamespace + 'footR_ikfk_ctl',
     currentPickerNamespace + 'forearmL_ctl',
     currentPickerNamespace + 'forearmR_ctl',
     currentPickerNamespace + 'handL_ctl',
     currentPickerNamespace + 'handL_ikfk_ctl',
     currentPickerNamespace + 'handL_rot_ctl',
     currentPickerNamespace + 'handR_ctl',
     currentPickerNamespace + 'handR_ikfk_ctl',
     currentPickerNamespace + 'handR_rot_ctl',
     currentPickerNamespace + 'head_ctl',
     currentPickerNamespace + 'hip_ctl',
     currentPickerNamespace + 'legL_ctl',
     currentPickerNamespace + 'legR_ctl',
     currentPickerNamespace + 'neck_ctl',
     currentPickerNamespace + 'root_ctl',
     currentPickerNamespace + 'root_pos_ctl',
     currentPickerNamespace + 'root_pos_ctl_loc',
     currentPickerNamespace + 'shoulderL_ctl',
     currentPickerNamespace + 'shoulderR_ctl',
     currentPickerNamespace + 'spine_01_ctl',
     currentPickerNamespace + 'spine_02_ctl',
     currentPickerNamespace + 'spine_03_ctl',
     currentPickerNamespace + 'toebaseL_ctl',
     currentPickerNamespace + 'toebaseR_ctl',
     currentPickerNamespace + 'world_ctl',
     currentPickerNamespace + 'camera_ctl']


    for ctrl in ctrls:
        try:
            cmds.xform(ctrl, t=[0,0,0], ro=[0,0,0], s=[1,1,1])
        except:
            pass


def matchConstraint(currentNamespace='', jointNamepace='', gender='male'):
    def constraint_convert(src, dst, pos, rot, scl, mo):
        print(src, dst)
        cnsts = []
        if pos:
            cnst = cmds.pointConstraint(src, dst, w=1, mo=mo)
            cnsts.append(cnst)
        if rot:
            if ('fk_forearmL_ctl' in dst
                or 'fk_forearmR_ctl' in dst
                or 'fk_legL_ctl' in dst
                or 'fk_legR_ctl' in dst):
                cnst = cmds.orientConstraint(src, dst, w=1, mo=mo, sk=['x', 'z'])
                cnsts.append(cnst)
            else:
                cnst = cmds.orientConstraint(src, dst, w=1, mo=mo)
                cnsts.append(cnst)
        if scl:
            cnst = cmds.scaleConstraint(src, dst, w=1, mo=mo)
            cnsts.append(cnst)

        return cnsts

    def constraint_convert_ik_pv(dst, pos, rot, scl, mo, start, mid, end, move):
        print(dst)
        cnsts = []

        # start, mid, end = 'uplegL_jnt', 'legL_jnt', 'footL_jnt'

        loc1 = cmds.spaceLocator()
        loc2 = cmds.duplicate(loc1)
        loc3 = cmds.duplicate(loc1)
        cmds.parent(loc3, loc2)
        cmds.parent(loc2, loc1)

        cmds.pointConstraint(start, loc1, w=1)
        cmds.pointConstraint(end, loc1, w=1)

        cmds.aimConstraint(mid, loc2, w=1, aim=(1,0,0), u=(0,1,0), wut='vector', wu=(0,1,0))

        cmds.move(move, 0, 0, loc3, r=1, os=1, wd=1)

        cnsts.append(loc1)

        src = loc3[0]

        if pos:
            cnst = cmds.pointConstraint(src, dst, w=1, mo=mo)
            cnsts.append(cnst)
        if rot:
            cnst = cmds.orientConstraint(src, dst, w=1, mo=mo)
            cnsts.append(cnst)
        if scl:
            cnst = cmds.scaleConstraint(src, dst, w=1, mo=mo)
            cnsts.append(cnst)

        return cnsts

    source_joints = [u'root_jnt',
     u'cog_jnt',
     u'spine_01_jnt',
     u'spine_02_jnt',
     u'spine_03_jnt',
     u'neck_jnt',
     u'head_jnt',
     u'shoulderL_jnt',
     u'armL_jnt',
     u'forearmL_jnt',
     u'handL_jnt',
     u'handWeaponL_offset_jnt',
     u'handWeaponL_bind_jnt',
     u'shoulderR_jnt',
     u'armR_jnt',
     u'forearmR_jnt',
     u'handR_jnt',
     u'handWeaponR_offset_jnt',
     u'handWeaponR_bind_jnt',
     u'hip_jnt',
     u'uplegL_jnt',
     u'legL_jnt',
     u'footL_jnt',
     u'toebaseL_jnt',
     u'uplegR_jnt',
     u'legR_jnt',
     u'footR_jnt',
     u'toebaseR_jnt']


    match_ctrls = OrderedDict()
    match_ctrls[currentNamespace+'root_ctl'] = [jointNamepace+'root_jnt', 1, 1, 0, 1]
    match_ctrls[currentNamespace+'cog_ctl'] = [jointNamepace+'cog_jnt', 1, 1, 0, 1]
    match_ctrls[currentNamespace+'hip_ctl'] = [jointNamepace+'hip_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'spine_01_ctl'] = [jointNamepace+'spine_01_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'spine_02_ctl'] = [jointNamepace+'spine_02_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'spine_03_ctl'] = [jointNamepace+'spine_03_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'neck_ctl'] = [jointNamepace+'neck_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'head_ctl'] = [jointNamepace+'head_jnt', 0, 1, 0, 1]

    # IK arm
    match_ctrls[currentNamespace+'shoulderL_ctl'] = [jointNamepace+'shoulderL_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'handL_ctl'] = [jointNamepace+'handL_jnt', 1, 0, 0, 1]
    match_ctrls[currentNamespace+'handL_rot_ctl'] = [jointNamepace+'handL_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_con_armL_loc'] = [jointNamepace+'armL_jnt', 1, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_con_forearmL_loc'] = [jointNamepace+'forearmL_jnt', 1, 1, 0, 1]

    match_ctrls[currentNamespace+'shoulderR_ctl'] = [jointNamepace+'shoulderR_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'handR_ctl'] = [jointNamepace+'handR_jnt', 1, 0, 0, 1]
    match_ctrls[currentNamespace+'handR_rot_ctl'] = [jointNamepace+'handR_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_con_armR_loc'] = [jointNamepace+'armR_jnt', 1, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_con_forearmR_loc'] = [jointNamepace+'forearmR_jnt', 1, 1, 0, 1]

    # IK arm pv
    match_ctrls[currentNamespace+'forearmL_ctl'] = [1, 0, 0, 0, jointNamepace+'armL_jnt', jointNamepace+'forearmL_jnt', jointNamepace+'handL_jnt', 60]
    match_ctrls[currentNamespace+'forearmR_ctl'] = [1, 0, 0, 0, jointNamepace+'armR_jnt', jointNamepace+'forearmR_jnt', jointNamepace+'handR_jnt', 60]


    # FK arm
    match_ctrls[currentNamespace+'fk_armL_ctl'] = [jointNamepace+'armL_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_forearmL_ctl'] = [jointNamepace+'forearmL_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_handL_ctl'] = [jointNamepace+'handL_jnt', 0, 1, 0, 1]

    match_ctrls[currentNamespace+'fk_armR_ctl'] = [jointNamepace+'armR_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_forearmR_ctl'] = [jointNamepace+'forearmR_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_handR_ctl'] = [jointNamepace+'handR_jnt', 0, 1, 0, 1]


    # IK leg
    match_ctrls[currentNamespace+'footL_ctl'] = [jointNamepace+'footL_jnt', 1, 1, 0, 1]
    match_ctrls[currentNamespace+'toebaseL_ctl'] = [jointNamepace+'toebaseL_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_con_uplegL_loc'] = [jointNamepace+'uplegL_jnt', 1, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_con_legL_loc'] = [jointNamepace+'legL_jnt', 1, 1, 0, 1]

    match_ctrls[currentNamespace+'footR_ctl'] = [jointNamepace+'footR_jnt', 1, 1, 0, 1]
    match_ctrls[currentNamespace+'toebaseR_ctl'] = [jointNamepace+'toebaseR_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_con_uplegR_loc'] = [jointNamepace+'uplegR_jnt', 1, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_con_legR_loc'] = [jointNamepace+'legR_jnt', 1, 1, 0, 1]

    # IK leg pv
    match_ctrls[currentNamespace+'legL_ctl'] = [1, 0, 0, 0, jointNamepace+'uplegL_jnt', jointNamepace+'legL_jnt', jointNamepace+'footL_jnt', 60]
    match_ctrls[currentNamespace+'legR_ctl'] = [1, 0, 0, 0, jointNamepace+'uplegR_jnt', jointNamepace+'legR_jnt', jointNamepace+'footR_jnt', 60]


    # FK leg
    match_ctrls[currentNamespace+'fk_uplegL_ctl'] = [jointNamepace+'uplegL_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_legL_ctl'] = [jointNamepace+'legL_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_footL_ctl'] = [jointNamepace+'footL_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_toebaseL_ctl'] = [jointNamepace+'toebaseL_jnt', 0, 1, 0, 1]

    match_ctrls[currentNamespace+'fk_uplegR_ctl'] = [jointNamepace+'uplegR_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_legR_ctl'] = [jointNamepace+'legR_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_footR_ctl'] = [jointNamepace+'footR_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_toebaseR_ctl'] = [jointNamepace+'toebaseR_jnt', 0, 1, 0, 1]

    # Weapons
    match_ctrls[currentNamespace+'handWeaponL_offset_ctl'] = [jointNamepace+'handWeaponL_offset_jnt', 1, 1, 1, 0]
    match_ctrls[currentNamespace+'handWeaponR_offset_ctl'] = [jointNamepace+'handWeaponR_offset_jnt', 1, 1, 1, 0]

    match_ctrls[currentNamespace+'handWeaponL_ctl'] = [jointNamepace+'handWeaponL_bind_jnt', 1, 1, 1, 0]
    match_ctrls[currentNamespace+'handWeaponR_ctl'] = [jointNamepace+'handWeaponR_bind_jnt', 1, 1, 1, 0]



    for jnt in source_joints:
        cmds.xform(jointNamepace+jnt, ro=[0, 0, 0], a=1)

    # root cog zero out
    cmds.xform(jointNamepace+'root_jnt', t=[0, 0, 0], a=1)

    if gender == 'male':
        cmds.xform(jointNamepace+'cog_jnt', t=[0, 103.400, 0], a=1)

        # weapon
        if cmds.objExists(jointNamepace+'handWeaponL_offset_jnt'):
            cmds.xform(jointNamepace+'handWeaponL_offset_jnt', t=[7.300, -2.400, 0.0], a=1)
        if cmds.objExists(jointNamepace+'handWeaponR_offset_jnt'):
            cmds.xform(jointNamepace+'handWeaponR_offset_jnt', t=[7.300, 2.400, 0.0], a=1)

        if cmds.objExists(jointNamepace+'handWeaponL_bind_jnt'):
            cmds.xform(jointNamepace+'handWeaponL_bind_jnt', t=[0, 0, 0], a=1)
        if cmds.objExists(jointNamepace+'handWeaponR_bind_jnt'):
            cmds.xform(jointNamepace+'handWeaponR_bind_jnt', t=[0, 0, 0], a=1)

    if gender == 'female':
        cmds.xform(jointNamepace+'cog_jnt', t=[0, 102.250, 0], a=1)

        # weapon
        if cmds.objExists(jointNamepace+'handWeaponL_offset_jnt'):
            cmds.xform(jointNamepace+'handWeaponL_offset_jnt', t=[5.300, -2.400, 0.0], a=1)
        if cmds.objExists(jointNamepace+'handWeaponR_offset_jnt'):
            cmds.xform(jointNamepace+'handWeaponR_offset_jnt', t=[5.300, 2.400, 0.0], a=1)

        if cmds.objExists(jointNamepace+'handWeaponL_bind_jnt'):
            cmds.xform(jointNamepace+'handWeaponL_bind_jnt', t=[0, 0, 0], a=1)
        if cmds.objExists(jointNamepace+'handWeaponR_bind_jnt'):
            cmds.xform(jointNamepace+'handWeaponR_bind_jnt', t=[0, 0, 0], a=1)

    # const sets
    if not cmds.objExists('bake_cnst_sets'):
        cmds.sets(em=1, n='bake_cnst_sets')


    ik_pv_ctrls = [currentNamespace+'forearmL_ctl',
                   currentNamespace+'forearmR_ctl',
                   currentNamespace+'legL_ctl',
                   currentNamespace+'legR_ctl']

    bake_ctrls = []
    for ctrl, jnt_value in match_ctrls.items():
        bake_ctrls.append(ctrl)
        if ('fk_con_armL_loc' in ctrl
            or 'fk_con_forearmL_loc' in ctrl
            or 'fk_con_armR_loc' in ctrl
            or 'fk_con_forearmR_loc' in ctrl
            or 'fk_con_uplegL_loc' in ctrl
            or 'fk_con_legL_loc' in ctrl
            or 'fk_con_uplegR_loc' in ctrl
            or 'fk_con_legR_loc' in ctrl):
                cmds.xform(ctrl, t=[0, 0, 0], ro=[0, 0, 0], a=1)

        try:
            if ctrl in ik_pv_ctrls:
                cnsts = constraint_convert_ik_pv(ctrl,
                                                 jnt_value[0],
                                                 jnt_value[1],
                                                 jnt_value[2],
                                                 jnt_value[3],
                                                 jnt_value[4],
                                                 jnt_value[5],
                                                 jnt_value[6],
                                                 jnt_value[7])
            else:
                cnsts = constraint_convert(jnt_value[0], ctrl, jnt_value[1], jnt_value[2], jnt_value[3], jnt_value[4])
            for ccnn in cnsts:
                cmds.sets(ccnn, add='bake_cnst_sets')
        except Exception as e:
            print(e)

    # # PoleVectors
    # cnsts = constraint_convert(currentNamespace+'fk_con_armL_pv_loc', currentNamespace+'forearmL_ctl', 1, 0, 0, 0)
    # for ccnn in cnsts:
    #     cmds.sets(ccnn, add='bake_cnst_sets')
    # cnsts = constraint_convert(currentNamespace+'fk_con_forearmL_pv_loc', currentNamespace+'forearmL_ctl', 1, 0, 0, 0)
    # for ccnn in cnsts:
    #     cmds.sets(ccnn, add='bake_cnst_sets')
    # cnsts = constraint_convert(currentNamespace+'fk_con_armR_pv_loc', currentNamespace+'forearmR_ctl', 1, 0, 0, 0)
    # for ccnn in cnsts:
    #     cmds.sets(ccnn, add='bake_cnst_sets')
    # cnsts = constraint_convert(currentNamespace+'fk_con_forearmR_pv_loc', currentNamespace+'forearmR_ctl', 1, 0, 0, 0)
    # for ccnn in cnsts:
    #     cmds.sets(ccnn, add='bake_cnst_sets')

    # cnsts = constraint_convert(currentNamespace+'fk_con_uplegL_pv_loc', currentNamespace+'legL_ctl', 1, 0, 0, 0)
    # for ccnn in cnsts:
    #     cmds.sets(ccnn, add='bake_cnst_sets')
    # cnsts = constraint_convert(currentNamespace+'fk_con_legL_pv_loc', currentNamespace+'legL_ctl', 1, 0, 0, 0)
    # for ccnn in cnsts:
    #     cmds.sets(ccnn, add='bake_cnst_sets')
    # cnsts = constraint_convert(currentNamespace+'fk_con_uplegR_pv_loc', currentNamespace+'legR_ctl', 1, 0, 0, 0)
    # for ccnn in cnsts:
    #     cmds.sets(ccnn, add='bake_cnst_sets')
    # cnsts = constraint_convert(currentNamespace+'fk_con_legR_pv_loc', currentNamespace+'legR_ctl', 1, 0, 0, 0)
    # for ccnn in cnsts:
    #     cmds.sets(ccnn, add='bake_cnst_sets')


def cache_transform(ctrls):
    cache_dict = {}
    for ctrl in ctrls:
        wt = cmds.xform(ctrl, q=1, t=1, ws=1)
        wr = cmds.xform(ctrl, q=1, ro=1, ws=1)
        cache_dict[ctrl] = [wt, wr]

    return cache_dict


def space_match(ctrl=None, set_spc_at=None, spaces=None, setkey=None):
    space_dict = {}
    for spc in spaces:
        listAttrs = cmds.listAttr(ctrl, ud=1, k=1)
        if listAttrs:
            for at in listAttrs:
                if at == spc:
                    cur_val = cmds.getAttr(ctrl+'.'+spc)
                    space_dict[spc] = cur_val

    space_dict[set_spc_at] = 1.0

    for set_spc, val in space_dict.items():
        listAttrs = cmds.listAttr(ctrl, ud=1, k=1)
        if listAttrs:
            if not set_spc in listAttrs:
                return

            if set_spc == set_spc_at:
                cmds.setAttr(ctrl+'.'+set_spc, val)
            else:
                cmds.setAttr(ctrl+'.'+set_spc, 0.0)

        if setkey:
            cmds.setKeyframe([ctrl], at=set_spc)


def space_match_bake(ctrls=None, set_spc_at=None, spaces=None, value=1.0):
    if ctrls:

        cur_time=cmds.currentTime(q=1)
        if cmds.autoKeyframe(q=True, st=True):
            autoKeyState = 1
        else:
            autoKeyState = 0

        cmds.autoKeyframe(st=0)

        playmin = cmds.playbackOptions(q=1, min=1)
        playmax = cmds.playbackOptions(q=1, max=1)

        start = playmin
        end = playmax-1

        gPlayBackSlider = mel.eval('$temp=$gPlayBackSlider')
        if gPlayBackSlider:
            if cmds.timeControl(gPlayBackSlider, q=True, rv=True):
                frameRange = cmds.timeControl(gPlayBackSlider, q=True, ra=True)
                start = frameRange[0]
                end = frameRange[1]
            else:
                frameRange = cmds.currentTime(q=1)
                start = frameRange
                end = frameRange-1

        if playmax < end:
            end = playmax

        setkey_attrs = mel.eval('string $selectedChannelBox[] = `channelBox -query -selectedMainAttributes mainChannelBox`;')
        if setkey_attrs == []:
            setkey_attrs =  [u'tx', u'ty', u'tz', u'rx', u'ry', u'rz', u'sx', u'sy', u'sz']

        get_transforms_frames = {}
        for i in range (int(start), int(end+1)):
            cmds.currentTime(i, e=True)
            get_transforms = cache_transform(ctrls)
            get_transforms_frames[i] = get_transforms

        for i in range (int(start), int(end+1)):
            cmds.currentTime(i, e=True)
            # space match
            if set_spc_at != 'rotSpace':
                for ctrl in ctrls:
                    space_match(ctrl=ctrl, set_spc_at=set_spc_at, spaces=spaces, setkey=True)
                    wt, wr = get_transforms_frames[i][ctrl]
                    cmds.xform(ctrl, t=wt, ro=wr, a=1, ws=1)

                    cmds.setKeyframe([ctrl], at=setkey_attrs)

            # handRot
            elif set_spc_at == 'rotSpace':
                for ctrl in ctrls:
                    wt, wr = get_transforms_frames[i][ctrl]

                    listAttrs = cmds.listAttr(ctrl, ud=1, k=1)
                    if listAttrs:
                        if set_spc_at in listAttrs:
                            cmds.setAttr(ctrl+'.'+set_spc_at, value)
                            cmds.setKeyframe([ctrl], at=set_spc_at)

                    cmds.xform(ctrl, t=wt, ro=wr, a=1, ws=1)

                    cmds.setKeyframe([ctrl], at=setkey_attrs)


        cmds.currentTime(cur_time)
        cmds.autoKeyframe(state=autoKeyState)

        cmds.filterCurve(ctrls, f='euler')


class ReplaceReferenceTool(object):
    def __init__(self):
        self.MAIN_WINDOW = 'Replace Reference Tool'

    def show(self):
        if cmds.workspaceControl(self.MAIN_WINDOW, q=1, ex=1):
            cmds.deleteUI(self.MAIN_WINDOW)

        self.win = cmds.workspaceControl(self.MAIN_WINDOW, l=self.MAIN_WINDOW)

        self.layout()

        cmds.showWindow(self.win)

    def layout(self):
        self.init_txtfield_asset_filter = 'ply*male*female'
        self.init_work_tab_label = 'Work'
        self.init_share_tab_label = 'Share'
        self.init_txtfield_file_filter = 'mdl'
        self.init_txtfield_exclude_filter = 'head*test*tmp*maya*ui*1000'

        menuBarLayout = cmds.menuBarLayout(p=self.win)
        cmds.menu(label='Edit')
        cmds.menuItem(label='Save Settings', c=self.save_settings)
        cmds.menuItem(label='Reset Settings', c=self.reset_settings)
        cmds.menuItem(label='Reload Settings', c=self.load_settings)
        cmds.menuItem(d=1)
        cmds.menuItem(label='Reload', c=self.all_reload)
        cmds.menuItem(label='ReferenceEditor', c='cmds.ReferenceEditor()')
        self.history_menuitems = cmds.menuItem(label='History', sm=1)
        self.history_items_buff = []

        self.col_layout_00 = cmds.columnLayout(adj=1, rs=7)

        self.txtfield_asset_filter = cmds.textFieldGrp(l='Assets Filter', tx=self.init_txtfield_asset_filter, tcc=self.all_reload, ad2=2, cat=[1, 'left', 50], p=self.col_layout_00)

        self.rowCol_layout_00 = cmds.rowColumnLayout(nr=1)

        self.opsmenu_tab = cmds.optionMenu( l='Tab', cc=self.all_reload)
        cmds.menuItem(l=self.init_work_tab_label, p=self.opsmenu_tab)
        cmds.menuItem(l=self.init_share_tab_label, p=self.opsmenu_tab)

        self.opsmenu_sub = cmds.optionMenu( l='Sub Cat', cc=self.load_assets_list)
        self.opsmenu_ast = cmds.optionMenu( l='Asset', cc=self.load_assets_list)

        self.txtfield_file_filter = cmds.textFieldGrp(l='List Filter', tx=self.init_txtfield_file_filter, tcc=self.load_assets_list, ad2=2, cat=[1, 'left', 50], p=self.col_layout_00)
        self.txtfield_exclude_filter = cmds.textFieldGrp(l='Exclude Filter', tx=self.init_txtfield_exclude_filter, tcc=self.load_assets_list, ad2=2, cat=[1, 'left', 50], p=self.col_layout_00)

        self.pan_layout_00 = cmds.paneLayout(cn='vertical2', p=self.col_layout_00)

        self.texSclLst_layout_src = cmds.textScrollList()
        self.texSclLst_layout_dst = cmds.textScrollList()

        self.apply_button = cmds.button(l='Apply', p=self.col_layout_00, c=self.apply_replace)

        self.list_sub_cat_array, self.list_asset_array, self.list_vari_array, self.list_file_array = self.search_work_path()
        self.ref_path_dict = self.search_references()

        self.load_assets_list()

        cmds.popupMenu(p=self.texSclLst_layout_src)
        cmds.menuItem(l='Show in Explorer', c=self.show_in_explorer_src)

        cmds.popupMenu(p=self.texSclLst_layout_dst)
        cmds.menuItem(l='Show in Explorer', c=self.show_in_explorer_dst)

        self.get_history_items()
        self.add_history_items()

        # load settings
        self.load_settings()


    def search_work_path(self):
        self.opsmenu_tab_value = cmds.optionMenu(self.opsmenu_tab, q=1, v=1)
        if self.opsmenu_tab_value == 'Work':
            search_path = 'W:/production/work/asset/character'
        else:
            search_path = '//CGS-STR-FAS05/100_projects/051_world/production/share/asset/character'
            result = cmds.confirmDialog(title='Change Share Tab',
                                       message='ファイル取得に時間がかかる場合があります。Share領域を検索しますか？',
                                       button=['OK', 'Cancel'],
                                       defaultButton='OK',
                                       cancelButton='Cancel',
                                       dismissString='Cancel')

            if not result == 'OK':
                cmds.optionMenu(self.opsmenu_tab, e=1, v='Work')
                return


        if not os.path.exists(search_path):
            cmds.error("Unable to find folder.{}".format(search_path))
            return

        self.filter_words = cmds.textFieldGrp(self.txtfield_asset_filter, q=1, tx=1)

        sub_cat_array = []
        asset_array = []
        vari_array = []
        file_array = []
        exclude = ['animation', 'hair', 'head', 'rig', 'test']
        for root, dirs, files in os.walk(search_path, topdown=True):
            dirs[:] = [d for d in dirs if d not in exclude]
            for fname in files:
                for fw in self.filter_words.split('*'):
                    if fw in fname:
                        file_path = os.path.join(root, fname)
                        search_file = file_path.replace('\\', '/')

                        if self.opsmenu_tab_value == 'Work':
                            sub_cat_array.append('/'.join(search_file.split('/')[:6]))
                            asset_array.append('/'.join(search_file.split('/')[:7]))
                            vari_array.append('/'.join(search_file.split('/')[:8]))

                            if search_file.split('/')[9] == 'model':
                                if search_file.endswith('.mb') or search_file.endswith('.ma'):
                                    file_array.append('/'.join(search_file.split('/')[:14]))

                        else:
                            sub_cat_array.append('/'.join(search_file.split('/')[:10]))
                            asset_array.append('/'.join(search_file.split('/')[:11]))
                            vari_array.append('/'.join(search_file.split('/')[:12]))

                            if search_file.split('/')[13] == 'model':
                                if search_file.endswith('.mb') or search_file.endswith('.ma'):
                                    file_array.append('/'.join(search_file.split('/')[:18]))


        list_sub_cat_array = list(set(sub_cat_array))
        list_asset_array = list(set(asset_array))
        list_vari_array = list(set(vari_array))
        list_file_array = list(set(file_array))

        # for menuItems
        items_list_sub_cat_array = [i_sub_cat.split('/')[-1] for i_sub_cat in list_sub_cat_array]
        items_list_asset_cat_array = [i_asset_cat.split('/')[-1] for i_asset_cat in list_asset_array]

        items_list_sub_cat_array.sort()
        items_list_asset_cat_array.sort()

        cmds.optionMenu(self.opsmenu_sub, e=1, dai=1)
        cmds.optionMenu(self.opsmenu_ast, e=1, dai=1)

        self.load_menuItems(array=items_list_sub_cat_array, parent=self.opsmenu_sub)
        self.load_menuItems(array=items_list_asset_cat_array, parent=self.opsmenu_ast)

        return list_sub_cat_array, list_asset_array, list_vari_array, list_file_array


    def search_references(self):
        ref_path_dict = OrderedDict()
        for rf in cmds.ls(rf=True, r=1):
            ref_path_dict[rf] = cmds.referenceQuery(rf, f=True)

        return ref_path_dict


    def load_assets_list(self, *args):
        cmds.textScrollList(self.texSclLst_layout_src, e=1, ra=1)
        cmds.textScrollList(self.texSclLst_layout_dst, e=1, ra=1)

        self.opsmenu_tab_value = cmds.optionMenu(self.opsmenu_tab, q=1, v=1)
        self.opsmenu_sub_value = cmds.optionMenu(self.opsmenu_sub, q=1, v=1)
        self.opsmenu_ast_value = cmds.optionMenu(self.opsmenu_ast, q=1, v=1)

        self.file_filter_words = cmds.textFieldGrp(self.txtfield_file_filter, q=1, tx=1)
        self.exclude_filter_words = cmds.textFieldGrp(self.txtfield_exclude_filter, q=1, tx=1)

        self.set_asset_items = OrderedDict()
        for file_name in self.list_file_array:
            if self.opsmenu_sub_value in file_name and self.opsmenu_ast_value in file_name:
                for fw in self.file_filter_words.split('*'):
                    if fw in file_name.split('/')[-1]:
                        self.set_asset_items[file_name.split('/')[-1]] = file_name

            if self.exclude_filter_words:
                for ew in self.exclude_filter_words.split('*'):
                    if ew in file_name.split('/')[-1]:
                        try:
                            self.set_asset_items.pop(file_name.split('/')[-1])
                        except KeyError:
                            pass


        self.asset_items_sorted_list = self.set_asset_items.keys()
        self.asset_items_sorted_list.sort(reverse=True)

        self.ref_items_sorted_list = self.ref_path_dict.keys()
        self.ref_items_sorted_list.sort()

        cmds.textScrollList(self.texSclLst_layout_src, e=1, a=self.ref_items_sorted_list)
        cmds.textScrollList(self.texSclLst_layout_dst, e=1, a=self.asset_items_sorted_list)


    def load_menuItems(self, array=None, parent=None):
        for item in array:
            cmds.menuItem(l=item, p=parent)


    def all_reload(self, *args):
        try:
            self.list_sub_cat_array, self.list_asset_array, self.list_vari_array, self.list_file_array = self.search_work_path()
            self.ref_path_dict = self.search_references()
            self.load_assets_list()
        except:
            pass


    def apply_replace(self, *args):
        sel_src_item = cmds.textScrollList(self.texSclLst_layout_src, q=1, si=1)
        sel_dst_item = cmds.textScrollList(self.texSclLst_layout_dst, q=1, si=1)

        if sel_dst_item is None or sel_src_item is None:
            cmds.error('You have to select items on lists.')
            return


        replace_path = self.set_asset_items[sel_dst_item[0]]
        ref_node = sel_src_item[0]

        if replace_path.endswith('.ma'):
            asset_type = 'mayaAscii'
        elif replace_path.endswith('.mb'):
            asset_type = 'mayaBinary'

        cmds.file(replace_path,
                  type=asset_type,
                  options="v=0;p=17;f=0",
                  loadReference=ref_node)


        self.save_settings()


    def add_history_items(self, *args):
        if self.history_items_buff:
            for del_mi in self.history_items_buff:
                cmds.deleteUI(del_mi)

        dreversed = OrderedDict()
        for k in reversed(self.history_items):
            dreversed[k] = self.history_items[k]

        for k, v in dreversed.items():
            mi = cmds.menuItem(l=k, c=partial(self.load_partial_historyItems, v[0], v[1], v[2], v[3], v[4], v[5], k.split('>>')[0], k.split('>>')[1]), p=self.history_menuitems)
            self.history_items_buff.append(mi)


    def load_partial_historyItems(self, txt_ast, tab_value, sub_value, ast_value, file_value, ex_value, src_refnode, dst_data, *args):
        cmds.textFieldGrp(self.txtfield_asset_filter, e=1, tx=txt_ast)
        cmds.optionMenu(self.opsmenu_tab, e=1, sl=int(tab_value))
        cmds.optionMenu(self.opsmenu_sub, e=1, sl=int(sub_value))
        cmds.optionMenu(self.opsmenu_ast, e=1, sl=int(ast_value))
        cmds.textFieldGrp(self.txtfield_file_filter, e=1, tx=file_value)
        cmds.textFieldGrp(self.txtfield_exclude_filter, e=1, tx=ex_value)

        self.load_assets_list()

        cmds.textScrollList(self.texSclLst_layout_src, e=1, si=src_refnode)
        cmds.textScrollList(self.texSclLst_layout_dst, e=1, si=dst_data)


    def get_history_items(self, *args):
        try:
            self.history_items = load_optionvar('Replace_Reference_Tool_for_world')[6]
        except:
            self.history_items = OrderedDict()


    def get_files(self, path='.'):
        total = []
        for p in os.listdir(path):
            full_path = os.path.join(path, p)
            if os.path.isfile(full_path):
                search_file = full_path.replace('\\', '/')
                total.append(search_file)
            elif os.path.isdir(full_path):
                for search_file in get_files(full_path):
                    total.append(search_file)
        return total


    def save_settings(self, *args):
        asset_filter_value = cmds.textFieldGrp(self.txtfield_asset_filter, q=1, tx=1)
        opsmenu_tab_value = cmds.optionMenu(self.opsmenu_tab, q=1, sl=1)
        opsmenu_sub_value = cmds.optionMenu(self.opsmenu_sub, q=1, sl=1)
        opsmenu_ast_value = cmds.optionMenu(self.opsmenu_ast, q=1, sl=1)
        txtfield_file_filter_value = cmds.textFieldGrp(self.txtfield_file_filter, q=1, tx=1)
        txtfield_exclude_filter_value = cmds.textFieldGrp(self.txtfield_exclude_filter, q=1, tx=1)


        sel_src_item = cmds.textScrollList(self.texSclLst_layout_src, q=1, si=1)
        sel_dst_item = cmds.textScrollList(self.texSclLst_layout_dst, q=1, si=1)

        try:
            self.get_history_items()
            self.history_items['{}>>{}'.format(sel_src_item[0], sel_dst_item[0])] = [asset_filter_value,
                                                              opsmenu_tab_value,
                                                              opsmenu_sub_value,
                                                              opsmenu_ast_value,
                                                              txtfield_file_filter_value,
                                                              txtfield_exclude_filter_value,]

            self.add_history_items()

            if 10 < len(self.history_items.keys()):
                self.history_items.pop(self.history_items.keys()[-1])


        except:
            pass


        save_items = OrderedDict()
        save_items['Replace_Reference_Tool_for_world'] = [asset_filter_value,
                                                          opsmenu_tab_value,
                                                          opsmenu_sub_value,
                                                          opsmenu_ast_value,
                                                          txtfield_file_filter_value,
                                                          txtfield_exclude_filter_value,
                                                          self.history_items]


        for key, value in save_items.items():
            v = str(value)
            cmds.optionVar(sv=[key, v])


    def show_in_explorer_dst(self, *args):
        sel_dst_item = cmds.textScrollList(self.texSclLst_layout_dst, q=1, si=1)
        replace_path = self.set_asset_items[sel_dst_item[0]]
        path = os.path.realpath('/'.join(replace_path.split('/')[:-1]))
        os.startfile(path)


    def show_in_explorer_src(self, *args):
        sel_src_item = cmds.textScrollList(self.texSclLst_layout_src, q=1, si=1)
        replace_path = self.ref_path_dict[sel_src_item[0]]
        path = os.path.realpath('/'.join(replace_path.split('/')[:-1]))
        os.startfile(path)


    def load_settings(self, *args):
        try:
            values = load_optionvar('Replace_Reference_Tool_for_world')

            for i, value in enumerate(values):
                # print(value)
                if i == 0:
                    cmds.textFieldGrp(self.txtfield_asset_filter, e=1, tx=value)
                elif i == 1:
                    cmds.optionMenu(self.opsmenu_tab, e=1, sl=int(value))
                elif i == 2:
                    cmds.optionMenu(self.opsmenu_sub, e=1, sl=int(value))
                elif i == 3:
                    cmds.optionMenu(self.opsmenu_ast, e=1, sl=int(value))
                elif i == 4:
                    cmds.textFieldGrp(self.txtfield_file_filter, e=1, tx=value)
                elif i == 5:
                    cmds.textFieldGrp(self.txtfield_exclude_filter, e=1, tx=value)

            self.load_assets_list()

        except Exception as e:
            print('Load settings Error:{}'.format(e))


    def reset_settings(self, *args):
        cmds.textFieldGrp(self.txtfield_asset_filter, e=1, tx=self.init_txtfield_asset_filter)
        cmds.optionMenu(self.opsmenu_tab, e=1, v=self.init_work_tab_label)
        cmds.textFieldGrp(self.txtfield_file_filter, e=1, tx=self.init_txtfield_file_filter)
        cmds.textFieldGrp(self.txtfield_exclude_filter, e=1, tx=self.init_txtfield_exclude_filter)

        self.all_reload()

        self.save_settings()


def load_optionvar(key):
    if cmds.optionVar(ex=key):
        return eval(cmds.optionVar(q=key))
    else:
        return None


class RefreshTool(object):
    def __init__(self):
        self.MAIN_WINDOW = 'Refresh Tool'

    def show(self):
        if cmds.workspaceControl(self.MAIN_WINDOW, q=1, ex=1):
            cmds.deleteUI(self.MAIN_WINDOW)

        self.win = cmds.workspaceControl(self.MAIN_WINDOW, l=self.MAIN_WINDOW, rt=1)

        self.layout()

        cmds.showWindow(self.win)

        cmds.scriptJob(e=['SceneOpened', self.add_items_in_namespace_menu], p=self.win, rp=1)


    def layout(self):
        self.row_lay_common_settings = {'cw2':(80, 100),
                                   'cl2':['center', 'left'],
                                   'ct2':['right', 'left'],
                                   'h':24}

        self.frm_lay_common_settings = {'cll':1}

        menuBarLayout = cmds.menuBarLayout(p=self.win)
        cmds.menu(label='Maya Menu')
        cmds.menuItem(label='Optimize Scene', c='mel.eval("OptimizeSceneOptions;")')

        # cmds.menuItem(label='Save Settings', c=self.save_settings)
        # cmds.menuItem(label='Reset Settings', c=self.reset_settings)
        # cmds.menuItem(label='Reload Settings', c=self.load_settings)
        # cmds.menuItem(d=1)
        # cmds.menuItem(label='Reload', c=self.all_reload)
        # cmds.menuItem(label='ReferenceEditor', c='cmds.ReferenceEditor()')

        self.scl_lay = cmds.scrollLayout(p=self.MAIN_WINDOW, cr=1)

        self.nss_ops_menu = cmds.optionMenu(l='NameSpace')
        self.add_items_in_namespace_menu()

        self.plot_lay(self.scl_lay)
        self.del_animLayers_lay(self.scl_lay)
        self.run_all_lay(self.scl_lay)

        cmds.setParent('..')


    def list_namespaces(self):
        exclude_list = ['UI', 'shared']

        current = cmds.namespaceInfo(cur=1)
        cmds.namespace(set=':')
        namespaces = ['{}'.format(ns) for ns in cmds.namespaceInfo(lon=1) if ns not in exclude_list]
        cmds.namespace(set=current)

        return namespaces

    def load_menuItems(self, array=None, parent=None):
        for item in array:
            cmds.menuItem(l=item, p=parent)

    def add_items_in_namespace_menu(self):
        namespaces = self.list_namespaces()
        cmds.optionMenu(self.nss_ops_menu, e=1, dai=1)
        cmds.menuItem(l='', p=self.nss_ops_menu)
        self.load_menuItems(array=namespaces, parent=self.nss_ops_menu)

    def change_managed(self, *args, **kwargs):
        print(args, kwargs)

    # Plot
    def plot_lay(self, parent=None):
        # correct
        # self.cor_mch_frm_lay = cmds.frameLayout(p=parent, l='Correct Match', **self.frm_lay_common_settings)

        cmds.separator(p=parent, st='in')
        self.cor_mch_all_cb = cmds.checkBox(l='Correct Match', v=1, p=parent)
        self.cor_mch_row = cmds.rowLayout(adj=5, p=parent, nc=6, **self.row_lay_common_settings)

        self.l_hand_cor_mch_cb = cmds.checkBox(l='Left Hand', v=1, p=self.cor_mch_row)
        self.r_hand_cor_mch_cb = cmds.checkBox(l='Right Hand', v=1, p=self.cor_mch_row)
        self.l_foot_cor_mch_cb = cmds.checkBox(l='Left Foot', v=1, p=self.cor_mch_row)
        self.r_foot_cor_mch_cb = cmds.checkBox(l='Right Foot', v=1, p=self.cor_mch_row)
        cmds.button(l='Done!', c=self.cor_mch_main)


    def cor_mch_main(self, *args):
        namespace = cmds.optionMenu(self.nss_ops_menu, q=1, v=1)
        if not namespace:
            namespace = ''
        elif not namespace.endswith(':'):
            namespace = namespace + ':'

        self.l_hand_cor_mch_val = cmds.checkBox(self.l_hand_cor_mch_cb, q=1, v=1)
        self.r_hand_cor_mch_val = cmds.checkBox(self.r_hand_cor_mch_cb, q=1, v=1)
        self.l_foot_cor_mch_val = cmds.checkBox(self.l_foot_cor_mch_cb, q=1, v=1)
        self.r_foot_cor_mch_val = cmds.checkBox(self.r_foot_cor_mch_cb, q=1, v=1)

        try:
            refresh_tool_correctMatch(namespace=namespace,
                              l_hand=self.l_hand_cor_mch_val,
                              r_hand=self.r_hand_cor_mch_val,
                              l_foot=self.l_foot_cor_mch_val,
                              r_foot=self.r_foot_cor_mch_val)
        except:
            print(traceback.format_exc())


    # Delete AnimationLayers
    def del_animLayers_lay(self, parent=None):
        # correct
        # self.dal_frm_lay = cmds.frameLayout(p=parent, l='Delete AnimLayers', **self.frm_lay_common_settings)

        cmds.separator(p=parent, st='in')
        self.dal_all_cb = cmds.checkBox(l='Delete AnimLayers', v=1, p=parent)
        self.dal_row = cmds.rowLayout(adj=3, p=parent, nc=6, **self.row_lay_common_settings)

        self.dal_cb = cmds.checkBox(l='Exclude BaseAnimation', v=1, p=self.dal_row)
        self.dar_cb = cmds.checkBox(l='Rename animCurves', v=1, p=self.dal_row)
        cmds.button(l='Done!', c=self.del_animLayers_main)


    def del_animLayers_main(self, *args):
        self.dal_cb_val = cmds.checkBox(self.dal_cb, q=1, v=1)
        self.dar_cb_val = cmds.checkBox(self.dar_cb, q=1, v=1)
        try:
            refresh_tool_delete_all_animLayers(exclude_baseAnimation=self.dal_cb_val, rename_animCurves=self.dar_cb_val)
        except:
            print(traceback.format_exc())


    # Run All
    def run_all_lay(self, parent=None):
        cmds.separator(p=parent, st='in')

        self.check_all_row = cmds.rowLayout(adj=2, p=parent, nc=6, **self.row_lay_common_settings)
        self.check_all_cb = cmds.checkBox(l='All Check', v=1, p=self.check_all_row, cc=self.all_check)
        cmds.button(l='Run All!', p=self.check_all_row, c=self.run_all)


    def all_check(self, args):
        cmds.checkBox(self.cor_mch_all_cb, e=1, v=args)
        cmds.checkBox(self.dal_all_cb, e=1, v=args)


    def run_all(self, *args):
        self.cor_mch_all_cb_val = cmds.checkBox(self.cor_mch_all_cb, q=1, v=1)
        if self.cor_mch_all_cb_val:
            self.cor_mch_main()

        self.dal_all_cb_val = cmds.checkBox(self.dal_all_cb, q=1, v=1)
        if self.dal_all_cb_val:
            self.del_animLayers_main()



def get_trs_attrs(obj=None, local=None, pos=True, rot=True, scl=True, roo=True):
    """
    return translate, rotate, scale, rotateOrder, jointOrient
    """
    if not obj:
        sel = cmds.ls(os=1)
        if sel:
            obj = sel[0]
        else:
            return

    rel = 0
    wld = 1

    get_t = None
    get_ro = None
    get_s = None
    get_roo = None
    get_jo = None

    if local:
        rel = 1
        wld = 0

    if pos:
        get_t = cmds.xform(obj, q=1, t=1, ws=wld, os=rel)
    if rot:
        get_ro = cmds.xform(obj, q=1, ro=1, ws=wld, os=rel)
    if scl:
        get_s = cmds.xform(obj, q=1, s=1, ws=wld, os=rel)
    if roo:
        get_roo = cmds.xform(obj, q=1, roo=1)

    if cmds.objectType(obj) == 'joint':
        get_jo = cmds.getAttr(obj+'.jo')
        get_jo = get_jo[0]
        # cmds.setAttr(sel[0]+'.jo', *get_jo[0])

    return get_t, get_ro, get_s, get_roo, get_jo


def get_pole_vec(start=None, mid=None, end=None, move=None):
    startV = om.MVector(start[0] ,start[1],start[2])
    midV = om.MVector(mid[0] ,mid[1],mid[2])
    endV = om.MVector(end[0] ,end[1],end[2])
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
    matrixV = [arrowV.x , arrowV.y , arrowV.z , 0 ,cross1.x ,cross1.y , cross1.z , 0 ,cross2.x , cross2.y , cross2.z , 0,0,0,0,1]
    matrixM = om.MMatrix()
    om.MScriptUtil.createMatrixFromList(matrixV , matrixM)
    matrixFn = om.MTransformationMatrix(matrixM)
    rot = matrixFn.eulerRotation()

    pvLoc = cmds.spaceLocator(n='poleVecPosLoc')
    cmds.xform(pvLoc[0] , ws =1 , t= (finalV.x , finalV.y ,finalV.z))
    cmds.xform(pvLoc[0] , ws = 1 , rotation = ((rot.x/math.pi*180.0),(rot.y/math.pi*180.0),(rot.z/math.pi*180.0)))
    cmds.select(pvLoc[0])
    cmds.move(move, 0, 0, r=1, os=1, wd=1)

    pv_val = get_trs_attrs(obj=pvLoc[0])

    cmds.delete(pvLoc)
    cmds.select(cl=True)

    return pv_val


def refresh_tool_correctMatch(namespace=None, l_hand=None, r_hand=None, l_foot=None, r_foot=None):
    ##################
    # ik components
    ##################
    # ik_l_hand
    ik_l_hand_src_array = [namespace + 'proxy_armL_jnt',
     namespace + 'proxy_forearmL_jnt',
     namespace + 'proxy_handL_jnt',
     namespace + 'handL_match_loc',
     namespace + 'proxy_handL_jnt']

    ik_l_hand_dst_array = [namespace + 'handL_ctl',
     namespace + 'forearmL_ctl',
     namespace + 'handL_rot_ctl']

    ik_l_hand_ikfk_switch = namespace + 'handL_ikfk_ctl'


    # ik_r_hand
    ik_r_hand_src_array = [namespace + 'proxy_armR_jnt',
     namespace + 'proxy_forearmR_jnt',
     namespace + 'proxy_handR_jnt',
     namespace + 'handR_match_loc',
     namespace + 'proxy_handR_jnt']

    ik_r_hand_dst_array = [namespace + 'handR_ctl',
     namespace + 'forearmR_ctl',
     namespace + 'handR_rot_ctl']

    ik_r_hand_ikfk_switch = namespace + 'handR_ikfk_ctl'


    # ik_l_foot
    ik_l_foot_src_array = [namespace + 'proxy_uplegL_jnt',
     namespace + 'proxy_legL_jnt',
     namespace + 'proxy_footL_jnt',
     namespace + 'footL_match_loc',
     namespace + 'proxy_toebaseL_jnt']

    ik_l_foot_dst_array = [namespace + 'footL_ctl',
     namespace + 'legL_ctl',
     namespace + 'toebaseL_ctl']

    ik_l_foot_ikfk_switch = namespace + 'footL_ikfk_ctl'


    # ik_r_foot
    ik_r_foot_src_array = [namespace + 'proxy_uplegR_jnt',
     namespace + 'proxy_legR_jnt',
     namespace + 'proxy_footR_jnt',
     namespace + 'footR_match_loc',
     namespace + 'proxy_toebaseR_jnt']

    ik_r_foot_dst_array = [namespace + 'footR_ctl',
     namespace + 'legR_ctl',
     namespace + 'toebaseR_ctl']

    ik_r_foot_ikfk_switch = namespace + 'footR_ikfk_ctl'


    ##################
    # fk components
    ##################
    # ik_l_hand
    fk_l_hand_src_array = [namespace + 'proxy_armL_jnt',
     namespace + 'proxy_forearmL_jnt',
     namespace + 'proxy_handL_jnt']

    fk_l_hand_dst_array = [namespace + 'fk_armL_ctl',
     namespace + 'fk_forearmL_ctl',
     namespace + 'fk_handL_ctl']

    # ik_r_hand
    fk_r_hand_src_array = [namespace + 'proxy_armR_jnt',
     namespace + 'proxy_forearmR_jnt',
     namespace + 'proxy_handR_jnt']

    fk_r_hand_dst_array = [namespace + 'fk_armR_ctl',
     namespace + 'fk_forearmR_ctl',
     namespace + 'fk_handR_ctl']

    # ik_l_foot
    fk_l_foot_src_array = [namespace + 'proxy_uplegL_jnt',
     namespace + 'proxy_legL_jnt',
     namespace + 'proxy_footL_jnt',
     namespace + 'proxy_toebaseL_jnt']

    fk_l_foot_dst_array = [namespace + 'fk_uplegL_ctl',
     namespace + 'fk_legL_ctl',
     namespace + 'fk_footL_ctl',
     namespace + 'fk_toebaseL_ctl']

    # ik_r_foot
    fk_r_foot_src_array = [namespace + 'proxy_uplegR_jnt',
     namespace + 'proxy_legR_jnt',
     namespace + 'proxy_footR_jnt',
     namespace + 'proxy_toebaseR_jnt']

    fk_r_foot_dst_array = [namespace + 'fk_uplegR_ctl',
     namespace + 'fk_legR_ctl',
     namespace + 'fk_footR_ctl',
     namespace + 'fk_toebaseR_ctl']

    correct_flips = [namespace + 'proxy_handL_jnt',
                     namespace + 'proxy_handR_jnt']

    def refresh_func(start=None, end=None, match_type=None):
        """
        match_type = 'l_hand'
        match_type = 'r_hand'
        match_type = 'l_foot'
        match_type = 'r_foot'
        """

        if match_type == 'l_hand':
            src_array = ik_l_hand_src_array
            dst_array = ik_l_hand_dst_array
            ikfk_switch = ik_l_hand_ikfk_switch
            fk_src_array = fk_l_hand_src_array
            fk_dst_array = fk_l_hand_dst_array

        if match_type == 'r_hand':
            src_array = ik_r_hand_src_array
            dst_array = ik_r_hand_dst_array
            ikfk_switch = ik_r_hand_ikfk_switch
            fk_src_array = fk_r_hand_src_array
            fk_dst_array = fk_r_hand_dst_array

        elif match_type == 'l_foot':
            src_array = ik_l_foot_src_array
            dst_array = ik_l_foot_dst_array
            ikfk_switch = ik_l_foot_ikfk_switch
            fk_src_array = fk_l_foot_src_array
            fk_dst_array = fk_l_foot_dst_array

        elif match_type == 'r_foot':
            src_array = ik_r_foot_src_array
            dst_array = ik_r_foot_dst_array
            ikfk_switch = ik_r_foot_ikfk_switch
            fk_src_array = fk_r_foot_src_array
            fk_dst_array = fk_r_foot_dst_array


        setkey_attrs = mel.eval('string $selectedChannelBox[] = `channelBox -query -selectedMainAttributes mainChannelBox`;')
        if setkey_attrs == []:
            setkey_attrs =  [u'tx', u'ty', u'tz', u'rx', u'ry', u'rz', u'sx', u'sy', u'sz']

        # ik match
        save_items = OrderedDict()
        for i in range (int(start), int(end+1)):
            cmds.currentTime(i, e=True)
            values = OrderedDict()
            # IK trs
            values[dst_array[0]] = get_trs_attrs(obj=src_array[3])

            # Pole Vec
            values[dst_array[1]] = get_pole_vec(start=get_trs_attrs(obj=src_array[0])[0],
                                        mid=get_trs_attrs(obj=src_array[1])[0],
                                        end=get_trs_attrs(obj=src_array[2])[0],
                                        move=20)

            # IK rot
            get_roo = cmds.xform(src_array[4], q=1, roo=1)
            if src_array[4] in correct_flips:
                cmds.xform(src_array[4], p=1, roo='xyz')

            values[dst_array[2]] = get_trs_attrs(obj=src_array[4])

            if src_array[4] in correct_flips:
                cmds.xform(src_array[4], p=0, roo=get_roo)

            save_items[str(i)] = values


        for frame, obj_array in save_items.items():
            # print(frame, obj_array)
            for obj, value in obj_array.items():
                # print(obj, value)

                # print(obj, value)
                cmds.currentTime(float(frame), e=True)
                cmds.xform(obj, t=value[0], ro=value[1], a=1, ws=1)
                cmds.setKeyframe(obj, at=setkey_attrs)

                cmds.setAttr(ikfk_switch+'.ikfk', 1.0)
                cmds.setKeyframe(ikfk_switch, at=['ikfk'])


        # fk match
        save_items = OrderedDict()
        for i in range (int(start), int(end+1)):
            cmds.currentTime(i, e=True)
            values = OrderedDict()
            for j, (fk_dst, fk_src) in enumerate(zip(fk_dst_array, fk_src_array)):

                get_roo = cmds.xform(fk_src, q=1, roo=1)
                if fk_src in correct_flips:
                    cmds.xform(fk_src, p=1, roo='xyz')

                values[fk_dst] = get_trs_attrs(obj=fk_src)

                if fk_src in correct_flips:
                    cmds.xform(fk_src, p=0, roo=get_roo)

            save_items[str(i)] = values


        for frame, obj_array in save_items.items():
            for obj, value in obj_array.items():
                cmds.currentTime(float(frame), e=True)
                cmds.xform(obj, t=value[0], ro=value[1], a=1, ws=1)
                cmds.setKeyframe(obj, at=setkey_attrs)

        filter_ctrls = dst_array + fk_dst_array
        cmds.filterCurve(filter_ctrls, f='euler')

    ##############################
    cur_time=cmds.currentTime(q=1)

    if cmds.autoKeyframe(q=True, st=True):
        autoKeyState = 1
    else:
        autoKeyState = 0

    cmds.autoKeyframe(st=0)

    gPlayBackSlider = mel.eval('$temp=$gPlayBackSlider')
    if gPlayBackSlider:
        if cmds.timeControl(gPlayBackSlider, q=True, rv=True):
            frameRange = cmds.timeControl(gPlayBackSlider, q=True, ra=True)
            start = frameRange[0]
            end = frameRange[1]
        else:
            frameRange = cmds.currentTime(q=1)
            start = frameRange
            end = frameRange-1

    try:
        cmds.undoInfo(ock=1)
        cmds.refresh(su=1)

        if l_hand:
            refresh_func(start=start, end=end, match_type='l_hand')
        if r_hand:
            refresh_func(start=start, end=end, match_type='r_hand')
        if l_foot:
            refresh_func(start=start, end=end, match_type='l_foot')
        if r_foot:
            refresh_func(start=start, end=end, match_type='r_foot')

        cmds.refresh(su=0)
        cmds.undoInfo(cck=1)

    except Exception as e:
        cmds.refresh(su=0)

        print(traceback.format_exc())

    cmds.autoKeyframe(state=autoKeyState)

    cmds.currentTime(cur_time)


def refresh_tool_delete_all_animLayers(exclude_baseAnimation=None, rename_animCurves=None):
    mel.eval('source "C:/Program Files/Autodesk/Maya{}/scripts/others/performAnimLayerMerge.mel"'.format(cmds.about(version=True)))

    deleteMerged = True
    if cmds.optionVar(exists='animLayerMergeDeleteLayers'):
        deleteMerged = cmds.optionVar(query='animLayerMergeDeleteLayers')

    cmds.optionVar(intValue=('animLayerMergeDeleteLayers', 1))

    animLayers = cmds.ls(type='animLayer')
    if animLayers:
        mel.eval('animLayerMerge {"%s"}' % '","'.join(animLayers))

        if exclude_baseAnimation:
            if 'BaseAnimation' in animLayers:
                animLayers.remove('BaseAnimation')

        [cmds.delete(anl) for anl in animLayers if cmds.objExists(anl)]

    if rename_animCurves:
        def custom_rename(obj=None, rplname=None):
            if cmds.objExists(obj):
                cmds.rename(obj, rplname)

        animCurves = cmds.ls(type=['animCurveTL', 'animCurveTA', 'animCurveTU'])
        not_connects = []
        error_crvs = []
        for ancv in animCurves:
            connected_plug = cmds.listConnections(ancv, d=1, p=1, scn=1) or None
            if not connected_plug:
                not_connects.append(ancv)

            else:
                spl_connected_plugs = re.split('[:\[\].]', connected_plug[0].split(':')[-1])
                spl_connected_plugs_remove_empty = [cprm for cprm in spl_connected_plugs if not cprm == '']
                spl_connected_plug = '_'.join(spl_connected_plugs_remove_empty)
                custom_rename(ancv, spl_connected_plug)


def interactive_space_match(ctrl=None, space=None, spaces=None):
    currentPickerNamespace = mel.eval('MGP_GetCurrentPickerNamespace')

    if currentPickerNamespace:
        currentPickerNamespace = currentPickerNamespace + ':'
    else:
        currentPickerNamespace = ''

    hand_rot_ctrl = None
    if ctrl == "handL_ctl":
        rot_ctrl = currentPickerNamespace+"handL_rot_ctl"
        wt, wr = cmds.xform(currentPickerNamespace+ctrl, q=1, t=1, ws=1), cmds.xform(rot_ctrl, q=1, ro=1, ws=1)
    elif ctrl == "handR_ctl":
        rot_ctrl = currentPickerNamespace+"handR_rot_ctl"
        wt, wr = cmds.xform(currentPickerNamespace+ctrl, q=1, t=1, ws=1), cmds.xform(rot_ctrl, q=1, ro=1, ws=1)
    else:
        rot_ctrl = currentPickerNamespace+ctrl
        wt, wr = cmds.xform(currentPickerNamespace+ctrl, q=1, t=1, ws=1), cmds.xform(rot_ctrl, q=1, ro=1, ws=1)

    for elsp in spaces:
        try:
            cmds.setAttr(currentPickerNamespace+'{}.{}'.format(ctrl, elsp), 0)
        except:
            pass

    cmds.setAttr(currentPickerNamespace+'{}.{}'.format(ctrl, space), 1)

    cmds.xform(currentPickerNamespace+ctrl, t=wt, ws=1)
    cmds.xform(rot_ctrl, ro=wr, ws=1)


import math
from collections import OrderedDict
import re
import traceback
import maya.cmds as cmds
import maya.mel as mel

def renameDuplicates(duplicated=None, prefix=''):
    #Find all objects that have the same shortname as another
    #We can indentify them because they have | in the name
    duplicates = [f for f in duplicated if '|' in f]
    #Sort them by hierarchy so that we don't rename a parent before a child.
    duplicates.sort(key=lambda obj: obj.count('|'), reverse=True)

    #if we have duplicates, rename them
    renamed = []
    if duplicates:
        for name in duplicates:
            # extract the base name
            m = re.compile("[^|]*$").search(name)
            shortname = m.group(0)

            # extract the numeric suffix
            m2 = re.compile(".*[^0-9]").match(shortname)
            if m2:
                stripSuffix = m2.group(0)
            else:
                stripSuffix = shortname

            #rename, adding '#' as the suffix, which tells maya to find the next available number
            newname = cmds.rename(name, (prefix + stripSuffix))

            renamed.append(newname)

        return renamed

    else:
        return duplicated

def simplebake(objects, start):
    try:
        cmds.refresh(su=1)
        cmds.bakeResults(objects,
                         at=['rx', 'ry', 'rz', 'tx', 'ty', 'tz'],
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
                         t=((cmds.playbackOptions(q=1, min=1), cmds.playbackOptions(q=1, max=1))),
                         disableImplicitControl=True,
                         controlPoints=False)
        cmds.refresh(su=0)

    except:
        cmds.refresh(su=0)

    cmds.currentTime(start)

def ikpv_cnst(prefix, dst, start, mid, end, move, bake_sets, cnst_sets):
    loc1 = cmds.spaceLocator()
    loc2 = cmds.duplicate(loc1)
    loc3 = cmds.duplicate(loc1)
    cmds.parent(loc3, loc2)
    cmds.parent(loc2, loc1)

    cmds.sets(loc1, add=bake_sets)
    cmds.sets(loc2, add=bake_sets)
    cmds.sets(loc3, add=bake_sets)


    po = cmds.pointConstraint(start, loc1, w=1)
    cmds.pointConstraint(end, loc1, w=1)
    # cmds.delete(po)

    # cmds.matchTransform(loc1, start, pos=1, rot=1, scl=0)
    if ('forearmL_ctl' in dst
        or 'forearmR_ctl' in dst):
        cmds.move(0, 0, 5, r=1, os=1, wd=1)

        if 'L_' in dst:
            wuo = '{}armL_jnt'.format(prefix)

        if 'R_' in dst:
            wuo = '{}armR_jnt'.format(prefix)

        cmds.aimConstraint(mid, loc2, w=1, aim=(0,0,1), u=(0,1,0), wut='objectrotation', wu=(0,1,0), wuo=wuo)
        cmds.move(0, 0, move, loc3, r=1, os=1, wd=1)


    elif ('legL_ctl' in dst
        or 'legR_ctl' in dst):
        cmds.move(0, 0, -15, loc2, r=1, os=1, wd=1)

        if 'L_' in dst:
            wuo = '{}uplegL_jnt'.format(prefix)

        if 'R_' in dst:
            wuo = '{}uplegR_jnt'.format(prefix)

        cmds.aimConstraint(mid, loc2, w=1, aim=(0,0,1), u=(0,1,0), wut='objectrotation', wu=(0,1,0), wuo=wuo)
        cmds.move(0, 0, move, loc3, r=1, os=1, wd=1)

    cmds.orientConstraint(wuo, loc1[0], w=1, mo=1)

    cmds.matchTransform(loc3, dst)
    po = cmds.pointConstraint(loc3, dst)
    cmds.sets(po, add=cnst_sets)



def euler_to_quaternion(yaw, pitch, roll, order):
    yaw = math.radians(yaw)
    pitch = math.radians(pitch)
    roll = math.radians(roll)

    if (order == 'xyz'):
        qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
        qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
        qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
        qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)

    elif (order == 'yzx'):
        qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
        qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) - math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
        qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
        qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)

    elif (order == 'zxy'):
        qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
        qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) - math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
        qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
        qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)

    elif (order == 'xzy'):
        qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
        qy = math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) + math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
        qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
        qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)

    elif (order == 'yxz'):
        qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
        qy = math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) + math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
        qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
        qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)

    elif (order == 'zyx'):
        qx = math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2) + math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2)
        qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) - math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
        qz = math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) + math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
        qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)


    return [qx, qy, qz, qw]

def quaternion_to_euler(x, y, z, w):
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    X = math.degrees(math.atan2(t0, t1))

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    Y = math.degrees(math.asin(t2))

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    Z = math.degrees(math.atan2(t3, t4))

    return X, Y, Z


def crop_rotation(degree):
    if (degree > 180):
        return degree -360

    elif (degree < -180):
        return degree + 360

    else:
        return degree



def convertRotateOrder(sel=None, root_jnt = 'root_jnt', prefix = 'dummybake_', nss = '', ik_pv=None,
                       startFrame = None, endFrame = None, order = 'xyz', delete_dummy=None, correct_anim=None,
                       external=None):

    roo = {'xyz':0,
           'yzx':1,
           'zxy':2,
           'xzy':3,
           'yxz':4,
           'zyx':5}

    if not sel:
        sel = cmds.ls(os=1)

    all_dummy_bake_sets = 'all_dummy_bake_sets'
    if not cmds.objExists(all_dummy_bake_sets):
        cmds.sets(n=all_dummy_bake_sets, em=1)

    else:
        cmds.select(all_dummy_bake_sets, ne=1)
        [cmds.delete(obj) for obj in cmds.pickWalk(d='down') if cmds.objExists(obj)]
        cmds.sets(n=all_dummy_bake_sets, em=1)

    dummy_bake_sets = 'dummy_bake_sets'
    if not cmds.objExists(dummy_bake_sets):
        cmds.sets(n=dummy_bake_sets, em=1)

    cmds.sets(dummy_bake_sets, add=all_dummy_bake_sets)

    if external:
        dummy_bake_ctl_sets = 'dummy_bake_ctl_sets'
        if not cmds.objExists(dummy_bake_ctl_sets):
            cmds.sets(n=dummy_bake_ctl_sets, em=1)

        cmds.sets(dummy_bake_ctl_sets, add=all_dummy_bake_sets)

        dummy_bake_ctl_cnst_sets = 'dummy_bake_ctl_cnst_sets'
        if not cmds.objExists(dummy_bake_ctl_cnst_sets):
            cmds.sets(n=dummy_bake_ctl_cnst_sets, em=1)

        cmds.sets(dummy_bake_ctl_cnst_sets, add=all_dummy_bake_sets)

    dummy_bake_cnst_sets = 'dummy_bake_cnst_sets'
    if not cmds.objExists(dummy_bake_cnst_sets):
        cmds.sets(n=dummy_bake_cnst_sets, em=1)

    cmds.sets(dummy_bake_cnst_sets, add=all_dummy_bake_sets)


    ct = cmds.currentTime(q=1)

    dups = cmds.duplicate(root_jnt)

    renamed_dups = renameDuplicates(dups, prefix)

    cmds.parent(prefix+root_jnt.split(':')[-1], w=1)


    for obj in renamed_dups:
        if cmds.objectType(obj) == 'joint':
            cmds.sets(obj, add=dummy_bake_sets)

            listConnections = cmds.listConnections(obj, c=1, p=1)
            src_break = None
            dst_break = None
            for con in listConnections:
                if 'drawInfo' in con:
                    src_break = con

                if 'drawOverride' in con:
                    dst_break = con

            if src_break and dst_break:
                cmds.disconnectAttr(src_break, dst_break)


        if cmds.objectType(obj) == ('parentConstraint' or 'pointConstraint' or 'orientConstraint'):
            cmds.delete(obj)


    cmds.select(dummy_bake_sets, ne=1)
    sorted_renamed_dups = cmds.pickWalk(d='down')
    sorted_renamed_dups.sort()

    root_children = cmds.ls(root_jnt, dag=1, type='joint')
    root_children.sort()

    pacs = []
    for i, (orig, rdup) in enumerate(zip(root_children, sorted_renamed_dups)):
        pac = cmds.parentConstraint(orig, rdup, w=1)
        pacs.append(pac[0])


    simplebake(sorted_renamed_dups, ct)


    cmds.delete(pacs)


    if ik_pv:
        armL_iks = ['{}forearmL_ctl'.format(nss), '{}armL_jnt'.format(prefix), '{}forearmL_jnt'.format(prefix), '{}handL_jnt'.format(prefix)]
        armR_iks = ['{}forearmR_ctl'.format(nss), '{}armR_jnt'.format(prefix), '{}forearmR_jnt'.format(prefix), '{}handR_jnt'.format(prefix)]

        legL_iks = ['{}legL_ctl'.format(nss),'{}uplegL_jnt'.format(prefix), '{}legL_jnt'.format(prefix), '{}footL_jnt'.format(prefix)]
        legR_iks = ['{}legR_ctl'.format(nss),'{}uplegR_jnt'.format(prefix), '{}legR_jnt'.format(prefix), '{}footR_jnt'.format(prefix)]

        ikpv_cnst(prefix, armL_iks[0], armL_iks[1], armL_iks[2], armL_iks[3], 60, dummy_bake_sets, dummy_bake_cnst_sets)
        ikpv_cnst(prefix, armR_iks[0], armR_iks[1], armR_iks[2], armR_iks[3], 60, dummy_bake_sets, dummy_bake_cnst_sets)

        ikpv_cnst(prefix, legL_iks[0], legL_iks[1], legL_iks[2], legL_iks[3], 60, dummy_bake_sets, dummy_bake_cnst_sets)
        ikpv_cnst(prefix, legR_iks[0], legR_iks[1], legR_iks[2], legR_iks[3], 60, dummy_bake_sets, dummy_bake_cnst_sets)


    bodyparts = ['root', 'camera', 'hip', 'cog', 'spine', 'neck', 'head',
               'shoulder', 'arm', 'forearm', 'hand',
               'foot', 'toebase', 'upleg', 'leg']

    base_ctrls = []
    # ik rot
    for part in bodyparts:
        if part in bodyparts[7:]:
            for side in ['L', 'R']:
                if part in ['foot']:
                    loc = cmds.spaceLocator()
                    cmds.matchTransform(loc[0], nss+part+side+'_ctl')
                    cmds.parent(loc[0], prefix+part+side+'_jnt')
                    ori = cmds.orientConstraint(loc[0], nss+part+side+'_ctl', w=1, mo=1)
                    base_ctrls.append(nss+part+side+'_ctl')
                elif part in ['shoulder', 'toebase']:
                    ori = cmds.orientConstraint(prefix+part+side+'_jnt', nss+part+side+'_ctl', w=1, mo=1)
                    base_ctrls.append(nss+part+side+'_ctl')
                elif part in ['hand']:
                    ori = cmds.orientConstraint(prefix+part+side+'_jnt', nss+part+side+'_rot_ctl', w=1, mo=1)
                    base_ctrls.append(nss+part+side+'_rot_ctl')
                cmds.sets(ori, add=dummy_bake_cnst_sets)
        elif part == 'spine':
            for i in range(3):
                ori = cmds.orientConstraint(prefix+part+'_'+str(i+1).zfill(2)+'_jnt', nss+part+'_'+str(i+1).zfill(2)+'_ctl', w=1, mo=1)
                base_ctrls.append(nss+part+'_'+str(i+1).zfill(2)+'_ctl')
                cmds.sets(ori, add=dummy_bake_cnst_sets)
        elif part == 'camera':
            pass
        elif part == 'root':
            ori = cmds.orientConstraint(prefix+part+'_jnt', nss+part+'_pos_ctl', w=1, mo=1)
            base_ctrls.append(nss+part+'_pos_ctl')
            cmds.sets(ori, add=dummy_bake_cnst_sets)
        else:
            ori = cmds.orientConstraint(prefix+part+'_jnt', nss+part+'_ctl', w=1, mo=1)
            base_ctrls.append(nss+part+'_ctl')
            cmds.sets(ori, add=dummy_bake_cnst_sets)

    # ik pos
    for part in bodyparts:
        if part in ['hand','foot']:
            for side in ['L', 'R']:
                poc = cmds.pointConstraint(prefix+part+side+'_jnt', nss+part+side+'_ctl', w=1, mo=1)
                base_ctrls.append(nss+part+side+'_ctl')
                cmds.sets(poc, add=dummy_bake_cnst_sets)
        elif part in ['camera', 'cog']:
            poc = cmds.pointConstraint(prefix+part+'_jnt', nss+part+'_ctl', w=1, mo=1)
            base_ctrls.append(nss+part+'_ctl')
            cmds.sets(poc, add=dummy_bake_cnst_sets)
        elif part in ['root']:
            poc = cmds.pointConstraint(prefix+part+'_jnt', nss+part+'_pos_ctl', w=1, mo=1)
            base_ctrls.append(nss+part+'_pos_ctl')
            cmds.sets(poc, add=dummy_bake_cnst_sets)

    if sel:
        base_ctrls = [bctrl for bctrl in base_ctrls if bctrl in sel]

    base_ctrls = list(set(base_ctrls))


    if external:
        dummy_bake_ctl_gp = 'dummy_bake_ctl_gp'
        if not cmds.objExists(dummy_bake_ctl_gp):
            cmds.createNode('transform', n=dummy_bake_ctl_gp, ss=1)

        cmds.sets(dummy_bake_ctl_gp, add=dummy_bake_ctl_sets)

        base_ctrls.sort()
        base_ctrls_locs = []
        base_ctrls_loc_cnsts = []
        for ctrl in base_ctrls:
            bc = cmds.spaceLocator(n='{}_dummy_bake_loc'.format(ctrl.split(':')[-1]))
            cmds.setAttr('{}.rotateOrder'.format(bc[0]), k=1)
            cmds.parent(bc[0], dummy_bake_ctl_gp)
            base_ctrls_locs.append(bc[0])
            cmds.sets(bc[0], add=dummy_bake_ctl_sets)
            bpac = cmds.parentConstraint(ctrl, bc[0], w=1)
            base_ctrls_loc_cnsts.append(bpac[0])
            cmds.sets(bpac, add=dummy_bake_ctl_cnst_sets)

        c, p = 'handL_rot_ctl_dummy_bake_loc', 'handL_ctl_dummy_bake_loc'
        if cmds.objExists(c) and cmds.objExists(p):
            cmds.parent(c, p)

        c, p = 'handR_rot_ctl_dummy_bake_loc', 'handR_ctl_dummy_bake_loc'
        if cmds.objExists(c) and cmds.objExists(p):
            cmds.parent(c, p)

        simplebake(base_ctrls_locs, ct)
        cmds.delete(base_ctrls_loc_cnsts)

        loc_ctl_cnsts = [cmds.orientConstraint(obj, loc, w=1) for i, (obj, loc) in enumerate(zip(base_ctrls, base_ctrls_locs))]

    if external:
        for loc in base_ctrls_locs:
            cmds.setAttr('{}.rotateOrder'.format(loc), roo[order])

        simplebake(base_ctrls_locs, ct)
        locs_cnsts = cmds.ls(dummy_bake_ctl_gp, dag=1, type='orientConstraint')
        [cmds.delete(obj) for obj in locs_cnsts if cmds.objExists(obj)]

    if sel:
        if not external:
            for obj in sel:
                cmds.setAttr('{}.rotateOrder'.format(obj), roo[order])
        # print('{} Set Order:'.format(obj), order)
    # for obj in sel:
    #     listAttrs = cmds.listAttr(obj, k=1) or None
    #     if listAttrs:
    #         for at in listAttrs:
    #             if 'blendOrient' in at:
    #                 cmds.setAttr('{}.{}'.format(obj, at), 0)

        simplebake(sel, ct)


    if correct_anim:
        if sel:
            if startFrame == None:
                playmin = cmds.playbackOptions(q=1, min=1)
            else:
                playmin = startFrame

            if endFrame == None:
                playmax = cmds.playbackOptions(q=1, max=1)
            else:
                playmax = endFrame

            x = int(playmin)
            for i in range(int(playmax)+1):
                f = i + x
                cmds.currentTime(f)
                for obj in sel:
                    # q1 = euler_to_quaternion(roll=cmds.getAttr('{}.rx'.format(obj)),
                    #                   pitch=cmds.getAttr('{}.ry'.format(obj)),
                    #                   yaw=cmds.getAttr('{}.rz'.format(obj)),
                    #                   order='xyz')

                    # qtoe = quaternion_to_euler(*q1)
                    qtoe = cmds.xform(obj, q=1, ro=1, os=1)

                    cmds.xform('{}'.format(obj), ro=[crop_rotation(qtoe[0]), crop_rotation(qtoe[1]), crop_rotation(qtoe[2])], a=1, os=1)

                    cmds.setKeyframe('{}.r'.format(obj), breakdown=0)


    if delete_dummy:
        cmds.select(all_dummy_bake_sets, ne=1)
        [cmds.delete(obj) for obj in cmds.pickWalk(d='down') if cmds.objExists(obj)]

    if external:
        if cmds.objExists(dummy_bake_sets):
            cmds.select(dummy_bake_sets, ne=1)
            [cmds.delete(obj) for obj in cmds.pickWalk(d='down') if cmds.objExists(obj)]

        print(base_ctrls_locs)
        print(base_ctrls)


        loc_ctl_cnsts = []
        for i, (loc, obj) in enumerate(zip(base_ctrls_locs, base_ctrls)):
            if ('foot' in loc.replace('_dummy_bake_loc', '')
                or 'cog' in loc.replace('_dummy_bake_loc', '')
                or 'pos' in loc.replace('_dummy_bake_loc', '')):
                poc = cmds.pointConstraint(loc, obj, w=1)
                oric = cmds.orientConstraint(loc, obj, w=1)

                loc_ctl_cnsts.append(poc)
                loc_ctl_cnsts.append(oric)

            elif 'camera' in loc.replace('_dummy_bake_loc', ''):
                poc = cmds.pointConstraint(loc, obj, w=1)

                loc_ctl_cnsts.append(poc)

            elif 'hand' in loc.replace('_dummy_bake_loc', ''):
                if '_rot_' in loc.replace('_dummy_bake_loc', ''):
                    oric = cmds.orientConstraint(loc, obj, w=1)

                    loc_ctl_cnsts.append(oric)

                else:
                    poc = cmds.pointConstraint(loc, obj, w=1)

                    loc_ctl_cnsts.append(poc)

            else:
                oric = cmds.orientConstraint(loc, obj, w=1)

                loc_ctl_cnsts.append(oric)

        for ocnst in loc_ctl_cnsts:
            cmds.sets(ocnst, add=dummy_bake_ctl_sets)


    cmds.filterCurve(sel, f='euler')

    cmds.currentTime(ct)

    if sel:
        cmds.select(sel, r=1)


def convertRotateOrderFunc(sel=None, root_jnt = 'ref:root_jnt', prefix = 'dummybake_', nss = 'ref:', ik_pv=True,
                       startFrame = None, endFrame = None, order = 'xyz', delete_dummy=None, correct_anim=None,
                       external=None):
    try:
        cmds.refresh(su=1)
        convertRotateOrder(sel, root_jnt, prefix, nss, ik_pv, startFrame, endFrame, order, delete_dummy, correct_anim, external)
        cmds.refresh(su=0)
    except Exception as e:
        print(traceback.format_exc())
        cmds.refresh(su=0)


# convertRotateOrderFunc(sel=None, root_jnt = 'male00_all1000_mdl_def:root_jnt', prefix = '', nss = 'male00_all1000_mdl_def:', ik_pv=False,
#                        startFrame = None, endFrame = None, order = 'yxz', delete_dummy=False, correct_anim=True, external=True)

# get joints distance
def get_distance(objA, objB):
    gObjA = cmds.xform(objA, q=True, t=True, ws=True)
    gObjB = cmds.xform(objB, q=True, t=True, ws=True)

    return math.sqrt(math.pow(gObjA[0]-gObjB[0],2)+math.pow(gObjA[1]-gObjB[1],2)+math.pow(gObjA[2]-gObjB[2],2))

# def build_softik(self):
def create_softik_locators(nss=None, jointList=None, softik_ik_ctrl=None):
    jointList = [nss+jt for jt in jointList]
    softik_ik_ctrl = nss+softik_ik_ctrl
    softik_value = 20
    softik_axis = 'translateX'

    softik_loc_sets = '{}_softik_loc_sets'.format(softik_ik_ctrl)
    if not cmds.objExists(softik_loc_sets):
        cmds.sets(n=softik_loc_sets, em=1)

    else:
        cmds.select(softik_loc_sets, ne=1)
        [cmds.delete(obj) for obj in cmds.pickWalk(d='down') if cmds.objExists(obj)]
        cmds.sets(n=softik_loc_sets, em=1)


    softik_loc_gp = '{}_softik_loc_gp'.format(softik_ik_ctrl)
    if not cmds.objExists(softik_loc_gp):
        cmds.createNode('transform', n=softik_loc_gp, ss=1)

    length = 0.0
    i = 0
    for jnt in jointList:
        if i == 0:
            pass
        else:
            length += get_distance(jointList[i-1], jnt)
        i += 1

    # locators
    loc_a = '{}_softIkLoc'.format(jointList[0])
    loc_b = '{}_softIkLoc'.format(jointList[-1])
    loc_c = '{}_exp_softIkLoc'.format(jointList[-1])
    loc_d = '{}_aimobj_softIkLoc'.format(jointList[-1])

    locs = [loc_a, loc_b, loc_c, loc_d]

    [cmds.spaceLocator(n='{}'.format(loc)) for loc in locs]

    cmds.parent(loc_b, loc_a)
    cmds.parent(loc_c, loc_a)
    cmds.parent(loc_d, loc_a)

    # const
    const_loc = cmds.spaceLocator(n='{0}_const_softIkloc'.format(jointList[-1]))
    # cmds.matchTransform(const_loc[0], softik_ik_ctrl)

    pac = cmds.parentConstraint(softik_ik_ctrl, const_loc[0], w=1)
    simplebake([const_loc[0]], cmds.currentTime(q=1))
    cmds.delete(pac)

    cmds.pointConstraint(jointList[0], loc_a, w=1)
    cmds.pointConstraint(const_loc[0], loc_b, w=1)
    cmds.matchTransform(loc_d, const_loc[0])
    cmds.parent(loc_d, const_loc[0])
    cmds.move(0, 0, 10, loc_d, r=1, os=1, wd=1)
    cmds.setAttr('{0}.v'.format(loc_a), 0)
    cmds.setAttr('{0}.v'.format(loc_d), 0)

    aimConst_options = {}
    aimConst_options['offset'] = [0,0,0]
    aimConst_options['aimVector'] = [1,0,0]
    aimConst_options['upVector'] = [0,0,1]
    aimConst_options['worldUpType'] = "object"
    aimConst_options['worldUpObject'] = loc_d

    cmds.aimConstraint(const_loc[0], loc_a, w=1, **aimConst_options)
    cmds.pointConstraint(loc_c, softik_ik_ctrl, w=1)

    # softik_ik_ctrl = const_loc[0]
    # addAttr
    if 'softIk' not in cmds.listAttr(const_loc[0]):
        cmds.addAttr(const_loc[0], ln='softIk', k=1, at='double', dv=0, min=0, max=softik_value)
        cmds.setAttr('{}.{}'.format(const_loc[0], 'softIk'), l=0)
    else:
        cmds.deleteAttr(const_loc[0], at='softIk')
        cmds.addAttr(const_loc[0], ln='softIk', k=1, at='double', dv=0, min=0, max=softik_value)
        cmds.setAttr('{}.{}'.format(const_loc[0], 'softIk'), l=0)

    exp = cmds.createNode('expression', n='{}_softIkExp'.format(softik_ik_ctrl))
    cmds.expression(exp, e=1, s=u"""\nif ({0}.{1} > ({2} - {3}.softIk))\n\t{4}.{1} = ({2} - {3}.softIk) + {3}.softIk * (1-exp( -({0}.{1} - ({2} - {3}.softIk)) /{5}));\nelse\n\t{4}.{1} = {0}.{1}""".format(loc_b, softik_axis, length, const_loc[0], loc_c, softik_value), ae=0, uc='all')

    cmds.parent(const_loc[0], softik_loc_gp)
    cmds.parent(loc_a, softik_loc_gp)

    cmds.sets(softik_loc_gp, add=softik_loc_sets)
    cmds.sets(const_loc[0], add=softik_loc_sets)
    cmds.sets(loc_a, add=softik_loc_sets)
    cmds.sets(exp, add=softik_loc_sets)

    cmds.select(const_loc[0], r=1)
