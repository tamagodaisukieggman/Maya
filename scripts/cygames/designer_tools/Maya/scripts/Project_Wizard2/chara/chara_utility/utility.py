# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
try:
    # Maya 2022-
    from builtins import str
except Exception:
    pass
import os
import maya.cmds as cmds

def is_selection_root_transform():
    """選択がメッシュを持たないRootのトランスフォームならTrueを返す。
    親がある、もしくはメッシュがあるならFalse。
    Returns:
        _type_: bool
    """
    parent = cmds.listRelatives(cmds.ls(sl=True), p=True, fullPath=True)
    shapes = cmds.listRelatives(cmds.ls(sl=True), shapes=True, fullPath=True)
    if not parent and not shapes:
        return True
    return False


def get_selected_mesh_transforms(except_outline=False):
    """選択されているメッシュのトランスフォームのリストを返す
    子ノードにメッシュがあっても選択されていなければ返さない
    Returns:
        _type_: [transform]
    """
    selected_mesh_transforms = []
    selection = cmds.ls(sl=True)
    if not selection:
        return []
    rel_shapes = cmds.listRelatives(selection, shapes=True, fullPath=True)
    if not rel_shapes:
        return []
    for shape in rel_shapes:
        parent_transforms = cmds.listRelatives(shape, p=True, fullPath=True)
        if parent_transforms:
            if except_outline:
                if shape.endswith('_Outline'):
                    continue
            selected_mesh_transforms.append(parent_transforms[0])
    return list(set(selected_mesh_transforms))


def list_child_mesh_transforms(root_node, except_outline=False):
    """root_node配下のmeshのtransformのリスト(fullPath)を返す
    Args:
        root_node (str): 例：chr0004_00
    Returns:
        str[]: root_node配下のメッシュtransformのリスト
    """
    orig_selection = cmds.ls(sl=True)
    mesh_transforms = []
    if root_node:
        children = cmds.listRelatives(root_node, children=True,fullPath=True)
        cmds.select(children, hierarchy=True)
        meshes = cmds.ls(sl=True, long=True, type='mesh')
        if not meshes:
            return []
        for mesh in meshes:
            transforms = cmds.listRelatives(mesh, p=True, fullPath=True)
            if transforms:
                transform = transforms[0]
                if except_outline:
                    if transform.endswith('_Outline'):
                        continue
                mesh_transforms.append(transform)
        mesh_transforms = list(set(mesh_transforms))
    cmds.select(orig_selection) # 選択状態を元に戻す
    return mesh_transforms


def get_root_nodes(nodes):
    """nodes(現在の選択リストを想定)から再帰的に辿ってrootノードのリストを返す
    選択オブジェクトが複数の場合、それぞれのrootノードを調べ重複しないリストを返す
    Args:
        nodes (str[]): 選択リスト
    Returns:
        str[]: 
    """
    found_roots = []
    for node in nodes:
        root = get_root_node(node)
        if root:
            found_roots.append(root)
    return list(set(found_roots))


def get_root_node(item):
    """itemから再帰的に辿りrootノードを返す
    Args:
        item (str): シーン内のノード
    Returns:
        str: rootノードの名前
    """
    if not item:
        return
    if type(item) is list:
        cmds.warning('Usage: get_root_node にはリストではなくシーン内のオブジェクト名を1つ渡してください')
        return
    parents = cmds.listRelatives(item, parent=True, fullPath=True)
    if not parents:
        return item
    else:
        for node in parents:
            return get_root_node(node)


def get_current_project_dir():
    """
    現在Mayaで開いているシーンのプロジェクトフォルダへのパスを返す
    :return: string. Path to the current Maya scene project.
    """
    proj_path = ''
    try:
        proj_path = cmds.file(q=True, sn=True)
        if proj_path:
            proj_path = os.path.abspath(os.path.join(proj_path, os.pardir))
            if os.path.basename(proj_path) == 'scenes':
                proj_path = os.path.abspath(os.path.join(proj_path, os.pardir))
            else:
                cmds.warning('Error: 現在のシーンはscenesフォルダに入っていません')
    except Exception as e:
        cmds.error(str(e))
    return proj_path

def get_folder_path() -> str:
    """
    MayaのfileDialog2を使って任意のフォルダパスを取得し、POSIX形式で返す。
    Args: なし
    Returns:
        str: 選択されたフォルダのPOSIX形式のパス
    """
    folder_path = cmds.fileDialog2(dialogStyle=2, fileMode=3, okCaption='Select Folder')[0]
    posix_folder_path = folder_path.replace('\\', '/')
    return posix_folder_path

def get_short_name(path_name:str) -> str:
    """pathからshort nameを取得

    Args:
        path_name (str): ノードのpathを渡す

    Returns:
        str: short nameを返す
    """
    short_name = path_name.split("|")[-1]
    return short_name

def get_namespace(node: str) -> str:
    """
    対象のノードのネームスペースを取得します。
    Args:
        node (str): ネームスペースを取得したいノードの名前
    Returns:
        str: ノードのネームスペース、ノードがネームスペースに属していない場合は空の文字列
    """
    # ノード名を":"で分割
    split_name = node.split(":")
    # ネームスペースが存在する場合
    if len(split_name) > 1:
        # 最後の要素(ノードの本名)を除いたものをネームスペースとする
        namespace = ":".join(split_name[:-1])
        return namespace
    else:
        # ネームスペースが存在しない場合は空の文字列を返す
        return ""