# -*- coding: utf-8 -*-
# -*- linfeed: lf   -*-

try:
    # Maya 2022-
    from builtins import str
    from builtins import object
    from importlib import reload
except Exception:
    pass

import tempfile
import platform
import os.path
import sys

import CyCommon.CyXml
from CyCommon.CyXml import CyXml
reload(CyCommon.CyXml)

# -------------------------------------------------------------------------------------------
#   CySettingクラス
# -------------------------------------------------------------------------------------------


class CySetting(object):

    # ===========================================
    # コンストラクタ
    # ===========================================
    def __init__(self, toolName, customPath=""):

        self.toolName = toolName
        self.tempPath = tempfile.gettempdir()
        self.tempPath = self.tempPath.replace("\\", "/")

        if customPath == "":
            if platform.system() == "Windows":
                self.tempPath = self.tempPath.replace("appdata/local/temp", "Documents/maya/scripts")
        else:
            self.tempPath = customPath

        self.filePath = self.tempPath + "/" + self.toolName + "_setting.xml"

    # ===========================================
    # 保存
    # ===========================================
    def Save(self, key, value):

        if self.__CreateFile() is False:
            return

        thisType = type(value)
        thisConvValue = ""
        if sys.version_info.major == 2:
            if thisType == str or thisType == unicode:
                thisConvValue = eval(repr(value))
            else:
                thisConvValue = str(value)
        else:
            # for Maya 2022-
            if thisType == str:
                thisConvValue = eval(repr(value))
            else:
                thisConvValue = str(value)

        doc = CyXml.GetDocument(self.filePath)

        if doc is None:
            return

        rootNode = doc.documentElement

        dataNode = self.__GetDataNode(rootNode, key)

        if dataNode:
            dataNode.setAttribute("Value", thisConvValue)

        else:

            dataNode = doc.createElement("Data")
            dataNode.setAttribute("Value", thisConvValue)
            dataNode.setAttribute("Key", key)

            rootNode.appendChild(dataNode)

        CyXml.SaveDocument(self.filePath, doc)

    # ===========================================
    # 読み込み
    # ===========================================
    def Load(self, key, dataType="string"):

        dataValue = ""

        doc = CyXml.GetDocument(self.filePath)

        if doc:

            rootNode = doc.documentElement
            dataNode = self.__GetDataNode(rootNode, key)
            dataValue = ""

            if dataNode:
                dataValue = CyXml.GetAttrValue("Value", dataNode)

        if dataType == "string" or dataType == "":

            try:
                return eval(repr(dataValue))
            except Exception:
                return ""

        elif dataType == "int":

            try:
                return int(dataValue)
            except Exception:
                return 0

        elif dataType == "float":

            try:
                return float(dataValue)
            except Exception:
                return 0.0

        elif dataType == "bool":

            try:

                if dataValue == 0 or dataValue == "False" or dataValue == "":
                    return False
                else:
                    return True
            except Exception:
                return False

    # ===========================================
    # ファイル作成
    # ===========================================
    def __CreateFile(self):

        if os.path.isdir(self.tempPath) is False:
            return False

        if os.path.isfile(self.filePath) is False:

            CyXml.CreateDocument(self.filePath, "SettingData")

        return True

    # ===========================================
    # ノード取得
    # ===========================================
    def __GetDataNode(self, rootNode, key):

        dataNodeList = CyXml.GetNodeList("", rootNode)

        for node in dataNodeList:

            thisKey = CyXml.GetAttrValue("Key", node)

            if thisKey == key:
                return node

        return None
