# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import re
import sys

import maya.cmds as cmds

from .. import utility as base_utility

try:
    # Maya 2022-
    from builtins import range
except Exception:
    pass


# ==================================================
def exists(target_node, target_attr):
    """
    アトリビュートが存在するか

    :param target_node: ノード
    :param target_attr: アトリビュート
    :return :存在する場合はTrue
    """

    if not base_utility.node.exists(target_node):
        return False

    if not target_attr:
        return False

    this_exists = True
    try:
        cmds.getAttr(target_node + '.' + target_attr, type=True)
    except Exception:
        this_exists = False

    return this_exists


# ==================================================
def add(target_node, target_attr, attr_value,
        attr_type=None, attr_nice_name=None):
    """
    アトリビュートを追加

    :param target_node: ノード
    :param target_attr: アトリビュート
    :param attr_value: アトリビュート値
    :param attr_type: アトリビュートタイプ(color, vector, enum, array, message)
    :param attr_nice_name: アトリビュートショート名
    """

    if exists(target_node, target_attr):
        return

    if not target_attr:
        return

    if attr_value is None:
        return

    if not attr_nice_name:
        attr_nice_name = target_attr

    this_attr_value_type = type(attr_value)

    # Python3ではunicodeのtypeはない
    target_type = ''
    if sys.version_info.major == 2:
        target_type = unicode
    else:
        target_type = bytes

    if this_attr_value_type == str or this_attr_value_type == target_type:

        cmds.addAttr(target_node,
                     longName=target_attr,
                     dataType='string',
                     niceName=attr_nice_name)
        cmds.setAttr(target_node + '.' + target_attr,
                     attr_value,
                     type='string')

    elif this_attr_value_type == int:

        cmds.addAttr(target_node,
                     longName=target_attr,
                     attributeType='long',
                     defaultValue=attr_value,
                     niceName=attr_nice_name)

    elif this_attr_value_type == float:

        cmds.addAttr(target_node,
                     longName=target_attr,
                     attributeType='double',
                     defaultValue=attr_value,
                     niceName=attr_nice_name)

    elif this_attr_value_type == bool:

        cmds.addAttr(target_node,
                     longName=target_attr,
                     attributeType='bool',
                     defaultValue=attr_value,
                     niceName=attr_nice_name)

    elif this_attr_value_type == list:

        if attr_type == 'color':

            cmds.addAttr(target_node,
                         longName=target_attr,
                         usedAsColor=True,
                         attributeType='float3')

            cmds.addAttr(target_node,
                         longName=target_attr + 'R',
                         attributeType='float',
                         parent=target_attr)

            cmds.addAttr(target_node,
                         longName=target_attr + 'G',
                         attributeType='float',
                         parent=target_attr)

            cmds.addAttr(target_node,
                         longName=target_attr + 'B',
                         attributeType='float',
                         parent=target_attr)

            cmds.setAttr(target_node + '.' + target_attr,
                         attr_value[0], attr_value[1], attr_value[2],
                         type='float3')

        elif attr_type == 'enum':

            enum_str = ''

            for cnt in range(0, len(attr_value)):

                enum_str += attr_value[cnt]

                if cnt != len(attr_value) - 1:
                    enum_str += ':'

            cmds.addAttr(target_node,
                         longName=target_attr,
                         attributeType='enum',
                         enumName=enum_str,
                         niceName=attr_nice_name)

        else:

            cmds.addAttr(target_node,
                         longName=target_attr,
                         attributeType='double3')

            cmds.addAttr(target_node,
                         longName=target_attr + 'X',
                         attributeType='double',
                         parent=target_attr)

            cmds.addAttr(target_node,
                         longName=target_attr + 'Y',
                         attributeType='double',
                         parent=target_attr)

            cmds.addAttr(target_node,
                         longName=target_attr + 'Z',
                         attributeType='double',
                         parent=target_attr)

            cmds.setAttr(target_node + '.' + target_attr,
                         attr_value[0], attr_value[1], attr_value[2],
                         type='double3')

    elif attr_type == 'array':

        cmds.addAttr(target_node,
                     longName=target_attr,
                     dataType='Int32Array',
                     multi=True,
                     niceName=attr_nice_name)

    elif attr_type == 'message':

        cmds.addAttr(target_node,
                     longName=target_attr,
                     attributeType='message',
                     niceName=attr_nice_name)


# ==================================================
def delete(target_node, target_attr_name):
    """
    アトリビュートを削除

    :param target_node: ノード
    :param target_attr_name: アトリビュート名
    """

    if not exists(target_node, target_attr_name):
        return

    try:
        cmds.deleteAttr(target_node, at=target_attr_name)
    except Exception as e:
        print('{0}'.format(e))


# ==================================================
def search(target_node, target_attr_name):
    """
    アトリビュートを検索

    :param target_node: ノード
    :param target_attr_name: 対象アトリビュート名 正規表現

    :return :アトリビュート名
    """

    hit_attr_list = search_list(target_node, target_attr_name)

    if not hit_attr_list:
        return

    return hit_attr_list[0]


# ==================================================
def search_list(target_node, target_attr_name):
    """
    アトリビュートを検索 リスト版

    :param target_node: ノード
    :param target_attr_name: 対象アトリビュート名 正規表現

    :return :アトリビュート名リスト
    """

    if not base_utility.node.exists(target_node):
        return

    all_attr_list = cmds.listAttr(target_node)

    if not all_attr_list:
        return

    hit_attr_list = []

    if target_attr_name in all_attr_list:

        hit_attr_list = [target_attr_name]

    else:

        re_obj = re.compile(target_attr_name)

        for attr in all_attr_list:

            if not re_obj.search(attr):
                continue

            hit_attr_list.append(attr)

    return hit_attr_list


# ==================================================
def get_value(target_node, target_attr, default_value=None):
    """
    アトリビュートの値を取得

    :param target_node: ノード
    :param target_attr: アトリビュート
    :param default_value: デフォルト値

    :return :アトリビュートの値
    """

    result_value = __get_value_base(
        target_node, target_attr, None, default_value)

    return result_value


# ==================================================
def get_value_from_frame(target_node, target_attr, frame, default_value=None):
    """
    フレームのアトリビュートの値を取得

    :param target_node: ノード
    :param target_attr: アトリビュート
    :param default_value: デフォルト値

    :return :アトリビュートの値
    """

    result_value = __get_value_base(
        target_node, target_attr, frame, default_value)

    return result_value


# ==================================================
def __get_value_base(target_node, target_attr, frame, default_value):

    result_value = default_value

    if not exists(target_node, target_attr):
        return result_value

    if frame is None:
        result_value = cmds.getAttr(target_node + '.' + target_attr)
    else:
        result_value = cmds.getAttr(target_node + '.' + target_attr, t=frame)

    if type(result_value) == list:
        result_value = list(result_value[0])

    return result_value


# ==================================================
def set_value(target_node, target_attr, value):
    """
    アトリビュートの値を設定

    :param target_node: 対象ノード
    :param target_attr: アトリビュート名
    :param value: アトリビュート値
    """

    if not exists(target_node, target_attr):
        return

    attr_type = cmds.getAttr(target_node + '.' + target_attr, typ=True)

    if attr_type == 'string':

        # ------------------------------
        # 文字列の場合

        is_settable = \
            cmds.getAttr(target_node + '.' + target_attr, settable=True)

        if not is_settable:
            return

        cmds.setAttr(target_node + '.' + target_attr,
                     value,
                     type='string')

    elif re.search('.*\d$', attr_type):

        # ------------------------------
        # 配列系で一括設定ができそうな場合は対応

        is_settable = \
            cmds.getAttr(target_node + '.' + target_attr, settable=True)

        if is_settable:

            if attr_type.find('2') > 0:
                cmds.setAttr(target_node + '.' +
                             target_attr, value[0], value[1])
                return

            if attr_type.find('3') > 0:
                cmds.setAttr(target_node + '.' + target_attr,
                             value[0], value[1], value[2])
                return

        # ------------------------------
        # アトリビュートタイプがdouble3などの場合

        attr_list = search_list(
            target_node, target_attr + '.{1}$')

        if not attr_list:
            return

        # ------------------------------
        # リスト作成

        value_list = None
        if type(value) == list:
            value_list = value
        else:
            value_list = [value]

        # ------------------------------
        # 値割り当て

        count = -1
        for attr in attr_list:
            count += 1

            this_value = value_list[-1]

            if count < len(value_list):
                this_value = value_list[count]

            is_settable = \
                cmds.getAttr(target_node + '.' + attr, settable=True)

            if not is_settable:
                continue

            cmds.setAttr(target_node + '.' + attr, this_value)

    else:

        # ------------------------------
        # その他

        is_settable = \
            cmds.getAttr(target_node + '.' + target_attr, settable=True)

        if not is_settable:
            return

        cmds.setAttr(target_node + '.' + target_attr, value)


# ==================================================
def set_key(target_node, target_attr, value, frame):
    """
    キーフレームをセット

    :param target_node: ノード
    :param target_attr: アトリビュート
    :param value: 値
    :param frame: フレーム
    """

    if not exists(target_node, target_attr):
        return

    attr_type = cmds.getAttr(target_node + '.' + target_attr, typ=True)

    if re.search('.*\d$', attr_type):

        # ------------------------------
        # アトリビュートタイプがdouble3などの場合

        attr_list = search_list(
            target_node, target_attr + '.{1}$')

        if not attr_list:
            return

        # ------------------------------
        # リスト作成

        value_list = None
        if type(value) == list:
            value_list = value
        else:
            value_list = [value]

        # ------------------------------
        # 値割り当て

        count = -1
        for attr in attr_list:
            count += 1

            this_value = value_list[-1]

            if count < len(value_list):
                this_value = value_list[count]

            fix_value = this_value

            if this_value is None:
                fix_value = get_value_from_frame(
                    target_node, attr, frame)

            is_keyable = \
                cmds.getAttr(target_node + '.' + attr, keyable=True)

            if not is_keyable:
                return

            is_settable = \
                cmds.getAttr(target_node + '.' + attr, settable=True)

            if not is_settable:
                return

            cmds.setKeyframe(target_node + '.' + attr,
                             value=fix_value, time=frame)

    else:

        # ------------------------------
        # その他

        fix_value = value

        if value is None:
            fix_value = get_value_from_frame(
                target_node, target_attr, frame)

        is_keyable = \
            cmds.getAttr(target_node + '.' + target_attr, keyable=True)

        if not is_keyable:
            return

        is_settable = \
            cmds.getAttr(target_node + '.' + target_attr, settable=True)

        if not is_settable:
            return

        cmds.setKeyframe(target_node + '.' + target_attr,
                         value=fix_value, time=frame)


# ==================================================
def get_key_info_list(target_node, target_attr):

    if not exists(target_node, target_attr):
        return

    frame_list = cmds.keyframe(
        target_node, attribute=target_attr, query=True, tc=True)

    if not frame_list:
        return

    key_info_list = []

    for frame in frame_list:

        this_key_info = get_key_info(target_node, target_attr, frame)

        if not this_key_info:
            return

        key_info_list.append(this_key_info)

    return key_info_list


# ==================================================
def get_key_info(target_node, target_attr, frame):

    frame_list = cmds.keyframe(
        target_node, attribute=target_attr, query=True, tc=True)

    if not frame_list:
        return

    if frame not in frame_list:
        return

    value = cmds.getAttr(target_node + '.' + target_attr, t=frame)

    in_angle = cmds.keyTangent(
        target_node + '.' + target_attr,
        q=True,
        t=(frame, frame),
        inAngle=True)

    out_angle = cmds.keyTangent(
        target_node + '.' + target_attr,
        q=True,
        t=(frame, frame),
        outAngle=True)

    in_type = cmds.keyTangent(
        target_node + '.' + target_attr,
        q=True,
        t=(frame, frame),
        inTangentType=True)

    out_type = cmds.keyTangent(
        target_node + '.' + target_attr,
        q=True,
        t=(frame, frame),
        outTangentType=True)

    lock = cmds.keyTangent(
        target_node + '.' + target_attr, q=True, t=(frame, frame), lock=True)

    in_weight = cmds.keyTangent(
        target_node + '.' + target_attr,
        q=True,
        t=(frame, frame),
        inWeight=True)

    out_weight = cmds.keyTangent(
        target_node + '.' + target_attr,
        q=True,
        t=(frame, frame),
        outWeight=True)

    weight_lock = cmds.keyTangent(
        target_node + '.' + target_attr,
        q=True,
        t=(frame, frame),
        weightLock=True)

    if in_angle:
        in_angle = in_angle[0]

    if out_angle:
        out_angle = out_angle[0]

    if in_type:
        in_type = in_type[0]

    if out_type:
        out_type = out_type[0]

    if lock:
        lock = lock[0]

    if in_weight:
        in_weight = in_weight[0]

    if out_weight:
        out_weight = out_weight[0]

    if weight_lock:
        weight_lock = weight_lock[0]

    result_info = {}

    result_info['frame'] = frame
    result_info['value'] = value
    result_info['inAngle'] = in_angle
    result_info['outAngle'] = out_angle
    result_info['inType'] = in_type
    result_info['outType'] = out_type
    result_info['lock'] = lock
    result_info['inWeight'] = in_weight
    result_info['outWeight'] = out_weight
    result_info['weightLock'] = weight_lock

    return result_info


# ==================================================
def set_key_info_list(target_node, target_attr, key_info_list):

    if not exists(target_node, target_attr):
        return

    if not key_info_list:
        return

    for key_info in key_info_list:

        set_key_info(target_node, target_attr, key_info)


# ==================================================
def set_key_info(target_node, target_attr, key_info):

    if not exists(target_node, target_attr):
        return

    if not key_info:
        return

    if type(key_info) != dict:
        return

    frame = None
    value = None
    in_angle = None
    out_angle = None
    in_type = None
    out_type = None
    lock = None
    in_weight = None
    out_weight = None
    weight_lock = None

    if 'frame' in key_info:
        frame = key_info['frame']

    if 'value' in key_info:
        value = key_info['value']

    if frame is None:
        return

    if value is None:
        return

    if 'inAngle' in key_info:
        in_angle = key_info['inAngle']

    if 'outAngle' in key_info:
        out_angle = key_info['outAngle']

    if 'inType' in key_info:
        in_type = key_info['inType']

    if 'outType' in key_info:
        out_type = key_info['outType']

    if 'lock' in key_info:
        lock = key_info['lock']

    if 'inWeight' in key_info:
        in_weight = key_info['inWeight']

    if 'outWeight' in key_info:
        out_weight = key_info['outWeight']

    if 'weightLock' in key_info:
        weight_lock = key_info['weightLock']

    try:
        cmds.setKeyframe(target_node + '.' + target_attr,
                         value=value, time=frame)
    except Exception as e:
        print('{0}'.format(e))

    is_weighted = cmds.keyTangent(
        target_node + '.' + target_attr, q=True, weightedTangents=True)

    if in_type is not None:

        try:
            cmds.keyTangent(
                target_node + '.' + target_attr,
                e=True,
                t=(frame, frame),
                inTangentType=True)
        except Exception as e:
            print('{0}'.format(e))

    if out_type is not None:

        try:
            cmds.keyTangent(
                target_node + '.' + target_attr,
                e=True,
                t=(frame, frame),
                outTangentType=True)
        except Exception as e:
            print('{0}'.format(e))

    if in_angle is not None:

        try:
            cmds.keyTangent(
                target_node + '.' + target_attr,
                e=True,
                t=(frame, frame),
                inAngle=True)
        except Exception as e:
            print('{0}'.format(e))

    if out_angle is not None:

        try:
            cmds.keyTangent(
                target_node + '.' + target_attr,
                e=True,
                t=(frame, frame),
                inAngle=True)
        except Exception as e:
            print('{0}'.format(e))

    if lock is not None:

        try:
            cmds.keyTangent(
                target_node + '.' + target_attr,
                e=True,
                t=(frame, frame),
                lock=True)
        except Exception as e:
            print('{0}'.format(e))

    if in_weight is not None and is_weighted:

        try:
            cmds.keyTangent(
                target_node + '.' + target_attr,
                e=True,
                t=(frame, frame),
                inWeight=True)
        except Exception as e:
            print('{0}'.format(e))

    if out_weight is not None and is_weighted:

        try:
            cmds.keyTangent(
                target_node + '.' + target_attr,
                e=True,
                t=(frame, frame),
                outWeight=True)
        except Exception as e:
            print('{0}'.format(e))

    if weight_lock is not None and is_weighted:

        try:
            cmds.keyTangent(
                target_node + '.' + target_attr,
                e=True,
                t=(frame, frame),
                weightLock=True)
        except Exception as e:
            print('{0}'.format(e))


# ==================================================
def get_lock(target_node, target_attr):
    """
    アトリビュートの値を取得

    :param target_node: ノード
    :param target_attr: アトリビュート

    :return :アトリビュートのロック状態
    """

    if not exists(target_node, target_attr):
        return

    lock = cmds.getAttr(target_node + '.' + target_attr, lock=True)

    return lock


# ==================================================
def set_lock(target_node, target_attr, lock):
    """
    アトリビュートの値を取得

    :param target_node: ノード
    :param target_attr: アトリビュート
    :param lock: ロック状態
    """

    if not exists(target_node, target_attr):
        return

    try:
        cmds.setAttr(target_node + '.' + target_attr, lock=lock)
    except Exception as e:
        print('{0}'.format(e))


# ==================================================
def connect(src_target, src_attr, dst_target, dst_attr):
    """
    アトリビュートを接続

    :param src_target: 接続元ノード
    :param src_attr: 接続元アトリビュート
    :param dst_target: 接続先ノード
    :param dst_attr: 接続先アトリビュート
    """

    if not exists(src_target, src_attr):
        return

    if not exists(dst_target, dst_attr):
        return

    if cmds.isConnected(src_target + '.' + src_attr,
                        dst_target + '.' + dst_attr):
        return

    try:
        cmds.connectAttr(src_target + '.' + src_attr,
                         dst_target + '.' + dst_attr,
                         force=True)
    except Exception as e:
        print('{0}'.format(e))


# ==================================================
def disconnect(src_target, src_attr, dst_target, dst_attr):
    """
    アトリビュートの接続を解除

    :param src_target: 接続元ノード
    :param src_attr: 接続元アトリビュート
    :param dst_target: 接続先ノード
    :param dst_attr: 接続先アトリビュート
    """

    if not exists(src_target, src_attr):
        return

    if not exists(dst_target, dst_attr):
        return

    if not cmds.isConnected(src_target + '.' + src_attr,
                            dst_target + '.' + dst_attr):
        return

    try:
        cmds.disconnectAttr(src_target + '.' + src_attr,
                            dst_target + '.' + dst_attr)
    except Exception as e:
        print('{0}'.format(e))


# ==================================================
def get_input_attr_list(target_node, target_attr):
    """
    接続している入力アトリビュートリストを取得

    :param target_node: ノード
    :param target_attr: アトリビュート
    """

    if not exists(target_node, target_attr):
        return

    connect_list = \
        cmds.listConnections(
            target_node + '.' + target_attr, p=True, s=True, d=False)

    if not connect_list:
        return

    return connect_list


# ==================================================
def get_output_attr_list(target_node, target_attr):
    """
    接続している出力アトリビュートリストを取得

    :param target_node: ノード
    :param target_attr: アトリビュート
    """

    if not exists(target_node, target_attr):
        return

    connect_list = \
        cmds.listConnections(
            target_node + '.' + target_attr, p=True, s=False, d=True)

    if not connect_list:
        return

    return connect_list


# ==================================================
def disconnect_all_input_attr(target_node, target_attr):
    """
    全ての接続している入力アトリビュートを解除

    :param target_node: ノード
    :param target_attr: アトリビュート
    """

    if not exists(target_node, target_attr):
        return

    connect_attr_list = get_input_attr_list(
        target_node, target_attr
    )

    if not connect_attr_list:
        return

    for connect_attr in connect_attr_list:

        try:
            cmds.disconnectAttr(
                connect_attr,
                target_node + '.' + target_attr
            )
        except Exception as e:
            print('{0}'.format(e))


# ==================================================
def disconnect_all_output_attr(target_node, target_attr):
    """
    全ての接続している出力アトリビュートを解除

    :param target_node: ノード
    :param target_attr: アトリビュート
    """

    if not exists(target_node, target_attr):
        return

    connect_attr_list = get_output_attr_list(
        target_node, target_attr
    )

    if not connect_attr_list:
        return

    for connect_attr in connect_attr_list:

        try:
            cmds.disconnectAttr(
                target_node + '.' + target_attr,
                connect_attr
            )
        except Exception as e:
            print('{0}'.format(e))


# ==================================================
def disconnect_all(target_node, target_attr):
    """全ての接続を解除

    :param target_node: ノード
    :param target_attr: アトリビュート
    """

    if not exists(target_node, target_attr):
        return

    disconnect_all_input_attr(target_node, target_attr)
    disconnect_all_output_attr(target_node, target_attr)
