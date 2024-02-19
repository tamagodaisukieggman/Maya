# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.mel as mel
from imp import reload
import traceback

import buildRig.common as brCommon
import buildRig.ik as brIk
reload(brCommon)
reload(brIk)

# 引数の確認
brCommon.get_args_and_defaults(brIk.Ik, False)

"""
self.solvers = {
    0: 'ikSCsolver',
    1: 'ikRPsolver',
    2: 'ikSplineSolver',
    3: 'ikSpringSolver'
}
"""

"""
# 3ジョイントを選択してIKコントローラを作成する
# ikRPsolver
kwargs = {'dForwardAxis': 'x',
 'dWorldUpAxis': 'z',
 'ik_base_axis': [0, 0, 0],
 'ik_base_scale': 5,
 'ik_base_shape': 'cube',
 'ik_local_axis': [0, 0, 0],
 'ik_local_scale': 5,
 'ik_local_shape': 'cube',
 'ik_main_axis': [0, 0, 0],
 'ik_main_scale': 5,
 'ik_main_shape': 'jack',
 'ik_pv_axis': [0, 0, 0],
 'ik_pv_scale': 5,
 'ik_pv_shape': 'locator_3d',
 'joints': cmds.ls(os=True, type='joint'),
 'module': None,
 'rig_ctrls_parent': None,
 'rig_joints_parent': None,
 'roll_fk_axis': 'z',
 'roll_fk_ctrl_axis': [0, 90, 0],
 'side': None,
 'softik': None,
 'solver': 1,
 'stretchy_axis': 'x'}

try:
    ik = brIk.Ik(**kwargs)

except:
    print(traceback.format_exc())

ik.base_connection()
"""

# spineのIKを作成する
# dForwardAxisはTwist Axis
# dWorldUpAxisは基本dForwardAxis以外のPositive軸でいい
kwargs = {'dForwardAxis': 'x',
 'dWorldUpAxis': 'z',
 'ik_base_axis': [0, 0, 0],
 'ik_base_scale': 5,
 'ik_base_shape': 'cube',
 'ik_local_axis': [0, 0, 0],
 'ik_local_scale': 5,
 'ik_local_shape': 'cube',
 'ik_main_axis': [0, 0, 0],
 'ik_main_scale': 5,
 'ik_main_shape': 'jack',
 'ik_pv_axis': [0, 0, 0],
 'ik_pv_scale': 5,
 'ik_pv_shape': 'locator_3d',
 'joints': cmds.ls(os=True, type='joint'),
 'module': None,
 'rig_ctrls_parent': None,
 'rig_joints_parent': None,
 'roll_fk_axis': 'x',
 'roll_fk_ctrl_axis': [0, 90, 0],
 'side': None,
 'softik': None,
 'solver': 2,
 'stretchy_axis': 'x'}

try:
    ik = brIk.Ik(**kwargs)

except:
    print(traceback.format_exc())

ik.base_connection()

# WingA
sel = cmds.ls(os=True, type='joint')
try:
    ik = brIk.Ik(module=None,
                 side=None,
                 rig_joints_parent=None,
                 rig_ctrls_parent=None,
                 joints=sel,
                 ik_base_shape='cube',
                 ik_base_axis=[0,0,0],
                 ik_base_scale=1000,
                 ik_main_shape='jack',
                 ik_main_axis=[0,0,0],
                 ik_main_scale=1000,
                 ik_pv_shape='locator_3d',
                 ik_pv_axis=[0,0,0],
                 ik_pv_scale=1000,
                 ik_local_shape='cube',
                 ik_local_axis=[0,0,0],
                 ik_local_scale=1000,
                 stretchy_axis='x',
                 solver=2,
                 dForwardAxis='x',
                 dWorldUpAxis='y',
                 roll_fk_axis='x',
                 roll_fk_ctrl_axis=[0,0,0])

except:
    print(traceback.format_exc())

ik.base_connection()
