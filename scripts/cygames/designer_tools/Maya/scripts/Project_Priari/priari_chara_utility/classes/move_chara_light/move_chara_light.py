# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

"""
CGFX用ライト「CharaLight0」用の
カメラ移動、フォロー、自動回転ツール
"""

try:
    # Maya 2022-
    from builtins import object
except:
    pass

import maya.cmds as cmds


class MoveCharaLight(object):

    def __init__(self):
        """
        initialize
        """

        self.chara_light_name = 'charaLight0'

        self.chara_light_rig_group = '____charaLightRig'
        self.chara_light_rig_aim = '____charaLightAim'
        self.chara_light_move_parent = '____charaLightMoveP'
        self.chara_light_move_child = '____charaLightMoveC'
        self.persp_aim_constraint_name = '____charaLightAim_Constraint'
        self.tmp_parent_constraint_name = '____charaLightTmp_Constraint'

        self.shadow_angle_param = {
            'initial': 0,  # デフォルト角度
            'side': 77,  # 45度影
            'half': 101.5  # 半影
        }

        # ライトのoffset値
        self.light_offset_param = {
            'x': 0,
            'y': {'low': -25, 'middle': 25, 'high': 75, 'user': 0},
            'z': 75
        }

        # キーフレームポイント
        self.loop_key_frame_param = [
            {'time': 0, 'value': 0},
            {'time': 180, 'value': 360},
        ]

        self.before_aim_translate = [0, 0, 0]

    def _create_light_rig(self):
        """
        charaLight用の操作Ligを作成する
        """

        cmds.group(w=True, em=True, n=self.chara_light_rig_group)
        cmds.group(p=self.chara_light_rig_group, em=True, n=self.chara_light_rig_aim)
        cmds.group(p=self.chara_light_rig_group, em=True, n=self.chara_light_move_parent)
        cmds.group(p=self.chara_light_move_parent, em=True, n=self.chara_light_move_child)

        cmds.aimConstraint(
            'persp', self.chara_light_rig_aim, mo=True, n=self.persp_aim_constraint_name)

        cmds.xform(
            self.chara_light_move_child, ws=True, a=True,
            t=[
                self.light_offset_param['x'],
                self.light_offset_param['y']['middle'],
                self.light_offset_param['z']
            ]
        )

        self._set_chara_light_keyframe()

    def _reset_light_states(self):
        """
        charaLightの状態を初期状態に戻す
        """

        cmds.play(state=False)
        cmds.currentTime(0)

        if cmds.objExists(self.tmp_parent_constraint_name):
            cmds.delete(self.tmp_parent_constraint_name)

        if cmds.objExists(self.chara_light_name):
            cmds.xform(self.chara_light_name, ws=True, a=True, t=[0, 0, 0])
            cmds.xform(self.chara_light_name, ws=True, a=True, ro=[0, 0, 0])

        if cmds.objExists(self.chara_light_move_parent):
            cmds.cutKey(self.chara_light_move_parent, time=(0, 60))
            cmds.xform(self.chara_light_move_parent, ws=True, a=True, ro=[0, 0, 0])

    def _set_chara_light_keyframe(self):
        """
        キャラライトにキーをセットする
        """

        cmds.cutKey(self.chara_light_move_parent, time=(0, 60))

        for loop_key_frame in self.loop_key_frame_param:
            cmds.setKeyframe(
                self.chara_light_move_parent,
                t=loop_key_frame['time'],
                v=loop_key_frame['value'],
                at='rotateY', itt='linear', ott='linear'
            )
            cmds.setInfinity(self.chara_light_move_parent, pri='cycle', poi='cycle')

    def _get_light_translate(self, light_height):
        """
        設定するライトのoffset値を取得する
            :param light_height='middle': ライトのoffset値
        """

        light_translate = [
            self.light_offset_param['x'],
            self.light_offset_param['y'][light_height],
            self.light_offset_param['z']
        ]

        # light_heightがuserの場合、現在のライトのwsでのtranslateYの値を設定する
        if light_height == 'user':
            old_light_translate = cmds.xform(
                self.chara_light_name, q=True, ws=True, t=True)
            light_translate[1] = old_light_translate[1]

        return light_translate

    def set_chara_light_transform(self, shadow_angle='initial', light_direction='right', light_height='middle'):
        """
        キャラライトの位置を規定された位置に設定する
            :param shadow_angle='initial': ライトの角度
            :param light_height='middle': ライトのoffset値
        """
        self._reset_light_states()

        if not cmds.objExists(self.chara_light_name):
            return

        if not cmds.objExists(self.chara_light_rig_group):
            self._create_light_rig()

        if light_height not in self.light_offset_param['y']:
            return
        if shadow_angle not in self.shadow_angle_param:
            return

        light_translate = self._get_light_translate(light_height)

        self._reset_light_states()

        cmds.parentConstraint(self.chara_light_move_child, self.chara_light_name, n=self.tmp_parent_constraint_name)
        cmds.xform(self.chara_light_move_child, ws=True, a=True, t=light_translate)

        light_rotate = [0, self.shadow_angle_param[shadow_angle], 0]
        if light_direction == 'left':
            light_rotate[1] = light_rotate[1] * -1

        cmds.xform(self.chara_light_move_parent, ws=True, a=True, ro=light_rotate)

        cmds.delete(self.tmp_parent_constraint_name)

    def chara_light_anim(self, light_height='middle'):
        """
        原点を中心に回転するキャラライトのアニメーションを行う
            :param light_height='middle': ライトの高さ
        """

        if not cmds.objExists(self.chara_light_name):
            return

        if not cmds.objExists(self.chara_light_rig_group):
            self._create_light_rig()

        play_state = cmds.play(q=True, state=True)

        light_translate = self._get_light_translate(light_height)
        currentFrame = cmds.currentTime(q=True)
        cmds.currentTime(0)
        self._reset_light_states()
        self._set_chara_light_keyframe()
        cmds.xform(self.chara_light_move_child, ws=True, a=True, t=light_translate)
        cmds.parentConstraint(self.chara_light_move_child, self.chara_light_name, n=self.tmp_parent_constraint_name)
        cmds.currentTime(currentFrame)

        if play_state:
            cmds.play(state=True)

    def follow_light_to_persp(self):
        """
        perspカメラにcharaLightを追従させる
        """

        if not cmds.objExists(self.chara_light_name):
            return

        if not cmds.objExists(self.chara_light_rig_group):
            self._create_light_rig()

        # 追従解除
        if cmds.objExists(self.tmp_parent_constraint_name):
            self._reset_light_states()
            cmds.xform(self.chara_light_name, ws=True, a=True, t=self.before_aim_translate)

        # 追従開始
        else:
            self.before_aim_translate = cmds.xform(self.chara_light_name, q=True, ws=True, t=True)
            cmds.parentConstraint(self.chara_light_rig_aim, self.chara_light_name, mo=True, n=self.tmp_parent_constraint_name)

    def delete_chara_light_Rig(self):
        """
        charaLightRigを削除する
        """

        if cmds.objExists(self.chara_light_rig_group):
            cmds.delete(self.chara_light_rig_group)
