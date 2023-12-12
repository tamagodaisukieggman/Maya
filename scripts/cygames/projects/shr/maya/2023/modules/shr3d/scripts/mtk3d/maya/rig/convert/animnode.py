# -*- coding: utf-8 -*-
from maya import cmds, mel
from maya.api import OpenMaya as om
from maya.api import OpenMayaAnim as oma

class DeleteAnimNode(object):

    static_values = [om.MFn.kBlendNodeAdditiveRotation,
                     om.MFn.kBlendNodeAdditiveScale,
                     om.MFn.kBlendNodeBase,
                     om.MFn.kBlendNodeBoolean,
                     om.MFn.kBlendNodeDouble,
                     om.MFn.kBlendNodeDoubleAngle,
                     om.MFn.kBlendNodeDoubleLinear,
                     om.MFn.kBlendNodeEnum,
                     om.MFn.kBlendNodeFloat,
                     om.MFn.kBlendNodeFloatAngle,
                     om.MFn.kBlendNodeFloatLinear,
                     om.MFn.kBlendNodeInt16,
                     om.MFn.kBlendNodeInt32,
                     om.MFn.kBlendNodeTime,
                     om.MFn.kAnimLayer,
                     om.MFn.kPairBlend,
                     om.MFn.kAnimCurve]

    def __init__(self):
        self.attribute_list = ['lineWidth']

    def main(self, mtkCtrl=True, current_scene=None, save_path=None):

        if mtkCtrl:
            # mtk ctrl set
            CtrlSet = cmds.ls('*:ctrls_sets', '*:CtrlSet', r=1)
            cmds.select(CtrlSet, r=1, ne=1)
            ctrls = cmds.pickWalk(d='down')

            try:
                self.deleteConnectedAnimCurve_call(ctrls=ctrls, connectAttributes=self.attribute_list, shapeAttr=True)
                fbxspl = current_scene.split('/')
                fname = fbxspl[-1].split('.')[0]

                cmds.file(rn='{0}/{1}.ma'.format(save_path, fname))
                cmds.file(f=1, save=1)

                print('Saved:{0}/{1}.ma'.format(save_path, fname))
            except Exception as e:
                print(e)

    def deleteConnectedAnimCurve(self, obj=None, connectAttributes=None, shapeAttr=None):
        selection_list = om.MSelectionList()
        selection_list.add(obj)
        m_obj = selection_list.getDependNode(0)

        if shapeAttr:
            m_dag = selection_list.getDagPath(0)

            shape = m_dag.extendToShape(0)

            shape_sel_list = om.MSelectionList()
            shape_sel_list.add(shape)

            m_obj = shape_sel_list.getDependNode(0)

        m_dep = om.MFnDependencyNode(m_obj)

        for at in connectAttributes:
            plug = m_dep.findPlug(at, 0)

            m_depend_graph = om.MItDependencyGraph(plug, om.MItDependencyGraph.kUpstream, om.MItDependencyGraph.kPlugLevel)

            while not m_depend_graph.isDone():
                currentnode = m_depend_graph.currentNode()
                m_dep = om.MFnDependencyNode(currentnode)
                for sv in self.static_values:
                    if currentnode.hasFn(sv):
                        cmds.delete(m_dep.name())

                m_depend_graph.next()

    def deleteConnectedAnimCurve_call(self, ctrls=None, connectAttributes=None, shapeAttr=None):
        [self.deleteConnectedAnimCurve(obj=ctrl, connectAttributes=connectAttributes, shapeAttr=shapeAttr) for ctrl in ctrls]

if '__main__' == __name__:
    dan = DeleteAnimNode()
    dan.main()
