from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import subprocess
import webbrowser
from pathlib import Path

import maya.api.OpenMaya as om2
import maya.cmds as cmds

from mtk.utils import getCurrentSceneFilePath

from . import gui_util
from . import TOOL_NAME


def select_list(nodes=[]):
    """選択の切り替え

    Args:
        nodes (list): mesh nodes
    """
    if nodes:
        cmds.select([cmds.listRelatives(x, parent=True,
                    type="transform")[0] for x in nodes], r=True)


def get_current_selections():
    """現在選択しているトランスフォームノード
    からメッシュノードの取得

    Returns:
        [list]: mesh nodes
    """
    selections = cmds.ls(sl=True, type="transform")
    if not selections:
        return

    mesh_nodes = []
    for _node in selections:
        _meshes = cmds.listRelatives(
            _node, allDescendents=True, fullPath=True, type="mesh")
        if _meshes:
            _meshes = [x for x in _meshes if not cmds.getAttr(
                "{}.intermediateObject".format(x))]
            if _meshes:
                mesh_nodes.extend(_meshes)
    return mesh_nodes


def get_transform_node(mesh_node=""):
    """メッシュノードを受け取り親のトランスフォームノードを返す

    Args:
        mesh_node (str): maya mesh shape node

    Returns:
        [str]: maya transform node
    """
    transform_node = cmds.listRelatives(
        mesh_node, parent=True, type="transform", fullPath=True)
    if transform_node:
        return transform_node[0]
    else:
        return transform_node


def open_export_directory(directory_path=""):
    """directory_path をウィンドウズエクスプローラで開く

    Args:
        directory_path (str):

    Returns:
        [str]: メッセージ
    """

    _message = ""
    if directory_path:
        if not os.path.exists(directory_path):
            _message = f"{directory_path.replace(os.sep, '/')}\nは存在しません"
        else:
            try:
                subprocess.Popen(
                    ['explorer', os.path.normpath(directory_path)])
            except Exception as e:
                print(e)
                _message = "Windows Explorer で開けませんでした"

    return _message


def open_help_site() -> None:
    """ヘルプサイト表示
    """
    _web_site = "https://wisdom.cygames.jp/pages/viewpage.action?pageId=142529087"
    webbrowser.open(_web_site)


def get_current_directory(current_directory: str) -> str:
    """ファイルの出力先設定
    mutsu 仕様の「model」ディレクトリが存在する場合に
    「workbench」「houdini_maps_baker」
    のディレクトリを作る

    Args:
        current_directory (str): すでにラインに入力がある場合はパスが入ってくる

    Returns:
        [str]: 出力先のディレクトリパス
    """
    _mtk_work_flag = False
    _workbench = "workbench"
    _export_directory = "houdini_maps_baker"
    _model_directory = "model"

    # エクスポートパスを設定していない場合
    if not current_directory and not os.path.exists(current_directory):
        # 開いているシーンから取得
        current_directory = getCurrentSceneFilePath()
        if not current_directory:
            # シーンを開いていない場合はアクティブプロジェクト
            current_directory = cmds.workspace(q=True, active=True)
            if not current_directory:
                # アクティブプロジェクトもない場合はローカルのマイドキュメント
                current_directory = os.getenv("HOME")
        else:
            # シーンが開かれている場合一つ上のディレクトリ（プロジェクトでは「model」となるはず）
            current_directory = os.path.split(current_directory)[0]

    current_directory = Path(current_directory)

    # 一つ上のディレクトリから、子のディレクトリを探り「model」を探す
    # あれば _mtk_work_flag を True
    for _path in current_directory.parents[0].iterdir():
        if _path.stem == _model_directory:
            _mtk_work_flag = True
            break

    # _mtk_work_flag が True の場合プロジェクト仕様のディレクトリ構造とみなし
    # 「workbench」フォルダ、「houdini_maps_baker」フォルダを生成パスに追加
    if _mtk_work_flag:
        current_directory = current_directory.parents[1]
        current_directory = current_directory / _workbench / _export_directory

        if not current_directory.exists():
            current_directory.mkdir(parents=True, exist_ok=True)

    return str(current_directory).replace(os.sep, '/')


def node_exists(nodes=[]):
    """ノード有無の検証

    Args:
        nodes (list): maya dag nodes

    Returns:
        [list]: 存在しないノードをリストで返す
    """
    not_exists = []
    for node in nodes:
        if cmds.objExists(node):
            not_exists.append(node)
    return not_exists


def check_bake_items(current_directory="", target_items=[], source_items=[]):
    """ベイク前の検証
    問題なければ True

    Args:
        current_directory (str): 画像の出力先
        target_items (list): ターゲットとなるメッシュシェイプ
        source_items (list): ソースとなるメッシュシェイプ

    Returns:
        [type]: [description]
    """

    # エクスポートパスの確認
    if not current_directory or not os.path.exists(current_directory):
        _d = gui_util.ConformDialog(title=TOOL_NAME,
                                    message="Not Exists Export Path")
        _d.exec_()
        return

    # ターゲット、ソースが空で無いかの確認
    if not target_items:
        _d = gui_util.ConformDialog(title=TOOL_NAME,
                                    message="Not Exists Targets")
        _d.exec_()
        return
    if not source_items:
        _d = gui_util.ConformDialog(title=TOOL_NAME,
                                    message="Not Exists Sources")
        _d.exec_()
        return

    # ターゲット、ソースが現在のシーンに存在するかの確認
    target_exists = node_exists(target_items)
    if target_exists:
        _d = gui_util.ConformDialog(title=TOOL_NAME,
                                    message=f'Target Meshes\n[ {", ".join(target_exists)} ]\nis not exists')
        _d.exec_()
        return
    source_exists = node_exists(source_items)
    if source_exists:
        _d = gui_util.ConformDialog(title=TOOL_NAME,
                                    message=f'Source Meshes\n[ {", ".join(source_exists)} ]\nis not exists')
        _d.exec_()
        return

    return True


def get_shading_group(souece_meshes: list) -> dict:
    """メッシュノードからシェーディンググループを取得

    Args:
        souece_meshes (list, optional): [description]. Defaults to [].

    Returns:
        dict: [description]
    """
    mesh_shading_group = {}
    for mesh in souece_meshes:
        _shading_engines = cmds.listConnections(
            mesh, source=False, destination=True, type='shadingEngine')
        if _shading_engines:
            mesh_shading_group[mesh] = _shading_engines
    return mesh_shading_group


def get_leaf_connection(node: str) -> str:
    """コネクションでつながっているノードを返す

    Args:
        node (str): maya dg node

    Returns:
        str: maya dg node

    Yields:
        Iterator[str]: maya dg node
    """
    children = cmds.listConnections(node, source=True, destination=False)
    if children:
        yield children[0]
        for p in get_leaf_connection(children):
            yield p


def get_textures(shading_groups: list) -> dict:
    """シェーディンググループにつながったテクスチャを返す
    color: color につながっているもの
    alpha: transparency につながっているもの

    Args:
        shading_groups (list): maya shading engine

    Returns:
        dict: shading engine: texturepath dict
    """
    shading_group_textures = {}

    for shading_group in shading_groups:
        textures = {}
        _connections = cmds.listConnections(
            shading_group, source=True, destination=False)

        if not _connections:
            continue

        materials = cmds.ls(_connections, materials=True)

        if not materials:
            continue

        for material in materials:
            connections = cmds.listConnections(
                material, source=True, destination=True, connections=True)

            if not connections:
                continue

            # 例:
            # plugs: [ph_tex_ply00_w_001_hair_k_depth_mtl.color, ph_tex_ply00_w_001_hair_k_depth_mtl.transparency]
            # plug_nodes: [blendColors16, reverse16]
            plugs = connections[0::2]
            plug_nodes = connections[1::2]

            for plug, plug_node in zip(plugs, plug_nodes):
                texture_path = ""

                if cmds.nodeType(plug_node) == "file":
                    texture_path = cmds.getAttr(f'{plug_node}.ftn')
                else:
                    for _leaf in get_leaf_connection(plug_node):
                        if cmds.nodeType(_leaf) == "file":
                            texture_path = cmds.getAttr(
                                f'{_leaf}.ftn')

                if not texture_path:
                    continue

                # color とtransparency を検出して振り分ける
                if plug.endswith("color"):
                    textures["color"] = texture_path
                elif plug.endswith("transparency"):
                    textures["alpha"] = texture_path

        shading_group_textures[shading_group] = textures

    return shading_group_textures
