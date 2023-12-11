# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import maya.cmds as cmds
import maya.mel as mel


MMASK_SET_NAME = 'MMaskSet'
MMASK_SUFFIX = '_Mask'


def create_mmask_set(target_list):
    """アイコンマスク用のフェースセットを作成

    Args:
        target_list (list): セットに登録するフェースリスト
    """

    target_faces = cmds.ls(cmds.polyListComponentConversion(target_list, tf=True), l=True, fl=True)

    mmask_set = cmds.sets(em=True, n=MMASK_SET_NAME)
    if target_faces:
        cmds.sets(target_faces, add=mmask_set)


def add_mmask(target_list):
    """アイコンマスク用のフェースセットにフェースを追加

    Args:
        target_list (list): 追加するフェースリスト
    """

    target_faces = cmds.ls(cmds.polyListComponentConversion(target_list, tf=True), l=True, fl=True)

    if not target_faces:
        return

    if cmds.objExists(MMASK_SET_NAME):
        cmds.sets(target_faces, add=MMASK_SET_NAME)
    else:
        create_mmask_set(target_faces)


def remove_mmask(target_list):
    """アイコンマスク用のフェースセットからフェースを削除

    Args:
        target_list (list): 削除するフェース
    """

    target_faces = cmds.ls(cmds.polyListComponentConversion(target_list, tf=True), l=True, fl=True)

    if not target_faces:
        return

    if cmds.objExists(MMASK_SET_NAME):
        cmds.sets(target_faces, rm=MMASK_SET_NAME)


def turn_on_body_isolate_view():
    """衣装部分を分離表示
    """

    target_transforms = cmds.ls('*|M_Body*', type='transform')
    all_faces = cmds.ls(cmds.polyListComponentConversion(target_transforms, tf=True), l=True, fl=True)

    target_faces = all_faces

    if cmds.objExists(MMASK_SET_NAME):
        skin_faces = cmds.ls(cmds.sets(MMASK_SET_NAME, q=True), l=True, fl=True)
        target_faces = [x for x in all_faces if x not in skin_faces]

    __switch_isolate_view(True, target_faces)


def turn_on_mask_isolate_view():
    """マスク部分を分離表示
    """

    if cmds.objExists(MMASK_SET_NAME):
        __switch_isolate_view(True, cmds.sets(MMASK_SET_NAME, q=True))


def turn_off_isolate_view():
    """分離表示解除
    """

    __switch_isolate_view(False)


def __switch_isolate_view(view_state, target_list=[]):
    """分離表示切り替え

    Args:
        view_state (bool): 分離表示をオンにするか
        target_list (list, optional): 分離表示するもののリスト. Defaults to [].
    """

    cmds.select(target_list, r=True)

    p1 = cmds.paneLayout('viewPanes', q=True, pane1=True)
    p2 = cmds.paneLayout('viewPanes', q=True, pane2=True)
    p3 = cmds.paneLayout('viewPanes', q=True, pane3=True)
    p4 = cmds.paneLayout('viewPanes', q=True, pane4=True)

    for viewPain in [p1, p2, p3, p4]:
        # cmds.isolateSelectでは挙動が安定せず、UIも更新されなかったのでmelのenableIsolateSelectを使用
        mel.eval('enableIsolateSelect {} {}'.format(viewPain, str(int(view_state))))

    cmds.select(clear=True)
