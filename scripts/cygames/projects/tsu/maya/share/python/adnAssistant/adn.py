# -*- coding: utf-8 -*-
from __future__ import absolute_import

import pymel.core as pm
import maya.cmds as mc

import tsubasa.maya.rig.assistdrive as assistdrive


# ---- type
type = {'CR':'CopyRotate',
        'AR':'AxisRoll',
        'AB':'AxisRollBlend',
        'AM':'AxisMove',
        'RM':'RollMove',
        'YP':'YawPitchRotate',
        'RS':'RollScale'
        } 


# ------------------------------------------------------------------------------
def create_assistdrive_node(drive_type, driver, driven, name=None):
    """AssistDriveNodeを作成

    | CreateAssistDriveNodeコマンドがUndoできない

    :param str drive_type: AssistDriveNodeのタイプ
    :param str driver: ドライバノード名
    :param str driven: ドリブンノード名(補助骨)
    :param str name: 新規AssitDriveNodeノード名
    :return: 作成したAssistDriveNode名
    :rtype: str
    """

    mc.select(driver, driven, r=True)

    before = set(assistdrive.list_assistdrive_node())
    # mel.eval('CreateAssistDriveNode "{}"'.format(drive_type))
    mc.CreateAssistDriveNode(drive_type)
    after = set(assistdrive.list_assistdrive_node())
    diff = list(after - before)
    if diff:
        if name:
            name = mc.rename(diff[0], name)
        else:
            name = diff[0]
        return name
    else:
        return None



def showADE():
    assistdrive.AssistDriveEditorGUI().show()


def adn_refresh(driver=''):
    drv = pm.PyNode(driver)
    drv.r.set(drv.r.get())



def adn_select(tgt=''):
    adn = pm.PyNode(tgt)
    if pm.nodeType(adn) == 'AssistDriveNode':
        pm.select(tgt, r=True)
        return tgt.name()
    else:
        return False


def adn_input(adn=''):
    src = pm.listConnections(adn, s=True, d=False, p=False, c=False, t='transform')
    if src:
        return src[0]
    else:
        return False


def adn_output(adn=''):
    tgt = pm.listConnections(adn, s=False, d=True, p=False, c=False, t='transform')
    if tgt:
        return tgt[0]
    else:
        return False


def adn_type(adn=''):
    tgt = pm.PyNode(adn)
    typ = tgt.dt.get()
    return typ


def adn_commentField(adn=''):
    tgt = pm.PyNode(adn)
    cfv = tgt.cf.get()
    return cfv


def adn_getSelectedList(typ=''):
    vl  = []
    adl = ['CopyRotate', 'AxisRoll', 'AxisRollBlend', 
           'AxisMove', 'RollMove', 'YawPitchRotate', 'RollScale']
    for i in adl:
        if i == typ:
            vl.append(True)
        else:
            vl.append(False)
    return vl


def setOverrideColorIndex(tgt=''):
    tgt = pm.PyNode(tgt) 
    tgt.overrideEnabled.set(True)
    tgt.overrideColor.set(13)
    tgt.useOutlinerColor.set(1)
    tgt.outlinerColor.set(1.0,0.0,0.0)


def getAdnFromDelection():
    res = []
    for i in pm.selected(typ='joint'):
        adnList = pm.listConnections(i, s=True, c=False, d=False, p=False, t='AssistDriveNode')
        if adnList:
            for adn in adnList:
                res.append(adn.name())
    res = list(set(res))
    return res


# ------------------------------------------------------------------------------

def createLeftHip_adn():
    # ---- Left hip
    dvr = pm.PyNode('_012')
    pa  = dvr.getParent()
    dvn = pm.createNode('joint', n='_a12')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.side.set(1)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_hip')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def createRightHip_adn():
    # ---- Right hip
    dvr = pm.PyNode('_00e')
    pa  = dvr.getParent()
    dvn = pm.createNode('joint', n='_a0e')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.side.set(2)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_hip')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def createLeftKnee_adn():
    # ---- Left knee
    dvr = pm.PyNode('_013')
    pa  = dvr.getParent()
    dvn = pm.createNode('joint', n='_a13')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.side.set(1)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_knee')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def createRightKnee_adn():
    # ---- Right knee
    dvr = pm.PyNode('_00f')
    pa  = dvr.getParent()
    dvn = pm.createNode('joint', n='_a0f')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.side.set(2)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_knee')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def createLeftAnkle_adn():
    # ---- left ankle
    dvr = pm.PyNode('_014')
    pa  = dvr.getParent()
    dvn = pm.createNode('joint', n='_a14')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.side.set(1)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_ankle')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def createRightAnkle_adn():
    # ---- Right ankle
    dvr = pm.PyNode('_010')
    pa  = dvr.getParent()
    dvn = pm.createNode('joint', n='_a10')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.side.set(2)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_ankle')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def createLeftHipTwist_adn():
    # ---- Left hip twist
    adnd = {u'RollRate': -0.5, u'RollAxis2': 0.0, u'RollAxis1': 1.0, u'RollAxis0': 0.0}
    dvr = pm.PyNode('_012')
    pa  = dvr
    dvn = pm.createNode('joint', n='_a32')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, '_013', dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.side.set(1)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_hipTwist')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def createRightHipTwist_adn():
    # ---- Right hip twist
    adnd = {u'RollRate': -0.5, u'RollAxis2': 0.0, u'RollAxis1': 1.0, u'RollAxis0': 0.0}
    dvr = pm.PyNode('_00e')
    pa  = dvr
    dvn = pm.createNode('joint', n='_a22')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, '_00f', dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.side.set(2)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_hipTwist')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def createLeftAnkleTwist_adn():
    # ---- Left ankle twist
    adnd = {u'RollRate': 0.5, u'RollAxis2': 0.0, u'RollAxis1': 1.0, u'RollAxis0': 0.0}
    dvr = pm.PyNode('_014')
    pa  = dvr.getParent()
    dvn = pm.createNode('joint', n='_a33')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, pa, dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.side.set(1)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_ankleTwist')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def createRightAnkleTwist_adn():
    # ---- Right ankle twist
    adnd = {u'RollRate': 0.5, u'RollAxis2': 0.0, u'RollAxis1': 1.0, u'RollAxis0': 0.0}
    dvr = pm.PyNode('_010')
    pa  = dvr.getParent()
    dvn = pm.createNode('joint', n='_a23')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, pa, dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.side.set(2)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_ankleTwist')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def createNeckTwist_adn():
    adnd = {u'YawLimit1': 179.0, u'YawRate': 1.0, u'PitchRate': 1.0, u'RollType': 1, 
            u'PitchLimit1': 179.0, u'PitchLimit0': -179.0, u'YawLimit0': -179.0}
    dvr = pm.PyNode('_004')
    pa  = dvr.getParent()
    dvn = pm.createNode('joint', n='_a04')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.side.set(0)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_neck')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def createLeftClavicle_adn():
    # ---- Left clavicle 
    adnd = {u'EtcRate': 1.0, u'RollRate': 0.0, u'RollAxis2': 0.0, u'RollAxis1': 0.0, u'RollAxis0': 1.0}
    dvr = pm.PyNode('_00a')
    pa  = dvr.getParent()
    dvn = pm.createNode('joint', n='_a0a')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.side.set(1)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_clavicle')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def createRightClavicle_adn():
    # ---- Right clavicle 
    adnd = {u'EtcRate': 1.0, u'RollRate': 0.0, u'RollAxis2': 0.0, u'RollAxis1': 0.0, u'RollAxis0': 1.0}
    dvr = pm.PyNode('_006')
    pa  = dvr.getParent()
    dvn = pm.createNode('joint', n='_a06')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.side.set(2)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_clavicle')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def createLeftShoulder_adn():
    # ---- Left shoulder
    adnd = {u'EtcRate': 1.0, u'RollRate': 0.0, u'RollAxis2': 0.0, u'RollAxis1': 0.0, u'RollAxis0': 1.0}
    dvr = pm.PyNode('_00b')
    pa  = dvr.getParent()
    dvn = pm.createNode('joint', n='_a0b')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.side.set(1)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_shoulder')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def createRightShoulder_adn():
    # ---- Right shoulder
    adnd = {u'EtcRate': 1.0, u'RollRate': 0.0, u'RollAxis2': 0.0, u'RollAxis1': 0.0, u'RollAxis0': 1.0}
    dvr = pm.PyNode('_007')
    pa  = dvr.getParent()
    dvn = pm.createNode('joint', n='_a07')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.side.set(2)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_shoulder')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def createLeftElbow_adn():
    # ---- Left elbow
    adnd = {u'RollRate': 0.5, u'RollAxis2': 0.0, u'RollAxis1': 1.0, u'RollAxis0': 0.0}
    dvr = pm.PyNode('_00c')
    pa  = dvr.getParent()
    dvn = pm.createNode('joint', n='_a0c')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.side.set(1)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_elbow')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def createRightElbow_adn():
    # ---- Right elbow
    adnd = {u'RollRate': 0.5, u'RollAxis2': 0.0, u'RollAxis1': 1.0, u'RollAxis0': 0.0}
    dvr = pm.PyNode('_008')
    pa  = dvr.getParent()
    dvn = pm.createNode('joint', n='_a08')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.side.set(2)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_elbow')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def createLeftWrist_adn():
    # ---- Left wrist
    adnd = {u'RollRate': 1.0, u'RollAxis2': 0.0, u'RollAxis1': 0.0, u'RollAxis0': 1.0}
    dvr = pm.PyNode('_00d')
    pa  = dvr.getParent()
    dvn = pm.createNode('joint', n='_a0d')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.side.set(1)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_wrist')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def createRightWrist_adn():
    # ---- Right wrist
    adnd = {u'RollRate': 1.0, u'RollAxis2': 0.0, u'RollAxis1': 0.0, u'RollAxis0': 1.0}
    dvr = pm.PyNode('_009')
    pa  = dvr.getParent()
    dvn = pm.createNode('joint', n='_a09')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.side.set(2)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_wrist')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def createLeftShoulderTwist_adn():
    adnd = {u'RollRate': -0.5, u'RollAxis2': 0.0, u'RollAxis1': 0.0, u'RollAxis0': 1.0}
    dvr = pm.PyNode('_00b')
    pa  = dvr
    dvn = pm.createNode('joint', n='_a30')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, '_00c', dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.side.set(1)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_shoulderTwist')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def createRightShoulderTwist_adn():
    adnd = {u'RollRate': -0.5, u'RollAxis2': 0.0, u'RollAxis1': 0.0, u'RollAxis0': 1.0}
    dvr = pm.PyNode('_007')
    pa  = dvr
    dvn = pm.createNode('joint', n='_a20')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, '_008', dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.side.set(2)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_shoulderTwist')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def createLeftWristTwist_adn():
    # ---- Left wrist twist
    adnd = {u'RollRate': 0.5, u'RollAxis0': 1.0, u'RollAxis1': 0.0, u'RollAxis2': 0.0}
    dvr = pm.PyNode('_00d')
    pa  = dvr.getParent()
    dvn = pm.createNode('joint', n='_a21')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, pa, dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.side.set(1)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_wristTwist')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def createRightWristTwist_adn():
    # ---- Right wrist twist
    adnd = {u'RollRate': 0.5, u'RollAxis0': 1.0, u'RollAxis1': 0.0, u'RollAxis2': 0.0}
    dvr = pm.PyNode('_009')
    pa  = dvr.getParent()
    dvn = pm.createNode('joint', n='_a31')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, pa, dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.side.set(2)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_wristTwist')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn



# -----------------------------------------

def createLeftElbowBack_adn():
    # ---- Left elbow back
    adnd = {u'MoveRange0': 0.0, u'MoveRange1': 5.0, u'MoveLength': -5.0, u'MoveOffset1': 0.0, 
            u'MoveOffset0': 0.0, u'MoveOffset2': -2.0, u'MoveAxis1': 0.0, u'MoveAxis0': 0.0, 
            u'MoveAxis2': -1.0, u'RollAxis2': 0.0, u'RollAxis1': 1.0, u'RollAxis0': 0.0}
    dvr = pm.PyNode('_00c')
    if pm.objExists('_a0c'):
        pa = pm.PyNode('_a0c')
    else:
        pa = pm.PyNode('_00b')
    dvn = pm.createNode('joint', n='_a38')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.r.set(0,0,0)
    dvn.side.set(1)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_elbowBack')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def createRightElbowBack_adn():
    # ---- Right elbow back
    adnd = {u'MoveRange0': 0.0, u'MoveRange1': 5.0, u'MoveLength': 5.0, u'MoveOffset1': 0.0, 
            u'MoveOffset0': 0.0, u'MoveOffset2': -2.0, u'MoveAxis1': 0.0, u'MoveAxis0': 0.0, 
            u'MoveAxis2': -1.0, u'RollAxis2': 0.0, u'RollAxis1': 1.0, u'RollAxis0': 0.0}
    dvr = pm.PyNode('_008')
    if pm.objExists('_a08'):
        pa = pm.PyNode('_a08')
    else:
        pa = pm.PyNode('_007')
    dvn = pm.createNode('joint', n='_a28')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.r.set(0,0,0)
    dvn.side.set(2)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_elbowBack')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def createLeftElbowFront_adn():
    # ---- Left elbow front 
    adnd = {u'MoveRange0': 0.0, u'MoveRange1': 5.0, u'MoveLength': 5.0, u'MoveOffset1': 0.0, 
            u'MoveOffset0': 0.0, u'MoveOffset2': 2.0, u'MoveAxis1': 0.0, u'MoveAxis0': 0.0, 
            u'MoveAxis2': -1.0, u'RollAxis2': 0.0, u'RollAxis1': 1.0, u'RollAxis0': 0.0}
    dvr = pm.PyNode('_00c')
    pa  = pm.PyNode('_a0c')
    dvn = pm.createNode('joint', n='_a37')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.r.set(0,0,0)
    dvn.side.set(1)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_elbowFront')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def createRightElbowFront_adn():
    # ---- Right elbow front 
    adnd = {u'MoveRange0': -5.0, u'MoveRange1': 0.0, u'MoveLength': -5.0, u'MoveOffset1': 0.0, 
            u'MoveOffset0': 0.0, u'MoveOffset2': 2.0, u'MoveAxis1': 0.0, u'MoveAxis0': 0.0, 
            u'MoveAxis2': -1.0, u'RollAxis2': 0.0, u'RollAxis1': 1.0, u'RollAxis0': 0.0}
    dvr = pm.PyNode('_008')
    pa  = pm.PyNode('_a08')
    dvn = pm.createNode('joint', n='_a27')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.r.set(0,0,0)
    dvn.side.set(2)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_elbowFront')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def createLeftHipFront_adn():
    # ---- Left hip front
    adnd = {u'MoveRange0': 0.0, u'MoveRange1': 20.0, u'MoveLength': 20.0, u'MoveOffset1': 0.0, 
            u'MoveOffset0': 0.0, u'MoveOffset2': 7.5, u'MoveAxis1': -1.0, u'MoveAxis0': 0.0, 
            u'MoveAxis2': 1.0, u'RollAxis2': 0.0, u'RollAxis1': 0.0, u'RollAxis0': -1.0}
    dvr = pm.PyNode('_012')
    pa  = pm.PyNode('_a12')
    dvn = pm.createNode('joint', n='_a34')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.r.set(0,0,0)
    dvn.side.set(1)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_hipFront')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def createRightHipFront_adn():
    # ---- Right hip front
    adnd = {u'MoveRange0': 0.0, u'MoveRange1': 20.0, u'MoveLength': 20.0, u'MoveOffset1': 0.0, 
            u'MoveOffset0': 0.0, u'MoveOffset2': 7.5, u'MoveAxis1': -1.0, u'MoveAxis0': 0.0, 
            u'MoveAxis2': 1.0, u'RollAxis2': 0.0, u'RollAxis1': 0.0, u'RollAxis0': -1.0}
    dvr = pm.PyNode('_00e')
    pa  = pm.PyNode('_a0e')
    dvn = pm.createNode('joint', n='_a24')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.r.set(0,0,0)
    dvn.side.set(2)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_hipFront')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def createLeftHipSide_adn():
    # ---- Left hip side 
    adnd = {u'MoveRange0': 0.0, u'MoveRange1': 20.0, u'MoveLength': 20.0, u'MoveOffset1': 0.0, 
            u'MoveOffset0': 5.0, u'MoveOffset2': 0.0, u'MoveAxis1': -1.0, u'MoveAxis0': 1.0, 
            u'MoveAxis2': 0.0, u'RollAxis2': 1.0, u'RollAxis1': 0.0, u'RollAxis0': 0.0}
    dvr = pm.PyNode('_012')
    pa  = pm.PyNode('_a12')
    dvn = pm.createNode('joint', n='_a35')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.r.set(0,0,0)
    dvn.side.set(1)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_hipSide')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def createRightHipSide_adn():
    # ---- Right hip side 
    adnd = {u'MoveRange0': 0.0, u'MoveRange1': 20.0, u'MoveLength': 20.0, u'MoveOffset1': 0.0, 
            u'MoveOffset0': -5.0, u'MoveOffset2': 0.0, u'MoveAxis1': -1.0, u'MoveAxis0': -1.0, 
            u'MoveAxis2': 0.0, u'RollAxis2': -1.0, u'RollAxis1': 0.0, u'RollAxis0': 0.0}
    dvr = pm.PyNode('_00e')
    pa  = pm.PyNode('_a0e')
    dvn = pm.createNode('joint', n='_a25')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.r.set(0,0,0)
    dvn.side.set(2)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_hipSide')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def createLeftHipBack_adn():
    # ---- Left hip back
    adnd = {u'MoveRange0': 0.0, u'MoveRange1': 20.0, u'MoveLength': 20.0, u'MoveOffset1': 0.0, 
            u'MoveOffset0': 0.0, u'MoveOffset2': -10.0, u'MoveAxis1': -1.0, u'MoveAxis0': 0.0, 
            u'MoveAxis2': -1.0, u'RollAxis2': 0.0, u'RollAxis1': 0.0, u'RollAxis0': 1.0}
    dvr = pm.PyNode('_012')
    pa  = pm.PyNode('_a12')
    dvn = pm.createNode('joint', n='_a36')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.r.set(0,0,0)
    dvn.side.set(1)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_hipBack')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def createRightHipBack_adn():
    # ---- Right hip back
    adnd = {u'MoveRange0': 0.0, u'MoveRange1': 30.0, u'MoveLength': 30.0, u'MoveOffset1': 0.0, 
            u'MoveOffset0': 0.0, u'MoveOffset2': -10.0, u'MoveAxis1': -1.0, u'MoveAxis0': 0.0, 
            u'MoveAxis2': -1.0, u'RollAxis2': 0.0, u'RollAxis1': 0.0, u'RollAxis0': 1.0}
    dvr = pm.PyNode('_00e')
    pa  = pm.PyNode('_a0e')
    dvn = pm.createNode('joint', n='_a26')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.r.set(0,0,0)
    dvn.side.set(2)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_hipBack')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def createLeftKneeFront_adn():
    # ---- Left knee front
    adnd = {'RollAxis0':1.0, 'RollAxis1':0.0, 'RollAxis2':0.0, 'MoveAxis0':0.0, 'MoveAxis1':0.0, 'MoveAxis2':1.0, 
            'MoveOffset0':0.0, 'MoveOffset1':0.0, 'MoveOffset2':1.0, 'MoveLength':5.0, 'MoveRange0':0.0, 'MoveRange1':5.0}
    dvr = pm.PyNode('_013')
    if pm.objExists('_a13'):
        pa = pm.PyNode('_a13')
    else:
        pa = pm.PyNode('_012')
    dvn = pm.createNode('joint', n='_a39')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.r.set(0,0,0)
    dvn.side.set(1)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_kneeFront')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def createRightKneeFront_adn():
    # ---- Right knee front
    adnd = {'RollAxis0':1.0, 'RollAxis1':0.0, 'RollAxis2':0.0, 'MoveAxis0':0.0, 'MoveAxis1':0.0, 'MoveAxis2':1.0, 
            'MoveOffset0':0.0, 'MoveOffset1':0.0, 'MoveOffset2':1.0, 'MoveLength':5.0, 'MoveRange0':0.0, 'MoveRange1':5.0}
    dvr = pm.PyNode('_00f')
    if pm.objExists('_a0f'):
        pa = pm.PyNode('_a0f')
    else:
        pa = pm.PyNode('_00e')
    dvn = pm.createNode('joint', n='_a29')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.r.set(0,0,0)
    dvn.side.set(2)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_kneeFront')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn



def createLeftKneeUp_adn():
    # ---- Left knee Up
    adnd = {'RollAxis0':1.0, 'RollAxis1':0.0, 'RollAxis2':0.0, 'MoveAxis0':0.0, 'MoveAxis1':1.0, 'MoveAxis2':0.5, 
            'MoveOffset0':0.0, 'MoveOffset1':0.0, 'MoveOffset2':2.0, 'MoveLength':10.0, 'MoveRange0':0.0, 'MoveRange1':10.0}
    dvr = pm.PyNode('_013')
    pa  = pm.PyNode('_a13')
    dvn = pm.createNode('joint', n='_a3a')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.r.set(0,0,0)
    dvn.side.set(1)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_kneeUp')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def createRightKneeUp_adn():
    # ---- Right knee Up
    adnd = {'RollAxis0':1.0, 'RollAxis1':0.0, 'RollAxis2':0.0, 'MoveAxis0':0.0, 'MoveAxis1':1.0, 'MoveAxis2':0.5, 
            'MoveOffset0':0.0, 'MoveOffset1':0.0, 'MoveOffset2':2.0, 'MoveLength':10.0, 'MoveRange0':0.0, 'MoveRange1':10.0}
    dvr = pm.PyNode('_00f')
    pa  = pm.PyNode('_a0f')
    dvn = pm.createNode('joint', n='_a2a')
    # -- set driven
    pm.delete(pm.parentConstraint(dvr, dvn, mo=False))
    dvn.setParent(pa)
    dvn.jo.set(0,0,0)
    dvn.r.set(0,0,0)
    dvn.side.set(2)
    dvn.typ.set(18)
    dvn.otherType.set('ADN_kneeUp')
    dvn.radius.set(dvr.radius.get()*2)
    return dvn


def addJoint_adn():
    jtList = []
    jtList.append(createLeftHip_adn())
    jtList.append(createRightHip_adn())
    jtList.append(createLeftKnee_adn())
    jtList.append(createRightKnee_adn())
    jtList.append(createLeftAnkle_adn())
    jtList.append(createRightAnkle_adn())
    jtList.append(createLeftHipTwist_adn())
    jtList.append(createRightHipTwist_adn())
    jtList.append(createLeftAnkleTwist_adn())
    jtList.append(createRightAnkleTwist_adn())
    jtList.append(createNeckTwist_adn())
    jtList.append(createLeftClavicle_adn())
    jtList.append(createRightClavicle_adn())
    jtList.append(createLeftShoulder_adn())
    jtList.append(createRightShoulder_adn())
    jtList.append(createLeftElbow_adn())
    jtList.append(createRightElbow_adn())
    jtList.append(createLeftWrist_adn())
    jtList.append(createRightWrist_adn())
    jtList.append(createLeftShoulderTwist_adn())
    jtList.append(createRightShoulderTwist_adn())
    jtList.append(createLeftWristTwist_adn())
    jtList.append(createRightWristTwist_adn())
    jtList.append(createLeftElbowBack_adn())
    jtList.append(createRightElbowBack_adn())
    jtList.append(createLeftElbowFront_adn())
    jtList.append(createRightElbowFront_adn())
    jtList.append(createLeftHipFront_adn())
    jtList.append(createRightHipFront_adn())
    jtList.append(createLeftHipSide_adn())
    jtList.append(createRightHipSide_adn())
    jtList.append(createLeftHipBack_adn())
    jtList.append(createRightHipBack_adn())
    jtList.append(createLeftKneeFront_adn())
    jtList.append(createRightKneeFront_adn())
    jtList.append(createLeftKneeUp_adn())
    jtList.append(createRightKneeUp_adn())

    for dvn in jtList:
        # -- color
        dvn.overrideEnabled.set(True)
        dvn.overrideColor.set(13)
        dvn.useOutlinerColor.set(1)
        dvn.outlinerColor.set(1.0,0.0,0.0)


def addJoint_adn_npc():
    jtList = []
    jtList.append(createLeftHipTwist_adn())
    jtList.append(createRightHipTwist_adn())
    jtList.append(createLeftAnkleTwist_adn())
    jtList.append(createRightAnkleTwist_adn())
    jtList.append(createLeftShoulderTwist_adn())
    jtList.append(createRightShoulderTwist_adn())
    jtList.append(createLeftWristTwist_adn())
    jtList.append(createRightWristTwist_adn())
    jtList.append(createLeftElbowBack_adn())
    jtList.append(createRightElbowBack_adn())
    jtList.append(createLeftKneeFront_adn())
    jtList.append(createRightKneeFront_adn())


    for dvn in jtList:
        # -- color
        dvn.overrideEnabled.set(True)
        dvn.overrideColor.set(13)
        dvn.useOutlinerColor.set(1)
        dvn.outlinerColor.set(1.0,0.0,0.0)



def importDefaultADN(path=r''):
    assistdrive.import_assistdrive_settings(path)



