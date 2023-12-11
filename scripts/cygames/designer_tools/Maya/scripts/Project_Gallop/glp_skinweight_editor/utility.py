# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
import maya.cmds as cmds
import maya.mel as mel


def get_namespace_removed_shortname(name):
    """ネームスペースが付いていないショートネームを取得

    Args:
        name (str): 名前

    Returns:
        str: ネームスペースが除去されたショートネーム
    """
    if ":" in name:
        return name.rsplit(':', 1)[1]
    return name


def get_transform_from_vertexes(vtx_list):
    """vertexのリストから含まれているトランスフォーム名を取得

    Args:
        vtx_list (list(str)): 確認対象のvertexのリスト

    Returns:
        list(str): 名前のリスト
    """
    transforms = []

    for vtx in vtx_list:
        transform = vtx.split('.vtx')[0]
        if transform not in transforms:
            transforms.append(transform)

    return transforms


def get_mfn_skin_clusters_by_transform(transform):
    """トランスフォーム名からmfnSkinClusterを取得

    Args:
        transform (str): 対象のトランスフォーム名

    Returns:
        oma.MFnSkinCluster: トランスフォームに紐づいていたスキンクラスター
    """
    skinclusters = cmds.ls(cmds.listHistory(transform), type='skinCluster')
    if not skinclusters:
        om.MGlobal.displayWarning('紐づいているスキンクラスターが見つかりません')
        return None

    skincluster = skinclusters[0]

    sel = om.MSelectionList()
    sel.add(skincluster)
    target_obj = sel.getDependNode(0)
    mfn_skincluster = oma.MFnSkinCluster(target_obj)

    return mfn_skincluster


def get_selected_vertex_list():
    """選択からvertexを取得

    Returns:
        list(str): vertexのリスト
    """
    selection_list = get_selection_list()
    if not selection_list:
        return []

    mel.eval('PolySelectConvert 3')
    vtx_list = cmds.ls(os=True, l=True, fl=True)

    # メッシュ関連のオブジェクト以外のものが選択されていた時のためにフィルタリングする
    vtx_list = [vtx for vtx in vtx_list if '.vtx[' in vtx]

    cmds.select(selection_list, r=True)

    return vtx_list


def get_selection_list():
    """選択のリストを取得

    Returns:
        list(str): 選択している物のリスト
    """
    select_list = []

    select_list = cmds.ls(os=True, l=True, fl=True)
    if select_list:
        return select_list

    select_list = cmds.ls(sl=True, l=True, fl=True)
    if not select_list:
        return []

    return select_list


def convert_str_to_float_list(src_str):
    """str文字列をfloatのリストに変換します

    Args:
        src_str (str): カンマで区切られた形式のstrに変換されたfloat文字列

    Returns:
        list(float) : 復元されたlist
    """
    converted_list = []
    for part in src_str.split(','):
        converted_list.append(float(part))

    return converted_list
