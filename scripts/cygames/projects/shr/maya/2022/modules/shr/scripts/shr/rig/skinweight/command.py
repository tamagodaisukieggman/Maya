# -*- coding: utf-8 -*-

from __future__ import absolute_import

# import cPickle as pickle
import _pickle as pickle
import datetime
import glob
import os
import traceback
from contextlib import contextmanager
from collections import OrderedDict

import maya.cmds as cmds
import maya.OpenMaya as OpenMaya
import maya.OpenMayaAnim as OpenMayaAnim
import maya.api.OpenMaya as OpenMaya2

import mtk.utils.plugin as plugin
from mtk.utils.decoration import keep_selections
import logging
# from mtku.maya.mtklog import MtkLog

# logger = MtkLog(__name__)
logger = logging.getLogger("Skin Weight ... : スキンウェイトツール")

# skinweightコマンドプラグインのロード
if plugin.load('skinWeightCmd.py'):
    use_skinWeightCmd = True
else:
    use_skinWeightCmd = False

WEIGHT_FILE_EXT = '.weightdata'
"""ウェイトデータファイルの拡張子
"""


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

    def __init__(self, title='', progress=0, minValue=0, maxValue=100, isInterruptable=True, show_progress=True):
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


def find_items(root_dir, name='*', depth=1, find_type='all'):
    """指定ディレクトリ階層化のファイルを取得

    :param str root_dir: jsonファイルを探すルートディレクトリ
    :param str name: 取得ファイル名
    :param int depth: jsonファイルを探すサブディレクトリの深さ
    :param str find_type: 対象データタイプ, 'all' or 'file' or 'directory'
    :return: jsonファイルを辞書で取得 {filename: filepath, ...}
    :rtype: dict
    """

    _valid_find_types = ['all', 'file', 'directory']

    depth = depth if depth > 0 else 1

    find_type = find_type or 'all'
    if find_type not in _valid_find_types:
        return {}

    search_dirs = [os.path.join(root_dir, *(['*'] * i + [name])).replace(os.sep, '/') for i in range(depth)]

    ret = {}
    for search_dir in search_dirs:
        match_list = glob.glob(search_dir)
        for match_item in match_list:
            if find_type == 'file' and not os.path.isfile(match_item):
                continue

            elif find_type == 'directory' and not os.path.isdir(match_item):
                continue

            basename = os.path.basename(match_item)
            basename, ext = os.path.splitext(basename)
            ret[basename] = match_item.replace(os.sep, '/')

    return ret


def is_same_path(a, b):
    """入力が同じか調査(小文字に変換して調査する)
    :param str a: パス
    :param str b: パス
    :return: 同じパスの場合はTrue
    :rtype: bool
    """

    return a.lower() == b.lower()


def is_contain_path(path, path_list):
    """入力パスがパスリストに含まれる調査し、含まれる場合はそのインデックスを返す
    :param str path: パス
    :param list path_list: パスのリスト
    :return: パスリストのインデックス(見つからない場合は -1 を返す)
    :rtype: int
    """

    for i, p in enumerate(path_list):
        if is_same_path(p, path):
            return i

    return -1


def get_workspace_weights_dir():
    """ワークスペース直下のweightsディレクトリパスを返す
    :return: workspace + '/weights'
    :rtype: str
    """

    return os.path.join(cmds.workspace(q=True, rd=True), 'weights').replace(os.sep, '/')


class SkinWeightFile(object):
    ext = WEIGHT_FILE_EXT

    def __init__(self, path):
        self._path = None
        self.path = path

    def _get_path(self):
        return self._path

    def _set_path(self, path):
        self._path = (os.path.splitext(path)[0] + self.ext).replace(os.sep, '/')

    path = property(_get_path, _set_path)

    @staticmethod
    def _get_file_information():
        ret = OrderedDict()
        ret['file_information'] = OrderedDict()
        ret['file_information']['data_type'] = 'skinWeight'
        ret['file_information']['user'] = os.environ['USER']
        ret['file_information']['date'] = datetime.datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
        return ret

    def read(self):
        with open(self.path, 'rb') as f:
            try:
                return pickle.loads(f.read().decode('zip'))

            except Exception as e:
                cmds.error(traceback.format_exc())

    def write(self, data):
        dir_name = os.path.dirname(self.path)
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)

        with open(self.path, 'wb') as f:
            try:
                write_data = self._get_file_information()
                write_data.update(data)
                f.write(pickle.dumps(write_data, protocol=pickle.HIGHEST_PROTOCOL).encode('zip'))
                f.flush()
                os.fsync(f.fileno())

            except Exception as e:
                cmds.error(traceback.format_exc())


def get_skinCluster_attribute_data(skincluster):
    """skinClusterノードのアトリビュートを辞書で取得
    :param str skincluster: skinClusterノード名
    :return: skinClusterノードのアトリビュートの辞書
    :rtype: dict
    """

    ret = OrderedDict()

    if not cmds.objExists(skincluster):
        return ret

    skinClusterAttrs = [
        'skinningMethod',
        'useComponents',
        'deformUserNormals',
        'normalizeWeights',
        'weightDistribution',
        'maxInfluences',
        'maintainMaxInfluences',
    ]

    for attr in skinClusterAttrs:
        ret[attr] = cmds.getAttr('{}.{}'.format(skincluster, attr))

    return ret


def get_skinCluster_data(node):
    """skinClusterデータを取得
    :param str node: ノード名
    :return: skinClusterデータ(weight, skinClusterAttributes) を取得
    :rtype: dict
    """

    ret = OrderedDict()

    if not cmds.objExists(node):
        return ret

    skinClusters = list_related_skinClusters(node)
    if not skinClusters:
        return ret

    skinClusterNode = skinClusters[0]
    weights, infls, infl_indices = get_skinCluster_weights(node)

    ret['geometry'] = node
    ret['skinCluster'] = skinClusterNode
    ret['numInfluences'] = len(infls)
    ret['influences'] = infls
    ret['influenceIndices'] = infl_indices
    ret['numComponents'] = len(weights) / len(infls)
    ret['skinClusterAttributes'] = get_skinCluster_attribute_data(skinClusterNode)
    ret['weights'] = weights

    return ret


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


def get_maya_version():
    """maya api バージョンの取得
    :return: maya api バージョン
    :rtype: int
    """
    return cmds.about(api=True)


def get_MObject2(object_name):
    """MObject (API 2.0)を取得
    :param str object_name: オブジェクト名
    :return: MObject (API 2.0) を取得
    :rtype: MObject (API 2.0)
    """

    sel_list = OpenMaya2.MSelectionList()
    sel_list.add(object_name)

    return sel_list.getDependNode(0)


def get_MDagPath2(object_name):
    """MDagPath (API 2.0)を取得
    :param str object_name: オブジェクト名
    :return: MDagPath (API 2.0) を取得
    :rtype: MDagPath (API 2.0)
    """

    sel_list = OpenMaya2.MSelectionList()
    sel_list.add(object_name)

    return sel_list.getDagPath(0)


def get_MObjectComponent2(object_name):
    """MObject (Component) (API 2.0)を取得
    :param str object_name: オブジェクト名
    :return: MObject (Component) (API 2.0) を取得
    :rtype: MObject (Component) (API 2.0)
    """

    sel_list = OpenMaya2.MSelectionList()
    sel_list.add(object_name)

    return sel_list.getComponent(0)


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


def get_MDagPath(object_name):
    """MDagPath (API 1.0)を取得
    :param str object_name: オブジェクト名
    :return: MDagPath (API 1.0) を取得
    :rtype: MDagPath (API 1.0)
    """

    sel_list = OpenMaya.MSelectionList()
    sel_list.add(object_name)
    dag_path = OpenMaya.MDagPath()
    sel_list.getDagPath(0, dag_path)

    return dag_path


def get_dagPath_and_comps(objects):
    """MDagPath と MObject(component) (API 1.0)を取得
    :param list objects: オブジェクトのリスト
    :return: MDagPath, MObject(component) (API 1.0) を取得
    :rtype: tuple (MDagPath, MObject(component))
    """

    sel_list = OpenMaya.MSelectionList()
    [sel_list.add(x) for x in objects]
    dag_path = OpenMaya.MDagPath()
    comps = OpenMaya.MObject()
    sel_list.getDagPath(0, dag_path, comps)
    return dag_path, comps


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


def get_component_index(comp):
    """コンポーネントインデックスを取得
    :param str comp: コンポーネント名
    :return: コンポーネントインデックス
    :rtype: int
    """

    if '.f[' in comp or '.vtx[' in comp or '.e[' in comp or '.map[' in comp:
        return int(comp.rsplit(']', 1)[0].rsplit('[', 1)[-1])
    try:
        return int(cmds.attributeName(comp, s=True).rsplit(']', 1)[0].rsplit('[', 1)[-1])
    except Exception as e:
        return None


def get_objects(objs):
    """オブジェクト名の取得
    :param list or str objs: オブジェクト / コンポーネント
    :return: オブジェクト名
    :rtype: list
    """

    ret = []

    objs = cmds.ls(objs, o=True)
    for o in sorted(set(objs), key=objs.index):
        if cmds.objectType(o, isa='controlPoint'):
            ret.append(cmds.listRelatives(o, p=True, pa=True)[0])
        else:
            ret.append(o)

    return ret


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
    """接続されているskinClusgetのインフルエンスを取得
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

    cmds.dgdirty(skincluster)

    return remove_influences


def normalize_weights(skincluster, comps):
    """normalize weights
    :param str skincluster: skinClusterノード
    :param list comps: コンポーネントリスト
    """

    if not cmds.objExists(skincluster):
        return

    with WaitCursorBlock():
        cmds.setAttr('{}.normalizeWeights'.format(skincluster), 1)
        cmds.skinPercent(skincluster, comps, normalize=True)


def prune_weights(skincluster, comps, prune_weights=0.01):
    """prune weights
    :param str skincluster: skinClusterノード
    :param list comps: コンポーネントリスト
    :param float prune_weights: カットオフする値
    """

    if not cmds.objExists(skincluster):
        return

    with WaitCursorBlock():
        # unhold
        hold_stat = {}
        influences = cmds.listConnections('{}.matrix'.format(skincluster), s=1, d=0) or []
        for infl in influences:
            plug = '{}.lockInfluenceWeights'.format(infl)
            if not cmds.objExists(plug):
                continue

            v = cmds.getAttr(plug)
            if v:
                hold_stat[plug] = v
                cmds.setAttr(plug, False)

        cmds.skinPercent(skincluster, comps, pruneWeights=prune_weights, normalize=True)

        # hold状態を再設定
        for k, v in hold_stat.iteritems():
            cmds.setAttr(k, v)


def round_weights(skincluster, comps, round_digits=3, **kwargs):
    """round weights
    :param str skincluster: skinClusterノード
    :param list comps: コンポーネントリスト
    :param int round_digits: 丸め小数点桁数
    """

    set_by_api = kwargs.get('set_by_api', True)
    if not use_skinWeightCmd:
        set_by_api = False

    index_list, infl_list = list_influences(skincluster, as_object=False, long_name=False)
    if len(infl_list) < 2:
        return

    eps = 0.1 ** (round_digits + 1)
    mind = 0.1 ** round_digits

    comps = cmds.ls(comps, fl=True)

    if set_by_api:
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
                w = round(w0, round_digits)
                comp_set_weights.append(w)
                comp_diff_weights.append(w0 - w)

            comp_weights_sum = sum(comp_weights)
            comp_set_weights_sum = sum(comp_set_weights)

            if abs(comp_weights_sum - 1.0) > 1e-08:
                comp_set_weights_sum = 0.0
                for j in range(num_infls):
                    w0 = comp_weights[j] / comp_weights_sum
                    w = round(w0, round_digits)
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

            [set_weights.append(v) for v in comp_set_weights]

        cmds.skinWeightCmd(
            geometry=dag_path.partialPathName(),
            components=comps,
            skinCluster=skincluster,
            weights=set_weights
        )

    else:
        # setAttr
        max_infl_index = max(index_list)
        w_slice = '[0:{}]'.format(max_infl_index) if max_infl_index > 0 else '[0]'
        array_size = max_infl_index + 1

        for comp in comps:
            comp_index = get_component_index(comp)
            if comp_index is None:
                continue

            weights = cmds.getAttr('{}.wl[{}].w{}'.format(skincluster, comp_index, w_slice))

            # Round Weights
            set_weights, diff_weights = [], []
            for j in range(array_size):
                w0 = weights[j]
                w = round(w0, round_digits)
                set_weights.append(w)
                diff_weights.append(w0 - w)

            weights_sum = sum(weights)
            set_weights_sum = sum(set_weights)

            if abs(weights_sum - 1.0) > 1e-08:
                set_weights_sum = 0.0
                for j in range(array_size):
                    w0 = weights[j] / weights_sum
                    w = round(w0, round_digits)
                    set_weights[j] = w
                    diff_weights[j] = w0 - w
                    set_weights_sum += w

            if 1.0 - set_weights_sum > eps:
                d = max(diff_weights)
                j = diff_weights.index(d)
                set_weights[j] += mind

            elif 1.0 - set_weights_sum < -eps:
                d = min(diff_weights)
                j = diff_weights.index(d)
                set_weights[j] -= mind

            cmds.setAttr('{}.wl[{}].w{}'.format(skincluster, comp_index, w_slice), *set_weights, size=array_size)

    # prune weights を実行してウェイトが0.0のインデックスを除去
    prune_weights(skincluster, comps, prune_weights=eps)


def export_weight_by_deformerWeights(node, file_path, **kwargs):
    """skinClusterのウェイトを書き出す (maya: deformerWeightsコマンドを使用)
    :param node:
    :param str file_path: exportファイルパス
    """

    if not cmds.objExists(node):
        return

    skinClusters = list_related_skinClusters(node)
    if not skinClusters:
        return

    dir_path, base_name = os.path.split(file_path)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

    export_options = {
        'path': dir_path,
        'export': True,
        'defaultValue': -1.0,
        'weightTolerance': kwargs.get('weightTolerance', kwargs.get('wt', 0.001))
    }

    if get_maya_version() >= 201600:
        export_options.update({
            'weightPrecision': 6,
            'vertexConnections': True
        })

    cmds.deformerWeights(base_name, deformer=skinClusters[0], **export_options)

    return file_path


def export_weights_by_deformerWeights(nodes, dir_path, **kwargs):
    """skinClusterのウェイトを書き出す (maya: deformerWeightsコマンドを使用)
    :param list nodes: ノード名のリスト
    :param str dir_path: exportディレクトリパス
    """

    valid_nodes = [node for node in nodes if cmds.objExists(node)]
    if not valid_nodes:
        return

    ret = []

    for node in valid_nodes:
        export_path = export_weight_by_deformerWeights(
            node,
            os.path.join(dir_path, '{}.xml'.format(node.replace('|', '__'))).replace(os.sep, '/'),
            **kwargs)

        if export_path:
            ret.append(export_path)

    return ret


def import_weight_by_deformerWeights(node, file_path, **kwargs):
    """skinClusterのウェイトを読み込む (maya: deformerWeightsコマンドを使用)
    :param node:
    :param str file_path: importファイルパス
    """

    if not cmds.objExists(node):
        return

    skinClusters = list_related_skinClusters(node)
    if not skinClusters:
        return

    if not os.path.isfile(file_path):
        return

    dir_path, base_name = os.path.split(file_path)

    method = kwargs.get('method', kwargs.get('m', 'index'))

    import_options = {
        'path': dir_path,
        'im': True,
        'method': method,
    }

    if method == 'nearest':
        import_options.update({
            'worldSpace': True,
            'positionTolerance': kwargs.get('positionTolerance', kwargs.get('pt', 0.01))
        })

    cmds.deformerWeights(base_name, deformer=skinClusters[0], **import_options)


def import_weights_by_deformerWeights(nodes, dir_path, **kwargs):
    """skinClusterのウェイトを読み込む (maya: deformerWeightsコマンドを使用)
    :param list nodes: ノード名のリスト
    :param str dir_path: ウェイトファイルが保存されているディレクトリ
    """

    valid_nodes = [node for node in nodes if cmds.objExists(node)]
    if not valid_nodes:
        return

    if not os.path.isdir(dir_path):
        return

    for node in valid_nodes:
        import_weight_by_deformerWeights(
            node,
            os.path.join(dir_path, '{}.xml'.format(node.replace('|', '__'))).replace(os.sep, '/'),
            **kwargs
        )


def get_skinCluster_weights(object_name, **kwargs):
    """skinClusterのウェイト情報の取得
    :param str object_name: ノード名
    :keyword bool use_py_object: 取得データをpythonObjectで返すかのブール
    :return: weights, influences, influences indices を取得
    :rtype: tuple (weights, influences, influences indices)
    """

    use_py_object = kwargs.get('use_py_object', True)

    if not cmds.objExists(object_name):
        logger.warning('{} is not found.'.format(object_name))
        return

    skinClusters = list_related_skinClusters(object_name)
    if not skinClusters:
        logger.warning('Related skinCluster not found : {}'.format(object_name))
        return
    skinCluster = skinClusters[0]

    try:
        dag_path, comps = get_dagPath_and_comps(['{}.cp[*]'.format(object_name)])
    except RuntimeError as e:
        cmds.warning(str(e))
        logger.warning('Can not get components : {}'.format(object_name))
        return

    sc_obj = get_MObject(skinCluster)
    sc_fn = OpenMayaAnim.MFnSkinCluster(sc_obj)

    weights = OpenMaya.MDoubleArray()
    infl_indices = OpenMaya.MIntArray()
    infls = OpenMaya.MDagPathArray()
    util = OpenMaya.MScriptUtil()
    int_ptr = util.asUintPtr()

    sc_fn.influenceObjects(infls)
    for i in range(infls.length()):
        infl_indices.append(sc_fn.indexForInfluenceObject(infls[i]))

    sc_fn.getWeights(dag_path, comps, weights, int_ptr)

    if use_py_object:
        py_weights = [v for v in weights]
        py_infls = []
        for i in range(infls.length()):
            py_infls.append(infls[i].partialPathName())
        py_infl_indices = [v for v in infl_indices]

        return py_weights, py_infls, py_infl_indices

    else:
        return weights, infls, infl_indices


def set_skinCluster_weights(object_name, weights, infls, comps=None, **kwargs):
    """skinClusterにウェイトをセット
    :param str object_name: ノード名
    :param list or MDoubleArray weights: ウェイトデータの配列
    :param list or MDagPathArray infls: インフルエンスデータの配列
    :param list comps: コンポーネントリスト
    :keyword bool use_py_object: 入力データがpythonObjectかのブール
    :keyword bool set_by_api: api でセットするかのブール
    :keyword bool undoable: set_by_api がTrueの場合のundoの可否 (Trueの場合はskinWeightCmdでウェイトを設定)
    """

    use_py_object = kwargs.get('use_py_object', True)
    set_by_api = kwargs.get('set_by_api', True)
    undoable = kwargs.get('undoable', True)

    if comps:
        object_name = get_objects(comps)[0]

    if not cmds.objExists(object_name):
        logger.warning('{} is not found.'.format(object_name))
        return

    skinClusters = list_related_skinClusters(object_name)
    if not skinClusters:
        logger.warning('Related skinCluster not found : {}'.format(object_name))
        return
    skinCluster = skinClusters[0]

    try:
        if comps:
            dag_path, comps = get_dagPath_and_comps(comps)
        else:
            dag_path, comps = get_dagPath_and_comps(['{}.cp[*]'.format(object_name)])
    except RuntimeError as e:
        cmds.warning(str(e))
        logger.warning('Can not get components : {}'.format(object_name))
        return

    if not use_skinWeightCmd:
        set_by_api = False

    if use_py_object:
        py_weights = weights[::]
        py_infls = infls[::]

        weights = OpenMaya.MDoubleArray()
        [weights.append(v) for v in py_weights]

        infls = OpenMaya.MDagPathArray()
        [infls.append(get_MDagPath(v)) for v in py_infls]

    num_weights = weights.length()
    num_infls = infls.length()
    num_comps = num_weights / num_infls

    sc_obj = get_MObject(skinCluster)
    sc_fn = OpenMayaAnim.MFnSkinCluster(sc_obj)

    src_to_dst_map = {}
    dst_fix_map = {}

    dst_infls = OpenMaya.MDagPathArray()
    dst_infl_indices = OpenMaya.MIntArray()
    sc_fn.influenceObjects(dst_infls)
    num_dst_infls = dst_infls.length()

    for i in range(dst_infls.length()):
        dst_infl_indices.append(i)
        dst_fix_map[sc_fn.indexForInfluenceObject(dst_infls[i])] = i

    uncontain_infls = []
    for i in range(infls.length()):
        try:
            src_to_dst_map[i] = sc_fn.indexForInfluenceObject(infls[i])
        except RuntimeError:
            uncontain_infls.append(infls[i].partialPathName())

    if uncontain_infls:
        logger.warning('{} is not in \'{}\' influences.'.format(uncontain_infls, skinCluster))
        return

    if set_by_api:
        if undoable:
            set_weights = [0.0] * (num_comps * num_dst_infls)
        else:
            set_weights = OpenMaya.MDoubleArray(num_comps * num_dst_infls, 0.0)

        # weightの整形
        for i in range(num_comps):
            for j in range(num_infls):
                set_weights[i * num_dst_infls + dst_fix_map[src_to_dst_map[j]]] = weights[i * num_infls + j]

        if undoable:
            cmds.skinWeightCmd(geometry=object_name, skinCluster=skinCluster, weights=set_weights)
        else:
            sc_fn.setWeights(dag_path, comps, dst_infl_indices, set_weights, False)

    else:
        max_infl_index = max(dst_fix_map.keys())
        w_slice = '[0:{}]'.format(max_infl_index) if max_infl_index > 0 else '[0]'
        for i in range(num_comps):
            set_weights = [0.0] * (max_infl_index + 1)
            for j in range(num_infls):
                # weightの整形
                set_weights[src_to_dst_map[j]] = weights[i * num_infls + j]

            # component毎にセット
            cmds.setAttr('{}.wl[{}].w{}'.format(skinCluster, i, w_slice), *set_weights, size=num_infls)


def export_skinCluster_weights(object_name, file_path):
    """ウェイトデータのエクスポート
    :param str object_name: ノード名
    :param str file_path: ファイルパス
    :return エクスポートファイルパス
    :rtype: str
    """

    write_data = get_skinCluster_data(object_name)
    if not write_data:
        return

    if get_shape_type(object_name) == 'mesh':
        write_data['geometry_data'] = get_mesh_data(object_name)

    writer = SkinWeightFile(file_path)
    writer.write(write_data)

    return file_path


@keep_selections
def import_skinCluster_weights(object_name, file_path, method='index', force_bind=False, **kwargs):
    """
    :param str object_name: ノード名
    :param str file_path: weightファイルパス
    :param str method: importメソッド - index or closestPoint or closestComponent or uvspace
    :param bool force_bind: 強制的にウェイトデータで再バインド
    :return: importに成功した場合はTrue
    :rtype: bool
    """

    set_by_api = kwargs.get('set_by_api', True)
    undoable = kwargs.get('undoable', True)
    # influences_remap_table = kwargs.get('remap_table', {})

    method = method.lower()
    if method not in ['index', 'closestpoint', 'closestcomponent', 'uvspace']:
        logger.warning('{} is Invalid import method.'.format(method))
        return False

    if not cmds.objExists(object_name):
        logger.warning('{} is not found.'.format(object_name))
        return False

    read_data = read_weights_data(file_path)
    if not read_data:
        return False

    influences = read_data['influences']
    not_found_influences = [inf for inf in influences if not cmds.objExists(inf)]
    if not_found_influences:
        logger.warning('{} is not fuond.'.format(not_found_influences))
        return False

    shapes = list_shapes(object_name)
    shape = shapes[0]
    shape_type = cmds.objectType(shape)
    num_components = get_component_count(['{}.cp[*]'.format(object_name)])

    geometry_data = read_data.get('geometry_data', {})

    # Check Method and numComponents
    if method == 'index':
        if num_components != int(read_data.get('numComponents', 0)):
            logger.warning('{} and {} components count missmatch.'.format(object_name, file_path))
            return False
    else:
        if not geometry_data:
            logger.warning(
                'Not found geometry data in weight file.\n Please select \'index\' method. : {}'.format(object_name))
            return False

    if shape_type != 'mesh' and method == 'uvspace':
        logger.warning(
            'Import method \'uvspace\' is mesh-only method. : {} is {} type.'.format(object_name, shape_type))
        return False

    skinClusterAttributes = read_data.get('skinClusterAttributes', {})
    skinclusters = list_related_skinClusters(object_name)
    if force_bind:
        if skinclusters:
            cmds.skinCluster(object_name, e=True, unbind=True)

        skincluster = cmds.skinCluster(
            influences,
            object_name,
            toSelectedBones=True,
            bindMethod=skinClusterAttributes['skinningMethod'],
            normalizeWeights=skinClusterAttributes['deformUserNormals'],
            weightDistribution=skinClusterAttributes['weightDistribution'],
            maximumInfluences=skinClusterAttributes['maxInfluences'],
            obeyMaxInfluences=skinClusterAttributes['maintainMaxInfluences'],
            dropoffRate=4,
            removeUnusedInfluence=False,
            name='{}_skinCluster'.format(object_name.replace('|', '__'))
        )[0]

        # 強制バインド時はインフルエンスが１つの場合はウェイトコピー処理は必要ない。
        if len(influences) == 1:
            return True

    else:
        if not skinclusters:
            logger.warning('Related skinCluster not found : {}'.format(object_name))
            return False
        skincluster = skinclusters[0]

    # Import Weights
    # method が'index'の場合
    if method == 'index':
        set_skinCluster_weights(
            object_name,
            read_data['weights'],
            read_data['influences'],
            set_by_api=set_by_api,
            undoable=undoable,
        )

    # methodが'index'以外の場合
    else:
        # ダミーオブジェクトを作成
        dmy = create_mesh('import_weight_dmy__{}'.format(read_data['geometry']), geometry_data)

        # ダミーオブジェクトをsmoothBind
        dmy_skincluster = cmds.skinCluster(
            influences,
            dmy,
            toSelectedBones=True,
            bindMethod=skinClusterAttributes['skinningMethod'],
            normalizeWeights=skinClusterAttributes['deformUserNormals'],
            weightDistribution=skinClusterAttributes['weightDistribution'],
            maximumInfluences=skinClusterAttributes['maxInfluences'],
            obeyMaxInfluences=skinClusterAttributes['maintainMaxInfluences'],
            dropoffRate=4,
            removeUnusedInfluence=False,
            name='{}_skinCluster'.format(dmy.replace('|', '__'))
        )[0]

        # ダミーオブジェクトにウェイトをロード
        set_skinCluster_weights(
            dmy,
            read_data['weights'],
            read_data['influences'],
            set_by_api=True,
            undoable=False
        )

        # ダミーオブジェクトからウェイトをコピー
        # closestcomponent
        if method == 'closestcomponent':
            cmds.copySkinWeights(ss=dmy_skincluster, ds=skincluster,
                                 noMirror=True,
                                 influenceAssociation=('oneToOne', 'name', 'label'),
                                 surfaceAssociation='closestComponent',
                                 noBlendWeight=True,
                                 normalize=True)

        # uv space
        elif method == 'uvspace':
            current_uv_set = cmds.polyUVSet(object_name, q=True, currentUVSet=True)[0]
            dmy_uv_set = 'map1'
            if current_uv_set in geometry_data.get('uvValues', {}).keys():
                dmy_uv_set = current_uv_set

            cmds.copySkinWeights(ss=dmy_skincluster, ds=skincluster,
                                 noMirror=True,
                                 influenceAssociation=('oneToOne', 'name', 'label'),
                                 surfaceAssociation='closestPoint',
                                 uvSpace=[dmy_uv_set, current_uv_set],
                                 noBlendWeight=True,
                                 normalize=True)

        # closestpoint
        else:
            cmds.copySkinWeights(ss=dmy_skincluster, ds=skincluster,
                                 noMirror=True,
                                 influenceAssociation=('oneToOne', 'name', 'label'),
                                 surfaceAssociation='closestPoint',
                                 noBlendWeight=True,
                                 normalize=True)

        # ウェイトコピー用ダミーオブジェクトを削除
        cmds.delete(dmy)

    return True


def read_weights_data(file_path):
    """ウェイトデータの読み込み
    :param str file_path: ファイルパス
    :return: ウェイトデータの辞書
    :rtype: dict
    """

    if not os.path.isfile(file_path):
        logger.warning('{} is not found.'.format(file_path))
        return {}

    reader = SkinWeightFile(file_path)
    read_data = reader.read()

    if not read_data:
        return {}

    if read_data.get('file_information', {}).get('data_type', '') != 'skinWeight':
        return {}

    return read_data


def select_geometry_from_data(file_path):
    """ウェイトデータに記載されているジオメトリを選択
    :param str file_path: ファイルパス
    """

    read_data = read_weights_data(file_path)
    if not read_data:
        return

    geometry = read_data.get('geometry', '')
    if not cmds.objExists(geometry):
        logger.warning('{} is not found.'.format(geometry))
        return

    cmds.select(geometry, r=True)


def select_influences_from_data(file_path):
    """ウェイトデータに記載されているインフルエンスを選択
    :param str file_path: ファイルパス
    """

    read_data = read_weights_data(file_path)
    if not read_data:
        return

    infls = read_data.get('influences', [])
    not_found_influences = [inf for inf in infls if not cmds.objExists(inf)]
    if not_found_influences:
        logger.warning('{} is not found.'.format(not_found_influences))
        return

    cmds.select(infls, r=True)


def restore_mesh_from_data(file_path):
    """
    :param str file_path: ファイルパス
    """

    read_data = read_weights_data(file_path)
    if not read_data:
        return

    restore_mesh = create_mesh('restore__{}'.format(read_data['geometry']), read_data['geometry_data'])
    return restore_mesh


def get_mesh_data(node, **kwargs):
    """meshデータの取得
    :param str node: ノード名
    :keyword bool use_py_object: 取得データをpythonObjectで返すかのブール
    :return: メッシュ情報の辞書
    :rtype: dict
    """

    use_py_object = kwargs.get('use_py_object', True)

    dag_path = get_MDagPath2(node)
    mesh_fn = OpenMaya2.MFnMesh(dag_path)

    num_vertices = mesh_fn.numVertices
    num_polygons = mesh_fn.numPolygons
    vertex_array = mesh_fn.getPoints()
    vertexCount, vertexList = mesh_fn.getVertices()

    uv_values = {}
    uv_names = mesh_fn.getUVSetNames()
    for uv_name in uv_names:
        u_values, v_values = mesh_fn.getUVs(uv_name)
        uv_counts, uv_ids = mesh_fn.getAssignedUVs(uv_name)
        if use_py_object:
            u_values = [v for v in u_values]
            v_values = [v for v in v_values]
            uv_counts = [v for v in uv_counts]
            uv_ids = [v for v in uv_ids]

        uv_values[uv_name] = [
            u_values, v_values,
            uv_counts, uv_ids,
        ]

    if use_py_object:
        return {
            'objectType': 'mesh',
            'numVertices': num_vertices,
            'numPolygons': num_polygons,
            'vertexArray': [list(v) for v in vertex_array],
            'polygonCounts': [v for v in vertexCount],
            'polygonConnects': [v for v in vertexList],
            'uvValues': uv_values,
        }

    else:
        return {
            'objectType': 'mesh',
            'numVertices': num_vertices,
            'numPolygons': num_polygons,
            'vertexArray': vertex_array,
            'polygonCounts': vertexCount,
            'polygonConnects': vertexList,
            'uvValues': uv_values,
        }


def create_mesh(node_name, data, **kwargs):
    """meshデータを元にmeshノードを作成
    :param str node_name: 作成ノード名
    :param dict data: meshデータ
    :keyword bool use_py_object: 取得データをpythonObjectで返すかのブール
    :return: 作成ノード名
    :rtype: str
    """

    use_py_object = kwargs.get('use_py_object', True)

    if not data:
        return

    if data['objectType'] != 'mesh':
        return

    transform = cmds.createNode('transform', n=node_name, ss=True)
    mesh = cmds.createNode('mesh', n='{}Shape'.format(transform), ss=True, p=transform)

    if use_py_object:
        vertexArray = OpenMaya2.MPointArray()
        [vertexArray.append(OpenMaya2.MPoint(point)) for point in data['vertexArray']]
    else:
        vertexArray = data['vertexArray']
    polygonCounts = data['polygonCounts']
    polygonConnects = data['polygonConnects']
    uv_data = data['uvValues']

    mesh_fn = OpenMaya2.MFnMesh()
    mesh_fn.create(vertexArray, polygonCounts, polygonConnects, parent=get_MObject2(transform))
    for key, values in uv_data.items():
        if key != 'map1':
            mesh_fn.createUVSet(key)
        mesh_fn.setUVs(values[0], values[1], key)
        mesh_fn.assignUVs(values[2], values[3], key)

    dmy_mesh = OpenMaya2.MFnDependencyNode(mesh_fn.object()).name()
    cmds.connectAttr(
        '{}.o'.format(dmy_mesh),
        '{}.i'.format(mesh),
        f=True
    )
    cmds.dgdirty('{}.o'.format(mesh))
    cmds.dgeval('{}.o'.format(mesh))
    cmds.delete(dmy_mesh)

    return transform


@keep_selections
def bind_and_copy(src, dst, src_components=None, dst_components=None, bind=True, method='closestpoint'):
    """Smooth bind と copy weight を実行
    :param str src: ソースジオメトリ名
    :param str dst: デスティネーションジオメトリ名
    :param list src_components: ソースコンポーネント
    :param list dst_components: デスティネーションジコンポーネント
    :param bool bind: bind処理の実行有無 (False の場合は copy weightsのみの実行)
    :param str method: コピー方法 'closestpoint' or 'closestcomponent' or 'uvspace'
    """

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
    if method not in ['index', 'closestpoint', 'closestcomponent', 'uvspace']:
        logger.warning('{} is Invalid import method.'.format(method))
        return

    if method == 'index':
        if get_component_count(['{}.cp[*]'.format(src)]) != get_component_count(['{}.cp[*]'.format(dst)]):
            logger.warning('{} and {} components count missmatch.'.format(src, dst))
            return

    elif method == 'uvspace':
        src_shapes = list_shapes(src)
        src_shape_type = cmds.objectType(src_shapes[0])

        dst_shapes = list_shapes(dst)
        dst_shape_type = cmds.objectType(dst_shapes[0])
        if src_shape_type != 'mesh' or dst_shape_type != 'mesh':
            logger.warning('Import method \'uvspace\' is mesh-only method.')
            return

    src_influenceIndexList, src_influenceList = list_influences(src_clst, as_object=False, long_name=False)

    if not bind:
        if dst_clst:
            dst_clst = dst_clst[0]
            dst_influenceIndexList, dst_influenceList = list_influences(dst_clst, as_object=False, long_name=False)
            add_joints = [joint for joint in src_influenceList if joint not in dst_influenceList]
            if add_joints:
                OpenMaya.MGlobal.displayInfo(
                    '[ Add influences ] : {} is uncontain influences in \'{}\''.format(add_joints, dst_clst))
                cmds.skinCluster(dst_clst, e=True, dr=4, lw=True, wt=0.0, addInfluence=add_joints)

    else:
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

    if src_components:
        src_components = get_object_filtered_components(src, src_components)

    if dst_components:
        dst_components = get_object_filtered_components(dst, dst_components)

    with WaitCursorBlock():
        if method == 'index':
            weights, infls, infl_indices = get_skinCluster_weights(src)
            if dst_components:
                set_skinCluster_weights(dst, weights, infls, set_by_api=True, undoable=True, comps=dst_components)
            else:
                set_skinCluster_weights(dst, weights, infls, set_by_api=True, undoable=True)

        else:
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
                copy_skinweight_options = {
                    'ss': src_clst,
                    'ds': dst_clst
                }

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
