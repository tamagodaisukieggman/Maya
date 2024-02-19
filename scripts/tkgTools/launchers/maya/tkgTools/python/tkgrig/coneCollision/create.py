# -*- coding: utf-8 -*-
from imp import reload
from maya import cmds

import tkgrig.coneCollision.swingTwist as swingTwist
reload(swingTwist)

def mr_poseReader(name='poseReader', coneAngle=90):
    '''
    Run mr_poseReader() to get a pose reader.
    Change name or coneAngle if you need to.
    ex: mr_poseReader('myPoseReader', 45)
    '''

    baseLoc = cmds.spaceLocator(n=name + '_base')[0]
    poseLoc = cmds.spaceLocator(n=name + '_pose')[0]
    targetLoc = cmds.spaceLocator(n=name + '_target')[0]
    angleNode = cmds.createNode('angleBetween', n=name + '_angle', ss=True)
    multNode = cmds.createNode('multiplyDivide', n=name + '_divideAngle', ss=True)
    remapNode = cmds.createNode('remapValue', n=name + '_remapValue', ss=True)
    poseSwingTwistJnt = cmds.createNode('joint', n=name + '_pose_swingTwist_jnt', ss=True)
    swingTwistMmx = cmds.createNode('multMatrix', n=name + '_swingTwist_multMatrix', ss=True)
    swingTwistDcmx = cmds.createNode('decomposeMatrix', n=name + '_swingTwist_decomposeMatrix', ss=True)

    cmds.parent(poseSwingTwistJnt, targetLoc, baseLoc)
    cmds.parent(poseLoc, poseSwingTwistJnt)

    cmds.setAttr(multNode + '.input2X', 0.5)
    cmds.move(0, 2, 0, targetLoc)
    cmds.move(2, 0, 0, poseLoc)

    #
    cmds.connectAttr(poseLoc + '.matrix', swingTwistMmx + '.matrixIn[0]')
    cmds.connectAttr(poseSwingTwistJnt + '.matrix', swingTwistMmx + '.matrixIn[1]')
    cmds.connectAttr(swingTwistMmx + '.matrixSum', swingTwistDcmx + '.inputMatrix')
    cmds.connectAttr(swingTwistDcmx + '.outputTranslate', angleNode + '.vector1')

    # cmds.connectAttr(poseLoc + '.translate', angleNode + '.vector1')

    #

    cmds.connectAttr(targetLoc + '.translate', angleNode + '.vector2')
    cmds.connectAttr(angleNode + '.angle', remapNode + '.inputValue')

    cmds.addAttr(baseLoc, ln='coneAngle', dv=coneAngle, k=1)
    cmds.connectAttr(baseLoc + '.coneAngle', multNode + '.input1X')
    cmds.connectAttr(multNode + '.outputX', remapNode + '.inputMin')

    cmds.addAttr(baseLoc, ln='outputWeight', at='float', k=1)
    cmds.connectAttr(remapNode + '.outValue', baseLoc + '.outputWeight')

    return baseLoc, poseLoc, targetLoc, poseSwingTwistJnt

def get_mid_point(pos1, pos2, percentage=0.5):
    mid_point = [pos1[0] + (pos2[0] - pos1[0]) * percentage,
                 pos1[1] + (pos2[1] - pos1[1]) * percentage,
                 pos1[2] + (pos2[2] - pos1[2]) * percentage]
    return mid_point

def addAttr_compound(node=None, ln=None, at='compound', children_attributes=None, keyable=True, lock=False, channel_box=True):
    list_attrs = cmds.listAttr(node) or list()
    cmds.addAttr(node, ln=ln, at=at, nc=len(children_attributes), k=keyable) if list_attrs else False

    compound_attrs = [attr for attr in children_attributes]
    [cmds.addAttr(node, ln=attr, at='float', k=keyable, parent=ln) for attr in compound_attrs]
    [cmds.setAttr('{}.{}'.format(node, attr), lock=lock, channelBox=channel_box) for attr in compound_attrs]


def create_coneCollision_rig(joints=None,
                              angle_base_obj=None,
                              angle_pose_obj=None,
                              center_pose_obj=None,
                              default_coneAngle=180,
                              default_target_aim_vec=[0,0,1],
                              default_target_up_vec=[0,1,0],
                              angle_base_obj_twist_axis='y'):
    # skirt joints
    # joints = cmds.ls(os=True)
    if not joints:
        joints = cmds.ls(os=True)

    jnt_pose_reader = angle_base_obj+joints[0]+'_poseReader'
    base_loc, pose_loc, target_loc, pose_swingTwist_jnt = mr_poseReader(jnt_pose_reader)

    cmds.setAttr(base_loc+'.coneAngle', default_coneAngle)

    # add aim vec
    addAttr_compound(node=base_loc,
                     ln='aimVector',
                     at='compound',
                     children_attributes=['aimVectorX', 'aimVectorY', 'aimVectorZ'],
                     keyable=True,
                     lock=False,
                     channel_box=True)

    cmds.setAttr(base_loc+'.aimVector', *default_target_aim_vec)

    # add up vec
    addAttr_compound(node=base_loc,
                     ln='upVector',
                     at='compound',
                     children_attributes=['upVectorX', 'upVectorY', 'upVectorZ'],
                     keyable=True,
                     lock=False,
                     channel_box=True)

    cmds.setAttr(base_loc+'.upVector', *default_target_up_vec)

    # add intense
    addAttr_compound(node=base_loc,
                     ln='intense',
                     at='compound',
                     children_attributes=['intenseX', 'intenseY', 'intenseZ'],
                     keyable=True,
                     lock=False,
                     channel_box=True)

    cmds.setAttr(base_loc+'.intense', *[1,1,1])

    cmds.matchTransform(base_loc, angle_base_obj, pos=True, rot=True, scl=False)
    cmds.matchTransform(pose_swingTwist_jnt, angle_base_obj, pos=True, rot=True, scl=False)

    angle_base_obj_twist_axis_dict = {
        'x':0,
        'y':1,
        'z':2
    }

    swingTwist.create_swing_twist(angle_base_obj,
                                   pose_swingTwist_jnt,
                                   twist_weight=0.0,
                                   swing_weight=1.0,
                                   twist_axis=angle_base_obj_twist_axis_dict[angle_base_obj_twist_axis],
                                   connect_rotate=True)

    cmds.parentConstraint(center_pose_obj, base_loc, w=True, mo=True)

    pos1 = cmds.xform(angle_base_obj, q=True, t=True, ws=True)
    pos2 = cmds.xform(angle_pose_obj, q=True, t=True, ws=True)
    mid_point = get_mid_point(pos1, pos2, percentage=2)

    cmds.xform(pose_loc, t=mid_point, ws=True, a=True)
    # pose_po_con = cmds.parentConstraint(angle_base_obj, pose_loc, w=True, mo=True)[0]

    # set target loc
    pos1 = cmds.xform(center_pose_obj, q=True, t=True, ws=True)
    pos2 = cmds.xform(joints[0], q=True, t=True, ws=True)
    mid_point = get_mid_point(pos1, pos2, percentage=2)

    jnt_wt = cmds.xform(joints[0], q=True, t=True, ws=True)
    cmds.xform(target_loc, t=[mid_point[0], jnt_wt[1], mid_point[2]], ws=True, a=True)

    for i, jnt in enumerate(joints):
        connected_pbs = cmds.listConnections(jnt, s=True, scn=True, type='pairBlend') or list()
        connected_pbs = list(set(connected_pbs))

        laytex = jnt+'_blend_layeredTexture'
        if connected_pbs:
            if not cmds.objExists(laytex):
                cmds.createNode('layeredTexture', n=laytex, ss=True)
            else:
                cmds.delete(laytex)
                cmds.createNode('layeredTexture', n=laytex, ss=True)

        pb = cmds.createNode('pairBlend', ss=True)
        md = cmds.createNode('multiplyDivide', ss=True)
        chain_md = cmds.createNode('multiplyDivide', ss=True)
        chain_pma = cmds.createNode('plusMinusAverage', ss=True)

        cmds.setAttr(pb+'.rotInterpolation', 1)
        cmds.setAttr(pb+'.inRotate1',
                     *cmds.getAttr(jnt+'.r')[0])

        chain_num = '{}'.format(str(i).zfill(2))
        chain_at = 'chain{}'.format(chain_num)
        if not cmds.objExists(base_loc+'.{}'.format(chain_at)):
            cmds.addAttr(base_loc, ln=chain_at, at='float', k=True)
        cmds.setAttr(base_loc+'.{}'.format(chain_at), e=True, l=True)

        # add part intense
        addAttr_compound(node=base_loc,
                         ln='intensePart{}'.format(chain_num),
                         at='compound',
                         children_attributes=['intensePart{}X'.format(chain_num),
                                              'intensePart{}Y'.format(chain_num),
                                              'intensePart{}Z'.format(chain_num)],
                         keyable=True,
                         lock=False,
                         channel_box=True)

        cmds.setAttr(base_loc+'.intensePart{}'.format(chain_num), *[1,1,1])

        # add part offset
        addAttr_compound(node=base_loc,
                         ln='offsetPart{}'.format(chain_num),
                         at='compound',
                         children_attributes=['offsetPart{}X'.format(chain_num),
                                              'offsetPart{}Y'.format(chain_num),
                                              'offsetPart{}Z'.format(chain_num)],
                         keyable=True,
                         lock=False,
                         channel_box=True)

        if i == len(joints)-1:
            aim_base = joints[i-1]
            aim_pose = jnt
        else:
            aim_base = jnt
            aim_pose = joints[i+1]

        pos1 = cmds.xform(aim_base, q=True, t=True, ws=True)
        pos2 = cmds.xform(aim_pose, q=True, t=True, ws=True)
        mid_point = get_mid_point(pos1, pos2, percentage=10)

        jnt_aim_loc = cmds.spaceLocator(n=pose_loc+'_'+jnt+'_cone_aim_loc')[0]

        cmds.xform(jnt_aim_loc, t=mid_point)

        cmds.parent(jnt_aim_loc, pose_loc)

        aim_con_node = cmds.aimConstraint(jnt_aim_loc, jnt,
                           aim=[1,0,0], u=[0,1,0], wut='vector', wu=[0,1,0])[0]

        cmds.connectAttr(base_loc+'.aimVector', aim_con_node+'.aimVector', f=True)
        cmds.connectAttr(base_loc+'.upVector', aim_con_node+'.upVector', f=True)

        cmds.connectAttr(base_loc+'.intense', md+'.input2', f=True)

        cmds.connectAttr(aim_con_node+'.constraintRotate', chain_md+'.input1', f=True)
        cmds.connectAttr(base_loc+'.intensePart{}'.format(chain_num), chain_md+'.input2', f=True)

        cmds.connectAttr(chain_md+'.output', md+'.input1', f=True)

        cmds.connectAttr(md+'.output', chain_pma+'.input3D[0]', f=True)
        cmds.connectAttr(base_loc+'.offsetPart{}'.format(chain_num), chain_pma+'.input3D[1]', f=True)

        cmds.connectAttr(chain_pma+'.output3D', pb+'.inRotate2', f=True)

        cmds.connectAttr(base_loc+'.outputWeight', pb+'.weight', f=True)

        if connected_pbs:
            connected_laytex_pbs = list()
            if cmds.objExists(laytex):
                connected_laytex_pbs = cmds.listConnections(laytex, s=True, scn=True, type='pairBlend') or list()
                connected_laytex_pbs = list(set(connected_laytex_pbs))
            if not connected_laytex_pbs:
                cmds.connectAttr(connected_pbs[0]+'.outRotate', laytex+'.inputs[0].color', f=True)
                cmds.connectAttr(pb+'.outRotate', laytex+'.inputs[1].color', f=True)

                cmds.setAttr(laytex+'.inputs[0].blendMode', 4)
                cmds.setAttr(laytex+'.inputs[1].blendMode', 4)

                cmds.connectAttr(laytex+'.outColorR', jnt+'.rx', f=True)
                cmds.connectAttr(laytex+'.outColorG', jnt+'.ry', f=True)
                cmds.connectAttr(laytex+'.outColorB', jnt+'.rz', f=True)

            else:
                lay_pb_num = len(connected_laytex_pbs)
                cmds.connectAttr(pb+'.outRotate', laytex+'.inputs[{}].color'.format(lay_pb_num), f=True)
                cmds.setAttr(laytex+'.inputs[{}].blendMode'.format(lay_pb_num), 4)

        else:
            cmds.connectAttr(pb+'.outRotateX', jnt+'.rx', f=True)
            cmds.connectAttr(pb+'.outRotateY', jnt+'.ry', f=True)
            cmds.connectAttr(pb+'.outRotateZ', jnt+'.rz', f=True)

        cmds.addAttr(pb, ln='connectTo', at='message')
        cmds.connectAttr(jnt+'.message', pb+'.connectTo', f=True)



# joints = cmds.ls(os=True)
# create_coneCollision_rig(joints,
#                           angle_base_obj='p2:chr:Thigh_R',
#                           angle_pose_obj='p2:chr:Knee_R',
#                           center_pose_obj='p2:chr:Hip',
#                           default_coneAngle=180,
#                           default_target_aim_vec=[0,0,1],
#                           default_target_up_vec=[0,1,0])
