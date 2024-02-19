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

import base64
import codecs
import fnmatch
import glob
import json
import math
import os
import pickle
import re
import subprocess
import sys
import time
import traceback

from collections import OrderedDict
from functools import partial
from imp import reload
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR
from timeit import default_timer as timer

import tkgrig.coneCollision.create as coneCollision_create
reload(coneCollision_create)

maya_version = cmds.about(v=True)

TOOL_VERSION = '1.0.0'
PROJ = 'wizard2'
WINDOW_TITLE = 'Cone Collision'
WINDOW_OPTIONVAR = WINDOW_TITLE.replace(' ', '_')
try:
    DIR_PATH = '/'.join(__file__.replace('\\', '/').split('/')[0:-1])
except:
    DIR_PATH = ''

class ConeCollisionUI(MayaQWidgetDockableMixin, QMainWindow):
    # QMainWindowを継承するとmenubarの使える幅が広い
    def __init__(self, *args, **kwargs):
        super(ConeCollisionUI, self).__init__(*args, **kwargs)
        self.setWindowTitle('{}:{}:{}'.format(WINDOW_TITLE, TOOL_VERSION, PROJ))

        self.presets_items = []
        self.namespaces = ['p1', 'p2']
        self.ref_nss = 'chr'
        self.hips = ['Hip']
        self.L_legs = ['Thigh_L', 'Knee_L']
        self.R_legs = ['Thigh_R', 'Knee_R']
        self.ex_L_legs = []
        self.ex_R_legs = []

        self.get_presets_items()
        self.presets_qcmbox_adds = OrderedDict({
            'Thigh_L':self.ex_L_legs,
            'Thigh_R':self.ex_R_legs
        })

    def layout(self):
        # 全体の大きさの変更
        self.setGeometry(10, 10, 300, 100) # (left, top, width, height)

        self.main_widget = QWidget() # 1
        self.setCentralWidget(self.main_widget)

    def widgets(self):
        self.main_qvbl = QVBoxLayout()
        self.main_widget.setLayout(self.main_qvbl)

        self.main_qhbl = QHBoxLayout()
        self.main_qvbl.addLayout(self.main_qhbl)

        self.angle_obj_qvbl = QVBoxLayout()
        self.main_qhbl.addLayout(self.angle_obj_qvbl)

        # presets
        self.preset_ql = QLabel('Presets')
        self.angle_obj_qvbl.addWidget(self.preset_ql)

        self.preset_qcmbox = QComboBox()
        items = [None]
        [items.append(item) for item in self.presets_qcmbox_adds.keys()]
        self.preset_qcmbox.addItems(items)
        self.angle_obj_qvbl.addWidget(self.preset_qcmbox)

        # Angle Base
        self.angle_base_obj_qhbl = QHBoxLayout()
        self.angle_obj_qvbl.addLayout(self.angle_base_obj_qhbl)
        self.angle_base_obj_ql = QLabel('Angle Base')
        self.angle_base_obj_qhbl.addWidget(self.angle_base_obj_ql)
        self.angle_base_obj_qle = QLineEdit()
        self.angle_base_obj_qhbl.addWidget(self.angle_base_obj_qle)
        self.set_angle_base_obj_btn = QPushButton('<< Set')
        self.angle_base_obj_qhbl.addWidget(self.set_angle_base_obj_btn)

        # angle_base_twist
        self.angle_base_twist_qhbl = QHBoxLayout()
        self.angle_obj_qvbl.addLayout(self.angle_base_twist_qhbl)
        self.angle_base_twist_ql = QLabel('Angle Base Twist Axis')
        self.angle_base_twist_qhbl.addWidget(self.angle_base_twist_ql)
        self.angle_base_twist_qcmbox = QComboBox()
        self.angle_obj_qvbl.addWidget(self.angle_base_twist_qcmbox)
        self.angle_base_twist_qcmbox.addItems(['x', 'y', 'z'])

        # Angle Pose
        self.angle_pose_obj_qhbl = QHBoxLayout()
        self.angle_obj_qvbl.addLayout(self.angle_pose_obj_qhbl)
        self.angle_pose_obj_ql = QLabel('Angle Pose')
        self.angle_pose_obj_qhbl.addWidget(self.angle_pose_obj_ql)
        self.angle_pose_obj_qle = QLineEdit()
        self.angle_pose_obj_qhbl.addWidget(self.angle_pose_obj_qle)
        self.set_angle_pose_obj_btn = QPushButton('<< Set')
        self.angle_pose_obj_qhbl.addWidget(self.set_angle_pose_obj_btn)

        # Center Pose
        self.center_pose_obj_qhbl = QHBoxLayout()
        self.angle_obj_qvbl.addLayout(self.center_pose_obj_qhbl)
        self.center_pose_obj_ql = QLabel('Center Pose')
        self.center_pose_obj_qhbl.addWidget(self.center_pose_obj_ql)
        self.center_pose_obj_qle = QLineEdit()
        self.center_pose_obj_qhbl.addWidget(self.center_pose_obj_qle)
        self.set_center_pose_obj_btn = QPushButton('<< Set')
        self.center_pose_obj_qhbl.addWidget(self.set_center_pose_obj_btn)

        # combo signal
        self.preset_qcmbox.currentTextChanged.connect(partial(self.set_combobox_items,
                                                              self.preset_qcmbox,
                                                              self.angle_base_obj_qle,
                                                              self.angle_pose_obj_qle,
                                                              self.center_pose_obj_qle))

        # QPushButton
        self.create_btn = QPushButton('Create Cone Collision')
        self.create_btn.clicked.connect(partial(self.create_coneCollision_rig))
        self.main_qvbl.addWidget(self.create_btn)

    def buildUI(self):
        # UI
        self.layout()
        self.widgets()

    def get_exist_joints(self, items=None, chr_joints=None):
        exist_jonts = []
        for lj in items:
            for cj in chr_joints:
                if lj in cj:
                    exist_jonts.append(cj)

        return exist_jonts

    def get_presets_items(self):
        chr_joints = []
        for nss in self.namespaces:
            chr_ids = cmds.ls(nss+':'+self.ref_nss+':*', type='joint')
            if chr_ids:
                for jnt in chr_ids:
                    if not jnt in chr_joints:
                        chr_joints.append(jnt)

        # append legs
        ex_L_legs = self.get_exist_joints(self.L_legs, chr_joints)
        ex_R_legs = self.get_exist_joints(self.R_legs, chr_joints)

        [self.ex_L_legs.append(ell) for ell in ex_L_legs]
        [self.ex_R_legs.append(erl) for erl in ex_R_legs]

        self.ex_hips = self.get_exist_joints(self.hips, chr_joints)

        [self.ex_L_legs.append(eh) for eh in self.ex_hips]
        [self.ex_R_legs.append(eh) for eh in self.ex_hips]

        self.presets_items.append(self.ex_L_legs)
        self.presets_items.append(self.ex_R_legs)

    def set_combobox_items(self, combobox=None, base_le=None, pose_le=None, center_le=None, dummy=None):
        cur_text = combobox.currentText() or None
        if cur_text:
            items = self.presets_qcmbox_adds[cur_text]
            base_le.setText(items[0])
            pose_le.setText(items[1])
            center_le.setText(items[2])

    def create_coneCollision_rig(self):
        cmds.undoInfo(openChunk=True)

        angle_base_obj = self.angle_base_obj_qle.text()
        angle_pose_obj = self.angle_pose_obj_qle.text()
        center_pose_obj = self.center_pose_obj_qle.text()
        angle_base_obj_twist_axis = self.angle_base_twist_qcmbox.currentText()

        joints = cmds.ls(os=True)
        if joints:
            try:
                coneCollision_create.create_coneCollision_rig(joints,
                                          angle_base_obj=angle_base_obj,
                                          angle_pose_obj=angle_pose_obj,
                                          center_pose_obj=center_pose_obj,
                                          default_coneAngle=180,
                                          default_target_aim_vec=[0,0,1],
                                          default_target_up_vec=[0,1,0],
                                          angle_base_obj_twist_axis=angle_base_obj_twist_axis)
            except:
                print(traceback.format_exc())

            cmds.select(joints, r=True)

        cmds.undoInfo(closeChunk=True)

if __name__ == '__main__':
    ui = ConeCollisionUI()
    ui.buildUI()
    ui.show(dockable=True)
