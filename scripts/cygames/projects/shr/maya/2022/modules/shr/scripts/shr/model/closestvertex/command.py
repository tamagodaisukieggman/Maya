# coding=utf-8
u"""選択された頂点を別メッシュの近接頂点へ移動

"""
import maya.cmds as cmds
import maya.api.OpenMaya as om


def get_closest_point(point, name):
    u"""point(頂点座標)からmesh(メッシュ)の近傍頂点を取得

    :param point: 頂点座標(3vector) MPoint
    :param mesh: メッシュ名(strig ex:Sphere1’)
    :return:
    """
    selection = om.MSelectionList()
    selection.add(name)
    dag_path = selection.getDagPath(0)
    mesh_fn = om.MFnMesh(dag_path)
    space = om.MSpace.kWorld
    # 近傍頂点、面のIDを取得
    closest_point, face_id = mesh_fn.getClosestPoint(point, space)
    # Vertexのポイントを取得
    mesh_faces = om.MItMeshPolygon(dag_path)
    mesh_faces.setIndex(face_id)
    mesh_points = mesh_faces.getPoints(space)
    # 一番近い頂点をclosest_pointに格納
    min = None
    closest_point = None
    for mesh_point in mesh_points:
        len = (mesh_point - point).length()
        if min is None or len < min:
            min = len
            closest_point = mesh_point

    selection.clear()

    return list(closest_point)[:3]


def get_closest_surface(point, name):
    u"""point(頂点座標)からmesh(メッシュ)の近傍頂点を取得

    :param point: 頂点座標(3vector) MPoint
    :param mesh: メッシュ名(strig ex:Sphere1’)
    :return:
    """
    selection = om.MSelectionList()
    selection.add(name)
    dag_path = selection.getDagPath(0)
    mesh_fn = om.MFnMesh(dag_path)
    space = om.MSpace.kWorld
    # 近傍頂点、面のIDを取得
    closest_point, face_id = mesh_fn.getClosestPoint(point, space)

    selection.clear()

    return list(closest_point)[:3]


def get_mesh():
    u"""UIのテキストフィールド登録用

    :return:
    """
    selections = cmds.ls(selection=True)
    return selections[0]


def run_vertex(name):
    u"""頂点座標移動処理実行

    :param mesh: メッシュ名(strig ex:Sphere1’)
    :return:
    """
    if len(name) == 0:
        cmds.warning(u'頂点検索対象にメッシュを指定して下さい')
        return False

    vertices = cmds.ls(selection=True, flatten=True)

    for vertex in vertices:
        point = cmds.xform(vertex, worldSpace=True, translation=True, query=True)
        mpoint = om.MPoint(point)
        closest = get_closest_point(mpoint, name)
        cmds.xform(vertex, worldSpace=True, translation=closest)


def run_surface(name):
    u"""表面座標移動処理実行

    :param mesh: メッシュ名(strig ex:Sphere1’)
    :return:
    """
    if len(name) == 0:
        cmds.warning(u'頂点検索対象にメッシュを指定して下さい')
        return False

    vertices = cmds.ls(selection=True, flatten=True)

    for vertex in vertices:
        point = cmds.xform(vertex, worldSpace=True, translation=True, query=True)
        mpoint = om.MPoint(point)
        closest = get_closest_surface(mpoint, name)
        cmds.xform(vertex, worldSpace=True, translation=closest)
