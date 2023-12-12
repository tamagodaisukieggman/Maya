# -*- coding: utf-8 -*-
# ----------------------------------
# Project : Tsubasa
# Name    : tailCtrlCreatorMayaVer
# Author  : toi
# Version : 0.1.0
# Updata  : 2022/6/13
# ----------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import maya.cmds as cmds
#import maya.mel as mm
import pymel.core as pm
import os
#import sys
#import stat
#from collections import OrderedDict
#from rigSupportTools import ui as rstui
#from dccUserMayaSharePythonLib import ui
from dccUserMayaSharePythonLib import common as cm
#reload(cm)


class TailCtrlCreatorMayaVer(object):
    TAIL_RIG_GP = 'tail_rig_GP'
    window_name = 'TailCtrlCreatorMayaVer'
    conses = ''
    set_limmit_axs = ''

    def addAttr_Tailctrl_AssetCtrl(self):
        if pm.objExists('Asset_ctrl'):
            if not pm.objExists('Asset_ctrl.tail_ctrl'):
                pm.addAttr('Asset_ctrl', ln='tail_ctrl', at='enum', enumName='FK=1: IK=2')
                return 0
            else:
                return '既に存在する'
        else:
            return 'Asset_ctrlが無い'

    def makeGroup(self, name, parent_=None, set_zero=False):
        if pm.objExists(name):
            gp = pm.PyNode(name)
        else:
            gp = pm.createNode('transform', n=name, ss=True)

        if parent_ is not None:
            pm.parent(gp, parent_)

        if set_zero:
            gp.setTranslation([0, 0, 0])
            gp.setRotation([0, 0, 0])

        return gp

    def locator(slef, name, size):
        loc = pm.spaceLocator(n=name)
        size /= 2
        pm.setAttr(loc.getShape() + '.localScaleX', size)
        pm.setAttr(loc.getShape() + '.localScaleY', size)
        pm.setAttr(loc.getShape() + '.localScaleZ', size)
        return loc

    def setSamePosParent(self, parent, node):
        node.setTranslation(parent.getTranslation('world'), 'world')
        node.setRotation(parent.getRotation('world'), 'world')

    def _addExtraAttr2RigGp(self, at_name, val):
        val = val[: -1]
        cm.addAt(self.TAIL_RIG_GP, at_name, val)

    def _setRotZero(self, joint):
        pm.setAttr(joint + '.jointOrientX', 0)
        pm.setAttr(joint + '.jointOrientY', 0)
        pm.setAttr(joint + '.jointOrientZ', 0)
        pm.setAttr(joint + '.rotateX', 0)
        pm.setAttr(joint + '.rotateY', 0)
        pm.setAttr(joint + '.rotateZ', 0)

    def mekeSpik(self):
        dup_joints = pm.duplicate(self.ori_joints)
        pm.parent(dup_joints[0], 'tail_spik_ax')
        self._setRotZero(dup_joints[0])

        distance = cm.getDistance(self.ori_joints[0], self.ori_joints[1])

        #--------------------------------------------------------
        #スプラインIK用のオリジナルジョイント
        #--------------------------------------------------------
        i = 0
        spjt_joints = ''
        for j, d in zip(self.ori_joints, dup_joints):
            new_name = j.name() + '_spjt'
            d.rename(new_name)
            spjt_joints += d.name() + ','
            i += 1
        self._addExtraAttr2RigGp('spjt_joints', spjt_joints)

        #--------------------------------------------------------
        #スプラインIKジョイントから位置を拾い、向きはupベクターからもらう最終結果のジョイント
        #--------------------------------------------------------
        dup_joints = pm.duplicate(self.ori_joints)
        pm.parent(dup_joints[0], 'tail_rig_GP_cnst')
        self._setRotZero(dup_joints[0])

        i = 0
        fkjt_joints = ''
        for j, d in zip(self.ori_joints, dup_joints):
            new_name = j.name() + '_fkjt'
            d.rename(new_name)
            fkjt_joints += d.name() + ','
            i += 1
        self._addExtraAttr2RigGp('fkjt_joints', fkjt_joints)

        #--------------------------------------------------------
        #FK用のctrl
        #--------------------------------------------------------
        _fk_ctrl_ax = self.makeGroup('_fk_ctrl_ax', self.parent)
        self.set_limmit_axs += _fk_ctrl_ax  + ','
        last_l = None
        i = 0
        fk_ctrls = ''
        for j in self.ori_joints:
            new_name = j.name() + '_fk_ctrl'
            l = pm.spaceLocator(n=new_name)
            fk_ctrls += l.name() + ','

            if last_l is None:
                pm.parent(l, _fk_ctrl_ax)
                _fk_ctrl_ax.setTranslation(j.getTranslation('world'), 'world')
                _fk_ctrl_ax.setRotation(j.getRotation('world'), 'world')
                l.setTranslation([0, 0, 0])
                l.setRotation([0, 0, 0])
            else:
                pm.parent(l, last_l)
                pm.setAttr(l + '.t', *pm.getAttr(j + '.t'))
                pm.setAttr(l + '.r', *pm.getAttr(j + '.r'))
            last_l = l
            i += 1
        self._addExtraAttr2RigGp('fk_ctrls', fk_ctrls)

        #--------------------------------------------------------
        #IK_ctrls
        #--------------------------------------------------------
        spik_ctrl_GP = self.makeGroup('spik_ctrl_GP', self.parent)
        self.setSamePosParent(self.parent, spik_ctrl_GP)

        ik_pos_num = 0
        last_upv_ctrl = None
        make_ik_ctrl_pos_attr_string = ''
        pos_ctrls = ''
        upv_ctrls = ''
        tail_upv_ctrls = ''
        tail_ik_poses = ''
        fk_ctrls = self._convertToList(fk_ctrls)
        upv_ax_2_list = []
        for i, j in enumerate(self.ori_joints):
            num = str(i)

            #ik_pos_ctrlを作成するポイント
            if self.make_ik_ctrl_pos_dict[j.name()]:

                ax = self.makeGroup('tail' + num + '_pos_ctrl_ax', spik_ctrl_GP)
                self.set_limmit_axs += ax  + ','
                ax.setTranslation(j.getTranslation('world'), 'world')
                ax.setRotation(j.getRotation('world'), 'world')

                #IKポイントctrl（pos_ctrl）
                pos_ctrl = self.locator(name='a', size=distance)
                pos_ctrl.rename('tail' + str(ik_pos_num) + '_pos_ctrl')
                pm.parent(pos_ctrl, ax)
                pos_ctrl.setTranslation([0, 0, 0])
                pos_ctrl.setRotation([0, 0, 0])
                pos_ctrls += pos_ctrl.name() + ','

                #アップベクターax（upv_ctrl_ax）
                upv_ax = self.makeGroup('tail' + num + '_upv_ctrl_ax', pos_ctrl)
                self.set_limmit_axs += upv_ax  + ','
                upv_ax.setTranslation([0, distance, 0])
                upv_ax.setRotation([0, 0, 0])

                #IKポイントアップベクター
                upv_ctrl = self.locator(name='upv_' + str(ik_pos_num) + '_ctrl', size=distance)
                pm.parent(upv_ctrl, upv_ax)
                upv_ctrl.setTranslation([0, 0, 0])
                upv_ctrl.setRotation([0, 0, 0])
                upv_ctrls += upv_ctrl.name() + ','

                if last_upv_ctrl is not None:
                    for _num, upv_ax_2 in upv_ax_2_list:
                        p_cons = pm.parentConstraint(
                            last_upv_ctrl, upv_ctrl, upv_ax_2, mo=True,
                            n='tail{0}_upv_parentConstraint'.format(_num))

                        v = cm.getDistanceFromValue(cm.getWorldTrans(last_upv_ctrl), cm.getWorldTrans(upv_ax_2))
                        v2 = cm.getDistanceFromValue(cm.getWorldTrans(upv_ctrl), cm.getWorldTrans(upv_ax_2))
                        pm.setAttr('{0}.{1}W0'.format(p_cons.name(), last_upv_ctrl.name()), v2)
                        pm.setAttr('{0}.{1}W1'.format(p_cons.name(), upv_ctrl.name()), v)

                        self.conses += p_cons.name() + ','

                upv_ax_2_list = []
                last_upv_ctrl = upv_ctrl

                #末端アップベクター（upv_ctrl）
                tail_upv_ctrl = self.locator(name='tail' + num + '_upv_ctrl', size=distance)
                pm.parent(tail_upv_ctrl, upv_ctrl)
                tail_upv_ctrl.setTranslation([0, 0, 0])
                tail_upv_ctrl.setRotation([0, 0, 0])
                tail_upv_ctrls += tail_upv_ctrl.name() + ','

                #FK → IK 用のポイント（ik_pos）
                tail_ik_pos = self.locator(name='tail{0}_ik_pos'.format(ik_pos_num), size=distance / 2)
                pm.parent(tail_ik_pos, 'tail_ik_pos_GP')
                tail_ik_pos.setTranslation(j.getTranslation('world'), 'world')
                tail_ik_poses += tail_ik_pos.name() + ','
                #parentConst
                p_cons = pm.parentConstraint(
                    fk_ctrls[i], tail_ik_pos, n='ik_pos{0}_parentConstraint'.format(ik_pos_num))
                self.conses += p_cons.name() + ','
                ik_pos_num += 1
                make_ik_ctrl_pos_attr_string += '1,'

            #その他のポイント
            else:
                #アップベクターax
                upv_ax_2 = self.makeGroup('tail' + num + '_upv_ctrl_ax', spik_ctrl_GP)
                t = j.getTranslation('world')
                set_trans = [t[0], t[1] + distance, t[2]]
                upv_ax_2.setTranslation(set_trans, 'world')
                upv_ax_2.setRotation(j.getRotation('world'), 'world')
                upv_ax_2_list.append([num, upv_ax_2])

                #末端アップベクター
                tail_upv_ctrl_2 = self.locator(name='tail' + num + '_upv_ctrl', size=distance)
                pm.parent(tail_upv_ctrl_2, upv_ax_2)
                tail_upv_ctrl_2.setTranslation([0, 0, 0])
                tail_upv_ctrl_2.setRotation([0, 0, 0])
                tail_upv_ctrls += tail_upv_ctrl_2.name() + ','

                make_ik_ctrl_pos_attr_string += '0,'

        #--------------------------------------------------------
        #builer側で簡単にノードを取得できるようにアトリビュートに追加しておく
        #--------------------------------------------------------
        self._addExtraAttr2RigGp('pos_ctrls', pos_ctrls)
        self._addExtraAttr2RigGp('upv_ctrls', upv_ctrls)
        self._addExtraAttr2RigGp('tail_upv_ctrls', tail_upv_ctrls)
        self._addExtraAttr2RigGp('tail_ik_poses', tail_ik_poses)
        self._addExtraAttr2RigGp('make_ik_ctrl_pos', make_ik_ctrl_pos_attr_string)
        self._addExtraAttr2RigGp('set_limmit_axs', self.set_limmit_axs)
        cm.addAt(
            self.TAIL_RIG_GP,
            'aim_vec', '{0},{1},{2}'.format(
                int(self.aim_vec[0]), int(self.aim_vec[1]), int(self.aim_vec[2])
            )
        )
        cm.addAt(
            self.TAIL_RIG_GP,
            'upv_vec', '{0},{1},{2}'.format(
                int(self.upv_vec[0]), int(self.upv_vec[1]), int(self.upv_vec[2])
            )
        )
        cm.addAt(self.TAIL_RIG_GP, 'ctrl_size', distance)

        #self._setAimConst(fkjt_joints, tail_upv_ctrls) #おかしくなるのでビルダー側で対応
        self._addExtraAttr2RigGp('constraints', self.conses)

        return 0

    def _setAimConst(self, fkjt_joints, tail_upv_ctrls):
        """
        splineIKジョイントの位置からローテーションを拾う為のエイムコンスト
        mayaだとサイクルになるので、器だけ作ってブロッキングしておく
        ※不使用
        """
        fkjt_joints = self._convertToList(fkjt_joints)
        tail_upv_ctrls = self._convertToList(tail_upv_ctrls)
        for i in range(len(fkjt_joints)):
            if i != len(fkjt_joints) - 1:
                aim = pm.aimConstraint(
                    fkjt_joints[i + 1], fkjt_joints[i],
                    n='tail{0}_aimConstraint'.format(i),
                    aim=self.aim_vec, upVector=self.upv_vec,
                    worldUpType='object', worldUpObject=tail_upv_ctrls[i + 1],
                    mo=True)
                self.conses += aim.name() + ','
                pm.setAttr(aim + '.nodeState', 2)

    def _convertToList(self, stringList):
        return [x for x in stringList.split(',') if x]

    #----------------------------------------------------------------------------------------------
    #ui
    #----------------------------------------------------------------------------------------------
    def delOverwrapWindow(self):
        if pm.window(self.window_name, ex=True):
            pm.deleteUI(self.window_name)

    def initUi(self):
        self.delOverwrapWindow()
        win = pm.window(self.window_name, t=self.window_name, mb=True)
        pm.menu(l='Help')
        pm.menuItem(l='Tool help', c=pm.Callback(os.startfile, 'https://wisdom.cygames.jp/x/uDn3DQ'))
        pm.columnLayout(adj=True, co=['both', 3])

        with pm.frameLayout(l='１． tail リグの親となる　「_wld」　ノードを選択', mh=4, mw=4, bgc=[0.1, 0.3, 1]):
            with pm.rowLayout(adj=True, nc=2):
                self.tx_parent = pm.textFieldGrp(l='tailの親ノード_wld ', placeholderText='_***_wld')
                pm.button(l='選択から取得', c=pm.Callback(self._setParent))

        with pm.frameLayout(l='２. アップベクターの方向を設定', mh=4, mw=4, bgc=[0.1, 0.3, 1]):
            with pm.columnLayout(adj=True):
                self.ffg_aim = pm.floatFieldGrp(l='aim vector ', nf=3, v1=0, v2=0, v3=1)
                self.ffg_upv = pm.floatFieldGrp(l='up vector ', nf=3, v1=0, v2=1, v3=-0)

        with pm.frameLayout(l='３. tail を適用するジョイントを選択', mh=4, mw=4, bgc=[0.1, 0.3, 1]):
            pm.button(l='ジョイントを選択して実行すると　4番にジョイントが表示されます', c=pm.Callback(self._setJoints))

        with pm.frameLayout(l='４． IK_ctrl（制御ポイント）を置く位置のジョイントを選択', mh=4, mw=4, bgc=[0.1, 0.3, 1]):
            self.cl_joint_second = pm.columnLayout(adj=True)
            self.cl_joint_main = pm.columnLayout(adj=True)
            pm.setParent('..')
            pm.setParent('..')

        pm.separator(h=10)
        pm.button(l='５．tail作成 実行', c=pm.Callback(self.start_main), h=50)

        win.show()

    def _setParent(self):
        self.sels = pm.ls(sl=True)
        if not self.sels:
            pm.warning('親を選択してください')
            return

        self.tx_parent.setText(self.sels[0].name())

    def _setJoints(self):
        self.sels = pm.ls(sl=True)
        if not self.sels:
            pm.warning('tailジョイントを選択してください')
            return

        pm.deleteUI(self.cl_joint_main)
        pm.setParent(self.cl_joint_second)

        self.cl_joint_main = pm.columnLayout(adj=True)
        self.cb_list = []
        for i, sel in enumerate(self.sels):
            cb = cmds.checkBox(l=sel.name())
            if i == 0 or i == len(self.sels) - 1:
                cmds.checkBox(cb, e=True, v=True, en=False)
            self.cb_list.append(cb)

    def start_main(self):
        self.parent = self.tx_parent.getText()
        if not self.parent:
            pm.warning('親の入力がありません')
            return

        self.parent = pm.PyNode(self.parent)

        self.aim_vec = pm.floatFieldGrp(self.ffg_aim, q=True, v=True)
        self.upv_vec =  pm.floatFieldGrp(self.ffg_upv, q=True, v=True)
        print(self.aim_vec, self.upv_vec)

        self.ori_joints = []
        self.make_ik_ctrl_pos_dict = {}
        for cb in self.cb_list:
            self.make_ik_ctrl_pos_dict[cmds.checkBox(cb, q=True, l=True)] = cmds.checkBox(cb, q=True, v=True)
            self.ori_joints.append(pm.PyNode(cmds.checkBox(cb, q=True, l=True)))
        self.main()

    #------------------------------------------------------------------------------------------------
    def main(self):
        self.addAttr_Tailctrl_AssetCtrl()

        if pm.objExists('rig_GP'):
            gp = self.makeGroup(self.TAIL_RIG_GP, 'rig_GP', True)
        else:
            gp = self.makeGroup(self.TAIL_RIG_GP, None, True)
        self.setSamePosParent(self.parent, gp)
        set_srting = ''
        for j in self.ori_joints:
            set_srting += j.name() + ','
        self._addExtraAttr2RigGp('ori_joints', set_srting)

        gp = self.makeGroup('tail_rig_GP_cnst', self.TAIL_RIG_GP)
        self.setSamePosParent(self.ori_joints[0], gp)

        gp = self.makeGroup('tail_spik_ax', self.TAIL_RIG_GP, True)
        self.setSamePosParent(self.ori_joints[0], gp)

        gp = self.makeGroup('spik_GP', self.TAIL_RIG_GP, True)
        self.setSamePosParent(self.ori_joints[0], gp)

        gp = self.makeGroup('tail_ik_pos_GP', self.TAIL_RIG_GP, True)
        self.setSamePosParent(self.ori_joints[0], gp)

        self.mekeSpik()

        pm.confirmDialog(
            icn='information',
            b='確認',
            t='message',
            p=self.window_name,
            m=('処理が無事完了しました！\n\n'
            'fbx出力後\n'
            'TailCtrlCreaterMBVerで処理を続けてください')
        )


def main():
    TailCtrlCreatorMayaVer().initUi()
