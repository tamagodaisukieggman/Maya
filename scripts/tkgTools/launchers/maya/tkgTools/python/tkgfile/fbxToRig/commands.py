# -*- coding: utf-8 -*-
from maya import cmds, mel
import maya.OpenMaya as om
import maya.api.OpenMaya as om2

from collections import OrderedDict
import fnmatch
import math
import os
import re
import traceback

if cmds.pluginInfo('fbxmaya', q=True, l=True) == False:
    cmds.loadPlugin("fbxmaya")

def create_distance_weight(nodes=None):
    connect_dict = {}
    connect_dict['s_m'] = list()
    connect_dict['m_e'] = list()
    connect_dict['s_e'] = list()
    disbs = list()
    for i, obj in enumerate(nodes):
        disb = cmds.createNode('distanceBetween', ss=True)
        dcmx = cmds.createNode('decomposeMatrix', ss=True)
        disbs.append(disb)
        cmds.connectAttr(
            '{}.worldMatrix[0]'.format(obj),
            '{}.inputMatrix'.format(dcmx),
            f=True
            )
        if i == 0 or i == 1:
            connect_dict['s_m'].append(dcmx)
        if i == 1 or i == 2:
            connect_dict['m_e'].append(dcmx)
        if i == 0 or i == 2:
            connect_dict['s_e'].append(dcmx)


    dcmxs = list()
    dcmxs.append(connect_dict['s_m'])
    dcmxs.append(connect_dict['m_e'])
    dcmxs.append(connect_dict['s_e'])

    for dis, dcmx in zip(disbs, dcmxs):
        cmds.connectAttr(
            '{}.outputTranslate'.format(dcmx[0]),
            '{}.point1'.format(dis),
            f=True
            )

        cmds.connectAttr(
            '{}.outputTranslate'.format(dcmx[1]),
            '{}.point2'.format(dis),
            f=True
            )


    dis_pma = cmds.createNode('plusMinusAverage', ss=True)
    dis_md = cmds.createNode('multiplyDivide', ss=True)
    dis_w_md = cmds.createNode('multiplyDivide', ss=True)
    weight_param_md = cmds.createNode('multiplyDivide', ss=True)

    cmds.connectAttr(
        disbs[0] + '.distance',
        dis_pma + '.input1D[0]',
        f=True
    )
    cmds.connectAttr(
        disbs[1] + '.distance',
        dis_pma + '.input1D[1]',
        f=True
    )

    # md
    cmds.setAttr(
        dis_md + '.operation',
        2
    )

    cmds.connectAttr(
        disbs[2] + '.distance',
        dis_md + '.input1X',
        f=True
    )

    cmds.connectAttr(
        disbs[0] + '.distance',
        dis_md + '.input1Y',
        f=True
    )

    cmds.connectAttr(
        disbs[1] + '.distance',
        dis_md + '.input1Z',
        f=True
    )

    #
    cmds.connectAttr(
        dis_pma + '.output1D',
        dis_md + '.input2X',
        f=True
    )

    cmds.connectAttr(
        disbs[2] + '.distance',
        dis_md + '.input2Y',
        f=True
    )

    cmds.connectAttr(
        disbs[2] + '.distance',
        dis_md + '.input2Z',
        f=True
    )

    #
    cmds.connectAttr(
        dis_md + '.output',
        dis_w_md + '.input1',
        f=True
    )

    # md
    cmds.connectAttr(
        dis_w_md + '.outputX',
        weight_param_md + '.input1Y',
        f=True
    )

    cmds.connectAttr(
        dis_w_md + '.outputX',
        weight_param_md + '.input1Z',
        f=True
    )

    cmds.connectAttr(
        dis_w_md + '.outputY',
        weight_param_md + '.input2Y',
        f=True
    )

    cmds.connectAttr(
        dis_w_md + '.outputZ',
        weight_param_md + '.input2Z',
        f=True
    )

    return weight_param_md


def create_angle_dim(start=None, middle=None, end=None):
    angle_dim = cmds.createNode('angleDimension', ss=True)
    dim_p = cmds.listRelatives(angle_dim, p=True)[0]
    cmds.parent(dim_p, start)
    for i, obj in enumerate([start, middle, end]):
        dcmx = cmds.createNode('decomposeMatrix', ss=True)
        cmds.connectAttr(
            '{}.worldMatrix[0]'.format(obj),
            '{}.inputMatrix'.format(dcmx),
            f=True
            )

        angle_dim_connect = 'start'
        if i == 0:
            pass
        elif i == 1:
            angle_dim_connect = 'middle'
        elif i == 2:
            angle_dim_connect = 'end'

        cmds.connectAttr(
            '{}.outputTranslate'.format(dcmx),
            '{}.{}Point'.format(angle_dim, angle_dim_connect),
            f=True
            )


    return angle_dim


def create_angle_dim_to_weight(joints=None):
    angle_dim = create_angle_dim(*joints)

    angle_pma = cmds.createNode('plusMinusAverage', ss=True)
    angle_md = cmds.createNode('multiplyDivide', ss=True)
    weight_md = cmds.createNode('multiplyDivide', ss=True)

    # pma
    cmds.setAttr(
        angle_pma + '.operation',
        2
    )

    cmds.setAttr(
        angle_pma + '.input1D[0]',
        180
    )

    cmds.connectAttr(
        angle_dim + '.angle',
        angle_pma + '.input1D[1]',
        f=True
    )

    # md
    cmds.setAttr(
        angle_md + '.operation',
        2
    )

    cmds.setAttr(
        angle_md + '.input2X',
        180
    )

    cmds.connectAttr(
        angle_pma + '.output1D',
        angle_md + '.input1X',
        f=True
    )

    cmds.connectAttr(
        angle_md + '.outputX',
        weight_md + '.input1X',
        f=True
    )

    return weight_md


def create_pv_locators(joints=None, aim=None, up=None,
                       set_prim=None, set_scnd=None, ik_pv_ctrl=None):

    aim_settings = {
        'w':True,
        'offset':[0,0,0],
        'aimVector':set_prim,
        'upVector':set_scnd,
        'worldUpType':'object',
        'worldUpObject':up
    }

    angle_md = create_angle_dim_to_weight(joints=joints)
    dis_w_md = create_distance_weight(nodes=joints)

    dis_w_pb = cmds.createNode('pairBlend', ss=True)
    aim_dis_loc = joints[1] + '_p_match_loc'
    loc = cmds.spaceLocator()[0]
    cmds.rename(loc, aim_dis_loc)
    cmds.parent(aim_dis_loc, joints[0])

    end_dis_loc = joints[2] + '_end_match_loc'
    loc = cmds.spaceLocator()[0]
    cmds.rename(loc, end_dis_loc)
    cmds.pointConstraint(joints[2], end_dis_loc)
    cmds.parent(end_dis_loc, joints[0])
    cmds.connectAttr(
        end_dis_loc + '.t',
        dis_w_pb + '.inTranslate2',
        f=True
    )
    cmds.connectAttr(
        dis_w_md + '.outputY',
        dis_w_pb + '.weight',
        f=True
    )
    cmds.connectAttr(
        dis_w_pb + '.outTranslate',
        aim_dis_loc + '.t',
        f=True
    )

    aim_cnst = cmds.aimConstraint(aim, aim_dis_loc, **aim_settings)

    cnd = cmds.createNode('condition', ss=True)
    cmds.setAttr(
        cnd + '.operation',
        2
    )
    cmds.setAttr(
        cnd + '.colorIfTrueR',
        1
    )
    cmds.setAttr(
        cnd + '.colorIfFalseR',
        0
    )

    cmds.connectAttr(
        angle_md + '.outputX',
        cnd + '.firstTerm',
        f=True
    )

    aim_const_pb = cmds.createNode('pairBlend', ss=True)

    cmds.connectAttr(
        aim_cnst[0] + '.constraintRotate',
        aim_const_pb + '.inRotate2',
        f=True
    )

    cmds.disconnectAttr(
        aim_cnst[0] + '.constraintRotateX',
        aim_dis_loc + '.rx'
    )
    cmds.disconnectAttr(
        aim_cnst[0] + '.constraintRotateY',
        aim_dis_loc + '.ry'
    )
    cmds.disconnectAttr(
        aim_cnst[0] + '.constraintRotateZ',
        aim_dis_loc + '.rz'
    )

    cmds.connectAttr(
        aim_const_pb + '.outRotate',
        aim_dis_loc + '.r',
        f=True
    )

    cmds.connectAttr(
        cnd + '.outColorR',
        aim_const_pb + '.weight',
        f=True
    )

    new_name = joints[1] + '_match_loc'
    pv_loc = cmds.spaceLocator()[0]
    cmds.rename(pv_loc, new_name)
    cmds.matchTransform(new_name, joints[1], pos=True, rot=False, scl=False)
    cmds.xform(new_name, **ik_pv_ctrl)
    cmds.parent(new_name, aim_dis_loc)

    return new_name


class MatchConstraint():
    def __init__(self, namespace=None):
        self.parent_const_ops = {
            'mo':True,
            'w':True
        }

        self.point_const_ops = {
            'mo':False,
            'w':True
        }

        self.orient_const_ops = {
            'mo':True,
            'w':True
        }


        self.orient_setAttr_ops = {
            'interpType':2
        }

        self.namespace = namespace

        self.root_ctrl = self.namespace + 'Root_ctrl'
        self.hip_ctrl = self.namespace + 'Cog_ctrl'
        self.spine01_ctrl = self.namespace + 'Spine1_ctrl'
        self.spine02_ctrl = self.namespace + 'Spine2_ctrl'
        self.spine03_ctrl = self.namespace + 'Spine3_ctrl'
        self.neck_ctrl = self.namespace + 'Neck_ctrl'
        self.head_ctrl = self.namespace + 'Head_ctrl'

        self.shoulder_L_ctrl = self.namespace + 'Shoulder_L_ctrl'
        self.arm_L_ctrl = self.namespace + 'Arm_L_ctrl'
        self.elbow_L_ctrl = self.namespace + 'Elbow_L_ctrl'
        self.wrist_L_ctrl = self.namespace + 'Wrist_L_ctrl'

        self.thumb01_L_ctrl = self.namespace + 'Thumb_01_L_ctrl'
        self.thumb02_L_ctrl = self.namespace + 'Thumb_02_L_ctrl'
        self.thumb03_L_ctrl = self.namespace + 'Thumb_03_L_ctrl'
        self.index01_L_ctrl = self.namespace + 'Index_01_L_ctrl'
        self.index02_L_ctrl = self.namespace + 'Index_02_L_ctrl'
        self.index03_L_ctrl = self.namespace + 'Index_03_L_ctrl'
        self.middle01_L_ctrl = self.namespace + 'Middle_01_L_ctrl'
        self.middle02_L_ctrl = self.namespace + 'Middle_02_L_ctrl'
        self.middle03_L_ctrl = self.namespace + 'Middle_03_L_ctrl'
        self.ring01_L_ctrl = self.namespace + 'Ring_01_L_ctrl'
        self.ring02_L_ctrl = self.namespace + 'Ring_02_L_ctrl'
        self.ring03_L_ctrl = self.namespace + 'Ring_03_L_ctrl'
        self.pinky01_L_ctrl = self.namespace + 'Pinky_01_L_ctrl'
        self.pinky02_L_ctrl = self.namespace + 'Pinky_02_L_ctrl'
        self.pinky03_L_ctrl = self.namespace + 'Pinky_03_L_ctrl'

        self.thigh_L_ctrl = self.namespace + 'Thigh_L_ctrl'
        self.knee_L_ctrl = self.namespace + 'Knee_L_ctrl'
        self.ankle_L_ctrl = self.namespace + 'Ankle_L_ctrl'
        self.toe_L_ctrl = self.namespace + 'Toe_L_ctrl'

        self.ik_wrist_L_switch = self.namespace + 'ikfk_Wrist_L_ctrl'
        self.ik_wrist_L_ctrl = self.namespace + 'ik_Wrist_L_ctrl'
        self.ik_wrist_rot_L_ctrl = self.namespace + 'ik_rot_Wrist_L_ctrl'
        self.ik_elbow_L_ctrl = self.namespace + 'ik_Elbow_L_ctrl'
        self.ik_wrist_L_match_loc = 'Wrist_L_match_loc'
        self.ik_elbow_L_match_loc = 'Elbow_L_match_loc'

        self.ik_ankle_L_switch = self.namespace + 'ikfk_Ankle_L_ctrl'
        self.ik_ankle_L_ctrl = self.namespace + 'ik_Ankle_L_ctrl'
        self.ik_toe_L_ctrl = self.namespace + 'ik_Toe_L_ctrl'
        self.ik_knee_L_ctrl = self.namespace + 'ik_Knee_L_ctrl'
        self.ik_ankle_L_match_loc = 'Ankle_L_match_loc'
        self.ik_knee_L_match_loc = 'Knee_L_match_loc'

        self.weapon01_L_ctrl = self.namespace + 'Handattach_L_ctrl'

        self.const_settings = {
            'Root':{
                'targets':['{}'.format(self.root_ctrl)],
                'const_type':'parent',
                'const_ops':self.parent_const_ops
            },
            'Hip':{
                'targets':['{}'.format(self.hip_ctrl)],
                'const_type':'parent',
                'const_ops':self.parent_const_ops
            },
            'Spine1':{
                'targets':['{}'.format(self.spine01_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },
            'Spine2':{
                'targets':['{}'.format(self.spine02_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },
            'Spine3':{
                'targets':['{}'.format(self.spine03_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },
            'Neck':{
                'targets':['{}'.format(self.neck_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },
            'Head':{
                'targets':['{}'.format(self.head_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },

            # arm
            'Shoulder_L':{
                'targets':['{}'.format(self.shoulder_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },
            '{}'.format(self.ik_wrist_L_match_loc):{
                'targets':['{}'.format(self.ik_wrist_L_ctrl)],
                'const_type':'point',
                'const_ops':self.point_const_ops,
            },
            'Wrist_L':{
                'targets':['{}'.format(self.ik_wrist_rot_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },
            '{}'.format(self.ik_elbow_L_match_loc):{
                'targets':['{}'.format(self.ik_elbow_L_ctrl)],
                'const_type':'point',
                'const_ops':self.point_const_ops,
            },

            # leg
            '{}'.format(self.ik_ankle_L_match_loc):{
                'targets':['{}'.format(self.ik_ankle_L_ctrl)],
                'const_type':'parent',
                'const_ops':self.parent_const_ops,
            },
            '{}'.format(self.ik_knee_L_match_loc):{
                'targets':['{}'.format(self.ik_knee_L_ctrl)],
                'const_type':'point',
                'const_ops':self.point_const_ops,
            },
            'Toe_L':{
                'targets':['{}'.format(self.ik_toe_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },

            # finger
            'Thumb_01_L':{
                'targets':['{}'.format(self.thumb01_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },
            'Thumb_02_L':{
                'targets':['{}'.format(self.thumb02_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },
            'Thumb_03_L':{
                'targets':['{}'.format(self.thumb03_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },

            'Index_01_L':{
                'targets':['{}'.format(self.index01_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },
            'Index_02_L':{
                'targets':['{}'.format(self.index02_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },
            'Index_03_L':{
                'targets':['{}'.format(self.index03_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },

            'Middle_01_L':{
                'targets':['{}'.format(self.middle01_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },
            'Middle_02_L':{
                'targets':['{}'.format(self.middle02_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },
            'Middle_03_L':{
                'targets':['{}'.format(self.middle03_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },

            'Ring_01_L':{
                'targets':['{}'.format(self.ring01_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },
            'Ring_02_L':{
                'targets':['{}'.format(self.ring02_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },
            'Ring_03_L':{
                'targets':['{}'.format(self.ring03_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },

            'Pinky_01_L':{
                'targets':['{}'.format(self.pinky01_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },
            'Pinky_02_L':{
                'targets':['{}'.format(self.pinky02_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },
            'Pinky_03_L':{
                'targets':['{}'.format(self.pinky03_L_ctrl)],
                'const_type':'orient',
                'const_ops':self.orient_const_ops,
                'setAttr_ops':self.orient_setAttr_ops
            },

            # weapon
            'Handattach_L':{
                'targets':['{}'.format(self.weapon01_L_ctrl)],
                'const_type':'parent',
                'const_ops':self.parent_const_ops,
            },

        }

        self.mirror_src = [
            'Shoulder_L',
            '{}'.format(self.ik_wrist_L_match_loc),
            'Wrist_L',
            '{}'.format(self.ik_elbow_L_match_loc),
            '{}'.format(self.ik_ankle_L_match_loc),
            '{}'.format(self.ik_knee_L_match_loc),
            'Toe_L',
            'Thumb_01_L',
             'Thumb_02_L',
             'Thumb_03_L',
             'Index_01_L',
             'Index_02_L',
             'Index_03_L',
             'Middle_01_L',
             'Middle_02_L',
             'Middle_03_L',
             'Ring_01_L',
             'Ring_02_L',
             'Ring_03_L',
             'Pinky_01_L',
             'Pinky_02_L',
             'Pinky_03_L',
            'Handattach_L'
        ]

        self.mirrors = ['_L', '_R']

        self.chr_nss_joints = list()
        self.chr_nss = None

    def mirror_character(self, mirrors=['_L', '_R'], replace_src=None):
        mirrors_src_found = re.findall(mirrors[0], replace_src)

        renamed_char = replace_src.replace(mirrors[0], mirrors[1])

        if len(mirrors_src_found) > 1:
            splited_src = replace_src.split('_')
            splited_mir_src = [mir for mir in mirrors[0].split('_') if not mir == '']
            splited_mir_dst = [mir for mir in mirrors[1].split('_') if not mir == '']
            replace_src_idx = 0
            for spl_d in splited_src:
                for spl_ms in splited_mir_src:
                    if spl_d == spl_ms:
                        replace_src_idx = splited_src.index(spl_d)
                        break

            combined = []
            for i, repl_d in enumerate(splited_src):
                if i == replace_src_idx:
                    repl_d = ''.join(splited_mir_dst)

                combined.append(repl_d)

            renamed_char = '_'.join(combined)

        return renamed_char


    def order_joints(self, joints=None):
        parent_jnt = cmds.ls(joints[0], l=1, type='joint')[0].split('|')[1]

        all_hir = cmds.listRelatives(parent_jnt, ad=True, f=True)
        hir_split_counter = {}
        for fp_node in all_hir:
            hir_split_counter[fp_node] = len(fp_node.split('|'))

        hir_split_counter_sorted = sorted(hir_split_counter.items(), key=lambda x:x[1])

        sorted_joint_list = [jnt_count[0] for jnt_count in hir_split_counter_sorted]

        all_ordered_jnts = cmds.ls(sorted_joint_list)
        return [jnt for jnt in all_ordered_jnts if jnt in joints]

    def create_dummy_bind_joints(self):
        ref_top_nodes = cmds.ls(rn=True, assemblies=True, type='joint')

        search_txt_list = [
            '*cloth_test*',
            '*proxy_*',
            '*ik_*'
        ]

        for search_txt in search_txt_list:
            filtered = list(set(fnmatch.filter(ref_top_nodes, search_txt)))
            [ref_top_nodes.remove(filt) for filt in filtered]

        self.ordered_jnts = self.order_joints(joints=ref_top_nodes)

        self.chr_nss_joints = list(set(fnmatch.filter(self.ordered_jnts, '*:chr:*')))
        self.chr_nss_joints = self.order_joints(joints=self.chr_nss_joints)
        self.chr_nss = ':'.join(self.chr_nss_joints[0].split(':')[0:-1]) + ':'

        dup_jnts = cmds.duplicate(self.ordered_jnts[0])
        self.ordered_jnts = self.order_joints(joints=dup_jnts)

        cmds.parent(self.ordered_jnts[0], w=True)

        consts = cmds.listRelatives(self.ordered_jnts[0], type='constraint', ad=True, f=True)
        cmds.delete(consts)

        # aim locs
        create_aim_locs = {
            'Arm_L':{
                'type':'wld',
                'suffix':'_aim_match_loc',
                'offset':{

                    },
                'rev_pointConstraint':{
                    'sources':['Arm_L', 'Wrist_L'],
                    'dest':'offset',
                    'settings':{
                        'mo':False,
                        'w':True
                    },
                    'setAttrs':{

                    }
                }
            },
            'Arm_R':{
                'type':'wld',
                'suffix':'_aim_match_loc',
                'offset':{

                    },
                'rev_pointConstraint':{
                    'sources':['Arm_R', 'Wrist_R'],
                    'dest':'offset',
                    'settings':{
                        'mo':False,
                        'w':True
                    },
                    'setAttrs':{

                    }
                }
            },
            'Thigh_L':{
                'type':'wld',
                'suffix':'_aim_match_loc',
                'offset':{

                    },
                'rev_pointConstraint':{
                    'sources':['Thigh_L', 'Ankle_L'],
                    'dest':'offset',
                    'settings':{
                        'mo':False,
                        'w':True
                    },
                    'setAttrs':{

                    }
                }
            },
            'Thigh_R':{
                'type':'wld',
                'suffix':'_aim_match_loc',
                'offset':{

                    },
                'rev_pointConstraint':{
                    'sources':['Thigh_R', 'Ankle_R'],
                    'dest':'offset',
                    'settings':{
                        'mo':False,
                        'w':True
                    },
                    'setAttrs':{

                    }
                }
            },
        }

        self.create_ikfk_match_locs(create_aim_locs)


        create_match_locs = {
            'Wrist_L':{
                'type':'wld',
                'suffix':'_match_loc'
            },
            'Wrist_R':{
                'type':'wld',
                'suffix':'_match_loc'
            },

            'Ankle_L':{
                'type':'wld',
                'suffix':'_match_loc'
            },
            'Ankle_R':{
                'type':'wld',
                'suffix':'_match_loc'
            },
        }

        self.create_ikfk_match_locs(create_match_locs)

        # hand L
        joints = [
            'Arm_L',
            'Elbow_L',
            'Wrist_L'
        ]

        aim = 'Elbow_L'
        up = 'Wrist_L'
        set_prim = [0,0,-1]
        set_scnd = [1,0,0]

        create_pv_locators(
            joints=joints,
            aim=aim,
            up=up,
            set_prim=set_prim,
            set_scnd=set_scnd,
            ik_pv_ctrl={
                't':[0,0,-50],
                'ws':True,
                'r':True
            }
        )

        # hand R
        joints = [
            'Arm_R',
            'Elbow_R',
            'Wrist_R'
        ]

        aim = 'Elbow_R'
        up = 'Wrist_R'
        set_prim = [0,0,-1]
        set_scnd = [-1,0,0]

        create_pv_locators(
            joints=joints,
            aim=aim,
            up=up,
            set_prim=set_prim,
            set_scnd=set_scnd,
            ik_pv_ctrl={
                't':[0,0,-50],
                'ws':True,
                'r':True
            }
        )

        # foot L
        joints = [
            'Thigh_L',
            'Knee_L',
            'Ankle_L'
        ]

        aim = 'Knee_L'
        up = 'Ankle_L'
        set_prim = [0,0,1]
        set_scnd = [0,-1,0]

        create_pv_locators(
            joints=joints,
            aim=aim,
            up=up,
            set_prim=set_prim,
            set_scnd=set_scnd,
            ik_pv_ctrl={
                't':[0,0,50],
                'ws':True,
                'r':True
            }
        )

        # foot R
        joints = [
            'Thigh_R',
            'Knee_R',
            'Ankle_R'
        ]

        aim = 'Knee_R'
        up = 'Ankle_R'
        set_prim = [0,0,1]
        set_scnd = [0,-1,0]

        create_pv_locators(
            joints=joints,
            aim=aim,
            up=up,
            set_prim=set_prim,
            set_scnd=set_scnd,
            ik_pv_ctrl={
                't':[0,0,50],
                'ws':True,
                'r':True
            }
        )


    def create_ikfk_match_locs(self, create_match_locs=None):
        u"""
        create_ikfk_match_locs(self.create_match_locs)
        """
        for obj, settings in create_match_locs.items():
            loc = cmds.spaceLocator()
            suffix = settings['suffix']
            match_loc = obj+suffix
            cmds.rename(loc[0], match_loc)

            cmds.matchTransform(match_loc, obj, pos=True, rot=False, scl=False)

            cmds.parent(match_loc, obj)


            if 'offset' in settings.keys():
                p_loc = cmds.spaceLocator()
                p_match_loc = obj+'_p'+suffix
                cmds.rename(p_loc[0], p_match_loc)

                cmds.matchTransform(p_match_loc, obj, pos=True, rot=False, scl=False)

                cmds.parent(p_match_loc, obj)
                cmds.parent(match_loc, p_match_loc)

                for attr, val in settings['offset'].items():
                    cmds.setAttr(match_loc+'.'+attr, val)


            if 'orientConstraint' in settings.keys():
                for const, const_set in settings.items():
                    if 'orient' in const:
                        const_srcs = const_set['sources']
                        const_dst = const_set['dest']
                        const_settings = const_set['settings']
                        const_setAttrs = const_set['setAttrs']
                        if const_dst == 'offset':
                            const_dst = p_match_loc
                        for const_src in const_srcs:
                            ori_const = cmds.orientConstraint(const_src, const_dst, **const_settings)
                            for set_const_at, set_const_at_val in const_setAttrs.items():
                                cmds.setAttr(ori_const[0]+'.'+set_const_at, set_const_at_val)

            elif 'rev_pointConstraint' in settings.keys():
                for const, const_set in settings.items():
                    if 'point' in const:
                        const_srcs = const_set['sources']
                        const_dst = const_set['dest']
                        const_settings = const_set['settings']
                        const_setAttrs = const_set['setAttrs']
                        if const_dst == 'offset':
                            const_dst = p_match_loc
                        for const_src in const_srcs:
                            rev_po_const = cmds.pointConstraint(const_src, const_dst, **const_settings)
                            for set_const_at, set_const_at_val in const_setAttrs.items():
                                cmds.setAttr(rev_po_const[0]+'.'+set_const_at, set_const_at_val)

            elif 'rev_aimConstraint' in settings.keys():
                for const, const_set in settings.items():
                    if 'aim' in const:
                        const_srcs = const_set['sources']
                        const_dst = const_set['dest']
                        const_settings = const_set['settings']
                        const_setAttrs = const_set['setAttrs']
                        if const_dst == 'offset':
                            const_dst = p_match_loc
                        for const_src in const_srcs:
                            rev_po_const = cmds.aimConstraint(const_src, const_dst, **const_settings)
                            for set_const_at, set_const_at_val in const_setAttrs.items():
                                cmds.setAttr(rev_po_const[0]+'.'+set_const_at, set_const_at_val)

    def match_bind_joints_to_ctrls(self):

        self.create_dummy_bind_joints()

        mirror_const_settings = {}
        for src, const_set in self.const_settings.items():
            if src in self.mirror_src:
                mirror_obj = self.mirror_character(mirrors=self.mirrors, replace_src=src)
                targets = const_set['targets']
                mirror_targets = []
                for tgt in targets:
                    mirror_tgt = self.mirror_character(mirrors=self.mirrors, replace_src=tgt)
                    mirror_targets.append(mirror_tgt)

                mirror_const_settings[mirror_obj] = {}
                mirror_const_settings[mirror_obj]['targets'] = mirror_targets
                for mir_key, mir_val in const_set.items():
                    if not mir_key == 'targets':
                        mirror_const_settings[mirror_obj][mir_key] = mir_val

        for mir_set_key, mir_set_val in mirror_const_settings.items():
            self.const_settings[mir_set_key] = mir_set_val

        bake_cnst_sets = 'bake_cnst_sets'
        if not cmds.objExists(bake_cnst_sets):
            cmds.sets(n=bake_cnst_sets, em=True)

        cmds.sets(self.ordered_jnts[0], add=bake_cnst_sets)

        for src, const_set in self.const_settings.items():
            targets = const_set['targets']
            if 'const_type' in const_set.keys():
                const_ops = const_set['const_ops']
                setAttr_ops = None
                if 'setAttr_ops' in const_set.keys():
                    setAttr_ops = const_set['setAttr_ops']

                if 'point' == const_set['const_type']:
                    for target in targets:
                        print('src:', src, 'dst:', target)
                        const = cmds.pointConstraint(src, target, **const_ops)

                elif 'orient' == const_set['const_type']:
                    for target in targets:
                        print('src:', src, 'dst:', target)
                        const = cmds.orientConstraint(src, target, **const_ops)

                elif 'parent' == const_set['const_type']:
                    for target in targets:
                        print('src:', src, 'dst:', target)
                        const = cmds.parentConstraint(src, target, **const_ops)

                cmds.sets(const, add=bake_cnst_sets)

                if setAttr_ops:
                    for const_at, const_val in setAttr_ops.items():
                        cmds.setAttr(const[0] + '.' + const_at, const_val)


    def hand_fk_const(self, side=None):
        hand_fk_const = {
            'L':[
                {
                    'src':'Arm_L',
                    'target':self.arm_L_ctrl,
                    'const_ops':{
                        'w':True,
                        'mo':True
                    },
                    'set_attr':{
                        'interpType':2
                    }
                },
                {
                    'src':'Elbow_L',
                    'target':self.elbow_L_ctrl,
                    'const_ops':{
                        'w':True,
                        'mo':True,
                        'skip':['x', 'z']
                    },
                    'set_attr':{
                        'interpType':2
                    }
                },
                {
                    'src':'Wrist_L',
                    'target':self.wrist_L_ctrl,
                    'const_ops':{
                        'w':True,
                        'mo':True
                    },
                    'set_attr':{
                        'interpType':2
                    }
                },
            ],
            'R':[
                {
                    'src':'Arm_R',
                    'target':self.mirror_character(self.mirrors, self.arm_L_ctrl),
                    'const_ops':{
                        'w':True,
                        'mo':True
                    },
                    'set_attr':{
                        'interpType':2
                    }
                },
                {
                    'src':'Elbow_R',
                    'target':self.mirror_character(self.mirrors, self.elbow_L_ctrl),
                    'const_ops':{
                        'w':True,
                        'mo':True,
                        'skip':['x', 'z']
                    },
                    'set_attr':{
                        'interpType':2
                    }
                },
                {
                    'src':'Wrist_R',
                    'target':self.mirror_character(self.mirrors, self.wrist_L_ctrl),
                    'const_ops':{
                        'w':True,
                        'mo':True
                    },
                    'set_attr':{
                        'interpType':2
                    }
                },
            ]
        }

        if side in hand_fk_const.keys():
            fk_items = hand_fk_const[side]
            for item in fk_items:
                src = item['src']
                target = item['target']
                const_ops = item['const_ops']
                const = cmds.orientConstraint(src, target, **const_ops)
                if 'set_attr' in item.keys():
                    for at, val in item['set_attr'].items():
                        cmds.setAttr(const[0] + '.' + at, val)

            cmds.sets(const, add='bake_cnst_sets')

    def foot_fk_const(self, side=None):
        foot_fk_const = {
            'L':[
                {
                    'src':'Thigh_L',
                    'target':self.thigh_L_ctrl,
                    'const_ops':{
                        'w':True,
                        'mo':True
                    },
                    'set_attr':{
                        'interpType':2
                    }
                },
                {
                    'src':'Knee_L',
                    'target':self.knee_L_ctrl,
                    'const_ops':{
                        'w':True,
                        'mo':True,
                        'skip':['x', 'z']
                    },
                    'set_attr':{
                        'interpType':2
                    }
                },
                {
                    'src':'Ankle_L',
                    'target':self.ankle_L_ctrl,
                    'const_ops':{
                        'w':True,
                        'mo':True
                    },
                    'set_attr':{
                        'interpType':2
                    }
                },
                {
                    'src':'Toe_L',
                    'target':self.toe_L_ctrl,
                    'const_ops':{
                        'w':True,
                        'mo':True
                    },
                    'set_attr':{
                        'interpType':2
                    }
                },
            ],
            'R':[
                {
                    'src':'Thigh_R',
                    'target':self.mirror_character(self.mirrors, self.thigh_L_ctrl),
                    'const_ops':{
                        'w':True,
                        'mo':True
                    },
                    'set_attr':{
                        'interpType':2
                    }
                },
                {
                    'src':'Knee_R',
                    'target':self.mirror_character(self.mirrors, self.knee_L_ctrl),
                    'const_ops':{
                        'w':True,
                        'mo':True,
                        'skip':['x', 'z']
                    },
                    'set_attr':{
                        'interpType':2
                    }
                },
                {
                    'src':'Ankle_R',
                    'target':self.mirror_character(self.mirrors, self.ankle_L_ctrl),
                    'const_ops':{
                        'w':True,
                        'mo':True
                    },
                    'set_attr':{
                        'interpType':2
                    }
                },
                {
                    'src':'Toe_R',
                    'target':self.mirror_character(self.mirrors, self.toe_L_ctrl),
                    'const_ops':{
                        'w':True,
                        'mo':True
                    },
                    'set_attr':{
                        'interpType':2
                    }
                },
            ]
        }

        if side in foot_fk_const.keys():
            fk_items = foot_fk_const[side]
            for item in fk_items:
                src = item['src']
                target = item['target']
                const_ops = item['const_ops']
                const = cmds.orientConstraint(src, target, **const_ops)
                if 'set_attr' in item.keys():
                    for at, val in item['set_attr'].items():
                        cmds.setAttr(const[0] + '.' + at, val)

            cmds.sets(const, add='bake_cnst_sets')


    def fk_base_constraint(self, fk_parts=None):
        if ('foot_L' in fk_parts
            or 'foot_R' in fk_parts
            or 'hand_L' in fk_parts
            or 'hand_R' in fk_parts):

                if 'foot_L' in fk_parts:
                    cmds.setAttr(self.ik_ankle_L_switch + '.ikfk', 0)
                    self.foot_fk_const(side='L')

                if 'foot_R' in fk_parts:
                    cmds.setAttr(self.mirror_character(self.mirrors,
                                 self.ik_ankle_L_switch) + '.ikfk', 0)
                    self.foot_fk_const(side='R')

                if 'hand_L' in fk_parts:
                    cmds.setAttr(self.ik_wrist_L_switch + '.ikfk', 0)
                    self.hand_fk_const(side='L')

                if 'hand_R' in fk_parts:
                    cmds.setAttr(self.mirror_character(self.mirrors,
                                 self.ik_wrist_L_switch) + '.ikfk', 0)
                    self.hand_fk_const(side='R')


def mirror_character(mirrors=['_L', '_R'], replace_src=None):
    mirrors_src_found = re.findall(mirrors[0], replace_src)

    renamed_char = replace_src.replace(mirrors[0], mirrors[1])

    if len(mirrors_src_found) > 1:
        splited_src = replace_src.split('_')
        splited_mir_src = [mir for mir in mirrors[0].split('_') if not mir == '']
        splited_mir_dst = [mir for mir in mirrors[1].split('_') if not mir == '']
        replace_src_idx = 0
        for spl_d in splited_src:
            for spl_ms in splited_mir_src:
                if spl_d == spl_ms:
                    replace_src_idx = splited_src.index(spl_d)
                    break

        combined = []
        for i, repl_d in enumerate(splited_src):
            if i == replace_src_idx:
                repl_d = ''.join(splited_mir_dst)

            combined.append(repl_d)

        renamed_char = '_'.join(combined)

    return renamed_char


def get_reference_info():
    ret = []

    refNodes = cmds.ls(references=True)
    for RNnode in refNodes:
        ref = {}
        ref.update({
            'namespace' : cmds.referenceQuery(RNnode, namespace=True),
            'filename'   : cmds.referenceQuery(RNnode, filename=True),
            'w_filenam' : cmds.referenceQuery(RNnode, filename=True, withoutCopyNumber=True),
            'isLoaded'  : cmds.referenceQuery(RNnode, isLoaded=True),
            'nodes'     : cmds.referenceQuery(RNnode, nodes=True),
            'node'      : cmds.referenceQuery(RNnode, nodes=True)[0],
            })
        ret.append(ref)

    return ret


def fullbake(nodes=None):
    try:
        cmds.refresh(su=1)
        cmds.cycleCheck(e=0)

        playmin = cmds.playbackOptions(q=1, min=1)
        playmax = cmds.playbackOptions(q=1, max=1)

        cmds.bakeResults(nodes, sm=1, t=(playmin, playmax), sb=1, osr=1, dic=1, pok=1, sac=0, ral=0, rba=0, bol=0, mr=1, cp=0, s=0)

        cmds.filterCurve(sel, f='euler')

        cmds.refresh(su=0)
        cmds.cycleCheck(e=1)
    except:
        cmds.refresh(su=0)
        cmds.cycleCheck(e=1)


def bake_with_func(func):
    def wrapper(*args, **kwargs):
        try:
            cmds.refresh(su=1)

            cur_time=cmds.currentTime(q=1)
            if cmds.autoKeyframe(q=True, st=True):
                autoKeyState = True
            else:
                autoKeyState = False

            cmds.autoKeyframe(st=0)

            playmin = cmds.playbackOptions(q=1, min=1)
            playmax = cmds.playbackOptions(q=1, max=1)

            start = playmin
            end = playmax

            for i in range (int(start), int(end+1)):
                cmds.currentTime(i, e=True)
                func(*args, **kwargs)

            cmds.currentTime(cur_time)
            cmds.autoKeyframe(state=autoKeyState)

            cmds.refresh(su=0)

        except:
            cmds.refresh(su=0)
            print(traceback.format_exc())

    return wrapper

def fbx_to_rig(fbx_path=None, namespace=None):
    match_const = MatchConstraint(namespace)
    match_const.match_bind_joints_to_ctrls()

    mel.eval('FBXImportSetMayaFrameRate -v 1;')
    mel.eval('FBXImportMode -v "exmerge";')
    # mel.eval('FBXImport -f "{}";'.format(fbx_path))

    basename_without_ext = os.path.splitext(os.path.basename(fbx_path))[0]
    cmds.file(
        fbx_path,
        i=True,
        type='FBX',
        ignoreVersion=True,
        mergeNamespacesOnClash=False,
        pr=True,
        importTimeRange='override',
        importFrameRate=True,
        ra=True,
        namespace=basename_without_ext
    )

    # フレームがスナップされるように設定
    cmds.optionVar(intValue=['scaleKeyAutoSnap', True])

    # translateのキーを削除&修正
    fix_pos_anim(chr_joints=match_const.ordered_jnts, chr_nss=match_const.chr_nss)

    cmds.select(namespace + 'ctrl_sets', ne=True, r=True)
    ctrls = cmds.pickWalk(d='down')
    fullbake(nodes=ctrls)

    cmds.select('bake_cnst_sets', ne=True, r=True)
    const_nodes = cmds.pickWalk(d='down')
    cmds.delete(const_nodes)

    # 設定をデフォルトに戻さないと他のオプションに影響が出るので戻しておく
    mel.eval('FBXImportMode -v "merge";')

def get_animCurve(obj=None, attrs=None):
    settings = {
        'p':True,
        's':True,
        'type':'animCurve'
    }
    anim_curves_list = list()
    for at in attrs:
        anim_curves = cmds.listConnections('{}.{}'.format(obj, at), **settings) or None
        if anim_curves: anim_curves_list.append(anim_curves[0])

    return anim_curves_list


def fix_pos_anim(chr_joints=None, chr_nss=None):
    # 移動値を残すノード
    delete_pos_nodes = [
        'Root',
        'Hip',
        'Handattach_L',
        'Handattach_R'
    ]

    delete_pos_attrs = [
        'tx',
        'ty',
        'tz'
    ]

    # 回転のアニメーションを削除するノード
    delete_rot_nodes = [
        'HandattachOffset_L',
        'HandattachOffset_R'
    ]

    delete_rot_attrs = [
        'rx',
        'ry',
        'rz'
    ]

    # スケールのアニメーションを削除するノード
    delete_scl_nodes = [
        'HandattachOffset_L',
        'HandattachOffset_R'
    ]

    delete_scl_attrs = [
        'sx',
        'sy',
        'sz'
    ]

    chr_joints = [j for j in chr_joints if cmds.objExists(j)]

    for ch_j in chr_joints:
        if cmds.objectType(ch_j) == 'joint':
            if not ch_j in delete_pos_nodes:
                anim_curves = get_animCurve(obj=ch_j, attrs=delete_pos_attrs)
                [cmds.delete(ac.split('.')[0]) for ac in anim_curves]

                try:
                    cmds.setAttr(ch_j + '.t', *cmds.getAttr(chr_nss + ch_j + '.t')[0])
                except:
                    print(traceback.format_exc())

            if ch_j in delete_rot_nodes:
                anim_curves = get_animCurve(obj=ch_j, attrs=delete_rot_attrs)
                [cmds.delete(ac.split('.')[0]) for ac in anim_curves]

                try:
                    cmds.setAttr(ch_j + '.r', *cmds.getAttr(chr_nss + ch_j + '.r')[0])
                    # cmds.xform(ch_j, ro=cmds.xform(chr_nss + ch_j, q=True, ro=True, ws=True), ws=True, a=True)
                    quaternionToEuler_no_key(obj=ch_j)
                except:
                    print(traceback.format_exc())

            if ch_j in delete_scl_nodes:
                anim_curves = get_animCurve(obj=ch_j, attrs=delete_scl_attrs)
                [cmds.delete(ac.split('.')[0]) for ac in anim_curves]

                try:
                    cmds.setAttr(ch_j + '.s', *cmds.getAttr(chr_nss + ch_j + '.s')[0])
                except:
                    print(traceback.format_exc())


def match_objects(children=None, parents=None, settings=None):
    [cmds.matchTransform(c, p, **settings) for c, p in zip(children, parents)]

def get_hand_L_ctrl_values(namespace=None):
    if namespace == '<from_picker>':
        currentPickerNamespace = get_mgpickernamespace()
    else:
        currentPickerNamespace = namespace

    ikfk_switch = currentPickerNamespace+'ikfk_Wrist_L_ctrl.ikfk'
    state = cmds.getAttr(ikfk_switch)
    jnts = [currentPickerNamespace+'proxy_Arm_L',
            currentPickerNamespace+'proxy_Elbow_L',
            currentPickerNamespace+'proxy_Wrist_L']
    ctrls = [currentPickerNamespace+'Arm_L_ctrl',
             currentPickerNamespace+'Elbow_L_ctrl',
             currentPickerNamespace+'Wrist_L_ctrl']

    ik_pos_ctrl = currentPickerNamespace+'ik_Wrist_L_ctrl'
    ik_rot_ctrl = currentPickerNamespace+'ik_rot_Wrist_L_ctrl'
    ikpv_ctrl = currentPickerNamespace+'ik_Elbow_L_ctrl'

    pos_match_loc = currentPickerNamespace+'proxy_Wrist_L_match_loc'
    ikpv_match_loc = currentPickerNamespace+'proxy_Elbow_L_match_loc'

    return ikfk_switch, state, jnts, ctrls, ik_pos_ctrl, ik_rot_ctrl, ikpv_ctrl, pos_match_loc, ikpv_match_loc, currentPickerNamespace

def get_foot_L_ctrl_values(namespace=None):
    if namespace == '<from_picker>':
        currentPickerNamespace = get_mgpickernamespace()
    else:
        currentPickerNamespace = namespace

    ikfk_switch = currentPickerNamespace+'ikfk_Ankle_L_ctrl.ikfk'
    state = cmds.getAttr(ikfk_switch)
    jnts = [currentPickerNamespace+'proxy_Thigh_L',
            currentPickerNamespace+'proxy_Knee_L',
            currentPickerNamespace+'proxy_Ankle_L',
            currentPickerNamespace+'proxy_Toe_L',]
    ctrls = [currentPickerNamespace+'Thigh_L_ctrl',
             currentPickerNamespace+'Knee_L_ctrl',
             currentPickerNamespace+'Ankle_L_ctrl',
             currentPickerNamespace+'Toe_L_ctrl']

    ik_pos_ctrl = currentPickerNamespace+'ik_Ankle_L_ctrl'
    ik_rot_ctrl = currentPickerNamespace+'ik_Toe_L_ctrl'
    ikpv_ctrl = currentPickerNamespace+'ik_Knee_L_ctrl'

    pos_match_loc = currentPickerNamespace+'proxy_Ankle_L_match_loc'
    ikpv_match_loc = currentPickerNamespace+'proxy_Knee_L_match_loc'

    return ikfk_switch, state, jnts, ctrls, ik_pos_ctrl, ik_rot_ctrl, ikpv_ctrl, pos_match_loc, ikpv_match_loc, currentPickerNamespace


def ik2fk_match(ctrls=None, jnts=None, ikfk_switch=None, match=None):
    # IK to FK
    if match:
        [cmds.matchTransform(ctrl, jt, rot=1, pos=0, scl=0) for ctrl, jt in zip(ctrls, jnts)]
    cmds.setAttr(ikfk_switch, 0)

def fk2ik_match(match_type=None,
                ik_pos_ctrl=None,
                pos_match_loc=None,
                ikpv_ctrl=None,
                ikpv_match_loc=None,
                ik_rot_ctrl=None,
                rot_match_jnt=None,
                ikfk_switch=None,
                match=None,
                start=None,
                mid=None,
                end=None,
                move=None,
                loc_match=None):
    # FK to IK
    if match:
        if loc_match:
            cmds.matchTransform(ik_pos_ctrl, pos_match_loc)
            cmds.matchTransform(ikpv_ctrl, ikpv_match_loc)
            cmds.matchTransform(ik_rot_ctrl, rot_match_jnt)
        else:
            cmds.matchTransform(ik_pos_ctrl, pos_match_loc, rot=1, pos=1, scl=0)
            set_pole_vec(start=start, mid=mid, end=end, move=move, obj=ikpv_ctrl)
            # cmds.matchTransform(ikpv_ctrl, ikpv_match_loc, rot=1, pos=1, scl=0)
            cmds.matchTransform(ik_rot_ctrl, rot_match_jnt, rot=1, pos=1, scl=0)

    cmds.setAttr(ikfk_switch, 1)

def ikfk_hand_L(picker=None, match=None, force_state=None, force_state_key=None, namespace=None):
    ikfk_switch, state, jnts, ctrls, ik_pos_ctrl, ik_rot_ctrl, ikpv_ctrl, pos_match_loc, ikpv_match_loc, namespace = get_hand_L_ctrl_values(namespace)

    if force_state:
        if force_state == 'ik2fk':
            state = 1
        elif force_state == 'fk2ik':
            state = 0
        cmds.setAttr(ikfk_switch, state)

        cmds.setKeyframe(ikfk_switch) if force_state_key else False

    if state == 1:
        ik2fk_match(ctrls=ctrls,
                    jnts=jnts,
                    ikfk_switch=ikfk_switch,
                    match=match)

        if picker:
            # IK
            mel.eval('MGPickerItem -e -vis false selectButton79;')
            mel.eval('MGPickerItem -e -vis false selectButton88;')
            mel.eval('MGPickerItem -e -vis false selectButton101;')

            # FK
            mel.eval('MGPickerItem -e -vis true selectButton99;')
            mel.eval('MGPickerItem -e -vis true selectButton94;')
            mel.eval('MGPickerItem -e -vis true selectButton91;')

    else:
        fk2ik_match(ik_pos_ctrl=ik_pos_ctrl,
                    pos_match_loc=pos_match_loc,
                    ikpv_ctrl=ikpv_ctrl,
                    ikpv_match_loc=ikpv_match_loc,
                    ik_rot_ctrl=ik_rot_ctrl,
                    rot_match_jnt=jnts[2],
                    ikfk_switch=ikfk_switch,
                    match=match,
                    start=jnts[0],
                    mid=jnts[1],
                    end=jnts[2],
                    move=50,
                    loc_match=True)

        if picker:
            # IK
            mel.eval('MGPickerItem -e -vis true selectButton79;')
            mel.eval('MGPickerItem -e -vis true selectButton88;')
            mel.eval('MGPickerItem -e -vis true selectButton101;')

            # FK
            mel.eval('MGPickerItem -e -vis false selectButton99;')
            mel.eval('MGPickerItem -e -vis false selectButton94;')
            mel.eval('MGPickerItem -e -vis false selectButton91;')

    ctrls.append(ik_pos_ctrl)
    ctrls.append(ik_rot_ctrl)
    ctrls.append(ikpv_ctrl)

    ctrls.append(ikfk_switch) if force_state_key else False

    return ctrls



def ikfk_hand_R(picker=None, match=None, force_state=None, force_state_key=None, namespace=None):
    ikfk_switch, state, jnts, ctrls, ik_pos_ctrl, ik_rot_ctrl, ikpv_ctrl, pos_match_loc, ikpv_match_loc, namespace = get_hand_L_ctrl_values(namespace)

    ikfk_switch = mirror_character(['_L', '_R'], ikfk_switch)
    ik_pos_ctrl = mirror_character(['_L', '_R'], ik_pos_ctrl)
    ik_rot_ctrl = mirror_character(['_L', '_R'], ik_rot_ctrl)
    ikpv_ctrl = mirror_character(['_L', '_R'], ikpv_ctrl)
    pos_match_loc = mirror_character(['_L', '_R'], pos_match_loc)
    ikpv_match_loc = mirror_character(['_L', '_R'], ikpv_match_loc)

    jnts = [mirror_character(['_L', '_R'], jnt) for jnt in jnts]
    ctrls = [mirror_character(['_L', '_R'], ctrl) for ctrl in ctrls]

    state = cmds.getAttr(ikfk_switch)

    if force_state:
        if force_state == 'ik2fk':
            state = 1
        elif force_state == 'fk2ik':
            state = 0
        cmds.setAttr(ikfk_switch, state)

        cmds.setKeyframe(ikfk_switch) if force_state_key else False

    if state == 1:
        ik2fk_match(ctrls=ctrls,
                    jnts=jnts,
                    ikfk_switch=ikfk_switch,
                    match=match)

        if picker:
            # IK
            mel.eval('MGPickerItem -e -vis false selectButton110;')
            mel.eval('MGPickerItem -e -vis false selectButton118;')
            mel.eval('MGPickerItem -e -vis false selectButton102;')

            # FK
            mel.eval('MGPickerItem -e -vis true selectButton115;')
            mel.eval('MGPickerItem -e -vis true selectButton75;')
            mel.eval('MGPickerItem -e -vis true selectButton109;')

    else:
        fk2ik_match(ik_pos_ctrl=ik_pos_ctrl,
                    pos_match_loc=pos_match_loc,
                    ikpv_ctrl=ikpv_ctrl,
                    ikpv_match_loc=ikpv_match_loc,
                    ik_rot_ctrl=ik_rot_ctrl,
                    rot_match_jnt=jnts[2],
                    ikfk_switch=ikfk_switch,
                    match=match,
                    start=jnts[0],
                    mid=jnts[1],
                    end=jnts[2],
                    move=50,
                    loc_match=True)

        if picker:
            # IK
            mel.eval('MGPickerItem -e -vis true selectButton110;')
            mel.eval('MGPickerItem -e -vis true selectButton118;')
            mel.eval('MGPickerItem -e -vis true selectButton102;')

            # FK
            mel.eval('MGPickerItem -e -vis false selectButton115;')
            mel.eval('MGPickerItem -e -vis false selectButton75;')
            mel.eval('MGPickerItem -e -vis false selectButton109;')

    ctrls.append(ik_pos_ctrl)
    ctrls.append(ik_rot_ctrl)
    ctrls.append(ikpv_ctrl)

    ctrls.append(ikfk_switch) if force_state_key else False

    return ctrls



def ikfk_foot_L(picker=None, match=None, force_state=None, force_state_key=None, namespace=None):
    ikfk_switch, state, jnts, ctrls, ik_pos_ctrl, ik_rot_ctrl, ikpv_ctrl, pos_match_loc, ikpv_match_loc, namespace = get_foot_L_ctrl_values(namespace)

    roll_Toe_ctrl = namespace + 'roll_Toe_L_ctrl'

    if force_state:
        if force_state == 'ik2fk':
            state = 1
        elif force_state == 'fk2ik':
            state = 0
        cmds.setAttr(ikfk_switch, state)

        cmds.setKeyframe(ikfk_switch) if force_state_key else False

    if state == 1:
        ik2fk_match(ctrls=ctrls,
                    jnts=jnts,
                    ikfk_switch=ikfk_switch,
                    match=match)

        cmds.xform(roll_Toe_ctrl, t=[0,0,0], ro=[0,0,0], p=True, a=True) if match else False

        if picker:
            # IK
            mel.eval('MGPickerItem -e -vis false selectButton87;')
            mel.eval('MGPickerItem -e -vis false selectButton81;')
            mel.eval('MGPickerItem -e -vis false selectButton111;')
            mel.eval('MGPickerItem -e -vis false selectButton258;')

            # FK
            mel.eval('MGPickerItem -e -vis true selectButton107;')
            mel.eval('MGPickerItem -e -vis true selectButton77;')
            mel.eval('MGPickerItem -e -vis true selectButton90;')
            mel.eval('MGPickerItem -e -vis true selectButton98;')

    else:
        fk2ik_match(ik_pos_ctrl=ik_pos_ctrl,
                    pos_match_loc=pos_match_loc,
                    ikpv_ctrl=ikpv_ctrl,
                    ikpv_match_loc=ikpv_match_loc,
                    ik_rot_ctrl=ik_rot_ctrl,
                    rot_match_jnt=jnts[3],
                    ikfk_switch=ikfk_switch,
                    match=match,
                    start=jnts[0],
                    mid=jnts[1],
                    end=jnts[2],
                    move=50,
                    loc_match=True)

        cmds.xform(roll_Toe_ctrl, t=[0,0,0], ro=[0,0,0], p=True, a=True) if match else False

        if picker:
            # IK
            mel.eval('MGPickerItem -e -vis true selectButton87;')
            mel.eval('MGPickerItem -e -vis true selectButton81;')
            mel.eval('MGPickerItem -e -vis true selectButton111;')
            mel.eval('MGPickerItem -e -vis true selectButton258;')

            # FK
            mel.eval('MGPickerItem -e -vis false selectButton107;')
            mel.eval('MGPickerItem -e -vis false selectButton77;')
            mel.eval('MGPickerItem -e -vis false selectButton90;')
            mel.eval('MGPickerItem -e -vis false selectButton98;')

    ctrls.append(ik_pos_ctrl)
    ctrls.append(ik_rot_ctrl)
    ctrls.append(ikpv_ctrl)
    ctrls.append(roll_Toe_ctrl)

    ctrls.append(ikfk_switch) if force_state_key else False

    return ctrls



def ikfk_foot_R(picker=None, match=None, force_state=None, force_state_key=None, namespace=None):
    ikfk_switch, state, jnts, ctrls, ik_pos_ctrl, ik_rot_ctrl, ikpv_ctrl, pos_match_loc, ikpv_match_loc, namespace = get_foot_L_ctrl_values(namespace)

    ikfk_switch = mirror_character(['_L', '_R'], ikfk_switch)
    ik_pos_ctrl = mirror_character(['_L', '_R'], ik_pos_ctrl)
    ik_rot_ctrl = mirror_character(['_L', '_R'], ik_rot_ctrl)
    ikpv_ctrl = mirror_character(['_L', '_R'], ikpv_ctrl)
    pos_match_loc = mirror_character(['_L', '_R'], pos_match_loc)
    ikpv_match_loc = mirror_character(['_L', '_R'], ikpv_match_loc)

    jnts = [mirror_character(['_L', '_R'], jnt) for jnt in jnts]
    ctrls = [mirror_character(['_L', '_R'], ctrl) for ctrl in ctrls]

    state = cmds.getAttr(ikfk_switch)

    roll_Toe_ctrl = namespace + 'roll_Toe_R_ctrl'

    if force_state:
        if force_state == 'ik2fk':
            state = 1
        elif force_state == 'fk2ik':
            state = 0
        cmds.setAttr(ikfk_switch, state)

        cmds.setKeyframe(ikfk_switch) if force_state_key else False

    if state == 1:
        ik2fk_match(ctrls=ctrls,
                    jnts=jnts,
                    ikfk_switch=ikfk_switch,
                    match=match)

        cmds.xform(roll_Toe_ctrl, t=[0,0,0], ro=[0,0,0], p=True, a=True) if match else False

        if picker:
            # IK
            mel.eval('MGPickerItem -e -vis false selectButton86;')
            mel.eval('MGPickerItem -e -vis false selectButton93;')
            mel.eval('MGPickerItem -e -vis false selectButton112;')
            mel.eval('MGPickerItem -e -vis false selectButton259;')

            # FK
            mel.eval('MGPickerItem -e -vis true selectButton92;')
            mel.eval('MGPickerItem -e -vis true selectButton114;')
            mel.eval('MGPickerItem -e -vis true selectButton106;')
            mel.eval('MGPickerItem -e -vis true selectButton108;')

    else:
        fk2ik_match(ik_pos_ctrl=ik_pos_ctrl,
                    pos_match_loc=pos_match_loc,
                    ikpv_ctrl=ikpv_ctrl,
                    ikpv_match_loc=ikpv_match_loc,
                    ik_rot_ctrl=ik_rot_ctrl,
                    rot_match_jnt=jnts[3],
                    ikfk_switch=ikfk_switch,
                    match=match,
                    start=jnts[0],
                    mid=jnts[1],
                    end=jnts[2],
                    move=50,
                    loc_match=True)

        cmds.xform(roll_Toe_ctrl, t=[0,0,0], ro=[0,0,0], p=True, a=True) if match else False

        if picker:
            # IK
            mel.eval('MGPickerItem -e -vis true selectButton86;')
            mel.eval('MGPickerItem -e -vis true selectButton93;')
            mel.eval('MGPickerItem -e -vis true selectButton112;')
            mel.eval('MGPickerItem -e -vis true selectButton259;')

            # FK
            mel.eval('MGPickerItem -e -vis false selectButton92;')
            mel.eval('MGPickerItem -e -vis false selectButton114;')
            mel.eval('MGPickerItem -e -vis false selectButton106;')
            mel.eval('MGPickerItem -e -vis false selectButton108;')


    ctrls.append(ik_pos_ctrl)
    ctrls.append(ik_rot_ctrl)
    ctrls.append(ikpv_ctrl)
    ctrls.append(roll_Toe_ctrl)

    ctrls.append(ikfk_switch) if force_state_key else False

    return ctrls


def add_ctrls_namespace(*args, **kwargs):
    ctrls = []
    added_namespaces = {}
    for key, value in kwargs.items():
        if key == 'namespace':
            namespace = value
        else:
            ctrls.append(value)
            added_namespaces[key] = value

    if 'namespace' in kwargs.keys():
        kwargs.pop('namespace')

    for key, value in kwargs.items():
        added_namespaces[key] = namespace + value

    return added_namespaces

@bake_with_func
def ikfk_match_with_bake(hand_L=None, hand_L_ikfk=None, hand_R=None, hand_R_ikfk=None,
                         foot_L=None, foot_L_ikfk=None, foot_R=None, foot_R_ikfk=None,
                         force_state_key=None, namespace=None):

    hand_L_ctrls = ikfk_hand_L(picker=False, match=True, force_state=hand_L_ikfk, force_state_key=force_state_key, namespace=namespace) if hand_L else False
    hand_R_ctrls = ikfk_hand_R(picker=False, match=True, force_state=hand_R_ikfk, force_state_key=force_state_key, namespace=namespace) if hand_R else False
    foot_L_ctrls = ikfk_foot_L(picker=False, match=True, force_state=foot_L_ikfk, force_state_key=force_state_key, namespace=namespace) if foot_L else False
    foot_R_ctrls = ikfk_foot_R(picker=False, match=True, force_state=foot_R_ikfk, force_state_key=force_state_key, namespace=namespace) if foot_R else False

    cmds.setKeyframe(hand_L_ctrls) if hand_L_ctrls else False
    cmds.setKeyframe(hand_R_ctrls) if hand_R_ctrls else False
    cmds.setKeyframe(foot_L_ctrls) if foot_L_ctrls else False
    cmds.setKeyframe(foot_R_ctrls) if foot_R_ctrls else False

@bake_with_func
def fk2ik_ik2fk_matchbake(force_state_key=None, namespace=None):
    force_state_key=force_state_key

    # fk2ik
    hand_L=True
    hand_L_ikfk='fk2ik'

    hand_R=True
    hand_R_ikfk='fk2ik'

    foot_L=True
    foot_L_ikfk='fk2ik'

    foot_R=True
    foot_R_ikfk='fk2ik'

    hand_L_ctrls = ikfk_hand_L(picker=False, match=True, force_state=hand_L_ikfk, force_state_key=force_state_key, namespace=namespace) if hand_L else False
    hand_R_ctrls = ikfk_hand_R(picker=False, match=True, force_state=hand_R_ikfk, force_state_key=force_state_key, namespace=namespace) if hand_R else False
    foot_L_ctrls = ikfk_foot_L(picker=False, match=True, force_state=foot_L_ikfk, force_state_key=force_state_key, namespace=namespace) if foot_L else False
    foot_R_ctrls = ikfk_foot_R(picker=False, match=True, force_state=foot_R_ikfk, force_state_key=force_state_key, namespace=namespace) if foot_R else False

    cmds.setKeyframe(hand_L_ctrls) if hand_L_ctrls else False
    cmds.setKeyframe(hand_R_ctrls) if hand_R_ctrls else False
    cmds.setKeyframe(foot_L_ctrls) if foot_L_ctrls else False
    cmds.setKeyframe(foot_R_ctrls) if foot_R_ctrls else False

    # ik2fk
    hand_L=True
    hand_L_ikfk='ik2fk'

    hand_R=True
    hand_R_ikfk='ik2fk'

    foot_L=True
    foot_L_ikfk='ik2fk'

    foot_R=True
    foot_R_ikfk='ik2fk'

    hand_L_ctrls = ikfk_hand_L(picker=False, match=True, force_state=hand_L_ikfk, force_state_key=force_state_key, namespace=namespace) if hand_L else False
    hand_R_ctrls = ikfk_hand_R(picker=False, match=True, force_state=hand_R_ikfk, force_state_key=force_state_key, namespace=namespace) if hand_R else False
    foot_L_ctrls = ikfk_foot_L(picker=False, match=True, force_state=foot_L_ikfk, force_state_key=force_state_key, namespace=namespace) if foot_L else False
    foot_R_ctrls = ikfk_foot_R(picker=False, match=True, force_state=foot_R_ikfk, force_state_key=force_state_key, namespace=namespace) if foot_R else False

    cmds.setKeyframe(hand_L_ctrls) if hand_L_ctrls else False
    cmds.setKeyframe(hand_R_ctrls) if hand_R_ctrls else False
    cmds.setKeyframe(foot_L_ctrls) if foot_L_ctrls else False
    cmds.setKeyframe(foot_R_ctrls) if foot_R_ctrls else False

@bake_with_func
def ik2fk_fk2ik_matchbake(force_state_key=None, namespace=None):
    force_state_key=force_state_key

    # ik2fk
    hand_L=True
    hand_L_ikfk='ik2fk'

    hand_R=True
    hand_R_ikfk='ik2fk'

    foot_L=True
    foot_L_ikfk='ik2fk'

    foot_R=True
    foot_R_ikfk='ik2fk'

    hand_L_ctrls = ikfk_hand_L(picker=False, match=True, force_state=hand_L_ikfk, force_state_key=force_state_key, namespace=namespace) if hand_L else False
    hand_R_ctrls = ikfk_hand_R(picker=False, match=True, force_state=hand_R_ikfk, force_state_key=force_state_key, namespace=namespace) if hand_R else False
    foot_L_ctrls = ikfk_foot_L(picker=False, match=True, force_state=foot_L_ikfk, force_state_key=force_state_key, namespace=namespace) if foot_L else False
    foot_R_ctrls = ikfk_foot_R(picker=False, match=True, force_state=foot_R_ikfk, force_state_key=force_state_key, namespace=namespace) if foot_R else False

    cmds.setKeyframe(hand_L_ctrls) if hand_L_ctrls else False
    cmds.setKeyframe(hand_R_ctrls) if hand_R_ctrls else False
    cmds.setKeyframe(foot_L_ctrls) if foot_L_ctrls else False
    cmds.setKeyframe(foot_R_ctrls) if foot_R_ctrls else False

    # fk2ik
    hand_L=True
    hand_L_ikfk='fk2ik'

    hand_R=True
    hand_R_ikfk='fk2ik'

    foot_L=True
    foot_L_ikfk='fk2ik'

    foot_R=True
    foot_R_ikfk='fk2ik'

    hand_L_ctrls = ikfk_hand_L(picker=False, match=True, force_state=hand_L_ikfk, force_state_key=force_state_key, namespace=namespace) if hand_L else False
    hand_R_ctrls = ikfk_hand_R(picker=False, match=True, force_state=hand_R_ikfk, force_state_key=force_state_key, namespace=namespace) if hand_R else False
    foot_L_ctrls = ikfk_foot_L(picker=False, match=True, force_state=foot_L_ikfk, force_state_key=force_state_key, namespace=namespace) if foot_L else False
    foot_R_ctrls = ikfk_foot_R(picker=False, match=True, force_state=foot_R_ikfk, force_state_key=force_state_key, namespace=namespace) if foot_R else False

    cmds.setKeyframe(hand_L_ctrls) if hand_L_ctrls else False
    cmds.setKeyframe(hand_R_ctrls) if hand_R_ctrls else False
    cmds.setKeyframe(foot_L_ctrls) if foot_L_ctrls else False
    cmds.setKeyframe(foot_R_ctrls) if foot_R_ctrls else False

def fbx_to_rig_and_matchbake(fbx_path=None):
    ref_info = get_reference_info()

    chara_rig = cmds.ls(ref_info[-1]['node'])
    namespace = ':'.join(chara_rig[0].split(':')[0:-1]) + ':'

    fbx_to_rig(fbx_path=fbx_path, namespace=namespace)
    ik2fk_fk2ik_matchbake(force_state_key=True, namespace=namespace)

def all_check_references():
    unLoaded_ref_files = {}
    references = [ref_node for ref_node in cmds.ls(type='reference')]
    for eachnode in references:
        if (not 'sharedReferenceNode' in eachnode
            ):
            ref_files = cmds.referenceQuery(eachnode, filename=True, isLoaded=False)
            unLoaded_ref_files[eachnode] = ref_files

    [cmds.file(ulf_val, lrd="asPrefs", lr=ulf_key) for ulf_key, ulf_val in unLoaded_ref_files.items()]

def run_fbx_to_rig(fbx_files=None, to_rig_file=None, save_path=None, extension='ma', override=True):
    save_path = save_path.replace('\\', '/')
    saved_files = []
    errors = OrderedDict()
    for fbx_path in fbx_files:
        if os.path.isfile(to_rig_file):
            cmds.file(to_rig_file, o=True, f=True)
            all_check_references()
            try:
                fbx_to_rig_and_matchbake(fbx_path)
            except Exception as e:
                errors[fbx_path] = e
                print(traceback.format_exc())
        else:
            print(to_rig_file + ' is not exist')

        if not os.path.isdir(save_path):
            os.makedirs(save_path)

        file_name = save_path + '/' + os.path.splitext(os.path.basename(fbx_path))[0] + '.' + extension

        if override:
            cmds.file(rn=file_name)
            if extension == 'ma':
                file_type = 'mayaAscii'
            if extension == 'mb':
                file_type = 'mayaBinary'

            cmds.file(s=True, f=True, options='v=0', type=file_type)
            saved_files.append(file_name)

    return saved_files, errors

def set_pole_vec(start=None, mid=None, end=None, move=None, obj=None):
    start = cmds.xform(start, q=True, t=True, ws=True)
    mid = cmds.xform(mid, q=True, t=True, ws=True)
    end = cmds.xform(end, q=True, t=True, ws=True)

    startV = om.MVector(start[0] ,start[1],start[2])
    midV = om.MVector(mid[0] ,mid[1],mid[2])
    endV = om.MVector(end[0] ,end[1],end[2])
    startEnd = endV - startV
    startMid = midV - startV
    dotP = startMid * startEnd
    proj = float(dotP) / float(startEnd.length())
    startEndN = startEnd.normal()
    projV = startEndN * proj
    arrowV = startMid - projV
    arrowV*= 0.5
    finalV = arrowV + midV
    cross1 = startEnd ^ startMid
    cross1.normalize()
    cross2 = cross1 ^ arrowV
    cross2.normalize()
    arrowV.normalize()
    matrixV = [arrowV.x , arrowV.y , arrowV.z , 0 ,cross1.x ,cross1.y , cross1.z , 0 ,cross2.x , cross2.y , cross2.z , 0,0,0,0,1]
    matrixM = om.MMatrix()
    om.MScriptUtil.createMatrixFromList(matrixV , matrixM)
    matrixFn = om.MTransformationMatrix(matrixM)
    rot = matrixFn.eulerRotation()

    pvLoc = cmds.spaceLocator(n='poleVecPosLoc')
    cmds.xform(pvLoc[0] , ws =1 , t= (finalV.x , finalV.y ,finalV.z))
    cmds.xform(pvLoc[0] , ws = 1 , rotation = ((rot.x/math.pi*180.0),(rot.y/math.pi*180.0),(rot.z/math.pi*180.0)))
    cmds.select(pvLoc[0])
    cmds.move(move, 0, 0, r=1, os=1, wd=1)

    cmds.matchTransform(obj, pvLoc[0])
    cmds.delete(pvLoc[0])

def quaternionToEuler_no_key(obj=None):
    rot = cmds.xform(obj, q=True, ro=True, os=True)
    rotOrder = cmds.getAttr('{}.rotateOrder'.format(obj))
    euler = om2.MEulerRotation(math.radians(rot[0]), math.radians(rot[1]), math.radians(rot[2]), rotOrder)
    quat = euler.asQuaternion()
    euler = quat.asEulerRotation()
    r = euler.reorder(rotOrder)

    cmds.xform(obj, ro=[math.degrees(r.x), math.degrees(r.y), math.degrees(r.z)], os=True, a=True)

    return math.degrees(r.x), math.degrees(r.y), math.degrees(r.z)


# fbx_files = [
#     'C:/cygames/wiz2/team/3dcg/mot/chr/chr0005_00/export/chr0005_00_wom_run.fbx',
#     'C:/cygames/wiz2/team/3dcg/mot/chr/chr0005_00/export/chr0005_00_wom_jump_IN.fbx'
#     ]
# to_rig_file = 'C:/cygames/wiz2/team/3dcg/mot/chr/chr0005_00/rigReference/chr0005_00_anim.ma'
# save_path = 'C:/Users/CF0990/Documents/maya/scripts/tkgTools/launchers/maya/tkgTools/python/tkgfile/fbxToRig/bookmarks'

# saved_files, errors = run_fbx_to_rig(fbx_files=fbx_files,
#                                        to_rig_file=to_rig_file,
#                                        save_path=save_path,
#                                        extension='ma',
#                                        override=True)
