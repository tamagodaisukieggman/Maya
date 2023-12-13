# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from functools import partial
from collections import OrderedDict

import glob
from logging import root
import os
import subprocess
import json
import re
from pathlib import Path
import webbrowser

import maya.OpenMaya as om
import maya.cmds as cmds

# import shr.utils.perforce as _MtkP4
from ...utils import getCurrentSceneFilePath

from . import NAME
from . import TOOL_NAME
from ...utils import gui_util

from . import NOT_MOVE_JOINTS

SAVE_DIRECTORY = os.path.join(os.environ["HOME"], NAME)
HASKEY_JOINTS = "haskey_joints"
THUMBNAIL = "thumbnail"


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

def get_file_info_data(data_name="") -> str:
    """Maya のシーンに設定されたfileInfo のデータ取得
    shenron Easy Bind_{data_name}
    の形になる
    Args:
        data_name (str, optional): fileInfo のデータ名. Defaults to "".

    Returns:
        str: _description_
    """
    _info_data = cmds.fileInfo("{}_{}".format(TOOL_NAME, data_name), q=True)

    return _info_data or None

def set_file_info_data(data_name="", value=""):
    """Maya シーンにfileInfo のデータを設定する

    Args:
        data_name (str, optional): fileInfo のデータ名. Defaults to "".
        value (str, optional): 設定するのデータの値. Defaults to "".
    """
    cmds.fileInfo("{}_{}".format(TOOL_NAME, data_name), value)

def conform_dialog(title='', message=''):
    """ダイアログ表示

    Args:
        title (str, optional): ウィンドウタイトル. Defaults to ''.
        message (str, optional): 表示メッセージ. Defaults to ''.
    """
    if not title:
        title=TOOL_NAME
    _d = gui_util.ConformDialog(title=title,
                    message=message)
    _d.exec_()
    print(message)

def conform_result_dialog(title='', message=''):
    """確認ダイアログ表示

    Args:
        title (str, optional): ウィンドウタイトル. Defaults to ''.
        message (str, optional): 表示メッセージ. Defaults to ''.
    """
    _m = message

    _d = gui_util.ConformDialogResult(title=TOOL_NAME, message=_m)
    result = _d.exec_()
    print(_m)

    if not result:
        return
    else:
        return True

def open_help_site():
    """ヘルプサイトを開く
    """
    _web_site = "https://wisdom.cygames.jp/display/mutsunokami/Maya:+Joint+Motion+Manager"
    # webbrowser.open(_web_site)
    cmds.warning('coming soon ....')

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

def check_path_exists(path="", make_dir=False):
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

def create_work_directory(work_dir='', create=True):
    work_dir = Path(work_dir)
    work_dir = work_dir / NAME

    if create:
        work_dir.mkdir(parents=True, exist_ok=True)

    return work_dir

def open_exploer(path=''):
    """パスを受け取りWindowsエクスプローラーで表示させる

    Args:
        path (str): ディレクトリパス
    """
    _path = str(path)
    _path = _path.replace(os.sep, "/")
    _m = ''
    if not os.path.exists(_path):
        _m = f"[ {_path} ] not found"
        conform_dialog(message=_m)
        return
    try:
        subprocess.Popen(['explorer', os.path.normpath(_path)])
    except:
        _m = f'[ {_path} ] could not open'
        conform_dialog(message=_m)
        pass


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

def get_p4_file_status(file_path=''):
    file_status_flags = P4.get_file_status_flags(file_path)
    return file_status_flags

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

def goto_zero_frame():
    """開始フレームに移動
    """
    _start_time =cmds.playbackOptions(q=True, animationStartTime=True)
    cmds.currentTime(_start_time)


def get_selection_joints()->list:
    joints = cmds.ls(type='joint', selection=True, long=True)
    return joints

def get_scene_joints()->list:
    joints = cmds.ls(type='joint', long=True)
    return joints

def get_shenron_joints()->list:
    joints = []
    for joint in cmds.ls(type='joint', long=True):
        suffix = joint.rsplit("_", 1)[-1]
        if suffix in NOT_MOVE_JOINTS:
            continue
        joints.append(joint)
    return joints

def get_scene_joints_dict()->dict:
    joint_dict = {}
    for joint in cmds.ls(type='joint', long=True):
        short_name = cmds.ls(joint, shortNames=True)[0]
        joint_dict[short_name] = joint
    return joint_dict

def get_mtk_joints()->list:
    """helper ジョイント以外のジョイントを取得して返す

    Returns:
        [list]: joints
    """
    joints = [x for x in cmds.ls(type="joint", l=True) if "helper" not in x]
    return joints

def get_joints_animation():
    """
    ジョイントのフルパス名：アトリビュートのキーフレーム
    を取得

    Returns:
        [dict]:
    """
    joint_anim_dict = {}

    joints = cmds.ls(type="joint", long=True)

    if not joints:
        return

    for joint in joints:
        attribute_keyframes = {}
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

    if not joint_anim_dict:
        _m = 'Joints in the scene had no keyframe animation'
        conform_dialog(message=_m)
        return

    return joint_anim_dict


def read_json_file(json_file_path, onlyRotateFlag=False):
    """json ファイルの読み込みと内容の適用

    Args:
        json_file_path (str): json file path
        onlyRotateFlag (bool): 回転地のみ適用フラグ

    Returns:
        [list]: キーを適用したジョイント
    """
    _m = 'Import Animation?'

    if not conform_result_dialog(message=_m):
        return

    joints = get_scene_joints()
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
    goto_zero_frame()

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

def save_json_file(path="", scene_name="", joint_anim_dict=None)->str:
    """ジョイントのキーフレーム情報をjson で保存

    Args:
        path (str, root directory): ファイルを保存するディレクトリ
        scene_name (str, maya scene path): Maya シーンのフルパス
        joint_anim_dict (dict): ジョイント名とキーの情報

    Returns:
        [str]: 生成したjson ファイルの名前
    """
    if not path:
        conform_dialog(message="Scene files need to be saved")
        return

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

def all_keyframe_alljoints():
    joints = get_shenron_joints()

    if not joints:
        return

    cmds.setKeyframe(
                    joints,
                    breakdown=False,
                    hierarchy="none",
                    controlPoints=False,
                    shape=False
                    )

def set_keyframe_alljoints():
    """キーフレーム作成
    """
    joints = get_selection_joints()
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
    joints = get_selection_joints()
    if not joints:
        return
    current_time = cmds.currentTime(q=True)
    cmds.cutKey(joints, time=(current_time, current_time),
                hierarchy='none', controlPoints=False, shape=False)

def remove_joint_keyframe():
    """キーアニメーション削除
    """
    _m = 'Remove All Animation?'

    if not conform_result_dialog(message=_m):
        return

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

def goto_next_keyframe():
    """次のキーフレームに移動
    """
    cmds.currentTime(cmds.findKeyframe(timeSlider=True, which='next'), edit=True)

def goto_previous_keyframe():
    """前のキーフレームに移動
    """
    cmds.currentTime(cmds.findKeyframe(timeSlider=True, which='previous'), edit=True)

def mirror_keyframe():
    """キーフレームのミラーコピー
    """
    all_joint = get_scene_joints_dict()
    if not all_joint:
        return

    joint_anim_dict = get_joints_animation()
    if not joint_anim_dict:
        return

    _right = "R"
    _left = "L"
    _prefix = [_right, _left]

    joints = get_selection_joints()
    if not joints:
        return

    _not_found_joint = []
    _not_found_motion = []
    for joint in joints:
        joint_shrot_name = cmds.ls(joint, shortNames=True)[0]
        if joint_shrot_name[0] in _prefix:
            # 選択したジョイントの始めの位置文字を_prefixのリストと照合し、対応するインデックスで無い方をターゲットとする
            mirror_target = f'{_prefix[int(not _prefix.index(joint_shrot_name[0]))]}{joint_shrot_name[1:]}'
            if mirror_target not in all_joint:
                _not_found_joint.append(mirror_target)
                continue
            motions = joint_anim_dict.get(joint)
            if not motions:
                _not_found_motion.append(joint_shrot_name)
                continue
            for attribute, keys in motions.items():
                if not attribute.startswith("rotate"):
                    continue
                for time, value in zip(keys["times"], keys["values"]):
                    if round(time) == 0.0:
                        value = cmds.getAttr(
                            "{}.{}".format(mirror_target, attribute))
                    else:
                        if not attribute.endswith("X"):
                            value = value * -1

                    cmds.setKeyframe(
                                    mirror_target,
                                    hierarchy="none",
                                    controlPoints=False,
                                    shape=False,
                                    attribute=attribute,
                                    value=value,
                                    time=time
                                    )

    if _not_found_joint:
        conform_dialog(title='Not Found', message='{}\n\nJoints not found'.format("\n".join(_not_found_joint)))
    if _not_found_motion:
        conform_dialog(title='Not Found', message='{}\n\nAnimations not found'.format("\n".join(_not_found_motion)))



# ここからスライダー部分
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
    axis_dict = {
        0: "x",
        1: "y",
        2: "z",
    }

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

    axis = axis_dict.get(axis, None)

    if not _type:
        conform_dialog(message=u'Use [ Move, Rotate, Scale ] tool')
    if _type and not axis:
        conform_dialog(message=u'Select [ Axis ] of the handle')

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

    if not selections:
        conform_dialog(message=u'Select Joints')
    return selections

def get_default_value(node="", attribute=""):
    """アトリビュートの取得

    Args:
        node (str): node name
        attribute (str): attribute name

    Returns:
        [type]: [description]
    """
    return cmds.getAttr(f'{node}.{attribute}')

def undo_info_open_chunk():
    cmds.undoInfo(openChunk=True)

def undo_info_close_chunk():
    cmds.undoInfo(closeChunk=True)

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

