# -*- coding: utf-8 -*-

# ---------------------------------------------
# ======= author : honda_satoshi
#                  yoshida_yutaka
# ---------------------------------------------

import maya.OpenMaya as om
import maya.api.OpenMaya as om2
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mm

import math

from .. import myUtilities as utils
reload(utils)

mu = utils.MyUtilities()



# honda ---------------------------------------------------------------------------------------

def rebuild_curve_by_length(crvs=None, interval=1):
    """カーブをリビルド
    param list crvs: カーブオブジェクト
    param float interval: spanの大体の長さ
    """
    crvs = crvs or cmds.ls(sl=True)
    if not crvs:
        cmds.warning(u'カーブを選択して下さい。')
        return

    for crv in crvs:
        crv_sh = cmds.listRelatives(crv, s=True, ni=True, type='nurbsCurve')
        if not crv_sh:
            continue

        degree = cmds.getAttr('{}.degree'.format(crv_sh[0]))
        length = cmds.arclen(crv, ch=False)
        span = math.ceil(length / interval)
        cmds.rebuildCurve(crv, ch=False, rpo=True, rt=0, end=1, kr=2, kcp=0, kep=0, kt=0, s=span, d=degree, tol=0.01)

    cmds.select(crvs, r=True)



#----------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------

# yoshida -------------------------------------------------------------------------------------

class DynamicSplineIK():
    def __init__(self):
        self.sel = []
        self.solver = []
        self.ikCBGP = []
        self.ikCCGP = []
        self.ikCGP = []
        self.ikSG = []
        self.name = []
        self.hsGP = []
        self.ikGP = []
        self.ikSGP = []


    # ciks +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def _ciks_createIKSpline(self, tgt, name):
        sel = tgt or pm.selected()
        ctrlCrvs = []

        for obj in sel:
            children = pm.listRelatives(obj, ad=1, type='joint')
            src = obj
            tgt = children[0]
            num = len(children) * 6

            iK = pm.ikHandle(sj=src, ee=tgt, sol='ikSplineSolver', ns=num, n='{}_ikSpline'.format(src))
            rebuild_curve_by_length(crvs=cmds.ls(str(iK[-1])), interval=0.5)
            pm.bakePartialHistory(iK[-1], q=1, ppt=1)

            pm.rename(iK[1], '{}_effector'.format(iK[0]))
            pm.rename(iK[-1], '{}_ik_curve'.format(iK[0]))

            ctrlCrv = pm.duplicate(iK[-1], n='{}_ctrl_curve'.format(iK[0]))
            rebuild_curve_by_length(crvs=cmds.ls(str(ctrlCrv[0])), interval=3)
            mu._cleanupMeshes(cln=ctrlCrv, bor=0)

            self._ciks_makeHierarchy(iK, ctrlCrv, name)

            ctrlCrvs.append(ctrlCrv)

        return ctrlCrvs


    def _ciks_makeHierarchy(self, iK, ctrlCrv, name):
        if pm.objExists('{}_ik_GP'.format(name)):
            ikHGP = pm.PyNode('{}_ikSystem_GP'.format(name))
            self.ikCCGP = pm.PyNode('{}_ikCtrlCrv_GP'.format(name))
            self.ikCBGP = pm.PyNode('{}_ikCtrlCrvBase_GP'.format(name))
            self.hsGP = pm.PyNode('hariSystem_{}_GP'.format(name))
            self.ikGP = pm.PyNode('{}_ik_GP'.format(name))
            pm.parent(self.ikCBGP, w=1)
            pm.parent(iK[0], iK[-1], ikHGP)
            pm.parent(ctrlCrv, self.ikCCGP)

        else:
            ikHGP = pm.group(iK[0], iK[-1], n='{}_ikSystem_GP'.format(name))
            self.ikCBGP = pm.group(em=1, n='{}_ikCtrlCrvBase_GP'.format(name))
            self.ikCCGP = pm.group(ctrlCrv, n='{}_ikCtrlCrv_GP'.format(name))
            self.ikCGP = pm.group(self.ikCCGP, n='{}_ikCrv_GP'.format(name))
            self.hsGP = pm.group(em=1, n='hariSystem_{}_GP'.format(name))
            self.ikGP = pm.group(ikHGP, n='{}_ik_GP'.format(name))

        if pm.objExists('ikDynamicSpline_GP'):
            self.ikSGP = pm.PyNode('ikDynamicSpline_GP')
        else:
            self.ikSGP = pm.group(em=1, n='ikDynamicSpline_GP')

        pm.hide(ikHGP)


    def _ciks_activeNucleus(self, solver=""):
        self.solver = pm.ls(solver)
        if not self.solver:
            mm.eval('$gActiveNucleusNode = "";')
        else:
            mm.eval('$gActiveNucleusNode = "{}";'.format(solver))


    def _ciks_createDynamicCurve(self, ctrlCrvs, name):
        pm.select(ctrlCrvs)
        mm.eval('makeCurvesDynamic 2 { "0", "0", "1", "1", "0"};')
        outCrv = []
        folShape = []

        for crv in ctrlCrvs:
            crvName = crv[0].replace("_ctrl_curve", "")

            fol = pm.listRelatives(crv, p=1)
            folShape = pm.listRelatives(fol, s=1, ni=1)
            outCrv = pm.listConnections(folShape, t='nurbsCurve')

            pm.rename(fol, '{}_follicle'.format(crvName))
            pm.rename(outCrv[-1], '{}_outCurve'.format(crvName))

            pm.wire(crv[0].replace("ctrl", "ik"), w=outCrv[-1], gw=False, en=1.000000, ce=0.000000, li=0.000000, dds=[0,100000])
            wp = pm.listHistory(crv[0].replace("ctrl", "ik"), type='wire')
            pm.rename(wp, '{}_wire'.format(crv[0]))

            pm.hide(crv)
            pm.parent(outCrv[-1]+ "BaseWire", self.ikCBGP)

        hSys = pm.listConnections(folShape, t='hairSystem')
        hOutGP = pm.listRelatives(outCrv[-1], p=1)
        nuc = pm.listHistory(hSys[0], type='nucleus')

        pm.rename(hSys[0], 'hairSystem_{}'.format(name))
        pm.rename(hOutGP, '{}_outputCurves'.format(hSys[0]))

        pm.parent(hSys[0], self.hsGP)
        pm.parent(self.ikCBGP, self.ikCCGP)
        pm.parent(hOutGP, self.ikCGP)
        pm.parent(self.hsGP, self.ikCGP)
        pm.parent(self.hsGP, self.ikCGP, self.ikGP)

        if not self.solver:
            pm.parent(nuc, self.ikGP, self.ikSGP)
        else:
            pm.parent(self.ikGP, self.ikSGP)


    def _ciks_main(self, solver="", name="jtHair"):
        tgt = mu._checkObj(typ='joint') or []
        if tgt:
            ctrlCrvs = self._ciks_createIKSpline(tgt, name)
            self._ciks_activeNucleus(solver)
            self._ciks_createDynamicCurve(ctrlCrvs, name)


    # ciks +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#hu = HairUtilities()
