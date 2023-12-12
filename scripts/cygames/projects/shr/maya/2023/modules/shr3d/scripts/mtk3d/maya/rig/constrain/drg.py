# -*- coding: utf-8 -*-
u"""drgリグ"""


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
    pv_ctrl = 'BPoleVectorCtrl'  # 2
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


# dragon rig-------------------------------------------------------------------
class CtrlDrg00(object):
    u"""dragon rig """
    cog = 'cogCtrl'

    footF = 'footF'
    footF_l, footF_r = _get_left_and_right_ctrls(footF, 0)
    arm = 'arm'
    footF_pv_l, footF_pv_r = _get_left_and_right_ctrls(arm, 2)

    foot = "foot"
    foot_l, foot_r = _get_left_and_right_ctrls(foot, 0)
    leg = 'leg'
    foot_pv_l, foot_pv_r = _get_left_and_right_ctrls(leg, 2)


class LocatorDrg00(object):
    u"""制御用Locator"""

    turntable = 'turnTable_loc'
    foots = 'foots_loc'

    cog = 'cog_loc'

    footF = 'footF'
    footF_l, footF_r = _get_left_and_right_locators(footF)
    footF_pv = 'footFPV'
    footF_pv_l, footF_pv_r = _get_left_and_right_locators(footF_pv)

    foot = 'foot'
    foot_r, foot_l = _get_left_and_right_locators(foot)

    foot_pv = 'footPV'
    foot_pv_l, foot_pv_r = _get_left_and_right_locators(foot_pv)
