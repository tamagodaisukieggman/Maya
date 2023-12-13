# -*- coding: utf-8 -*-
u"""plyリグ"""


def _get_left_and_right_ctrls(id_, typ=0):
    u"""左右のコントローラー名を取得

    :param id_: 識別子
    :param typ: 0 'Ctrl', 1 'fkCtrl', 2 'PVCtrl', 3 'PBCtrl'
    :return: (leftCtrl, rightCtrl)
    """
    left = 'L'
    right = 'R'
    ctrl = 'Ctrl'  # 0
    fk_ctrl = 'fkCtrl'  # 1
    pv_ctrl = 'PVCtrl'  # 2
    pb_ctrl = 'PBCtrl'  # 3

    left_ctrl, right_ctrl = None, None

    if typ == 0:
        left_ctrl = u'{}_{}_{}'.format(id_, left, ctrl)
        right_ctrl = u'{}_{}_{}'.format(id_, right, ctrl)
    elif typ == 1:
        left_ctrl = u'{}_{}_{}'.format(id_, left, fk_ctrl)
        right_ctrl = u'{}_{}_{}'.format(id_, right, fk_ctrl)
    elif typ == 2:
        left_ctrl = u'{}_{}_{}'.format(id_, left, pv_ctrl)
        right_ctrl = u'{}_{}_{}'.format(id_, right, pv_ctrl)
    elif typ == 3:
        left_ctrl = u'{}_{}_{}'.format(id_, left, pb_ctrl)
        right_ctrl = u'{}_{}_{}'.format(id_, right, pb_ctrl)

    return left_ctrl, right_ctrl


def _get_old_left_and_right_proxy_jts(id_, ):
    u"""左右のMcProxyJtを取得 (旧McProxyJt用)

    :param id_: 識別子
    :return: (leftMcProxyJt, rightMcProxyJt)
    """
    left = 'left'
    right = 'right'
    jt = 'McProxyJt'

    left_jt = u'{}{}{}'.format(left, id_, jt)
    right_jt = u'{}{}{}'.format(right, id_, jt)

    return left_jt, right_jt


def _get_left_and_right_proxy_jts(id_, left_index, right_index):
    u"""左右のMcProxyJtを取得

    :param id_: 識別子
    :param left_index: 左のインデックス
    :param right_index: 右のインデックス
    :return: (leftMcProxyJt, rightMcProxyJt)
    """
    left = 'L'
    right = 'R'
    jt = 'mcProxyJt'

    left_jt = u'j{i:02d}_{id}_{lr}_{jt}'.format(i=left_index, id=id_, lr=left, jt=jt)
    right_jt = u'j{i:02d}_{id}_{lr}_{jt}'.format(i=right_index, id=id_, lr=right, jt=jt)

    return left_jt, right_jt


def _get_left_and_right_locators(id_):
    u"""左右の制御用Locatorを取得

    :param id_: 識別子
    :return:
    """
    left = 'L'
    right = 'R'
    loc = 'loc'

    left_locator = u'{}_{}_{}'.format(id_, left, loc)
    right_locator = u'{}_{}_{}'.format(id_, right, loc)

    # left_locator = u'{}_{}'.format(id_, left)
    # right_locator = u'{}_{}'.format(id_, right)

    return left_locator, right_locator


class OldCtrlPly00(object):
    u"""Ctrl Ply00 (旧リグ)"""
    hip = 'hipCtrl'

    spine_a = 'spineACtrl'
    spine_b = 'spineBCtrl'

    neck = 'neckCtrl'
    head = 'headCtrl'

    hand = 'hand'
    hand_l, hand_r = _get_left_and_right_ctrls(hand, 0)
    wrist = 'wrist'
    wrist_l, wrist_r = _get_left_and_right_ctrls(wrist, 0)
    arm = 'arm'
    arm_pv_l, arm_pv_r = _get_left_and_right_ctrls(arm, 3)
    shoulder = 'shoulder'
    shoulder_l, shoulder_r = _get_left_and_right_ctrls(shoulder, 0)

    leg = 'leg'
    leg_l, leg_r = _get_left_and_right_ctrls(leg, 0)
    leg_pv_l, leg_pv_r = _get_left_and_right_ctrls(leg, 2)


class CtrlPly00(OldCtrlPly00):
    u"""Ctrl Ply00"""
    hip = 'hip_Ctrl'

    spine_a = 'spineA_Ctrl'
    spine_b = 'spineB_Ctrl'

    neck = 'neck_Ctrl'
    head = 'head_Ctrl'

    arm = 'arm'
    arm_pv_l, arm_pv_r = _get_left_and_right_ctrls(arm, 2)


class OldMcProxyJtPly00(object):
    u"""McProxyJt Ply00 (旧リグ)"""

    arm = 'Arm'
    arm_l, arm_r = _get_old_left_and_right_proxy_jts(arm)
    forearm = 'ForeArm'
    forearm_l, forearm_r = _get_old_left_and_right_proxy_jts(forearm)
    shoulder = 'Shoulder'
    shoulder_l, shoulder_r = _get_old_left_and_right_proxy_jts(shoulder)

    leg = 'Leg'
    leg_l, leg_r = _get_old_left_and_right_proxy_jts(leg)
    upleg = 'UpLeg'
    upleg_l, upleg_r = _get_old_left_and_right_proxy_jts(upleg)


class McProxyJtPly00(object):
    u"""McProxyJt Ply00"""
    arm = 'arm'
    arm_l, arm_r = _get_left_and_right_proxy_jts(arm, 15, 35)
    forearm = 'foreArm'
    forearm_l, forearm_r = _get_left_and_right_proxy_jts(forearm, 16, 36)
    shoulder = 'shoulder'
    shoulder_l, shoulder_r = _get_left_and_right_proxy_jts(shoulder, 14, 34)

    leg = 'leg'
    leg_l, leg_r = _get_left_and_right_proxy_jts(leg, 3, 7)
    upleg = 'upleg'
    upleg_l, upleg_r = _get_left_and_right_proxy_jts(upleg, 2, 6)


class LocatorPly00(object):
    u"""制御用Locator"""

    turntable = 'turnTable_loc'
    foots = 'foots_loc'

    hip = 'hip_loc'

    spine_a = 'spineA_loc'
    spine_b = 'spineB_loc'

    neck = 'neck_loc'
    head = 'head_loc'

    waist = 'waist_loc'
    chest = 'chest_loc'

    hand = 'hand'
    hand_l, hand_r = _get_left_and_right_locators(hand)
    wrist = 'wrist'
    wrist_l, wrist_r = _get_left_and_right_locators(wrist)
    dmy_hand = 'dmyHand'
    dmy_hand_l, dmy_hand_r = _get_left_and_right_locators(dmy_hand)
    palm = 'palm'
    palm_l, palm_r = _get_left_and_right_locators(palm)
    dmy_palm = 'dmyPalm'
    dmy_palm_l, dmy_palm_r = _get_left_and_right_locators(dmy_palm)

    forearm = 'foreArm'
    forearm_l, forearm_r = _get_left_and_right_locators(forearm)
    arm = 'arm'
    arm_l, arm_r = _get_left_and_right_locators(arm)
    arm_pv = 'armPV'
    arm_pv_l, arm_pv_r = _get_left_and_right_locators(arm_pv)

    shoulder = 'shoulder'
    shoulder_l, shoulder_r = _get_left_and_right_locators(shoulder)

    leg = 'leg'
    leg_r, leg_l = _get_left_and_right_locators(leg)
    leg_pv = 'legPV'
    leg_pv_l, leg_pv_r = _get_left_and_right_locators(leg_pv)
    knee = 'knee'
    knee_r, knee_l = _get_left_and_right_locators(knee)
    foot = 'foot'
    foot_r, foot_l = _get_left_and_right_locators(foot)
