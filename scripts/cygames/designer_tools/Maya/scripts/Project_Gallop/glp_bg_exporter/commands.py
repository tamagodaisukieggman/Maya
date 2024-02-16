# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function

try:
    # Maya 2022-
    from importlib import reload
except Exception:
    pass

import os
import re
from logging import getLogger

from maya import cmds
from maya import mel
import maya.OpenMaya as om

from . import constants
from . import export_model
from . import outline_process

reload(constants)
reload(export_model)
reload(outline_process)

logger = getLogger(__name__)


def get_tool_name():
    return '{0}_Ver_{1}'.format(constants.TOOL_NAME, constants.TOOL_VERSION)


def get_setting_locator_name():
    return '|{}|{}'.format(constants.SETTING_LOCATOR_NAME, get_tool_name())


def open_url(url):

    # エラー対策として変換した文字を元に戻す
    url = url.replace('~percent~', '%')

    # Webページを開く
    cmds.showHelp(url, absolute=1)


def open_explorer(mode, path):

    # 対象のパス
    target_path = ''

    if mode == '':
        target_path = path
    else:
        if mode == 'maya_setting':
            target_path = os.environ.get('MAYA_APP_DIR')
        elif mode == 'maya_project':
            target_path = cmds.workspace(q=True, fullName=True)
        elif mode == 'maya_scene':
            target_path = cmds.file(q=True, sceneName=True)

    target_path = target_path.replace('/', '\\')

    if os.path.isfile(target_path) or os.path.isdir(target_path):

        # Windowsエクスプローラーを開く
        print('path : ' + target_path)

        if os.path.isdir(target_path):
            os.popen('explorer {}'.format(target_path))
        elif os.path.isfile(target_path):
            os.popen('explorer /select,{}'.format(target_path))
    else:
        message = '● 指定のパスが存在しません。'
        message += '\n'
        message += '   ' + '「' + target_path + '」'
        cmds.confirmDialog(title='Open Explorer', message=message)


def check_plugin():
    """必要なプラグインの状態をチェックする
    """

    plugin_names = ['fbxmaya', 'objExport']

    plugin_folder_paths = mel.eval('getenv MAYA_PLUG_IN_PATH').split(';')

    # {プラグイン名:パスのリスト}
    plugin_name_paths = {}

    for plugin_folder_path in plugin_folder_paths:
        if os.path.isdir(plugin_folder_path):
            files = os.listdir(plugin_folder_path)
            for plugin_name in plugin_names:
                if (plugin_name + '.mll') in files:
                    if plugin_name not in plugin_name_paths:
                        plugin_name_paths[plugin_name] = []
                    plugin_name_paths[plugin_name].append(plugin_folder_path + '/' + plugin_name + '.mll')

    for plugin_name in plugin_names:
        if plugin_name in plugin_name_paths:
            if len(plugin_name_paths[plugin_name]) == 1:
                plugin_path = plugin_name_paths[plugin_name][0]

                # ロードされていない場合はロードする
                if cmds.pluginInfo(plugin_name, q=True, loaded=True) == 0:
                    cmds.loadPlugin(plugin_path)
                if cmds.pluginInfo(plugin_name, q=True, autoload=True) == 0:
                    cmds.pluginInfo(plugin_path, e=True, autoload=True)


def export_all(export_info):
    """モデルをまとめてエクスポート

    Args:
        export_info (dict[str, Any]): export対象の情報(辞書型)
    """

    selected = cmds.ls(sl=True)

    nodes = export_info['exportNodes']
    node_name_to_dst_folder_path = export_info['exportNodeName_dstFolderPath']
    file_type = export_info['fileType']
    make_dirs_flg = export_info['makedirsFlg']

    for node in nodes:

        # サイリウム/モブの場合は特殊処理を行う
        is_mob_cyalume = _is_mob_or_cyalume(node)

        # 特殊事前処理
        if is_mob_cyalume:
            node, original_node = _mob_cyalume_export_unique_pre_process(node)

        # モデルをエクスポート
        export_one(node, node_name_to_dst_folder_path[node], file_type, make_dirs_flg)

        # 特殊後処理
        if is_mob_cyalume:
            _mob_cyalume_export_unique_post_process(node, original_node)

    cmds.select(selected)
    cmds.confirmDialog(title=get_tool_name(), message='● エクスポート完了！')


def export_one(node, dst_folder_path, file_type, make_dirs_flg=False):
    """モデルをエクスポート

    Args:
        node (str): 対象ノード名
        dst_folder_path (str): 出力フォルダパス
        file_type (str): ファイルタイプ
        make_dirs_flg (bool): ディレクトリ作成フラグ
    """

    # エクスポート用のノード名
    export_name = node.split('|')[-1].split('__')[0]
    long_export_name = '|'.join(node.split('|')[:-1] + [export_name])

    # シーン内に既に同名のノードが存在する場合は、既存ノードを一時リネーム
    existing_node = None
    if cmds.objExists(long_export_name):
        existing_node = cmds.rename(long_export_name, export_name + constants.TEMP_NODE_SUFFIX)
        existing_node = cmds.ls(existing_node, long=True)[0]

        if long_export_name == node:
            node = existing_node

    # エクスポート用のモデルを作成(1データ)
    result_info = export_model.create_one(node, 'export')

    export_node = result_info['topNode']

    # ライト系特殊処理
    _light_export_unique_pre_process(export_node)

    cmds.select(export_node)

    # Toon-Propの場合の特殊処理
    normal_prepare = outline_process.OutlineProcess()
    normal_prepare.initialize(export_node)
    if normal_prepare.is_ready:
        normal_prepare.outline_transfer_to_original()

    # ファイルパス
    if make_dirs_flg:
        if not os.path.exists(dst_folder_path):
            os.makedirs(dst_folder_path)
    export_file_path = dst_folder_path + '/' + export_name + '.' + file_type

    # エクスポート
    cmds.select(export_node, hi=True)

    if file_type == 'ma':
        cmds.file(export_file_path, force=1, exportSelected=1, type='mayaAscii', options='v=0;', preserveReferences=1)
    elif file_type == 'mb':
        cmds.file(export_file_path, force=1, exportSelected=1, type='mayaBinary', options='v=0;', preserveReferences=1)
    elif file_type == 'fbx':
        fbx_export_selection(export_file_path, False)
    elif file_type == 'obj':
        cmds.file(export_file_path, force=1, exportSelected=1, type='OBJexport', options='groups=1;ptgroups=1;materials=1;smoothing=1;normals=1', preserveReferences=1)

    # エクスポート専用ノードを削除
    if cmds.objExists(export_node):
        cmds.delete(export_node)

    # 一時リネームした既存ノードの名前を元に戻す
    if existing_node is not None:
        cmds.rename(existing_node, export_name)


def fbx_export_selection(path, is_ascii=False):
    """選択項目を出力

    Args:
        path (str): 出力パス
        is_ascii (bool, optional): アスキーで出力するか. Defaults to False.

    Returns:
        str: 出力パス
    """

    if not cmds.pluginInfo('fbxmaya', query=True, loaded=True):
        cmds.loadPlugin('fbxmaya.mll')

    mel.eval('FBXResetExport')

    mel.eval('FBXExportAnimationOnly -v false ;')

    mel.eval('FBXExportCameras -v false ;')

    mel.eval('FBXExportLights -v false ;')

    mel.eval('FBXExportInputConnections  -v false ;')

    mel.eval('FBXExportFileVersion -v FBX201300 ;')

    if is_ascii:
        mel.eval('FBXExportInAscii -v true ;')
    else:
        mel.eval('FBXExportInAscii -v false ;')

    return cmds.FBXExport('-f', path, '-s', True)


def _is_mob_or_cyalume(node):
    """ノードがサイリウム/モブの命名規則に則しているかをチェック

    Args:
        node (str): 対象ノード名
    """

    short_name = node.split('|')[-1]

    # 「md_stg_cyalume_」もしくは「md_stg_mob_」（旧命名規則）
    # 「md_stg_****_cyalume_」もしくは「md_stg_****_mob_」（新命名規則）
    match_obj = constants.REGEX_MOB_CYALUME_ROOT.match(short_name)
    if not match_obj:
        return False

    return True


def _mob_cyalume_export_unique_pre_process(node):
    """mobとcyalume特殊エクスポートの前処理

    Args:
        node (str): 対象ノード名

    Returns:
        str: 処理後のノード名
    """

    short_name = node.split('|')[-1]

    # 複製した後、元のノードの名前を一旦リネーム
    duplicated_node = cmds.duplicate(node)[0]
    original_node = cmds.rename(node, 'tmp_' + short_name)
    original_node = cmds.ls(original_node, long=True)[0]
    duplicated_node = cmds.rename(duplicated_node, short_name)
    duplicated_node = cmds.ls(duplicated_node, long=True)[0]

    # Memo : stageより1階層深くなる
    child_nodes = cmds.listRelatives(duplicated_node, f=True, type='transform')

    if child_nodes:

        for child_node in child_nodes:

            is_conbine = False

            mesh_nodes = cmds.listRelatives(child_node, f=True, type='mesh')

            # メッシュ
            if mesh_nodes and len(mesh_nodes) == 1:

                _add_position_and_groupnum_param(child_node)
                continue

            else:

                gorup_child_nodes = cmds.listRelatives(child_node, f=True, type='transform')

                if not gorup_child_nodes:
                    cmds.delete(child_node)
                    continue

                for group_child_node in gorup_child_nodes:
                    group_child_mesh_nodes = cmds.listRelatives(group_child_node, f=True, type='mesh')
                    # TODO: グループノードだが中に入っているのがメッシュで無い場合は削除する 扱い要調整
                    if not group_child_mesh_nodes:
                        cmds.delete(child_node)
                        continue

                    result = _add_position_and_groupnum_param(group_child_node)
                    if result:
                        is_conbine = True

            # ひとつでもグループノードを処理した場合はメッシュを結合(=1メッシュ化)
            if is_conbine:
                _combine_mesh(child_node)

    return duplicated_node, original_node


def _mob_cyalume_export_unique_post_process(node, original_node):
    """mobとcyalume特殊エクスポートの後処理

    Args:
        node (str): 対象ノード名
    """

    short_name = node.split('|')[-1]

    cmds.delete(node)

    if cmds.objExists(original_node):
        cmds.rename(original_node, short_name)


def _add_position_and_groupnum_param(target_node):
    """UVにオフセットとグループ番号を書き込む

    Args:
        target_node (str): 対象ノード名
    """

    # 空だったら削除して次
    child_mesh_nodes = cmds.listRelatives(target_node, ad=True, type='mesh', f=True)
    if not child_mesh_nodes:
        logger.warning('メッシュが存在しないグループのため削除しました : {0}'.format(target_node))
        cmds.delete(target_node)
        return False

    # UVが規定，もしくはUVを含まない場合も削除
    uv_set_list = cmds.polyUVSet(target_node, q=True, allUVSets=True)
    if uv_set_list is None or 'map1' not in uv_set_list:
        logger.warning('UVが存在しない、またはmap1が存在しないため削除しました : {0}'.format(target_node))
        cmds.delete(target_node)
        return False

    is_group = False

    child_node_short_name = target_node.split('|')[-1]
    match_obj = constants.REGEX_MOB_CYALUME_GROUP.match(child_node_short_name)
    if match_obj:
        is_group = True

    # 入れ子のグループノードだった場合メッシュを結合
    _combine_mesh(target_node)

    # UVが規定，もしくはUVを含まない場合も削除
    uv_set_list = cmds.polyUVSet(target_node, q=True, allUVSets=True)
    if uv_set_list is None or 'map1' not in uv_set_list:
        return False

    # UVが1以上の場合「map1」以外は削除
    if len(uv_set_list) > 1:
        logger.warning('サイリウム/モブに「map1」以外のUVSetが使用されています．\n書き出しのために「map1」以外のUVSetを削除します． : {0}'.format(target_node))
        for uv_set in uv_set_list:
            if uv_set == 'map1':
                continue
            cmds.polyUVSet(target_node, delete=True, uvSet=uv_set)

    # オフセット値のリストを作成
    shell_center_position_list = []
    shell_maps_list, shell_faces_list = _get_shell_param_list(target_node)
    for shellfaces in shell_faces_list:
        center_position = [0, 0, 0]
        bounding_box = cmds.xform(shellfaces, q=True, boundingBox=True)
        for i in range(len(center_position)):
            tmp_value = bounding_box[3 + i] + bounding_box[0 + i]
            if tmp_value != 0:
                # Unityでは値がメートル、mayaはセンチメートルなので値を合わせるために100で割る
                center_position[i] = tmp_value / 2 / 100
        shell_center_position_list.append(center_position)

    group_num = 0
    # groupNumが指定されていなければ末尾の2文字からグループIDを取得
    if is_group:
        group_num = int(child_node_short_name[-2:])

    # UV2に「オフセット値X」「オフセット値Y」を流し込む
    uv2 = cmds.polyUVSet(target_node, copy=True, uvSet='map1')[0]
    # NOTE:選択しないとうまくcurrentUVSetの変更ができない
    cmds.select(target_node)
    cmds.polyUVSet(currentUVSet=True, uvSet=uv2)
    for i in range(len(shell_center_position_list)):
        shell_center_position = shell_center_position_list[i]
        shell_maps = shell_maps_list[i]
        for shell_map in shell_maps:
            # NOTE:unity側の座標軸とmayaの座標軸が異なるので、xに-1を掛ける
            cmds.polyEditUV(shell_map, u=shell_center_position[0] * -1, v=shell_center_position[1], r=False)

    # UV3に「オフセット値のZ」「グループ番号」を流し込む
    uv3 = cmds.polyUVSet(target_node, copy=True, uvSet='map1')[0]
    # 選択しないとうまくcurrentUVSetの変更ができない
    cmds.select(target_node)
    cmds.polyUVSet(currentUVSet=True, uvSet=uv3)
    for i in range(len(shell_center_position_list)):
        shell_center_position = shell_center_position_list[i]
        shell_maps = shell_maps_list[i]
        for shell_map in shell_maps:
            # unity側の座標軸とmayaの座標軸が異なるので、xに-1を掛ける
            cmds.polyEditUV(shell_map, u=shell_center_position[2], v=group_num, r=False)

    cmds.select(cl=True)

    return True


def _combine_mesh(node):
    """ノード以下のメッシュを全て結合し、1メッシュのノードとして返します。

    Args:
        node (str): 対象ノード名

    Returns:
        str: 結合後のノード名
    """

    short_name = node.split('|')[-1]

    parent_nodes = cmds.listRelatives(node, parent=True, fullPath=True)
    parent_node = parent_nodes[0] if parent_nodes else None

    shapes = cmds.listRelatives(node, allDescendents=True, fullPath=True, type='mesh')

    if not shapes:
        return None

    mesh_node = None

    # 1メッシュの場合はメッシュノードを一旦ワールドに出す
    if len(shapes) == 1:
        mesh = shapes[0]
        mesh_node = cmds.listRelatives(mesh, parent=True, fullPath=True)[0]
        mesh_parent_nodes = cmds.listRelatives(mesh_node, parent=True, fullPath=True)
        if mesh_parent_nodes:
            parented_node = cmds.parent(mesh_node, world=True)
            mesh_node = cmds.ls(parented_node, long=True)[0]

    # 複数メッシュの場合はメッシュをコンバイン（自動でワールドに出る）
    elif len(shapes) > 1:
        united_node, _ = cmds.polyUnite(node)
        mesh_node = cmds.ls(united_node, long=True)[0]

    # メッシュノードの親を元に戻す
    if parent_node:
        parented_node = cmds.parent(mesh_node, parent_node)
        mesh_node = cmds.ls(parented_node, long=True)[0]

    # メッシュのヒストリを削除
    cmds.select(mesh_node)
    mel.eval('doBakeNonDefHistory( 1, {"prePost" });')
    cmds.select(cl=True)

    # ヒストリ削除後もグループノードが残っていた場合削除
    # NOTE: 何故かコピー元のノードが消えるパターンがあったため，DAGパス経由で消しています
    if cmds.objExists(node) and node != mesh_node:
        cmds.delete(node)

    # メッシュノードの名前を元に戻す
    renamed_node = cmds.rename(mesh_node, short_name)
    mesh_node = cmds.ls(renamed_node, long=True)[0]

    return mesh_node


def _get_shell_param_list(name):
    """meshからシェル毎のフェースとuvの一覧を取得する

    Args:
        name (str): メッシュ名
    """

    sel_list = om.MSelectionList()
    sel_list.add(name)
    sel_list_iter = om.MItSelectionList(sel_list, om.MFn.kMesh)
    path_to_shape = om.MDagPath()
    sel_list_iter.getDagPath(path_to_shape)

    shape_fn = om.MFnMesh(path_to_shape)
    shells = om.MScriptUtil()
    shells.createFromInt(0)
    nb_uv_shells = shells.asUintPtr()

    u_array = om.MFloatArray()  # array for U coords
    v_array = om.MFloatArray()  # array for V coords
    uv_shell_ids = om.MIntArray()  # The container for the uv shell Ids

    shape_fn.getUVs(u_array, v_array)
    shape_fn.getUvShellsIds(uv_shell_ids, nb_uv_shells, 'map1')

    shells = {}
    for i, n in enumerate(uv_shell_ids):

        if n in shells:
            shells[n].append(i)
        else:
            shells[n] = [i]

    shell_maps_list = []
    shell_faces_list = []
    for idx in shells:

        shell_ids = shells[idx]
        maps = ['{0}.map[{1}]'.format(name, shell_id) for shell_id in shell_ids]
        faces = cmds.polyListComponentConversion(maps, fuv=True, tf=True)
        shell_maps_list.append(maps)
        shell_faces_list.append(faces)

    return shell_maps_list, shell_faces_list


def _light_export_unique_pre_process(node):
    """ライト特殊処理 単一メッシュの場合は入らない

    Args:
        node (str): 対象ノード名
    """

    pattern = r'^light00([0-9])_'

    light_transform_param_list = []

    child_node_list = cmds.listRelatives(node, ad=True, pa=True, f=True, type='transform')

    if child_node_list:

        for child_node in child_node_list:

            mesh = cmds.listRelatives(child_node, type='mesh')

            if not mesh:
                continue

            search_obj = re.search(pattern, child_node.split('|')[-1])

            if search_obj:
                group_str = search_obj.group(1)
                group_num = int(group_str)
                light_transform_param_list.append(
                    {
                        'node_name': child_node,
                        'group_index': group_num,
                    })

    for light_transform_param in light_transform_param_list:

        child_node = light_transform_param['node_name']
        group_index = light_transform_param['group_index']

        uv_set_list = cmds.polyUVSet(child_node, q=True, allUVSets=True)
        if 'map1' not in uv_set_list:
            continue

        # map1以外のuvSetは削除する
        for uv_set in uv_set_list:
            if uv_set == 'map1':
                continue

            cmds.polyUVSet(child_node, e=True, uvSet=uv_set, delete=True)

        uv2 = cmds.polyUVSet(child_node, copy=True, uvSet='map1', newUVSet='uvSet1')[0]
        cmds.select(child_node)
        cmds.polyUVSet(currentUVSet=True, uvSet=uv2)
        node_maps = cmds.ls(child_node + '.map[*]', fl=True)

        cmds.polyEditUV(node_maps, u=group_index, v=0, r=False)


def is_normal_process_target(base_node):
    """法線ベイクの対象か

    Args:
        base_node (str): 対象ノード名

    Returns:
        bool: 法線ベイクの対象か
    """
    return outline_process.OutlineProcess.is_outline_process_target(base_node)