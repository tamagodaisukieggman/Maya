# -*- coding: utf-8 -*-
#=========================================================================== # noqa
# Cygames Tools # noqa
# writeJSON.py # noqa
# # noqa
# Copyright 2017, Cygames Inc. # noqa
#=========================================================================== # noqa
import maya.cmds as mc
import os
import os.path
import json
import mtk3d.maya.rig.cyPoseStore.importJSON as iJsn
import mtk3d.maya.rig.cyPoseStore.createThumbnail as thumb

from functools import partial

# JSONファイルに書き込み
def writeJSON(*args):  # noqa
    tabToPath = getTabPath()  # noqa
    basePath = mc.textField('posePathTxt', q=True, text=True)
    posePath = basePath + 'store'
    savePosePath = '{}/{}'.format(posePath, tabToPath)  # noqa
    poseName = mc.textField('poseNameTxt', q=True, text=True)
    PosePathB = savePosePath + '/' + poseName + '/' + poseName
    NamePath = PosePathB + '.json'
    sts = os.path.isdir(savePosePath)
    if sts:
        # コントローラーのキー可能なアトリビュートを取得
        ctrls = mc.ls(sl=True)
        if ctrls:
            thumb.createThumbnail()
            for ctrl in ctrls:
                if mc.attributeQuery('blendPoint1', node=ctrl, ex=True):
                    mc.deleteAttr(ctrl, attribute='blendPoint1')
                else:
                    pass
                if mc.attributeQuery('blendOrient1', node=ctrl, ex=True):
                    mc.deleteAttr(ctrl, attribute='blendOrient1')
                else:
                    pass
                if mc.attributeQuery('blendAim1', node=ctrl, ex=True):
                    mc.deleteAttr(ctrl, attribute='blendAim1')
                else:
                    pass

            # 書き込みデータの作成
            write_dict = {}
            ctrl_dict = {}
            for ctrl in ctrls:
                attrs = mc.listAttr(ctrl, k=True, unlocked=True)
                if not attrs:
                    continue

                attr_dict = {}
                for attr in attrs:
                    if mc.attributeQuery(attr, n=ctrl, ch=True):
                        continue

                    attr_type = mc.attributeQuery(attr, n=ctrl, attributeType=True)
                    attr_value = mc.getAttr('{}.{}'.format(ctrl, attr))
                    attr_dict[attr] = {
                        'type': attr_type,
                        # import処理に合わせてboolの場合はintに変換して書き込む
                        'value': int(attr_value) if attr_type == 'bool' else attr_value
                    }

                if attr_dict:
                    ctrl_dict[ctrl] = {'attrs': attr_dict}

            if ctrl_dict:
                write_dict['objects'] = ctrl_dict

            # jsonの書き込み
            with open(NamePath, 'w') as f:
                json.dump(write_dict, f, indent=4)

            makePose()

        else:
            mc.warning(u'==========<　コントローラが選択されていません。 >==========')
    else:
        pass
        # mc.warning(u'==========<　既に同名ディレクトリが存在しています名前を変更して下さい。 >==========')


# 一つのポーズを作成する
def makePose(*args):
    percent = mc.intField('thumbSiz', q=True, value=True)
    imgSize = 256 * (percent * 0.010)

    tabToPath = getTabPath()
    layoutPathA = getTabGp()
    basePath = mc.textField('posePathTxt', q=True, text=True)
    posePath = basePath + 'store'
    savePosePath = '{}/{}'.format(posePath, tabToPath)  # noqa
    poseCurName = mc.textField('poseNameTxt', q=True, text=True)
    poseImgPath = savePosePath + '/' + poseCurName + '/' + poseCurName + '.png'
    os.path.isdir(posePath)
    pngImg = []
    if os.path.isfile(poseImgPath) == True:  # noqa
        os.path.isfile(poseImgPath)
        pngpath = poseImgPath.replace('/', '_')
        pngImg = poseImgPath.split('/')
        lbl = pngImg[-1].split('.')
        Jpathtmp = poseImgPath.split('.')
        Jpath = Jpathtmp[0] + '.json'
        mc.iconTextButton(pngpath, parent=layoutPathA, width=imgSize, h=imgSize, label=lbl[0], ann=lbl[0], fla=True, style='iconAndTextVertical', sic=True, image1=poseImgPath, c=partial(iJsn.importJSON, Jpath))
        popup = mc.popupMenu(b=0)
        pPathA = savePosePath + '/' + poseCurName
        expPath = pPathA.replace(r'/', r'\\')
        expPath2 = r''.join(expPath)
        pngpath2 = pngpath.replace('.', '_')
        mc.menuItem(p=popup, l=u'ポーズ名をコピーする', c='cmds.textField("poseNameTxt", e=True, text="{}")'.format(lbl[0]))
        mc.menuItem(p=popup, l=u'ポーズを置き換える', c="""import shutil;shutil.rmtree("{}");cmds.evalDeferred('cmds.deleteUI("{}")');cmds.textField("poseNameTxt", e=True, text="{}");import mtk3d.maya.rig.cyPoseStore.writeJSON as wJsn;wJsn.makeButton()""".format(pPathA, pngpath2, lbl[0]))
        mc.menuItem(p=popup, l=u'エクスプローラーで開く', c='import subprocess;subprocess.Popen("explorer {}")'.format(expPath2))
        mc.menuItem(p=popup, l=u'削除', c="""import shutil;shutil.rmtree("{}");cmds.evalDeferred('cmds.deleteUI("{}")')""".format(pPathA, pngpath2))
    else:
        mc.warning(u'==========<同名のポーズがストアーに存在しています。別名でストアーして下さい。>==========')
        mc.textField('messagesTxt', e=True, text=u'==========<同名のポーズがストアーに存在しています。別名でストアーして下さい。>==========')


def makeButton(*args):  # noqa
    tabToPath = getTabPath()
    splPath = tabToPath.split('/')
    joinPath = ''.join(splPath)
    if splPath[0] == joinPath:
        mc.warning(u'<2段目のタブを追加してください。>')
    else:
        basePath = mc.textField('posePathTxt', q=True, text=True)
        posePath = basePath + 'store'
        savePosePath = '{}/{}'.format(posePath, tabToPath)  # noqa
        poseName = mc.textField('poseNameTxt', q=True, text=True)
        PosePathB = savePosePath + '/' + poseName
        curPosePath = PosePathB + '/' + poseName + '.json'
        stsA = os.path.isdir(posePath)
        if stsA != True:  # noqa
            mc.warning(u'==========< storeが存在しません。storeを作成して下さい。 >==========')
        else:
            stsB = os.path.isfile(curPosePath)
            if stsB != True:  # noqa
                writeJSON()
            else:
                mc.warning(u'<同名のポーズがストアーに存在しています。別名でストアーして下さい。>')
                mc.textField('messagesTxt', e=True, text=u'<同名のポーズがストアーに存在しています。別名でストアーして下さい。>')


def getTabGp():  # noqa
    layoutPath = mc.tabLayout('tablayouts', q=True, st=True)
    layoutRootPath = mc.tabLayout('tablayouts', q=True, p=True)
    scrA = layoutRootPath.split('|')
    tab_root = layoutPath
    loop = 0
    path = []
    while loop < 5:
        layoutPath = mc.rowColumnLayout(layoutPath, q=True, ca=True)

        if layoutPath == None:  # noqa
            pass
        else:  # noqa
            sts = 1 == layoutPath[0].count(':_')

        if layoutPath == None:  # noqa
            break
        elif layoutPath[0] == scrA[-1]:  # noqa
            path.append(layoutPath)
        elif layoutPath[0] != scrA[-1]:  # noqa
            path.append(layoutPath[0])

        if layoutPath != None and sts == False:  # noqa
            layoutPath = mc.scrollLayout(layoutPath[0], q=True, ca=True)
            path.append(layoutPath[0])
            layoutPath = mc.tabLayout(layoutPath, q=True, st=True)
            path.append(layoutPath)
        elif layoutPath == None or sts == True:  # noqa
            break

        loop += 1

    if sts == True:  # noqa
        path_A = '|'.join(path[0:-1])
    elif sts == False:  # noqa
        path_A = '|'.join(path)
    tabToPath = '{}|tablayouts|{}|{}'.format(layoutRootPath, tab_root, path_A)
    return tabToPath  # noqa


def getTabPath():  # noqa
    row = mc.tabLayout('tablayouts', q=True, st=True)

    tab_root = row

    loop = 0
    path = []

    while loop < 5:
        scr = mc.rowColumnLayout(row, q=True, ca=True)
        if scr == None:  # noqa
            pass
        else:  # noqa
            sts = 1 == scr[0].count(':_')
        if scr != None and sts == False:  # noqa
            tab = mc.scrollLayout(scr[0], q=True, ca=True)
            row = mc.tabLayout(tab, q=True, st=True)
            path.append(row)
        elif scr == None or sts == True:  # noqa
            break
        loop += 1

    path_A = '/'.join(path)
    tabToPath = '{}/{}'.format(tab_root, path_A)
    return tabToPath
