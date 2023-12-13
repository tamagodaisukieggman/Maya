# -*- coding: utf-8 -*-
import maya.cmds as cm
import os
from functools import partial

clipAttr = ".clipid"
teNodeType = "timeEditorClip"
transformNodeType ="transform"
windowName = u"らくらくTimeEditor"
clipPanel = "clipPanel"
transKeepFlag = "transKeepFlag"


#全てのクリップを0f開始に統一
def clipZeroStart(oClipidList) :
    for id in oClipidList :
        stTime = cm.timeEditorClip(id,q=True,s=True)
        cm.timeEditorClip(e=True,moveClip=stTime * -1,clipId=id)


#クリップを選択順に並べる
def clipSort(oClipidList) :
    cnt = 0
    dur = 0
    duration = 0
    for selClipId in oClipidList :
        if cnt == 0 :
            dur = cm.timeEditorClip(selClipId,q=True,duration=True)
            duration += dur
            cnt += 1
        else :
            dur = cm.timeEditorClip(selClipId,q=True,duration=True)
            # moveClip
            cm.timeEditorClip(e=True,moveClip=duration,clipId=[selClipId])
            duration += dur
            cnt += 1


#選択したクリップから選択順に並べる
def clipSortSelClip(oClipidList) :
    cnt = 0
    dur = 0
    duration = 0
    for selClipId in oClipidList :
        if cnt == 0 :
            dur = cm.timeEditorClip(selClipId,q=True,endTime=True)
            duration += dur
            cnt += 1
        else :
            #1個前のクリップの終了時間が必要
            edTime = cm.timeEditorClip(oClipidList[cnt-1],q=True,endTime=True)
            curStTime = cm.timeEditorClip(selClipId,q=True,startTime=True)
            dur = cm.timeEditorClip(selClipId,q=True,duration=True)
            # moveClip
            cm.timeEditorClip(e=True,moveClip=(curStTime-edTime)*-1,clipId=[selClipId])
            duration += dur
            cnt += 1


#クリップのマッチング
def matchClip(oClipidList,oMatchObj) :
    cnt = 0
    for selClipId in oClipidList :
        if cnt == 0 :
            cnt += 1
        else :
            #1個前のクリップの終了時間が必要
            edTime = cm.timeEditorClip(oClipidList[cnt-1],q=True,endTime=True)
            curStTime = cm.timeEditorClip(selClipId,q=True,startTime=True)
            # match
            cm.timeEditorClipOffset( clipId=selClipId, matchClipId=oClipidList[cnt-1], matchObj=oMatchObj, matchSrcTime=curStTime, matchDstTime=curStTime, matchTransOp=0, matchRotOp=1, applyToAllRoots=1 )
            cnt += 1


#マッチ用のオブジェクトとクリップを振り分ける
def objSort(oObjList) :
    teList=[]
    mObj = ""
    for obj in oObjList :
        if cm.nodeType(obj) == teNodeType :
            teList.append(obj)
        elif cm.nodeType(obj) == transformNodeType :
            mObj = obj
    return teList,mObj


#クリップのIDを返す
def clipIdList(oClipList) :
    idList = []
    for ids in oClipList :
        i = cm.getAttr(ids+clipAttr)
        idList.append(i)
    return idList


#メイン関数
def execute(oTransKeepFlag,oStFlagGrp,*args) :

    procNumber = cm.radioButtonGrp(oStFlagGrp,q=True,sl=True)

    #処理するために選択項目を加工
    objectList = cm.ls(sl=True)
    sortItems = objSort(objectList)
    sortIds = sortItems[0]
    matchObj = sortItems[1]
    idsList = clipIdList(sortIds)

    #全て0Fに合わせる
    if procNumber == 1 :
        clipZeroStart(idsList)

    #0Fから揃えなおす
    elif procNumber == 2 :
        clipZeroStart(idsList)
        clipSort(idsList)

    #選択クリップ基準
    elif procNumber == 3 :
        clipSortSelClip(idsList)

    #何も選択していない
    else :
        cm.confirmDialog( title=u'エラー', message=u"オプションが正しく選択されていません。", button=['OK'], defaultButton='Yes' )

    #移動値を保持（マッチ処理）
    if cm.checkBox(oTransKeepFlag,q=True,value=True) and cm.checkBox(oTransKeepFlag,q=True,enable=False) :
        matchClip(idsList,matchObj)


# checkBox Mask
def tkfOn(transKeepFlag,*args) :
    cm.checkBox(transKeepFlag,e=True,enable=True)
def tkfOff(transKeepFlag,*args) :
    cm.checkBox(transKeepFlag,e=True,enable=False)

# close UI
def closeUI(*args) :
    cm.deleteUI(windowName, window=True)

# jump URL
def oJumpHelp(file,*args):
    if sys.platform.startswith("darwin"):
        subprocess.call(("open", file))
    elif os.name == "nt":
        os.startfile(file)
    elif os.name == "posix":
        subprocess.call(("xdg-open", file))
    else:
        raise OSError(u"サポートされていないOSです。： '%s'" % os.name)


def createUI() :

    # not Duplicate UI
    if cm.window(windowName, exists=True) :
        cm.deleteUI(windowName, window=True)

    # Create window
    cm.window(windowName)
    cm.menuBarLayout()
    cm.menu(label="Help")
    cm.menuItem(label=u"使い方（コンフルページへ飛びます）",c=partial(oJumpHelp,"https://wisdom.cygames.jp/x/h3xiAw"))
    cm.setParent( '..', menu=True )
    cm.columnLayout(adj=True,rs=1,w=400)
    cm.frameLayout(l=u"-- ClipSorting --")
    cm.setParent( '..' )
    cm.setParent( '..' )
    cm.frameLayout(l=u"■ Options")
    cm.checkBox(transKeepFlag,l=u"移動値を保持 ( マッチ用のオブジェクトを要選択 )")
    stFlagGrp = cm.radioButtonGrp(labelArray3=[u'全て0Fに合わせる', u'0Fから揃えなおす', u'選択クリップ基準'], \
                numberOfRadioButtons=3, onCommand1=partial(tkfOff,transKeepFlag), offCommand1=partial(tkfOn,transKeepFlag))
    cm.setParent( '..' )
    cm.button(l=u"実行",h=80,c=partial(execute,transKeepFlag,stFlagGrp))
    cm.button(l="close",c=partial(closeUI))
    cm.setParent( '..' )
    cm.showWindow()
