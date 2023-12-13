# -*- coding: utf-8 -*-
try:
    import maya.cmds as cmds
    import pymel.core as pm
except:
    pass

from workfile_manager.plugin_utils import Application, PluginType
from workfile_manager_maya.export.preproc.preproc_maya_base import MayaPreprocBase

class Plugin(MayaPreprocBase, object):
    def apps_executable_on(self):
        return (
            Application.Maya,
        )

    def is_asset_eligible(self, asset):
        if asset.task == 'model':
            return True
        else:
            return False

    def init(self):
        super(Plugin, self).init()
        self.max_inf = 4

    def execute(self, args):
        meshes = cmds.ls(type='mesh')
        weights = []
        res = []
        for m in meshes:
            skin_cluster = self._get_skincluster(m)
            if skin_cluster is None:
                continue
            infs = cmds.skinCluster(skin_cluster, q=True, inf=True)
            nvtx = cmds.polyEvaluate(m, v=True)
            for k in range(nvtx):
                vtx = m + '.vtx[%d]' % k
                weights = self._get_weights(skin_cluster, vtx, infs)
                if len(weights) > self.max_inf:
                    res.append(vtx)

        if len(res) > 0:
            buf = cmds.ls(sl=True)
            cmds.select(res)
            self.results = cmds.ls(selection=1)
            if buf is not None and len(buf):
                cmds.select(buf)
            return False, self.results
        else:
            return True, None

    def getlabel(self):
        return 'Check max influences'

    def get_label_jp(self):
        return u'max influences‚ÌŠm”F'

    def order(self):
        return 100000

    def _get_skincluster(self, mesh):
        buf = cmds.listHistory(mesh)
        for h in buf:
            if cmds.objectType(h, isType='skinCluster'):
                return h
        return None

    def _get_weights(self, skin_cluster, vtx, infs):
        weights = {}
        for inf in infs:
            weight = cmds.skinPercent(skin_cluster, vtx, transform=inf, q=True)
            if weight > 0.0 and weight is not None:
                weights[inf] = weight
        return weights