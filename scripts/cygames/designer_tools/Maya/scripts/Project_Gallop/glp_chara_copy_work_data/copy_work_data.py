# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function


import os
import shutil

import maya.cmds as cmds
import maya.mel as mel

from .. import base_common
from ..base_common import utility as base_utility

from . import const
from . import utility

try:
    # Maya2022-
    from builtins import object
    from importlib import reload
except Exception:
    pass

reload(base_common)
reload(const)
reload(utility)


def copy_datas(copy_data_infos):
    """コピーデータ情報をもとにコピーを実行

    Args:
        copy_data_infos ([CopyDataInfo]): コピーデータ情報のリスト
    """

    text_replace_target_datas = []
    scene_replace_target_datas = []
    copy_failed_infos = []

    for copy_data_info in copy_data_infos:

        # ファイル自体のコピー
        if not copy_file(copy_data_info.src_path, copy_data_info.dst_path):
            copy_failed_infos.append(copy_data_info)
            continue

        # 拡張子からコピー後の処理別にリストに追加していく
        if os.path.splitext(copy_data_info.dst_path)[-1] in const.EXT_TEXT_LIST:
            text_replace_target_datas.append(copy_data_info)

        if os.path.splitext(copy_data_info.dst_path)[-1] in const.EXT_SCENE_LIST:
            scene_replace_target_datas.append(copy_data_info)

    # テキスト編集による置換
    for copy_data_info in text_replace_target_datas:
        replace_text(copy_data_info.dst_path, copy_data_info.replace_str_old, copy_data_info.replace_str_new)

    # シーンを開いて各種置換を実行
    if scene_replace_target_datas:
        scene_data_replace(scene_replace_target_datas, exe_with_batch=True)


def copy_file(src, dst):
    """ファイルのコピー

    Args:
        src (str): コピー元のパス
        dst (str): コピー先のパス

    Returns:
        bool: 結果
    """

    if not os.path.exists(src) and not os.path.isfile(src):
        return False

    dst_dir = os.path.dirname(dst)

    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    try:
        shutil.copyfile(src, dst)
    except Exception:
        return False

    return True


def replace_text(target_path, old_str, new_str):
    """テキスト編集による文字列置換

    Args:
        target_path (str): 置換するファイルパス
        old_str (str): 置換前
        new_str (str): 置換後
    """

    if not os.path.exists(target_path) and not os.path.isfile(target_path):
        return
    if old_str == new_str:
        return

    org_text = ''

    try:
        with open(target_path) as f:
            org_text = f.read()
    except Exception:
        return

    new_text = org_text.replace(old_str, new_str)

    try:
        with open(target_path, mode='w') as f:
            f.write(new_text)
    except Exception:
        return

    return


def scene_data_replace(copy_data_infos, exe_with_batch=True):
    """シーンを開いて各種文字列置換を行う

    Args:
        copy_data_infos ([CopyDataInfo]): コピーデータ情報のリスト
        exe_with_batch (bool, optional): バッチ処理をするか.Falseはテスト用. Defaults to True.
    """

    target_paths = []
    old_strs = []
    new_strs = []

    for copy_data_info in copy_data_infos:

        # 置換が発生しない場合はスキップ
        if copy_data_info.replace_str_old == copy_data_info.replace_str_new:
            continue

        target_paths.append(copy_data_info.dst_path)
        old_strs.append(copy_data_info.replace_str_old)
        new_strs.append(copy_data_info.replace_str_new)

    if not target_paths:
        return

    if exe_with_batch:
        base_utility.simple_batch2.execute_mayabatch(
            'Project_Gallop.glp_chara_copy_work_data.copy_work_data',
            'scene_data_replace_batch_entry()',
            True,
            target_file_paths=target_paths,
            old_strs=old_strs,
            new_strs=new_strs,)

    else:
        for path, old_str, new_str in zip(target_paths, old_strs, new_strs):
            scene_data_replace_core(path, old_str, new_str)


def scene_data_replace_batch_entry():
    """バッチ処理から呼び出すようのメソッド
    """

    kwargs = base_utility.simple_batch2.get_kwargs()
    target_file_paths = []
    old_strs = []
    new_strs = []

    if kwargs:
        target_file_paths = kwargs['target_file_paths']
        old_strs = kwargs['old_strs']
        new_strs = kwargs['new_strs']

    for path, old_str, new_str in zip(target_file_paths, old_strs, new_strs):
        scene_data_replace_core(path, old_str, new_str)


def scene_data_replace_core(path, old_str, new_str):
    """シーンを開いて各種文字列置換を行う処理本体

    Args:
        path (str): シーンパス
        old_str (str): 置換前
        new_str (str): 置換後
    """

    # プラグインが必要ならロード
    utility.load_need_plugin(path)

    ext = os.path.splitext(path)[-1].lower()

    # シーンを開く
    if ext == '.fbx':
        cmds.file(new=True, f=True)
        mel.eval('FBXImport -file "{}";'.format(path))
    else:
        cmds.file(path, open=True, iv=True, f=True, executeScriptNodes=False)

    # 各種置換処理
    replace_reference(old_str, new_str)
    replace_namespace(old_str, new_str)
    replace_node_name(old_str, new_str)
    replace_file_path(old_str, new_str)

    # 保存
    if ext == '.fbx':
        mel.eval('FBXExport -f "' + path + '"')
    else:
        cmds.file(save=True, f=True)


def replace_reference(old_str, new_str):
    """リファレンスパスの置換

    Args:
        old_str (str): 置換前
        new_str (str): 置換後
    """

    ref_nodes = cmds.ls(rf=True)
    for ref_node in ref_nodes:

        try:
            ref_path = cmds.referenceQuery(ref_node, f=True)
        except Exception:
            continue

        if ref_path.find(old_str) < 0:
            continue

        new_ref_path = ref_path.replace(old_str, new_str)
        cmds.file(new_ref_path, lr=ref_node)


def replace_namespace(old_str, new_str):
    """ネームスペースの置換

    Args:
        old_str (str): 置換前
        new_str (str): 置換後
    """

    all_ref_files = cmds.file(q=True, reference=True)

    for ref_file in all_ref_files:
        namespace = cmds.file(ref_file, q=True, namespace=True)

        if namespace.find(old_str) >= 0:
            cmds.namespace(ren=[namespace, namespace.replace(old_str, new_str)])


def replace_node_name(old_str, new_str):
    """ノード名の置換

    Args:
        old_str (str): 置換前
        new_str (str): 置換後
    """

    nodes = cmds.ls('*{}*'.format(old_str))

    for hit in nodes:
        cmds.lockNode(hit, lock=False)
        cmds.rename(hit, hit.replace(old_str, new_str))


def replace_file_path(old_str, new_str):
    """テクスチャなどのファイルパスの置換

    Args:
        old_str (str): 置換前
        new_str (str): 置換後
    """

    file_nodes = cmds.ls(type='file')

    for file_node in file_nodes:
        file_path = cmds.getAttr(file_node + '.fileTextureName')
        if file_path.find(old_str) >= 0:
            cmds.setAttr(file_node + '.fileTextureName', file_path.replace(old_str, new_str), type='string')


class CopyDataInfo(object):
    """コピー情報を保持するクラス
    """

    def __init__(self, src_root, dst_root, src_path, dst_path, replace_str_old, replace_str_new):

        self.src_root = src_root
        self.dst_root = dst_root

        self.src_path = src_path
        self.dst_path = dst_path

        self.replace_str_old = replace_str_old
        self.replace_str_new = replace_str_new

        self.src_relative = self.src_path.replace(self.src_root, '')
        self.dst_relative = self.dst_path.replace(self.dst_root, '')

        self.status = ''

        if self.src_path == self.dst_path:
            self.status = const.STATUS_IS_SAME
        else:
            if os.path.exists(self.dst_path):
                self.status = const.STATUS_ALREADY_EXISTS
            else:
                self.status = const.STATUS_NO_EXISTS
