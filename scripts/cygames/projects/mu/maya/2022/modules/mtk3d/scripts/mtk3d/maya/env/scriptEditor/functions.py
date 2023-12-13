# -*- coding: cp932 -*-
#===============================================
#
# スクリプト関連
#
# Fujita Yukihiro
#
#===============================================
import maya.cmds as cmds
#import maya.mel as mel
#import pymel.core as pm

#-----------------------------------------------
# カレントタブのプロシージャリストを取得
#-----------------------------------------------
def getProcedures(gLastFocusedCommandControl):
    
    # コード全体を取得
    wholeCode = cmds.cmdScrollFieldExecuter(gLastFocusedCommandControl, q=True, text=True)

    # 各行を取得
    lines = wholeCode.split("\n")
    
    # 行番号
    lineNumber = 1
    
    # コメントブロックフラグ
    isComment = False

    procedureName = "notFound"

    # 見つかったプロシージャリスト
    procedures = []

    # 行ごとの処理
    for line in lines:
        # コメント検索
        commentStartIndex = line.find("//")
        
        # // が見つかったらコメント削除
        if commentStartIndex != -1:
            line = line[:commentStartIndex]

        # 文字列ブロック検索
        stringStartIndex = line.find('"')
        stringEndIndex = line.rfind('"')
        
        # 文字列ブロックがあれば文字列ブロック内を削除
        if stringStartIndex != -1:
            line = line[:stringStartIndex] + line[stringEndIndex+2:]
            
        # コメントブロックの開始を検索
        commentStartIndex = line.find("/*")
        
        # コメントブロックの終了を検索
        commentEndIndex = line.find("*/")
        
        # /* と */ が見つかったら
        if commentStartIndex != -1 and commentEndIndex != -1:

            # /* の後に */ がある場合、コメント部分を削除
            if commentStartIndex < commentEndIndex:
                
                # コメントブロック内じゃないなら
                if not isComment:
                    line = line[:commentStartIndex] + line[commentEndIndex+2:]
                # コメントブロック内なら
                else:
                    line = line[commentEndIndex+2:]
                
                isComment = False
                
                # プロシージャ宣言チェック
                procedureName = checkProcedure(line)
            
            # /* の前に */ がある場合、コメント部分を削除
            else:
                line = line[commentEndIndex+2:commentStartIndex]
                
                # コメントブロック内じゃないならプロシージャ宣言チェック
                if not isComment:
                    procedureName = checkProcedure(line)
                
                isComment = True
                
        # /* のみ見つかった場合、コメント部分を削除
        elif commentStartIndex != -1:
            line = line[:commentStartIndex]

            # コメントブロック内じゃないならプロシージャ宣言チェック
            if not isComment:
                procedureName = checkProcedure(line)

            isComment = True
    
        # */ のみ見つかった場合、コメント部分を削除
        elif commentEndIndex != -1:
            line = line[commentEndIndex+2:]
            
            isComment = False
            
            # プロシージャ宣言チェック
            procedureName = checkProcedure(line)
            
        else:
            # コメントブロック内じゃないならプロシージャ宣言チェック
            if not isComment:
                procedureName = checkProcedure(line)

        if procedureName == "notFound":
            pass
        elif procedureName is None:
            pass
        else:
            if procedureName.find("(") != -1:
                procedureName = procedureName[:procedureName.index("(")]
            
            # プロシージャ名 行番号 の形で
            procedures.append(procedureName + " " + str(lineNumber))
            #procedures.append(lineNumber)
            
        lineNumber = lineNumber + 1

    return procedures
    
#-----------------------------------------------
# プロシージャを検索
#-----------------------------------------------
def checkProcedure(line):

    if len(line) == 0:
        return

    # 行の各単語を取得
    words = line.split()
    
    if len(words) == 0:
        return
    
    # 変数型リスト
    variableTypes = ["int", "int[]", "float", "float[]", "string", "string[]", "vector", "vector[]", "matrix"]
    
    procedureName = "notFound"
    
    if "proc" in words:
        procIndex = words.index("proc")
        
        # 行がプロシージャ宣言のみで終わっていない場合
        if len(words)-1 > procIndex:

            # プロシージャが戻り値を指定している場合
            if words[procIndex + 1] in variableTypes:

                # 行が戻り値の指定で終わっていない場合
                if len(words)-2 > procIndex:
                    procedureName = words[procIndex + 2]

            # プロシージャが戻り値を指定していない場合
            else:
                procedureName = words[procIndex + 1]

    return procedureName

#-----------------------------------------------
# カレントタブの関数リストを取得
#-----------------------------------------------
def getFunctions(gLastFocusedCommandControl):
    
    # コード全体を取得
    wholeCode = cmds.cmdScrollFieldExecuter(gLastFocusedCommandControl, q=True, text=True)

    # 各行を取得
    lines = wholeCode.split("\n")
    
    # 行番号
    lineNumber = 1
    
    functionName = "notFound"

    # 見つかった関数リスト
    functions = []
    

    # 行ごとの処理
    for line in lines:
        # コメント検索
        commentStartIndex = line.find("#")
        
        # // が見つかったらコメント削除
        if commentStartIndex != -1:
            line = line[:commentStartIndex]

        functionName = checkFunction(line)

        if functionName == "notFound":
            pass
        elif functionName is None:
            pass
        else:
            if functionName.find("(") != -1:
                functionName = functionName[:functionName.index("(")]
            
            # プロシージャ名 行番号 の形で
            functions.append(functionName + " " + str(lineNumber))
            #procedures.append(lineNumber)
            
        lineNumber = lineNumber + 1

    return functions
    
#-----------------------------------------------
# 関数を検索
#-----------------------------------------------
def checkFunction(line):

    if len(line) == 0:
        return

    # 行の各単語を取得
    words = line.split()
    
    if len(words) == 0:
        return

    functionName = "notFound"

    if "def" in words:
        defIndex = words.index("def")

        # 行が関数宣言のみで終わっていない場合
        if len(words)-1 > defIndex:

            functionName = words[defIndex + 1]

    return functionName
