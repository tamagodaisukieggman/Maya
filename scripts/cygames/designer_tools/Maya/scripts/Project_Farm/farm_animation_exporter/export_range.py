# -*- coding: utf-8 -*-
try:
    # Maya 2022-
    from builtins import zip
    from builtins import object
except:
    pass

import maya.cmds as cmds


class ExportRange(object):
    node_name = 'animationExporterOption'
    attr_name = 'exportRanges'
    variables = [
        {'ln': 'name', 'dt': 'string', 'p': attr_name},
        {'ln': 'start', 'at': 'float', 'p': attr_name},
        {'ln': 'end', 'at': 'float', 'p': attr_name},
    ]

    def __init__(self, name=None, start=None, end=None):
        self.name = name
        self.start = start
        self.end = end

    def get_vars(self):
        return [self.name, self.start, self.end]

    @classmethod
    def get_attr_name(cls):
        return '.'.join([cls.node_name, cls.attr_name])

    @classmethod
    def from_attr(cls, attr, node_name=None):
        node = node_name or cls.node_name

        attrs = ['.'.join([node, attr, v['ln']]) for v in cls.variables]
        types = [v.get('at') or v.get('dt') for v in cls.variables]

        if any(cmds.getAttr(a, typ=True) != t for a, t in zip(attrs, types)):
            return None

        raw = {v['ln']: cmds.getAttr(a) for v, a in zip(cls.variables, attrs)}

        if any(v is None or v == '' for v in list(raw.values())):
            return None

        return cls(**raw)

    @classmethod
    def from_node(cls, node_name=None):
        node = node_name or cls.node_name

        if node not in cmds.ls(typ='script'):
            return None

        attr_list = cmds.listAttr(node)

        if cls.attr_name not in attr_list:
            return None

        attr_names = ('.'.join([v['p'], v['ln']]) for v in cls.variables)

        if not all(n in attr_list for n in attr_names):
            return None

        attrs = cmds.listAttr(node, st=cls.attr_name, m=True)

        if not attrs:
            return None

        raw_ranges = [cls.from_attr(r) for r in attrs]
        ranges = [r for r in raw_ranges if r]

        if not ranges:
            return None

        return ranges

    @classmethod
    def to_attr(cls, attr, r, node_name=None):
        node = node_name or cls.node_name

        for cls_v, inst_v in zip(cls.variables, r.get_vars()):
            a = '.'.join([node, attr, cls_v['ln']])
            typ = cls_v.get('dt')
            if typ:
                cmds.setAttr(a, inst_v, typ=typ)
            else:
                cmds.setAttr(a, inst_v)

    @classmethod
    def to_node(cls, ranges, node_name=None):
        node = node_name or cls.node_name

        cls.init_node(node)

        for i, r in enumerate(ranges):
            attr = cls.attr_name + '[{}]'.format(i)
            cls.to_attr(attr, r)

    @classmethod
    def init_node(cls, node_name=None):
        node = node_name or cls.node_name

        if node not in cmds.ls(typ='script'):
            cmds.scriptNode(n=node)

        attr_list = cmds.listAttr(node)

        if cls.attr_name in attr_list:
            cmds.deleteAttr(node, at=cls.attr_name)

        cmds.addAttr(node, ln=cls.attr_name, at='compound', nc=3, m=True)

        for variable in cls.variables:
            cmds.addAttr(node, **variable)
