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
    elif type == 'End':
        return tkgNodes.rename(node, '', '_END', None)