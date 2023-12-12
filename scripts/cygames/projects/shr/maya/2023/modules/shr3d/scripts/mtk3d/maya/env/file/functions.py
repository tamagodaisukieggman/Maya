# -*- coding: cp932 -*-
#===============================================
#
# ファイル 関連
#
# Fujita Yukihiro
#
#===============================================
import os
import datetime
import math
import sys

#===============================================
# 指定したパスにあるディレクトリ名のリストを取得
#
# @param vPath 指定パス
#
# @return vDirs 見つかったディレクトリリスト
#===============================================
def getDirs(vPath, **kwargs):
    """ 指定したパスにあるディレクトリ名のリストを取得 """

    vDirs = []

    for i in os.listdir(vPath):
        # 指定フォルダのフォルダリストを取得
        if os.path.isdir(os.path.join(vPath, i)):

            # リストに追加
            vDirs.append(i)

    return vDirs

#===============================================
# 指定したパスにあるファイル名のリストを取得
#
# @param vPath 指定パス
#
# @keyward ext 拡張子の有無
#
# @return vFiles 見つかったファイルリスト
#===============================================
def getFiles(vPath, **kwargs):
    """ 指定したパスにあるファイル名のリストを取得 """

    # キーワード引数取得・デフォルト指定
    withExtention = kwargs.get("ext", True)

    vFiles = []

    for i in os.listdir(vPath):
        # 指定フォルダのファイル名を取得
        if os.path.isfile(os.path.join(vPath, i)):

            # 拡張子なし指定の場合
            if withExtention == False:
                i = os.path.splitext(i)[0]

            # リストに追加
            vFiles.append(i)

    return vFiles

#===============================================
#
# ファイル タイムスタンプ取得
#
# @param targetFile 対象ファイル
# @return result タイムスタンプ
#
#===============================================
def getTimeStampStr(targetFile):

    # 対象ファイルのタイムスタンプを取得
    mTime_s = datetime.datetime.fromtimestamp(os.stat(targetFile).st_mtime);

    # マイクロ秒を0に（ターゲット側がマイクロ秒を取得できないので）
    # mTime_s = mTime_s.replace(microsecond = 0);

    # 対象ファイルの更新日時
    result = mTime_s.strftime('%Y/%m/%d %H:%M:%S');

    return result

#===============================================
#
# ファイル タイムスタンプ比較
#
# @param sourceFile 比較元ファイル
# @param targetFile 比較先ファイル
# @return result 比較結果
#
#===============================================
def compareTimeStamp(sourceFile, targetFile):

    # ソースファイルのタイムスタンプを取得
    mTime_s = datetime.datetime.fromtimestamp(os.stat(sourceFile).st_mtime);

    # マイクロ秒を0に（ターゲット側がマイクロ秒を取得できないので）
    mTime_s = mTime_s.replace(microsecond = 0);

    #ソースファイルの更新日時
    key = mTime_s.strftime('%Y/%m/%d %H:%M:%S');

    # ターゲットファイルが存在しない場合
    if not os.path.isfile(targetFile):
        result = 'new';

    else:
        # ターゲットファイルのタイムスタンプを取得
        mTime_t = datetime.datetime.fromtimestamp(os.stat(targetFile).st_mtime);

        # マイクロ秒を0に（ターゲット側がマイクロ秒を取得できないので）
        mTime_t = mTime_t.replace(microsecond = 0);

        # ソースファイルが新しい場合
        if mTime_s > mTime_t:
            result = 'update';

        # 同じ場合
        elif mTime_s == mTime_t:
            result = 'equal';

        # ターゲットファイルが新しい場合
        elif mTime_s < mTime_t:
            result = 'old';

    return result, key;


#===============================================
#
# ファイル・フォルダのサイズを整形した文字列で返す
#
# @param    filePath    ファイル・フォルダのフルパス
# @keyward  unit        単位:KB, MB, GB, Opt
# @keyward  pre         小数点桁数
# @keyward  cmm         カンマ区切りの有無
# @return   ファイルサイズ（整形された文字列）
#
#===============================================
def getSizeStr(filePath, **options):

    # パスのファイルかフォルダが存在するか
    isFile = os.path.isfile(filePath)
    isFolder = os.path.isdir(filePath)

    # ファイル・フォルダが存在しなければ終了
    if isFile == isFolder == False:
        sys.stderr.write("File or Folder not found.\n")
        return False

    # デフォルト値
    unit = options.get("unit", "Opt")
    pre = options.get("pre", 3)
    cmm = options.get("cmm", True)

    #
    unitDict = {
        "KB" : 1024.0,
        "MB" : 1024.0 ** 2,
        "GB" : 1024.0 ** 3
    }

    # ファイルサイズを取得
    if isFile:
        fileSize = os.path.getsize(filePath)
    elif isFolder:
        fileSize = getFolderSize(filePath)

    # 単位指定が opt の場合、サイズを判定して単位を決める
    if unit == "Opt":
        if fileSize < 1024:
            unit = "Bytes"
        elif fileSize < 1024 ** 2:
            unit = "KB"
        elif fileSize < 1024 ** 3:
            unit = "MB"
        elif fileSize < 1024 ** 4:
            unit = "GB"

    # 値を単位に合わせる
    if unit in unitDict:
        fileSize = round(fileSize / unitDict[unit], pre)
    else:
        unit = "Bytes"

    # 小数点なし指定なら整数に
    if pre == 0:
        fileSize = int(fileSize)

    # コンマ区切り
    if cmm:
        fileSize = "{:,}".format(fileSize)

    # 文字列を整形して返す
    return "%s %s" % (fileSize, unit)


#===============================================
#
# フォルダのサイズを返す
#
# @param    path        フォルダのフルパス
# @return   サイズ
#
#===============================================
def getFolderSize(path):

    # フォルダのサイズ
    folderSize = 0

    # フォルダが存在しなければ終了
    if os.path.isdir(path) == False:

        return folderSize

    for fileFolderName in os.listdir(path):
        fullPath = os.path.join(path, fileFolderName)

        # ファイルの場合、サイズを合計
        if os.path.isfile(fullPath):
            folderSize += os.path.getsize(fullPath)
        # フォルダの場合、再帰呼び出し
        elif os.path.isdir(fullPath):
            folderSize += getFolderSize(fullPath)

    return folderSize


#===============================================
#
# ファイルサイズ比較
#
# @param sourceFile 比較元ファイル
# @param targetFile 比較先ファイル
# @return result 比較結果
#
#===============================================
def compareSize(sourceFile, targetFile):

    # ソースファイルがなければ終了
    if os.path.isfile(sourceFile) == False:
        sys.stderr.write("File not found.\n")
        return False

    # ターゲットファイルがない場合
    if os.path.isfile(targetFile) == False:
        return "big"

    # 各ファイルのサイズを取得
    size_s = os.path.getsize(sourceFile)
    size_t = os.path.getsize(targetFile)

    result = "equal"

    # ソースファイルが大きい場合
    if size_s > size_t:
        result = 'big'

    # ターゲットファイルが大きい場合
    elif size_s < size_t:
        result = 'small'

    return result;


#===============================================
# 指定したパス以下のサブディレクトリを含むすべてのファイルとディレクトリをフルパス返す
#
# @param path 指定パス
# @keyword    recursion 再帰回数（検索する階層の深さ）
#
# @return  見つかったディレクトリとファイルのフルパスリスト
#===============================================
def getDirsFiles(path, **options):

    # デフォルト値
    recursion  = options.get("recursion", 100)

    # 戻り値
    result = []

    # 指定パスが存在しない、もしくはファイルの場合は終了
    if not os.path.exists(path) or os.path.isfile(path):
        return False

    # 指定パスのディレクトリとファイルのリストを取得
    dirsFiles = os.listdir(path)

    tempDirs = []
    tempFiles = []

    # リストを並べ替え ： ディレクトリ、ファイル の順
    for i in dirsFiles:
        fullPath = os.path.join(path, i)

        if os.path.isdir(fullPath):
            tempDirs.append(i)
        else:
            tempFiles.append(i)

    # リストを名前順（大文字、小文字の区別なし）にソート
    dirsFiles = sorted(tempDirs, key=str.lower) + sorted(tempFiles, key=str.lower)

    # 戻り値リストに要素を追加
    for i in dirsFiles:
        fullPath = os.path.join(path, i)

        result.append(fullPath.replace(os.sep, "/"))

        # ディレクトリだったら関数を再帰呼び出し
        if os.path.isdir(fullPath):

            if recursion != 0:
                result += getDirsFiles(fullPath, recursion = recursion-1)

    return result
