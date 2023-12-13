# -*- coding: utf-8 -*-
"""Retarget ベースセットアップ補助ツール

Faceware Retargeter for Maya: MEL Commands
http://support.facewaretech.com/maya-retargeter-mel-commands
onenote:///\\cgs-str-fas05\100_projects\117_mutsunokami\30_design\OneNote\Mutsunokami\Facial.one#■Retargeter作業&section-id={643AD320-12BE-4110-8AF0-7353A90C37B3}&page-id={603F2F72-C908-4570-8C2E-A10C89B24A8B}&end
..
    END__CYGAMES_DESCRIPTION
"""

from __future__ import absolute_import

import os
from contextlib import contextmanager

import maya.cmds as cmds
import maya.mel as mel
import maya.api.OpenMaya as om

from mtku.maya.utils.decoration import keep_selections


PLUGIN_NAME = 'ImRetargetMaya.mll'
"""リターゲタープラグイン名
"""


@contextmanager
def WaitCursorBlock():
    """ウェイトカーソルを表示させるコンテキストマネージャー
    """

    try:
        cmds.waitCursor(state=True)
        yield

    except Exception as e:
        cmds.error(e)

    finally:
        cmds.waitCursor(state=False)


def save_optionvar(key, value, force=True):
    """optionVarに保存

    :param str key: キー名
    :param mixin value: 値
    :param bool force: 強制的に上書きするかのブール値

    :return: 保存できたかどうかのブール値
    :rtype: bool
    """

    v = str(value)
    if force:
        cmds.optionVar(sv=[key, v])
        return True
    else:
        if not cmds.optionVar(ex=key):
            cmds.optionVar(sv=[key, v])
            return True
        else:
            return False


def load_optionvar(key):
    """optionVarを取得

    :param str key: キー名
    :return: 保存された値, キーが見つからない場合は None
    :rtype: value or None
    """

    if cmds.optionVar(ex=key):
        return eval(cmds.optionVar(q=key))
    else:
        return None


def remove_optionvar(key):
    """optionVarを削除

    :param str key: キー名
    :return: 削除成功したかのブール値
    :rtype: bool
    """

    if cmds.optionVar(ex=key):
        cmds.optionVar(rm=key)
        return True
    else:
        return False


def load_retargeter():
    """Retargeterプラグインのロード
    """

    plugin_name = PLUGIN_NAME
    if not cmds.pluginInfo(plugin_name, q=True, loaded=True):
        cmds.loadPlugin(plugin_name, quiet=True)

    if not cmds.pluginInfo(plugin_name, q=True, loaded=True):
        cmds.error('ImRetargetMaya plugin can not be loaded.')


def unload_retargeter():
    """Retargeterプラグインのアンロード
    """
    plugin_name = PLUGIN_NAME
    if cmds.pluginInfo(plugin_name, q=True, loaded=True):
        cmds.unloadPlugin(plugin_name, force=True)


def list_retargeter_commands():
    """ リターゲタープラグインの登録コマンドを取得
    :return: 登録コマンドのリスト
    :rtype: list
    """

    return cmds.pluginInfo(PLUGIN_NAME, q=True, command=True)


def ftiOpenPerformance(fwr_file, xml_file, **kwargs):
    """リターゲター　'パフォーマンスを開く'を実行
    :param str fwr_file: パフォーマンスファイル
    :param str xml_file: キャラクター設定ファイル
    :keyword int fr: SetFrameRate (on|off)
    :keyword int pr: SetPlaybackRange (on|off)
    :keyword int a: ImportAudio (on|off)
    :keyword int v: ImportVideo (on|off)
    :keyword int as: GenerateAutoSolve (on|off)
    :keyword int ue: UpdateExpressionSet (on|off)
    """

    if not (os.path.isfile(fwr_file) and os.path.isfile(xml_file)):
        return

    options = {
        'fwr': fwr_file,
        'xml': xml_file,
        'fr': kwargs.get('fr', 1),
        'pr': kwargs.get('pr', 1),
        'a': kwargs.get('a', 0),
        'v': kwargs.get('v', 1),
        'as': kwargs.get('as', 0),
        'ue': kwargs.get('ue', 0),
    }
    print('''ftiOpenPerformance "{fwr}" "{xml}" -fr {fr} -pr {pr} -a {a} -v {v} -as {as} -ue {ue};'''.format(**options))
    mel.eval('''ftiOpenPerformance "{fwr}" "{xml}" -fr {fr} -pr {pr} -a {a} -v {v} -as {as} -ue {ue}'''.format(**options))

    image_plane_trans = cmds.ls(sl=True)
    if image_plane_trans:
        image_pane = cmds.listRelatives(image_plane_trans, s=True, type='imagePlane')
        if image_pane:
            cmds.setAttr('{}.colorSpace'.format(image_pane[0]), 'Raw', type='string')


def ftiRetarget(pose_group, **kwargs):
    """リターゲット実行
    :param str pose_group: ポーズグループ名
    :keyword str retarget_range: リターゲットレンジ名
    :keyword int as: GenerateAutoSolve (on|off)
    :keyword int sp: useSharedPoses (on|off)
    """

    options = {
        'pose_group': pose_group,
        'retarget_range': kwargs.get('retarget_range', 'All Frames'),
        'as': kwargs.get('as', 0),
        'sp': kwargs.get('sp', 1),
    }
    print('''ftiRetarget "{pose_group}" "{retarget_range}" -as {as} -sp {sp}'''.format(**options))
    mel.eval('''ftiRetarget "{pose_group}" "{retarget_range}" -as {as} -sp {sp}'''.format(**options))


def retargeter():
    """リターゲターウィンドウを開く
    """

    mel.eval('''Retargeter;''')


def show_charactersetupwindow():
    """キャラクター設定ウィンドウを開く
    """

    mel.eval('''ImCharacterSetup;''')


def list_poseGroups():
    """ポーズグループ名のリストを取得
    """

    return mel.eval('''ImPoseGroupInfo -pg''')


def duplicate_camera(target, new_name):
    """カメラを複製
    :param str target: 複製対象のカメラノード名
    :param str new_name: 複製カメラノード名
    :return: 複製カメラノード名
    """

    return cmds.duplicate(target, rr=True, ic=True, n=new_name)[0]


def fit_videoplane(plane, camera, scale=4.0):
    """リファレンス用イメージプレーンの位置合わせ
    :param str plane: イメージプレーンノード名
    :param str camera: 位置合わせに使用するカメラ
    :param float scale: イメージプレーンスケール
    """

    if not cmds.objExists(camera):
        return

    if not cmds.objExists(plane):
        return

    plane_shape = cmds.listRelatives(plane, s=True, pa=True)[0]
    if cmds.objectType(plane_shape, i='mesh'):
        try:
            # メッシュで作成されて場合は imagePlaneノードに置き換える
            sg = cmds.listConnections(plane_shape, s=False, d=True, type='shadingEngine')
            if not sg:
                raise Exception('Shading Group not found.')
            mt = cmds.listConnections(sg, s=True, d=False, type='lambert')
            if not mt:
                raise Exception('Assign Material not found.')
            file_node = cmds.listConnections(mt, s=True, d=False, type='file')
            if not file_node:
                raise Exception('Assign file node not found.')
            file_path = cmds.getAttr('{}.fileTextureName'.format(file_node[0]))
            cmds.delete(plane_shape)
            plane_shape = cmds.createNode('imagePlane', n=plane_shape, ss=True, p=plane)
            cmds.setAttr('{}.useFrameExtension'.format(plane_shape), 1)
            cmds.setAttr('{}.imageName'.format(plane_shape), file_path, type='string')
            cmds.setAttr('{}.lockedToCamera'.format(plane_shape), False)
            cmds.setAttr('{}.height'.format(plane_shape), cmds.getAttr('{}.sy'.format(plane)))
            cmds.setAttr('{}.width'.format(plane_shape), cmds.getAttr('{}.sx'.format(plane)))
            cmds.setAttr('{}.s'.format(plane), *[1.0, 1.0, 1.0])

        except Exception as e:
            cmds.warning(str(e))
            cmds.delete(plane, ch=True)
            cmds.makeIdentity(plane, apply=True, t=True, r=True, s=True, n=False, pn=True)

    cam_mat = om.MMatrix(cmds.xform(camera, q=True, ws=True, m=True))
    plane_tmat = om.MTransformationMatrix()
    plane_tmat.setTranslation(om.MVector([0.0, 5.0, -50.0]), om.MSpace.kTransform)
    plane_tmat.setScale([scale, scale, scale], om.MSpace.kTransform)
    cmds.xform(plane, ws=True, m=plane_tmat.asMatrix() * cam_mat)


def facial_window(camera):
    """フェイシャル作業用のウィンドウを開く
    :param str camera: modelPanelに指定するカメラノード名
    """

    if not cmds.objExists(camera):
        return

    camera_shape = cmds.listRelatives(camera, s=True, pa=True, type='camera')[0]
    if not camera_shape:
        return

    win_name = 'facial_window'
    if cmds.window(win_name, q=True, ex=True):
        cmds.deleteUI(win_name)

    win = cmds.window(win_name, wh=[800, 600])
    lay = cmds.paneLayout(p=win, cn='vertical3')
    pane1 = cmds.modelPanel(p=lay)
    pane2 = cmds.modelPanel(p=lay)
    pane3 = cmds.modelPanel(p=lay)
    cmds.paneLayout(lay, e=True, ps=[1, 35, 100])
    cmds.paneLayout(lay, e=True, ps=[2, 35, 100])
    cmds.paneLayout(lay, e=True, ps=[3, 30, 100])
    cmds.modelEditor(
        cmds.modelPanel(pane1, q=True, me=True),
        e=True, cmEnabled=False, allObjects=False, imagePlane=True, hud=False, manipulators=False,
        rendererName='vp2Renderer',
        camera=camera_shape)
    cmds.modelEditor(
        cmds.modelPanel(pane2, q=True, me=True),
        e=True, cmEnabled=True, allObjects=False, polymeshes=True, da='smoothShaded', dtx=True,
        hud=False, manipulators=False,
        rendererName='vp2Renderer',
        camera=camera_shape)
    cmds.modelEditor(
        cmds.modelPanel(pane3, q=True, me=True),
        e=True, cmEnabled=True, allObjects=False, polymeshes=True, nc=True, ns=True, da='smoothShaded', hud=False,
        rendererName='vp2Renderer',
        camera='persp')
    cmds.showWindow(win)


@keep_selections
def facial_single_panel(camera, pivot):
    if not cmds.objExists(camera):
        return

    camera_shape = cmds.listRelatives(camera, s=True, pa=True, type='camera')[0]
    if not camera_shape:
        return

    new_camera = '{}_facial_diagonal'.format(camera)
    if not cmds.objExists(new_camera):
        new_camera = cmds.duplicate(camera_shape, rr=True, n=new_camera)[0]

    if cmds.listRelatives(new_camera, p=True, pa=True):
        new_camera = cmds.parent(new_camera, w=True)[0]

    cmds.xform(new_camera, ws=True, m=cmds.xform(camera, q=True, ws=True, m=True))
    camera_space = '{}_facial_diagonal_space'.format(camera)
    rot_space = '{}_rot'.format(camera_space)
    if cmds.objExists(camera_space):
        cmds.delete(camera_space)

    camera_space = cmds.createNode('transform', n=camera_space, ss=True)
    cmds.parentConstraint(camera, camera_space, mo=False, w=True)
    offset_space = cmds.createNode('transform', n='{}_offset'.format(camera_space), ss=True, p=camera_space)
    rot_space = cmds.createNode('transform', n=rot_space, ss=True, p=offset_space)
    cmds.xform(offset_space, ws=True, t=pivot, ro=[0.0, 0.0, 0.0])
    cmds.parent(new_camera, rot_space)
    cmds.setAttr('{}.ry'.format(rot_space), 30)

    diagonal_panel_label = 'Facial_Panel'
    diagonal_panel = cmds.getPanel(withLabel=diagonal_panel_label)

    if not diagonal_panel:
        diagonal_panel = cmds.modelPanel(toc='modelPanel4')
        cmds.modelPanel(diagonal_panel, e=True, l=diagonal_panel_label)
    else:
        cmds.modelPanel(diagonal_panel, e=True, tor=True)

    model_editor = cmds.modelEditor(
        cmds.modelPanel(diagonal_panel, q=True, me=True),
        e=True, allObjects=False, polymeshes=True, nc=False, ns=False, da='smoothShaded', hud=False,
        rendererName='vp2Renderer',
        camera=new_camera)

    slider_lay = 'facial_diagonal_panel_option_layout'
    if cmds.layout(slider_lay, exists=True):
        cmds.deleteUI(slider_lay)

    new_camera_shape = cmds.listRelatives(new_camera, s=True, pa=True, type='camera')[0]

    par_layout = cmds.modelEditor(model_editor, q=True, p=True).rsplit('|', 1)[0]
    cmds.columnLayout(slider_lay, adj=True, p=par_layout)
    cmds.attrFieldSliderGrp(min=0.2, max=3, at='{}.overscan'.format(new_camera_shape), p=slider_lay)
    cmds.attrFieldSliderGrp(min=-180, max=180, at='{}.rotateX'.format(rot_space), p=slider_lay)
    cmds.attrFieldSliderGrp(min=-180, max=180, at='{}.rotateY'.format(rot_space), p=slider_lay)
    cmds.attrFieldSliderGrp(min=-180, max=180, at='{}.rotateZ'.format(rot_space), p=slider_lay)


def setup_vertical3_panel(camera):
    """フェイシャル作業用のパネル設定を行う
    :param str camera: modelPanelに指定するカメラノード名
    """

    camera_shape = cmds.listRelatives(camera, s=True, pa=True, type='camera')[0]
    if not camera_shape:
        return

    view_pane = mel.eval('$tmp = $gMainPane')
    cmds.paneLayout(view_pane, e=True, cn='vertical3')
    pane1 = cmds.paneLayout(view_pane, q=True, p1=True)
    pane2 = cmds.paneLayout(view_pane, q=True, p2=True)
    pane3 = cmds.paneLayout(view_pane, q=True, p3=True)
    cmds.modelEditor(
        cmds.modelPanel(pane1, q=True, me=True),
        e=True, cmEnabled=False, allObjects=False, imagePlane=True,
        # hud=False, manipulators=False,
        rendererName='vp2Renderer',
        camera=camera_shape)
    cmds.modelEditor(
        cmds.modelPanel(pane2, q=True, me=True),
        e=True, cmEnabled=False, allObjects=False, polymeshes=True, da='smoothShaded', dtx=True,
        # hud=False, manipulators=False,
        rendererName='vp2Renderer',
        camera=camera_shape)
    cmds.modelEditor(
        cmds.modelPanel(pane3, q=True, me=True),
        e=True, cmEnabled=False, allObjects=False, polymeshes=True, nc=True, ns=True, da='smoothShaded', hud=False,
        rendererName='vp2Renderer',
        camera='persp')
