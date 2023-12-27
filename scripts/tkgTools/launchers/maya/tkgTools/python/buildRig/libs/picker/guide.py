# -*- coding: utf-8 -*-
from collections import OrderedDict
from functools import partial
from imp import reload
import traceback

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

import maya.cmds as cmds
import maya.mel as mel

import buildRig.libs.picker.ui as picker
import buildRig.embedJoints as brEJ
reload(picker)
reload(brEJ)

class PickerUI(MayaQWidgetDockableMixin, QMainWindow):
    def __init__(self):
        super().__init__()
        # 
        # self.picker = picker.PickerAnimTools()

        self.setWindowTitle('GuidePicker')

        # メニューバーの追加
        self.menubar = self.menuBar()

        # 4段まで
        self.menu_actions = OrderedDict({
            'File':OrderedDict({
                'Open':{
                    'triggered':partial(self.hello_world),
                    'icon':QIcon(''),
                    'statusTip':''
                }
            }),
            'Edit':OrderedDict({
                'Delete':{
                    'triggered':partial(self.hello_world),
                    'icon':QIcon(''),
                    'statusTip':''
                }
            }),
            'Axis':OrderedDict({
                'Set Axis':OrderedDict({
                    'Spine':{
                        'triggered':partial(self.hello_world),
                        'icon':QIcon(''),
                        'statusTip':''
                    },
                    'Arm':{
                        'triggered':partial(self.hello_world),
                        'icon':QIcon(''),
                        'statusTip':''
                    }
                })
            }),
        })

    def buildUI(self):
        self.menubars()
        self.layout()
        self.biped_layout()

    def menubars(self):
        for menu_name, menu_action in self.menu_actions.items():
            # 1段目追加
            menu_item = self.menubar.addMenu(menu_name)
            for second_menu_name, second_action_dict in menu_action.items():
                if 'triggered' in second_action_dict.keys():
                    # 2段目actionの追加
                    menu_item.addAction(self.add_action(menu_name=second_menu_name,
                                                               **second_action_dict))
                else:
                    # 3段目menuの追加
                    second_menu_item = menu_item.addMenu(second_menu_name)
                    for third_menu_name, third_action_dict in second_action_dict.items():
                        if 'triggered' in third_action_dict.keys():
                            # 3段目actionの追加
                            second_menu_item.addAction(self.add_action(menu_name=third_menu_name,
                                                                    **third_action_dict))
                        else:
                            # 4段目menuの追加
                            third_menu_item = menu_item.addMenu(third_menu_name)
                            for fourth_menu_name, fourth_action_dict in second_action_dict.items():
                                # 4段目actionの追加
                                third_menu_item.addAction(self.add_action(menu_name=fourth_menu_name,
                                                                        **fourth_action_dict))

    def add_action(self,
                   menu_name=None,
                   icon=None,
                   statusTip=None,
                   triggered=None):
        action = QAction(icon,
                         menu_name,
                         self,
                         statusTip=statusTip,
                         triggered=triggered)
        return action

    def hello_world(self):
        print('Hello world')

    def layout(self):
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        self.main_qvbl = QVBoxLayout()
        self.main_qvbl.setAlignment(Qt.AlignTop)
        self.main_widget.setLayout(self.main_qvbl)

        # tab widget
        self.main_tab_widget = QTabWidget()
        self.main_qvbl.addWidget(self.main_tab_widget)

    def biped_layout(self):
        # biped widget
        self.biped_widget = QWidget()
        self.main_tab_widget.addTab(self.biped_widget, 'Biped')

        # scroll areaの設定
        self.scroll_biped_qvbl = QVBoxLayout()
        self.biped_widget.setLayout(self.scroll_biped_qvbl)
        self.scroll_biped_area = QScrollArea()
        self.scroll_biped_area.setWidgetResizable(True)
        self.scroll_biped_area.setMinimumHeight(1)
        self.scroll_biped_qvbl.addWidget(self.scroll_biped_area)

        self.scroll_biped_widget = QWidget()
        self.scroll_biped_area.setWidget(self.scroll_biped_widget)

        self.biped_qvbl = QVBoxLayout()
        self.biped_qvbl.setAlignment(Qt.AlignTop)
        self.scroll_biped_widget.setLayout(self.biped_qvbl)

        # set mesh
        self.mesh_hb_layout = QHBoxLayout()
        self.biped_qvbl.addLayout(self.mesh_hb_layout)

        self.mesh_le = QLineEdit()
        self.mesh_btn = QPushButton('<< Set Mesh')
        self.mesh_btn.clicked.connect(partial(self.set_setText_selection, self.mesh_le))

        self.mesh_hb_layout.addWidget(self.mesh_le)
        self.mesh_hb_layout.addWidget(self.mesh_btn)

        # counter
        # root
        self.root_count_hb_layout = PartsLayout(parent_layout=self.biped_qvbl,
                                                 part_label='Root',
                                                 value=1)
        self.root_count_dsbox = self.root_count_hb_layout.count_box

        # spine
        self.spine_count_hb_layout = PartsLayout(parent_layout=self.biped_qvbl,
                                                 part_label='Spine',
                                                 value=3)
        self.spine_count_dsbox = self.spine_count_hb_layout.count_box

        # neck
        self.neck_count_hb_layout = PartsLayout(parent_layout=self.biped_qvbl,
                                                 part_label='Neck',
                                                 value=1)
        self.neck_count_dsbox = self.neck_count_hb_layout.count_box

        # knee
        self.knee_count_hb_layout = PartsLayout(parent_layout=self.biped_qvbl,
                                                 part_label='Knee',
                                                 value=1)
        self.knee_count_dsbox = self.knee_count_hb_layout.count_box

        # thumb
        self.thumb_count_hb_layout = PartsLayout(parent_layout=self.biped_qvbl,
                                                 part_label='Thumb',
                                                 value=3)
        self.thumb_count_dsbox = self.thumb_count_hb_layout.count_box

        # index
        self.index_count_hb_layout = PartsLayout(parent_layout=self.biped_qvbl,
                                                 part_label='Index',
                                                 value=3)
        self.index_count_dsbox = self.index_count_hb_layout.count_box

        # middle
        self.middle_count_hb_layout = PartsLayout(parent_layout=self.biped_qvbl,
                                                 part_label='Middle',
                                                 value=3)
        self.middle_count_dsbox = self.middle_count_hb_layout.count_box

        # ring
        self.ring_count_hb_layout = PartsLayout(parent_layout=self.biped_qvbl,
                                                 part_label='Ring',
                                                 value=3)
        self.ring_count_dsbox = self.ring_count_hb_layout.count_box

        # pinky
        self.pinky_count_hb_layout = PartsLayout(parent_layout=self.biped_qvbl,
                                                 part_label='Pinky',
                                                 value=3)
        self.pinky_count_dsbox = self.pinky_count_hb_layout.count_box

        # boxをリストに代入しておく
        self.parts_count_boxes = [
            self.root_count_dsbox,
            self.spine_count_dsbox,
            self.neck_count_dsbox,
            self.knee_count_dsbox,
            self.thumb_count_dsbox,
            self.index_count_dsbox,
            self.middle_count_dsbox,
            self.ring_count_dsbox,
            self.pinky_count_dsbox,
        ]

        # ガイド作成ボタン
        self.create_biped_guide_btn = QPushButton('Create Biped Guide')
        self.biped_qvbl.addWidget(self.create_biped_guide_btn)
        self.create_biped_guide_btn.clicked.connect(partial(self.create_biped_guide))


    def biped_source_mesh(self):
        self.current_biped_mesh = self.mesh_le.text()

    def biped_parts_count(self):
        self.current_parts_count = [int(box.value()) for box in self.parts_count_boxes]

    def set_setText_selection(self, text_type_object=None):
        sel = cmds.ls(os=True)
        if not sel:
            return
        if text_type_object.metaObject().className() in ['QLineEdit']:
            text_type_object.setText(sel[0])

    def create_biped_guide(self):
        cmds.undoInfo(openChunk=True)

        self.biped_source_mesh()
        self.biped_parts_count()
        embed = brEJ.EmbedJoints(mesh=self.current_biped_mesh,
                                root_count=self.current_parts_count[0],
                                spine_count=self.current_parts_count[1],
                                neck_count=self.current_parts_count[2],
                                knee_count=self.current_parts_count[3],
                                thumb_count=self.current_parts_count[4],
                                index_count=self.current_parts_count[5],
                                middle_count=self.current_parts_count[6],
                                ring_count=self.current_parts_count[7],
                                pinky_count=self.current_parts_count[8],
                                type='biped',
                                create=True,
                                guide_name=None)

        cmds.undoInfo(closeChunk=True)

class PartsCountSpinBox(QDoubleSpinBox):
    def __init__(self, value=None):
        super().__init__()
        self.setDecimals(0)
        self.setRange(1, 10)
        self.setValue(value)

class PartsLayout(QHBoxLayout):
    def __init__(self, parent_layout=None, part_label=None, value=None):
        super().__init__()
        parent_layout.addLayout(self)
        self.addWidget(QLabel(part_label))
        self.count_box = PartsCountSpinBox(value=value)
        self.addWidget(self.count_box)

