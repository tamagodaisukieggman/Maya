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
        self.blend = ['', '',['BIND_', 'BLEND_']]
        self.sc_ik_dummy = ['SC_IK_', '', None]
        self.bendy_limb = ['', '', ['BIND_', 'BENDY_LIMB_']]
        self.ribbon = ['', '', ['BIND_', 'RIBBON_']]
        self.start = ['START_', '', None]
        self.end = ['END_', '', None]

        # module parts
        self.nodes_top = ['NODES_', '', None]
        self.ctrls_top = ['CTRLS_', '', None]

        # utility node
        self.distanceBetween = ['', '_DBN', None]
        self.curveInfo = ['', '_CRVINFO', None]
        self.multiplyDivide = ['', '_MD', None]
        self.condition = ['', '_CDN', None]
        self.pairBlend = ['', '_PBN', None]
        self.plusMinusAverage = ['', '_PMA', None]
        self.multDoubleLinear = ['', '_MDL', None]
        self.addDoubleLinear = ['', '_ADL', None]
        self.controller = ['', '_CTRLER', None]

        # absolute name
        self.controller_node_sets = 'CTRLER_NODE_SETS'

        self.dev_000()

    def dev_000(self):
        # 検証用の名前
        self.fk = ['FK_', '', None]
        self.ik = ['IK_', '', None]
        self.blend = ['BLEND_', '', None]
        self.bendy_limb = ['BENDY_LIMB_', '', None]
        self.ribbon = ['RIBBON_', '', None]

name_reg = NameRegulation()

class NumRegulation:
    def __init__(self):
        self.bendy_limb_num = 5
        self.ribbon_num = 3

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
    elif type == 'blend':
        return name_reg.blend
    elif type == 'sc_ik_dummy':
        return tkgNodes.rename(node, *name_reg.sc_ik_dummy)
    elif type == 'bendy_limb':
        return tkgNodes.rename(node, *name_reg.bendy_limb)
    elif type == 'ribbon':
        return tkgNodes.rename(node, *name_reg.ribbon)
    elif type == 'start':
        return tkgNodes.rename(node, *name_reg.start)
    elif type == 'end':
        return tkgNodes.rename(node, *name_reg.end)

    # module parts
    elif type == 'nodes_top':
        return tkgNodes.rename(node, *name_reg.nodes_top)
    elif type == 'ctrls_top':
        return tkgNodes.rename(node, *name_reg.ctrls_top)

    # utility node
    elif type == 'distanceBetween':
        return tkgNodes.rename(node, *name_reg.distanceBetween)
    elif type == 'curveInfo':
        return tkgNodes.rename(node, *name_reg.curveInfo)
    elif type == 'multiplyDivide':
        return tkgNodes.rename(node, *name_reg.multiplyDivide)
    elif type == 'condition':
        return tkgNodes.rename(node, *name_reg.condition)
    elif type == 'pairBlend':
        return tkgNodes.rename(node, *name_reg.pairBlend)
    elif type == 'plusMinusAverage':
        return tkgNodes.rename(node, *name_reg.plusMinusAverage)
    elif type == 'multDoubleLinear':
        return tkgNodes.rename(node, *name_reg.multDoubleLinear)
    elif type == 'addDoubleLinear':
        return tkgNodes.rename(node, *name_reg.addDoubleLinear)
    elif type == 'controller':
        return tkgNodes.rename(node, *name_reg.controller)

def absolute_name(type=None):
    if type == 'controller_node_sets':
        return name_reg.controller_node_sets

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
        return 'pacman'
    elif type == 'bendy_limb':
        return 'circle'
    elif type == 'bendy_limb_main':
        return 'drop'

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
