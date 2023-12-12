# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel

from collections import OrderedDict

class FK2IKMatch(object):
    u"""IKFKMatch"""
    def __init__(self, namespace='ply00_m_000_000', mirrors=['_L_', '_R_'], setkey_attrs=[u'tx', u'ty', u'tz', u'rx', u'ry', u'rz']):
        u"""Initialize
        param:
        namespace='ply00_m_000_000'
        mirrors=['_L_', '_R_']
        setkey_attrs=[u'tx', u'ty', u'tz', u'rx', u'ry', u'rz']
        """

        self.namespace=namespace
        self.mirrors=mirrors
        self.setkey_attrs=setkey_attrs

        self.arms_pos_ctrls=OrderedDict()
        self.arms_rot_ctrls=OrderedDict()
        self.arms_pv_ctrls=OrderedDict()

        self.legs_pos_ctrls=OrderedDict()
        self.legs_rot_ctrls=OrderedDict()
        self.legs_pv_ctrls=OrderedDict()

    def main(self, current_scene=None, save_path=None):
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
        fbxspl = current_scene.split('/')
        fname = fbxspl[-1].split('.')[0]

        cmds.file(rn='{0}/{1}.ma'.format(save_path, fname))
        cmds.file(f=1, save=1)

        print('Saved:{0}/{1}.ma'.format(save_path, fname))

        return


    def add_pos_obj(self, type=None, fkctrl=None, ikctrl=None):
        u"""ポジションのマッチするオブジェクトを登録"""
        if type == 'arms':
            self.arms_pos_ctrls.setdefault('{0}'.format(fkctrl), '{0}'.format(ikctrl))
        elif type == 'legs':
            self.legs_pos_ctrls.setdefault('{0}'.format(fkctrl), '{0}'.format(ikctrl))

    def add_rot_obj(self, type=None, fkctrl=None, ikctrl=None):
        u"""回転のマッチするオブジェクトを登録"""
        if type == 'arms':
            self.arms_rot_ctrls.setdefault('{0}'.format(fkctrl), '{0}'.format(ikctrl))
        elif type == 'legs':
            self.legs_rot_ctrls.setdefault('{0}'.format(fkctrl), '{0}'.format(ikctrl))

    def add_pv_obj(self, type=None, fkctrl_start=None, fkctrl_mid=None, fkctrl_end=None, ikctrl=None):
        u"""PoleVextorのマッチするオブジェクトを登録"""
        if type == 'arms':
            self.arms_pv_ctrls.setdefault('ikpv', '{0}'.format(ikctrl))
            self.arms_pv_ctrls.setdefault('fkstart', '{0}'.format(fkctrl_start))
            self.arms_pv_ctrls.setdefault('fkmid', '{0}'.format(fkctrl_mid))
            self.arms_pv_ctrls.setdefault('fkend', '{0}'.format(fkctrl_end))
        elif type == 'legs':
            self.legs_pv_ctrls.setdefault('ikpv', '{0}'.format(ikctrl))
            self.legs_pv_ctrls.setdefault('fkstart', '{0}'.format(fkctrl_start))
            self.legs_pv_ctrls.setdefault('fkmid', '{0}'.format(fkctrl_mid))
            self.legs_pv_ctrls.setdefault('fkend', '{0}'.format(fkctrl_end))

    def matchsetkeys(self, type=None, setkey_attrs=None):
        u"""PoleVextorのマッチするオブジェクトを登録"""
        if type == 'arms':
            pos_ctrls = self.arms_pos_ctrls
            rot_ctrls = self.arms_rot_ctrls
            pv_ctrl = self.arms_pv_ctrls
        elif type == 'legs':
            pos_ctrls = self.legs_pos_ctrls
            rot_ctrls = self.legs_rot_ctrls
            pv_ctrl = self.legs_pv_ctrls

        # pos
        for fk_pos, ik_pos in pos_ctrls.items():
            cmds.matchTransform('{0}'.format(ik_pos), '{0}'.format(fk_pos))

        cmds.setKeyframe(pos_ctrls.values(), at=setkey_attrs)

        # pv
        loc = cmds.spaceLocator()
        cmds.pointConstraint('{0}'.format(pv_ctrl['fkstart']), loc[0], w=1)
        cmds.pointConstraint('{0}'.format(pv_ctrl['fkend']), loc[0], w=1)

        cmds.aimConstraint('{0}'.format(pv_ctrl['fkmid']), loc[0], weight=1, upVector=(0, 1, 0), worldUpType="vector", offset=(0, 0, 0), aimVector=(1, 0, 0), worldUpVector=(0, 1, 0))

        dup_loc=cmds.duplicate(loc[0], po=1)
        cmds.parent(dup_loc[0], loc[0])
        cmds.matchTransform(dup_loc[0], pv_ctrl['fkmid'], pos=1)
        cmds.xform(dup_loc[0], ro=[0,0,0], a=1, os=1)
        cmds.move(30, 0, 0, dup_loc[0], os=1, r=1, wd=1)
        cmds.matchTransform('{0}'.format(pv_ctrl['ikpv']), dup_loc[0])

        cmds.setKeyframe(pv_ctrl.values(), at=setkey_attrs)

        cmds.delete(loc)

        # rot
        for fk_rot, ik_rot in rot_ctrls.items():
            cmds.matchTransform('{0}'.format(ik_rot), '{0}'.format(fk_rot))

        cmds.setKeyframe(rot_ctrls.values(), at=setkey_attrs)

    def match_func(self):
        for mir in self.mirrors:
            # --
            # Arms
            # --
            # pos
            self.add_pos_obj(type='arms', fkctrl='{0}:hand{1}fk_ctrl'.format(self.namespace, mir), ikctrl='{0}:hand{1}ik_ctrl'.format(self.namespace, mir))

            # rot
            self.add_rot_obj(type='arms', fkctrl='{0}:clavicle{1}fk_ctrl'.format(self.namespace, mir), ikctrl='{0}:clavicle{1}ikAutoRot_ctrl_ikAutoShoulder_ctrl'.format(self.namespace, mir))
            self.add_rot_obj(type='arms', fkctrl='{0}:hand{1}fk_ctrl'.format(self.namespace, mir), ikctrl='{0}:hand{1}ikRot_ctrl_ikRot_ctrl'.format(self.namespace, mir))

            # pv
            self.add_pv_obj(type='arms',
                             fkctrl_start='{0}:upperarm{1}fk_ctrl'.format(self.namespace, mir),
                             fkctrl_mid='{0}:lowerarm{1}fk_ctrl'.format(self.namespace, mir),
                             fkctrl_end='{0}:hand{1}fk_ctrl'.format(self.namespace, mir),
                             ikctrl='{0}:upperarm{1}ik_pv_ctrl'.format(self.namespace, mir))

            # functions
            self.matchsetkeys(type='arms', setkey_attrs=self.setkey_attrs)

        for mir in self.mirrors:
            # --
            # Legs
            # --
            # pos
            self.add_pos_obj(type='legs', fkctrl='{0}:foot{1}fk_ctrl'.format(self.namespace, mir), ikctrl='{0}:foot{1}ik_ctrl'.format(self.namespace, mir))

            # rot
            self.add_rot_obj(type='legs', fkctrl='{0}:ikfk_match_loc_foot{1}proxy_jnt'.format(self.namespace, mir), ikctrl='{0}:foot{1}ik_ctrl'.format(self.namespace, mir))
            self.add_rot_obj(type='legs', fkctrl='{0}:ball{1}fk_ctrl'.format(self.namespace, mir), ikctrl='{0}:foot{1}ik_ctrl_revFoot_holdBall_ctrl'.format(self.namespace, mir))

            # pv
            self.add_pv_obj(type='legs',
                             fkctrl_start='{0}:thigh{1}fk_ctrl'.format(self.namespace, mir),
                             fkctrl_mid='{0}:calf{1}fk_ctrl'.format(self.namespace, mir),
                             fkctrl_end='{0}:foot{1}fk_ctrl'.format(self.namespace, mir),
                             ikctrl='{0}:calf{1}ik_pv_ctrl'.format(self.namespace, mir))

            # functions
            self.matchsetkeys(type='legs', setkey_attrs=self.setkey_attrs)


    def matchbake(self):
        u"""フレーム毎にベイク"""
        #check and save current autokey state
        cur_time=cmds.currentTime(q=1)
        if cmds.autoKeyframe(q=True, st=True):
            autoKeyState = 1
        else:
            autoKeyState = 0

        cmds.autoKeyframe(st=0)

        playmin = cmds.playbackOptions(q=1, min=1)
        playmax = cmds.playbackOptions(q=1, max=1)

        start = playmin
        end = playmax-1

        for i in range (int(start-1), int(end+2)):
            cmds.currentTime(i, e=True)
            self.match_func()
        cmds.currentTime(cur_time)
        cmds.autoKeyframe(state=autoKeyState)

if __name__ == "__main__":
    fk2ik=FK2IKMatch()
    fk2ik.main()
