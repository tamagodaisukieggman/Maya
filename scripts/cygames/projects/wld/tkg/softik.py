# -*- coding: utf-8 -*-
from maya import cmds, mel
import math


def simplebake(objects, start):
    try:
        cmds.refresh(su=1)
        cmds.bakeResults(objects,
                         at=['rx', 'ry', 'rz', 'tx', 'ty', 'tz'],
                         sparseAnimCurveBake=False,
                         minimizeRotation=False,
                         removeBakedAttributeFromLayer=False,
                         removeBakedAnimFromLayer=False,
                         oversamplingRate=1,
                         bakeOnOverrideLayer=False,
                         preserveOutsideKeys=True,
                         simulation=True,
                         sampleBy=1,
                         shape=False,
                         t=((cmds.playbackOptions(q=1, min=1), cmds.playbackOptions(q=1, max=1))),
                         disableImplicitControl=True,
                         controlPoints=False)
        cmds.refresh(su=0)

    except:
        cmds.refresh(su=0)

    cmds.currentTime(start)

# get joints distance
def get_distance(objA, objB):
    gObjA = cmds.xform(objA, q=True, t=True, ws=True)
    gObjB = cmds.xform(objB, q=True, t=True, ws=True)

    return math.sqrt(math.pow(gObjA[0]-gObjB[0],2)+math.pow(gObjA[1]-gObjB[1],2)+math.pow(gObjA[2]-gObjB[2],2))

# def build_softik(self):
def create_softik_locators(nss=None, jointList=None, softik_ik_ctrl=None):
    jointList = [nss+jt for jt in jointList]
    softik_ik_ctrl = nss+softik_ik_ctrl
    softik_value = 20
    softik_axis = 'translateX'

    softik_loc_sets = '{}_softik_loc_sets'.format(softik_ik_ctrl)
    if not cmds.objExists(softik_loc_sets):
        cmds.sets(n=softik_loc_sets, em=1)

    else:
        cmds.select(softik_loc_sets, ne=1)
        [cmds.delete(obj) for obj in cmds.pickWalk(d='down') if cmds.objExists(obj)]
        cmds.sets(n=softik_loc_sets, em=1)


    softik_loc_gp = '{}_softik_loc_gp'.format(softik_ik_ctrl)
    if not cmds.objExists(softik_loc_gp):
        cmds.createNode('transform', n=softik_loc_gp, ss=1)

    length = 0.0
    i = 0
    for jnt in jointList:
        if i == 0:
            pass
        else:
            length += get_distance(jointList[i-1], jnt)
        i += 1

    # locators
    loc_a = '{}_softIkLoc'.format(jointList[0])
    loc_b = '{}_softIkLoc'.format(jointList[-1])
    loc_c = '{}_exp_softIkLoc'.format(jointList[-1])
    loc_d = '{}_aimobj_softIkLoc'.format(jointList[-1])

    locs = [loc_a, loc_b, loc_c, loc_d]

    [cmds.spaceLocator(n='{}'.format(loc)) for loc in locs]

    cmds.parent(loc_b, loc_a)
    cmds.parent(loc_c, loc_a)
    cmds.parent(loc_d, loc_a)

    # const
    const_loc = cmds.spaceLocator(n='{0}_const_softIkloc'.format(jointList[-1]))
    # cmds.matchTransform(const_loc[0], softik_ik_ctrl)

    pac = cmds.parentConstraint(softik_ik_ctrl, const_loc[0], w=1)
    simplebake([const_loc[0]], cmds.currentTime(q=1))
    cmds.delete(pac)

    cmds.pointConstraint(jointList[0], loc_a, w=1)
    cmds.pointConstraint(const_loc[0], loc_b, w=1)
    cmds.matchTransform(loc_d, const_loc[0])
    cmds.parent(loc_d, const_loc[0])
    cmds.move(0, 0, 10, loc_d, r=1, os=1, wd=1)
    cmds.setAttr('{0}.v'.format(loc_a), 0)
    cmds.setAttr('{0}.v'.format(loc_d), 0)

    aimConst_options = {}
    aimConst_options['offset'] = [0,0,0]
    aimConst_options['aimVector'] = [1,0,0]
    aimConst_options['upVector'] = [0,0,1]
    aimConst_options['worldUpType'] = "object"
    aimConst_options['worldUpObject'] = loc_d

    cmds.aimConstraint(const_loc[0], loc_a, w=1, **aimConst_options)
    cmds.pointConstraint(loc_c, softik_ik_ctrl, w=1)

    # softik_ik_ctrl = const_loc[0]
    # addAttr
    if 'softIk' not in cmds.listAttr(const_loc[0]):
        cmds.addAttr(const_loc[0], ln='softIk', k=1, at='double', dv=0, min=0, max=softik_value)
        cmds.setAttr('{}.{}'.format(const_loc[0], 'softIk'), l=0)
    else:
        cmds.deleteAttr(const_loc[0], at='softIk')
        cmds.addAttr(const_loc[0], ln='softIk', k=1, at='double', dv=0, min=0, max=softik_value)
        cmds.setAttr('{}.{}'.format(const_loc[0], 'softIk'), l=0)

    exp = cmds.createNode('expression', n='{}_softIkExp'.format(softik_ik_ctrl))
    cmds.expression(exp, e=1, s=u"""\nif ({0}.{1} > ({2} - {3}.softIk))\n\t{4}.{1} = ({2} - {3}.softIk) + {3}.softIk * (1-exp( -({0}.{1} - ({2} - {3}.softIk)) /{5}));\nelse\n\t{4}.{1} = {0}.{1}""".format(loc_b, softik_axis, length, const_loc[0], loc_c, softik_value), ae=0, uc='all')

    cmds.parent(const_loc[0], softik_loc_gp)
    cmds.parent(loc_a, softik_loc_gp)

    cmds.sets(softik_loc_gp, add=softik_loc_sets)
    cmds.sets(const_loc[0], add=softik_loc_sets)
    cmds.sets(loc_a, add=softik_loc_sets)
    cmds.sets(exp, add=softik_loc_sets)
