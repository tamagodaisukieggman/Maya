from maya import cmds, mel

from maya.api import OpenMaya as om
from maya.api import OpenMayaUI as omui
from maya.api import OpenMayaRender as omr

from collections import OrderedDict
import os

def ex_addAttr(node, adat):
    listAttrs = cmds.listAttr(node, ud=1)
    if not listAttrs or not adat in listAttrs:
        cmds.addAttr(node, ln=adat, max=1, dv=0, at='double', min=0, k=1)

def createScaleBwd(weight_node=None, jnt=None, sv=None, weight=None, time=None, loc=None):
    scale_bwd = '{0}_{1}_bwd'.format(jnt, sv)
    if not cmds.objExists(scale_bwd):
        cmds.createNode('blendWeighted', n=scale_bwd, ss=1)

    scale_loc = loc
    if not cmds.objExists(scale_loc):
        cmds.spaceLocator(n=scale_loc)

    default_val = cmds.getAttr('{0}.{1}'.format(jnt, sv))

    init_weight = 'init_weight'
    listAttrs = cmds.listAttr(scale_bwd, ud=1)
    if not listAttrs or not init_weight in listAttrs:
        cmds.addAttr(scale_bwd, ln=init_weight, dv=default_val, at='double', k=1)
        cmds.connectAttr('{0}.{1}'.format(scale_bwd, init_weight), '{0}.i[{1}]'.format(scale_bwd, 0), f=1)

    init_weight_value = 'init_weight_value'
    listAttrs = cmds.listAttr(scale_bwd, ud=1)
    if not listAttrs or not init_weight_value in listAttrs:
        cmds.addAttr(scale_bwd, ln=init_weight_value, dv=1.0, at='double', k=1)
        cmds.connectAttr('{0}.{1}'.format(scale_bwd, init_weight_value), '{0}.w[{1}]'.format(scale_bwd, 0), f=1)


    init_value = cmds.getAttr('{0}.i[{1}]'.format(scale_bwd, 0))

    if 's' in sv:
        if default_val == 1.0:
            default_val = 0.0

        elif default_val != 1.0:
            default_val = default_val - 1.0

    if 't' in sv:
        default_val = default_val - init_value

    cmds.addAttr(scale_bwd, ln="{0}_{1}".format(weight, sv), dv=default_val, at='double', k=1)

    cmds.connectAttr('{0}.{1}'.format(weight_node, weight), '{0}.w[{1}]'.format(scale_bwd, time+1), f=1)
    cmds.connectAttr('{0}.{1}'.format(scale_bwd, "{0}_{1}".format(weight, sv)), '{0}.i[{1}]'.format(scale_bwd, time+1), f=1)

    # cmds.connectAttr('{0}.output'.format(scale_bwd), '{0}.{1}'.format(jnt, sv), f=1)
    cmds.setAttr('{0}.{1}'.format(scale_loc, sv), default_val)
    cmds.connectAttr('{0}.{1}'.format(scale_loc, sv), '{0}.{1}'.format(scale_bwd, "{0}_{1}".format(weight, sv)), f=1)

    # scale_bwds_set
    scale_bwds_set = 'scale_bwds_set'
    if not cmds.objExists(scale_bwds_set):
        cmds.sets(n=scale_bwds_set, em=1)

    cmds.sets(scale_bwd, add=scale_bwds_set)


# def set_multiAttrs(time, target, joints, mabn, connectWeightNode=None, mode='i', head='head_head'):
#     # transform_all_loc_grp
#     transform_all_loc_grp = 'transform_all_loc_grp'
#     if not cmds.objExists(transform_all_loc_grp):
#         cmds.createNode('transform', n=transform_all_loc_grp, ss=1)

#     children = cmds.listRelatives(head, c=1)
#     if not children or not transform_all_loc_grp in children:
#         cmds.parent(transform_all_loc_grp, head)
#         cmds.xform(transform_all_loc_grp, t=[0, 0, 0], ro=[0, 0, 0])

#     for i, jnt in enumerate(joints):
#         if mode == 'i':

#             # transform_loc_grp
#             transform_loc_grp = '{0}_transform_loc_grp'.format(target)
#             if not cmds.objExists(transform_loc_grp):
#                 cmds.createNode('transform', n=transform_loc_grp, ss=1)

#             children = cmds.listRelatives(transform_all_loc_grp, c=1)
#             if not children or not transform_loc_grp in children:
#                 cmds.parent(transform_loc_grp, transform_all_loc_grp)
#                 cmds.xform(transform_loc_grp, t=[0, 0, 0], ro=[0, 0, 0])

#             cmds.setAttr("{0}.v".format(transform_loc_grp), 0)

#             # transform loc
#             transform_loc = '{0}_{1}_transform_loc'.format(target, jnt)
#             if not cmds.objExists(transform_loc):
#                 cmds.spaceLocator(n=transform_loc)

#             children = cmds.listRelatives(transform_all_loc_grp, c=1)
#             if not children or not transform_loc in children:
#                 cmds.parent(transform_loc, transform_loc_grp)

#             cmds.matchTransform(transform_loc, jnt)

#             cmds.connectAttr('{0}.tx'.format(transform_loc), '{0}.iv[{1}].i[{2}].itrs[0].{3}tx'.format(mabn, i, time, mode), f=1)
#             cmds.connectAttr('{0}.ty'.format(transform_loc), '{0}.iv[{1}].i[{2}].itrs[0].{3}ty'.format(mabn, i, time, mode), f=1)
#             cmds.connectAttr('{0}.tz'.format(transform_loc), '{0}.iv[{1}].i[{2}].itrs[0].{3}tz'.format(mabn, i, time, mode), f=1)

#             cmds.connectAttr('{0}.rx'.format(transform_loc), '{0}.iv[{1}].i[{2}].itrs[0].{3}rx'.format(mabn, i, time, mode), f=1)
#             cmds.connectAttr('{0}.ry'.format(transform_loc), '{0}.iv[{1}].i[{2}].itrs[0].{3}ry'.format(mabn, i, time, mode), f=1)
#             cmds.connectAttr('{0}.rz'.format(transform_loc), '{0}.iv[{1}].i[{2}].itrs[0].{3}rz'.format(mabn, i, time, mode), f=1)

#             cmds.connectAttr('{0}.sx'.format(jnt), '{0}.iv[{1}].i[{2}].itrs[0].{3}sx'.format(mabn, i, time, mode), f=1)
#             cmds.connectAttr('{0}.sy'.format(jnt), '{0}.iv[{1}].i[{2}].itrs[0].{3}sy'.format(mabn, i, time, mode), f=1)
#             cmds.connectAttr('{0}.sz'.format(jnt), '{0}.iv[{1}].i[{2}].itrs[0].{3}sz'.format(mabn, i, time, mode), f=1)

#             #
#             cmds.disconnectAttr('{0}.sx'.format(jnt), '{0}.iv[{1}].i[{2}].itrs[0].{3}sx'.format(mabn, i, time, mode))
#             cmds.disconnectAttr('{0}.sy'.format(jnt), '{0}.iv[{1}].i[{2}].itrs[0].{3}sy'.format(mabn, i, time, mode))
#             cmds.disconnectAttr('{0}.sz'.format(jnt), '{0}.iv[{1}].i[{2}].itrs[0].{3}sz'.format(mabn, i, time, mode))

#         if connectWeightNode:
#             ex_addAttr(connectWeightNode, '{0}'.format(target))
#             cmds.connectAttr('{0}.{1}'.format(connectWeightNode, target), '{0}.iv[{1}].i[{2}].itrs[0].itw'.format(mabn, i, time), f=1)
#             createScaleBwd(connectWeightNode, jnt, sv='sx', weight='{0}'.format(target), time=time, loc=transform_loc)
#             createScaleBwd(connectWeightNode, jnt, sv='sy', weight='{0}'.format(target), time=time, loc=transform_loc)
#             createScaleBwd(connectWeightNode, jnt, sv='sz', weight='{0}'.format(target), time=time, loc=transform_loc)


def set_multiAttrs(time, target, joints, mabn, connectWeightNode=None, mode='i', head='head_head'):
    # transform_all_loc_grp
    transform_all_loc_grp = 'transform_all_loc_grp'
    if not cmds.objExists(transform_all_loc_grp):
        cmds.createNode('transform', n=transform_all_loc_grp, ss=1)

    children = cmds.listRelatives(head, c=1)
    if not children or not transform_all_loc_grp in children:
        cmds.parent(transform_all_loc_grp, head)
        cmds.xform(transform_all_loc_grp, t=[0, 0, 0], ro=[0, 0, 0])

    for i, jnt in enumerate(joints):
        if mode == 'i':

            # transform_loc_grp
            transform_loc_grp = '{0}_transform_loc_grp'.format(target)
            if not cmds.objExists(transform_loc_grp):
                cmds.createNode('transform', n=transform_loc_grp, ss=1)

            children = cmds.listRelatives(transform_all_loc_grp, c=1)
            if not children or not transform_loc_grp in children:
                cmds.parent(transform_loc_grp, transform_all_loc_grp)
                cmds.xform(transform_loc_grp, t=[0, 0, 0], ro=[0, 0, 0])

            cmds.setAttr("{0}.v".format(transform_loc_grp), 0)

            # transform loc
            transform_loc = '{0}_{1}_transform_loc'.format(target, jnt)
            if not cmds.objExists(transform_loc):
                cmds.spaceLocator(n=transform_loc)

            children = cmds.listRelatives(transform_all_loc_grp, c=1)
            if not children or not transform_loc in children:
                cmds.parent(transform_loc, transform_loc_grp)

            cmds.matchTransform(transform_loc, jnt)

            # cmds.connectAttr('{0}.tx'.format(transform_loc), '{0}.iv[{1}].i[{2}].itrs[0].{3}tx'.format(mabn, i, time, mode), f=1)
            # cmds.connectAttr('{0}.ty'.format(transform_loc), '{0}.iv[{1}].i[{2}].itrs[0].{3}ty'.format(mabn, i, time, mode), f=1)
            # cmds.connectAttr('{0}.tz'.format(transform_loc), '{0}.iv[{1}].i[{2}].itrs[0].{3}tz'.format(mabn, i, time, mode), f=1)

            # cmds.connectAttr('{0}.rx'.format(transform_loc), '{0}.iv[{1}].i[{2}].itrs[0].{3}rx'.format(mabn, i, time, mode), f=1)
            # cmds.connectAttr('{0}.ry'.format(transform_loc), '{0}.iv[{1}].i[{2}].itrs[0].{3}ry'.format(mabn, i, time, mode), f=1)
            # cmds.connectAttr('{0}.rz'.format(transform_loc), '{0}.iv[{1}].i[{2}].itrs[0].{3}rz'.format(mabn, i, time, mode), f=1)

            # cmds.connectAttr('{0}.sx'.format(jnt), '{0}.iv[{1}].i[{2}].itrs[0].{3}sx'.format(mabn, i, time, mode), f=1)
            # cmds.connectAttr('{0}.sy'.format(jnt), '{0}.iv[{1}].i[{2}].itrs[0].{3}sy'.format(mabn, i, time, mode), f=1)
            # cmds.connectAttr('{0}.sz'.format(jnt), '{0}.iv[{1}].i[{2}].itrs[0].{3}sz'.format(mabn, i, time, mode), f=1)

            # #
            # cmds.disconnectAttr('{0}.sx'.format(jnt), '{0}.iv[{1}].i[{2}].itrs[0].{3}sx'.format(mabn, i, time, mode))
            # cmds.disconnectAttr('{0}.sy'.format(jnt), '{0}.iv[{1}].i[{2}].itrs[0].{3}sy'.format(mabn, i, time, mode))
            # cmds.disconnectAttr('{0}.sz'.format(jnt), '{0}.iv[{1}].i[{2}].itrs[0].{3}sz'.format(mabn, i, time, mode))

        if connectWeightNode:
            ex_addAttr(connectWeightNode, '{0}'.format(target))
            # cmds.connectAttr('{0}.{1}'.format(connectWeightNode, target), '{0}.iv[{1}].i[{2}].itrs[0].itw'.format(mabn, i, time), f=1)

            createScaleBwd(connectWeightNode, jnt, sv='tx', weight='{0}'.format(target), time=time, loc=transform_loc)
            createScaleBwd(connectWeightNode, jnt, sv='ty', weight='{0}'.format(target), time=time, loc=transform_loc)
            createScaleBwd(connectWeightNode, jnt, sv='tz', weight='{0}'.format(target), time=time, loc=transform_loc)

            createScaleBwd(connectWeightNode, jnt, sv='rx', weight='{0}'.format(target), time=time, loc=transform_loc)
            createScaleBwd(connectWeightNode, jnt, sv='ry', weight='{0}'.format(target), time=time, loc=transform_loc)
            createScaleBwd(connectWeightNode, jnt, sv='rz', weight='{0}'.format(target), time=time, loc=transform_loc)

            createScaleBwd(connectWeightNode, jnt, sv='sx', weight='{0}'.format(target), time=time, loc=transform_loc)
            createScaleBwd(connectWeightNode, jnt, sv='sy', weight='{0}'.format(target), time=time, loc=transform_loc)
            createScaleBwd(connectWeightNode, jnt, sv='sz', weight='{0}'.format(target), time=time, loc=transform_loc)



def set_multiAttrs_init(joints_num, time, mabn, ost, osr, rss, mode='int'):

    if mode == 'int':
        cmds.setAttr('{0}.iv[{1}].i[{2}].itrs[0].{3}tx'.format(mabn, joints_num, time, mode), ost[0])
        cmds.setAttr('{0}.iv[{1}].i[{2}].itrs[0].{3}ty'.format(mabn, joints_num, time, mode), ost[1])
        cmds.setAttr('{0}.iv[{1}].i[{2}].itrs[0].{3}tz'.format(mabn, joints_num, time, mode), ost[2])

        cmds.setAttr('{0}.iv[{1}].i[{2}].itrs[0].{3}rx'.format(mabn, joints_num, time, mode), osr[0])
        cmds.setAttr('{0}.iv[{1}].i[{2}].itrs[0].{3}ry'.format(mabn, joints_num, time, mode), osr[1])
        cmds.setAttr('{0}.iv[{1}].i[{2}].itrs[0].{3}rz'.format(mabn, joints_num, time, mode), osr[2])

        cmds.setAttr('{0}.iv[{1}].i[{2}].itrs[0].{3}sx'.format(mabn, joints_num, time, mode), rss[0])
        cmds.setAttr('{0}.iv[{1}].i[{2}].itrs[0].{3}sy'.format(mabn, joints_num, time, mode), rss[1])
        cmds.setAttr('{0}.iv[{1}].i[{2}].itrs[0].{3}sz'.format(mabn, joints_num, time, mode), rss[2])

def check_exists_joints(target_joints_grp=None):
    for types, joints in target_joints_grp.items():
        exist_joints = [jnt for jnt in joints if cmds.objExists(jnt)]
        target_joints_grp[types] = exist_joints

    return target_joints_grp

# Currentframe 0
cmds.playbackOptions(ast=0, aet=14, min=0, max=14)
cmds.currentTime(0)

# facial_proxys
dup_neck = cmds.duplicate('neck_head', n='facial_proxy_neck_head')
dup_head = cmds.listRelatives(dup_neck[0], c=1, f=1)
dup_new_head_name = 'facial_proxy_{0}'.format(dup_head[0].split('|')[-1])
cmds.rename(dup_head[0], dup_new_head_name)
children = cmds.listRelatives(dup_new_head_name, c=1, f=1)
for obj in children:
    obj_new_name = 'facial_proxy_{0}'.format(obj.split('|')[-1])
    cmds.rename(obj, obj_new_name)


set_joints = [u'nose_top',
             u'chin',
             u'jaw',
             u'tooth_top',
             u'tooth_bottom',
             u'L_A_cheek',
             u'L_B_cheek',
             u'L_C_cheek',
             u'R_A_cheek',
             u'R_B_cheek',
             u'R_C_cheek',
             u'L_mouth',
             u'R_mouth',
             u'L_A_mouth_top',
             u'L_B_mouth_top',
             u'R_A_mouth_top',
             u'R_B_mouth_top',
             u'mouth_top',
             u'L_A_mouth_bottom',
             u'L_B_mouth_bottom',
             u'R_A_mouth_bottom',
             u'R_B_mouth_bottom',
             u'mouth_bottom',
             u'L_A_eyebrow',
             u'L_B_eyebrow',
             u'L_C_eyebrow',
             u'L_A_eye_top',
             u'L_B_eye_top',
             u'L_C_eye_top',
             u'L_D_eye_top',
             u'L_E_eye_top',
             u'L_F_eye_top',
             u'L_A_eye_bottom',
             u'L_B_eye_bottom',
             u'L_C_eye_bottom',
             u'L_D_eye_bottom',
             u'L_E_eye_bottom',
             u'R_A_eyebrow',
             u'R_B_eyebrow',
             u'R_C_eyebrow',
             u'R_A_eye_top',
             u'R_B_eye_top',
             u'R_C_eye_top',
             u'R_D_eye_top',
             u'R_E_eye_top',
             u'R_F_eye_top',
             u'R_A_eye_bottom',
             u'R_B_eye_bottom',
             u'R_C_eye_bottom',
             u'R_D_eye_bottom',
             u'R_E_eye_bottom']


# set inputs

targets = {'0':'bind',
           '1':'default',
           '2':'fine',
           '3':'angry',
           '4':'sad',
           '5':'serious',
           '6':'damage',
           '7':'surprise',
           '8':'eye_close_01',
           '9':'eye_close_02',
           '10':'a',
           '11':'i',
           '12':'u',
           '13':'e',
           '14':'o',
           }

brows_grp = {'L_brows':[u'L_A_eyebrow', u'L_B_eyebrow', u'L_C_eyebrow'],
             'R_brows':[u'R_A_eyebrow', u'R_B_eyebrow', u'R_C_eyebrow'],}

eyes_grp = {'L_eyes':[u'L_A_eye_bottom',
                      u'L_A_eye_top',
                      u'L_B_eye_bottom',
                      u'L_B_eye_top',
                      u'L_C_eye_bottom',
                      u'L_C_eye_top',
                      u'L_D_eye_bottom',
                      u'L_D_eye_top',
                      u'L_E_eye_bottom',
                      u'L_E_eye_top',
                      u'L_F_eye_top',
                      u'L_G_eye_top',
                      u'L_A_line',
                      u'L_B_line',
                      u'L_C_line',
                      u'L_line_01',
                      u'L_line_02',
                      u'L_line_03',
                      u'L_A_eyelid',
                      u'L_B_eyelid',
                      u'L_C_eyelid',
                      u'L_line',
                      u'L_A_line_01',
                      u'L_A_line_02',
                      u'L_A_line_03',
                      u'L_B_line_01',
                      u'L_B_line_02',
                      u'L_B_line_03'],
            'R_eyes':[u'R_A_eye_bottom',
                      u'R_A_eye_top',
                      u'R_B_eye_bottom',
                      u'R_B_eye_top',
                      u'R_C_eye_bottom',
                      u'R_C_eye_top',
                      u'R_D_eye_bottom',
                      u'R_D_eye_top',
                      u'R_E_eye_bottom',
                      u'R_E_eye_top',
                      u'R_F_eye_top',
                      u'R_G_eye_top',
                      u'R_A_line',
                      u'R_B_line',
                      u'R_C_line',
                      u'R_line_01',
                      u'R_line_02',
                      u'R_line_03',
                      u'R_A_eyelid',
                      u'R_B_eyelid',
                      u'R_C_eyelid',
                      u'R_line',
                      u'R_A_line_01',
                      u'R_A_line_02',
                      u'R_A_line_03',
                      u'R_B_line_01',
                      u'R_B_line_02',
                      u'R_B_line_03']}

mouth_grp = {'C_mouth':[u'L_A_cheek',
                         u'L_A_mouth_bottom',
                         u'L_A_mouth_top',
                         u'L_B_cheek',
                         u'L_B_mouth_bottom',
                         u'L_B_mouth_top',
                         u'L_C_cheek',
                         u'L_mouth',
                         u'R_A_cheek',
                         u'R_A_mouth_bottom',
                         u'R_A_mouth_top',
                         u'R_B_cheek',
                         u'R_B_mouth_bottom',
                         u'R_B_mouth_top',
                         u'R_C_cheek',
                         u'R_mouth',
                         u'chin',
                         u'jaw',
                         u'mouth_bottom',
                         u'mouth_top',
                         u'nose_top']}

tooth_grp = {'C_tooth':[u'tooth_bottom', u'tooth_top']}

face_grps = [check_exists_joints(brows_grp), check_exists_joints(eyes_grp), check_exists_joints(mouth_grp), check_exists_joints(tooth_grp)]

try:
    cmds.refresh(su=1)
    start = cmds.playbackOptions(q=1, min=1)
    end = cmds.playbackOptions(q=1, max=1)

    autokey_sts = cmds.autoKeyframe(q=1, st=1)
    cmds.autoKeyframe(e=1, st=0)

    for i in range(int((end - start))+1):
        # print(i)
        cmds.currentTime(i)
        for f_grp in face_grps:
            for type_base, type_joints in f_grp.items():
                mabn = '{0}_transform_mabn'.format(type_base)
                if not cmds.objExists(mabn):
                    cmds.createNode('tkgmultiattrblendnode', n=mabn, ss=1)

                weight_node = '{0}_weight_node'.format(type_base)
                if not cmds.objExists(weight_node):
                    cmds.createNode('transform', n=weight_node, ss=1)

                set_multiAttrs(i, targets[str(i)], type_joints, mabn, weight_node, mode='i')

    cmds.currentTime(start)
    cmds.autoKeyframe(e=1, st=autokey_sts)
    cmds.refresh(su=0)
except Exception as e:
    print(e)
    cmds.refresh(su=0)



# set init
# try:
#     cmds.refresh(su=1)
#     start = cmds.playbackOptions(q=1, min=1)
#     end = cmds.playbackOptions(q=1, max=1)

#     autokey_sts = cmds.autoKeyframe(q=1, st=1)
#     cmds.autoKeyframe(e=1, st=0)

#     for f_grp in face_grps:
#         for type_base, type_joints in f_grp.items():
#             mabn = '{0}_transform_mabn'.format(type_base)
#             for i, jnt in enumerate(type_joints):
#                 cmds.currentTime(start)
#                 ost = cmds.xform(jnt, q=1, t=1, os=1)
#                 osr = cmds.xform(jnt, q=1, ro=1, os=1)
#                 rss = cmds.xform(jnt, q=1, s=1, r=1)
#                 for j in range(int((end - start))+1):
#                     # print(i)
#                     cmds.currentTime(j)

#                     set_multiAttrs_init(i, j, mabn, ost, osr, rss, mode='int')

#     cmds.currentTime(start)
#     cmds.autoKeyframe(e=1, st=autokey_sts)

#     cmds.refresh(su=0)
# except Exception as e:
#     cmds.refresh(su=0)


# # Connect joints
# for f_grp in face_grps:
#     for type_base, type_joints in f_grp.items():
#         mabn = '{0}_transform_mabn'.format(type_base)
#         for i, jnt in enumerate(type_joints):
#             cmds.connectAttr('{0}.translate'.format(jnt), '{0}.inputValue[{1}].baseTranslate'.format(mabn, i), f=1)
#             cmds.connectAttr('{0}.rotate'.format(jnt), '{0}.inputValue[{1}].baseRotate'.format(mabn, i), f=1)
#             # cmds.connectAttr('{0}.scale'.format(jnt), '{0}.inputValue[{1}].baseScale'.format(mabn, i), f=1)

#             cmds.connectAttr('{0}.outputTransforms[{1}].outputTranslate'.format(mabn, i), 'facial_proxy_{0}.translate'.format(jnt), f=1)
#             cmds.connectAttr('{0}.outputTransforms[{1}].outputRotate'.format(mabn, i), 'facial_proxy_{0}.rotate'.format(jnt), f=1)
#             # cmds.connectAttr('{0}.outputTransforms[{1}].outputScale'.format(mabn, i), 'facial_proxy_{0}.scale'.format(jnt), f=1)

cmds.select('scale_bwds_set', r=1, ne=1)
scale_bwds = cmds.pickWalk(d='down')

for bwd in scale_bwds:
    ss = list(bwd)
    ss[-7:] = ""
    jnt = "".join(ss)
    if 'tx' in bwd:
        cmds.connectAttr('{0}.output'.format(bwd), 'facial_proxy_{0}.tx'.format(jnt), f=1)
    elif 'ty' in bwd:
        cmds.connectAttr('{0}.output'.format(bwd), 'facial_proxy_{0}.ty'.format(jnt), f=1)
    elif 'tz' in bwd:
        cmds.connectAttr('{0}.output'.format(bwd), 'facial_proxy_{0}.tz'.format(jnt), f=1)

    elif 'rx' in bwd:
        cmds.connectAttr('{0}.output'.format(bwd), 'facial_proxy_{0}.rx'.format(jnt), f=1)
    elif 'ry' in bwd:
        cmds.connectAttr('{0}.output'.format(bwd), 'facial_proxy_{0}.ry'.format(jnt), f=1)
    elif 'rz' in bwd:
        cmds.connectAttr('{0}.output'.format(bwd), 'facial_proxy_{0}.rz'.format(jnt), f=1)

    elif 'sx' in bwd:
        cmds.connectAttr('{0}.output'.format(bwd), 'facial_proxy_{0}.sx'.format(jnt), f=1)
    elif 'sy' in bwd:
        cmds.connectAttr('{0}.output'.format(bwd), 'facial_proxy_{0}.sy'.format(jnt), f=1)
    elif 'sz' in bwd:
        cmds.connectAttr('{0}.output'.format(bwd), 'facial_proxy_{0}.sz'.format(jnt), f=1)

cmds.delete('scale_bwds_set')

# delete joints
set_del_joints = cmds.ls('neck_head', dag=1, type='joint')
no_deletes = ['neck_head', 'head_head']
for del_j in set_del_joints:
    if cmds.objExists(del_j):
        if cmds.objectType(del_j) == 'joint':
            if not del_j in no_deletes:
                cmds.delete(del_j)

for rename_obj in no_deletes:
    cmds.rename(rename_obj, rename_obj.replace(rename_obj, 'transform_{0}'.format(rename_obj)))

# parent targets nodes
targets_all_grp = 'targets_all_grp'
if not cmds.objExists(targets_all_grp):
    cmds.createNode('transform', n=targets_all_grp, ss=1)

for f_grp in face_grps:
    for type_base, type_joints in f_grp.items():
        weight_node = '{0}_weight_node'.format(type_base)
        if not cmds.objExists(weight_node):
            cmds.createNode('transform', n=weight_node, ss=1)

        cmds.parent(weight_node, targets_all_grp)

facial_rig_grp = 'facial_rig_grp'
if not cmds.objExists(facial_rig_grp):
    cmds.createNode('transform', n=facial_rig_grp, ss=1)

if cmds.objExists('transform_neck_head'):
    cmds.parent('transform_neck_head', facial_rig_grp)

if cmds.objExists('facial_proxy_neck_head'):
    cmds.parent('facial_proxy_neck_head', facial_rig_grp)

if cmds.objExists('targets_all_grp'):
    cmds.parent('targets_all_grp', facial_rig_grp)


# after reference connections

# from maya import cmds, mel

# facial_proxies = cmds.ls(os=1, type='joint')
# for jnt in facial_proxies:
#     cmds.scaleConstraint(jnt, '{0}_CtrlG'.format(jnt.replace('targets:facial_proxy_', '')))
#     cmds.scaleConstraint(jnt, '{0}_CtrlG'.format(jnt.replace('targets:facial_proxy_', '')))

# targets_node = [u'targets:L_brows_weight_node',
#  u'targets:R_brows_weight_node',
#  u'targets:R_eyes_weight_node',
#  u'targets:L_eyes_weight_node',
#  u'targets:C_mouth_weight_node',
#  u'targets:C_tooth_weight_node']

# listAttrs = cmds.listAttr('face_pattern', ud=1)
# for at in listAttrs:
#     bwd = '{0}_blend_bwd'.format(at)
#     if not cmds.objExists(bwd):
#         cmds.createNode('blendWeighted', n=bwd, ss=1)

#     cmds.addAttr(bwd, ln="{0}_weight".format(at), dv=1.0, min=0.0, max=1.0, at='double')
#     cmds.connectAttr('{0}.{1}'.format(bwd, "{0}_weight".format(at)), '{0}.i[0]'.format(bwd), f=1)
#     cmds.connectAttr('{0}.{1}'.format('face_pattern', at), '{0}.w[0]'.format(bwd), f=1)

# const proxy to chara joints
# from maya import cmds, mel
#
# facial_chara_joints = cmds.ls('head_model:neck_head', dag=1, type='joint')
# for jnt in facial_chara_joints:
#     try:
#         if cmds.objExists(jnt) and cmds.objExists(jnt.replace('head_model:', 'dummy_')):
#             cmds.pointConstraint(jnt.replace('head_model:', 'dummy_'), jnt, mo=1)
#         else:
#             cmds.pointConstraint(jnt.replace('head_model:', 'targets:facial_proxy_'), jnt, mo=1)
#     except:
#         pass
#     try:
#         if cmds.objExists(jnt) and cmds.objExists(jnt.replace('head_model:', 'dummy_')):
#             cmds.orientConstraint(jnt.replace('head_model:', 'dummy_'), jnt, mo=1)
#         else:
#             cmds.orientConstraint(jnt.replace('head_model:', 'targets:facial_proxy_'), jnt, mo=1)
#     except:
#         pass
#     try:
#         if cmds.objExists(jnt) and cmds.objExists(jnt.replace('head_model:', 'dummy_')):
#             cmds.scaleConstraint(jnt.replace('head_model:', 'dummy_'), jnt, mo=1)
#         else:
#             cmds.scaleConstraint(jnt.replace('head_model:', 'targets:facial_proxy_'), jnt, mo=1)
#     except:
#         pass
