# -*- coding: utf-8 -*-
# ----------------------------------
# Project : Tsubasa
# Name    : vcpUi
# Author  : toi
# Update  : 2022/6/20
# ビルダー版と共有するファイル
# ----------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import os
import sys
#import stat
#import re
#import datetime
from functools import partial

try:
    from pyfbsdk import *
    fbapp = FBApplication()
    fbsys = FBSystem()
    is_motionbuilder = True
except ImportError:
    is_motionbuilder = False

if not is_motionbuilder:
    #import maya.cmds as cmds
    #import maya.mel as mm
    #import pymel.core as pm
    from dccUserMayaSharePythonLib import file_dumspl as f
    from dccUserMayaSharePythonLib import ui
else:
    import file_dumspl as f
    import ui

#reload(f)
#reload(ui)

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2 import __version__
    if not is_motionbuilder:
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

ICON_FOLDER_PATH = 'D:/cygames/tsubasa/tools/dcc_user/motionbuilder/share/python/dccUserMotionbuilderSharePythonLib/icon'


class TemplateUiInTab(QWidget):
    def __init__(self, obj, tabname, tmp_json):
        super(TemplateUiInTab, self).__init__()

        self.top_layout = QVBoxLayout()
        self.setLayout(self.top_layout)
        self.vcp = obj
        self.tabName = tabname
        self.tmp_json = tmp_json

        SETTING_DIR = os.path.join(
            os.getenv("HOMEDRIVE"), os.getenv("HOMEPATH"),
            'Documents', 'maya', 'Scripting_Files', 'variousCopyPaste', 'data')

        # UIデフォルト値
        self.def_set = {
            'bgrp_target_cop': 0,
            'bgrp_file_cop': 0,
            'l_edit_cop_file': SETTING_DIR,
            'bgrp_target_paste': 0,
            'bgrp_match': 0,
            'bgrp_space': 0,
            'bgrp_file_paste': 0,
            'l_edit_paste_file': SETTING_DIR,
        }

        gb_style = '''
            QFrame{{
                font-weight: bold;
                border-style: solid;
                border-width: 1px;
                border-color: {0};
                border-radius: 10spx;
                padding: 6px;
            }}
        '''

        # =================================================
        # copy
        # =================================================
        gb_copy = QGroupBox('[ Copy ]')
        #gb_copy.setStyleSheet(gb_style.format('maroon'))
        self.top_layout.addWidget(gb_copy)

        vbl_copy = QVBoxLayout(gb_copy)
        vbl_copy.setSpacing(5)

        # ---------------------------------
        # ノード指定方法
        # ---------------------------------
        vb_select = QVBoxLayout()
        hbl = QHBoxLayout()

        self.bgrp_target_cop = ui.ButtonGroup()
        self.rb_sel_cop = QRadioButton('Selected')
        self.rb_hie_cop = QRadioButton('Hierarchy')
        self.rb_sel_cop.setToolTip('選択中のノードのみが対象')
        self.rb_hie_cop.setToolTip('選択中のノード下の階層に含まれるノードが対象')
        self.bgrp_target_cop.addButton(self.rb_sel_cop, 0)
        self.bgrp_target_cop.addButton(self.rb_hie_cop, 1)

        vb_select.addLayout(hbl)
        hbl.addWidget(QLabel('Target Node : '))
        hbl.addWidget(self.rb_sel_cop)
        hbl.addWidget(self.rb_hie_cop)

        # ---------------------------------
        # 対象ファイル
        # ---------------------------------
        vb_target = QVBoxLayout()
        hbl = QHBoxLayout()

        self.bgrp_file_cop = ui.ButtonGroup()
        self.rb_tmp_cop = QRadioButton('Temp')
        self.rb_sp_cop = QRadioButton('Specify')
        self.rb_tmp_cop.setToolTip('デフォルトの一時ファイルを指定します')
        self.rb_sp_cop.setToolTip('過去に保存したデータを指定します')
        self.bgrp_file_cop.addButton(self.rb_tmp_cop, 0)
        self.bgrp_file_cop.addButton(self.rb_sp_cop, 1)
        self.bgrp_file_cop.buttonClicked.connect(self._changeTargetFileCopy)

        vb_target.addLayout(hbl)
        hbl.addWidget(QLabel('Data File : '))
        hbl.addWidget(self.rb_tmp_cop)
        hbl.addWidget(self.rb_sp_cop)

        # ファイルフィールド
        self.hbl_file_field_cop = QHBoxLayout()
        self.l_edit_cop_file = QLineEdit()
        self.bt_browse_cop = self._browseButton(self.l_edit_cop_file)
        self.hbl_file_field_cop.addWidget(self.l_edit_cop_file)
        self.hbl_file_field_cop.addWidget(self.bt_browse_cop)

        # 実行ボタン
        self.bt_copy = QPushButton('Copy')
        self.bt_copy.setStyleSheet('QPushButton{backGround-color: #cc6666;}')

        # addWidget
        vbl_copy.addLayout(vb_select)
        vbl_copy.addWidget(self._separator())
        vbl_copy.addLayout(vb_target)
        vbl_copy.addLayout(self.hbl_file_field_cop)
        vbl_copy.addWidget(self._separator())
        vbl_copy.addWidget(self.bt_copy)

        # =================================================
        # PASTE
        # =================================================
        gb_paste = QGroupBox('[ Paste ]')
        self.top_layout.addWidget(gb_paste)

        vb_paste = QVBoxLayout(gb_paste)
        vb_paste.setSpacing(5)

        # ---------------------------------
        # ノード指定方法
        # ---------------------------------
        vb_select = QVBoxLayout()
        hbl = QHBoxLayout()

        self.bgrp_target_paste = ui.ButtonGroup()
        self.rb_sel_paste = QRadioButton('Selected')
        self.rb_hie_paste = QRadioButton('Hierarchy')
        self.rb_sel_paste.setToolTip('選択中のノードのみが対象')
        self.rb_hie_paste.setToolTip('選択中のノード下の階層に含まれるノードが対象')
        self.bgrp_target_paste.addButton(self.rb_sel_paste, 0)
        self.bgrp_target_paste.addButton(self.rb_hie_paste, 1)

        vb_select.addLayout(hbl)
        hbl.addWidget(QLabel('Target Node : '))
        hbl.addWidget(self.rb_sel_paste)
        hbl.addWidget(self.rb_hie_paste)

        # ---------------------------------
        # 専用オプション
        # ---------------------------------
        self.vb_option_paste = QVBoxLayout()

        # 組み合わせ方法（Match）
        vb_match = QVBoxLayout()

        self.hbl_match = QHBoxLayout()
        self.bgrp_match = ui.ButtonGroup()
        self.rb_order_match = QRadioButton('Order')
        self.rb_name_match = QRadioButton('Name')
        self.rb_order_match.setToolTip('選択順に組み合わせます')
        self.rb_name_match.setToolTip('コピーしたデータの名前と、一致する名前のノード同士を組み合わせます')

        self.bgrp_match.addButton(self.rb_order_match, 0)
        self.bgrp_match.addButton(self.rb_name_match, 1)
        self.hbl_match.addWidget(QLabel('Match Method : '))
        self.hbl_match.addWidget(self.rb_order_match)
        self.hbl_match.addWidget(self.rb_name_match)

        # ローカルグローバル（Space）
        self.hbl_space = QHBoxLayout()

        self.bgrp_space = ui.ButtonGroup()
        self.rb_object_paste = QRadioButton('Object')
        self.rb_world_paste = QRadioButton('World')
        self.rb_object_paste.setToolTip('ローカル値でセットします')
        self.rb_world_paste.setToolTip('ワールド値でセットします')
        self.bgrp_space.addButton(self.rb_object_paste, 0)
        self.bgrp_space.addButton(self.rb_world_paste, 1)

        self.hbl_space.addWidget(QLabel('Space : '))
        self.hbl_space.addWidget(self.rb_object_paste)
        self.hbl_space.addWidget(self.rb_world_paste)

        # axis
        self.hbl_axis = QHBoxLayout()

        hbl_axis_right = QVBoxLayout()
        hbl_axis_t = QHBoxLayout()
        self.cb_tx = QCheckBox('tx')
        self.cb_ty = QCheckBox('ty')
        self.cb_tz = QCheckBox('tz')
        hbl_axis_r = QHBoxLayout()
        self.cb_rx = QCheckBox('rx')
        self.cb_ry = QCheckBox('ry')
        self.cb_rz = QCheckBox('rz')
        hbl_axis_s = QHBoxLayout()
        self.cb_sx = QCheckBox('sx')
        self.cb_sy = QCheckBox('sy')
        self.cb_sz = QCheckBox('sz')

        self.axis_cb_list = [
            self.cb_tx, self.cb_ty, self.cb_tz,
            self.cb_rx, self.cb_ry, self.cb_rz,
            self.cb_sx, self.cb_sy, self.cb_sz]

        hbl_axis_right.addLayout(hbl_axis_t)
        hbl_axis_right.addLayout(hbl_axis_r)
        hbl_axis_right.addLayout(hbl_axis_s)
        hbl_axis_t.addWidget(self.cb_tx)
        hbl_axis_t.addWidget(self.cb_ty)
        hbl_axis_t.addWidget(self.cb_tz)
        hbl_axis_r.addWidget(self.cb_rx)
        hbl_axis_r.addWidget(self.cb_ry)
        hbl_axis_r.addWidget(self.cb_rz)
        hbl_axis_s.addWidget(self.cb_sx)
        hbl_axis_s.addWidget(self.cb_sy)
        hbl_axis_s.addWidget(self.cb_sz)

        self.hbl_axis.addWidget(QLabel('Axis : '), 1)
        self.hbl_axis.addLayout(hbl_axis_right, 2)

        # ---------------------------------
        # 対象ファイル
        # ---------------------------------
        vb_target = QVBoxLayout()
        hbl = QHBoxLayout()

        self.bgrp_file_paste = ui.ButtonGroup()
        self.rb_tmp_paste = QRadioButton('Temp')
        self.rb_sp_paste = QRadioButton('Specify')
        self.rb_tmp_paste.setToolTip('デフォルトの一時ファイルを指定します')
        self.rb_sp_paste.setToolTip('過去に保存したデータを指定します')
        self.bgrp_file_paste.addButton(self.rb_tmp_paste, 0)
        self.bgrp_file_paste.addButton(self.rb_sp_paste, 1)
        self.bgrp_file_paste.buttonClicked.connect(self._changeTargetFilePaste)

        vb_target.addLayout(hbl)
        hbl.addWidget(QLabel('Data File : '))
        hbl.addWidget(self.rb_tmp_paste)
        hbl.addWidget(self.rb_sp_paste)

        # ファイルフィールド
        self.hbl_file_field_paste = QHBoxLayout()
        self.l_edit_paste_file = QLineEdit()
        self.bt_browse_paste = self._browseButton(self.l_edit_paste_file, is_copy=False)
        self.hbl_file_field_paste.addWidget(self.l_edit_paste_file)
        self.hbl_file_field_paste.addWidget(self.bt_browse_paste)

        # 実行ボタン
        self.bt_paste = QPushButton('Paste')
        self.bt_paste.setStyleSheet('QPushButton{backGround-color: #6666cc;}')

        # ---------------------------------
        # ---------------------------------
        # addWidget
        vb_paste.addLayout(vb_select)
        vb_paste.addLayout(vb_match)
        vb_paste.addLayout(self.vb_option_paste)
        vb_paste.addWidget(self._separator())
        vb_paste.addLayout(vb_target)
        vb_paste.addLayout(self.hbl_file_field_paste)
        vb_paste.addWidget(self._separator())
        vb_paste.addWidget(self.bt_paste)

        # オプションはタブごとに追加項目が異なる
        if self.tabName in ['Transform', 'anim']:
            self.vb_option_paste.addLayout(self.hbl_match)
        if self.tabName in ['Transform']:
            self.vb_option_paste.addLayout(self.hbl_space)
            self.vb_option_paste.addLayout(self.hbl_axis)

        self._setAllSettings()

    def _keyname(self, name_):
        return name_ + '_' + self.tabName

    def _resetSetting(self):
        self.bgrp_target_cop.setCheck(self.def_set['bgrp_target_cop'])
        self.bgrp_file_cop.setCheck(self.def_set['bgrp_file_cop'])
        self.l_edit_cop_file.setText(self.def_set['l_edit_cop_file'])

        self.bgrp_target_paste.setCheck(self.def_set['bgrp_target_paste'])
        self.bgrp_match.setCheck(self.def_set['bgrp_match'])
        self.bgrp_space.setCheck(self.def_set['bgrp_space'])
        self.bgrp_file_paste.setCheck(self.def_set['bgrp_file_paste'])
        self.l_edit_paste_file.setText(self.def_set['l_edit_paste_file'])

    def __setRb(self, rb_key):
        exec("self.{0}.setCheck(self.vcp.setting.get(self._keyname('{0}'), self.def_set['{0}']))".format(rb_key))

    def _setAllSettings(self):
        #copy
        self.__setRb('bgrp_target_cop')
        self.__setRb('bgrp_file_cop')
        self.l_edit_cop_file.setText(
            self.vcp.setting.get(self._keyname('l_edit_cop_file'), self.def_set['l_edit_cop_file'])
        )

        # paste
        self.__setRb('bgrp_target_paste')
        self.__setRb('bgrp_match')
        self.__setRb('bgrp_space')
        self.__setRb('bgrp_file_paste')
        self.l_edit_paste_file.setText(
            self.vcp.setting.get(self._keyname('l_edit_paste_file'), self.def_set['l_edit_paste_file'])
        )

        # axis
        for axis_cb in self.axis_cb_list:
            axis_cb.setChecked(
                self.vcp.setting.get(self._keyname('cb_{0}'.format(axis_cb.text())), True)
            )

        self._changeTargetFileCopy()
        self._changeTargetFilePaste()

    def _saveCopySetting(self):
        self.vcp.setting.set(self._keyname('bgrp_target_cop'), self.bgrp_target_cop.checkedId())
        self.vcp.setting.set(self._keyname('bgrp_file_cop'), self.bgrp_file_cop.checkedId())

    def _savePasteSetting(self):
        self.vcp.setting.set(self._keyname('bgrp_target_paste'), self.bgrp_target_paste.checkedId())
        self.vcp.setting.set(self._keyname('bgrp_match'), self.bgrp_match.checkedId())
        self.vcp.setting.set(self._keyname('bgrp_space'), self.bgrp_space.checkedId())
        self.vcp.setting.set(self._keyname('bgrp_file_paste'), self.bgrp_file_paste.checkedId())

    def _changeTargetFileCopy(self):
        checked_id = self.bgrp_file_cop.checkedId()
        self.l_edit_cop_file.setEnabled(checked_id)
        self.bt_browse_cop.setEnabled(checked_id)

    def _changeTargetFilePaste(self):
        checked_id = self.bgrp_file_paste.checkedId()
        self.l_edit_paste_file.setEnabled(checked_id)
        self.bt_browse_paste.setEnabled(checked_id)

    def _separator(self):
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        return sep

    def _browseButton(self, l_edit, is_copy=True):
        bt_browse = QPushButton()
        #style = bt_browse.style()
        #icon = style.standardIcon(QStyle.SP_DialogOpenButton)
        #bt_browse.setIcon(icon)
        bt_browse.setIcon(QIcon(os.path.join(ICON_FOLDER_PATH, 'folder-closed.png')))

        bt_browse.setMaximumWidth(20)
        bt_browse.setMaximumHeight(20)
        bt_browse.setIconSize(QSize(16, 16))
        bt_browse.clicked.connect(partial(self._fileDialog, l_edit, is_copy))
        return bt_browse

    def _fileDialog(self, l_edit, is_copy):
        if is_copy:
            choise = QFileDialog.getSaveFileName(self, "Select File", l_edit.text(), "*.json")
        else:
            choise = QFileDialog.getOpenFileName(self, "Select File", l_edit.text(), "*.json")
        if choise[0]:
            l_edit.setText(choise[0].replace('/', os.sep))

    def _getCurrentJsonPath(self, is_copy=True):
        current_json = ''
        if is_copy:
            if self.bgrp_file_cop.checkedId() == 0:
                current_json = self.tmp_json
            else:
                current_json = self.l_edit_cop_file.text()
        else:
            if self.bgrp_file_paste.checkedId() == 0:
                current_json = self.tmp_json
            else:
                current_json = self.l_edit_paste_file.text()
        return current_json

    def _getIgnoreAxis(self):
        ignore_axis = []
        for ax in self.axis_cb_list:
            if not ax.checkState():
                ignore_axis.append(ax.text())
        return ignore_axis


class VariousCopyPasteUi(ui.QWindow):
    def __init__(self, *args, **kwargs):
        if py3:
            super().__init__(*args, **kwargs)
        else:
            super(VariousCopyPasteUi, self).__init__(*args, **kwargs)

        self.SETTING_DIR = os.path.join(
            os.getenv("HOMEDRIVE"), os.getenv("HOMEPATH"),
            'Documents', 'maya', 'Scripting_Files', 'variousCopyPaste')
        SETTING_JSON = os.path.join(self.SETTING_DIR, 'variousCopyPaste.json')
        if not os.path.isfile(SETTING_JSON):
            f.exportJson(SETTING_JSON)
        self.setting = f.JsonDict(SETTING_JSON)

        self.help_path = ''

    def initUi(self):

        #メニュー
        #helpIcon = self.style().standardIcon(QStyle.SP_MessageBoxQuestion)
        #rebtIcon = self.style().standardIcon(QStyle.SP_BrowserReload)

        helpAct = QAction('Help', self)
        helpAct.triggered.connect(self._openHelp)
        rebtAct = QAction('Reset', self)
        rebtAct.triggered.connect(self._resetSetting)

        menu_bar = self.menuBar()
        menu = menu_bar.addMenu('Menu')
        menu.addAction(helpAct)
        menu.addSeparator()
        menu.addAction(rebtAct)

        self.tab = QTabWidget()
        self.tab.currentChanged.connect(self._currentChangedTab)

        # -------------------------------------------------------
        # 値
        # -------------------------------------------------------
        self.tab_value = TemplateUiInTab(self, 'Transform', os.path.join(self.SETTING_DIR, 'vcpValue.json'))
        self.tab.insertTab(0, self.tab_value, 'Transform')
        self.tab_value.bt_copy.clicked.connect(self._runCopyValue)
        self.tab_value.bt_paste.clicked.connect(self._runPasteValue)

        # -------------------------------------------------------
        # アニメーション
        # -------------------------------------------------------
        self.tab_anim = TemplateUiInTab(self, 'Anim', os.path.join(self.SETTING_DIR, 'vcpValue.json'))
        #self.tab.insertTab(1, self.tab_anim, 'Anim')

        # -------------------------------------------------------
        # 名前
        # -------------------------------------------------------
        self.tab_name = TemplateUiInTab(self, 'Name', os.path.join(self.SETTING_DIR, 'vcpValue.json'))
        self.tab.insertTab(2, self.tab_name, 'Name')
        self.tab_name.bt_copy.clicked.connect(self._runCopyValue)
        self.tab_name.bt_paste.clicked.connect(self._runPasteName)

        # -------------------------------------------------------
        # log
        # -------------------------------------------------------
        self.tx_ed = QTextEdit()
        self.tab.insertTab(3, self.tx_ed, '[ LOG ]')

        self.layout.addWidget(self.tab)

        self.show()
        self._updateUi()

    def _updateUi(self):
        pass

    def _currentChangedTab(self):
        print('currentChangedTab', self.tab.currentIndex())

    def _clearLog(self):
        self.tx_ed.setText('')

    def _openHelp(self):
        os.startfile(self.help_path)

    def _resetSetting(self):
        self.tab_value._resetSetting()
        self.tab_anim._resetSetting()
        self.tab_name._resetSetting()

    # -------------------------------------------------------
    # 値
    # -------------------------------------------------------
    def _runCopyValue(self):
        pass

    def _runPasteValue(self):
        pass

    # -------------------------------------------------------
    # 名前
    # -------------------------------------------------------
    def _runPasteName(self):
        pass

