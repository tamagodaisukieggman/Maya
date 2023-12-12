# -*- coding: utf-8 -*-

from __future__ import absolute_import

import ast
import os
import re

import maya.api.OpenMaya as OpenMaya2
import maya.cmds as cmds
import maya.mel as mel
from mtk.utils import getCurrentSceneFilePath

from . import const, lib_file


def get_workspace_dir():
    """ワークスペースルートディレクトリを取得
    :return: ルートディレクトリ
    :rtype: str
    """

    return cmds.workspace(q=True, rd=True)


def get_maya_version():
    u"""mayaバージョンを取得
    :return: apiバージョン
    :rtype: int
    """

    return cmds.about(api=True)


def is_maya_batch():
    u"""バッチモードかどうかを判断
    :return: batchモードの場合はTrue, GUIモードの場合はFalse
    :rtype: bool
    """

    return cmds.about(batch=True)


def list_mel_globals():
    """現在 MEL で宣言されているグローバル変数の名前を返します。
    :return: MELグローバル変数のリスト
    :rtype: list
    """

    return mel.eval('env')


def get_mel_global(variable_name):
    """mayaの変数
    :param variable_name:
    :return:
    """

    variable_name = '${}'.format(variable_name.strip('$'))

    ret = ''
    try:
        ret = mel.eval('$temp = {}'.format(variable_name))
    except Exception as e:
        cmds.warning(str(e))

    return ret


def list_maya_globals():
    """mayaグローバル変数名をリスト
    :return: mayaグローバル変数名のリスト
    :rtype: list
    """

    return mel.eval('env')


def get_maya_global(variable_name, var_type='string'):
    """mayaグローバル変数を取得
    :param str variable_name: mayaグローバル変数名
    :param str var_type: string or stringArray
    :return: mayaグローバル変数の値
    :rtype: str or list
    """

    default = '' if var_type == 'string' else []

    try:
        variable_name = '${}'.format(variable_name.strip('$'))
        if variable_name not in list_maya_globals():
            cmds.warning('{} is an undeclared variable. '.format(variable_name))
            return default

        if var_type == 'string':
            return mel.eval('string $__temp__s__={}'.format(variable_name))
        else:
            return mel.eval('string $__temp__sa__[]={}'.format(variable_name))

    except Exception as e:
        cmds.warning(str(e))
        return default


def get_scene_filepath():
    """シーンファイル名を取得
    :return: シーンファイル名
    :rtype: str
    """
    return getCurrentSceneFilePath()


def get_scene_timeunit():
    """シーンの時間単位を取得
    :return: 時間単位
    :rtype: str
    """

    return cmds.currentUnit(q=True, time=True)


def get_scene_linearunit():
    """シーンのリニア単位を取得
    :return: リニア単位
    :rtype: str
    """

    return cmds.currentUnit(q=True, linear=True)


def get_scene_angleunit():
    """シーンの角度単位を取得
    :return: 角度単位
    :rtype: str
    """

    return cmds.currentUnit(q=True, angle=True)


def get_object_namespace(node):
    u"""ノード名からネームスペースを取得

    :param str node: ノード名
    :return: ネームスペース名
    :rtype: str
    """

    node = node.rsplit('|', 1)[-1].split('.')[0]
    p = node.rfind(':')

    if p >= 0:
        return ':%s' % node[:p]
    else:
        return ':'


def get_object_name(node):
    u"""ノード名からオブジェクト名(ネームスペース無しのノード名)を取得
    :param str node: ノード名
    :return: オブジェクト名
    :rtype: str
    """

    node = node.rsplit('|', 1)[-1].split('.')[0]
    p = node.rfind(':')

    if p >= 0:
        return node[p + 1:]
    else:
        return node


def get_object_uniquename(object_name):
    """ノード名からオブジェクト名(ネームスペース無しのノード名)を取得

    get_object_name の ノード名重複対応版

    :param str object_name: ノード名
    :return: オブジェクト名
    :rtype: str
    """

    namespace = get_object_namespace(object_name).strip(':')
    return re.sub(':+', ':', '|'.join([
        p.replace(namespace, '', 1).strip(':') for p in object_name.split('|') if p
    ])).strip('|').split('.')[0]


def add_namespace(object_name, namespace=':'):
    """オブジェクトにネームスペースを追加した名前を取得
    dagNodeの場合は全階層にネームスペースを追加する
    :param str object_name: オブジェクト名
    :param str namespace: 追加ネームスペース名
    :return: object_name に namespaceを追加した名前
    :rtype: str
    """

    return '|'.join([
        '{}:{}'.format(namespace, p).strip(':') for p in object_name.split('|') if p
    ]).strip('|')


def replace_namespace(object_name, namespace=':'):
    """オブジェクトのネームスペースを入れ替えた名前を取得
    dagNodeの場合は全ての階層のネームスペースを入れ替える
    :param str object_name: オブジェクト名
    :param str namespace: 入れ替えるネームスペース名
    :return: ネームスペースを入れ替えたオブジェクト名
    :rtype: str
    """

    return re.sub(':+', ':', add_namespace(
        get_object_uniquename(object_name), namespace=namespace
    ))


def get_plug_longname(plug):
    """アトリビュート(プラグ)のロングネームを取得
    :param str plug: プラグ名
    :return: アトリビュートのロング名
    :rtype: str
    """

    if not cmds.objExists(plug):
        return ''

    node, attr = plug.split('.', 1)

    # return '{}.{}'.format(node, cmds.attributeQuery(attr, node=node, ln=True))
    return '{}.{}'.format(node, cmds.attributeName(plug, long=True))


def remove_extra_attributes(nodes, **kwargs):
    """ノードのユーザー定義アトリビュートを削除
    :param list nodes: ノード名のリスト
    :keyword list excludeAttrs: 除外アトリビュートのリスト
    """

    if not nodes:
        return

    exclude_attrs = kwargs.get('excludeAttrs', [])

    for node in nodes:
        attrs = cmds.listAttr(node, ud=True) or []
        for attr in attrs:
            if attr in exclude_attrs:
                continue

            cmds.setAttr('%s.%s' % (node, attr), lock=False)
            cmds.deleteAttr(node, attribute=attr)


def list_selected_channels(**kwargs):
    """選択中のチャンネルボックスのアトリビュートを取得
    :keyword str channelBox [cb]: ターゲットチャンネルボックスコントロール名
    :keyword bool longName [ln]: アトリビュートをロングネームで返す
    :keyword str targetSection: チャンネルを取得するセクションタイプ
    :keyword bool keyable [k]:
        True: keyableアトリビュートのみを取得する
        False: unkeyableアトリビュートのみを取得する
        None: 指定無しの場合は全て
    :keyword bool locked [l]: lockedアトリビュートのみを取得する
        True: lockedアトリビュートのみを取得する
        False: unlockedアトリビュートのみを取得する
        None: 指定無しの場合は全て
    """

    channel_box_ctrl = kwargs.get('channelBox', kwargs.get('cb', 'mainChannelBox'))
    as_long_name = kwargs.get('longName', kwargs.get('ln', True))
    target_section = kwargs.get('targetSection', kwargs.get('ts', 'all'))  # all or main or shape or output or history
    keyable = kwargs.get('keyable', kwargs.get('k', None))  # True or False or None
    locked = kwargs.get('locked', kwargs.get('l', None))  # True or False or None
    attr_name_only = kwargs.get('attrNameOnly', kwargs.get('ano', False))

    if not cmds.channelBox(channel_box_ctrl, q=True, ex=True):
        return []

    sels = cmds.ls(sl=True)
    if not sels:
        return []

    temp_list = []

    if target_section == 'all':
        target_sections = ['main', 'shape', 'output', 'history']
    else:
        target_sections = [target_section]

    for section in target_sections:
        attr_flags = {}
        obj_flags = {}
        if section == 'main':
            attr_flags = {'selectedMainAttributes': True}
            obj_flags = {'mainObjectList': True}

        elif section == 'shape':
            attr_flags = {'selectedShapeAttributes': True}
            obj_flags = {'shapeObjectList': True}

        elif section == 'output':
            attr_flags = {'selectedOutputAttributes': True}
            obj_flags = {'outputObjectList': True}

        elif section == 'history':
            attr_flags = {'selectedHistoryAttributes': True}
            obj_flags = {'historyObjectList': True}

        if not (attr_flags and obj_flags):
            continue

        attrs = cmds.channelBox(channel_box_ctrl, q=True, **attr_flags) or []
        if not attrs:
            continue

        objs = cmds.channelBox(channel_box_ctrl, q=True, **obj_flags) or []
        for obj in objs:
            for attr in attrs:
                if not cmds.attributeQuery(attr, node=obj, ex=True):
                    continue

                temp_list.append('{}.{}'.format(obj, attr))

    if not temp_list:
        return []

    if keyable is not None:
        if keyable:
            temp_list = [plug for plug in temp_list if cmds.getAttr(plug, k=True)]
        else:
            temp_list = [plug for plug in temp_list if not cmds.getAttr(plug, k=True)]

    if locked is not None:
        if locked:
            temp_list = [plug for plug in temp_list if cmds.getAttr(plug, lock=True)]
        else:
            temp_list = [plug for plug in temp_list if not cmds.getAttr(plug, lock=True)]

    if as_long_name:
        plugs = [get_plug_longname(plug) for plug in temp_list]
        if attr_name_only:
            attr_names = [plug.split('.', 1)[-1] for plug in plugs]
            return sorted(set(attr_names), key=attr_names.index)

        else:
            return plugs

    else:
        plugs = temp_list
        if attr_name_only:
            return [plug.split('.', 1)[-1] for plug in plugs]
        else:
            return plugs


def list_namespaces(root_namespace=':'):
    u"""シーン内のネームスペースのリストを取得

    ルート(':') 直下のネームスペースを取得します。

    :return: ネームスペースのリスト
    :rtype: list
    """

    exclude_list = ['UI', 'shared']
    root_namespace = root_namespace or ':'

    current = cmds.namespaceInfo(cur=True)
    cmds.namespace(set=root_namespace)
    namespaces = [':{}'.format(ns) for ns in cmds.namespaceInfo(lon=True) if ns not in exclude_list]
    cmds.namespace(set=current)

    return namespaces


def is_static_dag(node):
    """staticDag かの確認
    :param str node: ノード名
    :return: staticDagの場合はTrue
    :rtype: bool
    """

    if not cmds.objExists(node):
        return False

    if not cmds.objectType(node, isa='dagNode'):
        return False

    transformation_attrs = [
        't', 'tx', 'ty', 'tz',
        'r', 'rx', 'ry', 'rz',
        's', 'sx', 'sy', 'sz',
        'sh', 'shxy', 'shxz', 'shyz',
        'ra', 'rax', 'ray', 'raz',
        'jo', 'jox', 'joy', 'joz'
        'rp', 'rpx', 'rpy', 'rpz',
        'rpt', 'rptx', 'rpty', 'rptz',
        'sp', 'spx', 'spy', 'spz',
        'spt', 'sptx', 'spty', 'sptz',
        # 'is', 'isx', 'isy', 'isz',
    ]

    for attr in transformation_attrs:
        if not cmds.attributeQuery(attr, n=node, ex=1):
            continue

        src = cmds.connectionInfo('%s.%s' % (node, attr), sfd=1)
        if src:
            return False

    return True


def get_MObject2(objectName):
    """MObject (api2.0) を取得
    :param str objectName:ノード名
    :return: MObject
    :rtype: MObject
    """

    selList = OpenMaya2.MSelectionList()
    selList.add(objectName)

    return selList.getDependNode(0)


def get_MDagPath2(objectName):
    """MDagPath (api2.0) を取得
    :param str objectName:ノード名
    :return: MDagPath
    :rtype: MDagPath
    """

    selList = OpenMaya2.MSelectionList()
    selList.add(objectName)

    return selList.getDagPath(0)


def is_same_object(object_a, object_b):
    """同一ノードか判断
    :param str object_a: ノード名
    :param str object_b: ノード名
    :return: 同一オブジェクトかのブール値
    :rtype: bool
    """

    if not (object_a and object_b):
        return False

    if not (cmds.objExists(object_a) and cmds.objExists(object_b)):
        return False

    return get_MObject2(object_a) == get_MObject2(object_b)


def get_animcurve_timerange(crvs=None):
    """アニメーションカーブのレンジを取得
    :param list crvs: animCurveT ノードのリスト
    :return: タイムレンジのリスト([start_frame, end_frame])
    :rtype: tuple
    """

    if crvs:
        crvs = cmds.ls(crvs, type=const.ANIM_CURVE_T)
    else:
        crvs = cmds.ls(type=const.ANIM_CURVE_T)

    if crvs:
        return (
            cmds.findKeyframe(crvs, which='first'),
            cmds.findKeyframe(crvs, which='last')
        )

    else:
        return (
            cmds.findKeyframe(which='first'),
            cmds.findKeyframe(which='last')
        )


def get_timeslider_timerange(playback=True):
    """タイムスライダのレンジを取得
    :param bool playback:
        True: プレイバックレンジ (minTime - maxTime)
        False: アニメーションレンジ (animationStartTime - animationEndTime)
    :return: タイムレンジのリスト([start_frame, end_frame])
    :rtype: tuple
    """

    if playback:
        return (
            cmds.playbackOptions(q=True, minTime=True),
            cmds.playbackOptions(q=True, maxTime=True)
        )

    else:
        return (
            cmds.playbackOptions(q=True, animationStartTime=True),
            cmds.playbackOptions(q=True, animationEndTime=True)
        )


def get_timecontrol_timerange():
    """タイムコントロールのレンジを取得
    :return: タイムレンジのリスト([start_frame, end_frame])
    :rtype: tuple
    """

    return tuple(cmds.timeControl(get_maya_global('$gPlayBackSlider'), q=True, rangeArray=True))


def get_rendersettings_timerange():
    """レンダーセッティングのレンジを取得
    :return: レンダーセッティングのレンジ
    :rtype: tuple
    """

    return (
        cmds.getAttr('defaultRenderGlobals.startFrame'),
        cmds.getAttr('defaultRenderGlobals.endFrame')
    )


def create_pose_thumbnail(file_name):
    """ポーズサムネイルを作成
    :param str file_name: サムネイルファイル名
    :return: サムネイルファイル名
    :rtype: str
    """

    current_time = cmds.currentTime(q=True)

    ret = cmds.playblast(
        format='image',
        cf=file_name,
        clearCache=1, viewer=0, showOrnaments=0, fp=0, percent=100, compression='png', quality=100,
        st=current_time, et=current_time, os=1, w=const.THUMBNAIL_WIDTH, h=const.THUMBNAIL_HEIGHT)

    return ret


def create_animation_thumbnail(file_name, time_range=None):
    """アニメーションサムネイルを作成
    :param str file_name: サムネイルファイル名
    :param list time_range: タイムレンジのリスト [start_frame, end_frame]
    :return: サムネイルファイル名
    :rtype: str
    """

    if time_range is None:
        time_range = get_timeslider_timerange(playback=True)

    frames = range(time_range[0], time_range[1] + 1)

    ret = cmds.playblast(
        format='image',
        filename=file_name, fo=True,
        clearCache=1, viewer=0, showOrnaments=0, fp=4, percent=100, compression='png', quality=100,
        frame=frames, os=1, w=const.THUMBNAIL_WIDTH, h=const.THUMBNAIL_HEIGHT)

    dir_name, file_name = os.path.split(ret)

    files = lib_file.find_items(dir_name, file_name.replace('####', '*'), depth=0, find_type='file')
    files = sorted(files.values())

    return files


def save_optionvar(key, value, force=True):
    """optionVarに保存

    :param str key: キー名
    :param mixin value: 値
    :param bool force: 強制的に上書きするかのブール値

    :return: 保存できたかどうかのブール値
    :rtype: bool
    """

    v = str(value)
    if force:
        cmds.optionVar(sv=[key, v])
        return True
    else:
        if not cmds.optionVar(ex=key):
            cmds.optionVar(sv=[key, v])
            return True
        else:
            return False


def load_optionvar(key):
    """optionVarを取得

    :param str key: キー名
    :return: 保存された値, キーが見つからない場合は None
    :rtype: value or None
    """

    if cmds.optionVar(ex=key):
        return ast.literal_eval(cmds.optionVar(q=key))
    else:
        return None


def remove_optionvar(key):
    """optionVarを削除

    :param str key: キー名
    :return: 削除成功したかのブール値
    :rtype: bool
    """

    if cmds.optionVar(ex=key):
        cmds.optionVar(rm=key)
        return True
    else:
        return False
