# -*- coding: utf-8 -*-
from imp import reload

"""
命名規則によって変更する関数
"""

import TKG.nodes as tkgNodes
reload(tkgNodes)

class NameRegulation:
    """
    name: [prefix, suffix, [replace1, replace2]]
    """
    def __init__(self):
        self.ikHandle = ['', '_IKH', None]
        self.end = ['', '_END', None]
        self.ikSplineCrv = ['', '_CRV', None]
        self.fk = ['', '',['BIND_', 'FK_']]
        self.ik = ['', '',['BIND_', 'IK_']]
        self.sc_ik_dummy = ['SC_IK_', '', None]

        self.dev_000()

    def dev_000(self):
        # 検証用の名前
        self.fk = ['FK_', '', None]
        self.ik = ['IK_', '', None]

name_reg = NameRegulation()

# 
def segment_padding_rename(base=None, num=None, pudding=None, pattern=0):
    """
    0：BIND_ForeArm_L > BIND_ForeArm_00_L
    """
    if pattern == 0:
        bkwd_under = base.split('_')[-2]
        return '{}_{}'.format(bkwd_under, str(num).zfill(pudding)), bkwd_under

def node_type_rename(node=None, type=None):
    if type == 'ikHandle':
        return tkgNodes.rename(node, *name_reg.ikHandle)
    elif type == 'end':
        return tkgNodes.rename(node, *name_reg.end)
    elif type == 'ikSplineCrv':
        return tkgNodes.rename(node, *name_reg.ikSplineCrv)
    elif type == 'fk':
        return name_reg.fk
    elif type == 'ik':
        return name_reg.ik
    elif type == 'sc_ik_dummy':
        return tkgNodes.rename(node, *name_reg.sc_ik_dummy)

def offset_type_rename(node=None, type=None):
    if type:
        return tkgNodes.rename(node, 'OFF_{}_'.format(type), '', None)
    else:
        return tkgNodes.rename(node, 'OFF_', '', None)

def ctrl_type_rename(node=None, type=None):
    if type:
        return tkgNodes.rename(node, 'CTL_{}_'.format(type), '', None)
    else:
        return tkgNodes.rename(node, 'CTL_', '', None)

def shape_type(type=None):
    if type == 'fk':
        return 'cube'
    elif type == 'ikBase':
        return 'round_cube'
    elif type == 'ikMain':
        return 'jack'
    elif type == 'ikPv':
        return 'sphere2'
    elif type == 'scIkPv':
        return 'circle'

def axis_vector(axis):
    axis_dict = {
        'x':[1,0,0],
        'y':[0,1,0],
        'z':[0,0,1],
        '-x':[-1,0,0],
        '-y':[0,-1,0],
        '-z':[0,0,-1]
    }
    return axis_dict[axis]
