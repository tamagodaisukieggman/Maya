from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from collections import OrderedDict
import yaml
import base64
import itertools
import os
import subprocess

import maya.api.OpenMaya as om2
import maya.api.OpenMayaAnim as om2anim

import maya.cmds as cmds
from mtk.utils import getCurrentSceneFilePath


import cyllista.config_node as ccn
import cyllista.export

from mtk.utils.perforce import MtkP4

from . import NAME
from . import gui_util
from . import BODY_NAMES
from . import SKL_PELVIS_C
from . import ROOT_JOINT
from . import MODEL_GROUP


TEMP_NODE = "{}_temp_group".format(NAME)
COVERTER_FILE_NAME = "convert.py"


_type_dict = {"ma": "mayaAscii",
              "mb": "mayaBinary"}


def get_children_fullpath_dict(current_node="", node_type="transform"):
    full_path_short_path = {}
    children = cmds.listRelatives(
        current_node, children=True, type=node_type, fullPath=True)
    if children:
        for c in children:
            short_name = cmds.ls(c, shortNames=True)[0]
            full_path_short_path[c] = short_name
    return full_path_short_path


def represent_ordereddict(dumper, data):
    value = []

    for item_key, item_value in data.items():
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)

        value.append((node_key, node_value))

    return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)


yaml.add_representer(OrderedDict, represent_ordereddict)


def launchModelEditor(scene_name):

    python = os.path.join(
        os.environ["CYLLISTA_TOOLS_PATH"], 'python', 'python.bat')
    mediator = r"Z:\cyllista\tools\python\modules\cy\ed\asset\modeleditormediator.py"
    cmd = [python, mediator, scene_name]

    cflags = 0x08000000
    p = subprocess.Popen(cmd,
                         creationflags=cflags,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    stdout, stderr = p.communicate()
    retCode = p.returncode
    if retCode != 0:
        print("retCode: {}, err: {}", retCode, stderr)


# Maya fileInfo に書き込んだり読み込んだりの関数群
def file_info_decode(value):
    try:
        val = base64.b64decode(value.encode('utf-8'))
        return dict(yaml.safe_load(val))
    except TypeError:
        return value


def file_info_encode(value):
    return base64.b64encode(yaml.safe_dump(value, default_flow_style=False).encode('utf-8'))


def file_info_save(key, value):
    encoded = file_info_encode(value)
    cmds.fileInfo(key, encoded)


def file_info_load(key):
    answer = cmds.fileInfo(key, q=True)

    if not answer or answer[0] == "''\\n":
        return dict()
    return file_info_decode(answer[0])


def file_info_exists(key):
    answer = cmds.fileInfo(key, q=True)
    return len(answer) != 0


def file_info_ls():
    all_values = cmds.fileInfo(q=True)
    keys = itertools.islice(all_values, 0, None, 2)
    values = itertools.islice(all_values, 1, None, 2)
    return itertools.izip(keys, values)


def file_info_delete(key):
    cmds.fileInfo(rm=key)


def yaml_load_files(file_paths=[]):
    parts_preset = dict()
    root_nodes = dict()
    if not file_paths:
        return
    for p in file_paths:
        if not os.path.exists(p):
            continue
        _path, basename = os.path.split(p)
        basename, ext = basename.split(".", 1)
        with open(p) as _file:
            yml = yaml.safe_load(_file)
            _parts_preset = yml.get("parts_preset", None)
            _root_nodes = yml.get("root_nodes", None)
            if _parts_preset:
                parts_preset[basename] = _parts_preset
                root_nodes[basename] = _root_nodes

    return parts_preset, root_nodes


def yaml_save_files_p4(yml_path_stat=dict(),
                       _parts_preset=dict(),
                       _root_nodes=dict()):
    """自分でチェックアウトしているもの、P4 管理されていないもの以外は保存しない

    Args:
        yml_path_stat ([dict]): yaml_file_path : stat
        _parts_preset ([dict]): グループ名: 内容（ノードの辞書）
        _root_nodes ([dict]): グループ名: ルートノード
    """

    _message = []
    for group_name, node_children in _parts_preset.items():
        # yaml のファイルパスと、stat を取得
        (yaml_path, stat) = yml_path_stat.get(group_name, None)
        # stat があり、checkout でない場合は処理をしない
        if stat and stat != "checkout":
            _message.append(yaml_path)
            continue

        # 書き込む情報をまとめてから書き込み
        _obj = dict()
        _obj["parts_preset"] = _parts_preset.get(group_name, None)
        _obj["root_nodes"] = _root_nodes.get(group_name, None)
        with open(yaml_path, "w") as _file:
            yaml.dump(_obj, _file, encoding='utf-8', allow_unicode=True)

    # 書き込めないものがあればメッセージ表示
    if _message:
        _m = u"以下のファイルは他のユーザー使用しているようです\n\n"
        _m += u"{}".format(u"{}\n".join(_message))
        _d = gui_util.ConformDialog(message=_m)
        _d.exec_()


def yaml_save_files(path="", _parts_preset=dict(), _root_nodes=dict()):
    """yaml ファイルの書き込み

    Args:
        path (str, optional): [description]. Defaults to "".
        _parts_preset ([type], optional): [description]. Defaults to dict().
        _root_nodes ([type], optional): [description]. Defaults to dict().
    """
    _m = u""
    if not os.path.exists(path):
        _m = u"パスが存在しません"

    for group_name, node_children in _parts_preset.items():
        _obj = dict()
        _obj["parts_preset"] = _parts_preset.get(group_name, None)
        _obj["root_nodes"] = _root_nodes.get(group_name, None)
        # roots = root_nodes.get(group_name, None)
        parts_preset = file_info_encode(node_children)
        yaml_path = os.path.join(path, group_name + ".yaml")
        with open(yaml_path, "w") as _file:
            yaml.dump(_obj, _file, encoding='utf-8', allow_unicode=True)


def get_p4_file_state(file_path):
    """
    P4のファイルステータス取得
    ドライブレターが大文字の場合に取れないケースがあった
    しかし、小文字にして取ると、取ることはできるが別のファイルと認識される
    Mayaを再起動すると取れたりする

    チェックアウト
    (dict([('Z:/mtk/work/noshipping/characters/edit_test/player/00/001/model/body/mdl_ply00_m_body_001.ma',
    {'action': 'checkout', 'haveRev': 2, 'users': ['ando_shoji'], 'headRev': 2})]),
    'checkout',
    ['ando_shoji'])

    p4管理
    (dict([('Z:/mtk/work/noshipping/characters/edit_test/player/00/001/model/arm/mdl_ply00_m_arm_001.ma',
    {'action': 'latest', 'haveRev': 2, 'users': [], 'headRev': 2})]),
    'latest',
    [])

    p4管理外
    (dict([('Z:/mtk/work/noshipping/characters/edit_test/player/00/001/model/all/mdl_ply00_m_all_001.ma',
    {'action': None, 'haveRev': 0, 'users': [], 'headRev': 0})]),
    None,
    [])

    他の人チェックアウト
    (dict([('Z:/mtk/work/resources/env/r001/s000_ruinsbuilding002/model/mdl_r001_s000_ruinsbuilding002_000.ma',
    {'action': 'other', 'haveRev': 7, 'users': ['kuchiyama_kento'], 'headRev': 8})]),
    'other',
    ['kuchiyama_kento'])

    """
    file_status_ext = None
    stat = None
    current_users = None
    if file_path and os.path.exists(file_path):

        try:
            file_status_ext = MtkP4.status_ext([file_path])
            stat = file_status_ext[file_path]["action"]
            # file_status_ext = file_status_ext
            # stat = stat
            current_users = file_status_ext[file_path]["users"]
            # file_fstat = MtkP4.fstat(file_path)
            # self.fstat = self.file_fstat[0]["headAction"]
        except Exception as e:
            print(e)

    return file_status_ext, stat, current_users


def get_children_short_name(node, mesh_list):
    """子のノードを再帰的に取得する
    ショートネームバージョン

    Args:
        node ([type]): [description]
        mesh_list ([type]): [description]

    Returns:
        [type]: [description]

    使い方
    _li = []
    mesh_list = get_children_short_name(model_node, _li)

    """
    children = cmds.listRelatives(
        node, children=True, path=True, type="transform")

    if children:
        for i in children:
            mesh_list.append(i)
            get_children_short_name(i, mesh_list)
    return mesh_list


def get_children(node, mesh_list):
    """子のノードを再帰的に取得する
    ロングネームバージョン

    Args:
        node ([type]): [description]
        mesh_list ([type]): [description]

    Returns:
        [type]: [description]
    """
    children = cmds.listRelatives(
        node, children=True, fullPath=True, type="transform")

    if children:
        for i in children:
            mesh_list.append(i)
            get_children(i, mesh_list)
    return mesh_list


def get_parents(node=""):
    u"""ルートノード取得

    Args:
        node (str)): Maya ノードの文字列

    Yields:
        [type]: [description]
    """
    parent = cmds.listRelatives(node, parent=True, fullPath=True)
    if parent:
        yield parent[0]
        for p in get_parents(parent):
            yield p


def get_root_joint():
    """ルートジョイント
    ROOT_JOINT = "jnt_0000_skl_root"
    を見つけて返す

    Returns:
        [str]: [description]
    """
    _root_joint_name = ROOT_JOINT
    _root_joint = cmds.ls("*{}".format(_root_joint_name), type="joint", l=True)

    if not _root_joint:
        _m = u"ルートジョイントノード\n\n"
        _m += u"[ {} ]\n\n".format(_root_joint_name)
        _m += u"が見つかりません"
        _d = gui_util.ConformDialog(message=_m)
        _d.exec_()
        return
    return _root_joint[0]


def get_root_node(node):
    """ルートノードを返す

    Args:
        node ([type]): [description]

    Returns:
        [type]: [description]
    """
    root_node = None
    for _p in get_parents(node):
        root_node = _p

    return root_node


def get_model_node(root_node):
    """モデルノード取得
    ルートノード以下のモデルグループを取得する

    Args:
        root_node (str): [description]

    Returns:
        [str]: [description]
    """
    _model_group_name = MODEL_GROUP
    _model_group = None
    root_node_children = cmds.listRelatives(root_node,
                                            children=True,
                                            type="transform",
                                            fullPath=True)
    if not root_node_children:
        return

    for _node in root_node_children:
        if _node.split("|")[-1] == _model_group_name:
            _model_group = _node

    if not _model_group:
        _m = u"[ {} ] ノード以下に\n".format(root_node)
        _m += u"[ {} ] グループが存在しません".format(_model_group_name)
        _d = gui_util.ConformDialog(message=_m)
        _d.exec_()
        return

    return _model_group


def set_default_hierarchy(nodes, short_name_parent):
    """使っていないがアウトライナの順番整理に便利なのでとっておく

    Args:
        nodes ([list]): ノードのショートネームのリスト
                        このリストの順番にソートされる
        short_name_parent ([dict]): ショートネームとその親が入った辞書
    """
    for short_name in nodes:
        if not cmds.objExists(short_name):
            continue
        _current_parent = cmds.listRelatives(
            short_name, parent=True, path=True)
        _parent = short_name_parent[short_name]
        if not _parent and not cmds.objExists(_parent):
            continue
        if _current_parent != _parent:
            cmds.parent(short_name, _parent, absolute=True)
        cmds.reorder(short_name, back=True)


def check_group_nodes(group_name, nodes):
    """ツール上で作られるグループに特定のノードが含まれているかのチェック
    ジョイント、メッシュは必ず必要
    "upper_body"
    "lower_body"
    という名前のグループの場合は
    skl_pelvis_Cという名前で終わるジョイントが必要

    Args:
        group_name ([str]): ツールで作られるグループの名前
        nodes (list): 検査するノードリスト

    Returns:
        [str]: エラーメッセージ
        エラーがなければ空の文字列
    """
    _m = u""
    joint_nodes = []
    mesh_nodes = []
    pelvis_error = False
    if group_name in BODY_NAMES:
        pelvis_error = True

    for node in nodes:
        node_type = cmds.nodeType(node)
        if node_type == "joint":
            joint_nodes.append(node)
            if node.endswith(SKL_PELVIS_C) and pelvis_error:
                pelvis_error = False
        else:
            mesh_nodes.append(node)

    if not joint_nodes:
        _m += u"ジョイントノードがありません\n"
    if not mesh_nodes:
        _m += u"メッシュノードがありません\n"
    if pelvis_error:
        _m += u"[ {} ] ジョイントが必要です\n".format(SKL_PELVIS_C)

    return _m


def delete_empty_group(root_node):
    """空のグループノード削除
    深い階層順にソートするとこで正しく実行できる

    Args:
        root_node (str): 検査を開始するノード
    """
    children_nodes = cmds.listRelatives(root_node,
                                        allDescendents=True,
                                        fullPath=True,
                                        type="transform")
    # 階層の深い順にソートし、チェックすることで
    # 完全に空のグループを消せる
    for node in sorted(children_nodes,
                       key=lambda x: len(x.split("|")),
                       reverse=True):

        if not cmds.listRelatives(node, children=True):
            cmds.delete(node)


def open_scene(scene_name, _type):
    """Maya シーンを開く

    Args:
        scene_name ([str]): maya_scene_file_path
        _type ([str]): file type[mayaBinary, mayaAscii]
    """
    cmds.file(scene_name,
              open=True,
              force=True,
              executeScriptNodes=False,
              ignoreVersion=True,
              type=_type,
              options="v=0;")


def get_cyllista_config():
    """Cyllista のコンフィグ取得
    update_config を使うと、設定が存在すればそれを使い、
    無ければ再生成される
    """
    new_config = {"cyExportPhy": 1, "cyExportGfx": 1,
                  "cyExportAnm": -1, "cyExportAnmSkl": -1}

    ccn.update_config(new_config)
    return new_config


def check_p4state_yaml_files(path="", group_names=[]):
    """ファイルのチェックアウト状態を確認

    Args:
        path (str): ファイルパス
        group_names (list): 保存するグループのリスト

    ファイルパス+ グループ名 + .yaml

    Returns:
        [dict]: グループ名、[yaml_file_path, stat] の辞書
    """
    stat_dict = dict()
    if not os.path.exists(path):
        return
    if not group_names:
        return
    for group_name in group_names:
        yaml_path = os.path.join(
            path, group_name + ".yaml").replace(os.sep, '/')
        file_status_ext, stat, current_users = get_p4_file_state(yaml_path)
        stat_dict[group_name] = [yaml_path, stat]
    return stat_dict


def create_new_scene_path(group_name="", root_path="", parts_basename="", ext="", makedir=False):
    # 各パーツごとのディレクトリを作る場合はこれ
    if makedir:
        parts_path = os.path.join(root_path, group_name)
        if not os.path.exists(parts_path):
            os.makedirs(parts_path)
        new_scene = os.path.join(parts_path, parts_basename + "." + ext)
    else:
        new_scene = os.path.join(root_path, parts_basename + "." + ext)
    return new_scene.replace(os.sep, '/')


def check_parts_scene_state(group_name, root_path, basename, ext):
    """perfoce のチェックアウト状態を調べる

    Args:
        group_name ([str]): グループ名
        root_path ([str]]): 大元のパス
        basename ([str]): 拡張子抜きのファイル名
        ext ([str]): 拡張子

    Returns:
        [str, p4_stat]: maya_scene_file_path, p4_stat
    """
    # 管理ロック状態
    # (dict([('Z:/mtk/work/noshipping/characters/edit_test/player/00/001/model/arm/mdl_ply00_m_arm_001.ma',
    # {'action': 'latest', 'haveRev': 2, 'users': [], 'headRev': 2})]),
    # 'latest',
    # [])

    # 未管理
    # (dict([('Z:/mtk/work/noshipping/characters/edit_test/player/00/001/model/all/mdl_ply00_m_all_001.ma',
    # {'action': None, 'haveRev': 0, 'users': [], 'headRev': 0})]),
    # None,
    # [])

    # チェックアウト
    # (dict([('Z:/mtk/work/noshipping/characters/edit_test/player/00/001/model/body/mdl_ply00_m_body_001.ma',
    # {'action': 'checkout', 'haveRev': 2, 'users': ['ando_shoji'], 'headRev': 2})]),
    # 'checkout', ['ando_shoji'])

    new_scene = create_new_scene_path(
        group_name, root_path, basename, ext, False)

    file_status_ext, stat, current_users = get_p4_file_state(new_scene)

    return new_scene, stat


def save_parts_scene(group_name="", root_node="", root_path="", basename="", ext="", launch_editor=False):
    """グループ別にシーンを保存、保存は選択ノードを保存を使用
    Cyllista のコンフィグノードを生成し、保存している

    Args:
        group_name ([str]): ツールで作成したグループ名
        root_node ([str]): 選択するためのルートノード
        root_path ([str]): 元のシーンの一つ上のディレクトリパス
        basename ([str]): 元のシーンファイル名
        ext ([str]): 元の拡張子

    Returns:
        [str]: 保存したシーンパス
    """
    file_type = _type_dict[ext]

    if "_all" in basename:
        parts_basename = basename.replace("_all", "")
    else:
        parts_basename = basename

    parts_basename = parts_basename + "_" + group_name
    new_scene = create_new_scene_path(
        group_name, root_path, parts_basename, ext, False)

    file_status_ext, stat, current_users = get_p4_file_state(new_scene)
    _message = ""
    if not stat or stat == "checkout":
        cmds.select(root_node, r=True)
        cmds.rename(root_node, parts_basename)
        cmds.file(new_scene,
                  preserveReferences=True,
                  exportSelected=True,
                  force=True,
                  options="v=0;",
                  type=file_type)

        cmds.file(new_scene, open=True, force=True,
                  type=file_type, options="v=0;")
        _config = get_cyllista_config()
        _message = new_scene
        cmds.file(save=True)

        if launch_editor:
            # cyllista.export.export_for_current_scene(new_scene.lower(), _config)
            cyllista.export.exportWithinMaya(_config)
            try:
                launchModelEditor(new_scene)
            except Exception as e:
                print(e)
                pass

    return _message


def save_base_scene():
    cmds.file(save=True)


def set_root_joint_position(root_joint, joints):
    """joints の平均値に root_joint を移動させる

    Args:
        root_joint (str): ルートジョイント
        joints ([list]): ジョイントのリスト

    Returns:
        [str]: シーンルートに出されたルートジョイント
    """
    # _parent = cmds.listRelatives(root_joint, parent=True, fullPath=True)[0]
    pos_x = []
    pos_y = []
    pos_z = []
    for joint in joints:
        pos = cmds.xform(joint, q=True, translation=True, worldSpace=True)
        pos_x.append(pos[0])
        pos_y.append(pos[1])
        pos_z.append(pos[2])
    _root_joint = cmds.parent(root_joint, world=True)[0]
    cmds.xform(_root_joint,
               translation=[sum(pos_x) / len(pos_x),
                            sum(pos_y) / len(pos_y),
                            sum(pos_z) / len(pos_z)],
               worldSpace=True)
    # _root_joint = cmds.parent(_root_joint, _parent)
    return _root_joint


def check_scene_name(scene_name=""):
    """シーン名（シーンパス）をチェック「all」が入ったシーン名が対象
    分解して、パス、シーン名、拡張子を返す

    Args:
        scene_name (str, optional): [description]. Defaults to "".

    Returns:
        [str]: パーツのディレクトリパス、シーン名、拡張子
    """
    _m = u""

    if not scene_name:
        _m = u"シーンを開いてから実行してください"
        _d = gui_util.ConformDialog(message=_m)
        _d.exec_()
        return False, False, False

    scene_path, basename = os.path.split(scene_name)
    basename, ext = basename.split(".", 1)

    # if "all" not in basename:
    #     _m = u"シーン名に [ all ] が含まれてません"
    #     _d = gui_util.ConformDialog(message=_m)
    #     _d.exec_()
    #     return False, False, False

    # パーツごとのディレクトリ
    # root_path, _parts = os.path.split(scene_path)
    root_path = scene_path
    return root_path, basename, ext


def set_up_scene_path():
    """シーン名（シーンパス）取得

    Returns:
        [str]: シーンパス、パーツのディレクトリパス、
        元のシーン名、拡張子
    """
    scene_name = getCurrentSceneFilePath()
    root_path, basename, ext = check_scene_name(scene_name)
    if not ext:
        return False

    return scene_name, root_path, basename, ext


def check_parts_scene(parts_preset=None):
    """ツールで登録したグループの条件が適しているかの確認

    Args:
        parts_preset ([dict]): グループ名: グループのノード

    Returns:
        [bool]: エラーチェック
    """
    if not parts_preset:
        return True
    _errors = []

    for group_name, nodes in parts_preset.items():
        _m = check_group_nodes(group_name, nodes)
        if _m:
            _errors.append(u"[ {} ] グループには\n{}\n\n".format(group_name, _m))

    if _errors:
        _d = gui_util.ConformDialog(message="".join(_errors))
        _d.exec_()
        return True
    else:
        return False


def delete_nodes(nodes):
    for node in nodes:
        if cmds.objExists(node):
            cmds.delete(node)


def all_save_parts_scene(parts_preset=None,
                         scene_name="",
                         root_path="",
                         basename="",
                         ext=""):
    """グループごとにシーン保存する準備と保存

    Args:
        parts_preset ([dict], optional): [description]. Defaults to None.
        scene_name (str, optional): [description]. Defaults to "".
        root_path (str, optional): [description]. Defaults to "".
        basename (str, optional): [description]. Defaults to "".
        ext (str, optional): [description]. Defaults to "".

    Returns:
        [type]: [description]
    """

    if(not parts_preset or
            not scene_name or
            not root_path or
            not basename or
            not ext):
        return True

    file_type = _type_dict[ext]

    # 各グループのメッシュを持ったトランスフォームノード
    group_mesh_transforms = dict()

    # グループ内の一番親となるノードを集める
    group_parent_joint = dict()

    # グループに含まれていないノードを集めて消すための辞書
    delete_transform_nodes = dict()

    group_scene_p4_states = dict()

    root_joint = cmds.ls("{}".format(ROOT_JOINT), type="joint")[0]
    root_node = cmds.listRelatives(root_joint, parent=True, path=True)[0]
    _root_children = cmds.listRelatives(
        root_joint, children=True, path=True, type="joint")

    model_node = cmds.ls(MODEL_GROUP, type="transform")[0]
    meshes = cmds.listRelatives(
        model_node, allDescendents=True, path=True, type="mesh")
    meshes = [x for x in meshes if x and not cmds.getAttr(
        "{}.intermediateObject".format(x))]
    mesh_transforms = [cmds.listRelatives(x, parent=True)[0] for x in meshes]

    _warning_message = []
    for group_name, nodes in parts_preset.items():
        # perforce の管理状態を確認
        _new_scene_name, stat = check_parts_scene_state(
            group_name, root_path, basename, ext)
        if stat and stat != "checkout":
            _warning_message.append(_new_scene_name)

        group_scene_p4_states[group_name] = [_new_scene_name, stat]
        _mesh_transforms = []
        _delete_meshes = []
        _parent_joint = []
        _delete_joints = _root_children[:]

        for mesh in mesh_transforms:
            if mesh not in nodes and mesh not in _delete_meshes:
                _delete_meshes.append(mesh)
        for node in nodes:
            if cmds.nodeType(node) != "joint":
                if node not in _mesh_transforms:
                    _mesh_transforms.append(node)

            else:
                if node in _root_children:
                    _delete_joints.remove(node)
                _parent = cmds.listRelatives(node,
                                             parent=True,
                                             path=True,
                                             type="transform")
                _children = cmds.listRelatives(node,
                                               children=True,
                                               path=True,
                                               type="transform")

                if _parent:
                    _parent = _parent[0]
                    if not _parent in nodes and _parent not in _parent_joint:
                        _parent_joint.append(node)
                if _children:
                    for _cld in _children:
                        if _cld not in nodes:
                            _delete_joints.append(_cld)

            group_mesh_transforms[group_name] = _mesh_transforms
            group_parent_joint[group_name] = _parent_joint
            delete_transform_nodes[group_name] = _delete_meshes + \
                _delete_joints

    if _warning_message:
        _m = u"以下のファイルがチェックアウトされています\n\n"
        _m += u"{}".format(u"{}\n".join(_warning_message))
        _m += u"\n\n処理を続けますか？"
        _d = gui_util.ConformDialogResult(title=u"チェックアウトされている", message=_m)
        result = _d.exec_()
        if not result:
            return

    _message = []
    for group_name, _mesh_transforms in group_mesh_transforms.items():
        _new_scene_name, stat = group_scene_p4_states.get(group_name)
        if stat and stat != "checkout":
            continue
        if root_joint not in group_parent_joint[group_name]:
            _joints = cmds.parent(group_parent_joint[group_name], world=True)
            root_joint = set_root_joint_position(root_joint, _joints)
            root_joint = cmds.parent(root_joint, root_node)[0]
            cmds.parent(_joints, root_joint)

        delete_nodes(delete_transform_nodes[group_name])
        model_node = cmds.parent(model_node, world=True)[0]
        model_node = cmds.parent(model_node, root_node)[0]
        delete_empty_group(model_node)

        _m = save_parts_scene(group_name, root_node, root_path, basename, ext)
        if _m:
            _message.append(_m)
        open_scene(scene_name, file_type)

    if _message:
        _m = u"以下のファイルを保存しました\n\n"
        _m += u"{}".format(u"\n".join(_message))
        _d = gui_util.ConformDialog(message=_m)
        _d.exec_()


def get_dag_meshfns(meshes):
    """API2.0 のdagPath を取る

    Args:
        meshes ([list]): Maya のメッシュシェイプ

    Returns:
        [meshFn, dagPath]:
    """
    sel_list = om2.MSelectionList()
    for mesh in meshes:
        sel_list.add(mesh)

    _dags = []
    # mesh_fns = []
    # _deps = []

    for i in range(sel_list.length()):
        dag_path = sel_list.getDagPath(i)
        # dep = sel_list.getDependNode(i)
        _dags.append(dag_path)
        # _deps.append(dep)
        # mesh_fns.append(om2.MFnMesh(dag_path))
    return _dags


def joint_check(joints=[]):
    """helper ボーンが登録された場合、その親の骨のウェイトが無い場合に
    登録がされないのでそれを登録する仕組み

    Args:
        joints (list): ジョイントリスト

    Returns:
        [list]: 受け取ったジョイントリストを返す
    """
    for joint in joints:
        if "helper" in joint:
            parent = cmds.listRelatives(
                joint, parent=True, path=True, type="joint")[0]
            if "helper" not in parent:
                joints.append(parent)
    return joints


def get_influence_joints_api2(mesh_nodes=[], _joints=[]):
    """mesh_nodes にインフルエンスのウェイトが振られているジョイントを返す
    API2.0 版

    Args:
        mesh_nodes (list): Maya のメッシュを持ったトランスフォームノード
        _joints (list): 既にツリーに登録されているものを排除するため

    Returns:
        [type]: [description]
    """

    # トランスフォームノードからメッシュシェイプを抽出
    _meshes = cmds.listRelatives(
        mesh_nodes, allDescendents=True, fullPath=True, type="mesh")
    if not _meshes:
        return

    # 中間オブジェクトを抜かしている
    _meshes = [x for x in _meshes if not cmds.getAttr(
        "{}.intermediateObject".format(x))]
    if not _meshes:
        return

    # API2.0 のdagPath を抽出
    _dags = get_dag_meshfns(_meshes)

    # インフルエンスとして登録してあり、かつ、ウェイトの値が振られたジョイントを取得する
    joints = set()
    with gui_util.ProgressWindowBlock(title='Get Joints', maxValue=len(_dags)) as prg:
        prg.step(1)
        for _dag in _dags:
            prg.status = '{}'.format(_dag.fullPathName())
            _historys = [x for x in cmds.listHistory(
                _dag) if cmds.nodeType(x) == "skinCluster"]
            prg.step(1)
            if _historys:
                skin_cluster = _historys[0]
                prg.status = '{}'.format(skin_cluster)
                if prg.is_cancelled():
                    break
                skinNode = om2.MGlobal.getSelectionListByName(
                    skin_cluster).getDependNode(0)
                skinFn = om2anim.MFnSkinCluster(skinNode)

                singleIdComp = om2.MFnSingleIndexedComponent()
                vertexComp = singleIdComp.create(om2.MFn.kMeshVertComponent)
                infDags = skinFn.influenceObjects()

                for x in range(len(infDags)):
                    joint = infDags[x].fullPathName()
                    joint_short_name = joint.rsplit("|", 1)[-1]
                    if joint_short_name in _joints or joint_short_name in joints:
                        continue
                    vtx_weights = skinFn.getWeights(_dag, vertexComp, x)
                    for weight in vtx_weights:
                        if round(weight, 6):
                            joints.add(joint_short_name)
                            break
    _joints = joint_check(list(joints))
    return _joints
    # return list(joints)


def get_influence_joints(mesh_nodes):
    """mesh_nodes にインフルエンスのウェイトが振られているジョイントを返す
    Maya コマンド版

    Args:
        mesh_nodes ([type]): [description]

    Returns:
        [type]: [description]
    """
    _meshes = cmds.listRelatives(
        mesh_nodes, allDescendents=True, fullPath=True, type="mesh")
    if not _meshes:
        return
    _meshes = [x for x in _meshes if not cmds.getAttr(
        "{}.intermediateObject".format(x))]
    if not _meshes:
        return
    _skinClusters = [x for x in cmds.listHistory(
        _meshes) if cmds.nodeType(x) == "skinCluster"]
    joints = []
    _range = len(_skinClusters)
    with gui_util.ProgressWindowBlock(title='Get Joints', maxValue=_range) as prg:
        prg.status = 'Get joints'
        prg.step(1)
        for i, _skinCluster in enumerate(_skinClusters):
            prg.step(1)
            prg.status = '{}'.format(_skinCluster)
            if prg.is_cancelled():
                break
            inf = cmds.skinCluster(_skinCluster, q=True, influence=True)
            if inf:
                joints.extend(inf)
    return joints
