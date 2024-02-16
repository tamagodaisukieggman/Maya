# -*- coding: utf-8 -*-
import maya.cmds as cmds

SOURCE_ATTR_CONVERT_INFO = {
    'color': {
        'default': {
            'org_connection_attr': None,
            'tgt_connection_attrs': [
                'baseColor'
            ]
        }
    },
    'transparency': {
        'outTransparency': {
            'org_connection_attr': 'outAlpha',
            'tgt_connection_attrs': [
                'opacityR',
                'opacityG',
                'opacityB'
            ]
        },
        'default': {
            'org_connection_attr': None,
            'tgt_connection_attrs': [
                'opacity'
            ]
        }
    },
}


def replace_lambert_to_standard_surface():
    """lambertシェーダーをStandardSurfaceシェーダーに置き換える
    """

    # lambertマテリアル検索
    lambert_materials = [lambert_mat for lambert_mat in cmds.ls(type='lambert')]

    for lambert_material in lambert_materials:

        # Lambertへの接続元(テクスチャやNode等)の接続プラグ名
        material_src_connections = cmds.listConnections(lambert_material, d=False, p=True) or []
        # Lambertからの接続先(ShadingEngine等)の接続プラグ
        material_dst_connections = cmds.listConnections(lambert_material, s=False, p=True) or []

        # 乗せ換えるマテリアル
        standard_surface_material = None
        # lambert1は乗せ換え対象がStandardSurfaceの為、新規マテリアルを作成せずに載せ替え対象をstandardSurface1に設定
        if lambert_material == 'lambert1':
            standard_surface_material = 'standardSurface1'
        # それ以外の場合はここまで来た時点で接続先があるので、StandardSurfaceマテリアルを作成
        else:
            standard_surface_material = create_standard_surface_material()

        # lambertマテリアルの接続元(Source)とStandardSurfaceシェーダーの繋ぎ直し
        reconnect_lambert_material_src_to_standard_surface(material_src_connections, lambert_material, standard_surface_material)

        # lambertマテリアルの接続先(distribute)とStandardSurfaceシェーダーの繋ぎ直し
        reconnect_lambert_material_dst_to_standard_surface(material_dst_connections, standard_surface_material)

        # lambert1は削除/リネームしない
        if lambert_material == 'lambert1':
            continue

        # materialを削除
        cmds.delete(lambert_material)

        # materialをリネーム
        cmds.rename(standard_surface_material, lambert_material)

    # light intensityの値を3.14に
    cmds.setAttr('hardwareRenderingGlobals.defaultLightIntensity', 3.140)

    # initialShadingGroupとinitialParticleSEの接続先をstandardSurfaceに強制的に切り替え
    replace_initial_node()


def reconnect_lambert_material_src_to_standard_surface(material_src_connections, lambert_material, standard_surface_material):
    """lambertマテリアルの接続元(Source)とStandardSurfaceシェーダーの繋ぎ直し

    Args:
        material_src_connections ([str]): lambertマテリアルの接続元プラグ名リスト
        lambert_material (str): lambertマテリアル名
        standard_surface_material (str): StandardSurface名
    """
    for material_src_connection in material_src_connections:

        # ソースからの接続先(=Material)の接続名
        dst_connections = cmds.connectionInfo(material_src_connection, destinationFromSource=True)

        for dst_connection in dst_connections:
            org_connection = material_src_connection
            src_name, src_attr = org_connection.split('.')
            tgt_connections = []
            tgt_name, tgt_attr = dst_connection.split('.')

            # 接続先がlambertマテリアルじゃなければ何もしない
            if tgt_name != lambert_material:
                continue

            tgt_connections = []

            src_convert_info = SOURCE_ATTR_CONVERT_INFO.get(tgt_attr)
            if not src_convert_info:
                continue

            dst_convert_info = src_convert_info.get(src_attr) or src_convert_info.get('default')
            if not dst_convert_info:
                continue

            org_connection_attr = dst_convert_info.get('org_connection_attr')
            tgt_connection_attrs = dst_convert_info.get('tgt_connection_attrs')
            if org_connection_attr:
                org_connection = '{}.{}'.format(src_name, org_connection_attr)

            for tgt_connection_attr in tgt_connection_attrs:
                tgt_connections.append('{}.{}'.format(standard_surface_material, tgt_connection_attr))

            for tgt_connection in tgt_connections:
                cmds.connectAttr(org_connection, tgt_connection, f=True)


def reconnect_lambert_material_dst_to_standard_surface(material_dst_connections, standard_surface_material):
    """lambertマテリアルの接続先(distribute)とStandardSurfaceシェーダーの繋ぎ直し

    Args:
        mat_dst_connexes ([str]): lambertマテリアルの接続先プラグ名リスト
        standard_surface_material (str): StandardSurface名
    """

    material_attr = cmds.listAttr(standard_surface_material)

    for material_dst_connection in material_dst_connections:

        src_connection = cmds.connectionInfo(material_dst_connection, sourceFromDestination=True)
        src_attr = src_connection.split('.')[1]

        # 存在しないアトリビュートを接続しようとするとエラーになるので、事前チェックする
        if src_attr not in material_attr:
            continue

        cmds.connectAttr('{}.{}'.format(standard_surface_material, src_attr), material_dst_connection, f=True)


def replace_initial_node():
    """initialShadingGroupとinitialParticleSEの接続先をstandardSurface1に置き換え
    """
    cmds.connectAttr('standardSurface1.outColor', 'initialShadingGroup.surfaceShader', f=True)
    cmds.connectAttr('standardSurface1.outColor', 'initialParticleSE.surfaceShader', f=True)


def create_standard_surface_material():
    """standardSurfaceマテリアルを作成する

    Returns:
        str: standardSurfaceマテリアル
    """
    standard_surface_material = cmds.shadingNode('standardSurface', asShader=True)
    cmds.setAttr('{}.specular'.format(standard_surface_material), 0.0)

    return standard_surface_material
