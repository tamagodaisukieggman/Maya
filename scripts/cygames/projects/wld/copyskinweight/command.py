# -*- coding: utf-8 -*-

from __future__ import absolute_import

import datetime
import logging

from contextlib import contextmanager

import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim


logger = logging.getLogger('copyskinweight')


@contextmanager
def WaitCursorBlock():
    """ウェイトカーソルを表示させるコンテキストマネージャー
    """

    try:
        cmds.waitCursor(state=True)
        yield

    except Exception as e:
        cmds.error(str(e))

    finally:
        cmds.waitCursor(state=False)


class ProgressWindowBlock(object):
    """ProgressWindowを表示させるコンテキストマネージャー
    """

    def __init__(self, title='', progress=0,  minValue=0, maxValue=100, isInterruptable=True, show_progress=True):
        self._show_progress = show_progress and (not cmds.about(q=True, batch=True))

        self.title = title
        self.progress = progress
        self.minValue = minValue
        self.maxValue = maxValue
        self.isInterruptable = isInterruptable

        self._start_time = None

    def __enter__(self):
        logger.info('[ {} ] : Start'.format(self.title))

        if self._show_progress:
            cmds.progressWindow(
                title=self.title,
                progress=int(self.progress),
                status='[ {} ] : Start'.format(self.title),
                isInterruptable=self.isInterruptable,
                min=self.minValue,
                max=self.maxValue + 1
            )

        self._start_time = datetime.datetime.now()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        calc_time = datetime.datetime.now() - self._start_time
        logger.info('[ {} ] : End : Calculation time : {}'.format(self.title, calc_time))

        if self._show_progress:
            cmds.progressWindow(e=True, status='End : Calculation time : {}'.format(calc_time))
            cmds.progressWindow(ep=1)

    def step(self, step):
        if self._show_progress:
            cmds.progressWindow(e=True, step=step)

    def _set_status(self, status):
        if self._show_progress:
            cmds.progressWindow(e=True, status='[ {} / {} ] : {}'.format(self.progress, self.maxValue, status))

    def _get_status(self):
        if self._show_progress:
            return cmds.progressWindow(q=True, status=True)

    status = property(_get_status, _set_status)

    def _set_progress(self, progress):
        if self._show_progress:
            cmds.progressWindow(e=True, progress=progress)

    def _get_progress(self):
        if self._show_progress:
            return cmds.progressWindow(q=True, progress=True)

    progress = property(_get_progress, _set_progress)

    def is_cancelled(self):
        if self._show_progress:
            return cmds.progressWindow(q=True, ic=True)

    @staticmethod
    def wait(sec=1.0):
        cmds.pause(sec=sec)


def save_optionvar(key, value, force=True):
    """optionVarに保存

    :param str key: キー名
    :param mixin value: 値
    :param bool force: 強制的に上書きするかのブール値

    :return: 保存できたかどうかのブール値
    :rtype: bool
    """

    v = str(value)
    if force:
        cmds.optionVar(sv=[key, v])
        return True
    else:
        if not cmds.optionVar(ex=key):
            cmds.optionVar(sv=[key, v])
            return True
        else:
            return False


def load_optionvar(key):
    """optionVarを取得

    :param str key: キー名
    :return: 保存された値, キーが見つからない場合は None
    :rtype: value or None
    """

    if cmds.optionVar(ex=key):
        return eval(cmds.optionVar(q=key))
    else:
        return None


def remove_optionvar(key):
    """optionVarを削除

    :param str key: キー名
    :return: 削除成功したかのブール値
    :rtype: bool
    """

    if cmds.optionVar(ex=key):
        cmds.optionVar(rm=key)
        return True
    else:
        return False


def get_MObject(object_name):
    """MObject (API 1.0)を取得
    :param str object_name: オブジェクト名
    :return: MObject (API 1.0) を取得
    :rtype: MObject (API 1.0)
    """

    sel_list = OpenMaya.MSelectionList()
    sel_list.add(object_name)
    m_obj = OpenMaya.MObject()
    sel_list.getDependNode(0, m_obj)

    return m_obj


def get_component_count(objects):
    """controlPointタイプオブジェクトのコンポーネント数を取得
    :param list objects: オブジェクトのリスト
    :return: コンポーネント数
    :rtype: int
    """

    sel_list = OpenMaya.MSelectionList()
    [sel_list.add(x) for x in objects]
    comp_str = []
    sel_list.getSelectionStrings(comp_str)
    return len(cmds.ls(comp_str, fl=True))


def list_shapes(object_name):
    """シェイプノード名を取得 (中間形状オブジェクトを除く)
    :param str object_name: ノード名
    :return: シェイプノード名のリスト
    :rtype: list
    """

    shapes = cmds.listRelatives(object_name, s=True, ni=True, pa=True, type='controlPoint')
    if not shapes:
        shapes = cmds.ls(object_name, ni=True, type='controlPoint')
        if not shapes:
            return []

    return shapes


def get_shape_type(object_name):
    """シェイプノードのタイプ名を取得
    :param str object_name: ノード名
    :return: シェイプノードタイプ名
    :rtype: str
    """

    shapes = list_shapes(object_name)
    return cmds.objectType(shapes[0]) if shapes else ''


def list_influences(skincluster, **kwargs):
    """skinClusterのインフルエンスを取得

    :param str skincluster: skinClusterノード名
    :keyword bool as_object: True - MDagPathオブジェクトを取得、False - ノード名(str)を取得
    :keyword bool long_name: True - long_name(fullPath) を取得, False - shortName(unique) を取得
    :return: (インフルエンスインデックス, インフルエンスオブジェクト)
    :rtype: tuple
    """

    as_object = kwargs.get('as_object', False)
    long_name = kwargs.get('long_name', True)

    if not cmds.objExists(skincluster):
        return None

    sc_obj = get_MObject(skincluster)
    sc_fn = OpenMayaAnim.MFnSkinCluster(sc_obj)
    infls = OpenMaya.MDagPathArray()
    sc_fn.influenceObjects(infls)
    num_infls = infls.length()

    infl_indices = [sc_fn.indexForInfluenceObject(infls[i]) for i in range(num_infls)]
    if as_object:
        influences = [infls[i] for i in range(num_infls)]

    else:
        if long_name:
            influences = [infls[i].fullPathName() for i in range(num_infls)]
        else:
            influences = [infls[i].partialPathName() for i in range(num_infls)]

    return infl_indices, influences


def list_related_skinClusters(nodes):
    """接続されているskinClusterノードを取得
    :param list/str nodes: ノードのリスト
    :return: skinClusterノードのリスト
    :rtype: list
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
    """接続されているskinClusterのインフルエンスを取得
    :param list nodes: ノードのリスト
    :return: インフルエンスのリスト
    :rtype: list
    """

    if not nodes:
        return []

    skinClusters = cmds.ls(nodes, typ='skinCluster') or []
    if not skinClusters:
        return []

    plugs = ['{}.matrix'.format(sc) for sc in skinClusters]
    return cmds.listConnections(plugs, s=1, d=0) or []


def select_related_influences(nodes):
    """接続されているskinClusterのインフルエンスを選択
    :param list nodes: ノードのリスト
    """

    if not nodes:
        return

    skinClusters = list_related_skinClusters(nodes)
    influences = list_skinCluster_influences(skinClusters)
    if influences:
        cmds.select(influences, r=True)


def add_influences(nodes, influences):
    """接続されているskinClusterにインフルエンスを追加
    :param list nodes: ノードのリスト
    :param list influences: インフルエンスのリスト
    """

    if not nodes:
        return

    if not influences:
        return

    for node in nodes:
        skinclusters = list_related_skinClusters(node)
        if not skinclusters:
            logger.warning('[ Skin add influences ] : {} : skincluster not found.'.format(node))
            continue

        current_infl_indices, current_influences = list_influences(skinclusters[0], as_object=False, long_name=False)
        add_infls = [influence for influence in influences if influence not in current_influences]
        if add_infls:
            cmds.skinCluster(skinclusters[0], e=True, dr=4, lw=True, wt=0.0, addInfluence=add_infls)


def get_object_filtered_components(object_name, components):
    """オブジェクトでフィルターしたコンポーネントを取得
    :param str object_name:
    :param list components: コンポーネントリスト
    :return: コンポーネントリスト
    :rtype: list
    """

    if components:
        shp = '{}.'.format(object_name)
        par = cmds.listRelatives(object_name, pa=1, p=1)
        trs = '{}.'.format(par[0]) if par else ''
        return [x for x in components if x.startswith(trs) or x.startswith(shp)]


def remove_unused_influences(skincluster):
    """remove unused influences
    :param str skincluster: skinClusterノード
    :return: スキンクラスタから除外したインフルエンスノード
    :rtype: list
    """

    if not cmds.objExists(skincluster):
        return None

    sc_obj = get_MObject(skincluster)
    sc_fn = OpenMayaAnim.MFnSkinCluster(sc_obj)
    infls = OpenMaya.MDagPathArray()
    sc_fn.influenceObjects(infls)

    remove_influences = []
    for i in range(infls.length()):
        sel_list = OpenMaya.MSelectionList()
        weights = OpenMaya.MDoubleArray()
        sc_fn.getPointsAffectedByInfluence(infls[i], sel_list, weights)
        sel_str = []
        sel_list.getSelectionStrings(sel_str)

        if not sel_str:
            remove_influences += [infls[i].partialPathName()]

    if remove_influences:
        cmds.setAttr('{}.nodeState'.format(skincluster), 1)
        connects = cmds.listConnections(remove_influences, s=False, d=True, c=True, p=True, type='skinCluster')
        if connects:
            src, dst = connects[0::2], connects[1::2]
            for s, d in zip(src, dst):
                if skincluster not in d:
                    continue
                cmds.disconnectAttr(s, d)
        cmds.setAttr('{}.nodeState'.format(skincluster), 0)

        logger.info('[ Remove Unused Influences ] : {} : {}'.format(skincluster, remove_influences))

    return remove_influences


def bind_and_copy(src, dst, src_components=None, dst_components=None, bind=True, method='closestpoint'):
    """Smooth bind と copy weight を実行
    :param str src: ソースジオメトリ名
    :param str dst: デスティネーションジオメトリ名
    :param list src_components: ソースコンポーネント
    :param list dst_components: デスティネーションジコンポーネント
    :param bool bind: bind処理の実行有無 (False の場合は copy weightsのみの実行)
    :param str method: コピー方法 'closestpoint' or 'closestcomponent' or 'uvspace'
    """

    # print(src, dst, src_components, dst_components, bind, method)

    if not cmds.objExists(src):
        return

    src_clst = list_related_skinClusters(src)
    if not src_clst:
        logger.warning('skinCluster not found : {}'.format(src))
        return
    src_clst = src_clst[0]

    if not cmds.objExists(dst):
        return

    dst_clst = list_related_skinClusters(dst)
    if not bind and not dst_clst:
        logger.warning('skinCluster not found : {}'.format(dst))
        return

    method = method.lower()
    if method not in ['closestpoint', 'closestcomponent', 'uvspace']:
        logger.warning('{} is Invalid import method.'.format(method))
        return

    if method == 'uvspace':
        src_shapes = list_shapes(src)
        src_shape_type = cmds.objectType(src_shapes[0])

        dst_shapes = list_shapes(dst)
        dst_shape_type = cmds.objectType(dst_shapes[0])
        if src_shape_type != 'mesh' or dst_shape_type != 'mesh':
            logger.warning('Import method \'uvspace\' is mesh-only method.')
            return

    src_influenceIndexList, src_influenceList = list_influences(src_clst, as_object=False, long_name=False)

    if bind:
        if dst_clst:
            cmds.skinCluster(dst, e=True, unbind=True)

        dst_clst = cmds.skinCluster(
            src_influenceList,
            dst,
            toSelectedBones=True,
            bindMethod=cmds.getAttr('{}.skinningMethod'.format(src_clst)),
            normalizeWeights=cmds.getAttr('{}.normalizeWeights'.format(src_clst)),
            weightDistribution=cmds.getAttr('{}.weightDistribution'.format(src_clst)),
            maximumInfluences=cmds.getAttr('{}.maxInfluences'.format(src_clst)),
            obeyMaxInfluences=cmds.getAttr('{}.maintainMaxInfluences'.format(src_clst)),
            dropoffRate=4,
            removeUnusedInfluence=False,
            name='{}_skinCluster'.format(dst.replace('|', '__'))
        )[0]

    else:
        if dst_clst:
            dst_clst = dst_clst[0]
            dst_influenceIndexList, dst_influenceList = list_influences(dst_clst, as_object=False, long_name=False)
            add_joints = [joint for joint in src_influenceList if joint not in dst_influenceList]
            if add_joints:
                logger.info(
                    '[ Add influences ] : {} is uncontain influences in \'{}\''.format(add_joints, dst_clst))
                cmds.skinCluster(dst_clst, e=True, dr=4, lw=True, wt=0.0, addInfluence=add_joints)

    if src_components:
        src_components = get_object_filtered_components(src, src_components)

    if dst_components:
        dst_components = get_object_filtered_components(dst, dst_components)

    copy_skinweight_options = {}

    if src_components and dst_components:
        cmds.select(src_components, r=True)
        cmds.select(dst_components, add=True)

    elif src_components and (not dst_components):
        cmds.select(src_components, r=True)
        cmds.select(dst, add=True)

    elif (not src_components) and dst_components:
        cmds.select(src, r=True)
        cmds.select(dst_components, add=True)

    else:
        copy_skinweight_options['ss'] = src_clst
        copy_skinweight_options['ds'] = dst_clst

    with WaitCursorBlock():
        if method == 'closestcomponent':
            cmds.copySkinWeights(noMirror=True,
                                 influenceAssociation=('label', 'oneToOne', 'closestJoint'),
                                 surfaceAssociation='closestComponent',
                                 noBlendWeight=True,
                                 normalize=True,
                                 **copy_skinweight_options)

        elif method == 'uvspace':
            src_current_uv_set = cmds.polyUVSet(src, q=True, currentUVSet=True)[0]
            dst_current_uv_set = cmds.polyUVSet(dst, q=True, currentUVSet=True)[0]
            cmds.copySkinWeights(noMirror=True,
                                 influenceAssociation=('label', 'oneToOne', 'closestJoint'),
                                 surfaceAssociation='closestPoint',
                                 uvSpace=[src_current_uv_set, dst_current_uv_set],
                                 noBlendWeight=True,
                                 normalize=True,
                                 **copy_skinweight_options)

        else:
            cmds.copySkinWeights(noMirror=True,
                                 influenceAssociation=('label', 'oneToOne', 'closestJoint'),
                                 surfaceAssociation='closestPoint',
                                 noBlendWeight=True,
                                 normalize=True,
                                 **copy_skinweight_options)
