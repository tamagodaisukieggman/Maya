# -*- coding=utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

u"""
name: autocreate_rig/command.py
data: 2021/10/18
ussage: priari 用 Rig 自動作成ツール
version: 2.72
​
"""

try:
    # Maya 2022-
    from builtins import str
    from builtins import range
    from builtins import object
    from importlib import reload
except:
    pass

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
from maya.api import OpenMaya as om
import re
import os
import math
from collections import OrderedDict
from . import fix_joint
from . import const
#from .utils import Utils
# from .check import Check
from . import check
from . import utils

reload(fix_joint)
reload(check)
reload(utils)
reload(const)
Check = check.Check
Utils = utils.Utils

from logging import getLogger



logger = getLogger(__name__)
TOOL_VERSION = 'Ver 2.72'


# ----------------------------------------------------------------------------------------------------------------------
# GET FUNCTION
# ----------------------------------------------------------------------------------------------------------------------
def get_main(target=None):
    u"""
        ノード名からネームスペース取得
        :param target: str
        :return: ex_dict コントローラ対象ジョイントリスト
    """
    ex_dict = {}
    sels = pm.ls(sl = True)
    if sels:
        grp_name = sels[0]
        ex_dict = get_ex_node(grp_name, target)
        return ex_dict
    else:
        return ex_dict


def get_ex_node(grp=None, target=None):
    u"""
        グループ以下のEX FK/SplineIK ジョイントリスト取得
        :param grp: str or PyNode
        :param target: str
        :return: EX FK/SplineIK ジョイントリスト
    """

    ex_sik_list = []
    ex_fk_list = []
    ex_dict = OrderedDict()

    ns = Utils.get_namespace(grp)
    sim = "{}_".format(const.PREFIX_SIM)
    root_bone = Utils.get_pynode(grp, ns + const.ROOTJOINTNAME)

    if root_bone:
        joint_list = pm.listRelatives(root_bone, c = True, ad = True, type = 'joint', f = True) or []
        for joint in joint_list:
            j_name = str(joint.stripNamespace().nodeName())
            # ============================== SIM対応===============================
            if sim in j_name:
                orig_name = j_name
                if Utils.get_label(j_name) in const.SECONDARYJOINTNAME_LIST:
                    j_name = orig_name.replace(sim, "")  # print("Secondary: {} > {}".format(orig_name, j_name))
                else:
                    j_name = orig_name.replace(sim, "EX_")  # print("EX: {} > {}".format(orig_name, j_name))
            # =====================================================================
            j_label = Utils.get_label(j_name)
            c_2nd_childs = joint.getChildren(type="joint")
            c_2nd_count = len(c_2nd_childs)
            c_nodes = pm.listRelatives(joint, c=True, ad=True, type='joint', f=True) or []
            c_count = len(c_nodes)
            # print("joint:", joint, " c_2nd_count: ", c_2nd_count, " c_count:", c_count)

            if c_count:
                # if re.match('^EX_.+_(00)$', j_name) and not ('SplineIK' in j_name):
                # bustジョイント末尾が00では無いケースがあるので、例外サフィックスとして指定
                if re.match('.+_(00|bust)$', j_name) and Utils.get_label(joint) not in const.PRIMARYJOINTNAME_LIST:
                    p_j = joint.getParent()
                    p_j_name = p_j.stripNamespace().nodeName()
                    p_label = Utils.get_label(p_j_name)
                    arm_leg_list = const.ARMJOINTNAME_LIST + const.LEGJOINTNAME_LIST
                    is_arm_leg_parent = True if p_label in arm_leg_list else False

                    # 末端までのchildカウント 2以上、直下のchildカウント 1、Parent名末尾に"_00"もしくは"_bust"が付かない
                    if c_count > 1 and c_2nd_count == 1 and not re.match('.+_(00|bust)$', p_j_name):

                        # 00とend ジョイントの basenameが一致しない
                        is_valid_end = False
                        end_joints = [j for j in c_nodes if re.match('.+_End$', j.nodeName())]
                        for end_joint in end_joints:

                            end_joint = end_joint.fullPath().replace(joint.fullPath(), "")
                            for basename in end_joint.split("|")[1:]:

                                if Utils.get_label(basename) in const.SECONDARYJOINTNAME_LIST:
                                    basename = basename.replace(sim, "")
                                else:
                                    basename = basename.replace(sim, "EX_")
                                # Endまでのジョイントベース名がルートと違う場合はis_validはFalseのまま
                                if basename.split("_")[:-1] != j_name.split("_")[:-1]:
                                    # is_valid = False
                                    # print(basename, basename.split("_")[:-1], j_name.split("_")[:-1])
                                    break
                                is_valid_end = True

                        # 階層とSuffixがあっているか
                        is_valid = True
                        for cj in c_nodes:
                            cj_path = cj.fullPath()
                            depth_list = cj_path.replace(joint.fullPath(), j_name).split("|")
                            for num, name in enumerate(depth_list):
                                suffix = name.split("_")[-1]
                                if suffix != "End" and num != int(suffix):
                                    is_valid = False
                                    break

                        # TODO 複雑化してるので要リファクタリング
                        # 親がarmかlegの一部の場合　→　FK
                        if is_arm_leg_parent:
                            # print("ex_fk0:", j_name)
                            ex_fk_list.append(j_name)
                            ex_dict.update({j_name: dict(sik=False, node=joint)})

                        elif len(p_j.getChildren(type="joint")) > 1 and re.match('^EX_.+_[0-9][0-9]$', p_j_name):
                            # print("ex_fk1:", j_name)
                            ex_fk_list.append(j_name)
                            ex_dict.update({j_name: dict(sik=False, node=joint)})

                        elif not is_valid and not is_valid_end:
                            # print(">>>>> ", j_name, is_valid, is_valid_end)
                            print(("ex_fk2:", j_name))
                            ex_fk_list.append(j_name)
                            ex_dict.update({j_name: dict(sik=False, node=joint)})

                        elif not is_valid and is_valid_end and j_label not in const.SECONDARYJOINTNAME_LIST:
                            # print("ex_fk3:", j_name)
                            ex_fk_list.append(j_name)
                            ex_dict.update({j_name: dict(sik=False, node=joint)})

                        elif not is_valid and is_valid_end and j_label in const.SECONDARYJOINTNAME_LIST:
                            # print("ex_ik2:", j_name)
                            ex_sik_list.append(j_name)
                            ex_dict.update({j_name: dict(sik=True, node=joint)})

                        else:
                            # print("ex_sik:", j_name)
                            ex_sik_list.append(j_name)
                            ex_dict.update({j_name: dict(sik=True, node=joint)})

                    else:
                        # print("ex_fk:", j_name)
                        ex_fk_list.append(j_name)
                        ex_dict.update({j_name: dict(sik=False, node=joint)})

    if target == 'fk':
        # print("ex_fk_list:", ex_fk_list)
        return ex_fk_list

    elif target == 'sik':
        # print("ex_sik_list:", ex_sik_list)
        return ex_sik_list

    elif target is None:
        return ex_dict
    else:
        return ex_dict


def get_global_transform(node):
    u"""
        絶対値でtransform値を取得
        :param node:
        :return: 絶対値座標
    """
    # forPyNode
    if isinstance(node, pm.PyNode):
        node = node.longName()
    srt = []
    srt.extend(pm.xform(node, q = True, ws = True, a = True, t = True))
    srt.extend(pm.xform(node, q = True, ws = True, a = True, ro = True))
    srt.extend(pm.xform(node, q = True, ws = True, a = True, s = True))
    return srt


def get_root_parent(node):
    u"""
        親ノード取得
        :param node:
    """
    label = Utils.get_label(node)
    parents = pm.listRelatives(node, p = True)
    if parents:
        if label in parents[0]:
            return get_root_parent(node)
    return node


def get_sik_info(node):
    if node is None:
        return

    sik_dict = dict(ordered_joints = [], parent = None)
    spline_joints = get_spline_joints(node)
    parent = node.getParent()

    if spline_joints and parent:
        sik_dict["ordered_joints"].extend(spline_joints)
        sik_dict["parent"] = parent
        return sik_dict

    return None


def get_spline_joints(node):
    u"""
        node以下の階層ジョイント取得、複数の子階層があればNone
        :param node:
        :return: list of PyNode or None
    """
    if node is None:
        return

    dag_children = pm.ls(node, dag = True, type = "joint")
    for child in dag_children:
        if len(child.getChildren(type = "joint")) > 1:
            return

    return dag_children


def get_child(node, type=None):
    u"""
        子ノード取得
        :param node:

    """
    kwargs = dict(c = True) if type is None else dict(c = True, type = type)

    if pm.listRelatives(node, **kwargs):
        return pm.listRelatives(node, **kwargs)[0]
    else:
        return None


# TODO 取得方法が安定していないのでリファクタリング予定
def get_end_child(node):
    u"""
        子ノード取得
        :param node:
    """
    if not isinstance(node, pm.PyNode):
        node = pm.PyNode(node)

    if not node.getChildren():
        return node

    return get_end_child(node.getChildren()[0])


# TODO 取得方法が安定していないのでリファクタリング予定
def get_ik_child(node):
    u"""
        一階層下の子ノード取得
        :param node:
    """
    c_node = get_child(node)

    return get_child(c_node)


def get_root_bone(name=const.ROOTJOINTNAME):
    u"""
        ルートジョイントを取得
    """
    node = pm.ls(sl = True, type = 'joint')
    if len(node) > 0 and name in node[0]:
        return node[0]
    else:
        logger.warning('root ボーンが選択されていません。')
        return None


def get_intermediate_translate(node_a, node_b):
    u"""
        指定した2つのノードの中間値を取得
        :param node_a:
        :param node_b:
        :return: 中間の移動値
    """

    srt_a = get_global_transform(node_a)
    srt_b = get_global_transform(node_b)

    trans = []
    trans.append(int(srt_b[0] + srt_a[0]) / 2)
    trans.append(int(srt_b[1] + srt_a[1]) / 2)
    trans.append(int(srt_b[2] + srt_a[2]) / 2)

    return trans


def get_skincluster(name):
    u"""
        指定名のノードからスキンクラスターを取得
        :param str name:
        :return: str skincluster　or  None
    """
    if name.startswith("|"):
        name = name[1:]
    return mel.eval('findRelatedSkinCluster {}'.format(name))


# TODO 要Selection keep
def get_execution_dict(joint_list, center_list=const.C_JOINTNAME_LIST, arm_list=const.ARMJOINTNAME_LIST,
                       hand_list=const.HANDJOINTNAME_LIST, leg_list=const.LEGJOINTNAME_LIST,
                       secondary_list=const.SECONDARYJOINTNAME_LIST):
    u"""
        ジョイントリストからリグ作成工程に必要な部位分けと実行順番を設定した辞書を作成
        :param joint_list: list of joint str
        :param center_list: list of joint str
        :param arm_list: list of joint str
        :param hand_list: list of joint str
        :param leg_list: list of joint str
        :param secondary_list: list of joint str
        :return: dict {"center":[PyNode,,],"ex":[PyNode,,],"arm":[PyNode,,],
                        "hand":[PyNode,,],"leg":[PyNode,,], "secondary":[PyNode,,], }

    """
    if joint_list is None:
        return

    joint_dict = OrderedDict()

    for joint in joint_list:
        joint_dict[str(joint.stripNamespace().nodeName())] = joint

    if joint_dict.get(const.ROOTJOINTNAME):
        joint_dict.pop(const.ROOTJOINTNAME)

    # pprint(joint_dict.items())
    execution_dict = OrderedDict(center = [], arm = [], hand = [], leg = [], secondary = [], ex = [])

    lr_list = ['L_', 'R_']
    c_prefix = 'C_'
    ex_prefix = 'EX_'

    # secondary_list = secondary_list
    center_list = [c_prefix + center for center in center_list]
    arm_list = [lr + arm for lr in lr_list for arm in arm_list]
    hand_list = [lr + hand for lr in lr_list for hand in hand_list]
    leg_list = [lr + leg for lr in lr_list for leg in leg_list]

    # first center order list
    for c in center_list:
        val = joint_dict.get(c, None)
        if val:
            # print(">> ", val)
            execution_dict["center"].append(val)
            joint_dict.pop(c)

    # EX order list
    for k, val in list(joint_dict.items()):
        if k.startswith(ex_prefix):
            # print(">> ", val)
            execution_dict["ex"].append(val)
            joint_dict.pop(k)

    # arm order list
    for arm in arm_list:
        for k, val in list(joint_dict.items()):
            if k.startswith(arm):
                # print(">>arm ", k, type(k), val, type(val))
                execution_dict["arm"].append(val)
                joint_dict.pop(k)
                break

    # hand order list
    for hand in hand_list:
        for k, val in list(joint_dict.items()):
            if k.startswith(hand):
                # print(">>hand ", k, type(k), val, type(val))
                execution_dict["hand"].append(val)
                joint_dict.pop(k)
                break

    # leg order list
    for leg in leg_list:
        for k, val in list(joint_dict.items()):
            if k.startswith(leg):
                # print(">>leg ", k, type(k), val, type(val))
                execution_dict["leg"].append(val)
                joint_dict.pop(k)
                break

    # secondary は "C_", "L_", "R_","B_" があるのでひとまず順番づけは保留。
    execution_dict["secondary"] = list(joint_dict.values())

    return execution_dict


# ----------------------------------------------------------------------------------------------------------------------
# SET FUNCTION
# ----------------------------------------------------------------------------------------------------------------------
def set_global_transform(node, srt):
    u"""
        transform値を絶対値で設定する
        :param node:
        :param srt:[tx, ty, tz, rx, ry, rz, sx, sy, sz]
    """
    pm.xform(node, ws = True, a = True, t = srt[0:3])
    pm.xform(node, ws = True, a = True, ro = srt[3:6])
    pm.xform(node, ws = True, a = True, s = srt[6:9])


def set_global_translate(node, srt):
    u"""
        transform値を絶対値で設定する
        :param node:
        :param srt:[tx, ty, tz, rx, ry, rz, sx, sy, sz]
    """
    pm.xform(node, ws = True, a = True, t = srt[0:3])
    pm.xform(node, ws = True, a = True, ro = [0, 0, 0])  # pm.xform(node, ws=True, a=True, s=srt[6:9])


def set_wire_color(node, index=0):
    u"""
        アトリビュートの表示カラーを設定
        :param str node: string or PyNode
        :param int index:
    """
    if not isinstance(node, pm.PyNode):
        node = pm.PyNode(node)

    targets = node.getShapes() if node.getShapes() else [node]
    for target in targets:
        try:
            pm.setAttr("{}.overrideEnabled".format(target), 1)
            pm.setAttr("{}.overrideColor".format(target), index)
        except Exception as e:
            print(e)


def set_lock_srt(node, t=False, r=False, s=False):
    u"""
        ノードのSRTアトリビュートロック
        :param node: PyNode
        :param t: bool
        :param r: bool
        :param s: bool
        :return: bool
    """

    try:
        if t:  # Translate
            pm.setAttr('{}.tx'.format(node), lock = True, k = False)
            pm.setAttr('{}.ty'.format(node), lock = True, k = False)
            pm.setAttr('{}.tz'.format(node), lock = True, k = False)
        if r:  # Rotate
            pm.setAttr('{}.rx'.format(node), lock = True, k = False)
            pm.setAttr('{}.ry'.format(node), lock = True, k = False)
            pm.setAttr('{}.rz'.format(node), lock = True, k = False)
        if s:  # Scale
            pm.setAttr('{}.sx'.format(node), lock = True, k = False)
            pm.setAttr('{}.sy'.format(node), lock = True, k = False)
            pm.setAttr('{}.sz'.format(node), lock = True, k = False)
        return True

    except Exception as e:
        print(e)
        return False


def set_hair_scale_lock(name):
    u"""
        スケール値 y, z のロックとハイド
        :param name:
    """
    # pm.setAttr('{}.sx'.format(name), lock=True, k=False)
    pm.setAttr('{}.sy'.format(name), lock = True, k = False)
    pm.setAttr('{}.sz'.format(name), lock = True, k = False)


def set_drivenkey(driver=None, driven=None, type="bow", key_list=const.DRIVEN_KEY_LIST):
    u"""
        セットドリブンキーのセット
        :param driver: str of node
        :param driven: str of node
        :param type: str
        :param key_list: list of animation key values
        :return : bool

    """
    if driver is None or driven is None:
        return False

    if type == "bow":
        driver_attr = '{}.tx'.format(driver)
        driven_attr = '{}.tx'.format(driven)
        default_val = cmds.getAttr(driven_attr)
        for v in key_list:
            print("set DrivenKey: [Driver] {} [Driven] {} [Frame] {} [Value] {}".format(driver_attr, driven_attr, v[0],
                default_val + v[1]))
            cmds.setDrivenKeyframe(driven_attr, cd = driver_attr, dv = v[0], v = default_val + v[1])

    return True


# ----------------------------------------------------------------------------------------------------------------------
# CREATE FUNCTION
# ----------------------------------------------------------------------------------------------------------------------
def create_group(name, parent=None):
    u"""
    グループノード作成
    :param name: str name of group
    :param parent: PyNode
    :return node: Pynode
    """
    # return pm.group(em=True, n=name)
    if parent and pm.objExists(parent):
        node = pm.group(em = True, n = name, p = parent)
    else:
        node = pm.group(em = True, n = name)

    return node


def create_dummy(name, parent=None):
    u"""
    ダミーノード作成
    :param str name: 名前
    :param parent: PyNode
    :return node: Pynode
    """
    return create_group(name + '_null', parent = parent)


def create_offset(name, parent=None):
    u"""
    ダミーノード作成
    :param str name: 名前
    :param parent: PyNode
    :return node: Pynode
    """
    return create_group(name + '_offset', parent = parent)


def create_ikfk_controller(name, dict=None):
    u"""
    IKFK切り替えノード作成
    :param str name: 名前
    :param dict dict: 更新追加するdict
    :return ctrl, rev: Pynode, PyNode
    """
    ctrl = None

    if 'arm' in name:
        if name[:2] == 'L_':
            ctrl = create_wire('L_IKFK_arm', type = 'ikfk')
            pm.move(50, 50, 0, ctrl, a = True)
            rev = create_reverse('L_arm_reverse')
            pm.connectAttr('{}.ik0fk1'.format(ctrl), '{}.input.inputX'.format(rev), f = True)
            pm.setAttr('{}.visibility'.format(ctrl), k = False)

        elif name[:2] == 'R_':
            ctrl = create_wire('R_IKFK_arm', type = 'ikfk')
            pm.move(-50, 50, 0, ctrl, a = True)
            rev = create_reverse('R_arm_reverse')
            pm.connectAttr('{}.ik0fk1'.format(ctrl), '{}.input.inputX'.format(rev), f = True)
            pm.setAttr('{}.visibility'.format(ctrl), k = False)

    elif 'leg' in name:
        if name[:2] == 'L_':
            ctrl = create_wire('L_IKFK_leg', type = 'ikfk')
            pm.move(30, 0, 0, ctrl, a = True)
            rev = create_reverse('L_leg_reverse')
            pm.connectAttr('{}.ik0fk1'.format(ctrl), '{}.input.inputX'.format(rev), f = True)
            pm.setAttr('{}.visibility'.format(ctrl), k = False)

        elif name[:2] == 'R_':
            ctrl = create_wire('R_IKFK_leg', type = 'ikfk')
            pm.move(-30, 0, 0, ctrl, a = True)
            rev = create_reverse('R_leg_reverse')
            pm.connectAttr('{}.ik0fk1'.format(ctrl), '{}.input.inputX'.format(rev), f = True)
            pm.setAttr('{}.visibility'.format(ctrl), k = False)

    if dict and isinstance(ctrl, pm.PyNode):
        dict[ctrl.nodeName()] = ctrl

    return ctrl, rev


def create_controller(node, local=False, type='unique', offset=False, dict=None, parent=None, radius=None):
    u"""
    ワールド軸コントローラーノード作成
    :param str name: 名前
    :param str type: コントローラーワイヤーの種類
    :param bool offset: オフセット階層を作成するかどうか
    :param dict dict: 更新追加するdict
    :param PyNode parent: 階層下対象の親を指定
    :param float radius: コントローラーの大きさ
    :return null, ctrl: PyNode, PyNode
    """
    null = None
    ctrl = None

    # ns = Utils.get_namespace(node)
    srt = get_global_transform(node)
    name = Utils.get_name(node.stripNamespace().nodeName())

    # Dummyの削除
    if name[:5] == 'Dummy':
        name = name[6:]

    # ダミーとワイヤー作成
    if parent and pm.objExists(parent):
        null = create_dummy(name, parent = parent)
        ctrl = create_wire(name, type = type, parent = parent, radius = radius)
    else:
        null = create_dummy(name)
        ctrl = create_wire(name, type = type, radius = radius)

    if offset:
        # TODO parentフラグが無い場合を検討
        offset_node = create_offset(name, parent = parent)
        set_lock_srt(offset_node, s = True)
        pm.parent(ctrl, offset_node)
        pm.parent(offset_node, null)
    else:
        # 子、親
        pm.parent(ctrl, null)

    if local:
        set_global_transform(null, srt)
    else:
        set_global_translate(null, srt)

    pm.setAttr('{}.visibility'.format(ctrl), k = False)

    if dict and isinstance(null, pm.PyNode) and isinstance(ctrl, pm.PyNode):
        for pynode in [null, ctrl]:
            dict[pynode.nodeName()] = pynode

    return null, ctrl


def create_global_shadow_controller(node, srt, type='unique', offset=False, dict=None, parent=None):
    u"""
    ワールド軸コントローラーノード作成
    :param str name: 名前
    :param srt:[tx, ty, tz, rx, ry, rz, sx, sy, sz]
    :param str type: コントローラーワイヤーの種類
    :param bool offset: オフセット階層を作成するかどうか
    :param dict dict: 更新追加するdict
    :param PyNode parent: 階層下対象の親を指定
    :return null, ctrl: PyNode, PyNode
    """
    if isinstance(node, pm.PyNode):
        # ns = Utils.get_namespace(node)
        name = node.stripNamespace().nodeName()
        name = Utils.get_name(name)

    elif isinstance(node, str):
        name = Utils.get_name(node)

    else:
        print("Not String or PyNode:{}".format(node))
        return

    # Dummyの削除
    if name[:5] == 'Dummy':
        name = name[6:]

    # ダミーとワイヤー作成
    if parent and pm.objExists(parent):
        null = create_dummy(name, parent = parent)
        ctrl = create_wire(name, type, parent = parent)

    else:
        null = create_dummy(name)
        ctrl = create_wire(name, type)

    if offset:
        # TODO parentフラグが無い場合を検討
        offset_node = create_offset(name, parent = parent)
        set_lock_srt(offset_node, s = True)
        pm.parent(ctrl, offset_node)
        pm.parent(offset_node, null)

    else:
        # 子、親
        pm.parent(ctrl, null)

    set_global_translate(null, srt)
    pm.setAttr('{}.visibility'.format(ctrl), k = False)

    if dict:
        for pynode in [null, ctrl]:
            dict[pynode.nodeName()] = pynode

    return null, ctrl


def create_elbow_controller(node, type='unique', offset=False, dict=None, parent=None):
    u"""
    ひじ用のローカル、ワールドハイブリットコントローラーノード作成
    :param str name: 名前
    :param str type: コントローラーワイヤーの種類
    :param bool offset: オフセット階層を作成するかどうか
    :param PyNode parent: 階層下対象の親を指定
    :return null, ctrl: PyNode, PyNode
    """
    srt = get_global_transform(node)
    name = node.stripNamespace().nodeName()
    name = Utils.get_name(name)

    # Dummyの削除
    if name[:5] == 'Dummy':
        name = name[6:]

    # ダミーとワイヤー作成
    null = create_dummy(name, parent = parent)
    ctrl = create_wire(name, type, parent = parent)
    c_null = create_dummy(name, parent = parent)

    if offset:
        offset_node = create_offset(name)
        set_lock_srt(offset_node, s = True)
        pm.parent(c_null, offset_node)
        pm.parent(offset_node, null)
        pm.parent(ctrl, c_null)
    else:
        # 子、親
        pm.parent(ctrl, null)

    set_global_transform(null, srt)
    set_global_translate(c_null, srt)
    pm.setAttr('{}.visibility'.format(ctrl), k = False)

    if dict:
        if isinstance(ctrl, pm.PyNode):
            dict[ctrl.nodeName()] = ctrl
        if isinstance(null, pm.PyNode):
            dict[null.nodeName()] = null

    if offset:
        return null, ctrl, offset_node

    return null, ctrl


def create_wire(name, type='unique', parent=None, radius=None):
    u"""
    ワイヤーノード作成
    :param str name: 名前
    :param str type: 種類
    :param PyNode parent: 階層下対象の親を指定
    :param float radius: コントローラーの大きさ
    :return null, ctrl: PyNode, PyNode

    TODO: WIRE_GROUP, *_WIREのGlobal参照を検討
    """
    if name is None or name == "":
        name = type
    elif isinstance(name, str):
        name = name
    else:
        pass

    if type == 'oct':
        node = Utils.get_pynode(WIRE_GRP, const.WIRE_TYPE["OCTAHEDRON"])
    elif type == 'root':
        node = Utils.get_pynode(WIRE_GRP, const.WIRE_TYPE["ROOT"])
    elif type == 'ikfk':
        node = Utils.get_pynode(WIRE_GRP, const.WIRE_TYPE["IKFK"])
    elif type == 'pin':
        node = Utils.get_pynode(WIRE_GRP, const.WIRE_TYPE["PIN"])
    elif type == 'h_cross':
        node = Utils.get_pynode(WIRE_GRP, const.WIRE_TYPE["H_CROSS"])
    elif type == 'v_cross':
        node = Utils.get_pynode(WIRE_GRP, const.WIRE_TYPE["V_CROSS"])
    elif type == 'cube':
        node = Utils.get_pynode(WIRE_GRP, const.WIRE_TYPE["CUBE"])
    elif type == 'unique':
        node = Utils.get_pynode(WIRE_GRP, name[2:] + '_wire')
        if node is None:
            if 'tail' in name[2:]:
                node = Utils.get_pynode(WIRE_GRP, const.WIRE_TYPE["TAIL"])
            else:
                node = Utils.get_pynode(WIRE_GRP, const.WIRE_TYPE["CUBE"])
    elif type == 'wpn':
        node = Utils.get_pynode(WIRE_GRP, name + '_wire')
        node = node if node else Utils.get_pynode(WIRE_GRP, const.WIRE_TYPE["CUBE"])
    elif type == 'sphere':
        node = Utils.get_pynode(WIRE_GRP, const.WIRE_TYPE["SPHERE"])
    else:
        node = Utils.get_pynode(WIRE_GRP, const.WIRE_TYPE["SPHERE"])

    name = name + const.SUFFIX_CTRL

    # 保存しているWireに不要な値が入っていることがある為、リセット
    pm.setAttr('{}.rotate'.format(node), *[0, 0, 0], type = "double3")
    pm.setAttr('{}.scale'.format(node), *[1, 1, 1], type = "double3")
    dup_node = pm.duplicate(node, rc = False, n = name)[0]

    # need to rename for dupricate names
    dup_node.rename(name)
    # set radius for shape
    if radius and isinstance(radius, float):
        pm.setAttr('{}.scale'.format(dup_node), *[radius, radius, radius], type = "double3")
        pm.makeIdentity(dup_node, apply = True, t = 0, r = 0, s = 1, n = 0, pn = 0, jointOrient = 0)

    return dup_node


# class
class Wire(object):
    u"""
    ワイヤー作成クラス TODO 内包ノードのチェック

    """

    def __init__(self, wire_grp=None):
        if wire_grp is None or not isinstance(wire_grp, pm.PyNode):
            return
        self.wire_grp = wire_grp

    def create(self, name=None, type='unique', parent=None):
        u"""
        ワイヤーノード作成クラス
        :param str name: 名前

        """
        if name is None or name == "":
            name = type
        elif isinstance(name, str):
            name = name
        else:
            pass

        if type == 'oct':
            node = Utils.get_pynode(self.wire_grp, const.WIRE_TYPE["OCTAHEDRON"])
        elif type == 'root':
            node = Utils.get_pynode(self.wire_grp, const.WIRE_TYPE["ROOT"])
        elif type == 'ikfk':
            node = Utils.get_pynode(self.wire_grp, const.WIRE_TYPE["IKFK"])
        elif type == 'pin':
            node = Utils.get_pynode(self.wire_grp, const.WIRE_TYPE["PIN"])
        elif type == 'h_cross':
            node = Utils.get_pynode(self.wire_grp, const.WIRE_TYPE["H_CROSS"])
        elif type == 'v_cross':
            node = Utils.get_pynode(self.wire_grp, const.WIRE_TYPE["V_CROSS"])
        elif type == 'cube':
            node = Utils.get_pynode(self.wire_grp, const.WIRE_TYPE["CUBE"])
        elif type == 'unique':
            node = Utils.get_pynode(self.wire_grp, name[2:] + '_wire')
            if node is None:
                if 'tail' in name[2:]:
                    node = Utils.get_pynode(self.wire_grp, const.WIRE_TYPE["TAIL"])
                else:
                    node = Utils.get_pynode(self.wire_grp, const.WIRE_TYPE["CUBE"])
        elif type == 'wpn':
            node = Utils.get_pynode(self.wire_grp, name + '_wire')
            node = node if node else Utils.get_pynode(self.wire_grp, const.WIRE_TYPE["CUBE"])

        name = name + const.SUFFIX_CTRL
        # check node name Exists
        exists_node = Utils.get_pynode(self.wire_grp, name)
        if exists_node:
            pm.delete(exists_node)

        return pm.duplicate(node, rc = False, n = name)[0]


def create_ik_handle(start_joint, end_joint, parent=None):
    u"""
        IK作成
        :param PyNode start_joint:
        :param PyNode end_joint:
        :param PyNode parent:
        :return PyNode ikhandle

    """
    ik_name = '{}_ikHanlde'.format(end_joint)
    ik_handle = pm.ikHandle(sj = start_joint, ee = end_joint, sol = 'ikRPsolver', n = ik_name)
    pm.setAttr('{}.visibility'.format(ik_handle[0]), 0)

    if parent and pm.objExists(parent):
        pm.parent(ik_handle[0], parent)
        # parentされた場合にのみ重複名回避でリネーム処理
        ik_handle[0].rename(ik_name)

    return ik_handle[0]


def create_spline_ik_handle(start_joint, end_joint):
    u"""
        IK作成
        :param PyNode start_joint:
        :param PyNode end_joint:
        :return PyNode ik_handle, PyNode curve
    """
    ik_handle, eff, curve = pm.ikHandle(sj = start_joint, ee = end_joint, sol = 'ikSplineSolver',
                                        n = '{}_ikHanlde'.format(end_joint), simplifyCurve = False, numSpans = 2)
    pm.setAttr('{}.visibility'.format(ik_handle), 0)

    return ik_handle, curve


def create_upvector(ik_handle, upv_node):
    u"""
        ポールベクターコンストレイン作成
        :param str ik_handle: 名前
        :param str upv_node: 名前
        :return PyNode constraint
    """
    return pm.poleVectorConstraint(upv_node, ik_handle)


def create_constraint(target, source, mo=0, w=1, offset=[0, 0, 0], type='point'):
    u"""
       コンストレイン作成
        :param str [target ...]: 名前
        :param str source: 名前
        :param str type:
        :param bool mo:
        :param float w:
        :param list offset:
        :param str type: 種類
        :return PyNode constraint or None
    """
    if mo == 0:
        kwargs = dict(mo = mo, offset = offset, w = w)

    else:
        kwargs = dict(mo = mo, w = w)

    if type == 'point':
        return pm.pointConstraint(target, source, **kwargs)

    elif type == 'orient':
        return pm.orientConstraint(target, source, **kwargs)

    elif type == 'scale':
        kwargs.pop('mo')
        kwargs["offset"] = [1, 1, 1]
        return pm.scaleConstraint(target, source, **kwargs)

    elif type == 'parent':
        return pm.parentConstraint(target, source, mo = mo, w = w)

    else:
        return None


def create_ikfk_selection(j_node, ik_node, fk_node, ctrl_node, rev_node):
    u"""
       IK/FKセレクション作成
        :param PyNode j_node:
        :param PyNode ik_node:
        :param PyNode fk_node:
        :param PyNode ctrl_node:
        :param PyNode rev_node:
        :return bool:
    """

    # joint_name = Utils.get_name(j_node)

    # i = 2
    # if joint_name[:3] == 'EX_':
    #    i = 3
    # ik_name = const.DUMMY + joint_name[:i] + 'IK_' + joint_name[i:]
    # fk_name = const.DUMMY + joint_name[:i] + 'FK_' + joint_name[i:]

    if ik_node and fk_node and ctrl_node and rev_node:
        co_node = create_constraint((ik_node, fk_node), j_node, mo = 0, type = "orient")
        pm.connectAttr('{}.output.outputX'.format(rev_node), '{}.{}W0'.format(co_node, ik_node.nodeName()), f = True)
        pm.connectAttr('{}.ik0fk1'.format(ctrl_node), '{}.{}W1'.format(co_node, fk_node.nodeName()), f = True)
        return True

    return False


def create_ikfk_attr_selection(j_node, ik_node, fk_node, root_node, rev_node):
    u"""
       IK/FKセレクション作成
        :param PyNode j_node:
        :param PyNode ik_node:
        :param PyNode fk_node:
        :param PyNode ctrl_node:
        :param PyNode rev_node:
        :return bool:
    """
    # print(">>> ", j_node, ik_node, fk_node, root_node, rev_node)
    joint_name = Utils.get_name(j_node)

    # i = 2
    # if joint_name[:3] == 'EX_':
    #     i = 3
    # ik_name = const.DUMMY + joint_name[:i] + 'IK_' + joint_name[i:]
    # fk_name = const.DUMMY + joint_name[:i] + 'FK_' + joint_name[i:]

    if joint_name[:3] == 'EX_':
        label = 'ex_node'
    else:
        label = Utils.get_label(joint_name)

    if ik_node and fk_node and root_node and rev_node:
        co_node = create_constraint((ik_node, fk_node), j_node, mo = 0, type = "orient")
        pm.connectAttr('{}.output.outputX'.format(rev_node), '{}.{}W0'.format(co_node, ik_node.nodeName()), f = True)
        pm.connectAttr('{}.{}_CTRL_ik0fk1'.format(root_node, label), '{}.{}W1'.format(co_node, fk_node.nodeName()),
                       f = True)
        return True

    return False


def create_reverse(name):
    u"""
       リバースノード作成
        :param str name:
        :return PyNode:
    """
    return pm.shadingNode('reverse', n = name, au = True)


def create_multiplydivide(node, twist=None, attr="rotateX", val=0.5):
    u"""
        blendノードを作成して、
        指定した joint のik,fk用 joint から接続する。
        :param PyNode node:
        :param PyNode twist:
        :param str attr: attribute name
        :param float val: default 0.5
        :return PyNode or None
    """

    if node and node.hasAttr(attr) and twist:

        m_name = 'multiplyDivide_{}'.format(twist.stripNamespace().nodeName())
        m_node = pm.shadingNode('multiplyDivide', n = m_name, au = True)
        pm.setAttr('{}.input2X'.format(m_node), val)

        pm.connectAttr('{}.rotate.rotateX'.format(node), '{}.input1X'.format(m_node), f = True)
        pm.connectAttr('{}.output.outputX'.format(m_node), '{}.rotate.rotateX'.format(twist), f = True)
        return m_node

    else:
        return None


def create_dummy_group(grp=None, ex_sik=None):
    u"""
        grpノードとex_sikリストから、リグ作成に必要なダミージョイントを作成
        指定した joint のik,fk用 joint から接続する。
        :param PyNode or str grp:
        :param PyNode ex_sik:
        :return dict { name:PyNode,} or False
    """
    result_dict = OrderedDict()
    logger.info("-" * 72)

    if isinstance(grp, str):
        grp = pm.PyNode(grp) if pm.PyNode(grp) else None

    logger.info(u'ダミージョイント作成')
    if grp is None:
        logger.error(u'ダミージョイント作成失敗: {} グループがありません'.format(grp))
        return False

    logger.info("-" * 72)
    ns = Utils.get_namespace(grp)
    arm_list = const.ARMJOINTNAME_LIST
    leg_list = const.LEGJOINTNAME_LIST
    grp_dummy = create_group(const.GROUPDUMNAME, parent = grp)
    # save { String Name: Created PyNode }
    result_dict[const.GROUPDUMNAME] = grp_dummy
    pm.setAttr('{}.visibility'.format(grp_dummy), 0)
    root_bone = Utils.get_pynode(grp, ns + const.ROOTJOINTNAME)
    pyjoint_list = Utils.get_pyjoints(root_bone)

    if not pyjoint_list:
        print(("No Joints:grp, const.ROOTJOINTNAME, root_bone", grp, const.ROOTJOINTNAME, root_bone))
        return False

    logger.info(u'Prime_joint階層設定：')
    parent_dict = OrderedDict()

    for joint in pyjoint_list:

        pm.setAttr("{}.segmentScaleCompensate".format(joint), 0)

        joint_name = joint.stripNamespace().nodeName()
        label = Utils.get_label(joint_name)
        p_joint = joint.getParent()
        p_joint_name = p_joint.stripNamespace().nodeName()

        # only const.DUMMY_LIST and ignore startswith("EX_"), endswith("_End")
        if label in const.DUMMY_LIST and joint_name[-4:] != '_End' and joint_name[:2] != 'EX':
            # set name
            d_null_name = const.DUMMY + "null_" + joint_name
            d_joint_name = const.DUMMY + joint_name

            null = pm.group(em = True, n = d_null_name)
            offset_null = pm.group(em = True, n = d_null_name + const.SUFFIX_OFFSET)

            # save PyNode dict { String Name: Created PyNode }
            result_dict[d_null_name] = null
            result_dict[d_null_name + const.SUFFIX_OFFSET] = offset_null

            pm.parent(null, grp)
            pm.parent(offset_null, grp)

            # dupricate and save PyNode dict { String Name: Created PyNode }
            d_joint = pm_dup(joint, d_joint_name, result_dict)
            # save { String Name: Created PyNode }
            # result_dict[joint_name] = d_joint

            pm.parent(offset_null, null)
            pm.orientConstraint(joint, null, mo = 0)
            pm.pointConstraint(joint, null, mo = 0)

            pm.parent(d_joint, offset_null)
            parent_dict[null] = grp_dummy

        # Arm or Leg Joint Group ignore startswith("EX_"), endswith("_End")
        elif label in arm_list or label in leg_list and joint_name[-4:] != '_End' and joint_name[:2] != 'EX':
            if label != 'clavicle':
                # set name
                ik_joint_name = const.DUMMY + joint_name[:2] + 'IK_' + joint_name[2:]
                fk_joint_name = const.DUMMY + joint_name[:2] + 'FK_' + joint_name[2:]

                # dupricate and save PyNode dict { String Name: Created PyNode }
                ik_joint = pm_dup(joint, ik_joint_name, result_dict)
                fk_joint = pm_dup(joint, fk_joint_name, result_dict)

                if 'upper' not in joint_name:
                    # set name
                    p_ik_joint_name = const.DUMMY + p_joint_name[:2] + 'IK_' + p_joint_name[2:]
                    p_fk_joint_name = const.DUMMY + p_joint_name[:2] + 'FK_' + p_joint_name[2:]

                    # find and save PyNode dict { String Name: founded PyNode }
                    p_ik_joint = Utils.get_pynode(grp, p_ik_joint_name, result_dict)
                    p_fk_joint = Utils.get_pynode(grp, p_fk_joint_name, result_dict)
                    # save Parent dict
                    parent_dict[ik_joint] = p_ik_joint
                    parent_dict[fk_joint] = p_fk_joint

                else:
                    # set name
                    dummy_p_joint_name = const.DUMMY + p_joint_name

                    # find and save PyNode dict { String Name: founded PyNode }
                    dummy_p_joint = Utils.get_pynode(grp, dummy_p_joint_name, result_dict)

                    # save Parent dict
                    parent_dict[ik_joint] = dummy_p_joint
                    parent_dict[fk_joint] = dummy_p_joint

            elif label == 'clavicle':
                # set name
                d_joint_name = const.DUMMY + joint_name
                d_p_joint_name = const.DUMMY + p_joint_name

                # find and save PyNode dict { String Name: founded PyNode }
                d_p_joint = Utils.get_pynode(grp, d_p_joint_name, result_dict)
                # dupricate and save PyNode dict { String Name: Created PyNode }
                d_joint = pm_dup(joint, d_joint_name, result_dict)

                # save Parent dict
                parent_dict[d_joint] = d_p_joint

        # Seccondary Joint Group (ignore "EX")
        elif label in const.DUMMY_SECONDARY_LIST and joint_name[:2] != 'EX':
            i = 2

            # set name
            ik_joint_name = const.DUMMY + joint_name[:i] + 'IK_' + joint_name[i:]
            sik_joint_name = const.DUMMY + joint_name[:i] + 'SplineIK_' + joint_name[i:]
            fk_joint_name = const.DUMMY + joint_name[:i] + 'FK_' + joint_name[i:]

            # dupricate and save PyNode dict { String Name: Created PyNode }
            ik_joint = pm_dup(joint, ik_joint_name)
            sik_joint = pm_dup(joint, sik_joint_name)
            fk_joint = pm_dup(joint, fk_joint_name)

            if label not in p_joint_name:
                # set name
                dummy_p_joint_name = const.DUMMY + p_joint_name

                # find and save PyNode dict { String Name: founded PyNode }
                dummy_p_joint = Utils.get_pynode(grp, dummy_p_joint_name, result_dict)

                # save Parent dict
                parent_dict[ik_joint] = dummy_p_joint
                parent_dict[sik_joint] = dummy_p_joint
                parent_dict[fk_joint] = dummy_p_joint

            else:
                # set name
                p_ik_joint_name = const.DUMMY + p_joint_name[:i] + 'IK_' + p_joint_name[i:]
                p_sik_joint_name = const.DUMMY + p_joint_name[:i] + 'SplineIK_' + p_joint_name[i:]
                p_fk_joint_name = const.DUMMY + p_joint_name[:i] + 'FK_' + p_joint_name[i:]

                # find and save PyNode dict { String Name: founded PyNode }
                p_ik_joint = Utils.get_pynode(grp, p_ik_joint_name, result_dict)
                p_sik_joint = Utils.get_pynode(grp, p_sik_joint_name, result_dict)
                p_fk_joint = Utils.get_pynode(grp, p_fk_joint_name, result_dict)

                # save Parent dict
                parent_dict[ik_joint] = p_ik_joint
                parent_dict[sik_joint] = p_sik_joint
                parent_dict[fk_joint] = p_fk_joint # Seccondary Joint Group (ignore "EX")

        # sleeve で"EX"が付かない場合のエラー対応
        elif label == "sleeve" and joint_name[:2] != 'EX' and label:
            i = 2

            # set name
            ik_joint_name = const.DUMMY + joint_name[:i] + 'IK_' + joint_name[i:]
            sik_joint_name = const.DUMMY + joint_name[:i] + 'SplineIK_' + joint_name[i:]
            fk_joint_name = const.DUMMY + joint_name[:i] + 'FK_' + joint_name[i:]

            # dupricate and save PyNode dict { String Name: Created PyNode }
            ik_joint = pm_dup(joint, ik_joint_name)
            sik_joint = pm_dup(joint, sik_joint_name)
            fk_joint = pm_dup(joint, fk_joint_name)

            if label not in p_joint_name:
                # set name
                dummy_p_joint_name = const.DUMMY + p_joint_name.replace("_forearm", "_FK_forearm")

                # find and save PyNode dict { String Name: founded PyNode }
                dummy_p_joint = Utils.get_pynode(grp, dummy_p_joint_name, result_dict)

                # save Parent dict
                parent_dict[ik_joint] = dummy_p_joint
                parent_dict[sik_joint] = dummy_p_joint
                parent_dict[fk_joint] = dummy_p_joint
                if dummy_p_joint is None:
                    print(("dummy_p_joint_name:", dummy_p_joint_name, dummy_p_joint))
            else:
                # set name
                p_ik_joint_name = const.DUMMY + p_joint_name[:i] + 'IK_' + p_joint_name[i:]
                p_sik_joint_name = const.DUMMY + p_joint_name[:i] + 'SplineIK_' + p_joint_name[i:]
                p_fk_joint_name = const.DUMMY + p_joint_name[:i] + 'FK_' + p_joint_name[i:]

                # find and save PyNode dict { String Name: founded PyNode }
                p_ik_joint = Utils.get_pynode(grp, p_ik_joint_name, result_dict)
                p_sik_joint = Utils.get_pynode(grp, p_sik_joint_name, result_dict)
                p_fk_joint = Utils.get_pynode(grp, p_fk_joint_name, result_dict)

                # save Parent dict
                parent_dict[ik_joint] = p_ik_joint
                parent_dict[sik_joint] = p_sik_joint
                parent_dict[fk_joint] = p_fk_joint
                if p_sik_joint is None:
                    print(("Sleeve Else:{}".format(joint), ik_joint, p_ik_joint))
                    print(("Sleeve Else:{}".format(joint), sik_joint, p_sik_joint))
                    print(("Sleeve Else:{}".format(joint), fk_joint, p_fk_joint))
        else:
            pass
            # print("label:", label, "joint_name: ", joint_name)

    # Prime_joint階層化処理
    try:
        for child, parent in list(parent_dict.items()):
            pm.parent(child, parent)

    except Exception as e:
        print(e)
        logger.error(u'ダミージョイント作成: 失敗')
        logger.info("-" * 72)
        return False

    logger.info(u'EX_joint階層の設定：')
    parent_dict = OrderedDict()

    for joint in pyjoint_list:
        joint_name = joint.stripNamespace().nodeName()
        label = Utils.get_label(joint_name)

        if joint_name[:3] == 'EX_':
            p_joint = joint.getParent()

            ex_joints = []

            for ex_joint_name in ex_sik:
                # set name
                ex_joint_name = ex_joint_name.replace(ns, "")

                # find and save PyNode dict { String Name: founded PyNode }
                ex_joint = Utils.get_pynode(grp, ex_joint_name, result_dict)

                children = pm.listRelatives(ex_joint, c = True, ad = True, type = 'joint') or []
                ex_joints.append(ex_joint)
                ex_joints.extend(children)

            if joint in ex_joints:
                i = 3

                # set name
                ik_joint_name = const.DUMMY + joint.stripNamespace().nodeName()[
                                              :i] + 'IK_' + joint.stripNamespace().nodeName()[i:]
                sik_joint_name = const.DUMMY + joint.stripNamespace().nodeName()[
                                               :i] + 'SplineIK_' + joint.stripNamespace().nodeName()[i:]
                fk_joint_name = const.DUMMY + joint.stripNamespace().nodeName()[
                                              :i] + 'FK_' + joint.stripNamespace().nodeName()[i:]

                # dupricate and save PyNode dict { String Name: Created PyNode }
                ik_joint = pm_dup(joint, ik_joint_name, result_dict)
                sik_joint = pm_dup(joint, sik_joint_name, result_dict)
                fk_joint = pm_dup(joint, fk_joint_name, result_dict)

                if joint.nodeName()[-3:] != '_00':
                    # set name
                    p_ik_joint_name = const.DUMMY + p_joint.stripNamespace().nodeName()[
                                                    :i] + 'IK_' + p_joint.stripNamespace().nodeName()[i:]
                    p_sik_joint_name = const.DUMMY + p_joint.stripNamespace().nodeName()[
                                                     :i] + 'SplineIK_' + p_joint.stripNamespace().nodeName()[i:]
                    p_fk_joint_name = const.DUMMY + p_joint.stripNamespace().nodeName()[
                                                    :i] + 'FK_' + p_joint.stripNamespace().nodeName()[i:]

                    # find and save PyNode dict { String Name: founded PyNode }
                    p_ik_joint = Utils.get_pynode(grp, p_ik_joint_name, result_dict)
                    p_sik_joint = Utils.get_pynode(grp, p_sik_joint_name, result_dict)
                    p_fk_joint = Utils.get_pynode(grp, p_fk_joint_name, result_dict)

                    # save Parent dict
                    parent_dict[ik_joint] = p_ik_joint
                    parent_dict[sik_joint] = p_sik_joint
                    parent_dict[fk_joint] = p_fk_joint

                else:
                    if p_joint.stripNamespace().nodeName()[:3] != 'EX_':
                        i = 2

                        # set name
                        dummy_p_joint_name = const.DUMMY + p_joint.stripNamespace().nodeName()
                        p_ik_joint_name = const.DUMMY + p_joint.stripNamespace().nodeName()[
                                                        :i] + 'IK_' + p_joint.stripNamespace().nodeName()[i:]
                        p_sik_joint_name = const.DUMMY + p_joint.stripNamespace().nodeName()[
                                                         :i] + 'SplineIK_' + p_joint.stripNamespace().nodeName()[i:]
                        p_fk_joint_name = const.DUMMY + p_joint.stripNamespace().nodeName()[
                                                        :i] + 'FK_' + p_joint.stripNamespace().nodeName()[i:]

                        # find and save PyNode dict { String Name: founded PyNode }
                        dummy_p_joint = Utils.get_pynode(grp, dummy_p_joint_name)
                        p_ik_joint = Utils.get_pynode(grp, p_ik_joint_name, result_dict)
                        p_sik_joint = Utils.get_pynode(grp, p_sik_joint_name, result_dict)
                        p_fk_joint = Utils.get_pynode(grp, p_fk_joint_name, result_dict)

                        # save Parent dict
                        parent_dict[ik_joint] = dummy_p_joint
                        parent_dict[fk_joint] = dummy_p_joint
                        parent_dict[sik_joint] = dummy_p_joint

                        if p_ik_joint:
                            parent_dict[ik_joint] = p_ik_joint
                            parent_dict[sik_joint] = p_ik_joint

                        elif dummy_p_joint:
                            parent_dict[ik_joint] = dummy_p_joint
                            parent_dict[sik_joint] = dummy_p_joint

                        if p_fk_joint:
                            parent_dict[fk_joint] = p_ik_joint

                        elif dummy_p_joint:
                            parent_dict[fk_joint] = dummy_p_joint

    # EX_joint階層化処理
    try:
        for child, parent in list(parent_dict.items()):
            if pm.objExists(child) and pm.objExists(parent):
                try:
                    pm.parent(child, parent)
                except Exception as e:
                    print(e)
                    logger.error("{} {}".format(child, parent))
            else:
                # TODO parent設定ミスなので、前処理で解決するように対応予定。
                logger.error("missing pair: ", child, parent)
                p_node = child.getParent()
                dummy_node = const.DUMMY + p_node.stripNamespace().nodeName()

                if pm.objExists(dummy_node):
                    pm.parent(child, dummy_node)
                else:
                    null = pm.group(em = True, n = const.DUMMY + p_node)
                    pm.parentConstraint(p_node, null, mo = 0)
                    pm.parent(null, grp_dummy)
                    pm.parent(child, null)

    except Exception as e:
        print(e)
        logger.error(u'ダミージョイント作成: 失敗')
        logger.info("-" * 72)
        return False

    if result_dict:
        logger.info(u'ダミージョイント作成: 成功')
        logger.info("-" * 72)
        return result_dict

    else:
        logger.error(u'ダミージョイント作成: 失敗')
        logger.info("-" * 72)
        return False


def create_displaylayer(nodes=[], name=const.RIG_LAYERNAME):
    u"""
        ノードリストからディスプレイレイヤー作成
        :param list of PyNode nodes:
        :param str name: ディスプレイレイヤー名
        :return  display layer PyNode or None
    """
    lyr_node = None

    if not nodes:
        return
    try:
        lyr_node = pm.PyNode(name)
    except Exception as e:
        # print(e)
        lyr_node = ""

    if not pm.objExists(lyr_node):
        lyr_node = pm.createDisplayLayer(nodes, name = name, number = 1, nr = True)

    elif pm.objExists(lyr_node) and isinstance(lyr_node, pm.nodetypes.DisplayLayer):
        pm.editDisplayLayerMembers(lyr_node, nodes, noRecurse = True)

    elif pm.objExists(lyr_node) and not isinstance(lyr_node, pm.nodetypes.DisplayLayer):
        lyr_node.rename(name + "_renamed")
        lyr_node = pm.createDisplayLayer(nodes, name = name, number = 1, nr = True)

    else:
        pass

    return lyr_node


def set_root_attr(root_ctrl, attr_dict=const.ATTR_DICT, vis_list=[], ikfk_list=[]):
    u"""
        ルートコントロールに必要なアトリビュートを追加、再作成
        :param root_ctrl:　PyNode
        :param attr_dict:　dict(str:dict)
        :param vis_list:　list of string
        :param ikfk_list:　list of string
        :return  bool or None
    """

    if root_ctrl is None:
        return

    if vis_list == []:
        # const.SECONDARYJOINTNAME_LIST = ['tail', 'skirt', 'hair', 'mant', 'wing', 'sleeve', 'bust']
        vis_list.extend(const.SECONDARYJOINTNAME_LIST)
        vis_list.extend(["tail_up", "L_finger", "R_finger", "ex_node"])

    if ikfk_list == []:
        # const.SECONDARYJOINTNAME_LIST = ['tail', 'skirt', 'hair', 'mant', 'wing', 'sleeve', 'bust']
        ikfk_list.extend(const.SECONDARYJOINTNAME_LIST)
        ikfk_list.extend(["ex_node"])

    # pin_type = ['ringroot', 'ring', 'pinky', 'middle', 'index', 'thumb']
    # octahedron_type = ['forearm', 'foreleg']
    # vcroos_type = ['hand']
    # hcroos_type = ['foot', 'pelvis']

    # SIZE = dict(XS = 0.9, S = 0.95, M = 1.0, L = 1.04)

    for vis in vis_list:
        vis_attr = "{}_CTRL_Visibility".format(vis)
        attr_dict.update({vis_attr: dict(ln = vis_attr, at = "bool", dv = 0, k = True)})

    for ikfk in ikfk_list:
        ikfk_attr = "{}_CTRL_ik0fk1".format(ikfk)
        attr_dict.update({ikfk_attr: dict(ln = ikfk_attr, at = "float", dv = 0, min = 0, max = 1.0, k = True)})

    # delete all extra Attributes
    for attr, kwargs in list(attr_dict.items()):
        if pm.attributeQuery(attr, node = root_ctrl, exists = True):
            try:
                pm.deleteAttr(root_ctrl, attribute = attr)
            except Exception:
                print(("Skip, Cannot delete: ", "{}.{]".format(root_ctrl, attr)))

    # add ordered Extra Attributes
    for attr, kwargs in list(attr_dict.items()):
        # print(root_ctrl, kwargs)
        if not pm.attributeQuery(attr, node = root_ctrl, exists = True):
            pm.addAttr(root_ctrl, **kwargs)
        pm.setAttr("{}.{}".format(root_ctrl, attr), e = True, k = True)

    return True


def remove_unused_root_attr(root_ctrl):
    u"""
        ルートコントロールにコネクションの無い不要なアトリビュートを削除
        :param root_ctrl:　PyNode
    """
    if root_ctrl is None:
        return

    for attr in root_ctrl.listAttr(k = True):
        if "_CTRL_Visibility" in attr.name() or "_CTRL_ik0fk1" in attr.name():
            cons = pm.listConnections(attr, p = True, d = True, s = False) or []
            if cons:
                pass  # print(attr, len(cons))

            else:
                print(("Remove unused attr:", attr))
                attr.delete()


def create_rig(body=True, arm=True, leg=True, secondary=True, ex_flag=True, ex_s_flag=False, grp=None, size='M',
               ex_sik=None, node_dict=None):
    u"""
        リグ作成
        :param bool body:
        :param bool arm:
        :param bool leg:
        :param bool secondary:
        :param bool ex_flag:
        :param bool ex_s_flag:
        :param PyNode grp: ターゲットグループ
        :param str size: [XS, S, M, L]
        :param list ex_sik: EX SplineIKを設定するノード名リスト
        :param dict node_dict: 事前に作成されたダミーノードのdict
        :return bool:
    """
    num = 0
    print(ex_sik)

    Utils.print_info(u'Rig Creating')

    if not node_dict:
        return False

    parent_dict = {}

    # root_boneの設定　リファレンスによるネームスペース（ns）有/無　のどちらも対応。
    ns = Utils.get_namespace(grp)
    root_bone = Utils.get_pynode(grp, ns + const.ROOTJOINTNAME)

    # root_null, root_ctrl の作成
    root_ctrl = Utils.get_pynode(grp, const.ROOTCTRLNAME)
    root_null = Utils.get_pynode(grp, const.ROOTNULLNAME)

    # ルートCTRL作成
    if root_null is None:
        if root_ctrl:
            pm.delete(root_ctrl)
        root_null, root_ctrl = create_controller(root_bone, type = 'root', parent = grp)

        if not set_root_attr(root_ctrl):
            print("Failed to set root_CTRL's Attributes")
            return False

    node_dict[root_ctrl.nodeName()] = root_ctrl

    skirt_IK_null = None
    hair_IK_null = None
    mant_IK_null = None
    wing_IK_null = None
    tail_IK_null = None

    # grp_Dummy の変数代入 const.GROUPDUMNAME
    grp_dummy = node_dict.get(const.GROUPDUMNAME, None)

    # grp_rig の作成 const.GROUPRIGNAME
    grp_rig = Utils.get_pynode(grp, const.GROUPRIGNAME)
    grp_rig = create_group(const.GROUPRIGNAME, grp) if grp_rig is None else grp_rig

    # grp_joint の取得 const.GROUPJOINTNAME
    grp_joint = Utils.get_pynode(grp, const.GROUPJOINTNAME)

    # grp_SplineIK の作成 const.GROUPSIKNAME
    s_grp = Utils.get_pynode(grp, const.GROUPSIKNAME)
    s_grp = create_group(const.GROUPSIKNAME, grp) if s_grp is None else s_grp

    # ScaleFactorを使用する為にFalseである必要がある。
    if not pm.getAttr("{}.inheritsTransform".format(s_grp)) == 0:
        if pm.getAttr("{}.inheritsTransform".format(s_grp), l = True):
            pm.setAttr("{}.inheritsTransform".format(s_grp), l = False)
        pm.setAttr("{}.inheritsTransform".format(s_grp), 0)
        pm.setAttr("{}.inheritsTransform".format(s_grp), l = True)

    # センターメインのCTRL名
    chest_ctrl_name = const.CHESTJOINTNAME + const.SUFFIX_CTRL
    head_ctrl_name = const.HEADJOINTNAME + const.SUFFIX_CTRL
    hip_ctrl_name = const.HIPJOINTNAME + const.SUFFIX_CTRL

    if not root_ctrl:
        num += 1
        logger.info("-" * 72)

    # center_list = const.C_JOINTNAME_LIST
    pyjoint_list = Utils.get_pyjoints(root_bone)
    execution_dict = get_execution_dict(pyjoint_list)

    # First Excution for Primary Joints
    # -------------------------------------------------------------------------
    # 体コントローラー作成処理: <joint名>_null, <joint名>_CTRL
    # -------------------------------------------------------------------------
    for joint in execution_dict['center']:
        num += 1
        Utils.print_info(" {}:{} joint setting:".format(num, 'center'), joint)
        joint_name = Utils.get_name(joint.stripNamespace().nodeName())
        label = Utils.get_label(joint_name)
        # print(" label: {} , joint_name: {}".format(label,  joint_name))
        if not body:
            return False

        if joint_name[-4:] != '_End' and not Utils.get_pynode(grp, joint_name + const.SUFFIX_CTRL):
            logger.info(u'Rig作成 基本： {}'.format(joint))
            if label == 'pelvis':
                null, ctrl = create_controller(joint, dict = node_dict, parent = grp)
                create_constraint(ctrl, joint, 0, type = "point")
                set_lock_srt(ctrl, s = True)
            else:
                null, ctrl = create_controller(joint, dict = node_dict, parent = grp)
                set_lock_srt(ctrl, t = True, s = True)

            pa_node = joint.getParent()
            if not pa_node:
                print((u"親階層が無いと失敗", joint))
                return False
            else:
                pa_name = Utils.get_name(pa_node.stripNamespace().nodeName())
                parent_dict[null] = Utils.get_pynode(grp, pa_name + const.SUFFIX_CTRL)
                create_constraint(ctrl, joint, 1, type = "orient")
            # print("null, ctrl", null.name(), ctrl.name())
            if label == 'head':
                create_constraint(ctrl, joint, 0, type = "scale")

    Utils.print_info(" {} joint setting: Finished".format('center'))

    # 以降で使う変数
    chest_ctrl = node_dict[chest_ctrl_name]
    hip_ctrl = node_dict[hip_ctrl_name]
    head_ctrl = node_dict[head_ctrl_name]

    # Second Excution for Arm Joints
    # -------------------------------------------------------------------------
    # 腕コントローラー作成処理 TODO 作成オーダー順に処理を簡略化可能
    # -------------------------------------------------------------------------
    clavicle_ctrl = None
    for joint in execution_dict['arm']:
        num += 1
        Utils.print_info(" {}:{} joint setting:".format(num, 'arm'), joint)
        joint_name = Utils.get_name(joint.stripNamespace().nodeName())
        label = Utils.get_label(joint_name)
        LR_prefix = joint_name[:2] if joint_name[:2] in ["L_", "R_"] else ""

        if not arm:
            return False

        logger.info(u'Rig作成 腕： {}'.format(joint))
        ikfk_ctrl = ''
        # IK 処理
        if label == 'upperarm':
            ikfk_ctrl, rev = create_ikfk_controller(joint_name, dict = node_dict)
            parent_dict[ikfk_ctrl] = root_ctrl

            ik_joint_name = const.DUMMY + joint_name[:2] + 'IK_' + joint_name[2:]
            c_ik_joint_name = ik_joint_name.replace('upperarm', 'forearm')
            gc_ik_joint_name = ik_joint_name.replace('upperarm', 'hand')

            ik_joint = node_dict.get(ik_joint_name, None)
            c_ik_joint = node_dict.get(c_ik_joint_name, None)
            gc_ik_joint = node_dict.get(gc_ik_joint_name, None)
            gc_ik_joint_name = gc_ik_joint.stripNamespace().nodeName()

            handle = create_ik_handle(ik_joint, gc_ik_joint, parent = grp)

            c_null, c_ctrl, c_offset = create_elbow_controller(c_ik_joint, 'oct', offset = True, dict = node_dict,
                                                               parent = grp)
            g_null = c_ctrl.getParent()
            c_null.rename(LR_prefix + 'elbow' + const.SUFFIX_NULL)
            c_offset.rename(LR_prefix + 'elbow' + const.SUFFIX_OFFSET)
            g_null.rename(LR_prefix + 'elbow_global' + const.SUFFIX_NULL)
            c_ctrl.rename(LR_prefix + 'elbow' + const.SUFFIX_CTRL)

            if LR_prefix == 'L_':
                pm.move(-40, c_offset, z = True, os = True, r = True)
            else:
                pm.move(40, c_offset, z = True, os = True, r = True)

            pm.setAttr('{}.visibility'.format(c_ctrl), k = False)
            set_lock_srt(c_ctrl, r = True, s = True)
            set_lock_srt(c_offset, s = True)

            gc_t_null, gc_t_ctrl = create_controller(gc_ik_joint, type = 'oct', dict = node_dict, parent = grp)
            gc_t_null.rename(gc_t_null.replace('hand', 'hand_trans'))
            gc_t_ctrl.rename(gc_t_ctrl.replace('hand', 'hand_trans'))
            set_lock_srt(gc_t_ctrl, r = True, s = True)
            # IK_rot_CTRL 作成
            gc_str = get_global_transform(gc_ik_joint)
            c_srt = get_global_transform(c_ik_joint)

            gc_r_null = create_dummy(gc_ik_joint_name[6:].replace('hand', 'hand_rot'), parent = grp)
            gc_r_offset = create_offset(gc_ik_joint_name[6:].replace('hand', 'hand_rot'), parent = grp)
            gc_r_ctrl = create_wire(gc_ik_joint_name[6:].replace('hand', 'hand_rot'), parent = grp)
            node_dict[gc_r_ctrl.nodeName()] = gc_r_ctrl
            pm.setAttr('{}.visibility'.format(gc_r_ctrl), 0)

            set_global_transform(gc_r_null, c_srt)
            pm.parent(gc_r_ctrl, gc_r_offset)
            set_global_transform(gc_r_offset, gc_str)

            set_lock_srt(gc_r_ctrl, t = True, s = True)
            pm.parent(gc_r_offset, gc_r_null)

            create_upvector(handle, c_ctrl)
            create_constraint(c_ik_joint, gc_r_null, 0, type = "point")
            create_constraint(c_ik_joint, gc_r_null, 0, type = "orient")
            create_constraint(gc_r_ctrl, gc_ik_joint, 0, type = "orient")

            # set parent_dict
            parent_dict[c_null] = chest_ctrl
            parent_dict[gc_t_null] = chest_ctrl
            parent_dict[gc_r_null] = chest_ctrl
            parent_dict[handle] = gc_t_ctrl

            pm.connectAttr('{}.output.outputX'.format(rev), '{}.visibility'.format(gc_t_ctrl), f = True)
            pm.connectAttr('{}.output.outputX'.format(rev), '{}.visibility'.format(gc_r_ctrl), f = True)
            pm.connectAttr('{}.output.outputX'.format(rev), '{}.visibility'.format(c_ctrl), f = True)

            twistarm = Utils.get_pynode(grp, ns + "{}_twistarm".format(gc_r_ctrl.nodeName()[:1]))
            create_multiplydivide(gc_r_ctrl, twist = twistarm)

            # create "ikfk_selection" node
            c_joint = Utils.get_pynode(grp, ns + joint_name.replace('upperarm', 'forearm'))
            gc_joint = Utils.get_pynode(grp, ns + '{}_hand'.format(joint_name[:1]))

            for j_node in [joint, c_joint, gc_joint]:
                j_name = Utils.get_name(j_node.stripNamespace().nodeName())
                i = 3 if j_name[:3] == 'EX_' else 2
                ik_node = node_dict.get(const.DUMMY + j_name[:i] + 'IK_' + j_name[i:], None)
                fk_node = node_dict.get(const.DUMMY + j_name[:i] + 'FK_' + j_name[i:], None)
                create_ikfk_selection(j_node, ik_node, fk_node, ikfk_ctrl, rev)

        elif label == 'hand':
            srt = get_global_transform(joint)

            name = '{}_finger'.format(joint_name[:1])
            name = Utils.get_name(name)

            null = create_dummy(name, parent = grp)
            offset = create_offset(name, parent = grp)

            # 子、親
            pm.parent(offset, null)
            set_global_transform(null, srt)

            # set parent_dict
            parent_dict[null] = root_ctrl

            create_constraint(joint, null, 0, type = "point")
            create_constraint(joint, null, 0, type = "orient")

        else:
            pass  # print("IK Skipped: label:", label, "joint_name: ", joint_name)

        clavicle_ctrl = None
        # FK 処理
        if label == 'clavicle':
            fk_joint = node_dict.get(const.DUMMY + joint_name, None)
            fk_null, fk_ctrl = create_controller(fk_joint, local = True, dict = node_dict, parent = grp)
            parent_dict[fk_null] = chest_ctrl
            create_constraint(fk_ctrl, joint, 0, type = "orient")
            create_constraint(fk_ctrl, fk_joint, 0, type = "orient")
            # clavicle が　FK操作時に制御から外れていた為追加
            clavicle_ctrl = fk_ctrl

        elif label == 'upperarm':
            fk_joint = node_dict.get(const.DUMMY + LR_prefix + 'FK_' + joint_name[2:], None)
            fk_null, fk_ctrl = create_controller(fk_joint, local = True, dict = node_dict, parent = grp)
            parent_dict[fk_null] = chest_ctrl
            create_constraint(fk_ctrl, fk_joint, 0, type = "orient")
            pm.connectAttr('{}.ik0fk1'.format(ikfk_ctrl), '{}.visibility'.format(fk_ctrl), f = True)
            # clavicle が　FK操作時に制御から外れていた為追加
            if clavicle_ctrl:
                create_constraint(clavicle_ctrl, fk_null, 1, type = "parent")

        else:
            fk_joint = node_dict.get(const.DUMMY + LR_prefix + 'FK_' + joint_name[2:], None)
            fk_null, fk_ctrl = create_controller(fk_joint, local = True, dict = node_dict, parent = grp)
            pa_ctrl_name = Utils.get_name(fk_joint.getParent().stripNamespace().nodeName())[6:] + const.SUFFIX_CTRL
            parent_dict[fk_null] = Utils.get_pynode(grp, pa_ctrl_name)
            create_constraint(fk_ctrl, fk_joint, 0, type = "orient")

        set_lock_srt(fk_ctrl, t = True, s = True)

    Utils.print_info(" {}:{} joint setting: Finished".format(num, 'arm'))

    # Third Excution for Finger Joints
    # -------------------------------------------------------------------------
    # 指のコントローラー作成処理　TODO 作成オーダー順に処理を簡略化可能
    # -------------------------------------------------------------------------
    for joint in execution_dict['hand']:
        num += 1
        Utils.print_info(" {}:{} joint setting:".format(num, 'hand'), joint)
        joint_name = Utils.get_name(joint.stripNamespace().nodeName())
        label = Utils.get_label(joint_name)
        LR_prefix = joint_name[:2] if joint_name[:2] in ["L_", "R_"] else ""

        if not arm:
            return False

        if joint_name[-4:] != '_End':
            logger.info(u'Rig作成 指： {}'.format(joint))
            null, ctrl = create_controller(joint, local = True, type = 'pin', dict = node_dict, parent = grp)
            p_joint = joint.getParent()
            p_joint_name = p_joint.stripNamespace().nodeName()
            create_constraint(ctrl, joint, 0, type = "orient")

            if 'hand' in p_joint_name:
                finger_offset_name = p_joint_name.replace('hand', 'finger') + const.SUFFIX_OFFSET
                parent_dict[null] = Utils.get_pynode(grp, finger_offset_name, None)
            else:
                p_ctrl_name = p_joint_name + const.SUFFIX_CTRL
                parent_dict[null] = Utils.get_pynode(grp, p_ctrl_name, None)

            pm.connectAttr('{}.{}finger_CTRL_Visibility'.format(root_ctrl, LR_prefix), '{}.visibility'.format(ctrl),
                           f = True)
            set_lock_srt(ctrl, t = True, s = True)
    Utils.print_info(" {}:{} joint setting: Finished".format(num, 'hand'))

    # Forth Excution for Leg Joints
    # -------------------------------------------------------------------------
    # 足のコントローラー作成処理　TODO 作成オーダー順に処理を簡略化可能
    # -------------------------------------------------------------------------
    for joint in execution_dict['leg']:
        num += 1
        Utils.print_info(" {}:{} joint setting:".format(num, 'leg'), joint)
        joint_name = Utils.get_name(joint.stripNamespace().nodeName())
        label = Utils.get_label(joint_name)
        LR_prefix = joint_name[:2] if joint_name[:2] in ["L_", "R_"] else ""

        if not leg:
            return False

        if joint_name[-4:] != '_End':
            logger.info(u'Rig作成 脚： {}'.format(joint))

            # IK 処理
            if label == 'upperleg':
                ikfk_ctrl, rev = create_ikfk_controller(joint_name, dict = node_dict)
                parent_dict[ikfk_ctrl] = root_ctrl

                ik_joint = node_dict.get(const.DUMMY + LR_prefix + 'IK_' + joint_name[2:], None)
                gc_ik_joint = get_ik_child(ik_joint)
                handle = create_ik_handle(ik_joint, gc_ik_joint, parent = grp)

                c_ik_joint = get_child(ik_joint)
                c_null, c_ctrl = create_controller(c_ik_joint, type = 'oct', dict = node_dict, parent = grp)

                c_null.rename(LR_prefix + 'knee' + const.SUFFIX_NULL)
                c_ctrl.rename(LR_prefix + 'knee' + const.SUFFIX_CTRL)

                set_lock_srt(c_ctrl, r = True, s = True)
                gc_null, gc_ctrl = create_controller(gc_ik_joint, type = 'h_cross', dict = node_dict, parent = grp)

                pm.move(45, c_null, z = True, r = True)
                ggc_ik_joint = get_child(gc_ik_joint)
                ggc_null, ggc_ctrl = create_controller(ggc_ik_joint, dict = node_dict, parent = grp)
                parent_dict[ggc_null] = gc_ctrl

                create_upvector(handle, c_ctrl)

                set_lock_srt(gc_ctrl, s = True)
                create_constraint(gc_ctrl, gc_ik_joint, 1, type = "orient")
                create_constraint(ggc_ctrl, ggc_ik_joint, 1, type = "orient")

                set_lock_srt(ggc_ctrl, t = True, s = True)

                parent_dict[c_null] = gc_ctrl
                parent_dict[gc_null] = root_ctrl
                parent_dict[handle] = gc_ctrl

                pm.connectAttr('{}.output.outputX'.format(rev), '{}.visibility'.format(gc_ctrl), f = True)
                pm.connectAttr('{}.output.outputX'.format(rev), '{}.visibility'.format(ggc_ctrl), f = True)
                pm.connectAttr('{}.output.outputX'.format(rev), '{}.visibility'.format(c_ctrl), f = True)

                c_joint = Utils.get_pynode(grp, ns + joint_name.replace('upperleg', 'foreleg'))
                gc_joint = Utils.get_pynode(grp, ns + joint_name.replace('upperleg', 'foot'))
                ggc_joint = Utils.get_pynode(grp, ns + joint_name.replace('upperleg', 'toe'))

                for j_node in [joint, c_joint, gc_joint, ggc_joint]:
                    j_name = Utils.get_name(j_node.stripNamespace().nodeName())
                    i = 3 if j_name[:3] == 'EX_' else 2
                    ik_node = node_dict.get(const.DUMMY + j_name[:i] + 'IK_' + j_name[i:], None)
                    fk_node = node_dict.get(const.DUMMY + j_name[:i] + 'FK_' + j_name[i:], None)
                    create_ikfk_selection(j_node, ik_node, fk_node, ikfk_ctrl, rev)

            # FK 処理
            fk_joint = node_dict.get(const.DUMMY + LR_prefix + 'FK_' + joint_name[2:], None)
            fk_null, fk_ctrl = create_controller(fk_joint, dict = node_dict, parent = grp)

            if label == 'upperleg':
                # pa_node = joint.getParent()
                # parent_dict[fk_null] = Utils.get_name(pa_node.stripNamespace().nodeName()) + const.SUFFIX_CTRL
                parent_dict[fk_null] = hip_ctrl
                pm.connectAttr('{}.ik0fk1'.format(ikfk_ctrl), '{}.visibility'.format(fk_null), f = True)

            else:
                p_ctrl = Utils.get_pynode(grp, Utils.get_name(fk_joint.getParent().stripNamespace().nodeName())[
                                               6:] + const.SUFFIX_CTRL)
                parent_dict[fk_null] = p_ctrl

            create_constraint(fk_ctrl, fk_joint, 1, type = "orient")
            set_lock_srt(fk_ctrl, t = True, s = True)

    Utils.print_info(" {}:{} joint setting: Finished".format(num, 'leg'))

    # Fifth Excution for EX Joints
    # -------------------------------------------------------------------------
    # EX ＆ Secondaryのコントローラー作成処理
    # -------------------------------------------------------------------------
    # for joint in Utils.get_pyjoints(root_bone):
    ex_list = execution_dict["ex"] + execution_dict["secondary"]

    for joint in ex_list:
        num += 1
        Utils.print_info(" {}:{} joint setting:".format(num, 'EX and secondary'), joint)
        joint_name = Utils.get_name(joint.stripNamespace().nodeName())

        if joint_name[-4:] != '_End':
            label = Utils.get_label(joint_name)
            # -------------------------------------------------------------------------
            # セカンダリコントローラー作成処理
            # -------------------------------------------------------------------------
            i = 3 if joint_name[:3] == 'EX_' else 2

            # セカンダリージョイントリストに含まれ、かつ"EX"始まりではないジョイントに対する処理
            if secondary and label in const.SECONDARYJOINTNAME_LIST and joint_name[:i] and joint_name[:2] != 'EX':
                # v2.2~: 'bust'はSplineIKが無い仕様なので除外
                if label in ['tail', 'skirt', 'hair', 'mant', 'wing']:
                    s_joint = node_dict.get(const.DUMMY + joint_name[:2] + 'FK_' + joint_name[i:], None)
                else:
                    s_joint = joint

                logger.info(u'Rig作成 セカンダリー： {}'.format(joint))
                # FK controller作成
                if 'tail' in Utils.get_name(s_joint):
                    fk_null, fk_ctrl = create_controller(s_joint, offset = True, dict = node_dict, parent = grp)
                    create_constraint(fk_ctrl, s_joint, 1, type = "orient")
                elif 'bust' in Utils.get_name(s_joint):
                    fk_null, fk_ctrl = create_controller(s_joint, local = True, offset = True, dict = node_dict,
                                                         parent = grp)
                    create_constraint(fk_ctrl, s_joint, 0, type = "orient")
                    create_constraint(fk_ctrl, s_joint, 0, type = "point")
                    create_constraint(fk_ctrl, s_joint, 0, type = "scale")
                else:
                    fk_null, fk_ctrl = create_controller(s_joint, local = True, offset = True, dict = node_dict,
                                                         parent = grp)
                    create_constraint(fk_ctrl, s_joint, 0, type = "orient")

                # parent設定の取得、parent_dictへ登録
                if 'sleeve' in Utils.get_name(s_joint):
                    parent_dict[fk_null] = root_ctrl
                    p_joint = s_joint.getParent()
                    create_constraint(p_joint, fk_null, 1, type = "parent")

                else:
                    pa_name = joint.getParent().stripNamespace().nodeName()
                    if label not in Utils.get_name(pa_name):
                        parent_dict[fk_null] = Utils.get_pynode(grp, Utils.get_name(pa_name) + const.SUFFIX_CTRL)
                    else:
                        if const.DUMMY in Utils.get_name(s_joint):
                            s_joint_name = s_joint.getParent().stripNamespace().nodeName()
                            parent_dict[fk_null] = Utils.get_pynode(grp, Utils.get_name(s_joint_name)[
                                                                         6:] + const.SUFFIX_CTRL)
                        else:
                            parent_dict[fk_null] = Utils.get_pynode(grp, Utils.get_name(pa_name) + const.SUFFIX_CTRL)

                connect_visibility(root_ctrl, fk_ctrl)

                # 'bust'のみロックを除外
                if 'bust' in Utils.get_name(s_joint):
                    print(u"{} はSRTロック除外".format(fk_ctrl))  # set_lock_srt(fk_ctrl, s=True)
                else:
                    set_lock_srt(fk_ctrl, t = True, s = True)

                # IK 用の FK controller作成 v2.2~:'bust'はSplineIKが無い仕様なので除外
                if label in ['tail', 'skirt', 'hair', 'mant', 'wing']:
                    ik_joint = node_dict.get(const.DUMMY + joint_name[:i] + 'IK_' + joint_name[i:], None)
                    sik_joint = node_dict.get(const.DUMMY + joint_name[:i] + 'SplineIK_' + joint_name[i:], None)

                    if 'tail' in ik_joint.nodeName():
                        ik_null, ik_ctrl = create_controller(ik_joint, offset = True, dict = node_dict, parent = grp)
                        create_constraint(ik_joint, ik_null, 0, type = "point")
                        create_constraint(sik_joint, ik_null, 1, type = "orient")
                        create_constraint(ik_ctrl, ik_joint, 1, type = "orient")
                    else:
                        ik_null, ik_ctrl = create_controller(ik_joint, local = True, offset = True, dict = node_dict,
                                                             parent = grp)
                        create_constraint(ik_joint, ik_null, 0, type = "point")
                        create_constraint(sik_joint, ik_null, 0, type = "orient")
                        create_constraint(ik_ctrl, ik_joint, 0, type = "orient")

                    if 'skirt' in ik_joint.nodeName():
                        pass
                    if 'tail' in joint_name or 'skirt' in joint_name:
                        parent_dict[ik_null] = hip_ctrl
                    elif 'hair' in joint_name:
                        parent_dict[ik_null] = head_ctrl
                    elif 'mant' in joint_name or 'wing' in joint_name:
                        parent_dict[ik_null] = chest_ctrl
                    else:
                        pass
                        print((">>> Created and No Parent: ", ik_null))

                    rev = create_reverse('{}_reverse'.format(joint_name))
                    pm.connectAttr('{}.{}_CTRL_ik0fk1'.format(root_ctrl, label), '{}.input.inputX'.format(rev),
                                   f = True)
                    # v2.1~:参照ミスの為、ik_ctrl→ik_nullに修正
                    pm.connectAttr('{}.output.outputX'.format(rev), '{}.visibility'.format(ik_null), f = True)
                    # v2.1~:参照ミスの為、ik_ctrl→fk_nullに修正
                    pm.connectAttr('{}.{}_CTRL_ik0fk1'.format(root_ctrl, label), '{}.visibility'.format(fk_null),
                                   f = True)

                    connect_visibility(root_ctrl, ik_ctrl)
                    set_lock_srt(ik_ctrl, t = True, s = True)

                    i = 3 if joint_name[:3] == 'EX_' else 2
                    ik_node = Utils.get_pynode(grp, const.DUMMY + joint_name[:i] + 'IK_' + joint_name[i:])
                    fk_node = Utils.get_pynode(grp, const.DUMMY + joint_name[:i] + 'FK_' + joint_name[i:])
                    create_ikfk_attr_selection(joint, ik_node, fk_node, root_ctrl, rev)
            # -------------------------------------------------------------------------
            # セカンダリコントローラー作成処理：決め打ち　['tail', 'skirt', 'hair', 'mant', 'wing', 'sleeve', 'bust']
            # -------------------------------------------------------------------------
            if secondary and label in const.SECONDARYJOINTNAME_LIST:
                logger.info(u'Rig作成 セカンダリーコントローラ： {}'.format(joint))
                if joint_name[:2] != 'EX':
                    pa_name = joint.getParent().stripNamespace().nodeName()

                    if label not in Utils.get_name(pa_name):

                        # if label in ['tail', 'skirt', 'hair', 'mant'] or joint_name[:6] in ['R_hair', 'L_hair', 'B_hair']:
                        if joint_name in ex_sik:
                            logger.info(u'Rig作成 SplineIK： {}'.format(joint))
                            ik_joint = node_dict.get(const.DUMMY + joint_name[:i] + 'SplineIK_' + joint_name[i:], None)
                            end_ik_joint = get_end_child(ik_joint)

                            # TODO 後半のSplineIK で変数名を使用しているので、解決できれば不要
                            if label == 'skirt':
                                IK_null_name = label + '_IK' + const.SUFFIX_NULL
                                skirt_IK_null = Utils.get_pynode(grp, IK_null_name)
                                if not skirt_IK_null:
                                    skirt_IK_null = create_group(IK_null_name, grp)
                                secondary_null = skirt_IK_null
                                node_dict[IK_null_name] = skirt_IK_null

                            elif label == 'hair':
                                IK_null_name = label + '_IK' + const.SUFFIX_NULL
                                hair_IK_null = Utils.get_pynode(grp, IK_null_name)
                                if not hair_IK_null:
                                    hair_IK_null = create_group(IK_null_name, grp)
                                secondary_null = hair_IK_null
                                node_dict[IK_null_name] = hair_IK_null

                            elif label == 'mant':
                                IK_null_name = label + '_IK' + const.SUFFIX_NULL
                                mant_IK_null = Utils.get_pynode(grp, IK_null_name)
                                if not mant_IK_null:
                                    mant_IK_null = create_group(IK_null_name, grp)
                                secondary_null = mant_IK_null
                                node_dict[IK_null_name] = mant_IK_null

                            elif label == 'wing':
                                IK_null_name = label + '_IK' + const.SUFFIX_NULL
                                wing_IK_null = Utils.get_pynode(grp, IK_null_name)
                                if not wing_IK_null:
                                    wing_IK_null = create_group(IK_null_name, grp)
                                secondary_null = wing_IK_null
                                node_dict[IK_null_name] = wing_IK_null

                            elif label == 'tail':# skirt_IK_null 以下？　新しく作成して、C_hip_null以下が良い
                                IK_null_name = label + '_IK' + const.SUFFIX_NULL
                                tail_IK_null = Utils.get_pynode(grp, IK_null_name)
                                if not tail_IK_null:
                                    tail_IK_null = create_group(IK_null_name, grp)
                                secondary_null = tail_IK_null
                                node_dict[IK_null_name] = tail_IK_null

                            else:
                                pass
                                # print(">>>>>>>>> Else label:", label)

                            handle, curve = create_spline_ik_handle(ik_joint, end_ik_joint)
                            pm.parent(curve, s_grp)
                            pm.parent(handle, s_grp)

                            s_srt = get_global_transform(ik_joint)
                            e_srt = get_global_transform(end_ik_joint)

                            cv_count = len(pm.ls('{}.cv[*]'.format(curve), fl = True))

                            sik_joint_name = joint_name[:i] + 'SplineIK_' + joint_name[i:-3]
                            sik_grp = create_group('grp_' + sik_joint_name, grp)
                            set_global_transform(sik_grp, s_srt)

                            if label in ["sleeve"]:
                                dum_name = const.DUMMY + (Utils.get_name(pa_name)).replace("_forearm", "_FK_forearm")
                            else:
                                dum_name = const.DUMMY + Utils.get_name(pa_name)

                            dum_node = node_dict.get(dum_name, None)
                            if dum_node is None:
                                raise Exception
                            pm.parent(sik_grp, dum_node)
                            # print("sik_grp, dum_node: ", sik_grp, dum_node)

                            # tail以外全て対象
                            if label != 'tail':
                                childlist = list(
                                    reversed(pm.listRelatives(ik_joint, c = True, ad = True, type = 'joint')))
                                joint1 = childlist[int(len(childlist) / 2) - 1]
                                joint2 = childlist[int(len(childlist) / 2)]
                                p1_srt = pm.xform(joint1, q = True, ws = True, a = True, t = True)
                                p2_srt = pm.xform(joint2, q = True, ws = True, a = True, t = True)

                                p_srt = []
                                p_srt.append(int(p2_srt[0] + p1_srt[0]) / 2)
                                p_srt.append(int(p2_srt[1] + p1_srt[1]) / 2)
                                p_srt.append(int(p2_srt[2] + p1_srt[2]) / 2)

                                pm.select(d = True)
                                joint_a = pm.joint(n = sik_joint_name + '_00', p = (s_srt[0], s_srt[1], s_srt[2]),
                                                   a = True)
                                joint_b = pm.joint(n = sik_joint_name + '_01', p = (p_srt[0], p_srt[1], p_srt[2]),
                                                   a = True)
                                joint_c = pm.joint(n = sik_joint_name + '_02', p = (e_srt[0], e_srt[1], e_srt[2]),
                                                   a = True)
                                joint_end = pm.joint(n = sik_joint_name + '_End', p = (e_srt[0], e_srt[1], e_srt[2]),
                                                     a = True)

                                pm.select([curve, joint_a, joint_b, joint_c])

                                pm.joint(joint_a, e = True, oj = 'xyz', secondaryAxisOrient = 'yup', ch = True,
                                         zso = True)
                                # pm.parent(joint_b, joint_a)
                                pm.parent(joint_c, joint_a)
                                pm.delete(joint_end)

                                skin = pm.skinCluster([joint_a, joint_b, joint_c, curve], bm = 0, dr = 4.0, tsb = True,
                                                      n = '{}_skin'.format(ik_joint.stripNamespace().nodeName()))
                                bind_pose = pm.listConnections(skin, s = True, d = False, type = 'dagPose')[0]
                                pm.rename(bind_pose, '{}_bindPose'.format(skin))

                                cv = []
                                base_length = [round(e_srt[0] - s_srt[0], 3), round(e_srt[1] - s_srt[1], 3),
                                               round(e_srt[2] - s_srt[2], 3)]

                                sp_length = Utils.get_length(p_srt, s_srt)
                                pe_length = Utils.get_length(e_srt, p_srt)

                                for c in range(cv_count):
                                    cp_srt = pm.xform('{}.cv[{}]'.format(curve, c), q = True, ws = True, a = True,
                                                      t = True)

                                    sp = [round(cp_srt[0] - s_srt[0], 3), round(cp_srt[1] - s_srt[1], 3),
                                          round(cp_srt[2] - s_srt[2], 3)]

                                    point_length = Utils.get_length(s_srt, cp_srt)

                                    if c != 0:
                                        angle = Utils.get_angle(base_length, sp)
                                        point_length = point_length * angle

                                    if point_length < sp_length:
                                        v1 = float(1.0 - round(int(point_length / sp_length), 2))
                                        v2 = round(int(point_length / sp_length), 2)
                                        cv.append([(joint_a, v1), (joint_b, v2), (joint_c, 0.0)])
                                    else:
                                        v1 = float(1.0 - round((int(point_length - sp_length) / pe_length), 2))
                                        v2 = round((int(point_length - sp_length) / pe_length), 2)
                                        cv.append([(joint_a, 0.0), (joint_b, v1), (joint_c, v2)])

                                for i, v in enumerate(cv):
                                    pm.skinPercent(skin, '{}.cv[{}]'.format(curve, str(i)), transformValue = v)

                                pm.parent(joint_a, sik_grp)
                                pm.select(d = True)

                                b_null, b_ctrl = create_controller(joint_b, type = 'oct', offset = True,
                                                                   dict = node_dict, parent = grp)
                                c_null, c_ctrl = create_controller(joint_c, type = 'oct', offset = True,
                                                                   dict = node_dict, parent = grp)

                                connect_visibility(root_ctrl, b_null)
                                connect_visibility(root_ctrl, c_null)

                                set_lock_srt(b_ctrl, s = True)
                                set_lock_srt(c_ctrl, s = True)

                                pm.parent(b_null, secondary_null)
                                pm.parent(c_null, secondary_null)

                                create_constraint(b_ctrl, joint_b, 0, type = "point")
                                create_constraint(c_ctrl, joint_c, 0, type = "point")

                            elif label == 'tail':
                                childlist = list(
                                    reversed(pm.listRelatives(ik_joint, c = True, ad = True, type = 'joint')))

                                joint1 = childlist[int(len(childlist) / 3) - 1]
                                joint2 = childlist[int(len(childlist) / 3)]

                                j1_srt = pm.xform(joint1, q = True, ws = True, a = True, t = True)
                                j2_srt = pm.xform(joint2, q = True, ws = True, a = True, t = True)

                                p1_srt = []
                                p1_srt.append(int(j2_srt[0] + j1_srt[0]) / 2)
                                p1_srt.append(int(j2_srt[1] + j1_srt[1]) / 2)
                                p1_srt.append(int(j2_srt[2] + j1_srt[2]) / 2)

                                p2_srt = []
                                p2_srt.append(int(e_srt[0] + p1_srt[0]) / 2)
                                p2_srt.append(int(e_srt[1] + p1_srt[1]) / 2)
                                p2_srt.append(int(e_srt[2] + p1_srt[2]) / 2)

                                pm.select(d = True)
                                joint_a = pm.joint(n = sik_joint_name + '_00', p = (s_srt[0], s_srt[1], s_srt[2]),
                                                   a = True)
                                joint_b = pm.joint(n = sik_joint_name + '_01', p = (p1_srt[0], p1_srt[1], p1_srt[2]),
                                                   a = True)
                                joint_c = pm.joint(n = sik_joint_name + '_02', p = (p2_srt[0], p2_srt[1], p2_srt[2]),
                                                   a = True)
                                joint_d = pm.joint(n = sik_joint_name + '_03', p = (e_srt[0], e_srt[1], e_srt[2]),
                                                   a = True)
                                joint_end = pm.joint(n = sik_joint_name + '_End', p = (e_srt[0], e_srt[1], e_srt[2]),
                                                     a = True)

                                pm.select([curve, joint_a, joint_b, joint_c, joint_d])

                                pm.joint(joint_a, e = True, oj = 'xyz', secondaryAxisOrient = 'yup', ch = True,
                                         zso = True)
                                # pm.parent(joint_b, joint_a)
                                pm.parent(joint_c, joint_a)
                                pm.parent(joint_d, joint_a)
                                pm.delete(joint_end)

                                skin = pm.skinCluster([joint_a, joint_b, joint_c, joint_d, curve], bm = 0, dr = 4.0,
                                                      tsb = True,
                                                      n = '{}_skin'.format(ik_joint.stripNamespace().nodeName()))
                                bind_pose = pm.listConnections(skin, s = True, d = False, type = 'dagPose')
                                if bind_pose is not None:
                                    pm.rename(bind_pose, '{}_bindPose'.format(skin))

                                cv = []
                                base_length = [round(e_srt[0] - s_srt[0], 3), round(e_srt[1] - s_srt[1], 3),
                                               round(e_srt[2] - s_srt[2], 3)]

                                sp_length = Utils.get_length(p1_srt, s_srt)
                                pp_length = Utils.get_length(p2_srt, p1_srt)
                                pe_length = Utils.get_length(e_srt, p2_srt)

                                sp2_length = Utils.get_length(p2_srt, s_srt)

                                for c in range(cv_count):
                                    cp_srt = pm.xform('{}.cv[{}]'.format(curve, c), q = True, ws = True, a = True,
                                                      t = True)

                                    sp = [round(cp_srt[0] - s_srt[0], 3), round(cp_srt[1] - s_srt[1], 3),
                                          round(cp_srt[2] - s_srt[2], 3)]

                                    point_length = Utils.get_length(cp_srt, s_srt)

                                    if c != 0:
                                        angle = Utils.get_angle(base_length, sp)
                                        point_length = point_length * angle

                                    if point_length <= sp_length:
                                        v1 = float(1.0 - round(int(point_length / sp_length), 2))
                                        v2 = float(round(int(point_length / sp_length), 2))
                                        cv.append([(joint_a, v1), (joint_b, v2), (joint_c, 0.0), (joint_d, 0.0)])

                                    elif (point_length > sp_length) and (point_length <= sp2_length):
                                        v1 = float(1.0 - round(int(point_length - sp_length) / pp_length), 2)
                                        v2 = float(round(int(point_length - sp_length) / pp_length), 2)
                                        cv.append([(joint_a, 0.0), (joint_b, v1), (joint_c, v2), (joint_d, 0.0)])

                                    elif point_length > sp2_length:
                                        v1 = float(1.0 - round(int(point_length - sp2_length) / pe_length), 2)
                                        v2 = float(round(int(point_length - sp2_length) / pe_length), 2)
                                        cv.append([(joint_a, 0.0), (joint_b, 0.0), (joint_c, v1), (joint_d, v2)])

                                for i, v in enumerate(cv):
                                    pm.skinPercent(skin, '{}.cv[{}]'.format(curve, str(i)), transformValue = v)

                                pm.parent(joint_a, sik_grp)
                                pm.select(d = True)

                                b_null, b_ctrl = create_controller(joint_b, type = 'oct', offset = True,
                                                                   dict = node_dict, parent = grp)
                                c_null, c_ctrl = create_controller(joint_c, type = 'oct', offset = True,
                                                                   dict = node_dict, parent = grp)
                                d_null, d_ctrl = create_controller(joint_d, type = 'oct', offset = True,
                                                                   dict = node_dict, parent = grp)

                                connect_visibility(root_ctrl, b_null)
                                connect_visibility(root_ctrl, c_null)
                                connect_visibility(root_ctrl, d_null)

                                set_lock_srt(b_ctrl, s = True)
                                set_lock_srt(c_ctrl, s = True)
                                set_lock_srt(d_ctrl, s = True)
                                pm.parent(b_null, secondary_null)
                                pm.parent(c_null, secondary_null)
                                pm.parent(d_null, secondary_null)

                                create_constraint(b_ctrl, joint_b, 0, type = "point")
                                create_constraint(c_ctrl, joint_c, 0, type = "point")
                                create_constraint(d_ctrl, joint_d, 0, type = "point")
            # -------------------------------------------------------------------------
            # セカンダリコントローラー作成処理：EXジョイント
            # -------------------------------------------------------------------------
            if ex_flag and joint_name[:2] == 'EX':
                logger.info(u'Rig作成 EXコントローラ： {}'.format(joint))
                i = 3

                p_joint = joint.getParent()
                p_joint_name = Utils.get_name(p_joint)
                p_joint_ctrl = Utils.get_pynode(grp, p_joint_name + const.SUFFIX_CTRL)

                # EX かつスプラインIK指定のものは除外リストに追加
                # TODO ジョイントごとに都度作成する必要があるか確認。
                ex_ignore_list = []
                for j in ex_sik:
                    children = pm.listRelatives(Utils.get_pynode(grp, j), c = True, ad = True, type = 'joint') or []
                    ex_ignore_list.append(j)
                    ex_ignore_list.extend(children)

                # 除外リストに無い場合
                if not (joint_name in ex_ignore_list):
                    ex_null, ex_ctrl = create_controller(joint, local = True, type = 'cube', dict = node_dict,
                                                         parent = grp)
                    if joint_name[-3:] != '_00':
                        parent_dict[ex_null] = p_joint_ctrl if p_joint_ctrl else root_ctrl
                    else:
                        parent_dict[ex_null] = root_ctrl
                        create_constraint(p_joint, ex_null, 1, type = "parent")

                        # 親ジョイント以下に配置しないので、orientではなくParentコンストレインをかける  # create_constraint(p_joint, ex_null, 1, type="orient")

                    # create_parentconstraint(ctrl, joint, 1)
                    create_constraint(ex_ctrl, joint, 1, type = "orient")
                    connect_visibility(root_ctrl, ex_ctrl)
                    set_lock_srt(ex_ctrl, t = True, s = True)

                # 除外リストにある場合
                else:
                    fk_joint = node_dict.get(const.DUMMY + joint_name[:i] + 'FK_' + joint_name[i:], None)
                    fk_null, fk_ctrl = create_controller(fk_joint, local = True, type = 'cube', dict = node_dict,
                                                         parent = grp)

                    if not (label in p_joint_name) and p_joint_ctrl:
                        parent_dict[fk_null] = p_joint_ctrl
                    else:
                        pa_name = Utils.get_name(fk_joint.getParent())[6:] + const.SUFFIX_CTRL

                        # TODO: forearmのnull,CTRLを要所で例外的な名前として処理しているので暫定対応
                        if 'IK_forearm' in pa_name:
                            pa_name = pa_name.replace('IK_forearm' + const.SUFFIX_CTRL, 'IK_hand_rot_null')
                        # TODO: upperarmのnull,CTRLを要所で例外的な名前として処理しているので暫定対応
                        elif 'IK_upperarm' in pa_name:
                            pa_name = pa_name.replace('IK_upperarm', 'FK_upperarm')

                        parent_dict[fk_null] = Utils.get_pynode(grp, pa_name)

                    create_constraint(fk_ctrl, fk_joint, 1, type = "orient")

                    connect_visibility(root_ctrl, fk_ctrl)
                    set_lock_srt(fk_ctrl, t = True, s = True)

                    ik_joint = node_dict.get(const.DUMMY + joint_name[:i] + 'IK_' + joint_name[i:], None)
                    sik_joint = node_dict.get(const.DUMMY + joint_name[:i] + 'SplineIK_' + joint_name[i:], None)

                    ik_null, ik_ctrl = create_controller(ik_joint, local = True, type = 'cube', offset = True,
                                                         dict = node_dict, parent = grp)
                    set_wire_color(ik_ctrl, 19)
                    create_constraint(ik_joint, ik_null, 0, type = "point")
                    create_constraint(sik_joint, ik_null, 0, type = "orient")
                    create_constraint(ik_ctrl, ik_joint, 0, type = "orient")

                    if const.DUMMY in Utils.get_name(ik_joint.getParent()):
                        p_ik_ctrl_name = Utils.get_name(ik_joint.getParent())[6:] + const.SUFFIX_CTRL
                    else:
                        p_ik_ctrl_name = Utils.get_name(ik_joint.getParent()) + const.SUFFIX_CTRL

                    # IK_handがあれば置き換え
                    if "IK_hand" in p_ik_ctrl_name:
                        p_ik_ctrl_name = p_ik_ctrl_name.replace('IK_hand', 'IK_hand_trans')

                    # TODO: forearmのnull,CTRLを要所で例外的な名前として処理しているので暫定対応
                    elif "IK_forearm" in p_ik_ctrl_name:
                        p_ik_ctrl_name = p_ik_ctrl_name.replace('IK_forearm' + const.SUFFIX_CTRL, 'IK_hand_rot_null')

                    # TODO: upperarmのnull,CTRLを要所で例外的な名前として処理しているので暫定対応
                    elif "IK_upperarm" in p_ik_ctrl_name:
                        p_ik_ctrl_name = p_ik_ctrl_name.replace('IK_upperarm', 'FK_upperarm')

                    p_ik_ctrl = Utils.get_pynode(grp, p_ik_ctrl_name)

                    parent_dict[ik_null] = p_ik_ctrl

                    rev = create_reverse('{}_reverse'.format(joint_name))
                    pm.connectAttr('{}.{}_CTRL_ik0fk1'.format(root_ctrl, 'ex_node'), '{}.input.inputX'.format(rev),
                                   f = True)

                    pm.connectAttr('{}.output.outputX'.format(rev), '{}.visibility'.format(ik_null), f = True)
                    # 参照ミスの為、null → fk_nullに変更
                    pm.connectAttr('{}.{}_CTRL_ik0fk1'.format(root_ctrl, 'ex_node'), '{}.visibility'.format(fk_null),
                                   f = True)

                    connect_visibility(root_ctrl, ik_ctrl)
                    set_lock_srt(ik_ctrl, t = True, s = True)

                    i = 3 if joint_name[:3] == 'EX_' else 2
                    ik_node = Utils.get_pynode(grp, const.DUMMY + joint_name[:i] + 'IK_' + joint_name[i:])
                    fk_node = Utils.get_pynode(grp, const.DUMMY + joint_name[:i] + 'FK_' + joint_name[i:])
                    create_ikfk_attr_selection(joint, ik_node, fk_node, root_ctrl, rev)

                # TODO SplineIK系の処理が可変仕様移行時に例外が出てきたので、要確認
                if ex_s_flag and joint_name in ex_sik:
                    logger.info(u'Rig作成 SplineIK： {}'.format(joint))
                    if label not in Utils.get_name(joint.getParent()):

                        ik_joint_name = const.DUMMY + joint_name[:i] + 'SplineIK_' + joint_name[i:]
                        ik_joint = node_dict.get(ik_joint_name, None)
                        end_ik_joint = get_end_child(ik_joint)

                        secondary_null_name = joint_name + const.SUFFIX_NULL
                        secondary_null = Utils.get_pynode(grp, secondary_null_name)

                        if not secondary_null:
                            secondary_null = create_group('{}_null'.format(joint_name), parent = grp)

                        if const.DUMMY in Utils.get_name(ik_joint.getParent()):
                            p_ctrl_name = Utils.get_name(ik_joint.getParent())[6:] + const.SUFFIX_CTRL
                        else:
                            p_ctrl_name = Utils.get_name(ik_joint.getParent()) + const.SUFFIX_CTRL

                        if 'IK_hand' in p_ctrl_name:
                            p_ctrl_name = p_ctrl_name.replace('IK_hand', 'IK_hand_trans')

                        # TODO: forearmのnull,CTRLを要所で例外的な名前として処理しているので暫定対応
                        elif "IK_forearm" in p_ctrl_name:
                            p_ctrl_name = p_ctrl_name.replace('IK_forearm' + const.SUFFIX_CTRL, 'IK_hand_rot_null')

                        # TODO: upperarmのnull,CTRLを要所で例外的な名前として処理しているので暫定対応
                        elif "IK_upperarm" in p_ctrl_name:
                            p_ctrl_name = p_ctrl_name.replace('IK_upperarm', 'FK_upperarm')

                        else:
                            pass

                        p_ctrl = Utils.get_pynode(grp, p_ctrl_name)
                        if p_ctrl:
                            # print("ik_joint, secondary_null, p_ctrl", ik_joint, secondary_null, p_ctrl)
                            pm.parent(secondary_null, p_ctrl)

                        handle, curve = create_spline_ik_handle(ik_joint, end_ik_joint)
                        pm.parent(curve, s_grp)
                        pm.parent(handle, s_grp)

                        s_srt = get_global_transform(ik_joint)
                        e_srt = get_global_transform(end_ik_joint)

                        cv_count = len(pm.ls('{}.cv[*]'.format(curve), fl = True))

                        sik_joint_name = joint_name[:i] + 'SplineIK_' + joint_name[i:-3]

                        sik_grp = create_group('grp_' + sik_joint_name)
                        set_global_transform(sik_grp, s_srt)

                        p_node = Utils.get_pynode(grp, Utils.get_name(ik_joint.getParent()))
                        pm.parent(sik_grp, p_node)

                        childlist = list(
                            reversed(pm.listRelatives(ik_joint, c = True, ad = True, type = 'joint') or []))
                        joint1 = childlist[int(len(childlist) / 2) - 1]
                        joint2 = childlist[int(len(childlist) / 2)]
                        p1_srt = pm.xform(joint1, q = True, ws = True, a = True, t = True)
                        p2_srt = pm.xform(joint2, q = True, ws = True, a = True, t = True)

                        p_srt = []
                        p_srt.append(int(p2_srt[0] + p1_srt[0]) / 2)
                        p_srt.append(int(p2_srt[1] + p1_srt[1]) / 2)
                        p_srt.append(int(p2_srt[2] + p1_srt[2]) / 2)

                        pm.select(d = True)
                        joint_a = pm.joint(n = sik_joint_name + '_00', p = (s_srt[0], s_srt[1], s_srt[2]), a = True)
                        joint_b = pm.joint(n = sik_joint_name + '_01', p = (p_srt[0], p_srt[1], p_srt[2]), a = True)
                        joint_c = pm.joint(n = sik_joint_name + '_02', p = (e_srt[0], e_srt[1], e_srt[2]), a = True)
                        joint_end = pm.joint(n = sik_joint_name + '_End', p = (e_srt[0], e_srt[1], e_srt[2]), a = True)

                        pm.select([curve, joint_a, joint_b, joint_c])

                        pm.joint(joint_a, e = True, oj = 'xyz', secondaryAxisOrient = 'yup', ch = True, zso = True)
                        # pm.parent(joint_b, joint_a)
                        pm.parent(joint_c, joint_a)
                        pm.delete(joint_end)

                        skin = pm.skinCluster([joint_a, joint_b, joint_c, curve], bm = 0, dr = 4.0, tsb = True,
                                              n = '{}_skin'.format(ik_joint.stripNamespace().nodeName()))
                        bind_pose = pm.listConnections(skin, s = True, d = False, type = 'dagPose')
                        if bind_pose is not None:
                            pm.rename(bind_pose, '{}_bindPose'.format(skin))

                        # CVの座標計算
                        cv = []
                        base_length = [round(e_srt[0] - s_srt[0], 3), round(e_srt[1] - s_srt[1], 3),
                                       round(e_srt[2] - s_srt[2], 3)]

                        sp_length = Utils.get_length(p_srt, s_srt)
                        pe_length = Utils.get_length(e_srt, p_srt)

                        for c in range(cv_count):
                            cp_srt = pm.xform('{}.cv[{}]'.format(curve, c), q = True, ws = True, a = True, t = True)

                            sp = [round(cp_srt[0] - s_srt[0], 3), round(cp_srt[1] - s_srt[1], 3),
                                  round(cp_srt[2] - s_srt[2], 3)]

                            point_length = Utils.get_length(s_srt, cp_srt)

                            if c != 0:
                                angle = Utils.get_angle(base_length, sp)
                                point_length = point_length * angle

                            if point_length < sp_length:
                                v1 = float(1.0 - round(int(point_length / sp_length), 2))
                                v2 = round(int(point_length / sp_length), 2)
                                cv.append([(joint_a, v1), (joint_b, v2), (joint_c, 0.0)])
                            else:
                                v1 = float(1.0 - round(int(point_length - sp_length) / pe_length, 2))
                                v2 = round(int(point_length - sp_length) / pe_length, 2)
                                cv.append([(joint_a, 0.0), (joint_b, v1), (joint_c, v2)])

                        for i, v in enumerate(cv):
                            pm.skinPercent(skin, '{}.cv[{}]'.format(curve, str(i)), transformValue = v)

                        pm.parent(joint_a, sik_grp)
                        pm.select(d = True)

                        b_null, b_ctrl = create_controller(joint_b, type = 'oct', offset = True, dict = node_dict,
                                                           parent = grp)
                        c_null, c_ctrl = create_controller(joint_c, type = 'oct', offset = True, dict = node_dict,
                                                           parent = grp)

                        rev = create_reverse('{}_reverse'.format(sik_joint))

                        pm.connectAttr('{}.{}_CTRL_ik0fk1'.format(root_ctrl, 'ex_node'), '{}.input.inputX'.format(rev),
                                       f = True)
                        pm.connectAttr('{}.output.outputX'.format(rev), '{}.visibility'.format(b_ctrl), f = True)
                        pm.connectAttr('{}.output.outputX'.format(rev), '{}.visibility'.format(c_ctrl), f = True)

                        connect_visibility(root_ctrl, b_null)
                        connect_visibility(root_ctrl, c_null)

                        set_lock_srt(b_ctrl, r = True, s = True)
                        set_lock_srt(c_ctrl, r = True, s = True)

                        pm.parent(b_null, secondary_null)
                        pm.parent(c_null, secondary_null)

                        create_constraint(b_ctrl, joint_b, 0, type = "point")
                        create_constraint(c_ctrl, joint_c, 0, type = "point")
                else:
                    pass  # print(">>> CHECK: joint_name NOT in ex_sik: ", joint_name)

    Utils.print_info(" {}:{} joint setting: Finished".format(num, 'ex'))

    # -------------------------------------------------------------------------
    # コントローラノードの階層化設定処理
    # -------------------------------------------------------------------------
    logger.info(u'ノードの階層化')
    for ch, pa in list(parent_dict.items()):
        if not isinstance(ch, pm.PyNode):
            print((u">> ch is not PyNode: ", ch))
            return False

        if not isinstance(pa, pm.PyNode):
            pa_node = node_dict.get(pa, None)
            if pa_node is None:
                Utils.print_info(u">> ch is ", ch)
                Utils.print_info(u">> pa is None ", pa)
                pa = root_ctrl
                return False
        try:
            # print("ch, pa", ch, pa)
            pm.parent(ch, pa)
            set_lock_srt(ch, t = True, r = True)

            if const.HEADJOINTNAME not in ch.nodeName():
                set_lock_srt(ch, s = True)

        except Exception as e:
            logger.error(e)

    logger.info(u"ノードの階層化処理：　完了")
    # -------------------------------------------------------------------------
    # 頭、体のスケール設定処理
    # -------------------------------------------------------------------------
    logger.info(u'スケール設定')
    scale = True
    md = 'multiplyDivide_'
    cd = 'condition_'

    if scale:
        # スケール設定で使用する変数
        C_head_null = node_dict.get("C_head_null", None)

        # rig scale settings -----------------------------------------------------------------------------------------------
        for node in [root_ctrl, grp_dummy, root_bone]:
            pm.connectAttr('{}.{}'.format(root_ctrl, const.ATTR_BODYSCALE), '{}.scaleX'.format(node), f = True)
            pm.connectAttr('{}.{}'.format(root_ctrl, const.ATTR_BODYSCALE), '{}.scaleY'.format(node), f = True)
            pm.connectAttr('{}.{}'.format(root_ctrl, const.ATTR_BODYSCALE), '{}.scaleZ'.format(node), f = True)

        multi = pm.shadingNode('multiplyDivide', n = md + 'head_Scale', au = True)

        pm.setAttr('{}.operation'.format(multi), 2)
        pm.setAttr('{}.input1'.format(multi), *[1, 1, 1], type = "double3")

        pm.connectAttr('{}.scale'.format(root_ctrl), '{}.input2'.format(multi), f = True)

        pm.connectAttr('{}.output'.format(multi), '{}.scale'.format(C_head_null), f = True)

        xs_condition = pm.shadingNode('condition', n = cd + 'XS_Size', au = True)
        xs_val = const.SIZE_DICT['XS']['value']
        xs_id = const.SIZE_DICT['XS']['index']
        pm.setAttr('{}.secondTerm'.format(xs_condition), xs_id)
        pm.setAttr('{}.colorIfTrue'.format(xs_condition), *[xs_val, xs_val, xs_val], type = "double3")
        pm.connectAttr('{}.{}'.format(root_ctrl, const.ATTR_CHARSIZE), '{}.firstTerm'.format(xs_condition), f = True)

        s_condition = pm.shadingNode('condition', n = cd + 'S_Size', au = True)
        s_val = const.SIZE_DICT['S']['value']
        s_id = const.SIZE_DICT['S']['index']
        pm.setAttr('{}.secondTerm'.format(s_condition), s_id)
        pm.setAttr('{}.colorIfTrue'.format(s_condition), *[s_val, s_val, s_val], type = "double3")
        pm.connectAttr('{}.{}'.format(root_ctrl, const.ATTR_CHARSIZE), '{}.firstTerm'.format(s_condition), f = True)

        l_condition = pm.shadingNode('condition', n = cd + 'L_Size', au = True)
        l_val = const.SIZE_DICT['L']['value']
        l_id = const.SIZE_DICT['L']['index']
        pm.setAttr('{}.secondTerm'.format(l_condition), l_id)
        pm.setAttr('{}.colorIfTrue'.format(l_condition), *[l_val, l_val, l_val], type = "double3")
        pm.connectAttr('{}.{}'.format(root_ctrl, const.ATTR_CHARSIZE), '{}.firstTerm'.format(l_condition), f = True)

        s_farm_condition = pm.shadingNode('condition', n = cd + 'S_Farm_Size', au = True)
        s_fram_val = const.SIZE_DICT['S_farm']['value']
        s_farm_id = const.SIZE_DICT['S_farm']['index']
        pm.setAttr('{}.secondTerm'.format(s_farm_condition), s_farm_id)
        pm.setAttr('{}.colorIfTrue'.format(s_farm_condition), *[s_fram_val, s_fram_val, s_fram_val], type = "double3")
        pm.connectAttr('{}.{}'.format(root_ctrl, const.ATTR_CHARSIZE), '{}.firstTerm'.format(s_farm_condition), f = True)

        l_farm_condition = pm.shadingNode('condition', n = cd + 'L_Farm_Size', au = True)
        l_fram_val = const.SIZE_DICT['L_farm']['value']
        l_farm_id = const.SIZE_DICT['L_farm']['index']
        pm.setAttr('{}.secondTerm'.format(l_farm_condition), l_farm_id)
        pm.setAttr('{}.colorIfTrue'.format(l_farm_condition), *[l_fram_val, l_fram_val, l_fram_val], type = "double3")
        pm.connectAttr('{}.{}'.format(root_ctrl, const.ATTR_CHARSIZE), '{}.firstTerm'.format(l_farm_condition), f = True)

        s_multi = pm.shadingNode('multiplyDivide', n = md + 'Scale_XS_S', au = True)
        pm.setAttr('{}.operation'.format(s_multi), 1)
        pm.setAttr('{}.input1'.format(s_multi), *[1, 1, 1], type = "double3")

        s_farm_multi = pm.shadingNode('multiplyDivide', n = md + 'Scale_Farm_XS_S', au = True)
        pm.setAttr('{}.operation'.format(s_farm_multi), 1)
        pm.setAttr('{}.input1'.format(s_farm_multi), *[1, 1, 1], type = "double3")

        s_pariari_farm_multi = pm.shadingNode('multiplyDivide', n = md + 'Scale_Priari_Farm_S', au = True)
        pm.setAttr('{}.operation'.format(s_pariari_farm_multi), 1)
        pm.setAttr('{}.input1'.format(s_pariari_farm_multi), *[1, 1, 1], type = "double3")

        l_multi = pm.shadingNode('multiplyDivide', n = md + 'Scale_L', au = True)
        pm.setAttr('{}.operation'.format(l_multi), 1)
        pm.setAttr('{}.input1'.format(l_multi), *[1, 1, 1], type = "double3")

        l_farm_multi = pm.shadingNode('multiplyDivide', n = md + 'Scale_Farm_L', au = True)
        pm.setAttr('{}.operation'.format(l_farm_multi), 1)
        pm.setAttr('{}.input1'.format(l_farm_multi), *[1, 1, 1], type = "double3")

        l_pariari_farm_multi = pm.shadingNode('multiplyDivide', n = md + 'Scale_Priari_Farm_L', au = True)
        pm.setAttr('{}.operation'.format(l_pariari_farm_multi), 1)
        pm.setAttr('{}.input1'.format(l_pariari_farm_multi), *[1, 1, 1], type = "double3")

        pariari_farm_multi = pm.shadingNode('multiplyDivide', n = md + 'Scale_Priari_Farm', au = True)
        pm.setAttr('{}.operation'.format(pariari_farm_multi), 1)
        pm.setAttr('{}.input1'.format(pariari_farm_multi), *[1, 1, 1], type = "double3")

        pm.connectAttr('{}.outColor'.format(xs_condition), '{}.input1'.format(s_multi), f = True)
        pm.connectAttr('{}.outColor'.format(s_condition), '{}.input2'.format(s_multi), f = True)
        pm.connectAttr('{}.outColor'.format(s_farm_condition), '{}.input1'.format(s_farm_multi), f = True)
        pm.connectAttr('{}.output'.format(s_multi), '{}.input1'.format(s_pariari_farm_multi), f = True)
        pm.connectAttr('{}.output'.format(s_farm_multi), '{}.input2'.format(s_pariari_farm_multi), f = True)
        pm.connectAttr('{}.output'.format(s_pariari_farm_multi), '{}.input1'.format(pariari_farm_multi), f = True)

        pm.connectAttr('{}.outColor'.format(l_condition), '{}.input2'.format(l_multi), f = True)
        pm.connectAttr('{}.outColor'.format(l_farm_condition), '{}.input2'.format(l_farm_multi), f = True)
        pm.connectAttr('{}.output'.format(l_multi), '{}.input1'.format(l_pariari_farm_multi), f = True)
        pm.connectAttr('{}.output'.format(l_farm_multi), '{}.input1'.format(l_pariari_farm_multi), f = True)
        pm.connectAttr('{}.output'.format(l_pariari_farm_multi), '{}.input2'.format(pariari_farm_multi), f = True)

        pm.connectAttr('{}.outputX'.format(pariari_farm_multi), '{}.{}'.format(root_ctrl, const.ATTR_BODYSCALE), f = True)

        logger.info(u'スケール設定：完了')
    # rig scale settings Finished-----------------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # SplineIKコントローラー作成処理
    # -------------------------------------------------------------------------
    logger.info(
        u'SplineIK: Secondary IKFK　及び Visibilityスイッチ作成 {}'.format(",".join(["hair", "skirt", "tail", "mant", "wing"])))
    # ================================================================
    for sik_name in ["hair", "skirt", "tail", "mant", "wing"]:
        # grp 以下の"*_SplineIK_{}*_CTRL"を探す
        spline_list = [Utils.get_pynode(grp, tr) for tr in
                       cmds.ls('*_SplineIK_{}*{}'.format(sik_name, const.SUFFIX_CTRL), tr = True) if
                       Utils.get_pynode(grp, tr)]
        # EXは既にVisivilityコントロールが接続されている為、除外
        spline_list = [tr for tr in spline_list if not tr.nodeName().startswith("EX_")]

        # 各splineIKコントローラが、1つでも存在すれば、reverseノード作成
        if spline_list:
            rev = create_reverse('SplineIK_{}_reverse'.format(sik_name))
            pm.connectAttr('{}.{}_CTRL_ik0fk1'.format(root_ctrl, sik_name), '{}.input.inputX'.format(rev), f = True)

        for s_ctrl in spline_list:
            pm.connectAttr('{}.output.outputX'.format(rev), '{}.visibility'.format(s_ctrl), f = True)

    # SplineIK hair 統合コントローラ作成
    if hair_IK_null:
        pm.parent(hair_IK_null, head_ctrl)
    # ================================================================

    pm.setAttr('{}.visibility'.format(s_grp), 0)
    if skirt_IK_null:
        pm.parent(skirt_IK_null, hip_ctrl)
    # ================================================================
    # SplineIK Tail　統合コントローラ作成
    if tail_IK_null:
        pm.parent(tail_IK_null, hip_ctrl)
    '''secondary_name = 'tail'
    spline_tail_list = cmds.ls('C_SplineIK_{}*{}'.format(secondary_name, const.SUFFIX_CTRL), tr=True)
    spline_tail_list = [tr for tr in spline_tail_list if Utils.get_pynode(grp, tr)]
    if spline_tail_list:
        rev = create_reverse('SplineIK_tail_reverse'.format(joint))
        pm.connectAttr('{}.{}_CTRL_ik0fk1'.format(root_ctrl, secondary_name), '{}.input.inputX'.format(rev), f=True)
        for s_tail in spline_tail_list:
            pm.connectAttr('{}.output.outputX'.format(rev), '{}.visibility'.format(s_tail), f=True)'''

    # ================================================================
    # SplineIK mant　統合コントローラ作成

    if mant_IK_null:
        pm.parent(mant_IK_null, chest_ctrl)
    # ================================================================
    # SplineIK wing　統合コントローラ作成
    if wing_IK_null:
        pm.parent(wing_IK_null, chest_ctrl)
    # ================================================================

    # Wire テンプレートノードの削除
    logger.info(u'Wire テンプレートノードの削除')
    pm.delete('wire_group', hi = True)
    # ================================================================

    grp_ctrl = create_group(const.GROUPCTRLNAME, parent = grp)
    pm.parent(root_null, grp_ctrl)

    # Lockのかけ忘れが無ければ不要なので、コメントアウト。
    '''for sec_null in [hair_IK_null, mant_IK_null, skirt_IK_null]:
        set_lock_srt(sec_null, t= True, s=True, r=True)'''

    try:
        pm.parent(s_grp, grp_rig)
        pm.parent(grp_dummy, grp_rig)
        pm.parent(grp_ctrl, grp_rig)
    except Exception as e:
        print(e)

    # ================================================================
    # Connect ScaleFactor Settings 現状 defaultとenum1 のみ。２つ以上あれば繋ぎ方を変更する必要がある
    for sf_name, val_list in list(const.SCALEFACTOR_DICT.items())[1:]:

        sf_condition = pm.shadingNode('condition', n = "{}{}_{}".format(cd, const.ATTR_SCALEFACTOR, sf_name), au = True)
        sf_multi = pm.shadingNode('multiplyDivide', n = "{}{}_{}".format(md, const.ATTR_SCALEFACTOR, sf_name),
                                  au = True)
        pm.setAttr('{}.input1'.format(sf_multi), *[1, 1, 1], type = "double3")
        pm.setAttr('{}.colorIfTrue'.format(sf_condition), *val_list, type = "double3")

        if len(const.SCALEFACTOR_DICT) == 2:
            pm.connectAttr('{}.{}'.format(root_ctrl, const.ATTR_SCALEFACTOR), '{}.firstTerm'.format(sf_condition),
                           f = True)
            pm.connectAttr('{}.outColor'.format(sf_condition), '{}.input2'.format(sf_multi), f = True)
            pm.setAttr('{}.secondTerm'.format(sf_condition), 1)

            pm.connectAttr('{}.output'.format(sf_multi), '{}.scale'.format(grp_rig), f = True)
            pm.connectAttr('{}.output'.format(sf_multi), '{}.scale'.format(grp_joint), f = True)
    logger.info(u'Scale Factor 設定を追加')
    # ================================================================
    # Rig コントローラのサイズ設定
    val = const.SIZE_DICT.get(size)
    if val:
        pm.setAttr('{}.{}'.format(root_ctrl, const.ATTR_CHARSIZE), val['index'])
    logger.info(u'Rig コントローラのサイズ設定: {}　完了'.format(size))
    # ================================================================

    # ================================================================
    # Rig コントローラのカラー設定
    set_ctrl_colors(node_dict)
    logger.info(u'Rig コントローラのカラー設定　完了')
    # ================================================================
    pm.select(cl = True)
    # ================================================================
    # Rig コントローラのレイヤー設定
    create_displaylayer(nodes = [grp_rig], name = const.RIG_LAYERNAME)
    logger.info(u'Rig コントローラのレイヤー設定　完了')
    # ================================================================
    # Rig Rootコントローラの不要なアトリビュート設定削除
    remove_unused_root_attr(root_ctrl)
    logger.info(u'Rig Rootコントローラの不要なアトリビュート設定削除　完了')
    # ================================================================

    # DEBUG_DICT = node_dict
    pm.select(grp)
    logger.info(u'Rig作成 完了')

    return True


def set_ctrl_colors(node_dict):
    if node_dict is None:
        return

    # CTRL の末尾でフィルター
    node_dict = {k: v for k, v in list(node_dict.items()) if const.SUFFIX_CTRL in k}

    for name, node in list(node_dict.items()):
        num = 0
        if "_mant_" in name:
            num = 10
            if "_SplineIK_mant" in name:
                num = 18

        elif "_tail_" in name:
            num = 15
            if "_SplineIK_tail" in name:
                num = 18
            if "_IK_tail" in name:
                num = 15

        elif "_skirt_" in name:
            num = 23
            if "_SplineIK_skirt_" in name:
                num = 18

        elif "_hair_" in name:
            num = 9
            if "_SplineIK_hair" in name:
                num = 18

        elif "_wing_" in name:
            num = 7
            if "_SplineIK_wing_" in name:
                num = 18

        elif re.match(r"(R_|L_)(knee|IK_foot|IK_toe|IKFK_leg|FK_foot|FK_upperleg|FK_foreleg|FK_toe)", node.nodeName()):
            if name.startswith("L_"):
                num = 6
            elif name.startswith("R_"):
                num = 13  # print("setColor: ", name, num, node)

        elif re.match(
                r"(R_|L_)(clavicle|FK_upperarm|FK_forearm|FK_hand|IKFK_arm|bust|elbow|sleeve|IK_hand_trans|IK_hand_rot)",
                node.nodeName()):
            if name.startswith("L"):
                num = 6
            elif name.startswith("R"):
                num = 13  # print("setColor: ", name, num, node)

        elif re.match(r"(R_|L_)(thumb|index|middle|ring|pinky|ringroot)", node.nodeName()):
            if name.startswith("L_"):
                num = 6
            elif name.startswith("R_"):
                num = 13  # print("setColor: ", name, num, node)

        elif re.match(r"(C_)(neck|head|chest|spine|hip)", node.nodeName()):
            num = 17  # print("setColor: ", name, num, node)

        elif re.match(r"^(EX_)", node.nodeName()):
            num = 31
            if "_SplineIK_wing_" in name:
                num = 18
        else:
            num = 16
            pass

        if num == 0:
            print((" >  Else, setColor: ", name, num, node))

        set_wire_color(node, num)


def reset_ctrl_transform(grp=None, pos=True, rot=True, sca=True):
    ctrl_list = [ctrl for ctrl in pm.ls(grp, dag = True, tr = True) if "_CTRL" in ctrl.nodeName()]
    for ctrl in ctrl_list:
        if pos:
            for attr in ["tx", "ty", "tz"]:
                if not pm.getAttr('{}.{}'.format(ctrl, attr), lock = True):
                    # pm.setAttr('{}.{}'.format(ctrl, attr), lock=False)
                    pm.setAttr('{}.{}'.format(ctrl, attr), 0)  # pm.move(0, ctrl, x=True, os=True, a=True)

        if rot:
            for attr in ["rx", "ry", "rz"]:
                if not pm.getAttr('{}.{}'.format(ctrl, attr), lock = True):
                    # pm.setAttr('{}.{}'.format(ctrl, attr), lock=False)
                    pm.setAttr('{}.{}'.format(ctrl, attr), 0)

        # bust のみ例外としてScaleコントロールを設定
        if sca and "bust" in ctrl.nodeName():
            for attr in ["sx", "sy", "sz"]:
                if not pm.getAttr('{}.{}'.format(ctrl, attr), lock = True):
                    # pm.setAttr('{}.{}'.format(ctrl, attr), lock=False)
                    # set default scale:1.0
                    pm.setAttr('{}.{}'.format(ctrl, attr), 1)  # pm.rotate(0, ctrl, x=True, os=True, a=True)


def connect_visibility(src, dst):
    dst_name = str(dst.stripNamespace().nodeName())
    if dst_name[:3] == 'EX_':
        label = 'ex_node'
    elif 'SplineIK_' in dst_name:
        label = Utils.get_label(dst_name.replace('SplineIK_', ''))
    else:
        label = Utils.get_label(dst_name)

    if label == 'tail':
        if 'up' in dst_name:
            label = label + '_up'

    attr_vis = '{}{}_Visibility'.format(label, const.SUFFIX_CTRL)
    if not pm.attributeQuery(attr_vis, node = src, exists = True):
        pm.addAttr(src, ln = attr_vis, at = "bool")
        pm.setAttr('{}.{}'.format(src, attr_vis), e = True, channelBox = True)

        print(("addAttribute:", src, attr_vis))

    pm.connectAttr('{}.{}'.format(src, attr_vis), '{}.visibility'.format(dst), f = True)


def pm_dup(node, name, dict={}):
    dup = pm.duplicate(node, n = name, po = True, rr = True, rc = False)[0]
    dup.rename(name)
    if dict:
        dict[name] = dup

    return dup


def goto_bindpose(joint):
    bp_list = pm.listConnections(joint, d = True, type = 'dagPose') or []
    for bp in bp_list:
        # pm.select(joint)
        # mel.eval('gotoBindPose')
        # index0のバインドポーズから実行。実行に失敗すれば次のバインドポーズを実行
        try:
            pm.dagPose(joint, bp, restore = True)
            logger.info(u'Bind Pose に戻します。')
            break
        except Exception as e:
            print(e)
            continue


def select_ctrl_main(grp=None, pos=True, rot=True):
    pm.undoInfo(openChunk = True)
    # -----------------------------------------------------------------
    logger.info(u'コントローラーを選択します。')
    if grp:
        select_ctrl(grp = grp, pos = pos, rot = rot)
    else:
        if pm.ls(sl = True):
            grp_name = pm.ls(sl = True)[0]
            select_ctrl(grp = grp_name, pos = pos, rot = rot)
        else:
            select_ctrl(pos = pos, rot = rot)
    # -----------------------------------------------------------------
    pm.undoInfo(closeChunk = True)


def select_ctrl(grp=None, pos=False, rot=False):
    select_list = []
    ctrl_list = [ctrl for ctrl in pm.ls('*{}'.format(const.SUFFIX_CTRL), l = True) if re.search(grp, ctrl.longName())]

    for ctrl in ctrl_list:
        if pos:
            pos_locked = False
            for attr in ["tx", "ty", "tz"]:
                if pm.getAttr('{}.{}'.format(ctrl, attr), lock = True):
                    pos_locked = True
                    break
            if not pos_locked:
                select_list.append(ctrl)

        if rot:
            rot_locked = False
            for attr in ["rx", "ry", "rz"]:
                if pm.getAttr('{}.{}'.format(ctrl, attr), lock = True):
                    rot_locked = True
                    break
            if not rot_locked:
                select_list.append(ctrl)

    pm.select(select_list)


# ----------------------------------------------------------------------------------------------------------------------
# DELETE FUNCTION
# ----------------------------------------------------------------------------------------------------------------------
def delete_rig(grp_rig, keep_nodes=[]):
    u"""
       リグ関連ノードの削除処理
        :param grp_rig: PyNode
        :param keep_nodes: list of PyNode
        :return failed_list:
        :rtype list of PyNode:
    """
    sels = pm.selected()

    if not sels:
        return

    grp = sels[0]
    ns = Utils.get_namespace(grp)

    if not grp_rig or not isinstance(grp_rig, pm.PyNode):
        return

    trans_dict = {}
    for node in keep_nodes:
        print(("keep_node:", node))
        trans_dict[node] = dict(sc = pm.xform(node, q = True, s = True, r = True))

    failed_list = []
    # リファレンス状態のリグ削除は不具合が多いので考慮しない。ネームスペース対応が必要な時に有効化
    # grp_sik = Utils.get_pynode(grp_rig, const.GROUPSIKNAME)
    # grp_dum = Utils.get_pynode(grp_rig, const.GROUPDUMNAME)
    # grp_ctrl = Utils.get_pynode(grp_rig, const.GROUPCTRLNAME)
    # grp_joint = Utils.get_pynode(grp, const.GROUPJOINTNAME)
    # root_ctrl = Utils.get_pynode(grp, const.ROOTCTRLNAME)
    # root = Utils.get_pynode(grp, ns + const.ROOTJOINTNAME)

    grp_sik = Utils.get_pynode(grp_rig, const.GROUPSIKNAME)
    grp_dum = Utils.get_pynode(grp_rig, const.GROUPDUMNAME)

    grp_ctrls = Utils.get_pynodes(grp_rig, r"^(.*)\|" + const.GROUPCTRLNAME + r"[0-9]?$")
    grp_joints = Utils.get_pynodes(grp, r"^(.*)\|" + const.GROUPJOINTNAME + r"[0-9]?$")
    root_ctrls = Utils.get_pynodes(grp, r"^(.*)\|" + const.ROOTCTRLNAME + r"[0-9]?$")
    roots = Utils.get_pynodes(grp, r"^(.*)\|" + ns + const.ROOTJOINTNAME + r"[0-9]?$")

    # scaleFactor reset
    for root_ctrl in root_ctrls:
        if pm.attributeQuery(const.ATTR_SCALEFACTOR, node = root_ctrl, exists = True):
            pm.setAttr("{}.{}".format(root_ctrl, const.ATTR_SCALEFACTOR), 0)  # default: 1.0

    # 関連するdgノードを取得、削除

    dg_nodes = Utils.get_dg_node([grp_rig.longName()])
    pm.delete(dg_nodes)

    if grp_sik:
        try:
            pm.delete(grp_sik, hi = True)
            logger.info(u'{} を削除しました。'.format(grp_sik))
        except Exception as e:
            logger.error(u'{} の削除に失敗: {}'.format(grp_sik, e))
            failed_list.append(grp_sik)

    if grp_dum:
        try:
            pm.delete(grp_dum, hi = True)
            logger.info(u'{} を削除しました。'.format(grp_dum))
        except Exception as e:
            logger.error(u'{} の削除に失敗: {}'.format(grp_dum, e))
            failed_list.append(grp_dum)

    for grp_ctrl in grp_ctrls:
        try:
            pm.delete(grp_ctrl, hi = True)
            logger.info(u'{} を削除しました。'.format(grp_ctrl))
        except Exception as e:
            logger.error(u'{} の削除に失敗: {}'.format(grp_ctrl, e))
            failed_list.append(grp_ctrl)

    if grp_rig:
        try:
            pm.delete(grp_rig, hi = True)
            logger.info(u'{} を削除しました。'.format(grp_rig))
        except Exception as e:
            logger.error(u'{} の削除に失敗: {}'.format(grp_rig, e))
            failed_list.append(grp_rig)

    for node, trans in list(trans_dict.items()):
        print(("set scale:", node))
        if node:
            pm.setAttr('{}.scale'.format(node), *trans["sc"], type = "double3")

    for root in roots:
        goto_bindpose(root)
        print(("go to bind pose root:", root.longName()))

    # SIMアトリビュートからのリネームはEXとSecondary名がバッティングする可能性があるのでOFF
    '''for grp_joint in grp_joints:
        rename_conversion(Utils.get_pyjoints(grp_joint))
        print("Renamed to SIM:", root.longName())'''

    if pm.objExists(grp):
        pm.select(grp)

    return failed_list


def delete_main():
    u"""
       リグの削除実行、削除に必要なノードの確認
        :return bool:
        :rtype bool:
    """
    pm.undoInfo(openChunk = True)
    sels = pm.selected()
    failed_list = []

    if sels:
        grp = sels[0]
        ns = Utils.get_namespace(grp)

        grp_joint = Utils.get_pynode(grp, ns + const.GROUPJOINTNAME)
        grp_mesh = Utils.get_pynode(grp, ns + const.GROUPMESHNAME)
        grp_rig = Utils.get_pynode(grp, const.GROUPRIGNAME)

        if grp_joint:
            if grp_joint.getParent() != grp:
                pm.parent(grp_joint, grp)
                # rename_sim from if attribute is True
                pm.select(grp)

        if grp_mesh:
            if grp_mesh.getParent() != grp:
                pm.parent(grp_mesh, grp)
                pm.select(grp)

        if grp_rig:
            keep_nodes = [Utils.get_pynode(grp, ns + const.HEADJOINTNAME),
                          Utils.get_pynode(grp, ns + const.ROOTJOINTNAME)]
            print((keep_nodes, ns + const.HEADJOINTNAME, ns + const.ROOTJOINTNAME))
            failed_list = delete_rig(grp_rig, keep_nodes)
        else:
            logger.warning(u"{}以下に、grp_rig が含まれていません。".format(grp))

    else:
        logger.warning(u"Rigが含まれているトップノードを選択してください。")

    pm.undoInfo(closeChunk = True)
    if not failed_list:
        return True
    else:
        # logger.warning(failed_list)
        return False


def reset_main(grp=None):
    u"""
       コントローラのリセット
        :param grp: string
    """
    if grp is None:
        logger.info(u'選択グループがありません。')
        return

    pm.undoInfo(openChunk = True)
    # -----------------------------------------------------------------
    logger.info(u'コントローラーの移動値、回転値をリセットします。')
    grp = pm.PyNode(grp) if pm.objExists(grp) else None
    grp_rig = Utils.get_pynode(grp, const.GROUPRIGNAME)
    if grp_rig:
        reset_ctrl_transform(grp = grp_rig, pos = True, rot = True)
    else:
        if pm.ls(sl = True):
            grp_name = pm.ls(sl = True)[0]
            reset_ctrl_transform(grp = grp_name, pos = True, rot = True)
        else:
            reset_ctrl_transform(pos = True, rot = True)
    # -----------------------------------------------------------------
    pm.undoInfo(closeChunk = True)


def remake_bindpose(root_joint):
    u"""
       バインドポーズをリセット（1つのみに作り直す）
        :param root_joint: str of joint
    """
    if root_joint and pm.objExists(root_joint):
        pm.delete(pm.listConnections(root_joint, type = "dagPose"))
        pm.dagPose(root_joint, bp = True, save = True)
        logger.info(u'ルートからバインドポーズをリセット（1つに集約）')
    else:
        logger.info(u'ルートジョイントがありません。')


# SIMリネーム戻しは重複が発生する可能性がある為、コメントアウト
'''def rename_conversion(joint_list, sim=const.PREFIX_SIM):
    u"""
       "SIM"アトリビュートが有効なジョイントをPrefix"SIM_"にリネーム
        :param joint_list: list of PyNode　Joint
        :return rename_list:
    """
    if joint_list is None:
        return

    rename_list = []

    for joint in joint_list:
        j_name = joint.stripNamespace().nodeName()
        label = Utils.get_label(j_name)

        if pm.attributeQuery(sim, node=joint, exists=True):
            if pm.getAttr("{}.{}".format(joint, sim)):
                print("SIM attribute True")
                orig_name = j_name

                if label in const.SECONDARYJOINTNAME_LIST:
                    joint.rename("{}_{}".format(sim, orig_name))
                    print("Secondary: {} > {}".format(orig_name, joint.name()))

                else:
                    joint.rename(orig_name.replace("EX_", "{}_".format(sim)))
                    rename_list.append((orig_name, joint))
                    print("EX: {} > {}".format(orig_name, joint.name()))'''


def add_attr(node, cb=False, **kwargs):
    if not node or not kwargs:
        return
    # TODO
    if not pm.attributeQuery(kwargs.get("ln", ""), node=node, exists=True):
        pm.addAttr(node, **kwargs)

        if cb is not None:
            pm.setAttr("{}.{}".format(node, kwargs["ln"]), e=True, cb=cb)



def rename_back_origname(node_list, attr_name=const.ATTR_ORIGNAME):
    # attr_name = ATTR_DICT["orig"]["ln"]
    # TODO
    for node in node_list:
        if pm.attributeQuery(attr_name, node=node, exists=True):
            node.rename(pm.getAttr("{}.{}".format(node, attr_name)))
            print(("rename back", node.nodeName()))


# TODO:一時的な処置としてリネーム
def check_fix_name(grp=None):
    # TODO
    attr_name = "orignal_name"

    if grp is None:
        return

    ns = Utils.get_namespace(grp)
    root_bone = Utils.get_pynode(grp, ns + const.ROOTJOINTNAME)
    if root_bone:
        joint_list = pm.listRelatives(root_bone, c=True, ad=True, type='joint', f=True) or []

        for joint in joint_list:
            j_name = joint.stripNamespace().nodeName()
            label = Utils.get_label(j_name)
            is_ex = True if re.match("^EX_", j_name) else False
            is_numbered = True if re.match(".*_[0-9][0-9]$", j_name) else False
            is_LRFB = True if j_name[3:5] in ["L_", "R_", "F_", "B_", "C_"] else False

            # sleeveのみ、SplineIK使用時に階層指定に制限がある為、必ずEX_を付ける
            if label == "sleeve" and is_LRFB:
                if is_numbered and not is_ex:
                    print(("renamed:", joint, "EX_{}".format(j_name)))
                    add_attr(joint, **ATTR_DICT["orig"])
                    pm.setAttr("{}.{}".format(joint, ATTR_DICT["orig"]["ln"]), j_name)
                    joint.rename("EX_{}".format(j_name))
                else:
                    pass

            elif is_ex and label in const.SECONDARYJOINTNAME_LIST and is_LRFB:
                print(("renamed:", joint, j_name.replace("EX_", "")))
                add_attr(joint, **ATTR_DICT["orig"])
                pm.setAttr("{}.{}".format(joint, ATTR_DICT["orig"]["ln"]), j_name)
                joint.rename(j_name.replace("EX_", ""))


def set_name_conversion(joint_list, attr_name=const.PREFIX_SIM):
    u"""
       "SIM"Prefixジョイントの一時的なリネーム
        :param joint_list: list of PyNode　Joint
        :param attr_name: string
        :return rename_dict:
        :rtype list of tupple(str, PyNode:Joint):
    """
    if joint_list is None:
        return

    rename_dict = {"orig": {}, "sim": {}}

    for joint in joint_list:
        j_name = joint.stripNamespace().nodeName()
        label = Utils.get_label(j_name)
        # is_end = True if j_name.endswith("_End") else False

        # ----------------------------------------------------------------------------------
        is_ex = True if re.match("^EX_", j_name) else False
        is_numbered = True if re.match(".*_[0-9][0-9]$", j_name) else False
        is_LRFB = True if j_name[3:5] in ["L_", "R_", "F_", "B_", "C_"] else False

        # TODO:暫定対応 sleeveのみ、SplineIK使用時に階層指定に制限がある為、必ずEX_を付ける
        if label == "sleeve" and is_LRFB:
            if is_numbered and not is_ex:
                print(("renamed:", joint, "EX_{}".format(j_name)))
                add_attr(joint, **const.ATTR_DICT[const.ATTR_ORIGNAME])
                pm.setAttr("{}.{}".format(joint, const.ATTR_ORIGNAME), j_name)
                joint.rename("EX_{}".format(j_name))
                rename_dict["orig"].update({j_name: joint})

            else:
                pass

        elif is_ex and label in const.SECONDARYJOINTNAME_LIST and is_LRFB:
            print(("renamed:", joint, j_name.replace("EX_", "")))
            add_attr(joint, **const.ATTR_DICT[const.ATTR_ORIGNAME])
            pm.setAttr("{}.{}".format(joint, const.ATTR_ORIGNAME), j_name)
            joint.rename(j_name.replace("EX_", ""))
            rename_dict["orig"].update({j_name: joint})

        # ----------------------------------------------------------------------------------

        # プライマリと除外リスト以外は全て"SIM"アトリビュートを追加、Default:False

        if label not in const.PRIMARYJOINTNAME_LIST and label not in const.IGNOREJOINTNAME_LIST:
            if not pm.attributeQuery(attr_name, node = joint, exists = True):
                pm.addAttr(joint, ln=attr_name, at="bool")
                pm.setAttr("{}.{}".format(joint, attr_name), False)
                pm.setAttr("{}.{}".format(joint, attr_name), e = True, channelBox = True)
                # print("set {} attribute".format(attr_name))

        # ジョイント名に"SIM_"があれば、リネームし、SIMアトリビュートをTrueにする
        if "{}_".format(attr_name) in j_name:
            # 例外としてconst.SECONDARYJOINTNAME_LISTがマッチしていても、EXの可能性がある為、"L_", "R_", "F_", "B_"で判定
            is_LRFB = True if j_name[4:6] in ["L_", "R_", "F_", "B_"] else False
            orig_name = j_name
            pm.setAttr("{}.{}".format(joint, attr_name), True)

            if label in const.SECONDARYJOINTNAME_LIST and is_LRFB:
                joint.rename(orig_name.replace("{}_".format(attr_name), ""))
                rename_dict["sim"].update({orig_name: joint})
                # print("Secondary: {} > {} is_LRFB:{}".format(orig_name, joint.name(), is_LRFB))

            else:
                joint.rename(orig_name.replace("{}_".format(attr_name), "EX_"))
                rename_dict["sim"].update({orig_name: joint})
                # print("EX: {} > {}".format(orig_name, joint.name()))

        else:
            pass  # print("No Change:", j_name)
    return rename_dict


def reset_name_conversion(rename_dict):
    u"""
       "SIM"Prefixジョイントの一時的なリネーム戻し
        :param rename_dict: dict(str=PyNode:Joint):
    """
    if rename_dict is None:
        return

    for str, pynode in list(rename_dict.items()):
        if pm.objExists(pynode):
            pynode.rename(str)

        else:
            pass
            # print("str, pynode:", str, pynode)


# v2.2~:後からSIMアトリビュート追加ボタン用
def add_sim_attributes(joint_list, attr_name=const.PREFIX_SIM):
    u"""
        選択したジョイントにSIMアトリビュートを追加
        :param joint_list: list of PyNode　Joint
        :param attr_name: string
    """
    if joint_list is None:
        joint_list = pm.selected()  # return

    for joint in pm.ls(joint_list, type = "joint"):
        if not pm.attributeQuery(attr_name, node = joint, exists = True):
            pm.addAttr(joint, ln = attr_name, at = "bool")

        pm.setAttr("{}.{}".format(joint, attr_name), True)
        pm.setAttr("{}.{}".format(joint, attr_name), e = True, channelBox = True)
        # print("set {} attribute".format(attr_name))


# v2.2~:SIMアトリビュート削除ボタン用
def remove_sim_attributes(sel_list, attr_name=const.PREFIX_SIM):
    u"""
        選択したノードからSIMアトリビュートを削除
        :param sel_list: list of PyNode
        :param attr_name: string
    """
    if sel_list is None:
        sel_list = pm.selected()  # return

    for sel in sel_list:
        if pm.attributeQuery(attr_name, node = sel, exists = True):
            pm.deleteAttr(sel, at = attr_name)
            print("remove {} attribute".format(attr_name))


def reorder_outliner(node_list):
    u"""
        ノードリストから直下のノードのアウトライナー順番をソート順に変更
        :param node_list: list of PyNode
    """
    if node_list is None:
        node_list = pm.selected()

    for node in node_list:
        print((node, isinstance(node, pm.PyNode)))
        for each in sorted(node.getChildren()):
            pm.reorder(each, back = True)


def main(ex_s_flag=False, ex_sik=None):
    u"""
       AutoCreateRigメイン関数
        :param ex_s_flag: bool
        :param ex_sik: list of joint str
    """

    fix_node_dict = {}
    grp = pm.selected()[0] if pm.selected() else None
    error_list = []

    if not grp or not re.match(const.ID_PATTERN, grp.nodeName()):
        # print(grp, grp.nodeName())
        msg = u'{} グループのトップノードを選択してください。'.format(const.ID_PATTERN)
        logger.error((msg, grp))
        error_list.append((msg, ""))
        return False, error_list

    grp_name = grp.name()
    ns = Utils.get_namespace(grp)

    root = Utils.get_pynode(grp, ns + const.ROOTJOINTNAME)
    head = Utils.get_pynode(grp, ns + const.HEADJOINTNAME)
    grp_mesh = Utils.get_pynode(grp, ns + const.GROUPMESHNAME)
    grp_joint = Utils.get_pynode(grp, ns + const.GROUPJOINTNAME)
    grp_rig = Utils.get_pynode(grp, const.GROUPRIGNAME)

    unfixed_size = "M"

    if grp_rig:
        msg = u'既に{}が存在します。'.format(grp_rig)
        logger.error(msg)
        error_list.append((msg, ""))

    for joint in Check.double(Utils.get_pyjoints(grp)):
        msg = u'名前の重複しているジョイントが見つかりました。'
        error_list.append((msg, joint))

    # 基本情報取得でエラーのケース
    if error_list:
        return False, error_list
    # rename
    # check_fix_name(grp_joint)

    rename_dict = set_name_conversion(Utils.get_pyjoints(grp_joint))
    # rename 後の名前をPyNodeから再取得
    ex_sik = [v["node"].nodeName() for k, v in list(ex_sik.items()) if v["sik"]]

    # unfixed_size = pm.xform(root, q=True, ws=True, a=True, s=True)
    fix_node_dict = dict(root = root, head = head, grp_mesh = grp_mesh, grp_joint = grp_joint)
    check, error_list = Check.scene(grp, ex_sik=ex_sik) #TODO ex_dict

    if check:

        # Referenced, through fixing Joint.　
        if pm.referenceQuery(grp, isNodeReferenced = True):
            logger.error("{} is Referenced. Failed To CreateAutoRig'  ".format(grp.longName()))

            # TODO Reference運用が保留なのでOFFにする
            ''' # reset joint
            for jnt in [root, head]:
                print("set scale:", jnt)
                pm.setAttr("{}.scale".format(jnt), *[1, 1, 1], type="double3")
            logger.info("{} is Referenced. Skipped 'FixJoint'  ".format(grp.longName()))
            # goto_bindpose(root)
            fix, rot_log = fix_joint.joint_rot_check(grp_name)'''
            # fix = fix_joint.fix_joint(grp_name, fix_node_dict, rebind=False)
            # reset_name_conversion(rename_dict)
            return False

        # Not Referenced, fix Joint.
        else:
            logger.info("{} is Not Referenced. Excute 'FixJoint'  ".format(grp.longName()))
            goto_bindpose(root)
            fix = fix_joint.fix_joint(grp_name, fix_node_dict)
            rot_log = ""

        if fix:
            # FixJointにて複製する為、root, head, grp_jointのPyNodeを再取得
            root = Utils.get_pynode(grp, ns + const.ROOTJOINTNAME)
            head = Utils.get_pynode(grp, ns + const.HEADJOINTNAME)
            grp_joint = Utils.get_pynode(grp, ns + const.GROUPJOINTNAME)
            # reset joint
            for jnt in [root, head]:
                pm.setAttr("{}.scale".format(jnt), *[1, 1, 1], type = "double3")

            # Import wire mayaFile and Set wire group.
            global WIRE_GRP
            WIRE_GRP = Utils.get_wire()

            if pm.attributeQuery("unfixed_size", node = grp_joint, exists = True):
                unfixed_size = pm.getAttr(
                    "{}.unfixed_size".format(grp_joint))  # print("## unfixed_size:", grp_joint, unfixed_size)

            if WIRE_GRP:
                pm.undoInfo(openChunk = True)
                # -----------------------------------------------------------------
                Utils.print_info("ex_sik ", ex_sik)
                dummy_node_dict = create_dummy_group(grp = grp, ex_sik = ex_sik)#TODO ex_dict

                if not dummy_node_dict:
                    # print("dummy_node_dict:", dummy_node_dict)
                    logger.error('Failed: create_dummy_group')
                    reset_name_conversion(rename_dict["orig"])
                    pm.undoInfo(closeChunk = True)
                    return False, error_list
                # ------Create Rig-------------------------------------------------
                result = create_rig(grp=grp, ex_s_flag = ex_s_flag, size = unfixed_size, ex_sik = ex_sik,
                                    node_dict = dummy_node_dict)#TODO ex_dict
                if not result:
                    logger.error('Failed: create_rig')
                    reset_name_conversion(rename_dict["orig"])
                    pm.undoInfo(closeChunk = True)
                    return False, error_list
                # -----------------------------------------------------------------
                reset_name_conversion(rename_dict["orig"])
                pm.undoInfo(closeChunk = True)
                return True, error_list
        else:
            logger.error("Fix Joint Error or Referenced Joint Rotation Check Error: {}".format(grp.longName()))
            if len(rot_log.split(u"。")) > 8:
                rot_log = u'。'.join(rot_log.split(u"。")[:8]) + "\n......" + u"\n > 詳細は、ScriptEditorを確認してください。"
            reset_name_conversion(rename_dict["orig"])
            error_list.append((rot_log, grp))
            return False, error_list
    else:
        # v2.2~:scene Checkでダメな場合のみSIMリネームを戻す
        reset_name_conversion(rename_dict["sim"])
        reset_name_conversion(rename_dict["orig"])

        return False, error_list


def wpn_main():
    u"""
       武器作成メイン関数
    """
    # fix_node_dict = {}
    grp = pm.selected()[0] if pm.selected() else None
    grp_rig = None
    error_list = []

    # 選択されたグループ名が命名規則に沿っていなければ止める
    if not grp or not re.match(const.WPN_ID_PATTERN, grp.nodeName()):
        msg = u'wpnもしくはprpグループ名のついたトップノードを選択してください。'
        logger.error(msg)
        error_list.append((msg, grp))
        return False, error_list

    # 選択されたグループ以下に重複がノード名があれば止める
    for double_node in Check.double(grp, type = "transform"):
        msg = u'{}以下に重複ノード名が存在します。'.format(grp)
        logger.error(msg)
        error_list.append((msg, double_node))

    if error_list:
        return False, error_list

    wpn_dict = OrderedDict()
    # grp_name = grp.name()
    ns = Utils.get_namespace(grp)

    # Rigグループノード は1階層下に存在すれば止める
    # r"^|mdl_wpn_105301_1|grp_rig[0-9]?"
    # grp_rig_list = Utils.get_pynodes(grp, r"^" + grp.longName() + r"|(" + const.GROUPRIGNAME + r"[0-9]?)$")
    grp_rig_list = Utils.get_pynodes(grp, r"^(.*)\|(" + const.GROUPRIGNAME + r"[0-9]?)$")

    if grp_rig_list:
        msg = u'既に{}が存在します。'.format(const.GROUPRIGNAME)
        logger.error(msg)
        error_list.append((msg, ""))
        return False, error_list

    # v2.5 複数のWpnパターンに対応、wpn#（新仕様）が無ければトップグループ（旧仕様）を親グループに設定
    # pattern = r"^(" + grp.longName() + r")\|(" + WPN_GROUP_PATTERN + r")$"
    pattern = r"^(.*)\|(" + const.WPN_GROUP_PATTERN + r")$"

    grp_wpn_list = Utils.get_pynodes(grp, pattern = pattern) or [grp]
    for pa_node in grp_wpn_list:
        suffix = ""
        if pa_node != grp:
            m = re.search(r'\d$', pa_node.nodeName())
            suffix = m.group() if m else ""

        root = Utils.get_pynode(pa_node, ns + const.ROOTJOINTNAME + suffix)
        grp_joint = Utils.get_pynode(pa_node, ns + const.GROUPJOINTNAME + suffix)
        grp_mesh = Utils.get_pynode(pa_node, ns + const.GROUPMESHNAME + suffix)

        if pa_node and grp_joint and root:
            wpn_dict.update({pa_node: dict(grp_mesh = grp_mesh, grp_joint = grp_joint, root = root)})

    # v2.4 複数のWpnパターンに対応
    if not wpn_dict:
        msg = u'階層下に grp_joint：Groupノード,　root：Jointノード, grp_joint:Groupノードがありません。'
        logger.error(msg)
        error_list.append((msg, grp))
        return False, error_list

    pm.undoInfo(openChunk = True)
    logger.info(u'武器用のコントローラー作成')
    global WIRE_GRP
    WIRE_GRP = Utils.get_wire(const.FILE_PATH)

    if not WIRE_GRP:
        pm.undoInfo(closeChunk = True)
        msg = u'Missing Wire file {}: WIREファイルがありません。'.format(const.FILE_PATH)
        logger.error(msg)
        error_list.append((msg, grp))
        return False, error_list

    for wpn_grp, v in list(wpn_dict.items()):

        parent_dict = {}
        node_dict = {}

        # 【AutoCreateRig】武器リグのジョイント方向補正をしない対応
        # fix_node_dict.update(root=root, grp_mesh=grp_mesh, grp_joint=grp_joint)
        # 武器はJointOrientの修正が不要の為、コメントアウト
        # fix = fix_joint.fix_joint_wpn(grp_name, fix_node_dict)

        grp_rig = create_group(const.GROUPRIGNAME, grp) if grp_rig is None else grp_rig
        root = v["root"]
        # grp_joint = v["grp_joint"]
        # grp_mesh = v["grp_mesh"]
        pyjoint_list = Utils.get_pyjoints(root)

        if wpn_grp != grp:
            wpn_grp_rig = pm.group(em = True, n = "{}{}".format(wpn_grp.nodeName(), const.SUFFIX_NULL),
                                   parent = grp_rig)
        else:
            wpn_grp_rig = grp_rig

        root_null, root_ctrl = create_controller(root, type = 'sphere', dict = node_dict, parent = wpn_grp_rig)

        set_wire_color(root_ctrl, 13)
        create_constraint(root_ctrl, root, 1, type = "parent")

        # Fix が確認出来なければ止める
        # 【AutoCreateRig】武器リグのジョイント方向につきましての対応
        '''if not fix:
            logger.error(u'Fix_Joint失敗')
            return False'''

        num = 0
        for joint in pyjoint_list:

            num += 1
            Utils.print_info(" {}:{} joint setting:".format(num, 'Weapon'), joint)
            joint_name = Utils.get_name(joint.stripNamespace().nodeName())
            label = Utils.get_label(joint_name)

            if joint_name[-4:] != '_End':
                logger.info(u'Weapon Rig作成： {}'.format(joint))
                if label == 'root':
                    print(("skipped", joint))

                else:
                    # 【AutoCreateRig】武器リグのジョイント方向につきましての対応
                    # local=False → local=True に変更し、各コントローラをローカル軸で生成。
                    null, ctrl = create_controller(joint, local = True, type = 'sphere', dict = node_dict,
                                                   parent = wpn_grp_rig, radius = 0.5)
                    set_wire_color(ctrl, 6)
                    # set_lock_srt(ctrl, t=True, s=True)

                    pa_node = joint.getParent()
                    if not pa_node:
                        msg = u'No Parent Joint {}: 親ノードがありません。'.format(joint)
                        logger.error(msg)
                        error_list.append((msg, joint))
                        pm.undoInfo(closeChunk = True)  # return False, error_list

                    else:
                        pa_name = Utils.get_name(pa_node.stripNamespace().nodeName())
                        parent_dict[null] = Utils.get_pynode(wpn_grp_rig, pa_name + const.SUFFIX_CTRL)
                        create_constraint(ctrl, joint, 1, type = "parent")
                        create_constraint(ctrl, joint, 1, type = "scale")

            pm.select(cl = True)
            create_displaylayer(nodes = [grp_rig], name = const.RIG_LAYERNAME)
            logger.info(u'Rig コントローラのレイヤー設定　完了')

        # -------------------------------------------------------------------------
        # コントローラノードの階層化設定処理
        # -------------------------------------------------------------------------
        logger.info(u'ノードの階層化')
        for ch, pa in list(parent_dict.items()):

            if not isinstance(ch, pm.PyNode):
                pm.undoInfo(closeChunk = True)
                return False, error_list

            if not isinstance(pa, pm.PyNode):
                pa_node = node_dict.get(pa, None)
                if pa_node is None:
                    pa = grp_rig  # return

            try:
                if ch.getParent() != pa:
                    pm.parent(ch, pa)  # Lock不要とのことでコメントアウト  # set_lock_srt(ch, t=True, r=True)

            except (ValueError, RuntimeError) as e:
                logger.error(e)

        # bow タイプの場合セットドリブンキーの設定
        if Utils.get_pynode(grp_rig, "bow_01_CTRL") and Utils.get_pynode(grp_rig, "bow_00_CTRL"):
            driver = Utils.get_pynode(grp_rig, "bow_01_CTRL")
            driven = Utils.get_pynode(grp_rig, "bow_00_CTRL")
            set_drivenkey(driver, driven)

    # Reorder Outliner
    logger.info(u'ノードの順序をソーティング')
    reorder_outliner([grp_rig])

    if pm.objExists(WIRE_GRP):
        logger.info(u'テンプレートノードの削除')
        pm.delete(WIRE_GRP, hi = True)

    pm.select(grp)
    pm.undoInfo(closeChunk = True)  # -----------------------------------------------------------------

    return True, error_list
