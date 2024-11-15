# -*- coding: utf-8 -*-
from collections import OrderedDict
from imp import reload
import re

import maya.cmds as cmds
import maya.mel as mel

import buildRig.connecter as brConnecter
import buildRig.common as brCommon
import buildRig.node as brNode
import buildRig.grps as brGrp
import buildRig.joint as brJnt
import buildRig.libs.control.draw as brDraw
import buildRig.transform as brTrs
import buildRig.file as brFile
reload(brConnecter)
reload(brCommon)
reload(brNode)
reload(brGrp)
reload(brJnt)
reload(brDraw)
reload(brTrs)
reload(brFile)

class Root(brGrp.RigModule):
    def __init__(self,
                 module=None,
                 side=None,
                 setup_env_path=None,
                 rig_joints_parent=None,
                 rig_ctrls_parent=None,
                 namespace=None,
                 joints=None,
                 shapes=['gnomon', 'pacman', 'arrow_one_way_z'],
                 axis=[0,0,0],
                 scale=5,
                 scale_step=0,
                 prefix='ROOT_'):
        """
        Params:
        module = string<モジュール名を指定する>
        side = string<中央、右、左がわかる識別子を指定する>
        rig_joints_parent = string<ジョイントをペアレントする親を指定する>
        rig_ctrls_parent = string<コントローラをペアレントする親を指定する>
        joints = list[string]<ベースになるジョイントのリストを指定する>
        shape = string<コントローラのタイプを指定する>
        axis = list[float, float, float]
        scale = float<コントローラのサイズを指定する>
from imp import reload
import re
import traceback

import maya.cmds as cmds
import maya.mel as mel

import buildRig.fk as brFk
reload(brFk)

try:
    sel = cmds.ls(os=True)
    fk = brFk.Fk(module='arm',
                 side='left',
                 rig_joints_parent=None,
                 rig_ctrls_parent=None,
                 namespace='chr',
                 joints=sel,
                 shapes=['gnomon', 'pacman', 'arrow_one_way_z'],
                 axis=[0,0,0],
                 scale=1000,
                 scale_step=0,
                 prefix='root_')
except:
    print(traceback.format_exc())

fk.base_connection()
        """
        super(Root, self).__init__(module=module,
                                 side=side,
                                 setup_env_path=setup_env_path)

        self.settings = brFile.Settings(setup_env_path=self.setup_env_path)
        self.root_settings = self.settings.setting_dict['ROOT']

        self.rig_joints_parent = rig_joints_parent
        self.rig_ctrls_parent = rig_ctrls_parent
        self.namespace = namespace
        self.joints = joints
        self.shapes = shapes
        self.axis = axis
        self.scale = scale
        self.scale_step = scale_step
        self.prefix = prefix

        self.jnt_object = None
        self.trs_object = None
        self.trs_objects = []
        self.top_root_joint_nodes = []
        self.top_root_ctrl_nodes = []

        # Controller
        self.draw = brDraw.Draw()

        # Exist Roots
        self.exist_roots = []

        # モジュールのノードを追加
        self.trs_module_root = brTrs.create_transforms(nodes=[self.module_grp, self.module_grp + '_ROOT'], offsets=False)
        self.trs_ctrl_root = brTrs.create_transforms(nodes=[self.ctrl_grp, self.ctrl_grp + '_ROOT'], offsets=False)

        self.create_root_module()

    def create_root_module(self):
        self.create_joints()
        self.create_ctrls()
        self.create_rig_module()
        self.connection()

    def create_joints(self):
        parent = None
        for n in self.joints:
            if self.namespace:
                n = self.namespace + ':' + n
            if not cmds.objExists(n):
                cmds.createNode('joint', n=n, ss=True)
                cmds.parent(n, parent)
            self.exist_roots.append(n)
            parent = n

        self.jnt_object = brJnt.create_joints(namespace=self.namespace, nodes=self.joints, prefix=self.prefix, suffix=None, replace=['_copy', ''])
        cmds.parent(self.jnt_object.nodes[-1], self.jnt_object.nodes[-2])
        for node in self.jnt_object.node_list:
            node.freezeTransform()
            node.set_preferredAngle()
            node.get_values()
        self.top_root_joint_nodes.append(self.jnt_object.node_list[0].full_path.split('|')[1])

    def create_ctrls(self):
        ctrl_names = self.root_settings['ctrl']
        ctrl_colors = self.root_settings['colors']
        color_dict = {}
        for side, values in ctrl_colors.items():
            filtered_items = brCommon.filter_items(source_items=self.jnt_object.nodes,
                                                    search_txt_list=values['filter'],
                                                    remover=False)
            for jnt in filtered_items:
                color_dict[jnt] = values['value']

        print('color_dict', color_dict)

        scale_steps = 0
        for i, jnt in enumerate(self.jnt_object.node_list):
            shape = self.shapes[i]
            self.draw.create_curve(name=jnt.node + '_CURVE', shape=shape, axis=self.axis, scale=self.scale + scale_steps)
            scale_steps += self.scale_step
            if jnt.node in color_dict.keys():
                brCommon.set_rgb_color(ctrl=self.draw.curve,
                                    color=color_dict[jnt.node])
                brCommon.set_obj_color(obj=self.draw.curve,
                                    color=color_dict[jnt.node],
                                    outliner=True)

            cmds.matchTransform(self.draw.curve, jnt.node)

            nodes = self.root_settings['offsets'] + [self.draw.curve]
            settings = {
                'nodes':nodes,
                'offsets':True,
                'prefix':ctrl_names[0],
                'suffix':ctrl_names[1],
                'replace':ctrl_names[2]
            }
            self.trs_object = brTrs.create_transforms(**settings)
            self.trs_objects.append(self.trs_object)
            if jnt.parent:
                parent_ctrl = brCommon.rename(obj=jnt.parent.split('|')[-1] + '_CURVE',
                                              prefix=ctrl_names[0],
                                              suffix=ctrl_names[1],
                                              replace=ctrl_names[2])
                if cmds.objExists(parent_ctrl):
                    cmds.parent(self.trs_object.nodes[0], parent_ctrl)

        # cmds.parent(self.trs_objects[-1].nodes[0], self.trs_objects[-2].nodes[-1])

        for trs_object in self.trs_objects:
            for node in trs_object.node_list:
                node.get_values()
            self.top_root_ctrl_nodes.append(trs_object.node_list[0].full_path.split('|')[1])

        self.top_root_ctrl_nodes = list(set(self.top_root_ctrl_nodes))

    def create_rig_module(self):
        # リグ用のジョイントをペアレント化させる
        if not self.rig_joints_parent:
            self.rig_joints_parent = self.trs_module_root.nodes[-1]

        for jnt in self.top_root_joint_nodes:
            cmds.parent(jnt, self.rig_joints_parent)

        # コントローラをペアレント化させる
        if not self.rig_ctrls_parent:
            self.rig_ctrls_parent = self.trs_ctrl_root.nodes[-1]

        for ctrl in self.top_root_ctrl_nodes:
            cmds.parent(ctrl, self.rig_ctrls_parent)

    def connect_children(self):
        first_trs_object = self.trs_objects[0]
        first_ctrl = first_trs_object.nodes[-1]

        cmds.addAttr(first_ctrl, ln='rotChildren', at='double', dv=0, k=True)

        for i, trs_object in enumerate(self.trs_objects):
            if i != 0:
                pbn = cmds.createNode('pairBlend', n=trs_object.nodes[-2]+'_ROT_PBN', ss=True)
                cmds.setAttr(pbn+'.rotInterpolation', 1)

                cmds.connectAttr(first_ctrl+'.r', pbn+'.inRotate2', f=True)
                cmds.connectAttr(pbn+'.outRotate', trs_object.nodes[-2]+'.r', f=True)

                cmds.connectAttr(first_ctrl+'.rotChildren', pbn+'.w', f=True)

    def connection(self):
        for ctrl_object, jnt in zip(self.trs_objects, self.jnt_object.nodes):
            ctrl = ctrl_object.nodes[-1]

            """
            splineIKのFKコントローラが機能しないので普通にコンストしてみる
            # pairBlend
            pbn = cmds.createNode('pairBlend', n=jnt+'_PBN', ss=True)

            # setAttr
            cmds.setAttr(pbn+'.rotInterpolation', 1)

            # connectAttr
            cmds.connectAttr(ctrl+'.r', pbn+'.inRotate2', f=True)
            cmds.connectAttr(pbn+'.outRotate', jnt+'.r', f=True)

            cmds.connectAttr(ctrl+'.rotateOrder', jnt+'.rotateOrder', f=True)
            cmds.connectAttr(jnt+'.rotateOrder', pbn+'.rotateOrder', f=True)

            cmds.connectAttr(ctrl+'.s', jnt+'.s', f=True)
            """

            #
            cmds.pointConstraint(ctrl, jnt, w=True)
            cmds.orientConstraint(ctrl, jnt, w=True)

            cmds.connectAttr(ctrl+'.s', jnt+'.s', f=True)
            cmds.connectAttr(ctrl+'.shear', jnt+'.shear', f=True)
            # cmds.scaleConstraint(ctrl, jnt, w=True)

        cmds.connectAttr(self.char_grp+'.jntVisibility', '{}.v'.format(self.exist_roots[-1]), f=1)
        cmds.connectAttr(self.char_grp+'.jntOverrideEnabled', '{}.overrideEnabled'.format(self.exist_roots[-1]), f=1)
        cmds.connectAttr(self.char_grp+'.jntChangeDisplayType', '{}.overrideDisplayType'.format(self.exist_roots[-1]), f=1)

    def base_connection(self, to_nodes=None, pos=True, rot=True, scl=True, mo=True):
        if not to_nodes:
            if self.namespace:
                self.joints = [self.namespace+':'+n for n in self.joints]

            to_nodes=self.joints

        connects = brConnecter.Connecters(nodes=self.jnt_object.nodes, to_nodes=to_nodes)
        connects.constraints_nodes(pos, rot, scl, mo)
