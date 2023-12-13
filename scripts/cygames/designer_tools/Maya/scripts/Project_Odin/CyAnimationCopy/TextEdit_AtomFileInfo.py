#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# TextEdit_AtomFileInfo.py
#

import sys
import os
import re
import PySide.QtCore as QtCore
import PySide.QtGui as QtGui


class TextEdit_AtomFileInfo(QtGui.QTextEdit):
    def __init__(self, parent=None):
        super(TextEdit_AtomFileInfo, self).__init__(parent)
        self.parent = parent
        self.setup()

    def setup(self):
        self.setReadOnly(True);

    def setAtomFileInfo(self, filePath):
        f = open(filePath)
        lines = f.readlines()
        f.close()

        atomVersion = ""
        mayaVersion = ""
        mayaSceneFile = ""
        timeUnit = ""
        linearUnit = ""
        angularUnit = ""
        startTime = ""
        endTime = ""
        animatedNodeNum = 0
        for i, line in enumerate(lines):
            if line.find('atomVersion') >= 0:
                atomVersion = line.replace(";","").split(" ", 1)[1].rsplit("\n", 1)[0]

            if line.find('mayaVersion') >= 0:
                mayaVersion = line.replace(";","").split(" ", 1)[1].rsplit("\n", 1)[0]

            if line.find('mayaSceneFile') >= 0:
                mayaSceneFile = line.replace(";","").split(" ", 1)[1].rsplit("\n", 1)[0]

            if line.find('timeUnit') >= 0:
                timeUnit = line.replace(";","").split(" ", 1)[1].rsplit("\n", 1)[0]

            if line.find('linearUnit') >= 0:
                linearUnit = line.replace(";","").split(" ", 1)[1].rsplit("\n", 1)[0]

            if line.find('angularUnit') >= 0:
                angularUnit = line.replace(";","").split(" ", 1)[1].rsplit("\n", 1)[0]

            if line.find('startTime') >= 0:
                startTime = line.replace(";","").split(" ", 1)[1].rsplit("\n", 1)[0]

            if line.find('endTime') >= 0:
                endTime = line.replace(";","").split(" ", 1)[1].rsplit("\n", 1)[0]

            if line.find('dagNode {') >= 0:
                try:
                    rootNode
                except:
                    rootNode = lines[i+1].split()[0]
                if lines[i+2].find('anim ') >= 0:
                    animatedNodeNum += 1;

        self.setText(u"Atomファイルバージョン : " + atomVersion + "\n\n" +
                     u"Mayaバージョン : " + mayaVersion + "\n\n" +
                     u"コピー元シーン : \n" + mayaSceneFile + "\n\n" +
                     u"ルートノード : \n" + rootNode + "\n\n" +
                     u"開始フレーム : " + startTime + "\n\n" +
                     u"終了フレーム : " + endTime + "\n\n" +
                     u"アニメーション付ノード数 : " + str(animatedNodeNum))
