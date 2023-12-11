# -*- coding: utf-8 -*-
# -*- linfeed: lf   -*-

#-------------------------------------------------------------------------------------------
#   OdinCharaDataChecker
#-------------------------------------------------------------------------------------------

import maya.cmds as cmds
import maya.mel as mel

import math
import sys

import CyDataCheckerBase
reload(CyDataCheckerBase)

#-------------------------------------------------------------------------------------------
#   UI
#-------------------------------------------------------------------------------------------
def UI():

    CyDataCheckerBase.Initialize(__file__)
    CyDataCheckerBase.UI()
    #print "---ui open---"
    CyDataCheckerBase.g_checkerProcessor = OdinCheckerProcessor()

#-------------------------------------------------------------------------------------------
#   UI
#-------------------------------------------------------------------------------------------
def BatchCheck(targetFolderPath, filterString, logFilePath):

    CyDataCheckerBase.Initialize(__file__)

    CyDataCheckerBase.g_checkerProcessor = OdinCheckerProcessor()
    
    CyDataCheckerBase.BatchCheck(targetFolderPath, filterString, logFilePath)

class OdinCheckerProcessor(CyDataCheckerBase.CheckerProcessor):

    #===========================================
    # 初期化
    #===========================================
    def __init__(self):

        CyDataCheckerBase.CheckerProcessor.__init__(self)

        self.currentSelect = []
        self.targetList = []
        self.targetTransFullList = []

        self.targetTransList = ["root","waist","spine_1","spine_2","neck","head","F_hair",
        "L_shoulder","L_upperarm","L_forearm","L_hand","L_finger","L_weapon_1","L_weapon_2",
        "R_shoulder","R_upperarm","R_forearm","R_hand","R_finger","R_weapon_1","R_weapon_2",
        "L_thigh","L_shin","L_foot",
        "R_thigh","R_shin","R_foot",]

        self.pc01PosList = [[0,89.333,5.356],[0,0,0],[0,14.145,-0.582],[0,14.09,-2.073],[0,10.231,-1.584],[0,6.505,0],[0.132,23.5,2.997],
        [ 5.914,7.513,-2.002],[ 7.443,-2.355,0],[ 24.357,0,-1.232],[ 22.381,0,1.232],[ 9.904,5.175,0],[ 10.418,-1.186,0],[0.0,0.0,0.0],
        [-5.914,7.513,-2.002],[-7.443,-2.355,0],[-24.357,0,-1.232],[-22.381,0,1.232],[-9.905,5.175,0],[-10.418,-1.186,0],[0.0,0.0,0.0],
        [ 10,-16.98,-0.472],[0,-29.718,-2.286],[0,-32.978,-5.076],
        [-10,-16.98,-0.472],[0,-29.718,-2.286],[0,-32.978,-5.076],
        ]   # 男性

        self.pc02PosList = [[0,84.497,6.226],[0,0,0],[0,12.972,0.132],[0,13.299,-1.881],[0,12.286,-3.554],[0,6.451,-0.169],[0.0,21.226,5.21],
        [ 4.919,10.086,-3.687],[ 4.852,-1.360,0],[ 24.654,0,-1.229],[ 20.783,0,0.948],[ 10.210,5.005,0.065],[ 10.960,-1.768,0],[0.0,0.0,0.0],
        [-4.919,10.086,-3.687],[-4.852,-1.360,0],[-24.654,0,-1.229],[-20.783,0,0.948],[-10.210,5.005,0.065],[-10.960,-1.768,0],[0.0,0.0,0.0],
        [ 8.396,-11.442,-0.374],[0,-30.796,-2.779],[0,-32.153,-4.956],
        [-8.396,-11.442,-0.374],[0,-30.796,-2.779],[0,-32.153,-4.956],
        ]   # 女性

        self.pc03PosList = [[0,95.538,7.301],[0,0,0],[0,16.752,-0.813],[0,17.086,-2.219],[0,13.389,-3.102],[0,8.861,0.384],[0.0,25.804,14.256],
        [ 11.913,7.663,-4.286],[ 14.209,-1.526,0],[ 27.787,0,-0.684],[ 24.302,0,0.684],[ 13.5,10.487,0],[ 12.877,-1.156,0],[0.0,0.0,0.0],
        [-11.913,7.663,-4.286],[-14.209,-1.526,0],[-27.787,0,-0.684],[-24.302,0,0.684],[-13.5,10.487,0],[-12.876,-1.156,0],[0.0,0.0,0.0],
        [ 12.854,-21.722,-0.153],[0,-31.57,-1.423],[0,-33.235,-4.831],
        [-12.854,-21.722,-0.153],[0,-31.57,-1.423],[0,-33.235,-4.831],
        ]   # おっさん

        self.pc04PosList = [[0,57.203,2.931],[0,0,0],[0,10.929,-0.135],[0,10.687,-1.535],[0,7.356,-1.717],[0,4.348,0.078],[0.0,18.378,2.435],
        [ 3.965,5.037,-0.792],[ 4.353,-1.936,-1.200],[ 16.329,0,-0.072],[ 15.005,0,1.272],[ 5.618,3.470,0],[ 6.420,-0.918,-0.001],[0.0,0.0,0.0],
        [-3.965,5.037,-0.792],[-4.353,-1.936,-1.200],[-16.329,0,-0.072],[-15.005,0,1.272],[-5.618,3.470,0],[-6.420,-0.918,-0.001],[0.0,0.0,0.0],
        [ 7.701,-11.559,-0.163],[0,-17.691,-1.75],[0,-19.905,-2.553],
        [-7.701,-11.559,-0.163],[0,-17.691,-1.75],[0,-19.905,-2.553],
        ]   # 子供

        self.pc05PosList = [[0,87.439,6.154],[0,0,0],[0,24.851,-0.487],[0,17.086,-1.167],[0,15.399,0.314],[0,13.191,5.291],[0.0,19.234,10.270],
        [ 11.913,6.334,-0.479],[ 12.96,-0.71,-0.054],[ 33.991,0,-1.074],[ 28.153,0,1.08],[ 13.321,5.206,-0.142],[ 12.482,0.277,0],[0.0,0.0,0.0],
        [-11.913,6.334,-0.479],[-12.96,-0.71,-0.054],[-33.991,0,-1.074],[-28.153,0,1.08],[-13.321,5.206,-0.142],[-12.482,0.277,0],[0.0,0.0,0.0],
        [ 11.731,-15.804,0.167],[0,-29.9,-0.677],[0,-29.913,-4.066],
        [-11.731,-15.804,0.167],[0,-29.9,-0.677],[0,-29.913,-4.066],
        ]   # ゴリ

        self.pcPosList = [self.pc01PosList,self.pc02PosList,self.pc03PosList,self.pc04PosList,self.pc05PosList]
        self.pcNameList = [u"男性",u"女性",u"おっさん",u"子供",u"ゴリ"]

        self.errMsg = []

    #===========================================
    # ポストプロセス
    #===========================================
    def OnPostprocess(self):

        self.Initialize()
        self.Check()

    #===========================================
    # チェック
    #===========================================
    def Initialize(self):

        self.logList = []

        self.currentSelect = []
        
        self.targetList = []
        self.targetTransFullList = []

    #===========================================
    # チェック
    #===========================================
    def Check(self):

        doTypeCheck = True

        self.UpdateTargetList()

        boneCheck = self.ExistTargetTransform()
        if boneCheck != True:
            print "---err message---"
            print "Missing Bones"
            #print u"\t対象となるボーン" # バッチモードでエラーになるので日本語なしにさせてください。
            for ngItem in boneCheck:
                print u"\t" + str(ngItem)
            #print u"\tが存在しません"
            mel.eval("ScriptEditor;")
            doTypeCheck = False
            #sys.exit() # ボーンが足りないとそもそもキャラクタータイプの照らし合わせができないので終了。　（exitしちゃうとチェック結果.txtが出なくなる）

        if doTypeCheck == True:
            charaType = self.GetCharaType()

            if charaType == -1:
                #self.logList.append(u"\tPC体型以外キャラか、root, spine_1, L_weapon, L_thighの値が正しくありません")
                self.logList.append(u"\t体型不一致")
                self.SelectCurrent()
                return

            self.logList.append( "\t" + self.pcNameList[charaType] + u"体型のキャラです")

            # 途中で数値のおかしい物が未使ったときのエラー
            if len(self.errMsg) > 0:
                for msgList in self.errMsg:
                    self.logList.append(msgList)
                    self.errMsg = []

            self.SelectCurrent()
            
    #===========================================
    # キャラタイプ取得 (現在選択されているキャラクターのタイプをボーンのテンプレートと照らし合わせてタイプを判定する)
    #===========================================
    def GetCharaType(self):

        curModelPosList = []

        for target in self.targetTransFullList:
            curModelPosList.append(cmds.getAttr(target + ".translate")[0])

        targetPcPosIndex = -1
        for pcTypeIndex in range(0,len(self.pcPosList)): # pcPosList は男性、女性、おっさん、子供、ゴリのボーン位置が入っている
            templatePosList = self.pcPosList[pcTypeIndex]
            allSame = True
            count = -1
            for boneIndex in range(0,len(templatePosList)):
                count+=1
                try:
                    currentPos = curModelPosList[boneIndex]
                except IndexError: # templatePosListを規準にしているのでcurModelPosListの長さが足りないとindex out of bound Exceptionになる
                    currentPos = []
                childPos = templatePosList[boneIndex]

                if self.GetSameValueList(childPos, currentPos, 2) == False:

                    if count > 0:
                        targetPcPosIndex = pcTypeIndex
                        try:
                            jointStr = self.targetTransFullList[boneIndex]
                        except IndexError:
                            jointStr = ""
                        joint = jointStr.split("|")
                        msg = ""
                        msg += "\t" + u"ボーン"
                        msg += "\t\t" + str(joint[-1])
                        msg += "\t\t\t\t\t" + u"位置が正しくありません（正しい位置" + str(childPos) + u"\t\t現在の値" + str(currentPos) +u"）"
                        self.errMsg.append(msg)

                    if count <= 0:
                        allSame = False
                        break

            if allSame == False:
                continue

            targetPcPosIndex = pcTypeIndex

        return targetPcPosIndex

    #===========================================
    # 同じ値を持つリストかどうかチェック
    #===========================================
    def GetSameValueList(self, srcList, dstList, digit):

        if len(srcList) != len(dstList):
            return False

        for cnt in range(0, len(srcList)):

            srcValue = round(srcList[cnt], 3) * pow(10,digit)
            dstValue = round(dstList[cnt], 3) * pow(10,digit)
            #print srcValue ,
            #print dstValue

            differSrcValue = abs(math.fmod(srcValue,1))
            differDstValue = abs(math.fmod(dstValue,1))
            #print round(differSrcValue, 3) ,
            #print round(differDstValue, 3)

            if differSrcValue > 0.001 and differSrcValue < 0.999:
                if srcValue < 0:
                    srcValue = math.ceil(srcValue)
                else:
                    srcValue = math.floor(srcValue)
            else:
                srcValue = round(srcValue)

            if differDstValue > 0 and differDstValue < 1:
                if dstValue < 0:
                    dstValue = math.ceil(dstValue)
                else:
                    dstValue = math.floor(dstValue)
            else:
                dstValue = round(dstValue)

            if srcValue != dstValue:
                return False

        return True

    #===========================================
    # ターゲットリスト更新
    #===========================================
    def UpdateTargetList(self):

        self.currentSelect = []
        self.targetList = []

        self.currentSelect = cmds.ls(sl=True, fl=True, l=True)

        if self.currentSelect == None:
            return

        if len(self.currentSelect) == 0:
            return

        cmds.select(self.currentSelect, hi=True)

        self.targetList = cmds.ls(sl=True, fl=True, l=True, tr=True)

    #===========================================
    # ターゲットリスト更新
    #===========================================
    def SelectCurrent(self):

        if self.currentSelect == None:
            return

        if len(self.currentSelect) == 0:
            return

        cmds.select(self.currentSelect, r=True)

    #===========================================
    # ターゲットトランスフォームが全て存在しているかどうか
    #===========================================
    def ExistTargetTransform(self):
        self.targetTransFullList = []
        notFounds = []
        for targetTrans in self.targetTransList:

            targetObject = self.GetObject(targetTrans, self.targetList)
            if targetObject == "":
                notFounds.append(targetTrans)
            else:
                self.targetTransFullList.append(targetObject)
        if len(notFounds) > 0:
            return notFounds
        else:
            return True

    #===========================================
    # オブジェクトの存在確認
    #===========================================
    def GetObject(self, objectName, targetList):

        for target in targetList:

            thisShortName = self.GetShortName(target)

            if thisShortName == objectName:
                return target

        return ""

    #===========================================
    # オブジェクト名を取得
    #===========================================
    def GetShortName(self, longName):

        splitString = longName.split("|")

        if len(splitString) == 0:
            return longName

        return splitString[len(splitString) - 1]
