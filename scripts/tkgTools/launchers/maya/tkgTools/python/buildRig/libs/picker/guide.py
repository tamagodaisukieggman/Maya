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

import buildRig.libs.picker.graphics as graphics
import buildRig.embedJoints as brEJ
import buildRig.modifyJoints as brMJ
reload(graphics)
reload(brEJ)
reload(brMJ)

# default color
DEFAULT_BUTTON_COLOR = QColor()
DEFAULT_BUTTON_COLOR.setRgbF(0.364706, 0.364706, 0.364706)
"""
# self.biped_collapse_toggle = False

# set_palette.setColor(QPalette.Button, DEFAULT_BUTTON_COLOR)
# chbx.setAutoFillBackground(True)
# chbx.setPalette(set_palette)

widget.hide()
# self.biped_collapse_toggle = True

# new_color = QColor()
# new_color.setRgbF(0.5, 0.5, 0.25)
# set_palette.setColor(QPalette.Button, new_color)
# chbx.setAutoFillBackground(True)
# chbx.setPalette(set_palette)
"""

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

        self.embed = None

    def buildUI(self):
        self.menubars()
        self.layout()
        self.biped_layout()
        self.biped_signal_slots()

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

        # ガイド用のscroll areaの設定
        self.scroll_biped_qvbl = QVBoxLayout()
        self.scroll_biped_qvbl.setAlignment(Qt.AlignTop)
        self.biped_widget.setLayout(self.scroll_biped_qvbl)

        # 展開
        self.biped_collapsible_qvbl = QVBoxLayout()
        self.biped_collapsible_qvbl.setAlignment(Qt.AlignTop)
        self.scroll_biped_qvbl.addLayout(self.biped_collapsible_qvbl)

        self.biped_collapsible_chbx = QCheckBox('Guide Settings')
        self.biped_collapsible_chbx.setChecked(True)
        self.biped_collapsible_qvbl.addWidget(self.biped_collapsible_chbx)

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
        self.biped_qhbl = QHBoxLayout()
        self.biped_qvbl.addLayout(self.biped_qhbl)

        self.mesh_le = QLineEdit()
        self.mesh_btn = QPushButton('<< Set Mesh')

        self.biped_qhbl.addWidget(self.mesh_le)
        self.biped_qhbl.addWidget(self.mesh_btn)

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

        # メッシュのペアレント、アンペアレント
        self.biped_pa_unparent_mesh_btn = QPushButton('Parent Unparent Mesh')
        self.biped_qvbl.addWidget(self.biped_pa_unparent_mesh_btn)

        ###########################
        # コントローラ調整用のscroll areaの設定
        # 展開
        self.biped_ctrl_collapsible_qvbl = QVBoxLayout()
        self.scroll_biped_qvbl.addLayout(self.biped_ctrl_collapsible_qvbl)

        self.biped_ctrl_collapsible_chbx = QCheckBox('Guide Controller Settings')
        self.biped_ctrl_collapsible_chbx.setChecked(True)
        self.biped_ctrl_collapsible_qvbl.addWidget(self.biped_ctrl_collapsible_chbx)

        self.scroll_ctrl_biped_area = QScrollArea()
        self.scroll_ctrl_biped_area.setWidgetResizable(True)
        self.scroll_ctrl_biped_area.setMinimumHeight(1)
        self.scroll_biped_qvbl.addWidget(self.scroll_ctrl_biped_area)

        self.scroll_ctrl_biped_widget = QWidget()
        self.scroll_ctrl_biped_area.setWidget(self.scroll_ctrl_biped_widget)

        self.biped_ctrl_qvbl = QVBoxLayout()
        self.biped_ctrl_qvbl.setAlignment(Qt.AlignTop)
        self.scroll_ctrl_biped_widget.setLayout(self.biped_ctrl_qvbl)

        # adjust ctrls
        self.biped_ctrl_qhbl = QHBoxLayout()
        self.biped_ctrl_qvbl.addLayout(self.biped_ctrl_qhbl)

        self.get_cur_adj_ctrl_btn = QPushButton('Get Current Adjust Ctrls')
        self.biped_ctrl_qvbl.addWidget(self.get_cur_adj_ctrl_btn)

        # all check axis
        self.all_axis_chbx = QCheckBox('All Check')
        self.all_axis_chbx.setChecked(True)
        self.biped_ctrl_qvbl.addWidget(self.all_axis_chbx)

        # spine axis
        self.spine_axis_layout = SetAxisLayout(parent_layout=self.biped_ctrl_qvbl,
                                               part='Spine',
                                               aim_axis_offset=True,
                                               init_aim_axis='y',
                                               init_up_axis='z')

        # set spine axis button
        self.set_spine_axis_btn = QPushButton('Set Spine Axis')
        self.spine_axis_layout.addWidget(self.set_spine_axis_btn)

        # neck axis
        self.neck_axis_layout = SetAxisLayout(parent_layout=self.biped_ctrl_qvbl,
                                               part='Neck',
                                               aim_axis_offset=True,
                                               init_aim_axis='y',
                                               init_up_axis='z')

        # set neck axis button
        self.set_neck_axis_btn = QPushButton('Set Neck Axis')
        self.neck_axis_layout.addWidget(self.set_neck_axis_btn)

        # head axis
        self.head_axis_layout = SetAxisLayout(parent_layout=self.biped_ctrl_qvbl,
                                               part='Head',
                                               aim_axis_offset=True,
                                               init_aim_axis='y',
                                               init_up_axis='z')

        # set head axis button
        self.set_head_axis_btn = QPushButton('Set Head Axis')
        self.head_axis_layout.addWidget(self.set_head_axis_btn)

        # arm axis
        self.shoulder_axis_layout = SetAxisLayout(parent_layout=self.biped_ctrl_qvbl,
                                                  part='Shoulder',
                                                  aim_axis_offset=None,
                                                  init_aim_axis='x',
                                                  init_up_axis='y')
        self.arm_axis_layout = SetAxisLayout(parent_layout=self.biped_ctrl_qvbl,
                                             part='Arm',
                                             aim_axis_offset=None,
                                             init_aim_axis='x',
                                             init_up_axis='y')

        # set shoulder arm axis button
        self.set_arm_axis_btn = QPushButton('Set Shoulder Arm Axis')
        self.arm_axis_layout.addWidget(self.set_arm_axis_btn)

        # thigh leg ankle ball axis
        self.thigh_axis_layout = SetAxisLayout(parent_layout=self.biped_ctrl_qvbl,
                                                  part='Thigh',
                                                  aim_axis_offset=None,
                                                  init_aim_axis='x',
                                                  init_up_axis='y')

        self.leg_axis_layout = SetAxisLayout(parent_layout=self.biped_ctrl_qvbl,
                                                  part='Leg',
                                                  aim_axis_offset=None,
                                                  init_aim_axis='x',
                                                  init_up_axis='y')

        self.ankle_axis_layout = SetAxisLayout(parent_layout=self.biped_ctrl_qvbl,
                                                  part='Ankle',
                                                  aim_axis_offset=None,
                                                  init_aim_axis='x',
                                                  init_up_axis='y')

        self.ball_axis_layout = SetAxisLayout(parent_layout=self.biped_ctrl_qvbl,
                                                  part='Ball',
                                                  aim_axis_offset=None,
                                                  init_aim_axis='x',
                                                  init_up_axis='y')

        # set legs axis button
        self.set_legs_axis_btn = QPushButton('Set Legs Axis')
        self.ball_axis_layout.addWidget(self.set_legs_axis_btn)

        # fingers axis
        # thumb axis
        self.thumb_axis_layout = SetAxisLayout(parent_layout=self.biped_ctrl_qvbl,
                                                  part='Thumb',
                                                  aim_axis_offset=True,
                                                  init_aim_axis='x',
                                                  init_up_axis='y')

        # set thumb axis button
        self.set_thumb_axis_btn = QPushButton('Set Thumb Axis')
        self.thumb_axis_layout.addWidget(self.set_thumb_axis_btn)

        # index axis
        self.index_axis_layout = SetAxisLayout(parent_layout=self.biped_ctrl_qvbl,
                                                  part='Index',
                                                  aim_axis_offset=True,
                                                  init_aim_axis='x',
                                                  init_up_axis='y')

        # set index axis button
        self.set_index_axis_btn = QPushButton('Set Index Axis')
        self.index_axis_layout.addWidget(self.set_index_axis_btn)

        # middle axis
        self.middle_axis_layout = SetAxisLayout(parent_layout=self.biped_ctrl_qvbl,
                                                  part='Middle',
                                                  aim_axis_offset=True,
                                                  init_aim_axis='x',
                                                  init_up_axis='y')

        # set middle axis button
        self.set_middle_axis_btn = QPushButton('Set Middle Axis')
        self.middle_axis_layout.addWidget(self.set_middle_axis_btn)

        # ring axis
        self.ring_axis_layout = SetAxisLayout(parent_layout=self.biped_ctrl_qvbl,
                                                  part='Ring',
                                                  aim_axis_offset=True,
                                                  init_aim_axis='x',
                                                  init_up_axis='y')

        # set ring axis button
        self.set_ring_axis_btn = QPushButton('Set Ring Axis')
        self.ring_axis_layout.addWidget(self.set_ring_axis_btn)

        # pinky axis
        self.pinky_axis_layout = SetAxisLayout(parent_layout=self.biped_ctrl_qvbl,
                                                  part='Pinky',
                                                  aim_axis_offset=True,
                                                  init_aim_axis='x',
                                                  init_up_axis='y')

        # set pinky axis button
        self.set_pinky_axis_btn = QPushButton('Set Pinky Axis')
        self.pinky_axis_layout.addWidget(self.set_pinky_axis_btn)

        # layouts for all scales
        self.part_layouts = [
            self.spine_axis_layout,
            self.neck_axis_layout,
            self.head_axis_layout,
            self.shoulder_axis_layout,
            self.arm_axis_layout,
            self.thigh_axis_layout,
            self.leg_axis_layout,
            self.ankle_axis_layout,
            self.ball_axis_layout,
            self.thumb_axis_layout,
            self.index_axis_layout,
            self.middle_axis_layout,
            self.ring_axis_layout,
            self.pinky_axis_layout
        ]

        # checkbox for all check
        self.axis_chbxes = [lay.axis_chbx for lay in self.part_layouts]

        if not self.embed:
            self.get_cur_adj_ctrls()

    def biped_signal_slots(self):
        # 展開
        # self.biped_collapsible_chbx.toggled.connect(partial(self.collapsible_toggle,
        #                                                    self.biped_collapsible_chbx,
        #                                                    self.scroll_biped_area))

        self.biped_collapsible_chbx.stateChanged.connect(lambda: collapsible_toggle(self.biped_collapsible_chbx, self.scroll_biped_area))

        # self.biped_ctrl_collapsible_chbx.toggled.connect(partial(self.collapsible_toggle,
        #                                                    self.biped_ctrl_collapsible_chbx,
        #                                                    self.scroll_ctrl_biped_area))

        self.biped_ctrl_collapsible_chbx.stateChanged.connect(lambda: collapsible_toggle(self.biped_ctrl_collapsible_chbx, self.scroll_ctrl_biped_area))

        # Set Mesh
        self.mesh_btn.clicked.connect(partial(self.set_setText_selection, self.mesh_le))

        # ガイド作成ボタン
        self.create_biped_guide_btn.clicked.connect(partial(self.create_biped_guide))

        # メッシュのペアレント、アンペアレント
        self.biped_pa_unparent_mesh_btn.clicked.connect(partial(self.pa_unparent_mesh))

        # カレントのadjustコントローラの取得
        self.get_cur_adj_ctrl_btn.clicked.connect(partial(self.get_cur_adj_ctrls))

        # all axis check
        self.all_axis_chbx.stateChanged.connect(lambda: check_to_checks(self.all_axis_chbx, self.axis_chbxes))

        # set axis btn
        self.set_spine_axis_btn.clicked.connect(lambda: self.set_spine_axis(axis_layout=self.spine_axis_layout))
        self.set_neck_axis_btn.clicked.connect(lambda: self.set_neck_axis(axis_layout=self.neck_axis_layout))
        self.set_thumb_axis_btn.clicked.connect(lambda: self.set_thumb_axis(axis_layout=self.thumb_axis_layout))
        self.set_index_axis_btn.clicked.connect(lambda: self.set_index_axis(axis_layout=self.index_axis_layout))
        self.set_middle_axis_btn.clicked.connect(lambda: self.set_middle_axis(axis_layout=self.middle_axis_layout))
        self.set_ring_axis_btn.clicked.connect(lambda: self.set_ring_axis(axis_layout=self.ring_axis_layout))
        self.set_pinky_axis_btn.clicked.connect(lambda: self.set_pinky_axis(axis_layout=self.pinky_axis_layout))

        self.set_arm_axis_btn.clicked.connect(lambda: self.set_arm_axis(shoulder_axis_layout=self.shoulder_axis_layout,
                                                                        arm_axis_layout=self.arm_axis_layout))

        self.set_legs_axis_btn.clicked.connect(lambda: self.set_legs_axis([self.thigh_axis_layout,
                                                                           self.leg_axis_layout,
                                                                           self.ankle_axis_layout,
                                                                           self.ball_axis_layout]))



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
        self.embed = brEJ.EmbedJoints(mesh=self.current_biped_mesh,
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

        self.create_guide_pickers()

        cmds.undoInfo(closeChunk=True)

    def set_spine_axis(self, axis_layout=None):
        axis_layout.get_current_values()
        # self.embed.set_spine_axis_pv_up(spine_aim_axis=axis_layout.aim_axis,
        #                         spine_up_axis=axis_layout.up_axis,
        #                         offset_aim_rotate=axis_layout.offset_rotate)

        brMJ.set_chain_axis(chain=self.embed.spine_rot_locs,
                   aim_axis=axis_layout.aim_axis,
                   up_axis=axis_layout.up_axis,
                   worldSpace=False,
                   world_axis='y',
                   offset_aim_rotate=axis_layout.offset_rotate,
                   set_tip=True)

    def set_neck_axis(self, axis_layout=None):
        axis_layout.get_current_values()
        self.embed.set_neck_axis_pv_up(spine_aim_axis=axis_layout.aim_axis,
                                spine_up_axis=axis_layout.up_axis,
                                offset_aim_rotate=axis_layout.offset_rotate)

        # brMJ.set_chain_axis(chain=self.embed.neck_rot_locs,
        #            aim_axis=axis_layout.aim_axis,
        #            up_axis=axis_layout.up_axis,
        #            worldSpace=False,
        #            world_axis='y',
        #            offset_aim_rotate=axis_layout.offset_rotate,
        #            set_tip=True)


    def set_thumb_axis(self, axis_layout=None):
        axis_layout.get_current_values()
        # self.embed.set_thumb_axis_pv_up(thumb_aim_axis=axis_layout.aim_axis,
        #                         thumb_up_axis=axis_layout.up_axis,
        #                         offset_aim_rotate=axis_layout.offset_rotate)

        brMJ.set_chain_axis(chain=self.embed.left_thumb_rot_locs,
                   aim_axis=axis_layout.aim_axis,
                   up_axis=axis_layout.up_axis,
                   worldSpace=False,
                   world_axis='y',
                   offset_aim_rotate=axis_layout.offset_rotate,
                   set_tip=True)

    def set_index_axis(self, axis_layout=None):
        axis_layout.get_current_values()
        # self.embed.set_index_axis_pv_up(index_aim_axis=axis_layout.aim_axis,
        #                         index_up_axis=axis_layout.up_axis,
        #                         offset_aim_rotate=axis_layout.offset_rotate)

        brMJ.set_chain_axis(chain=self.embed.left_index_rot_locs,
                   aim_axis=axis_layout.aim_axis,
                   up_axis=axis_layout.up_axis,
                   worldSpace=False,
                   world_axis='y',
                   offset_aim_rotate=axis_layout.offset_rotate,
                   set_tip=True)


    def set_middle_axis(self, axis_layout=None):
        axis_layout.get_current_values()
        # self.embed.set_middle_axis_pv_up(middle_aim_axis=axis_layout.aim_axis,
        #                         middle_up_axis=axis_layout.up_axis,
        #                         offset_aim_rotate=axis_layout.offset_rotate)

        brMJ.set_chain_axis(chain=self.embed.left_middle_rot_locs,
                   aim_axis=axis_layout.aim_axis,
                   up_axis=axis_layout.up_axis,
                   worldSpace=False,
                   world_axis='y',
                   offset_aim_rotate=axis_layout.offset_rotate,
                   set_tip=True)


    def set_ring_axis(self, axis_layout=None):
        axis_layout.get_current_values()
        # self.embed.set_ring_axis_pv_up(ring_aim_axis=axis_layout.aim_axis,
        #                         ring_up_axis=axis_layout.up_axis,
        #                         offset_aim_rotate=axis_layout.offset_rotate)

        brMJ.set_chain_axis(chain=self.embed.left_ring_rot_locs,
                   aim_axis=axis_layout.aim_axis,
                   up_axis=axis_layout.up_axis,
                   worldSpace=False,
                   world_axis='y',
                   offset_aim_rotate=axis_layout.offset_rotate,
                   set_tip=True)

    def set_pinky_axis(self, axis_layout=None):
        axis_layout.get_current_values()
        # self.embed.set_pinky_axis_pv_up(pinky_aim_axis=axis_layout.aim_axis,
        #                         pinky_up_axis=axis_layout.up_axis,
        #                         offset_aim_rotate=axis_layout.offset_rotate)

        brMJ.set_chain_axis(chain=self.embed.left_pinky_rot_locs,
                   aim_axis=axis_layout.aim_axis,
                   up_axis=axis_layout.up_axis,
                   worldSpace=False,
                   world_axis='y',
                   offset_aim_rotate=axis_layout.offset_rotate,
                   set_tip=True)

    def set_arm_axis(self, shoulder_axis_layout=None, arm_axis_layout=None):
        shoulder_axis_layout.get_current_values()
        arm_axis_layout.get_current_values()

        self.embed.set_arm_axis_pv_up(shoulder_aim_axis=shoulder_axis_layout.aim_axis,
                                      shoulder_up_axis=shoulder_axis_layout.up_axis,
                                      shoulder_worldSpace=False,
                                      shoulder_world_axis='y',
                                      arm_aim_axis=arm_axis_layout.aim_axis,
                                      arm_up_axis=arm_axis_layout.up_axis,
                                      arm_worldSpace=False,
                                      arm_world_axis='y')

        # brMJ.set_chain_axis(chain=self.embed.left_arm_rot_locs,
        #            aim_axis=axis_layout.aim_axis,
        #            up_axis=axis_layout.up_axis,
        #            worldSpace=False,
        #            world_axis='y',
        #            offset_aim_rotate=axis_layout.offset_rotate,
        #            set_tip=True)

    def set_legs_axis(self, axis_layouts=None):
        [lay.get_current_values() for lay in axis_layouts]

        self.embed.set_leg_axis_pv_up(thigh_aim_axis=axis_layouts[0].aim_axis,
                                      thigh_up_axis=axis_layouts[0].up_axis,
                                      thigh_worldSpace=False,
                                      thigh_world_axis='y',
                                      leg_aim_axis=axis_layouts[1].aim_axis,
                                      leg_up_axis=axis_layouts[1].up_axis,
                                      leg_worldSpace=False,
                                      leg_world_axis='y',
                                      ankle_aim_axis=axis_layouts[2].aim_axis,
                                      ankle_up_axis=axis_layouts[2].up_axis,
                                      ankle_worldSpace=False,
                                      ankle_world_axis='y',
                                      ball_aim_axis=axis_layouts[3].aim_axis,
                                      ball_up_axis=axis_layouts[3].up_axis,
                                      ball_worldSpace=False,
                                      ball_world_axis='y')


    def pa_unparent_mesh(self):
        if self.embed:
            self.embed.pa_unparent_mesh()

    def get_cur_adj_ctrls(self):
        self.embed = brEJ.EmbedJoints(create=None)
        self.embed.get_current_adjust_axis_values()

        self.create_guide_pickers()

    def create_guide_pickers(self):
        try:
            self.part_layout_index = {
                0:'spine',
                1:'neck',
                2:'head',
                3:'arm',
                4:'arm',
                5:'leg',
                6:'leg',
                7:'leg',
                8:'leg',
                9:'thumb',
                10:'index',
                11:'middle',
                12:'ring',
                13:'pinky'
            }
            for i, part_lay in enumerate(self.part_layouts):
                part = self.part_layout_index[i]
                CtrlScaleSpinBoxes(parent_layout=part_lay,
                                part=part.capitalize(),
                                pos_scale_attr='{}PosLocsScale'.format(part),
                                rot_scale_attr='{}RotLocsScale'.format(part))
        except:
            pass

        try:
            # pinky picker
            pinky_guide_picker = CreateGuidePicker(parent_layout=self.pinky_axis_layout,
                                                   embed_pos_ctrls=self.embed.left_pinky_pos_locs,
                                                   embed_rot_ctrls=self.embed.left_pinky_rot_locs)
        except:
            pass


class PartsCountSpinBox(QDoubleSpinBox):
    def __init__(self, value=None):
        super().__init__()
        self.setDecimals(0)
        self.setRange(1, 10)
        self.setValue(value)

class AimOffsetAxisSpinBox(QDoubleSpinBox):
    def __init__(self):
        super().__init__()
        self.setDecimals(1)
        self.setRange(-360, 360)
        self.setValue(0)

class CtrlScaleSpinBox(QDoubleSpinBox):
    def __init__(self, parent_layout=None, part=None, scale_attr=None):
        super().__init__()
        self.setDecimals(1)
        self.setRange(1, 100)
        self.setSingleStep(1)

        qhbl = QHBoxLayout()
        parent_layout.addLayout(qhbl)

        qhbl.addWidget(QLabel(part))
        qhbl.addWidget(self)
        self.valueChanged.connect(lambda: self.ctrl_scale_change(self))
        self.scale_attr = scale_attr

        self.init_attr = cmds.getAttr('all_adjust_ctrl.{}'.format(self.scale_attr))
        self.setValue(self.init_attr)

    def ctrl_scale_change(self, spbx=None):
        cmds.setAttr('all_adjust_ctrl.{}'.format(self.scale_attr), spbx.value())

class CtrlScaleSpinBoxes:
    def __init__(self, parent_layout=None, part=None, pos_scale_attr=None, rot_scale_attr=None):
        self.pos_ctrl_scale_spbx = CtrlScaleSpinBox(parent_layout=parent_layout, part='{} Pos Ctrl Scale'.format(part), scale_attr=pos_scale_attr)
        self.rot_ctrl_scale_spbx = CtrlScaleSpinBox(parent_layout=parent_layout, part='{} Rot Ctrl Scale'.format(part), scale_attr=rot_scale_attr)

class PartsLayout(QHBoxLayout):
    def __init__(self, parent_layout=None, part_label=None, value=None):
        super().__init__()
        parent_layout.addLayout(self)
        self.addWidget(QLabel(part_label))
        self.count_box = PartsCountSpinBox(value=value)
        self.addWidget(self.count_box)

class CustomSplitter(QSplitter):
    def __init__(self, parent_layout=None, type='Horizontal'):
        super().__init__()

        if type == 'Horizontal':
            splitter = QSplitter(Qt.Horizontal)
        elif type == 'Vertical':
            splitter = QSplitter(Qt.Vertical)
        bottom = QFrame()
        bottom.setFrameShape(QFrame.HLine)
        splitter.addWidget(bottom)
        parent_layout.addWidget(splitter)


class SetAxisLayout(QVBoxLayout):
    def __init__(self,
                 parent_layout=None,
                 part=None,
                 aim_axis_offset=None,
                 init_aim_axis='x',
                 init_aim_negative=None,
                 init_up_axis='y',
                 init_up_negative=None):
        super().__init__()

        self.aim_axis = None
        self.up_axis = None
        self.aim_axis_offset = aim_axis_offset
        self.offset_rotate = 0

        CustomSplitter(parent_layout, 'Horizontal')

        self.axis_chbx = QCheckBox('{} Position & Axis'.format(part))
        self.axis_chbx.setChecked(True)
        parent_layout.addWidget(self.axis_chbx)

        self.axis_widget = QWidget()
        parent_layout.addWidget(self.axis_widget)

        self.axis_widget.setLayout(self)

        self.axis_chbx.stateChanged.connect(lambda: collapsible_toggle(self.axis_chbx,
                                                                        self.axis_widget))


        # aim axis
        self.aim_axis_qhbl = QHBoxLayout()
        self.addLayout(self.aim_axis_qhbl)

        self.aim_axis_radioGroup = QButtonGroup()
        self.aim_axis_radioGroup.buttonClicked.connect(lambda: self.get_current_values())

        aim_axis_radio_x = QRadioButton("X")
        aim_axis_radio_y = QRadioButton("Y")
        aim_axis_radio_z = QRadioButton("Z")

        self.aim_axis_radioGroup.addButton(aim_axis_radio_x, 1)
        self.aim_axis_radioGroup.addButton(aim_axis_radio_y, 2)
        self.aim_axis_radioGroup.addButton(aim_axis_radio_z, 3)

        self.aim_axis_qhbl.addWidget(QLabel('Aim Axis'))
        self.aim_axis_qhbl.addWidget(aim_axis_radio_x)
        self.aim_axis_qhbl.addWidget(aim_axis_radio_y)
        self.aim_axis_qhbl.addWidget(aim_axis_radio_z)

        if init_aim_axis == 'x':
            aim_axis_radio_x.setChecked(True)
        elif init_aim_axis == 'y':
            aim_axis_radio_y.setChecked(True)
        elif init_aim_axis == 'z':
            aim_axis_radio_z.setChecked(True)

        self.aim_negative_chbx = QCheckBox('Negative')
        if init_aim_negative:
            self.aim_negative_chbx.setChecked(True)
        self.aim_axis_qhbl.addWidget(self.aim_negative_chbx)
        self.aim_negative_chbx.stateChanged.connect(lambda: self.get_current_values())

        # up axis
        self.up_axis_qhbl = QHBoxLayout()
        self.addLayout(self.up_axis_qhbl)

        self.up_axis_radioGroup = QButtonGroup()
        self.up_axis_radioGroup.buttonClicked.connect(lambda: self.get_current_values())

        up_axis_radio_x = QRadioButton("X")
        up_axis_radio_y = QRadioButton("Y")
        up_axis_radio_z = QRadioButton("Z")

        self.up_axis_radioGroup.addButton(up_axis_radio_x, 1)
        self.up_axis_radioGroup.addButton(up_axis_radio_y, 2)
        self.up_axis_radioGroup.addButton(up_axis_radio_z, 3)

        if init_up_axis == 'x':
            up_axis_radio_x.setChecked(True)
        elif init_up_axis == 'y':
            up_axis_radio_y.setChecked(True)
        elif init_up_axis == 'z':
            up_axis_radio_z.setChecked(True)

        self.up_axis_qhbl.addWidget(QLabel('Up Axis'))
        self.up_axis_qhbl.addWidget(up_axis_radio_x)
        self.up_axis_qhbl.addWidget(up_axis_radio_y)
        self.up_axis_qhbl.addWidget(up_axis_radio_z)

        self.up_negative_chbx = QCheckBox('Negative')
        if init_up_negative:
            self.up_negative_chbx.setChecked(True)
        self.up_axis_qhbl.addWidget(self.up_negative_chbx)
        self.up_negative_chbx.stateChanged.connect(lambda: self.get_current_values())

        # aim offset
        if self.aim_axis_offset: self.add_aim_axis_offset()

    def add_aim_axis_offset(self):
        self.aim_axis_offset_qhbl = QHBoxLayout()
        self.addLayout(self.aim_axis_offset_qhbl)

        self.aim_axis_offset_qhbl.addWidget(QLabel('Aim Axis Offset Rotate'))

        self.aim_axis_offset_dsbox = AimOffsetAxisSpinBox()
        self.aim_axis_offset_qhbl.addWidget(self.aim_axis_offset_dsbox)

    def get_current_values(self):
        # aim
        aim_negative = ''
        if self.aim_negative_chbx.isChecked():
            aim_negative = '-'

        aim_axis_btn = self.aim_axis_radioGroup.checkedButton()
        self.aim_axis = aim_negative + aim_axis_btn.text().lower()

        # up
        up_negative = ''
        if self.up_negative_chbx.isChecked():
            up_negative = '-'

        up_axis_btn = self.up_axis_radioGroup.checkedButton()
        self.up_axis = up_negative + up_axis_btn.text().lower()

        # offset rotate
        if self.aim_axis_offset:
            self.offset_rotate = self.aim_axis_offset_dsbox.value()
        
class CreateGuidePicker:
    def __init__(self,
                 parent_layout=None,
                 embed_pos_ctrls=None,
                 embed_rot_ctrls=None):
        self.pos_rot_picker_items = {}
        init_x = -100
        init_y = -100
        for ctrl in embed_pos_ctrls:
            self.pos_rot_picker_items[ctrl] = {}
            self.pos_rot_picker_items[ctrl]['item_name'] = ctrl
            self.pos_rot_picker_items[ctrl]['shape'] = 3
            self.pos_rot_picker_items[ctrl]['rect'] = [init_x, init_y, 15, 15]
            self.pos_rot_picker_items[ctrl]['color'] = [255, 255, 100]
            self.pos_rot_picker_items[ctrl]['edge_color'] = [0,0,0]
            self.pos_rot_picker_items[ctrl]['width'] = 1
            self.pos_rot_picker_items[ctrl]['text_size'] = 2
            self.pos_rot_picker_items[ctrl]['text_offset_pos'] = [-5, -10]

            init_x += 20

        init_x = -100
        init_y += 20
        for ctrl in embed_rot_ctrls:
            self.pos_rot_picker_items[ctrl] = {}
            self.pos_rot_picker_items[ctrl]['item_name'] = ctrl
            self.pos_rot_picker_items[ctrl]['shape'] = 2
            self.pos_rot_picker_items[ctrl]['rect'] = [init_x, init_y, 15, 15]
            self.pos_rot_picker_items[ctrl]['color'] = [100, 128, 255]
            self.pos_rot_picker_items[ctrl]['edge_color'] = [0,0,0]
            self.pos_rot_picker_items[ctrl]['width'] = 1
            self.pos_rot_picker_items[ctrl]['text_size'] = 2
            self.pos_rot_picker_items[ctrl]['text_offset_pos'] = [-5, -10]

            init_x += 20

        self.graphics_view = graphics.GraphicsView(self.pos_rot_picker_items)
        self.graphics_view.enable_wheelEvent = False
        parent_layout.addWidget(self.graphics_view)


def collapsible_toggle(chbx=None, widget=None):
    if chbx.isChecked():
        widget.show()
        # self.biped_collapse_toggle = False

        # set_palette.setColor(QPalette.Button, DEFAULT_BUTTON_COLOR)
        # chbx.setAutoFillBackground(True)
        # chbx.setPalette(set_palette)

    else:
        widget.hide()
        # self.biped_collapse_toggle = True

        # new_color = QColor()
        # new_color.setRgbF(0.5, 0.5, 0.25)
        # set_palette.setColor(QPalette.Button, new_color)
        # chbx.setAutoFillBackground(True)
        # chbx.setPalette(set_palette)

def check_to_checks(chbx=None, chbxes=None):
    if chbx.isChecked():
        [c.setChecked(True) for c in chbxes]
    else:
        [c.setChecked(False) for c in chbxes]