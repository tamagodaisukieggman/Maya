# -*- coding: utf-8 -*-
#=========================================================================== # noqa
# Cygames Tools # noqa
# ui.py # noqa
# # noqa
# Copyright 2017, Cygames Inc. # noqa
#=========================================================================== # noqa
import maya.cmds as mc
import mtk3d.maya.rig.cyPoseStore
import mtk3d.maya.rig.cyPoseStore.buttonFuncs as btnF
import mtk3d.maya.rig.cyPoseStore.writeJSON as wJsn
import re
import maya.mel as mm

mm.eval('python("import maya.cmds as mc");')

reload(mtk3d.maya.rig.cyPoseStore.buttonFuncs)  # noqa
reload(mtk3d.maya.rig.cyPoseStore.writeJSON)  # noqa
reload(mtk3d.maya.rig.cyPoseStore.importJSON)  # noqa

uiFunc = 'import mtk3d.maya.rig.cyPoseStore.ui as ui;ui'
uiFuncIm = 'import mtk3d.maya.rig.cyPoseStore.importJSON as importJSON;importJSON'

WorkspaceName = 'cyPoseStore'


def CloseUI(*args):
    if mc.workspaceControl(WorkspaceName, query=True, exists=True):
        mc.workspaceControl(WorkspaceName, edit=True, close=True, retain=False)


def poseImgUI(*args):
    KitVersion = 'cyPoseStore v2.0.0'
    v = 'v1.0.0'

    if mc.workspaceControl(WorkspaceName, query=True, exists=True):
        buildUI(WorkspaceName)
        getCurPrj()
        btnF.storeRefresh()
    else:
        mc.workspaceControl(WorkspaceName, uiScript='', closeCommand='', retain=False, ih=1000, iw=500)
        mc.workspaceControl(WorkspaceName, e=True, uiScript='import mtk3d.maya.rig.cyPoseStore.ui as ui;ui.poseImgUI()', closeCommand='import mtk3d.maya.rig.cyPoseStore.ui as ui;ui.CloseUI()')
        buildUI(WorkspaceName)


def buildUI(parent=None):
    if mc.scrollLayout('mainScr', query=True, exists=True):
        mc.deleteUI('mainScr')

    mc.scrollLayout('mainScr', cr=True, w=500, p=parent)

    mc.columnLayout('poseClm', adj=True)

    mc.frameLayout(collapsable=False, collapse=False, label=u'カレントワークディレクトリ :')  # frameLayoutA  # noqa
    popup = mc.popupMenu('pathPop', b=0)
    mc.menuItem('pItem', p=popup, l=u'Z:/mtku/work/anim/へ移動', c='{}.setAnimPoseDir()'.format(uiFunc))
    mc.textField('posePathTxt', text='', ec='{}.enterCommand()'.format(uiFunc), aie=True)
    mc.button('brwsBtn', label=u'ブラウズ..', bgc=[0.112, 0.612, 0.562], en=True, c=btnF.txtBrows)
    mc.textField('messagesTxt', text='', ed=False, en=True)
    mc.setParent('..')  # frameLayoutA  # noqa

    mc.frameLayout('poseStoreFrame', label=u'Pose Store :')  # frameLayoutB  # noqa
    mc.rowColumnLayout('poseSet', numberOfColumns=4)
    mc.button('addStore', label=u'Storeを追加する', c=btnF.makeStore)  # ディレクトリ作成
    mc.text(label=u'サムネイルサイズ:')
    mc.intField('thumbSiz', minValue=10, maxValue=100, value=50, ec=btnF.storeRefresh)
    mc.button('delBtn', label=u'Store内の全Poseリフレッシュ', c=btnF.storeRefresh)  # 表示中の全てのボタンを削除する
    mc.setParent('..')  # rowColumnLayout  # noqa
    mc.setParent('..')  # frameLayoutB  # noqa

    mc.rowColumnLayout(numberOfColumns=3, p='poseStoreFrame')
    mc.text(l=u'ネームスペース:  ', ann=u'左クリックでネームスペースを選択')
    frame = mc.frameLayout('nameSpList', l=u'', mw=170, mh=20, h=20, ann=u'左クリックでネームスペースを選択')  # noqa
    mc.setParent('..')
    nsl = mc.popupMenu('nsPop', b=1, pmc=getNss, p='nameSpList')
    mc.menuItem(p=nsl, l=u'', c='{}.setAnimPoseDir()'.format(uiFunc))
    mc.checkBox('replaceGp', label=u'置き換え')
    mc.setParent('..')

    mc.rowColumnLayout('poseFrm', numberOfColumns=3)
    mc.text(label=u'ポーズ名 :  ')
    mc.textField('poseNameTxt', w=250, h=30, text='')
    mc.button('addBtn', label=u'ポーズを追加', c=wJsn.makeButton)
    mc.button('shotButton', label=u'サムネイルウィンドウ', c='{}.modelPanelShot()'.format(uiFunc))
    mc.setParent('..')  # rowColumnLayout # noqa

    mc.checkBox('nmspChkBox', label=u'ネームスペース使用する:', en=False, v=False, vis=False)
    mc.checkBox('revertPoseChk', label=u'POSEを反転する:', vis=False)
    mc.radioButtonGrp('sideChk', numberOfRadioButtons=2, label='Side', labelArray2=['L', 'R'], select=1, vis=False)

    mc.frameLayout(label=u'Store :')  # frameLayoutC # noqa
    mc.rowColumnLayout(numberOfColumns=6)  # rowColumnLayoutA # noqa
    mc.text(label=u'追加するタブ :  ')
    mc.radioCollection('selTabCollection')
    mc.radioButton('rootTab', label=u'1段目', sl=True, cl='selTabCollection', cc=btnF.getRbtn)  # noqa
    mc.radioButton('aTab', label=u'2段目', cl='selTabCollection', cc=btnF.getRbtn)
    mc.setParent('..')  # rowColumnLayoutA # noqa

    mc.rowColumnLayout(numberOfColumns=4)  # rowColumnLayoutB # noqa
    mc.text(label=u'タブ名 :  ')
    mc.textField('tabTxt', w=250, h=20, text='')
    mc.button('addTabBtnDown', label=u'2段目に追加', c=btnF.createTabs, en=False)
    mc.button('addTabBtnSide', label=u'1段目横に追加', c=btnF.createTabs)
    mc.setParent('..')  # rowColumnLayoutB # noqa

    mc.rowColumnLayout(numberOfColumns=4)  # rowColumnLayoutC # noqa
    mc.text(label=u'固定する値を選択してください :  ')
    mc.checkBox('lockPoseChkT', label=u'移動値を固定する:')
    mc.checkBox('lockPoseChkR', label=u'回転値を固定する:')
    mc.setParent('..')  # rowColumnLayoutC # noqa

    mc.rowColumnLayout(numberOfColumns=4)  # rowColumnLayoutC # noqa
    mc.text(label=u'インポートオプション :  ')
    mc.button('impOption', label=u'ImportOptionWindow', c='{}.optionUi()'.format(uiFunc))
    mc.setParent('..')  # rowColumnLayoutC # noqa

    mc.setParent('..')

    mc.scrollLayout('iconsScrl', h=750)
    mc.tabLayout('tablayouts', h=700)
    mc.rowColumnLayout('poses', numberOfColumns=3)

    getCurPrj()
    btnF.storeRefresh()


def setAnimPoseDir(*args):  # noqa
    mc.textField('posePathTxt', e=True, text='Z:/mtku/work/anim/')
    btnF.storeRefresh()


def setPath(path):  # noqa
    mc.textField('posePathTxt', e=True, text=path)
    btnF.storeRefresh()

# カレントプロジェクト取得 # noqa


def getCurPrj(*args):  # noqa
    curPrj = mc.workspace(q=True, active=True)
    curPrjDir = mc.workspace(curPrj, q=True, fullName=True)  # noqa
    # mc.textField('posePathTxt', e=True, text=curPrjDir)
    mc.textField('posePathTxt', e=True, text='Z:/mtku/work/anim/')  # デフォルトパスを指定 # noqa


def ui(*args):  # noqa
    poseImgUI()
    getCurPrj()
    btnF.storeRefresh()

# referenceのネームスペースを取得して、ネームスペースが１つのreferenceだったらnameSpaceListへ加える


def getNss(*args):  # noqa
    # mc.textScrollList('nameSpList', e=True, removeAll=True)
    mc.popupMenu('nsPop', e=True, dai=True)
    mc.menuItem(p='nsPop', l='', c='cmds.frameLayout("nameSpList", e=True, l="");cmds.checkBox("replaceGp", e=True, v=False)')
    rn = mc.ls(type='reference')
    nsl = list_namespaces()
    if rn is not None:
        mc.menuItem(p='nsPop', l='-ReferenceNode-', bld=True)
        for ns in rn:
            if 0 < ns.count('sharedReferenceNode'):
                continue
            else:
                ns2 = ns.replace('RN', '')
                mc.menuItem(p='nsPop', l=ns2, c='cmds.frameLayout("nameSpList", e=True, l="{}")'.format(ns2))
    if nsl is not None:
        mc.menuItem(p='nsPop', l='-Namespace-', bld=True)
        for nss in nsl:
            mc.menuItem(p='nsPop', l=nss, c='cmds.frameLayout("nameSpList", e=True, l="{}")'.format(nss))


def list_namespaces():  # noqa
    exclude_list = ['UI', 'shared']

    current = mc.namespaceInfo(cur=True)
    mc.namespace(set=':')
    namespaces = ['{}'.format(ns) for ns in mc.namespaceInfo(lon=True) if ns not in exclude_list]
    mc.namespace(set=current)

    return namespaces


def enterCommand(*args):  # noqa
    posePath = mc.textField('posePathTxt', q=True, text=True)
    menus = mc.popupMenu('pathPop', q=True, ia=True)
    excludeList = '-|&'
    if posePath == '':
        pass
    else:
        dirPath = re.sub(r'\\', '/', posePath)
        if 0 < dirPath.count(r'\/'):
            setPathA = dirPath.replace(r'\/', '/')
        elif 0 < dirPath.count(r'/\\'):
            setPathA = dirPath.replace(r'/\\', '/')
        elif 0 < dirPath.count('/'):
            setPathA = dirPath
        if setPathA[-1] == '/':
            setPathB = setPathA
        else:
            setPathB = '{}/'.format(setPathA)
        if 0 < setPathB.count('store'):
            setPathC = setPathB.split('store')
            mc.textField('posePathTxt', e=True, text=setPathC[0])
            memoryPath = setPathC[0]
        else:
            mc.textField('posePathTxt', e=True, text=setPathB)
            memoryPath = setPathB
        btnF.storeRefresh()
        items = ','.join(list(set(menus)))
        gpMem = memoryPath.replace('/', '_')
        if 0 < items.count(gpMem):
            pass
        else:
            rep = re.sub(r'{}'.format(excludeList), '_', gpMem)
            if 0 < items.count(rep):
                pass
            else:
                mc.menuItem(gpMem, p='pathPop', l=memoryPath, c='{}.setPath("{}")'.format(uiFunc, memoryPath))


def optionUi(*args):
    wintitle = 'ImportOptionWindow'
    if mc.window(wintitle, q=True, exists=True):
        mc.deleteUI(wintitle)
    win = mc.window(wintitle, t=wintitle)

    flag = {}
    flag['nc'] = 5
    flag['adj'] = True
    transform = ['all_Translate', 'tx', 'ty', 'tz', 'all_Rotate', 'rx', 'ry', 'rz', 'all_Scale', 'sx', 'sy', 'sz']

    mc.columnLayout('colMain')
    mc.frameLayout('imframeA', l=u'現在の値からポーズの値を計算', mw=170, mh=20, h=20, ann=u'')  # noqa
    mc.setParent('..')

    mc.columnLayout('colA', adj=True)
    mc.rowLayout('rowA', **flag)
    for trs in transform:
        if trs in transform[1:4]:
            mc.checkBox('{}_CB'.format(trs), label='Translate{}'.format(trs.split('t')[1].upper()), align='left')
        elif trs in transform[5:8]:
            mc.checkBox('{}_CB'.format(trs), label='Rotate{}'.format(trs.split('r')[1].upper()), align='left')
        elif trs in transform[9:12]:
            mc.checkBox('{}_CB'.format(trs), label='Scale{}'.format(trs.split('s')[1].upper()), align='left')
        elif trs.count('all') == 1:
            mc.checkBox('{}_CB'.format(trs), label=trs, align='left')
            if trs.count('_Translate') == 1:
                mc.checkBox('{}_CB'.format(trs), e=True, onc="{}.allCheckOn('{}', {})".format(uiFunc, trs, transform), ofc="{}.allCheckOff('{}', {})".format(uiFunc, trs, transform))
            elif trs.count('_Rotate') == 1:
                mc.checkBox('{}_CB'.format(trs), e=True, onc="{}.allCheckOn('{}', {})".format(uiFunc, trs, transform), ofc="{}.allCheckOff('{}', {})".format(uiFunc, trs, transform))
            elif trs.count('_Scale') == 1:
                mc.checkBox('{}_CB'.format(trs), e=True, onc="{}.allCheckOn('{}', {})".format(uiFunc, trs, transform), ofc="{}.allCheckOff('{}', {})".format(uiFunc, trs, transform))
        if trs in transform[3::4]:
            mc.setParent('..')
            mc.rowLayout(**flag)
    mc.setParent('..')

    mc.columnLayout()
    mc.rowLayout('rowB', **flag)
    mc.radioCollection('RGOC')
    mc.radioButton('adBtn', label=u'+ Add', sl=True)
    mc.radioButton('sbBtn', label=u'- Subtract')
    mc.radioButton('mtBtn', label=u'* Multiply')
    mc.radioButton('dvBtn', label=u'/ Divide')
    mc.setParent('..')

    mc.columnLayout('colB', adj=True)
    mc.rowLayout('rowC', **flag)
    mc.floatSliderGrp('fsg', field=True, pre=6, minValue=-100.00000000, maxValue=100.00000000, fieldMinValue=-100.00000000, fieldMaxValue=100.00000000, value=0, cw=[2, 150])
    mc.button(l='zero', c="mc.floatSliderGrp('fsg', e=True, value=0)")
    mc.button(l='done', c='{}.addSubMultDivide()'.format(uiFunc))
    mc.setParent('..')

    mc.frameLayout('imframeB', l=u'指定したポイントから反転', mw=170, mh=20, h=20, ann=u'')  # noqa
    mc.setParent('..')

    mc.rowLayout('rowD', **flag)
    for trs in transform:
        if trs in transform[9:12]:
            continue
        if trs in transform[1:4]:
            mc.checkBox('{}_rCB'.format(trs), label='Translate{}'.format(trs.split('t')[1].upper()), align='left')
        elif trs in transform[5:8]:
            mc.checkBox('{}_rCB'.format(trs), label='Rotate{}'.format(trs.split('r')[1].upper()), align='left')
        elif trs in transform[9:12]:
            mc.checkBox('{}_rCB'.format(trs), label='Scale{}'.format(trs.split('s')[1].upper()), align='left')
        if trs.count('all') == 1:
            if trs != 'all_Scale':
                mc.checkBox('{}_rCB'.format(trs), label=trs, align='left')
                if trs.count('_Translate') == 1:
                    mc.checkBox('{}_rCB'.format(trs), e=True, onc="{}.revallCheckOn('{}', {})".format(uiFunc, trs, transform), ofc="{}.revallCheckOff('{}', {})".format(uiFunc, trs, transform))
                elif trs.count('_Rotate') == 1:
                    mc.checkBox('{}_rCB'.format(trs), e=True, onc="{}.revallCheckOn('{}', {})".format(uiFunc, trs, transform), ofc="{}.revallCheckOff('{}', {})".format(uiFunc, trs, transform))
        if trs in transform[3::4]:
            mc.setParent('..')
            mc.rowLayout(**flag)

    mc.setParent('..')
    mc.rowLayout('rowE', **flag)
    mc.checkBox('rev_CB', l=u'反転の有無:倍率', ann=u'基準となるロケータを選択しているオブジェクトの位置に作成')
    mc.floatSliderGrp('revfsg', field=True, pre=6, minValue=-100.00000000, maxValue=100.00000000, fieldMinValue=-100.00000000, fieldMaxValue=100.00000000, value=1, cw=[2, 150])
    mc.setParent('..')

    mc.frameLayout('imframeC', l=u'値が変更されたオブジェクト', mw=170, mh=20, h=20, ann=u'')  # noqa
    mc.setParent('..')

    mc.columnLayout(adj=True)
    mc.rowLayout('rowF', **flag)
    mc.textField('insertTextA', tx=u'.*検索する文字.*検索する文字.*', ed=False)
    mc.button(l=u'検索をリセット', c="mc.textFieldGrp('search', e=True, tx='.*.*');{}.searchList()".format(uiFunc))
    mc.setParent('..')

    mc.textFieldGrp('search', tx='.*.*', cc='{}.searchList()'.format(uiFunc), fcc=True, cw=[1, 340])
    mc.textFieldGrp('getImportObj', tx='', vis=False)
    mc.rowLayout('rowG', **flag)
    mc.scrollLayout()
    mc.textScrollList('changeAttrTsl', numberOfRows=8, allowMultiSelection=True, append=[''], showIndexedItem=4, h=300, w=335, sc="{}.selectList()".format(uiFunc), dcc="{}.selectAll()".format(uiFunc), ann=u'ダブルクリック:全選択\n右クリック:検索する文字に挿入')
    popup = mc.popupMenu('scrPop', b=0)
    mc.menuItem(p=popup, l=u'検索する文字に挿入', c="{}.insertSearxhText()".format(uiFunc))
    mc.setParent('..')

    mc.setParent('..')

    mc.rowLayout('rowH', **flag)
    mc.text("objectsTxt", l=u"オブジェクト数:")
    mc.text("objectSels", l=u"選択数:0")
    mc.setParent('..')

    mc.showWindow()
    mc.scriptJob(e=['SelectionChanged', "{}.lenObj();{}.insertList()".format(uiFunc, uiFunc)], p=win, rp=True)


def allCheckOn(trs, transform):
    if trs == 'all_Translate':
        for attr in transform[1:4]:
            mc.checkBox('{}_CB'.format(attr), e=True, v=True)
    elif trs == 'all_Rotate':
        for attr in transform[5:8]:
            mc.checkBox('{}_CB'.format(attr), e=True, v=True)
    elif trs == 'all_Scale':
        for attr in transform[9:12]:
            mc.checkBox('{}_CB'.format(attr), e=True, v=True)


def allCheckOff(trs, transform):
    if trs == 'all_Translate':
        for attr in transform[1:4]:
            mc.checkBox('{}_CB'.format(attr), e=True, v=False)
    elif trs == 'all_Rotate':
        for attr in transform[5:8]:
            mc.checkBox('{}_CB'.format(attr), e=True, v=False)
    elif trs == 'all_Scale':
        for attr in transform[9:12]:
            mc.checkBox('{}_CB'.format(attr), e=True, v=False)


def revallCheckOn(trs, transform):
    if trs == 'all_Translate':
        for attr in transform[1:4]:
            mc.checkBox('{}_rCB'.format(attr), e=True, v=True)
    elif trs == 'all_Rotate':
        for attr in transform[5:8]:
            mc.checkBox('{}_rCB'.format(attr), e=True, v=True)
    elif trs == 'all_Scale':
        for attr in transform[9:12]:
            mc.checkBox('{}_rCB'.format(attr), e=True, v=True)


def revallCheckOff(trs, transform):
    if trs == 'all_Translate':
        for attr in transform[1:4]:
            mc.checkBox('{}_rCB'.format(attr), e=True, v=False)
    elif trs == 'all_Rotate':
        for attr in transform[5:8]:
            mc.checkBox('{}_rCB'.format(attr), e=True, v=False)
    elif trs == 'all_Scale':
        for attr in transform[9:12]:
            mc.checkBox('{}_rCB'.format(attr), e=True, v=False)


def selectList(*args):
    try:
        sl = mc.textScrollList('changeAttrTsl', q=True, si=True)
        mc.select(list(set(sl)), r=True)
    except:  # noqa
        pass


def selectAll(*args):
    try:
        num = mc.textScrollList('changeAttrTsl', q=True, ni=True)
        for s in range(num):  # noqa
            mc.textScrollList('changeAttrTsl', e=True, sii=s+1)  # noqa
        selectList()
    except:  # noqa
        pass


def searchList(*args):
    fi = mc.textFieldGrp('getImportObj', q=True, tx=True)
    fis = fi.split(',')
    stext = mc.textFieldGrp('search', q=True, tx=True)
    # all = mc.textScrollList('changeAttrTsl', q=True, ai=True)
    mc.textScrollList('changeAttrTsl', e=True, ra=True)
    m = [s for s in fis if re.match(stext, s)]
    if m != []:
        m.sort()
        for name in m:
            mc.textScrollList('changeAttrTsl', e=True, a=name)
    elif m in fis:
        fis.sort()
        for name in fis:
            mc.textScrollList('changeAttrTsl', e=True, a=name)
    objectLength()


def addSubMultDivide():
    try:
        sel = mc.ls(sl=True)
        if mc.checkBox('tx_CB', q=True, ex=True):
            imtx = mc.checkBox('tx_CB', q=True, v=True)
        if mc.checkBox('ty_CB', q=True, ex=True):
            imty = mc.checkBox('ty_CB', q=True, v=True)
        if mc.checkBox('tz_CB', q=True, ex=True):
            imtz = mc.checkBox('tz_CB', q=True, v=True)
        if mc.checkBox('rx_CB', q=True, ex=True):
            imrx = mc.checkBox('rx_CB', q=True, v=True)
        if mc.checkBox('ry_CB', q=True, ex=True):
            imry = mc.checkBox('ry_CB', q=True, v=True)
        if mc.checkBox('rz_CB', q=True, ex=True):
            imrz = mc.checkBox('rz_CB', q=True, v=True)
        if mc.checkBox('sx_CB', q=True, ex=True):
            imsx = mc.checkBox('sx_CB', q=True, v=True)
        if mc.checkBox('sy_CB', q=True, ex=True):
            imsy = mc.checkBox('sy_CB', q=True, v=True)
        if mc.checkBox('sz_CB', q=True, ex=True):
            imsz = mc.checkBox('sz_CB', q=True, v=True)
        transform = {'translateX': imtx, 'translateY': imty, 'translateZ': imtz, 'rotateX': imrx, 'rotateY': imry, 'rotateZ': imrz, 'scaleX': imsx, 'scaleY': imsy, 'scaleZ': imsz}
        radioname = mc.radioCollection('RGOC', q=True, sl=True)
        option = {'adBtn': 'Add', 'sbBtn': 'Subtract', 'mtBtn': 'Multiply', 'dvBtn': 'Divide'}
        slideValue = mc.floatSliderGrp('fsg',  q=True, v=True)
        for obj in sel:
            for attr in transform.keys():
                attrValue = mc.getAttr('{}.{}'.format(obj, attr))
                if transform[attr] == True:  # noqa
                    if option[radioname] == 'Add':
                        mc.setAttr('{}.{}'.format(obj, attr), attrValue + slideValue)
                    elif option[radioname] == 'Subtract':
                        mc.setAttr('{}.{}'.format(obj, attr), attrValue - slideValue)
                    elif option[radioname] == 'Multiply':
                        mc.setAttr('{}.{}'.format(obj, attr), attrValue * slideValue)
                    elif option[radioname] == 'Divide':
                        mc.setAttr('{}.{}'.format(obj, attr), attrValue / slideValue)
    except:  # noqa
        pass


def modelPanelShot(*args):
    sel = mc.ls(sl=True)
    wintitle = 'Thumbnail'
    cam = 'dupPerspThumbnailCam'
    if mc.window(wintitle, q=True, exists=True):
        mc.deleteUI(wintitle)
    win = mc.window(wintitle, s=False, w=500, h=500)
    mc.paneLayout('mppl', w=504, h=543)
    sp = mc.modelPanel(mbv=True, p=win, l='ThumbnailModelPanel')
    mc.setFocus(sp)
    if mc.objExists(cam):
        mc.delete(cam)
    dupCam = mc.duplicate('persp', n=cam)
    mm.eval('lookThroughModelPanel {} {};'.format(dupCam[0], sp))
    mc.modelEditor(sp, e=True, manipulators=False, sel=False, hud=False)
    mm.eval('DisplayShadedAndTextured;')
    mc.inViewMessage(hd=True)
    mc.showWindow()
    mc.scriptJob(uiDeleted=[win, '{}.delCam("{}")'.format(uiFunc, dupCam[0])])
    mc.scriptJob(e=['NewSceneOpened', "{}.reboot_modelPanelShot('{}')".format(uiFunc, win)], p=win, rp=True)
    mc.scriptJob(e=['SceneOpened', "{}.reboot_modelPanelShot('{}')".format(uiFunc, win)], p=win, rp=True)
    mc.button('shotButton', e=True, en=False)
    mc.select(cam, r=True)
    mm.eval('doHideInOutliner 1;')
    mc.select(sel, r=True)
    mc.inViewMessage(hd=False)


def reboot_modelPanelShot(win):
    mc.deleteUI(win)
    # modelPanelShot()


def delCam(cam):
    try:
        mc.delete(cam)
    except Exception as e:  # noqa
        print e  # noqa

    if mc.button('shotButton', q=True, en=True) == False:  # noqa
        mc.button('shotButton', e=True, en=True)


def objectLength(*args):
    sel = mc.ls(sl=True)
    all = mc.textScrollList('changeAttrTsl', q=True, ai=True)
    try:
        mc.text("objectsTxt", e=True, l=u"オブジェクト数:{}".format(len(all)))
    except TypeError as e:
        mc.text("objectsTxt", e=True, l=u"オブジェクト数:0")
        print 'Error:{}'.format(e)


def insertSearxhText():
    try:
        scrSel = mc.textScrollList('changeAttrTsl', q=True, si=True)
        for set in scrSel:
            if mc.textFieldGrp('search', q=True, tx=True) == '.*.*':
                mc.textFieldGrp('search', e=True, tx='.*{}.*'.format(set))
            else:
                searchTex = mc.textFieldGrp('search', q=True, tx=True)
                mc.textFieldGrp('search', e=True, tx='{}{}.*'.format(searchTex, set))
    except Exception as e:
        print 'Error:{}'.format(e)
    searchList()


def insertText(args):
    if mc.textFieldGrp('search', q=True, tx=True) == '.*.*':
        mc.textFieldGrp('search', e=True, tx='.*{}.*'.format(args))
    else:
        searchTex = mc.textFieldGrp('search', q=True, tx=True)
        mc.textFieldGrp('search', e=True, tx='{}{}.*'.format(searchTex, args))
    searchList()


def lenObj():
    sel = mc.ls(sl=True)
    mc.text("objectSels", e=True, l=u'選択数:{}'.format(len(sel)))


def insertList():
    try:
        seps = []
        scrSel = mc.textScrollList('changeAttrTsl', q=True, si=True)
        for scrs in scrSel:
            if '_' in scrs:
                sep = scrs.split('_')
                for s in sep:
                    if '_{}'.format(s) in scrs:  # noqa
                        seps.append('_'+s)  # noqa
                    if '{}_'.format(s) in scrs:  # noqa
                        seps.append(str(s+'_'))  # noqa
            if ':' in scrs:
                sep = scrs.split(':')
                for s in sep:
                    if ':{}'.format(s) in scrs:  # noqa
                        seps.append(':'+s)  # noqa
                    if '{}:'.format(s) in scrs:  # noqa
                        seps.append(str(s+':'))  # noqa

        wordList = list(set(seps))
        mc.popupMenu('scrPop', e=True, dai=True)
        mc.menuItem(p='scrPop', l=u'検索する文字に挿入', c="{}.insertSearxhText()".format(uiFunc))
        wordList.sort()
        for word in wordList:
            mc.menuItem(p='scrPop', l=word, c="{}.insertText('{}')".format(uiFunc, word))
    except:  # noqa
        pass
