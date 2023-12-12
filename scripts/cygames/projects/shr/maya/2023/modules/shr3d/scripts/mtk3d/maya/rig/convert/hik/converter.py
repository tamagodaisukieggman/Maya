# -*- coding: utf-8 -*-
from maya import cmds, mel

from mtk3d.maya.rig.convert.hik import common as hik_common
reload(hik_common)

class ConvertMVN(object):

    def __init__(self, sourceChara='mvn_00', destinationChara='ply00_m_000', sourceCharaRootJoint='Reference', destinationCharaRootJoint='root_jnt',
                 ctrlsSets=['ply00_m_000_000:ctrls_sets'], destinationFilePath=None, connectFilePath=None):

        self.sourceChara = sourceChara
        self.sourceCharaRootJoint = sourceCharaRootJoint

        self.destinationChara = destinationChara
        self.destinationCharaRootJoint = destinationCharaRootJoint

        self.ctrlsSets = ctrlsSets

        self.destinationFilePath = destinationFilePath
        self.connectFilePath = connectFilePath

    def convert(self):
        hik_common.hik_define(character1=self.destinationChara,
                              character2=self.sourceChara,
                              character1_root_joint=self.destinationCharaRootJoint,
                              character2_root_joint=self.sourceCharaRootJoint)

        cmds.select(self.ctrlsSets, r=1, ne=1)
        ctrls = cmds.pickWalk(d='down')
        # file_path = 'C:/Users/shunsuke/Documents/maya/scripts/tkgTools/tkgRig/scripts/convert/hik/data/characters/ply00_m_000/ply00_m_000_ctrls.json'
        hik_common.objectValues(joints=ctrls, export_or_import='import', fix=True, file_path=self.destinationFilePath, namespace=None)

        cConst = hik_common.ConstraintList()
        # cConst.constraint(file_path='C:/Users/shunsuke/Documents/maya/scripts/tkgTools/tkgRig/scripts/convert/hik/data/characters/ply00_m_000/ply00_m_000_connect_ctrls.json')
        cConst.constraint(file_path=self.connectFilePath)
