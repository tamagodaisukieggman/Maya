# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
    from importlib import reload
except Exception:
    pass

import re
import maya.cmds as cmds


def setup(eye_cover_joint_name, l_x_offset=1.5, l_z_offset=-2.5):
    """目隠し表情に遷移させる処理を行う

    通常シーンではジョイントをフェイシャルシーンではコントローラーを動かして、目隠しを実行する

    Args:
        eye_cover_joint_name: 目隠しメッシュをバインドしたジョイントのショートネーム(L, Rは問わない）
        l_x_offset(float): 左目セットアップ時のX移動値(セットアップデータやUIから指定される)
        l_z_offset(float): 左目セットアップ時のZ移動値(触られないので規定値がそのまま入る)
    """

    scene_path = cmds.file(q=True, sn=True)

    if not scene_path:
        return

    l_target_transform = None
    r_target_transform = None
    is_facial_scene = False

    # LRのジョイント名に変換
    target_base_name = re.sub('_[LR]$', '', eye_cover_joint_name)
    l_target_transform = target_base_name + '_L'
    r_target_transform = target_base_name + '_R'

    if scene_path.endswith('_facial_target.ma'):
        # フェイシャルシーンならコントロール名に変換
        is_facial_scene = True
        l_target_transform += '_Ctrl'
        r_target_transform += '_Ctrl'

    if not cmds.objExists(l_target_transform) or not cmds.objExists(r_target_transform):
        return

    # 移動処理開始
    cmds.undoInfo(openChunk=True)

    # コントローラーを初期位置に戻す
    if is_facial_scene:
        cmds.xform(l_target_transform, ro=[0, 0, 0], t=[0, 0, 0], a=True)
        cmds.xform(r_target_transform, ro=[0, 0, 0], t=[0, 0, 0], a=True)
    else:
        cmds.dagPose(l_target_transform, bp=True, r=True)
        cmds.dagPose(r_target_transform, bp=True, r=True)

    # 回転はワールドY180度以外とらない
    cmds.rotate(0, 180, 0, l_target_transform, r=True, ws=True, fo=True)
    cmds.rotate(0, -180, 0, r_target_transform, r=True, ws=True, fo=True)

    cmds.xform(l_target_transform, t=[l_x_offset, 0, l_z_offset], r=True, ws=True)
    cmds.xform(r_target_transform, t=[l_x_offset * -1, 0, l_z_offset], r=True, ws=True)

    cmds.undoInfo(closeChunk=True)
