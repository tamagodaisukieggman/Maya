# -*- coding: utf-8 -*-
# ----------------------------------
# Project : Tsubasa
# Name    : variousCopyPaste
# Author  : toi
# Update  : 2022/6/17
# ----------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import pymel.core as pm
import sys

from dccUserMayaSharePythonLib import common as cm
#from dccUserMayaSharePythonLib import file_dumspl as f
#from dccUserMayaSharePythonLib import ui
from . import vcpUi


try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2 import __version__
    from shiboken2 import wrapInstance
except ImportError:
    from PySide.QtCore import *
    from PySide.QtGui import *
    from PySide import __version__

if sys.hexversion < 0x3000000:
    BYTES = str
    UNICODE = unicode
    BASESTR = basestring
    LONG = long
    py3 = False
else:
    BYTES = bytes
    UNICODE = str
    BASESTR = str
    LONG = int
    py3 = True


class VariousCopyPasteMaya(vcpUi.VariousCopyPasteUi):
    def __init__(self, *args, **kwargs):
        if py3:
            super().__init__(*args, **kwargs)
        else:
            super(VariousCopyPasteMaya, self).__init__(*args, **kwargs)

        self.help_path = 'https://wisdom.cygames.jp/x/QwzhCw'
        self.resize(350, 300)

    # -------------------------------------------------------
    # 値
    # -------------------------------------------------------
    def _runCopyValue(self):
        nodes = pm.ls(sl=True)
        if nodes:
            self._clearLog()

            is_selected_mode = self.tab_value.rb_sel_cop.isChecked()

            # Selected
            if is_selected_mode:
                target_nodes = nodes
            # Hierarchy
            else:
                target_nodes = []
                for node in nodes:
                    target_nodes += pm.ls(node, dag=True, tr=True)

            json_path = self.tab_value._getCurrentJsonPath()

            result = cm.whiteJsonTransforms(target_nodes, json_path)
            self.tab_value._saveCopySetting()
            cm.hum('Copied')

            # Log
            log = 'Copy Value : {0} nodes\n'.format(len(result))
            for node, val in result.items():
                log += '-' * 50 + '\n'
                log += node + '\n'
                log += str(val) + '\n'
            self.tx_ed.setText(log)

    def _runPasteValue(self):
        nodes = pm.ls(sl=True)
        if nodes:
            pm.undoInfo(ock=True)
            self._clearLog()

            is_selected_mode = self.tab_value.rb_sel_paste.isChecked()
            match_mode = self.tab_value.rb_name_match.isChecked()
            is_object = self.tab_value.rb_object_paste.isChecked()
            ignore_axis = self.tab_value._getIgnoreAxis()

            #Selected
            if is_selected_mode:
                target_nodes = nodes
            #Hierarchy
            else:
                target_nodes = []
                for node in nodes:
                    target_nodes += pm.ls(node, dag=True, tr=True)

            json_path = self.tab_value._getCurrentJsonPath(is_copy=False)

            space_ = 'object' if is_object else 'world'
            result = cm.readJsonTransform(target_nodes, json_path, match_mode, space_, ignore_axis)
            self.tab_value._savePasteSetting()
            pm.undoInfo(cck=True)
            cm.hum('Pasted')

            #Log
            log = 'Paste Value : {0} nodes\n'.format(len(result))
            for source_node, target_node, error_occur in result:
                log += '-' * 50 + '\n'
                if error_occur:
                    log += 'Error\n'
                log += '{0} >> {1}\n'.format(source_node, target_node)
            self.tx_ed.setText(log)

    # -------------------------------------------------------
    # 名前
    # -------------------------------------------------------
    def _runPasteName(self):
        nodes = pm.ls(sl=True)
        if nodes:
            pm.undoInfo(ock=True)
            self._clearLog()

            is_selected_mode = self.tab_name.rb_sel_paste.isChecked()
            #match_mode = self.tab_name.rb_name_match.isChecked()
            #is_object = self.tab_value.rb_object_paste.isChecked()

            #Selected
            if is_selected_mode:
                target_nodes = nodes
            #Hierarchy
            else:
                target_nodes = []
                for node in nodes:
                    target_nodes += pm.ls(node, dag=True, tr=True)

            json_path = self.tab_name._getCurrentJsonPath(is_copy=False)

            #space_ = 'object' if is_object else 'world'
            result = cm.readJsonName(target_nodes, json_path)#, match_mode, space_)
            self.tab_name._savePasteSetting()
            pm.undoInfo(cck=True)
            cm.hum('Pasted')

            #Log
            log = 'Paste Value : {0} nodes\n'.format(len(result))
            for source_node, target_node, error_occur in result:
                log += '-' * 50 + '\n'
                if error_occur:
                    log += 'Error\n'
                log += '{0} >> {1}\n'.format(source_node, target_node)
            self.tx_ed.setText(log)


def main():
    VariousCopyPasteMaya('VariousCopyPaste').initUi()
