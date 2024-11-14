# -*- coding: utf-8 -*-
import math
import traceback

from maya import cmds
from maya import mel
import maya.api.OpenMaya as om2

def get_MDagPath2(objectName):
    selList = om2.MSelectionList()
    selList.add(objectName)

    return selList.getDagPath(0)

def get_shapeDagPath2(dag_path):
    if not isinstance(dag_path, om2.MDagPath):
        return None

    if dag_path.apiType() not in [om2.MFn.kMesh, om2.MFn.kNurbsSurface, om2.MFn.kNurbsCurve]:
        dag_path.extendToShape()
        if dag_path.apiType() not in [om2.MFn.kMesh, om2.MFn.kNurbsSurface, om2.MFn.kNurbsCurve]:
            return None

    return dag_path

def get_closestPointData(base_pos, targetMesh, space=om2.MSpace.kWorld):
    dag_path = get_shapeDagPath2(get_MDagPath2(targetMesh))
    if not dag_path:
        return None

    mesh_fn = om2.MFnMesh(dag_path)

    closest_pos, face_id = mesh_fn.getClosestPoint(base_pos, space=space)
    vIds = mesh_fn.getPolygonVertices(face_id)
    vertPoints = [[vId, mesh_fn.getPoint(vId, space=space)] for vId in vIds]

    nearestVerts = sorted(sorted(vertPoints, key=lambda x: x[1].distanceTo(closest_pos))[:3], key=lambda x: x[0])
    vert_ids, vert_points = [v[0] for v in nearestVerts], [v[1] for v in nearestVerts]

    return closest_pos, face_id, vert_points, vert_ids

def closest_point(targetObject, base_pos, world=True):
    base_pos = om2.MPoint(*base_pos)
    space = om2.MSpace.kWorld if world else om2.MSpace.kObject
    closest_pos, face_id, vert_points, vert_ids = get_closestPointData(base_pos, targetObject, space=space)
    return closest_pos, face_id, vert_points, vert_ids

def get_center_of_cmps(cmps=None):
    if not cmps:
        return None
    
    # 選択された頂点とエッジを取得
    vertices = cmds.filterExpand(cmps, selectionMask=31)  # 31は頂点の選択マスク
    edges = cmds.filterExpand(cmps, selectionMask=32)  # 32はエッジの選択マスク

    # エッジが選択されている場合、その頂点を取得
    if edges:
        vertices_from_edges = cmds.polyListComponentConversion(edges, toVertex=True)
        vertices_from_edges = cmds.filterExpand(vertices_from_edges, selectionMask=31)
        if vertices_from_edges:
            vertices = vertices_from_edges

    if not vertices:
        cmds.warning("頂点またはエッジが選択されていません。")
        return None

    # 合計の位置を初期化
    total_position = om2.MVector(0.0, 0.0, 0.0)
    vertex_count = len(vertices)

    # 各頂点の位置を合計
    for vertex in vertices:
        position = cmds.pointPosition(vertex, world=True)
        total_position += om2.MVector(position[0], position[1], position[2])

    # 重心を計算
    center_of_mass = total_position / vertex_count

    # 重心の位置を表示
    # cmds.spaceLocator(position=(center_of_mass.x, center_of_mass.y, center_of_mass.z))
    # print(f"重心の位置: {center_of_mass.x}, {center_of_mass.y}, {center_of_mass.z}")
    return [center_of_mass.x, center_of_mass.y, center_of_mass.z]

def get_vertices_within_distance(mesh1, face_index, mesh2, max_distance):
    # Get the vertices of the face on the first mesh
    face_vertices = cmds.polyInfo(f"{mesh1}.f[{face_index}]", faceToVertex=True)[0].split()[2:]
    face_vertices = [int(v) for v in face_vertices]

    # Get the positions of the face vertices
    face_positions = []
    for v in face_vertices:
        pos = cmds.pointPosition(f"{mesh1}.vtx[{v}]", world=True)
        face_positions.append(om.MVector(pos))

    # Get all vertices of the second mesh
    mesh2_vertices = cmds.ls(f"{mesh2}.vtx[*]", fl=True)

    # Initialize the list of close vertices
    close_vertices = []

    # Iterate over all vertices of the second mesh
    for vertex in mesh2_vertices:
        pos = cmds.pointPosition(vertex, world=True)
        vertex_pos = om.MVector(pos)
        
        # Calculate the average position of the face
        face_center = sum(face_positions, om.MVector()) / len(face_positions)
        
        # Calculate the distance from the face center to the current vertex
        distance = (vertex_pos - face_center).length()
        
        # Check if this vertex is within the max distance
        if distance <= max_distance:
            close_vertices.append((vertex, distance))

    return close_vertices

# sel = cmds.ls(os=True)
# obj = sel[0]
# target = sel[1]
# faces = cmds.ls(f'{obj}.f[*]', fl=True)
# center_of_masses = {}
# for f in faces:
#     cmds.select(f, r=True)
#     cmds.ConvertSelectionToVertices()
#     vertices = cmds.ls(os=True, fl=True)
#     center_of_mass = get_center_from_face(vertices)
#     center_of_masses[f] = center_of_mass
#     # closest_faces.append(closest_point(target, center_of_mass, world=True))

# closest_verts_data = {}
# for f, fwt in center_of_masses.items():
#     closest_info = closest_point(target, fwt, world=True)
#     closest_verts = []
#     for clov in closest_info[3]:
#         closest_verts.append(f'{target}.vtx[{clov}]')
#     closest_verts_data[f] = closest_verts

# closest_face_verts = []
# for f, verts in closest_verts_data.items():
#     [closest_face_verts.append(v) for v in verts if not v in closest_face_verts]

# cmds.select(closest_face_verts)

# cmds.ConvertSelectionToFaces()

# closest_faces = cmds.ls(os=True, fl=True)

# verts_center_of_masses = {}
# for f in closest_faces:
#     cmds.select(f, r=True)
#     cmds.ConvertSelectionToVertices()
#     vertices = cmds.ls(os=True, fl=True)
#     center_of_mass = get_center_from_face(vertices)
#     verts_center_of_masses[f] = center_of_mass
#     # closest_faces.append(closest_point(target, center_of_mass, world=True))

# obj_closest_verts_data = {}
# for f, fwt in verts_center_of_masses.items():
#     closest_info = closest_point(obj, fwt, world=True)
#     closest_verts = []
#     for clov in closest_info[3]:
#         closest_verts.append(f'{obj}.vtx[{clov}]')
#     obj_closest_verts_data[f] = closest_verts

# obj_closest_face_verts = []
# for f, verts in obj_closest_verts_data.items():
#     [obj_closest_face_verts.append(v) for v in verts if not v in obj_closest_face_verts]

# cmds.select(obj_closest_face_verts, r=True)
