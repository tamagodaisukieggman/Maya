# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os
import json
import time
import subprocess

import maya.cmds as cmds
import maya.mel as mel

try:
    from builtins import range
except Exception:
    pass


# 引数一時保存用のjsonパス
SAVE_SETTING_DIR = '{}{}/Documents/maya/scripts'.format(os.getenv('HOMEDRIVE'), os.getenv('HOMEPATH'))


def debug_print(msg='', status='INFO'):

    print('[{}] {}'.format(status, msg).encode('cp932'))


def batch_exec(module, func):

    batch_file_path = os.path.join('{}\\batch'.format(os.path.dirname(__file__)), 'mayabatch.bat')
    command = 'import {0}; {0}.{1};'.format(module, func).replace('\\', '\\\\').replace(' ', '__space__')

    maya_info = cmds.about(version=True)
    maya_version = maya_info.split(' ')[0]

    subprocess.Popen([batch_file_path, maya_version, '"' + command + '"'])


def save_setting(tool_name, settings):

    setting_json_path = os.path.join(SAVE_SETTING_DIR, '{}.json'.format(tool_name))
    with open(setting_json_path, 'w') as f:
        json.dump(settings, f, indent=4)

    # ファイル保存に時間がかかる場合があるので、10秒経過して出来てなかったらFalseを返す
    for _ in range(5):
        if os.path.exists(setting_json_path):
            return True
        time.sleep(2)

    return False


def load_setting(tool_name, delete_setting_file=True):

    settings = {}

    setting_json_path = os.path.join(SAVE_SETTING_DIR, '{}.json'.format(tool_name))
    with open(setting_json_path, 'r') as f:
        settings = json.load(f)

    if delete_setting_file:
        if os.path.exists(setting_json_path):
            os.remove(setting_json_path)

    return settings


def find_node(target_name, root_name=None):

    if root_name:
        node_list = [node for node in cmds.ls(target_name, l=True) if node.find(root_name) >= 0]
    else:
        node_list = [node for node in cmds.ls(target_name, l=True)]
    if len(node_list) == 1:
        return node_list[0]

    # 見つからなかったらリファレンスも検索する
    if root_name:
        node_list = [node for node in cmds.ls(target_name, l=True, r=True) if node.find(root_name) >= 0]
    else:
        node_list = [node for node in cmds.ls(target_name, l=True, r=True)]
    if len(node_list) == 1:
        return node_list[0]

    return None


def transfer_local_pivot_to_translate(target):
    """_summary_

    Args:
        target (_type_): _description_
    """

    if __has_locked_translate(target):
        return

    if __has_skin_cluster(target):
        return

    # ローカルピボットとトランスレートから原点からのベクトルと原点へのベクトルを計算
    pivs = cmds.xform(target, q=True, piv=True)[:3]
    trans = cmds.xform(target, q=True, t=True)
    sum_trans = [pivs[0] + trans[0], pivs[1] + trans[1], pivs[2] + trans[2]]
    inv_trans = [-sum_trans[0], -sum_trans[1], -sum_trans[2]]

    # 原点でフリーズしてローカルピボットの値をトランスレートにいれる
    cmds.xform(target, r=True, t=inv_trans)
    cmds.makeIdentity(target, a=True, t=True)
    cmds.xform(target, r=True, t=sum_trans)


def __has_locked_translate(target):
    """対象または対象の子供がlockされているtranslateを持っているかどうかを判別する

    Args:
        target (_type_): _description_

    Returns:
        _type_: _description_
    """

    all_transform = [target]
    add_transform = cmds.listRelatives(target, ad=True, type='transform', f=True)

    if add_transform:
        all_transform.extend(add_transform)

    for transform in all_transform:

        locked_attr_list = cmds.listAttr(transform, locked=True)
        if not locked_attr_list:
            continue

        for attr in locked_attr_list:
            if attr.endswith('translateX') or attr.endswith('translateY') or attr.endswith('translateZ'):
                return True

    return False


def __has_skin_cluster(target):
    """対象または対象の子供がskinClusterノードを持っているかどうかを判別する

    Args:
        target (_type_): _description_

    Returns:
        _type_: _description_
    """

    all_child_list = [target]
    add_child_list = cmds.listRelatives(target, ad=True, f=True)

    if add_child_list:
        all_child_list.extend(add_child_list)

    for child in all_child_list:

        if cmds.objectType(child) == 'joint':
            return True

        node_list = cmds.listHistory(child)
        if not node_list:
            continue

        for node in node_list:
            if node.find('skinCluster') >= 0:
                return True

    return False


def apply_euler_filter():
    """_summary_

    Returns:
        _type_: _description_
    """

    all_target_list = cmds.ls(typ='joint', fl=True, l=True)
    all_target_list.extend(cmds.ls(typ='transform', fl=True, l=True))

    if not all_target_list:
        return None

    target_list = []
    target_attr_list = []
    tmp_frame_time_list = []
    tmp_cut_time_list = []
    last_time = 0
    result = None

    for target in all_target_list:

        if target.find('|Neck') < 0:
            continue

        this_target_name = target.split('|')[-1]

        this_last_time = None
        has_keyframe = False

        if not cmds.keyframe('{}.rotateX'.format(target), q=True, keyframeCount=True) == 0:
            has_keyframe = True
            target_attr_list.append(this_target_name + '_rotateX')
            this_last_time = cmds.findKeyframe('{}.rotateX'.format(target), which='last')

        if not cmds.keyframe('{}.rotateY'.format(target), q=True, keyframeCount=True) == 0:
            has_keyframe = True
            target_attr_list.append(this_target_name + '_rotateY')
            this_last_time = cmds.findKeyframe('{}.rotateX'.format(target), which='last')

        if not cmds.keyframe('{}.rotateZ'.format(target), q=True, keyframeCount=True) == 0:
            has_keyframe = True
            target_attr_list.append(this_target_name + '_rotateZ')
            this_last_time = cmds.findKeyframe('{}.rotateX'.format(target), which='last')

        if this_last_time and this_last_time > last_time:
            last_time = this_last_time

        if has_keyframe:
            target_list.append(target)

    if not last_time:
        return result

    # filterで振り切ってしまうことがあるため、間に0キーを挿入
    for _time in range(int(last_time)):
        tmp_frame_time_list.append(_time + 0.5)
        tmp_cut_time_list.append((_time + 0.5, _time + 0.5))

    cmds.setKeyframe(target_list, at=['rx', 'ry', 'rz'], v=0, t=tmp_frame_time_list)

    # filter実行
    # pythonコマンドが動かないことがあったためmelコマンドを使用する
    target_attr_str = ' '.join(target_attr_list)
    result = mel.eval('filterCurve {}'.format(target_attr_str))

    # 挿入した0キーを除去
    cmds.cutKey(target_list, at=['rx', 'ry', 'rz'], t=tmp_cut_time_list, option="keys")

    return result
