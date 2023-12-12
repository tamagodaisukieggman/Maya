# coding: utf-8

from maya import cmds
from maya.api import OpenMaya as om2

COLOR_SET_NAME = 'bakePivot'


def set_color(mesh, color):
    if COLOR_SET_NAME in mesh.getColorSetNames():
        mesh.deleteColorSet(COLOR_SET_NAME)
    mesh.createColorSet(COLOR_SET_NAME, True)
    mesh.setCurrentColorSetName(COLOR_SET_NAME)

    numColors = mesh.numFaceVertices

    colors = [om2.MColor(color)] * numColors

    mesh.setColors(colors)
    mesh.assignColors(range(numColors))


def set_bb_color(dag, base, scale):
    mesh = om2.MFnMesh(dag)

    temp_dag = om2.MFnDagNode(dag)
    copy_dag = temp_dag.getPath()
    copy_dag.pop()

    transform = om2.MFnTransform(copy_dag)
    pos = transform.translation(om2.MSpace.kWorld) - base
    p = om2.MVector(pos.x * scale.x, pos.y * scale.y, pos.z * scale.z)

    # UE は Z-up なので軸を入れ替える
    p = om2.MVector(p.x, p.z, p.y)

    set_color(mesh, p)


def main():
    selList = om2.MGlobal.getActiveSelectionList()

    if selList.isEmpty():
        cmds.error("Don't select object")
        return

    parentName = selList.getDagPath(0).fullPathName().split('|')[1]

    meshList = []
    dagList = []

    itDag = om2.MItDag()

    while not itDag.isDone():
        dag = itDag.currentItem()
        if dag.apiType() == om2.MFn.kMesh:
            if parentName in itDag.fullPathName().split('|'):
                meshList.append(itDag.getPath())
                dagList.append(dag)
        itDag.next()

    bb = cmds.exactWorldBoundingBox(meshList)
    base = om2.MVector(bb[0], bb[1], bb[2])
    scale = om2.MVector(1 / (bb[3] - bb[0]), 1 / (bb[4] - bb[1]), 1 / (bb[5] - bb[2]))

    for mesh in meshList:
        set_bb_color(mesh, base, scale)

    return
