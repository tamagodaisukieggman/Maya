# -*- coding: utf-8 -*-
import traceback

import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim
import maya.OpenMayaMPx as OpenMayaMPx


class SkinWeightCmd(OpenMayaMPx.MPxCommand):
    kPluginCmdName = 'skinWeightCmd'
    kGeometryFlag = 'g'
    kGeometryLongFlag = 'geometry'
    kComponentFlag = 'c'
    kComponentLongFlag = 'components'
    kSkinClusterFlag = 'sc'
    kSkinClusterLongFlag = 'skinCluster'
    kWeightFlag = 'w'
    kWeightLongFlag = 'weights'

    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)

        self._arg_components = None
        self._arg_geometry = None
        self._arg_skinCluster = None
        self._arg_weights = None

        self._skin_fn = None
        self._dagpath = None
        self._influences = None
        self._influence_indices = None
        self._components = None
        self._old_weights = None

    @staticmethod
    def isUndoable():
        return True

    def parse_arguments(self, args):
        argData = OpenMaya.MArgParser(self.syntax(), args)
        if argData.isFlagSet(self.kGeometryFlag):
            self._arg_geometry = argData.flagArgumentString(self.kGeometryFlag, 0)

        if argData.isFlagSet(self.kComponentFlag):
            self._arg_components = []
            argList = OpenMaya.MArgList()
            for i in range(argData.numberOfFlagUses(self.kComponentFlag)):
                argData.getFlagArgumentList(self.kComponentFlag, i, argList)
                self._arg_components.append(argList.asString(i))

        if argData.isFlagSet(self.kSkinClusterFlag):
            self._arg_skinCluster = argData.flagArgumentString(self.kSkinClusterFlag, 0)

        if argData.isFlagSet(self.kWeightFlag):
            self._arg_weights = OpenMaya.MDoubleArray()
            argList = OpenMaya.MArgList()
            for i in range(argData.numberOfFlagUses(self.kWeightFlag)):
                argData.getFlagArgumentList(self.kWeightFlag, i, argList)
                self._arg_weights.append(argList.asDouble(i))

    def doIt(self, args):
        try:
            self.parse_arguments(args)
            self.redoIt()

        except Exception as e:
            OpenMaya.MGlobal.displayError(traceback.format_exc())

    def redoIt(self):
        if self._arg_components:
            self._dagpath, self._components = self.get_dagPath_and_comps(self._arg_components)

        else:
            if self._arg_geometry:
                self._dagpath, self._components = self.get_dagPath_and_comps(['{}.cp[*]'.format(self._arg_geometry)])

            else:
                raise Exception('[ %s ] : Please specify geometry or components.' % self.kPluginCmdName)

        if not self._arg_skinCluster:
            raise Exception('[ %s ] : Please specify skinCluster.' % self.kPluginCmdName)

        if not self._arg_weights:
            raise Exception('[ %s ] : Please specify weights.' % self.kPluginCmdName)

        self._skin_fn = OpenMayaAnim.MFnSkinCluster(self.get_MObject(self._arg_skinCluster))
        self._influences = OpenMaya.MDagPathArray()
        self._skin_fn.influenceObjects(self._influences)

        self._influence_indices = OpenMaya.MIntArray()
        [self._influence_indices.append(i) for i in range(self._influences.length())]

        self._old_weights = OpenMaya.MDoubleArray()
        self._skin_fn.setWeights(
            self._dagpath, self._components, self._influence_indices, self._arg_weights, False, self._old_weights)

    def undoIt(self):
        self._skin_fn.setWeights(self._dagpath, self._components, self._influence_indices, self._old_weights, False)

    @staticmethod
    def get_MObject(obj):
        sel_list = OpenMaya.MSelectionList()
        sel_list.add(obj)
        m_obj = OpenMaya.MObject()
        sel_list.getDependNode(0, m_obj)

        return m_obj

    @staticmethod
    def get_dagPath_and_comps(objects):
        sel_list = OpenMaya.MSelectionList()
        [sel_list.add(x) for x in objects]
        dag_path = OpenMaya.MDagPath()
        comps = OpenMaya.MObject()
        sel_list.getDagPath(0, dag_path, comps)
        return dag_path, comps

    @classmethod
    def cmdCreator(cls):
        return OpenMayaMPx.asMPxPtr(cls())

    @classmethod
    def syntaxCreator(cls):
        syntax = OpenMaya.MSyntax()

        syntax.addFlag(cls.kComponentFlag, cls.kComponentLongFlag, OpenMaya.MSyntax.kString)
        syntax.makeFlagMultiUse(cls.kComponentFlag)

        syntax.addFlag(cls.kGeometryFlag, cls.kGeometryLongFlag, OpenMaya.MSyntax.kString)

        syntax.addFlag(cls.kSkinClusterFlag, cls.kSkinClusterLongFlag, OpenMaya.MSyntax.kString)

        syntax.addFlag(cls.kWeightFlag, cls.kWeightLongFlag, OpenMaya.MSyntax.kDouble)
        syntax.makeFlagMultiUse(cls.kWeightFlag)

        return syntax


def initializePlugin(obj):
    mplugin = OpenMayaMPx.MFnPlugin(obj, 'tkg', '1.0', 'Any')
    try:
        mplugin.registerCommand(
            SkinWeightCmd.kPluginCmdName,
            SkinWeightCmd.cmdCreator,
            SkinWeightCmd.syntaxCreator
        )

    except Exception:
        raise Exception('Failed to register command: %s' % SkinWeightCmd.kPluginCmdName)


def uninitializePlugin(obj):
    mplugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        mplugin.deregisterCommand(SkinWeightCmd.kPluginCmdName)
    except Exception:
        raise Exception('Failed to unregister command: %s' % SkinWeightCmd.kPluginCmdName)
