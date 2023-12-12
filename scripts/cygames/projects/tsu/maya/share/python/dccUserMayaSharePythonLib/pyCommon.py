# -*- coding: utf-8 -*-
# ----------------------------------
# Project : Tsubasa
# Name    : dccUserMayaSharePythonLib.pyCommon
# Author  : toi
# Version : 0.0.3
# Update  : 2021/12/16
# ----------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import os
import sys
import time
import json
import stat
import inspect
import datetime
import collections
from functools import partial
from collections import OrderedDict


def isContainingAllWordsInString(words, string_):
    """target_String内にwordsの要素がすべて含まれる場合はTrue"""

    result = True
    for w in words:
        if w not in string_:
            result = False
            break
    return result


def make_list(string_or_list):
    """ string_or_listをリスト化する（リストの場合はそのまま）"""

    if not isinstance(string_or_list, list):
        string_or_list = [string_or_list]
    return string_or_list


def get_existsString_inList(stringList, string):
    """指定リスト内で、指定文字列内【に】ふくまれているものを返す"""

    return [x for x in stringList if x in string]


def get_existsString_inStr(stringList, string):
    """指定リスト内で、指定文字列内【が】ふくまれているものを返す"""

    return [x for x in stringList if string in x]


def get_existsList_inStr(string, list_):
    """指定文字内に、指定リスト内の文字【が】ふくまれているかどうかの判定"""

    return [x for x in list_ if x in string]


# リスト-------------------------------------------------
def move_val_list(list_, val, num_to_move):
    """list_の中のvalをnum_to_move番に移動（同じ値がある場合は全部移動）"""

    list_.remove(val)
    list_.insert(num_to_move, val)
    return list_


def valueAddingList(listA, listB):
    """２つのリスト同士の値を加算"""

    resultList = []
    for i in range(len(listA)):
        val = listA[i] + listB[i]
        resultList.append(val)
    return resultList


def valueSubtractionList(listA, listB):
    """２つのリスト同士の値を減算"""

    resultList = []
    for i in range(len(listA)):
        val = listA[i] - listB[i]
        resultList.append(val)
    return resultList


def logicalConjunctionList(listA, listB):
    u"""２つのリストでユニークな値を抜き出す"""

    return list(set(listA + listB))


def matchedList(listA, listB):
    """listA と　listB 共通の要素を返す"""

    listA = set(listA)
    listB = set(listB)
    matchedList = list(listA & listB)
    return matchedList


def negationList(listA, listB):
    """listA にあって　listB に無い要素を返す"""

    listA = set(listA)
    listB = set(listB)
    negationList = list(listA - listB)
    return negationList


def most_count_element(list_):
    """ リストの中から、最大登場の要素を返す"""

    return collections.Counter(list_).most_common()[0][0]


def doubleSort(list_, num=0, reverse=False):
    """二重リストをソート"""

    return sorted(list_, key=lambda x: x[num], reverse=reverse)


def roundList(list_, digits=3):
    """フロートのリストを丸めて返す"""

    newList = []
    for i in list_:
        newList.append(round(i, digits))
    return newList


def getDecimalPoint(float):
    """与えられたフロート値の小数点以下を文字列数字で返す"""

    result = str(float)
    result = result[result.find('.') + 1:]
    return result


def list2String(targetList, add_tab=False):
    """文字列リストを要素ごとに改行した文字列として返す"""

    result = ''
    for l in targetList:
        if add_tab:
            result += '\t' + l + '\n'
        else:
            result += l + '\n'
    return result


def make_list(string_or_list):
    u""" string_or_listをリスト化する（リストの場合はそのまま）"""

    if not isinstance(string_or_list, list):
        string_or_list = [string_or_list]
    return string_or_list


def remove_indent(target_string):
    """文字列リストを連結した文字列として返す"""

    target_string_split = target_string.splitlines()
    result = ''
    for target_string in target_string_split:
        result += target_string
    return result


def remove_false(target_list):
    """値が全て空のリストだったら、空のリストとして返す"""

    return [x for x in target_list if x]


def reduce_list_index(original_list_num, reduce_list_num):
    """original_list_num 分の数を reduce_list_num まで均等に減らしたリストのインデックスを作成する"""

    def main(original_list_num, reduce_list_num):
        original_list_num = int(original_list_num)
        reduce_list_num = int(reduce_list_num)

        # 比率
        deg = round(float(original_list_num) / float(reduce_list_num), 2)
        # 比率の倍数のリストを作成（四捨五入で整数化しておく）
        baisu = [int(round(x * deg)) for x in range(original_list_num)]

        result = []
        for i in range(original_list_num):
            # 前後は必ず入れる
            if 1 == 0 or i == range(original_list_num)[-1]:
                result.append(i)
            # iがbaisuの中にあれば、追加する
            elif i in baisu:
                result.append(i)
        return result

    result = main(original_list_num, reduce_list_num)

    # 数が異なる場合は後ろから２番目を削除（暫定処置）
    if len(result) != reduce_list_num:
        result.pop(-2)

    return result


def divide_intermediate_list(original_num, divide_num):
    """original_numの数をdivide_numで等分した際、各分割パートの中央値（整数）のリストを返す"""

    div_value = float(original_num) / float(divide_num)
    div_value_half = div_value / 2.0

    result = []
    for i in range(divide_num):
        if i == 0:
            base = 0
        else:
            base = i * div_value
        result.append(int(base + div_value_half) + 1)
    return result


def startswith_in_list(string_, list_):
    is_startswith = False
    for l in list_:
        if string_.startswith(l):
            is_startswith = True
            return is_startswith
    else:
        return is_startswith


def startswith_in_stringlist(word, string_list):
    is_startswith = False
    for s in string_list:
        if word.startswith(s):
            is_startswith = True
            return is_startswith
    else:
        return is_startswith


# 辞書-------------------------------------------------
def sortDict(dic):
    """辞書をキー名でソートして並び替える"""

    keyList = []
    for k in dic:
        keyList.append(k)
    sortedList = sorted(keyList)

    sortedDic = collections.OrderedDict()
    for key in sortedList:
        sortedDic[key] = dic[key]
    return sortedDic


def sortDictValueDown(dict_):
    return sorted(dict_.items(), key=lambda x: x[1])


def sortDictValueUp(dict_):
    return sorted(dict_.items(), key=lambda x: -x[1])


def doubleFind(l, numOrKey):
    """二重（辞書）内の指定番号（キー）要素をリスト"""

    return [i[numOrKey] for i in l]


def getKeyFormValDict(dict, val):
    """値からキーを返す　（値も同じものが無いことが前提：最初に同値のキーを返す）"""

    for k, v in dict.items():
        if v == val:
            return k
            break


# その他-------------------------------------------------
def printMethod(obj):
    """ オブジェクトのメソッドをprint"""

    for x in inspect.getmembers(obj, inspect.ismethod):
        print(x[0])


def str2List(listStr):
    """リスト記述の文字列をリストに変換"""

    list_ = listStr.replace("u'", '').replace("'", '')[1:-1].split(',')
    return list(filter(None, list_))


def getDateTimeString():
    """
    現在の日付を文字列で返す
    例）2016_0405_2025
    """
    todaydetail = datetime.datetime.today()
    result = str(todaydetail.year) + '_'
    result += str(todaydetail.month).zfill(2)
    result += str(todaydetail.day).zfill(2) + '_'
    result += str(todaydetail.hour).zfill(2)
    result += str(todaydetail.minute).zfill(2)
    return result


def popString(str, popStr):
    """str 内の一番左側にある popStr を削除する"""

    c = str.find(popStr)
    sList = list(str)
    sList.pop(c)
    result = ''
    for s in sList:
        result += s
    return result


def rPopString(str, popStr):
    """str 内の一番右側にある popStr を削除する"""

    c = str.rfind(popStr)
    sList = list(str)
    sList.pop(c)
    result = ''
    for s in sList:
        result += s
    return result


def removeInt(str):
    result = ''
    for s in str:
        if not s.isdigit():
            result += s
    return result


def get_suf_int(string):
    """
    文字列から末尾の整数を取得する
    :param string:
    :return string:
    """
    try:
        string = string[::-1]
        if not string[-1].isdigit():
            string = string[::-1]
            return get_suf_int(string[1:])
        else:
            return int(string[::-1])
    except:
        return None


def remove_suf_int(string):
    """
    文字列から末尾の整数を削除して返す
    :param string:
    :return string:
    """
    if string[-1].isdigit():
        return remove_suf_int(string[:-1])
    else:
        return string