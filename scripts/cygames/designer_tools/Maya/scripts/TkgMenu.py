# -*- coding: utf-8 -*-
# -*- linfeed: lf   -*-

# -------------------------------------------------------------------------------------------
#   TkgMenu
# -------------------------------------------------------------------------------------------
from __future__ import absolute_import

import os

import maya.cmds as cmds
import maya.mel as mel
from xml.dom import minidom
import webbrowser

import TkgCommon.TkgXml
import TkgMenuUpdateWindow
from TkgCommon.TkgXml import TkgXml

try:
    from importlib import reload
except Exception:
    pass

reload(TkgCommon.TkgXml)
reload(TkgMenuUpdateWindow)

toolName = "TkgMenu"
uiPrefix = toolName + "UI"

# -------------------------------------------------------------------------------------------
#   メインUI
# -------------------------------------------------------------------------------------------


def UI():

    menuList = MakeMenuList()

    if len(menuList) == 0:
        return

    mayaWinName = mel.eval("$temp=$gMainWindow")

    menuName = uiPrefix

    # ウィンドウのチェック
    if (mayaWinName == ""):
        return

    if (cmds.menu(menuName, q=True, ex=True) is True):
        cmds.deleteUI(menuName)

    # メニュー構築
    cmds.setParent(mayaWinName)
    cmds.menu(menuName, p=mayaWinName, l="TKG Tools")

    for menu in menuList:

        menu.CreateMenu()

    cmds.menuItem(d=True)

    cmds.menuItem(l=u"TKG Tools 更新ツールを開く", c=OpenUpdateWindow)
    cmds.menuItem(l="About", c=ShowVersion)
    cmds.menuItem(l=u'TKG Tools Wiki',c=OpenTKGToolsWiki)
    cmds.setParent("..", m=True)


def OpenUpdateWindow(*args):

    TkgMenuUpdateWindow.TkgMenuUpdateWindow().show_ui()

# -------------------------------------------------------------------------------------------
#   バージョン情報表示
# -------------------------------------------------------------------------------------------


def ShowVersion(*args):
    cmds.confirmDialog(t="TKG Maya Tools", m="TKG Maya Tools\n\n(C) TKG, ", b="OK", db="OK", ma="center")

# -------------------------------------------------------------------------------------------
#   Wikiを開く
# -------------------------------------------------------------------------------------------


def OpenTKGToolsWiki(temp):
    webbrowser.open(
        "https://wisdom.tkgpublic.jp/pages/viewpage.action?pageId=25927354", new=2, autoraise=True)

# -------------------------------------------------------------------------------------------
#   コマンド起動関数
# -------------------------------------------------------------------------------------------


def CommandToShelf(typ, command, shelfName):

    isMel = 0

    if typ == "Mel":
        isMel = 1

    mel.eval("scriptToShelf (\"" + shelfName + "\",\"" + command + "\"," + str(isMel) + ")")


# -------------------------------------------------------------------------------------------
#   コマンド起動関数
# -------------------------------------------------------------------------------------------
def GetBootCommand(typ, command):
    import sys
    bootCommandStr = ""

    if typ == "Mel":
        bootCommandStr = "mel.eval(\"%s\")" % command

    elif typ == "Python":
        if sys.version_info.major < 3:
            bootCommandStr = command
        else:
            # Python3からはreloadがimportlibモジュールに移動した
            commands = command.split(";")
            for com in commands:
                if com.strip().startswith("reload"):
                    bootCommandStr += "import importlib;importlib." + com.strip() + ";"
                else:
                    bootCommandStr += com.strip() + ";"
            # 最後の余分な;を削除
            bootCommandStr = bootCommandStr[0:-1]

    return bootCommandStr

# -------------------------------------------------------------------------------------------
#   メニューとアイテムのリストを作成
# -------------------------------------------------------------------------------------------


def MakeMenuList():

    result = []

    xmlPath = os.path.abspath(os.path.dirname(__file__)) + "/TkgMenu.xml"

    if os.path.exists(xmlPath) is False:
        return result

    doc = minidom.parse(xmlPath)

    rootNode = doc.getElementsByTagName("TkgMenu")[0]

    menuNodeList = TkgXml.GetNodeList("MenuList", rootNode)

    for menuNode in menuNodeList:

        newMenu = Menu()
        newMenu.ReadXmlNode(menuNode)
        result.append(newMenu)

    return result


# -------------------------------------------------------------------------------------------
#   メニュークラス
# -------------------------------------------------------------------------------------------
class Menu(object):

    def __init__(self):

        self.name = ""
        self.subMenu = True
        self.divide = False
        self.shelfName = ""
        self.commandType = ""
        self.command = ""
        self.image = ""
        self.optionBox = False
        self.menuItemList = []

    def ReadXmlNode(self, node):

        self.name = TkgXml.GetAttrValue("name", node)
        self.image = TkgXml.GetAttrValue("image", node)
        if TkgXml.GetAttrValue("optionBox", node) == "True":
            self.optionBox = True

        if node.nodeName == "Separator":
            self.name = ""
            self.divide = True

        menuItemNodeList = TkgXml.GetNodeList("", node)

        for menuItemNode in menuItemNodeList:

            # nodeNameがMenuであれば下層にドロップダウンメニューを作成する
            if menuItemNode.nodeName == 'Menu':
                newMenu = Menu()
                newMenu.ReadXmlNode(menuItemNode)
                self.menuItemList.append(newMenu)
                continue

            newMenuItem = MenuItem()
            newMenuItem.ReadXmlNode(menuItemNode)
            self.menuItemList.append(newMenuItem)

    def CreateMenu(self):

        command = GetBootCommand(str(self.commandType), str(self.command))

        cmds.menuItem(l=self.name, d=self.divide, subMenu=self.subMenu, tearOff=True, c=command, i=self.image, ob=self.optionBox)

        # メニュー構築
        for item in self.menuItemList:

            item.CreateMenu()

        cmds.setParent("..", m=True)

# -------------------------------------------------------------------------------------------
#   メニューアイテムクラス
# -------------------------------------------------------------------------------------------


class MenuItem(object):

    def __init__(self):

        self.name = ""
        self.divide = False
        self.shelfName = ""
        self.commandType = ""
        self.command = ""
        self.image = ""
        self.optionBox = False

    def ReadXmlNode(self, node):

        self.name = TkgXml.GetAttrValue("name", node)

        if node.nodeName == "Separator":
            self.name = ""
            self.divide = True

        self.shelfName = TkgXml.GetAttrValue("shelfName", node)
        self.commandType = TkgXml.GetAttrValue("type", node)
        self.command = TkgXml.GetAttrValue("command", node).replace("%", "~percent~")
        self.image = TkgXml.GetAttrValue("image", node)
        if TkgXml.GetAttrValue("optionBox", node) == "True":
            self.optionBox = True

    def CreateMenu(self):

        command = GetBootCommand(str(self.commandType), str(self.command))

        cmds.menuItem(l=self.name, d=self.divide, c=command, i=self.image, iol=self.shelfName, ob=self.optionBox, enable=True if self.command else False)
