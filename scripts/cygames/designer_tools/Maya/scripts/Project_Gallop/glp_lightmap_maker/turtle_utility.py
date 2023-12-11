# -*- coding: utf-8 -*-
u"""
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import str
    from builtins import range
    from builtins import object
    from importlib import reload
except Exception:
    pass

import maya.cmds as cmds
import maya.mel as mel


def load_turtle():
    """turtleのロード
    """

    if not cmds.pluginInfo('Turtle', query=True, loaded=True):
        cmds.loadPlugin('Turtle.mll')
        cmds.warning(u'Turtleプラグインをロードしました')


def switch_turtle_renderer():
    """レンダラーをturtleへ切り替え
    """

    cmds.setAttr('defaultRenderGlobals.currentRenderer', 'turtle', type='string')


def set_turtle_bake_layer(bake_layer):
    """turtleのベイクレイヤー設定

    Args:
        bake_layer (str): カレントに設定するベイクレイヤー
    """

    cmds.setAttr('TurtleRenderOptions.renderer', 1)  # renderType=Baking
    mel.eval('ilrSetCurrentBakeLayer {}'.format(bake_layer))


def initialize_turtle_system():
    """turtleの初期設定
    """

    if not cmds.objExists('TurtleBakeLayerManager'):
        mel.eval('ilrCreateBakeLayerManagerNode')
    if not cmds.objExists('TurtleRenderOptions'):
        mel.eval('ilrCreateRenderOptionsNode')
    if not cmds.objExists('TurtleDefaultBakeLayer'):
        mel.eval('ilrCreateDefaultBakeLayer')


def create_turtle_bake_layer(name):
    """ベイクレイヤーの作成

    Args:
        name (str): 作成するベイクレイヤー名
    """

    if not cmds.objExists('TurtleDefaultBakeLayer'):
        initialize_turtle_system()

    mel.eval('ilrCreateBakeLayer(\"' + name + '\", 0)')


def delete_turtle_bake_layer(name):
    """ベイクレイヤーの削除

    Args:
        name (str): 削除するベイクレイヤー名
    """

    # ツールがデフォルトで割り当てるカスタムシェーダーも削除
    custom_shader = cmds.listConnections(name + '.customShader')
    if custom_shader:
        cmds.delete(custom_shader)

    mel.eval('ilrDeleteBakeLayer(\"' + name + '\")')


def add_target_surface(mesh, bake_layer):
    """ベイクターゲットのサーフェイスを追加

    Args:
        mesh (str): 追加するベイクターゲット
        bake_layer (str): ターゲットを追加するベイクレイヤー
    """

    if not cmds.objExists(bake_layer):
        return

    mel_cmd = 'string $ss[]={'
    mel_cmd += ','.join(['\"{}\"'.format(x) for x in mesh])
    mel_cmd += '};ilrAddSurfacesToBakeLayer $ss ' + bake_layer

    mel.eval(mel_cmd)


def delete_target_surface(shape_list, bake_layer):
    """ベイクターゲットを削除

    Args:
        shape_list (str): 削除するベイクターゲット
        bake_layer (str): ターゲットを削除するベイクレイヤー
    """

    if not cmds.objExists(bake_layer):
        return

    exist_target_list = cmds.sets(bake_layer, q=True)
    del_shape_list = [x for x in shape_list if x in exist_target_list]

    if not del_shape_list:
        return

    mel_cmd = 'string $ss[]={'
    mel_cmd += ','.join(['\"{}\"'.format(x) for x in del_shape_list])
    mel_cmd += '};ilrRemoveSurfacesFromBakeLayer $ss ' + bake_layer

    mel.eval(mel_cmd)


def set_gi_enable(use_gi):
    """ベイク時のGIの有効化

    Args:
        use_gi (bool): GIを使用するか
    """

    if not cmds.objExists('TurtleRenderOptions'):
        return
    cmds.setAttr('TurtleRenderOptions.enableGI', use_gi)
