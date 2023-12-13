# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import

try:
    # Maya 2022-
    from builtins import zip
    from builtins import str
except:
    pass

import maya.cmds as cmds
import maya.mel as mel
from PySide2 import QtWidgets
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
import re
import os
import glob
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
import logging
from . import animation_bake
from . import export_range
import csv

TOOL_VERSION = 'Ver 1.7'

ALL_MODEL = 'mdl_([a-z]{3})_([0-9]{4})([0-9]{2})_([1-3]{1})'
MODEL = '(unt|avt|enm|smn)_([0-9]{4})([0-9]{2})_([1-3]{1})'
CAMERA = '(cam)_([0-9]{4})([0-9]{2})_([1-3]{1})'
WEAPON_PROP = '(wpn|prp)_([0-9]{4})([0-9]{2})_([1-3]{1})'

COMMON = '[a-z]{3}_common[SM]{1}_([0-9]{1})'
LONG_SCENE = '^[a-z]{3}_([0-9]{4})([0-9]{2})_([0-9]{1})_([a-z]{3})_'

OLD_SCENE = '^([0-9]{4})([0-9]{2})_([0-9]{2})'
OLD_LONG_SCENE = '^(unt|avt)_([0-9]{4})([0-9]{2})_([0-9]{2})'

LONG_MODEL_SCENE = '^(unt|avt|prp|wpn|enm|smn)_(([0-9]?)([0-9]{4})([0-9]{2})|common[SML])_(?P<rank>[^_]+)_([a-z]{3})_'

LONG_COMMON_SCENE = '^[a-z]{3}_common[SM]{1}_([1-3]{1})_([a-z]{3})_'

ENEMY_SCENE = '^enm_([0-9]{4})([0-9]{2})'
LONG_ENEMY_SCENE = '^enm_([0-9]{4})([0-9]{2})_([1-3]{1})_([a-z]{3})_'

SIM_LABEL = "SIM"
EX_LABEL = "EX"

GRP_MESH = 'grp_mesh'
GRP_JOINT = 'grp_joint'
GRP_RIG = 'grp_rig'
ROOT_CTRL = 'root_CTRL'
ROOT_CTRL_FILTER = '^.*[|]{}$'.format(ROOT_CTRL)

SCALE_LABEL = 'scaleFactor'
DEFAULT_VALUE = 0

PROJECT_PATH = 'W:/Priari/svn/priari/80_3D'
EXP_PATH = '03_motion/animation'
BAKE = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]
REF = '_ref'
NS_TEMP = 'export_temp'

# 設定csv向けの値
SETTINGS = 'exporter_setting.csv'
EXP_PATH_LABEL = 'export_path'

TYPE_DICT = {
    "unt": "unit",
    "avt": "avatar",
    "enm": "enemy",
    "wpn": "weapon",
    "prp": "prop",
    "smn": "summon",
    "cam": "camera"
}

EXCLUDE = [
    '^{}_.*$'.format(SIM_LABEL),
    '^Head_center_offset$',
    '^Head_tube_center_offset$',
    '^Head_direction$',
    '^Eye_origin$',
    '^Look_target$',
    '^FX_pos_center$',
]

logger = logging.getLogger(__name__)


def fbx_options(fmt='Binary', bake='false'):
    u"""FBX の出力オプションを設定する

    :param fmt: ASCII or Binary
    :type fmt: str
    :param bake: 出力時のベイク設定 True ベイク False ベイクしない
    :type bake: bool
    """
    fbx_option = ''
    fbx_option += 'FBXExportFileVersion -v FBX201900;'
    fbx_option += 'FBXExportSmoothingGroups -v false;'  # Smooting Groups
    fbx_option += 'FBXExportHardEdges -v false;'  # Split per-vertex Normals
    fbx_option += 'FBXExportTangents -v false;'  # Tangents and Binormals
    fbx_option += 'FBXExportSmoothMesh -v false;'  # Smooth Mesh
    fbx_option += 'FBXProperty Export|IncludeGrp|Geometry|SelectionSet -v false;'  # Selection Sets
    fbx_option += 'FBXProperty Export|IncludeGrp|Geometry|AnimationOnly -v false;'  # Convert to Null objects
    fbx_option += 'FBXExportInstances -v false;'  # Preserve Instances
    fbx_option += 'FBXExportReferencedAssetsContent -v false;'  # Referenced Assets Content
    fbx_option += 'FBXExportTriangulate -v false;'  # Triangulate
    fbx_option += 'FBXExportCameras -v false;'
    fbx_option += 'FBXExportConstraints -v true;'
    fbx_option += 'FBXExportShapes -v true;'
    fbx_option += 'FBXExportSkeletonDefinitions -v true;'
    fbx_option += 'FBXExportInputConnections -v true;'
    fbx_option += 'FBXExportBakeComplexAnimation -v "{}";'.format(bake)
    fbx_option += 'FBXProperty Export|AdvOptGrp|Fbx|AsciiFbx -v "{}";'.format(fmt)
    fbx_option += 'FBXProperty Export|IncludeGrp|Animation -v true;'

    mel.eval(fbx_option)


def insert_keys(joints):
    u"""キーの挿入

    :param joints: ジョイントのリスト
    :type joints: list
    """
    if not joints:
        return

    start, end = get_frame()
    bake_list = ['{}.{}'.format(joint, t) for joint in joints for t in BAKE]

    for attr in bake_list:
        if not cmds.listConnections(attr):
            if cmds.keyframe(attr, query=True, keyframeCount=True) < 1:
                cmds.setKeyframe(attr, t=(start))


def bake_animation(joints):
    u"""ジョイントのアニメーションをベイクする。

    :param joints: ジョイントのリスト
    :type joints: list
    """
    if not joints:
        return

    start, end = get_frame()

    bake_list = [
        '{}.{}'.format(joint, t) for joint in joints for t in BAKE
    ]
    cmds.bakeResults(
                    bake_list,
                    t=(start, end),
                    disableImplicitControl=True,
                    minimizeRotation=True,
                    sm=True
                    )

    # 回転値のアトリビュートだけフィルターをかける。
    filter_list = [
        '{}.{}'.format(joint, t) for joint in joints for t in BAKE[3:6]
    ]
    cmds.filterCurve(filter_list)


def set_joint_keys(dup_node, node, exclude_patterns):
    u"""ジョイントのキーを設定

    :param node: ノード
    :type node: string

    :return: 想定する名前と違う名前にリネームされたもののリスト
    :rtype: list
    """

    grp = get_grp_joint(node)
    joints = cmds.listRelatives(grp, ad=True, type='joint', f=True) or []

    shapes = cmds.listRelatives(grp, ad=True, type='locator', f=True) or []
    locators = cmds.listRelatives(shapes, p=True, type='transform', f=True, s=False) or []
    joints.extend(locators)

    dup_grp = get_grp_joint(dup_node)
    dup_joints = cmds.listRelatives(dup_grp, ad=True, type='joint', f=True) or []

    dup_shapes = cmds.listRelatives(dup_grp, ad=True, type='locator', f=True) or []
    dup_locators = cmds.listRelatives(dup_shapes, p=True, type='transform', f=True, s=False) or []
    dup_joints.extend(dup_locators)

    constraints = cmds.listRelatives(dup_grp, ad=True, type='constraint', f=True) or []
    if constraints:
        cmds.delete(constraints)
    delete_animation(dup_grp)

    constraint_list = constraint_joints(dup_joints, joints)
    bake_animation(dup_joints)
    constraint_list = [c for c in cmds.listRelatives(dup_joints, type="constraint") or []]
    if constraint_list:
        cmds.delete(constraint_list)

    # weapon と prop 用の アニメーションリセット処理
    if re.search(WEAPON_PROP, dup_node):
        reset_joint(dup_joints)

    # リネーム前にuuidを保持
    joint_uuids = [cmds.ls(j, uid=True)[0] for j in dup_joints] or []

    # 出力用にリネームする
    differentlist = rename_joint(dup_joints)

    clear_animation(joint_uuids, exclude_patterns)

    return differentlist


def rename_joint(joints):
    u"""出力時にジョイントのリネーム

    :param joints: ジョイントのリスト
    :type joints: list

    :return: 想定する名前と違う名前にリネームされたもののリスト
    :rtype: list
    """
    if not joints:
        return

    sim_count = len(SIM_LABEL) + 1
    ex_count = len(EX_LABEL) + 1

    differentlist = []

    for joint in joints:
        if not (SIM_LABEL in cmds.listAttr(joint)):
            continue

        if cmds.getAttr("{}.{}".format(joint, SIM_LABEL)):
            joint_name = joint.rsplit("|", 1)[1]
            if SIM_LABEL + '_' in joint_name[:sim_count]:
                continue
            elif EX_LABEL + '_' in joint_name[:ex_count]:
                new_joint_name = joint_name.replace(EX_LABEL, SIM_LABEL)
            else:
                new_joint_name = "{}_{}".format(SIM_LABEL, joint_name)

            # リネーム
            slist = om.MSelectionList()
            slist.add(joint)
            dag = slist.getDagPath(0)
            node = dag.node()

            dgmodifier = om.MDGModifier()
            dgmodifier.renameNode(node, new_joint_name)
            dgmodifier.doIt()

            renamed_name = om.MFnDependencyNode(node).name()
            print("Renamed : {} > {}".format(joint_name, renamed_name))

            # リネームしようとした名前と違うとき
            if renamed_name != new_joint_name:
                differentlist.append([new_joint_name, renamed_name])

    return differentlist


def reset_joint(joints):
    u"""移動値と回転値のアニメーションを削除して値をリセット

    :param joints: ジョイントのリスト
    :type joints: list
    """
    if not joints:
        return

    reset_attr = ["tx", "ty", "tz", "rx", "ry", "rz"]

    for j in joints:
        if re.match('.*\|root\d$', j):
            root_child = cmds.listRelatives(j, c=True, type='joint', f=True) or []
            root_child.append(j)
            cmds.cutKey(root_child, cl=True, at=reset_attr)

            for rc in root_child:
                for attr in reset_attr:
                    cmds.setAttr("{}.{}".format(rc, attr), 0)


def clear_animation(joint_uuids, exclude_patterns):
    u"""除外対象ジョイントからアニメーションを削除

    :param joint_uuids: ジョイントのリスト（uuid）
    :type joint_uuids: list
    """
    if not joint_uuids:
        return

    clear_attr = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]

    for joint_uuid in joint_uuids:
        joint = cmds.ls(joint_uuid, l=True)[0]
        joint_name = joint.rsplit("|", 1)[1]
        if any(re.match(pattern, joint_name) for pattern in exclude_patterns):
            for attr in clear_attr:
                # アニメーション削除時に値が消えるのを防ぐためアクセスしておく
                cmds.getAttr("{}.{}".format(joint, attr))
            cmds.cutKey(joint, cl=True, at=clear_attr)


def delete_animation(joint_grp):
    u"""アニメーションを削除

    :param joint_grp: ジョイントグループ
    :type joint_grp: list
    """
    nodes = cmds.listRelatives(joint_grp, ad=True, f=True) or []

    delete_attr = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]

    for node in nodes:
        cmds.cutKey(node, cl=True, at=delete_attr)


def constraint_joints(dup_joints, joints):
    u"""同じ名前のジョイントにコンストレイン設定

    :param dup_joints: 複製ジョイントリスト
    :param joints: ジョイントリスト
    :type dup_joints: list
    :type joints: list

    :return: コンストレイントリスト
    :rtype: list
    """

    constraint_list = []
    for d_joint in dup_joints:
        if d_joint.startswith("|"):
            d_joint_name = d_joint[1:].split("|", 1)[1]
        else:
            d_joint_name = d_joint.split("|", 1)[1]
        for joint in joints:
            if joint.startswith("|"):
                joint_name = joint[1:].split("|", 1)[1]
            else:
                joint_name = joint.split("|", 1)[1]

            if d_joint_name == joint_name:
                constraint_list.append(
                    create_orientconstraint(joint, d_joint, False)[0]
                )
                constraint_list.append(
                    create_pointconstraint(joint, d_joint, False)[0]
                )
                # 親スケールの値が正しくベイクされない為、スケールのみコネクションで接続　-要解除-
                cmds.connectAttr("{}.scale".format(joint), "{}.scale".format(d_joint), f=True)
    return constraint_list


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


def get_scene_path():
    u"""シーンファイルのパスを取得

    :return: ファイル名
    :rtype: str
    """
    return cmds.file(q=True, sn=True)


def search_dir(path, dir):
    u"""パスで指定したディレクトリまで取得

    :param str path: パス
    :param str dir: 検索名
    :type path: str
    :type dir: str

    :return: パス
    :rype: str
    """
    if '/' in path:
        current_path = path.rsplit('/', 1)[0]
        current_dir = path.rsplit('/', 1)[1]
        if current_dir != dir:
            return search_dir(current_path, dir)
        else:
            return path.rsplit('/', 1)[0]
    else:
        return os.path.splitdrive(path)[0]


def check_scene_name():
    u"""シーン名が命名規則に沿っているか調べる

    :return: 正しい True 正しくない False
    :rtype: bool
    """
    file_name = os.path.basename(cmds.file(q=True, sn=True))
    if re.match(LONG_MODEL_SCENE, file_name):
        return True
    elif re.match(LONG_ENEMY_SCENE, file_name):
        return True
    elif re.match(OLD_SCENE, file_name):
        text = "This is the name of the scene given by the old naming convention."
        warning_log(text, file_name)
        return True
    elif re.match(OLD_LONG_SCENE, file_name) or re.match(ENEMY_SCENE, file_name):
        text = "This is the name of the scene given by the old naming convention."
        warning_log(text, file_name)
        return True
    # elif re.match(LONG_COMMON_SCENE, file_name):
    #    return True
    else:
        return False


def get_name(uuid):
    u"""uuid から オブジェクト名を取得

    :param uuid: ノードの uuid
    :type uuid: str

    :return: ノード名
    :rtype: str
    """
    node = cmds.ls(uuid, long=True)[0]
    if node.startswith("|"):
        node = node[1:]

    return node


def get_frame():
    u"""現在のタイムラインの開始フレームと終了フレームを取得

    :returns: 開始フレーム、終了フレーム
    :rtype: int, int
    """
    return int(oma.MAnimControl.minTime().value), int(oma.MAnimControl.maxTime().value)


def set_frame(start, end):
    u"""タイムラインの開始フレームと終了フレームを設定

    :param start: 開始フレーム
    :type start: int
    :param end: 終了フレーム
    :type end: int
    """
    cmds.playbackOptions(min=start, ast=start, max=end, aet=end)


def duplicate_node(node):
    u"""ノードを複製

    :param node: 複製するノード名
    :type node: str

    :returns: dup_node 複製したノード, uid 複製したノードのuuid
    :rtype: str, str
    """
    dup_nodes = cmds.duplicate(node, un=True)
    dup_node = dup_nodes[0]
    uid = cmds.ls(dup_nodes, uid=True)[0]

    delete_list = []

    if ":" in node:
        node_name = node.split(":")[1]
    else:
        node_name = node

    for d in dup_nodes:
        dn = cmds.ls(d, l=True)[0]
        if cmds.nodeType(dn) in ["joint", "transform"]:
            if dn.startswith("|"):
                name = dn[1:].split("|", 1)[0]
            else:
                name = dn.split("|", 1)[0]

            # 別のアセットグループのノードは削除
            if node_name != name:
                delete_list.append(dn)

        elif cmds.nodeType(dn) in ["unitConversion", "multiplyDivide", "reverse"]:
            # 不要なノードは削除
            delete_list.append(dn)
        else:
            pass

    cmds.delete(delete_list)

    return dup_node, uid


def get_grp_joint(node):
    u"""ノード直下の grp_joint を取得

    :param node: ノード
    :type node: str

    :return: child grp_jointノード
    :rtype: str
    """
    grp = []
    children = cmds.listRelatives(node, c=True, f=True) or []
    for child in children:
        if re.search(GRP_JOINT, child):
            grp.append(child)

        if re.search(GRP_RIG, child):
            continue

        g_children = cmds.listRelatives(child, c=True, f=True) or []
        for g_child in g_children:

            if re.search(GRP_JOINT, g_child):
                grp.append(g_child)

    if grp:
        return grp
    return None


def reset_scale(node):
    u"""リグに特定のアトリビュートがあれば、値をリセット

    :param node: ノード
    :type node: str
    """
    children = cmds.listRelatives(node, ad=True, f=True, type='transform') or []
    for child in children:
        if re.match(ROOT_CTRL_FILTER, child):
            if cmds.attributeQuery(SCALE_LABEL, node=child, exists=True):
                cmds.setAttr('{}.{}'.format(child, SCALE_LABEL), DEFAULT_VALUE)
                print("Exists: {}, and set {} {}".format(child, SCALE_LABEL, DEFAULT_VALUE))
                break


def get_scale(node):
    u""" リグに特定のアトリビュートがあれば、値を取得

    :param node: ノード
    :type node: str

    :return: アトリビュートの値
    :rtype: int
    """
    children = cmds.listRelatives(node, ad=True, f=True, type='transform') or []
    for child in children:
        if re.match(ROOT_CTRL_FILTER, child):
            if cmds.attributeQuery(SCALE_LABEL, node=child, exists=True):
                value = cmds.getAttr('{}.{}'.format(child, SCALE_LABEL))
                return value


def set_scale(node, value):
    u""" リグに特定のアトリビュートがあれば、値をリセット

    :param node: ノード
    :type node: str
    """
    children = cmds.listRelatives(node, ad=True, f=True, type='transform') or []
    for child in children:
        if re.match(ROOT_CTRL_FILTER, child):
            if cmds.attributeQuery(SCALE_LABEL, node=child, exists=True):
                cmds.setAttr('{}.{}'.format(child, SCALE_LABEL), value)
                print("Exists: {}, and set {} {}".format(child, SCALE_LABEL, value))
                break


def delete_grp_node(node):
    u"""ノード直下 または 孫階層 の grp_joint と grp_mesh 以外を削除

    :param node: ノード
    :type node: str
    """
    children = cmds.listRelatives(node, c=True, f=True) or []
    delete_list = []

    if re.search(WEAPON_PROP, node):
        for child in children:
            g_children = cmds.listRelatives(child, c=True, f=True) or []
            if re.search(GRP_RIG, child):
                delete_list.append(child)
                continue

            if re.search(GRP_MESH, child) or re.search(GRP_JOINT, child):
                continue

            grp = False
            for g_child in g_children:
                if re.search(GRP_MESH, g_child) or re.search(GRP_JOINT, g_child):
                    grp = True
                    continue
                else:
                    delete_list.append(g_child)

            if not grp:
                delete_list.append(child)

        else:
            if delete_list != []:
                cmds.delete(delete_list, hi=True)
    else:
        for child in children:
            if re.search(GRP_MESH, child) or re.search(GRP_JOINT, child):
                continue
            else:
                delete_list.append(child)
        else:
            if delete_list != []:
                cmds.delete(delete_list, hi=True)


def get_csv_setting():
    u"""setting.csvから値の取得

    :return: setting_dict { 設定ラベル : 値 }
    :rtype: dict
    """
    file_dir = os.path.dirname(__file__).replace(os.sep, '/')
    setting_path = '{}/{}'.format(file_dir, SETTINGS)
    setting_dict = {}

    try:
        with open(setting_path) as f:
            reader = csv.reader(f)
            row_list = [row for row in reader]

            for row in row_list:
                if row[0] == EXP_PATH_LABEL:
                    if not row[1]:
                        warning_log('{} : Output path not found.'.format(EXP_PATH_LABEL), setting_path)
                        continue

                    path = row[1].replace(os.sep, '/')
                    if not re.match(r'^[a-zA-Z0-9_/]+$', path):
                        warning_log('{} : Invalid path.'.format(EXP_PATH_LABEL), setting_path)
                        continue

                    setting_dict[EXP_PATH_LABEL] = path
    except Exception:
        warning_log('The setting csv file is not correct.', setting_path)

    return setting_dict


def get_export_path(exp_type, node_name, split_name):
    u"""書き出しパスを取得

    :param exp_type: unit or enemy
    :type rxp_type: str

    :return: export_path 書き出しパス
    :rtype: str
    """
    setting_dict = get_csv_setting()

    # 設定ファイルがあればそこからパスを取得する。
    if EXP_PATH_LABEL in setting_dict:
        s_path = setting_dict[EXP_PATH_LABEL]
        s_dir = s_path.split('/', 1)[0]
        scene_path = get_scene_path()

        work_dir = search_dir(scene_path, s_dir)
        base_path = '{}/{}/'.format(work_dir, s_path)

    else:
        project_dir = PROJECT_PATH.replace(os.sep, '/')
        # 標準書き出しパスを設定
        base_path = '{}/{}/'.format(project_dir, EXP_PATH)
        warning_log('Output with default path.', base_path)

    file_name = os.path.splitext(os.path.basename(get_scene_path()))[0]
    """
    if exp_type == 'common':
        type_path = ''
        if node_name[:3] == 'unt':
            type_path = 'unit/'
        elif node_name[:3] == 'avt':
            type_path = 'avatar/'

        if re.search(COMMON, file_name):
            com = re.search(COMMON, file_name).group()
        else:
            com = node_name[:4] + 'common'
        dir_name = com
        node_name = com
    """

    type_path = '{}/'.format(exp_type)
    dir_name = node_name[:-2]
    split_suffix = split_name or ''

    match = re.match(LONG_MODEL_SCENE, file_name)

    if match:
        # ノード名とファイル名のタイプが等しい場合はモデルIDをファイル名から取得
        # ランク以降は常にファイル名から取得する
        if TYPE_DICT.get(match.group(1)) == exp_type:
            dir_name = '{}_{}'.format(match.group(1), match.group(2))
        export_dir = base_path + type_path + dir_name + '/' + dir_name + '_' + match.group('rank')
        export_file = dir_name + '_' + file_name[match.start('rank'):] + split_suffix + '.fbx'
    else:
        export_dir = base_path + type_path + dir_name + '/' + node_name
        export_file = node_name + '_' + file_name.split("_", 2)[-1] + split_suffix + '.fbx'

    export_path = export_dir + '/' + export_file

    if not os.path.isdir(export_dir):
        os.makedirs(export_dir)

    return export_path


def check_child(node):
    u"""ノード直下に grp_joint、grp_mesh が存在するか確認

    :param node: ノード
    :type node: str

    :return: 存在する True 存在しない False
    :rtype: bool
    """
    children = cmds.listRelatives(node, c=True, f=True) or []
    joint = False
    mesh = False
    for child in children:
        if re.search(GRP_JOINT, child):
            joint = True
        if re.search(GRP_MESH, child):
            mesh = True

    if joint and mesh:
        return True
    else:
        return False


def check_grandchild(node):
    u"""ノードの孫階層に grp_joint、grp_mesh が存在するか確認

    :param node: ノード
    :type node: str

    :return: 存在する True 存在しない False
    :rtype: bool
    """
    children = cmds.listRelatives(node, c=True, f=True) or []
    joint = False
    mesh = False
    child_count = 0
    check_count = 0
    for child in children:
        if re.search(GRP_RIG, child):
            continue

        child_count += 1
        g_children = cmds.listRelatives(child, c=True, f=True) or []
        for g_child in g_children:
            if re.search(GRP_JOINT, g_child):
                joint = True
            if re.search(GRP_MESH, g_child):
                mesh = True
        else:
            if joint and mesh:
                check_count += 1

    if child_count == check_count:
        return True
    else:
        return False


def cleanup_child(exp_grp):
    u"""ノードの複製をした時に外部へのコンストレインが残ってしまうことがある対応
        現状は Constraint のみ確認

    :param exp_grp: 出力ノードのリスト
    :type exp_grp: list
    """

    delete_list = []
    for exp_node in cmds.ls(exp_grp, long=True):
        dup_grp = get_grp_joint(exp_node)
        dup_joints = cmds.listRelatives(dup_grp, ad=True, f=True) or []
        for j in dup_joints:
            if cmds.objectType(j) != 'joint':
                if 'Constraint' in cmds.objectType(j):
                    delete_list.append(j)

                    nodes = cmds.listRelatives(exp_node, ad=True, f=True) or []
                    for tag in cmds.listConnections(j + '.target'):
                        if not ("|" + tag in nodes):
                            delete_list.append(tag)
    else:
        if delete_list:
            cmds.delete(delete_list)

    # ジョイントのスケールコネクション解除
    for exp_node in cmds.ls(exp_grp, long=True):
        joints = cmds.ls(exp_node, dag=True, type="joint")
        if joints:
            connections = cmds.listConnections(["{}.scale".format(j) for j in joints], p=True, c=True, d=False, s=True)
            # 接続アトリビュートごとのペアでイテレーション接続を解除
            for cons in zip(*[iter(connections)] * 2):
                cmds.disconnectAttr(cons[1], cons[0])

def create_temp_namespace():
    u"""ダミー用のネームスペース作成
    """
    cmds.namespace(set=':')
    if not cmds.namespace(ex=NS_TEMP):
        cmds.namespace(add=NS_TEMP)


def set_temp_namespace(node):
    u"""ダミー用のネームスペース設定
    """
    if not (':' in node):
        node = cmds.rename(node, '{}:{}'.format(NS_TEMP, node))

    typ = 'blendShape'
    ad = cmds.listRelatives(node, ad=True, f=True)
    bs = set([b for d in ad for b in cmds.ls(cmds.listHistory(d), typ=typ)])

    for blendShape in bs:
        if not (':' in blendShape):
            cmds.rename(blendShape, '{}:{}'.format(NS_TEMP, blendShape))

    return node


def delete_temp_namespace():
    u"""ダミー用のネームスペース削除
    """
    cmds.namespace(set=':')
    if cmds.namespace(ex=NS_TEMP):
        ns_nodes = cmds.namespaceInfo(NS_TEMP, ls=True)
        if ns_nodes and len(ns_nodes) > 0:
            for ns_node in ns_nodes:
                cmds.rename(ns_node, ':{}'.format(ns_node[len(NS_TEMP):]))

        cmds.namespace(rm=NS_TEMP, mnr=True)


def open_file(file_path):
    u"""maファイルを開く

    :param file_path: ファイルパス
    :type file_path: str
    """
    try:
        print("SceneOpen : {}".format(file_path))
        cmds.file(file_path, o=True, f=True, executeScriptNodes=True, ls='mplicitLoadSettings')
    except Exception as e:
        print(e)


def command_export(file_path, start=None, end=None, excludes_ex=False):
    u"""bat出力の基本処理

    :param file_path: ファイルパス
    :param start: 開始フレーム
    :param end: 終了フレーム
    :param excludes_ex: Ex骨を除外するか
    :type file_path: str
    :type start: int or None
    :type end: int or None
    :type excludes_ex: bool
    """
    open_file(file_path)
    if export_fbx(start, end, batch=True, excludes_ex=excludes_ex):
        info_log('Export completed.', file_path)
    else:
        critical_log('Export ERROR.', file_path)


def csv_export(file_path, excludes_ex=False):
    u"""csvから出力処理

    :param file_path: ファイルパス
    :type file_path: str
    """
    try:
        with open(file_path) as f:
            reader = csv.reader(f)
            row_list = [row for row in reader]

            for row in row_list:
                if not os.path.isfile(row[0]):
                    critical_log('Specified data not found.', row[0])
                    continue
                if u'{}'.format(row[1]).isdecimal() and u'{}'.format(
                        row[2]).isdecimal():
                    if int(row[2]) > int(row[1]):
                        command_export(row[0], int(row[1]), int(row[2]), excludes_ex)
                    else:
                        value = '(file : {} start : {} , end : {} )'.format(
                            row[0], row[1], row[2])
                        critical_log('Illegal frame value is set.', value)
                        continue
                else:
                    value = '(file : {} start : {} , end : {} )'.format(
                        row[0], row[1], row[2])
                    critical_log(
                        'The frame value is set to a non-numeric value.',
                        value)
                    continue
    except Exception:
        critical_log('csv file is not correct.', file_path)


def bat_export(exportfiles, excludes_ex=False):
    u"""maファイルを検索する

    :param exportfiles: 出力ディレクトリリスト
    :type exportfiles: list
    """
    info_print('Animation Exporter {}'.format(TOOL_VERSION))

    for exportfile in exportfiles:
        if os.path.exists(exportfile):
            if os.path.isdir(exportfile):
                print('Directory : {}'.format(exportfile))
                dir_files = glob.glob('{}/*.m*'.format(exportfile))
                for dir_file in dir_files:
                    print('File : {}'.format(dir_file))
                    if dir_file[-3:] in ['.ma', '.mb']:
                        load_plugin()
                        command_export(dir_file, excludes_ex=excludes_ex)
                    else:
                        critical_print('Unsupported file types', dir_file)
            else:
                print('File : {}'.format(exportfile))
                if exportfile[-3:] in ['.ma', '.mb']:
                    load_plugin()
                    command_export(exportfile, excludes_ex=excludes_ex)
                elif exportfile[-4:] == '.csv':
                    load_plugin()
                    csv_export(exportfile, excludes_ex)
                else:
                    critical_print('Unsupported file types', exportfile)


def load_plugin():
    # FBX Plugin のロード
    if not hasattr(cmds, 'pluginInfo'):
        import maya.standalone
        maya.standalone.initialize(name='python')

    if not cmds.pluginInfo('fbxmaya.mll', q=True, loaded=True):
        try:
            cmds.loadPlugin('fbxmaya.mll')
        except Exception:
            critical_log('The plugin failed to load', 'fbxmaya.mll')

    if not cmds.pluginInfo('mtoa.mll', q=True, loaded=True):
        try:
            cmds.loadPlugin('mtoa.mll')
        except Exception:
            critical_log('The plugin failed to load', 'mtoa.mll')


def critical_print(text, node=None):
    u"""エラープリント表示

    :param text: 表示するテキスト
    :param node: ノード名
    :type text: str
    :type node: str
    """
    print(u'!' * 150)
    print(u'')
    if node:
        print('{} : {}'.format(text, node))
    else:
        print('{}'.format(text))
    print(u'')
    print(u'!' * 150)


def critical_log(text, node=None):
    u"""エラーロガー表示

    :param text: 表示するテキスト
    :param node: ノード名
    :type text: str
    :type node: str
    """
    logger.critical(u'!' * 150)
    logger.critical(u'')
    if node:
        try:
            logger.critical(u'{} : {}'.format(text, node))
        except Exception:
            print('{} : {}'.format(text, node))
    else:
        try:
            logger.critical(u'{}'.format(text))
        except Exception:
            print('{}'.format(text))
    logger.critical(u'')
    logger.critical(u'!' * 150)


def warning_log(text, node=None):
    u"""警告ロガー表示

    :param text: 表示するテキスト
    :param node: ノード名
    :type text: str
    :type node: str
    """
    logger.warning(u'*' * 150)
    logger.warning(u'')
    if node:
        try:
            logger.warning(u'{} : {}'.format(text, node))
        except Exception:
            print('{} : {}'.format(text, node))
    else:
        try:
            logger.warning(u'{}'.format(text))
        except Exception:
            print('{}'.format(text))
    logger.warning(u'')
    logger.warning(u'*' * 150)


def info_print(text, node=None):
    u"""お知らせプリント表示

    :param text: 表示するテキスト
    :param node: ノード名
    :type text: str
    :type node: str
    """
    print(u'#' * 150)
    if node:
        print('{} : {}'.format(text, node))
    else:
        print('{}'.format(text))
    print(u'#' * 150)


def info_log(text, node=None):
    u"""お知らせロガー表示

    :param text: 表示するテキスト
    :param node: ノード名
    :type text: str
    :type node: str
    """
    logger.info(u'#' * 150)
    if node:
        try:
            logger.info(u'{} : {}'.format(text, node))
        except Exception:
            print('{} : {}'.format(text, node))
    else:
        try:
            logger.info(u'{}'.format(text))
        except Exception:
            print('{}'.format(text))
    logger.info(u'#' * 150)


def export_fbx(start=None, end=None, batch=False, excludes_ex=False):
    u"""fbx出力処理

    :param start: 開始フレーム
    :param int end: 終了フレーム
    :param batch: バッチ出力かどうか
    :param excludes_ex: ex骨を除くかどうか
    :type start: int or None
    :type end: int or None
    :type excludes_ex: bool
    :type batch: bool
    """
    if not check_scene_name():
        critical_log('File name is incorrect.')
        return

    ranges = [export_range.ExportRange(None, start, end)]

    if start is None and end is None:
        ranges = export_range.ExportRange.from_node() or ranges

    u_nodes = [cmds.ls(n, uid=True)[0] for n in cmds.ls(assemblies=True)]
    exp_nodes = []

    # 途中リネームに対応できるようにuuidでリストを回す。
    for u_node in u_nodes:
        exp_type = None
        node = get_name(u_node)

        # リファレンスノードを判定して、リファレンスのネームスペースを除去
        if cmds.referenceQuery(node, isNodeReferenced=True):
            ref_file = cmds.referenceQuery(node, f=True)
            rn = cmds.referenceQuery(ref_file, referenceNode=True)
            ns = rn.replace("RN", ":")
            num = len(ns)
            name = node[num:]
        else:
            name = node

        # ネームスペースが付いているものを除去してノードの名前取得
        if ':' in name:
            name = name.split(':', 1)[1]
        else:
            name = name

        node_name = ""

        # common 設定用
        # if re.search(COMMON, name):
        #    if not check_child(node):
        #        warning_log('grp_joint, grp_mesh not found. Skip.', node)
        #        continue
        #    node_name = re.search(COMMON, name).group()
        #    exp_type = 'common'

        if re.search(MODEL, name):
            if not check_child(node):
                warning_log('grp_joint, grp_mesh not found. Skip.', node)
                continue
            node_name = re.search(MODEL, name).group()
            exp_type = TYPE_DICT[node_name[:3]]

        # elif re.search(CAMERA, name):
        #    node_name = re.search(CAMERA, name).group()
        #    exp_type = TYPE_DICT[node_name[:3]]

        elif re.search(WEAPON_PROP, name):
            if check_child(node):
                warning_log('Old hierarchical data.', node)
            if not check_child(node) and not check_grandchild(node):
                warning_log('grp_joint, grp_mesh not found. Skip.', node)
                continue

            node_name = re.search(WEAPON_PROP, name).group()
            exp_type = TYPE_DICT[node_name[:3]]

        if re.search(ALL_MODEL, name):
            if cmds.namespace(ex=name):
                cmds.namespace(rename=[name, name + REF])
                warning_log('Rename because of conflicts.',
                            '{} → {}'.format(name, name + REF))

            if ':' in node and cmds.objExists(name):
                critical_log('Name conflicts occur during output.', name)
                continue

        if exp_type is None:
            continue

        try:
            cmds.undoInfo(stateWithoutFlush=False)
            create_temp_namespace()

            differentlists = []
            exp_grp = []

            if re.search(ALL_MODEL, node):
                # namespaceが設定されていない場合、ダミー用ネームスペースを付与
                node = set_temp_namespace(node)

                scale_value = get_scale(node)
                # スケールリセット
                reset_scale(node)
                # 出力用の複製作成
                dup_node, uid = duplicate_node(node)
                # 出力に関係のないものを削除
                delete_grp_node(dup_node)
                exclude_patterns = EXCLUDE[:]
                if excludes_ex:
                    exclude_patterns.append('^{}_.*$'.format(EX_LABEL))
                differentlists.extend(set_joint_keys(dup_node, node, exclude_patterns))
                exp_grp.append(uid)
                set_scale(node, scale_value)

            if not exp_grp:
                info_log('Output node not found.')
                delete_temp_namespace()
                cmds.undoInfo(stateWithoutFlush=True)
                return False

            cmds.select(cmds.ls(exp_grp, long=True), hi=True)

            # ディスプレイレイヤー削除処理
            # 一旦選択ノードでディスプレイレイヤーを作成後、削除
            d_layer = cmds.createDisplayLayer()
            cmds.delete(d_layer)

            cmds.bakePartialHistory()
            cleanup_child(exp_grp)

            fbx_options()

            for r in ranges:
                # エクスポートするタイプからパスを生成
                export_path = get_export_path(exp_type, node_name, r.name)

                if r.start is not None and r.end is not None:
                    print('start : {}, end : {}'.format(r.start, r.end))
                    set_frame(r.start, r.end)

                mel.eval(u'FBXExport -f "{}" -s'.format(export_path))
                info_log('FBXExport ', export_path)

            # 出力後の後処理
            cmds.delete(cmds.ls(exp_grp, long=True), hi=True)
            delete_temp_namespace()

            # リネーム時に競合が発生した場合
            if differentlists:
                text = "A name conflict occurred during renaming.\nIt has been renamed as shown below."
                warning_log(text.replace("\n", ""))

                detailetext = ''
                for data in differentlists:
                    d = '{} > {}'.format(data[0], data[1])
                    print(d)
                    detailetext += d + '\n'
                if not batch:
                    confirm_msgbox(text, detailetext)

            cmds.undoInfo(stateWithoutFlush=True)

        except Exception as e:
            print('type: {}\nerror : {}'.format(type(e), str(e)))
            cmds.undoInfo(stateWithoutFlush=True)
            return False
    return True


def confirm_msgbox(text, detailetext, title=None, parent=None):
    u"""確認メッセージボックス

    :param datalist : 詳細リストに表示する文字列
    :param title : 表示する文言
    :param parent : 親Widget
    :type datalist: list
    :type title: str
    :type parent: QWidget
    """
    msgbox = AEMsgBox(parent)
    _title = u"Warning !"
    msgbox.setIcon(msgbox.Warning)

    if title:
        msgbox.setWindowTitle(u"{}".format(title))
    else:
        msgbox.setWindowTitle(_title)

    msgbox.setText(text)
    msgbox.setDetailedText(detailetext)
    msgbox.addButton(u"OK", msgbox.ActionRole)

    # 詳細リストを開くために、ボタンをクリックする。
    for button in msgbox.buttons():
        if button.text() == "Show Details...":
            button.click()

    msgbox.exec_()


# Maya window の子供としてメッセージボックスを作成
class AEMsgBox(MayaQWidgetBaseMixin, QtWidgets.QMessageBox):
    def __init__(self, parent=None):
        super(AEMsgBox, self).__init__(parent=parent)


def main(excludes_ex=False):
    info_log('Animation Exporter {}'.format(TOOL_VERSION))
    print(get_scene_path())

    if export_fbx(excludes_ex=excludes_ex):
        info_log('Export completed.')
    else:
        critical_log('Export ERROR.')
