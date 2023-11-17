# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division

from maya import cmds, mel
from maya import OpenMayaUI as omui
import maya.api.OpenMaya as om2

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
    from shiboken import wrapInstance

from maya.app.general.mayaMixin import MayaQWidgetBaseMixin, MayaQWidgetDockableMixin

import fnmatch
import re
import time
import traceback

from collections import OrderedDict
from functools import partial
from imp import reload

maya_version = cmds.about(v=True)

TOOL_VERSION = '1.0.0'
PROJ = 'wizard2'
WINDOW_TITLE = 'Set Time From Key'
WINDOW_OPTIONVAR = WINDOW_TITLE.replace(' ', '_')
try:
    DIR_PATH = '/'.join(__file__.replace('\\', '/').split('/')[0:-1])
except:
    DIR_PATH = ''

class SetTimeFromKey(MayaQWidgetDockableMixin, QMainWindow):
    # QMainWindowを継承するとmenubarの使える幅が広い
    def __init__(self, *args, **kwargs):
        super(SetTimeFromKey, self).__init__(*args, **kwargs)

        self.time_range = list()

        self.clipboard = QClipboard()

        self.setWindowTitle('{}:{}:{}'.format(WINDOW_TITLE, TOOL_VERSION, PROJ))


    def layout(self):
        # 全体の大きさの変更
        self.setGeometry(10, 10, 300, 100) # (left, top, width, height)

        self.main_widget = QWidget() # 1
        self.setCentralWidget(self.main_widget)

        self.main_qvbl = QVBoxLayout()
        self.main_widget.setLayout(self.main_qvbl) # 2 上下にウィジェットを追加するレイアウトを追加

        self.main_qhbl = QHBoxLayout()
        self.main_qvbl.addLayout(self.main_qhbl) # 3 左右にウィジェットを追加するレイアウトを追加

        self.main_qgl = QGridLayout()
        self.main_qvbl.addLayout(self.main_qgl)

    def widgets(self):
        # QPushButton
        self.set_cur_time_btn = QPushButton('Save Current Time')
        self.set_cur_time_btn.clicked.connect(partial(self.save_history))
        self.main_qhbl.addWidget(self.set_cur_time_btn)

        # QTreeView
        self.main_tree = QTreeView()
        self.main_tree.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.main_tree.clicked.connect(self.get_tree_items)
        self.main_qhbl.addWidget(self.main_tree)

        # QStandardItemModel
        self.main_tree_model = QStandardItemModel()
        self.main_tree_model.setColumnCount(1)
        self.main_tree_model.setHeaderData(0, Qt.Horizontal, 'History')
        self.main_tree.setModel(self.main_tree_model)

        # QTreeView connect context menu
        self.main_tree.setContextMenuPolicy(Qt.CustomContextMenu) # QTreeViewにコンテキストメニューを追加する設定
        self.main_tree.customContextMenuRequested.connect(self.list_menu_available_sender) # QTreeViewで設定するコンテキストメニュー

        # QPushButton
        self.set_start_btn = QPushButton('|<')
        self.set_start_btn.clicked.connect(partial(set_time_from_key, 'min'))
        self.set_start_btn.setToolTip(u'Set the start time of the playback range')
        self.main_qgl.addWidget(self.set_start_btn, 0, 0)

        self.set_both_btn = QPushButton('|<  >|')
        self.set_both_btn.clicked.connect(partial(set_time_from_key, None))
        self.set_start_btn.setToolTip(u'Set the both times of the playback range')
        self.main_qgl.addWidget(self.set_both_btn, 0, 1)

        self.set_end_btn = QPushButton('>|')
        self.set_end_btn.clicked.connect(partial(set_time_from_key, 'max'))
        self.set_start_btn.setToolTip(u'Set the end time of the playback range')
        self.main_qgl.addWidget(self.set_end_btn, 0, 2)

        self.set_start_time_btn = QPushButton('|<<')
        self.set_start_time_btn.clicked.connect(partial(set_time_slider, 'start'))
        self.main_qgl.addWidget(self.set_start_time_btn, 1, 0)

        self.set_both_time_btn = QPushButton('|<< >>|')
        self.set_both_time_btn.clicked.connect(partial(set_time_slider, 'both'))
        self.main_qgl.addWidget(self.set_both_time_btn, 1, 1)

        self.set_end_time_btn = QPushButton('>>|')
        self.set_end_time_btn.clicked.connect(partial(set_time_slider, 'end'))
        self.main_qgl.addWidget(self.set_end_time_btn, 1, 2)

    def buildUI(self):
        # UI
        self.layout()
        self.widgets()

        # initial set
        self.save_history()

    def copy_times(self):
        self.clipboard.setText('\n'.join(self.cur_items))

    def list_menu_available_sender(self, pos):
        sender = self.sender()
        # menus
        self.context_menu = QMenu(sender)

        # addAction
        context_menu = OrderedDict()
        context_menu['Set Playback Range'] = {'cmd':partial(self.set_time_from_tree)}
        context_menu['Copy Clipboard'] = {'cmd':partial(self.copy_times)}

        for menu_name, menu_cmd in context_menu.items():
            action = self.context_menu.addAction(menu_name)
            action.triggered.connect(menu_cmd['cmd'])

        # QMenuの表示
        self.context_menu.exec_(sender.mapToGlobal(pos))

    def get_tree_items(self):
        sender = self.sender()
        indexes = sender.selectionModel().selectedIndexes()
        self.cur_items = [index.data() for index in indexes]

    def set_time_from_tree(self):
        set_time = self.cur_items[0]
        start_val, min_val = set_time.split('--')[0].split('|')
        max_val, end_val = set_time.split('--')[1].split('|')

        cor_start_val = float(replace_square_brackets(start_val))
        cor_min_val = float(replace_square_brackets(min_val))
        cor_max_val = float(replace_square_brackets(max_val))
        cor_end_val = float(replace_square_brackets(end_val))
        cmds.playbackOptions(ast=cor_start_val, min=cor_min_val, max=cor_max_val, aet=cor_end_val)

    def save_history(self, *args, **kwargs):
        self.time_range = get_time_slider()
        self.insert_row()

    def insert_row(self, *args, **kwargs):
        text = '[{}]|[{}]--[{}]|[{}]'.format(
            self.time_range[2],
            self.time_range[0],
            self.time_range[1],
            self.time_range[3],
            )
        std_item = QStandardItem(text)
        std_item.setEditable(False)
        self.main_tree_model.insertRow(0, std_item)

def get_time_slider():
    min_time = cmds.playbackOptions(q=True, min=True)
    max_time = cmds.playbackOptions(q=True, max=True)
    start_time = cmds.playbackOptions(q=True, ast=True)
    end_time = cmds.playbackOptions(q=True, aet=True)
    return min_time, max_time, start_time, end_time

def set_time_from_key(range_type=None):
    min_time, max_time, start_time, end_time = get_time_slider()

    sel = cmds.ls(os=True)
    if not sel: return min_time, max_time, start_time, end_time
    selected_frame_range = cmds.keyframe(sel[0], q=True)

    fcurve_frame_range = cmds.keyframe(q=True)
    if len(fcurve_frame_range) > 1:
        cmds.playbackOptions(
            min=fcurve_frame_range[0],
            max=fcurve_frame_range[-1]
        )

    else:
        if range_type == 'min':
            cmds.playbackOptions(
                min=fcurve_frame_range[0],
            )
        elif range_type == 'max':
            cmds.playbackOptions(
                max=fcurve_frame_range[0],
            )

    return min_time, max_time, start_time, end_time

def set_time_slider(range_type='both'):
    min_time, max_time, start_time, end_time = get_time_slider()

    if range_type == 'both':
        cmds.playbackOptions(ast=min_time)
        cmds.playbackOptions(aet=max_time)
    elif range_type == 'start':
        cmds.playbackOptions(ast=min_time)
    elif range_type == 'end':
        cmds.playbackOptions(aet=max_time)

def replace_square_brackets(text=None):
    return text.replace('[', '').replace(']', '')


if __name__ == '__main__':
    ui = SetTimeFromKey()
    ui.buildUI()
    ui.show(dockable=True)
