# -*- coding: utf-8 -*-
# ----------------------------------
# Project : Tsubasa
# Name    : npcTools
# Author  : toi
# Update  : 2021/5/24
# ----------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import maya.cmds as cmds
import maya.mel as mm
import pymel.core as pm
import os
import re
from . import tools
from dccUserMayaSharePythonLib import common as cm
from dccUserMayaSharePythonLib import skinning as sk
from dccUserMayaSharePythonLib import ui

window_name = 'npcTools'


# abcタイプ---------------------------------------------------------------------------------
def getCurrentKindAllMesh(mesh_kind):
    taransforms = pm.ls(tr=True)
    msh_list = [x for x in taransforms if x.name().startswith('msh_{0}_'.format(mesh_kind))]
    return msh_list


def getTargetMesh():
    sels = pm.selected()
    if not sels:
        return

    target_mesh = sels[0]
    if not target_mesh.name().startswith('msh'):
        pm.confirmDialog(m='meshノードを選択してください', p=window_name)
        return

    return target_mesh


def showAllColor():
    mesh_list = [x for x in cmds.ls(transforms=True) if x.startswith('msh_')]
    for msh in mesh_list:
        pm.setAttr(msh + '.v', True)


def showMshAOnly():
    mesh_list = [x for x in cmds.ls(transforms=True) if x.startswith('msh_')]
    for msh in mesh_list:
        pm.setAttr(msh + '.v', msh.startswith('msh_a'))


def selectAllNpcMesh():
    target_mesh = getTargetMesh()
    if target_mesh is None:
        return

    mesh_kind = target_mesh.name()[4]
    msh_list = getCurrentKindAllMesh(mesh_kind)
    pm.select(msh_list)


def copyWeightFromA(mesh_kind):

    target_msh_list = getCurrentKindAllMesh(mesh_kind)
    a_msh_list = getCurrentKindAllMesh('a')

    pair_list = []
    for target_msh in target_msh_list:
        target_msh_name = target_msh.split('_', 2)[-1]

        for a_msh in a_msh_list:
            a_msh_name = a_msh.split('_', 2)[-1]
            if target_msh_name == a_msh_name:
                pair_list.append([a_msh, target_msh])
                break

    if not pair_list:
        return

    for a_msh, tgt_msh in pair_list:
        try:
            sk.bindPairModel(a_msh.name(), tgt_msh.name())
            sk.copySkinWeight(a_msh, tgt_msh, influenceAssociation_='oneToOne')
            print('success', a_msh, tgt_msh)
        except:
            print('failed', a_msh, tgt_msh)

    pm.select(target_msh_list)


def copyWeightFromASel():
    target_mesh = getTargetMesh()
    if target_mesh is None:
        return

    mesh_kind = target_mesh.name()[4]
    copyWeightFromA(mesh_kind)
    cm.hum('Finished')


def copyWeightFromAAll():
    sels = pm.ls(s=True)
    tgt_shapes = []
    for sel in sels:
        n = sel.name()
        if re.match('msh_+[b-z]+_', n):
            tgt_shapes.append(n[4])
    tgt_kinds = list(set(tgt_shapes))
    print(tgt_kinds)

    message = 'a → '
    if tgt_kinds:
        for tgt in tgt_kinds:
            copyWeightFromA(tgt)
            message += tgt + ', '
    cm.hum(message + ' : Finished')


# 00, 10タイプ-----------------------------------------------------------------------------
def select00():
    sels = cmds.ls(sl=True)
    cmds.select(cl=True)
    for node in sels:
        _00 = None

        if 'a10' in node:
            _00 = node.replace('a10', 'a00')
        elif 'a20' in node:
            _00 = node.replace('a20', 'a00')

        elif 'b10' in node:
            _00 = node.replace('b10', 'b00')
        elif 'b20' in node:
            _00 = node.replace('b20', 'b00')

        elif 'c10' in node:
            _00 = node.replace('c10', 'c00')
        elif 'c20' in node:
            _00 = node.replace('c20', 'c00')

        print(node, _00)
        if _00 is not None and cmds.objExists(_00):
            cmds.select(_00, node, add=True)


# ui-----------------------------------------------------------------------------
def initUi():
    if pm.window(window_name, ex=True):
        pm.deleteUI(window_name)
    win = pm.window(window_name, t=window_name, w=400)
    cl = pm.columnLayout(adj=True)

    with pm.frameLayout(l='abc...　タイプ', bgc=(0.32, 0.22, 0.32)):
        with pm.verticalLayout() as hl:
            cmds.button(
                l='全てのカラバリメッシュを　「　表示　」', ann='全てのカラバリメッシュを表示します',
                c=pm.Callback(showAllColor))
            cmds.button(
                l='「　msh_a　」　のみ　「　表示　」', ann='「msh_a」のみ表示します',
                c=pm.Callback(showMshAOnly))
            cmds.button(
                l='選択中のカラバリメッシュを　「　全て選択　」', ann='選択したNPCのカラバリメッシュを全て選択します',
                c=pm.Callback(selectAllNpcMesh))
            cmds.button(
                l='「　msh_a　」　から　「　weightコピー　」 （選択カラーのみ）', ann='選択したNPCのカラバリメッシュに「msh_a」からweightをコピーします',
                c=pm.Callback(copyWeightFromASel))
            cmds.button(
                l='「　msh_a　」　から　「　weightコピー　」 （全カラー一括）', ann='選択したNPCのカラバリメッシュに「msh_a」からweightをコピーします',
                c=pm.Callback(copyWeightFromAAll))

    with pm.frameLayout(l='00, 10...　タイプ', bgc=(0.32, 0.22, 0.32)):
        with pm.verticalLayout() as hl:
            cmds.button(
                l='選択中のメッシュに対応する00メッシュと　「　交互選択　」', ann='複数選択の場合は、交互に選択します',
                c=pm.Callback(select00))


    win.show()