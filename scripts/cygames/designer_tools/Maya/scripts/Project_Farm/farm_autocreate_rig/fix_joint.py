# -*- coding=utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import

u"""
name: autocreate_rig/fix_joint.py
data: 2021/10/18
ussage: priari 用 Rig 自動作成ツール ジョイントチェック、修正
version: 2.72
​
"""

try:
    # Maya 2022-
    from builtins import zip
    from builtins import str
    from builtins import range
except:
    pass

import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm
from . import const
from collections import OrderedDict
from pprint import pprint

from logging import getLogger
logger = getLogger(__name__)

TOOL_VERSION = 'Ver 2.73'

ATTR_UNFIXSIZE = dict(ln="unfixed_size", sn="us", dt="string")


def remake_bindpose(root_joint):
    u"""
       バインドポーズをリセット（1つのみに作り直す）
        :param root_joint: str of joint
    """
    if not root_joint or not cmds.objExists(root_joint):
        logger.error(u'ルートジョイントがありません。')
        return

    if not root_joint.startswith("|"):
        root_joints = cmds.ls(root_joint, l=True)
        if root_joints:
            root_joint = root_joints[0]
        else:
            return

    top_node = root_joint.split("|")[1]
    sels = cmds.ls(top_node, dag=True, l=True)
    dagposes = cmds.listConnections(sels, type="dagPose")
    if dagposes:
        cmds.delete(list(set(dagposes)))
    bp = cmds.dagPose(root_joint, bp=True, save=True)
    bindposename = "bindPose_wpn0" if "wpn" in top_node else "bindPose_unit0"
    cmds.rename(bp, bindposename)
    logger.info(u'ルートからバインドポーズをリセット（1つに集約）')


def set_segmentscale_zero(joints=[]):
    u"""
        全てのジョイントのワールド座標を維持したまま segmentScaleCompensate をゼロ
        :param root_joint: str of joint
    """
    parent_dict = OrderedDict()
    for jnt in joints:
        # ro = cmds.xform(jnt,q=True,ro=True)
        tr = pm.xform(jnt, q=True, t=True, ws=True)
        # sc = cmds.xform(jnt,q=True,s=True)
        parent_dict[jnt] = dict(p=jnt.getParent(), tr=tr)

    # set segmentScaleCompensate zero and parent to original parent node
    for pynode, d in list(parent_dict.items()):
        cmds.setAttr("{}.segmentScaleCompensate".format(pynode.name()), 0)

    # set transform original values
    for pynode, d in list(parent_dict.items()):
        cmds.xform(pynode.longName(), t=d["tr"], ws=True)

    # cmds.select(cl=True)
    logger.info(u'全ジョイントのSegmentScaleCompensate をゼロ設定。')


def set_transform(node_list=[], transform_dict={"t": [0, 0, 0]}):
    u"""
        transformの一括設定
        :param node_list: list of str node
        :param transform_dict: dict {"t": [0, 0, 0], "r": [0, 0, 0], "s": [1, 1, 1]}
    """
    for node in node_list:
        for attr, values in list(transform_dict.items()):
            if attr in ["t", "r", "s"]:
                try:
                    cmds.setAttr('{}.{}'.format(node, attr), *values, type="double3")
                except Exception as e:
                    logger.error(u'{}_{}:トランスフォーム設定に失敗。'.format(node, attr), e)


def set_attr(node_list=[], attr_dict={}):
    u"""
        attributeの一括設定
        :param node_list: list of str node
        :param attr_dict: dict {"tx": 0, "tz": 0}
    """
    for node in node_list:
        for attr, value in list(attr_dict.items()):
            try:
                cmds.setAttr('{}.{}'.format(node, attr), value)
            except Exception as e:
                logger.error(u'{}_{}:アトリビュート設定に失敗。'.format(node, attr), e)


def get_joint_list(root):
    u"""
        指定した名前以下のジョイントを全て取得
    """
    cmds.select(root, hi=True)
    joints = cmds.ls(sl=True, typ=['joint'], o=True, nt=False, l=True)
    # cmds.listRelatives(root, c=True, ad=True, type='joint', f=True)
    cmds.select(cl=True)
    return joints


def get_name(name):
    u"""
        名前の中から種別名を取得
        :param name:
        :return: 種別名
    """
    if len(name.rsplit('|')) > 1:
        s_name = name.rsplit('|', 1)[1]
    else:
        s_name = name
    return s_name


def get_mesh_transform(node_list=[]):
    """get target node type list, optional "selected" under dag nodes
    :param  node_list list (PyNode)
    :return: target_list
    :rtype: list (PyNode)
    """

    target_list = []
    kwargs = dict(dag=False, o=True, tr=True, long=True)
    # print("node_list: ", node_list)
    node_list = [node for node in node_list if pm.objExists(node)]
    kwargs.update(dag=True)
    for node in node_list:
        mesh_transforms = [i for i in pm.ls(node, **kwargs) if pm.listRelatives(i, type="mesh")]
        target_list.extend(mesh_transforms)

    return target_list


# TODO ShapeとTransformの名前が違う際の不具合対応
def get_skincluster(name):
    u"""
        指定名のノードからスキンクラスターを取得
        :param str name:
        :return: str skincluster　or  None
    """
    # input order を維持する為にOrderedDictを使用
    deformer_dict = OrderedDict()

    if name.startswith("|"):
        name = name[1:]
    return mel.eval('findRelatedSkinCluster {}'.format(name))


def get_deformer(node, type="skinCluster"):
    u"""
        ノードからデフォーマーを取得
        :param PyNode node:
        :return: deformer
        :rtype: PyNode of Deformer

    """
    if not node or not isinstance(node, pm.PyNode):
        return

    for deformer in node.listHistory(pdo=True, type=type):
        return deformer

    return None

def check_grp_node(grp, name):
    u"""
        指定名のノードがシーンに存在するかどうか
        :param str name:
        :return: bool
    """
    for node in cmds.ls('*|{}'.format(name), l=True):
        if '|{}'.format(grp) in node:
            return True
    return False


def scene_check():
    u"""
        リグ作成前のシーンチェック
        :return: bool
    """
    print("scene_check: start")

    check_flag = True
    error_log = ''
    grp = cmds.ls(sl=True)[0]
    if not check_grp_node(grp, 'grp_mesh'):
        logger.error(u'階層内に grp_mesh ノードが見つかりません。')
        error_log = error_log + u'・階層内に grp_mesh ノードが見つかりません。\n'
        check_flag = False

    else:
        if get_parent(node_select(grp, 'grp_mesh')) != grp:
            logger.error(u'grp_mesh ノードの階層が正しくありません。')
            error_log = error_log + u'・grp_mesh ノードの階層が正しくありません。\n'
            check_flag = False

    if not check_grp_node(grp, 'grp_joint'):
        logger.error(u'階層内に grp_joint ノードが見つかりません。')
        error_log = error_log + u'・階層内に grp_joint ノードが見つかりません。\n'
        check_flag = False

    else:
        if get_parent(node_select(grp, 'grp_joint')) != grp:
            logger.error(u'grp_joint ノードの階層が正しくありません。')
            error_log = error_log + u'・grp_joint ノードの階層が正しくありません。\n'
            check_flag = False

    if not check_grp_node(grp, 'root'):
        logger.error(u'階層内に root ジョイントが見つかりません。')
        error_log = error_log + u'・階層内に root ジョイントが見つかりません。\n'
        check_flag = False
    else:
        root = node_select(grp, 'root')
        # joints = cmds.listRelatives(root, c=True, ad=True, type='joint', f=True) or []
        # invalid_endjoints = [j for j in joints if not j.getChildren(type="transform") and not j.endswith("_End") and j.endswith("_twistarm")]

        if 'grp_joint' not in get_parent(root):
            logger.error(u'root ジョイントの階層が正しくありません。')
            error_log = error_log + u'・root ジョイントの階層が正しくありません。\n'
            check_flag = False

        if cmds.listConnections(root, d=True, type='dagPose') is None:
            logger.error(u'root ジョイントに Bind Pose が見つかりません。')
            error_log = error_log + u'・root ジョイントに Bind Pose が見つかりません。\n'
            check_flag = False

        if joint_rot_check(grp) and check_flag:
            logger.info(u'ジョイントの方向が修正済みのデータです。')
            error_log = error_log + u'・ジョイントの方向が修正済みのデータです。\n'
            check_flag = False

    cmds.select(grp, hi=True)
    meshes = cmds.ls(sl=True, type='mesh')

    if len(meshes) > 0:
        for mesh in meshes:
            print(('mesh.endswith("_Outline"): ', mesh.endswith("_Outline")))
            if not mesh.endswith("_Outline"):
                # skin = get_skincluster(mesh)
                mesh = pm.PyNode(mesh)
                # skin = mesh.listHistory(type="skinCluster")[0] if mesh.listHistory(type="skinCluster") else None
                skin = get_deformer(mesh)
                # parent_mesh = cmds.listRelatives(mesh, p=True, ni=True, f=True)
                parent_mesh = pm.listRelatives(mesh, p=True, ni=True, f=True)

                if parent_mesh:
                    if cmds.listRelatives(parent_mesh[0], p=True, f=True)[0] != node_select(grp, 'grp_mesh'):
                        logger.error(u'{} の階層が正しくありません。'.format(parent_mesh[0]))
                        error_log = error_log + u'・{} の階層が正しくありません。\n'.format(parent_mesh[0])
                        check_flag = False

                if skin:
                    skin_joint = cmds.skinCluster(skin, query=True, inf=True)
                    for joint in skin_joint:
                        if not check_grp_node(grp, joint):
                            logger.error(u'階層内に {} が見つかりません。'.format(joint))
                            error_log = error_log + u'・階層内に {} が見つかりません。\n'.format(joint)
                            check_flag = False
                else:
                    logger.error(u'{} に SkinCluster が見つかりません。'.format(mesh))
                    error_log = error_log + u'・{} に SkinCluster が見つかりません。\n'.format(mesh)
                    check_flag = False

        if joint_double_check(grp) != []:
            for joint in joint_double_check(grp):
                logger.error(u'名前の重複しているジョイントが見つかりました。 : {} '.format(joint))
                error_log = error_log + u'・名前の重複しているジョイントが見つかりました。\n'.format(joint)
            check_flag = False
    else:
        logger.warnning(u'階層内にメッシュデータが見つかりません。')
        error_log = error_log + u'・階層内にメッシュデータが見つかりません。\n'
        check_flag = False
    # print("error_log : ", error_log)
    if not (node_select(grp, 'L_mant_00')):
        logger.error(u'階層内に L_mant ジョイントが見つかりません。ジョイントデータを確認してください。')
        error_log = error_log + u'・階層内に L_mant ジョイントが見つかりません。\n'
        check_flag = False

    if not (node_select(grp, 'R_mant_00')):
        logger.error(u'階層内に R_mant ジョイントが見つかりません。ジョイントデータを確認してください。')
        error_log = error_log + u'・階層内に R_mant ジョイントが見つかりません。\n'
        check_flag = False

    if check_grp_node(grp, 'grp_CTRL'):
        logger.error(u'既にRigが作成されています。')
        error_log = error_log + u'・既にRigが作成されています。\n'
        check_flag = False

    cmds.select(grp)

    return check_flag, error_log


def joint_double_check(grp):
    u"""
        grp以下から重複ノードをチェック
        :param grp: PyNode
        :return: list of str
    """
    double_list = []
    joint_list = get_joint_list(grp)

    for i, joint_name in enumerate(joint_list):
        for x, search_name in enumerate(joint_list):
            if i != x:
                if get_name(joint_name) == get_name(search_name):
                    if not get_name(joint_name) in double_list:
                        double_list.append(get_name(joint_name))

    return double_list


def joint_rot_check(grp, ns=""):
    u"""
        grp以下から決め打ちジョイントの回転値をチェック
        :param grp: PyNode
        :param ns: str of namespace
        :return:  flag, error_log
        :rtype: bool, str

    """

    error_log = ''

    flag = True
    joint_list = get_joint_list(grp)
    logger.info(u'Rotate Check')

    if cmds.referenceQuery(grp, isNodeReferenced=True):
        ref_file = cmds.referenceQuery(grp, f=True)
        rn = cmds.referenceQuery(ref_file, referenceNode=True)
        ns = rn.replace("RN", ":")

    for joint_name in joint_list:
        if round(cmds.getAttr('{}.rotateX'.format(joint_name))) != 0:
            msg = u'{}.RotateX に値が入っています。'.format(joint_name.split("|")[-1])
            logger.error(msg)
            error_log = error_log + u'{}\n'.format(msg)
            flag = False

        if round(cmds.getAttr('{}.rotateY'.format(joint_name))) != 0:
            msg = u'{}.RotateY に値が入っています。'.format(joint_name.split("|")[-1])
            logger.error(msg)
            error_log = error_log + u'{}\n'.format(msg)
            flag = False

        if round(cmds.getAttr('{}.rotateZ'.format(joint_name))) != 0:
            msg = u'{}.RotateZ に値が入っています。'.format(joint_name.split("|")[-1])
            logger.error(msg)
            error_log = error_log + u'{}\n'.format(msg)
            flag = False

    l_node = node_select(grp, ns + 'L_forearm')
    if l_node:
        if round(cmds.getAttr('{}.jointOrientX'.format(l_node))) != 0:
            msg = u'{} の jointOrientX に値が入っています。'.format(l_node.split("|")[-1])
            flag = False
        if round(cmds.getAttr('{}.jointOrientZ'.format(l_node))) != 0:
            msg = u'{} の jointOrientZ に値が入っています。'.format(l_node.split("|")[-1])
            flag = False
        if round(cmds.getAttr('{}.translateY'.format(l_node))) != 0:
            msg = u'{} の translateY に値が入っています。'.format(l_node.split("|")[-1])
            flag = False
    else:
        msg = u'階層内に L_forearm ジョイントが見つかりません。'
        logger.error(msg)
        error_log = error_log + u'{}\n'.format(msg)
        flag = False

    r_node = node_select(grp, ns + 'R_forearm')
    if r_node:
        if round(cmds.getAttr('{}.jointOrientX'.format(r_node))) != 0:
            msg = u'{} の jointOrientX に値が入っています。'.format(r_node.split("|")[-1])
            logger.error(msg)
            error_log = error_log + u'{}\n'.format(msg)
            flag = False

        if round(cmds.getAttr('{}.jointOrientZ'.format(r_node))) != 0:
            msg = u'{} の jointOrientZ に値が入っています。'.format(r_node.split("|")[-1])
            logger.error(msg)
            error_log = error_log + u'{}\n'.format(msg)
            flag = False

        if round(cmds.getAttr('{}.translateY'.format(r_node))) != 0:
            msg = u'{} の translateY に値が入っています。'.format(r_node.split("|")[-1])
            logger.error(msg)
            error_log = error_log + u'{}\n'.format(msg)
            flag = False
    else:
        msg = u'階層内に R_forearm ジョイントが見つかりません。'
        logger.error(msg)
        error_log = error_log + u'{}\n'.format(msg)
        flag = False

    return flag, error_log


def node_select(grp, name):
    """ネームスペース取得
    :param node: list of string
    :return string
    """
    for node in cmds.ls(name, l=True):
        if grp == node.split('|')[1]:
            return node

    return None


def get_namespace(node):
    """ネームスペース取得
    :param node: list of string
    :return ns:
    :rtype string
    """
    # if string, convert to PyNode
    if isinstance(node, str):
        node = pm.PyNode(node)

    if node is None:
        return ""
    # string node must use "referenceQuery"
    if pm.referenceQuery(node, isNodeReferenced=True):
        ns = node.namespace()

    return ns


def fix_size_main(mesh_list=None):
    """スケール補正
    :param mesh_list: list of string
    :return bool or string
    """
    if cmds.ls(sl=True):
        check, log = scene_check()
        if check():
            base_grp = cmds.ls(sl=True)[0]
            cmds.undoInfo(openChunk=True)
            # -----------------------------------------------------------------
            mesh_list = ['msh_head']
            fix_size(base_grp, mesh_list)
            # -----------------------------------------------------------------
            cmds.select(base_grp)
            cmds.undoInfo(closeChunk=True)
            logger.info(u'サイズ 修正完了')
            return True
        else:
            return log
    else:
        logger.error(u'ノードが選択されていません。')
        return False

def fix_joint_arm(grp):

    if not grp or cmds.objExists(grp):
        return

    reset_joint_rotate(grp)  # grp → base_grp
    cmds.select(d = True)

    # 存在すれば親子関係を解消　現状sleeveのみオプション扱い
    arm_joints = ["forearm", "sleeve", "thumb_00", "index_00", "middle_00", "ringroot"]
    for arm_joint in ["{}_{}".format(LR, j) for j in arm_joints for LR in ["L", "R"]]:
        if node_select(grp, arm_joint):
            cmds.parent(node_select(grp, arm_joint), grp)
        else:
            print("Skip: Missing {}".format(arm_joint))

    cmds.parent(node_select(grp, 'R_hand'), node_select(grp, 'R_upperarm'))
    cmds.parent(node_select(grp, 'L_hand'), node_select(grp, 'L_upperarm'))

    # 値をきれいにする
    logger.info(u'hand_value_reset')
    l_hand = node_select(grp, 'L_hand')
    r_hand = node_select(grp, 'R_hand')
    set_transform([l_hand, r_hand], {"r": [0, 0, 0]})

    l_upperarm = node_select(grp, 'L_upperarm')
    r_upperarm = node_select(grp, 'R_upperarm')
    set_transform([l_upperarm, r_upperarm], {"r": [0, 0, 0]})

    attr_dict = {"jointOrientX": 0, "jointOrientZ": 0}
    set_attr([l_hand, r_hand], attr_dict)

    cmds.parent(l_upperarm, grp)
    cmds.parent(r_upperarm, grp)

    cmds.select(d = True)
    # 選択が必要か不明なのでデバッグが安定するまで削除しない
    cmds.select(node_select(grp, 'L_upperarm'), node_select(grp, 'R_upperarm'))

    # 上腕のジョイント向きを設定
    # cmds.joint(e=True, oj='xyz', secondaryAxisOrient='yup', ch=True, zso=True)

    cmds.parent(node_select(grp, 'L_upperarm'), node_select(grp, 'L_clavicle'))
    cmds.parent(node_select(grp, 'R_upperarm'), node_select(grp, 'R_clavicle'))

    # 前腕を階層を戻す
    cmds.parent(node_select(grp, 'L_forearm'), node_select(grp, 'L_upperarm'))
    cmds.parent(node_select(grp, 'R_forearm'), node_select(grp, 'R_upperarm'))

    # 値をきれいにする
    l_forearm = node_select(grp, 'L_forearm')
    r_forearm = node_select(grp, 'R_forearm')
    set_attr([l_forearm, r_forearm], attr_dict)

    set_attr([l_forearm, r_forearm], {"ty": 0})

    # 存在すれば階層を戻す 現状sleeveのみオプション扱い
    if node_select(grp, 'L_sleeve'):
        cmds.parent(node_select(grp, 'L_sleeve'), l_forearm)
    if node_select(grp, 'R_sleeve'):
        cmds.parent(node_select(grp, 'R_sleeve'), r_forearm)

    cmds.parent(node_select(grp, 'L_hand'), l_forearm)
    cmds.parent(node_select(grp, 'R_hand'), r_forearm)
    cmds.reorder(node_select(grp, 'L_hand'), r = -2)
    cmds.reorder(node_select(grp, 'R_hand'), r = -2)

    l_hand = node_select(grp, 'L_hand')
    r_hand = node_select(grp, 'R_hand')
    set_attr([l_hand, r_hand], {"ty": 0, "tz": 0})

    # FingerRootはOptionalJointに変更、存在すればHandの階層下に配置
    finger_list = ['thumb_00', 'index_00', 'middle_00', 'ringroot']
    for finger_root in ["{}_{}".format(LR, j) for j in finger_list for LR in ["L", "R"]]:
        if node_select(grp, finger_root):
            if finger_root.startswith("L_"):
                cmds.parent(node_select(grp, finger_root), l_hand)
            elif finger_root.startswith("R_"):
                cmds.parent(node_select(grp, finger_root), r_hand)
        else:
            print("Skip: Missing {}".format(finger_root))
    cmds.select(d = True)
    logger.info(u'arm, sleeve, hand and fingers joints are fixed')


def get_parent(node):
    """親階層ノード取得
    :param grp: string

    """
    parents = cmds.listRelatives(node, p=True)
    if parents:
        return parents[0]
    return None


def get_children(node):
    """子階層ノード取得
    :param grp: string

    """
    return cmds.listRelatives(node, c=True)


def set_preferred_Angle(grp):
    """(L|R)_foresrm,(L|R)_forelegのjoint優先角度の設定
    :param grp: str

    """
    l_forearm = node_select(grp, 'L_forearm')
    r_forearm = node_select(grp, 'R_forearm')
    l_foreleg = node_select(grp, 'L_foreleg')
    r_foreleg = node_select(grp, 'R_foreleg')
    cmds.setAttr('{}.preferredAngleY'.format(l_forearm), -30)
    cmds.setAttr('{}.preferredAngleY'.format(r_forearm), 30)
    cmds.setAttr('{}.preferredAngleZ'.format(l_foreleg), 30)
    cmds.setAttr('{}.preferredAngleZ'.format(r_foreleg), 30)


def rotate_check(node):
    """jointの回転値チェック
    :param grp: string

    """
    if cmds.getAttr('{}.rotateX'.format(node)) != 0:
        logger.warning(u'{}.RotateX の値を修正しました。'.format(node))
    if cmds.getAttr('{}.rotateY'.format(node)) != 0:
        logger.warning(u'{}.RotateY の値を修正しました。'.format(node))
    if cmds.getAttr('{}.rotateZ'.format(node)) != 0:
        logger.warning(u'{}.RotateZ の値を修正しました。'.format(node))


def reset_joint_rotate(grp):
    """jointの回転値チェック実行、優先角度の修正
    :param grp: PyNode

    """
    joint_list = get_joint_list(grp)
    for joint_name in joint_list:
        # print('base : '+joint_name)
        p_node = get_parent(joint_name)
        c_nodes = get_children(joint_name)
        rotate_check(joint_name)

        if p_node and p_node != grp:
            cmds.parent(joint_name, grp)
            joint_name = node_select(grp, joint_name.rsplit('|', 1)[1])

        if c_nodes:
            for c_node in c_nodes:
                cmds.parent(node_select(grp, c_node), grp)

        cmds.rotate(0, 0, 0, joint_name, os=True, ws=False, a=True)
        cmds.setAttr('{}.preferredAngleX'.format(joint_name), 0)
        cmds.setAttr('{}.preferredAngleY'.format(joint_name), 0)
        cmds.setAttr('{}.preferredAngleZ'.format(joint_name), 0)

        if c_nodes:
            for c_node in c_nodes:
                # print('joint_name :{}'.format(joint_name))
                # print('c_node :{}'.format(node_select(grp, c_node)))
                cmds.parent(node_select(grp, c_node), joint_name)

        if p_node and p_node != grp:
            cmds.parent(joint_name, node_select(grp, p_node))

    set_preferred_Angle(grp)


def goto_bind_pose(joint):
    """バインドポーズへ戻す
    :param joint: PyNode

    """
    bp_list = pm.listConnections(joint, d=True, type='dagPose')
    for bp in bp_list:
        # cmds.select(joint)
        # mel.eval('gotoBindPose')
        # index0のバインドポーズから実行。実行に失敗すれば次のバインドポーズを実行
        try:
            pm.dagPose(joint, bp, restore=True)
            logger.info(u'Bind Pose に戻します。')
            break
        except Exception as e:
            print(e)
            continue


def topnode_check():
    """トップノードかどうか
    :param base_grp: string or PyNode
    :return bool:
    :rtype bool
    """
    if cmds.ls(sl=True):
        if len(cmds.ls(sl=True)) > 0:
            grp_name = cmds.ls(sl=True,)[0]
            if cmds.listRelatives(grp_name, p=True, f=True) is None:
                return True

    logger.error(u'トップノードを選択してください。')
    return False


def get_shape_dagpath(name):
    u"""shape のMDagPathの取得
     :param name: str
     :return: dag_path
     :rtype: MDagPath or None
     """
    sel_list = om.MGlobal.getSelectionListByName(name)
    dag_path = sel_list.getDagPath(0)
    try:
        dag_path.extendToShape()
        return dag_path

    except RuntimeError:
        return None


def get_mobj(name):
    u"""MObjectの取得
     :param name: str
     :return: MDagPath or MObject
     :rtype: MDagPath or MObject
     """
    sellist = om.MGlobal.getSelectionListByName(name)
    try:
        return sellist.getDagPath(0)
    except (TypeError, RuntimeError):
        return sellist.getDependNode(0)


def get_skinweight(mesh, sc):

    if not mesh or not sc:
        return

    if isinstance(mesh, pm.PyNode):
        mesh = mesh.fullPath()

    if isinstance(sc, pm.PyNode):
        sc = sc.nodeName()

    skin_mobj = get_mobj(sc)
    skin_fn = oma.MFnSkinCluster(skin_mobj)
    # get shape
    mesh_mobj = get_shape_dagpath(mesh)
    mesh_dagfullpath = mesh_mobj.fullPathName()
    mesh_node = mesh_mobj.node()

    # get mesh vertex itr
    mit_meshvtx = om.MItMeshVertex(mesh_node)
    indices = list(range(mit_meshvtx.count()))

    # get vtx indices as component
    singleIdComp = om.MFnSingleIndexedComponent()
    vertexComp = singleIdComp.create(om.MFn.kMeshVertComponent)
    singleIdComp.addElements(indices)

    # IntArray of influences
    inf_dags = skin_fn.influenceObjects()
    inf_num = len(inf_dags)
    inf_indexes = om.MIntArray(inf_num, 0)
    for x in range(inf_num):
        inf_indexes[x] = int(skin_fn.indexForInfluenceObject(inf_dags[x]))

    # get  weights
    weightData = skin_fn.getWeights(mesh_mobj, vertexComp)

    # vtx index ordered weights
    weights_list = list(zip(*[iter(weightData[0])] * inf_num))
    skinpercent_weight = []
    for vtx_id, weights in enumerate(weights_list):
        # get dict index and rounded weights if not zero # TODO less string, not use fullpath
        valid_weights = [(inf_dags[i].fullPathName(), w) for i, w in enumerate(weights) if w > 0]
        skinpercent_weight.extend(valid_weights)
        # msg = "{}.vtx[{}]".format(mesh_dagfullpath, vtx_id)

    # pm.skinPercent(sc, vtx, tv=wVals, zri=True)

    return skinpercent_weight


def set_skinweight(sc, mesh, weight):


    # inf_list = cmds.skinCluster(sc, q=True, inf = True)
    print(weight[0])
    cmds.skinPercent(sc, mesh, tv=weight, zri=False)  # Set Final Fixed Weghts
    raise Exception


def fix_joint(base_grp, pynodes_dict={}, rebind=True):
    """キャラ用リグ生成前のジョイント補正
    :param base_grp: string or PyNode
    :param pynodes_dict: dict
    :param rebind: bool
    :return bool or None:
    :rtype bool
    """

    if not pynodes_dict:
        return None
    else:
        root = pynodes_dict.get('root', None)
        head = pynodes_dict.get('head', None)
        grp_mesh = pynodes_dict.get('grp_mesh', None)
        grp_joint = pynodes_dict.get('grp_joint', None)

    # トップノードにスケールが入る場合にはあらかじめ補正する。
    top_scales = [round(s, 4) for s in pm.xform(base_grp, q=True, ws=True, a=True, s=True)]
    if top_scales != [1, 1, 1]:
        # if node are locked, unlock.
        for scale in ["scaleX", "scaleY", "scaleZ"]:
            if pm.getAttr('{}.{}'.format(base_grp, scale), lock=True):
                pm.setAttr('{}.{}'.format(base_grp, scale), lock=False)

        pm.setAttr('{}.scale'.format(base_grp), *[1, 1, 1], type="double3")
        logger.info("{}.scale are Reset by [1.0, 1.0, 1.0]".format(base_grp))

    size = pm.xform(root, q=True, ws=True, a=True, s=True)
    # 小数点以下2位までにroundをかけて文字列に変換、const.SIZE_DICTから判定
    unfixed_size = "M"
    for key in const.SIZE_DICT:
        if const.SIZE_DICT[key]['value'] == round(size[0], 2):
            unfixed_size = key
            break

    uoc = pm.getAttr("{}.uoc".format(root))

    attr_unfixsize_name = ATTR_UNFIXSIZE.get("ln", "unfixed_size")
    # add attribute:unfixed_size if not exists
    if not pm.attributeQuery(attr_unfixsize_name, node=grp_joint, exists=True):
        pm.addAttr(grp_joint, **ATTR_UNFIXSIZE)
    pm.setAttr("{}.{}".format(grp_joint, attr_unfixsize_name), unfixed_size, type="string")
    print(("{}:".format(attr_unfixsize_name), unfixed_size, str(round(size[0], 2)), size[0]))

    pm.select(root, hi=True)
    joint_list = [jnt for jnt in pm.ls(sl=True, l=True, type="joint") if not jnt.nodeName().endswith("_End")]
    pm.select(d=True)

    # goto bindpose
    goto_bind_pose(root)

    # delete all animetion key
    pm.delete(root, c=True, uac=False, hi="below", cp=1, s=1)

    # Reset Scale for Detatch skin
    root_scales = pm.xform(root, q=True, r=True, s=True) if root else [1, 1, 1]
    head_scales = pm.xform(head, q=True, r=True, s=True) if head else [1, 1, 1]

    # get skinMesh and skinCluster as dict if it skinbinded #TODO cmds
    mesh_trs = get_mesh_transform([grp_mesh])
    skin_dict = {mesh: get_skincluster(mesh) for mesh in mesh_trs if get_skincluster(mesh)}
    # deformer_dict = {mesh: get_skincluster(mesh) for mesh in mesh_trs if get_skincluster(mesh)}

    sc_dict = {}
    for mesh in mesh_trs:
        sc = get_deformer(mesh)
        if sc:
            # skinからジョイント取得。不要な"_End"ジョイントを除外
            skin_list = [j for j in pm.skinCluster(sc, q=True, inf=True) if not j.nodeName().endswith("_End")]
            # skin_list = pm.skinCluster(sc, q=True, inf=True)
            skin_list.append(mesh)

            sc_kwargs = dict(toSelectedBones=True, bindMethod=0, normalizeWeights=1, weightDistribution=0,
                             maximumInfluences=3, obeyMaxInfluences=True, dropoffRate=4,
                             removeUnusedInfluence=False, name=sc.nodeName())
            try:
                sc_attr_list = [("skinningMethod", "bindMethod"),
                                ("normalizeWeights", "normalizeWeights"),
                                ("weightDistribution", "weightDistribution"),
                                ("maxInfluences", "maximumInfluences"),
                                ("maintainMaxInfluences", "obeyMaxInfluences")]
                for attr, kwarg in sc_attr_list:
                    sc_kwargs.update({kwarg: cmds.getAttr('{}.{}'.format(sc, attr))})
            except Exception as e:
                print(e)
            sc_dict[mesh] = dict(sc_args=skin_list,
                                 # sc_weight=get_skinweight(mesh, sc),
                                 sc_kwargs=sc_kwargs,
                                 )
    # ################# Only Rebind ##################
    # if skinmesh exists, detatch skin
    if rebind and skin_dict:
        pm.select(grp_mesh)
        mel.eval('doDetachSkin "2" { "2","1" }') # keep skin History
        # mel.eval('doDetachSkin "2" { "1","1" }') # Delete skin history

    cmds.select(d=True)
    # set segmentScalecompensate zero at all joints
    set_segmentscale_zero(joint_list)

    # ################# Only Rebind ##################
    if rebind:
        #for mesh, sc in skin_dict.items():
        for mesh, sc_info in list(sc_dict.items()):
            # print(mesh, sc_info)
            # re-bind skin
            try:
                pm.skinCluster(sc_info["sc_args"], **sc_info["sc_kwargs"])
                if uoc:
                    for j in joint_list:
                        pm.setAttr("{}.uoc".format(j), uoc)

            except Exception as e:
                print((u"Skipped Error: ", e))
                print(u"Skinbinding may have a problem. Check the Skincluster:{} ".format(sc))

    cmds.select(d=True)
    # reset scale head and root to unparent without "adding transform"
    set_transform([root.longName(), head.longName()], {"s": [1, 1, 1]})

    # Dupricate # TODO: 複製後が値補正処理が確実では無いので、リファクタリング予定
    logger.info(u'Duplicate: {}'.format(base_grp))
    # d_grp = cmds.duplicate('{}'.format(base_grp), rr=True)[0]#No input Graph
    d_grp = cmds.duplicate('{}'.format(base_grp), rr=True, un=True)[0]# with input Graph

    # スケール補正前の複製メッシュは不要なので削除。# TODO BlendShape保持の為、処理見直し
    for mesh, sc_info in list(sc_dict.items()):
        # pm.delete(get_deformer(mesh))
        # TODO delete Tweak?
        # cmds.delete(node_select(d_grp, 'grp_mesh'))
        pm.select(mesh)
        mel.eval('doDetachSkin "2" { "1","1" }')  # Delete skin history
    cmds.select(d=True)

    # TODO test exchange
    fix_joint_arm(base_grp)

    cmds.select(d=True)
    # dupricate 後にroot, head ノードを更新
    d_root = pm.PyNode(node_select(d_grp, 'root'))
    d_head = pm.PyNode(node_select(d_grp, 'C_head'))

    # re-set default scale
    try:
        for node in [root, d_root]:
            pm.setAttr("{}.scale".format(node), *root_scales, type="double3")
        for node in [head, d_head]:
            pm.setAttr("{}.scale".format(node), *head_scales, type="double3")
        logger.info(u'Root and head scale reset')
    except Exception as e:
        print(e)
        logger.warning(u'Root and head scale reset: Failed')
    # ################# Only Rebind ##################
    # if skinmesh exists, detatch skin　 TODO BlendShape保持の為、処理見直し
    if rebind and skin_dict:
        for mesh, sc_info in list(sc_dict.items()):
            try:
                sc_name = "{}_skinCluster".format(mesh.nodeName())
                sc_info["sc_kwargs"].update(name=sc_name)
                dst = pm.skinCluster(sc_info["sc_args"], **sc_info["sc_kwargs"])
                dst = dst.nodeName()
                sc = get_skincluster(mesh.replace(base_grp, d_grp))
                logger.info(u'copy skin:{} to {}'.format(sc, dst))
                cmds.copySkinWeights(ss=sc,
                                     ds=dst,
                                     noMirror=True,
                                     surfaceAssociation='closestPoint',
                                     influenceAssociation=('label', 'oneToOne', 'closestJoint')
                                     # influenceAssociation = ('label', 'name', 'closestJoint')

                )
            except Exception as e:
                print(e)

    # 削除、リネームだとPyNode(uid）のオブジェクト参照が無くなる為、元のグループ以下に移動させる
    # base_children = cmds.listRelatives(base_grp, c=True, f=True) or []
    # d_children = cmds.listRelatives(d_grp, c=True, f=True) or []
    # cmds.delete(base_children)

    #for c in d_children:
    #    cmds.parent(c, base_grp)
    cmds.delete(d_grp, hi=True)

    # set one dagpose if it has multiple dagposes
    remake_bindpose(root.longName())
    cmds.select(base_grp)
    return True


def fix_joint_wpn(base_grp, pynodes_dict={}, rebind=True):
    """武器用リグ生成前のジョイント補正
    :param base_grp: string or PyNode
    :param pynodes_dict: dict
    :param rebind: bool
    :return bool or None:
    :rtype bool
    """
    if not pynodes_dict:
        return None
    else:
        root = pynodes_dict.get('root', None)
        grp_mesh = pynodes_dict.get('grp_mesh', None)
        grp_joint = pynodes_dict.get('grp_joint', None)

    # トップノードにスケールが入る場合にはあらかじめ補正する。
    top_scales = [round(s, 4) for s in pm.xform(base_grp, q=True, ws=True, a=True, s=True)]
    if top_scales != [1, 1, 1]:
        # if node are locked, unlock.
        for scale in ["scaleX", "scaleY", "scaleZ"]:
            if pm.getAttr('{}.{}'.format(base_grp, scale), lock=True):
                pm.setAttr('{}.{}'.format(base_grp, scale), lock=False)

        pm.setAttr('{}.scale'.format(base_grp), *[1, 1, 1], type="double3")
        logger.info("{}.scale are Reset by [1.0, 1.0, 1.0]".format(base_grp))

    pm.select(grp_joint, hi=True)
    joint_list = pm.ls(sl=True, l=True, type="joint")
    # bindjoint_list = [jnt for jnt in joint_list if not jnt.nodeName().endswith("_End")]
    pm.select(d=True)

    # goto bindpose
    goto_bind_pose(root)

    # delete all animetion key
    pm.delete(root, c=True, uac=False, hi="below", cp=1, s=1)

    # Reset Scale for Detatch skin
    # root_scales = pm.xform(root, q=True, r=True, s=True) if root else [1, 1, 1]

    # get skinMesh and skinCluster as dict if it skinbinded
    mesh_trs = get_mesh_transform([grp_mesh])
    skin_dict = {mesh: get_skincluster(mesh) for mesh in mesh_trs if get_skincluster(mesh)}

    # ################# Only Rebind ##################
    # if skinmesh exists, detatch skin
    '''if rebind and skin_dict:
        pm.select(grp_mesh)
        mel.eval('doDetachSkin "2" { "2","1" }')'''

    cmds.select(d=True)
    # set segmentScalecompensate zero at all joints
    set_segmentscale_zero(joint_list)
    # ################# Only Rebind ##################
    '''if not rebind:

        skin_list = []
        skin_list.extend(bindjoint_list)
        for mesh, sc in skin_dict.items():

            skin_list.append(mesh)
            # re-bind skin
            try:
                pm.skinCluster(skin_list, toSelectedBones=True,
                                 bindMethod=cmds.getAttr('{}.skinningMethod'.format(sc)),
                                 normalizeWeights=cmds.getAttr('{}.normalizeWeights'.format(sc)),
                                 weightDistribution=cmds.getAttr('{}.weightDistribution'.format(sc)),
                                 maximumInfluences=cmds.getAttr('{}.maxInfluences'.format(sc)),
                                 obeyMaxInfluences=cmds.getAttr('{}.maintainMaxInfluences'.format(sc)),
                                 dropoffRate=4,
                                 removeUnusedInfluence=False)
                if uoc:
                    for j in joint_list:
                        pm.setAttr("{}.uoc".format(j), uoc)

            except Exception as e:
                print(u"Skipped Error: ", e)
                print(u"Skinbinding may have a problem. Check the Skincluster:{} ".format(sc))'''

    cmds.select(d=True)

    # Dupricate # TODO: 複製後が値補正処理が確実では無いので、リファクタリング予定
    logger.info(u'Duplicate')
    d_grp = cmds.duplicate('{}'.format(base_grp), rr=True)[0]

    # reset_joint_rotate(d_grp)

    d_joint_list = get_joint_list(node_select(d_grp, 'root'))
    d_bindjoint_list = [j for j in d_joint_list if not j.endswith("_End")]
    cmds.select(d=True)

    # 値をきれいにする
    cmds.makeIdentity(d_joint_list, apply=True, t=0, r=0, s=0, n=0, pn=0, jointOrient=1)

    cmds.select(d=True)
    # ################# Only Rebind ##################
    # if skinmesh exists, detatch skin
    if rebind and skin_dict:

        if check_grp_node(d_grp, 'grp_mesh'):
            cmds.select(node_select(d_grp, 'grp_mesh'))
            cmds.select(node_select(d_grp, 'grp_mesh'), hi=True, tgl=True)
            mesh_list = [mesh for mesh in cmds.ls(sl=True, type='transform', l=True) if not mesh.endswith("_Outline")]

        for mesh in mesh_list:
            logger.info(u'mesh :{}'.format(mesh))
            cmds.select(d=True)
            skin_list = []
            skin_list.extend(d_bindjoint_list)
            skin_list.append(mesh)
            # src = get_skincluster(mesh.replace(d_grp, base_grp))
            sc = get_skincluster(mesh.replace(d_grp, base_grp)[1:])
            logger.info(u'old_skinCluster :{}'.format(sc))
            dst = cmds.skinCluster(
                skin_list,
                toSelectedBones=True,
                bindMethod=cmds.getAttr('{}.skinningMethod'.format(sc)),
                normalizeWeights=cmds.getAttr('{}.normalizeWeights'.format(sc)),
                weightDistribution=cmds.getAttr('{}.weightDistribution'.format(sc)),
                maximumInfluences=cmds.getAttr('{}.maxInfluences'.format(sc)),
                obeyMaxInfluences=cmds.getAttr('{}.maintainMaxInfluences'.format(sc)),
                dropoffRate=4,
                removeUnusedInfluence=False,
                name='{}_skinCluster'.format(mesh.rsplit('|', 1)[1])
            )[0]

            cmds.copySkinWeights(ss=sc,
                                 ds=dst,
                                 noMirror=True,
                                 surfaceAssociation='closestPoint',
                                 influenceAssociation=('label', 'oneToOne', 'closestJoint')
                                 )

    # 削除、リネームだとPyNode(uid）のオブジェクト参照が無くなる為、元のグループ以下に移動させる
    base_children = cmds.listRelatives(base_grp, c=True, f=True) or []
    d_children = cmds.listRelatives(d_grp, c=True, f=True) or []
    cmds.delete(base_children)
    for c in d_children:
        cmds.parent(c, base_grp)
    cmds.delete(d_grp, hi=True)

    # dupricate 後にroot, head ノードを更新
    root = pm.PyNode(node_select(base_grp, 'root'))

    # set one dagpose if it has multiple dagposes
    if root:
        remake_bindpose(root.longName())
    else:
        print("Cannot find 'root' under {}".format(base_grp))
    cmds.select(base_grp)
    print("finish FixJoint_wpn")

    return True


def face_move(meshes, adjust_position):
    """体のスケールとのずれを補正
    :param meshes: list of string:mesh
    :param adjust_position: float Y軸補正値

    """
    # 選択オブジェクト
    mesh_list = om.MSelectionList()
    for s in meshes:
        cmds.select([i for i in cmds.ls(s, dag=True, o=True, tr=True) if cmds.listRelatives(i, type='mesh')])
        temp = om.MGlobal.getActiveSelectionList()

        for i in range(temp.length()):
            mesh_list.add(temp.getDagPath(i))

    if not mesh_list.isEmpty():
        for i in range(mesh_list.length()):
            selDagPath = mesh_list.getDagPath(i)
            mitMeshVertIns = om.MItMeshVertex(selDagPath)

            mitMeshVertIns.reset()
            for n in range(mitMeshVertIns.count()):
                vert_pos = mitMeshVertIns.position()
                new_pos = om.MPoint(vert_pos[0], vert_pos[1] + adjust_position, vert_pos[2])
                mitMeshVertIns.setPosition(new_pos)
                next(mitMeshVertIns)


def fix_size(base_grp, meshes=None):
    """キャラクターモデルのサイズをMサイズに変更する。
    :param base_grp node: トップノード
    :param meshes node: 大きさを変更しないメッシュリスト
    """
    # original_size = "M"
    # L = 87.48209411621094
    # M = 84.41199493408203
    # S = 80.57437095642089
    # XS = 76.73674697875977

    # 頭の補正値
    # M - L : -3.07009918213
    # M - M : 0.0
    # M - S : 3.83762397766
    # M - XS: 7.67524795532

    # XS pelvis = 45.423
    # M  pelvis = 50.47
    # S  pelvis = 47.947
    # L  pelvis = 52.489

    if cmds.listRelatives(base_grp, p=True) is not None:
        logger.error(u'トップノードが選択されていません。 :{}'.format(base_grp))
        return

    pelvis = node_select(base_grp, 'C_pelvis')
    pelvis_value = round(cmds.getAttr('{}.tx'.format(pelvis)), 3)
    # print('{} : {}'.format(pelvis, pelvis_value))

    if pelvis_value == 45.423:
        logger.info(u'実行前のサイズ　XS　Size :{}'.format(base_grp))
        adjust_position = 7.67524795532
        adjust_scale = 1.11111

    elif pelvis_value == 47.947:
        logger.info(u'実行前のサイズ　S　Size :{}'.format(base_grp))
        adjust_position = 3.83762397766
        adjust_scale = 1.0526

    elif pelvis_value == 50.47:
        logger.info(u'実行前のサイズ　M　Size :{}'.format(base_grp))
        adjust_position = 0.0
        adjust_scale = 1
        logger.warning(u'既に M Size です。')
        return

    elif pelvis_value == 52.489:
        logger.info(u'実行前のサイズ　L　Size :{}'.format(base_grp))
        adjust_position = -3.07009918213
        adjust_scale = 0.9615
    else:
        logger.error(u'不明なサイズです。 :{}'.format(base_grp))
        return

    d_grp = cmds.duplicate('{}'.format(base_grp), rr=True, un=True)[0]

    d_meshes = []

    if not meshes:
        return

    for mesh in meshes:
        if node_select(d_grp, mesh):
            d_meshes.append(node_select(d_grp, mesh))

    if d_meshes:
        cmds.delete(d_meshes, ch=True)
        face_move(d_meshes, adjust_position)

    cmds.scale(adjust_scale, adjust_scale, adjust_scale, '{}|grp_joint'.format(d_grp), xyz=True, r=True)

    mesh_list = cmds.listRelatives(d_grp, c=True, ad=True, f=True, type='mesh')
    m_list = []

    for mesh in mesh_list:
        obj = cmds.listRelatives(mesh, p=True, f=True)
        if obj:
            m_list.append(obj[0])

    cmds.delete(m_list, ch=True)

    bindpose = cmds.listConnections('{}|grp_joint|root'.format(d_grp), type='dagPose')
    cmds.delete(bindpose)

    cmds.makeIdentity('{}|grp_joint'.format(d_grp), a=True, s=True)

    cmds.select(node_select(d_grp, 'root'), hi=True)
    joint_list = cmds.ls(sl=True, type='joint', l=True)

    cmds.select(d=True)

    if check_grp_node(d_grp, 'grp_mesh'):
        cmds.select(node_select(d_grp, 'grp_mesh'))
        cmds.select(node_select(d_grp, 'grp_mesh'), hi=True, tgl=True)
        mesh_list = cmds.ls(sl=True, type='transform', l=True)

    for mesh in mesh_list:
        logger.info(u'mesh :{}'.format(mesh))
        cmds.select(d=True)
        skin_list = []
        skin_list.extend(joint_list)
        skin_list.append(mesh)

        src = mel.eval('findRelatedSkinCluster {}'.format(mesh.replace(d_grp, base_grp)[1:]))

        if src:
            logger.info(u'old_skinCluster :{}'.format(src))

            dst = cmds.skinCluster(
                skin_list,
                toSelectedBones=True,
                bindMethod=cmds.getAttr('{}.skinningMethod'.format(src)),
                normalizeWeights=cmds.getAttr('{}.normalizeWeights'.format(src)),
                weightDistribution=cmds.getAttr('{}.weightDistribution'.format(src)),
                maximumInfluences=cmds.getAttr('{}.maxInfluences'.format(src)),
                obeyMaxInfluences=cmds.getAttr('{}.maintainMaxInfluences'.format(src)),
                dropoffRate=4,
                removeUnusedInfluence=False,
                name='{}_skinCluster'.format(mesh.rsplit('|', 1)[1])
            )[0]

            m_sel = om.MGlobal.getSelectionListByName(mesh)
            m_sel.getDagPath(0)

            inf = cmds.skinCluster(src, inf=True, q=True)
            selDagPath = m_sel.getDagPath(0)
            mitMeshVertIns = om.MItMeshVertex(selDagPath)

            src_object = str(selDagPath).replace(d_grp, base_grp)
            dst_object = selDagPath

            mitMeshVertIns.reset()
            for n in range(mitMeshVertIns.count()):
                weights = []
                for joint in inf:
                    v = cmds.skinPercent(src, '{}.vtx[{}]'.format(src_object, n), v=True, t=joint, q=True)
                    weights.append((joint.replace(base_grp, d_grp), round(v, 4)))

                cmds.skinPercent(dst, '{}.vtx[{}]'.format(dst_object, n), transformValue=weights, nrm=True)
                next(mitMeshVertIns)
