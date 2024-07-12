# coding: utf-8

from __future__ import absolute_import
from __future__ import print_function

import codecs
import datetime
import itertools
import json
import math
import os
import sys
import time
import traceback
from collections import OrderedDict
from contextlib import contextmanager
from functools import wraps

import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim
import maya.api.OpenMaya as OpenMaya2

try:
    # Maya 2022-
    from builtins import str
    from builtins import range
    from builtins import object
    from importlib import reload
    from past.utils import old_div
except Exception:
    pass

dir_path = '/'.join(__file__.replace('\\', '/').split('/')[0:-1])
print(dir_path)

skinWeightCmd_py = f'{dir_path}/skinWeightCmd.py'

# skinweightコマンドプラグインのロード
plugins = [
    skinWeightCmd_py
]
plugin_results = []
for plugin in plugins:
    plugin_result = cmds.loadPlugin(plugin) if not cmds.pluginInfo(plugin, q=True, l=True) else False
    plugin_results.append(plugin_result)

print(f'{plugin_results} loaded')

def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{func.__name__} executed in: {elapsed_time:.6f} seconds")
        return result
    return wrapper

def get_maya_version():
    u"""mayaバージョンを取得
    :return: apiバージョン
    :rtype: int
    """

    return cmds.about(api=True)


def is_maya_batch():
    u"""バッチモードかどうかを判断
    :return: batchモードの場合はTrue, GUIモードの場合はFalse
    :rtype: bool
    """

    return cmds.about(batch=True)


@contextmanager
def waitCursorBlock():
    try:
        cmds.waitCursor(state=True)
        yield

    except:
        pass

    finally:
        cmds.waitCursor(state=False)


class JsonFile(object):
    u"""
    """

    @classmethod
    def read(cls, file_path):
        if not file_path:
            return {}

        if not os.path.isfile(file_path):
            return {}

        with codecs.open(file_path, 'r', 'utf-8') as f:
            try:
                data = json.load(f)
            except ValueError:
                data = {}

        return data

    @classmethod
    def write(cls, file_path, data):
        if not file_path:
            return

        dirname, basename = os.path.split(file_path)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)

        with codecs.open(file_path, 'w', 'utf-8') as f:
            json.dump(data, f, indent=4)
            f.flush()
            os.fsync(f.fileno())


class SkinClusterDataFile(JsonFile):
    u"""
    """

    data_type = 'skinClusterData'

    @classmethod
    def _get_file_infomation(cls):
        ret = OrderedDict()
        ret['file_information'] = OrderedDict()
        ret['file_information']['data_type'] = cls.data_type
        ret['file_information']['user'] = os.environ['USER']
        ret['file_information']['date'] = datetime.datetime.now().strftime("%Y/%m/%d-%H:%M:%S")

        return ret

    @classmethod
    def write(cls, file_path, data):
        write_data = cls._get_file_infomation()
        write_data.update(data)

        super(SkinClusterDataFile, cls).write(file_path, write_data)


class SkinClusterWeightData(object):
    def __init__(self, influenceIndices=None, influences=None, weights=None, components=None):
        if influenceIndices is not None:
            self.influenceIndices = influenceIndices

        if influences is not None:
            self.influences = influences

        if weights is not None:
            self.weights = weights

        if components is not None:
            self.components = components

    def __getitem__(self, item):
        if hasattr(self, item):
            return getattr(self, item)
        else:
            return None

    def _set_influenceIndices(self, influenceIndices):
        self._influenceIndices = influenceIndices

    def _get_influenceIndices(self):
        return self._influenceIndices[::]

    influenceIndices = property(_get_influenceIndices, _set_influenceIndices)

    def _set_influences(self, influences):
        self._influences = influences

    def _get_influences(self):
        return self._influences[::]

    influences = property(_get_influences, _set_influences)

    def _set_weights(self, weights):
        self._weights = weights

    def _get_weights(self):
        return self._weights[::]

    weights = property(_get_weights, _set_weights)

    def _set_components(self, components):
        self._components = flatten_components(components)

    def _get_components(self):
        return self._components[::]

    components = property(_get_components, _set_components)

    @property
    def numInfluences(self):
        if self._influences:
            return len(self._influences)
        else:
            return 0

    @property
    def numComponents(self):
        if self._components:
            return len(self._components)
        else:
            return 0

    @property
    def numWeights(self):
        if self._weights:
            return len(self._weights)
        else:
            return 0

    @property
    def numInfluencesFromWeights(self):
        if self._weights:
            return len(self._weights[0])
        else:
            return 0

    def get_maxInfluenceIndex(self):
        u"""インフルエンスインデックスの最大値を取得
        """

        return max(self.influenceIndices)

    def get_fillVacantWeights(self, weights=None):
        u"""空白インデックスを0.0で埋めたウェイトを取得
        """

        weights = weights[::] if weights else self.weights
        array_size = self.get_maxInfluenceIndex() + 1

        ret = []
        for weight in weights:
            _ = [0.0] * array_size
            for i, idx in enumerate(self.influenceIndices):
                _[idx] = weight[i]
            ret.append(_)

        return ret

    def get_remapTable(self, other):
        u"""インフルエンスインデックスのリマップテーブル
        self index to other index
        """

        if not isinstance(other, SkinClusterWeightData):
            return {}

        if self.numInfluences > other.numInfluences:
            return {}

        self_list = [get_MDagPath2(x) for x in self.influences]
        other_list = [get_MDagPath2(x) for x in other.influences]

        ret = {}
        for i, s_id in enumerate(self.influenceIndices):
            src_infl = self_list[i]
            if src_infl not in other_list:
                return {}

            ret[s_id] = other.influenceIndices[other_list.index(src_infl)]

        return ret

    def get_remapWeights(self, remapTable, arraySize):
        u"""リマップウェイトの取得
        self weights to other index
        """

        if not remapTable:
            return []

        ret = []
        for weight in self.weights:
            _ = [0.0] * arraySize
            for src_id, dst_id in remapTable.iteritems():
                _[dst_id] = weight[self.influenceIndices.index(src_id)]
            ret.append(_)

        return ret

    def is_same_influences(self, other):
        U"""インフルエンスが同じか確認
        """

        if not isinstance(other, SkinClusterWeightData):
            return False

        if self.numInfluences != other.numInfluences:
            return False

        if self.influenceIndices != other.influenceIndices:
            return False

        self_list = [get_MDagPath2(inf) for inf in self.influences]
        other_list = [get_MDagPath2(inf) for inf in other.influences]

        return self_list == other_list

    def asDict(self):
        u"""
        """

        ret = OrderedDict()
        ret['numInfluences'] = self.numInfluences
        ret['influences'] = self.influences
        ret['influenceIndices'] = self.influenceIndices
        ret['numComponents'] = self.numComponents
        ret['components'] = self.components
        ret['weights'] = self.weights

        return ret

    def setDict(self, data):
        u"""
        """

        if not data:
            return

        if 'influenceIndices' in data:
            self.influenceIndices = data['influenceIndices']

        if 'influences' in data:
            self.influences = data['influences']

        if 'weights' in data:
            self.weights = data['weights']

        if 'components' in data:
            self.components = data['components']


def clamp(minValue, maxValue, value):
    u"""数値をクランプ
    :param float minValue: 最小値
    :param float maxValue: 最大値
    :param float value: 元の数値
    :return: minValue, maxValueでクランプされた値
    :rtype: int / float
    """

    if minValue > maxValue:
        minValue, maxValue = maxValue, minValue

    return max(minValue, min(maxValue, value))


def getBarycentricCoordinate(p, a, b, c, roundDigits=6):
    u"""重心座標を取得

    :param MVector p: 変換する座標
    :param MVector a: 三角形頂点座標
    :param MVector b: 三角形頂点座標
    :param MVector c: 三角形頂点座標
    :param int roundDigits: 丸める小数点桁数
    :return: 三角形重心座標
    :rtype: [float, float, float]
    """

    norm = ((b - a) ^ (c - b)).normal()

    abc = norm * ((b - a) ^ (c - a))
    pbc = norm * ((b - p) ^ (c - p))
    pca = norm * ((c - p) ^ (a - p))

    u = round(pbc / abc, roundDigits)
    v = round(pca / abc, roundDigits)
    w = 1.0 - u - v

    return u, v, w


def get_MObject(nodeName):
    u"""MObjectを取得

    :param str nodeName: オブジェクト名
    :return: MObject
    :rtype: MObject
    """

    selList = OpenMaya.MSelectionList()
    selList.add(nodeName)
    m_obj = OpenMaya.MObject()
    selList.getDependNode(0, m_obj)

    return m_obj


def get_MDagPath(objectName):
    selList = OpenMaya.MSelectionList()
    selList.add(objectName)
    dag_path = OpenMaya.MDagPath()
    selList.getDagPath(0, dag_path)

    return dag_path


def get_shapeDagPath(dag_path):
    u"""
    """

    if not isinstance(dag_path, OpenMaya.MDagPath):
        return None

    if dag_path.apiType() not in [OpenMaya.MFn.kMesh, OpenMaya.MFn.kNurbsSurface, OpenMaya.MFn.kNurbsCurve]:
        dag_path.extendToShape()
        if dag_path.apiType() not in [OpenMaya.MFn.kMesh, OpenMaya.MFn.kNurbsSurface, OpenMaya.MFn.kNurbsCurve]:
            return None

    return dag_path


def get_MObject2(objectName):
    selList = OpenMaya2.MSelectionList()
    selList.add(objectName)

    return selList.getDependNode(0)


def get_MObjectComponent2(objectName):
    selList = OpenMaya2.MSelectionList()
    selList.add(objectName)

    return selList.getComponent(0)


def get_MDagPath2(objectName):
    selList = OpenMaya2.MSelectionList()
    selList.add(objectName)

    return selList.getDagPath(0)


def get_shapeDagPath2(dag_path):
    u"""
    """

    if not isinstance(dag_path, OpenMaya2.MDagPath):
        return None

    if dag_path.apiType() not in [OpenMaya2.MFn.kMesh, OpenMaya2.MFn.kNurbsSurface, OpenMaya2.MFn.kNurbsCurve]:
        dag_path.extendToShape()
        if dag_path.apiType() not in [OpenMaya2.MFn.kMesh, OpenMaya2.MFn.kNurbsSurface, OpenMaya2.MFn.kNurbsCurve]:
            return None

    return dag_path


def get_objects(objs):
    """オブジェクト名を取得
    """

    ret = []

    objs = cmds.ls(objs, o=True)
    for o in sorted(set(objs), key=objs.index):
        if cmds.objectType(o, isa='controlPoint'):
            ret.append(cmds.listRelatives(o, p=True, pa=True)[0])
        else:
            ret.append(o)

    return ret


def get_component_index(comp):
    u"""コンポーネントインデックスを取得
    :param str comp: コンポーネント名
    :return: コンポーネントインデックス
    :rtype: int
    """

    if '.f[' in comp or '.vtx[' in comp or '.e[' in comp or '.map[' in comp:
        return int(comp.rsplit(']', 1)[0].rsplit('[', 1)[-1])
    try:
        return int(cmds.attributeName(comp, s=True).rsplit(']', 1)[0].rsplit('[', 1)[-1])
    except:
        return None


def flatten_components(comps, asSingleIndex=True):
    u"""フラット化したコンポーネントリストを取得

    :param list comps: コンポーネントリスト
    :param bool asSingleIndex: Trueの場合はシングルインデックスコンポーネントを取得
    """

    if not comps:
        return []

    comps = cmds.ls(comps, fl=True)
    if not comps:
        return []

    if asSingleIndex:
        ret = []
        _ = {}
        for comp in comps:
            node = comp.split('.', 1)[0]
            compIndex = get_component_index(comp)
            if compIndex is None:
                continue

            if '.f[' in comp or '.vtx[' in comp or '.e[' in comp or '.map[' in comp:
                ret.append(comp)
                continue

            if node in _:
                ret.append('{}.cp[{}]'.format(_[node], compIndex))
            else:
                if cmds.objectType(node, isa='transform'):
                    shape = cmds.listRelatives(node, s=True, pa=True, ni=True)
                    if not shape:
                        continue

                    shape = shape[0]
                    if not cmds.objectType(shape, isa='controlPoint'):
                        continue

                    _[node] = shape
                    ret.append('{}.cp[{}]'.format(shape, compIndex))

                elif cmds.objectType(node, isa='controlPoint'):
                    _[node] = node
                    ret.append('{}.cp[{}]'.format(node, compIndex))

        _ = set(ret)
        return sorted(_,  key=ret.index)
    else:
        return comps


def get_object_components(obj, comps):
    if comps:
        shp = '{}.'.format(obj)
        par = cmds.listRelatives(obj, pa=1, p=1)
        trs = '{}.'.format(par[0]) if par else ''
        return [x for x in comps if x.startswith(trs) or x.startswith(shp)]


def reset_skinCluster_bindPreMatrix(**kwargs):
    u"""skinClusterノードのbindPreMatrixアトリビュートを更新
    skinClusterのバインド姿勢を変更しますので、influenceの姿勢を元に戻した状態で使用してください。
    """

    resetAllSkinClusters = kwargs.get('resetAllSkinClusters', kwargs.get('all', False))
    if resetAllSkinClusters:
        skinClusters = cmds.ls(type='skinCluster')
    else:
        nodes = kwargs.get('nodes', cmds.ls(sl=True))
        skinClusters = cmds.ls(nodes, type='skinCluster') or []

    for sc in skinClusters:
        connects = cmds.listConnections('{}.matrix'.format(sc), s=True, d=False, p=True, c=True)
        src = connects[1::2]
        dst = connects[0::2]
        for s, d in zip(src, dst):
            wim = cmds.getAttr('{}.wim'.format(s.split('.', 1)[0]))
            cmds.setAttr(d.replace('matrix', 'bindPreMatrix'), *wim, type='matrix')


def list_related_skinClusters(nodes):
    u"""
    """

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


def list_skinCluster_influences(nodes):
    if not nodes:
        return []

    skinClusters = cmds.ls(nodes, typ='skinCluster') or []
    if not skinClusters:
        return []

    plugs = ['{}.matrix'.format(sc) for sc in skinClusters]
    return cmds.listConnections(plugs, s=1, d=0) or []


def list_related_components_from_deformer(nodes):
    if not nodes:
        return []

    deformers = cmds.ls(nodes, type='geometryFilter')
    if not deformers:
        return

    sets = cmds.listConnections(deformers, s=False, d=True, type='objectSet')
    if not sets:
        return []

    ret = cmds.ls(cmds.sets(sets, q=True), fl=True)
    return sorted(set(ret[::]), key=ret.index)


def select_related_skinClusters(nodes):
    if not nodes:
        return

    skinClusters = list_related_skinClusters(nodes)
    if skinClusters:
        cmds.select(skinClusters, r=True)
    else:
        pass


def select_related_influences(nodes):
    if not nodes:
        return

    skinClusters = list_related_skinClusters(nodes)
    infls = list_skinCluster_influences(skinClusters)
    if infls:
        cmds.select(infls, r=True)
    else:
        pass


def get_skinCluster_maxInfluenceIndex(skinCluster):
    u"""
    """

    if not cmds.objExists(skinCluster):
        return None

    return int(
        cmds.listAttr('{}.matrix'.format(skinCluster), m=True)[-1].rsplit(']', 1)[0].rsplit('[', 1)[-1]
    )


def get_closestPoint(geometry='', ip=None, world=1):
    u"""
    """

    dagPath = get_shapeDagPath(get_MDagPath(geometry))
    if not dagPath:
        return None

    if ip is None:
        return None

    inPoint = OpenMaya.MPoint(*ip)
    outPoint = None
    space = OpenMaya.MSpace.kWorld if world else OpenMaya.MSpace.kObject
    typeId = dagPath.apiType()

    if typeId == OpenMaya.MFn.kMesh:
        meshFn = OpenMaya.MFnMesh(dagPath)
        outPoint = OpenMaya.MPoint()
        meshFn.getClosestPoint(inPoint, outPoint, space)

    elif typeId == OpenMaya.MFn.kNurbsSurface:
        srfFn = OpenMaya.MFnNurbsSurface(dagPath)
        u_util = OpenMaya.MScriptUtil()
        u_util.createFromDouble(0.0)
        u_ptr = u_util.asDoublePtr()
        v_util = OpenMaya.MScriptUtil()
        v_util.createFromDouble(0.0)
        v_ptr = v_util.asDoublePtr()
        outPoint = srfFn.closestPoint(inPoint, False, u_ptr, v_ptr, False, 1e-6, space)

    elif typeId == OpenMaya.MFn.kNurbsCurve:
        crvFn = OpenMaya.MFnNurbsCurve(dagPath)
        util = OpenMaya.MScriptUtil()
        util.createFromDouble(0.0)
        ptr = util.asDoublePtr()
        outPoint = crvFn.closestPoint(inPoint, False, ptr, 1e-6, space)

    return [outPoint.x, outPoint.y, outPoint.z]


def get_nearestComponent(geometry='', ip=None, world=1, point=0):
    u"""
    """

    dagPath = get_shapeDagPath(get_MDagPath(geometry))
    if not dagPath:
        return None

    if ip is None:
        return None

    typeId = dagPath.apiType()
    inPoint = OpenMaya.MPoint(*ip)
    space = OpenMaya.MSpace.kWorld if world else OpenMaya.MSpace.kObject

    distance = None
    nearestId = None
    nearestPoint = [0.0, 0.0, 0.0]

    if typeId == OpenMaya.MFn.kMesh:
        meshFn = OpenMaya.MFnMesh(dagPath)
        outPoint = OpenMaya.MPoint()
        util = OpenMaya.MScriptUtil()
        util.createFromInt(0)
        ptr = util.asIntPtr()
        meshFn.getClosestPoint(inPoint, outPoint, space, ptr)
        fIndex = util.getInt(ptr)
        vtxArray = OpenMaya.MIntArray()
        meshFn.getPolygonVertices(fIndex, vtxArray)
        vP = OpenMaya.MPoint()
        for cnt in range(vtxArray.length()):
            meshFn.getPoint(vtxArray[cnt], vP, space)
            if distance is None:
                distance = inPoint.distanceTo(vP)
                nearestId = vtxArray[cnt]
                nearestPoint = [vP.x, vP.y, vP.z]
            else:
                diff = inPoint.distanceTo(vP)
                if distance > diff:
                    distance = diff
                    nearestId = vtxArray[cnt]
                    nearestPoint = [vP.x, vP.y, vP.z]

    elif typeId == OpenMaya.MFn.kNurbsSurface:
        srf_iter = OpenMaya.MItSurfaceCV(dagPath)
        while not srf_iter.isDone():
            while not srf_iter.isRowDone():
                vP = srf_iter.position(space)
                if distance is None:
                    distance = inPoint.distanceTo(vP)
                    nearestId = srf_iter.index()
                    nearestPoint = [vP.x, vP.y, vP.z]
                else:
                    diff = inPoint.distanceTo(vP)
                    if distance > diff:
                        distance = diff
                        nearestId = srf_iter.index()
                        nearestPoint = [vP.x, vP.y, vP.z]
                srf_iter.next()
            srf_iter.nextRow()

    elif typeId == OpenMaya.MFn.kNurbsCurve:
        crv_iter = OpenMaya.MItCurveCV(dagPath)
        while not crv_iter.isDone():
            vP = crv_iter.position(space)
            if distance is None:
                distance = inPoint.distanceTo(vP)
                nearestId = crv_iter.index()
                nearestPoint = [vP.x, vP.y, vP.z]
            else:
                diff = inPoint.distanceTo(vP)
                if distance > diff:
                    distance = diff
                    nearestId = crv_iter.index()
                    nearestPoint = [vP.x, vP.y, vP.z]
            crv_iter.next()

    return nearestPoint if point else nearestId


def get_neighbour_components(targetObject, comp_id, **kwargs):
    u"""隣接コンポーネントを取得
    """

    # meshのみの対応
    method = kwargs.get('method', kwargs.get('m', 'connected_faces'))
    useMeshUV = kwargs.get('useMeshUV', kwargs.get('umuv', False))
    meshU = kwargs.get('meshU', kwargs.get('mu', True))
    meshV = kwargs.get('meshV', kwargs.get('mv', True))
    thresholdAngle = kwargs.get('thresholdAngle', kwargs.get('ta', 45))

    dag_path = get_shapeDagPath(get_MDagPath(targetObject))
    if not dag_path:
        return None

    meshFn = OpenMaya.MFnMesh(dag_path)
    mit = OpenMaya.MItMeshVertex(dag_path)
    util = OpenMaya.MScriptUtil()
    util.createFromInt(0)
    ptr = util.asIntPtr()
    mit.setIndex(comp_id, ptr)
    intArray = OpenMaya.MIntArray()
    ret = set()

    if method == 'connected_vertices':
        mit.getConnectedVertices(intArray)
        [ret.add(id_) for id_ in intArray]

    elif method == 'connected_edges':
        edgeIds = OpenMaya.MIntArray()
        mit.getConnectedEdges(edgeIds)
        int2ptr = util.asInt2Ptr()

        def _getInt0(x):
            return util.getInt2ArrayItem(x, 0, 0)

        def _getInt1(x):
            return util.getInt2ArrayItem(x, 0, 1)

        for edgeId in edgeIds:
            meshFn.getEdgeVertices(edgeId, int2ptr)
            ret.add(_getInt0(int2ptr))
            ret.add(_getInt1(int2ptr))

    elif method == 'connected_faces':
        faceIds = OpenMaya.MIntArray()
        mit.getConnectedFaces(faceIds)
        for faceId in faceIds:
            vIds = OpenMaya.MIntArray()
            meshFn.getPolygonVertices(faceId, vIds)
            for vId in vIds:
                ret.add(vId)

    if ret and useMeshUV:
        try:
            uvSetName = meshFn.currentUVSetName()
            uvPtr = util.asFloat2Ptr()
            mit.setIndex(comp_id, ptr)
            mit.getUV(uvPtr, uvSetName)

            def _getFloat0(x):
                return util.getFloat2ArrayItem(x, 0, 0)

            def _getFloat1(x):
                return util.getFloat2ArrayItem(x, 0, 1)

            piv_u = _getFloat0(uvPtr)
            piv_v = _getFloat1(uvPtr)

            diff_uvs = {}
            for comp in ret:
                mit.setIndex(comp, ptr)
                mit.getUV(uvPtr, uvSetName)
                u = _getFloat0(uvPtr)
                v = _getFloat1(uvPtr)

                # U,V(縦横)の角度は0～90°でカバーできるので正の数で扱う
                diff_uvs[comp] = OpenMaya.MVector(abs(u - piv_u), abs(v - piv_v), 0.0).normal()

            rad_thresholdAngle = math.radians(abs(thresholdAngle))  # 比較はラジアン角で行う。

            ret = set()
            if meshU:
                vec = OpenMaya.MVector(1.0, 0.0, 0.0)
                for k, v in diff_uvs.iteritems():
                    if rad_thresholdAngle > math.acos(clamp(-1.0, 1.0, vec * v)):
                        ret.add(k)

            if meshV:
                vec = OpenMaya.MVector(0.0, 1.0, 0.0)
                for k, v in diff_uvs.iteritems():
                    if rad_thresholdAngle > math.acos(clamp(-1.0, 1.0, vec * v)):
                        ret.add(k)

        except Exception as e:
            # traceback.print_exc()
            cmds.error(str(e))
            ret = []

    return ['{}.cp[{}]'.format(targetObject, vid) for vid in ret]


def get_closestPointData(base_pos, targetMesh, space=OpenMaya2.MSpace.kWorld):
    """closestPoint情報を取得

    pythonApi2.0を使用

    :param MPoint base_pos:
    :param str targetMesh:
    :param MSpace space:
    :return: closestPoint (MPoint), faceId (int), vertexPoints [int, int, int], vertexIds [MPoint, MPoint, MPoint]
    :rtype: tuple
    """

    # dagPathの取得
    dag_path = get_shapeDagPath2(get_MDagPath2(targetMesh))
    if not dag_path:
        return None

    # meshFunction
    mesh_fn = OpenMaya2.MFnMesh(dag_path)

    # closestPoint
    closest_pos, face_id = mesh_fn.getClosestPoint(base_pos, space=space)
    vIds = mesh_fn.getPolygonVertices(face_id)
    vertPoints = [[vId, mesh_fn.getPoint(vId, space=space)] for vId in vIds]

    nearestVerts = sorted(sorted(vertPoints, key=lambda x: x[1].distanceTo(closest_pos))[:3], key=lambda x: x[0])
    vert_ids, vert_points = [v[0] for v in nearestVerts], [v[1] for v in nearestVerts]

    return closest_pos, face_id, vert_points, vert_ids


def list_influences(skinCluster, **kwargs):
    u"""skinClusterのインフルエンスを取得

    :param str skinCluster: skinClusterノード名
    :keyword bool asObject: True - MDagPathオブジェクトを取得、False - ノード名(str)を取得
    :keyword bool longName: True - longName(fullPath) を取得, False - shortName(unique) を取得
    :return: (
        インフルエンスインデックス,
        インフルエンスオブジェクト
    )
    :rtype: tuple
    """

    asObject = kwargs.get('asObject', False)
    longName = kwargs.get('longName', True)

    if not cmds.objExists(skinCluster):
        return None

    scObj = get_MObject(skinCluster)
    skinClusterFn = OpenMayaAnim.MFnSkinCluster(scObj)
    influenceArray = OpenMaya.MDagPathArray()
    skinClusterFn.influenceObjects(influenceArray)
    numInfluences = influenceArray.length()

    indexList = [skinClusterFn.indexForInfluenceObject(influenceArray[i]) for i in range(numInfluences)]
    if asObject:
        influenceList = [influenceArray[i] for i in range(numInfluences)]

    else:
        if longName:
            influenceList = [influenceArray[i].fullPathName() for i in range(numInfluences)]
        else:
            influenceList = [influenceArray[i].partialPathName() for i in range(numInfluences)]

    return indexList, influenceList


def is_lockInfluence(node):
    plug = '{}.lockInfluenceWeights'.format(node)
    if not cmds.objExists(plug):
        return False

    return cmds.getAttr(plug)


def hold_influence(nodes):
    for node in nodes:
        plug = '{}.lockInfluenceWeights'.format(node)
        if not cmds.objExists(plug):
            continue

        cmds.setAttr(plug, True)


def unhold_influence(nodes):
    for node in nodes:
        plug = '{}.lockInfluenceWeights'.format(node)
        if not cmds.objExists(plug):
            continue

        cmds.setAttr(plug, False)


def togglehold_influence(nodes):
    for node in nodes:
        plug = '{}.lockInfluenceWeights'.format(node)
        if not cmds.objExists(plug):
            continue

        cmds.setAttr(plug, not cmds.getAttr(plug))


def get_affect_influences(clst, components):
    if not clst:
        return []

    if not components:
        return []

    sc_data = get_skinCluster_weights(clst, components)
    weights = sc_data.weights

    sumWeights = [0.0] * sc_data.numInfluences
    for i in range(sc_data.numInfluences):
        sumWeights[i] = sum([v[i] for v in weights])
    ret = []
    for infl, w in zip(sc_data.influences, sumWeights):
        if w > 1e-6:
            ret.append(infl)

    return ret


def get_unlock_weight_ratio(srcWeights, dstWeights, lockState):
    _size = len(lockState)
    srcLockSum = sum([srcWeights[i] for i in range(_size) if lockState[i]])
    dstLockSum = sum([dstWeights[i] for i in range(_size) if lockState[i]])
    if srcLockSum < 1.0:
        if dstLockSum < 1.0:
            return round((1.0 / (1.0 - srcLockSum)) / (1.0 / (1.0 - dstLockSum)), 3)
        else:
            return 0.0
    return 1.0


def get_skinCluster_weights(skinCluster, components):
    u"""skinClusterのウェイトを取得する

    :param str skinCluster: skinClusterノード名
    :param list components: コンポーネント名のリスト (vertex, cp, )
    :return: (
        indexList: インフルエンスインデックス
        inflList: インフルエンス名
        weightList: ウェイトリスト
        flatComponents: フラット化したコンポーネント名のリスト
    )

    :rtype: tuple
    """

    if not cmds.objExists(skinCluster):
        return []

    if not components:
        return []

    flat_comps = flatten_components(components)
    numComps = len(flat_comps)
    scObj = get_MObject(skinCluster)
    scFn = OpenMayaAnim.MFnSkinCluster(scObj)
    selList = OpenMaya.MSelectionList()
    [selList.add(x) for x in flat_comps]

    dagPath = OpenMaya.MDagPath()
    comp = OpenMaya.MObject()
    selList.getDagPath(0, dagPath, comp)

    weights = OpenMaya.MDoubleArray()
    util = OpenMaya.MScriptUtil()
    uIntPtr = util.asUintPtr()
    # ウェイトデータはindex順になる
    scFn.getWeights(dagPath, comp, weights, uIntPtr)
    weights = [w for w in weights]
    nInfls = util.getUint(uIntPtr)

    inflList = []
    indexList = []
    weightList = []

    dagPathArray = OpenMaya.MDagPathArray()
    scFn.influenceObjects(dagPathArray)
    for i in range(nInfls):
        # inflList.append(dagPathArray[i].fullPathName())
        inflList.append(dagPathArray[i].partialPathName())
        indexList.append(scFn.indexForInfluenceObject(dagPathArray[i]))

    for i in range(numComps):
        weightList.append(weights[i * nInfls:i * nInfls + nInfls])

    # ウェイトデータを入力コンポーネント順に並び替え
    sorted_comps = sorted(flat_comps, key=lambda x: get_component_index(x))
    weightList = [weightList[sorted_comps.index(x)] for x in flat_comps]

    retData = SkinClusterWeightData(indexList, inflList, weightList, flat_comps)

    return retData


def get_skinCluster_data(node):
    ret = OrderedDict()

    if not cmds.objExists(node):
        return ret

    skinClusterNodes = list_related_skinClusters(node)
    if not skinClusterNodes:
        return ret

    skinClusterNode = skinClusterNodes[0]
    components = cmds.ls('{}.cp[*]'.format(node))
    skinClusterData = get_skinCluster_weights(skinClusterNode, components)
    skinClusterAttrs = [
        'skinningMethod',
        'useComponents',
        'deformUserNormals',
        'normalizeWeights',
        'weightDistribution',
        'maxInfluences',
        'maintainMaxInfluences',
    ]

    ret['geometry'] = node
    ret['skinCluster'] = skinClusterNode
    ret['numInfluences'] = skinClusterData.numInfluences
    ret['influences'] = skinClusterData.influences
    ret['influenceIndices'] = skinClusterData.influenceIndices
    ret['numComponents'] = skinClusterData.numComponents
    ret['skinClusterAttributes'] = OrderedDict()
    for attr in skinClusterAttrs:
        ret['skinClusterAttributes'][attr] = cmds.getAttr('{}.{}'.format(skinClusterNode, attr))
    ret['weights'] = skinClusterData.weights

    return ret


def set_skinCluster_weights(node, skinClusterData):
    if not cmds.objExists(node):
        cmds.warning('{} is not found.'.format(node))
        return

    skinClusterNodes = list_related_skinClusters(node)
    if not skinClusterNodes:
        cmds.warning('Nothing related skinCluster node.')
        return

    skinClusterNode = skinClusterNodes[0]
    components = cmds.ls('{}.cp[*]'.format(node), fl=True)

    infls = list_skinCluster_influences(skinClusterNode)
    numInfluences = len(infls)

    if numInfluences != skinClusterData['numInfluences']:
        cmds.warning('Missing influence count.')
        return

    if len(components) != skinClusterData['numComponents']:
        cmds.warning('Missing component count.')
        return

    for i, w in enumerate(skinClusterData['weights']):
        cmds.setAttr('{}.wl[{}].w[0:{}]'.format(skinClusterNode, i, numInfluences - 1), *w, size=numInfluences)


def write_skinClusterData(node, file_path):
    skinClusterData = get_skinCluster_data(node)
    if not skinClusterData:
        return

    SkinClusterDataFile.write(file_path, skinClusterData)
    print('Write: {}'.format(file_path))


def read_skinClusterData(file_path):
    read_data = SkinClusterDataFile.read(file_path)
    if not read_data:
        return {}

    if 'file_information' not in read_data:
        return {}

    if 'data_type' not in read_data['file_information']:
        return {}

    if read_data['file_information']['data_type'] != SkinClusterDataFile.data_type:
        return {}

    print('Read: {}'.format(file_path))
    return read_data


def bind_by_skinClusterData(node, skinClusterData, **kwargs):
    """
    """

    rebind = kwargs.get('rebind', False)

    if not cmds.objExists(node):
        return

    skinClusters = list_related_skinClusters(node)
    if skinClusters:
        if rebind:
            cmds.skinCluster(node, e=True, unbind=True)
        else:
            return

    # geometry = skinClusterData['geometry']
    influences = skinClusterData['influences']
    attrs = skinClusterData['skinClusterAttributes']

    # smooth bind
    skinClusterNode = cmds.skinCluster(
        influences,
        node,
        toSelectedBones=True,
        bindMethod=attrs['skinningMethod'],
        normalizeWeights=attrs['normalizeWeights'],
        weightDistribution=attrs['weightDistribution'],
        maximumInfluences=attrs['maxInfluences'],
        obeyMaxInfluences=attrs['maintainMaxInfluences'],
        dropoffRate=4,
        removeUnusedInfluence=False,
        name='{}_skinCluster'.format(node.replace('|', '__'))
    )[0]

    # normalizeWeights: Off
    cmds.skinCluster(skinClusterNode, e=True, normalizeWeights=0)

    set_skinCluster_weights(node, skinClusterData)

    # normalizeWeights: On
    cmds.skinCluster(skinClusterNode, e=True, normalizeWeights=1)


def export_skinClusterWeights(nodes, export_directory):
    if not nodes:
        return

    bindNodes = [node for node in nodes if list_related_skinClusters(node)]

    if not bindNodes:
        return

    if not os.path.isdir(export_directory):
        os.makedirs(export_directory)

    ret = []
    for node in bindNodes:
        basename = '{}.json'.format(node).replace('|', '__').replace(':', '_')
        export_file = os.path.join(export_directory, basename).replace(os.sep, '/')

        # print 'Export: {}'.format(export_file)
        write_skinClusterData(node, export_file)

        ret.append(export_file)

    return ret


def import_skinClusterWeights(skinClusterDataFiles):
    if not skinClusterDataFiles:
        return

    importedGeometries = []
    for f in skinClusterDataFiles:
        if not os.path.isfile(f):
            continue

        read_data = read_skinClusterData(f)
        if not read_data:
            continue

        geometry = read_data['geometry']
        # print 'Import: {} / {}'.format(geometry, f)
        bind_by_skinClusterData(geometry, read_data, rebind=True)

        importedGeometries.append(geometry)

    return importedGeometries


def get_weight_from_componentID(targetObject, comp_id):
    u"""ジオメトリの頂点IDからウェイトを取得

    :param str targetObject: skinClusterが設定されているジオメトリ名
    :param int comp_id: コンポーネントID(vtx, cp)
    """

    skinClusters = list_related_skinClusters(targetObject)
    if not skinClusters:
        return []

    skinClusterNode = skinClusters[0]
    skinClusterData = get_skinCluster_weights(skinClusterNode, '{}.cp[{}]'.format(targetObject, comp_id))

    return skinClusterData.weights[0]


def get_weight_from_nearestComponent(targetObject, base_pos, world=True):
    u"""最近傍頂点のウェイトを取得
    :param str targetObject: skinClusterが設定されているジオメトリ名
    :param int comp_id: コンポーネントID(vtx, cp)
    """

    skinClusters = list_related_skinClusters(targetObject)
    if not skinClusters:
        return []

    skinClusterNode = skinClusters[0]
    comp_id = get_nearestComponent(targetObject, base_pos, world=world, point=False)
    skinClusterData = get_skinCluster_weights(skinClusterNode, '{}.cp[{}]'.format(targetObject, comp_id))

    return skinClusterData.weights[0]


def get_weight_from_closestPoint(targetObject, base_pos, world=True):
    u"""最近傍位置(face上の位置)のウェイトを取得(meshの場合のみ有効)
    :param str targetObject: skinClusterが設定されているジオメトリ名
    :param int comp_id: コンポーネントID(vtx, cp)
    """

    skinClusters = list_related_skinClusters(targetObject)
    if not skinClusters:
        return []

    base_pos = OpenMaya2.MPoint(*base_pos)

    skinClusterNode = skinClusters[0]
    space = OpenMaya2.MSpace.kWorld if world else OpenMaya2.MSpace.kObject
    closest_pos, face_id, vert_points, vert_ids = get_closestPointData(base_pos, targetObject, space=space)
    bary = getBarycentricCoordinate(closest_pos, *vert_points)
    comps = ['{}.cp[{}]'.format(targetObject, v) for v in vert_ids]
    skinClusterData = get_skinCluster_weights(skinClusterNode, comps)

    ret = []
    for i in range(skinClusterData.numInfluences):
        sumWeight = 0.0
        for wl, bw in zip(skinClusterData.weights, bary):
            sumWeight += wl[i] * bw
        ret.append(sumWeight)

    return ret


def get_weight_from_neighbourComponents(targetObject, comp_id, **kwargs):
    u"""ジオメトリの頂点IDからウェイトを取得

    :param str targetObject: skinClusterが設定されているジオメトリ名
    :param int comp_id: コンポーネントID(vtx, cp)
    """

    method = kwargs.get('method', kwargs.get('m', 'connected_faces'))
    useMeshUV = kwargs.get('useMeshUV', kwargs.get('umuv', False))
    meshU = kwargs.get('meshU', kwargs.get('mu', True))
    meshV = kwargs.get('meshV', kwargs.get('mv', True))
    thresholdAngle = kwargs.get('thresholdAngle', kwargs.get('ta', 45))

    skinClusters = list_related_skinClusters(targetObject)
    if not skinClusters:
        return []

    neighbour_components = get_neighbour_components(
        targetObject, comp_id,
        method=method, useMeshUV=useMeshUV, meshU=meshU, meshV=meshV, thresholdAngle=thresholdAngle)
    if not neighbour_components:
        return []

    skinClusterNode = skinClusters[0]
    skinClusterData = get_skinCluster_weights(skinClusterNode, neighbour_components)

    # return skinClusterData.get_fillVacantWeights()
    return skinClusterData.weights


def get_selected_clst_and_components():
    u"""
    """

    sels = cmds.ls(os=True, fl=True)
    selObjects = get_objects(sels)
    if not selObjects:
        return

    histories = cmds.listHistory(selObjects, interestLevel=1) or []
    geos = cmds.ls(histories, type='controlPoint', ni=1)
    geos = sorted(set(geos), key=geos.index)
    if len(geos) < 1:
        return

    comps = flatten_components(sels)
    if not comps:
        comps = cmds.ls('{}.cp[*]'.format(geos[0]))

    clst = list_related_skinClusters(geos[0])

    return (clst[0], comps)


def normalize_weights_from_selection():
    u"""normalize weights
    """

    clst_and_comps = get_selected_clst_and_components()
    if not clst_and_comps:
        return

    normalize_weights(*clst_and_comps)


def normalize_weights(clst, comps):
    u"""normalize weights
    """

    if not cmds.objExists(clst):
        return

    with waitCursorBlock():
        cmds.setAttr('{}.normalizeWeights'.format(clst), 1)
        cmds.skinPercent(clst, comps, normalize=True)

def normalize_list(numbers):
    u"""リストをノーマライズ
    """
    total = sum(numbers)
    if total == 0:
        raise ValueError("The sum of the list elements is zero, cannot normalize.")
    return [num / total for num in numbers]

def find_indices(input_list, value):
    u"""
    同じ値があってもそれぞれのindexを取得
    """
    return [index for index, element in enumerate(input_list) if element == value]

def sort_numbers(numbers):
    u"""
    昇順、降順で返す
    """
    ascending = sorted(numbers)
    descending = sorted(numbers, reverse=True)
    return ascending, descending

def prune_weights(clst, comps, prune_weights=0.01):
    u"""prune weights
    """

    if not cmds.objExists(clst):
        return

    with waitCursorBlock():
        # unhold
        hold_stat = {}
        influences = cmds.listConnections('{}.matrix'.format(clst), s=1, d=0) or []
        for infl in influences:
            plug = '{}.lockInfluenceWeights'.format(infl)
            if not cmds.objExists(plug):
                continue

            v = cmds.getAttr(plug)
            if v:
                hold_stat[plug] = v
                cmds.setAttr(plug, False)

        # cmds.setAttr('{}.normalizeWeights'.format(clst), 0)
        cmds.skinPercent(clst, comps, pruneWeights=pruneWeights, normalize=True)
        # cmds.setAttr('{}.normalizeWeights'.format(clst), 1)

        # hold状態を再設定
        for k, v in hold_stat.iteritems():
            cmds.setAttr(k, v)

@measure_time
def round_weights(skincluster, comps, roundDigits=3):
    u"""round weights
    """

    if not cmds.objExists(skincluster):
        return

    index_list, infl_list = list_influences(skincluster, as_object=False, long_name=False)
    if len(infl_list) < 2:
        return

    eps = 0.1 ** (roundDigits + 1)
    mind = 0.1 ** roundDigits

    comps = cmds.ls(comps, fl=True)
    # print('comps', comps)

    sel_list = OpenMaya.MSelectionList()
    [sel_list.add(x) for x in comps]
    dag_path = OpenMaya.MDagPath()
    comps_obj = OpenMaya.MObject()
    sel_list.getDagPath(0, dag_path, comps_obj)

    sc_obj = get_MObject(skincluster)
    sc_fn = OpenMayaAnim.MFnSkinCluster(sc_obj)

    current_weights = OpenMaya.MDoubleArray()
    infls = OpenMaya.MDagPathArray()
    util = OpenMaya.MScriptUtil()
    int_ptr = util.asUintPtr()
    sc_fn.influenceObjects(infls)
    num_infls = infls.length()

    sc_fn.getWeights(dag_path, comps_obj, current_weights, int_ptr)
    current_weights = [v for v in current_weights]
    set_weights = OpenMaya.MDoubleArray()

    for i in range(len(comps)):
        comp_weights = current_weights[i * num_infls: i * num_infls + num_infls]

        # Round Weights
        comp_set_weights, comp_diff_weights = [], []
        for j in range(num_infls):
            w0 = comp_weights[j]
            w = round(w0, roundDigits)
            comp_set_weights.append(w)
            comp_diff_weights.append(w0 - w)

        comp_weights_sum = sum(comp_weights)
        comp_set_weights_sum = sum(comp_set_weights)

        if abs(comp_weights_sum - 1.0) > 1e-08:
            comp_set_weights_sum = 0.0
            for j in range(num_infls):
                w0 = comp_weights[j] / comp_weights_sum
                w = round(w0, roundDigits)
                comp_set_weights[j] = w
                comp_diff_weights[j] = w0 - w
                comp_set_weights_sum += w

        if 1.0 - comp_set_weights_sum > eps:
            d = max(comp_diff_weights)
            j = comp_diff_weights.index(d)
            comp_set_weights[j] += mind

        elif 1.0 - comp_set_weights_sum < -eps:
            d = min(comp_diff_weights)
            j = comp_diff_weights.index(d)
            comp_set_weights[j] -= mind

        if sum(comp_set_weights) != 1.0:
            # _eps = round(0.1 ** roundDigits, roundDigits)
            search_comp_set_weights = [round(sw, roundDigits) for sw in comp_set_weights if not sw != 0]
            set_weights_list = [round(sw, roundDigits) for sw in comp_set_weights]
            max_sw = max(search_comp_set_weights)
            max_sw_idx = set_weights_list.index(max_sw)
            if sum(comp_set_weights) < 1.0:
                dif_val = 1.0 - sum(comp_set_weights)
                comp_set_weights[max_sw_idx] = comp_set_weights[max_sw_idx] + dif_val
            elif sum(comp_set_weights) > 1.0:
                dif_val = sum(comp_set_weights) - 1.0
                comp_set_weights[max_sw_idx] = comp_set_weights[max_sw_idx] - dif_val

        [set_weights.append(v) for v in comp_set_weights]


    cmds.skinWeightCmd(
        geometry=dag_path.partialPathName(),
        components=comps,
        skinCluster=skincluster,
        weights=set_weights
    )

    # prune weights を実行してウェイトが0.0のインデックスを除去
    prune_weights(skincluster, comps, prune_weights=eps)

@measure_time
def smooth_weights(**kwargs):
    geometry = kwargs.get('geometry', kwargs.get('geo', None))
    comps = kwargs.get('components', kwargs.get('comps', None))
    blend = kwargs.get('blend', kwargs.get('b', 0.2))
    keepLock = kwargs.get('keepLock', kwargs.get('kl', False))
    neighbourMethod = kwargs.get('neighbourMethod', kwargs.get('nm', 'connected_faces'))
    useMeshUV = kwargs.get('useMeshUV', kwargs.get('umuv', False))
    meshU = kwargs.get('meshU', kwargs.get('mu', True))
    meshV = kwargs.get('meshV', kwargs.get('mv', True))
    thresholdAngle = kwargs.get('thresholdAngle', kwargs.get('ta', 45))

    showProgress = kwargs.get('showProgress', kwargs.get('sp', False))

    blend = clamp(0.0, 1.0, blend)
    rest = 1.0 - blend

    def _get_target(objs):
        histories = cmds.listHistory(objs, interestLevel=1) or []
        geos = cmds.ls(histories, type='controlPoint', ni=1)
        geos = sorted(set(geos), key=geos.index)
        if len(geos) < 1:
            return None

        clst = list_related_skinClusters(geos[0])
        if not clst:
            return None

        return (geos[0], clst[0])

    sels = cmds.ls(os=True, fl=True)
    selObjects = get_objects(sels)

    if not geometry:
        _tg = _get_target(selObjects)
        if _tg is None:
            cmds.error('[Failed Smoth Weights] Invalid smooth weight geometry.')
            return
        geometry, clst = _tg

    if not all([geometry, clst]):
        if geometry:
            clst = list_related_skinClusters(geometry)
            if not clst:
                return
            clst = clst[0]

    if cmds.objectType(geometry, isa='transform'):
        geometry = cmds.listRelatives(geometry, s=True, ni=True, pa=True)[0]

    influenceIndexList, influenceList = list_influences(clst)
    # clst_data = SkinClusterWeightData(influenceIndices=influenceIndexList, influences=influenceList)

    maxInfluenceNumber = get_skinCluster_maxInfluenceIndex(clst)
    setSize = maxInfluenceNumber + 1
    w_slice = '[0:{}]'.format(maxInfluenceNumber)
    wKwargs = {'s': setSize}

    lockStateList = None
    if keepLock:
        lockStateList = cmds.getAttr('{}.lockWeights{}'.format(clst, w_slice))

    if not comps:
        comps = get_object_components(geometry, sels)

    if not comps:
        comps = cmds.ls('{}.cp[*]'.format(geometry))

    flat_components = flatten_components(comps)
    comps = [get_component_index(x) for x in flat_components]

    sel_list = OpenMaya.MSelectionList()
    [sel_list.add(x) for x in flat_components]
    dag_path = OpenMaya.MDagPath()
    comps_obj = OpenMaya.MObject()
    sel_list.getDagPath(0, dag_path, comps_obj)
    setWeights = OpenMaya.MDoubleArray()

    with waitCursorBlock():
        # 編集前のウェイトを取得
        original_weights = {idx: cmds.getAttr('{}.wl[{}].w{}'.format(clst, idx, w_slice)) for idx in comps}

        # 平均ウェイトを取得
        average_weights = {}
        for idx in comps:
            neighbour_comps = get_neighbour_components(
                geometry, idx,
                method=neighbourMethod, useMeshUV=useMeshUV, meshU=meshU, meshV=meshV, thresholdAngle=thresholdAngle)

            # 隣接コンポーネントが見つからない場合はオリジナルを設定
            if not neighbour_comps:
                average_weights[idx] = original_weights[idx]
                continue

            neighbour_comp_ids = [get_component_index(comp) for comp in neighbour_comps]
            neighbour_weights = [cmds.getAttr('{}.wl[{}].w{}'.format(clst, ncIdx, w_slice)) for ncIdx in neighbour_comp_ids]
            # neighbour_weights = get_weight_from_neighbourComponents(geometry, idx, method=neighbourMethod)
            numNeighbours = len(neighbour_weights)
            averageWeight = []
            for i in range(setSize):
                sum_value = 0.0
                for componentWeights in neighbour_weights:
                    sum_value += componentWeights[i]
                averageWeight.append(sum_value / numNeighbours)
            average_weights[idx] = averageWeight

    # ウェイト設定
    def _set_weights(idx):
        src_weight = average_weights[idx]
        dst_weight = original_weights[idx]
        if src_weight == dst_weight:
            return

        unlock_weight_ratio = get_unlock_weight_ratio(src_weight, dst_weight, lockStateList) if keepLock else 1.0
        comp_set_weights = None
        if blend < 1.0:
            if keepLock:
                comp_set_weights = [dst_weight[i] if lockStateList[i] else (dst_weight[i] * rest + src_weight[i] * blend * unlock_weight_ratio) for i in range(setSize)]
            else:
                comp_set_weights = [dst_weight[i] * rest + src_weight[i] * blend for i in range(setSize)]
        else:
            if keepLock:
                comp_set_weights = [dst_weight[i] if lockStateList[i] else (src_weight[i] * unlock_weight_ratio) for i in range(setSize)]
            else:
                comp_set_weights = src_weight[::]

        if comp_set_weights:
            cmds.skinWeightCmd(
                geometry=dag_path.partialPathName(),
                components=[f'{dag_path.partialPathName()}.vtx[{idx}]'],
                skinCluster=clst,
                weights=comp_set_weights
            )

            # cmds.setAttr('{}.wl[{}].w{}'.format(clst, idx, w_slice), *setWeights, **wKwargs)

    # progress window 表示
    if showProgress and not is_maya_batch():
        numComps = len(comps)
        progress = 0.0
        cmds.progressWindow(t='Transfer Weights', pr=int(progress), st='', ii=True, min=0, max=100)

        try:
            for cnt, compIndex in enumerate(comps):
                if showProgress:
                    progress = ((cnt + 1) * 100.0) / (numComps)
                    cmds.progressWindow(e=True, pr=int(progress), st='progress : [ {} / {} ]'.format(cnt, numComps))

                    _set_weights(compIndex)

                    if cmds.progressWindow(q=True, ic=True):
                        break

            normalize_weights(clst, flat_components)

        except Exception as e:
            # traceback.print_exc()
            cmds.error(str(e))

        finally:
            if showProgress:
                cmds.progressWindow(ep=1)

    else:
        [_set_weights(compIndex) for compIndex in comps]
        normalize_weights(clst, flat_components)

@measure_time
def transfer_weights(**kwargs):
    src = kwargs.get('source', kwargs.get('src', None))
    dst = kwargs.get('destination', kwargs.get('dst', None))
    comps = kwargs.get('components', kwargs.get('comps', None))  # destination components
    method = kwargs.get('method', kwargs.get('m', 'closestpoint')).lower()  # index or nearestcomponent or closestpoint
    world = kwargs.get('world', kwargs.get('ws', True))
    keepLock = kwargs.get('keepLock', kwargs.get('kl', False))
    blend = kwargs.get('blend', kwargs.get('b', 1.0))
    rest = 1.0 - blend
    showProgress = kwargs.get('showProgress', kwargs.get('sp', False))

    def _get_target(objs):
        histories = cmds.listHistory(objs, interestLevel=1) or []
        geos = cmds.ls(histories, type='controlPoint', ni=1)
        geos = sorted(set(geos), key=geos.index)
        if len(geos) < 2:
            return None

        src_clst = list_related_skinClusters(geos[0])
        if not src_clst:
            return None

        dst_clst = list_related_skinClusters(geos[1])
        if not dst_clst:
            return None

        return (geos[0], geos[1], src_clst[0], dst_clst[0])

    _methods = ['index', 'nearest', 'nearestcomponent', 'closest', 'closestpoint']
    if method not in _methods:
        cmds.error('[Failed Transfer Weights] \'{}\' is Invalid transfer method.'.format(method))
        return

    src_clst = None
    dst_clst = None

    sels = cmds.ls(os=True, fl=True)
    selObjects = get_objects(sels)

    if not src or not dst:
        _tg = _get_target(selObjects)
        if _tg is None:
            cmds.error('[Failed Transfer Weights] Invalid transfer geometries.')
            return
        src, dst, src_clst, dst_clst = _tg

    if not all([src, dst, src_clst, dst_clst]):
        if src:
            src_clsts = list_related_skinClusters(src)
            if not src_clsts:
                return
            src_clst = src_clsts[0]

        if dst:
            dst_clsts = list_related_skinClusters(dst)
            if not dst_clsts:
                return
            dst_clst = dst_clsts[0]

        if src == dst:
            cmds.error('[Failed Transfer Weights] src and dst is same object.')
            return

        if src_clst == dst_clst:
            cmds.error('[Failed Transfer Weights] src_clst and dst_clst is same object.')
            return

        if not all([src, dst, src_clst, dst_clst]):
            cmds.error('[Failed Transfer Weights] Invalid transfer geometries.')
            return

    if cmds.objectType(src, isa='transform'):
        src = cmds.listRelatives(src, s=True, ni=True, pa=True)[0]

    if cmds.objectType(dst, isa='transform'):
        dst = cmds.listRelatives(dst, s=True, ni=True, pa=True)[0]

    src_influenceIndexList, src_influenceList = list_influences(src_clst)
    src_data = SkinClusterWeightData(influenceIndices=src_influenceIndexList, influences=src_influenceList)

    dst_influenceIndexList, dst_influenceList = list_influences(dst_clst)
    dst_data = SkinClusterWeightData(influenceIndices=dst_influenceIndexList, influences=dst_influenceList)

    remapTable = src_data.get_remapTable(dst_data)
    if not remapTable:
        cmds.error('[Failed Transfer Weights] Found uncontain influences.')
        return

    maxInfluenceNumber = get_skinCluster_maxInfluenceIndex(dst_clst)
    setSize = maxInfluenceNumber + 1
    w_slice = '[0:{}]'.format(maxInfluenceNumber)
    wKwargs = {'s': setSize}

    lockStateList = None
    if keepLock:
        lockStateList = cmds.getAttr('{}.lockWeights{}'.format(dst_clst, w_slice))

    if not comps:
        comps = get_object_components(dst, sels)

    if not comps:
        comps = cmds.ls('{}.cp[*]'.format(dst))

    flat_components = flatten_components(comps)
    comps = [get_component_index(x) for x in flat_components]

    def _get_remapWeight(weights, remapTable, arraySize):
        _tmp = [0.0] * arraySize
        for sID, dID in remapTable.iteritems():
            _tmp[dID] = weights[src_influenceIndexList.index(sID)]
        return _tmp

    # ウェイト取得方法の設定
    if method == 'index':
        # コンポーネントＩＤのウェイトを取得
        def _get_weights(idx):
            return get_weight_from_componentID(src, idx)

    elif method in ['nearest', 'nearestcomponent']:
        # 近接頂点のウェイトを取得
        def _get_weights(idx):
            pos = cmds.xform('{}.cp[{}]'.format(dst, idx), q=True, t=True, ws=world)
            return get_weight_from_nearestComponent(src, pos, world=world)

    elif method in ['closest', 'closestpoint']:
        # 近接点(面上)のウェイトを取得
        def _get_weights(idx):
            pos = cmds.xform('{}.cp[{}]'.format(dst, idx), q=True, t=True, ws=world)
            return get_weight_from_closestPoint(src, pos, world=world)

    # ウェイト設定
    def _set_weights(idx):
        src_weight = _get_remapWeight(_get_weights(idx), remapTable, setSize)
        dst_weight = cmds.getAttr('{}.wl[{}].w{}'.format(dst_clst, idx, w_slice))
        unlock_weight_ratio = get_unlock_weight_ratio(src_weight, dst_weight, lockStateList) if keepLock else 1.0
        setWeights = None
        if blend < 1.0:
            if keepLock:
                setWeights = [dst_weight[i] if lockStateList[i] else (dst_weight[i] * rest + src_weight[i] * blend * unlock_weight_ratio) for i in range(setSize)]
            else:
                setWeights = [dst_weight[i] * rest + src_weight[i] * blend for i in range(setSize)]
        else:
            if keepLock:
                setWeights = [dst_weight[i] if lockStateList[i] else (src_weight[i] * unlock_weight_ratio) for i in range(setSize)]
            else:
                setWeights = src_weight[::]

        if setWeights:
            cmds.setAttr('{}.wl[{}].w{}'.format(dst_clst, idx, w_slice), *setWeights, **wKwargs)

    # progress window 表示
    if showProgress and not is_maya_batch():
        numComps = len(comps)
        progress = 0.0
        cmds.progressWindow(t='Transfer Weights', pr=int(progress), st='', ii=True, min=0, max=100)

        try:
            for cnt, compIndex in enumerate(comps):
                if showProgress:
                    progress = ((cnt + 1) * 100.0) / (numComps)
                    cmds.progressWindow(e=True, pr=int(progress), st='progress : [ {} / {} ]'.format(cnt, numComps))

                    _set_weights(compIndex)

                    if cmds.progressWindow(q=True, ic=True):
                        break

            normalize_weights(dst_clst, flat_components)

        except Exception as e:
            traceback.print_exc()
            cmds.error(str(e))

        finally:
            if showProgress:
                cmds.progressWindow(ep=1)

    else:
        [_set_weights(compIndex) for compIndex in comps]
        normalize_weights(dst_clst, flat_components)

@measure_time
def set_component_weights(skinCluster, target_components, src_data, **kwargs):
    u"""skinClusterのウェイトを設定

    :param str skinCluster: skinClusterノード名
    :param list target_components: ウェイトを更新するコンポーネント名のリスト
    :param SkinClusterWeightData src_data: 設定ウェイトデータ
    :keyword bool keepLock: ロックされているインフルエンスのウェイトを保持
    :keyword float blend: 元のウェイトとの合成割合(1.0の場合は置き換え) : 0.0 ～ 1.0
    :keyword bool useFirst: 設定ウェイト値に0番目のウェイト値を使用する
    :keyword bool average: 設定ウェイト値に平均値のウェイト値を使用する
    """

    keepLock = kwargs.get('keepLock', False)
    blend = clamp(0.0, 1.0, kwargs.get('blend', 1.0))
    rest = 1.0 - blend
    useFirst = kwargs.get('useFirst', False)
    average = kwargs.get('average', False)

    if not cmds.objExists(skinCluster):
        cmds.error('Not found skinCluster node.')
        return

    if not target_components:
        cmds.error('Invalid target_components argument.')
        return

    if not isinstance(src_data, SkinClusterWeightData):
        cmds.error('Invalid src data.')
        return

    dst_data = get_skinCluster_weights(skinCluster, target_components)
    if not (useFirst or average):
        if src_data.numComponents < dst_data.numComponents:
            cmds.error(u'[Copy Failed] Too many copy target components.')
            return

    remapTable = src_data.get_remapTable(dst_data)
    if not remapTable:
        cmds.error('found uncontain influences.')
        return

    dst_maxInfluenceIndex = dst_data.get_maxInfluenceIndex()
    setSize = dst_maxInfluenceIndex + 1
    w_slice = '[0:{}]'.format(setSize - 1)
    wKwargs = {'s': setSize}

    # weight remap src_infl to dst_infl
    src_weights = src_data.get_remapWeights(remapTable, setSize)

    # useFirst, average 設定の場合はweightリストを1つだけ用意
    # １つのウェイトを対象コンポーネント全てに適用する。
    singleSourceWeights = None
    with waitCursorBlock():
        if useFirst:
            singleSourceWeights = src_weights[0][::]

        else:
            if average:
                averageWeight = []
                for i in range(len(src_weights[0])):
                    sum_value = 0.0
                    for src_weight in src_weights:
                        sum_value += src_weight[i]
                    averageWeight.append(sum_value / len(src_weights))
                singleSourceWeights = averageWeight[::]

    lockStateList = None
    if keepLock:
        lockStateList = cmds.getAttr('{}.lockWeights{}'.format(skinCluster, w_slice))

    # ウェイト設定
    def _set_weights(idx, src_weight):
        dst_weight = cmds.getAttr('{}.wl[{}].w{}'.format(skinCluster, idx, w_slice))
        unlock_weight_ratio = get_unlock_weight_ratio(src_weight, dst_weight, lockStateList) if keepLock else 1.0
        setWeights = None
        if blend < 1.0:
            if keepLock:
                setWeights = [dst_weight[i] if lockStateList[i] else (dst_weight[i] * rest + src_weight[i] * blend * unlock_weight_ratio) for i in range(setSize)]
            else:
                setWeights = [dst_weight[i] * rest + src_weight[i] * blend for i in range(setSize)]
        else:
            if keepLock:
                setWeights = [dst_weight[i] if lockStateList[i] else (src_weight[i] * unlock_weight_ratio) for i in range(setSize)]
            else:
                setWeights = src_weight[::]

        if setWeights:
            cmds.setAttr('{}.wl[{}].w{}'.format(skinCluster, idx, w_slice), *setWeights, **wKwargs)

    with waitCursorBlock():
        for comp, sw in itertools.izip_longest(target_components, src_weights):
            if comp is None:
                break

            _set_weights(get_component_index(comp), singleSourceWeights or sw)

        normalize_weights(skinCluster, target_components)

@measure_time
def set_max_influence(skincluster, comps, setMaxInfluenceDigits=4):
    u"""
    max influenceを強制的に指定する
    """

    sel_list = OpenMaya.MSelectionList()
    [sel_list.add(x) for x in comps]
    dag_path = OpenMaya.MDagPath()
    comps_obj = OpenMaya.MObject()
    sel_list.getDagPath(0, dag_path, comps_obj)

    sc_obj = get_MObject(skincluster)
    sc_fn = OpenMayaAnim.MFnSkinCluster(sc_obj)

    current_weights = OpenMaya.MDoubleArray()
    infls = OpenMaya.MDagPathArray()
    util = OpenMaya.MScriptUtil()
    int_ptr = util.asUintPtr()
    sc_fn.influenceObjects(infls)
    num_infls = infls.length()

    sc_fn.getWeights(dag_path, comps_obj, current_weights, int_ptr)
    current_weights = [v for v in current_weights]
    set_weights = OpenMaya.MDoubleArray()

    for i in range(len(comps)):
        comp_weights = current_weights[i * num_infls: i * num_infls + num_infls]
        buf_comp_weights = [cw for cw in comp_weights]
        asc_weights, desc_weights = sort_numbers(buf_comp_weights)

        rest_weight = 0
        for j, weight in enumerate(desc_weights):
            if j < setMaxInfluenceDigits:
                continue
            rest_weight += weight
            desc_weights[j] = 0.0

        weightSum = 0
        for weight in buf_comp_weights:
            weightSum += weight

        zero_idxes = []
        for m, weight in enumerate(desc_weights):
            if weight != 0:
                # p = buf_comp_weights.index(weight)
                p_indices = find_indices(buf_comp_weights, weight)
                for p in p_indices:
                    if not p in zero_idxes:
                        zero_idxes.append(p)
                    if sys.version_info.major == 2:
                        comp_weights[p] += rest_weight * weight / weightSum
                    else:
                        # for Maya 2022-
                        comp_weights[p] += old_div(rest_weight * weight, weightSum)

        for i in range(len(comp_weights)):
            if not i in zero_idxes:
                comp_weights[i] = 0.0

        comp_weights = normalize_list(comp_weights)

        if sum(comp_weights) > 1:
            max_cw_idx = comp_weights.index(max(comp_weights))
            dif = sum(comp_weights) - 1.0
            comp_weights[max_cw_idx] -= dif
        if sum(comp_weights) < 1:
            min_cw_idx = comp_weights.index(min(comp_weights))
            dif = 1.0 - sum(comp_weights)
            comp_weights[min_cw_idx] += dif

        [set_weights.append(v) for v in comp_weights]

    cmds.skinWeightCmd(
        geometry=dag_path.partialPathName(),
        components=comps,
        skinCluster=skincluster,
        weights=set_weights
    )

def swap_or_move_weights(clsts, src='', dst='', components=None, **kwargs):
    u"""swap or move weights
    """

    mode = kwargs.get('mode', kwargs.get('m', 'swap')).lower()  # swap or move
    move_weight = clamp(0.0, 1.0, kwargs.get('weight', kwargs.get('w', 1.0)))
    src_infl = src
    dst_infl = dst

    if src_infl == dst_infl:
        return

    if not cmds.objExists(src_infl):
        return

    if not cmds.objExists(dst_infl):
        return

    l_src_infl = cmds.ls(src_infl, l=True)[0]
    l_dst_infl = cmds.ls(dst_infl, l=True)[0]

    components = flatten_components(components)

    with waitCursorBlock():
        for clst in clsts:
            indexList, influenceList = list_influences(clst, longName=True)
            if l_src_infl not in influenceList:
                continue

            if l_dst_infl not in influenceList:
                continue

            src_index = indexList[influenceList.index(l_src_infl)]
            dst_index = indexList[influenceList.index(l_dst_infl)]

            if not components:
                components = list_related_components_from_deformer(clst)
                if not components:
                    continue

            for comp in components:
                index = get_component_index(comp)
                src_weight = cmds.getAttr('{}.wl[{}].w[{}]'.format(clst, index, src_index))
                dst_weight = cmds.getAttr('{}.wl[{}].w[{}]'.format(clst, index, dst_index))

                if mode == 'swap':
                    cmds.setAttr('{}.wl[{}].w[{}]'.format(clst, index, src_index), dst_weight)
                    cmds.setAttr('{}.wl[{}].w[{}]'.format(clst, index, dst_index), src_weight)

                elif mode == 'move':
                    if move_weight < 1.0:
                        weight = src_weight * move_weight
                        cmds.setAttr('{}.wl[{}].w[{}]'.format(clst, index, src_index), src_weight - weight)
                        cmds.setAttr('{}.wl[{}].w[{}]'.format(clst, index, dst_index), weight + dst_weight)

                    else:
                        cmds.setAttr('{}.wl[{}].w[{}]'.format(clst, index, src_index), 0.0)
                        cmds.setAttr('{}.wl[{}].w[{}]'.format(clst, index, dst_index), src_weight + dst_weight)


def update_weights(value, influences, components=None, clsts=None, **kwargs):
    u"""
    """

    method = kwargs.get('method', kwargs.get('m', 'add')).lower()  # replace or add or multiply
    if method not in ['add', 'multiply', 'replace']:
        return

    if not influences:
        return

    if not components and not clsts:
        return

    if not components and clsts:
        components = list_related_components_from_deformer(clsts)
        if not components:
            return

    if not clsts and components:
        objects = get_objects(components)
        if not objects:
            return

        clsts = list_related_skinClusters(objects)
        if not clsts:
            return

    for clst in clsts:
        influenceIndexList, influenceList = list_influences(clst, longName=False)
        validInfls = [infl for infl in influences if infl in influenceList]
        if not validInfls:
            continue

        obj = get_objects(list_related_components_from_deformer(clst))[0]
        components = get_object_components(obj, flatten_components(components))
        if not components:
            continue

        if method == 'replace':
            tvs = [[infl, value] for infl in validInfls]
            cmds.skinPercent(clst, components, tv=tvs, nrm=True, prw=False)

        elif method == 'add':
            tvs = [[infl, value] for infl in validInfls]
            cmds.skinPercent(clst, components, tv=tvs, nrm=True, prw=False, r=True)

        elif method == 'multiply':
            value = max(0.0, value)
            for comp in components:
                idx = get_component_index(comp)
                tvs = []
                for infl in validInfls:
                    tvs.append([
                        infl,
                        cmds.getAttr('{}.wl[{}].w[{}]'.format(clst, idx, influenceIndexList[influenceList.index(infl)])) * value
                    ])

                cmds.skinPercent(clst, comp, tv=tvs, nrm=True, prw=False)
