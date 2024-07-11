# -*- coding: utf-8 -*-
# -*- linfeed: lf   -*-

#-------------------------------------------------------------------------------------------
#   Author: Hideyo Isayama
#-------------------------------------------------------------------------------------------

import maya.cmds as cmds
import maya.mel as mel
import os.path
import os

scriptPrefix="TkgEasySetting."
uiPrefix="TkgEasySettingUI"

#-------------------------------------------------------------------------------------------
#   UI
#-------------------------------------------------------------------------------------------
def UI():

    global scriptPrefix
    global uiPrefix    

    width=250
    height=1
    formWidth=width-5
    
    windowTitle=scriptPrefix.replace(".","")
    windowName=windowTitle+"Win"
    
    checkDoubleWindow(windowName)

    cmds.window( windowName, title=windowTitle, widthHeight=(width, height),s=1,mnb=True,mxb=False,rtf=True)

    cmds.columnLayout(adjustableColumn=True)
    
    cmds.button( label="Set Project",w=formWidth,command=scriptPrefix+"SetProject()")
    cmds.button( label="Open Directory",w=formWidth,command=scriptPrefix+"OpenCurrentDirectory()")

    cmds.separator( style='in',h=15,w=formWidth)
    
    #cmds.button( label="Reload Textures",w=formWidth,command=scriptPrefix+"ReloadTextures()")
    #cmds.button( label="Quick Reload Textures",w=formWidth,command=scriptPrefix+"QuickReloadTextures()")

    cmds.separator( style='in',h=15,w=formWidth)
    cmds.button( label="About",w=formWidth,command=scriptPrefix+"ShowVersion()")

    cmds.showWindow(windowName)

#-------------------------------------------------------------------------------------------
#   ウィンドウの二重表示チェック(使用しません)
#-------------------------------------------------------------------------------------------
def checkDoubleWindow(windowName):

    if cmds.window( windowName, exists=True ):
        cmds.deleteUI(windowName, window=True )
    else:
        if cmds.windowPref( windowName, exists=True ):
            cmds.windowPref( windowName, remove=True )

#-------------------------------------------------------------------------------------------
#   プロジェクトを開いているファイルのディレクトリにセットする関数
#-------------------------------------------------------------------------------------------
def SetProject():   

    currentFile=cmds.file( q=True, sn=True )

    if currentFile=="":
        return

    dirname=SearchScenesDir(currentFile)

    setPath=""
    if dirname==None:
        setPath=os.path.dirname(currentFile)
    else:
        setPath=os.path.dirname(dirname)

    confirmText="Set Project ?"        
        
    confirm=cmds.confirmDialog( title=confirmText,
                                message=setPath,
                                button=['Yes','No'],
                                defaultButton='Yes',
                                cancelButton='No',
                                dismissString='No'
                                )
    
    if confirm!="Yes":
        return

    mel.eval("setProject \""+setPath+"\"")
    
    if dirname==None:
        
        removeDir=["scenes","assets"]

        for dirName in removeDir:
            path=setPath+"/"+dirName

            if os.path.exists(path):
                
                os.rmdir(path)

#-------------------------------------------------------------------------------------------
#   scenes というフォルダを遡って探す関数
#-------------------------------------------------------------------------------
def SearchScenesDir(currentDir):

    resultDir=None

    dirname=os.path.dirname(currentDir)

    split=dirname.split("/")

    if len(split)<=2:
        return resultDir

    if split[len(split)-1]=="scenes":
        resultDir=dirname
    else:
        resultDir=SearchScenesDir(dirname)

    return resultDir

#-------------------------------------------------------------------------------------------
#   現在のファイルのディレクトリを開く関数
#-------------------------------------------------------------------------------------------
def OpenCurrentDirectory():
    currentFile=cmds.file( q=True, sn=True )

    if currentFile=="":
        return

    currentDirPath=os.path.dirname(currentFile)
    currentDirPath=currentDirPath.replace("/","\\")
    os.system('explorer \"'+currentDirPath+'\"')

#-------------------------------------------------------------------------------------------
#   テクスチャをすべてリロードする関数
#-------------------------------------------------------------------------------------------
def ReloadTextures():

    global scriptPrefix
    global uiPrefix 

    #ファイルリロード処理
    fileList=cmds.ls(typ="file")

    for fileAttr in fileList:
        thisPath=cmds.getAttr(fileAttr+".fileTextureName")

        if os.path.exists(thisPath):
            cmds.setAttr(fileAttr+".fileTextureName",thisPath,typ="string")
    

#-------------------------------------------------------------------------------------------
#   選択が変わるごとにテクスチャをりロードするイベントを追加する関数
#-------------------------------------------------------------------------------------------
def QuickReloadTextures():
    
    #セレクションが変化したときに常にリロードするかどうか
    confirm=cmds.confirmDialog( title="Confirm Dialog",
                                message="Would You Like To Reload Textures When You Change Selection ?",
                                button=['Yes','No'],
                                defaultButton='Yes',
                                cancelButton='No',
                                dismissString='No'
                                )

    if confirm!="Yes":
        return

    windowTitle=scriptPrefix.replace(".","")
    windowName=windowTitle+"Win"

    SelectChangeEvent(windowName)

#-------------------------------------------------------------------------------------------
#   選択イベント
#-------------------------------------------------------------------------------------------
def SelectChangeEvent(windowName):

    global scriptPrefix    
    
    cmds.scriptJob(p=windowName,e=("SelectionChanged",scriptPrefix+"ReloadTextures()"))


#-------------------------------------------------------------------------------------------
#   バージョン情報表示
#-------------------------------------------------------------------------------------------
def ShowVersion():

    global scriptPrefix

    authorName="Hideyo Isayama"
    toolName=scriptPrefix.replace(".","")
    update="2009.8.13"
    
    cmds.confirmDialog(t=toolName,
                       m=toolName+"\n\n"+"Update : "+update+"\n\nAuthor : "+authorName,
                       b="OK",db="OK",ma="center"
                       )
