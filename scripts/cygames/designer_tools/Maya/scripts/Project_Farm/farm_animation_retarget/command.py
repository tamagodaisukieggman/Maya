# -*- coding: utf-8 -*-
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
    from builtins import zip
except:
    pass

import maya.cmds as cmds
import maya.mel as mel
import re
import os
from logging import getLogger
import pymel.core as pm

logger = getLogger(__name__)

GROUPRIGNAME = 'grp_rig'
RETARGET_NAMESPACE = 'retarget_motion'
ROOTJOINTNAME = 'root'
jointlist = [
    'pelvis', 'hip', 'spine', 'chest', 'neck', 'head', 'clavicle', 'ringroot',
    'ring', 'pinky', 'middle', 'index', 'thumb'
]
FK_LIST = ['upperarm', 'forearm', 'hand', 'upperleg', 'foreleg', 'foot', 'toe']
IK_LIST = ['hand', 'foot', 'toe']
IKFK_LIST = ['R_IKFK_leg_CTRL', 'L_IKFK_leg_CTRL', 'R_IKFK_arm_CTRL', 'L_IKFK_arm_CTRL']

TRANSFORM_ATTRS = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz", "v"]
ROOT_BONE = RETARGET_NAMESPACE + ':' + ROOTJOINTNAME

ROOT_CTRL = 'root_CTRL'

SCALE_LABEL = 'scaleFactor'
DEFAULT_VALUE = 0

MAYA_ASCII = 'mayaAscii'
MAYA_BINARY = 'mayaBinary'
FBX = 'FBX'

FILE_TYPES = {
    '.ma': MAYA_ASCII,
    '.mb': MAYA_BINARY,
    '.fbx': FBX
}


def check_node(name):
    u"""指定名のノードがシーンに存在するかどうか

    :param name: ノード名
    :type name: str

    :return: 存在するなら　true 存在しないなら　false
    :rtype: bool
    """
    return cmds.objExists(name)


def get_joint_list(root):
    u"""指定した名前以下のジョイントを全て取得

    :param root: 指定ジョイント
    :type root: str

    :return: ジョイントリスト
    :rtype: list
    """
    cmds.select(root, hi=True)
    return cmds.ls(sl=True, typ=['joint'], o=True, nt=False)


def get_label(name):
    u"""ジョイントの種別名を取得

    :param name: ノード名
    :type name: str

    :return: ラベル名
    :rtype: str
    """
    return re.search('[^0-9_A-Z]+[a-z]', name).group()


def set_translate_unlock(name):
    u"""移動値のアトリビュートをアンロックする

    :param name: ノード名
    :type name: str
    """
    cmds.setAttr('{}.tx'.format(name), lock=False, k=True)
    cmds.setAttr('{}.ty'.format(name), lock=False, k=True)
    cmds.setAttr('{}.tz'.format(name), lock=False, k=True)


def check_translate_lock(name):
    u"""移動値のアトリビュートのロック状態を調べる

    :param name: ノード名
    :type name: str

    :return: ロックされていれば True ロックされていなければ False
    :rtype: bool
    """
    tx = cmds.getAttr('{}.tx'.format(name), lock=True)
    ty = cmds.getAttr('{}.ty'.format(name), lock=True)
    tz = cmds.getAttr('{}.tz'.format(name), lock=True)

    if tx or ty or tz:
        return True
    else:
        return False


def set_rotate_unlock(name):
    u"""回転値のアトリビュートをアンロックする

    :param name: ノード名
    :type name: str
    """
    cmds.setAttr('{}.rx'.format(name), lock=False, k=True)
    cmds.setAttr('{}.ry'.format(name), lock=False, k=True)
    cmds.setAttr('{}.rz'.format(name), lock=False, k=True)


def check_rotate_lock(name):
    u"""回転値のアトリビュートのロック状態を調べる

    :param name: ノード名
    :type name: str

    :return: ロックされていれば True ロックされていなければ False
    :rtype: bool
    """
    rx = cmds.getAttr('{}.rx'.format(name), lock=True)
    ry = cmds.getAttr('{}.ry'.format(name), lock=True)
    rz = cmds.getAttr('{}.rz'.format(name), lock=True)

    if rx or ry or rz:
        return True
    else:
        return False


def set_scale_unlock(name):
    u"""スケール値のアトリビュートをアンロックする

    :param name: ノード名
    :type name: str
    """
    cmds.setAttr('{}.sx'.format(name), lock=False, k=True)
    cmds.setAttr('{}.sy'.format(name), lock=False, k=True)
    cmds.setAttr('{}.sz'.format(name), lock=False, k=True)


def set_unlock(nodes=[], attrs=TRANSFORM_ATTRS):
    u"""アトリビュートをアンロックする

    :param nodes: ノードリスト
    :type nodes: list
    """
    for node in nodes:
        for attr in attrs:
            try:
                cmds.setAttr('{}.{}'.format(node, attr), lock=False, k=True)
            except RuntimeError:
                pass


def set_bind_pose(file_type):
    u"""バインドポーズに戻す

    :return: 正しくバインドポーズに戻る場合 True
    :rtype: bool
    """
    logger.info(u'バインドポーズに戻す')
    print(("root_bone:", ROOT_BONE))

    if file_type == FBX:
        for joint in get_joint_list(ROOT_BONE):
            base_joint = joint.split(':', 1)[1]
            if check_node(base_joint):
                try:
                    cmds.copyAttr(base_joint, joint, v=True, at=TRANSFORM_ATTRS)
                except RuntimeError:
                    logger.error(u'バインドポーズに戻れません。')
                    return False
        return True

    if cmds.listConnections(ROOT_BONE, s=False, d=True, t='dagPose') > 0:
        try:
            cmds.select(ROOT_BONE)
            mel.eval("gotoBindPose;")
            return True
        except Exception as e:
            print(e)
            logger.error(u'Retargetデータのスケルトンのバインドポーズに戻れません。')
    else:
        logger.error(u'Retargetデータのスケルトンにバインドポーズがありません。')

    return False


def create_orientconstraint(target, node, offset):
    u"""回転コンストレイント

    :param target: constraint対象
    :param node: constraintを掛けられるノード
    :param offset: オフセット設定
    :type target: str or list
    :type node: str
    :type offset: bool

    :return: コンストレイント
    :rtype: str
    """
    return cmds.orientConstraint(target, node, mo=offset, w=1)


def create_pointconstraint(target, node, offset):
    u"""位置コンストレイント

    :param target: constraint対象
    :param node: constraintを掛けられるノード
    :param offset: オフセット設定
    :type target: str or list
    :type node: str
    :type offset: bool

    :return: コンストレイント
    :rtype: str
    """
    return cmds.pointConstraint(target, node, mo=offset, w=1)


def create_scaleconstraint(target, node, offset):
    u"""スケールコンストレイント

    :param target: constraint対象
    :param node: constraintを掛けられるノード
    :param offset: オフセット設定
    :type target: str or list
    :type node: str
    :type offset: bool

    :return: コンストレイント
    :rtype: str
    """
    return cmds.scaleConstraint(target, node, mo=offset, w=1)


def create_parentconstraint(target, node, offset):
    u"""ペアレントコンストレイント

    :param target: constraint対象
    :param node: constraintを掛けられるノード
    :param offset: オフセット設定
    :type target: str or list
    :type node: str
    :type offset: bool

    :return: コンストレイント
    :rtype: str
    """
    return cmds.parentConstraint(target, node, mo=offset, w=1)


def get_filepath():
    u"""ファイルパス取得

    :return: パス
    :rtype: str
    """
    return os.path.dirname(cmds.file(q=True, sn=True))


def get_parent(name):
    u"""親の名前取得

    :param name: ノード名
    :type name: str

    :return: 見つかれば親の名前
    :rtype: str or None
    """
    parent = cmds.listRelatives(name, p=True) or []

    if len(parent) > 0:
        return parent[0]
    return None


def get_scale(node):
    u""" リグに特定のアトリビュートがあれば、値を取得

    :param node: ノード
    :type node: str

    :return: アトリビュートの値
    :rtype: int
    """
    children = pm.listRelatives(node, ad=True) or []
    for child in children:
        if child == ROOT_CTRL:
            if pm.attributeQuery(SCALE_LABEL, node=child, exists=True):
                value = pm.getAttr('{}.{}'.format(child, SCALE_LABEL))
                return value


def set_scale(node, value):
    u""" リグに特定のアトリビュートがあれば、値をリセット

    :param node: ノード
    :type node: str
    """
    children = pm.listRelatives(node, ad=True) or []
    for child in children:
        if child == ROOT_CTRL:
            if pm.attributeQuery(SCALE_LABEL, node=child, exists=True):
                pm.setAttr('{}.{}'.format(child, SCALE_LABEL), value)
                logger.info("Exists: {}, and set {} {}".format(child, SCALE_LABEL, value))
                break


def retarget_connect(primary=False):
    u"""リターゲット

    :param primary: 基本ノードのみ実行の場合は True
    :type primary: bool
    """
    logger.info(u'アニメーション リターゲット')
    for joint in get_joint_list(ROOT_BONE):
        base_joint = joint.split(':', 1)[1]
        if check_node(base_joint):
            label = get_label(base_joint)

            i = 2
            if 'EX_' in joint:
                i = 3

            if '_End' in joint:
                if primary:
                    continue

                # SplineIK用の処理
                num = base_joint.index("_End")
                ik3_ctrl = base_joint[:i] + 'SplineIK_' + base_joint[i:num] + '_03_CTRL'
                if check_node(ik3_ctrl):
                    continue
                    # SplineIKの制御点が3つの場合の処理
                    # create_pointconstraint(joint, ik3_ctrl, 0)

                else:
                    # SplineIKの制御点が2つの場合の処理
                    ik2_ctrl = base_joint[:i] + 'SplineIK_' + base_joint[i:num] + '_02_CTRL'
                    if check_node(ik2_ctrl):
                        create_pointconstraint(joint, ik2_ctrl, 0)
                        print("OK : {}".format(ik2_ctrl))

                        ik1_ctrl = base_joint[:i] + 'SplineIK_' + base_joint[i:num] + '_01_CTRL'
                        if check_node(ik1_ctrl):
                            p00_joint = get_parent(joint)

                            create_pointconstraint([joint, p00_joint], ik1_ctrl, 0)
                            print("OK : {}".format(ik1_ctrl))

                continue

            if label == 'root':
                # ルートには何もしない
                continue

            # Primary
            if not ('EX_' in joint):
                if label in jointlist:
                    try:
                        create_orientconstraint(joint, base_joint + '_CTRL', 1)
                    except ValueError:
                        print(("Skipped: Constraint ", joint, " and ", base_joint + '_CTRL'))
                    if label == 'pelvis':
                        create_pointconstraint(joint, base_joint + '_CTRL', 1)

                    continue

                if label in FK_LIST:
                    fk_joint = base_joint[:i] + 'FK_' + base_joint[i:] + '_CTRL'
                    create_orientconstraint(joint, fk_joint, 1)

                    if label == 'upperleg' or label == 'upperleg':
                        set_translate_unlock(fk_joint)
                        create_pointconstraint(joint, fk_joint, 1)

                    if label == 'forearm':
                        ctrl = base_joint[:i] + 'elbow_CTRL'
                        set_translate_unlock(ctrl)
                        set_rotate_unlock(ctrl)
                        create_parentconstraint(joint, ctrl, 1)

                    if label == 'foreleg':
                        ctrl = base_joint[:i] + 'knee_CTRL'
                        set_translate_unlock(ctrl)
                        set_rotate_unlock(ctrl)
                        create_parentconstraint(joint, ctrl, 1)

                if label in IK_LIST:
                    if label == 'hand':
                        ik_joint = base_joint[:i] + 'IK_' + base_joint[i:] + '_trans_CTRL'
                        set_translate_unlock(ik_joint)
                        create_pointconstraint(joint, ik_joint, 1)
                        ik_joint = base_joint[:i] + 'IK_' + base_joint[i:] + '_rot_CTRL'
                        set_rotate_unlock(ik_joint)
                        create_orientconstraint(joint, ik_joint, 1)
                    else:
                        ik_joint = base_joint[:i] + 'IK_' + base_joint[i:] + '_CTRL'
                        set_translate_unlock(ik_joint)
                        set_rotate_unlock(ik_joint)

                        create_orientconstraint(joint, ik_joint, 1)
                        create_pointconstraint(joint, ik_joint, 1)

                    continue

            if not primary:
                logger.info(base_joint)
                if check_node(base_joint + '_CTRL'):
                    print("OK : {}".format(base_joint + '_CTRL'))

                    # ロックされていればスキップ
                    if not check_rotate_lock(base_joint + '_CTRL'):
                        create_orientconstraint(joint, base_joint + '_CTRL', 1)
                    else:
                        print("Skipped: OrientConstraint {} > {}".format(
                            joint, base_joint + '_CTRL'))

                    # ロックされていればスキップ
                    if not check_translate_lock(base_joint + '_CTRL'):
                        create_pointconstraint(joint, base_joint + '_CTRL', 1)
                    else:
                        print("Skipped: PointConstraint {} > {}".format(
                            joint, base_joint + '_CTRL'))

                    if label == 'bust':
                        set_scale_unlock(base_joint + '_CTRL')
                        cmds.cutKey(base_joint + '_CTRL',
                                    cl=True,
                                    at=("sx", "sy", "sz"))
                        create_scaleconstraint(joint, base_joint + '_CTRL', 1)

                fk_joint = base_joint[:i] + 'FK_' + base_joint[i:] + '_CTRL'
                if check_node(fk_joint):
                    print("OK : {}".format(fk_joint))
                    create_orientconstraint(joint, fk_joint, 1)

                ik_joint = base_joint[:i] + 'IK_' + base_joint[i:] + '_CTRL'
                if check_node(ik_joint):
                    print("OK : {}".format(ik_joint))
                    set_translate_unlock(ik_joint)
                    set_rotate_unlock(ik_joint)

                    create_orientconstraint(joint, ik_joint, 1)
                    create_pointconstraint(joint, ik_joint, 1)

        else:
            logger.info(u'{} が無いのでスキップします。'.format(base_joint))


def retarget_rig():
    u"""リグ用リターゲット
    """
    namespace_pattern = re.compile(r'(?<=\|)[^|]*:')

    def delete_namespace(name):
        return namespace_pattern.sub('', name)

    def get_object(name):
        return cmds.ls(name, l=True, o=True)[0]

    def get_name(name):
        return cmds.ls(name, l=True)[0]

    def get_attr(name):
        return cmds.attributeName(name, l=True, lf=False)

    def get_connections(node, src=True, targets=None, **kwargs):
        kwargs.update({'c': True, 'plugs': True, 's': src, 'd': not src})
        cncts = cmds.listConnections(node, **kwargs)
        cncts = (get_name(c) for c in cncts or [])
        cncts = list(zip(*[iter(cncts)] * 2))
        if targets:
            cncts = (c for c in cncts if all(get_object(t) in targets for t in c))
        cncts = ((t, n) if src else (n, t) for n, t in cncts)
        return list(cncts)

    def get_constraints(node):
        constraints = get_connections(node, t='constraint')
        return set(get_object(c[0]) for c in constraints)

    def get_targets(node):
        temp_targets = get_connections(node + '.target')
        targets = set(get_object(t[0]) for t in temp_targets)
        return [t for t in targets if t != node]

    def rename_attr(attr, src_nodes, dst_nodes):
        name = get_object(attr)
        for src, dst in zip(src_nodes, dst_nodes):
            if src == name:
                return '{}.{}'.format(dst, get_attr(attr))
        return attr

    def rename_attrs(attr, src_nodes, dst_nodes):
        return tuple(rename_attr(c, src_nodes, dst_nodes) for c in attr)

    def connect_attrs(attrs):
        for src, dst in attrs:
            cncts = get_connections(src, src=False)
            if cncts and cncts[0][1] == dst:
                continue
            cmds.connectAttr(src, dst, f=True)

    temp_srcs = cmds.namespaceInfo(RETARGET_NAMESPACE, ls=True, dp=True)
    srcs = cmds.ls(temp_srcs, dag=True, l=True)
    dsts = [delete_namespace(src) for src in srcs]

    nodes = [(src, dst) for src, dst in zip(srcs, dsts) if cmds.objExists(dst)]

    constraints = []

    # コンストレインの複製
    for src, dst in nodes:
        src_cnsts = get_constraints(src)

        if not src_cnsts:
            continue

        dst_cnsts = get_constraints(dst)
        cnsts = [(cmds.nodeType(c), get_targets(c)) for c in dst_cnsts]

        for src_cnst in src_cnsts:
            src_type = cmds.nodeType(src_cnst)
            src_targets = get_targets(src_cnst)
            dst_targets = [delete_namespace(t) for t in src_targets]

            if any(typ == src_type and set(tgt) == set(dst_targets) for typ, tgt in cnsts):
                continue

            if not all(cmds.objExists(t) for t in dst_targets):
                continue

            src_nodes = [src, src_cnst] + src_targets
            src_in = get_connections(src_cnst, targets=src_nodes)
            src_out = get_connections(src_cnst, src=False, targets=src_nodes)
            src_cncts = src_in + src_out

            dst_cnst = get_object(cmds.duplicate(src_cnst))
            dst_parent = cmds.listRelatives(dst_cnst, p=True)
            if dst_parent:
                parent = delete_namespace(get_object(dst_parent[0]))
                dst_cnst = get_object(cmds.parent(dst_cnst, parent))

            dst_nodes = [dst, dst_cnst] + dst_targets

            dst_cncts = [rename_attrs(c, src_nodes, dst_nodes) for c in src_cncts]

            connect_attrs(dst_cncts)

            constraints.append((src_cnst, dst_cnst))

    nodes += constraints

    # アニメーションカーブの複製
    for src, dst in nodes:
        attrs = cmds.listAttr(src, u=True, k=True)

        if not attrs:
            continue

        for attr in attrs:
            src_attr = '{}.{}'.format(src, attr)
            dst_attr = '{}.{}'.format(dst, attr)

            if not cmds.objExists(src_attr) or not cmds.objExists(dst_attr):
                continue

            src_curves = cmds.listConnections(
                src_attr, d=False, plugs=True, t='animCurve')

            if not src_curves:
                continue

            src_curve = cmds.ls(src_curves[0], l=True)[0]
            src_curve_node = cmds.ls(src_curve, l=True, o=True)[0]
            curve_attr = cmds.attributeName(src_curve, l=True)

            dst_curve_node = cmds.duplicate(src_curve_node)[0]
            dst_curve = '{}.{}'.format(dst_curve_node, curve_attr)

            cmds.connectAttr(dst_curve, dst_attr, f=True)


def import_motion_files(file_path):
    u"""モーションファイルの読み込み

    :param file_path: ファイル名
    :type file_path: str
    """
    nodes = cmds.ls('{}:*'.format(RETARGET_NAMESPACE))
    if len(nodes) > 0:
        logger.warning(u'シーン内にアニメーションファイルが見つかりました。更新のために削除します。')
        cmds.delete(nodes)

    file_type = FILE_TYPES.get(os.path.splitext(file_path)[1])

    if file_type == FBX:
        # TODO: 現在の設定を取得して読み込み後復元
        mel.eval('FBXProperty Import|IncludeGrp|MergeMode -v "Add";')

    logger.info(u'アニメーションファイルの読み込み')
    cmds.file(
            file_path,
            i=True,
            type=file_type,
            mergeNamespacesOnClash=True,
            namespace=RETARGET_NAMESPACE,
            importTimeRange="override"
            )

    return file_type


def delete_displaylayer():
    u"""ディスプレイレイヤーの削除
    """
    for layer in cmds.ls('{}:*'.format(RETARGET_NAMESPACE), type="displayLayer") or []:
        cmds.delete(layer)


def animation_bake(grp):
    u"""アニメーションのベイク

    :param grp: グループノード
    :type grp: str
    """
    logger.info(u'アニメーションのベイク')
    ctrl_list = [
        ctrl for ctrl in pm.ls(grp, dag=True, tr=True)
        if "_CTRL" in ctrl.nodeName()
    ]
    ctrl_list.remove('root_CTRL')
    f_min = cmds.playbackOptions(q=True, min=True)
    f_max = cmds.playbackOptions(q=True, max=True)

    pm.bakeResults(ctrl_list, t=(f_min, f_max), simulation=True)


def main(file_path, bake=True, delete=True, primary=False):
    u"""メイン

    :param file_path: ファイル名
    :param bake: リターゲットをベイクするかどうか
    :param delete: 読み込んだファイルを削除するかどうか
    :param primary: 基本ジョイントのみにリターゲットするかどうか
    :type file_path: str
    :type bake: bool
    :type delete: bool
    :type primary: str
    """

    if not os.path.exists(file_path):
        logger.error(u'ファイルパスが正しく設定されていません。')
        return

    file_type = FILE_TYPES.get(os.path.splitext(file_path)[1])

    if file_type != MAYA_ASCII:
        grp = pm.selected()[0] if pm.selected() else None
        print(grp)

        if grp is None:
            logger.info(u'グループが選択されていません。')
            return

        if not(grp in pm.ls(assemblies=True)):
            logger.info(u'トップノードが選択されていません。')
            return

        ctrl_list = [
            ctrl for ctrl in pm.ls(grp, dag=True, tr=True)
            if "_CTRL" in ctrl.nodeName()
        ]
        print(ctrl_list)

        if not ('root_CTRL' in ctrl_list):
            logger.error(u'Rigが正しく設定されていません。')
            return

        reset_main(grp)

    logger.info(u'リターゲット 実行')
    import_motion_files(file_path)

    if file_type == MAYA_ASCII:
        cmds.undoInfo(openChunk=True)
        retarget_rig()
        if bake:
            cmds.select(d=True)
            pattern = re.compile(r'^mdl_[^_]{3}_\d{6}_\d$')
            grps = [n for n in cmds.ls(assemblies=True) if pattern.match(n)]
            animation_bake(grps)
        if delete:
            logger.info(u'リターゲットノードの削除')
            nodes = cmds.ls('{}:*'.format(RETARGET_NAMESPACE))
            cmds.delete(nodes)
            delete_displaylayer()
        logger.info(u'リターゲット 完了')
        cmds.undoInfo(closeChunk=True)
    else:
        cmds.undoInfo(openChunk=True)
        # -----------------------------------------------------------------
        if cmds.objExists(ROOT_BONE):
            joints = cmds.listRelatives(ROOT_BONE, ad=True, f=True, type="joint") or []
            set_unlock(joints)
            # バインドポーズに戻れなければ実行しない。
            if set_bind_pose(file_type):
                scale_value = get_scale(grp)
                logger.info(u"Rig スケールをリセット")
                set_scale(grp, DEFAULT_VALUE)
                retarget_connect(primary)
                if bake:
                    cmds.select(d=True)
                    animation_bake(grp)

                if delete:
                    logger.info(u'リターゲットノードの削除')
                    nodes = cmds.ls('{}:*'.format(RETARGET_NAMESPACE))
                    cmds.delete(nodes)
                    delete_displaylayer()
                    # 削除が on の場合、scale値をセット
                    set_scale(grp, scale_value)
                logger.info(u'リターゲット 完了')
            else:
                pass
        else:
            logger.error(u'ルートジョイント:{}が存在しません。'.format(ROOT_BONE))
        # -----------------------------------------------------------------
        cmds.undoInfo(closeChunk=True)


# 以下、autocreate_rig の依存を切り離すために、持ってきています。
def reset_main(grp=None):
    u"""コントローラーをリセットする処理

    :param grp: グループノード
    :type grp: PyNode
    """
    if grp is None:
        logger.info(u'選択グループがありません。')
        return

    pm.undoInfo(openChunk=True)
    # -----------------------------------------------------------------
    logger.info(u'コントローラーの移動値、回転値をリセットします。')
    grp = pm.PyNode(grp) if pm.objExists(grp) else None
    grp_rig = get_pynode(grp, GROUPRIGNAME)
    if grp_rig:
        reset_ctrl_transform(grp=grp_rig, pos=True, rot=True)
    else:
        if pm.ls(sl=True):
            grp_name = pm.ls(sl=True)[0]
            reset_ctrl_transform(grp=grp_name, pos=True, rot=True)
        else:
            reset_ctrl_transform(pos=True, rot=True)
    # -----------------------------------------------------------------
    pm.undoInfo(closeChunk=True)


def get_pynode(grp, name, dict={}):
    u"""指定名(grp)ノード以下からname名のノードを取得
        dictの指定があれば、　{name:PyNode} でdict情報更新

    :param grp: ノード
    :param name: name
    :param dict: ノード辞書
    :type grp: PyNode
    :type name: str
    :type dict: dict

    :return: ノード
    :rtype: PyNode
    """
    pynode = None
    # ns = get_namespace(grp)
    pynodes = pm.ls(name)

    if not isinstance(grp, pm.PyNode):
        return None
    grp_longname = grp.longName()
    if len(pynodes) > 0:
        for node in pynodes:
            longname = str(node.longName())
            if longname.startswith(grp_longname):
                pynode = node

    if dict and pynode:
        dict[name] = pynode

    return pynode


def reset_ctrl_transform(grp=None, pos=True, rot=True):
    u"""コントローラーのtransformの値を 0 にする

    :param grp: ノード
    :param pos: 移動値
    :param rot: 回転値
    :type grp: PyNode
    :type pos: bool
    :type rot: bool
    """
    ctrl_list = [
        ctrl for ctrl in pm.ls(grp, dag=True, tr=True)
        if "_CTRL" in ctrl.nodeName()
    ]
    for ctrl in ctrl_list:
        if pos:
            for attr in ["tx", "ty", "tz"]:
                if not pm.getAttr('{}.{}'.format(ctrl, attr), lock=True):
                    pm.setAttr('{}.{}'.format(ctrl, attr), 0)

        if rot:
            for attr in ["rx", "ry", "rz"]:
                if not pm.getAttr('{}.{}'.format(ctrl, attr), lock=True):
                    pm.setAttr('{}.{}'.format(ctrl, attr), 0)
