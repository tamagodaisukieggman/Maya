# -*- coding=utf-8 -*-
from __future__ import division
from __future__ import print_function

u"""
name: autocreate_rig/constant.py
data: 2021/8/31
ussage: priari 用 Rig 自動作成ツールの定数
version: 2.5
​
"""

try:
    # Maya 2022-
    from builtins import str
    from builtins import object
except:
    pass

from collections import OrderedDict
import maya.api.OpenMaya as om
import maya.cmds as cmds
import pymel.core as pm
import os
import traceback
import re
import math
from . import const

from logging import getLogger

logger = getLogger(__name__)


class Utils(object):

    @classmethod
    def print_info(cls, text, node=None):
        u"""
            print info
            :param str text :
            :param str node :
        """
        line = u'-' * 100
        info_text = u'{} : {}'.format(text, node) if node else u'{}'.format(text)

        print("{0}\n{1}\n{0}".format(line, info_text))

    @classmethod
    def get_label(cls, name):
        u"""
            名前の中からラベルを取得
            :param name:　str or PyNode
            :return: ラベル
        """
        if isinstance(name, pm.PyNode):
            name = name.stripNamespace().nodeName()

        if len(name.rsplit('|')) > 1:
            s_name = name.rsplit('|', 1)[1]
        else:
            s_name = name
        return re.search('[^0-9_A-Z]+[a-z]', s_name).group()

    @classmethod
    def get_name(cls, name):
        u"""
            名前の中から種別名を取得
            :param name:
            :return: 種別名
        """

        if name is None:
            return None

        if isinstance(name, pm.PyNode):
            name = name.stripNamespace().nodeName()

        if len(name.rsplit('|')) > 1:
            s_name = name.rsplit('|', 1)[1]
        else:
            s_name = name

        return s_name

    @classmethod
    def get_length(cls, s_srt, p_srt):
        u"""
            2点間の距離を測る
            :param s_srt:
            :param p_srt:
            :return: 距離
        """
        x2 = (p_srt[0] - s_srt[0]) * (p_srt[0] - s_srt[0])
        y2 = (p_srt[1] - s_srt[1]) * (p_srt[1] - s_srt[1])
        z2 = (p_srt[2] - s_srt[2]) * (p_srt[2] - s_srt[2])

        length = math.sqrt(x2 + y2 + z2)
        return length

    @classmethod
    def get_angle(cls, v1, v2):
        u"""
            2つのベクトルから角度を角度を取得
            :param v1:
            :param v2:
            :return: 距離
        """
        u = (v2[0] * v1[0]) + (v2[1] * v1[1]) + (v2[2] * v1[2])
        l = math.sqrt((v2[0] * v2[0]) + (v2[1] * v2[1]) + (v2[2] * v2[2]))
        r = math.sqrt((v1[0] * v1[0]) + (v1[1] * v1[1]) + (v1[2] * v1[2]))
        angle = 0
        if l != 0 and r != 0:
            angle = int(u / (l * r))
        return angle

    @classmethod
    def get_namespace(cls, node):
        u"""
            ノード名からネームスペース取得
            :param node: str or PyNode
            :return: ネームスペース
        """
        ns = ""
        if node is None:
            return ns

        # if string, convert to PyNode
        if isinstance(node, str):
            print((node, type(node)))
            node = pm.PyNode(node)
        # string node must use "referenceQuery"
        if pm.referenceQuery(node, isNodeReferenced = True):
            ns = node.namespace()
        #    ref_file = pm.referenceQuery(node, f=True)
        #    rn = pm.referenceQuery(ref_file, referenceNode=True)
        #    ns = rn.replace("RN", ":")'''

        return ns

    @classmethod
    def get_wire(cls, filepath=const.FILE_PATH):
        """
            wireファイルをインポート、wireグループを返す
            :param filepath: string
            :return: PyNode
        """
        wire_grp = None
        file_path = os.path.join(os.path.dirname(__file__), filepath)
        if os.path.exists(file_path):
            wire_grps = pm.ls('|wire_group*')
            if wire_grps:
                logger.warning(u'シーン内にテンプレートファイルが見つかりました。更新のために削除します。')
                pm.delete(wire_grps, hi=True)

            logger.info(u'テンプレートファイルの読み込み')
            cmds.file(file_path, i = True, type = 'mayaBinary', mergeNamespacesOnClash = True, namespace = ':')
            wire_grp = pm.ls('|wire_group*')[0] if pm.ls('|wire_group*') else None
        else:
            logger.error(u'テンプレートファイルが見つかりません。パスを確認してください。')

        return wire_grp

    @classmethod
    def get_pynode(cls, grp, name, dict={}):
        u"""
            指定名(grp)ノード以下からname名のノードを取得
            dictの指定があれば、　{name:PyNode} でdict情報更新
            :param grp:　PyNode
            :param name: str
            :param dict: dict
            :return: PyNode
        """
        pynode = None
        # ns = Utils.get_namespace(grp)
        pynodes = pm.ls(name)

        if not isinstance(grp, pm.PyNode):
            return None
        grp_longname = grp.longName()
        if len(pynodes) > 0:
            for node in pynodes:
                longname = str(node.longName())
                if longname.startswith(grp_longname):
                    pynode = node

        if dict and pynode:
            dict[name] = pynode

        return pynode

    @classmethod
    def get_pynodes(cls, grp=None, pattern="", dag=True, type="transform"):
        u"""
            指定名(grp)ノード以下から正規表現でPyNodeノードリストを取得
            :param grp:　PyNode
            :param pattern: str  例 r"^(.*)\|(wpn[0-9])\|(grp_mesh[0-9])$"
            :return: list of PyNode or None
        """
        kwargs = dict(dag = dag, type = type)

        # ns = Utils.get_namespace(grp)
        if not isinstance(grp, pm.PyNode):
            return None

        if grp is None:
            pynodes = pm.ls(**kwargs)
        else:
            pynodes = pm.ls(grp, **kwargs)

        if isinstance(pattern, str):
            pynodes = [pn for pn in pynodes if re.match(pattern, str(pn.longName()))]

        return pynodes

    @classmethod
    def get_pyjoints(cls, root):
        u"""
            root以下のPyNodeジョイントリスト取得
            :param root:　PyNode
            :return: list of PyNode
        """
        pm.select(root, hi=True)
        pn_list = pm.ls(sl=True, typ=['joint'], o=True, nt=False, l=True)
        pm.select(cl=True)

        return pn_list

    @classmethod
    def get_dg_node(cls, nodes=None, direction=None, node_types=None):
        '''
            関連するdgノードリストの取得
            :param nodes:　list of str
            :param direction:　om.MItDependencyGraph.kUpstream
            :param node_types:　[om.MFn.kMultiplyDivide, om.MFn.kCondition, om.MFn.kReverse]
            :return: list of nodes
        '''
        if nodes is None or not nodes:
            return

        # TODO: ノード接続構成によっては遅い場合があるので、良い取得方法があれば検討
        if direction is None:
            directions = [om.MItDependencyGraph.kUpstream, om.MItDependencyGraph.kDownstream]  # kUpstream, kDownstream
        if node_types is None:
            nodetypes = [om.MFn.kMultiplyDivide, om.MFn.kCondition, om.MFn.kReverse]  # condition, multipleDivide, reverse

        cmds.select(nodes, hi = True)
        cmds.ls(nodes, dag = 1, s = 1, l = 1)
        sel_list = om.MGlobal.getActiveSelectionList()

        # Create a selection list iterator for what we picked:
        nodes = []
        mit_sel_list = om.MItSelectionList(sel_list)
        while not mit_sel_list.isDone():
            dg_node = mit_sel_list.getDependNode()
            for direction in directions:
                mItDependencyGraph = om.MItDependencyGraph(dg_node, om.MFn.kInvalid, direction)
                while not mItDependencyGraph.isDone():
                    node = mItDependencyGraph.currentNode()
                    dep_node = om.MFnDependencyNode(node)
                    # See if the current item is an animCurve:
                    for mfn_type in nodetypes:
                        if node.hasFn(mfn_type):
                            name = dep_node.name()
                            nodes.append(name)
                            break
                    next(mItDependencyGraph)
            next(mit_sel_list)

        nodes = list(set(nodes))
        cmds.select(d = True)

        return nodes

    @classmethod
    def reorder_outliner(node_list):
        u"""
            ノードリストから直下のノードのアウトライナー順番をソート順に変更
            :param node_list: list of PyNode
        """
        if node_list is None:
            node_list = pm.selected()

        for node in node_list:
            print((node, isinstance(node, pm.PyNode)))
            for each in sorted(node.getChildren()):
                pm.reorder(each, back = True)

    @classmethod
    def create_wire(name, type='unique', grp=None, parent=None, radius=None):
        u"""
        ワイヤーノード作成
        :param str name: 名前
        :param str type: 種類
        :param PyNode grp: wireノードを含むグループ
        :param PyNode parent: 階層下対象の親を指定
        :param float radius: コントローラーの大きさ
        :return null, ctrl: PyNode, PyNode

        """
        if grp is None or not isinstance(grp, pm.PyNode):
            return

        if name is None or name == "":
            name = type
        elif isinstance(name, str):
            name = name
        else:
            pass

        if type == 'oct':
            node = Utils.get_pynode(grp, const.WIRE_TYPE["OCTAHEDRON"])
        elif type == 'root':
            node = Utils.get_pynode(grp, const.WIRE_TYPE["ROOT"])
        elif type == 'ikfk':
            node = Utils.get_pynode(grp, const.WIRE_TYPE["IKFK"])
        elif type == 'pin':
            node = Utils.get_pynode(grp, const.WIRE_TYPE["PIN"])
        elif type == 'h_cross':
            node = Utils.get_pynode(grp, const.WIRE_TYPE["H_CROSS"])
        elif type == 'v_cross':
            node = Utils.get_pynode(grp, const.WIRE_TYPE["V_CROSS"])
        elif type == 'cube':
            node = Utils.get_pynode(grp, const.WIRE_TYPE["CUBE"])
        elif type == 'unique':
            node = Utils.get_pynode(grp, name[2:] + '_wire')
            if node is None:
                if 'tail' in name[2:]:
                    node = Utils.get_pynode(grp, const.WIRE_TYPE["TAIL"])
                else:
                    node = Utils.get_pynode(grp, const.WIRE_TYPE["CUBE"])
        elif type == 'wpn':
            node = Utils.get_pynode(grp, name + '_wire')
            node = node if node else Utils.get_pynode(grp, const.WIRE_TYPE["CUBE"])
        elif type == 'sphere':
            node = Utils.get_pynode(grp, const.WIRE_TYPE["SPHERE"])
        else:
            node = Utils.get_pynode(grp, const.WIRE_TYPE["SPHERE"])

        name = name + const.SUFFIX_CTRL

        # 保存しているWireに不要な値が入っていることがある為、リセット
        pm.setAttr('{}.rotate'.format(node), *[0, 0, 0], type="double3")
        pm.setAttr('{}.scale'.format(node), *[1, 1, 1], type="double3")
        dup_node = pm.duplicate(node, rc=False, n=name)[0]

        # need to rename for dupricate names
        dup_node.rename(name)
        # set radius for shape
        if radius and isinstance(radius, float):
            pm.setAttr('{}.scale'.format(dup_node), *[radius, radius, radius], type="double3")
            pm.makeIdentity(dup_node, apply=True, t=0, r=0, s=1, n=0, pn=0, jointOrient=0)

        return dup_node


# class
class Wire(object):
    u"""
    ワイヤー作成クラス TODO 内包ノードのチェック

    """
    def __init__(self, wire_grp=None):
        if wire_grp is None or not isinstance(wire_grp, pm.PyNode):
            return
        self.wire_grp = wire_grp

    def create(self, name=None, type='unique', parent=None):
        u"""
        ワイヤーノード作成クラス
        :param str name: 名前

        """
        if name is None or name == "":
            name = type
        elif isinstance(name, str):
            name = name
        else:
            pass

        if type == 'oct':
            node = Utils.get_pynode(self.wire_grp, const.WIRE_TYPE["OCTAHEDRON"])
        elif type == 'root':
            node = Utils.get_pynode(self.wire_grp, const.WIRE_TYPE["ROOT"])
        elif type == 'ikfk':
            node = Utils.get_pynode(self.wire_grp, const.WIRE_TYPE["IKFK"])
        elif type == 'pin':
            node = Utils.get_pynode(self.wire_grp, const.WIRE_TYPE["PIN"])
        elif type == 'h_cross':
            node = Utils.get_pynode(self.wire_grp, const.WIRE_TYPE["H_CROSS"])
        elif type == 'v_cross':
            node = Utils.get_pynode(self.wire_grp, const.WIRE_TYPE["V_CROSS"])
        elif type == 'cube':
            node = Utils.get_pynode(self.wire_grp, const.WIRE_TYPE["CUBE"])
        elif type == 'unique':
            node = Utils.get_pynode(self.wire_grp, name[2:] + '_wire')
            if node is None:
                if 'tail' in name[2:]:
                    node = Utils.get_pynode(self.wire_grp, const.WIRE_TYPE["TAIL"])
                else:
                    node = Utils.get_pynode(self.wire_grp, const.WIRE_TYPE["CUBE"])
        elif type == 'wpn':
            node = Utils.get_pynode(self.wire_grp, name + '_wire')
            node = node if node else Utils.get_pynode(self.wire_grp, const.WIRE_TYPE["CUBE"])

        name = name + const.SUFFIX_CTRL
        # check node name Exists
        exists_node = Utils.get_pynode(self.wire_grp, name)
        if exists_node:
            pm.delete(exists_node)

        return pm.duplicate(node, rc=False, n=name)[0]

