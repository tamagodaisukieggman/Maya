from maya import cmds, mel
import maya.OpenMaya as om

from collections import OrderedDict
from imp import reload
import math
import traceback

import tkgRigBuild.libs.common as tkgCommon
reload(tkgCommon)

def get_dag_nodes(obj=None, type=None, remove_top=None):
    joints = cmds.ls(obj, dag=True, type=type)
    if remove_top:
        joints.remove(obj)

    if not joints:
        return None

    return tkgCommon.order_dags(joints)

def aim_nodes(base=None, target=None, aim_axis='z', up_axis='y', worldUpType='object', worldUpObject=None, worldSpace=False, world_axis='y'):
    axis_dict = {
        'x':[1,0,0],
        'y':[0,1,0],
        'z':[0,0,1],
        '-x':[-1,0,0],
        '-y':[0,-1,0],
        '-z':[0,0,-1]
    }

    aimVector = axis_dict[aim_axis]
    upVector = axis_dict[up_axis]

    settings = {}

    aim_obj = cmds.spaceLocator()[0]
    cmds.matchTransform(aim_obj, base)

    up_obj = cmds.spaceLocator()[0]
    cmds.matchTransform(up_obj, target)

    if worldUpType == 'object':
        if worldSpace:
            cmds.xform(up_obj, t=[v*10 for v in axis_dict[world_axis]], r=True, ws=True)
        else:
            cmds.xform(up_obj, t=[v*10 for v in axis_dict[up_axis]], r=True, os=True)

    if worldUpObject:
        settings['worldUpObject'] = worldUpObject
    else:
        settings['worldUpObject'] = up_obj

    cmds.delete(
        cmds.aimConstraint(
            aim_obj,
            target,
            offset=[0,0,0],
            w=True,
            aimVector=aimVector,
            upVector=upVector,
            worldUpType=worldUpType,
            **settings
        )
    )

    cmds.delete(aim_obj)
    cmds.delete(up_obj)

def aim_nodes_from_root(root_jnt=None, type='jonit', aim_axis='x', up_axis='y', worldUpType='object', worldUpObject=None, worldSpace=False, world_axis='y'):
    # 選択したトップジョイントを選択して実行
    joints = cmds.ls(root_jnt, dag=True, type=type)
    sorted_joints = tkgCommon.order_dags(joints)

    store_joint_values = OrderedDict()
    for sj in sorted_joints:
        store_joint_values[sj] = [cmds.xform(sj, q=True, t=True, ws=True),
                                  cmds.xform(sj, q=True, ro=True, ws=True)]

    tree = OrderedDict()

    for jnt in sorted_joints:
        tree[jnt] = OrderedDict()
        children = cmds.listRelatives(jnt, type=type, c=True)
        branches = OrderedDict()
        if children:
            if 1 < len(children):
                for chd in children:
                    branches[chd] = get_dag_nodes(obj=chd, type=type, remove_top=True)
            else:
                tree[jnt]['child'] = children[0]

        if branches:
            tree[jnt]['children'] = branches


    for jnt, child_info in tree.items():
        if 'child' in child_info.keys():
            child = child_info['child']

            # worldUpType='object' or worldUpType='scene'
            aim_nodes(base=child,
                      target=jnt,
                      aim_axis=aim_axis,
                      up_axis=up_axis,
                      worldUpType=worldUpType,
                      worldUpObject=worldUpObject,
                      worldSpace=worldSpace,
                      world_axis=world_axis)

            wt = store_joint_values[child][0]
            cmds.xform(child, t=wt, ws=True, a=True, p=True)

        # elif 'children' in child_info.keys():
        #     children = child_info['children']
        #     for chi, grand_chi in children.items():
        #         child_info = tree[chi]


        for obj, trs in store_joint_values.items():
            cmds.xform(obj, t=trs[0], ws=True, a=True, p=True)

            # if 'child' in tree[child].keys():
            #     grand_chi = tree[child]['child']
            #     wt = store_joint_values[grand_chi][0]
            #     cmds.xform(grand_chi, t=wt, ws=True, a=True, p=True)

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
