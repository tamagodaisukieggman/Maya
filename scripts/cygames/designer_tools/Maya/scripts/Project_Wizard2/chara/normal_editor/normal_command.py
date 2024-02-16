# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

import sys
from maya.api import OpenMaya as om2


class NormalSetCommand(om2.MPxCommand):
    kPluginCmdName = 'setNormal'

    def __init__(self):
        om2.MPxCommand.__init__(self)
        self.target = None
        self.vertex_ids = None
        self.face_ids = None
        self.normals = None
        self.before_normals = None
        self.unlock_vertex_ids = None
        self.unlock_face_ids = None
        self.smooth_edge_ids = None
        self.smooths = None
        self.keep_soft_edge = False

    @staticmethod
    def cmdCreator():
        return NormalSetCommand()

    @staticmethod
    def syntaxCreator():
        syntax = om2.MSyntax()
        syntax.setObjectType(om2.MSyntax.kStringObjects)
        syntax.addFlag('-vi', '-vertexIds', om2.MSyntax.kLong)
        syntax.makeFlagMultiUse('-vi')
        syntax.addFlag('-fi', '-faceIds', om2.MSyntax.kLong)
        syntax.makeFlagMultiUse('-fi')
        syntax.addFlag('-n', '-normals', (om2.MSyntax.kDouble, om2.MSyntax.kDouble, om2.MSyntax.kDouble))
        syntax.makeFlagMultiUse('-n')
        syntax.addFlag('-ks', '-keepSoftEdge', om2.MSyntax.kBoolean)
        return syntax

    def get_dag_path(self):
        sel_list = om2.MGlobal.getSelectionListByName(self.target)
        return sel_list.getDagPath(0)

    def get_mesh(self):
        dag_path = self.get_dag_path()
        return om2.MFnMesh(dag_path)

    def parse_arguments(self, args):
        arg_parser = om2.MArgParser(self.syntax(), args)

        self.target = arg_parser.getObjectStrings()[0]

        dag_path = self.get_dag_path()

        mesh_fn = self.get_mesh()

        vertex_num = arg_parser.numberOfFlagUses('-vi')
        face_num = arg_parser.numberOfFlagUses('-fi')
        normal_num = arg_parser.numberOfFlagUses('-n')

        num = min(vertex_num, face_num, normal_num)

        self.vertex_ids = []
        self.face_ids = []
        self.normals = []
        self.before_normals = []

        for i in range(num):
            vertex_id = arg_parser.getFlagArgumentList('-vi', i).asInt(0)
            face_id = arg_parser.getFlagArgumentList('-fi', i).asInt(0)
            normal = arg_parser.getFlagArgumentList('-n', i).asVector(0)
            before_normal = mesh_fn.getFaceVertexNormal(face_id, vertex_id)

            self.vertex_ids.append(vertex_id)
            self.face_ids.append(face_id)
            self.normals.append(normal)
            self.before_normals.append(before_normal)

        facevert_iter = om2.MItMeshFaceVertex(dag_path)

        self.unlock_vertex_ids = []
        self.unlock_face_ids = []

        while not facevert_iter.isDone():
            normal_id = facevert_iter.normalId()

            if not mesh_fn.isNormalLocked(normal_id):
                vertex_id = facevert_iter.vertexId()
                face_id = facevert_iter.faceId()

                self.unlock_vertex_ids.append(vertex_id)
                self.unlock_face_ids.append(face_id)

            facevert_iter.next()

        edge_iter = om2.MItMeshEdge(dag_path)

        self.smooth_edge_ids = []
        self.smooths = []

        while not edge_iter.isDone():
            edge_id = edge_iter.index()
            smooth = edge_iter.isSmooth

            self.smooth_edge_ids.append(edge_id)
            self.smooths.append(smooth)

            edge_iter.next()

        if arg_parser.isFlagSet('-ks'):
            self.keep_soft_edge = arg_parser.flagArgumentBool('-ks', 0)

    def doIt(self, args):
        self.parse_arguments(args)

        self.redoIt()

    def redoIt(self):
        mesh_fn = self.get_mesh()

        mesh_fn.setFaceVertexNormals(self.normals, self.face_ids, self.vertex_ids)

        if self.keep_soft_edge:
            mesh_fn.setEdgeSmoothings(self.smooth_edge_ids, self.smooths)
            mesh_fn.cleanupEdgeSmoothing()

    def undoIt(self):
        mesh_fn = self.get_mesh()

        mesh_fn.setFaceVertexNormals(self.before_normals, self.face_ids, self.vertex_ids)
        mesh_fn.unlockFaceVertexNormals(self.unlock_face_ids, self.unlock_vertex_ids)
        mesh_fn.setEdgeSmoothings(self.smooth_edge_ids, self.smooths)
        mesh_fn.cleanupEdgeSmoothing()

    def isUndoable(self):
        return True


def maya_useNewAPI():
    pass


def initializePlugin(mobject):
    mplugin = om2.MFnPlugin(mobject)
    try:
        mplugin.registerCommand(NormalSetCommand.kPluginCmdName, NormalSetCommand.cmdCreator, NormalSetCommand.syntaxCreator)
    except Exception:
        sys.stderr.write('Failed to register command: ' + NormalSetCommand.kPluginCmdName)


def uninitializePlugin(mobject):
    mplugin = om2.MFnPlugin(mobject)
    try:
        mplugin.deregisterCommand(NormalSetCommand.kPluginCmdName)
    except Exception:
        sys.stderr.write('Failed to unregister command: ' + NormalSetCommand.kPluginCmdName)
