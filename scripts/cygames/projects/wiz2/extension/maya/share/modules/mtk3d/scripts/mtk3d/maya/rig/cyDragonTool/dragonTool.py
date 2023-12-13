# -*- coding: utf-8 -*-
import maya.cmds as mc
import re
import os
import maya.mel as mm


def envs(*args):
    lang = []
    append = lang.append

    for k, v in os.environ.items():
        if k == "MAYA_UI_LANGUAGE":
            append(v)
    return lang


def viewChange(*args):
    env = envs()
    if env:
        if env[0] == 'en_US':
            mm.eval('setNamedPanelLayout("Single Perspective View")')
            mc.modelPanel("modelPanel4", edit=True, up=True)
        elif env[0] == 'ja_JP':
            mm.eval(u'setNamedPanelLayout (u"単一のパース ビュー")')
            mc.modelPanel("modelPanel4", edit=True, up=True)
    else:
        mm.eval(u'setNamedPanelLayout (u"単一のパース ビュー")')
        mc.modelPanel("modelPanel4", edit=True, up=True)


def viewChangeEnd(*args):
    env = envs()
    if env:
        if env[0] == 'en_US':
            mm.eval('setNamedPanelLayout("Single Perspective View")')
        elif env[0] == 'ja_JP':
            mm.eval(u'setNamedPanelLayout (u"単一のパース ビュー")')

    else:
        mm.eval(u'setNamedPanelLayout (u"単一のパース ビュー")')


def ui(*args):
    if mc.window('dragonToolUI', ex=True):
        mc.deleteUI('dragonToolUI')
    mc.window('dragonToolUI', title='dragon tool ui', w=100, h=100)
    mc.columnLayout()
    group1 = mc.radioButtonGrp('LRChkBoxA', numberOfRadioButtons=2, label='Parts', labelArray2=['HandR', 'LegR'])
    mc.radioButtonGrp('LRChkBoxB', numberOfRadioButtons=2, shareCollection=group1, label='', labelArray2=['HandL', 'LegL'])
    mc.setParent('..')

    # name space 取得
    mc.frameLayout(collapsable=False, collapse=False, label=u'ネームスペースリスト :')
    mc.columnLayout()
    mc.button('getNss', label=u'ゲットネームスペースリスト', bgc=[0.112, 0.612, 0.562], en=True, c=getNss)
    mc.textScrollList('nameSpList', numberOfRows=20, w=250, h=50, en=True, allowMultiSelection=False)
    mc.setParent('..')

    # IK FK switch　
    mc.frameLayout(collapsable=True, collapse=False, label='IK FK Switcher :', w=300)
    mc.text(label=u' IK FKをそれぞれ合わせる  ', al="left")
    mc.rowColumnLayout(numberOfColumns=3)
    mc.button(label='FK>IK', c=FktoIKMatch, bgc=[0.112, 0.612, 0.562], h=70, w=125)
    mc.button(label='IK>FK', c=IKtoFKMatch, bgc=[0.112, 0.612, 0.562], h=70, w=125)
    mc.text(label='                    ')
    mc.setParent('..')

    # IK FK をSwitchしてベイクする
    mc.text(label=u' タイムスライダーの範囲をベイクする', al="left")
    mc.button(label='IK>FK Bake', c=fkToIkBake, bgc=[0.112, 0.612, 0.562], h=35, w=125)
    mc.button(label='FK>IK Bake', c=ikToFkBake, bgc=[0.112, 0.612, 0.562], h=35, w=125)
    mc.text(label='                    ')
    mc.setParent('..')

    # move controlをセットするのタイムレンジ分をベイクするもの
    mc.frameLayout(collapsable=True, collapse=False, label=u'set and bake move contrl :')
    mc.text(label=u' move controlをヒップ直下にセットする ', al="left")
    mc.radioButtonGrp('headSpineSwt', numberOfRadioButtons=3, label='', select=3, labelArray3=['Head', 'spine_02', 'spineAverage'])
    mc.checkBox("setRot", label='Rot', value=True)
    mc.rowColumnLayout(numberOfColumns=3)

    # mc.text(label='                    ')
    mc.rowColumnLayout(numberOfColumns=3)

    # mc.radioButtonGrp('timeOffset', numberOfRadioButtons=1, label='timeOffset')
    mc.text(label='frameOffset')
    mc.intFieldGrp("numnum", numberOfFields=1)
    mc.setParent('..')
    mc.setParent('..')

    mc.rowColumnLayout(numberOfColumns=3)

    mc.button(label='set', c=setMoveCtrlAnimation, bgc=[0.112, 0.612, 0.562], h=70, w=125)
    mc.button(label='bake', c=moveCtrlAnimationBake, bgc=[0.112, 0.612, 0.562], h=70, w=125)
    mc.text(label='                    ')

    mc.setParent('..')
    mc.setParent('..')

    # 背骨IK で調整したポーズをベースに戻す
    mc.frameLayout(collapsable=True, collapse=False, label='IK to Base :', w=300)
    mc.text(label=u' IK背骨調整コントローラーの値をベースへ適用する ', al="left")
    mc.rowColumnLayout(numberOfColumns=3)

    mc.button(label='IK to Base', c=matchIkTransToBase, bgc=[0.112, 0.612, 0.562], h=70, w=125)
    mc.text(label='                  ')
    mc.setParent('..')
    mc.text(label='                    ')

    mc.showWindow('dragonToolUI')


# referenceのネームスペースを取得して、ネームスペースが１つのreferenceだったらnameSpaceListへ加える
def getNss(*args):
    mc.textScrollList('nameSpList', e=True, removeAll=True)
    rn = mc.ls(type='reference')
    for i in rn:
        list = i.split(":")
        count = len(list)
        if count == 1:
            for i in list:
                NSP = i.split("RN")
                mc.textScrollList('nameSpList', edit=True, append=NSP[0])
    else:
        pass


def FktoIKMatch(*args):
    Nmsp = mc.textScrollList('nameSpList', q=True, si=True)
    Nmsp = Nmsp[0] + ':'
    sideA = mc.radioButtonGrp('LRChkBoxA', q=True, select=True)  # 1=right 2=left
    sideB = mc.radioButtonGrp('LRChkBoxB', q=True, select=True)  # 1=right 2=left

    # right arm-------------------------------------------------------------------------------------------------------------
    rightRotUpArm = mc.xform(Nmsp + 'arm_R_fkJtProxy', q=True, rotation=True)
    rightRotArm = mc.xform(Nmsp + 'foreArm_R_fkJtProxy', q=True, rotation=True)
    rightRotHand = mc.xform(Nmsp + 'hand_R_fkJtProxy', q=True, rotation=True)

    rightRotHandMid = mc.xform(Nmsp + "hand_R_RotBCtrl", q=True, rotation=True)

    rightHandFingerSp = mc.getAttr(Nmsp + "footF_R_RotCtrl.fingerSpred")
    rightHandFingerCl = mc.getAttr(Nmsp + "footF_R_RotCtrl.fingerClose")

    # right finger
    rightHandAuxAIkVal = mc.xform(Nmsp + "handAuxA_R_ikCtrl", q=True, rotation=True)
    rightHandAuxBIkVal = mc.xform(Nmsp + "handAuxB_R_ikCtrl", q=True, rotation=True)

    rightPinkyAIkVal = mc.xform(Nmsp + "handPinkyA_R_IkCtrl", q=True, rotation=True)
    rightPinkyBIkVal = mc.xform(Nmsp + "handPinkyB_R_IkCtrl", q=True, rotation=True)
    rightRingAIkVal = mc.xform(Nmsp + "handRingA_R_IkCtrl", q=True, rotation=True)
    rightRingBIkVal = mc.xform(Nmsp + "handRingB_R_IkCtrl", q=True, rotation=True)
    rightMiddleAIkVal = mc.xform(Nmsp + "handMiddleA_R_IkCtrl", q=True, rotation=True)
    rightMiddleBIkVal = mc.xform(Nmsp + "handMiddleB_R_IkCtrl", q=True, rotation=True)
    rightIndexAIkVal = mc.xform(Nmsp + "handIndexA_R_IkCtrl", q=True, rotation=True)
    rightIndexBIkVal = mc.xform(Nmsp + "handIndexB_R_IkCtrl", q=True, rotation=True)
    rightThumbAIkVal = mc.xform(Nmsp + "handThumbA_R_IkCtrl", q=True, rotation=True)

    # left arm------------------------------------------------------------------------------------------------------------------
    leftRotUpArm = mc.xform(Nmsp + 'arm_L_fkJtProxy', q=True, rotation=True)
    leftRotArm = mc.xform(Nmsp + 'foreArm_L_fkJtProxy', q=True, rotation=True)
    leftRotHand = mc.xform(Nmsp + 'hand_L_fkJtProxy', q=True, rotation=True)

    leftRotHandMid = mc.xform(Nmsp + "hand_L_RotBCtrl", q=True, rotation=True)

    leftHandFingerSp = mc.getAttr(Nmsp + "footF_L_RotCtrl.fingerSpred")
    leftHandFingerCl = mc.getAttr(Nmsp + "footF_L_RotCtrl.fingerClose")

    # left finger
    leftHandAuxAIkVal = mc.xform(Nmsp + "handAuxA_L_ikCtrl", q=True, rotation=True)
    leftHandAuxBIkVal = mc.xform(Nmsp + "handAuxB_L_ikCtrl", q=True, rotation=True)

    leftPinkyAIkVal = mc.xform(Nmsp + "handPinkyA_L_IkCtrl", q=True, rotation=True)
    leftPinkyBIkVal = mc.xform(Nmsp + "handPinkyB_L_IkCtrl", q=True, rotation=True)
    leftRingAIkVal = mc.xform(Nmsp + "handRingA_L_IkCtrl", q=True, rotation=True)
    leftRingBIkVal = mc.xform(Nmsp + "handRingB_L_IkCtrl", q=True, rotation=True)
    leftMiddleAIkVal = mc.xform(Nmsp + "handMiddleA_L_IkCtrl", q=True, rotation=True)
    leftMiddleBIkVal = mc.xform(Nmsp + "handMiddleB_L_IkCtrl", q=True, rotation=True)
    leftIndexAIkVal = mc.xform(Nmsp + "handIndexA_L_IkCtrl", q=True, rotation=True)
    leftIndexBIkVal = mc.xform(Nmsp + "handIndexB_L_IkCtrl", q=True, rotation=True)
    leftThumbAIkVal = mc.xform(Nmsp + "handThumbA_L_IkCtrl", q=True, rotation=True)

    # right upLeg-------------------------------------------------------------------------------------------------------------
    rightUpLeg = mc.xform(Nmsp + 'upLeg_R_fkJtProxy', q=True, rotation=True)
    rightLeg = mc.xform(Nmsp + 'leg_R_fkJtProxy', q=True, rotation=True)
    rightFoot = mc.xform(Nmsp + 'foot_R_fkJtProxy', q=True, rotation=True)
    rightToe = mc.xform(Nmsp + 'toeBase_R_fkJtProxy', q=True, rotation=True)

    rightLegFingerSp = mc.getAttr(Nmsp + "toe_R_BCtrl.fingerSpred")
    rightLegFingerCl = mc.getAttr(Nmsp + "toe_R_BCtrl.fingerClose")

    rightLegAuxAIkVal = mc.xform(Nmsp + "legAuxA_R_ikCtrl", q=True, rotation=True)
    rightLegAuxBIkVal = mc.xform(Nmsp + "legAuxB_R_ikCtrl", q=True, rotation=True)
    legRingAIkVal = mc.xform(Nmsp + "legRingA_R_IkCtrl", q=True, rotation=True)
    legRingBIkVal = mc.xform(Nmsp + "legRingB_R_IkCtrl", q=True, rotation=True)
    legMiddleAIkVal = mc.xform(Nmsp + "legMiddleA_R_IkCtrl", q=True, rotation=True)
    legMiddleBIkVal = mc.xform(Nmsp + "legMiddleB_R_IkCtrl", q=True, rotation=True)
    legIndexAIkVal = mc.xform(Nmsp + "legIndexA_R_IkCtrl", q=True, rotation=True)
    legIndexBIkVal = mc.xform(Nmsp + "legIndexB_R_IkCtrl", q=True, rotation=True)
    legThumbAIkVal = mc.xform(Nmsp + "legThumbA_R_IkCtrl", q=True, rotation=True)

    # left upLeg-------------------------------------------------------------------------------------------------------------
    leftUpLeg = mc.xform(Nmsp + 'upLeg_L_fkJtProxy', q=True, rotation=True)
    leftLeg = mc.xform(Nmsp + 'leg_L_fkJtProxy', q=True, rotation=True)
    leftFoot = mc.xform(Nmsp + 'foot_L_BfkJtProxy', q=True, rotation=True)
    leftToe = mc.xform(Nmsp + 'toe_L_BFkJtProxy', q=True, rotation=True)
    leftLegFingerSp = mc.getAttr(Nmsp + "toe_L_BCtrl.fingerSpred")
    leftLegFingerCl = mc.getAttr(Nmsp + "toe_L_BCtrl.fingerClose")

    leftLegAuxAIkVal = mc.xform(Nmsp + "legAuxA_L_ikCtrl", q=True, rotation=True)
    leftLegAuxBIkVal = mc.xform(Nmsp + "legAuxB_L_ikCtrl", q=True, rotation=True)
    legRingAIkVal = mc.xform(Nmsp + "legRingA_L_IkCtrl", q=True, rotation=True)
    legRingBIkVal = mc.xform(Nmsp + "legRingB_L_IkCtrl", q=True, rotation=True)
    legMiddleAIkVal = mc.xform(Nmsp + "legMiddleA_L_IkCtrl", q=True, rotation=True)
    legMiddleBIkVal = mc.xform(Nmsp + "legMiddleB_L_IkCtrl", q=True, rotation=True)
    legIndexAIkVal = mc.xform(Nmsp + "legIndexA_L_IkCtrl", q=True, rotation=True)
    legIndexBIkVal = mc.xform(Nmsp + "legIndexB_L_IkCtrl", q=True, rotation=True)
    legThumbAIkVal = mc.xform(Nmsp + "legThumbA_L_IkCtrl", q=True, rotation=True)

    # fk controllerを ikのコントローラーへ合わせるフェーズ----------------------------------------------------------------------------
    if sideB == 1:
        mc.setAttr(Nmsp + "arm_L_fkCtrl" + ".rotate", leftRotUpArm[0], leftRotUpArm[1], leftRotUpArm[2], type="double3")
        mc.setAttr(Nmsp + "foreArm_L_fkCtrl" + ".rotateY", leftRotArm[1])
        mc.setAttr(Nmsp + "hand_L_fkCtrl" + ".rotate", leftRotHand[0], leftRotHand[1], leftRotHand[2], type="double3")

        mc.setAttr(Nmsp + "hand_L_fkRotCtrl" + ".rotateY", leftRotHandMid[1] * -1)

        mc.setAttr(Nmsp + "hand_L_fkCtrl" + ".fingerSpred", leftHandFingerSp)
        mc.setAttr(Nmsp + "hand_L_fkCtrl" + ".fingerClose", leftHandFingerCl)

        mc.setAttr(Nmsp + "handAuxA_L_FkCtrl" + ".rotate", *leftHandAuxAIkVal)
        mc.setAttr(Nmsp + "handAuxB_L_FkCtrl" + ".rotate", *leftHandAuxBIkVal)

        mc.setAttr(Nmsp + "handPinkyA_L_FkCtrl.rotateY", leftPinkyAIkVal[1])
        mc.setAttr(Nmsp + "handPinkyA_L_FkCtrl.rotateZ", leftPinkyAIkVal[2])

        mc.setAttr(Nmsp + "handPinkyB_L_FkCtrl.rotateY", leftPinkyBIkVal[1])

        mc.setAttr(Nmsp + "handRingA_L_FkCtrl.rotateY", leftRingAIkVal[1])
        mc.setAttr(Nmsp + "handRingA_L_FkCtrl.rotateZ", leftRingAIkVal[2])

        mc.setAttr(Nmsp + "handRingB_L_FkCtrl.rotateY", leftRingBIkVal[1])

        mc.setAttr(Nmsp + "handMiddleA_L_FkCtrl.rotateY", leftMiddleAIkVal[1])
        mc.setAttr(Nmsp + "handMiddleA_L_FkCtrl.rotateZ", leftMiddleAIkVal[2])

        mc.setAttr(Nmsp + "handMiddleB_L_FkCtrl.rotateY", leftMiddleBIkVal[1])

        mc.setAttr(Nmsp + "handIndexA_L_FkCtrl.rotateY", leftIndexAIkVal[1])
        mc.setAttr(Nmsp + "handIndexA_L_FkCtrl.rotateZ", leftIndexAIkVal[2])

        mc.setAttr(Nmsp + "handIndexB_L_FkCtrl.rotateY", leftIndexBIkVal[1])

        mc.setAttr(Nmsp + "handThumbA_L_FkCtrl.rotateY", leftThumbAIkVal[1])
        mc.setAttr(Nmsp + "handThumbA_L_FkCtrl.rotateZ", leftThumbAIkVal[2])

    elif sideA == 1:
        mc.setAttr(Nmsp + "arm_R_fkCtrl" + ".rotate", rightRotUpArm[0], rightRotUpArm[1], rightRotUpArm[2], type="double3")
        mc.setAttr(Nmsp + "foreArm_R_fkCtrl" + ".rotateY", rightRotArm[1])
        mc.setAttr(Nmsp + "hand_R_fkCtrl" + ".rotate", rightRotHand[0], rightRotHand[1], rightRotHand[2], type="double3")

        mc.setAttr(Nmsp + "hand_R_fkRotCtrl" + ".rotateY", rightRotHandMid[1] * -1)

        mc.setAttr(Nmsp + "hand_R_fkCtrl" + ".fingerSpred", rightHandFingerSp)
        mc.setAttr(Nmsp + "hand_R_fkCtrl" + ".fingerClose", rightHandFingerCl)

        mc.setAttr(Nmsp + "handAuxA_R_FkCtrl" + ".rotate", *rightHandAuxAIkVal)
        mc.setAttr(Nmsp + "handAuxB_R_FkCtrl" + ".rotate", *rightHandAuxBIkVal)

        mc.setAttr(Nmsp + "handPinkyA_R_FkCtrl.rotateY", rightPinkyAIkVal[1])
        mc.setAttr(Nmsp + "handPinkyA_R_FkCtrl.rotateZ", rightPinkyAIkVal[2])

        mc.setAttr(Nmsp + "handPinkyB_R_FkCtrl.rotateY", rightPinkyBIkVal[1])

        mc.setAttr(Nmsp + "handRingA_R_FkCtrl.rotateY", rightRingAIkVal[1])
        mc.setAttr(Nmsp + "handRingA_R_FkCtrl.rotateZ", rightRingAIkVal[2])

        mc.setAttr(Nmsp + "handRingB_R_FkCtrl.rotateY", rightRingBIkVal[1])

        mc.setAttr(Nmsp + "handMiddleA_R_FkCtrl.rotateY", rightMiddleAIkVal[1])
        mc.setAttr(Nmsp + "handMiddleA_R_FkCtrl.rotateZ", rightMiddleAIkVal[2])

        mc.setAttr(Nmsp + "handMiddleB_R_FkCtrl.rotateY", rightMiddleBIkVal[1])

        mc.setAttr(Nmsp + "handIndexA_R_FkCtrl.rotateY", rightIndexAIkVal[1])
        mc.setAttr(Nmsp + "handIndexA_R_FkCtrl.rotateZ", rightIndexAIkVal[2])

        mc.setAttr(Nmsp + "handIndexB_R_FkCtrl.rotateY", rightIndexBIkVal[1])

        mc.setAttr(Nmsp + "handThumbA_R_FkCtrl.rotateY", rightThumbAIkVal[1])
        mc.setAttr(Nmsp + "handThumbA_R_FkCtrl.rotateZ", rightThumbAIkVal[2])

    elif sideB == 2:
        mc.setAttr(Nmsp + "upLeg_L_fkCtrl" + ".rotate", leftUpLeg[0], leftUpLeg[1], leftUpLeg[2], type="double3")
        mc.setAttr(Nmsp + "leg_L_fkCtrl" + ".rotateY", leftLeg[1])
        mc.setAttr(Nmsp + "foot_L_BFkCtrl" + ".rotate", leftFoot[0], leftFoot[1], leftFoot[2], type="double3")
        mc.setAttr(Nmsp + "toe_L_BFkCtrl" + ".rotate", leftToe[0], leftToe[1], leftToe[2], type="double3")

        mc.setAttr(Nmsp + "toe_L_BFkCtrl" + ".fingerSpred", leftLegFingerSp)
        mc.setAttr(Nmsp + "toe_L_BFkCtrl" + ".fingerClose", leftLegFingerCl)

        mc.setAttr(Nmsp + "legAuxA_L_FkCtrl" + ".rotate", *leftLegAuxAIkVal)
        mc.setAttr(Nmsp + "legAuxB_L_FkCtrl" + ".rotate", *leftLegAuxBIkVal)

        mc.setAttr(Nmsp + "legRingA_L_FkCtrl.rotateY", legRingAIkVal[1])
        mc.setAttr(Nmsp + "legRingA_L_FkCtrl.rotateZ", legRingAIkVal[2])

        mc.setAttr(Nmsp + "legRingB_L_FkCtrl.rotateY", legRingBIkVal[1])

        mc.setAttr(Nmsp + "legMiddleA_L_FkCtrl.rotateY", legMiddleAIkVal[1])
        mc.setAttr(Nmsp + "legMiddleA_L_FkCtrl.rotateZ", legMiddleAIkVal[2])

        mc.setAttr(Nmsp + "legMiddleB_L_FkCtrl.rotateY", legMiddleBIkVal[1])

        mc.setAttr(Nmsp + "legIndexA_L_FkCtrl.rotateY", legIndexAIkVal[1])
        mc.setAttr(Nmsp + "legIndexA_L_FkCtrl.rotateZ", legIndexAIkVal[2])

        mc.setAttr(Nmsp + "legIndexB_L_FkCtrl.rotateY", legIndexBIkVal[1])

        mc.setAttr(Nmsp + "legThumbA_L_FkCtrl.rotateY", legThumbAIkVal[1])
        mc.setAttr(Nmsp + "legThumbA_L_FkCtrl.rotateZ", legThumbAIkVal[2])

    elif sideA == 2:
        mc.setAttr(Nmsp + "upLeg_R_fkCtrl" + ".rotate", rightUpLeg[0], rightUpLeg[1], rightUpLeg[2], type="double3")
        mc.setAttr(Nmsp + "leg_R_fkCtrl" + ".rotateY", rightLeg[1])
        mc.setAttr(Nmsp + "foot_R_BFkCtrl" + ".rotate", rightFoot[0], rightFoot[1], rightFoot[2], type="double3")
        mc.setAttr(Nmsp + "toe_R_BFkCtrl" + ".rotate", rightToe[0], rightToe[1], rightToe[2], type="double3")

        mc.setAttr(Nmsp + "toe_R_BFkCtrl" + ".fingerSpred", rightLegFingerSp)
        mc.setAttr(Nmsp + "toe_R_BFkCtrl" + ".fingerClose", rightLegFingerCl)

        mc.setAttr(Nmsp + "legAuxA_R_FkCtrl" + ".rotate", *rightLegAuxAIkVal)
        mc.setAttr(Nmsp + "legAuxB_R_FkCtrl" + ".rotate", *rightLegAuxBIkVal)

        mc.setAttr(Nmsp + "legRingA_R_FkCtrl.rotateY", legRingAIkVal[1])
        mc.setAttr(Nmsp + "legRingA_R_FkCtrl.rotateZ", legRingAIkVal[2])

        mc.setAttr(Nmsp + "legRingB_R_FkCtrl.rotateY", legRingBIkVal[1])

        mc.setAttr(Nmsp + "legMiddleA_R_FkCtrl.rotateY", legMiddleAIkVal[1])
        mc.setAttr(Nmsp + "legMiddleA_R_FkCtrl.rotateZ", legMiddleAIkVal[2])

        mc.setAttr(Nmsp + "legMiddleB_R_FkCtrl.rotateY", legMiddleBIkVal[1])

        mc.setAttr(Nmsp + "legIndexA_R_FkCtrl.rotateY", legIndexAIkVal[1])
        mc.setAttr(Nmsp + "legIndexA_R_FkCtrl.rotateZ", legIndexAIkVal[2])

        mc.setAttr(Nmsp + "legIndexB_R_FkCtrl.rotateY", legIndexBIkVal[1])

        mc.setAttr(Nmsp + "legThumbA_R_FkCtrl.rotateY", legThumbAIkVal[1])
        mc.setAttr(Nmsp + "legThumbA_R_FkCtrl.rotateZ", legThumbAIkVal[2])


def IKtoFKMatch(*args):
    Nmsp = mc.textScrollList('nameSpList', q=True, si=True)
    Nmsp = Nmsp[0] + ':'
    sideA = mc.radioButtonGrp('LRChkBoxA', q=True, select=True)  # 1=right 2=left
    sideB = mc.radioButtonGrp('LRChkBoxB', q=True, select=True)  # 1=right 2=left

    # right arm ---------------------------------------------------------------------------
    rightArmTra = mc.xform(Nmsp + "arm_R_dummyCtrl", q=True, t=True)
    rightArmRot = mc.xform(Nmsp + "arm_R_dummyCtrl", q=True, ro=True)
    rightHandRot = mc.xform(Nmsp + "hand_R_fkCtrl", q=True, ro=True)
    rightArmPoleVec = mc.xform(Nmsp + "armF_R_dummyCtrl", q=True, t=True)

    rightHandRot = mc.xform(Nmsp + "hand_R_fkRotCtrl", q=True, ro=True)
    rightHandFingerSp = mc.getAttr(Nmsp + "hand_R_fkCtrl.fingerSpred")
    rightHandFingerCl = mc.getAttr(Nmsp + "hand_R_fkCtrl.fingerClose")

    # right finger
    rightHandAuxAFkVal = mc.xform(Nmsp + "handAuxA_R_FkCtrl", q=True, rotation=True)
    rightHandAuxBFkVal = mc.xform(Nmsp + "handAuxB_R_FkCtrl", q=True, rotation=True)

    rightPinkyAFkVal = mc.xform(Nmsp + "handPinkyA_R_FkCtrl", q=True, rotation=True)
    rightPinkyBFkVal = mc.xform(Nmsp + "handPinkyB_R_FkCtrl", q=True, rotation=True)
    rightRingAFkVal = mc.xform(Nmsp + "handRingA_R_FkCtrl", q=True, rotation=True)
    rightRingBFkVal = mc.xform(Nmsp + "handRingB_R_FkCtrl", q=True, rotation=True)
    rightMiddleAFkVal = mc.xform(Nmsp + "handMiddleA_R_FkCtrl", q=True, rotation=True)
    rightMiddleBFkVal = mc.xform(Nmsp + "handMiddleB_R_FkCtrl", q=True, rotation=True)
    rightIndexAFkVal = mc.xform(Nmsp + "handIndexA_R_FkCtrl", q=True, rotation=True)
    rightIndexBFkVal = mc.xform(Nmsp + "handIndexB_R_FkCtrl", q=True, rotation=True)
    rightThumbAFkVal = mc.xform(Nmsp + "handThumbA_R_FkCtrl", q=True, rotation=True)

    # left arm-----------------------------------------------------------------------------
    leftArmTra = mc.xform(Nmsp + "arm_L_dummyCtrl", q=True, t=True)
    leftArmRot = mc.xform(Nmsp + "arm_L_dummyCtrl", q=True, ro=True)
    leftHandRot = mc.xform(Nmsp + "hand_L_fkCtrl", q=True, ro=True)
    leftArmPoleVec = mc.xform(Nmsp + "armF_L_dummyCtrl", q=True, t=True)

    leftHandRot = mc.xform(Nmsp + "hand_L_fkRotCtrl", q=True, ro=True)
    leftHandFingerSp = mc.getAttr(Nmsp + "hand_L_fkCtrl.fingerSpred")
    leftHandFingerCl = mc.getAttr(Nmsp + "hand_L_fkCtrl.fingerClose")

    # left finger
    leftHandAuxAFkVal = mc.xform(Nmsp + "handAuxA_L_FkCtrl", q=True, rotation=True)
    leftHandAuxBFkVal = mc.xform(Nmsp + "handAuxB_L_FkCtrl", q=True, rotation=True)

    leftPinkyAFkVal = mc.xform(Nmsp + "handPinkyA_L_FkCtrl", q=True, rotation=True)
    leftPinkyBFkVal = mc.xform(Nmsp + "handPinkyB_L_FkCtrl", q=True, rotation=True)
    leftRingAFkVal = mc.xform(Nmsp + "handRingA_L_FkCtrl", q=True, rotation=True)
    leftRingBFkVal = mc.xform(Nmsp + "handRingB_L_FkCtrl", q=True, rotation=True)
    leftMiddleAFkVal = mc.xform(Nmsp + "handMiddleA_L_FkCtrl", q=True, rotation=True)
    leftMiddleBFkVal = mc.xform(Nmsp + "handMiddleB_L_FkCtrl", q=True, rotation=True)
    leftIndexAFkVal = mc.xform(Nmsp + "handIndexA_L_FkCtrl", q=True, rotation=True)
    leftIndexBFkVal = mc.xform(Nmsp + "handIndexB_L_FkCtrl", q=True, rotation=True)
    leftThumbAFkVal = mc.xform(Nmsp + "handThumbA_L_FkCtrl", q=True, rotation=True)

    # leftHandFkRot = mc.xform(Nmsp + "hand_L_fkRotCtrl",q=True,ro=True)

    zero = [0, 0, 0]

    # right leg----------------------------------------------------------------------------------
    rightFootTra = mc.xform(Nmsp + "foot_R_dummyCtrl", q=True, t=True)
    rightFootRot = mc.xform(Nmsp + "foot_R_dummyCtrl", q=True, ro=True)
    rightToeRot = mc.xform(Nmsp + "toe_R_BFkCtrlDummy", q=True, ro=True)
    rightLegPoleVec = mc.xform(Nmsp + "legPoleVec_R_dummyCtrl", q=True, t=True)

    rightLegFingerSp = mc.getAttr(Nmsp + "toe_R_BFkCtrl.fingerSpred")
    rightLegFingerCl = mc.getAttr(Nmsp + "toe_R_BFkCtrl.fingerClose")

    # right finger
    rightLegAuxAFkVal = mc.xform(Nmsp + "legAuxA_R_FkCtrl", q=True, rotation=True)
    rightLegAuxBFkVal = mc.xform(Nmsp + "legAuxB_R_FkCtrl", q=True, rotation=True)

    legRingARFkVal = mc.xform(Nmsp + "legRingA_R_FkCtrl", q=True, rotation=True)
    legRingBRFkVal = mc.xform(Nmsp + "legRingB_R_FkCtrl", q=True, rotation=True)
    legMiddleARFkVal = mc.xform(Nmsp + "legMiddleA_R_FkCtrl", q=True, rotation=True)
    legMiddleBRFkVal = mc.xform(Nmsp + "legMiddleB_R_FkCtrl", q=True, rotation=True)
    legIndexARFkVal = mc.xform(Nmsp + "legIndexA_R_FkCtrl", q=True, rotation=True)
    legIndexBRFkVal = mc.xform(Nmsp + "legIndexB_R_FkCtrl", q=True, rotation=True)
    legThumbARFkVal = mc.xform(Nmsp + "legThumbA_R_FkCtrl", q=True, rotation=True)

    # left leg----------------------------------------------------------------------------------
    leftFootTra = mc.xform(Nmsp + "foot_L_dummyCtrl", q=True, t=True)
    leftFootRot = mc.xform(Nmsp + "foot_L_dummyCtrl", q=True, ro=True)
    leftToeRot = mc.xform(Nmsp + "toe_L_BFkCtrlDummy", q=True, ro=True)
    leftLegPoleVec = mc.xform(Nmsp + "legPoleVec_L_dummyCtrl", q=True, t=True)

    leftLegFingerSp = mc.getAttr(Nmsp + "toe_L_BFkCtrl.fingerSpred")
    leftLegFingerCl = mc.getAttr(Nmsp + "toe_L_BFkCtrl.fingerClose")

    # left finger
    leftLegAuxAFkVal = mc.xform(Nmsp + "legAuxA_L_FkCtrl", q=True, rotation=True)
    leftLegAuxBFkVal = mc.xform(Nmsp + "legAuxB_L_FkCtrl", q=True, rotation=True)

    legRingALFkVal = mc.xform(Nmsp + "legRingA_L_FkCtrl", q=True, rotation=True)
    legRingBLFkVal = mc.xform(Nmsp + "legRingB_L_FkCtrl", q=True, rotation=True)
    legMiddleALFkVal = mc.xform(Nmsp + "legMiddleA_L_FkCtrl", q=True, rotation=True)
    legMiddleBLFkVal = mc.xform(Nmsp + "legMiddleB_L_FkCtrl", q=True, rotation=True)
    legIndexALFkVal = mc.xform(Nmsp + "legIndexA_L_FkCtrl", q=True, rotation=True)
    legIndexBLFkVal = mc.xform(Nmsp + "legIndexB_L_FkCtrl", q=True, rotation=True)
    legThumbALFkVal = mc.xform(Nmsp + "legThumbA_L_FkCtrl", q=True, rotation=True)

    # 値を与えるフェーズ------------------------------------------------------------------------------
    if sideA == 1:
        mc.setAttr(Nmsp + "footF_R_Ctrl" + ".translate",  *rightArmTra)
        mc.setAttr(Nmsp + "footF_R_Ctrl" + ".rotate", *rightArmRot)
        mc.setAttr(Nmsp + "hand_R_RotCtrl" + ".rotate", *zero)
        mc.setAttr(Nmsp + "footF_R_RotCtrl" + ".rotate", *zero)
        mc.setAttr(Nmsp + "arm_R_BPoleVectorCtrl" + ".translate", *rightArmPoleVec)
        mc.setAttr(Nmsp + "hand_R_RotBCtrl" + ".rotateY", rightHandRot[1] * -1)
        mc.setAttr(Nmsp + "footF_R_RotCtrl" + ".fingerSpred", rightHandFingerSp)
        mc.setAttr(Nmsp + "footF_R_RotCtrl" + ".fingerClose", rightHandFingerCl)

        # left ik finger
        mc.setAttr(Nmsp + "footF_R_RotCtrl" + ".fingerSpred", rightHandFingerSp)
        mc.setAttr(Nmsp + "footF_R_RotCtrl" + ".fingerClose", rightHandFingerCl)

        mc.setAttr(Nmsp + "handAuxA_R_ikCtrl" + ".rotate", *rightHandAuxAFkVal)
        mc.setAttr(Nmsp + "handAuxB_R_ikCtrl" + ".rotate", *rightHandAuxBFkVal)

        mc.setAttr(Nmsp + "handPinkyA_R_IkCtrl.rotateY", rightPinkyAFkVal[1])
        mc.setAttr(Nmsp + "handPinkyA_R_IkCtrl.rotateZ", rightPinkyAFkVal[2])

        mc.setAttr(Nmsp + "handPinkyB_R_IkCtrl.rotateY", rightPinkyBFkVal[1])

        mc.setAttr(Nmsp + "handRingA_R_IkCtrl.rotateY", rightRingAFkVal[1])
        mc.setAttr(Nmsp + "handRingA_R_IkCtrl.rotateZ", rightRingAFkVal[2])

        mc.setAttr(Nmsp + "handRingB_R_IkCtrl.rotateY", rightRingBFkVal[1])

        mc.setAttr(Nmsp + "handMiddleA_R_IkCtrl.rotateY", rightMiddleAFkVal[1])
        mc.setAttr(Nmsp + "handMiddleA_R_IkCtrl.rotateZ", rightMiddleAFkVal[2])

        mc.setAttr(Nmsp + "handMiddleB_R_IkCtrl.rotateY", rightMiddleBFkVal[1])

        mc.setAttr(Nmsp + "handIndexA_R_IkCtrl.rotateY", rightIndexAFkVal[1])
        mc.setAttr(Nmsp + "handIndexA_R_IkCtrl.rotateZ", rightIndexAFkVal[2])

        mc.setAttr(Nmsp + "handIndexB_R_IkCtrl.rotateY", rightIndexBFkVal[1])

        mc.setAttr(Nmsp + "handThumbA_R_IkCtrl.rotateY", rightThumbAFkVal[1])
        mc.setAttr(Nmsp + "handThumbA_R_IkCtrl.rotateZ", rightThumbAFkVal[2])

    # left ik arm-----------------------------------------------------------------------------
    elif sideB == 1:
        mc.setAttr(Nmsp + "footF_L_Ctrl" + ".translate",  *leftArmTra)
        mc.setAttr(Nmsp + "footF_L_Ctrl" + ".rotate", *leftArmRot)
        mc.setAttr(Nmsp + "hand_L_RotCtrl" + ".rotate", *zero)
        mc.setAttr(Nmsp + "footF_L_RotCtrl" + ".rotate", *zero)
        mc.setAttr(Nmsp + "arm_L_BPoleVectorCtrl" + ".translate", *leftArmPoleVec)
        mc.setAttr(Nmsp + "hand_L_RotBCtrl" + ".rotateY", leftHandRot[1] * -1)
        mc.setAttr(Nmsp + "footF_L_RotCtrl" + ".fingerSpred", leftHandFingerSp)
        mc.setAttr(Nmsp + "footF_L_RotCtrl" + ".fingerClose", leftHandFingerCl)

        # left ik finger
        mc.setAttr(Nmsp + "footF_L_RotCtrl" + ".fingerSpred", leftHandFingerSp)
        mc.setAttr(Nmsp + "footF_L_RotCtrl" + ".fingerClose", leftHandFingerCl)

        mc.setAttr(Nmsp + "handAuxA_L_ikCtrl" + ".rotate", *leftHandAuxAFkVal)
        mc.setAttr(Nmsp + "handAuxB_L_ikCtrl" + ".rotate", *leftHandAuxBFkVal)

        mc.setAttr(Nmsp + "handPinkyA_L_IkCtrl.rotateY", leftPinkyAFkVal[1])
        mc.setAttr(Nmsp + "handPinkyA_L_IkCtrl.rotateZ", leftPinkyAFkVal[2])

        mc.setAttr(Nmsp + "handPinkyB_L_IkCtrl.rotateY", leftPinkyBFkVal[1])

        mc.setAttr(Nmsp + "handRingA_L_IkCtrl.rotateY", leftRingAFkVal[1])
        mc.setAttr(Nmsp + "handRingA_L_IkCtrl.rotateZ", leftRingAFkVal[2])

        mc.setAttr(Nmsp + "handRingB_L_IkCtrl.rotateY", leftRingBFkVal[1])

        mc.setAttr(Nmsp + "handMiddleA_L_IkCtrl.rotateY", leftMiddleAFkVal[1])
        mc.setAttr(Nmsp + "handMiddleA_L_IkCtrl.rotateZ", leftMiddleAFkVal[2])

        mc.setAttr(Nmsp + "handMiddleB_L_IkCtrl.rotateY", leftMiddleBFkVal[1])

        mc.setAttr(Nmsp + "handIndexA_L_IkCtrl.rotateY", leftIndexAFkVal[1])
        mc.setAttr(Nmsp + "handIndexA_L_IkCtrl.rotateZ", leftIndexAFkVal[2])

        mc.setAttr(Nmsp + "handIndexB_L_IkCtrl.rotateY", leftIndexBFkVal[1])

        mc.setAttr(Nmsp + "handThumbA_L_IkCtrl.rotateY", leftThumbAFkVal[1])
        mc.setAttr(Nmsp + "handThumbA_L_IkCtrl.rotateZ", leftThumbAFkVal[2])

    # right ik leg ------------------------------------------------------------------------------
    elif sideA == 2:
        mc.setAttr(Nmsp + "foot_R_Ctrl" + ".translate",  *rightFootTra)
        mc.setAttr(Nmsp + "foot_R_Ctrl" + ".rotate", *rightFootRot)
        mc.setAttr(Nmsp + "toe_R_BCtrl" + ".rotate", *rightToeRot)
        mc.setAttr(Nmsp + "leg_R_BCtrl" + ".rotate", *zero)
        mc.setAttr(Nmsp + "leg_R_BPoleVectorCtrl" + ".translate", *rightLegPoleVec)

        mc.setAttr(Nmsp + "toe_R_BCtrl" + ".fingerSpred", rightLegFingerSp)
        mc.setAttr(Nmsp + "toe_R_BCtrl" + ".fingerClose", rightLegFingerCl)

        mc.setAttr(Nmsp + "legAuxA_R_ikCtrl" + ".rotate", *rightLegAuxAFkVal)
        mc.setAttr(Nmsp + "legAuxB_R_ikCtrl" + ".rotate", *rightLegAuxBFkVal)

        mc.setAttr(Nmsp + "legRingA_R_IkCtrl.rotateY", legRingARFkVal[1])
        mc.setAttr(Nmsp + "legRingA_R_IkCtrl.rotateZ", legRingARFkVal[2])

        mc.setAttr(Nmsp + "legRingB_R_IkCtrl.rotateY", legRingBRFkVal[1])

        mc.setAttr(Nmsp + "legMiddleA_R_IkCtrl.rotateY", legMiddleARFkVal[1])
        mc.setAttr(Nmsp + "legMiddleA_R_IkCtrl.rotateZ", legMiddleARFkVal[2])

        mc.setAttr(Nmsp + "legMiddleB_R_IkCtrl.rotateY", legMiddleBRFkVal[1])

        mc.setAttr(Nmsp + "legIndexA_R_IkCtrl.rotateY", legIndexARFkVal[1])
        mc.setAttr(Nmsp + "legIndexA_R_IkCtrl.rotateZ", legIndexARFkVal[2])

        mc.setAttr(Nmsp + "legIndexB_R_IkCtrl.rotateY", legIndexBRFkVal[1])

        mc.setAttr(Nmsp + "legThumbA_R_IkCtrl.rotateY", legThumbARFkVal[1])
        mc.setAttr(Nmsp + "legThumbA_R_IkCtrl.rotateZ", legThumbARFkVal[2])

    # left ik leg  -------------------------------------------------------------------------------------
    elif sideB == 2:
        mc.setAttr(Nmsp + "foot_L_Ctrl" + ".translate",  *leftFootTra)
        mc.setAttr(Nmsp + "foot_L_Ctrl" + ".rotate", *leftFootRot)
        mc.setAttr(Nmsp + "toe_L_BCtrl" + ".rotate", *leftToeRot)
        mc.setAttr(Nmsp + "leg_L_BCtrl" + ".rotate", *zero)
        mc.setAttr(Nmsp + "leg_L_BPoleVectorCtrl" + ".translate", *leftLegPoleVec)

        mc.setAttr(Nmsp + "toe_L_BCtrl" + ".fingerSpred", leftLegFingerSp)
        mc.setAttr(Nmsp + "toe_L_BCtrl" + ".fingerClose", leftLegFingerCl)

        mc.setAttr(Nmsp + "legAuxA_L_ikCtrl" + ".rotate", *leftLegAuxAFkVal)
        mc.setAttr(Nmsp + "legAuxB_L_ikCtrl" + ".rotate", *leftLegAuxBFkVal)

        mc.setAttr(Nmsp + "legRingA_L_IkCtrl.rotateY", legRingALFkVal[1])
        mc.setAttr(Nmsp + "legRingA_L_IkCtrl.rotateZ", legRingALFkVal[2])

        mc.setAttr(Nmsp + "legRingB_L_IkCtrl.rotateY", legRingBLFkVal[1])

        mc.setAttr(Nmsp + "legMiddleA_L_IkCtrl.rotateY", legMiddleALFkVal[1])
        mc.setAttr(Nmsp + "legMiddleA_L_IkCtrl.rotateZ", legMiddleALFkVal[2])

        mc.setAttr(Nmsp + "legMiddleB_L_IkCtrl.rotateY", legMiddleBLFkVal[1])

        mc.setAttr(Nmsp + "legIndexA_L_IkCtrl.rotateY", legIndexALFkVal[1])
        mc.setAttr(Nmsp + "legIndexA_L_IkCtrl.rotateZ", legIndexALFkVal[2])

        mc.setAttr(Nmsp + "legIndexB_L_IkCtrl.rotateY", legIndexBLFkVal[1])

        mc.setAttr(Nmsp + "legThumbA_L_IkCtrl.rotateY", legThumbALFkVal[1])
        mc.setAttr(Nmsp + "legThumbA_L_IkCtrl.rotateZ", legThumbALFkVal[2])


def fkToIkBake(*args):
    viewChange()
    Nmsp = mc.textScrollList('nameSpList', q=True, si=True)
    Nmsp = Nmsp[0] + ':'
    sideA = mc.radioButtonGrp('LRChkBoxA', q=True, select=True)  # 1=right 2=left
    sideB = mc.radioButtonGrp('LRChkBoxB', q=True, select=True)  # 1=right 2=left

    leftFkArm = [Nmsp + "arm_L_fkCtrl", Nmsp + "foreArm_L_fkCtrl", Nmsp + "hand_L_fkCtrl", Nmsp + "handPinkyA_L_FkCtrl", Nmsp + "handPinkyB_L_FkCtrl", Nmsp + "handRingA_L_FkCtrl",
                 Nmsp + "handRingB_L_FkCtrl", Nmsp + "handMiddleA_L_FkCtrl", Nmsp + "handMiddleB_L_FkCtrl", Nmsp + "handIndexA_L_FkCtrl", Nmsp + "handIndexB_L_FkCtrl", Nmsp + "handThumbA_L_FkCtrl", Nmsp + "hand_L_fkRotCtrl",
                 Nmsp + 'handAuxA_L_FkCtrl', Nmsp + 'handAuxB_L_FkCtrl']

    rightFkArm = [Nmsp + "arm_R_fkCtrl", Nmsp + "foreArm_R_fkCtrl", Nmsp + "hand_R_fkCtrl", Nmsp + "handPinkyA_R_FkCtrl", Nmsp + "handPinkyB_R_FkCtrl", Nmsp + "handRingA_R_FkCtrl",
                  Nmsp + "handRingB_R_FkCtrl", Nmsp + "handMiddleA_R_FkCtrl", Nmsp + "handMiddleB_R_FkCtrl", Nmsp + "handIndexA_R_FkCtrl", Nmsp + "handIndexB_R_FkCtrl", Nmsp + "handThumbA_R_FkCtrl", Nmsp + "hand_R_fkRotCtrl",
                  Nmsp + 'handAuxA_R_FkCtrl', Nmsp + 'handAuxB_R_FkCtrl']

    leftFkLeg = [Nmsp + "upLeg_L_fkCtrl", Nmsp + "leg_L_fkCtrl", Nmsp + "foot_L_BFkCtrl", Nmsp + "toe_L_BFkCtrl",
                 Nmsp + "legThumbA_L_FkCtrl", Nmsp + "legIndexA_L_FkCtrl", Nmsp + "legIndexB_L_FkCtrl", Nmsp + "legMiddleA_L_FkCtrl",
                 Nmsp + "legMiddleB_L_FkCtrl", Nmsp + "legRingA_L_FkCtrl", Nmsp + "legRingB_L_FkCtrl",
                 Nmsp + 'legAuxA_L_FkCtrl', Nmsp + ':legAuxB_L_FkCtrl']

    rightFkLeg = [Nmsp + "upLeg_R_fkCtrl", Nmsp + "leg_R_fkCtrl", Nmsp + "foot_R_BFkCtrl", Nmsp + "toe_R_BFkCtrl",
                  Nmsp + "legThumbA_R_FkCtrl", Nmsp + "legIndexA_R_FkCtrl", Nmsp + "legIndexB_R_FkCtrl", Nmsp + "legMiddleA_R_FkCtrl",
                  Nmsp + "legMiddleB_R_FkCtrl", Nmsp + "legRingA_R_FkCtrl", Nmsp + "legRingB_R_FkCtrl",
                  Nmsp + 'legAuxA_R_FkCtrl', Nmsp + ':legAuxB_R_FkCtrl']

    sF = mc.playbackOptions(q=True, minTime=True)
    eF = mc.playbackOptions(q=True, maxTime=True)
    eF = eF + 2

    if sideA == 1:
        for j in xrange(int(sF), int(eF), 1):  # noqa
            FktoIKMatch()
            for i in rightFkArm:
                mc.setKeyframe(i)
            mc.currentTime(int(j), e=True)

    elif sideB == 1:
        for j in xrange(int(sF), int(eF), 1):  # noqa
            FktoIKMatch()
            for i in leftFkArm:
                mc.setKeyframe(i)
            mc.currentTime(int(j), e=True)

    elif sideA == 2:
        for j in xrange(int(sF), int(eF), 1):  # noqa
            FktoIKMatch()
            for i in rightFkLeg:
                mc.setKeyframe(i)
            mc.currentTime(int(j), e=True)

    elif sideB == 2:
        for j in xrange(int(sF), int(eF), 1):  # noqa
            FktoIKMatch()
            for i in leftFkLeg:
                mc.setKeyframe(i)
            mc.currentTime(int(j), e=True)
    viewChangeEnd()


def ikToFkBake(*args):
    viewChange()
    Nmsp = mc.textScrollList('nameSpList', q=True, si=True)
    Nmsp = Nmsp[0] + ':'
    sideA = mc.radioButtonGrp('LRChkBoxA', q=True, select=True)  # 1=right 2=left
    sideB = mc.radioButtonGrp('LRChkBoxB', q=True, select=True)  # 1=right 2=left

    leftIkArm = [Nmsp + 'footF_L_Ctrl', Nmsp + 'handPinkyA_L_IkCtrl', Nmsp + 'handPinkyB_L_IkCtrl', Nmsp + 'handRingA_L_IkCtrl',
                 Nmsp + 'handRingB_L_IkCtrl', Nmsp + 'handMiddleA_L_IkCtrl', Nmsp + 'handMiddleB_L_IkCtrl', Nmsp + 'handIndexA_L_IkCtrl',
                 Nmsp + 'handIndexB_L_IkCtrl', Nmsp + 'handThumbA_L_IkCtrl', Nmsp + 'hand_L_RotCtrl', Nmsp + 'hand_L_RotBCtrl', Nmsp + 'footF_L_RotCtrl',
                 Nmsp + 'handAuxA_L_ikCtrl', Nmsp + 'handAuxB_L_ikCtrl']

    rightIkArm = [Nmsp + 'footF_R_Ctrl', Nmsp + 'handPinkyA_R_IkCtrl', Nmsp + 'handPinkyB_R_IkCtrl', Nmsp + 'handRingA_R_IkCtrl',
                  Nmsp + 'handRingB_R_IkCtrl', Nmsp + 'handMiddleA_R_IkCtrl', Nmsp + 'handMiddleB_R_IkCtrl', Nmsp + 'handIndexA_R_IkCtrl',
                  Nmsp + 'handIndexB_R_IkCtrl', Nmsp + 'handThumbA_R_IkCtrl', Nmsp + 'hand_R_RotCtrl', Nmsp + 'hand_R_RotBCtrl', Nmsp + 'footF_R_RotCtrl',
                  Nmsp + 'handAuxA_R_ikCtrl', Nmsp + 'handAuxB_R_ikCtrl']

    leftIkLeg = [Nmsp + 'foot_L_Ctrl',  Nmsp + ' leg_L_BCtrl',  Nmsp + ' toe_L_BCtrl',  Nmsp + ' legThumbA_L_IkCtrl',
                 Nmsp + 'legIndexA_L_IkCtrl',  Nmsp + ' legIndexB_L_IkCtrl',  Nmsp + ' legMiddleA_L_IkCtrl',
                 Nmsp + 'legMiddleB_L_IkCtrl',  Nmsp + ' legRingA_L_IkCtrl',  Nmsp + ' legRingB_L_IkCtrl',
                 Nmsp + 'legAuxA_L_ikCtrl', Nmsp + 'legAuxB_L_ikCtrl']

    rightIkLeg = [Nmsp + 'foot_R_Ctrl',  Nmsp + ' leg_R_BCtrl',  Nmsp + ' toe_R_BCtrl',  Nmsp + ' legThumbA_R_IkCtrl',
                  Nmsp + 'legIndexA_R_IkCtrl',  Nmsp + ' legIndexB_R_IkCtrl',  Nmsp + ' legMiddleA_R_IkCtrl',
                  Nmsp + 'legMiddleB_R_IkCtrl',  Nmsp + ' legRingA_R_IkCtrl',  Nmsp + ' legRingB_R_IkCtrl',
                  Nmsp + 'legAuxA_R_ikCtrl', Nmsp + 'legAuxB_R_ikCtrl']

    sF = mc.playbackOptions(q=True, minTime=True)
    eF = mc.playbackOptions(q=True, maxTime=True)
    eF = eF + 2

    if sideA == 1:
        for j in xrange(int(sF), int(eF), 1):  # noqa
            IKtoFKMatch()
            for i in rightIkArm:
                mc.setKeyframe(i)
            mc.currentTime(int(j), e=True)

    elif sideB == 1:
        for j in xrange(int(sF), int(eF), 1):  # noqa
            IKtoFKMatch()
            for i in leftIkArm:
                mc.setKeyframe(i)
            mc.currentTime(int(j), e=True)

    elif sideA == 2:
        for j in xrange(int(sF), int(eF), 1):  # noqa
            IKtoFKMatch()
            for i in rightIkLeg:
                mc.setKeyframe(i)
            mc.currentTime(int(j), e=True)

    elif sideB == 2:
        for j in xrange(int(sF), int(eF), 1):  # noqa
            IKtoFKMatch()
            for i in leftIkLeg:
                mc.setKeyframe(i)
            mc.currentTime(int(j), e=True)
    viewChangeEnd()


def matchIkTransToBase(*args):

    Nmsp = mc.textScrollList('nameSpList', q=True, si=True)
    Nmsp = Nmsp[0] + ':'
    p = re.compile("(.*)(_rig)(.)")
    m = p.match(Nmsp)
    NmspB = m.group(1) + m.group(3)

    spine00Val = mc.xform(Nmsp + "spine_00Proxy", ro=True, q=True)
    spine01Val = mc.xform(Nmsp + NmspB + "spine_01", ro=True, q=True)
    spine02Val = mc.xform(Nmsp + NmspB + "spine_02", ro=True, q=True)
    neck00Val = mc.xform(Nmsp + NmspB + "neck_00", ro=True, q=True)
    neck01Val = mc.xform(Nmsp + NmspB + "neck_01", ro=True, q=True)
    headVal = mc.xform(Nmsp + NmspB + "head", ro=True, q=True)

    spine00 = []
    spine01 = []
    spine02 = []
    neck00 = []
    neck01 = []
    head = []

    for i in spine00Val:
        i = round(i, 3)
        spine00.append(i)
    # print spine00

    for i in spine01Val:
        i = round(i, 3)
        spine01.append(i)
    # print spine01

    for i in spine02Val:
        i = round(i, 3)
        spine02.append(i)
    # print spine02

    for i in neck00Val:
        i = round(i, 3)
        neck00.append(i)
    # print neck00

    for i in neck01Val:
        i = round(i, 3)
        neck01.append(i)
    # print neck01

    for i in headVal:
        i = round(i, 3)
        head.append(i)

    # ikを0に戻すフェーズ
    mc.setAttr(Nmsp + "spineAIkCtrl.translateY", 0)
    mc.setAttr(Nmsp + "spineAIkCtrl.translateZ", 0)
    mc.setAttr(Nmsp + "spineBIkCtrl.translateY", 0)
    mc.setAttr(Nmsp + "spineBIkCtrl.translateZ", 0)
    mc.setAttr(Nmsp + "spineCIkCtrl.translateY", 0)
    mc.setAttr(Nmsp + "spineCIkCtrl.translateZ", 0)
    mc.setAttr(Nmsp + "neckAIkCtrl.translateY", 0)
    mc.setAttr(Nmsp + "neckAIkCtrl.translateZ", 0)
    mc.setAttr(Nmsp + "headAimCtrl.translateX", 0)
    mc.setAttr(Nmsp + "headAimCtrl.translateY", 0)
    mc.setAttr(Nmsp + "headAimCtrl.translateZ", 0)

    # 値をsetするフェーズ-----------------------
    mc.setAttr(Nmsp + "spineACtrl.rotate", *spine00)
    mc.setAttr(Nmsp + "spineBCtrl.rotate", *spine01)
    mc.setAttr(Nmsp + "spineCCtrl.rotate", *spine02)
    mc.setAttr(Nmsp + "neckACtrl.rotate", *neck00)
    mc.setAttr(Nmsp + "neckBCtrl.rotate", *neck01)
    mc.setAttr(Nmsp + "headCtrl.rotate", *head)


def moveCtrlBake(*args):
    Nmsp = mc.textScrollList('nameSpList', q=True, si=True)
    Nmsp = Nmsp[0] + ':'
    sF = mc.playbackOptions(q=True, minTime=True)
    eF = mc.playbackOptions(q=True, maxTime=True)
    eF = eF + 2
    ctrls = [Nmsp + "moveCtrl"]

    if args[0] == "head":
        dum = "moveCtrlDummy"
    elif args[0] == "spine":
        dum = "moveCtrlDummySpine_02"
    else:
        dum = "moveCtrlDummySpineAvr"

    if args[1] == "trans":

        for j in range(int(sF), int(eF), 1):

            getMove = mc.xform(Nmsp + "%s" % dum, q=True, t=True)
            getMoveZ = getMove[2] - 54
            mc.setAttr(Nmsp + "moveCtrl.translate", *getMove)
            mc.setAttr(Nmsp + "moveCtrl.translateZ", getMoveZ)

            mc.select(ctrls, r=True)
            mc.setKeyframe(ctrls)
            mc.currentTime(int(j), e=True)
    else:
        for j in range(int(sF), int(eF), 1):

            getMove = mc.xform(Nmsp + "%s" % dum, q=True, t=True)
            getMoveZ = getMove[2] - 54
            mc.setAttr(Nmsp + "%s.tz" % dum, getMoveZ)

            getRot = mc.xform(Nmsp + "%s" % dum, q=True, ro=True)

            mc.setAttr(Nmsp + "moveCtrl.translate", *getMove)
            mc.setAttr(Nmsp + "moveCtrl.translateZ", getMoveZ)
            mc.setAttr(Nmsp + "moveCtrl.rotate", *getRot)
            mc.setAttr(Nmsp + "%s.tz" % dum, getMove[2])

            mc.select(ctrls, r=True)
            mc.setKeyframe(ctrls)
            mc.currentTime(int(j), e=True)


def moveCtrlOffsetBake(*args):
    Nmsp = mc.textScrollList('nameSpList', q=True, si=True)
    Nmsp = Nmsp[0] + ':'
    sF = mc.playbackOptions(q=True, minTime=True)
    eF = mc.playbackOptions(q=True, maxTime=True)
    eF = eF

    nums = mc.intFieldGrp("numnum", q=True, v=True)
    offsetStartA = sF + nums[0] + 1
    offsetStartB = sF + nums[0] + nums[0] + 2
    offsetEndA = eF - nums[0] - 1
    offsetEndB = eF - nums[0] - nums[0] - 1

    ctrls = [Nmsp + "moveCtrl"]

    if args[0] == "head":
        dum = "moveCtrlDummy"
    elif args[0] == "spine":
        dum = "moveCtrlDummySpine_02"
    else:
        dum = "moveCtrlDummySpineAvr"

    mc.currentTime(int(sF), e=True)
    getMove = mc.xform(Nmsp + "%s" % dum, q=True, t=True)
    getMoveZ = getMove[2] - 54
    mc.setAttr(Nmsp + "%s.tz" % dum, getMoveZ)
    getRot = mc.xform(Nmsp + "%s" % dum, q=True, ro=True)

    dst = mc.listConnections(Nmsp + "moveCtrl", d=False, s=True)
    if dst:
        for i in dst:
            mc.delete(i)
    else:
        pass

    if args[1] == "trans":
        mc.setAttr(Nmsp + "moveCtrl.translate", *getMove)
        mc.setAttr(Nmsp + "moveCtrl.translateZ", getMoveZ)
        mc.select(ctrls, r=True)
        mc.setKeyframe(ctrls)
        mc.currentTime(int(offsetStartA), e=True)
        mc.setKeyframe(ctrls)

    else:
        mc.setAttr(Nmsp + "moveCtrl.translate", *getMove)
        mc.setAttr(Nmsp + "moveCtrl.translateZ", getMoveZ)
        mc.setAttr(Nmsp + "moveCtrl.rotate", *getRot)
        mc.select(ctrls, r=True)
        mc.setKeyframe(ctrls)
        mc.currentTime(int(offsetStartA), e=True)
        mc.setKeyframe(ctrls)

    # end
    mc.currentTime(int(eF), e=True)
    getMove = mc.xform(Nmsp + "%s" % dum, q=True, t=True)
    getMoveZ = getMove[2] - 54
    mc.setAttr(Nmsp + "%s.tz" % dum, getMoveZ)
    getRot = mc.xform(Nmsp + "%s" % dum, q=True, ro=True)
    if args[1] == "trans":
        mc.setAttr(Nmsp + "moveCtrl.translate", *getMove)
        mc.setAttr(Nmsp + "moveCtrl.translateZ", getMoveZ)
        mc.select(ctrls, r=True)
        mc.setKeyframe(ctrls)
        mc.currentTime(int(offsetEndA), e=True)

    else:

        mc.setAttr(Nmsp + "moveCtrl.translate", *getMove)
        mc.setAttr(Nmsp + "moveCtrl.translateZ", getMoveZ)
        mc.setAttr(Nmsp + "moveCtrl.rotate", *getRot)
        mc.select(ctrls, r=True)
        mc.setKeyframe(ctrls)
        mc.currentTime(int(offsetEndA), e=True)

    if args[1] == "trans":
        mc.setAttr(Nmsp + "moveCtrl.translate", *getMove)
        mc.setAttr(Nmsp + "moveCtrl.translateZ", getMoveZ)
        mc.select(ctrls, r=True)
        mc.setKeyframe(ctrls)
    else:
        mc.setAttr(Nmsp + "moveCtrl.translate", *getMove)
        mc.setAttr(Nmsp + "moveCtrl.translateZ", getMoveZ)
        mc.setAttr(Nmsp + "moveCtrl.rotate", *getRot)
        mc.select(ctrls, r=True)
        mc.setKeyframe(ctrls)

    for j in xrange(int(offsetStartB), int(offsetEndB), 1):  # noqa
        mc.currentTime(int(j), e=True)
        getMove = mc.xform(Nmsp + "%s" % dum, q=True, t=True)
        getMoveZ = getMove[2] - 54
        mc.setAttr(Nmsp + "%s.tz" % dum, getMoveZ)

        getRot = mc.xform(Nmsp + "%s" % dum, q=True, ro=True)
        if args[1] == "trans":
            mc.setAttr(Nmsp + "moveCtrl.translate", *getMove)
            mc.setAttr(Nmsp + "moveCtrl.translateZ", getMoveZ)
            mc.select(ctrls, r=True)
            mc.setKeyframe(ctrls)
            mc.currentTime(int(j), e=True)
        else:
            mc.setAttr(Nmsp + "moveCtrl.translate", *getMove)
            mc.setAttr(Nmsp + "moveCtrl.translateZ", getMoveZ)
            mc.setAttr(Nmsp + "moveCtrl.rotate", *getRot)
            mc.select(ctrls, r=True)
            mc.setKeyframe(ctrls)
            mc.currentTime(int(j), e=True)

    mc.filterCurve(Nmsp + "moveCtrl.translate", Nmsp + "moveCtrl.translateZ", Nmsp + "moveCtrl.rotate")


def moveCtrlAnimationBake(*args):
    viewChange()
    setRot = mc.checkBox("setRot", q=True, value=True)
    pos = mc.radioButtonGrp("headSpineSwt", q=True, select=True)
    nums = mc.intFieldGrp("numnum", q=True, v=True)
    if pos == 1:
        if setRot == 1:
            # time offsetを行わない場合
            if nums[0] == 0:
                moveCtrlBake("head", "rot")
            # time offsetを行う場合
            else:
                moveCtrlOffsetBake("head", "rot")
        else:
            if nums[0] == 0:
                moveCtrlBake("head", "trans")
            else:
                moveCtrlOffsetBake("head", "trans")
    # spineだったら
    elif pos == 2:
        if setRot == 1:
            # time offsetを行わない場合
            if nums[0] == 0:
                moveCtrlBake("spine", "rot")
            # time offsetを行う場合
            else:
                moveCtrlOffsetBake("spine", "rot")
        else:
            if nums[0] == 0:
                moveCtrlBake("spine", "trans")
            else:
                moveCtrlOffsetBake("spine", "trans")

    else:
        if setRot == 1:
            # time offsetを行わない場合
            if nums[0] == 0:
                moveCtrlBake("spineAvr", "rot")
            # time offsetを行う場合
            else:
                moveCtrlOffsetBake("spineAvr", "rot")
        else:
            if nums[0] == 0:
                moveCtrlBake("spineAvr", "trans")
            else:
                moveCtrlOffsetBake("spineAvr", "trans")
    viewChangeEnd()


def setMoveCtrlAnimation(*args):
    Nmsp = mc.textScrollList('nameSpList', q=True, si=True)
    Nmsp = Nmsp[0] + ':'
    setRot = mc.checkBox("setRot", q=True, value=True)
    pos = mc.radioButtonGrp("headSpineSwt", q=True, select=True)
    if pos == 1:
        if setRot == 1:
            getMove = mc.xform(Nmsp + "moveCtrlDummy", q=True, t=True)
            getMoveZ = getMove[2] - 54

            mc.setAttr(Nmsp + "moveCtrlDummy.tz", getMoveZ)

            getRot = mc.xform(Nmsp + "moveCtrlDummy", q=True, ro=True)
            mc.setAttr(Nmsp + "moveCtrl.rotate", *getRot)
            mc.setAttr(Nmsp + "moveCtrl.translate", *getMove)
            mc.setAttr(Nmsp + "moveCtrl.translateZ", getMoveZ)
            mc.setAttr(Nmsp + "moveCtrlDummy.tz", getMove[2])

        else:
            getMove = mc.xform(Nmsp + "moveCtrlDummy", q=True, t=True)
            getMoveZ = getMove[2] - 54

            mc.setAttr(Nmsp + "moveCtrl.translate", *getMove)
            mc.setAttr(Nmsp + "moveCtrl.translateZ", getMoveZ)
    elif pos == 2:
        if setRot == 1:
            getMove = mc.xform(Nmsp + "moveCtrlDummySpine_02", q=True, t=True)
            getMoveZ = getMove[2] - 54

            mc.setAttr(Nmsp + "moveCtrlDummySpine_02.tz", getMoveZ)

            getRot = mc.xform(Nmsp + "moveCtrlDummySpine_02", q=True, ro=True)
            mc.setAttr(Nmsp + "moveCtrl.rotate", *getRot)
            mc.setAttr(Nmsp + "moveCtrl.translate", *getMove)
            mc.setAttr(Nmsp + "moveCtrl.translateZ", getMoveZ)
            mc.setAttr(Nmsp + "moveCtrlDummySpine_02.tz", getMove[2])

        else:
            getMove = mc.xform(Nmsp + "moveCtrlDummySpine_02", q=True, t=True)
            getRot = mc.xform(Nmsp + "moveCtrlDummySpine_02", q=True, ro=True)
            getMoveZ = getMove[2] - 54

            mc.setAttr(Nmsp + "moveCtrl.translate", *getMove)
            mc.setAttr(Nmsp + "moveCtrl.translateZ", getMoveZ)
    else:
        if setRot == 1:
            getMove = mc.xform(Nmsp + "moveCtrlDummySpineAvr", q=True, t=True)
            getMoveZ = getMove[2] - 54

            mc.setAttr(Nmsp + "moveCtrlDummySpineAvr.tz", getMoveZ)

            getRot = mc.xform(Nmsp + "moveCtrlDummySpineAvr", q=True, ro=True)
            mc.setAttr(Nmsp + "moveCtrl.rotate", *getRot)
            mc.setAttr(Nmsp + "moveCtrl.translate", *getMove)
            mc.setAttr(Nmsp + "moveCtrl.translateZ", getMoveZ)
            mc.setAttr(Nmsp + "moveCtrlDummySpineAvr.tz", getMove[2])

        else:
            getMove = mc.xform(Nmsp + "moveCtrlDummySpineAvr", q=True, t=True)
            getRot = mc.xform(Nmsp + "moveCtrlDummySpineAvr", q=True, ro=True)
            getMoveZ = getMove[2] - 54

            mc.setAttr(Nmsp + "moveCtrl.translate", *getMove)
            mc.setAttr(Nmsp + "moveCtrl.translateZ", getMoveZ)
