# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
import maya.api.OpenMaya as om2
from collections import OrderedDict

import math

# """
# Get polevector position
# """
def get_poleVector_position(startObj=None, middleObj=None, endObj=None, move=None):
    if startObj == None or middleObj == None or endObj == None:
        sel = cmds.ls(os=1)
        try:
            startObj = sel[0]
            middleObj = sel[1]
            endObj = sel[2]
        except Exception as e:
            return
    start = cmds.xform(startObj ,q= 1 ,ws = 1,t =1 )
    mid = cmds.xform(middleObj ,q= 1 ,ws = 1,t =1 )
    end = cmds.xform(endObj ,q= 1 ,ws = 1,t =1 )
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

    pvLoc = cmds.spaceLocator(n='{}_poleVecPosLoc'.format(middleObj))
    cmds.xform(pvLoc[0] , ws =1 , t= (finalV.x , finalV.y ,finalV.z))
    cmds.xform(pvLoc[0] , ws = 1 , rotation = ((rot.x/math.pi*180.0),(rot.y/math.pi*180.0),(rot.z/math.pi*180.0)))
    cmds.select(pvLoc[0])
    cmds.move(move, 0, 0, r=1, os=1, wd=1)
    cmds.select(cl=True)

    # result = {pvLoc:{'translate':(finalV.x , finalV.y ,finalV.z), 'rotate':((rot.x/math.pi*180.0),(rot.y/math.pi*180.0),(rot.z/math.pi*180.0))}}
    return pvLoc[0]

# """
# Get ikfk natch sets values
# """
def get_ikfk_state(sets='ik2fk_sets'):
    ikfk_state = {}
    cmds.select(sets, ne=1, r=1)
    ikfk_ntw = cmds.pickWalk(d='down')[0]
    ik_state = cmds.getAttr('{0}.ikstate'.format(ikfk_ntw))
    fk_state = cmds.getAttr('{0}.fkstate'.format(ikfk_ntw))

    ikfk_state['state_ik'] = '{0}'.format(":".join(ik_state.split(',')))
    ikfk_state['state_fk'] = '{0}'.format(":".join(fk_state.split(',')))

    return ikfk_state

def get_fk2ik_values(sets='fk2ik_sets'):
    cmds.select(sets, ne=1, r=1)
    ikfk_ntw = cmds.pickWalk(d='down')[0]
    fk_match = cmds.getAttr('{0}.fkmatch'.format(ikfk_ntw))
    fk2ik_fk = fk_match.split(',')
    ik_match = cmds.getAttr('{0}.ikmatch'.format(ikfk_ntw))
    fk2ik_ik = ik_match.split(',')

    return fk2ik_fk, fk2ik_ik

def get_ik2fk_ik_values(sets='ik2fk_sets'):
    ik2fk_ik = []
    cmds.select(sets, ne=1, r=1)
    ikfk_ntw = cmds.pickWalk(d='down')[0]
    ik_ctrls = cmds.getAttr('{0}.ikctrlmatch'.format(ikfk_ntw))
    ik2fk_ik.append(ik_ctrls)
    ik_pv = cmds.getAttr('{0}.ikpvmatch'.format(ikfk_ntw))
    ik2fk_ik.append(ik_pv)
    ik_match = cmds.getAttr('{0}.ikmatch'.format(ikfk_ntw))
    ik2fk_ik.append(ik_match)
    ikfkzeroout = cmds.getAttr('{0}.ikfkzeroout'.format(ikfk_ntw))
    ik2fk_ik.append(ikfkzeroout)

    return ik2fk_ik

def get_ik2fk_fk_values(sets='ik2fk_sets'):
    ik2fk_fk = []
    cmds.select(sets, ne=1, r=1)
    ikfk_ntw = cmds.pickWalk(d='down')[0]
    fk_ctrls = cmds.getAttr('{0}.fkctrlmatch'.format(ikfk_ntw))
    ik2fk_fk.append(fk_ctrls)
    fk_pv = cmds.getAttr('{0}.fkpvmatch'.format(ikfk_ntw))
    ik2fk_fk.append(fk_pv.split(','))
    fk_match = cmds.getAttr('{0}.fkmatch'.format(ikfk_ntw))
    ik2fk_fk.append(fk_match)

    return ik2fk_fk

# """
# Get namespace
# """
def get_current_namespaces():
    exclude_list = ['UI', 'shared']

    current = cmds.namespaceInfo(cur=True)
    cmds.namespace(set=':')
    namespaces = ['{}:'.format(ns) for ns in cmds.namespaceInfo(lon=True) if ns not in exclude_list]
    cmds.namespace(set=current)

    # Reference Nodes
    rn = cmds.ls(type="reference", r=1)
    for i in rn:
        ref_ns = i.split("RN")
        ns = '{0}:'.format(ref_ns[0])
        if not ns in namespaces:
            namespaces.append(ns)

    if namespaces == []:
        namespaces = ''

    return namespaces

# """
# euler quaternion
# """
def quaternionToEuler(obj=None):
    rot = cmds.xform(obj, q=1, ro=1, os=1)
    rotOrder = cmds.getAttr('{}.rotateOrder'.format(obj))
    euler = om2.MEulerRotation(math.radians(rot[0]), math.radians(rot[1]), math.radians(rot[2]), rotOrder)
    quat = euler.asQuaternion()
    euler = quat.asEulerRotation()
    r = euler.reorder(rotOrder)
    return math.degrees(r.x), math.degrees(r.y), math.degrees(r.z)

# """
# FK to IK
# """
def fk2ik(tag='', fk2ik_sets='fk2ik_sets', fk2ik_ik=None, fk2ik_fk=None, ikfk_state=None, namespace=None):
    if namespace == None:
        namespace = ''
    if not 1 < len(namespace.split(':')):
        ns = '{0}:'.format(namespace)
    else:
        ns = '{0}'.format(namespace)
    if namespace == '':
        ns = '{0}'.format(namespace)

    fk2ik_sets = '{0}{1}{2}'.format(ns, tag, fk2ik_sets)

    if not cmds.objExists(fk2ik_sets):
        print('{0} is not exists. Is there current namespaces in {1}?'.format(fk2ik_sets, ns))
        return

    if not fk2ik_fk or not fk2ik_ik:
        fk2ik_fk, fk2ik_ik = get_fk2ik_values(sets=fk2ik_sets)

    if not ikfk_state:
        ikfk_state = get_ikfk_state(sets=fk2ik_sets)

    fk_ctrls_buf = []
    for i , (ik_ctrl, fk_ctrl) in enumerate(zip(fk2ik_ik, fk2ik_fk)):
        cmds.matchTransform('{0}{1}'.format(ns, fk_ctrl), '{0}{1}'.format(ns, ik_ctrl))
        quaternionToEuler(obj='{0}{1}'.format(ns, fk_ctrl))
        fk_ctrls_buf.append('{0}{1}'.format(ns, fk_ctrl))

    switch_ctrl = ikfk_state['state_fk'].split(':')[0]
    switch_state = ikfk_state['state_fk'].split(':')[1]
    if '|' in switch_ctrl:
        parent_ctrl = switch_ctrl.split('|')[0]
        shape_ctrl = switch_ctrl.split('|')[1]
        ns_switch_ctrl = '{0}{1}|{0}{2}'.format(ns, parent_ctrl, shape_ctrl)
    else:
        ns_switch_ctrl = '{0}{1}'.format(ns, switch_ctrl)
    cmds.setAttr('{0}'.format(ns_switch_ctrl), int(switch_state))

    return fk2ik_fk, fk2ik_ik, ikfk_state, fk_ctrls_buf

# """
# IK to FK
# """
def ik2fk(tag='', ik2fk_sets='ik2fk_sets', ik2fk_ik=None, ik2fk_fk=None, ikfk_state=None, pv_move=None, namespace=None):
    if namespace == None:
        namespace = ''
    if not 1 < len(namespace.split(':')):
        ns = '{0}:'.format(namespace)
    else:
        ns = '{0}'.format(namespace)
    if namespace == '':
        ns = '{0}'.format(namespace)

    ik2fk_sets = '{0}{1}{2}'.format(ns, tag, ik2fk_sets)

    if not cmds.objExists(ik2fk_sets):
        print('{0} is not exists. Is there current namespaces in {1}?'.format(ik2fk_sets, ns))
        return

    if not ik2fk_ik:
        ik2fk_ik = get_ik2fk_ik_values(sets=ik2fk_sets)

    if not ik2fk_fk:
        ik2fk_fk = get_ik2fk_fk_values(sets=ik2fk_sets)

    if not ikfk_state:
        ikfk_state = get_ikfk_state(sets=ik2fk_sets)

    if ik2fk_ik[3]:
        init_ik_ctrls = ik2fk_ik[3].split(',')
        [cmds.xform('{0}{1}'.format(ns, ik), t=[0, 0, 0], ro=[0, 0, 0]) for ik in init_ik_ctrls]

    ik_ctrls_buf = []
    for i , (ik_ctrl, fk_ctrl) in enumerate(zip(ik2fk_ik, ik2fk_fk)):
        ik_ctrls = ik_ctrl.split(',')
        ik_from_fk_caches = OrderedDict()
        ik_from_fk_sts = None
        for j, ik in enumerate(ik_ctrls):
            ik_match_ctrl = ik.split(':')[0]
            if ':' in ik:
                ik_option = ik.split(':')[1]
            else:
                ik_option = None
            if ik_option == 'match_T':
                cmds.matchTransform('{0}{1}'.format(ns, ik_match_ctrl), '{0}{1}'.format(ns, fk_ctrl), pos=1)
            elif ik_option == 'match_R':
                cmds.matchTransform('{0}{1}'.format(ns, ik_match_ctrl), '{0}{1}'.format(ns, fk_ctrl), rot=1)
                quaternionToEuler(obj='{0}{1}'.format(ns, ik_match_ctrl))
            elif ik_option == 'match_P':
                pv_loc = get_poleVector_position(startObj='{0}{1}'.format(ns, fk_ctrl[0]), middleObj='{0}{1}'.format(ns, fk_ctrl[1]), endObj='{0}{1}'.format(ns, fk_ctrl[2]), move=pv_move)
                cmds.matchTransform('{0}{1}'.format(ns, ik_match_ctrl), pv_loc)
                quaternionToEuler(obj='{0}{1}'.format(ns, ik_match_ctrl))
                cmds.delete(pv_loc)
            elif ik_option == 'cache':
                if cmds.objExists('{0}{1}'.format(ns, ik_match_ctrl)) and cmds.objExists('{0}{1}'.format(ns, fk_ctrl.split(',')[j])):
                    ik_from_fk_caches['{0}{1}'.format(ns, ik_match_ctrl)] = ['{0}{1}'.format(ns, fk_ctrl.split(',')[j]), cmds.xform('{0}{1}'.format(ns, fk_ctrl.split(',')[j]), q=1, t=1, ws=1), cmds.xform('{0}{1}'.format(ns, fk_ctrl.split(',')[j]), q=1, ro=1, ws=1)]
            else:
                if cmds.objExists('{0}{1}'.format(ns, ik)) and cmds.objExists('{0}{1}'.format(ns, fk_ctrl.split(',')[j])):
                    cmds.matchTransform('{0}{1}'.format(ns, ik), '{0}{1}'.format(ns, fk_ctrl.split(',')[j]))
                    quaternionToEuler(obj='{0}{1}'.format(ns, ik))

            ik_ctrls_buf.append('{0}{1}'.format(ns, ik_match_ctrl))

        [cmds.xform(ik_ctrl, t=fk_ctrl_values[1], ro=fk_ctrl_values[2], ws=1, a=1) for ik_ctrl, fk_ctrl_values in ik_from_fk_caches.items() if cmds.objExists(ik_ctrl)]

        switch_ctrl = ikfk_state['state_ik'].split(':')[0]
        switch_state = ikfk_state['state_ik'].split(':')[1]
        if '|' in switch_ctrl:
            parent_ctrl = switch_ctrl.split('|')[0]
            shape_ctrl = switch_ctrl.split('|')[1]
            ns_switch_ctrl = '{0}{1}|{0}{2}'.format(ns, parent_ctrl, shape_ctrl)
        else:
            ns_switch_ctrl = '{0}{1}'.format(ns, switch_ctrl)
        cmds.setAttr('{0}'.format(ns_switch_ctrl), int(switch_state))

    return ik2fk_ik, ik2fk_fk, ikfk_state, ik_ctrls_buf

# """
# Matchbake
# """
def matchbake(fk_or_ik_list=['fk', 'fk', 'fk', 'fk'], tags=['arms_L_', 'arms_R_', 'legs_L_', 'legs_R_'], time_range=None, playbackSlider=True, pv_move=20, namespace=None):
    if not 1 < len(namespace.split(':')):
        ns = '{0}:'.format(namespace)
    else:
        ns = '{0}'.format(namespace)
    if namespace == '':
        ns = '{0}'.format(namespace)

    #check and save current autokey state
    if cmds.autoKeyframe(q=True, st=True):
        autoKeyState = 1
    else:
        autoKeyState = 0

    cmds.autoKeyframe(st=0)

    if not time_range:
        playmin = cmds.playbackOptions(q=1, min=1)
        playmax = cmds.playbackOptions(q=1, max=1)

    else:
        playmin = time_range[0]
        playmax = time_range[1]

    start = playmin
    end = playmax-1

    #check to see if time range is highlighted
    if playbackSlider:
        gPlayBackSlider = mel.eval('$temp=$gPlayBackSlider')
        if cmds.timeControl(gPlayBackSlider, q=True, rv=True):
            frameRange = cmds.timeControl(gPlayBackSlider, q=True, ra=True)
            start = frameRange[0]
            end = frameRange[1]-1
        else:
            frameRange = cmds.currentTime(q=1)
            start = frameRange
            end = frameRange-1

    #bookend and key pinner plus all controls in range
    setkey_attrs = mel.eval('string $selectedChannelBox[] = `channelBox -query -selectedMainAttributes mainChannelBox`;')
    if setkey_attrs == []:
        setkey_attrs =  [u'tx', u'ty', u'tz', u'rx', u'ry', u'rz', u'sx', u'sy', u'sz']
    # mel.eval('string $target = "{0}";'.format(cmds.ls(os=1)[0]))
    # custom_setkey_attrs = mel.eval('$customChannels = `listAttr -keyable -userDefined $target`;')
    fk_ctrls_buf = None
    ik_ctrls_buf = None
    for i in range (int(start-1), int(end+2)):
        cmds.currentTime(i, e=True)
        for j, (fk_or_ik, tag) in enumerate(zip(fk_or_ik_list, tags)):
            if fk_or_ik == 'fk':
                # [fk2ik(arms_fk2ik_ik, arms_fk2ik_fk) for set in ikfk_sets]
                fk2ik_fk, fk2ik_ik, ikfk_state, fk_ctrls_buf = fk2ik(tag=tag, fk2ik_sets='fk2ik_sets', fk2ik_ik=None, fk2ik_fk=None, ikfk_state=None, namespace=ns)
                fk2ik_setkeys = ['{0}{1}'.format(ns, fkctrl) for fkctrl in fk2ik_fk]
                cmds.setKeyframe(fk2ik_setkeys, at=setkey_attrs)
                ikfk_switch_ctrl = ikfk_state['state_fk'].split(':')[0]
                ikfk_switch_ctrl_switch_value = ikfk_state['state_ik'].split(':')[1]

            elif fk_or_ik == 'ik':
                ik2fk_ik, ik2fk_fk, ikfk_state, ik_ctrls_buf = ik2fk(tag=tag, ik2fk_sets='ik2fk_sets', ik2fk_ik=None, ik2fk_fk=None, ikfk_state=None, pv_move=pv_move, namespace=ns)
                for ik_ctrl in ik2fk_ik:
                    if ik_ctrl:
                        ik_ctrls = ik_ctrl.split(',')
                        for ik in ik_ctrls:
                            ik_match_ctrl = ik.split(':')[0]
                            if cmds.objExists('{0}{1}'.format(ns, ik_match_ctrl)):
                                cmds.setKeyframe('{0}{1}'.format(ns, ik_match_ctrl), at=setkey_attrs)

                ikfk_switch_ctrl = ikfk_state['state_ik'].split(':')[0]
                ikfk_switch_ctrl_switch_value = ikfk_state['state_fk'].split(':')[1]

            switch_at = ikfk_switch_ctrl.split('.')[1]

            if '|' in ikfk_switch_ctrl:
                parent_ctrl = ikfk_switch_ctrl.split('|')[0]
                shape_ctrl = ikfk_switch_ctrl.split('|')[1]
                ns_switch_ctrl = '{0}{1}|{0}{2}'.format(ns, parent_ctrl, shape_ctrl)
            else:
                ns_switch_ctrl = '{0}{1}'.format(ns, ikfk_switch_ctrl)
            cmds.setKeyframe('{0}'.format(ns_switch_ctrl), at=switch_at)

            # switch fk or ik
            currentFrame = cmds.currentTime(q=1)
            # start frame
            if int(start-1) == currentFrame:
                cmds.currentTime(int(start-1), e=True)
                cmds.setAttr('{0}'.format(ns_switch_ctrl), float(ikfk_switch_ctrl_switch_value))
                cmds.setKeyframe('{0}'.format(ns_switch_ctrl), at=switch_at)

            # end frame
            elif int(end+1) == currentFrame:
                cmds.currentTime(int(end+2), e=True)
                cmds.setAttr('{0}'.format(ns_switch_ctrl), float(ikfk_switch_ctrl_switch_value))
                cmds.setKeyframe('{0}'.format(ns_switch_ctrl), at=switch_at)
                cmds.currentTime(currentFrame, e=True)

    if not fk_ctrls_buf:
        cmds.filterCurve(fk_ctrls_buf, f='euler')
    if not ik_ctrls_buf:
        cmds.filterCurve(ik_ctrls_buf, f='euler')

    cmds.currentTime(start)

    cmds.autoKeyframe(state=autoKeyState)

def objExists_iter(objects):
    for obj in objects:
        if not cmds.objExists(obj):
            cmds.warning('{0} is not exists.'.format(obj))
            return False

# """
# Create IKFK Match Sets
# """
def create_ikfkmatch_sets(sel=None, tag=None, ik_or_fk='fk',
                          ik2fk_ikctrls=None, ik2fk_ikctrls_state=None, ik2fk_fkctrls=None,
                          ik2fk_ikpv=None, ik2fk_ikpv_state=None, ik2fk_fkpvctrls=None,
                          state_ik_attr=None, state_fk_attr=None,
                          ikfkzeroout=None
                          ):
    u"""
    Create ikfk match sets
    sel= list ikとfkのコントローラを交互に代入します
        ik_or_fkが'fk'か'ik'かによってsetAttrで入る値が変わります 偶数インデクス sel[::2] 奇数インデクス sel[1::2]
        ik_or_fk='fk'
            cmds.setAttr('{0}.ikmatch'.format(tag_fk2ik_ntw), ",".join(sel[1::2]), type='string')
            cmds.setAttr('{0}.fkmatch'.format(tag_fk2ik_ntw), ",".join(sel[::2]), type='string')
        ik_or_fk='ik'
            cmds.setAttr('{0}.ikmatch'.format(tag_ik2fk_ntw), ",".join(sel[::2]), type='string')
            cmds.setAttr('{0}.fkmatch'.format(tag_ik2fk_ntw), ",".join(sel[1::2]), type='string')
    tag= string 各部位を識別するタグ
    ik_or_fk= string 'fk' or 'ik' 'fk'でfk2ik, 'ik'でik2fkを発動します
    ik2fk_ikctrls= list マッチさせるIKコントローラを代入します
    ik2fk_ikctrls_state= list ['match_T', 'match_R']
        match_TはTranslateのみ, match_RはRotateのみ
        ik2fk_ikctrlsと同じインデクスで機能します
    ik2fk_fkctrls= list ik2fk_ikctrlsとマッチさせるfkコントローラ
    ik2fk_ikpv= list PoleVectorコントローラ
    ik2fk_ikpv_state= list ['match_P']で機能します
    ik2fk_fkpvctrls= list PoleVectorを算出するためのfkコントローラ
    state_ik_attr= list ['ikfkスイッチ', 'ikにした時の値']
    state_fk_attr= list ['ikfkスイッチ', 'fkにした時の値']

    --example--
    # arms_L fk2ik
    create_ikfkmatch_sets(sel=[u'proxy_shoulderL_fk_ctrl',
     u'proxy_shoulderL_jnt_ik_jnt',
     u'proxy_armL_fk_ctrl',
     u'proxy_armL_jnt_ik_jnt',
     u'proxy_forearmL_fk_ctrl',
     u'proxy_forearmL_jnt_ik_jnt',
     u'proxy_handL_fk_ctrl',
     u'proxy_handL_jnt_ik_jnt'], tag='arms_L_', ik_or_fk='fk', state_ik_attr=['proxy_handL_jnt_ik_ctrl.IKFK', '1'], state_fk_attr=['proxy_handL_jnt_ik_ctrl.IKFK', '0'])

    # arms_L ik2fk
    create_ikfkmatch_sets(sel=[u'proxy_shoulderL_jnt_ik_jnt_ik_jnt_autoRot_ctrl',u'proxy_shoulderL_fk_ctrl'], tag='arms_L_', ik_or_fk='ik',
                          ik2fk_ikctrls=[u'proxy_handL_jnt_ik_ctrl', u'proxy_armL_jnt_ik_autoRot_ctrl_autoRot_ctrl'], ik2fk_ikctrls_state=['match_T', 'match_R'], ik2fk_fkctrls=['proxy_handL_fk_ctrl'],
                          ik2fk_ikpv=['proxy_forearmL_jnt_ik_pv_ctrl'], ik2fk_ikpv_state=['match_P'], ik2fk_fkpvctrls=[u'proxy_armL_fk_ctrl', u'proxy_forearmL_fk_ctrl', u'proxy_handL_fk_ctrl'],
                          state_ik_attr=['proxy_handL_jnt_ik_ctrl.IKFK', '1'], state_fk_attr=['proxy_handL_jnt_ik_ctrl.IKFK', '0'])

    """
    if sel == None:
        sel = cmds.ls(os=1)

    # ikfk match sets
    ikfk_match_sets = 'ikfk_match_sets'
    if not cmds.objExists(ikfk_match_sets):
        cmds.sets(em=1, n=ikfk_match_sets)

    if ik_or_fk == 'fk':
        # add fk to ik sets select fk and ik, fk and ik, fk and ik, ,,,
        tag_fk2ik_sets = '{0}fk2ik_sets'.format(tag)
        if not cmds.objExists(tag_fk2ik_sets):
            cmds.sets(em=1, n=tag_fk2ik_sets)

        tag_fk2ik_ntw = '{0}fk2ik_ntw'.format(tag)
        if not cmds.objExists(tag_fk2ik_ntw):
            cmds.createNode('network', n=tag_fk2ik_ntw, ss=1)

        listAttr = cmds.listAttr(tag_fk2ik_ntw)
        if listAttr == None or not 'ikmatch' in listAttr:
            cmds.addAttr(tag_fk2ik_ntw, ln='ikmatch', dt='string')

        listAttr = cmds.listAttr(tag_fk2ik_ntw)
        if listAttr == None or not 'fkmatch' in listAttr:
            cmds.addAttr(tag_fk2ik_ntw, ln='fkmatch', dt='string')

        listAttr = cmds.listAttr(tag_fk2ik_ntw)
        if listAttr == None or not 'ikfkmatchtag' in listAttr:
            cmds.addAttr(tag_fk2ik_ntw, ln='ikfkmatchtag', dt='string')

        cmds.sets(tag_fk2ik_ntw, add=tag_fk2ik_sets)
        cmds.sets(tag_fk2ik_sets, add=ikfk_match_sets)

        cmds.setAttr('{0}.ikmatch'.format(tag_fk2ik_ntw), ",".join(sel[1::2]), type='string')
        cmds.setAttr('{0}.fkmatch'.format(tag_fk2ik_ntw), ",".join(sel[::2]), type='string')
        cmds.setAttr('{0}.ikfkmatchtag'.format(tag_fk2ik_ntw), "{0}".format(tag), type='string')

        ikfk_state = tag_fk2ik_ntw

    elif ik_or_fk == 'ik':
        # add fk to ik sets select fk and ik, fk and ik, fk and ik, ,,,
        tag_ik2fk_sets = '{0}ik2fk_sets'.format(tag)
        if not cmds.objExists(tag_ik2fk_sets):
            cmds.sets(em=1, n=tag_ik2fk_sets)

        tag_ik2fk_ntw = '{0}ik2fk_ntw'.format(tag)
        if not cmds.objExists(tag_ik2fk_ntw):
            cmds.createNode('network', n=tag_ik2fk_ntw, ss=1)

        # ik
        listAttr = cmds.listAttr(tag_ik2fk_ntw)
        if listAttr == None or not 'ikctrlmatch' in listAttr:
            cmds.addAttr(tag_ik2fk_ntw, ln='ikctrlmatch', dt='string')

        listAttr = cmds.listAttr(tag_ik2fk_ntw)
        if listAttr == None or not 'ikpvmatch' in listAttr:
            cmds.addAttr(tag_ik2fk_ntw, ln='ikpvmatch', dt='string')

        listAttr = cmds.listAttr(tag_ik2fk_ntw)
        if listAttr == None or not 'ikmatch' in listAttr:
            cmds.addAttr(tag_ik2fk_ntw, ln='ikmatch', dt='string')

        # fk
        listAttr = cmds.listAttr(tag_ik2fk_ntw)
        if listAttr == None or not 'fkctrlmatch' in listAttr:
            cmds.addAttr(tag_ik2fk_ntw, ln='fkctrlmatch', dt='string')

        listAttr = cmds.listAttr(tag_ik2fk_ntw)
        if listAttr == None or not 'fkpvmatch' in listAttr:
            cmds.addAttr(tag_ik2fk_ntw, ln='fkpvmatch', dt='string')

        listAttr = cmds.listAttr(tag_ik2fk_ntw)
        if listAttr == None or not 'fkmatch' in listAttr:
            cmds.addAttr(tag_ik2fk_ntw, ln='fkmatch', dt='string')

        listAttr = cmds.listAttr(tag_ik2fk_ntw)
        if listAttr == None or not 'ikfkmatchtag' in listAttr:
            cmds.addAttr(tag_ik2fk_ntw, ln='ikfkmatchtag', dt='string')

        listAttr = cmds.listAttr(tag_ik2fk_ntw)
        if listAttr == None or not 'ikfkzeroout' in listAttr:
            cmds.addAttr(tag_ik2fk_ntw, ln='ikfkzeroout', dt='string')

        cmds.sets(tag_ik2fk_ntw, add=tag_ik2fk_sets)
        cmds.sets(tag_ik2fk_sets, add=ikfk_match_sets)

        cmds.setAttr('{0}.ikmatch'.format(tag_ik2fk_ntw), ",".join(sel[::2]), type='string')
        cmds.setAttr('{0}.fkmatch'.format(tag_ik2fk_ntw), ",".join(sel[1::2]), type='string')
        cmds.setAttr('{0}.ikfkmatchtag'.format(tag_ik2fk_ntw), "{0}".format(tag), type='string')
        if ikfkzeroout:
            cmds.setAttr('{0}.ikfkzeroout'.format(tag_ik2fk_ntw), '{0}'.format(",".join(ikfkzeroout)), type='string')

        ik2fk_ikctrls_matchstate = ['{0}:{1}'.format(ikctrl, ikctrl_state) for i, (ikctrl, ikctrl_state) in enumerate(zip(ik2fk_ikctrls, ik2fk_ikctrls_state))]

        cmds.setAttr('{0}.ikctrlmatch'.format(tag_ik2fk_ntw), ",".join(ik2fk_ikctrls_matchstate), type='string')
        cmds.setAttr('{0}.fkctrlmatch'.format(tag_ik2fk_ntw), ",".join(ik2fk_fkctrls), type='string')

        ik2fk_ikpvmatch_matchstate = ['{0}:{1}'.format(ikctrl, ikctrl_state) for i, (ikctrl, ikctrl_state) in enumerate(zip(ik2fk_ikpv, ik2fk_ikpv_state))]

        cmds.setAttr('{0}.ikpvmatch'.format(tag_ik2fk_ntw), ",".join(ik2fk_ikpvmatch_matchstate), type='string')
        cmds.setAttr('{0}.fkpvmatch'.format(tag_ik2fk_ntw), ",".join(ik2fk_fkpvctrls), type='string')

        ikfk_state = tag_ik2fk_ntw

    listAttr = cmds.listAttr(ikfk_state)
    if listAttr == None or not 'ikstate' in listAttr:
        cmds.addAttr(ikfk_state, ln='ikstate', dt='string')

    listAttr = cmds.listAttr(ikfk_state)
    if listAttr == None or not 'fkstate' in listAttr:
        cmds.addAttr(ikfk_state, ln='fkstate', dt='string')

    cmds.setAttr('{0}.ikstate'.format(ikfk_state), ",".join(state_ik_attr), type='string')
    cmds.setAttr('{0}.fkstate'.format(ikfk_state), ",".join(state_fk_attr), type='string')

# """
# Rig scene setup
# """
# arms_L fk2ik
"""
create_ikfkmatch_sets(sel=[u'proxy_shoulderL_fk_ctrl',
 u'proxy_shoulderL_jnt_ik_jnt',
 u'proxy_armL_fk_ctrl',
 u'proxy_armL_jnt_ik_jnt',
 u'proxy_forearmL_fk_ctrl',
 u'proxy_forearmL_jnt_ik_jnt',
 u'proxy_handL_fk_ctrl',
 u'proxy_handL_jnt_ik_jnt'], tag='arms_L_', ik_or_fk='fk', state_ik_attr=['arms_L_01_IKFKswitch.IKFK', '1'], state_fk_attr=['arms_L_01_IKFKswitch.IKFK', '0'])

# arms_L ik2fk
create_ikfkmatch_sets(sel=[u'proxy_shoulderL_autoRot_ctrl',u'proxy_shoulderL_fk_ctrl'], tag='arms_L_', ik_or_fk='ik',
                      ik2fk_ikctrls=[u'proxy_handL_jnt_ik_ctrl', u'proxy_armL_autoRot_ctrl'], ik2fk_ikctrls_state=['match_T', 'match_R'], ik2fk_fkctrls=['proxy_handL_fk_ctrl'],
                      ik2fk_ikpv=['proxy_forearmL_jnt_ik_pv_ctrl'], ik2fk_ikpv_state=['match_P'], ik2fk_fkpvctrls=[u'proxy_armL_fk_ctrl', u'proxy_forearmL_fk_ctrl', u'proxy_handL_fk_ctrl'],
                      state_ik_attr=['arms_L_01_IKFKswitch.IKFK', '1'], state_fk_attr=['arms_L_01_IKFKswitch.IKFK', '0'])


# legs_L fk2ik
create_ikfkmatch_sets(sel=[u'proxy_uplegL_fk_ctrl',
 u'proxy_uplegL_ik_jnt',
 u'proxy_legL_fk_ctrl',
 u'proxy_legL_ik_jnt',
 u'proxy_footL_fk_ctrl',
 u'proxy_footL_ik_jnt',
 u'proxy_toebaseL_fk_ctrl',
 u'proxy_toebaseL_ik_ctrl'], tag='legs_L_', ik_or_fk='fk', state_ik_attr=['legs_L_01_IKFKswitch.IKFK', '1'], state_fk_attr=['legs_L_01_IKFKswitch.IKFK', '0'])

# legs_L ik2fk
create_ikfkmatch_sets(sel=[u'proxy_footL_ik_ctrl',u'ikfk_match_loc_proxy_footL_jnt', u'proxy_toebaseL_ik_ctrl', u'proxy_toebaseL_fk_ctrl'], tag='legs_L_', ik_or_fk='ik',
                      ik2fk_ikctrls=[u'proxy_footL_ik_ctrl'], ik2fk_ikctrls_state=['match_T'], ik2fk_fkctrls=['proxy_footL_fk_ctrl'],
                      ik2fk_ikpv=['proxy_legL_ik_pv_ctrl'], ik2fk_ikpv_state=['match_P'], ik2fk_fkpvctrls=[u'proxy_uplegL_fk_ctrl', u'proxy_legL_fk_ctrl', u'proxy_footL_fk_ctrl'],
                      state_ik_attr=['legs_L_01_IKFKswitch.IKFK', '1'], state_fk_attr=['legs_L_01_IKFKswitch.IKFK', '0'])

# arms_R fk2ik
create_ikfkmatch_sets(sel=[u'proxy_shoulderR_fk_ctrl',
 u'proxy_shoulderR_jnt_ik_jnt',
 u'proxy_armR_fk_ctrl',
 u'proxy_armR_jnt_ik_jnt',
 u'proxy_forearmR_fk_ctrl',
 u'proxy_forearmR_jnt_ik_jnt',
 u'proxy_handR_fk_ctrl',
 u'proxy_handR_jnt_ik_jnt'], tag='arms_R_', ik_or_fk='fk', state_ik_attr=['arms_R_01_IKFKswitch.IKFK', '1'], state_fk_attr=['arms_R_01_IKFKswitch.IKFK', '0'])

# arms_R ik2fk
create_ikfkmatch_sets(sel=[u'proxy_shoulderR_autoRot_ctrl',u'proxy_shoulderR_fk_ctrl'], tag='arms_R_', ik_or_fk='ik',
                      ik2fk_ikctrls=[u'proxy_handR_jnt_ik_ctrl', u'proxy_armR_autoRot_ctrl'], ik2fk_ikctrls_state=['match_T', 'match_R'], ik2fk_fkctrls=['proxy_handR_fk_ctrl'],
                      ik2fk_ikpv=['proxy_forearmR_jnt_ik_pv_ctrl'], ik2fk_ikpv_state=['match_P'], ik2fk_fkpvctrls=[u'proxy_armR_fk_ctrl', u'proxy_forearmR_fk_ctrl', u'proxy_handR_fk_ctrl'],
                      state_ik_attr=['arms_R_01_IKFKswitch.IKFK', '1'], state_fk_attr=['arms_R_01_IKFKswitch.IKFK', '0'])


# legs_R fk2ik
create_ikfkmatch_sets(sel=[u'proxy_uplegR_fk_ctrl',
 u'proxy_uplegR_ik_jnt',
 u'proxy_legR_fk_ctrl',
 u'proxy_legR_ik_jnt',
 u'proxy_footR_fk_ctrl',
 u'proxy_footR_ik_jnt',
 u'proxy_toebaseR_fk_ctrl',
 u'proxy_toebaseR_ik_ctrl'], tag='legs_R_', ik_or_fk='fk', state_ik_attr=['legs_R_01_IKFKswitch.IKFK', '1'], state_fk_attr=['legs_R_01_IKFKswitch.IKFK', '0'])

# legs_R ik2fk
create_ikfkmatch_sets(sel=[u'proxy_footR_ik_ctrl',u'ikfk_match_loc_proxy_footR_jnt', u'proxy_toebaseR_ik_ctrl', u'proxy_toebaseR_fk_ctrl'], tag='legs_R_', ik_or_fk='ik',
                      ik2fk_ikctrls=[u'proxy_footR_ik_ctrl'], ik2fk_ikctrls_state=['match_T'], ik2fk_fkctrls=['proxy_footR_fk_ctrl'],
                      ik2fk_ikpv=['proxy_legR_ik_pv_ctrl'], ik2fk_ikpv_state=['match_P'], ik2fk_fkpvctrls=[u'proxy_uplegR_fk_ctrl', u'proxy_legR_fk_ctrl', u'proxy_footR_fk_ctrl'],
                      state_ik_attr=['legs_R_01_IKFKswitch.IKFK', '1'], state_fk_attr=['legs_R_01_IKFKswitch.IKFK', '0'])
"""

# """
# In Work Scene
# """

"""
tags = ['arms_L_', 'arms_R_', 'legs_L_', 'legs_R_']
fk_or_ik_list = ['ik', 'ik', 'ik', 'ik']

# tags = ['arms_R_', 'legs_L_', 'legs_R_']
# fk_or_ik_list = ['ik', 'ik', 'ik']

ns = get_current_namespaces()

fk2ik(tag='legs_R_', fk2ik_sets='fk2ik_sets', namespace='')
ik2fk(tag='legs_R_', ik2fk_sets='ik2fk_sets', pv_move=20, namespace='')

ik2fk(tag='arms_R_', ik2fk_sets='ik2fk_sets', pv_move=20, namespace='')
fk2ik(tag='arms_R_', fk2ik_sets='fk2ik_sets', namespace='ply00')
ik2fk(tag='arms_R_', ik2fk_sets='ik2fk_sets', pv_move=20, namespace='ply00')
fk2ik(tag='arms_R_', fk2ik_sets='fk2ik_sets', namespace='')


playbackSlider = True
pv_move = 20
matchbake(fk_or_ik_list=fk_or_ik_list, tags=tags, time_range=None, playbackSlider=playbackSlider, pv_move=pv_move, namespace='ply00')
"""
