# -*- coding: utf-8 -*-
u"""Baseクラス

"""
import os

import maya.cmds as cmds

from mtku.maya.log import MtkDBLog
from mtku.maya.menus.animation.bakesimulation import BakeSimulation


logger = MtkDBLog(__name__)


class BaseConst(object):

    @classmethod
    def get_namespace_from_selection(cls):
        u"""選択しているコントローラーからnamespaceを取得

        :return: namespace
        """
        ctrl_sets = cmds.ls(sl=True, typ='objectSet')
        if not ctrl_sets:
            return

        namespace = ctrl_sets[0].split(':')[0]
        if namespace == ctrl_sets[0]:
            return ''
        else:
            return namespace

    @classmethod
    def create_locator(cls, name, namespace=None):
        u"""locator作成

        :param name: locator名
        :param namespace: ネームスペース
        :return: locator名
        """
        if namespace:
            locator_name = u'{}:{}'.format(namespace, name)
        else:
            locator_name = name

        cmds.spaceLocator(n=locator_name)
        return locator_name

    @classmethod
    def parent(cls, parent_, children, namespace):
        u"""parent

        :param parent_: 親
        :param children: 子 （単数、複数両方可)
        :param namespace: ネームスペース
        :return: 子の名前
        """
        if namespace:
            parent_name = u'{}:{}'.format(namespace, parent_)
            if isinstance(children, str):
                children_names = u'{}:{}'.format(namespace, children)
            else:
                children_names = [u'{}:{}'.format(namespace, c) for c in children]
        else:
            parent_name = parent_
            children_names = children[:]

        children_names = cmds.parent(children_names, parent_name)

        return children_names

    @classmethod
    def _constraint(cls, src, dst, typ):
        u"""コンストレイン

        :param src: source
        :param dst: destination
        :param typ: 'point', 'orient'
        """
        if typ == 'point':
            cmds.pointConstraint(src, dst)
        elif typ == 'orient':
            cmds.orientConstraint(src, dst)

    @classmethod
    def constraint(cls, src, dst, types, namespace=None):
        u"""コンストレイン

        :param src: source
        :param dst: destination
        :param types: コンストレインのタイプ ex) ('point', 'orient')
        :param namespace: ネームスペース
        """
        if namespace:
            for typ in types:
                cls._constraint(u'{}:{}'.format(namespace, src), u'{}:{}'.format(namespace, dst), typ)
        else:
            for typ in types:
                cls._constraint(src, dst, typ)

    @classmethod
    def bake(cls, root_nodes, namespace=None):
        u"""Bake

        :param root_nodes: ルートノードのリスト
        :param namespace: ネームスペース
        """
        if namespace:
            if isinstance(root_nodes, str):
                root_names = u'{}:{}'.format(namespace, root_nodes)
            else:
                root_names = [u'{}:{}'.format(namespace, n) for n in root_nodes]
        else:
            root_names = root_nodes[:]

        # Bake
        # BakeSimulation.bake(root_names, attrs=('tx', 'ty', 'tz', 'rx', 'ry', 'rz'))
        BakeSimulation.bake(root_names)

        # constraintノードの削除
        point_constraints = cmds.ls(root_names, dag=True, typ='pointConstraint')
        orient_constraints = cmds.ls(root_names, dag=True, typ='orientConstraint')

        if point_constraints:
            cmds.delete(point_constraints)
        if orient_constraints:
            cmds.delete(orient_constraints)

    @classmethod
    def hide(cls, node, namespace=None):
        u"""非表示

        :param node: ノード名
        :param namespace: ネームスペース
        """
        if namespace:
            name = u'{}:{}'.format(namespace, node)
        else:
            name = node

        cmds.setAttr(u'{}.visibility'.format(name), False)
