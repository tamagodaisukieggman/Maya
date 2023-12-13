# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from functools import partial
from collections import OrderedDict

import glob
import importlib
from logging import root
import os
import sys
import subprocess
import json
import re
from pathlib import Path
import webbrowser
from PySide2 import QtCore, QtGui, QtWidgets

import maya.OpenMaya as om
import maya.cmds as cmds

import mtk.utils.perforce as _MtkP4
from mtk.utils import getCurrentSceneFilePath

from . import NAME

importlib.reload(_MtkP4)
MtkP4 = _MtkP4.MtkP4


MTK_ROOT_PATH = "Z:/mtk/work/resources"
THUMBNAIL_ROOT_PATH = "Z:/mtk/.cas/p4/meta-extra/original/resources"
CHARACTER_DIR_NAME = "characters"
CHARACTER_MODEL_ROOT_PATH = os.path.join(MTK_ROOT_PATH, CHARACTER_DIR_NAME)

CY_THUMBNAIL_EXT = ".mdli.cy-asset-prv"

SAVE_DIRECTORY = os.path.join(os.environ["HOME"], NAME)
HASKEY_JOINTS = "haskey_joints"
THUMBNAIL = "thumbnail"


def open_help_site():
    _web_site = "https://wisdom.cygames.jp/display/mutsunokami/Maya:+Joint+Motion+Manager"
    webbrowser.open(_web_site)


def remove_json_file(json_file_path):
    """json ファイルの削除

    Args:
        json_file_path (str): file path

    Returns:
        [type]: [description]
    """
    flag = False
    try:
        os.remove(json_file_path)
    except Exception as e:
        flag = e
        cmds.warning("Can not remove file [ {} ]".format(e))
    return flag


def open_exploer(path):
    """パスを受け取りWindowsエクスプローラーで表示させる

    Args:
        path (str): ディレクトリパス
    """
    _path = path.replace(os.sep, "/")
    if not os.path.exists(_path):
        _m = u"[ {} ] は存在しません".format(_path)
        print(_m)
        cmds.warning(_m)
        return
    try:
        subprocess.Popen(['explorer', os.path.normpath(_path)])
    except:
        _m = _path + u" が開けませんでした"
        print(_m)
        cmds.warning(_m)
        pass


def check_path_exists(path, make_dir=False):
    """パスが存在するかの確認

    Args:
        path (str): [description]
        make_dir (bool, optional): [description]. Defaults to False.

    Returns:
        [type]: [description]
    """
    if not os.path.exists(path) and make_dir:
        os.makedirs(path)

    if not os.path.exists(path):
        print("Not Found [ {} ]".format(path.replace(os.sep, '/')))
        cmds.warning("Not Found [ {} ]".format(path.replace(os.sep, '/')))
        return
    else:
        return True


def get_scene_name():
    """シーン名を取得
    cmds で取得できないシーンがあったのでOpenMayaでも取得を試みる
    ただし、OpenMayaの場合は開いていなくても文字列は空にならないので
    そのための対処
    """
    scene_name = ""
    scene_path = ""
    scene_basename = ""

    scene_name = getCurrentSceneFilePath()
    if not scene_name:
        scene_name = om.MFileIO.currentFile()

    if len(scene_name.split(".")) < 2:
        scene_name = ""

    if scene_name:
        scene_path, basename = os.path.split(scene_name)
        scene_basename = basename.rsplit(".")[0]

    return scene_name, scene_path, scene_basename


def check_model_directory(directory=""):
    """ルートパスに適しているかの検査
    直下に[model] ディレクトリが必要

    Args:
        directory (str):

    Returns:
        [bool]: exists flag
    """
    directory = Path(directory)
    flag = False
    for _dir in directory.iterdir():
        basename = _dir.stem
        if basename == "model":

            flag = True
            break
    return flag


def get_save_directory(root_path=""):
    """json の保存先を作成
    直下に[model]フォルダが存在するのが条件
    z:/mtk/work/resources/characters/player/00/000
    を受け取り、
    workbench/maya/joint_motion_manager
    を付けて返す

    Args:
        root_path (str): direcotry path

    Returns:
        [str]:
    """
    save_path = Path(root_path)

    save_path = save_path / "workbench"
    save_path = save_path / "maya"
    save_path = save_path / NAME

    if not save_path.exists():
        save_path.mkdir(parents=True)

    return str(save_path)


def get_root_directory(root_path=""):
    """ルートディレクトリを返す
    z:/mtk/work/resources/characters/player/00/000/model/mdl_ply00_m_000.ma
    のシーンパスから
    z:/mtk/work/resources/characters/player/00/000/
    を抽出して返す
    シーンを開いていない場合はマイドキュメントに作成

    Returns:
        [str]: path
    """

    scene_name, scene_path, scene_basename = get_scene_name()

    if not scene_name:
        root_path = Path(os.environ["HOME"])
        root_path = root_path / NAME
        if not root_path.exists():
            root_path.mkdir(parents=True)
    else:
        scene_path = Path(scene_path)
        root_path = scene_path.parent

    return str(root_path)


def get_p4_file_state(file_path=""):
    """
    P4のファイルステータス取得
    ドライブレターが大文字の場合に取れないケースがあった
    しかし、小文字にして取ると、取ることはできるが別のファイルと認識される
    Mayaを再起動すると取れたりする
    """
    file_status_ext = ""
    stat = ""
    current_users = ""

    try:
        file_status_ext = MtkP4.status_ext([file_path])
        stat = file_status_ext[file_path]["action"]
        current_users = file_status_ext[file_path]["users"]

    except Exception as e:
        print(e)

    return file_status_ext, stat, current_users


def get_newest_file(directory_path=""):
    """
    p4 での最新データ取得
    """
    flag = True

    try:
        MtkP4.sync([u"{}".format(directory_path)])
    except Exception as e:
        print(e)
        flag = False

    return flag


def add_p4_files(file_paths=[]):
    """ファイルパスをadd する

    Args:
        file_paths (list, filepath str):

    Returns:
        [bool]:

    """
    flag = False
    try:
        MtkP4.add(file_paths)
        flag = True
    except Exception as e:
        print(e)
    return flag


def submit_p4_files(file_paths=[]):
    """ファイルをサブミット

    Args:
        file_paths (list, filepath str):

    Returns:
        [bool]:
    """
    flag = False
    try:
        MtkP4.submit(file_paths, '[{}]'.format(NAME))
        flag = True
    except Exception as e:
        print(e)
    return flag


def check_out_p4_files(file_paths=[]):
    """ファイルをチェックアウト

    Args:
        file_paths (list, filepath str):
    """
    flag = False
    try:
        MtkP4.edit(file_paths)
        flag = True
    except Exception as e:
        print(e)
    return flag


def check_p4_file_status(file_path=""):
    """p4 のステータスを取得

    Args:
        file_path (str): target filepath

    Returns:
        [str, str]:
    """
    file_status_ext = ""
    status = ""
    current_users = ""

    try:
        file_status_ext = MtkP4.status_ext([file_path])
        status = file_status_ext[file_path]["action"]
        current_users = file_status_ext[file_path]["users"]
    except Exception as e:
        print(e)

    return status, current_users


def check_p4_file_statuses(root_path=""):
    """p4 のステータスを取得　複数版

    Args:
        root_path (str): directory path

    Returns:
        [dict]:
    """
    file_states = {}
    root_path = Path(root_path)
    for _file in root_path.glob('*.json'):
        status, current_users = check_p4_file_status(str(_file))
        file_states[str(_file)] = [status, current_users]
    return file_states


def save_json_file(path="", scene_name="", joint_anim_dict=None):
    """ジョイントのキーフレーム情報をjson で保存

    Args:
        path (str, root directory): ファイルを保存するディレクトリ
        scene_name (str, maya scene path): Maya シーンのフルパス
        joint_anim_dict (dict): ジョイント名とキーの情報

    Returns:
        [str]: 生成したjson ファイルの名前
    """
    _flag = False
    _id = "000"
    json_data = OrderedDict()

    scene_path, basename = os.path.split(scene_name)
    scene_basename = basename.rsplit(".")[0]

    json_files = get_json_files(path, prefix=scene_basename)
    if json_files:

        last_num = json_files[-1]
        _, last_num = os.path.split(last_num)
        last_num = last_num.split(".", 1)[0]
        last_num = last_num.rsplit("__", 1)[-1]
        if last_num.isdigit():
            last_num = int(last_num)
            next_num = last_num + 1
            _id = "{:0>3}".format(next_num)

    json_name = "{}__{}".format(scene_basename, _id)
    json_file_name = "{}.json".format(json_name)
    new_json_file = os.path.join(path, json_file_name).replace(os.sep, "/")

    split_path = scene_path.split(CHARACTER_DIR_NAME)
    thumbnail_path = ""
    if len(split_path) == 2:
        thumbnail_path = os.path.join(
            THUMBNAIL_ROOT_PATH,
            CHARACTER_DIR_NAME,
            split_path[-1][1:],
            scene_basename + CY_THUMBNAIL_EXT)
        thumbnail_path = thumbnail_path.replace(os.sep, "/")

    json_data[THUMBNAIL] = thumbnail_path
    json_data[HASKEY_JOINTS] = joint_anim_dict

    with open(new_json_file, "w") as _json_file:
        _json_data = json.dumps(
            json_data,
            indent=4,
            separators=(',', ': '))
        try:
            _json_file.write(_json_data)
            _flag = True
        except Exception as e:
            print(e)
            return
    return json_name


def get_mtk_joints():
    """helper ジョイント以外のジョイントを取得して返す

    Returns:
        [list]: joints
    """
    joints = [x for x in cmds.ls(type="joint", l=True) if "helper" not in x]
    return joints


def goto_zero_frame():
    """ゼロフレームに移動
    """
    cmds.currentTime(0.0)


def get_joints_animation():
    """
    ジョイントのフルパス名：アトリビュートのキーフレーム
    を取得

    Returns:
        [dict]:
    """
    joint_anim_dict = OrderedDict()

    joints = cmds.ls(type="joint", long=True)

    if not joints:
        return

    for joint in joints:
        attribute_keyframes = OrderedDict()
        attributes = cmds.listAnimatable(joint)
        for attribute in attributes:
            num_keyframes = cmds.keyframe(
                attribute, q=True, keyframeCount=True)
            if num_keyframes == 0:
                continue
            _attr = attribute.split(".", 1)[-1]

            key_dict = {}
            times = cmds.keyframe(attribute,
                                  q=True,
                                  index=(0, num_keyframes),
                                  timeChange=True,
                                  a=False)
            values = cmds.keyframe(attribute,
                                   q=True,
                                   index=(0, num_keyframes),
                                   valueChange=True,
                                   a=False)

            key_dict["times"] = tuple(times)
            key_dict["values"] = tuple(values)

            attribute_keyframes[_attr] = key_dict
        if attribute_keyframes:
            joint_anim_dict[joint] = attribute_keyframes

    return joint_anim_dict


def get_json_files(path="", prefix=""):
    """json ファイルの取得

    Args:
        path (str): directory
        prefix (str): json file name

    Returns:
        [list]: json files
    """
    seach_path = os.path.join(path, "{}*.json".format(prefix))
    json_files = glob.glob(seach_path)

    return json_files


def get_thumbnail_paths(json_files=[]):
    """サムネイルパスの取得

    Args:
        json_files (list): json file paths

    Returns:
        [dict]: Cyllista のサムネイルの場所
    """
    thumbnail_paths = OrderedDict()

    for json_file in json_files:
        path, basename = os.path.split(json_file)
        basename = basename.split(".")[0]
        with open(json_file, "r") as _f:
            _data = json.load(_f)
            thumbnail_path = _data.get(THUMBNAIL, None)
            thumbnail_paths[basename] = thumbnail_path

    return thumbnail_paths


def set_keyframe_alljoints():
    """キーフレーム作成
    """
    joints = get_mtk_joints()
    if not joints:
        return
    cmds.setKeyframe(
        joints,
        breakdown=False,
        hierarchy="none",
        controlPoints=False,
        shape=False
    )


def delete_keyframe(joint_anim_dict):
    """キーフレーム削除

    Args:
        joint_anim_dict (dict):ジョイント:キーフレーム
    """
    joints = get_mtk_joints()
    if not joints:
        return
    current_time = cmds.currentTime(q=True)
    cmds.cutKey(joints, iub=False, animation="objects",
                cl=True, time=(current_time, current_time + 1))


def remove_joint_keyframe():
    """キーアニメーション削除
    """
    joints = cmds.ls(type="joint", l=True)
    if not joints:
        return
    current_time = cmds.currentTime(q=True)
    cmds.currentTime(0.0)
    for joint in joints:
        cmds.cutKey(joint, cl=True)
    cmds.currentTime(current_time)

    root_nodes = cmds.ls(assemblies=True)
    for root_node in root_nodes:
        try:
            cmds.dagPose(root_node, g=True, restore=True, bindPose=True)
        except Exception as e:
            _m = "warning [ {} ]".format(e)
            print(_m)
            cmds.warning(_m)


def do_mirror_copy(joint_dict={}, joint_anim_dict={}, _source="R", _target="L"):
    """ミラーコピー実行部分

    Args:
        joint_dict (dict): jointShortName__strlength: jointLongName
        joint_anim_dict (dict): jointLongName: Keyframes
        _source (str): Defaults to "R".
        _target (str): Defaults to "L".
    """
    for joint, motions in joint_anim_dict.items():

        joint_short_name = joint.split("|")[-1]

        pattern = r'([0-9]{4})'
        result = re.findall(pattern, joint_short_name)
        if result:
            joint_short_name = joint_short_name.split(result[0])[-1][1:]
            if _source in joint:
                str_length = len(joint)
                replace_name = joint_short_name.replace(_source, _target)
                target_joint = joint_dict.get(
                    f'{replace_name}__{str_length}', None)
                if not target_joint:
                    continue

                for attribute, keys in motions.items():
                    if not attribute.startswith("rotate"):
                        continue
                    for time, value in zip(keys["times"], keys["values"]):
                        if round(time) == 0.0:
                            value = cmds.getAttr(
                                "{}.{}".format(target_joint, attribute))
                        else:
                            if not attribute.endswith("X"):
                                value = value * -1

                        cmds.setKeyframe(
                            target_joint,
                            hierarchy="none",
                            controlPoints=False,
                            shape=False,
                            attribute=attribute,
                            value=value,
                            time=time
                        )


def mirror_keyframe(joint_anim_dict={}, r_to_l_flag=True):
    """キーフレームのミラーリング

    Args:
        joint_anim_dict (dict): ジョイント:キーフレーム
        r_to_l_flag (bool): 左右反転
    """

    _source = "_R"
    _target = "_L"
    if not r_to_l_flag:
        _source = "_L"
        _target = "_R"

    joints = get_mtk_joints()
    if not joints:
        return

    joint_dict = OrderedDict()
    for joint in joints:
        joint_short_name = joint.split("|")[-1]

        pattern = r'([0-9]{4})'
        result = re.findall(pattern, joint_short_name)

        if result:
            joint_short_name = joint_short_name.split(result[0])[-1][1:]

        joint_dict[f'{joint_short_name}__{len(joint)}'] = joint

    current_time = cmds.currentTime(q=True)

    cmds.undoInfo(openChunk=True)
    cmds.currentTime(0.0)

    do_mirror_copy(joint_dict, joint_anim_dict, _source, _target)

    cmds.currentTime(current_time)
    cmds.undoInfo(closeChunk=True)


def attach_job(object_name="", job=None):
    """GUI にスクリプトジョブを付ける

    Args:
        object_name (str): GUI Object name
        job (function):
    """
    if not object_name or not job:
        return
    cmds.scriptJob(parent=object_name, event=("SceneOpened", partial(job)))
    cmds.scriptJob(parent=object_name, event=("NewSceneOpened", partial(job)))


def str_to_list(_str=""):
    """文字列をリストにして返す

    Args:
        _str (str): list_to_str で作った文字列

    Returns:
        [list]:
    """
    result = list()
    for _s in _str.split(","):
        if not _s:
            continue
        result.append(_s)
    return result


def list_to_str(str_list):
    """文字列リストを文字列に変換
    ",".join(list)の場合、一つしかないと, を付けてくれない

    Args:
        str_list (list): 文字列のリスト

    Returns:
        [str]: , でつなげた文字列
    """
    result = ""
    for _s in str_list:
        result += f'{_s},'
    return result.strip()


def get_active_handle():
    """選択されている回転ハンドルの軸を取得
    0: x, 1: y, 2: z, 3:None
    Returns:
        [str, int]: axis
    """
    _types = [
        "transform",
        "rotate",
        "scale",
    ]
    _type = None
    axis = None
    current_tool = cmds.currentCtx()
    if current_tool == 'RotateSuperContext':
        _type = "r"
        axis = cmds.manipRotateContext(
            "Rotate", q=True, currentActiveHandle=True)
    elif current_tool == "moveSuperContext":
        _type = "t"
        axis = cmds.manipMoveContext("Move", q=True, currentActiveHandle=True)
    elif current_tool == "scaleSuperContext":
        _type = "s"
        axis = cmds.manipScaleContext(
            "Scale", q=True, currentActiveHandle=True)
    return _type, axis


def get_selection_nodes():
    """選択されているジョイントを返す
    リストを文字列に変換して返している
    """
    selections = cmds.ls(sl=True, type='joint', long=True)

    if selections:
        selections = list_to_str(selections)
    else:
        selections = None
    return selections


def get_node_attribute():
    selections = cmds.ls(sl=True, type='joint', long=True)

    if selections:
        selections = list_to_str(selections)

    attributes = cmds.channelBox("mainChannelBox",
                                 query=True,
                                 selectedMainAttributes=True)

    return selections, attributes


def get_default_value(node="", attribute=""):
    """アトリビュートの取得

    Args:
        node (str): node name
        attribute (str): attribute name

    Returns:
        [type]: [description]
    """
    return cmds.getAttr(f'{node}.{attribute}')


def attribute_value_chane(nodes=[], attribute="", value=0.0):
    """アトリビュートの値の変更

    Args:
        nodes (list): maya node
        attribute (str): attribute name
        value (float): attribute value
    """
    if not nodes and not attribute:
        return
    for node in nodes:
        if not cmds.objExists(node):
            continue

        if not cmds.attributeQuery(attribute, node=node, exists=True):
            continue
        cmds.setAttr(f'{node}.{attribute}', value)


def check_node_exists(node_name=""):
    """ノードの存在確認

    Args:
        node_name (str): node name

    Returns:
        [bool]: [description]
    """
    return cmds.objExists(node_name)


def create_channel_slider():
    """
    ['tz', 'rx', 'ry', 'rz'] or None
    """
    cmds.channelBox("mainChannelBox", query=True, selectedMainAttributes=True)


def read_json_file(json_file_path, onlyRotateFlag=False):
    """json ファイルの読み込みと内容の適用

    Args:
        json_file_path (str): json file path
        onlyRotateFlag (bool): 回転地のみ適用フラグ

    Returns:
        [list]: キーを適用したジョイント
    """
    joints = get_mtk_joints()
    if not joints:
        return

    joint_dict = OrderedDict()
    for joint in joints:
        joint_short_name = joint.split("|")[-1]
        pattern = r'([0-9]{4})'
        result = re.findall(pattern, joint_short_name)
        if result:
            joint_short_name = joint_short_name.split(result[0])[-1][1:]
        joint_dict[joint_short_name] = joint

    with open(json_file_path, "r") as json_data:
        _data = json.load(json_data)

    if not _data:
        return
    key_joints = _data.get(HASKEY_JOINTS, None)
    if not key_joints:
        return

    current_time = cmds.currentTime(q=True)
    cmds.currentTime(0.0)

    apply_joints = []
    for joint, motions in key_joints.items():
        joint_short_name = joint.split("|")[-1]
        pattern = r'([0-9]{4})'
        result = re.findall(pattern, joint_short_name)
        if result:
            joint_short_name = joint_short_name.split(result[0])[-1][1:]
        joint = joint_dict.get(joint_short_name, joint)
        if not cmds.objExists(joint):
            continue

        joint_short_name = joint.split("|")[-1]
        for attribute, keys in motions.items():
            if not cmds.attributeQuery(attribute, node=joint, ex=True):
                continue
            if onlyRotateFlag and not attribute.startswith("rotate"):
                continue
            else:
                if(not attribute.startswith("translate") and
                        not attribute.startswith("rotate") and
                        not attribute.startswith("scale")):
                    continue
            for time, value in zip(keys["times"], keys["values"]):
                if round(time) == 0.0:
                    value = cmds.getAttr("{}.{}".format(joint, attribute))

                cmds.setKeyframe(
                    joint,
                    breakdown=False,
                    hierarchy="none",
                    controlPoints=False,
                    shape=False,
                    attribute=attribute,
                    value=value,
                    time=time
                )

                if not joint_short_name in apply_joints:
                    apply_joints.append(joint_short_name)

    cmds.currentTime(current_time)
    return apply_joints
