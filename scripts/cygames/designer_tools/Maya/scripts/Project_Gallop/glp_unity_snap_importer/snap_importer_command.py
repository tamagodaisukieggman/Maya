# -*- coding: utf-8 -*-
u"""
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from importlib import reload
except Exception:
    pass

import math

import maya.cmds as cmds
import maya.api.OpenMaya as om

from . import unity_snap_data
from . import const


reload(unity_snap_data)
reload(const)


def import_local_snap_data(snap_data, mapping_data, frame_index, force_apply=False):
    """ローカルのトランスフォーム値を読み込む

    Args:
        snap_data (unity_snap_data.UnitySnapData): 記録データ
        mapping_data (obj_mapping_data.ObjMappingData): シーンとのマッピング情報
        frame_index (int): 読み込むフレーム
        force_apply (bool, optional): オプションフラグに関わらず強制適用（復元時などに使用）. Defaults to False.
    """

    itr = snap_data.generate_obj_info_iterator(frame_index)

    # snapデータをイテレーターで走査
    for obj_name, obj_type, grp_id, is_root, attr_label, snap_val in itr:

        # シーン上のオブジェクトの取得
        maya_obj, parent_obj, opt_flags = mapping_data.get_mapping_info(grp_id, obj_name)
        if not maya_obj or not cmds.objExists(maya_obj):
            continue

        target_attr = const.ALL_OBJ_ATTR_DICT[attr_label]

        # posの処理
        if attr_label == const.ATTR_LOCAL_POS_KEY:
            if not force_apply and is_root and const.FLAG_ROOT_TRANS not in opt_flags:
                continue

            chara_light = const.FLAG_USE_CHAR_LIGHT in opt_flags
            position(maya_obj, obj_type, snap_val=snap_val, use_char_light=chara_light, ws=False)
            continue

        # rotの処理
        if attr_label == const.ATTR_LOCAL_ROT_KEY:
            if not force_apply and is_root and const.FLAG_ROOT_ROT not in opt_flags:
                continue

            chara_light = const.FLAG_USE_CHAR_LIGHT in opt_flags
            rotate(maya_obj, parent_obj, obj_type, snap_val=snap_val, use_char_light=chara_light, ws=False)
            continue

        # scaleの処理
        if attr_label == const.ATTR_LOCAL_SCALE_KEY:
            if not force_apply and is_root and const.FLAG_ROOT_SCALE not in opt_flags:
                continue

            scale(maya_obj, snap_val)
            continue

        # マテリアルの処理
        if obj_type == const.TYPE_CHARA_MATERIAL:
            if attr_label == const.ATTR_USE_ORG_LIGHT_KEY:

                if not force_apply and const.FLAG_USE_ORG_LIGHT not in opt_flags:
                    continue

            if attr_label == const.ATTR_ORG_LIGHT_DIR_KEY:
                if not force_apply and const.FLAG_USE_ORG_LIGHT not in opt_flags:
                    continue

            material_param(maya_obj, target_attr, snap_val)

        # カメラの処理
        if obj_type == const.TYPE_CAMERA:
            if attr_label == const.ATTR_CAM_FOV_KEY:
                camera_param(maya_obj, snap_val)


def import_world_transform_to_root(snap_data, mapping_data, frame_index):
    """rootのワールドトランスフォーム値を読み込む

    Args:
        snap_data (unity_snap_data.UnitySnapData): 記録データ
        mapping_data (obj_mapping_data.ObjMappingData): シーンとのマッピング情報
        frame_index (int): 読み込むフレーム
    """

    itr = snap_data.generate_obj_info_iterator(frame_index)

    # snapデータをイテレーターで走査
    for obj_name, obj_type, grp_id, is_root, attr_label, snap_val in itr:

        # シーン上のオブジェクトの取得
        root_obj, parent_obj, opt_flags = mapping_data.get_mapping_info(grp_id, obj_name)
        if not root_obj or not cmds.objExists(root_obj):
            continue

        # このイテレーション内容の確認
        is_root = is_root
        is_trans = (attr_label == const.ATTR_WORLD_POS_KEY)
        is_rot = (attr_label == const.ATTR_WORLD_ROT_KEY)
        is_scale = (attr_label == const.ATTR_WORLD_SCALE_KEY)
        use_char_light = (const.FLAG_USE_CHAR_LIGHT in opt_flags)

        # 適用確認
        if not is_root:
            continue

        if is_trans and const.FLAG_ROOT_TRANS not in opt_flags:
            continue
        if is_rot and const.FLAG_ROOT_ROT not in opt_flags:
            continue
        if is_scale and const.FLAG_ROOT_SCALE not in opt_flags:
            continue

        # 移動
        if is_trans:
            position(root_obj, obj_type, snap_val=snap_val, use_char_light=use_char_light, ws=True)

        # 回転
        if is_rot:
            rotate(root_obj, parent_obj, obj_type, snap_val=snap_val, use_char_light=use_char_light, ws=True)

        # スケール
        if is_scale:
            scale(root_obj, snap_val=snap_val)


def import_axis_transform_to_root(snap_data, mapping_data, frame_index):
    """rootの基準オブジェクト座標系のトランスフォーム値を読み込む

    Args:
        snap_data (unity_snap_data.UnitySnapData): 記録データ
        mapping_data (obj_mapping_data.ObjMappingData): シーンとのマッピング情報
        frame_index (int): 読み込むフレーム
    """

    axis_obj = mapping_data.get_axis_obj_path()
    axis_rot_attr = snap_data.get_axis_obj_attr(frame_index, const.QUAT_DATA_LIST_KEY, const.ATTR_WORLD_ROT_KEY)
    axis_pos_attr = snap_data.get_axis_obj_attr(frame_index, const.VEC3_DATA_LIST_KEY, const.ATTR_WORLD_POS_KEY)
    axis_scale_attr = snap_data.get_axis_obj_attr(frame_index, const.VEC3_DATA_LIST_KEY, const.ATTR_WORLD_SCALE_KEY)

    if not axis_obj:
        return

    itr = snap_data.generate_obj_info_iterator(frame_index)

    # snapデータをイテレーターで走査
    for obj_name, obj_type, grp_id, is_root, attr_label, snap_val in itr:

        # シーン上のオブジェクトの取得
        root_obj, parent_obj, opt_flags = mapping_data.get_mapping_info(grp_id, obj_name)
        if not root_obj or not cmds.objExists(root_obj):
            continue

        # このイテレーション内容の確認
        is_root = is_root
        is_trans = (attr_label == const.ATTR_WORLD_POS_KEY)
        is_rot = (attr_label == const.ATTR_WORLD_ROT_KEY)
        is_scale = (attr_label == const.ATTR_WORLD_SCALE_KEY)
        use_char_light = (const.FLAG_USE_CHAR_LIGHT in opt_flags)

        # 適用確認
        if not is_root:
            continue

        if is_trans and const.FLAG_ROOT_TRANS not in opt_flags:
            continue
        if is_rot and const.FLAG_ROOT_ROT not in opt_flags:
            continue
        if is_scale and const.FLAG_ROOT_SCALE not in opt_flags:
            continue

        # 移動
        if is_trans and axis_pos_attr:

            if obj_type == const.TYPE_LIGHT and use_char_light:
                continue  # キャラライトはローテーションで扱うので触らない

            root_pos = [
                snap_val['x'] * const.MAYA_TRANS_SCALE * -1,
                snap_val['y'] * const.MAYA_TRANS_SCALE,
                snap_val['z'] * const.MAYA_TRANS_SCALE
            ]  # X反転

            axis_pos = [
                axis_pos_attr['x'] * const.MAYA_TRANS_SCALE * -1,
                axis_pos_attr['y'] * const.MAYA_TRANS_SCALE,
                axis_pos_attr['z'] * const.MAYA_TRANS_SCALE
            ]  # X反転

            # 基準オブジェクトのローカル座標を計算
            unity_a_to_r = [x - y for x, y in zip(root_pos, axis_pos)]
            unity_a_to_r_quat = om.MQuaternion([unity_a_to_r[0], unity_a_to_r[1], unity_a_to_r[2], 0])
            unity_axis_quat = om.MQuaternion([axis_rot_attr['x'], axis_rot_attr['y'] * -1, axis_rot_attr['z'] * -1, axis_rot_attr['w']])
            local_a_to_r_quat = unity_axis_quat * unity_a_to_r_quat * unity_axis_quat.inverse()

            # Maya上でのワールド座標を計算
            axis_obj_pos = cmds.xform(axis_obj, q=True, t=True, ws=True)

            maya_axis_euler = cmds.xform(axis_obj, q=True, ro=True, ws=True)
            maya_axis_euler = om.MEulerRotation([math.radians(x) for x in maya_axis_euler])
            maya_axis_quat = maya_axis_euler.asQuaternion()
            maya_a_to_r_quat = maya_axis_quat.inverse() * local_a_to_r_quat * maya_axis_quat

            root_obj_pos = [axis_obj_pos[0] + maya_a_to_r_quat[0], axis_obj_pos[1] + maya_a_to_r_quat[1], axis_obj_pos[2] + maya_a_to_r_quat[2]]

            # 移動
            cmds.xform(root_obj, t=root_obj_pos, a=True, ws=True)

        # 回転
        if is_rot and axis_rot_attr:

            unity_root_quat = om.MQuaternion([snap_val['x'], snap_val['y'] * -1, snap_val['z'] * -1, snap_val['w']])
            unity_axis_quat = om.MQuaternion([axis_rot_attr['x'], axis_rot_attr['y'] * -1, axis_rot_attr['z'] * -1, axis_rot_attr['w']])
            axis_rot_quat = unity_root_quat * unity_axis_quat.inverse()

            maya_axis_euler = cmds.xform(axis_obj, q=True, ro=True, ws=True)
            maya_axis_euler = om.MEulerRotation([math.radians(x) for x in maya_axis_euler])
            maya_axis_quat = maya_axis_euler.asQuaternion()

            maya_root_quat = axis_rot_quat * maya_axis_quat
            maya_root_euler = maya_root_quat.asEulerRotation()
            maya_root_euler = [math.degrees(x) for x in maya_root_euler]

            if obj_type == const.TYPE_LIGHT and use_char_light:
                cmds.xform(root_obj, t=[0, 0, 0], a=True, ws=True)
                cmds.xform(root_obj, ro=maya_root_euler, a=True, ws=True)
                cmds.xform(root_obj, t=[0, 0, -30], a=True, os=True)  # 原点との位置でライト方向が決まるので適当な値ずらす
            else:
                cmds.xform(root_obj, ro=maya_root_euler, a=True, ws=True)

                if obj_type == const.TYPE_CAMERA:
                    cmds.xform(root_obj, ro=[0, 180, 0], r=True, os=True)  # カメラ反転

        # スケール
        if is_scale and axis_scale_attr:

            root_scale = [snap_val['x'], snap_val['y'], snap_val['z']]
            axis_scale = [axis_scale_attr['x'], axis_scale_attr['y'], axis_scale_attr['z']]
            set_scale = [x * y for x, y in zip(root_scale, axis_scale)]

            cmds.xform(root_obj, s=set_scale)


def save_current_scene_to_snap(base_snap_data, mapping_data):
    """現在のシーンのスナップを保存する
    読み込み解除後に復元できるように、読み込み実行前にスナップを保存する用途で使用する

    Args:
        base_snap_data (unity_snap_data.UnitySnapData): 保存するオブジェクト情報を持っているスナップデータ(=これから読み込むスナップデータ)
        mapping_data (obj_mapping_data.ObjMappingData): シーンとのマッピング情報

    Returns:
        unity_snap_data.UnitySnapData: 現在のシーン情報を格納したスナップデータ
    """

    # base_snap_dataからひな型を作成
    new_data = unity_snap_data.UnitySnapData()
    new_data.init_from_snap_data(base_snap_data)

    # 一度スナップ情報を空にする
    new_data.snap_list = []

    # 1フレだけの記録を作成
    this_snap_data = {
        const.OBJ_DATA_LIST_KEY: [],
        const.AXIS_OBJ_DATA_KEY: {},
        const.SANP_TIME_KEY: 0
    }

    # 復元用なので雑に全部とってくる
    itr = base_snap_data.generate_obj_info_iterator(0)

    # 記録オブジェクト情報を取得
    for obj_name, obj_type, grp_id, is_root, attr_label, snap_val in itr:

        # シーン上のオブジェクトの取得
        maya_obj, parent_obj, opt_flags = mapping_data.get_mapping_info(grp_id, obj_name)
        if not maya_obj or not cmds.objExists(maya_obj):
            continue

        data = None
        if obj_type == const.TYPE_CHARA_MATERIAL:
            data = create_mat_obj_data(obj_name, maya_obj, grp_id, obj_type, is_root)
        else:
            data = create_transform_obj_data(obj_name, maya_obj, grp_id, obj_type, is_root)

        if data:
            this_snap_data[const.OBJ_DATA_LIST_KEY].append(data)

    # axisオブジェクト情報を取得
    axis_maya_path = mapping_data.get_axis_obj_path()
    if axis_maya_path and cmds.objExists(axis_maya_path):
        this_snap_data[const.AXIS_OBJ_DATA_KEY] = create_transform_obj_data(base_snap_data.get_axis_obj_name(), axis_maya_path, -1, const.TYPE_OBJ, True)

    # 記録したスナップデータを登録
    new_data.snap_list.append(this_snap_data)
    new_data.exists = True

    return new_data


def create_transform_obj_data(name, obj, grp_id, type, is_root):
    """トランスフォーム情報を作成

    Args:
        name (str): スナップデータ上のオブジェクト名
        obj (str): Mayaのオブジェクトパス
        root (str): スナップデータ上のオブジェクトルート名
        type (str): オブジェクトタイプ

    Returns:
        dict: スナップデータに記録するトランスフォーム情報dict
    """

    this_data = {
        const.OBJ_NAME_KEY: name,
        const.OBJ_GRP_ID_KEY: grp_id,
        const.OBJ_TYPE_KEY: type,
        const.OBJ_IS_ROOT_KEY: is_root,
        const.FLOAT_DATA_LIST_KEY: [],
        const.VEC3_DATA_LIST_KEY: [],
        const.QUAT_DATA_LIST_KEY: [],
        const.COLOR_DATA_LIST_KEY: []
    }

    # pos
    label = const.ATTR_WORLD_POS_KEY
    val = position(obj, type, q=True, ws=True)
    this_data[const.VEC3_DATA_LIST_KEY].append({const.ATTR_LABEL: label, const.DATA_LABEL: val})

    label = const.ATTR_LOCAL_POS_KEY
    val = position(obj, type, q=True, ws=False)
    this_data[const.VEC3_DATA_LIST_KEY].append({const.ATTR_LABEL: label, const.DATA_LABEL: val})

    # scale
    label = const.ATTR_LOCAL_SCALE_KEY
    val = scale(obj, q=True)
    this_data[const.VEC3_DATA_LIST_KEY].append({const.ATTR_LABEL: label, const.DATA_LABEL: val})

    # world_rot
    if is_root:
        label = const.ATTR_WORLD_ROT_KEY
        val = rotate(obj, None, type, q=True, ws=True)
        this_data[const.QUAT_DATA_LIST_KEY].append({const.ATTR_LABEL: label, const.DATA_LABEL: val})

    # local_rot
    label = const.ATTR_LOCAL_ROT_KEY
    parents = cmds.listRelatives(obj, p=True, f=True)
    parent = parents[0] if parents else None
    val = rotate(obj, parent, type, q=True)
    this_data[const.QUAT_DATA_LIST_KEY].append({const.ATTR_LABEL: label, const.DATA_LABEL: val})

    # camera以外はここまで
    if type != const.TYPE_CAMERA or not cmds.listRelatives(obj, c=True, type='camera'):
        return this_data

    label = const.ATTR_CAM_FOV_KEY
    val = camera_param(obj, q=True)
    this_data[const.FLOAT_DATA_LIST_KEY].append({const.ATTR_LABEL: label, const.DATA_LABEL: val})

    return this_data


def create_mat_obj_data(name, obj, grp_id, type, is_root):
    """マテリアル情報を作成

    Args:
        name (str): スナップデータ上のオブジェクト名
        obj (str): Mayaのオブジェクトパス
        root (str): スナップデータ上のオブジェクトルート名
        type (str): オブジェクトタイプ

    Returns:
        dict: スナップデータに記録するマテリアル情報dict
    """

    this_data = {
        const.OBJ_NAME_KEY: name,
        const.OBJ_GRP_ID_KEY: grp_id,
        const.OBJ_TYPE_KEY: type,
        const.OBJ_IS_ROOT_KEY: is_root,
        const.FLOAT_DATA_LIST_KEY: [],
        const.VEC3_DATA_LIST_KEY: [],
        const.QUAT_DATA_LIST_KEY: [],
        const.COLOR_DATA_LIST_KEY: []
    }

    for attr_key in const.ALL_OBJ_ATTR_DICT:

        label = attr_key
        attr = const.ALL_OBJ_ATTR_DICT[label]
        val = material_param(obj, attr, q=True)

        if not val:
            continue

        data_type_key = const.FLOAT_DATA_LIST_KEY
        if label in [const.ATTR_ORG_LIGHT_DIR_KEY]:
            data_type_key = const.QUAT_DATA_LIST_KEY
        elif label in [const.ATTR_CHARA_COLOR_KEY, const.ATTR_TOON_BRIGHT_KEY, const.ATTR_TOON_DARK_KEY]:
            data_type_key = const.COLOR_DATA_LIST_KEY

        this_data[data_type_key].append({const.ATTR_LABEL: label, const.DATA_LABEL: val})

    return this_data


def position(maya_obj, obj_type, snap_val=None, use_char_light=False, ws=False, q=False):
    """位置情報を扱うコマンド

    Args:
        maya_obj (str): Mayaオブジェクトパス
        obj_type (str): オブジェクトのタイプ
        snap_val ({'x': float, 'y': float, 'z': float}, optional): スナップしたデータ. Defaults to None.
        use_char_light (bool, optional): キャラライトとして扱うか. Defaults to False.
        ws (bool, optional): ワールド座標で扱うか. Defaults to False.
        q (bool, optional): このフラグをオンにすると現在シーンから作成したスナップデータを返す. Defaults to False.

    Returns:
        {'x': float, 'y': float, 'z': float}: 位置情報のスナップデータ（qフラグがTrueの時のみ）
    """

    # Mayaシーンから情報を取得
    if q:

        pos_val = cmds.xform(maya_obj, q=True, t=True, ws=ws)
        return {'x': pos_val[0] * -1 / const.MAYA_TRANS_SCALE, 'y': pos_val[1] / const.MAYA_TRANS_SCALE, 'z': pos_val[2] / const.MAYA_TRANS_SCALE}  # X反転

    # スナップデータを適用
    else:

        if not snap_val:
            return

        if obj_type == const.TYPE_LIGHT and use_char_light:
            return  # キャラライトはローテーションで扱うので触らない

        maya_pos = [
            snap_val['x'] * const.MAYA_TRANS_SCALE * -1,
            snap_val['y'] * const.MAYA_TRANS_SCALE,
            snap_val['z'] * const.MAYA_TRANS_SCALE
        ]  # X反転

        cmds.xform(maya_obj, t=maya_pos, a=True, ws=ws)


def rotate(maya_obj, parent_obj, obj_type, snap_val=None, use_char_light=False, ws=False, q=False):
    """ローテート情報を扱うコマンド

    Args:
        maya_obj (str): Mayaオブジェクトパス
        parent_obj (str): 親オブジェクトパス
        obj_type (str): オブジェクトのタイプ
        snap_val ({'x': float, 'y': float, 'z': float、'w': float}, optional): スナップしたデータ. Defaults to None.
        use_char_light (bool, optional): キャラライトとして扱うか. Defaults to False.
        ws (bool, optional): ワールド座標で扱うか. Defaults to False.
        q (bool, optional): このフラグをオンにすると現在シーンから作成したスナップデータを返す. Defaults to False.

    Returns:
        {'x': float, 'y': float, 'z': float、'w': float}: ローテート情報のスナップデータ（qフラグがTrueの時のみ）
    """

    # 親をなしにしてWorldSpaceでとる
    if ws:
        parent_obj = None

    # Mayaシーンから情報を取得
    if q:

        w_rot_val = cmds.xform(maya_obj, q=True, ro=True, ws=True)
        w_euler = om.MEulerRotation([math.radians(x) for x in w_rot_val])
        w_quat = w_euler.asQuaternion()

        if parent_obj:
            w_p_rot_val = cmds.xform(parent_obj, q=True, ro=True, ws=True)
            w_p_euler = om.MEulerRotation([math.radians(x) for x in w_p_rot_val])
            w_p_quat = w_p_euler.asQuaternion()
            l_quat = w_quat * w_p_quat.inverse()
        else:
            l_quat = w_quat

        return {'x': l_quat[0], 'y': l_quat[1] * -1, 'z': l_quat[2] * -1, 'w': l_quat[3]}

    # スナップデータを適用
    else:

        if not snap_val:
            return

        parent_world_quat = om.MQuaternion([0, 0, 0, 1])
        if parent_obj:
            parent_world_euler = cmds.xform(parent_obj, q=True, ro=True, ws=True)
            parent_world_euler = om.MEulerRotation([math.radians(x) for x in parent_world_euler])
            parent_world_quat = parent_world_euler.asQuaternion()

        raw_data = [snap_val['x'], snap_val['y'], snap_val['z'], snap_val['w']]
        snap_local_quat = om.MQuaternion([raw_data[0], raw_data[1] * -1, raw_data[2] * -1, raw_data[3]])  # X反転
        this_world_quat = snap_local_quat * parent_world_quat
        this_world_euler = this_world_quat.asEulerRotation()
        this_world_euler = [math.degrees(x) for x in this_world_euler]

        if obj_type == const.TYPE_LIGHT and use_char_light:
            cmds.xform(maya_obj, t=[0, 0, 0], a=True, ws=True)
            cmds.xform(maya_obj, ro=this_world_euler, a=True, ws=True)
            cmds.xform(maya_obj, t=[0, 0, -30], a=True, os=True)  # 原点との位置でライト方向が決まるので適当な値ずらす
        else:
            cmds.xform(maya_obj, ro=this_world_euler, a=True, ws=True)

            if obj_type == const.TYPE_CAMERA:
                cmds.xform(maya_obj, ro=[0, 180, 0], r=True, os=True)  # カメラ反転


def scale(maya_obj, snap_val=None, q=False):
    """スケール情報を扱うコマンド

    Args:
        maya_obj (str): Mayaオブジェクトパス
        obj_type (str): オブジェクトのタイプ
        snap_val ({'x': float, 'y': float, 'z': float}, optional): スナップしたデータ. Defaults to None.
        q (bool, optional): このフラグをオンにすると現在シーンから作成したスナップデータを返す. Defaults to False.

    Returns:
        {'x': float, 'y': float, 'z': float}: スケール情報のスナップデータ（qフラグがTrueの時のみ）
    """

    # Mayaシーンから情報を取得
    if q:

        scale_val = cmds.xform(maya_obj, q=True, r=True, s=True)
        return {'x': scale_val[0], 'y': scale_val[1], 'z': scale_val[2]}

    # スナップデータを適用
    else:

        if not snap_val:
            return

        scale = [snap_val['x'], snap_val['y'], snap_val['z']]
        cmds.xform(maya_obj, s=scale)


def camera_param(maya_obj, snap_val=None, q=False):
    """カメラパラメーターを扱うコマンド

    Args:
        maya_obj (str): Mayaオブジェクトパス
        obj_type (str): オブジェクトのタイプ
        snap_val (float, optional): スナップしたUnityのFOV値. Defaults to None.
        q (bool, optional): このフラグをオンにすると現在シーンから作成したスナップデータを返す. Defaults to False.

    Returns:
        float: FOV値のスナップデータ（qフラグがTrueの時のみ）
    """

    # Mayaシーンから情報を取得
    if q:

        # Mayaのvert_apertureとfocal_lengthを使ってUnityのFOVを計算
        vert_aperture = cmds.camera(maya_obj, q=True, vfa=True)
        focal_length = cmds.camera(maya_obj, q=True, fl=True)
        return (2.0 * math.atan((0.5 * vert_aperture) / (focal_length * 0.03937)) * 57.29578)

    # スナップデータを適用
    else:

        if not snap_val:
            return

        if not cmds.listRelatives(maya_obj, c=True, type='camera'):
            return

        this_vert_aperture = cmds.camera(maya_obj, q=True, vfa=True)
        unity_fov = snap_val

        # Mayaの規定値
        maya_focal_length_min = 2.5
        # unityのFOVを使ってMayaのfocalLengthを計算
        maya_focal_length = this_vert_aperture / (2 * 0.03937 * math.tan(unity_fov / (2 * 57.29578)))

        if maya_focal_length < maya_focal_length_min:
            cmds.setAttr('{}.{}'.format(maya_obj, const.ALL_OBJ_ATTR_DICT[const.ATTR_CAM_FOV_KEY]), maya_focal_length_min)
        else:
            cmds.setAttr('{}.{}'.format(maya_obj, const.ALL_OBJ_ATTR_DICT[const.ATTR_CAM_FOV_KEY]), maya_focal_length)


def material_param(maya_obj, attr, snap_val=None, q=False):
    """マテリアルパラメーターを扱うコマンド

    Args:
        maya_obj (str): Mayaオブジェクトパス
        attr (str): パラメーターのアトリビュート
        obj_type (str): オブジェクトのタイプ
        snap_val (any, optional): スナップしたアトリビュート値. Defaults to None.
        q (bool, optional): このフラグをオンにすると現在シーンから作成したスナップデータを返す. Defaults to False.

    Returns:
        any: アトリビュートに対応したパラメーター値（qフラグがTrueの時のみ）
    """

    if not cmds.attributeQuery(attr, n=maya_obj, ex=True):
        return

    # オリジナルライトを使うか
    if attr == const.ALL_OBJ_ATTR_DICT[const.ATTR_USE_ORG_LIGHT_KEY]:
        if q:
            return cmds.getAttr('{}.{}'.format(maya_obj, attr))
        else:
            if snap_val:
                cmds.setAttr('{}.{}'.format(maya_obj, attr), int(snap_val))

    # オリジナルライト方向
    if attr == const.ALL_OBJ_ATTR_DICT[const.ATTR_ORG_LIGHT_DIR_KEY]:
        if q:
            val = cmds.getAttr('{}.{}'.format(maya_obj, attr))[0]
            return {'x': val[0] * -1, 'y': val[1], 'z': val[2], 'w': 0}  # lightDirの中身は実質Vec3
        else:
            if snap_val:
                light_dir = [snap_val['x'] * -1, snap_val['y'], snap_val['z']]
                cmds.setAttr('{}.{}'.format(maya_obj, attr + 'X'), light_dir[0])
                cmds.setAttr('{}.{}'.format(maya_obj, attr + 'Y'), light_dir[1])
                cmds.setAttr('{}.{}'.format(maya_obj, attr + 'Z'), light_dir[2])

    # 鼻の外連味表現
    if attr == const.ALL_OBJ_ATTR_DICT[const.ATTR_NOSE_PRETENSE_KEY]:
        if q:
            return cmds.getAttr('{}.{}'.format(maya_obj, attr))
        else:
            if snap_val:
                cmds.setAttr('{}.{}'.format(maya_obj, attr), snap_val)

    # 頬の外連味表現
    if attr == const.ALL_OBJ_ATTR_DICT[const.ATTR_CHEEK_PRETENSE_KEY]:
        if q:
            return cmds.getAttr('{}.{}'.format(maya_obj, attr))
        else:
            if snap_val:
                cmds.setAttr('{}.{}'.format(maya_obj, attr), snap_val)

    # 顔の疑似法線ブレンド
    if attr == const.ALL_OBJ_ATTR_DICT[const.ATTR_CYLINDER_BLEND_KEY]:
        if q:
            return cmds.getAttr('{}.{}'.format(maya_obj, attr))
        else:
            if snap_val:
                cmds.setAttr('{}.{}'.format(maya_obj, attr), snap_val)

    # 髪の疑似法線ブレンド
    if attr == const.ALL_OBJ_ATTR_DICT[const.ATTR_CYLINDER_BLEND_KEY]:
        if q:
            return cmds.getAttr('{}.{}'.format(maya_obj, attr))
        else:
            if snap_val:
                cmds.setAttr('{}.{}'.format(maya_obj, attr), snap_val)

    # キャラカラー
    if attr == const.ALL_OBJ_ATTR_DICT[const.ATTR_CHARA_COLOR_KEY]:
        if q:
            rgb = cmds.getAttr('{}.{}'.format(maya_obj, attr + 'RGB'))[0]
            a = cmds.getAttr('{}.{}'.format(maya_obj, attr + 'A'))
            return {'r': rgb[0], 'g': rgb[1], 'b': rgb[2], 'a': a}
        else:
            if snap_val:
                cmds.setAttr('{}.{}'.format(maya_obj, attr + 'RGB'), snap_val['r'], snap_val['g'], snap_val['b'], type='double3')
                cmds.setAttr('{}.{}'.format(maya_obj, attr + 'A'), snap_val['a'])

    # toon明部
    if attr == const.ALL_OBJ_ATTR_DICT[const.ATTR_TOON_BRIGHT_KEY]:
        if q:
            rgb = cmds.getAttr('{}.{}'.format(maya_obj, attr + 'RGB'))[0]
            a = cmds.getAttr('{}.{}'.format(maya_obj, attr + 'A'))
            return {'r': rgb[0], 'g': rgb[1], 'b': rgb[2], 'a': a}
        else:
            if snap_val:
                cmds.setAttr('{}.{}'.format(maya_obj, attr + 'RGB'), snap_val['r'], snap_val['g'], snap_val['b'], type='double3')
                cmds.setAttr('{}.{}'.format(maya_obj, attr + 'A'), snap_val['a'])

    # toon暗部
    if attr == const.ALL_OBJ_ATTR_DICT[const.ATTR_TOON_DARK_KEY]:
        if q:
            rgb = cmds.getAttr('{}.{}'.format(maya_obj, attr + 'RGB'))[0]
            a = cmds.getAttr('{}.{}'.format(maya_obj, attr + 'A'))
            return {'r': rgb[0], 'g': rgb[1], 'b': rgb[2], 'a': a}
        else:
            if snap_val:
                cmds.setAttr('{}.{}'.format(maya_obj, attr + 'RGB'), snap_val['r'], snap_val['g'], snap_val['b'], type='double3')
                cmds.setAttr('{}.{}'.format(maya_obj, attr + 'A'), snap_val['a'])
