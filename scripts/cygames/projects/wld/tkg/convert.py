from maya import mel, cmds
from collections import OrderedDict

if cmds.objExists('bake_cnst_sets'):
    cmds.select('bake_cnst_sets', r=1, ne=1)
    cnsts = cmds.pickWalk(d='down')
    for cnst in cnsts:
        try:
            cmds.delete(cnst)
        except:
            pass

#get the namespace of current picker file.
currentPickerNamespace = mel.eval('MGP_GetCurrentPickerNamespace')

if currentPickerNamespace:
    currentPickerNamespace = currentPickerNamespace + ':'
else:
    currentPickerNamespace = ''


cmds.setAttr(currentPickerNamespace + "root_ctl.rotateZ", 0)
cmds.setAttr(currentPickerNamespace + "root_ctl.translateX", 0)
cmds.setAttr(currentPickerNamespace + "handL_ctl.translateX", 0)
cmds.setAttr(currentPickerNamespace + "handR_ctl.translateX", 0)
cmds.setAttr(currentPickerNamespace + "forearmL_ctl.translateX", 0)
cmds.setAttr(currentPickerNamespace + "forearmR_ctl.translateX", 0)
cmds.setAttr(currentPickerNamespace + "footR_ctl.translateX", 0)
cmds.setAttr(currentPickerNamespace + "legL_ctl.translateX", 0)
cmds.setAttr(currentPickerNamespace + "legR_ctl.translateX", 0)
cmds.setAttr(currentPickerNamespace + "footL_ctl.translateX", 0)
cmds.setAttr(currentPickerNamespace + "cog_ctl.translateX", 0)
cmds.setAttr(currentPickerNamespace + "root_ctl.translateY", 0)
cmds.setAttr(currentPickerNamespace + "handL_ctl.translateY", 0)
cmds.setAttr(currentPickerNamespace + "handR_ctl.translateY", 0)
cmds.setAttr(currentPickerNamespace + "forearmL_ctl.translateY", 0)
cmds.setAttr(currentPickerNamespace + "forearmR_ctl.translateY", 0)
cmds.setAttr(currentPickerNamespace + "footR_ctl.translateY", 0)
cmds.setAttr(currentPickerNamespace + "legL_ctl.translateY", 0)
cmds.setAttr(currentPickerNamespace + "legR_ctl.translateY", 0)
cmds.setAttr(currentPickerNamespace + "footL_ctl.translateY", 0)
cmds.setAttr(currentPickerNamespace + "cog_ctl.translateY", 0)
cmds.setAttr(currentPickerNamespace + "root_ctl.translateZ", 0)
cmds.setAttr(currentPickerNamespace + "handL_ctl.translateZ", 0)
cmds.setAttr(currentPickerNamespace + "handR_ctl.translateZ", 0)
cmds.setAttr(currentPickerNamespace + "forearmL_ctl.translateZ", 0)
cmds.setAttr(currentPickerNamespace + "forearmR_ctl.translateZ", 0)
cmds.setAttr(currentPickerNamespace + "footR_ctl.translateZ", 0)
cmds.setAttr(currentPickerNamespace + "legL_ctl.translateZ", 0)
cmds.setAttr(currentPickerNamespace + "legR_ctl.translateZ", 0)
cmds.setAttr(currentPickerNamespace + "footL_ctl.translateZ", 0)
cmds.setAttr(currentPickerNamespace + "cog_ctl.translateZ", 0)
cmds.setAttr(currentPickerNamespace + "root_ctl.rotateX", 0)
cmds.setAttr(currentPickerNamespace + "shoulderL_ctl.rotateX", 0)
cmds.setAttr(currentPickerNamespace + "shoulderR_ctl.rotateX", 0)
cmds.setAttr(currentPickerNamespace + "neck_ctl.rotateX", 0)
cmds.setAttr(currentPickerNamespace + "head_ctl.rotateX", 0)
cmds.setAttr(currentPickerNamespace + "spine_01_ctl.rotateX", 0)
cmds.setAttr(currentPickerNamespace + "spine_02_ctl.rotateX", 0)
cmds.setAttr(currentPickerNamespace + "spine_03_ctl.rotateX", 0)
cmds.setAttr(currentPickerNamespace + "fk_armR_ctl.rotateX", 0)
cmds.setAttr(currentPickerNamespace + "fk_handR_ctl.rotateX", 0)
cmds.setAttr(currentPickerNamespace + "fk_armL_ctl.rotateX", 0)
cmds.setAttr(currentPickerNamespace + "fk_handL_ctl.rotateX", 0)
cmds.setAttr(currentPickerNamespace + "hip_ctl.rotateX", 0)
cmds.setAttr(currentPickerNamespace + "fk_uplegR_ctl.rotateX", 0)
cmds.setAttr(currentPickerNamespace + "fk_footR_ctl.rotateX", 0)
cmds.setAttr(currentPickerNamespace + "fk_toebaseR_ctl.rotateX", 0)
cmds.setAttr(currentPickerNamespace + "fk_uplegL_ctl.rotateX", 0)
cmds.setAttr(currentPickerNamespace + "fk_footL_ctl.rotateX", 0)
cmds.setAttr(currentPickerNamespace + "fk_toebaseL_ctl.rotateX", 0)
cmds.setAttr(currentPickerNamespace + "handL_rot_ctl.rotateX", 0)
cmds.setAttr(currentPickerNamespace + "handR_rot_ctl.rotateX", 0)
cmds.setAttr(currentPickerNamespace + "footR_ctl.rotateX", 0)
cmds.setAttr(currentPickerNamespace + "toebaseL_ctl.rotateX", 0)
cmds.setAttr(currentPickerNamespace + "toebaseR_ctl.rotateX", 0)
cmds.setAttr(currentPickerNamespace + "footL_ctl.rotateX", 0)
cmds.setAttr(currentPickerNamespace + "root_ctl.rotateY", 0)
cmds.setAttr(currentPickerNamespace + "shoulderL_ctl.rotateY", 0)
cmds.setAttr(currentPickerNamespace + "shoulderR_ctl.rotateY", 0)
cmds.setAttr(currentPickerNamespace + "neck_ctl.rotateY", 0)
cmds.setAttr(currentPickerNamespace + "head_ctl.rotateY", 0)
cmds.setAttr(currentPickerNamespace + "spine_01_ctl.rotateY", 0)
cmds.setAttr(currentPickerNamespace + "spine_02_ctl.rotateY", 0)
cmds.setAttr(currentPickerNamespace + "spine_03_ctl.rotateY", 0)
cmds.setAttr(currentPickerNamespace + "fk_armR_ctl.rotateY", 0)
cmds.setAttr(currentPickerNamespace + "fk_handR_ctl.rotateY", 0)
cmds.setAttr(currentPickerNamespace + "fk_forearmR_ctl.rotateY", 0)
cmds.setAttr(currentPickerNamespace + "fk_armL_ctl.rotateY", 0)
cmds.setAttr(currentPickerNamespace + "fk_forearmL_ctl.rotateY", 0)
cmds.setAttr(currentPickerNamespace + "fk_handL_ctl.rotateY", 0)
cmds.setAttr(currentPickerNamespace + "hip_ctl.rotateY", 0)
cmds.setAttr(currentPickerNamespace + "fk_uplegR_ctl.rotateY", 0)
cmds.setAttr(currentPickerNamespace + "fk_footR_ctl.rotateY", 0)
cmds.setAttr(currentPickerNamespace + "fk_toebaseR_ctl.rotateY", 0)
cmds.setAttr(currentPickerNamespace + "fk_legR_ctl.rotateY", 0)
cmds.setAttr(currentPickerNamespace + "fk_uplegL_ctl.rotateY", 0)
cmds.setAttr(currentPickerNamespace + "fk_legL_ctl.rotateY", 0)
cmds.setAttr(currentPickerNamespace + "fk_footL_ctl.rotateY", 0)
cmds.setAttr(currentPickerNamespace + "fk_toebaseL_ctl.rotateY", 0)
cmds.setAttr(currentPickerNamespace + "handL_rot_ctl.rotateY", 0)
cmds.setAttr(currentPickerNamespace + "handR_rot_ctl.rotateY", 0)
cmds.setAttr(currentPickerNamespace + "footR_ctl.rotateY", 0)
cmds.setAttr(currentPickerNamespace + "toebaseL_ctl.rotateY", 0)
cmds.setAttr(currentPickerNamespace + "toebaseR_ctl.rotateY", 0)
cmds.setAttr(currentPickerNamespace + "footL_ctl.rotateY", 0)
cmds.setAttr(currentPickerNamespace + "shoulderL_ctl.rotateZ", 0)
cmds.setAttr(currentPickerNamespace + "shoulderR_ctl.rotateZ", 0)
cmds.setAttr(currentPickerNamespace + "neck_ctl.rotateZ", 0)
cmds.setAttr(currentPickerNamespace + "head_ctl.rotateZ", 0)
cmds.setAttr(currentPickerNamespace + "spine_01_ctl.rotateZ", 0)
cmds.setAttr(currentPickerNamespace + "spine_02_ctl.rotateZ", 0)
cmds.setAttr(currentPickerNamespace + "spine_03_ctl.rotateZ", 0)
cmds.setAttr(currentPickerNamespace + "fk_armR_ctl.rotateZ", 0)
cmds.setAttr(currentPickerNamespace + "fk_handR_ctl.rotateZ", 0)
cmds.setAttr(currentPickerNamespace + "fk_armL_ctl.rotateZ", 0)
cmds.setAttr(currentPickerNamespace + "fk_handL_ctl.rotateZ", 0)
cmds.setAttr(currentPickerNamespace + "hip_ctl.rotateZ", 0)
cmds.setAttr(currentPickerNamespace + "fk_uplegR_ctl.rotateZ", 0)
cmds.setAttr(currentPickerNamespace + "fk_footR_ctl.rotateZ", 0)
cmds.setAttr(currentPickerNamespace + "fk_toebaseR_ctl.rotateZ", 0)
cmds.setAttr(currentPickerNamespace + "fk_uplegL_ctl.rotateZ", 0)
cmds.setAttr(currentPickerNamespace + "fk_footL_ctl.rotateZ", 0)
cmds.setAttr(currentPickerNamespace + "fk_toebaseL_ctl.rotateZ", 0)
cmds.setAttr(currentPickerNamespace + "handL_rot_ctl.rotateZ", 0)
cmds.setAttr(currentPickerNamespace + "handR_rot_ctl.rotateZ", 0)
cmds.setAttr(currentPickerNamespace + "footR_ctl.rotateZ", 0)
cmds.setAttr(currentPickerNamespace + "toebaseL_ctl.rotateZ", 0)
cmds.setAttr(currentPickerNamespace + "toebaseR_ctl.rotateZ", 0)
cmds.setAttr(currentPickerNamespace + "footL_ctl.rotateZ", 0)
cmds.setAttr(currentPickerNamespace + "root_pos_ctl.translateX", 0)
cmds.setAttr(currentPickerNamespace + "root_pos_ctl.translateY", 0)
cmds.setAttr(currentPickerNamespace + "root_pos_ctl.translateZ", 0)
cmds.setAttr(currentPickerNamespace + "root_pos_ctl.rotateX", 0)
cmds.setAttr(currentPickerNamespace + "root_pos_ctl.rotateY", 0)
cmds.setAttr(currentPickerNamespace + "root_pos_ctl.rotateZ", 0)
cmds.setAttr(currentPickerNamespace + "handWeaponL_ctl.translateX", 0)
cmds.setAttr(currentPickerNamespace + "handWeaponL_ctl.translateY", 0)
cmds.setAttr(currentPickerNamespace + "handWeaponL_ctl.translateZ", 0)
cmds.setAttr(currentPickerNamespace + "handWeaponL_ctl.rotateX", 0)
cmds.setAttr(currentPickerNamespace + "handWeaponL_ctl.rotateY", 0)
cmds.setAttr(currentPickerNamespace + "handWeaponL_ctl.rotateZ", 0)
cmds.setAttr(currentPickerNamespace + "handWeaponR_ctl.translateX", 0)
cmds.setAttr(currentPickerNamespace + "handWeaponR_ctl.translateY", 0)
cmds.setAttr(currentPickerNamespace + "handWeaponR_ctl.translateZ", 0)
cmds.setAttr(currentPickerNamespace + "handWeaponR_ctl.rotateX", 0)
cmds.setAttr(currentPickerNamespace + "handWeaponR_ctl.rotateY", 0)
cmds.setAttr(currentPickerNamespace + "handWeaponR_ctl.rotateZ", 0)
cmds.setAttr(currentPickerNamespace + "handWeaponL_ctl.scaleX", 1)
cmds.setAttr(currentPickerNamespace + "handWeaponL_ctl.scaleY", 1)
cmds.setAttr(currentPickerNamespace + "handWeaponL_ctl.scaleZ", 1)
cmds.setAttr(currentPickerNamespace + "handWeaponR_ctl.scaleX", 1)
cmds.setAttr(currentPickerNamespace + "handWeaponR_ctl.scaleY", 1)
cmds.setAttr(currentPickerNamespace + "handWeaponR_ctl.scaleZ", 1)


def matchConstraint(currentNamespace='', jointNamepace='', gender='male'):
    def constraint_convert(src, dst, pos, rot, scl, mo):
        print(src, dst)
        cnsts = []
        if pos:
            cnst = cmds.pointConstraint(src, dst, w=1, mo=mo)
            cnsts.append(cnst)
        if rot:
            if ('fk_forearmL_ctl' in dst
                or 'fk_forearmR_ctl' in dst
                or 'fk_legL_ctl' in dst
                or 'fk_legR_ctl' in dst):
                cnst = cmds.orientConstraint(src, dst, w=1, mo=mo, sk=['x', 'z'])
                cnsts.append(cnst)
            else:
                cnst = cmds.orientConstraint(src, dst, w=1, mo=mo)
                cnsts.append(cnst)
        if scl:
            cnst = cmds.scaleConstraint(src, dst, w=1, mo=mo)
            cnsts.append(cnst)

        return cnsts

    source_joints = [u'root_jnt',
     u'cog_jnt',
     u'spine_01_jnt',
     u'spine_02_jnt',
     u'spine_03_jnt',
     u'neck_jnt',
     u'head_jnt',
     u'shoulderL_jnt',
     u'armL_jnt',
     u'forearmL_jnt',
     u'handL_jnt',
     u'handWeaponL_offset_jnt',
     u'handWeaponL_bind_jnt',
     u'shoulderR_jnt',
     u'armR_jnt',
     u'forearmR_jnt',
     u'handR_jnt',
     u'handWeaponR_offset_jnt',
     u'handWeaponR_bind_jnt',
     u'hip_jnt',
     u'uplegL_jnt',
     u'legL_jnt',
     u'footL_jnt',
     u'toebaseL_jnt',
     u'uplegR_jnt',
     u'legR_jnt',
     u'footR_jnt',
     u'toebaseR_jnt']


    match_ctrls = OrderedDict()
    match_ctrls[currentNamespace+'root_ctl'] = [jointNamepace+'root_jnt', 1, 1, 0, 1]
    match_ctrls[currentNamespace+'cog_ctl'] = [jointNamepace+'cog_jnt', 1, 0, 0, 1]
    match_ctrls[currentNamespace+'hip_ctl'] = [jointNamepace+'hip_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'spine_01_ctl'] = [jointNamepace+'spine_01_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'spine_02_ctl'] = [jointNamepace+'spine_02_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'spine_03_ctl'] = [jointNamepace+'spine_03_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'neck_ctl'] = [jointNamepace+'neck_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'head_ctl'] = [jointNamepace+'head_jnt', 0, 1, 0, 1]

    # IK arm
    match_ctrls[currentNamespace+'shoulderL_ctl'] = [jointNamepace+'shoulderL_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'handL_ctl'] = [jointNamepace+'handL_jnt', 1, 0, 0, 1]
    match_ctrls[currentNamespace+'handL_rot_ctl'] = [jointNamepace+'handL_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_con_armL_loc'] = [jointNamepace+'armL_jnt', 1, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_con_forearmL_loc'] = [jointNamepace+'forearmL_jnt', 1, 1, 0, 1]

    match_ctrls[currentNamespace+'shoulderR_ctl'] = [jointNamepace+'shoulderR_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'handR_ctl'] = [jointNamepace+'handR_jnt', 1, 0, 0, 1]
    match_ctrls[currentNamespace+'handR_rot_ctl'] = [jointNamepace+'handR_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_con_armR_loc'] = [jointNamepace+'armR_jnt', 1, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_con_forearmR_loc'] = [jointNamepace+'forearmR_jnt', 1, 1, 0, 1]

    # FK arm
    match_ctrls[currentNamespace+'fk_armL_ctl'] = [jointNamepace+'armL_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_forearmL_ctl'] = [jointNamepace+'forearmL_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_handL_ctl'] = [jointNamepace+'handL_jnt', 0, 1, 0, 1]

    match_ctrls[currentNamespace+'fk_armR_ctl'] = [jointNamepace+'armR_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_forearmR_ctl'] = [jointNamepace+'forearmR_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_handR_ctl'] = [jointNamepace+'handR_jnt', 0, 1, 0, 1]


    # IK leg
    match_ctrls[currentNamespace+'footL_ctl'] = [jointNamepace+'footL_jnt', 1, 1, 0, 1]
    match_ctrls[currentNamespace+'toebaseL_ctl'] = [jointNamepace+'toebaseL_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_con_uplegL_loc'] = [jointNamepace+'uplegL_jnt', 1, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_con_legL_loc'] = [jointNamepace+'legL_jnt', 1, 1, 0, 1]

    match_ctrls[currentNamespace+'footR_ctl'] = [jointNamepace+'footR_jnt', 1, 1, 0, 1]
    match_ctrls[currentNamespace+'toebaseR_ctl'] = [jointNamepace+'toebaseR_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_con_uplegR_loc'] = [jointNamepace+'uplegR_jnt', 1, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_con_legR_loc'] = [jointNamepace+'legR_jnt', 1, 1, 0, 1]

    # FK leg
    match_ctrls[currentNamespace+'fk_uplegL_ctl'] = [jointNamepace+'uplegL_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_legL_ctl'] = [jointNamepace+'legL_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_footL_ctl'] = [jointNamepace+'footL_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_toebaseL_ctl'] = [jointNamepace+'toebaseL_jnt', 0, 1, 0, 1]

    match_ctrls[currentNamespace+'fk_uplegR_ctl'] = [jointNamepace+'uplegR_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_legR_ctl'] = [jointNamepace+'legR_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_footR_ctl'] = [jointNamepace+'footR_jnt', 0, 1, 0, 1]
    match_ctrls[currentNamespace+'fk_toebaseR_ctl'] = [jointNamepace+'toebaseR_jnt', 0, 1, 0, 1]

    # Weapons
    match_ctrls[currentNamespace+'handWeaponL_offset_ctl'] = [jointNamepace+'handWeaponL_offset_jnt', 1, 1, 1, 1]
    match_ctrls[currentNamespace+'handWeaponR_offset_ctl'] = [jointNamepace+'handWeaponR_offset_jnt', 1, 1, 1, 1]

    match_ctrls[currentNamespace+'handWeaponL_ctl'] = [jointNamepace+'handWeaponL_bind_jnt', 1, 1, 1, 1]
    match_ctrls[currentNamespace+'handWeaponR_ctl'] = [jointNamepace+'handWeaponR_bind_jnt', 1, 1, 1, 1]



    for jnt in source_joints:
        cmds.xform(jointNamepace+jnt, ro=[0, 0, 0], a=1)

    # root cog zero out
    cmds.xform(jointNamepace+'root_jnt', t=[0, 0, 0], a=1)

    if gender == 'male':
        cmds.xform(jointNamepace+'cog_jnt', t=[0, 103.337, 2.88754], a=1)

        # weapon
        if cmds.objExists(jointNamepace+'handWeaponL_offset_jnt'):
            cmds.xform(jointNamepace+'handWeaponL_offset_jnt', t=[6.689, -0.526, 0.0], a=1)
        if cmds.objExists(jointNamepace+'handWeaponR_offset_jnt'):
            cmds.xform(jointNamepace+'handWeaponR_offset_jnt', t=[-6.689, 0.526, 0.0], a=1)

        if cmds.objExists(jointNamepace+'handWeaponL_bind_jnt'):
            cmds.xform(jointNamepace+'handWeaponL_bind_jnt', t=[0, 0, 0], a=1)
        if cmds.objExists(jointNamepace+'handWeaponR_bind_jnt'):
            cmds.xform(jointNamepace+'handWeaponR_bind_jnt', t=[0, 0, 0], a=1)

    if gender == 'female':
        cmds.xform(jointNamepace+'cog_jnt', t=[0, 101.147, 1.688], a=1)

        # weapon
        if cmds.objExists(jointNamepace+'handWeaponL_offset_jnt'):
            cmds.xform(jointNamepace+'handWeaponL_offset_jnt', t=[7.456, 0.0, 0.0], a=1)
        if cmds.objExists(jointNamepace+'handWeaponR_offset_jnt'):
            cmds.xform(jointNamepace+'handWeaponR_offset_jnt', t=[-7.456, 0.0, 0.0], a=1)

        if cmds.objExists(jointNamepace+'handWeaponL_bind_jnt'):
            cmds.xform(jointNamepace+'handWeaponL_bind_jnt', t=[0, 0, 0], a=1)
        if cmds.objExists(jointNamepace+'handWeaponR_bind_jnt'):
            cmds.xform(jointNamepace+'handWeaponR_bind_jnt', t=[0, 0, 0], a=1)

    # const sets
    if not cmds.objExists('bake_cnst_sets'):
        cmds.sets(em=1, n='bake_cnst_sets')


    bake_ctrls = []
    for ctrl, jnt_value in match_ctrls.items():
        bake_ctrls.append(ctrl)
        if ('fk_con_armL_loc' in ctrl
            or 'fk_con_forearmL_loc' in ctrl
            or 'fk_con_armR_loc' in ctrl
            or 'fk_con_forearmR_loc' in ctrl
            or 'fk_con_uplegL_loc' in ctrl
            or 'fk_con_legL_loc' in ctrl
            or 'fk_con_uplegR_loc' in ctrl
            or 'fk_con_legR_loc' in ctrl):
                cmds.xform(ctrl, t=[0, 0, 0], ro=[0, 0, 0], a=1)

        try:
            cnsts = constraint_convert(jnt_value[0], ctrl, jnt_value[1], jnt_value[2], jnt_value[3], jnt_value[4])
            for ccnn in cnsts:
                cmds.sets(ccnn, add='bake_cnst_sets')
        except Exception as e:
            print(e)

    # PoleVectors
    cnsts = constraint_convert(currentNamespace+'fk_con_armL_pv_loc', currentNamespace+'forearmL_ctl', 1, 0, 0, 0)
    for ccnn in cnsts:
        cmds.sets(ccnn, add='bake_cnst_sets')
    cnsts = constraint_convert(currentNamespace+'fk_con_forearmL_pv_loc', currentNamespace+'forearmL_ctl', 1, 0, 0, 0)
    for ccnn in cnsts:
        cmds.sets(ccnn, add='bake_cnst_sets')
    cnsts = constraint_convert(currentNamespace+'fk_con_armR_pv_loc', currentNamespace+'forearmR_ctl', 1, 0, 0, 0)
    for ccnn in cnsts:
        cmds.sets(ccnn, add='bake_cnst_sets')
    cnsts = constraint_convert(currentNamespace+'fk_con_forearmR_pv_loc', currentNamespace+'forearmR_ctl', 1, 0, 0, 0)
    for ccnn in cnsts:
        cmds.sets(ccnn, add='bake_cnst_sets')

    cnsts = constraint_convert(currentNamespace+'fk_con_uplegL_pv_loc', currentNamespace+'legL_ctl', 1, 0, 0, 0)
    for ccnn in cnsts:
        cmds.sets(ccnn, add='bake_cnst_sets')
    cnsts = constraint_convert(currentNamespace+'fk_con_legL_pv_loc', currentNamespace+'legL_ctl', 1, 0, 0, 0)
    for ccnn in cnsts:
        cmds.sets(ccnn, add='bake_cnst_sets')
    cnsts = constraint_convert(currentNamespace+'fk_con_uplegR_pv_loc', currentNamespace+'legR_ctl', 1, 0, 0, 0)
    for ccnn in cnsts:
        cmds.sets(ccnn, add='bake_cnst_sets')
    cnsts = constraint_convert(currentNamespace+'fk_con_legR_pv_loc', currentNamespace+'legR_ctl', 1, 0, 0, 0)
    for ccnn in cnsts:
        cmds.sets(ccnn, add='bake_cnst_sets')

currentNamespace = mel.eval('MGP_GetCurrentPickerNamespace')

if currentNamespace:
    currentNamespace = currentNamespace + ':'
else:
    currentNamespace = ''


try:
    btnLabel = mel.eval('string $btnLabel = `MGPickerItem -q -l commandButton41`;')
    if ':' in btnLabel:
        spl_names = btnLabel.split(':')
        jointNamepace = ':'.join(spl_names[:-1:]) + ':'
    else:
        jointNamepace = ''

    matchConstraint(currentNamespace=currentNamespace, jointNamepace=jointNamepace, gender='male')
except Exception as e:
    print(e)
