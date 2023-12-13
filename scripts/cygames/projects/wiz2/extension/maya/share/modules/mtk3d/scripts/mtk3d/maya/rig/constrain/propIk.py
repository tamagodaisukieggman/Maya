# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mm
import mtku.maya.menus.animation.bakesimulation as bakesimulation
from maya import cmds, OpenMaya  # noqa
import math
import re

wintitle = 'cyPropIK'
func = 'import mtku.maya.menus.animation.constrain.propIk as propIk;propIk'
bak = 'import mtku.maya.menus.animation.bakesimulation as bakesimulation;'


def ui(*args):  # noqa
    if cmds.window(wintitle, q=True, exists=True):
        cmds.deleteUI(wintitle)
    win = cmds.window(wintitle, t=wintitle, w=400, h=140)  # noqa

    cmds.tabLayout('propIkTab')
    cmds.columnLayout('clmLay', adj=True, p='propIkTab')  # noqa

    cmds.rowLayout(nc=2, adj=True)  # noqa
    cmds.columnLayout(adj=True)
    cmds.textFieldButtonGrp('wristFBG', l=u'手首のコントローラ', tx=u'ノードを選択して--set--してください。', bl='--set--', h=30, w=100, cl3=['center', 'center', 'right'], adj=2, cw=[1, 130], bc='{}.getObj("wristFBG")'.format(func), ann=u'選択したノードが設定されます。')  # noqa
    cmds.textFieldButtonGrp('propFBG', l=u'プロップのコントローラ', tx=u'ノードを選択して--set--してください。', bl='--set--', h=30, w=100, cl3=['center', 'center', 'right'], adj=2, cw=[1, 130], bc='{}.getObj("propFBG")'.format(func), ann=u'選択したノードが設定されます。')  # noqa
    cmds.textFieldButtonGrp('aimFBG', l=u'エイムさせるオブジェクト', tx=u'ノードを選択して--set--してください。', bl='--set--', h=30, w=100, cl3=['center', 'center', 'right'], adj=2, cw=[1, 130], bc='{}.getObj("aimFBG")'.format(func), ann=u'選択したノードが設定されます。')  # noqa
    cmds.setParent('..')

    cmds.columnLayout(adj=True)
    cmds.button(l='select', c='{}.selectItem("wristFBG")'.format(func), bgc=[0.5, 0.5, 0.5])
    cmds.text(l='', h=7)
    cmds.button(l='select', c='{}.selectItem("propFBG")'.format(func), bgc=[0.5, 0.5, 0.5])
    cmds.text(l='', h=7)
    cmds.button(l='select', c='{}.selectItem("aimFBG")'.format(func))
    cmds.setParent('..')

    cmds.setParent('..')

    cmds.separator(st='in')

    cmds.rowLayout(nc=8, adj=True)
    cmds.button(l='Create', w=40, h=40, c='{}.call_main()'.format(func))
    cmds.button(l='Bake', w=40, h=40, c='{}.selectItem2();{}bakesimulation.main()'.format(func, bak), ann=u'手首とプロップのコントローラがベイクされます。')
    cmds.button(l='Locator', h=40, c='{}.locOffset()'.format(func), ann=u'選択したオブジェクトの位置にロケータを作成します。')
    cmds.setParent('..')

    cmds.rowLayout(nc=3)  # noqa
    cmds.text(l=u'  PropIKノード  ', fn='tinyBoldLabelFont')
    cmds.textFieldButtonGrp('propIKGRP1', tx=u'', ed=False, bl='select', bc='{}.selectItem("propIKGRP1")'.format(func), h=30, w=320, cl3=['center', 'center', 'right'], adj=2, cw=[2, 150])  # noqa
    cmds.button(l='delete', c='{}.delItem("propIKGRP1")'.format(func))
    cmds.setParent('..')

    cmds.separator(st='in')

    cmds.rowLayout(nc=5)
    cmds.button('BTNA', l='SelectIKCtrlA', w=80, h=40, c='', en=False)
    cmds.button('BTNB', l='SelectIKCtrlB', w=80, h=40, c='', en=False)

    cmds.button('JDSWDset', l=u'set\nJDとSword', w=80, h=40, c='{}.jdSet()'.format(func), bgc=[0.5, 0.2, 0.2], ann=u'JDと剣の設定をします。')
    cmds.button('MSTRODset', l=u'set\nMSTとRod', w=80, h=40, c='{}.mstSet()'.format(func), bgc=[0.2, 0.2, 0.5], ann=u'MSTと杖の設定をします。')

    cmds.text(l='', w=100, h=40, ann=u'(^ q ^)')

    cmds.setParent('..')

    cmds.columnLayout(adj=True, p='propIkTab')

    cmds.rowLayout(nc=2, adj=True)  # noqa
    cmds.columnLayout(adj=True)
    cmds.textFieldButtonGrp('wristFBG2', l=u'手首のコントローラ', tx=u'ノードを選択して--set--してください。', bl='--set--', h=30, w=100, cl3=['center', 'center', 'right'], adj=2, cw=[1, 130], bc='{}.getObj2("wristFBG2")'.format(func))  # noqa
    cmds.textFieldButtonGrp('propFBG2', l=u'プロップのコントローラ', tx=u'ノードを選択して--set--してください。', bl='--set--', h=30, w=200, cl3=['center', 'center', 'right'], adj=2, cw=[1, 130], bc='{}.getObj2("eqCtrlBG")'.format(func))  # noqa
    cmds.setParent('..')

    cmds.columnLayout(adj=True)
    cmds.button(l='select', c='{}.selectItem("wristFBG2")'.format(func), bgc=[0.5, 0.5, 0.5])
    cmds.text(l='', h=7)
    cmds.button(l='select', c='{}.selectItem("propFBG2")'.format(func), bgc=[0.5, 0.5, 0.5])
    cmds.setParent('..')

    cmds.setParent('..')

    cmds.separator(st='in')

    cmds.rowLayout(nc=8, adj=True)
    cmds.button(l='Create', h=40, c='{}.call_fixProp()'.format(func))
    cmds.button(l='Bake', w=40, h=40, c='{}.selectItem3();{}bakesimulation.main();{}.delBlendAim()'.format(func, bak, func), ann=u'手首とプロップのコントローラがベイクされます。')
    cmds.button(l='Locator', h=40, c='{}.locOffset()'.format(func), ann=u'選択したオブジェクトの位置にロケータを作成します。')
    cmds.setParent('..')

    cmds.rowLayout(nc=3)  # noqa
    cmds.text(l=u'  PropIKノード  ', fn='tinyBoldLabelFont')
    cmds.textFieldButtonGrp('propIKGRP2', tx=u'', ed=False, bl='select', bc='{}.selectItem("propIKGRP2")'.format(func), h=30, w=320, cl3=['center', 'center', 'right'], adj=2, cw=[2, 150])  # noqa
    cmds.button(l='delete', c='{}.delItem("propIKGRP2")'.format(func))
    cmds.setParent('..')

    cmds.separator(st='in')

    cmds.rowLayout(nc=5)
    cmds.button('JDSWDset2', l=u'set\nJDとSword', w=80, h=40, c='{}.jdSet2()'.format(func), bgc=[0.5, 0.2, 0.2], ann=u'JDと剣の設定をします。')
    cmds.button('MSTRODset2', l=u'set\nMSTとRod', w=80, h=40, c='{}.mstSet2()'.format(func), bgc=[0.2, 0.2, 0.5], en=False, ann=u'MSTと杖の設定をします。', vis=False)
    cmds.text(l='', w=100, h=40, ann=u'(ﾟДﾟ；)')
    cmds.setParent('..')

    cmds.showWindow()
    cmds.tabLayout('propIkTab', e=True, tli=[[1, u'プロップ先端のIK制御'], [2, u'手の微調整']])  # noqa


def getObj(btGrp):  # noqa
    grps = ['wristFBG', 'propFBG', 'aimFBG']
    sel = cmds.ls(os=True)
    if 1 < len(sel):
        for i in range(len(sel)):
            cmds.textFieldButtonGrp(grps[i], e=True, tx=sel[i])
    else:
        for obj in sel:
            cmds.textFieldButtonGrp(btGrp, e=True, tx=obj)


def getObj2(btGrp):  # noqa
    grps = ['wristFBG2', 'propFBG2']
    sel = cmds.ls(os=True)
    if 1 < len(sel):
        for i in range(len(sel)):
            cmds.textFieldButtonGrp(grps[i], e=True, tx=sel[i])
    else:
        for obj in sel:
            cmds.textFieldButtonGrp(btGrp, e=True, tx=obj)


def call_main(*args):  # noqa
    wristR = cmds.textFieldButtonGrp('wristFBG', q=True, tx=True)
    propCtrl = cmds.textFieldButtonGrp('propFBG', q=True, tx=True)
    propTopObj = cmds.textFieldButtonGrp('aimFBG', q=True, tx=True)

    if cmds.objExists(wristR) and cmds.objExists(propCtrl) and cmds.objExists(propTopObj):
        main(wristR, propCtrl, propTopObj)
    else:
        cmds.warning(u'ノードを選択して--set--してください。')


def call_fixProp(*args):  # noqa
    wristR = cmds.textFieldButtonGrp('wristFBG2', q=True, tx=True)
    eqCtrl = cmds.textFieldButtonGrp('propFBG2', q=True, tx=True)

    if cmds.objExists(wristR) and cmds.objExists(eqCtrl):
        fixProp(wristR, eqCtrl)
    else:
        cmds.warning(u'ノードを選択して--set--してください。')


def selectItem(btGrp):  # noqa
    item = cmds.textFieldButtonGrp(btGrp, q=True, tx=True)
    if cmds.objExists(item):
        cmds.select(item)
    else:
        cmds.warning(u'ノードが--set--されていない、もしくは存在しないノードです。')


def selectItem2(*args):  # noqa
    item1 = cmds.textFieldButtonGrp('wristFBG', q=True, tx=True)
    item2 = cmds.textFieldButtonGrp('propFBG', q=True, tx=True)
    if cmds.objExists(item1) and cmds.objExists(item2):
        cmds.select(item1, item2)
    else:
        cmds.warning(u'ノードが--set--されていない、もしくは存在しないノードです。')


def selectItem3(*args):  # noqa
    item1 = cmds.textFieldButtonGrp('wristFBG2', q=True, tx=True)
    item2 = cmds.textFieldButtonGrp('propFBG2', q=True, tx=True)
    if cmds.objExists(item1) and cmds.objExists(item2):
        cmds.select(item1, item2)
    else:
        cmds.warning(u'ノードが--set--されていない、もしくは存在しないノードです。')


def delItem(btGrp):  # noqa
    item = cmds.textFieldButtonGrp(btGrp, q=True, tx=True)
    item2 = cmds.textFieldButtonGrp('aimFBG', q=True, tx=True)
    if cmds.objExists(item):
        cmds.delete(item)
        cmds.delete(item2)
    else:
        cmds.warning(u'ノードが--set--されていない、もしくは存在しないノードです。')


def deleteFuncObj(*args):  # noqa
    if cmds.objExists('*:wristRotLocGp'):
        cmds.delete('*:wristRotLocGp')
    else:
        pass


def locOffset(*args):  # noqa
    sel = cmds.ls(sl=True)
    if 0 < len(sel):
        loc = cmds.spaceLocator(p=[0, 0, 0])
        poCons = cmds.parentConstraint(sel[0], loc, w=1)
        cmds.delete(poCons)
        cmds.select(loc, r=True)
    else:
        loc = cmds.spaceLocator(p=[0, 0, 0])

    cmds.textFieldButtonGrp('aimFBG', e=True, tx='{}'.format(loc[0]))

    return loc


def queryIkCtrls(ctrl):  # noqa
    try:
        cmds.select("{}".format(ctrl), r=True)
    except:
        cmds.warning(u'コントローラが存在しません。')
        cmds.button('BTNA', e=True, en=False)
        cmds.button('BTNB', e=True, en=False)


def jdSet(*args):  # noqa
    cmds.select('eqw00_999_rig:swordTopCtrl', r=True)
    cmds.textFieldButtonGrp('wristFBG', e=True, tx='ply00_999_rig:wrist_R_Ctrl')
    cmds.textFieldButtonGrp('propFBG', e=True, tx='ply00_999_rig:eq_rightHandCtrl')
    loc = locOffset()
    main('ply00_999_rig:wrist_R_Ctrl', 'ply00_999_rig:eq_rightHandCtrl', loc)


def mstSet(*args):  # noqa
    cmds.select('eqw99_999_rig:wandCtrl', r=True)
    cmds.textFieldButtonGrp('wristFBG', e=True, tx='mst00_998_rig:wrist_R_Ctrl')
    cmds.textFieldButtonGrp('propFBG', e=True, tx='eqw99_999_rig:wandCtrl')
    loc = locOffset()
    cmds.move(0, 180, 0, '{}'.format(loc[0]), r=True, os=True, wd=True)
    main('mst00_998_rig:wrist_R_Ctrl', 'eqw99_999_rig:wandCtrl', loc)


def jdSet2(*args):  # noqa
    cmds.textFieldButtonGrp('wristFBG2', e=True, tx='ply00_999_rig:wrist_R_Ctrl')
    cmds.textFieldButtonGrp('propFBG2', e=True, tx='ply00_999_rig:eq_rightHandCtrl')
    loc = locOffset()  # noqa
    fixProp('ply00_999_rig:wrist_R_Ctrl', 'ply00_999_rig:eq_rightHandCtrl')


def mstSet2(*args):  # noqa
    cmds.select('eqw99_999_rig:wandCtrl', r=True)
    cmds.textFieldButtonGrp('wristFBG', e=True, tx='mst00_998_rig:wrist_R_Ctrl')
    cmds.textFieldButtonGrp('propFBG', e=True, tx='eqw99_999_rig:wandCtrl')
    loc = locOffset()
    cmds.move(0, 180, 0, '{}'.format(loc[0]), r=True, os=True, wd=True)
    main('mst00_998_rig:wrist_R_Ctrl', 'eqw99_999_rig:wandCtrl', loc)


def delBlendAim(*args):  # noqa
    item1 = cmds.textFieldButtonGrp('wristFBG2', q=True, tx=True)
    attr = cmds.listConnections(item1)
    blAm = [atr for atr in attr if re.match('.*blendAim.*', atr)]
    if blAm == []:
        pass
    else:
        cmds.delete(blAm)
        cmds.deleteAttr(item1, at='blendAim1')


def main(wristR, propCtrl, propTopObj):  # noqa
    if cmds.objExists('{}_wristRotLocGp'.format(wristR)):
        cmds.delete('{}_wristRotLocGp'.format(wristR))
    gpA = cmds.group(em=True, n='{}_wristRotLocGp'.format(wristR))

    cmds.select(cl=True)
    aJt = cmds.joint(n='{}_propIkA'.format(wristR))
    cmds.select(cl=True)
    bJt = cmds.joint(n='{}_propIkB'.format(wristR))
    cmds.select(cl=True)
    cJt = cmds.joint(n='{}_propIkC'.format(wristR))

    consA = cmds.parentConstraint(wristR, aJt, w=1)
    consB = cmds.parentConstraint(propCtrl, bJt, w=1)
    consC = cmds.parentConstraint(propTopObj, cJt, w=1)

    cmds.delete(consA, consB, consC)

    amConsA = cmds.aimConstraint(cJt, bJt, offset=[0, 0, 0], w=1, aimVector=[1, 0, 0], upVector=[0, 1, 0], worldUpType="vector", worldUpVector=[0, 1, 0])
    amConsB = cmds.aimConstraint(bJt, aJt, offset=[0, 0, 0], w=1, aimVector=[1, 0, 0], upVector=[0, 1, 0], worldUpType="vector", worldUpVector=[0, 1, 0])
    amConsC = cmds.aimConstraint(cJt, bJt, offset=[0, 0, 0], w=1, aimVector=[1, 0, 0], upVector=[0, 1, 0], worldUpType="vector", worldUpVector=[0, 1, 0])

    cmds.delete(amConsA, amConsB, amConsC)

    cmds.makeIdentity(aJt, bJt, cJt, apply=True, t=0, r=1, s=0, n=0, pn=1)

    cmds.parent(cJt, bJt)
    cmds.parent(bJt, aJt)

    cmds.select(aJt, cJt, r=True)
    ikNode = cmds.ikHandle(sol='ikRPsolver', n='{}_propIKHandle'.format(wristR))

    ctrlA = cmds.curve(d=1, p=[(0, 9, 0), (9, 0, 0), (0, 0, 9), (-9, 0, 0), (0, 0, -9), (0, 9, 0), (0, 0, 9), (0, -9, 0), (0, 0, -9), (9, 0, 0), (0, 9, 0), (-9, 0, 0), (0, -9, 0), (9, 0, 0)], k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], n='{}_aimFromCtrl'.format(wristR))  # noqa

    start = cmds.xform(aJt, q=1, ws=1, t=1)
    mid = cmds.xform(bJt, q=1, ws=1, t=1)
    end = cmds.xform(cJt, q=1, ws=1, t=1)

    startV = OpenMaya.MVector(start[0], start[1], start[2])
    midV = OpenMaya.MVector(mid[0], mid[1], mid[2])
    endV = OpenMaya.MVector(end[0], end[1], end[2])

    startEnd = endV - startV
    startMid = midV - startV

    dotP = startMid * startEnd
    proj = float(dotP) / float(startEnd.length())
    startEndN = startEnd.normal()
    projV = startEndN * proj

    arrowV = startMid - projV
    arrowV *= 0.5
    finalV = arrowV + midV

    cross1 = startEnd ^ startMid
    cross1.normalize()

    cross2 = cross1 ^ arrowV
    cross2.normalize()
    arrowV.normalize()

    matrixV = [arrowV.x, arrowV.y, arrowV.z, 0,
               cross1.x, cross1.y, cross1.z, 0,
               cross2.x, cross2.y, cross2.z, 0,
               0, 0, 0, 1]

    matrixM = OpenMaya.MMatrix()

    OpenMaya.MScriptUtil.createMatrixFromList(matrixV, matrixM)

    matrixFn = OpenMaya.MTransformationMatrix(matrixM)

    rot = matrixFn.eulerRotation()

    loc = cmds.spaceLocator()[0]
    cmds.xform(loc, ws=1, t=(finalV.x, finalV.y, finalV.z))

    cmds.xform(loc, ws=1, rotation=((rot.x / math.pi * 180.0),
                                    (rot.y / math.pi * 180.0),
                                    (rot.z / math.pi * 180.0)))

    cmds.move(20, 0, 0, os=True, wd=True, r=True)

    cmds.delete(cmds.pointConstraint(loc, ctrlA, w=1), loc)

    cmds.poleVectorConstraint(ctrlA, ikNode[0], w=1)

    cmds.orientConstraint(aJt, wristR, w=1, mo=True)
    cmds.orientConstraint(bJt, propCtrl, w=1, mo=True)

    cmds.pointConstraint(wristR, aJt, w=1)

    ctrlB = cmds.curve(d=1, p=[(0, 5.8, 0), (5.8, 0, 0), (0, 0, 5.8), (-5.8, 0, 0), (0, 0, -5.8), (0, 5.8, 0), (0, 0, 5.8), (0, -5.8, 0), (0, 0, -5.8), (5.8, 0, 0), (0, 5.8, 0), (-5.8, 0, 0), (0, -5.8, 0), (5.8, 0, 0)], k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], n='{}_aimCtrl'.format(wristR))  # noqa

    paConsB = cmds.parentConstraint(propTopObj, ctrlB, w=1)
    cmds.delete(paConsB)

    cmds.pointConstraint(ctrlB, ikNode[0], w=1)

    cmds.parent(aJt, gpA)
    cmds.parent(ikNode[0], gpA)
    cmds.parent(ctrlA, gpA)
    cmds.parent(ctrlB, gpA)

    cmds.setAttr('{}.visibility'.format(aJt), 0)
    cmds.setAttr('{}.visibility'.format(ikNode[0]), 0)

    mm.eval("""setAttr -lock true -keyable false -channelBox false "{0}.rx";
            setAttr -lock true -keyable false -channelBox false "{0}.ry";
            setAttr -lock true -keyable false -channelBox false "{0}.rz";
            setAttr -lock true -keyable false -channelBox false "{0}.sx";
            setAttr -lock true -keyable false -channelBox false "{0}.sy";
            setAttr -lock true -keyable false -channelBox false "{0}.sz";
            setAttr -lock true -keyable false -channelBox false "{0}.v";
            setAttr -lock true -keyable false -channelBox false "{1}.rx";
            setAttr -lock true -keyable false -channelBox false "{1}.ry";
            setAttr -lock true -keyable false -channelBox false "{1}.rz";
            setAttr -lock true -keyable false -channelBox false "{1}.sx";
            setAttr -lock true -keyable false -channelBox false "{1}.sy";
            setAttr -lock true -keyable false -channelBox false "{1}.sz";
            setAttr -lock true -keyable false -channelBox false "{1}.v";
            setAttr "{0}.overrideEnabled" 1;
            setAttr "{0}.overrideColor" 9;
            setAttr "{1}.overrideEnabled" 1;
            setAttr "{1}.overrideColor" 9;
            """.format(ctrlA, ctrlB))

    keyFd = cmds.findKeyframe(wristR, curve=True)  # noqa
    keyFdp = cmds.findKeyframe(propCtrl, curve=True)  # noqa
    ct = cmds.currentTime(query=True)
    preTime = ct - 1
    if keyFd is None:
        cmds.setKeyframe("{}.rotate".format(wristR), t=ct)
    if keyFdp is None:
        cmds.setKeyframe("{}.translate".format(propCtrl), t=ct)
        cmds.setKeyframe("{}.rotate".format(propCtrl), t=ct)

    bakLocA = cmds.spaceLocator()
    bakLocB = cmds.spaceLocator()

    cmds.delete(cmds.parentConstraint(ctrlA, bakLocA, w=1), cmds.parentConstraint(ctrlB, bakLocB, w=1))

    bakConsA = cmds.parentConstraint(wristR, bakLocA, w=1, mo=True)
    bakConsB = cmds.parentConstraint(propCtrl, bakLocB, w=1, mo=True)

    cmds.setAttr("{}.blendOrient1".format(wristR), 0)
    cmds.setAttr("{}.blendOrient1".format(propCtrl), 0)

    cmds.setKeyframe("{}.blendOrient1".format(wristR), t=preTime)
    cmds.setKeyframe("{}.blendOrient1".format(propCtrl), t=preTime)

    cmds.select(bakLocA, bakLocB, r=True)
    bakesimulation.main()

    cmds.delete(bakConsA, bakConsB)

    bakConsA = cmds.pointConstraint(bakLocA, ctrlA, w=1)
    bakConsB = cmds.pointConstraint(bakLocB, ctrlB, w=1)

    cmds.select(ctrlA, ctrlB, r=True)
    bakesimulation.main()

    cmds.setAttr("{}.blendOrient1".format(wristR), 1)
    cmds.setAttr("{}.blendOrient1".format(propCtrl), 1)

    cmds.setKeyframe("{}.blendOrient1".format(wristR), t=ct)
    cmds.setKeyframe("{}.blendOrient1".format(propCtrl), t=ct)

    cmds.delete(bakLocA, bakLocB)

    cmds.select(bJt, r=True)  # noqa
    cmds.setAttr("{}.rotateX".format(bJt), 0, lock=True)
    cmds.setAttr("{}.rotateY".format(bJt), 0, lock=True)
    cmds.setAttr("{}.rotateZ".format(bJt), 0, lock=True)

    cmds.select(ctrlB, r=True)  # noqa

    cmds.button('BTNA', e=True, c='{}.queryIkCtrls("{}")'.format(func, ctrlA), en=True)
    cmds.button('BTNB', e=True, c='{}.queryIkCtrls("{}")'.format(func, ctrlB), en=True)  # noqa
    cmds.textFieldButtonGrp('propIKGRP1', e=True, tx=u'{}'.format(gpA))  # noqa


def fixProp(wristR, propCtrl):  # noqa
    if cmds.objExists('{}_fixProp'.format(wristR)):
        cmds.delete('{}_fixProp'.format(wristR))
    fp = cmds.group(em=True, n='{}_fixProp'.format(wristR))
    loc = cmds.spaceLocator()
    cmds.setAttr('{}.visibility'.format(loc[0]), 0)
    cmds.parent(loc, fp)
    con = cmds.parentConstraint(propCtrl, loc, w=1)
    cmds.select(loc, r=True)
    bakesimulation.main()
    cmds.parentConstraint(loc, propCtrl, w=1)
    cmds.delete(con)

    loc2 = cmds.duplicate(loc)
    cmds.parent(loc2, loc)

    cmds.setAttr('{}.translateZ'.format(loc2[0]), 30)
    cmds.select(loc, wristR, r=True)

    try:
        cmds.aimConstraint(loc, wristR, mo=True, w=1, aimVector=[1, 0, 0], upVector=[0, 1, 0], worldUpType='objectrotation', worldUpVector=[0, 1, 0], worldUpObject=loc2[0])
        cmds.textFieldButtonGrp('propIKGRP2', e=True, tx=u'{}'.format(fp))  # noqa
    except:
        cmds.warning(u'{}にBlendOrientなどが無いか確認してください。'.format(wristR))
        cmds.delete(fp)

    cmds.select(cl=True)
