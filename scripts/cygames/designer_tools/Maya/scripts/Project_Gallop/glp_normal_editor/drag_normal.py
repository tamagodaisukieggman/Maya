# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from builtins import object
except Exception:
    pass

import maya.cmds as cmds

"""
Mayaの機能のMesh Display > Vertex Normal Edit Tool だと一度に動かせる法線の方向がx, y, zのどれか1つだが、
通常のRotate Tool のように一度に各方向に法線の向きをドラッグして変えたいとの希望で作ったツール。
Created: 2022/01/13
Last Modified: 2022/04/21
Author(s): Natsuko Kinoshita
チケット
https://prodigy.tkgpublic.jp/browse/TDN-4680
"""

g_tool_name = "glp_drag_normal"
g_tool_context = "glp_drag_normal_context"
g_version = "2022.04.21"


class VertexNormalDragger(object):
    """
    マウスドラッグで法線を動かせるコンテキストを作るクラス
    """

    def __init__(self):
        pass

    def begin_drag_normal(self):
        """
        ドラッグコンテキスト使用開始
        """
        vertices = cmds.filterExpand(
            cmds.polyListComponentConversion(cmds.ls(sl=True), toVertex=True),
            selectionMask=31)
        if not cmds.selectMode(q=True, component=True) or not vertices:
            cmds.warning("頂点を選択してから実行してください")
            # 重要：一旦ツールは起動してひとつ前のツールとして使えるようにしておくのでreturnしない
        # ツール使用前の法線表示状態確認
        self.selected_objects = self.list_selected_objects()
        if self.selected_objects:
            # Vertexノーマルの表示stateリスト
            self.vertex_normal_states = cmds.polyOptions(
                q=True, activeObjects=True, point=True, displayNormal=True)
            self.vertex_normal_states = self.vertex_normal_states[0::2]
            # Faceノーマルの表示stateリスト
            self.face_normal_states = cmds.polyOptions(
                q=True, activeObjects=True, facet=True, displayNormal=True)
            self.face_normal_states = self.face_normal_states[1::2]
        # 頂点の法線を表示
        cmds.polyOptions(activeObjects=True, point=True, displayNormal=True)
        # 既存のドラッグコンテキストがあったら削除
        if cmds.draggerContext(g_tool_context, q=True, exists=True):
            cmds.deleteUI(g_tool_context)
        # ドラッグコンテキスト作成
        cmds.draggerContext(g_tool_context, pressCommand=self.on_press,
                            releaseCommand=self.on_release,
                            dragCommand=self.on_drag, space="world",
                            i1="vertexNormalEdit.xpm")
        cmds.setToolTo(g_tool_context)

    def end_drag_normal(self):
        """
        ツール使用終了
        """
        # ツールのコンテキストを削除
        if cmds.draggerContext(g_tool_context, q=True, exists=True):
            cmds.deleteUI(g_tool_context)
        # ノーマルの表示状態をbegin_drag_normal開始時に戻す
        if self.selected_objects:
            for i, obj in enumerate(self.selected_objects):
                cmds.select(obj)
                try:
                    # Vertex
                    cmds.polyOptions(activeObjects=True, point=True,
                                     displayNormal=self.vertex_normal_states[i])
                    # Face
                    cmds.polyOptions(activeObjects=True, facet=True,
                                     displayNormal=self.face_normal_states[i])
                except Exception:
                    pass
        # 選択ツールにする
        cmds.setToolTo("selectSuperContext")

    def list_selected_objects(self):
        """
        選択されているオブジェクトのリストを返す。
        選択されているのがVertexコンポーネントだった場合、それを含んでいるオブジェクトを返す。
        """
        selected = cmds.ls(sl=True, type="transform")
        if selected:
            return selected
        selected = cmds.ls(sl=True)
        selected_objects = []
        for sel in selected:
            if sel.find(".vtx") > -1:
                selected_objects.append(sel[0:sel.find(".vtx")])
        selected_objects = list(set(selected_objects))
        return selected_objects

    def on_press(self):
        """
        マウスドラッグ開始
        """
        vertices = cmds.filterExpand(
            cmds.polyListComponentConversion(cmds.ls(sl=True), toVertex=True),
            selectionMask=31)
        if not cmds.selectMode(q=True, component=True) or not vertices:
            # ドラッグコンテキスト中にバーテックスが選択されていなかったら選択モードに切り替え
            cmds.warning("頂点を選択してから実行してください")
            cmds.selectMode(component=True)
            cmds.setToolTo("selectSuperContext")
            cmds.refresh()
            return
        # Undo chunk開始。一回のドラッグにつき一回のUndoで元に戻すため
        cmds.undoInfo(openChunk=True)
        # 選択されているVertexを確認
        vertices = cmds.filterExpand(
            cmds.polyListComponentConversion(cmds.ls(sl=True), toVertex=True),
            selectionMask=31)
        if vertices:
            # Vertexが選択されていたら法線情報取得
            self.original_normal_value = cmds.polyNormalPerVertex(q=True, 
                                                                  xyz=True)

    def on_release(self):
        """
        マウスドラッグ終了
        """
        if not cmds.selectMode(q=True, component=True):
            return
        # Undo chunk終了。一回のドラッグにつき一回のUndoで元に戻すため
        cmds.undoInfo(closeChunk=True)

    def on_drag(self):
        """
        Mouse DragでVertexノーマルの方向を設定する
        """
        if not cmds.selectMode(q=True, component=True):
            return
        if not cmds.polyListComponentConversion(cmds.ls(sl=True), tv=True):
            return
        anchor_pos = cmds.draggerContext(
            g_tool_context, q=True, anchorPoint=True)
        drag_pos = cmds.draggerContext(
            g_tool_context, q=True, dragPoint=True)
        sensitivity = 0.1
        if self.original_normal_value:
            normal_x = self.original_normal_value[0] + (
                drag_pos[0] - anchor_pos[0]) * sensitivity
            normal_y = self.original_normal_value[1] + (
                drag_pos[1] - anchor_pos[1]) * sensitivity
            normal_z = self.original_normal_value[2] + (
                drag_pos[2] - anchor_pos[2]) * sensitivity
            cmds.polyNormalPerVertex(relative=False, xyz=(
                normal_x, normal_y, normal_z))
            cmds.refresh()
