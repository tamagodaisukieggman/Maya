# -*- coding: utf-8 -*-
import re

import maya.cmds as cmds

from . import common

"""
よく使用するスクリプト
# selection
nodes = cmds.ls(os=True, fl=True) or []

"""
# rename
def rename(obj=None, prefix=None, suffix=None, replace=None):
    """
    obj=None, prefix=None, suffix=None, replace=None
    """
    # replace
    replace_name = obj
    if replace:
        replace_name = obj.replace(*replace)

    # prefix
    if not prefix:
        prefix = ''
    prefix_name = re.sub('^', prefix, replace_name)

    # suffix
    if not suffix:
        suffix = ''
    renamed = re.sub('$', suffix, prefix_name)

    return renamed

# virtual rename
def virtual_reames(names=None, p='', s='', r=['', '']):
    """
    仮想のリネームを取得
    """
    return [rename(n, p, s, r) for n in names]

# duplicate
class Duplicate:
    """
    dup = Duplicate(nodes, '', '', ['BIND_', 'IK_'])
    dups = dup.duplicate()
    """
    def __init__(self, nodes=None, prefix=None, suffix=None, replace=None, hierarchy=None):
        if nodes:
            self.nodes = nodes
        else:
            self.nodes = cmds.ls(os=True, fl=True) or []
        self.prefix = prefix
        self.suffix = suffix
        self.replace = replace
        self.hierarchy = hierarchy
        self.virtuals = None

        self.virtual_reames()

    def virtual_reames(self):
        if self.hierarchy:
            self.nodes = cmds.ls(self.nodes, dag=True)

        self.virtuals = virtual_reames(self.nodes,
                              self.prefix,
                              self.suffix,
                              self.replace)

    def duplicate(self):
        if self.hierarchy:
            dups = cmds.duplicate(self.nodes, rc=True)
        else:
            dups = cmds.duplicate(self.nodes, rc=True, po=True)

        return [cmds.rename(d, rslt) for d, rslt in zip(dups, self.virtuals)]

def segment_duplicates(base=None, tip=None, i=2, base_include=None, tip_include=None, children=None):
    """
    baseとtipの間にジョイントを作成する
    例：BIND_ForeArm_L > BIND_ForeArm_00_L
    """
    segments = []
    mps = common.step_positions(nodes=[base, tip],
                                   i=i,
                                   base_include=base_include,
                                   tip_include=tip_include)
    for j in range(i):
        bkwd_under = base.split('_')[-2]
        dup = Duplicate([base], '', '', [bkwd_under, '{}_{}'.format(bkwd_under, str(j).zfill(2))], False)
        dups = dup.duplicate()
        cmds.xform(dups[0], t=mps[j], ws=True, a=True)
        if children:
            cmds.parent(dups[0], base)
        segments.append(dups[0])

    return segments