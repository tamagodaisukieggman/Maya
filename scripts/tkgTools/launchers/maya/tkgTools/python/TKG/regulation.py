# -*- coding: utf-8 -*-
from imp import reload

"""
命名規則によって変更する関数
"""

import TKG.nodes as tkgNodes
reload(tkgNodes)

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
        return tkgNodes.rename(node, '', '_IKH', None)
    elif type == 'end':
        return tkgNodes.rename(node, '', '_END', None)
    elif type == 'ikSplineCrv':
        return tkgNodes.rename(node, '', '_CRV', None)
    elif type == 'fk':
        return ['', '',['BIND_', 'FK_']]
    elif type == 'ik':
        return ['', '',['BIND_', 'IK_']]

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
