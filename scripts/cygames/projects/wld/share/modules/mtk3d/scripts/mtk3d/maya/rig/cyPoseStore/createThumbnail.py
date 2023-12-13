# -*- coding: utf-8 -*-
#=========================================================================== # noqa
# Cygames Tools # noqa
# createThumbnail.py # noqa
# # noqa
# Copyright 2017, Cygames Inc. # noqa
#=========================================================================== # noqa
import maya.cmds as mc
import os
import re
import os.path
import maya.OpenMaya as OpenMaya
import maya.OpenMayaUI as OpenMayaUI
import maya.mel as mm


def parse_active_panel():
    panel = mc.getPanel(withFocus=True)
    if not panel or "modelPanel" not in panel:
        raise RuntimeError("No active model panel found")
    return panel


def grabViewport(directory, imageName, ext="png"):
    activePanel = parse_active_panel()
    mc.setFocus(activePanel)
    viewport = OpenMayaUI.M3dView.active3dView()
    viewport.refresh()
    img = OpenMaya.MImage()
    img.create(512, 512)
    viewport.readColorBuffer(img, True)
    filePath = os.path.join(directory, imageName + "." + ext)
    img = img.writeToFile(filePath, ext)

# サムネイル作成関数


def createThumbnail(*args):
    basePath = mc.textField('posePathTxt', q=True, text=True)
    posePath = basePath + 'store'
    stsA = os.path.isdir(posePath)  # storeがあるかないか
    if stsA != True:  # noqa
        mc.warning(u'==========<storeが存在してません。storeを作成して下さい。>==========')
    else:
        poseName = mc.textField('poseNameTxt', q=True, text=True)
        tabToPath = getTabPath()
        basePath = mc.textField('posePathTxt', q=True, text=True)
        posePath = basePath + 'store'
        savePosePath = '{}/{}'.format(posePath, tabToPath)
        poseCurName = mc.textField('poseNameTxt', q=True, text=True)
        NamePath = savePosePath + '/' + poseCurName + '/'
        sts = os.path.isdir(NamePath)
        if sts == True:  # noqa
            mc.warning('already exists')
        else:
            os.makedirs(NamePath)
            thumbDir = (NamePath + '/')
            ext = 'png'
            renameImg = (thumbDir + poseName + ext)
            if mc.window('shotWin', ex=True):
                mc.setFocus('shotWin')
                grabViewport(thumbDir, poseName, ext="png")
                # mc.deleteUI('poseUI')
            else:
                shotWin = modelPanelShot()
                grabViewport(thumbDir, poseName, ext="png")
                mc.deleteUI(shotWin)


# プレビュー表示関数
def preView(*args):
    # サムネイルパスで全てのpng取得してそうあたり
    imgOutPath = mc.textField('savePathTxt', q=True, text=True)
    dir = mc.textScrollList('curDirs', q=True, si=True)
    scnName = mc.textScrollList('localSceneList', query=True, si=True)
    path = imgOutPath + '/' + dir[0] + '/' + 'thumbs'
    sts = os.path.isdir(path)
    img = []
    if sts == True:  # noqa
        files = mc.getFileList(fld=path, fs='*.png')
        n = len(files)
        for a in range(0, n, 1):
            fileN = files[a].split('.png')
            if fileN[0] == scnName[0]:
                img.append(files[a])
            else:
                pass
        if len(img) != 0:
            mc.image('previewIMG', e=True, image=(path + '/' + img[0]), visible=True)
        else:
            mc.image('previewIMG', e=True, visible=False)
    else:
        print 'no image exists'  # noqa


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


def modelPanelShot(*args):
    wintitle = 'ThumbnailShot'
    if mc.window(wintitle, q=True, exists=True):
        mc.deleteUI(wintitle)
    win = mc.window(wintitle, s=False, w=500, h=500)
    dupCam = mc.duplicate('persp', n='dupPerspShotCam')
    mc.paneLayout(w=504, h=524)
    if mc.window('Thumbnail', q=True, exists=True):
        listPanel = []
        for panelName in mc.getPanel(type="modelPanel"):
            if mc.modelPanel(panelName, query=True, camera=True) == "dupPerspThumbnailCam":
                listPanel.append(panelName)
        sp = listPanel[0]
        mc.setFocus(sp)
        mc.delete(dupCam)
    else:
        sp = mc.modelPanel(mbv=False, p=win)
        mc.setFocus(sp)
        mm.eval('lookThroughModelPanel {} {};'.format(dupCam[0], sp))
        mc.modelEditor(sp, e=True, manipulators=False, sel=False, hud=False)
        mm.eval('DisplayShadedAndTextured;')
        mc.inViewMessage(hd=True)
        mc.showWindow()
        mc.scriptJob(uiDeleted=[win, 'mc.delete("{}")'.format(dupCam[0])])
        mc.inViewMessage(hd=False)
    return win
