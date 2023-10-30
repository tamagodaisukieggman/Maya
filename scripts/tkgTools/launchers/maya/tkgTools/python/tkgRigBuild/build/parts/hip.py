# -*- coding: utf-8 -*-

import maya.cmds as cmds
from imp import reload

import tkgRigBuild.build.rigModule as tkgModule
import tkgRigBuild.build.chain as tkgChain
import tkgRigBuild.libs.control.ctrl as tkgCtrl
import tkgRigBuild.libs.attribute as tkgAttr
reload(tkgModule)
reload(tkgChain)
reload(tkgCtrl)
reload(tkgAttr)

class Hip(tkgModule.RigModule):
    def __init__(self,
                 side=None,
                 part=None,
                 guide_list=None,
                 ctrl_scale=None,
                 offset_hip=None,
                 hip_01_name='hip_01',
                 hip_02_name='hip_02',
                 ctrl_shape="hip",
                 ctrl_color=[1, 1, 0.24],
                 model_path=None,
                 guide_path=None):
        super(Hip, self).__init__(side=side, part=part,
                                  guide_list=guide_list,
                                  ctrl_scale=ctrl_scale,
                                  model_path=model_path,
                                  guide_path=guide_path)

        self.offset_hip = offset_hip
        self.hip_01_name = hip_01_name
        self.hip_02_name = hip_02_name
        self.ctrl_shape = ctrl_shape
        self.ctrl_color = ctrl_color

        self.part_ctrls = []

        self.create_module()

    def create_module(self):
        super(Hip, self).create_module()

        self.control_rig()
        self.output_rig()
        self.skeleton()
        # self.add_plugs()

    def control_rig(self):
        # create controls
        self.hip_01 = tkgCtrl.Control(parent=self.control_grp,
                                     shape=self.ctrl_shape,
                                     prefix=self.side,
                                     suffix='CTRL',
                                     name=self.hip_01_name,
                                     axis='y',
                                     group_type='main',
                                     rig_type=self.hip_01_name,
                                     position=self.guide_list[0],
                                     rotation=(0, 0, 0),
                                     ctrl_scale=self.ctrl_scale * 0.4,
                                     ctrl_color=self.ctrl_color)
        self.part_ctrls.append(self.hip_01.ctrl)

        self.hip_02 = tkgCtrl.Control(parent=self.hip_01.ctrl,
                                     shape=self.ctrl_shape,
                                     prefix=self.side,
                                     suffix='CTRL',
                                     name=self.hip_02_name,
                                     axis='y',
                                     group_type='main',
                                     rig_type=self.hip_02_name,
                                     position=self.guide_list[0],
                                     rotation=(0, 0, 0),
                                     ctrl_scale=self.ctrl_scale * 0.35,
                                     ctrl_color=[v*0.35 for v in self.ctrl_color])
        self.part_ctrls.append(self.hip_02.ctrl)

    def output_rig(self):
        hip_jnt_grp = cmds.group(parent=self.module_grp, empty=True,
                                 name=self.base_name + '_JNT_GRP')
        cmds.matchTransform(hip_jnt_grp, self.hip_02.ctrl)
        self.hip_jnt = cmds.joint(hip_jnt_grp,
                                  name=self.hip_02.ctrl.replace('CTRL', 'JNT'))

        cmds.parentConstraint(self.hip_02.ctrl, self.hip_jnt, mo=True)

        self.tag_buid_ctrls(self.part+'Ctrls', self.part_ctrls, self.part_grp)

    def skeleton(self):
        hip_chain = tkgChain.Chain(transform_list=[self.hip_jnt],
                                  prefix=self.side,
                                  suffix='JNT',
                                  name=self.part)
        hip_chain.create_from_transforms(parent=self.skel,
                                         pad=False)
        self.bind_joints = hip_chain.joints

        # offset hip joint for better weight mirroring
        if self.offset_hip:
            cmds.setAttr(
                hip_chain.constraints[0] + '.target[0].targetOffsetTranslateY',
                self.offset_hip)

        self.tag_bind_joints(self.bind_joints, self.part_grp)

    def add_plugs(self):
        part_ctrls_dict = self.ctrl_info_from_module()
        # *ジョイント階層の指定
        # plugを追加するmodule
        part_grp = 'Cn_hip'

        # 親にするジョイントの取得
        root_jnt = part_ctrls_dict['Cn_root']['partJoints']

        # 子にするジョイントの取得
        jnts = part_ctrls_dict[part_grp]['partJoints']

        # 親子関係の情報を設定
        tkgAttr.Attribute(node=part_grp, type='plug',
                         value=[root_jnt], name='skeletonPlugs',
                         children_name=[jnts[0]])

        # *コントローラの空間の指定
        # spaceを追加するコントローラを取得
        ctrl = [n for n in part_ctrls_dict[part_grp]['hipCtrls'].keys()][0]

        # spaceの元になるコントローラの取得
        target_list = [n for n in part_ctrls_dict['Cn_root']['rootCtrls'].keys()]

        # spaceの名前を取得する
        name_list = [n.replace('Cn_', '').replace('_CTRL', '') for n in target_list]

        # spaceのデフォルトにするインデクス
        default_idx = 2

        # デフォルトのインデクスとdefault_valueを最後に追加
        target_list.append(str(default_idx))
        name_list.append('default_value')

        # parentでのspaceを設定する
        tkgAttr.Attribute(node=part_grp, type='plug',
                         value=target_list,
                         name=ctrl + '_parent',
                         children_name=name_list)
