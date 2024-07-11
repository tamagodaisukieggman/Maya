# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import os

import maya.cmds as cmds
import maya.mel as mel

from . import utility

try:
    # Maya2022-
    from importlib import reload
except Exception:
    pass

reload(utility)


def open_as_new_scene(path, exec_script_node, exec_set_project, exec_fix_tex_path):
    """新規シーンとして開く

    Args:
        path (str): 開くパス
        exec_script_node (bool): スクリプトノードを実行するか
        exec_set_project (bool): scenesの親をプロジェクトにセットするか
        exec_fix_tex_path (bool): テクスチャパスが切れていたら修正するか
    """

    if not os.path.exists(path):
        return

    result = mel.eval('saveChanges("");')
    if not result:
        return

    load_need_plugin(path)
    cmds.file(path, open=True, f=True, executeScriptNodes=exec_script_node)
    add_recent_files(path)

    if exec_fix_tex_path:
        fix_texture_path(path)
    if exec_set_project:
        set_project(path)


def create_reference(path, namespace, exec_script_node, exec_fix_tex_path):
    """リファレンスとして開く

    Args:
        path (str): 開くパス
        namespace (str): ネームスペース
        exec_script_node (bool): スクリプトノードを実行するか
        exec_fix_tex_path (bool): テクスチャパスが切れていたら修正するか
    """

    if not os.path.exists(path):
        return

    load_need_plugin(path)

    if not namespace:
        cmds.file(
            path,
            ignoreVersion=True,
            reference=True,
            executeScriptNodes=exec_script_node)
    else:
        cmds.file(
            path,
            ignoreVersion=True,
            reference=True,
            namespace=namespace,
            executeScriptNodes=exec_script_node)

    add_recent_files(path)

    if exec_fix_tex_path:
        fix_texture_path(path)


def import_file(path, namespace, exec_script_node, exec_fix_tex_path):
    """インポートとして開く

    Args:
        path (str): 開くパス
        namespace (str): ネームスペース
        exec_script_node (bool): スクリプトノードを実行するか
        exec_fix_tex_path (bool): テクスチャパスが切れていたら修正するか
    """

    if not os.path.exists(path):
        return

    load_need_plugin(path)

    if not namespace:
        cmds.file(path, i=True, executeScriptNodes=exec_script_node)
    else:
        cmds.file(path, i=True, namespace=namespace, executeScriptNodes=exec_script_node)

    add_recent_files(path)

    if exec_fix_tex_path:
        fix_texture_path(path)


def set_project(scene_path):
    """scenesの親をプロジェクトにセット

    Args:
        scene_path (str): 対象シーンファイルのパス
    """

    root_split = os.path.dirname(scene_path).rsplit('\\scenes', 1)

    if root_split:
        project_path = utility.normalize_path(root_split[0])

        mel.eval('setProject ' + '"' + project_path + '"')
        print('project set : ', project_path)


def fix_texture_path(path):
    """テクスチャパスが切れていたら修正

    Args:
        path (str): シーンのパス
    """

    file_nodes = cmds.ls(type='file')

    if not file_nodes:
        return

    for file_node in file_nodes:

        if os.path.exists(cmds.getAttr(file_node + '.fileTextureName')):
            continue

        dir_path = ''
        if cmds.referenceQuery(file_node, isNodeReferenced=True) == 1:
            dir_path = cmds.referenceQuery(file_node, filename=True).split('scenes')[0] + 'sourceimages/'
        else:
            dir_path = path.split('scenes')[0] + 'sourceimages/'

        path_old = cmds.getAttr(file_node + '.fileTextureName')
        tex_name = os.path.basename(path_old)

        path_new = os.path.join(dir_path, tex_name)

        if os.path.exists(path_new):
            cmds.setAttr(file_node + '.fileTextureName', path_new, type='string')

    print('fix texture path')


def add_recent_files(scene_path):
    """最近使用したファイルに追加

    Args:
        scene_path (str): 追加するシーンのパス
    """

    file_types = cmds.file(scene_path, q=True, type=True)
    if not file_types:
        return
    mel.eval('addRecentFile("{}", "{}");'.format(utility.normalize_path(scene_path), file_types[0]))


def load_need_plugin(open_file_path):
    """開く際に必要なプラグインのロード
    現状FBXのみ

    Args:
        open_file_path (str): 開くシーンのパス
    """

    ext = os.path.splitext(open_file_path)[-1].lower()
    if ext == '.fbx':
        load_fbx_plugin()


def load_fbx_plugin():
    """fbxプラグインのロード
    """

    if not cmds.pluginInfo('fbxmaya', query=True, loaded=True):
        cmds.loadPlugin('fbxmaya.mll')
