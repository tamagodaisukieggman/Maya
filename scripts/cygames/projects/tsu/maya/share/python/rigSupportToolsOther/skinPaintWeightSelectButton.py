# -*- coding: utf-8 -*-
# ----------------------------------
# Project : Tsubasa
# Name    : skinPaintWeightSelectButton
# Author  : toi
# Update  : 2022/6/13
# ----------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import maya.cmds as cmds
import maya.mel as mm
import pymel.core as pm
#import os
#import sys
#import time
#from . import tools
#from . import convertTex2ColorOnly
from dccUserMayaSharePythonLib import common as cm
from dccUserMayaSharePythonLib import skinning as sk
from dccUserMayaSharePythonLib import ui
#reload(sk)

window_name = 'skin_paint_weight_select_button'
copyPasteMesh2Vtx = sk.CopyPasteMesh2Vtx()
copyPasteVtxsWeight = sk.CopyPasteVtxsWeight()


def selmode():
    mm.eval('changeSelectMode -component;') # ハイライトをオフにする為に、一度コンポートネントにしてから
    mm.eval('changeSelectMode -object;')
    for p in ui.getModelPanels():
        cmds.modelEditor(p, e=True, displayAppearance='smoothShaded')
    cmds.setToolTo('selectSuperContext')


def psw():
    mm.eval('ArtPaintSkinWeightsTool')
    mm.eval('toolPropertyWindow;')


def startDuplicateSelPolygon(copy_weight=False):
    cm.hum()
    sels = cmds.ls(sl=True, fl=True)
    if not sels:
        return

    if '.f[' not in sels[0] or cmds.nodeType(sels[0]) != 'mesh':
        return

    if copy_weight:
        sk.duplicateSelPolygonAndBindAndCopy(sels)
    else:
        dupnode, original_node = sk.duplicateSelPolygon(sels)
        cmds.select(dupnode)


#def convertfbxtexture():
#    tsubasa.maya.tools.convertfbxtexture.gui.main()


def startSelectRelatedInfluences():
    sels = cmds.ls(sl=True)
    sk.selectRelatedInfluences(sels, True)


def startCopyWeight2Original():
    cm.hum()
    sels = cmds.ls(sl=True)
    for sel in sels:
        if not pm.objExists(sels[0] + '.vtx_set'):
            continue

        vtx_set = pm.getAttr(sels[0] + '.vtx_set')
        sk.copySkinWeight(sel, vtx_set, influenceAssociation_='oneToOne')
        cm.hum('copySkinWeight : {0} > {1}'.format(sel, vtx_set))


def startDuplicateMeshWithWeight():
    cm.hum()
    sels = cmds.ls(sl=True)
    for sel in sels:
        try:
            dup = cmds.duplicate(sel)
            cmds.parent(dup, w=True)

            sk.bindPairModel(sel, dup)
            sk.copySkinWeight(sel, dup)
        except:
            pass


def setCopyMesh():
    copyPasteMesh2Vtx.copy()
    cm.hum('copied : {0}'.format(copyPasteMesh2Vtx.mesh_node))


def paste2Set():
    if not copyPasteMesh2Vtx.mesh_node:
        pm.warning('先にCopyしてください')
        return

    copyPasteMesh2Vtx.startPaste()
    cm.hum('pasted : {0}'.format(copyPasteMesh2Vtx.paste_mesh))


def copyVtxsWeight():
    copyPasteVtxsWeight.copyWeightSelVtxs()


def pasteVtxsWeight():
    copyPasteVtxsWeight.pasteWeightSelVtxs()


# ----------------------------------------------------------------------------------------------------------
def skinPaintWeightSelectButton():
    if cmds.window(window_name, ex=True):
        cmds.deleteUI(window_name)

    cmds.window(window_name, t=window_name, w=300)
    cmds.columnLayout(adj=True, rs=2, co=['both', 2])
    cmds.iconTextButton(
        l='Select Tool  ( & Object Mode & smoothShade )', st='iconAndTextHorizontal', i='aselect.png',
        c=selmode, bgc=(0.32, 0.32, 0.32), h=40)
    cmds.iconTextButton(
        l='Paint Skin Weights', st='iconAndTextHorizontal', i='paintSkinWeights.png', h=40,
        c=psw, bgc=(0.32, 0.32, 0.32))

    cmds.separator(h=10)

    cmds.frameLayout(l='Other Skinning Commands', cl=0, cll=True, bgc=(0.323, 0.262, 0.509))
    cmds.columnLayout(adj=True, rs=2, co=['both', 2])

    cmds.text(l='maya -----', al='left')
    with pm.horizontalLayout() as hl:
        cmds.iconTextButton(
            l='Bind Skin', st='iconAndTextHorizontal', i='smoothSkin.png',
            c="import maya.mel as mm; mm.eval('SmoothBindSkinOptions')", bgc=(0.32, 0.32, 0.32))
        cmds.iconTextButton(
            l='Unbind Skin', st='iconAndTextHorizontal', i='detachSkin.png',
            c="import maya.mel as mm; mm.eval('DetachSkinOptions')", bgc=(0.32, 0.32, 0.32))

    with pm.horizontalLayout() as hl:
        cmds.iconTextButton(
            l='Mirror Skin Weights', st='iconAndTextHorizontal', i='mirrorSkinWeight.png',
            c="import maya.mel as mm; mm.eval('MirrorSkinWeightsOptions')", bgc=(0.32, 0.32, 0.32))
        cmds.iconTextButton(
            l='Copy Skin Weights', st='iconAndTextHorizontal', i='copySkinWeight.png',
            c="import maya.mel as mm; mm.eval('CopySkinWeightsOptions')", bgc=(0.32, 0.32, 0.32))

    with pm.horizontalLayout() as hl:
        cmds.iconTextButton(
            l='Add Influence', st='iconAndTextHorizontal', i='addWrapInfluence.png',
            c="import maya.mel as mm; mm.eval('AddInfluenceOptions')", bgc=(0.32, 0.32, 0.32))
        cmds.iconTextButton(
            l='Removes Influence', st='iconAndTextHorizontal', i='removeWrapInfluence.png',
            c="import maya.mel as mm; mm.eval('RemoveInfluence')", bgc=(0.32, 0.32, 0.32))

    with pm.horizontalLayout() as hl:
        cmds.iconTextButton(
            l='Orient Joint', st='iconAndTextHorizontal', i='orientJoint.png',
            c="import maya.mel as mm; mm.eval('OrientJointOptions')", bgc=(0.32, 0.32, 0.32))
        cmds.iconTextButton(
            l='Mirror Joint', st='iconAndTextHorizontal', i='kinMirrorJoint_S.png',
            c="import maya.mel as mm; mm.eval('MirrorJointOptions')", bgc=(0.32, 0.32, 0.32))

    with pm.horizontalLayout() as hl:
        cmds.iconTextButton(
            l='Weight Hammer', st='iconAndTextHorizontal', i='weightHammer.png',
            c="import maya.mel as mm; mm.eval('weightHammerVerts')", bgc=(0.32, 0.32, 0.32))
        cmds.iconTextButton(
            l='Freeze Transformation', st='iconAndTextHorizontal', i='menuIconModify.png',
            c="import maya.mel as mm; mm.eval('FreezeTransformationsOptions')", bgc=(0.32, 0.32, 0.32))

    cmds.text(l='tsubasa tools -----', al='left')
    with pm.horizontalLayout() as hl:
        cmds.button(
            l='Skin Weight',
            c='import tsubasa.maya.tools.skinweight as skinweight;skinweight.main()')
        cmds.button(
            l='Skin Weight Editor',
            c='import tsubasa.maya.tools.skinweighteditor.gui;tsubasa.maya.tools.skinweighteditor.gui.main()')
    with pm.horizontalLayout() as hl:
        cmds.button(
            l='Merge Rotation',
            c='import tsubasa.maya.rig.mergerotation as mergerotation;mergerotation.MergeRotationGUI().show()')
        cmds.button(
            l='SIWeightEditor',
            c='from siweighteditor import siweighteditor;siweighteditor.Option()')

    cmds.text(l='other -----', al='left')
    with pm.horizontalLayout() as hl:
        cmds.button(
            l='Select related influence', ann='接続されているskinClusterのインフルエンスを選択',
            c=pm.Callback(startSelectRelatedInfluences))
        cmds.button(
            l='Convert select to shell vertex', ann='選択しているコンポーネントを、シェル状態のバーテックスに拡大して選択する',
            c=pm.Callback(sk.convertShellVertex))

    with pm.horizontalLayout() as hl:
        cmds.button(
            l='Create vertex set', ann='選択コンポートネントをバーテックスに変換してセットを作成します',
            c=pm.Callback(sk.createSetComponent))
    cmds.separator(h=10)

    with pm.horizontalLayout() as hl:
        cmds.button(
            l='Duplicate sel polygon', ann='選択ポリゴンのみを複製します',
            c=pm.Callback(startDuplicateSelPolygon, False))
        cmds.button(
            l='Duplicate sel polygon with weight', ann='選択ポリゴンのみをWeight付きで複製します',
            c=pm.Callback(startDuplicateSelPolygon, True))

    with pm.horizontalLayout() as hl:
        cmds.button(
            l='Copy weight to original', ann='Duplicate Sel Polygonで作成したポリゴンを選択して実行、元のメッシュにウエイトをコピペします',
            c=pm.Callback(startCopyWeight2Original))
    cmds.separator(h=10)

    with pm.horizontalLayout() as hl:
        cmds.button(
            l='Duplicate sel mesh with weight', ann='選択meshをWeight付きで複製します',
            c=pm.Callback(startDuplicateMeshWithWeight))
    cmds.separator(h=10)

    with pm.horizontalLayout() as hl:
        cmds.button(
            l='CopyVtxs', ann='コピー元のバーテックスを選択',
            c=pm.Callback(copyVtxsWeight))
        cmds.button(
            l='PasteVtxs', ann='選択されたバーテックスにWeightをペーストする',
            c=pm.Callback(pasteVtxsWeight))

    with pm.horizontalLayout() as hl:
        cmds.button(
            l='CopyMesh', ann='コピー元のmeshノードを選択',
            c=pm.Callback(setCopyMesh))
        cmds.button(
            l='PasteVtxs', ann='選択されたバーテックスにWeightをペーストする',
            c=pm.Callback(paste2Set))
        cmds.button(
            l='Select Vtxs', ann='ペースト先のバーテックスを選択',
            c=pm.Callback(copyPasteMesh2Vtx.selVtx))

    cmds.showWindow(window_name)




