# -*- coding: utf-8 -*-
# ----------------------------------
# Project : Tsubasa
# Name    : dccUserMayaSharePythonLib.skinning
# Author  : toi
# Version : 0.0.4
# Updata  : 2021/6/3
# ----------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import maya.cmds as cmds
import maya.mel as mm
import pymel.core as pm
from dccUserMayaSharePythonLib import pyCommon as pycm
import math
import os
import sys
import xml.etree.ElementTree as et


def writePairModel(parent_, child_):
    tmp_node = '_tmp_node'
    if not cmds.objExists(tmp_node):
        cmds.createNode('transform', n=tmp_node, ss=True)

    parent_ = parent_.replace('|', '___')
    child_ = child_.replace('|', '___')

    if not cmds.objExists(tmp_node + '.' + parent_):
        pm.addAttr(tmp_node, ln=parent_, nn=parent_, dt='string')
    pm.setAttr(tmp_node + '.' + parent_, child_)


def getShapeHierarchy(node):
    """node以下の階層に含まれるシェイプノードを取得"""

    nodes = pm.ls(node, dag=True)
    result = []
    for node in nodes:
        try:
            if node.getShape():
                result.append(node)
        except:
            pass
    return result


def listRelatedSkinClusters(nodes, return_string=False):
    """接続されているskinClusterノードを取得
    :param list/str nodes: メッシュノードのリスト
    :return: skinClusterノードのリスト
    :rtype: list
    """

    if return_string:
        if not nodes:
            return []

        shapes = cmds.listRelatives(nodes, s=True, ni=True, pa=True, type='controlPoint')
        if not shapes:
            shapes = cmds.ls(nodes, ni=True, type='controlPoint')
            if not shapes:
                return []

        history = cmds.listHistory(shapes, pdo=True)
        if not history:
            return []

        return cmds.ls(history, typ='skinCluster') or []

    else:
        if not nodes:
            return []

        shapes = pm.listRelatives(nodes, s=True, ni=True, pa=True, type='controlPoint')
        if not shapes:
            shapes = pm.ls(nodes, ni=True, type='controlPoint')
            if not shapes:
                return []

        history = pm.listHistory(shapes, pdo=True)
        if not history:
            return []

        return pm.ls(history, typ='skinCluster') or []


def listSkinClusterIinfluences(skinClusters):
    """接続されているskinClusterのインフルエンスを取得
    :param list skinClusters: skinClusterノードのリスト
    :return: インフルエンスのリスト
    :rtype: list
    """

    if not skinClusters:
        return []

    skinClusters = cmds.ls(skinClusters, typ='skinCluster') or []
    if not skinClusters:
        return []

    plugs = ['{}.matrix'.format(sc) for sc in skinClusters]
    return cmds.listConnections(plugs, s=1, d=0) or []


def selectRelatedInfluences(nodes, sel=False):
    """接続されているskinClusterのインフルエンスを取得
    :param list nodes: ノードのリスト
    """

    if not nodes:
        return

    skinClusters = listRelatedSkinClusters(nodes, return_string=True)
    influences = listSkinClusterIinfluences(skinClusters)
    if sel:
        cmds.select(influences, add=True)
    return influences


#未使用
def create_bind_pair_model_window():
    def main(nodes, b):
        cmds.select(nodes)
        cmds.button(b, e=True, bgc=(256, 256, 256))

    tmp_node = '_tmp_node'
    if not cmds.objExists(tmp_node):
        return

    if cmds.window(__name__, ex=True):
        cmds.deleteUI(__name__)
    w = cmds.window(__name__, t=__name__)

    cmds.scrollLayout()

    atList = cmds.listAttr(tmp_node, ud=True)
    for at in atList:
        try:
            parent_ = at.replace('___', '|')
            print(parent_)
            influences = selectRelatedInfluences(parent_)

            child_ = pm.getAttr(tmp_node + '.' + at)

            #cmds.select(influences)
            #cmds.select(child_, add=True)
            #cmds.bindSkin(tsb=True)

            nodes = influences + [child_]
            print(nodes)

            b = cmds.button(l=child_)
            cmds.button(b, e=True, c=pm.Callback(main, nodes, b))
        except:
            pass

    cmds.showWindow(w)


def selJointHierarchyIgnoreDel(nodes):
    for i, node in enumerate(nodes):
        if i == 0:
            cmds.select(node, hi=True)
        else:

            h_nodes = cmds.ls(node, dag=True)
            cmds.select(h_nodes, d=True)

    sels = cmds.ls(sl=True)
    for sel in sels:
        if sel.startswith('del_') or not cmds.nodeType(sel) == 'joint':
            cmds.select(sel, d=True)


def selHierarchy(nodes):
    for node in nodes:
        cmds.select(node, hi=True, d=True)


def forceBind(set_obj):
    child_influences = selectRelatedInfluences(child_)
    # child_が既にバインド済の場合は、バインドされていないinfluencesのみをadd
    if child_influences:
        add_influences = pycm.negationList(influences, child_influences)
        #if not add_influences:
        #	return 1

        pm.skinCluster(
            child_,
            e=True,
            addInfluence=add_influences,
            weight=0,
            lockWeights=True)
    else:
        set_obj = influences
        set_obj.append(child_)
        pm.skinCluster(set_obj, tsb=True)


def bindPairModel(parent_, child_):
    """parent_と同じinfluencesにchild_もバインドする"""

    pm.select(cl=True)

    # parent_メッシュのインフルエンスを取得
    influences = selectRelatedInfluences(parent_)
    if not influences:
        return 1

    child_influences = selectRelatedInfluences(child_)
    # child_が既にバインド済の場合は、バインドされていないinfluencesのみをadd
    if child_influences:
        add_influences = pycm.negationList(influences, child_influences)
        #if not add_influences:
        #	return 1

        pm.skinCluster(
            child_,
            e=True,
            addInfluence=add_influences,
            weight=0,
            lockWeights=True)
    else:
        set_obj = influences
        set_obj.append(child_)
        pm.skinCluster(set_obj, tsb=True)

    return 0


def copySkinWeight(
        parent_, child_,
        noMirror_=True,
        surfaceAssociation_='closestPoint',
        influenceAssociation_=['label', 'closestJoint'],
        normalize_=False):
    """
    influenceAssociation_; 「closestJoint」、「closestBone」、「label」、「name」、「oneToOne」
    """

    pm.select(cl=True)
    pm.select(parent_, child_)
    #print(pm.ls(parent_, type="skinCluster"))
    #skin_cluster_p = pm.ls(parent_, type="skinCluster")[0]
    #skin_cluster_c = pm.ls(child_, type="skinCluster")[0]
    pm.copySkinWeights(
        #ss=skin_cluster_p, ds=skin_cluster_c,
        noMirror=noMirror_, normalize=normalize_,
        surfaceAssociation=surfaceAssociation_,
        influenceAssociation=influenceAssociation_)


def copyPasteVertexWeight(parent_, child_):
    pm.select(parent_)
    pm.mel.eval('CopyVertexWeights')
    pm.select(child_)
    pm.mel.eval('PasteVertexWeights')


def getValuedInfluence(vertex):
    """
    vertexの有効なインフルエンスを取得する
    [(joint, value)]
    """

    mesh = vertex.split('.')[0]
    skc = listRelatedSkinClusters(mesh, return_string=True)
    jnt_list = cmds.skinPercent(skc[0], vertex, q=True, t=None)
    val_list = cmds.skinPercent(skc[0], vertex, q=True, v=True)

    valued_list = []
    for j, v in zip(jnt_list, val_list):
        if v:
            valued_list.append((j, v))
    return valued_list


def forceSetMaxInfluence(vertex, max_influence, weight_hammer=False):
    mesh = vertex.split('.')[0]
    # print(vertex, mesh)
    skc = listRelatedSkinClusters(mesh, return_string=True)[0]
    cmds.setAttr(skc + '.normalizeWeights', 1)
    cmds.select(vertex)

    if weight_hammer:
        mm.eval('weightHammerVerts')

    valued_list = getValuedInfluence(vertex)
    valued_list = pycm.doubleSort(valued_list, 1, True)
    cull_list = valued_list[: max_influence]
    # print(valued_list)
    # print(skc, [vertex], cull_list)
    cmds.skinPercent(skc, transformValue=cull_list, relative=True, normalize=True)


class CopyPasteVtxsWeight(object):
    """複数インデックスのWeightをコピーペースト"""

    def __init__(self):
        self.transform_value = []
        self.copy_mesh = None
        self.paste_mesh = None

    def copyWeightSelVtxs(self):
        self.transform_value = []
        sels = pm.ls(fl=True, os=True)
        self.copy_mesh = getMeshNameFromSelVtx()
        skc = listRelatedSkinClusters([self.copy_mesh])
        if sels:
            for s in sels:
                jnt_list = pm.skinPercent(skc[0], s, q=True, t=None)
                val_list = pm.skinPercent(skc[0], s, q=True, v=True)
                j_v_list = []
                for j, v in zip(jnt_list, val_list):
                    if v:
                        j_v_list.append((j, v))
                self.transform_value.append(j_v_list)

    def pasteWeightSelVtxs(self):
        if self.transform_value:
            sels = pm.ls(fl=True, os=True)
            if sels:
                self.paste_mesh = getMeshNameFromSelVtx()
                skc = listRelatedSkinClusters([self.paste_mesh])
                bindPairModel(self.copy_mesh, self.paste_mesh)
                for i in range(len(sels)):
                    pm.select(sels[i])
                    pm.skinPercent(skc, transformValue=self.transform_value[i])

    def pasteFirstSelVtx(self):
        sels = pm.ls(fl=True, os=True)
        base = sels[0]

        pm.select(base)
        self.copyWeightSelVtxs()
        j_v_list = self.transform_value[0]
        self.transform_value = []

        paste_vtxs = sels[1:]
        paste_vtxs_num = len(paste_vtxs)
        for i in range(paste_vtxs_num):
            self.transform_value.append(j_v_list)

        pm.select(paste_vtxs)
        self.pasteWeightSelVtxs()

        pm.select(sels)

    def alternateCopyPaste(self):
        sels = pm.ls(fl=True, os=True)
        for i in range(len(sels)):
            if i % 2 == 0:
                pm.select(sels[i])
                self.copyWeightSelVtxs()
                pm.refresh()

                pm.select(sels[i + 1])
                self.pasteWeightSelVtxs()
                pm.refresh()

        cmds.select(sels)


def convertShellVertex():
    """選択しているコンポーネントをシェル状態に拡大して選択する"""

    vertext_list = cmds.polyListComponentConversion(cmds.ls(sl=True), toVertex=True)
    cmds.select(vertext_list)
    cmds.polySelectConstraint(m=2, sh=True)
    cmds.polySelectConstraint(bo=0, m=0, sh=False)
    result = cmds.ls(sl=True, fl=True)
    return result


def createSetComponent():
    """選択コンポートネントをバーテックスに変換してセット化する"""

    component_selection = cmds.ls(sl=True, fl=True)
    '''
    for c in component_selection:
        selnode = component_selection.split('.')[0]
        comp = component_selection.split('[')[-1]
        comp = comp[:-1].replace(':', '_')
        
        vertext_list = pm.polyListComponentConversion(component_selection, toVertex=True)
        cmds.select(vertext_list)
        s = pm.sets()
    '''
    vertext_list = pm.polyListComponentConversion(component_selection, toVertex=True)
    cmds.select(vertext_list)
    s = pm.sets(n='vtxset')
    return s


def duplicateSelPolygon(polygon_selection):
    """選択ポリゴンをのみを複製する"""

    original_node, comp = polygon_selection[0].split('.f[')
    #comp = comp[:-1]
    #comp = comp[:-1]
    dupnode = cmds.duplicate(original_node)[0]

    dupnode_selcomp = [x.replace(original_node, dupnode) for x in polygon_selection]
    cmds.select(cl=True)
    #pm.select(dupnode + '.f[{0}]'.format(comp))
    cmds.select(dupnode_selcomp)
    pm.mel.InvertSelection()
    cmds.delete()

    dupnode = cmds.rename(dupnode, original_node + '_dupicatePolygon')
    cmds.select(polygon_selection)
    return dupnode, original_node


def duplicateSelPolygon2(polygon_selection):
    """
    選択ポリゴンをのみを複製する（マルチノード対応）
    return; dup_node, original_node, polys
    """
    cmds.select(polygon_selection)
    original_nodes = list(set([x.split('.f[')[0] for x in polygon_selection]))

    original_poly_dict = {}
    for original_node in original_nodes:
        tmp_list = []
        for poly in polygon_selection:
            if original_node == poly.split('.')[0]:
                tmp_list.append(poly)
        original_poly_dict[original_node] = tmp_list

    result_list = []
    for original_node, polys in original_poly_dict.items():
        dup_node = cmds.duplicate(original_node)[0]
        dup_node_selcomp = [x.replace(original_node, dup_node) for x in polys]

        cmds.select(cl=True)
        cmds.select(dup_node_selcomp)
        pm.mel.InvertSelection()
        cmds.delete()

        dup_node = cmds.rename(dup_node, original_node + '_dupicatePolygon#')
        cmds.select(polygon_selection)

        result_list.append([dup_node, original_node, polys])
        cmds.parent(dup_node, w=True)

    return result_list


def duplicateSelPolygonAndBindAndCopy(polygon_selection):
    """選択ポリゴンをのみを複製して、元のウエイトをコピーする"""

    dupnode, node = duplicateSelPolygon(polygon_selection)
    vtx_set = createSetComponent()
    bindPairModel(node, dupnode)
    copySkinWeight(node, dupnode)

    dup_group = 'Duplicate_Group'
    if not pm.objExists(dup_group):
        pm.group(em=True, n=dup_group)

    pm.parent(dupnode, dup_group)
    pm.addAttr(dupnode, ln='vtx_set', dt="string")
    pm.setAttr(dupnode + '.vtx_set', vtx_set.name())


def polySelectTraverse():
    """選択拡大"""

    pm.mel.eval("select `ls -sl`;PolySelectTraverse 1;select `ls -sl`;")


def getMeshNameFromSelVtx():
    """メッシュ：選択中のバーテックスからメッシュ名を取得する"""

    sels = pm.ls(sl=True, fl=True)
    if not sels:
        return

    return sels[0].split('.')[0]


def distance2Coordinate(vtx1, vtx2, world=True):
    """メッシュ：2点間の距離"""

    x1, y1, z1 = pm.pointPosition(vtx1, w=world, l=not world)
    x2, y2, z2 = pm.pointPosition(vtx2, w=world, l=not world)
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)


def get_adjacent_vertices(mesh, vertex_index):
    """メッシュ：隣接するバーテックスの取得"""

    vertex = '{}.vtx[{}]'.format(mesh, vertex_index)
    connected_edges = cmds.polyListComponentConversion(vertex, fromVertex=True, toEdge=True)
    connected_vertices = cmds.polyListComponentConversion(connected_edges, fromEdge=True, toVertex=True)
    return connected_vertices


def get_opposite_vertex(mesh, vertex_index, axis='x', tolerance=0.01):
    """
    メッシュ：反対側のバーテックスの取得.
    :param mesh: str, name of the mesh
    :param vertex_index: int, index of the vertex to find the opposite of
    :param axis: str, symmetry axis ('x', 'y' or 'z')
    :param tolerance: float, tolerance for position comparison
    :return: int, index of the opposite vertex, or None if not found
    """
    pre_sels = cmds.ls(sl=True)

    target_vtx = '{}.vtx[{}]'.format(mesh, vertex_index)
    cmds.select(target_vtx, sym=True)
    current_sels = cmds.ls(sl=True)
    if len(current_sels) == 2:
        current_sels.remove(target_vtx)
        return current_sels[0]
    else:
        if axis.lower() not in ['x', 'y', 'z']:
            raise ValueError("Invalid axis. Must be 'x', 'y', or 'z'.")

        # Get the position of the specified vertex
        vertex_position = cmds.pointPosition(f"{mesh}.vtx[{vertex_index}]", world=True)

        # Find the opposite position
        opposite_position = list(vertex_position)
        if axis.lower() == 'x':
            opposite_position[0] = -opposite_position[0]
        elif axis.lower() == 'y':
            opposite_position[1] = -opposite_position[1]
        else:
            opposite_position[2] = -opposite_position[2]

        # Get all vertices of the mesh
        vertex_count = cmds.polyEvaluate(mesh, vertex=True)

        # Iterate through all vertices and find the opposite vertex
        for i in range(vertex_count):
            if i == vertex_index:
                continue
            current_position = cmds.pointPosition(f"{mesh}.vtx[{i}]")
            if abs(opposite_position[0] - current_position[0]) < tolerance \
                and abs(opposite_position[1] - current_position[1]) < tolerance \
                    and abs(opposite_position[2] - current_position[2]) < tolerance:
                return i
        cmds.select(pre_sels)
        return None


class CopyPasteMesh2Vtx(object):
    def __init__(self):
        self.mesh_node = ''
        self.vtxs = []
        self.set = ''
        self.paste_mesh = ''
        self.influenceAssociation = 'oneToOne'
        self.force_bind = False

    def _setMeshNodeFromSel(self):
        sels = cmds.ls(sl=True)
        if not sels:
            return

        self.mesh_node = sels[0]

    def _setVtxsFromSel(self):
        sels = cmds.ls(sl=True, fl=True)
        if not sels:
            return

        vtxs = pm.polyListComponentConversion(sels, toVertex=True)

        if '.vtx[' not in vtxs[0]:
            return

        self.vtxs = vtxs
        self.paste_mesh = getMeshNameFromSelVtx()

    def _createSet(self):
        pm.select(self.vtxs)
        self.set = pm.sets(n='vtxset')

    def copy(self):
        self.__init__()
        self._setMeshNodeFromSel()

    def startPaste(self):
        self._setVtxsFromSel()

    def paste(self):
        self._createSet()
        if self.force_bind:
            bindPairModel(self.mesh_node, self.paste_mesh)
        copySkinWeight(self.mesh_node, self.set, influenceAssociation_=self.influenceAssociation)
        pm.delete(self.set)

    def selVtx(self):
        if self.vtxs:
            pm.select(self.vtxs)


def unbind(mesh):
    #skcs = [x.name() for x in listRelatedSkinClusters([mesh])]
    #for skc in skcs:
    #    cmds.skinCluster(skc, e=True, unbind=True)
    try:
        sels = cmds.ls(sl=True)
        cmds.select(mesh)
        mm.eval('doDetachSkin "2" { "3","0" };')
        cmds.select(sels)
    except Exception as e:
        print(e.message)


def exportWeight(mesh_node, xml_dir='', xml_name=''):
    skc = listRelatedSkinClusters([mesh_node])
    if skc:
        if not xml_name:
            xml_name = mesh_node
        return cmds.deformerWeights(
            xml_name + '_weight.xml',
            ex=True,
            format='XML',
            vc=True,
            sh=mesh_node,
            path=xml_dir,
            wp=20)
    else:
        return None


def exportWeightMulti(mesh_nodes, xml_dir='', unbind_mesh=False):
    export_meshes = []
    xml_files = []
    for mesh in mesh_nodes:
        xml_path = exportWeight(mesh, xml_dir)
        if xml_path is not None:
            xml_files.append(os.path.basename(xml_path))
            export_meshes.append(mesh)

            if unbind_mesh:
                unbind(mesh)
        else:
            print('no deformer {}'.format(mesh))
    return export_meshes, xml_files


def importWeight(mesh_node, xml_dir='', xml_file_name='', mode=0):
    mode_dict = {0: 'index', 1: 'nearest', 2: 'barycentric', 3: 'bilinear', 4: 'over'}
    if not xml_file_name:
        xml_file_name = mesh_node + '_weight.xml'

    # ダミージョイント作成（一旦前Weightを入れておくジョイント）
    #cmds.select(d=True)
    #tmp_joint = cmds.joint(p=(0, 0, 0))

    # 元のバインドは一旦解除
    skcs = listRelatedSkinClusters([mesh_node])
    if skcs:
        unbind(mesh_node)

    # ダミージョイントをバインド
    #cmds.select(mesh_node, tmp_joint)
    #new_skc = cmds.skinCluster(toSelectedBones=True)

    # xmlからインフルエンスジョイントを取得（自動でバインドしてくれない為）
    tree = et.parse(os.path.join(xml_dir, xml_file_name))
    root = tree.getroot()
    sources = []
    for value in root.iter('weights'):
        sources.append(value.attrib['source'])

    # xmlから取得したジョイントでバインド
    cmds.select(mesh_node, sources)
    #cmds.skinCluster(new_skc, e=True, addInfluence=sources, weight=0, lockWeights=True)
    cmds.skinCluster(toSelectedBones=True)
    #cmds.select(mesh_node)
    #cmds.skinPercent(skc, transformValue=[(tmp_joint, 1)])

    # deformerWeightsでWeightをimport
    shape = cmds.listRelatives(mesh_node, s=True)
    #cmds.deformer(mesh_node, type='skinCluster')
    print(xml_file_name, shape[0], mode_dict[mode], sources)
    cmds.deformerWeights(xml_file_name, im=True, m=mode_dict[mode], sh=shape[0], path=xml_dir, dv=1)

    # ダミージョイントをremove
    #cmds.skinCluster(mesh_node, e=True, g=tmp_joint, rm=True)
    #cmds.delete(tmp_joint)

    # 不使用ジョイントをremove
    #cmds.skinCluster(mesh_node, removeUnusedInfluence=True)

    # Normalize 完全な精度でimportされないので
    cmds.select(d=True)
    skcs = listRelatedSkinClusters([mesh_node])
    for skc in skcs:
        skc = skc.name()
        cmds.evalDeferred('cmds.skinPercent("{}", normalize=True)'.format(skc))

    return sources


def importWeightMulti(mesh_nodes, xml_dir, xml_files, import_mode=0):
    inful_joints = []
    for i in range(len(mesh_nodes)):
        # xmlは生成順に適用する（異なるメッシュの場合はメッシュ名からファイル名を取得できない為）
        try:
            inful_joints += importWeight(mesh_nodes[i], xml_dir, xml_files[i], mode=import_mode)
        except Exception as e:
            tb = sys.exc_info()[2]
            print('failed import: {} : {}'.format(mesh_nodes[i], e.with_traceback(tb)))
    return inful_joints


def copyJointLabel(joints):
    result_dict = {}
    for j in joints:
        result_dict[j] = [cmds.getAttr(j + '.side'), cmds.getAttr(j + '.type'), cmds.getAttr(j + '.otherType')]
    return result_dict


def pasteJointLabel(joints, copy_dict):
    for j in joints:
        j_name = j.split(':')[-1]
        j_name = j_name.split('|')[-1]
        if j_name in copy_dict:
            cmds.setAttr(j + '.side', copy_dict[j_name][0])
            cmds.setAttr(j + '.type', copy_dict[j_name][1])
            cmds.setAttr(j + '.otherType', copy_dict[j_name][2], type="string")
            print(j_name)


