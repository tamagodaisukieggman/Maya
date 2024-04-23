# !/usr/bin/env python
# -*- coding: utf-8 -*-

import re, os, sys, codecs
try:
    import autopep8
except:
    print("\n    autopep isn't installed on modules.\n    need autopep for format a code.\n    ")

import maya.cmds as cmds, pymel.core as pm, pymel.tools.mel2py as mel2py
from maya import OpenMayaUI

from maya.app.general.mayaMixin import MayaQWidgetBaseMixin, MayaQWidgetDockableMixin

ver = cmds.about(v=True)

if int(ver) >= 2025:
    from PySide6.QtCore import *
    from PySide6.QtGui import *
    from PySide6.QtWidgets import *
    from PySide6 import __version__
    from shiboken6 import wrapInstance
else:
    try:
        from PySide2.QtCore import *
        from PySide2.QtGui import *
        from PySide2.QtWidgets import *
        from PySide2 import __version__
        from shiboken2 import wrapInstance
    except Exception as e:
        from PySide.QtCore import *
        from PySide.QtGui import *
        from PySide import __version__
        from shiboken import wrapInstance

Evacuate = "!#$%&'()|{}*+"
dirCmds = dir(cmds)
# ptr = OpenMayaUI.MQtUtil.mainWindow()
# parent = shiboken.wrapInstance(long(ptr), QWidget)

def SearchChenge(pyCode=[], strCode='', Type=0):
    Code = '%s' % strCode
    pyCode_spl = pyCode.split('\n')
    defCode = []
    if Type is 0:
        return [ s for s in range(len(pyCode_spl)) if pyCode_spl[s].find(Code) >= 0
               ]
    if Type is 1:
        for s in range(len(pyCode_spl)):
            if pyCode_spl[s].find(Code) >= 0:
                defCode.append(pyCode_spl[s])

        return defCode


def mel2pycmd(melCord=''):
    codingSet = '# !/usr/bin/env python\n# -*- coding: utf-8 -*-\n    '
    source = []
    hex_encoded = []
    hex_decoded = []
    for Cord in melCord:
        Cord_encoded = Cord.encode('utf-8')
        if len(Cord_encoded) is 1:
            source.append(Cord)
        else:
            source.append(Cord.encode('utf-8').encode('hex'))
            hex_encoded.append(Cord.encode('utf-8').encode('hex'))
            hex_decoded.append(Cord)

    str_list = source
    melCord_encoded = (',').join(str_list).replace(',,,', '%s' % Evacuate).replace(',', '').replace('%s' % Evacuate, ',')
    pyCmd = mel2py.mel2pyStr(melCord_encoded, pymelNamespace='pm', forceCompatibility=True)
    pyConverted = pyCmd.replace('pymel.all', 'pymel.core')
    if pyConverted.find('pm.pm.') > -1:
        pyConverted = pyConverted.replace('pm.pm.', 'pm.')
    if pyConverted.find('pm.cmds.') > -1:
        pyConverted = pyConverted.replace('pm.cmds.', 'pm.')
    pyConverting = pyConverted
    for cmd in dirCmds:
        if pyConverted.find('pm.%s' % cmd) > -1:
            pyConverting = pyConverting.replace('pm.%s' % cmd, 'cmds.%s' % cmd)

    if pyConverting.find('pm.') is -1:
        pyConverting = pyConverting.replace('import pymel.core as pm', '')
    else:
        pyConverting = pyConverting.replace('import pymel.core as pm', 'import pymel.core as pm\n\n')
    for i in range(len(hex_encoded)):
        pyConverting = pyConverting.replace('%s' % hex_encoded[i], '%s' % hex_decoded[i])

    try:
        pyFixed = '%s\nimport maya.cmds as cmds\n%s' % (
         codingSet, pyConverting)
    except:
        pyFixed = '%s\nimport maya.cmds as cmds\n%s' % (
         codingSet, pyConverting)

    pyFixed = pyFixed.replace('pm.util.defaultlist(str)', '[]')
    hit_num = SearchChenge(pyCode=pyFixed, strCode='def', Type=1)
    for i in range(len(hit_num)):
        try:
            pyCmds = re.search('def (.*)[(]', hit_num[i]).group(1)
            pyFixed = pyFixed.replace('pm.mel.%s' % pyCmds, '%s' % pyCmds)
        except:
            pass

    str_split = pyFixed.split('\n')
    hit_num = SearchChenge(pyCode=pyFixed, strCode='[', Type=0)
    sch_s = '(.*)'
    sch_m = '\\+'
    for i in range(len(hit_num)):
        s = str_split[hit_num[i]]
        str_list = [sch_s]
        count = 0
        try:
            while count < 9999:
                str_list.append(sch_m)
                str_list.append(sch_s)
                maped_list = map(str, str_list)
                str_sch = (',').join(maped_list).replace(',', '')
                try:
                    sched = re.search('\\[%s\\]' % str_sch, s).groups()
                    str_sch_old = str_sch
                except:
                    sched = re.search('\\[%s\\]' % str_sch_old, s)
                    break

                count += 1

            maped_sched = map(str, list(sched.groups()))
            str_sched = (',').join(maped_sched).replace(',', '+')
            str_sched_o = '[%s]' % str_sched
            pyFixed = pyFixed.replace('%s' % str_sched_o, '%s' % str_sched)
        except:
            pass

    try:
        pyFixed = autopep8.fix_code(pyFixed)
    except:
        return pyFixed

    return pyFixed


class SerpensUI_Widget(MayaQWidgetDockableMixin, QWidget):

    def __init__(self):
        super(SerpensUI_Widget, self).__init__()
        self.vbox = QHBoxLayout()
        self.setLayout(self.vbox)
        self.vbox.addWidget(QLabel(text='Input:'))
        self.linetext = QTextEdit()
        self.vbox.addWidget(self.linetext)
        self.linetext.installEventFilter(self)
        self.vbox.addWidget(QLabel(text='Output:'))
        self.textedit = QTextEdit()
        self.vbox.addWidget(self.textedit)

    def eventFilter(self, obj, event, *args):
        self.linetext.autoFormatting()
        if event.type() == QEvent.KeyPress:
            key = event.key()
            mod = event.modifiers()
            if key == Qt.Key_Return:
                pycmd = mel2pycmd(melCord='%s' % self.linetext.toPlainText())
                self.textedit.clear()
                self.textedit.append(pycmd)
        return self.textedit.textCursor()

    def on_press_enter(self):
        self.textedit.append(self.linetext.text())
        self.linetext.clear()


class Serpens_MainWindow(MayaQWidgetDockableMixin, QMainWindow):

    def __init__(self):
        super(Serpens_MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(500, 500, 1000, 500)
        self.setWindowTitle('Serpens Mel2Py ver.α')
        self.setCentralWidget(SerpensUI_Widget())


def Serpens_start():
    # app = QApplication.instance()
    win = Serpens_MainWindow()
    win.show()
    # sys.exit()
    # app.exec_()


if __name__ == '__main__':
    Serpens_start()