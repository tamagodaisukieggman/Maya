# -*- coding: utf-8 -*-
import maya.cmds as mc
import maya.mel as mm

# ui


def ui(*args):
    if mc.window('matchCtrlUI', ex=True):
        mc.deleteUI('matchCtrlUI')
    mc.window('matchCtrlUI', title='match control ui', w=100, h=100)
    mc.columnLayout()
    mc.radioButtonGrp('LRChkBox', numberOfRadioButtons=2,  label='ctrl type', labelArray2=['right', 'left'], select=1)
    mc.setParent('..')
    mc.frameLayout(collapsable=False, collapse=False, label=u'ネームスペースリスト :')
    mc.columnLayout()
    mc.button('getNss', label=u'ゲットネームスペースリスト', bgc=[0.112, 0.612, 0.562], en=True, c=getNss)
    mc.textScrollList('nameSpList', numberOfRows=20, w=250, h=50, en=True, allowMultiSelection=False)
    mc.setParent('..')
    mc.frameLayout(collapsable=True, collapse=False, label='IK FK Switcher :', w=300)
    mc.rowColumnLayout(numberOfColumns=3)
    mc.button(label='Match IK to FK', c=IKtoFKMatch)
    mc.text(label='                    ')
    """mc.button(label='Reset FK Controller',c=resetFKCtrl) 
    mc.separator(h=2,style='none')
    mc.separator(h=2,style='none')
    mc.separator(h=2,style='none')"""
    mc.button(label='Match FK to IK', c=FktoIKMatch)
    mc.text(label='                    ')
    """mc.button(label='Reset IK Controller',c=resetIKCtrl)"""
    mc.showWindow('matchCtrlUI')


# referenceのネームスペースを取得して、ネームスペースが１つのreferenceだったらnameSpaceListへ加える
def getNss(*args):
    mc.textScrollList('nameSpList', e=True, removeAll=True)
    rn = mc.ls(type='reference')
    ref1 = []
    for i in rn:
        list = i.split(":")
        count = len(list)
        if count == 1:
            for i in list:
                NSP = i.split("RN")
                print NSP[0]
                mc.textScrollList('nameSpList', edit=True, append=NSP[0])
    else:
        pass


def FktoIKMatch(*args):
    Nmsp = mc.textScrollList('nameSpList', q=True, si=True)
    Nmsp = Nmsp[0] + ':'
    side = mc.radioButtonGrp('LRChkBox', q=True, select=True)  # 1=right 2=left
    rightRotUpArm = mc.xform(Nmsp + 'rightArmIkJt', q=True, rotation=True)
    rightRotArm = mc.xform(Nmsp + 'rightForeArmIkJt', q=True, rotation=True)
    leftRotUpArm = mc.xform(Nmsp + 'leftArmIkJt', q=True, rotation=True)
    leftRotArm = mc.xform(Nmsp + 'leftForeArmIkJt', q=True, rotation=True)

    if side == 1:
        mc.setAttr(Nmsp + "upArm_R_fkCtrl" + ".rotate", rightRotUpArm[0], rightRotUpArm[1], rightRotUpArm[2], type="double3")
        mc.setAttr(Nmsp + "arm_R_fkCtrl" + ".rotate", rightRotArm[0], rightRotArm[1], rightRotArm[2], type="double3")
    else:
        mc.setAttr(Nmsp + "upArm_L_fkCtrl" + ".rotate", leftRotUpArm[0], leftRotUpArm[1], leftRotUpArm[2], type="double3")
        mc.setAttr(Nmsp + "arm_L_fkCtrl" + ".rotate", leftRotArm[0], leftRotArm[1], leftRotArm[2], type="double3")

 # proxyJointを介してpoleVectorの値を取得する


def IKtoFKMatch(*args):
    Nmsp = mc.textScrollList('nameSpList', q=True, si=True)
    Nmsp = Nmsp[0] + ':'
    side = mc.radioButtonGrp('LRChkBox', q=True, select=True)  # 1=right 2=left
    rightElbow = mc.xform(Nmsp + "rightElbowVectorPosProxyLocFk", q=True, t=True)
    rightWrist = mc.xform(Nmsp + "wristRCtrl_space", q=True, t=True)
    leftElbow = mc.xform(Nmsp + "leftElbowVectorPosProxyLocFk", q=True, t=True)
    leftWrist = mc.xform(Nmsp + "wristLCtrl_space", q=True, t=True)
    if side == 1:
        print rightElbow

        mc.setAttr(Nmsp + "arm_R_PBCtrl" + ".translate", *rightElbow)
        mc.setAttr(Nmsp + "hand_R_Ctrl" + ".translate", *rightWrist)
    else:
        mc.setAttr(Nmsp + "arm_L_PBCtrl" + ".translate", *leftElbow)
        mc.setAttr(Nmsp + "hand_L_Ctrl" + ".translate", *leftWrist)
    """def resetIKCtrl(*args):
    ikctrl=['handIKCtrlMatchConnector','handCtrl','L_hand_Upvector_Ctrl','L_hand_Upvector_Ctrl']
    for i in ikctrl:        
        mc.setAttr((i + '.translateX'),0)
        mc.setAttr((i + '.translateY'),0)
        mc.setAttr((i + '.translateZ'),0)
    constA=mc.pointConstraint('L_hand_Upvector_posIK','L_hand_UpvectorMatchConnectror',w=1,offset=(0,0,0))
    mc.delete(constA)
    def resetFKCtrl(*args):
    fkctrl=['upArmCtrlMatchConnector','upArmCtrl','armCtrlMatchConnector','armCtrl']
    for i in fkctrl:        
        mc.setAttr((i + '.rotateX'),0)
        mc.setAttr((i + '.rotateY'),0)
        mc.setAttr((i + '.rotateZ'),0)"""
ui()
