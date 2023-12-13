import math
from collections import OrderedDict
import re
import traceback
import maya.cmds as cmds
import maya.mel as mel

def renameDuplicates(duplicated=None, prefix=''):
    #Find all objects that have the same shortname as another
    #We can indentify them because they have | in the name
    duplicates = [f for f in duplicated if '|' in f]
    #Sort them by hierarchy so that we don't rename a parent before a child.
    duplicates.sort(key=lambda obj: obj.count('|'), reverse=True)

    #if we have duplicates, rename them
    renamed = []
    if duplicates:
        for name in duplicates:
            # extract the base name
            m = re.compile("[^|]*$").search(name)
            shortname = m.group(0)

            # extract the numeric suffix
            m2 = re.compile(".*[^0-9]").match(shortname)
            if m2:
                stripSuffix = m2.group(0)
            else:
                stripSuffix = shortname

            #rename, adding '#' as the suffix, which tells maya to find the next available number
            newname = cmds.rename(name, (prefix + stripSuffix))

            renamed.append(newname)

        return renamed

    else:
        return duplicated

def simplebake(objects, start):
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

    cmds.currentTime(start)

def ikpv_cnst(prefix, dst, start, mid, end, move, bake_sets, cnst_sets):
    loc1 = cmds.spaceLocator()
    loc2 = cmds.duplicate(loc1)
    loc3 = cmds.duplicate(loc1)
    cmds.parent(loc3, loc2)
    cmds.parent(loc2, loc1)

    cmds.sets(loc1, add=bake_sets)
    cmds.sets(loc2, add=bake_sets)
    cmds.sets(loc3, add=bake_sets)


    po = cmds.pointConstraint(start, loc1, w=1)
    cmds.pointConstraint(end, loc1, w=1)
    # cmds.delete(po)

    # cmds.matchTransform(loc1, start, pos=1, rot=1, scl=0)
    if ('forearmL_ctl' in dst
        or 'forearmR_ctl' in dst):
        cmds.move(0, 0, 5, r=1, os=1, wd=1)

        if 'L_' in dst:
            wuo = '{}armL_jnt'.format(prefix)

        if 'R_' in dst:
            wuo = '{}armR_jnt'.format(prefix)

        cmds.aimConstraint(mid, loc2, w=1, aim=(0,0,1), u=(0,1,0), wut='objectrotation', wu=(0,1,0), wuo=wuo)
        cmds.move(0, 0, move, loc3, r=1, os=1, wd=1)


    elif ('legL_ctl' in dst
        or 'legR_ctl' in dst):
        cmds.move(0, 0, -15, loc2, r=1, os=1, wd=1)

        if 'L_' in dst:
            wuo = '{}uplegL_jnt'.format(prefix)

        if 'R_' in dst:
            wuo = '{}uplegR_jnt'.format(prefix)

        cmds.aimConstraint(mid, loc2, w=1, aim=(0,0,1), u=(0,1,0), wut='objectrotation', wu=(0,1,0), wuo=wuo)
        cmds.move(0, 0, move, loc3, r=1, os=1, wd=1)

    cmds.orientConstraint(wuo, loc1[0], w=1, mo=1)

    cmds.matchTransform(loc3, dst)
    po = cmds.pointConstraint(loc3, dst)
    cmds.sets(po, add=cnst_sets)



def euler_to_quaternion(yaw, pitch, roll, order):
    yaw = math.radians(yaw)
    pitch = math.radians(pitch)
    roll = math.radians(roll)

    if (order == 'xyz'):
        qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
        qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
        qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
        qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)

    elif (order == 'yzx'):
        qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
        qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) - math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
        qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
        qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)

    elif (order == 'zxy'):
        qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
        qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) - math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
        qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
        qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)

    elif (order == 'xzy'):
        qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
        qy = math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) + math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
        qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
        qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)

    elif (order == 'yxz'):
        qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
        qy = math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) + math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
        qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) + math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
        qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)

    elif (order == 'zyx'):
        qx = math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2) + math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2)
        qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) - math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
        qz = math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) + math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
        qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)


    return [qx, qy, qz, qw]

def quaternion_to_euler(x, y, z, w):
    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    X = math.degrees(math.atan2(t0, t1))

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    Y = math.degrees(math.asin(t2))

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    Z = math.degrees(math.atan2(t3, t4))

    return X, Y, Z


def crop_rotation(degree):
    if (degree > 180):
        return degree -360

    elif (degree < -180):
        return degree + 360

    else:
        return degree



def convertRotateOrder(sel=None, root_jnt = 'root_jnt', prefix = 'dummybake_', nss = '', ik_pv=None,
                       startFrame = None, endFrame = None, order = 'xyz', delete_dummy=None, correct_anim=None,
                       external=None):

    roo = {'xyz':0,
           'yzx':1,
           'zxy':2,
           'xzy':3,
           'yxz':4,
           'zyx':5}

    if not sel:
        sel = cmds.ls(os=1)

    all_dummy_bake_sets = 'all_dummy_bake_sets'
    if not cmds.objExists(all_dummy_bake_sets):
        cmds.sets(n=all_dummy_bake_sets, em=1)

    else:
        cmds.select(all_dummy_bake_sets, ne=1)
        [cmds.delete(obj) for obj in cmds.pickWalk(d='down') if cmds.objExists(obj)]
        cmds.sets(n=all_dummy_bake_sets, em=1)

    dummy_bake_sets = 'dummy_bake_sets'
    if not cmds.objExists(dummy_bake_sets):
        cmds.sets(n=dummy_bake_sets, em=1)

    cmds.sets(dummy_bake_sets, add=all_dummy_bake_sets)

    if external:
        dummy_bake_ctl_sets = 'dummy_bake_ctl_sets'
        if not cmds.objExists(dummy_bake_ctl_sets):
            cmds.sets(n=dummy_bake_ctl_sets, em=1)

        cmds.sets(dummy_bake_ctl_sets, add=all_dummy_bake_sets)

        dummy_bake_ctl_cnst_sets = 'dummy_bake_ctl_cnst_sets'
        if not cmds.objExists(dummy_bake_ctl_cnst_sets):
            cmds.sets(n=dummy_bake_ctl_cnst_sets, em=1)

        cmds.sets(dummy_bake_ctl_cnst_sets, add=all_dummy_bake_sets)

    dummy_bake_cnst_sets = 'dummy_bake_cnst_sets'
    if not cmds.objExists(dummy_bake_cnst_sets):
        cmds.sets(n=dummy_bake_cnst_sets, em=1)

    cmds.sets(dummy_bake_cnst_sets, add=all_dummy_bake_sets)


    ct = cmds.currentTime(q=1)

    dups = cmds.duplicate(root_jnt)

    renamed_dups = renameDuplicates(dups, prefix)

    cmds.parent(prefix+root_jnt.split(':')[-1], w=1)


    for obj in renamed_dups:
        if cmds.objectType(obj) == 'joint':
            cmds.sets(obj, add=dummy_bake_sets)

            listConnections = cmds.listConnections(obj, c=1, p=1)
            src_break = None
            dst_break = None
            for con in listConnections:
                if 'drawInfo' in con:
                    src_break = con

                if 'drawOverride' in con:
                    dst_break = con

            if src_break and dst_break:
                cmds.disconnectAttr(src_break, dst_break)


        if cmds.objectType(obj) == ('parentConstraint' or 'pointConstraint' or 'orientConstraint'):
            cmds.delete(obj)


    cmds.select(dummy_bake_sets, ne=1)
    sorted_renamed_dups = cmds.pickWalk(d='down')
    sorted_renamed_dups.sort()

    root_children = cmds.ls(root_jnt, dag=1, type='joint')
    root_children.sort()

    pacs = []
    for i, (orig, rdup) in enumerate(zip(root_children, sorted_renamed_dups)):
        pac = cmds.parentConstraint(orig, rdup, w=1)
        pacs.append(pac[0])


    simplebake(sorted_renamed_dups, ct)


    cmds.delete(pacs)


    if ik_pv:
        armL_iks = ['{}forearmL_ctl'.format(nss), '{}armL_jnt'.format(prefix), '{}forearmL_jnt'.format(prefix), '{}handL_jnt'.format(prefix)]
        armR_iks = ['{}forearmR_ctl'.format(nss), '{}armR_jnt'.format(prefix), '{}forearmR_jnt'.format(prefix), '{}handR_jnt'.format(prefix)]

        legL_iks = ['{}legL_ctl'.format(nss),'{}uplegL_jnt'.format(prefix), '{}legL_jnt'.format(prefix), '{}footL_jnt'.format(prefix)]
        legR_iks = ['{}legR_ctl'.format(nss),'{}uplegR_jnt'.format(prefix), '{}legR_jnt'.format(prefix), '{}footR_jnt'.format(prefix)]

        ikpv_cnst(prefix, armL_iks[0], armL_iks[1], armL_iks[2], armL_iks[3], 60, dummy_bake_sets, dummy_bake_cnst_sets)
        ikpv_cnst(prefix, armR_iks[0], armR_iks[1], armR_iks[2], armR_iks[3], 60, dummy_bake_sets, dummy_bake_cnst_sets)

        ikpv_cnst(prefix, legL_iks[0], legL_iks[1], legL_iks[2], legL_iks[3], 60, dummy_bake_sets, dummy_bake_cnst_sets)
        ikpv_cnst(prefix, legR_iks[0], legR_iks[1], legR_iks[2], legR_iks[3], 60, dummy_bake_sets, dummy_bake_cnst_sets)


    bodyparts = ['root', 'camera', 'hip', 'cog', 'spine', 'neck', 'head',
               'shoulder', 'arm', 'forearm', 'hand',
               'foot', 'toebase', 'upleg', 'leg']

    base_ctrls = []
    # ik rot
    for part in bodyparts:
        if part in bodyparts[7:]:
            for side in ['L', 'R']:
                if part in ['foot']:
                    loc = cmds.spaceLocator()
                    cmds.matchTransform(loc[0], nss+part+side+'_ctl')
                    cmds.parent(loc[0], prefix+part+side+'_jnt')
                    ori = cmds.orientConstraint(loc[0], nss+part+side+'_ctl', w=1, mo=1)
                    base_ctrls.append(nss+part+side+'_ctl')
                elif part in ['shoulder', 'toebase']:
                    ori = cmds.orientConstraint(prefix+part+side+'_jnt', nss+part+side+'_ctl', w=1, mo=1)
                    base_ctrls.append(nss+part+side+'_ctl')
                elif part in ['hand']:
                    ori = cmds.orientConstraint(prefix+part+side+'_jnt', nss+part+side+'_rot_ctl', w=1, mo=1)
                    base_ctrls.append(nss+part+side+'_rot_ctl')
                cmds.sets(ori, add=dummy_bake_cnst_sets)
        elif part == 'spine':
            for i in range(3):
                ori = cmds.orientConstraint(prefix+part+'_'+str(i+1).zfill(2)+'_jnt', nss+part+'_'+str(i+1).zfill(2)+'_ctl', w=1, mo=1)
                base_ctrls.append(nss+part+'_'+str(i+1).zfill(2)+'_ctl')
                cmds.sets(ori, add=dummy_bake_cnst_sets)
        elif part == 'camera':
            pass
        elif part == 'root':
            ori = cmds.orientConstraint(prefix+part+'_jnt', nss+part+'_pos_ctl', w=1, mo=1)
            base_ctrls.append(nss+part+'_pos_ctl')
            cmds.sets(ori, add=dummy_bake_cnst_sets)
        else:
            ori = cmds.orientConstraint(prefix+part+'_jnt', nss+part+'_ctl', w=1, mo=1)
            base_ctrls.append(nss+part+'_ctl')
            cmds.sets(ori, add=dummy_bake_cnst_sets)

    # ik pos
    for part in bodyparts:
        if part in ['hand','foot']:
            for side in ['L', 'R']:
                poc = cmds.pointConstraint(prefix+part+side+'_jnt', nss+part+side+'_ctl', w=1, mo=1)
                base_ctrls.append(nss+part+side+'_ctl')
                cmds.sets(poc, add=dummy_bake_cnst_sets)
        elif part in ['camera', 'cog']:
            poc = cmds.pointConstraint(prefix+part+'_jnt', nss+part+'_ctl', w=1, mo=1)
            base_ctrls.append(nss+part+'_ctl')
            cmds.sets(poc, add=dummy_bake_cnst_sets)
        elif part in ['root']:
            poc = cmds.pointConstraint(prefix+part+'_jnt', nss+part+'_pos_ctl', w=1, mo=1)
            base_ctrls.append(nss+part+'_pos_ctl')
            cmds.sets(poc, add=dummy_bake_cnst_sets)

    if sel:
        base_ctrls = [bctrl for bctrl in base_ctrls if bctrl in sel]

    base_ctrls = list(set(base_ctrls))


    if external:
        dummy_bake_ctl_gp = 'dummy_bake_ctl_gp'
        if not cmds.objExists(dummy_bake_ctl_gp):
            cmds.createNode('transform', n=dummy_bake_ctl_gp, ss=1)

        cmds.sets(dummy_bake_ctl_gp, add=dummy_bake_ctl_sets)

        base_ctrls.sort()
        base_ctrls_locs = []
        base_ctrls_loc_cnsts = []
        for ctrl in base_ctrls:
            bc = cmds.spaceLocator(n='{}_dummy_bake_loc'.format(ctrl.split(':')[-1]))
            cmds.setAttr('{}.rotateOrder'.format(bc[0]), k=1)
            cmds.parent(bc[0], dummy_bake_ctl_gp)
            base_ctrls_locs.append(bc[0])
            cmds.sets(bc[0], add=dummy_bake_ctl_sets)
            bpac = cmds.parentConstraint(ctrl, bc[0], w=1)
            base_ctrls_loc_cnsts.append(bpac[0])
            cmds.sets(bpac, add=dummy_bake_ctl_cnst_sets)

        c, p = 'handL_rot_ctl_dummy_bake_loc', 'handL_ctl_dummy_bake_loc'
        if cmds.objExists(c) and cmds.objExists(p):
            cmds.parent(c, p)

        c, p = 'handR_rot_ctl_dummy_bake_loc', 'handR_ctl_dummy_bake_loc'
        if cmds.objExists(c) and cmds.objExists(p):
            cmds.parent(c, p)

        simplebake(base_ctrls_locs, ct)
        cmds.delete(base_ctrls_loc_cnsts)

        loc_ctl_cnsts = [cmds.orientConstraint(obj, loc, w=1) for i, (obj, loc) in enumerate(zip(base_ctrls, base_ctrls_locs))]

    if external:
        for loc in base_ctrls_locs:
            cmds.setAttr('{}.rotateOrder'.format(loc), roo[order])

        simplebake(base_ctrls_locs, ct)
        locs_cnsts = cmds.ls(dummy_bake_ctl_gp, dag=1, type='orientConstraint')
        [cmds.delete(obj) for obj in locs_cnsts if cmds.objExists(obj)]

    if sel:
        if not external:
            for obj in sel:
                cmds.setAttr('{}.rotateOrder'.format(obj), roo[order])
        # print('{} Set Order:'.format(obj), order)
    # for obj in sel:
    #     listAttrs = cmds.listAttr(obj, k=1) or None
    #     if listAttrs:
    #         for at in listAttrs:
    #             if 'blendOrient' in at:
    #                 cmds.setAttr('{}.{}'.format(obj, at), 0)

        simplebake(sel, ct)


    if correct_anim:
        if sel:
            if startFrame == None:
                playmin = cmds.playbackOptions(q=1, min=1)
            else:
                playmin = startFrame

            if endFrame == None:
                playmax = cmds.playbackOptions(q=1, max=1)
            else:
                playmax = endFrame

            x = int(playmin)
            for i in range(int(playmax)+1):
                f = i + x
                cmds.currentTime(f)
                for obj in sel:
                    # q1 = euler_to_quaternion(roll=cmds.getAttr('{}.rx'.format(obj)),
                    #                   pitch=cmds.getAttr('{}.ry'.format(obj)),
                    #                   yaw=cmds.getAttr('{}.rz'.format(obj)),
                    #                   order='xyz')

                    # qtoe = quaternion_to_euler(*q1)
                    qtoe = cmds.xform(obj, q=1, ro=1, os=1)

                    cmds.xform('{}'.format(obj), ro=[crop_rotation(qtoe[0]), crop_rotation(qtoe[1]), crop_rotation(qtoe[2])], a=1, os=1)

                    cmds.setKeyframe('{}.r'.format(obj), breakdown=0)


    if delete_dummy:
        cmds.select(all_dummy_bake_sets, ne=1)
        [cmds.delete(obj) for obj in cmds.pickWalk(d='down') if cmds.objExists(obj)]

    if external:
        if cmds.objExists(dummy_bake_sets):
            cmds.select(dummy_bake_sets, ne=1)
            [cmds.delete(obj) for obj in cmds.pickWalk(d='down') if cmds.objExists(obj)]

        print(base_ctrls_locs)
        print(base_ctrls)


        loc_ctl_cnsts = []
        for i, (loc, obj) in enumerate(zip(base_ctrls_locs, base_ctrls)):
            if ('foot' in loc.replace('_dummy_bake_loc', '')
                or 'cog' in loc.replace('_dummy_bake_loc', '')
                or 'pos' in loc.replace('_dummy_bake_loc', '')):
                poc = cmds.pointConstraint(loc, obj, w=1)
                oric = cmds.orientConstraint(loc, obj, w=1)

                loc_ctl_cnsts.append(poc)
                loc_ctl_cnsts.append(oric)

            elif 'camera' in loc.replace('_dummy_bake_loc', ''):
                poc = cmds.pointConstraint(loc, obj, w=1)

                loc_ctl_cnsts.append(poc)

            elif 'hand' in loc.replace('_dummy_bake_loc', ''):
                if '_rot_' in loc.replace('_dummy_bake_loc', ''):
                    oric = cmds.orientConstraint(loc, obj, w=1)

                    loc_ctl_cnsts.append(oric)

                else:
                    poc = cmds.pointConstraint(loc, obj, w=1)

                    loc_ctl_cnsts.append(poc)

            else:
                oric = cmds.orientConstraint(loc, obj, w=1)

                loc_ctl_cnsts.append(oric)

        for ocnst in loc_ctl_cnsts:
            cmds.sets(ocnst, add=dummy_bake_ctl_sets)


    cmds.filterCurve(sel, f='euler')

    cmds.currentTime(ct)

    if sel:
        cmds.select(sel, r=1)


def convertRotateOrderFunc(sel=None, root_jnt = 'ref:root_jnt', prefix = 'dummybake_', nss = 'ref:', ik_pv=True,
                       startFrame = None, endFrame = None, order = 'xyz', delete_dummy=None, correct_anim=None,
                       external=None):
    try:
        cmds.refresh(su=1)
        convertRotateOrder(sel, root_jnt, prefix, nss, ik_pv, startFrame, endFrame, order, delete_dummy, correct_anim, external)
        cmds.refresh(su=0)
    except Exception as e:
        print(traceback.format_exc())
        cmds.refresh(su=0)


convertRotateOrderFunc(sel=None, root_jnt = 'male00_all1000_mdl_def:root_jnt', prefix = '', nss = 'male00_all1000_mdl_def:', ik_pv=False,
                       startFrame = None, endFrame = None, order = 'yxz', delete_dummy=False, correct_anim=True, external=True)
