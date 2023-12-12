# -*- coding: utf-8 -*-

# --How to use--
# fk2ik=FK2IKMatch(mirrors=['_L_', '_R_'], types=['arms', 'legs'])
# fk2ik.left_enable=None # left controll only
# fk2ik.right_enable=None # right controll only
# fk2ik.match_func()
# fk2ik.main()

# --Extra--
# IK2FK
# fk2ik=fktoikmatch.FK2IKMatch(mirrors=['_L_', '_R_'], types=['arms', 'legs'], mirror_left_right=True, mirror_right_left=None,
#                  pos_set=None,
#                  rot_set={'arms':{'_L_':[{'clavicle_L_proxy_jnt':'clavicle_L_fk_ctrl'},
#                                          {'upperarm_L_proxy_jnt':'upperarm_L_fk_ctrl'},
#                                          {'lowerarm_L_proxy_jnt':'lowerarm_L_fk_ctrl'},
#                                          {'hand_L_proxy_jnt':'hand_L_fk_ctrl'}]},
#                           'legs':{'_L_':[{'thigh_L_proxy_jnt':'thigh_L_fk_ctrl'},
#                                          {'calf_L_proxy_jnt':'calf_L_fk_ctrl'},
#                                          {'foot_L_proxy_jnt':'foot_L_fk_ctrl'},
#                                          {'ball_L_proxy_jnt':'ball_L_fk_ctrl'}]}},
#                  pv_set=None)
#
# fk2ik=fktoikmatch.FK2IKMatch()
# # fk2ik.mirror_objects()
# fk2ik.match_func()
# fk2ik.main()

# --Extra--
# fk2ik=fktoikmatch.FK2IKMatch() # FK > IK
# fk2ik.match_func() # マッチ
# ik2fk.main() # マッチベイク
#
# ik2fk=fktoikmatch.IK2FKMatch() IK > FK
# ik2fk.match_func() # マッチ
# ik2fk.main() # マッチベイク

# --Extra--
# from tkgTools.tkgRig.scripts.ikfkMatch import common as ikfk_common
# reload(ikfk_common)
# --
# FK2IKMatch
# --
# # fk2ik arms l
# fk2ik=ikfk_common.FK2IKMatch(types=['arms'], left_enable=None, right_enable=None) # FK > IK
# fk2ik.match_func() # マッチ
# fk2ik.main() # マッチベイク

# # fk2ik arms r
# fk2ik=ikfk_common.FK2IKMatch(types=['arms'], left_enable=None, right_enable=None) # FK > IK
# fk2ik.match_func() # マッチ
# fk2ik.main() # マッチベイク
#
# # fk2ik legs
# fk2ik=ikfk_common.FK2IKMatch(types=['legs'], left_enable=None, right_enable=None) # FK > IK
# fk2ik.match_func() # マッチ
# fk2ik.main() # マッチベイク
#
# # fk2ik legs l
# fk2ik=ikfk_common.FK2IKMatch(types=['legs'], left_enable=None, right_enable=None) # FK > IK
# fk2ik.match_func() # マッチ
# fk2ik.main() # マッチベイク
#
# # fk2ik legs r
# fk2ik=ikfk_common.FK2IKMatch(types=['legs'], left_enable=None, right_enable=None) # FK > IK
# fk2ik.match_func() # マッチ
# fk2ik.main() # マッチベイク
#
# # fk2ik arms, legs l
# fk2ik=ikfk_common.FK2IKMatch(types=['arms', 'legs'], left_enable=None, right_enable=None) # FK > IK
# fk2ik.match_func() # マッチ
# fk2ik.main() # マッチベイク
#
# # fk2ik arms, legs r
# fk2ik=ikfk_common.FK2IKMatch(types=['arms', 'legs'], left_enable=None, right_enable=None) # FK > IK
# fk2ik.match_func() # マッチ
# fk2ik.main() # マッチベイク

# --
# IK2FKMatch
# --
# # ik2fk arms
# ik2fk=ikfk_common.IK2FKMatch(types=['arms'], left_enable=None, right_enable=None) # FK > IK
# ik2fk.match_func() # マッチ
# ik2fk.main() # マッチベイク
#
# # ik2fk arms l
# ik2fk=ikfk_common.IK2FKMatch(types=['arms'], left_enable=None, right_enable=None) # FK > IK
# ik2fk.match_func() # マッチ
# ik2fk.main() # マッチベイク
#
# # ik2fk arms r
# ik2fk=ikfk_common.IK2FKMatch(types=['arms'], left_enable=None, right_enable=None) # FK > IK
# ik2fk.match_func() # マッチ
# ik2fk.main() # マッチベイク
#
# # ik2fk legs
# ik2fk=ikfk_common.IK2FKMatch(types=['legs'], left_enable=None, right_enable=None) # FK > IK
# ik2fk.match_func() # マッチ
# ik2fk.main() # マッチベイク
#
# # ik2fk legs l
# ik2fk=ikfk_common.IK2FKMatch(types=['legs'], left_enable=None, right_enable=None) # FK > IK
# ik2fk.match_func() # マッチ
# ik2fk.main() # マッチベイク
#
# # ik2fk legs r
# ik2fk=ikfk_common.IK2FKMatch(types=['legs'], left_enable=None, right_enable=None) # FK > IK
# ik2fk.match_func() # マッチ
# ik2fk.main() # マッチベイク
#
# # ik2fk arms, legs l
# ik2fk=ikfk_common.IK2FKMatch(types=['arms', 'legs'], left_enable=None, right_enable=None) # FK > IK
# ik2fk.match_func() # マッチ
# ik2fk.main() # マッチベイク
#
# # ik2fk arms, legs r
# ik2fk=ikfk_common.IK2FKMatch(types=['arms', 'legs'], left_enable=None, right_enable=None) # FK > IK
# ik2fk.match_func() # マッチ
# ik2fk.main() # マッチベイク
# --
# IKFKMatchMan
# --
# IKFKスイッチアトリビュートを見てフルベイク
# ik2fk_fk2ik=ikfk_common.IKFKMatchMan()
#
# ik2fk_fk2ik.iktofk_match()
# ik2fk_fk2ik.fktoik_match()
#
# ik2fk_fk2ik.main()

# --
# With File Command
# --
# fk2ik_cc=ikfk_common.FK2IKMatch()
# ik2fk_cc=ikfk_common.IK2FKMatch()
# ikfk_man=ikfk_common.IKFKMatchMan()
#
# fk2ik_cc.export_settings(default=1)
# fk2ik_cc.import_fk_to_ik_setting='C:/fktoik_setting.json'
# fk2ik_cc.call_import_fk_to_ik_setting()
#
# ik2fk_cc.export_settings(default=1)
# ik2fk_cc.import_ik_to_fk_setting='C:/iktofk_setting.json'
# ik2fk_cc.call_import_ik_to_fk_setting()
#
# ikfk_man.export_settings(default=1)
# ikfk_man.import_ik_to_fk_setting='C:/iktofk_setting.json'
# ikfk_man.import_fk_to_ik_setting='C:/fktoik_setting.json'
# ikfk_man.import_switch_setting='C:/iktofk_switch_setting.json'
# ikfk_man.call_import_switch_setting()


import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
import maya.api.OpenMaya as om2

import codecs
import json
import math
import os

from collections import OrderedDict

default_fk_to_ik_pos_set = {'arms': {'_L_': [{'hand_L_proxy_jnt': 'hand_L_ik_ctrl'}],
                                     '_R_': [{'hand_R_proxy_jnt': 'hand_R_ik_ctrl'}]},
                            'legs': {'_L_': [{'foot_L_proxy_jnt': 'foot_L_ik_ctrl'}],
                                     '_R_': [{'foot_R_proxy_jnt': 'foot_R_ik_ctrl'}]}}

default_fk_to_ik_rot_set = {'arms': {'_L_': [{'hand_L_proxy_jnt': 'hand_L_ikRot_ctrl_ikRot_ctrl'},
                                             {'clavicle_L_proxy_jnt': 'clavicle_L_ikAutoRot_ctrl_ikAutoShoulder_ctrl'}],
                                     '_R_': [{'hand_R_proxy_jnt': 'hand_R_ikRot_ctrl_ikRot_ctrl'}, {
                                         'clavicle_R_proxy_jnt': 'clavicle_R_ikAutoRot_ctrl_ikAutoShoulder_ctrl'}]},
                            'legs': {'_L_': [{'ikfk_match_loc_foot_L_proxy_jnt': 'foot_L_ik_ctrl'},
                                             {'ball_L_proxy_jnt': 'foot_L_ik_ctrl_revFoot_holdBall_ctrl'}],
                                     '_R_': [{'ikfk_match_loc_foot_R_proxy_jnt': 'foot_R_ik_ctrl'},
                                             {'ball_R_proxy_jnt': 'foot_R_ik_ctrl_revFoot_holdBall_ctrl'}]}}

default_fk_to_ik_pv_set = {
    'arms': {'_L_': [{'upperarm_L_ik_pv_ctrl': ['upperarm_L_proxy_jnt', 'lowerarm_L_proxy_jnt', 'hand_L_proxy_jnt']}],
             '_R_': [{'upperarm_R_ik_pv_ctrl': ['upperarm_R_proxy_jnt', 'lowerarm_R_proxy_jnt', 'hand_R_proxy_jnt']}]},
    'legs': {'_L_': [{'calf_L_ik_pv_ctrl': ['thigh_L_proxy_jnt', 'calf_L_proxy_jnt', 'foot_L_proxy_jnt']}],
             '_R_': [{'calf_R_ik_pv_ctrl': ['thigh_R_proxy_jnt', 'calf_R_proxy_jnt', 'foot_R_proxy_jnt']}]}}

dir = '{}'.format(os.path.split(os.path.abspath(__file__))[0])
dir_path = dir.replace('\\', '/')

dataFolder = '{}/data/'.format(dir_path)


class FK2IKMatch(object):
    u"""IKFKMatch"""

    def __init__(self, namespace='ply00_m_000_000', mirrors=['_L_', '_R_'],
                 setkey_attrs=[u'tx', u'ty', u'tz', u'rx', u'ry', u'rz'], types=['arms', 'legs'],
                 pos_set=default_fk_to_ik_pos_set,
                 rot_set=default_fk_to_ik_rot_set,
                 pv_set=default_fk_to_ik_pv_set,
                 playbackSlider=None, mirror_left_right=None, mirror_right_left=None, left_enable=None,
                 right_enable=None, pole_vector_pos=30,
                 import_fk_to_ik_setting=None, import_ik_to_fk_setting=None, import_switch_setting=None,
                 spines_match=None):

        u"""Initialize
        param:
        """

        self.namespace = namespace
        self.setkey_attrs = setkey_attrs
        self.mirrors = mirrors

        self.types = types

        self.playbackSlider = playbackSlider

        self.arms_pos_ctrls = OrderedDict()
        self.arms_rot_ctrls = OrderedDict()
        self.arms_pv_ctrls = OrderedDict()

        self.legs_pos_ctrls = OrderedDict()
        self.legs_rot_ctrls = OrderedDict()
        self.legs_pv_ctrls = OrderedDict()

        self.pos_set = pos_set
        self.rot_set = rot_set
        self.pv_set = pv_set

        self.left_enable = left_enable
        self.right_enable = right_enable

        self.mirror_objects_left_right = mirror_left_right
        self.mirror_objects_right_left = mirror_right_left

        self.set_eulerFilter = True
        self.ctrls = []
        self.pole_vector_pos = pole_vector_pos

        self.import_fk_to_ik_setting = import_fk_to_ik_setting
        self.import_ik_to_fk_setting = import_ik_to_fk_setting
        self.import_switch_setting = import_switch_setting

        self.spines_match = spines_match

    def main(self, current_scene=None, save_path=None, bat_mode=None):
        u"""main実行関数
        """
        cmds.undoInfo(openChunk=True)
        try:
            cmds.refresh(su=1)
            self.matchbake()
            cmds.refresh(su=0)
        except Exception as e:
            cmds.refresh(su=0)
            print(e)
        cmds.undoInfo(closeChunk=True)

        # 保存するときの処理
        if bat_mode:
            fbxspl = current_scene.split('/')
            fname = fbxspl[-1].split('.')[0]

            cmds.file(rn='{0}/{1}.ma'.format(save_path, fname))
            cmds.file(f=1, save=1)

            print('Saved:{0}/{1}.ma'.format(save_path, fname))

        return

    def add_pos_obj(self, type=None, fkctrl=None, ikctrl=None):
        u"""ポジションのマッチするオブジェクトを登録"""
        if self.left_enable:
            if (
                    self.left_mir in fkctrl
                    and self.left_mir in ikctrl
            ):
                if type == 'arms' and 'arms' in self.left_enable:
                    self.arms_pos_ctrls.setdefault('{0}'.format(fkctrl), '{0}'.format(ikctrl))
                elif type == 'legs' and 'legs' in self.left_enable:
                    self.legs_pos_ctrls.setdefault('{0}'.format(fkctrl), '{0}'.format(ikctrl))

        if self.right_enable:
            if (
                    self.right_mir in fkctrl
                    and self.right_mir in ikctrl
            ):
                if type == 'arms' and 'arms' in self.right_enable:
                    self.arms_pos_ctrls.setdefault('{0}'.format(fkctrl), '{0}'.format(ikctrl))
                elif type == 'legs' and 'legs' in self.right_enable:
                    self.legs_pos_ctrls.setdefault('{0}'.format(fkctrl), '{0}'.format(ikctrl))

    def add_rot_obj(self, type=None, fkctrl=None, ikctrl=None):
        u"""回転のマッチするオブジェクトを登録"""
        if self.left_enable:
            if (
                    self.left_mir in fkctrl
                    and self.left_mir in ikctrl
            ):
                if type == 'arms' and 'arms' in self.left_enable:
                    self.arms_rot_ctrls.setdefault('{0}'.format(fkctrl), '{0}'.format(ikctrl))
                elif type == 'legs' and 'legs' in self.left_enable:
                    self.legs_rot_ctrls.setdefault('{0}'.format(fkctrl), '{0}'.format(ikctrl))

        if self.right_enable:
            if (
                    self.right_mir in fkctrl
                    and self.right_mir in ikctrl
            ):
                if type == 'arms' and 'arms' in self.right_enable:
                    self.arms_rot_ctrls.setdefault('{0}'.format(fkctrl), '{0}'.format(ikctrl))
                elif type == 'legs' and 'legs' in self.right_enable:
                    self.legs_rot_ctrls.setdefault('{0}'.format(fkctrl), '{0}'.format(ikctrl))

    def add_pv_obj(self, type=None, fkctrl_start=None, fkctrl_mid=None, fkctrl_end=None, ikctrl=None):
        u"""PoleVextorのマッチするオブジェクトを登録"""
        # if type == 'arms':
        #     self.arms_pv_ctrls.setdefault('ikpv', '{0}'.format(ikctrl))
        #     self.arms_pv_ctrls.setdefault('fkstart', '{0}'.format(fkctrl_start))
        #     self.arms_pv_ctrls.setdefault('fkmid', '{0}'.format(fkctrl_mid))
        #     self.arms_pv_ctrls.setdefault('fkend', '{0}'.format(fkctrl_end))
        # elif type == 'legs':
        #     self.legs_pv_ctrls.setdefault('ikpv', '{0}'.format(ikctrl))
        #     self.legs_pv_ctrls.setdefault('fkstart', '{0}'.format(fkctrl_start))
        #     self.legs_pv_ctrls.setdefault('fkmid', '{0}'.format(fkctrl_mid))
        #     self.legs_pv_ctrls.setdefault('fkend', '{0}'.format(fkctrl_end))

        if self.left_enable:
            if (
                    self.left_mir in fkctrl_start
                    and self.left_mir in fkctrl_mid
                    and self.left_mir in fkctrl_end
                    and self.left_mir in ikctrl
            ):
                if type == 'arms' and 'arms' in self.left_enable:
                    self.arms_pv_ctrls.setdefault('{0}'.format(ikctrl),
                                                  ['{0}'.format(fkctrl_start), '{0}'.format(fkctrl_mid),
                                                   '{0}'.format(fkctrl_end)])
                elif type == 'legs' and 'legs' in self.left_enable:
                    self.legs_pv_ctrls.setdefault('{0}'.format(ikctrl),
                                                  ['{0}'.format(fkctrl_start), '{0}'.format(fkctrl_mid),
                                                   '{0}'.format(fkctrl_end)])

        if self.right_enable:
            if (
                    self.right_mir in fkctrl_start
                    and self.right_mir in fkctrl_mid
                    and self.right_mir in fkctrl_end
                    and self.right_mir in ikctrl
            ):
                if type == 'arms' and 'arms' in self.right_enable:
                    self.arms_pv_ctrls.setdefault('{0}'.format(ikctrl),
                                                  ['{0}'.format(fkctrl_start), '{0}'.format(fkctrl_mid),
                                                   '{0}'.format(fkctrl_end)])
                elif type == 'legs' and 'legs' in self.right_enable:
                    self.legs_pv_ctrls.setdefault('{0}'.format(ikctrl),
                                                  ['{0}'.format(fkctrl_start), '{0}'.format(fkctrl_mid),
                                                   '{0}'.format(fkctrl_end)])

    def check_exists(self, obj):
        if cmds.objExists(obj):
            return True
        else:
            cmds.warning('{0} is not exist.'.format(obj))
            return False

    def matchsetkeys(self, type=None, setkey_attrs=None):
        u"""PoleVextorのマッチするオブジェクトを登録"""
        pos_ctrls = None
        rot_ctrls = None
        pv_ctrls = None
        if type == 'arms':
            pos_ctrls = self.arms_pos_ctrls
            rot_ctrls = self.arms_rot_ctrls
            pv_ctrls = self.arms_pv_ctrls
        elif type == 'legs':
            pos_ctrls = self.legs_pos_ctrls
            rot_ctrls = self.legs_rot_ctrls
            pv_ctrls = self.legs_pv_ctrls

        # pos
        if pos_ctrls:
            for fk_pos, ik_pos in pos_ctrls.items():
                if (
                        self.check_exists(fk_pos)
                        or self.check_exists(ik_pos)
                ):
                    cmds.matchTransform('{0}'.format(ik_pos), '{0}'.format(fk_pos), pos=1)
                    self.ctrls.append(ik_pos)
                else:
                    return

            cmds.setKeyframe(list(pos_ctrls.values()), at=setkey_attrs)

        # pv
        if pv_ctrls:
            for ik_pv, fk_pv_list in pv_ctrls.items():
                if (
                        self.check_exists(ik_pv)
                        or self.check_exists(fk_pv_list[0])
                        or self.check_exists(fk_pv_list[1])
                        or self.check_exists(fk_pv_list[2])
                ):
                    loc = get_poleVector_position(startObj=fk_pv_list[0], middleObj=fk_pv_list[1], endObj=fk_pv_list[2],
                                                  move=30)

                    # loc = cmds.spaceLocator()
                    # cmds.pointConstraint('{0}'.format(pv_ctrl['fkstart']), loc[0], w=1)
                    # cmds.pointConstraint('{0}'.format(pv_ctrl['fkend']), loc[0], w=1)
                    #
                    # cmds.aimConstraint('{0}'.format(pv_ctrl['fkmid']), loc[0], weight=1, upVector=(0, 1, 0), worldUpType="object", offset=(0, 0, 0), aimVector=(1, 0, 0), worldUpObject=pv_ctrl['fkstart'])
                    #
                    # dup_loc=cmds.duplicate(loc[0], po=1)
                    # cmds.parent(dup_loc[0], loc[0])
                    # # cmds.matchTransform(dup_loc[0], pv_ctrl['fkmid'], pos=1)
                    # distance=get_distance(dup_loc[0], pv_ctrl['fkmid'])
                    # cmds.move(distance, 0, 0, dup_loc[0], os=1, r=1, wd=1)
                    # cmds.xform(dup_loc[0], ro=[0,0,0], a=1, os=1)
                    # cmds.move(30, 0, 0, dup_loc[0], os=1, r=1, wd=1)
                    cmds.matchTransform('{0}'.format(ik_pv), loc)

                    cmds.setKeyframe(ik_pv, at=setkey_attrs)

                    cmds.delete(loc)

                    self.ctrls.append(ik_pv)
                else:
                    return

        # rot
        if rot_ctrls:
            for fk_rot, ik_rot in rot_ctrls.items():
                if (
                        self.check_exists(fk_rot)
                        or self.check_exists(ik_rot)
                ):
                    cmds.matchTransform('{0}'.format(ik_rot), '{0}'.format(fk_rot), rot=1)
                    self.ctrls.append(ik_rot)
                else:
                    return
            cmds.setKeyframe(list(rot_ctrls.values()), at=setkey_attrs)

    def mirror_objects(self):
        if self.pos_set:
            add_objects_dict = self.pos_set
            self.mirror_sets(set_objects=add_objects_dict, add_type='pos')
        if self.rot_set:
            add_objects_dict = self.rot_set
            self.mirror_sets(set_objects=add_objects_dict, add_type='rot')
        if self.pv_set:
            add_objects_dict = self.pv_set
            self.mirror_sets(set_objects=add_objects_dict, add_type='pv')

    def mirror_sets(self, set_objects=None, add_type=None):
        set_objects_buf = set_objects
        for type, match_objects in set_objects_buf.items():
            for mir, objects in match_objects.items():
                objects_buf = []
                for obj_var in objects:
                    for mat_objA, mat_objB in obj_var.items():
                        if self.mirror_objects_left_right:
                            mir = mir.replace(self.left_mir, self.right_mir)
                            if add_type == 'pos' or add_type == 'rot':
                                mat_objA, mat_objB = mat_objA.replace(self.left_mir, self.right_mir), mat_objB.replace(
                                    self.left_mir, self.right_mir)
                            elif add_type == 'pv':
                                mat_objA = mat_objA.replace(self.left_mir, self.right_mir)
                                mat_objB = [objB.replace(self.left_mir, self.right_mir) for objB in mat_objB]
                        elif self.mirror_objects_right_left:
                            mir = mir.replace(self.right_mir, self.left_mir)
                            if add_type == 'pos' or add_type == 'rot':
                                mat_objA, mat_objB = mat_objA.replace(self.right_mir, self.left_mir), mat_objB.replace(
                                    self.right_mir, self.left_mir)
                            elif add_type == 'pv':
                                mat_objA = mat_objA.replace(self.right_mir, self.left_mir)
                                mat_objB = [objB.replace(self.right_mir, self.left_mir) for objB in mat_objB]

                        objects_buf.append({mat_objA: mat_objB})

                set_objects_buf[type][mir] = objects_buf

        # print(set_objects_buf)

    def add_objects(self, add_type=None):
        if add_type == 'pos':
            add_objects_dict = self.pos_set
        elif add_type == 'rot':
            add_objects_dict = self.rot_set
        elif add_type == 'pv':
            add_objects_dict = self.pv_set

        for type, match_objects in add_objects_dict.items():
            for mir, objects in match_objects.items():
                for obj_var in objects:
                    for mat_objA, mat_objB in obj_var.items():
                        if add_type == 'pos':
                            self.add_pos_obj(type=type, fkctrl='{0}:{1}'.format(self.namespace, mat_objA),
                                             ikctrl='{0}:{1}'.format(self.namespace, mat_objB))
                        elif add_type == 'rot':
                            self.add_rot_obj(type=type, fkctrl='{0}:{1}'.format(self.namespace, mat_objA),
                                             ikctrl='{0}:{1}'.format(self.namespace, mat_objB))
                        elif add_type == 'pv':
                            self.add_pv_obj(type=type,
                                            fkctrl_start='{0}:{1}'.format(self.namespace, mat_objB[0]),
                                            fkctrl_mid='{0}:{1}'.format(self.namespace, mat_objB[1]),
                                            fkctrl_end='{0}:{1}'.format(self.namespace, mat_objB[2]),
                                            ikctrl='{0}:{1}'.format(self.namespace, mat_objA))

    def match_func(self):
        if self.mirrors:
            self.left_mir = self.mirrors[0]
            self.right_mir = self.mirrors[1]

        if self.mirror_objects_left_right or self.mirror_objects_right_left:
            self.mirror_objects()
        # pos
        if self.pos_set:
            self.add_objects(add_type='pos')

        # rot
        if self.rot_set:
            self.add_objects(add_type='rot')

        # pv
        if self.pv_set:
            self.add_objects(add_type='pv')

        # functions
        if self.types:
            for type in self.types:
                self.matchsetkeys(type=type, setkey_attrs=self.setkey_attrs)

    def spines_match_func(self):
        if self.spines_match == 'FK2IK':
            default_fk_to_ik_pos_set = {
                'spines': {'_C_': [{'spine_C_02_proxy_jnt': 'spine_C_02_proxy_jnt_ikSpline_point_ctrl'},
                                   {'spine_C_03_proxy_jnt': 'spine_C_03_proxy_jnt_ikSpline_main_ctrl'}, ]
                           }
            }

            default_fk_to_ik_rot_set = {
                'spines': {'_C_': [{'spine_C_01_proxy_jnt': 'spine_C_01_proxy_jnt_ikSpline_main_ctrl'},
                                   {'spine_C_01_proxy_jnt': 'spine_C_01_proxy_jnt_ikSpline_rotate_ctrl'},
                                   {'spine_C_02_proxy_jnt': 'spine_C_02_proxy_jnt_ikSpline_rotate_ctrl'},
                                   {'spine_C_03_proxy_jnt': 'spine_C_03_proxy_jnt_ikSpline_rotate_ctrl'}, ]
                           }
            }

            pos_match_list = default_fk_to_ik_pos_set['spines']['_C_']
            rot_match_list = default_fk_to_ik_rot_set['spines']['_C_']

            for match_obj in pos_match_list:
                src = '{0}:{1}'.format(self.namespace, list(match_obj.keys())[0])
                dst = '{0}:{1}'.format(self.namespace, list(match_obj.values())[0])
                cmds.matchTransform(dst, src)
                self.ctrls.append(dst)
                cmds.setKeyframe(dst, at=self.setkey_attrs)

            for match_obj in rot_match_list:
                src = '{0}:{1}'.format(self.namespace, list(match_obj.keys())[0])
                dst = '{0}:{1}'.format(self.namespace, list(match_obj.values())[0])
                cmds.matchTransform(dst, src)
                self.ctrls.append(dst)
                cmds.setKeyframe(dst, at=self.setkey_attrs)

        elif self.spines_match == 'IK2FK':
            default_ik_to_fk_rot_set = {'spines': {'_C_': [{'spine_C_01_proxy_jnt': 'spine_C_01_fk_ctrl'},
                                                           {'spine_C_02_proxy_jnt': 'spine_C_02_fk_ctrl'},
                                                           {'spine_C_03_proxy_jnt': 'spine_C_03_fk_ctrl'}, ]
                                                   }
                                        }

            rot_match_list = default_ik_to_fk_rot_set['spines']['_C_']

            for match_obj in rot_match_list:
                src = '{0}:{1}'.format(self.namespace, list(match_obj.keys())[0])
                dst = '{0}:{1}'.format(self.namespace, list(match_obj.values())[0])
                cmds.matchTransform(dst, src)
                self.ctrls.append(dst)
                cmds.setKeyframe(dst, at=self.setkey_attrs)

    def matchbake(self):
        u"""フレーム毎にベイク"""
        # check and save current autokey state
        cur_time = cmds.currentTime(q=1)
        if cmds.autoKeyframe(q=True, st=True):
            autoKeyState = 1
        else:
            autoKeyState = 0

        cmds.autoKeyframe(st=0)

        playmin = cmds.playbackOptions(q=1, min=1)
        playmax = cmds.playbackOptions(q=1, max=1)

        start = playmin
        end = playmax - 1

        if self.playbackSlider:
            gPlayBackSlider = mel.eval('$temp=$gPlayBackSlider')
            if gPlayBackSlider:
                if cmds.timeControl(gPlayBackSlider, q=True, rv=True):
                    frameRange = cmds.timeControl(gPlayBackSlider, q=True, ra=True)
                    start = frameRange[0]
                    end = frameRange[1] - 1
                else:
                    frameRange = cmds.currentTime(q=1)
                    start = frameRange
                    end = frameRange - 1

        for i in range(int(start - 1), int(end + 2)):
            cmds.currentTime(i, e=True)
            if self.spines_match:
                self.spines_match_func()
            self.match_func()
        cmds.currentTime(cur_time)
        cmds.autoKeyframe(state=autoKeyState)

        sort_ctrls = list(set(self.ctrls))
        if self.ctrls and self.set_eulerFilter:
            cmds.filterCurve(sort_ctrls, f='euler')
            print('Euler Filter:{0}'.format(sort_ctrls))

    def export_settings(self, file_path=None, default=None, objects_values=None):
        if not file_path:
            file_path = fileDialog_export()

        if default:
            objects_values = {}
            objects_values['pos'] = self.pos_set
            objects_values['rot'] = self.rot_set
            objects_values['pv'] = self.pv_set

        create_json = JsonFile()
        dirname, basename = os.path.split(file_path)
        save_file_path = '{0}/{1}'.format(dirname, basename)
        if objects_values:
            create_json.write('{0}'.format(save_file_path), objects_values)

    def import_settings(self, file_path=None):
        if not file_path:
            file_path = fileDialog_import()

        create_json = JsonFile()
        dirname, basename = os.path.split(file_path)
        import_file_path = '{0}/{1}'.format(dirname, basename)
        import_values = create_json.read(import_file_path)

        self.pos_set = import_values['pos']
        self.rot_set = import_values['rot']
        self.pv_set = import_values['pv']

        print('Import File:{0}'.format(file_path))
        # print('Imported:{0}\n{1}\n{2}\n'.format(self.pos_set, self.rot_set, self.pv_set))

    def call_import_ik_to_fk_setting(self):
        if self.import_ik_to_fk_setting:
            self.import_settings(file_path=self.import_ik_to_fk_setting)

    def call_import_fk_to_ik_setting(self):
        if self.import_fk_to_ik_setting:
            self.import_settings(file_path=self.import_fk_to_ik_setting)


default_ik_to_fk_pos_set = None

default_ik_to_fk_rot_set = {'arms': {'_L_': [{'clavicle_L_proxy_jnt': 'clavicle_L_fk_ctrl'},
                                             {'upperarm_L_proxy_jnt': 'upperarm_L_fk_ctrl'},
                                             {'lowerarm_L_proxy_jnt': 'lowerarm_L_fk_ctrl'},
                                             {'hand_L_proxy_jnt': 'hand_L_fk_ctrl'}]},
                            'legs': {'_L_': [{'thigh_L_proxy_jnt': 'thigh_L_fk_ctrl'},
                                             {'calf_L_proxy_jnt': 'calf_L_fk_ctrl'},
                                             {'foot_L_proxy_jnt': 'foot_L_fk_ctrl'},
                                             {'ball_L_proxy_jnt': 'ball_L_fk_ctrl'}]}}

default_ik_to_fk_pv_set = None


class IK2FKMatch(FK2IKMatch):
    def __init__(self, namespace='ply00_m_000_000', mirrors=['_L_', '_R_'],
                 setkey_attrs=[u'tx', u'ty', u'tz', u'rx', u'ry', u'rz'], types=['arms', 'legs'],
                 pos_set=default_ik_to_fk_pos_set,
                 rot_set=default_ik_to_fk_rot_set,
                 pv_set=default_ik_to_fk_pv_set,
                 playbackSlider=None, mirror_left_right=True, mirror_right_left=None, left_enable=None,
                 right_enable=None,
                 import_fk_to_ik_setting=None, import_ik_to_fk_setting=None, import_switch_setting=None,
                 spines_match=None):
        super(IK2FKMatch, self).__init__(namespace=namespace,
                                         mirrors=mirrors,
                                         setkey_attrs=setkey_attrs,
                                         types=types,
                                         pos_set=pos_set,
                                         rot_set=rot_set,
                                         pv_set=pv_set,
                                         playbackSlider=playbackSlider,
                                         mirror_left_right=mirror_left_right,
                                         mirror_right_left=mirror_right_left,
                                         left_enable=left_enable,
                                         right_enable=right_enable,
                                         import_fk_to_ik_setting=import_fk_to_ik_setting,
                                         import_ik_to_fk_setting=import_ik_to_fk_setting,
                                         import_switch_setting=import_switch_setting,
                                         spines_match=spines_match)

    def match_func(self):
        super(IK2FKMatch, self).match_func()

    def main(self, current_scene=None, save_path=None, bat_mode=None):
        super(IK2FKMatch, self).main(current_scene,
                                     save_path,
                                     bat_mode)


def fileDialog_export():
    filename = cmds.fileDialog2(ds=2, cap='File', okc='Done', ff='*.json', fm=0)
    if filename is None:
        return False
    return filename[0]


def fileDialog_import():
    filename = cmds.fileDialog2(ds=2, cap='File', okc='Done', ff='*.json', fm=1)
    if filename is None:
        return
    return filename[0]


def get_poleVector_position(startObj=None, middleObj=None, endObj=None, move=None):
    if startObj == None or middleObj == None or endObj == None:
        sel = cmds.ls(os=1)
        try:
            startObj = sel[0]
            middleObj = sel[1]
            endObj = sel[2]
        except Exception as e:
            return
    start = cmds.xform(startObj, q=1, ws=1, t=1)
    mid = cmds.xform(middleObj, q=1, ws=1, t=1)
    end = cmds.xform(endObj, q=1, ws=1, t=1)
    startV = om.MVector(start[0], start[1], start[2])
    midV = om.MVector(mid[0], mid[1], mid[2])
    endV = om.MVector(end[0], end[1], end[2])
    startEnd = endV - startV
    startMid = midV - startV
    dotP = startMid * startEnd
    proj = float(dotP) / float(startEnd.length())
    startEndN = startEnd.normal()
    projV = startEndN * proj
    arrowV = startMid - projV
    arrowV *= 0.5
    finalV = arrowV + midV
    cross1 = startEnd ^ startMid
    cross1.normalize()
    cross2 = cross1 ^ arrowV
    cross2.normalize()
    arrowV.normalize()
    matrixV = [arrowV.x, arrowV.y, arrowV.z, 0, cross1.x, cross1.y, cross1.z, 0, cross2.x, cross2.y, cross2.z, 0, 0, 0,
               0, 1]
    matrixM = om.MMatrix()
    om.MScriptUtil.createMatrixFromList(matrixV, matrixM)
    matrixFn = om.MTransformationMatrix(matrixM)
    rot = matrixFn.eulerRotation()

    pvLoc = cmds.spaceLocator(n='{}_poleVecPosLoc'.format(middleObj))
    cmds.xform(pvLoc[0], ws=1, t=(finalV.x, finalV.y, finalV.z))
    cmds.xform(pvLoc[0], ws=1,
               rotation=((rot.x / math.pi * 180.0), (rot.y / math.pi * 180.0), (rot.z / math.pi * 180.0)))
    cmds.select(pvLoc[0])
    cmds.move(move, 0, 0, r=1, os=1, wd=1)
    cmds.select(cl=True)

    # result = {pvLoc:{'translate':(finalV.x , finalV.y ,finalV.z), 'rotate':((rot.x/math.pi*180.0),(rot.y/math.pi*180.0),(rot.z/math.pi*180.0))}}
    return pvLoc[0]


def convert_switch(node_dict, namespace):
    new_node_dict = {}
    for node, types in node_dict.items():
        if '|' in node:
            node_spl = node.split('|')
            new_names = ['{0}:{1}'.format(namespace, node) for node in node_spl]
            node = '|'.join(new_names)

        new_node_dict[node] = types

    return new_node_dict


def getAttr_switch(node_dict):
    new_node_dict = {}
    for node, types in node_dict.items():
        if cmds.objExists(node.split('.')[0]):
            value = cmds.getAttr(node)
            switch_type = node_dict[node][value]
        else:
            cmds.warning('{0} is not exists.'.format(node.split('.')[0]))

    return switch_type


def setAttr_switch(node_dict, set_type, animcheck):
    new_node_dict = {}
    for node, types in node_dict.items():
        for value, type in types.items():
            if cmds.objExists(node.split('.')[0]):
                if type == set_type:
                    if check_switch_anim(node):
                        print('Animkey:{0}'.format(node))
                        return
                    cmds.setAttr(node, float(value))
                    print('Set:{0} {1} {2}'.format(node, set_type, value))
            else:
                cmds.warning('{0} is not exists.'.format(node.split('.')[0]))


def check_switch_anim(node):
    listConnections = cmds.listConnections(node, s=1)
    if listConnections:
        for con_src in listConnections:
            if (
                    cmds.objectType(con_src) == 'animCurveTA'
                    or cmds.objectType(con_src) == 'animCurveTU'
                    or cmds.objectType(con_src) == 'animCurveTL'
            ):
                return True


default_arms_L_switch = {"hand_L_fk_ctrl|arms_L_01_IKFK_shared_crvShape.IKFK": {0: 'fk', 1: 'ik'}}

default_arms_R_switch = {"hand_R_fk_ctrl|arms_R_01_IKFK_shared_crvShape.IKFK": {0: 'fk', 1: 'ik'}}

default_legs_L_switch = {"ballend_L_fk_ctrl|legs_L_01_IKFK_shared_crvShape.IKFK": {0: 'fk', 1: 'ik'}}

default_legs_R_switch = {"ballend_R_fk_ctrl|legs_R_01_IKFK_shared_crvShape.IKFK": {0: 'fk', 1: 'ik'}}

default_spines_C_switch = {"spine_C_03_fk_ctrl|spine_01_IKFK_shared_crvShape.IKFK": {0: 'fk', 1: 'ik'}}


class IKFKMatchMan(object):
    def __init__(self, order=None, namespace='ply00_m_000_000', mirrors=['_L_', '_R_'],
                 setkey_attrs=[u'tx', u'ty', u'tz', u'rx', u'ry', u'rz'], types=['arms', 'legs'],
                 playbackSlider=None, mirror_left_right=True, mirror_right_left=None, left_enable=['arms', 'legs'],
                 right_enable=['arms', 'legs'],
                 arms_L_switch=default_arms_L_switch, arms_R_switch=default_arms_R_switch,
                 legs_L_switch=default_legs_L_switch, legs_R_switch=default_legs_R_switch,
                 spines_C_switch=default_spines_C_switch,
                 import_fk_to_ik_setting=None, import_ik_to_fk_setting=None, import_switch_setting=None):

        """Initialize
        order='ik2fk' or 'fk2ik'
        ik2fk_fk2ik=fktoikmatch.IKFKMatchMan()

        ik2fk_fk2ik.iktofk_match()
        ik2fk_fk2ik.fktoik_match()
        """
        self.order = order

        self.init_arms_L_switch = arms_L_switch
        self.init_arms_R_switch = arms_R_switch
        self.init_legs_L_switch = legs_L_switch
        self.init_legs_R_switch = legs_R_switch
        self.init_spines_C_switch = spines_C_switch

        self.arms_L_switch = convert_switch(arms_L_switch, namespace)
        self.arms_R_switch = convert_switch(arms_R_switch, namespace)
        self.legs_L_switch = convert_switch(legs_L_switch, namespace)
        self.legs_R_switch = convert_switch(legs_R_switch, namespace)
        self.spines_C_switch = convert_switch(spines_C_switch, namespace)

        self.left_enable = left_enable
        self.right_enable = right_enable
        self.types = types
        self.playbackSlider = playbackSlider
        self.namespace = namespace

        self.import_fk_to_ik_setting = import_fk_to_ik_setting
        self.import_ik_to_fk_setting = import_ik_to_fk_setting
        self.import_switch_setting = import_switch_setting

        self.fk2ik = FK2IKMatch(namespace=self.namespace,
                                mirrors=mirrors,
                                setkey_attrs=setkey_attrs,
                                types=types,
                                playbackSlider=playbackSlider,
                                mirror_left_right=mirror_left_right,
                                mirror_right_left=mirror_right_left,
                                left_enable=left_enable,
                                right_enable=right_enable,
                                import_fk_to_ik_setting=self.import_fk_to_ik_setting,
                                import_ik_to_fk_setting=self.import_ik_to_fk_setting,
                                import_switch_setting=self.import_switch_setting,
                                spines_match='FK2IK')

        self.ik2fk = IK2FKMatch(namespace=self.namespace,
                                mirrors=mirrors,
                                setkey_attrs=setkey_attrs,
                                types=types,
                                playbackSlider=playbackSlider,
                                mirror_left_right=mirror_left_right,
                                mirror_right_left=mirror_right_left,
                                left_enable=left_enable,
                                right_enable=right_enable,
                                import_fk_to_ik_setting=self.import_fk_to_ik_setting,
                                import_ik_to_fk_setting=self.import_ik_to_fk_setting,
                                import_switch_setting=self.import_switch_setting,
                                spines_match='IK2FK')

        print(self.import_fk_to_ik_setting, self.import_ik_to_fk_setting, self.import_switch_setting)

        self.set_eulerFilter = True
        self.ctrls = []

    def main(self, current_scene=None, save_path=None, bat_mode=None, set_switch=None):
        u"""main実行関数
        """
        cmds.undoInfo(openChunk=True)
        try:
            cmds.refresh(su=1)
            self.check_set_switch(set_switch)
            self.matchbake()
            cmds.refresh(su=0)
        except Exception as e:
            cmds.refresh(su=0)
            print(e)
        cmds.undoInfo(closeChunk=True)

        # 保存するときの処理
        if bat_mode:
            fbxspl = current_scene.split('/')
            fname = fbxspl[-1].split('.')[0]

            cmds.file(rn='{0}/{1}.ma'.format(save_path, fname))
            cmds.file(f=1, save=1)

            print('Saved:{0}/{1}.ma'.format(save_path, fname))

        return

    def reset_switch(self):
        self.fk2ik.left_enable = self.left_enable
        self.fk2ik.right_enable = self.left_enable
        self.fk2ik.types = self.types

        self.ik2fk.left_enable = self.left_enable
        self.ik2fk.right_enable = self.left_enable
        self.ik2fk.types = self.types

    def fktoik_match(self):
        self.fk2ik.match_func()
        self.reset_switch()

    def fktoik_bake(self):
        self.fk2ik.main()

    def iktofk_match(self):
        self.ik2fk.match_func()
        self.reset_switch()

    def iktofk_bake(self):
        self.ik2fk.main()

    def order_match(self):
        if self.order == 'ik2fk':
            self.ik2fk.match_func()
            self.fk2ik.match_func()
        elif self.order == 'fk2ik':
            self.fk2ik.match_func()
            self.ik2fk.match_func()

    def order_bake(self):
        if self.order == 'ik2fk':
            self.ik2fk.main()
            self.fk2ik.main()
        elif self.order == 'fk2ik':
            self.fk2ik.main()
            self.ik2fk.main()

    def matchbake(self):
        u"""フレーム毎にベイク"""
        # check and save current autokey state
        cur_time = cmds.currentTime(q=1)
        if cmds.autoKeyframe(q=True, st=True):
            autoKeyState = 1
        else:
            autoKeyState = 0

        cmds.autoKeyframe(st=0)

        playmin = cmds.playbackOptions(q=1, min=1)
        playmax = cmds.playbackOptions(q=1, max=1)

        start = playmin
        end = playmax - 1

        if self.playbackSlider:
            gPlayBackSlider = mel.eval('$temp=$gPlayBackSlider')
            if gPlayBackSlider:
                if cmds.timeControl(gPlayBackSlider, q=True, rv=True):
                    frameRange = cmds.timeControl(gPlayBackSlider, q=True, ra=True)
                    start = frameRange[0]
                    end = frameRange[1] - 1
                else:
                    frameRange = cmds.currentTime(q=1)
                    start = frameRange
                    end = frameRange - 1

        for i in range(int(start - 1), int(end + 2)):
            cmds.currentTime(i, e=True)
            if self.arms_L_switch:
                arms_L_type = getAttr_switch(self.arms_L_switch)
                if arms_L_type == 'fk':
                    self.fk2ik.left_enable = ['arms']
                    self.fk2ik.types = ['arms']
                    self.fktoik_match()
                    self.ctrls += self.fk2ik.ctrls
                else:
                    self.ik2fk.left_enable = ['arms']
                    self.ik2fk.types = ['arms']
                    self.iktofk_match()
                    self.ctrls += self.ik2fk.ctrls

            if self.arms_R_switch:
                arms_L_type = getAttr_switch(self.arms_R_switch)
                if arms_L_type == 'fk':
                    self.fk2ik.right_enable = ['arms']
                    self.fk2ik.types = ['arms']
                    self.fktoik_match()
                    self.ctrls += self.fk2ik.ctrls
                else:
                    self.ik2fk.right_enable = ['arms']
                    self.ik2fk.types = ['arms']
                    self.iktofk_match()
                    self.ctrls += self.ik2fk.ctrls

            if self.legs_L_switch:
                legs_L_type = getAttr_switch(self.legs_L_switch)
                if legs_L_type == 'fk':
                    self.fk2ik.left_enable = ['legs']
                    self.fk2ik.types = ['legs']
                    self.fktoik_match()
                    self.ctrls += self.fk2ik.ctrls
                else:
                    self.ik2fk.left_enable = ['legs']
                    self.ik2fk.types = ['legs']
                    self.iktofk_match()
                    self.ctrls += self.ik2fk.ctrls

            if self.legs_R_switch:
                legs_R_type = getAttr_switch(self.legs_R_switch)
                if legs_R_type == 'fk':
                    self.fk2ik.right_enable = ['legs']
                    self.fk2ik.types = ['legs']
                    self.fktoik_match()
                    self.ctrls += self.fk2ik.ctrls
                else:
                    self.ik2fk.right_enable = ['legs']
                    self.ik2fk.types = ['legs']
                    self.iktofk_match()
                    self.ctrls += self.ik2fk.ctrls

            if self.spines_C_switch:
                spines_C_type = getAttr_switch(self.spines_C_switch)
                if spines_C_type == 'fk':
                    self.fk2ik.spines_match_func()
                    self.ctrls += self.fk2ik.ctrls
                else:
                    self.ik2fk.spines_match_func()
                    self.ctrls += self.ik2fk.ctrls

        cmds.currentTime(cur_time)
        cmds.autoKeyframe(state=autoKeyState)

        sort_ctrls = list(set(self.ctrls))
        if self.ctrls and self.set_eulerFilter:
            cmds.filterCurve(sort_ctrls, f='euler')
            print('Euler Filter:{0}'.format(sort_ctrls))

    def export_settings(self, file_path=None, default=None, objects_values=None):
        if not file_path:
            file_path = fileDialog_export()

        if default:
            objects_values = {}
            objects_values['arms_L_switch'] = self.init_arms_L_switch
            objects_values['arms_R_switch'] = self.init_arms_R_switch
            objects_values['legs_L_switch'] = self.init_legs_L_switch
            objects_values['legs_R_switch'] = self.init_legs_R_switch
            objects_values['spines_C_switch'] = self.init_spines_C_switch

        create_json = JsonFile()
        dirname, basename = os.path.split(file_path)
        save_file_path = '{0}/{1}'.format(dirname, basename)
        if objects_values:
            create_json.write('{0}'.format(save_file_path), objects_values)

    def import_settings(self, file_path=None):
        if not file_path:
            file_path = fileDialog_import()

        create_json = JsonFile()
        dirname, basename = os.path.split(file_path)
        import_file_path = '{0}/{1}'.format(dirname, basename)
        import_values = create_json.read(import_file_path)

        self.arms_L_switch = convert_switch(import_values['arms_L_switch'], self.namespace)
        self.arms_R_switch = convert_switch(import_values['arms_R_switch'], self.namespace)
        self.legs_L_switch = convert_switch(import_values['legs_L_switch'], self.namespace)
        self.legs_R_switch = convert_switch(import_values['legs_R_switch'], self.namespace)
        self.spines_C_switch = convert_switch(import_values['spines_C_switch'], self.namespace)

        print('Import File:{0}'.format(file_path))
        # print('Imported:{0}\n{1}\n{2}\n{3}\n'.format(self.arms_L_switch, self.arms_R_switch, self.legs_L_switch, self.legs_R_switch))

    def call_import_switch_setting(self):
        if self.import_switch_setting:
            self.import_settings(file_path=self.import_switch_setting)

    def check_set_switch(self, set_switch):
        if not set_switch:
            return
        spl_set_switch = set_switch.split(',')
        set_switch_list = list(set(spl_set_switch))

        if 'arms_l_fk' in set_switch_list:
            setAttr_switch(self.arms_L_switch, 'fk', True)

        if 'arms_r_fk' in set_switch_list:
            setAttr_switch(self.arms_R_switch, 'fk', True)

        if 'arms_l_ik' in set_switch_list:
            setAttr_switch(self.arms_L_switch, 'ik', True)

        if 'arms_r_ik' in set_switch_list:
            setAttr_switch(self.arms_R_switch, 'ik', True)

        if 'legs_l_fk' in set_switch_list:
            setAttr_switch(self.legs_L_switch, 'fk', True)

        if 'legs_r_fk' in set_switch_list:
            setAttr_switch(self.legs_R_switch, 'fk', True)

        if 'legs_l_ik' in set_switch_list:
            setAttr_switch(self.legs_L_switch, 'ik', True)

        if 'legs_r_ik' in set_switch_list:
            setAttr_switch(self.legs_R_switch, 'ik', True)


class JsonFile(object):
    @classmethod
    def read(cls, file_path):
        if not file_path:
            return {}
        if not os.path.isfile(file_path):
            return {}
        with codecs.open(file_path, 'r', 'utf-8') as f:
            try:
                data = json.load(f, object_pairs_hook=OrderedDict)
            except ValueError:
                data = {}
        return data

    @classmethod
    def write(cls, file_path, data):
        if not file_path:
            return
        dirname, basename = os.path.split(file_path)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        with codecs.open(file_path, 'w', 'utf-8') as f:
            json.dump(data, f, indent=4)
            f.flush()
            os.fsync(f.fileno())

# if __name__ == "__main__":
#     fk2ik=FK2IKMatch()
#     fk2ik.main()
