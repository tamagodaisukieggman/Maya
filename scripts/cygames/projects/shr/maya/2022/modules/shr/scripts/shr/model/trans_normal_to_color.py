# coding: utf-8

from maya import cmds
from maya.api import OpenMaya as om2


def trans_normal_to_color(mesh):
    if mesh.numColorSets == 0:
        mesh.createColorSet('bakeNormal', True)
    else:
        mesh.clearColors()

    originalNormals = []

    for faceId in range(mesh.numPolygons):
        originalNormals.append(mesh.getFaceVertexNormals(faceId))

    mesh.unlockVertexNormals(range(mesh.numNormals))

    faceColors = om2.MColorArray()
    # faceIds = []
    # vertexIds = []
    for faceId, normals  in enumerate(originalNormals):
        faceNormals = mesh.getFaceVertexNormals(faceId)
        faceTangents = mesh.getFaceVertexTangents(faceId)
        faceBinormals = mesh.getFaceVertexBinormals(faceId)
        for i, v in enumerate(normals):
            n = faceNormals[i]
            t = faceTangents[i]
            b = faceBinormals[i]
            c = om2.MVector(v * t, v * b, v * n)
            c = c * 0.5 + om2.MVector(0.5, 0.5, 0.5)
            faceColors.append(om2.MColor(c))
            # faceIds.append(faceId)
            # vertexIds.append(i)

    mesh.setColors(faceColors)
    mesh.assignColors(range(len(faceColors)))


def main():
    selList = om2.MGlobal.getActiveSelectionList()

    if selList.isEmpty():
        cmds.error("Don't select object")
        return

    mDagPath = selList.getDagPath(0)
    mesh = om2.MFnMesh(mDagPath)
    trans_normal_to_color(mesh)
