# -*- coding: utf-8 -*-
# -*- linfeed: lf   -*-

import maya.cmds as cmds
import maya.mel as mel
import sys
import string
import random

#-------------------------------------------------------------------------------------------
#   CyUtilityクラス
#-------------------------------------------------------------------------------------------
class CyUtility:

    #===========================================
    # ウィンドウの二重チェック
    #===========================================
    @staticmethod
    def CheckWindow(windowName):

        if cmds.window( windowName, exists=True ):
            cmds.deleteUI(windowName, window=True )
        else:
            if cmds.windowPref( windowName, exists=True ):
                cmds.windowPref( windowName, remove=True )

    #===========================================
    # ツールの情報表示
    #===========================================
    @staticmethod
    def ShowAbout(toolName, version, info):

        message = toolName

        if version != "":
            message += "\n\n" + "Version : "+version

        if info != "":
            message += "\n\n" + info
        
        cmds.confirmDialog(t=toolName,
                           m=message,
                           b="OK",db="OK",ma="center"
                           )

    @staticmethod
    def GetIndex(dataName):

        result = 0

        startIndex = dataName.find("[")
        endIndex = dataName.find("]")

        if startIndex == -1 or endIndex == -1:
            return result

        resultStr = dataName[startIndex+1:endIndex]

        result = int(resultStr)

        return result

    #===========================================
    # ランダム文字列を取得
    #===========================================
    @staticmethod
    def GetRandomString(length):
    
        # Python3対応コード
        if sys.version_info[0] == 3:
            source = string.digits + string.ascii_letters
        else:
            source = string.digits + string.letters


        result = ""
        for i in range(0, length + 1):
            result += random.choice(source)

        return result

    #===========================================
    # ネームスペースを除去
    #===========================================
    @staticmethod
    def RemoveNamespace(name):
        
        if name.find("|") == -1:
            return CyUtility.RemoveNamespaceBase(name)

        splitStrList = name.split("|")
        resultName = ""
        for p in range(0,len(splitStrList)):
        
            fixName = CyUtility.RemoveNamespaceBase(splitStrList[p])

            resultName += fixName

            if p == len(splitStrList) - 1:
                continue

            resultName += "|"

        return resultName

    #===========================================
    # ネームスペースを除去 ベースメソッド
    #===========================================
    @staticmethod
    def RemoveNamespaceBase(name):

        if name.find(":") == -1:
            return name

        splitStr = name.split(":")

        return splitStr[len(splitStr) - 1]

    #===========================================
    # ショートネームを取得
    #===========================================
    @staticmethod
    def GetShortName(name):

        longName = CyUtility.GetLongName(name)

        if longName == "":
            return ""

        if longName.find("|") == -1:
            return longName

        splitStr = longName.split("|")

        return splitStr[len(splitStr) - 1]

    #===========================================
    # ロングネームを取得
    #===========================================
    @staticmethod
    def GetLongName(name):

        longName = cmds.ls(name,l=True)

        if longName == None:
            return ""

        if len(longName) == 0:
            return ""

        return longName[0]

    #===========================================
    # 頂点名からメッシュ名を取得
    #===========================================
    @staticmethod
    def GetMeshNameFromVertex(vertexName):

        if vertexName.find("[") == -1:
            return vertexName

        if vertexName.find("]") == -1:
            return vertexName

        if vertexName.find(".") == -1:
            return vertexName

        meshName=vertexName.split(".")[0]
        
        return meshName

    #===========================================
    # 頂点名から頂点番号取得
    #===========================================
    @staticmethod
    def GetVertexIndex(vertexName):

        if vertexName.find("[") == -1:
            return -1

        if vertexName.find("]") == -1:
            return -1

        startIndex = vertexName.find("[") + 1
        endIndex = vertexName.find("]")

        return int(vertexName[startIndex:endIndex])

    #===========================================
    # 頂点フェース名から頂点フェース番号取得
    #===========================================
    @staticmethod
    def GetVertexFaceIndex(vertexFaceName):

        if vertexFaceName.rfind("[") == -1:
            return -1

        if vertexFaceName.rfind("]") == -1:
            return -1

        startIndex = vertexFaceName.rfind("[") + 1
        endIndex = vertexFaceName.rfind("]")

        return int(vertexFaceName[startIndex:endIndex])

    #===========================================
    # 選択リストを取得 選択した順番のリストを優先して取得
    #===========================================
    @staticmethod
    def GetSelectList():

        cmds.selectPref(tso=True)

        selectList=[]
    
        selectList=cmds.ls(os=True,l=True,fl=True)

        if selectList != None:
            if len(selectList) != 0:
                return selectList

        selectList=cmds.ls(sl=True,l=True,fl=True)

        if selectList == None:
            return []

        if len(selectList) == 0:
            return []

        return selectList

    #===========================================
    # リストコピー
    #===========================================
    @staticmethod
    def CopyList(value):

        result = []

        for p in range(0,len(value)):

            result.append(value[p])

        return result

    #===========================================
    # 値が同じかどうか
    #===========================================
    @staticmethod
    def SameValue(value0,value1):

        accuracy = 100000

        value0 *= accuracy
        value0 = round(value0)

        value1 *= accuracy
        value1 = round(value1)

        if value0 == value1:
            return True

        return False

    #===========================================
    # リストのなかの値が同じかどうか
    #===========================================
    @staticmethod
    def SameValueList(valueList0, valueList1):

        if len(valueList0) != len(valueList1):
            return False

        for p in range(len(valueList0)):

            if CyUtility.SameValue(valueList0[p], valueList1[p]) == False:
                return False

        return True

    #***************************************************************************************************
    #   プログレスバー関連
    #***************************************************************************************************

    #===========================================
    # プログレスバー開始
    #===========================================
    @staticmethod
    def StartProgress(titleName):

        cmds.progressWindow(title=titleName,status="",isInterruptable=True, min=0, max=100 )

    #===========================================
    # プログレスバー更新
    #===========================================
    @staticmethod
    def UpdateProgress(amount,info):

        cmds.progressWindow( edit=True, progress=amount * 100.0, status=info )

        if cmds.progressWindow( query=True, isCancelled=True ) == True:
            return False

        return True

    #===========================================
    # プログレスバー終了
    #===========================================
    @staticmethod
    def EndProgress():

        cmds.progressWindow(endProgress=1)
