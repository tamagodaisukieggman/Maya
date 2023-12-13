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

from functools import partial
import math

class MyUtilities():
    def __init__(self):
        self.sel = []


    #----------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------
    # Utilities
    #----------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------

    # honda ---------------------------------------------------------------------------------------

    @staticmethod
    def clamp(value, min_value=0.0, max_value=1.0):
        return max(min_value, min(max_value, value))


    def calc_thickness_values(self, node, scale=1.0):
        dag_path = om2.MGlobal.getSelectionListByName(node).getDagPath(0)
        mesh_fn = om2.MFnMesh(dag_path)
        iter = om2.MItMeshVertex(dag_path)
        edge_iter = om2.MItMeshEdge(dag_path)

        ave_length_per_vtx = [0.0] * mesh_fn.numVertices
        all_edge_length_list = [1.0] * mesh_fn.numEdges

        while not iter.isDone():
            edges = iter.getConnectedEdges()
            edge_length_list = []
            for edge in edges:
                edge_iter.setIndex(edge)
                length = edge_iter.length()
                all_edge_length_list[edge] = length
                edge_length_list.append(length)

            # エッジ平均合わせ
            # ave_length_per_vtx[iter.index()] = sum(edge_length_list) / len(edge_length_list)

            # 最短エッジ合わせ
            # ave_length_per_vtx[iter.index()] = min(edge_length_list)

            # 最長エッジ合わせ
            ave_length_per_vtx[iter.index()] = max(edge_length_list)

            iter.next()

        max_length = max(all_edge_length_list)
        for v_index in range(mesh_fn.numVertices):
            ave_length_per_vtx[v_index] = self.clamp(ave_length_per_vtx[v_index] / max_length, 0.0, 1.0) * scale

        return ave_length_per_vtx, max_length


    def set_thickness_values(self, node, scale=1.0):
        if not cmds.objExists(node):
            cmds.warning('\'{}\' is not found.'.format(node))
            return

        shapes = cmds.listRelatives(node, s=True, ni=True, pa=True, typ='mesh')
        if not shapes:
            cmds.warning('Not found mesh node.')
            return

        ncloth = cmds.listConnections(shapes, s=True, d=False, sh=True, type='nCloth')
        if not ncloth:
            cmds.warning('Not found related nCloth node.')
            return

        ncloth = ncloth[0]
        thickness_values, max_edge_length = self.calc_thickness_values(node, scale=scale)

        thickness = cmds.getAttr('{}.thickness'.format(ncloth))
        max_thickness_value = max(thickness_values)
        self_collide_scale = max_edge_length * 0.5 / (thickness * max_thickness_value)

        cmds.setAttr('{}.selfCollideWidthScale'.format(ncloth), self_collide_scale)
        cmds.setAttr('{}.thicknessMapType'.format(ncloth), 1)
        cmds.setAttr('{}.thicknessPerVertex'.format(ncloth), thickness_values, type='doubleArray')


    def rebuild_curve_by_length(self, crvs=None, interval=1):
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

    def _subdivWrap(self, lv = 1):
        sel = pm.selected()
        srcA = sel[-1]
        tgt = []

        for obj in sel:
            if not obj == srcA:
                tgt.append(obj)

        srcB = pm.duplicate(srcA, n='{}_subdiv'.format(srcA))
        pm.hide(srcB)

        self._cleanupMeshes(cln = srcB, bor = 0)

        bs = pm.blendShape(srcA, srcB, o="local", en=1.0, n='{}_blendShape'.format(srcA))[0]
        pm.setAttr(bs+ '.{}'.format(srcA), 1)

        sm = pm.polySmooth(srcB, ovb=1, dv=lv, sdt=2)[0]
        pm.rename(sm, '{}_polySmooth'.format(srcB[0]))

        pm.select(cl=1)
        pm.select(tgt, srcB)
        mm.eval("CreateWrap;")

        wpTgt = pm.listHistory(tgt, type='wrap')
        pm.rename(wpTgt[0], '{}_{}'.format(srcB[0], wpTgt[0]))


    # select ===========================
    def _selectHierarchyByType(self, arg, typ='mesh'):
        sel = pm.selected()
        src = []
        tgt = []

        lgt = ['PxrAovLight', 'PxrDiskLight', 'PxrDistantLight', 'PxrDomeLight', 'PxrEnvDayLight', 'PxrMeshLight',
                'PxrPortalLight', 'PxrRectLight', 'PxrSphereLight', 'ambientLight', 'directionalLight', 'pointLight',
                'spotLight', 'areaLight', 'volumeLight']

        exd = ['joint', 'transform', 'nucleus']

        if typ == 'light':
            typ = lgt

        if not sel:
            sel = pm.ls(assemblies=1)

        for obj in sel:
            children = obj.getChildren(ad=1)

            for child in children:
                if pm.objectType(child) in typ:
                    src.append(child)

            if pm.objectType(obj) in typ:
                    src.append(obj)

        if typ not in exd:
            for shape in src:
                trans = shape.getParent()
                tgt.append(trans)

        elif typ == 'transform':
            for trans in src:
                shape = pm.listRelatives(trans, s=1) or []

                if not shape:
                    tgt.append(trans)

        else:
            tgt = src

        if tgt:
            pm.select(tgt, r=1)
            print('selected the Hierarchy')
        elif typ == 'light':
            print("Does not exist 'light'")
        else:
            print("Does not exist '{}'".format(typ))


    # select ===========================
    def _selectCVsNum(self, *args):
        try:
            num = int(cmds.textFieldButtonGrp('cvNumberButton', q=1, tx=1))
        except:
            num = 2
        sel = pm.selected()
        pm.select(cl=1)

        for i in sel:
            degs = pm.getAttr(i+ '.degree')
            spans = pm.getAttr(i+ '.spans')
            cvs = degs + spans - 1

            if num > cvs:
                pm.select(i.cv[cvs], add=1)
            else:
                pm.select(i.cv[num], add=1)


    def _selectCVs(self, arg, num='1'):
        sel = pm.selected()
        pm.select(cl=1)

        if num == 0:
            for i in sel:
                pm.select(i.cv[0], add=1)
        else:
            for i in sel:
                degs = pm.getAttr(i+ '.degree')
                spans = pm.getAttr(i+ '.spans')
                cvs = degs + spans - 1

                pm.select(i.cv[cvs], add=1)


    #----------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------

    # before run script

    def _warning(self):
        sel = pm.selected()
        warn = []
        if not sel:
            warn = pm.warning("You must've selected the object(s)")
        return warn


    def _checkObj(self, typ='mesh'):
        sel = pm.selected()
        tgt = []
        for obj in sel:
            if pm.objectType(obj, i='transform'):
                src = pm.listRelatives(obj, s=1, ni=1) or []
                if src and pm.objectType(src, i=typ):
                    tgt.append(obj)

            elif pm.objectType(obj, i=typ):
                trans = obj.getParent()
                tgt.append(trans)

        if not tgt:
            pm.warning("You must've selected the '{} Object(s)'".format(typ))
        return tgt


    #----------------------------------------------------------------------------------------------

    #++++++++++++++++++++++++++++++++++++
    def _getUnconnectedShapeOrigins(self, clnSrc):   # cleanup
        ### get unConnectedShapeOrigins ###
        pm.select(cl=1)
        garb = []

        for tgt in clnSrc:
            list = pm.listConnections(tgt, d=1, s=0)
            scn = pm.connectionInfo(tgt + '.instObjGroups', isSource=1)
            if (len(list) < 1):
                if (scn == 0):
                    if tgt.isIntermediate():
                        garb.append(tgt)
        return garb


    #************************************
    def _getMObjectFromSelection(self):    # get Extra Attributes
        m_selectionList = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(m_selectionList)
        m_node = om.MObject()
        try:
            m_selectionList.getDependNode(0, m_node)
            if (m_node.isNull()):
                return None
        except:
            return None
        return m_node

    #************************************
    def _getAllExtraAttributes(self):    # get Extra Attributes
        m_result = []
        m_obj = self._getMObjectFromSelection()
        m_workMFnDep  = om.MFnDependencyNode()
        m_workMDagMod = om.MDagModifier()
        if (m_obj):
            m_objFn = om.MFnDependencyNode()
            m_objFn.setObject(m_obj) # get function set from MObject
            m_objRef = m_workMFnDep.create(m_objFn.typeName()) # Create reference MObject of the given type
            # -- get the list --
            m_result = self._getAttrListDifference(m_obj,m_objRef)
            # --
            m_workMDagMod.deleteNode(m_objRef) # set node to delete
            m_workMDagMod.doIt() # execute delete operation
        return m_result

    #************************************
    def _getAttrListDifference(self, m_obj, m_objRef):    # get Extra Attributes
        m_objFn = om.MFnDependencyNode()
        m_objRefFn = om.MFnDependencyNode()
        m_objFn.setObject(m_obj)
        m_objRefFn.setObject(m_objRef)
        m_result = []
        if (m_objFn.attributeCount() > m_objRefFn.attributeCount()):
            for i in range(m_objRefFn.attributeCount(), m_objFn.attributeCount()):
                m_atrr = m_objFn.attribute(i)
                m_fnAttr = om.MFnAttribute(m_atrr)
                m_result.append(m_fnAttr.name())
        return m_result

    #++++++++++++++++++++++++++++++++++++
    #************************************
    def _cleanupMeshes(self, cln, bor = 0):   # cleanup
        ### delete History ###
        clnTgt = pm.ls(cln)
        tgt = []
        attrs = ['t', 'r', 's']
        axis = ['x', 'y', 'z']

        typ = ['mesh','nurbsCurve','nurbsSurface']

        for obj in clnTgt:
            if pm.objectType(obj, i='transform'):
                tgt.append(obj)
            elif pm.objectType(obj) in typ:
                trans = obj.getParent()
                tgt.append(trans)

        for src in tgt:
            pm.delete(src, ch=1)
            orig = self._getUnconnectedShapeOrigins(clnSrc = pm.listRelatives(src, s=1))
            pm.delete(orig)
            ### rename Shape ###
            clnShape = pm.listRelatives(src, s=1)
            pm.rename(clnShape[0], '{}Shape'.format(src))
            ### get Extra Attributes ###
            pm.select(src)
            m_list = self._getAllExtraAttributes()
            if m_list:
                for ea in m_list:
                    pm.setAttr(src+ '.' +ea, l=0)
                    pm.deleteAttr(src, at=ea)
            pm.select(cl=1)

            if not ('_INIT' in str(src) or '_REST' in str(src)):
                try:
                    for attr in attrs:
                        for ax in axis:
                            pm.setAttr(src+ '.'+attr+ax, l=0)
                    pm.makeIdentity(src, apply=1, t=1, r=1, s=1, n=0)
                except:
                    for i in pm.listAttr(src, l=1):
                        src.attr(i).unlock()
                    pm.makeIdentity(src, apply=1, t=1, r=1, s=1, n=0)
            pm.setAttr(src+ '.visibility', l=0)
            if bor == 1:
                pm.setAttr(clnShape[0]+ '.displayBorders', 1)
                pm.setAttr(clnShape[0]+ '.borderWidth', 4.7)
            if pm.objectType(clnShape, i='mesh'):
                pm.polyNormalPerVertex(src, ufn=1)
                clu = pm.cluster(src)
            pm.delete(src, ch=1)

        return tgt


# ---------------------------------------------------------------------------------

#mu = MyUtilities()
