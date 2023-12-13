# -*- coding: utf-8 -*-
#=========================================================================== # noqa
# Cygames Tools # noqa
# buttonFuncs.py # noqa
# # noqa
# Copyright 2017, Cygames Inc. # noqa
#=========================================================================== # noqa

import maya.cmds as mc
import mtk3d.maya.rig.cyPoseStore
import mtk3d.maya.rig.cyPoseStore.writeJSON as wJsn  # noqa
import mtk3d.maya.rig.cyPoseStore.importJSON as iJsn

uiFunc = 'import mtk3d.maya.rig.cyPoseStore.ui as ui;ui'

from functools import partial  # noqa
import os  # noqa
import os.path  # noqa
import glob  # noqa
import re  # noqa

import time


reload(mtk3d.maya.rig.cyPoseStore.writeJSON)  # noqa
reload(mtk3d.maya.rig.cyPoseStore.importJSON)  # noqa

# ブラウズ用関数


def txtBrows(*args):
    txtDir = mc.fileDialog2(fileMode=3, returnFilter=True, okc='select', caption="select")
    menus = mc.popupMenu('pathPop', q=True, ia=True)
    excludeList = '-|&'
    if txtDir:
        txtDir[0].replace('\\', '/')
        mc.textField('posePathTxt', edit=True, text=(txtDir[0] + '/'))
        pDir = mc.textField('posePathTxt', q=True, text=True)  # noqa
        if re.findall(r'store/.*', pDir) == [] or re.findall(r'store/.*', pDir)[0] == 'store/':
            mc.textField('posePathTxt', e=True, text=pDir.split('store/')[0])
        storeRefresh()
        items = ','.join(list(set(menus)))
        gpMem = pDir.replace('/', '_')
        if 0 < items.count(gpMem):
            pass
        else:
            rep = re.sub(r'{}'.format(excludeList), '_', gpMem)
            if 0 < items.count(rep):
                pass
            else:
                mc.menuItem(gpMem, p='pathPop', l=pDir, c='{}.setPath("{}")'.format(uiFunc, pDir))
    else:
        pass


# カレントプロジェクト取得
def getCurPrj(*args):
    curPrj = mc.workspace(q=True, active=True)
    curPrjDir = mc.workspace(curPrj, q=True, fullName=True)
    mc.textField('posePathTxt', e=True, text=curPrjDir)


# 指定のディレクトリにStore作成
def makeStore(*args):
    pDir = mc.textField('posePathTxt', q=True, text=True)
    ppDir = (pDir + 'store')
    sts = os.path.exists(ppDir)
    if sts == True:  # noqa
        result = ('<' + str(ppDir) + u' ストアーは既に存在します。>')
        mc.textField('messagesTxt', e=True, text=(result))
    else:
        os.mkdir(ppDir)
        result = ('<' + str(ppDir) + u'にストアーを作成しました。>')
        mc.textField('messagesTxt', e=True, text=(result))
        os.mkdir(ppDir + '/poses')


# tabを作成する
def createTabs(*args):
    tabName = mc.textField('tabTxt', q=True, text=True)
    if tabName == '':
        mc.warning(u'タブ名を入力して下さい！')
    else:
        pDir = mc.textField('posePathTxt', q=True, text=True)
        poseDir = (pDir + 'store')
        stsA = os.path.exists(poseDir)
        if stsA == False:  # noqa
            mc.warning(u'==========<storeが存在しません。storeを作成して下さい。>===========')
        else:
            ppDir = (pDir + 'store/' + tabName)
            sts = os.path.exists(ppDir)
            if sts == True:  # noqa
                mc.warning(u'==========<' + ppDir + u'は既に存在しています。別のタブ名に変更して下さい。>===========')
            else:
                uisFull = mc.lsUI(type=['control'], l=True)
                exui = tabName
                exTab = []
                exTabPathA = []
                exTabPathB = []
                exTabPathC = []
                for ui in uisFull:  # noqa
                    matchUi = re.findall(r'.*tablayouts.*scrollLayout.*{}.*'.format(exui), ui)
                    if matchUi == []:
                        continue
                    else:
                        exTab.append(matchUi[0])
                        for matchTab in exTab:
                            exTabPathA = matchTab.split('tablayouts|')
                            exTabPathB = exTabPathA[1].split('|')
                            try:
                                if exTabPathB[3] == exui:
                                    exTabPathC.append(u'1段目:{}/2段目:{}'.format(exTabPathB[0], exTabPathB[3]))
                            except:  # noqa
                                if exTabPathB[0] == exui:
                                    exTabPathC.append(u'1段目:{}/2段目:{}'.format(exTabPathB[0], exTabPathB[3]))
                if 0 < len(exTabPathC):
                    mc.warning(u'==========<' + exui + u'は下記のタブに既に存在しています。タブ名を変更して下さい。>===========\n{}'.format('\n'.join(set(exTabPathC))))
                else:
                    os.mkdir(ppDir)
                    result = ('<' + str(ppDir) + u'にストアーを作成しました。>')
                    mc.textField('messagesTxt', e=True, text=(result))
                    rows = mc.rowColumnLayout(tabName, numberOfColumns=2, p='tablayouts')  # noqa
                    mc.textField('tabTxt', e=True, text='')

# 全ボタンのデリート


def delBtn(*args):
    nPoses = mc.rowColumnLayout('poseImg', q=True, nch=True)  # noqa
    poses = mc.rowColumnLayout('poseImg', q=True, childArray=True)
    if poses is not None:
        len(poses)
        for i in poses:
            mc.deleteUI(i)

# 全タブを削除


def delTabs(*args):
    poses = mc.tabLayout('tablayouts', q=True, childArray=True)
    if poses is not None:
        PathA = mc.textField('posePathTxt', q=True, text=True)
        PathB = PathA + 'store/'
        numDir = PathB.split('/')
        numDir.remove('')
        len(numDir)
        dirNum = len(poses)
        for i in range(0, dirNum, 1):
            mc.deleteUI(poses[i])
    else:
        pass


# 指定ディレクトリの全ポーズボタン追加
def mkAllPoseBtn(*args):
    percent = mc.intField('thumbSiz', q=True, value=True)
    pDir = mc.textField('posePathTxt', q=True, text=True)
    imgSize = 256 * (percent * 0.010)
    path = pDir + 'store/'
    print 'pDir: ', pDir
    sts = os.path.exists(path)
    tabs = []
    errorDialog = []
    endtime0 = 0
    endtime1 = 0
    if sts == True:  # noqa
        storeFolders = glob.glob('{}/*'.format(path))
        # sFol = storeFolders
        for sFol in storeFolders:
            sPath = sFol.replace('\\', '/')
            sFiles = glob.glob('{}/*'.format(sPath))
            sumPath = ''.join(sFiles)
            if sumPath.count('.json') > 0 or sumPath.count('.json') > 0:
                # mc.warning(u'<{}のフォルダ構成を見直してください。>'.format(sPath))
                errorDialog.append(sPath)
            else:
                # print sPath
                tabNames = sPath.split('/')
                tabName = tabNames[-1]
                tabs.append(tabNames[-1])  # タブ名取得
                rows = mc.rowColumnLayout(tabName, numberOfColumns=3, p='tablayouts')  # noqa
                tabs = []
                # pFil = sFiles
                for i in range(len(sFiles)):
                    pPath = sFiles[i].replace('\\', '/')
                    poseFolders = glob.glob('{}/*'.format(pPath))
                    sumPath = ''.join(poseFolders)
                    if poseFolders == []:
                        if i == 0:
                            tabNames = pPath.split('/')
                            tabName = tabNames[-1]
                            tabs.append(tabNames[-1])  # タブ名取得
                            mc.tabLayout('tablayouts', e=True, st=rows)
                            mc.textField('tabTxt', e=True, text=tabName)
                            rowsB = downAddMainRefresh(0)
                            tabs = []  # noqa
                        elif i > 0:  # noqa
                            try:
                                if rowsB != None:  # noqa
                                    tabNames = pPath.split('/')
                                    tabName = tabNames[-1]
                                    tabs.append(tabNames[-1])  # タブ名取得
                                    mc.tabLayout('tablayouts', e=True, st=rows)
                                    mc.textField('tabTxt', e=True, text=tabName)
                                    rowsB = sideAddMainRefresh(0)
                                    # sideAddMainRefresh
                                    tabs = []
                                else:
                                    pass
                            except Exception as e:  # 失敗したら
                                tabNames = pPath.split('/')
                                tabName = tabNames[-1]
                                tabs.append(tabNames[-1])  # タブ名取得
                                mc.tabLayout('tablayouts', e=True, st=rows)
                                mc.textField('tabTxt', e=True, text=tabName)
                                rowsB = downAddMainRefresh(0)
                                tabs = []

                    else:

                        if sumPath.count('.json') > 0 or sumPath.count('.json') > 0:
                            # mc.warning(u'<{}のフォルダ構成を見直してください。>'.format(pPath))
                            errorDialog.append(pPath)
                        else:
                            # pFol = poseFolders
                            if i == 0:
                                tabNames = pPath.split('/')
                                tabName = tabNames[-1]
                                tabs.append(tabNames[-1])  # タブ名取得
                                mc.tabLayout('tablayouts', e=True, st=rows)
                                mc.textField('tabTxt', e=True, text=tabName)
                                rowsB = downAddMainRefresh(0)
                                tabs = []
                                start = time.time()
                                iconButtonSetup( rowsB,poseFolders,tabName,imgSize)
                                calcTime = time.time() -start
                                endtime0 += calcTime
                            elif i > 0:
                                tabNames = pPath.split('/')
                                tabName = tabNames[-1]
                                tabs.append(tabNames[-1])  # タブ名取得
                                mc.tabLayout('tablayouts', e=True, st=rows)
                                mc.textField('tabTxt', e=True, text=tabName)
                                rowsC = sideAddMainRefresh(0)
                                tabs = []
                                start = time.time()
                                iconButtonSetup( rowsC,poseFolders,tabName,imgSize)
                                calcTime = time.time() - start
                                endtime1 += calcTime


    else:
        mc.warning(u'<ストアーが存在していません。ストアーを作成して下さい。>')
        mc.textField('messagesTxt', e=True, text=u'<ストアーが存在していません。ストアーを作成して下さい。>')

    if errorDialog != []:
        errorPath = '\n'.join(errorDialog)
        mc.confirmDialog(t=u'Warning', b=u'確認します',  m=u'下記のフォルダ構成を見直してください。\n正しくは../store/main/sub/pose/です。\n----------------------------------------------\n{}'.format(errorPath))

        print(u'-------------------------------------------------\n下記のフォルダ構成を見直してください。\n{}\n-------------------------------------------------'.format(errorPath))
    else:
        pass
def iconButtonSetup( row,poseFolders,tabName,imgSize ):
    for pFol in poseFolders:
        pPathA = pFol.replace('\\', '/')
        poses = glob.glob('{}/*'.format(pPathA))
        # print poses
        pngpath = poses[1].replace('\\', '/')
        Jpath = poses[0].replace('\\', '/')
        Img = pPathA.split('/')
        lbl = Img[-1]
        if tabName == Img[-2]:
            mc.iconTextButton(pngpath, parent=row, width=imgSize, h=imgSize, label=lbl[0], ann=lbl[0],
                             fla=True, style='iconAndTextVertical', sic=True, image1=pngpath,
                            c=partial(iJsn.importJSON, Jpath))
            popup = mc.popupMenu(b=0)
            pngpath2 = pngpath.replace('.', '/')
            mc.menuItem(p=popup, l=u'ポーズ名をコピーする',
                        c='cmds.textField("poseNameTxt", e=True, text="{}")'.format(lbl[0]))
            mc.menuItem(p=popup, l=u'ポーズを置き換える',
                        c="""import shutil;shutil.rmtree("{}");cmds.evalDeferred('cmds.deleteUI("{}")');cmds.textField("poseNameTxt", e=True, text="{}");import mtk3d.maya.rig.cyPoseStore.writeJSON as wJsn;wJsn.makeButton()""".format(
                            pPathA, pngpath2, lbl[0]))
            mc.menuItem(p=popup, l=u'エクスプローラーで開く',
                        c='import subprocess;subprocess.Popen("explorer {}")'.format(r''.join(pFol)))
            mc.menuItem(p=popup, l=u'削除',
                        c="""import shutil;shutil.rmtree("{}");cmds.evalDeferred('cmds.deleteUI("{}")')""".format(
                            pPathA, pngpath2))
        else:
            pass

def storeRefresh(*args):
    # delBtn()
    delTabs()
    mkAllPoseBtn()

def getRbtn(*args):
    radio = mc.radioCollection('selTabCollection', q=True, sl=True)
    import mtk3d.maya.rig.cyPoseStore.buttonFuncs as btnF
    mod = 'import mtk3d.maya.rig.cyPoseStore.buttonFuncs as btnF;btnF'

    if radio == 'rootTab':
        mc.button('addTabBtnDown', e=True, en=False)
        mc.button('addTabBtnSide', e=True, c=btnF.createTabs, en=True, label=u'1段目に追加')
    elif radio == 'aTab':
        mc.button('addTabBtnDown', e=True, c='{};btnF.downAddMain(0)'.format(mod), en=True, label=u'2段目に追加')
        mc.button('addTabBtnSide', e=True, c='{};btnF.sideAddMain(0)'.format(mod), en=True, label=u'2段目横に追加')
    elif radio == 'bTab':
        mc.button('addTabBtnDown', e=True, c='{};btnF.downAddMain(1)'.format(mod), en=True)
        mc.button('addTabBtnSide', e=True, c='{};btnF.sideAddMain(1)'.format(mod))
    elif radio == 'cTab':
        mc.button('addTabBtnDown', e=True, c='{};btnF.downAddMain(2)'.format(mod), en=True)
        mc.button('addTabBtnSide', e=True, c='{};btnF.sideAddMain(2)'.format(mod))

    # print radio
    return radio


def getTabPath():
    row = mc.tabLayout('tablayouts', q=True, st=True)

    tab_root = row

    loop = 0
    path = []

    while loop < 5:
        scr = mc.rowColumnLayout(row, q=True, ca=True)
        if scr == None:  # noqa
            pass
        else:
            sts = 1 == scr[0].count(':_')
            # scr = None

        if scr != None and sts == False:  # noqa
            tab = mc.scrollLayout(scr[0], q=True, ca=True)
            row = mc.tabLayout(tab, q=True, st=True)
            path.append(row)
        elif scr == None or sts == True:  # noqa
            break

        loop += 1

    path_A = '/'.join(path)
    tabToPath = '{}/{}'.format(tab_root, path_A)
    # print tabToPath
    return tabToPath


def createSubCat():
    tabToPath = getTabPath()
    tabName = mc.textField('tabTxt', q=True, text=True)
    if tabName is None:
        mc.warning(u'タブ名を入力して下さい！')
    else:
        pDir = mc.textField('posePathTxt', q=True, text=True)
        poseDir = (pDir + 'store')
        stsA = os.path.exists(poseDir)
        if stsA == False:  # noqa
            mc.warning(u'==========<storeが存在しません。storeを作成して下さい。>===========')
        else:
            tabValue = getRbtn()
            if tabValue == 'rootTab':
                pass
            else:
                subPath = tabToPath.split('/')
                tabToPath = '/'.join(subPath[0:-1])
                ppDir = (pDir + 'store/' + tabToPath + '/' + tabName)
                sts = os.path.exists(ppDir)
                if sts == True:  # noqa
                    mc.warning(u'==========<' + ppDir + u'は既に存在しています。別のタブ名に変更して下さい。>===========')
                else:
                    os.makedirs(ppDir)
                    result = ('<' + str(ppDir) + u'にストアーを作成しました。>')
                    mc.textField('messagesTxt', e=True, text=(result))
                    mc.textField('tabTxt', e=True, text='')


def downAddMain(num):
    dict = {0: 'A', 1: 'B', 2: 'C'}
    tabName = mc.textField('tabTxt', q=True, text=True)
    if tabName == '':
        mc.warning(u'タブ名を入力して下さい！')
    else:
        uisFull = mc.lsUI(type=['control'], l=True)
        exui = tabName
        exTab = []
        exTabPathA = []
        exTabPathB = []
        exTabPathC = []
        for ui in uisFull:  # noqa
            matchUi = re.findall(r'.*tablayouts.*{}.*'.format(exui), ui)
            if matchUi == []:
                continue
            else:
                exTab.append(matchUi[0])
                for matchTab in exTab:
                    exTabPathA = matchTab.split('tablayouts|')
                    exTabPathB = exTabPathA[1].split('|')
                    if exTabPathB[0] == exui:
                        exTabPathC.append(u'1段目:{}'.format(exTabPathB[0]))

        if 0 < len(exTabPathC):
            mc.warning(u'==========<' + exui + u'は下記のタブに既に存在しています。タブ名を変更して下さい。>===========\n{}'.format('\n'.join(set(exTabPathC))))
        else:
            tabToPath = getTabPath()
            splPath = tabToPath.split('/')
            joinPath = ''.join(splPath)
            if tabName == joinPath:
                mc.warning(u'<1段目に同じ名前のタブが追加されています。別名に変更してください。>')
            else:
                if splPath[0] != joinPath:
                    mc.warning(u'<このタブの2段目はすでに追加されています。横列に追加してください。>')
                else:
                    mainTab = mc.tabLayout('tablayouts', q=True, st=True)

                    if num == 0:
                        curTab = mainTab
                        newScrFrom = []
                    elif num == 1:
                        parentTab = '{}_{}'.format(mainTab, dict[num - 1])
                        curTab = mc.tabLayout(parentTab, q=True, st=True)
                        scr = mc.tabLayout(parentTab, q=True, p=True)

                        newScrFrom = '{}|{}|{}'.format(scr, parentTab, curTab)

                    elif num == 2:
                        parentTab = '{}_{}'.format(mainTab, dict[num - 2])
                        tab_A = mc.tabLayout(parentTab, q=True, st=True)
                        scr_A = mc.tabLayout(parentTab, q=True, p=True)
                        row_A = '{}|{}|{}'.format(scr_A, parentTab, tab_A)

                        scr_B = mc.rowColumnLayout(row_A, q=True, ca=True)
                        tab_B = mc.scrollLayout(scr_B[0], q=True, ca=True)

                        tab_C = '{}|{}|{}'.format(row_A, scr_B[0], tab_B[0])

                        curTab = mc.tabLayout(tab_C, q=True, st=True)

                        newScrFrom = '{}|{}'.format(tab_C, curTab)

                    if num == 0:
                        newScrTo = mc.scrollLayout(p=curTab, h=1000, w=800)
                        tabs = mc.tabLayout('{}_{}'.format(curTab, dict[num]), p=newScrTo, h=670, w=800, scr=True)
                    elif num == 1:
                        newScrTo = mc.scrollLayout(p=newScrFrom)
                        tabs = mc.tabLayout('{}_{}_{}'.format(mainTab, curTab, dict[num]), p=newScrTo)
                    elif num == 2:
                        newScrTo = mc.scrollLayout(p=newScrFrom)
                        tabs = mc.tabLayout('{}_{}_{}_{}'.format(mainTab, tab_A, curTab, dict[num]), p=newScrTo)

                    rows = mc.rowColumnLayout(tabName, numberOfColumns=3, p=tabs)
                    createSubCat()
                    return rows
                    del(num)


def sideAddMain(num):
    dict = {0: 'A', 1: 'B', 2: 'C'}  # noqa
    tabName = mc.textField('tabTxt', q=True, text=True)
    if tabName == '':
        mc.warning(u'タブ名を入力して下さい！')
    else:
        uisFull = mc.lsUI(type=['control'], l=True)
        exui = tabName
        exTab = []
        exTabPathA = []
        exTabPathB = []
        exTabPathC = []
        for ui in uisFull:  # noqa
            matchUi = re.findall(r'.*tablayouts.*{}.*'.format(exui), ui)
            if matchUi == []:
                continue
            else:
                exTab.append(matchUi[0])
                for matchTab in exTab:
                    exTabPathA = matchTab.split('tablayouts|')
                    exTabPathB = exTabPathA[1].split('|')
                    if exTabPathB[0] == exui:
                        exTabPathC.append(u'1段目:{}'.format(exTabPathB[0]))

        if 1 < len(exTabPathC):
            mc.warning(u'==========<' + exui + u'は下記のタブに既に存在しています。タブ名を変更して下さい。>===========\n{}'.format('\n'.join(set(exTabPathC))))
        else:
            tabToPath = getTabPath()
            splPath = tabToPath.split('/')
            # joinPath = ''.join(splPath)
            if tabName == splPath[0]:
                mc.warning(u'<1段目に同じ名前のタブが追加されています。別名に変更してください。>')
            else:
                mainTab = mc.tabLayout('tablayouts', q=True, st=True)
                scr = mc.tabLayout('tablayouts', q=True, p=True)

                if num == 0:
                    scr_A = mc.rowColumnLayout(mainTab, q=True, ca=True)
                    if scr_A == None:  # noqa
                        mc.warning(u'==========<2段目を追加してください。>===========')
                    else:
                        tab_A = mc.scrollLayout(scr_A, q=True, ca=True)

                        tabs = tab_A[0]
                elif num == 1:
                    scr_A = mc.rowColumnLayout(mainTab, q=True, ca=True)
                    tab_A = mc.scrollLayout(scr_A[0], q=True, ca=True)
                    row_A = mc.tabLayout(tab_A, q=True, st=True)

                    row = '{}|tablayouts|{}|{}|{}|{}'.format(scr, mainTab, scr_A[0], tab_A[0], row_A)

                    scr_B = mc.rowColumnLayout(row, q=True, ca=True)

                    if scr_B != None:  # noqa
                        tab_B = mc.scrollLayout(scr_B[0], q=True, ca=True)  # noqa
                        row_B = mc.tabLayout(tab_B, q=True, st=True)

                        rowTab = '{}|{}|{}'.format(row, scr_B[0], tab_B[0])

                        tabs = rowTab

                    elif scr_B == None:  # noqa
                        tabs = scr

                elif num == 2:
                    scr_A = mc.rowColumnLayout(mainTab, q=True, ca=True)
                    tab_A = mc.scrollLayout(scr_A[0], q=True, ca=True)
                    row_A = mc.tabLayout(tab_A, q=True, st=True)

                    scr = mc.rowColumnLayout(row_A, q=True, p=True)

                    row = '{}|{}'.format(scr, row_A)

                    scr_B = mc.rowColumnLayout(row, q=True, ca=True)
                    tab_B = mc.scrollLayout(scr_B[0], q=True, ca=True)
                    row_B = mc.tabLayout(tab_B, q=True, st=True)  # noqa

                    row_gp = '{}|{}|{}'.format(row, scr_B[0], tab_B[0])

                    tab_gp = mc.tabLayout(row_gp, q=True, st=True)

                    tab_sum = '{}|{}|{}|{}'.format(row, scr_B[0], tab_B[0], tab_gp)
                    scr_C = mc.rowColumnLayout(tab_sum, q=True, ca=True)
                    tab_C = mc.scrollLayout(scr_C, q=True, ca=True)

                    rowTab = '{}|{}|{}'.format(tab_sum, scr_C[0], tab_C[0])

                    tabs = rowTab
                if scr_A is None:
                    pass
                else:
                    try:
                        rows = mc.rowColumnLayout(tabName, numberOfColumns=3, p=tabs)
                        mc.tabLayout(tabs, e=True, st=tabName)
                        createSubCat()
                        return rows
                        del(num)

                    except Exception:
                        mc.warning(u'<このタブは既に追加されています。別名に変更してください。>')
                        rows = None


def downAddMainRefresh(num):
    dict = {0: 'A', 1: 'B', 2: 'C'}

    tabName = mc.textField('tabTxt', q=True, text=True)
    mainTab = mc.tabLayout('tablayouts', q=True, st=True)

    if num == 0:
        curTab = mainTab
        newScrFrom = []
    elif num == 1:
        parentTab = '{}_{}'.format(mainTab, dict[num - 1])
        curTab = mc.tabLayout(parentTab, q=True, st=True)
        scr = mc.tabLayout(parentTab, q=True, p=True)

        newScrFrom = '{}|{}|{}'.format(scr, parentTab, curTab)

    elif num == 2:
        parentTab = '{}_{}'.format(mainTab, dict[num - 2])
        tab_A = mc.tabLayout(parentTab, q=True, st=True)
        scr_A = mc.tabLayout(parentTab, q=True, p=True)
        row_A = '{}|{}|{}'.format(scr_A, parentTab, tab_A)

        scr_B = mc.rowColumnLayout(row_A, q=True, ca=True)
        tab_B = mc.scrollLayout(scr_B[0], q=True, ca=True)

        tab_C = '{}|{}|{}'.format(row_A, scr_B[0], tab_B[0])

        curTab = mc.tabLayout(tab_C, q=True, st=True)

        newScrFrom = '{}|{}'.format(tab_C, curTab)

    if num == 0:
        newScrTo = mc.scrollLayout(p=curTab, h=1000, w=800)
        tabs = mc.tabLayout('{}_{}'.format(curTab, dict[num]), p=newScrTo, h=670, w=800, scr=True)
    elif num == 1:
        newScrTo = mc.scrollLayout(p=newScrFrom)
        tabs = mc.tabLayout('{}_{}_{}'.format(mainTab, curTab, dict[num]), p=newScrTo)
    elif num == 2:
        newScrTo = mc.scrollLayout(p=newScrFrom)
        tabs = mc.tabLayout('{}_{}_{}_{}'.format(mainTab, tab_A, curTab, dict[num]), p=newScrTo)

    rows = mc.rowColumnLayout(tabName, numberOfColumns=3, p=tabs)
    # createSubCat()
    return rows
    del(num)


def sideAddMainRefresh(num):
    dict = {0: 'A', 1: 'B', 2: 'C'}  # noqa

    tabName = mc.textField('tabTxt', q=True, text=True)
    mainTab = mc.tabLayout('tablayouts', q=True, st=True)
    scr = mc.tabLayout('tablayouts', q=True, p=True)

    if num == 0:
        scr_A = mc.rowColumnLayout(mainTab, q=True, ca=True)
        if scr_A == None:  # noqa
            rows = downAddMainRefresh(num)
            return rows
            del(num)
        else:
            tab_A = mc.scrollLayout(scr_A, q=True, ca=True)
            tabs = tab_A[0]

            rows = mc.rowColumnLayout(tabName, numberOfColumns=3, p=tabs)
            mc.tabLayout(tabs, e=True, st=tabName)
            # createSubCat()
            return rows
            del(num)

    elif num == 1:
        scr_A = mc.rowColumnLayout(mainTab, q=True, ca=True)
        tab_A = mc.scrollLayout(scr_A[0], q=True, ca=True)
        row_A = mc.tabLayout(tab_A, q=True, st=True)
        row = '{}|tablayouts|{}|{}|{}|{}'.format(scr, mainTab, scr_A[0], tab_A[0], row_A)
        scr_B = mc.rowColumnLayout(row, q=True, ca=True)
        if scr_B != None:  # noqa
            tab_B = mc.scrollLayout(scr_B[0], q=True, ca=True)
            row_B = mc.tabLayout(tab_B, q=True, st=True)
            rowTab = '{}|{}|{}'.format(row, scr_B[0], tab_B[0])
            tabs = rowTab
        elif scr_B == None:  # noqa
            tabs = scr
        rows = mc.rowColumnLayout(tabName, numberOfColumns=3, p=tabs)
        mc.tabLayout(tabs, e=True, st=tabName)
        # createSubCat()
        return rows
        del(num)

    elif num == 2:
        scr_A = mc.rowColumnLayout(mainTab, q=True, ca=True)
        tab_A = mc.scrollLayout(scr_A[0], q=True, ca=True)
        row_A = mc.tabLayout(tab_A, q=True, st=True)
        scr = mc.rowColumnLayout(row_A, q=True, p=True)
        row = '{}|{}'.format(scr, row_A)
        scr_B = mc.rowColumnLayout(row, q=True, ca=True)
        tab_B = mc.scrollLayout(scr_B[0], q=True, ca=True)
        row_B = mc.tabLayout(tab_B, q=True, st=True)  # noqa
        row_gp = '{}|{}|{}'.format(row, scr_B[0], tab_B[0])  # noqa
        tab_gp = mc.tabLayout(row_gp, q=True, st=True)
        tab_sum = '{}|{}|{}|{}'.format(row, scr_B[0], tab_B[0], tab_gp)
        scr_C = mc.rowColumnLayout(tab_sum, q=True, ca=True)
        tab_C = mc.scrollLayout(scr_C, q=True, ca=True)
        rowTab = '{}|{}|{}'.format(tab_sum, scr_C[0], tab_C[0])
        tabs = rowTab
        rows = mc.rowColumnLayout(tabName, numberOfColumns=3, p=tabs)
        mc.tabLayout(tabs, e=True, st=tabName)
        # createSubCat()
        return rows
        del(num)
