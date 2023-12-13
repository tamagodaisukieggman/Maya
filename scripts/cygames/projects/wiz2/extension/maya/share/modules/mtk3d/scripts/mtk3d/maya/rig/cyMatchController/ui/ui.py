# -*- coding: utf-8 -*-
import maya.cmds as mc
import mtk3d.maya.rig.cyMatchController.module.exe as exe
import mtk3d.maya.rig.cyMatchController.module.util as utl


def ui(*args):
    if mc.window('mahCtrlUI', ex=True):
        mc.deleteUI('mahCtrlUI')
    mc.window('mahCtrlUI', title='cyMatchController', w=300, h=100)
    mc.columnLayout()
    mc.frameLayout(collapsable=False, collapse=False, label=u'左右　パーツ　選択', w=305)

    mc.rowColumnLayout(numberOfColumns=2)  #
    mc.checkBox('boxLR', l=u'左右選択', w=150, onc=utl.onLRCmd, ofc=utl.offLRCmd, cc=utl.radioChangeVis)  #
    mc.checkBox('boxArmLeg', l=u'手と足', onc=utl.onArmLegCmd, ofc=utl.offArmLegCmd, cc=utl.radioChangeVis)  #
    mc.setParent('..')

    mc.radioButtonGrp('sideChk', numberOfRadioButtons=2, label='Side', labelArray2=['L', 'R'], select=1, vis=False)
    mc.radioButtonGrp('partsChk', numberOfRadioButtons=2, label='Parts', labelArray2=['Arm', 'Leg'], select=1,
                      vis=False)

    # mc.rowLayout(numberOfColumns=2)#
    mc.radioButtonGrp('radioHand', numberOfRadioButtons=2, label=u'手の選択', labelArray2=[u'左手', u'右手'], select=1,
                      cc=utl.radioChangeHandsLegs)
    mc.radioButtonGrp('radioLegs', numberOfRadioButtons=2, label=u'足の選択', labelArray2=[u'左足', u'右足'],
                      cc=utl.radioChangeHandsLegs, scl='radioHand')

    mc.setParent('..')
    mc.frameLayout(collapsable=False, collapse=False, label=u'ネームスペースリスト :')
    mc.columnLayout()
    mc.checkBox('useNMspsChk', label=u'ネームスペースを指定する', onc=utl.chkOnCmd, ofc=utl.chkOffCmd)
    mc.rowColumnLayout(numberOfColumns=2)
    mc.button('getNss', label=u'ゲットネームスペースリスト', w=150, bgc=[0.112, 0.612, 0.562], en=False, c=getNss)
    mc.button('deselBtn', label=u'セレクト解除', w=150, bgc=[0.112, 0.612, 0.562], en=False, c=desel)
    mc.setParent('..')
    mc.columnLayout()
    mc.textScrollList('nmspList', numberOfRows=20, w=200, h=200, en=False, allowMultiSelection=False)
    mc.setParent('..')

    mc.frameLayout(collapsable=False, collapse=False, label='IK FK Switcher :', w=300)
    mc.columnLayout()
    mc.checkBox('bakeOnOff', label=u'コントローラベイクON:', onc=utl.bakeOnCmd, ofc=utl.bakeOffCmd)
    mc.radioButtonGrp('bakeType', numberOfRadioButtons=2, label=u'ベイクタイプ:', labelArray2=[u'FK', u'IK'], en=False,
                      select=1, on1=utl.FkButnChk, on2=utl.IkButnChk)
    mc.setParent('..')
    mc.rowColumnLayout(numberOfColumns=2)
    mc.button('FKButton', label='FK > IK', c=exe.exeFKIK, bgc=[0.112, 0.612, 0.562], h=50, w=150)
    mc.button('IKButton', label='IK > FK', c=exe.exeIKFK, bgc=[0.112, 0.612, 0.562], h=50, w=150)
    mc.setParent('..')

    mc.showWindow('mahCtrlUI')


def getNss(*args):
    mc.textScrollList('nmspList', e=True, removeAll=True)
    exclude_list = ['UI', 'shared']
    mc.namespaceInfo(cur=True)
    mc.namespace(set=':')
    namespaces = ['{}'.format(ns) for ns in mc.namespaceInfo(lon=True) if ns not in exclude_list]

    [mc.textScrollList('nmspList', edit=True, append=x) for x in namespaces]


def desel(*args):
    mc.textScrollList('nmspList', e=True, da=True)
