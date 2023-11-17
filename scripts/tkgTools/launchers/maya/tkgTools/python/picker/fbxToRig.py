# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
import maya.OpenMayaAnim as oma
import maya.OpenMayaUI as omui
import maya.api.OpenMaya as om2
import maya.api.OpenMayaAnim as oma2

import re
import traceback

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

        cmds.joint(self.ordered_jnts[0], e=True, apa=True, ch=True)

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
