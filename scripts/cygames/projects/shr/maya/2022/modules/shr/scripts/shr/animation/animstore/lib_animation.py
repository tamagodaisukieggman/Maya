# -*- coding: utf-8 -*-

from __future__ import absolute_import

from collections import OrderedDict
import logging
import traceback

import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

from .const import ANIM_CURVE_U, ANIM_CURVE_T, ANIM_CURVE_TANGENT_TYPES, TRANSFORMATION_CHANNELS, KEY_TANGENT_FLAGS

from . import lib_maya
from . import lib_util
from . import lib_file

CRV_ATTRS = {
    'tangentType': '{}.tangentType',
    'preInfinity': '{}.preInfinity',
    'postInfinity': '{}.postInfinity',
    'weightedTangents': '{}.weightedTangents',
    'keyTime': '{}.keyTimeValue[*].keyTime',
    'keyValue': '{}.keyTimeValue[*].keyValue',
    'keyTanLocked': '{}.keyTanLocked[*]',
    'keyWeightLocked': '{}.keyWeightLocked[*]',
    'keyTanInType': '{}.keyTanInType[*]',
    'keyTanInX': '{}.keyTanInX[*]',
    'keyTanInY': '{}.keyTanInY[*]',
    'keyTanOutType': '{}.keyTanOutType[*]',
    'keyTanOutX': '{}.keyTanOutX[*]',
    'keyTanOutY': '{}.keyTanOutY[*]',
    'keyBreakdown': '{}.keyBreakdown[*]',
}

logger = logging.getLogger(__name__)


class AnimationDataFile(lib_file.PickleFile):
    """
    """

    data_type = 'animationData'

    @classmethod
    def _get_file_infomation(cls):
        ret = OrderedDict()
        ret['file_information'] = OrderedDict()
        ret['file_information']['data_type'] = cls.data_type
        ret['file_information']['user'] = lib_util.get_username()
        ret['file_information']['date'] = lib_util.get_utcnow()
        ret['file_information']['scene'] = lib_maya.get_scene_filepath()
        ret['file_information']['timeunit'] = lib_maya.get_scene_timeunit()
        ret['file_information']['linearunit'] = lib_maya.get_scene_linearunit()
        ret['file_information']['angleunit'] = lib_maya.get_scene_angleunit()

        return ret

    @classmethod
    def write(cls, file_path, data):
        write_data = cls._get_file_infomation()
        write_data.update({'data': data})

        super(AnimationDataFile, cls).write(file_path, write_data)

    @classmethod
    def read(cls, file_path):
        read_data = super(AnimationDataFile, cls).read(file_path)
        return read_data.get('data', {})


def is_valid_curve(crv):
    """有効なカーブかを判断する

    :param str crv: カーブノード名
    :return: 有効なカーブの場合はTrue
    :rtype: bool
    """

    if not cmds.objExists(crv):
        return False

    num_keys = cmds.getAttr('%s.ktv' % crv, s=True)
    if not num_keys:
        return False

    if not cmds.listConnections(crv, s=False, d=True, scn=True):
        return False

    return True


def is_static_channel(plug, attr=None, eps=1e-6):
    """staticChannelか判断する

    :param str plug: プラグ名 or ノード名
    :param str attr: アトリビュート名
    :param float eps: アトリビュートの変化量の閾値
    :return: staticChannelかのブール値
    :rtype: bool
    """

    if '.' in plug:
        pass
    elif attr:
        plug = '{}.{}'.format(plug.split('.', 1)[0], attr)
    else:
        pass
        # return False

    if not cmds.objExists(plug):
        return False

    changed = cmds.keyframe(plug, q=True, vc=True)
    if changed:
        changed = set(changed)
        if len(changed) == 1:
            return True
        else:
            changed = list(changed)
            for v in changed[1:]:
                if abs(v - changed[0]) > eps:
                    return False
            return True
    else:
        src = cmds.listConnections(plug, s=True, d=False)
        if src:
            return False
        else:
            node, attr = plug.split('.', 1)
            parent_attrs = cmds.attributeQuery(attr, n=node, lp=True)
            if not parent_attrs:
                return True
            else:
                for parent_attr in parent_attrs:
                    parent_plug = '{}.{}'.format(node, parent_attr)
                    if cmds.listConnections(parent_plug, s=True, d=False):
                        return False
                    else:
                        return True


def list_uncurveinput_plugs(plugs):
    """ベイクが必要なプラグを取得
    入力がanimCurveT以外のプラグを取得します。
    :param list plugs: 調査対象のプラグ
    :return: ベイクが必要なプラグ
    :rtype: list
    """

    valid_plugs = [plug for plug in plugs if cmds.objExists(plug)]
    if not valid_plugs:
        return []

    ret = []
    for plug in valid_plugs:
        src = cmds.listConnections(plug, s=True, d=False)
        if not src:
            continue

        if cmds.nodeType(src[0]) not in ANIM_CURVE_T:
            ret.append(plug)

    return ret


def list_keyable_plugs(
        nodes, below=False, channelbox=False, contain_static_channels=True, specify_channels=None):
    """keyaleなプラグを取得
    :param list nodes: ノードのリスト
    :param bool below: 選択階層下のノードをリスト対象に含むかのブール値
    :param bool channelbox: 選択したチャンネルだけをリストに含むかのブール値
    :param bool contain_static_channels: staticチャンネルを含むかのブール値
    :param list specify_channels: 指定チャンネル(アトリビュート)
    :return: keyablePlugのリスト
    :rtype: list
    """

    nodes = nodes or cmds.ls(sl=True)
    if not nodes:
        return []

    if below:
        nodes += cmds.listRelatives(nodes, ad=True, pa=True) or []

    valid_nodes = [node for node in nodes if cmds.objExists(node)]
    if not valid_nodes:
        return []

    plugs = []

    if channelbox:
        sels = cmds.ls(sl=True)
        cmds.select(valid_nodes, r=True)
        plugs = lib_maya.list_selected_channels(keyable=True, locked=False)

        if sels:
            cmds.select(sels, r=True)

    elif specify_channels:
        for node in valid_nodes:
            attrs = specify_channels
            for attr in attrs:
                if not cmds.attributeQuery(attr, n=node, ex=True):
                    continue

                if not cmds.attributeQuery(attr, n=node, ch=True):
                    plugs.append('{}.{}'.format(node, attr))

    else:
        for node in valid_nodes:
            attrs = cmds.listAttr(node, k=True, unlocked=True) or []
            for attr in attrs:
                if not cmds.attributeQuery(attr, n=node, ex=True):
                    continue

                if not cmds.attributeQuery(attr, n=node, ch=True):
                    plugs.append('{}.{}'.format(node, attr))

    if contain_static_channels:
        return plugs
    else:
        return [plug for plug in plugs if not is_static_channel(plug)]


def get_animcurve_data(targets, **kwargs):
    """アニメーションカーブデータを取得
    :param list targets: ノード名 or プラグ名 のリスト
    :return: アニメーションカーブのデータを辞書で取得
    :rtype: dict
    """

    if not targets:
        return

    all_range = kwargs.get('allRange', kwargs.get('ar', False))
    copy_start = kwargs.get('startFrame', kwargs.get('start', None))
    copy_end = kwargs.get('endFrame', kwargs.get('end', None))
    copy_option = kwargs.get('option', kwargs.get('o', 'curve'))

    targets = [targets] if not hasattr(targets, '__iter__') else targets
    valid_targets = [tg for tg in targets if cmds.objExists(tg)]
    if not valid_targets:
        return {}

    copy_time = None
    if not all_range:
        _range = [None, None]
        if copy_start is None:
            _range[0] = cmds.findKeyframe(valid_targets, which='first')
        else:
            _range[0] = copy_start

        if copy_end is None:
            _range[1] = cmds.findKeyframe(valid_targets, which='last')
        else:
            _range[1] = copy_end

        copy_time = tuple(_range)

    ret = {
        'curve_data': {},
        'data_range': copy_time,
        'copy_option': copy_option,
    }

    for tg in valid_targets:
        crvs = cmds.findKeyframe(tg, c=True)
        if not crvs:
            continue

        crvs = cmds.ls(crvs, type=ANIM_CURVE_T)
        if not crvs:
            continue

        crv_data = {}
        for crv in crvs:
            if not is_valid_curve(crv):
                continue

            changed = cmds.keyframe(crv, q=True, vc=True)
            if not changed:
                continue

            crv_data[crv] = {}

            dmy_crv = crv
            if copy_time:
                dmy_crv = cmds.duplicate(crv)[0]
                cmds.copyKey(crv, time=copy_time, option=copy_option)
                cmds.pasteKey(dmy_crv, option='replaceCompletely')

            changed = cmds.keyframe(dmy_crv, q=True, vc=True)
            num_keys = len(changed)
            if num_keys == 1:
                for key, attr in CRV_ATTRS.items():
                    if '*' in attr:
                        crv_data[crv][key] = [cmds.getAttr(attr.format(dmy_crv))]
                    else:
                        crv_data[crv][key] = cmds.getAttr(attr.format(dmy_crv))
            else:
                crv_data[crv] = {key: cmds.getAttr(attr.format(dmy_crv)) for key, attr in CRV_ATTRS.items()}

            for kt_key in KEY_TANGENT_FLAGS:
                key_tangent_options = {'q': True, kt_key: True}
                crv_data[crv][kt_key] = cmds.keyTangent(dmy_crv, **key_tangent_options)

            if dmy_crv != crv:
                cmds.delete(dmy_crv)

            crv_data[crv].update({
                'name': crv,
                'nodeType': cmds.nodeType(crv),
                'plug': lib_maya.get_plug_longname(tg),
            })

        if crv_data:
            ret['curve_data'][tg] = crv_data

    ret['data_range'] = ret['data_range'] or lib_maya.get_animcurve_timerange(ret['curve_data'].keys())

    return ret


def set_animcurve_data(data, **kwargs):
    """データを元にドリブンキーを設定
    :param dict data: アニメーションカーブデータ
    :return: ペーストに成功したプラグのリスト
    :rtype: list
    """

    if not data:
        return

    curve_data = data.get('curve_data', {})
    data_range = data.get('data_range', None)
    # data_copy_option = data.get('copy_option', 'curve')

    # paste target
    target_nodes = kwargs.get('targetNodes', [])
    target_plugs = kwargs.get('targetPlugs', [])
    target_channels = kwargs.get('targetChannels', [])
    target_namespace = kwargs.get('namespace', '')

    source_time_offset = kwargs.get('sourceTimeOffset', kwargs.get('sto', 0))
    source_value_offset = kwargs.get('sourceValueOffset', kwargs.get('svo', 0))
    source_time_zero_start = kwargs.get('sourceTimeZeroStart', kwargs.get('stzs', False))

    paste_inside_breakdown = kwargs.get('breakdown', False)
    remove_breakdown = kwargs.get('removeBreakdown', False)

    connect = kwargs.get('connect', False)

    # 'startEnd' or 'inputData'
    copy_range_type = kwargs.get('copyRangeType', kwargs.get('crt', 'inputData'))
    # 'keys' or 'curve'
    copy_option = kwargs.get('copyOption', kwargs.get('co', 'curve'))
    copy_start = kwargs.get('copyStartFrame', kwargs.get('csf', None))
    copy_end = kwargs.get('copyEndFrame', kwargs.get('cef', None))

    if copy_range_type == 'inputData':
        copy_start, copy_end = data_range

    if source_time_zero_start:
        source_time_offset -= data_range[0]

    paste_time = kwargs.get('time', kwargs.get('t', None))

    # insert, replace, replaceCompletely, merge, scaleInsert, scaleReplace, scaleMerge, fitInsert, fitReplace, fitMerge
    paste_option = kwargs.get('option', kwargs.get('o', 'replaceCompletely'))

    paste_time_offset = kwargs.get('timeOffset', kwargs.get('to', 0))
    paste_value_offset = kwargs.get('valueOffset', kwargs.get('vo', 0))
    copies = kwargs.get('copies', kwargs.get('cp', 1))

    paste_options = {
        'option': paste_option,
        'timeOffset': paste_time_offset,
        'valueOffset': paste_value_offset,
        'copies': copies,
        'connect': connect,
    }

    if paste_time is not None:
        paste_options['time'] = tuple(paste_time)

    breakdown_start = paste_time[0]
    breakdown_end = paste_time[1] if len(paste_time) > 1 else paste_time[0] + data_range[1] - data_range[0]

    pasted_plugs = []

    for values in curve_data.values():
        for crv_name, crv_data in values.items():
            try:
                plug = crv_data['plug']
                obj, attr = plug.split('.', 1)

                object_name = lib_maya.get_object_uniquename(plug)
                if target_namespace:
                    plug = '{}.{}'.format(lib_maya.add_namespace(object_name, target_namespace), attr)
                    obj = lib_maya.add_namespace(object_name, target_namespace)

                if target_channels:
                    check_plugs = ['{}.{}'.format(plug.split('.', 1)[0], channel) for channel in target_channels]
                    if plug not in check_plugs:
                        continue

                if target_plugs and plug not in target_plugs:
                    continue

                if target_nodes and obj not in target_nodes:
                    continue

                if not cmds.objExists(plug):
                    continue

                crvs = cmds.findKeyframe(plug, c=True) or []

                u_crvs = cmds.ls(crvs, type=ANIM_CURVE_U)
                # drivenKeyが設定されている場合
                if u_crvs:
                    continue

                t_crvs = cmds.ls(crvs, type=ANIM_CURVE_T)
                if t_crvs:
                    # カーブがリファレンスデータの場合
                    if cmds.referenceQuery(t_crvs[0], isNodeReferenced=True):
                        continue

                # カーブ削除
                # cmds.cutKey(plug)

                new_crv = create_animcurve_from_crvdata(crv_data)
                if remove_breakdown:
                    cmds.keyframe(new_crv, time=(data_range[0], data_range[1]), breakdown=False)

                if source_time_offset != 0 or source_value_offset != 0:
                    cmds.keyframe(new_crv,
                                  timeChange=source_time_offset,
                                  valueChange=source_value_offset,
                                  relative=True)

                num_copy_keys = cmds.copyKey(
                    new_crv, option=copy_option,
                    time=(copy_start + source_time_offset, copy_end + source_time_offset))

                if not num_copy_keys:
                    cmds.warning('Failed copyKey : {}'.format(new_crv))

                cmds.delete(new_crv)

                logger.debug('Paste Plug : {}'.format(plug))

                try:
                    num_paste_keys = cmds.pasteKey(plug, **paste_options)
                except Exception as e:
                    cmds.setKeyframe(plug, t=paste_time[0])
                    num_paste_keys = cmds.pasteKey(plug, **paste_options)

                if not num_paste_keys:
                    cmds.warning('Failed pasteKey : {}'.format(plug))
                    continue

                if paste_inside_breakdown:
                    start_inside = cmds.findKeyframe(plug, which='next', t=(breakdown_start, breakdown_start))
                    out_inside = cmds.findKeyframe(plug, which='previous', t=(breakdown_end, breakdown_end))
                    cmds.keyframe(plug, e=True, breakdown=True, time=(start_inside, out_inside))

                pasted_plugs.append(plug)

            except Exception as e:
                traceback.print_exc()
                cmds.warning(str(e))

    return pasted_plugs


def select_nodes_from_animcurve_data(data, namespaces=None):
    """データからノードを選択
    :param dict data: アニメーションカーブデータ
    :param list namespaces: 入れ替えるネームスペース
    """

    if not data:
        return

    plugs = data.get('curve_data', {}).keys()
    if not plugs:
        return

    nodes = [plug.split('.', 1)[0] for plug in plugs]
    if not nodes:
        return

    if namespaces:
        ns_nodes = []
        for namespace in namespaces:
            ns_nodes += [lib_maya.replace_namespace(node, namespace) for node in nodes]

        nodes = ns_nodes

    exist_nodes = [node for node in nodes if cmds.objExists(node)]
    if exist_nodes:
        cmds.select(exist_nodes, r=True)


def create_animcurve_from_crvdata(crv_data):
    """カーブデータからanimCurveU?ノードを作成
    :param dict crv_data: animCurveデータの辞書
    :return: animCurveノード名
    :rtype: str
    """

    if not crv_data:
        return ''

    num_keys = len(crv_data['keyTime'])
    if not num_keys:
        return ''

    cmds.keyTangent(g=True, weightedTangents=True)

    crv = cmds.createNode(crv_data['nodeType'], n=crv_data['name'], ss=True)
    cmds.setAttr('{}.preInfinity'.format(crv), crv_data['preInfinity'])
    cmds.setAttr('{}.postInfinity'.format(crv), crv_data['postInfinity'])
    cmds.keyTangent(crv, weightedTangents=crv_data['weightedTangents'])

    for t, v, bd, in zip(crv_data['keyTime'], crv_data['keyValue'], crv_data['keyBreakdown']):
        cmds.setKeyframe(crv, t=t, v=v, bd=bd)

    for key_index in range(num_keys):
        cmds.keyTangent(crv, e=True,
                        # f=(crv_data['keyTime'][key_index], crv_data['keyTime'][key_index]),
                        index=(key_index,),
                        lock=crv_data['keyTanLocked'][key_index])
        cmds.keyTangent(crv, e=True,
                        # f=(crv_data['keyTime'][key_index], crv_data['keyTime'][key_index]),
                        index=(key_index,),
                        inWeight=crv_data['inWeight'][key_index],
                        outWeight=crv_data['outWeight'][key_index],
                        inAngle=crv_data['inAngle'][key_index],
                        outAngle=crv_data['outAngle'][key_index],
                        )
        cmds.keyTangent(crv, e=True,
                        # f=(crv_data['keyTime'][key_index], crv_data['keyTime'][key_index]),
                        index=(key_index,),
                        itt=ANIM_CURVE_TANGENT_TYPES[crv_data['keyTanInType'][key_index]],
                        ott=ANIM_CURVE_TANGENT_TYPES[crv_data['keyTanOutType'][key_index]],
                        )

    return crv


def get_animcurve_nodetype(plug, time_type=True):
    """プラグに接続されるanimCurveのタイプを取得
    :param str plug: プラグ名
    :param bool time_type:
        True: animCurveTタイプのanimCurveノードタイプを取得
        False: animCurveUタイプのanimCurveノードタイプを取得
    :return: animCurveノードタイプ名
    :rtype: str
    """

    if not cmds.objExists(plug):
        return ''

    time_or_unitless = 'animCurveT' if time_type else 'animCurveU'

    attr_type = cmds.getAttr(plug, type=True)
    if attr_type == 'doubleLinear':
        return '{}L'.format(time_or_unitless)
    elif attr_type == 'doubleAngle':
        return '{}A'.format(time_or_unitless)
    elif attr_type == 'time':
        return '{}T'.format(time_or_unitless)
    else:
        return '{}U'.format(time_or_unitless)


def bake_animation(plugs, **kwargs):
    """ベイクアニメーション

    :param list plugs: ベイク対象のプラグリスト
    :param bool allRange:
    :param float start:
    :param float end:
    :param float sampleBy:
    :param float overSample:
    :param str tangent:
    :param bool eulerFilter:
    :param bool deleteStaticChannels:
    :param bool preserveOutsideKeys:
    :param bool suspendRefresh:
    """

    if not plugs:
        return

    plugs = [plugs] if not hasattr(plugs, '__iter__') else plugs
    valid_plugs = [plug for plug in plugs if cmds.objExists(plug) and (not cmds.getAttr(plug, lock=True))]
    if not valid_plugs:
        return

    all_renge = kwargs.get('allRange', False)
    start_frame = kwargs.get('start', None)
    end_frame = kwargs.get('end', None)
    sample_by = kwargs.get('sampleBy', 1.0)
    over_sample = kwargs.get('overSample', 0.0)
    key_tangent = kwargs.get('tangent', None)
    euler_filter = kwargs.get('eulerFilter', True)
    delete_static_channels = kwargs.get('deleteStaticChannels', False)
    preserve_outside_keys = kwargs.get('preserveOutsideKeys', True)
    suspend_refresh = kwargs.get('suspendRefresh', True)
    curve_range = lib_maya.get_animcurve_timerange(valid_plugs)
    slider_range = lib_maya.get_timeslider_timerange()

    if start_frame is None:
        start_frame = curve_range[0] if all_renge else slider_range[0]

    if end_frame is None:
        end_frame = curve_range[1] if all_renge else slider_range[1]

    itt = ott = 'auto'
    if key_tangent is None:
        itt = cmds.keyTangent(q=1, g=1, itt=1)[0]
        ott = cmds.keyTangent(q=1, g=1, ott=1)[0]
    else:
        tangent_types = [typ.lower() for typ in ANIM_CURVE_TANGENT_TYPES.values()]
        if key_tangent.lower() in tangent_types:
            itt = ott = key_tangent

    if start_frame > end_frame:
        start_frame, end_frame = end_frame, start_frame

    # logger.debug('Bake Animation: {}'.format(str(kwargs)))

    current_time = cmds.currentTime(q=True)

    cmds.waitCursor(state=True)

    if suspend_refresh:
        cmds.refresh(suspend=True)

    start = start_frame - over_sample
    end = end_frame + over_sample + sample_by * 0.25

    try:
        # 2016以前の場合は自前ベイク
        if lib_maya.get_maya_version() < 201600:
            cur_time = start
            plug_values = []
            key_times = []
            while cur_time <= end:
                cmds.undoInfo(stateWithoutFlush=False)

                # currentTimeを移動して値を取得
                OpenMaya.MGlobal.executeCommand('currentTime {}'.format(cur_time), False, False)
                cmds.dgdirty(valid_plugs)
                cmds.dgeval(valid_plugs)
                plug_values.append([cmds.getAttr(plug) for plug in valid_plugs])

                # # getAttr で timeを指定して値を取得
                # plug_values.append([cmds.getAttr(plug, time=cur_time) for plug in valid_plugs])

                key_times.append(cur_time)
                cur_time += sample_by

                cmds.undoInfo(stateWithoutFlush=True)

            crvs = []
            for plug_index, plug in enumerate(valid_plugs):
                crv = ''

                src_plug = cmds.listConnections(plug, s=1, d=0, p=1)
                if src_plug:
                    src_plug = src_plug[0]
                    src_node = src_plug.split('.', 1)[0]
                    if preserve_outside_keys and cmds.nodeType(src_node).startswith('animCurveT'):
                        if not cmds.referenceQuery(src_node, isNodeReferenced=True):
                            crv = src_node

                    cmds.disconnectAttr(src_plug, plug)

                    if cmds.objExists(crv):
                        cmds.cutKey(crv, time=(start, end))

                create_new_crv = False
                if not cmds.objExists(crv):
                    crv_type = get_animcurve_nodetype(plug)
                    crv = cmds.createNode(crv_type, ss=True)
                    create_new_crv = True

                if create_new_crv:
                    cmds.undoInfo(stateWithoutFlush=False)

                for key_index, key_time in enumerate(key_times):
                    cmds.setKeyframe(crv, v=plug_values[key_index][plug_index], time=key_time)

                if create_new_crv:
                    cmds.undoInfo(stateWithoutFlush=True)

                cmds.connectAttr('{}.output'.format(crv), plug, f=True)
                crvs.append(crv)
        else:
            cmds.bakeResults(valid_plugs,
                             simulation=True,
                             time=(start, end),
                             sampleBy=sample_by,
                             oversamplingRate=1,
                             disableImplicitControl=False,
                             preserveOutsideKeys=True,
                             sparseAnimCurveBake=False,
                             removeBakedAttributeFromLayer=True,
                             removeBakedAnimFromLayer=True,
                             bakeOnOverrideLayer=False,
                             minimizeRotation=False,
                             controlPoints=False,
                             shape=True,
                             )
            crvs = cmds.findKeyframe(valid_plugs, c=True)

        if crvs:
            cmds.keyTangent(crvs, e=1, itt=itt, ott=ott, time=(start, end))

            if euler_filter:
                cmds.filterCurve(crvs)

            if delete_static_channels:
                cmds.dgdirty(valid_plugs)
                cmds.dgeval(valid_plugs)
                cmds.delete(valid_plugs, sc=True, tac=True)
                OpenMaya.MGlobal.executeCommand('currentTime {}'.format(start_frame), False, False)
                cmds.dgdirty(valid_plugs)
                cmds.dgeval(valid_plugs)
                cmds.setKeyframe(valid_plugs)

    except Exception as e:
        traceback.print_exc()
        cmds.error('Failed bake animation.')

    finally:
        if suspend_refresh:
            cmds.refresh(suspend=False)

        cmds.waitCursor(state=False)

        cmds.currentTime(current_time)
        cmds.dgdirty(valid_plugs)
        cmds.dgeval(valid_plugs)
        # cmds.dgdirty(a=True)


def write_animation(file_path, **kwargs):
    """アニメーションデータの書き出し

    :param str file_path: ファイルパス
    :param str hierarchy: select or below
    :param str channels: all or select or transform
    :param bool contain_static_channels: if true contain static channels
    :param str timerange: all or timeslider or startend
    :param float startframe: startFrame
    :param float endFrame: endFrame
    :param str method: curve or keys
    :param str bakemethod: none or excludecurveinputs or all
    :return: 書き出しに成功した場合はTrue
    :rtype: bool
    """

    sels = cmds.ls(sl=True)
    if not sels:
        cmds.warning('Please select target nodes.')
        return False

    # select or below
    hirarchy = kwargs.get('hirarchy', 'select')
    # all or select or transform
    channels = kwargs.get('channels', 'all')
    contain_static_channels = kwargs.get('contain_static_channels', True)
    # all or timeslider or startend
    timerange = kwargs.get('timerange', 'timeslider')
    startframe = kwargs.get('startframe', 0)
    endframe = kwargs.get('endframe', 1)
    if timerange == 'all':
        startframe = None
        endframe = None
    elif timerange == 'timeslider':
        startframe, endframe = lib_maya.get_timeslider_timerange()
    elif timerange == 'timecontrol':
        startframe, endframe = lib_maya.get_timecontrol_timerange()

    # curve or keys
    method = kwargs.get('method', 'curve')

    # none or excludecurveinput or all
    bakemethod = kwargs.get('bakemethod', 'none')

    # user_channels
    user_channels = TRANSFORMATION_CHANNELS if channels == 'transform' else None

    plugs = list_keyable_plugs(
        [],
        below=hirarchy == 'below',
        channelbox=channels == 'select',
        contain_static_channels=contain_static_channels,
        specify_channels=user_channels
    )

    if not plugs:
        cmds.warning('Copy target not found.')
        return False

    current_time = cmds.currentTime(q=True)

    if bakemethod == 'all':
        bake_animation(
            plugs,
            allRange=timerange == 'all',
            start=startframe,
            end=endframe,
            deleteStaticChannels=False,
        )
    else:
        if bakemethod == 'excludecurveinputs':
            uncurve_input_plugs = list_uncurveinput_plugs(plugs)
            if uncurve_input_plugs:
                bake_animation(
                    uncurve_input_plugs,
                    allRange=timerange == 'all',
                    start=startframe,
                    end=endframe,
                    deleteStaticChannels=False,
                )

        if contain_static_channels:
            static_plugs = [plug for plug in plugs if is_static_channel(plug)]
            if static_plugs:
                OpenMaya.MGlobal.executeCommand(
                    'currentTime {}'.format(startframe or lib_maya.get_timeslider_timerange()[0]), False, False)
                cmds.dgdirty(static_plugs)
                cmds.dgeval(static_plugs)
                cmds.setKeyframe(static_plugs)

    OpenMaya.MGlobal.executeCommand('currentTime {}'.format(current_time), False, False)

    cmds.undoInfo(swf=False)
    data = get_animcurve_data(
        plugs,
        allRange=timerange == 'all',
        start=startframe,
        end=endframe,
        o=method
    )
    cmds.undoInfo(swf=True)

    if not data.get('curve_data', {}):
        cmds.warning('Copy target not found.')
        return False

    try:
        AnimationDataFile.write(file_path, data)
        logger.info('Success copy animation. : {}'.format(file_path))

    except Exception as e:
        traceback.print_exc()
        cmds.error('Failed copy animation.')
        return False

    return True


def read_animation(file_path, **kwargs):
    """アニメーションデータの読み込み

    :param str file_path: ファイルパス
    :param crv_data data: カーブデータ
    :param str tareget: all or selecet or below
    :param str channels: all or select or transform
    :param str namespace: original or select or specify
    :param list specify_namespaces:
    :param str timerange: all or timeslider or startend
    :param float startframe: startFrame
    :param float endFrame: endFrame
    :param bool breakdown: ロードしたアニメーションの中間キーをbreakdownに設定
    :param bool connect:
    :return: アニメーションをロードしたプラグ
    :rtype: list
    """

    crv_data = kwargs.get('data', AnimationDataFile.read(file_path))
    if not crv_data:
        cmds.warning('Not found copied data.')
        return

    data_range = crv_data.get('data_range', ())
    if not data_range:
        cmds.warning('\'copy data range\' not found.')
        return

    data_copy_option = crv_data.get('copy_option', 'curve')

    # replacecompletely or replace or insert
    method = kwargs.get('method', 'replacecompletely')

    # all or select or below
    target = kwargs.get('target', 'all')

    # all or select or transform
    channels = kwargs.get('channels', 'all')

    # original or select
    target_namespace = kwargs.get('namespace', 'select')

    specify_namespaces = kwargs.get('spacify_namespaces', [])

    # current or start or startend or timeslider or timecontrol or sourcedata
    timerange = kwargs.get('timerange', 'timeslider')

    startframe = kwargs.get('startframe', 0)
    endframe = kwargs.get('endframe', 1)

    breakdown = kwargs.get('breakdown', False)
    removeBreakdown = kwargs.get('removeBreakdown', True)

    connect = kwargs.get('connect', False)

    paste_time = None

    copy_start, copy_end = data_range
    if method == 'replacecompletely':
        method = 'replaceCompletely'
        paste_time = (copy_start, )

    else:
        if timerange == 'current':
            current_time = cmds.currentTime(q=True)
            if method == 'insert':
                paste_time = (current_time,)
            else:
                paste_time = (current_time, current_time + data_range[1] - data_range[0])
        elif timerange == 'start':
            if method == 'insert':
                paste_time = (startframe, )
            else:
                paste_time = (startframe, startframe + data_range[1] - data_range[0])
        elif timerange == 'startend':
            paste_time = (startframe, endframe)
        elif timerange == 'timeslider':
            paste_time = lib_maya.get_timeslider_timerange()
        elif timerange == 'timecontrol':
            paste_time = lib_maya.get_timecontrol_timerange()
        elif timerange == 'sourcedata':
            paste_time = data_range
        if timerange not in ['current', 'start']:
            method = 'scale{}'.format(method.title())

    sels = cmds.ls(sl=True)
    nodes = sels
    if target == 'below':
        nodes += cmds.listRelatives(nodes, ad=True, pa=True) or []
    valid_nodes = [node for node in nodes if cmds.objExists(node)]
    paste_nodes = [] if target == 'all' else valid_nodes

    valid_channels = []
    if channels == 'transform':
        valid_channels = TRANSFORMATION_CHANNELS

    elif channels == 'select':
        selected_plugs = lib_maya.list_selected_channels(keyable=True, locked=False)
        valid_channels = list(set([plug.split('.', 1)[1] for plug in selected_plugs if '.' in plug]))

    paste_channels = []
    if channels != 'all':
        if not valid_channels:
            cmds.warning('Please select mainChannelBox attributes.')
            return

        paste_channels = valid_channels

    paste_plugs = []

    paste_namespaces = []
    if target_namespace == 'select':
        if sels:
            paste_namespaces = list(set([
                lib_maya.get_object_namespace(sel) for sel in sels
            ]))

    elif target_namespace == 'specify':
        paste_namespaces = [namespace for namespace in specify_namespaces if cmds.namespace(ex=namespace)]

    if not paste_namespaces:
        paste_namespaces.append('')

    pasted_plugs = []

    for paste_namespace in paste_namespaces:
        set_animcurve_data_options = {
            'option': method,
            'time': paste_time,
            'copyOption': data_copy_option,
            'copyStartFrame': copy_start,
            'copyEndFrame': copy_end,
            'targetNodes': paste_nodes,
            'targetPlugs': paste_plugs,
            'targetChannels': paste_channels,
            'namespace': paste_namespace,
            'breakdown': breakdown,
            'removeBreakdown': removeBreakdown,
            'connect': connect,
        }

        logger.debug('set_animcurve_data({})'.format(
            ', '.join('{!s}={!r}'.format(k, v) for k, v in set_animcurve_data_options.items())))

        try:
            pasted = set_animcurve_data(
                crv_data, **set_animcurve_data_options)

            if pasted:
                logger.info('Read Animation : {} : {} plugs.'.format(paste_namespace, len(pasted)))
                pasted_plugs += pasted

        except Exception as e:
            pass

    return pasted_plugs
