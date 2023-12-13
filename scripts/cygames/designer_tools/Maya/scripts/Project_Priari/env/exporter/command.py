# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import zip
    from importlib import reload
except:
    pass

import os

import maya.api.OpenMaya as om
import maya.cmds as cmds

from ...base_common import classes as base_class
from ...base_common import utility as base_utility
from ..common import command as env_cmd

reload(base_class)
reload(base_utility)
reload(env_cmd)


def execute_batch(paths, nodes, should_trims):
    """mayabatchの実行

    mayaから実行する関数

    """

    cmd = ''
    cmd += 'import Project_Priari.env.exporter;'
    cmd += 'reload(Project_Priari.env.exporter);'
    cmd += 'Project_Priari.env.exporter.batch_export();'

    base_utility.simple_batch.execute(cmd, True, paths=paths, nodes=nodes, should_trims=should_trims)


def batch_export():
    """バッチエクスポート

    mayabatchから実行する関数

    """

    paths = base_utility.simple_batch.get_param_value('paths')
    nodes = base_utility.simple_batch.get_param_value('nodes')
    should_trims = [v == 'True' for v in base_utility.simple_batch.get_param_value('should_trims')]
    keep_temp_file = False

    for path, node, should_trim in zip(paths, nodes, should_trims):
        fbx_path = env_cmd.get_fbx_path(path, node)

        if not open_temp_file(path):
            continue

        try:
            export(node, fbx_path, should_trim)
        except Exception as e:
            print(e)


def export(target_node, fbx_path, should_trim):
    """エクスポート

    :param target_node: 対象ノード名
    :type target_node: str
    :param fbx_path: 出力パス
    :type fbx_path: str
    :param should_trim: フェースの削除を実行するか
    :type should_trim: bool
    """

    unite_mesh(target_node)

    if should_trim:
        trim_mesh(target_node)

    delete_color_set(target_node)

    export_fbx(target_node, fbx_path)


def trim_mesh(target_node):
    """フェースの削除

    :param target_node: 対象ノード名
    :type target_node: str
    """

    backfaces = env_cmd.get_face_by_alpha(target_node, env_cmd.BACKFACE_COLOR_SET)

    face_str = to_face_str(target_node, backfaces.getElements())

    if face_str:
        cmds.polyDelFacet(face_str, ch=False)


def delete_color_set(target_node):
    """カラーセットの削除

    :param target_node: 対象ノード名
    :type target_node: str
    """

    env_cmd.delete_color_set(target_node, env_cmd.BACKFACE_COLOR_SET)


def to_face_str(target_node, indices):
    """メッシュ文字列を返す

    :param target_node: 対象ノード
    :type target_node: str
    :param indices: 対象インデックス
    :type target_node: int
    :return: メッシュ文字列
    :rtype: list[str]
    """

    return ['{}.f[{}]'.format(target_node, index) for index in indices]


def unite_mesh(target_node):
    """メッシュの結合処理

    :param target_node: 対象ノード
    :type target_node: str
    """

    # ノード以下に複数のシェイプがある場合は結合する
    shape_nodes = cmds.listRelatives(target_node, ad=True, typ='shape')

    if len(shape_nodes) > 1:
        # 元のノード名と被るため、nameフラグは使わずに後から名前を指定
        united_node = cmds.polyUnite(target_node, ch=False)
        cmds.rename(united_node, target_node)


def export_fbx(target_node, fbx_path):
    """FBXファイルの出力

    :param target_node: 対象ノード名
    :type target_node: str
    :param fbx_path: 出力パス
    :type fbx_path: str
    """

    exporter = base_class.fbx_exporter.FbxExporter()

    exporter.target_node_list = [target_node]
    exporter.fbx_file_path = fbx_path

    exporter.export()


def open_temp_file(original_path, keep=False):
    """一時ファイルを開く

    :param original_path: 対象ファイルパス
    :type original_path: str
    :return: 一時ファイルが読み込めたか
    :rtype: bool
    """

    temp_path = base_utility.file.open_temp(original_path)

    if temp_path is None:
        return False

    if not keep:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return True
